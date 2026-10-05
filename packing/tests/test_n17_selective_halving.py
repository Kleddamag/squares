"""Independent finite mask algebra and atomic certificate controls."""

from __future__ import annotations

import copy
import time
from typing import Any

import pytest

from devtools import bounded_diagnostics
from devtools import probe_n17_full_core_ablation as full
from devtools import probe_n17_selective_halving as probe
from devtools.check_hull_kernel_mask0 import n17_unique_frame
from devtools.probe_n17_residual_graph import Atom
from sqpack.hull_kernel.geometry import Budget, RefusalError
from sqpack.hull_kernel.rational import Q


@pytest.fixture(autouse=True)
def isolated_memory(monkeypatch: pytest.MonkeyPatch) -> None:
    # Historical peaks of a shared pytest worker are not a standalone protocol sample.
    monkeypatch.setattr(bounded_diagnostics, "current_memory_bytes", lambda: 0)


def budget() -> Budget:
    return Budget(time.monotonic() + 10, probe.MAX_CALLS)


def edge(left: int, right: int, a: int, b: int) -> dict[str, Any]:
    # Explicit assignment enumeration is independent of the implementation's bit algebra.
    masks = [m for m in range(64) if (m // 2**left) % 2 == a and (m // 2**right) % 2 == b]
    return {
        "left_position": left,
        "right_position": right,
        "left_half": a,
        "right_half": b,
        "coverage_hex": hex(sum(2**m for m in masks)),
    }


def test_all_asymmetric_patterns_match_explicit_assignments() -> None:
    for left in range(6):
        for right in range(left + 1, 6):
            for a in (0, 1):
                for b in (0, 1):
                    expected = int(edge(left, right, a, b)["coverage_hex"], 16)
                    assert probe.pattern(left, right, a, b) == expected
                    assert expected.bit_count() == 16
    assert probe.pattern(1, 5, 1, 0) != probe.pattern(1, 5, 0, 1)


@pytest.mark.parametrize("choices", [(None, None), (None, 0), (1, None), (0, 1)])
def test_full_positions_are_wildcards(choices: tuple[int | None, int | None]) -> None:
    a, b = choices
    expected = sum(
        2**m
        for m in range(64)
        if (a is None or (m // 2) % 2 == a) and (b is None or (m // 32) % 2 == b)
    )
    assert probe.coverage(1, 5, a, b) == expected


@pytest.mark.parametrize(
    "args", [(True, 4, 0, 1), (1, 1, 0, 1), (0, 6, 0, 1), (0, 1, False, 1)]
)
def test_bad_pattern_grammar(args: tuple[Any, ...]) -> None:
    with pytest.raises(RefusalError):
        probe.pattern(*args)


def test_bad_full_choice_refuses() -> None:
    with pytest.raises(RefusalError):
        probe.coverage(0, 1, None, False)  # noqa: FBT003 - deliberately malformed choice


def test_all64_costs_eligibility_and_lex_minimum() -> None:
    rows = [(i, 0) for i in range(6)]
    costs = dict.fromkeys(rows, 1)
    edges = [
        edge(left, right, a, b)
        for left, right in ((0, 1), (3, 4))
        for a in (0, 1)
        for b in (0, 1)
    ]
    candidates, chosen = probe.subsets(rows, costs, edges)
    assert [c["subset_mask"] for c in candidates] == list(range(64))
    assert chosen is not None
    assert chosen["selected_rows"] == [[0, 0], [1, 0]]
    assert chosen["extra_atoms"] == 2
    assert candidates[1]["eligible_edge_indices"] == []
    costs[(0, 0)] = 10
    _, weighted = probe.subsets(rows, costs, edges)
    assert weighted is not None
    assert weighted["selected_rows"] == [[3, 0], [4, 0]]
    assert candidates[3]["coverage_hex"] == probe.hex64(probe.FULL)


def test_incomplete_library_is_not_feasible() -> None:
    rows = [(i, 0) for i in range(6)]
    candidates, chosen = probe.subsets(
        rows, dict.fromkeys(rows, 1), [edge(3, 4, a, b) for a, b in ((0, 0), (0, 1), (1, 0))]
    )
    assert chosen is None
    assert not any(c["feasible"] for c in candidates)


@pytest.mark.parametrize("cost", [0, -1, True])
def test_nonpositive_or_bool_cost_refuses(cost: Any) -> None:
    rows = [(i, 0) for i in range(6)]
    costs = dict.fromkeys(rows, 1)
    costs[rows[0]] = cost
    with pytest.raises(RefusalError):
        probe.subsets(rows, costs, [])


def test_forged_library_mask_refuses() -> None:
    rows = [(i, 0) for i in range(6)]
    forged = {**edge(0, 1, 0, 1), "coverage_hex": "0xffffffffffffffff"}
    with pytest.raises(RefusalError, match="mask differs"):
        probe.subsets(rows, dict.fromkeys(rows, 1), [forged])


@pytest.fixture
def bound() -> probe.Bound:
    old = [(Q(-1, 4), Q(-1, 4)), (Q(1, 4), Q(-1, 4)), (Q(1, 4), Q(1, 4)), (Q(-1, 4), Q(1, 4))]
    raw = [
        Atom(owner, row, (0,), [(Q(owner), Q(row))], old)
        for owner in range(6)
        for row in range(10)
    ]
    raw.extend(Atom(owner, 0, (99,), [(Q(owner), Q(99))], old) for owner in range(6))
    selected = {(3, 0), (4, 0)}
    atoms: list[Atom] = []
    refs: list[dict[str, Any]] = []
    lookup: dict[tuple[int, int | None], int] = {}
    for i, atom in enumerate(raw):
        for half in (0, 1) if (atom.owner, atom.row) in selected else (None,):
            lookup[i, half] = len(atoms)
            atoms.append(atom)
            refs.append(
                {
                    "raw_atom_index": i,
                    "owner": atom.owner,
                    "row": atom.row,
                    "piece": atom.pieces[0],
                    "half": half,
                    "kind": "full" if half is None else "half",
                }
            )
    inv = probe.Inventory(atoms, refs, lookup, selected, probe.content_sha256(refs))
    negative = list(range(60, 66))
    selections = [negative[:] for _ in range(79)]
    context = full.Context(n17_unique_frame(), raw, {}, selections, {1}, {0, 58}, {})
    edges = [edge(3, 4, a, b) for a in (0, 1) for b in (0, 1)]
    positives = [
        [
            lookup[owner * 10 + i % 10, 0 if (owner, i % 10) in selected else None]
            for owner in range(6)
        ]
        for i in range(44)
    ]
    d = {
        "full_lost_indices": [0],
        "tuple_results": [{"first_collision": {"left_position": 0, "right_position": 1}}],
    }
    return probe.Bound(
        context,
        inv,
        d,
        {"incompatible_pairs": edges},
        positives,
        [],
        {
            "chosen_J58_edge_indices": list(range(4)),
            "diagnostic_only": True,
            "unsupported_rows_verified": False,
            "input_identity": {"seed_sha256": "control-seed", "node_sha256": "control-node"},
            "selected_parent_rows": [[3, 0], [4, 0]],
            "extra_atoms": 4,
        },
    )


def finite(left: Atom, right: Atom, _: Budget) -> bool:
    assert left.owner < right.owner
    return left.pieces == right.pieces == (99,)


def test_complete_certificates_and_all44_cliques(bound: probe.Bound) -> None:
    result = probe.prove(bound, budget(), predicate=finite)
    assert result["status"] == "PASS_FIXED_CERTIFICATES_PRESERVED"
    assert result["fresh_pair_calls"] == 665
    assert len(result["positive_selections"]) == 44
    assert result["supported_parents"] == 60
    assert result["fixed_E_lost_indices"] == [0, 58]
    assert all(
        c["coverage_hex"] == probe.hex64(probe.FULL) for c in result["negative_certificates"]
    )


@pytest.mark.parametrize("bad", [0, 1, None, "unknown"])
def test_failed_answer_never_commits_certificate(bound: probe.Bound, bad: Any) -> None:
    result = probe.prove(bound, budget(), predicate=lambda *_: bad)
    assert result["status"] == "REFUSED"
    assert result["negative_certificates"] == []
    assert result["positive_selections"] == []
    assert result["fresh_pair_calls"] == 1


def test_unknown_refusal_is_not_false(bound: probe.Bound) -> None:
    def refuse(*_: Any) -> bool:
        raise RefusalError("unrecognized geometric failure")

    result = probe.prove(bound, budget(), predicate=refuse)
    assert result["status"] == "REFUSED"
    assert result["negative_certificates"] == []


def test_cap_retains_only_complete_loss(
    bound: probe.Bound, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(probe, "MAX_CALLS", 2)
    result = probe.prove(bound, budget(), predicate=finite)
    assert result["status"] == "INCOMPLETE"
    assert result["fresh_pair_calls"] == 2
    assert [c["source_E_index"] for c in result["negative_certificates"]] == [0]
    assert result["positive_selections"] == []


def test_partial_clique_is_not_retained(
    bound: probe.Bound, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(probe, "MAX_CALLS", 6)
    result = probe.prove(bound, budget(), predicate=finite)
    assert result["status"] == "INCOMPLETE"
    assert result["positive_selections"] == []
    assert len(result["negative_certificates"]) == 2


def test_pre_and_post_query_wall_guard(
    bound: probe.Bound, monkeypatch: pytest.MonkeyPatch
) -> None:
    assert probe.prove(bound, Budget(0, 0), predicate=finite)["fresh_pair_calls"] == 0

    def overrun(*_: Any) -> bool:
        monkeypatch.setattr(probe.time, "monotonic", lambda: float("inf"))
        return True

    result = probe.prove(bound, budget(), predicate=overrun)
    assert result["status"] == "INCOMPLETE"
    assert result["negative_certificates"] == []
    assert result["fresh_pair_calls"] == 1


def test_peak_threshold_and_failed_post_query(
    bound: probe.Bound, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        bounded_diagnostics, "current_memory_bytes", lambda: probe.MAX_PEAK_BYTES
    )
    probe.remaining(budget())

    def inflate(*_: Any) -> bool:
        monkeypatch.setattr(
            bounded_diagnostics, "current_memory_bytes", lambda: probe.MAX_PEAK_BYTES + 1
        )
        return True

    result = probe.prove(bound, budget(), predicate=inflate)
    assert result["status"] == "INCOMPLETE"
    assert result["negative_certificates"] == []


def test_canonical_owner_direction_refuses_before_call(bound: probe.Bound) -> None:
    calls: list[Any] = []
    guard = probe.Guard(budget(), lambda *args: bool(calls.append(args)))
    with pytest.raises(RefusalError, match="noncanonical"):
        guard.check_pair(bound.inventory.atoms[10], bound.inventory.atoms[0])
    assert guard.calls == 0
    assert not calls


def test_replay_full_identity_fresh_calls_and_strict_tamper(
    bound: probe.Bound, monkeypatch: pytest.MonkeyPatch
) -> None:
    original = probe.prove
    calls: list[tuple[int, int]] = []

    def wrapped(*args: Any, **kwargs: Any) -> dict[str, Any]:
        def record(left: Atom, right: Atom, guard: Budget) -> bool:
            calls.append((left.owner, right.owner))
            return finite(left, right, guard)

        return original(*args, **kwargs, predicate=record)

    monkeypatch.setattr(probe, "prove", wrapped)
    value = wrapped(bound, budget())
    value.update(wall_seconds=1.2, worker_peak_bytes=123)
    calls.clear()
    replay = probe.verify_packet(value, bound, budget())
    assert replay["fresh_pair_calls"] == len(calls) == 665
    assert replay["packet_content_verified"] is True
    for key, replacement in (
        ("positive_selections", []),
        ("negative_certificates", []),
        ("supported_parents", 0),
        ("unsupported_rows_verified", 0),
    ):
        with pytest.raises(RefusalError):
            probe.verify_packet({**value, key: replacement}, bound, budget())
    forged = copy.deepcopy(value)
    forged["positive_selections"][0]["atoms"][0]["half"] = False
    with pytest.raises(RefusalError, match="replay differs"):
        probe.verify_packet(forged, bound, budget())


def test_partial_replay_cannot_certify(bound: probe.Bound) -> None:
    with pytest.raises(RefusalError, match="partial"):
        probe.verify_packet({**bound.header, "status": "INCOMPLETE"}, bound, budget())


def test_frozen_identity_refuses_before_geometry() -> None:
    with pytest.raises(RefusalError, match="frozen"):
        probe.bind(
            {},
            {},
            source={},
            baseline={},
            refinement={},
            certificate={},
            d_packet={},
            d_replay={},
            b_packet={},
            budget=budget(),
        )


@pytest.fixture
def geometry_context() -> full.Context:
    core = [(-Q(1, 4), -Q(1, 4)), (Q(1, 4), -Q(1, 4)), (Q(1, 4), Q(1, 4)), (-Q(1, 4), Q(1, 4))]
    atoms = [Atom(owner, 0, (0,), [(Q(owner), Q(0))], core) for owner in range(6)]
    document = {
        "final_state": {
            "cells": {
                str(owner): [
                    {
                        "interval": ["0", "1/16"],
                        "reference": {"kind": "phase3", "row": 0, "step": owner},
                    }
                ]
                for owner in range(6)
            }
        }
    }
    return full.Context(n17_unique_frame(), atoms, document, [list(range(6))], {0}, set(), {})


def test_inventory_preserves_domains_and_distinct_halves(
    geometry_context: full.Context,
) -> None:
    saved = copy.deepcopy(geometry_context.raw)
    inv, _ = probe.build_inventory(geometry_context, geometry_context.raw, {(3, 0)}, budget())
    assert len(inv.atoms) == 7
    assert geometry_context.raw == saved
    assert inv.variants(3) == [3, 4]
    assert inv.refs[3]["half"] == 0
    assert inv.refs[4]["half"] == 1
    assert inv.refs[3]["model_interval"] != inv.refs[4]["model_interval"]
    for ref, atom in zip(inv.refs, inv.atoms, strict=True):
        old = saved[ref["raw_atom_index"]]
        assert atom.domain == old.domain
        assert atom.pieces == old.pieces
        assert ref["domain_sha256"] == probe.content_sha256(full.encode(old.domain))


def test_inventory_refuses_foreign_row_and_changed_domain(
    geometry_context: full.Context,
) -> None:
    with pytest.raises(RefusalError, match="outside inventory"):
        probe.build_inventory(geometry_context, geometry_context.raw, {(3, 1)}, budget())
    changed = geometry_context.raw[:]
    atom = changed[0]
    changed[0] = Atom(atom.owner, atom.row, atom.pieces, [(Q(99), Q(0))], atom.core)
    with pytest.raises(RefusalError, match="domain/piece changed"):
        probe.build_inventory(geometry_context, changed, set(), budget())
