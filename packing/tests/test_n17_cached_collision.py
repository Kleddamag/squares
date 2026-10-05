"""Exact verdict, frozen-query provenance, cache and resource controls."""

from __future__ import annotations

import copy
import time
from typing import Any

import pytest

from devtools import bounded_diagnostics
from devtools import probe_n17_cached_collision as probe
from devtools import probe_n17_enhanced_row_support as enhanced
from devtools import probe_n17_raw_row_support as raw
from devtools.probe_n17_residual_graph import Atom, incompatible
from sqpack.hull_kernel.geometry import Budget, IncompleteError, RefusalError
from sqpack.hull_kernel.rational import Q


def budget() -> Budget:
    return Budget(time.monotonic() + 10, 10000)


@pytest.fixture(autouse=True)
def isolate_shared_worker_peak(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(bounded_diagnostics, "current_memory_bytes", lambda: 128 * 1024**2)


def atom(owner: int, x: Q, *, segment: bool = False) -> Atom:
    h = Q(49, 100)
    domain = [(x, Q(0)), (x + Q(1, 100), Q(0))] if segment else [(x, Q(0))]
    return Atom(owner, 0, (0,), domain, [(-h, -h), (h, -h), (h, h), (-h, h)])


@pytest.mark.parametrize("segment", [False, True])
@pytest.mark.parametrize(("x", "expected"), [(Q(1, 10), True), (Q(3), False)])
def test_all_backends_and_empty_then_warm_cache_agree(
    *, segment: bool, x: Q, expected: bool
) -> None:
    atoms = [atom(0, Q(0)), atom(1, x, segment=segment)]
    cached = probe.CachedPredicate(atoms, budget())
    assert cached.sizes() == {"prepared_atoms": 2, "facet_entries": 0, "minimum_entries": 0}
    assert incompatible(atoms[0], atoms[1], budget()) is expected
    assert probe.integer_incompatible(atoms[0], atoms[1], budget()) is expected
    assert cached(atoms[0], atoms[1], budget()) is expected
    first = cached.sizes()
    assert first["facet_entries"] == 1
    assert first["minimum_entries"] > 0
    assert cached(atoms[0], atoms[1], budget()) is expected
    assert cached.sizes() == first
    assert probe.CachedPredicate(atoms, budget()).sizes()["facet_entries"] == 0


@pytest.mark.parametrize("field", ["domain", "core", "owner", "row", "pieces"])
def test_cache_rejects_inventory_mutation(field: str) -> None:
    atoms = [atom(0, Q(0)), atom(1, Q(1, 10))]
    cached = probe.CachedPredicate(atoms, budget())
    assert cached(atoms[0], atoms[1], budget())
    if field in {"domain", "core"}:
        getattr(atoms[1], field).append((Q(5), Q(5)))
    elif field == "pieces":
        atoms[1].pieces = (1,)
    else:
        setattr(atoms[1], field, 9)
    with pytest.raises(RefusalError, match="mutated"):
        cached(atoms[0], atoms[1], budget())


def test_unknown_atom_and_duplicate_object_refuse() -> None:
    a, b = atom(0, Q(0)), atom(1, Q(1, 10))
    cached = probe.CachedPredicate([a, b], budget())
    with pytest.raises(RefusalError, match="belong"):
        cached(a, copy.deepcopy(b), budget())
    with pytest.raises(RefusalError, match="duplicate"):
        probe.CachedPredicate([a, a], budget())


@pytest.mark.parametrize("backend", ["cached", "integer"])
def test_unexpected_refusal_propagates(monkeypatch: pytest.MonkeyPatch, backend: str) -> None:
    atoms = [atom(0, Q(0)), atom(1, Q(1, 10))]
    cached = probe.CachedPredicate(atoms, budget())

    def reject(*_: Any, **__: Any) -> int:
        raise RefusalError("unexpected bad core")

    name = (
        "cached_universal_collision" if backend == "cached" else "integer_universal_collision"
    )
    monkeypatch.setattr(probe.collision, name, reject)
    with pytest.raises(RefusalError, match="unexpected bad core"):
        (cached if backend == "cached" else probe.integer_incompatible)(
            atoms[0], atoms[1], budget()
        )


def test_guard_checks_both_sides_and_does_not_return_failed_query(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    atoms = [atom(0, Q(0)), atom(1, Q(1, 10))]
    guard = probe.Guard(budget(), max_calls=1)
    assert guard.check_pair(lambda *_: True, *atoms)
    with pytest.raises(IncompleteError, match="call ceiling"):
        guard.check_pair(lambda *_: True, *atoms)
    assert guard.calls == 1
    guard = probe.Guard(budget())

    def overrun(*_: Any) -> bool:
        guard.budget = Budget(0, 10000)
        return True

    with pytest.raises(IncompleteError, match="wall ceiling"):
        guard.check_pair(overrun, *atoms)
    assert guard.calls == 1
    monkeypatch.setattr(
        bounded_diagnostics, "current_memory_bytes", lambda: probe.MAX_PEAK_BYTES + 1
    )
    with pytest.raises(IncompleteError, match="current RSS"):
        probe.Guard(budget()).check_pair(lambda *_: True, *atoms)


def test_post_memory_guard_and_exact_bool(monkeypatch: pytest.MonkeyPatch) -> None:
    atoms = [atom(0, Q(0)), atom(1, Q(1, 10))]

    def inflate(*_: Any) -> bool:
        monkeypatch.setattr(
            bounded_diagnostics, "current_memory_bytes", lambda: probe.MAX_PEAK_BYTES + 1
        )
        return True

    with pytest.raises(IncompleteError, match="current RSS"):
        probe.Guard(budget()).check_pair(inflate, *atoms)
    monkeypatch.setattr(bounded_diagnostics, "current_memory_bytes", lambda: 128 * 1024**2)
    with pytest.raises(RefusalError, match="exact bool"):
        probe.Guard(budget()).check_pair(lambda *_: 1, *atoms)  # type: ignore[arg-type]
    with pytest.raises(RefusalError, match="noncanonical"):
        probe.Guard(budget()).check_pair(lambda *_: True, *reversed(atoms))


def bound_fixture(monkeypatch: pytest.MonkeyPatch) -> tuple[Any, ...]:
    originals = [atom(owner, Q(3 * owner)) for owner in range(6)]
    doc = {
        "final_state": {
            "cells": {
                str(owner): [
                    {
                        "interval": ["0", "1"],
                        "reference": {"kind": "control", "step": owner, "row": 0},
                    }
                ]
                for owner in range(6)
            }
        }
    }
    atoms, refs, lookup = [], [], {}
    for index, original in enumerate(originals):
        for half in (0, 1):
            atoms.append(copy.deepcopy(original))
            refs.append(
                {
                    **raw.atom_reference(original, doc),
                    "raw_atom_index": index,
                    "half": half,
                    "child_interval": ["0", "1/2"] if half == 0 else ["1/2", "1"],
                    "child_core_sha256": raw.content_sha256(raw.encode(original.core)),
                }
            )
            lookup[original.owner, 0, 0, half] = len(atoms) - 1
    inv = enhanced.Inventory(originals, atoms, refs, lookup, "control-inventory")
    identity = {"seed_sha256": "control-seed", "node_sha256": "control"}
    source = raw.packet(
        raw.LazySupports(originals, budget(), predicate=lambda *_: False).run(),
        originals,
        doc,
        identity,
    )
    baseline, refinement = {}, {}
    common = enhanced.header(inv, identity, refinement, source, baseline)
    support = {
        **common,
        "schema": "n17.scheduled-enhanced-parent-row-support.v1",
        "selections": [refs[::2]],
    }
    children = [
        {
            "original": raw.atom_reference(original, doc),
            "children": [
                {
                    "half": h,
                    "interval": refs[2 * i + h]["child_interval"],
                    "core_sha256": refs[2 * i + h]["child_core_sha256"],
                }
                for h in (0, 1)
            ],
        }
        for i, original in enumerate(originals)
    ]
    certificate = {
        "model": enhanced.MODEL,
        "predicate": enhanced.PREDICATE,
        "diagnostic_only": True,
        "new_exclusions": 0,
        "input_identity": identity,
        "H_packet_sha256": raw.content_sha256(refinement),
        "baseline_replay_sha256": raw.content_sha256(baseline),
        "E_packet_sha256": raw.content_sha256(source),
        "row_unsupportedness_verified": False,
        "certified_fixed_tuples": 1,
        "tuple_certificates": [
            {
                "source_selection_index": 0,
                "atoms": children,
                "incompatible_pairs": [
                    {"left_position": 0, "right_position": 1, "left_half": 1, "right_half": 1}
                ],
            }
        ],
    }
    expected = {probe.B_PATH: copy.deepcopy(support), probe.J_PATH: copy.deepcopy(certificate)}
    monkeypatch.setattr(
        probe,
        "retained_matches",
        lambda held, _, path: bounded_diagnostics.same_content(held, expected[path]),
    )
    monkeypatch.setattr(probe, "EXPECTED_B_SELECTIONS", 1)
    monkeypatch.setattr(probe, "EXPECTED_J_TUPLES", 1)
    monkeypatch.setattr(probe, "EXPECTED_J_WITNESSES", 1)
    return support, certificate, source, refinement, baseline, inv, doc, identity


def test_exact_mixed_corpus_order_and_provenance(monkeypatch: pytest.MonkeyPatch) -> None:
    values = bound_fixture(monkeypatch)
    queries = probe.corpus(*values[:5], inv=values[5], document=values[6], identity=values[7])
    assert len(queries) == 16
    assert [(q.left, q.right) for q in queries] == sorted((q.left, q.right) for q in queries)
    assert sum(q.expected for q in queries) == 1
    assert probe.Query(1, 3, expected=True) in queries
    support, certificate, source, refinement, baseline, inv, _, identity = values
    common = probe.header(
        inv,
        queries,
        support,
        certificate,
        identity,
        refinement=refinement,
        source=source,
        baseline=baseline,
    )
    assert common["query_count"] == 16
    assert common["queries"][0]["left"] == inv.references[0]


@pytest.mark.parametrize(
    "mutation",
    ["frozen_hash", "child_core", "half", "position", "original", "expected_conflict"],
)
def test_corpus_tamper_refuses(monkeypatch: pytest.MonkeyPatch, mutation: str) -> None:
    values = bound_fixture(monkeypatch)
    _support, certificate = values[:2]
    if mutation == "frozen_hash":
        certificate["diagnostic_only"] = False
    elif mutation == "child_core":
        certificate["tuple_certificates"][0]["atoms"][0]["children"][0]["core_sha256"] = "wrong"
    elif mutation == "original":
        certificate["tuple_certificates"][0]["atoms"][0]["original"]["owner"] = 99
    else:
        edge = certificate["tuple_certificates"][0]["incompatible_pairs"][0]
        if mutation == "half":
            edge["left_half"] = False
        elif mutation == "position":
            edge["left_position"] = 5
        else:
            edge.update(left_half=0, right_half=0)
    if mutation != "frozen_hash":
        monkeypatch.setattr(probe, "retained_matches", lambda *_: True)
    with pytest.raises(RefusalError):
        probe.corpus(*values[:5], inv=values[5], document=values[6], identity=values[7])


def test_four_answer_arrays_and_direct_replay() -> None:
    atoms = [atom(0, Q(0)), atom(1, Q(1, 10)), atom(2, Q(3))]
    inv = enhanced.Inventory(atoms, atoms, [{"owner": a.owner} for a in atoms], {}, "control")
    queries = [probe.Query(0, 1, expected=True), probe.Query(0, 2, expected=False)]
    common: dict[str, Any] = {
        "input_identity": {"seed_sha256": "control-seed", "node_sha256": "control"}
    }
    result: dict[str, Any] = dict(common)
    probe.profile(inv, queries, probe.Guard(budget()), result)
    assert result["status"] == "PASS_EQUIVALENT_MIXED_CORPUS"
    assert result["primitive_calls"] == 8
    assert all(result["answers"][name] == [True, False] for name in probe.PASSES)
    assert (
        result["timings"]["cached_first_use_seconds"]
        == result["timings"]["cached_setup_seconds"] + result["timings"]["cached_first_seconds"]
    )
    assert result["cache_after_first"] == result["cache_after_warm"]
    checked = probe.replay(result, inv, queries, common, probe.Guard(budget()))
    assert checked["fresh_pair_checks"] == 2
    assert checked["performance_statistics_verified"] is False
    forged = copy.deepcopy(result)
    forged["answers"]["cached_first"] = [1, 0]
    with pytest.raises(RefusalError, match="arrays"):
        probe.replay(forged, inv, queries, common, probe.Guard(budget()))
    result["answers"]["cached_warm"][0] = False
    with pytest.raises(RefusalError, match="arrays"):
        probe.replay(result, inv, queries, common, probe.Guard(budget()))


def test_cached_constructor_wall_and_query_post_memory_guard(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    atoms = [atom(0, Q(0)), atom(1, Q(1, 10))]
    with pytest.raises(IncompleteError, match="wall"):
        probe.CachedPredicate(atoms, Budget(0, 10000))
    cached = probe.CachedPredicate(atoms, budget())

    def inflate(*_: Any, **__: Any) -> int:
        monkeypatch.setattr(
            bounded_diagnostics, "current_memory_bytes", lambda: probe.MAX_PEAK_BYTES + 1
        )
        return 4

    monkeypatch.setattr(probe.collision, "cached_universal_collision", inflate)
    with pytest.raises(IncompleteError, match="current RSS"):
        cached(atoms[0], atoms[1], budget())


def test_failed_profile_query_never_enters_answer_array(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    atoms = [atom(0, Q(0)), atom(1, Q(1, 10))]
    inv = enhanced.Inventory(atoms, atoms, [], {}, "control")
    guard = probe.Guard(budget())

    def overrun(*_: Any) -> bool:
        guard.budget = Budget(0, 10000)
        return True

    monkeypatch.setattr(probe, "incompatible", overrun)
    result = {}
    with pytest.raises(IncompleteError, match="wall"):
        probe.profile(inv, [probe.Query(0, 1, expected=True)], guard, result)
    assert result["answers"]["rational"] == []


def test_profile_ceiling_refuses_before_calls() -> None:
    atoms = [atom(0, Q(0)), atom(1, Q(1, 10))]
    inv = enhanced.Inventory(atoms, atoms, [], {}, "control")
    guard = probe.Guard(budget(), max_calls=3)
    with pytest.raises(RefusalError, match="ceiling"):
        probe.profile(inv, [probe.Query(0, 1, expected=True)], guard, {})
    assert guard.calls == 0
