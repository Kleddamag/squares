"""Finite provenance, geometry and failed-query controls for fixed-sample ablation."""

from __future__ import annotations

import copy
import time
from typing import Any

import pytest

from devtools import bounded_diagnostics
from devtools import probe_n17_core_refinement as refinement
from devtools import probe_n17_full_core_ablation as probe
from devtools.check_hull_kernel_mask0 import n17_unique_frame
from devtools.probe_n17_core_refinement import Child
from devtools.probe_n17_residual_graph import Atom
from sqpack.hull_kernel.geometry import Budget, IncompleteError, RefusalError
from sqpack.hull_kernel.rational import Q


@pytest.fixture(autouse=True)
def isolated_memory(monkeypatch: pytest.MonkeyPatch) -> None:
    # Shared pytest process peaks are not a standalone protocol's resource sample.
    monkeypatch.setattr(bounded_diagnostics, "current_memory_bytes", lambda: 0)
    # Reused H.children has the same standalone guard; isolate its sampler too.
    monkeypatch.setattr(refinement, "peak_memory_bytes", lambda: 0)


def budget() -> Budget:
    return Budget(time.monotonic() + 10, probe.MAX_PAIRS)


def square(size: Q) -> list[tuple[Q, Q]]:
    return [(-size, -size), (size, -size), (size, size), (-size, size)]


@pytest.fixture
def context() -> probe.Context:
    old = square(Q(1, 4))
    atoms = [
        Atom(owner, 0, (piece,), [(Q(owner), Q(piece))], old)
        for owner, piece in ((1, 0), (1, 1), (2, 0), (3, 0))
    ]
    document = {
        "final_state": {
            "cells": {
                str(owner): [
                    {
                        "interval": ["0", "1/16"],
                        "reference": {"kind": "phase3", "row": 0, "step": owner},
                    }
                ]
                for owner in (1, 2, 3)
            }
        }
    }
    return probe.Context(
        n17_unique_frame(),
        atoms,
        document,
        [[0, 2, 3], [1, 2, 3]],
        {1},
        {0},
        {
            "schema": probe.SCHEMA,
            "live_parent_rows": 3,
            "source_selections": 2,
            "input_identity": {"seed_sha256": "control-seed", "node_sha256": "control-node"},
            "diagnostic_only": True,
            "new_exclusions": 0,
            "unsupported_rows_verified": False,
        },
    )


def finite_predicate(left: Atom, right: Atom, _: Budget) -> bool:
    assert left.owner < right.owner
    return left.owner == 1 and left.pieces == (0,) and right.owner == 2


def finite_geometry(
    context: probe.Context, _: Budget
) -> tuple[list[Atom], list[dict[str, Any]], None]:
    return context.raw, [{"area_gain2": "1"}], None


def test_exact_nesting_catches_asymmetric_vertex() -> None:
    full = square(Q(1))
    assert probe.nesting_failure(full, square(Q(2))) is None
    small = [(Q(-2), Q(-2)), (Q(1, 2), Q(-2)), (Q(1, 2), Q(2)), (Q(-2), Q(2))]
    assert probe.nesting_failure(full, small) == (Q(1), Q(-1))


def test_geometry_preserves_every_domain_piece_and_checks_all_rows(
    context: probe.Context,
) -> None:
    saved = copy.deepcopy(context.raw)
    atoms, rows, _ = probe.geometry(context, budget())
    assert len(atoms) == len(saved)
    assert len(rows) == 3
    assert context.raw == saved
    assert all(
        a.domain == b.domain and a.pieces == b.pieces for a, b in zip(atoms, saved, strict=True)
    )
    assert all(Q(row["full_area2"]) >= Q(row["old_area2"]) for row in rows)
    assert all(Q(row["area_gain2"]) > 0 for row in rows)


def test_nonnesting_retains_witness_and_stops_queries(
    context: probe.Context, monkeypatch: pytest.MonkeyPatch
) -> None:
    failure = {"owner": 2, "row": 0, "half": 1, "vertex": ["1", "0"]}
    monkeypatch.setattr(
        probe, "geometry", lambda *_: (context.raw, [{"area_gain2": "1"}], failure)
    )
    result = probe.analyze(context, budget())
    assert result["status"] == "NESTING_FAILED"
    assert result["nesting_failure"] == failure
    assert result["fresh_pair_checks"] == 0
    assert result["tuple_results"] == []
    assert "full_lost_indices" not in result


def test_zero_growth_is_geometry_only(
    context: probe.Context, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        probe, "geometry", lambda *_: (context.raw, [{"area_gain2": "0"}], None)
    )
    result = probe.analyze(context, budget())
    assert result["status"] == "NO_CORE_GROWTH"
    assert result["fresh_pair_checks"] == 0
    assert "full_lost_indices" not in result


def test_full_loss_witness_and_survival_all_pairs(context: probe.Context) -> None:
    result: dict[str, Any] = {}
    probe.classify(context, context.raw, budget(), result, predicate=finite_predicate)
    assert result["status"] == "PASS_FIXED_SAMPLE_COMPARISON"
    assert result["full_lost_indices"] == [0]
    assert result["full_survivor_indices"] == [1]
    assert result["halving_additional_lost_indices"] == []
    assert result["fixed_classification_equal"] is True
    assert result["fresh_pair_checks"] == 4
    assert result["tuple_results"][0]["first_collision"] == {
        "left_position": 0,
        "right_position": 1,
    }
    assert result["tuple_results"][1]["pair_checks"] == 3
    assert result["observed_supported_parents"] == 3


def test_strict_loss_subset_quantifies_only_fixed_sample(context: probe.Context) -> None:
    result: dict[str, Any] = {}
    probe.classify(context, context.raw, budget(), result, predicate=lambda *_: False)
    assert result["full_lost_indices"] == []
    assert result["halving_additional_lost_indices"] == [0]
    assert result["fixed_classification_equal"] is False
    assert result["fresh_pair_checks"] == 6


def test_monotonic_contradiction_stops_acceptance(context: probe.Context) -> None:
    result: dict[str, Any] = {}
    probe.classify(context, context.raw, budget(), result, predicate=lambda *_: True)
    assert result["status"] == "STOP_SOUNDNESS_INVESTIGATION"
    assert "full_lost_indices" not in result


@pytest.mark.parametrize("bad", [1, 0, None, "unknown"])
def test_nonbool_failed_query_never_commits_tuple(context: probe.Context, bad: Any) -> None:
    result: dict[str, Any] = {}
    with pytest.raises(RefusalError, match="exactbool"):
        probe.classify(context, context.raw, budget(), result, predicate=lambda *_: bad)
    assert result["tuple_results"] == []
    assert result["fresh_pair_checks"] == 1


def test_unexpected_refusal_is_not_false(context: probe.Context) -> None:
    def refuse(*_: Any) -> bool:
        raise RefusalError("unrecognized exact failure")

    result: dict[str, Any] = {}
    with pytest.raises(RefusalError, match="unrecognized"):
        probe.classify(context, context.raw, budget(), result, predicate=refuse)
    assert result["tuple_results"] == []


def test_pair_cap_preserves_only_completed_tuple(
    context: probe.Context, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(probe, "MAX_PAIRS", 1)
    result: dict[str, Any] = {}
    with pytest.raises(IncompleteError, match="pair ceiling"):
        probe.classify(context, context.raw, budget(), result, predicate=finite_predicate)
    assert len(result["tuple_results"]) == 1
    assert result["fresh_pair_checks"] == 1


def test_before_query_time_guard_is_atomic(context: probe.Context) -> None:
    result: dict[str, Any] = {}
    with pytest.raises(IncompleteError, match="wall ceiling"):
        probe.classify(context, context.raw, Budget(0, 0), result, predicate=finite_predicate)
    assert result["fresh_pair_checks"] == 0
    assert result["tuple_results"] == []


def test_after_query_time_guard_omits_failed_answer(
    context: probe.Context, monkeypatch: pytest.MonkeyPatch
) -> None:
    def overrun(*_: Any) -> bool:
        monkeypatch.setattr(probe.time, "monotonic", lambda: float("inf"))
        return False

    result: dict[str, Any] = {}
    with pytest.raises(IncompleteError, match="wall ceiling"):
        probe.classify(context, context.raw, budget(), result, predicate=overrun)
    assert result["fresh_pair_checks"] == 1
    assert result["tuple_results"] == []


def test_peak_threshold_and_postquery_guard(
    context: probe.Context, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        bounded_diagnostics, "current_memory_bytes", lambda: probe.MAX_PEAK_BYTES
    )
    probe.remaining(budget())

    def inflate(*_: Any) -> bool:
        monkeypatch.setattr(
            bounded_diagnostics, "current_memory_bytes", lambda: probe.MAX_PEAK_BYTES + 1
        )
        return False

    result: dict[str, Any] = {}
    with pytest.raises(IncompleteError, match="512 MiB"):
        probe.classify(context, context.raw, budget(), result, predicate=inflate)
    assert result["tuple_results"] == []


def test_owner_order_refuses_before_query(context: probe.Context) -> None:
    context.selections[0].reverse()
    result: dict[str, Any] = {}
    with pytest.raises(RefusalError, match="tuple owners"):
        probe.classify(context, context.raw, budget(), result, predicate=finite_predicate)
    assert result["fresh_pair_checks"] == 0


def test_parent_core_mismatch_refuses(context: probe.Context) -> None:
    context.raw[1] = Atom(1, 0, (1,), context.raw[1].domain, square(Q(1, 5)))
    with pytest.raises(RefusalError):
        probe.geometry(context, budget())


def test_geometry_requires_sample_to_cover_each_parent(
    context: probe.Context, monkeypatch: pytest.MonkeyPatch
) -> None:
    def missing(*_: Any) -> tuple[dict[tuple[int, int], Child], list[Any]]:
        return {}, []

    monkeypatch.setattr(probe, "children", missing)
    with pytest.raises(RefusalError, match="omits a parent"):
        probe.geometry(context, budget())


def test_frozen_packet_identity_refuses_before_geometry(context: probe.Context) -> None:
    with pytest.raises(RefusalError, match="frozen"):
        probe.bind(
            context.frame,
            context.raw,
            context.document,
            {},
            source={},
            baseline={},
            refinement={},
            certificate=None,
            budget=budget(),
            endpoint=False,
        )


def test_replay_is_fresh_and_detects_claim_tampering(
    context: probe.Context, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(probe, "geometry", finite_geometry)
    original = probe.classify
    calls = []

    def finite(*args: Any, **kwargs: Any) -> None:
        def record(left: Atom, right: Atom, guard: Budget) -> bool:
            calls.append((left.owner, right.owner))
            return finite_predicate(left, right, guard)

        original(*args, **kwargs, predicate=record)

    monkeypatch.setattr(probe, "classify", finite)
    value = probe.analyze(context, budget())
    value.update(wall_seconds=1.25, worker_peak_bytes=123)
    calls.clear()
    replay = probe.verify_packet(value, context, budget())
    assert replay["fresh_pair_checks"] == len(calls) == 4
    assert replay["status"] == "PASS_REPLAYED_FIXED_SAMPLE"
    assert replay["packet_content_verified"] is True
    for key, replacement in (
        ("tuple_results", []),
        ("full_lost_indices", []),
        ("observed_supported_parents", 0),
        ("nesting_failure", {}),
    ):
        tampered = {**value, key: replacement}
        with pytest.raises(RefusalError, match="replay differs"):
            probe.verify_packet(tampered, context, budget())


@pytest.mark.parametrize("status", ["INCOMPLETE", "REFUSED", "STOP_SOUNDNESS_INVESTIGATION"])
def test_replay_refuses_incomplete_or_unaccepted_status(
    context: probe.Context, status: str
) -> None:
    with pytest.raises(RefusalError, match="incomplete packet"):
        probe.verify_packet({**context.header, "status": status}, context, budget())


def test_replay_bool_is_not_integer(context: probe.Context) -> None:
    value = {**context.header, "status": "NESTING_FAILED", "unsupported_rows_verified": 0}
    with pytest.raises(RefusalError, match="unsupported_rows_verified"):
        probe.verify_packet(value, context, budget())


def test_no_growth_replay_never_certifies_tuple_classification(
    context: probe.Context, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        probe, "geometry", lambda *_: (context.raw, [{"area_gain2": "0"}], None)
    )
    value = probe.analyze(context, budget())
    replay = probe.verify_packet(value, context, budget())
    assert replay["status"] == "PASS_REPLAYED_GEOMETRY_OBSTRUCTION"
    assert replay["full_lost_indices"] is None
    assert replay["fresh_pair_checks"] == 0
