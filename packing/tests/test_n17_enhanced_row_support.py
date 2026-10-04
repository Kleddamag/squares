"""Small finite controls for the additive enhanced-parent wrapper."""

from __future__ import annotations

import copy
import json
import random
import time
from itertools import combinations, product
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from devtools import probe_n17_core_refinement as core
from devtools import probe_n17_enhanced_row_support as enhanced
from devtools import probe_n17_raw_row_support as raw
from sqpack.hull_kernel.frame import make_frame
from sqpack.hull_kernel.geometry import Budget, IncompleteError, RefusalError, area2
from sqpack.hull_kernel.rational import Q


def budget() -> Budget:
    return Budget(time.monotonic() + 10, 10000)


@pytest.fixture(autouse=True)
def isolate_shared_worker_peak(monkeypatch: pytest.MonkeyPatch) -> None:
    # Independent CLI still samples real process memory; threshold is tested below.
    for module in (enhanced, raw, core):
        monkeypatch.setattr(module, "peak_memory_bytes", lambda: 128 * 1024**2)


def fixture() -> tuple[Any, ...]:
    def box(lo: Q, hi: Q) -> list[tuple[Q, Q]]:
        return [(lo, lo), (hi, lo), (hi, hi), (lo, hi)]

    frame = make_frame(
        name="enhanced-controls",
        cap=Q(3),
        length=Q(3),
        cells=[box(Q(1, 2), Q(3, 5)), box(Q(3, 2), Q(8, 5)), box(Q(12, 5), Q(5, 2))],
        cell_names=["a", "b", "c"],
        occupancy=3,
        action_names=("r0",),
    )
    steps, cells = [], {}
    for owner in range(3):
        h = Q(47, 100)
        old = [(-h, -h), (h, -h), (h, h), (-h, h)]
        point = [(Q(owner) + Q(1, 2), Q(3, 2))]
        # Include a distinct second point piece; both halves of every piece survive.
        pieces = [raw.encode(point), raw.encode([(point[0][0], Q(151, 100))])]
        ref = {"kind": "phase3", "node": "control", "step": owner, "row": 0}
        row = {
            "interval": ["0", "1/100"],
            "reference": ref,
            "residual_polygons": pieces,
            "outer_domain": raw.encode(point),
        }
        steps.append(
            {"owner": owner, "rows": [{**copy.deepcopy(row), "core_vertices": raw.encode(old)}]}
        )
        cells[str(owner)] = [row]
    doc = {
        "node_id": "control",
        "U": "3",
        "B": "1",
        "mask": [0, 1, 2],
        "steps": steps,
        "final_state": {"mask": [0, 1, 2], "cells": cells},
    }
    atoms = raw.raw_atoms(frame, doc)
    inv = enhanced.build_inventory(frame, atoms, doc, budget())
    identity = {"node_sha256": raw.content_sha256(doc)}
    source = raw.packet(raw.LazySupports(atoms, budget()).run(), atoms, doc, identity)
    baseline = {
        "diagnostic_only": True,
        "new_exclusions": 0,
        **raw.verify_packet(source, atoms, doc, identity, budget()),
    }
    selections = core.bound_source(source, baseline, atoms, doc, identity)
    children, growth = core.children(frame, atoms, selections, doc, budget())
    search = core.Refiner(selections, children, budget())
    status, reason = search.run()
    hpacket = core.packet(
        search,
        atoms,
        doc,
        identity,
        source,
        baseline=baseline,
        growth=growth,
        status=status,
        reason=reason,
        endpoint=None,
    )
    initial = enhanced.seeds(hpacket, source, baseline, inv, doc, identity=identity)
    common = enhanced.header(inv, identity, hpacket, source, baseline)
    return frame, doc, inv, identity, source, baseline, hpacket, initial, common


def retained(values: tuple[Any, ...]) -> dict[str, Any]:
    inv, initial, common = values[2], values[7], values[8]
    search = raw.LazySupports(inv.atoms, budget(), predicate=enhanced.bounded_incompatible)
    enhanced.prevalidate(search, initial)
    snapshot = search.run(initial_selections=initial, strategy="forward-mrv")
    return enhanced.packet(snapshot, inv, common, initial, seeded=True)


def test_full_piece_cover_half_identity_and_monotone_cores() -> None:
    values = fixture()
    inv = values[2]
    assert len(inv.raw) == 6
    assert len(inv.atoms) == 12
    assert len(inv.parents()) == 3
    assert set(inv.lookup.values()) == set(range(12))
    for index, atom in enumerate(inv.raw):
        for half in (0, 1):
            child = inv.atoms[2 * index + half]
            assert child.domain is atom.domain
            assert child.pieces == atom.pieces
            assert area2(child.core) > area2(atom.core)
            assert all(core.in_convex(child.core, point) for point in atom.core)
            assert inv.references[2 * index + half]["raw_atom_index"] == index
    assert enhanced.selection_indices([inv.references[i] for i in [1, 5, 9]], inv) == [1, 5, 9]


@pytest.mark.parametrize("seed", range(6))
def test_parent_search_agrees_with_all_half_piece_assignments(seed: int) -> None:
    inv = fixture()[2]
    rng = random.Random(seed)
    edges = {
        (a, b)
        for a, b in combinations(range(12), 2)
        if inv.atoms[a].owner != inv.atoms[b].owner and rng.random() < 0.45
    }
    ids = {id(atom): index for index, atom in enumerate(inv.atoms)}

    def predicate(a: raw.Atom, b: raw.Atom, _budget: Budget) -> bool:
        assert a.owner < b.owner
        return (ids[id(a)], ids[id(b)]) not in edges

    expected = [
        choice
        for choice in product(range(4), range(4, 8), range(8, 12))
        if all(tuple(sorted(pair)) in edges for pair in combinations(choice, 2))
    ]
    result = raw.LazySupports(inv.atoms, budget(), predicate=predicate).run(
        strategy="forward-mrv"
    )
    covered = {
        parent
        for choice in result["selections"]
        for parent in enhanced.parent_coverage(choice, inv)
    }
    assert covered == {
        parent for choice in expected for parent in enhanced.parent_coverage(list(choice), inv)
    }
    assert all(
        tuple(sorted(pair)) in edges
        for choice in result["selections"]
        for pair in combinations(choice, 2)
    )


def test_all_seeds_charged_before_any_coverage() -> None:
    inv = fixture()[2]
    initial = [[0, 4, 8], [1, 5, 9]]
    search = raw.LazySupports(inv.atoms, budget(), predicate=lambda *_: False)
    enhanced.prevalidate(search, initial)
    assert search.pair_tests == 6
    assert len(search.cache) == 6
    assert not search.supported
    assert not search.selections
    result = search.run(initial_selections=initial, strategy="forward-mrv")
    assert result["initial_unique_pairs"] == 6
    assert result["selections"][:2] == initial


def test_late_seed_failure_never_marks_partial_baseline() -> None:
    inv = fixture()[2]
    calls = 0

    def fail(*_: Any) -> bool:
        nonlocal calls
        calls += 1
        if calls == 4:
            raise IncompleteError("injected late seed failure")
        return False

    search = raw.LazySupports(inv.atoms, budget(), predicate=fail)
    with pytest.raises(IncompleteError):
        enhanced.prevalidate(search, [[0, 4, 8], [1, 5, 9]])
    assert search.pair_tests == 4
    assert len(search.cache) == 3
    assert not search.supported
    assert not search.selections


@pytest.mark.parametrize(
    "field", ["half", "raw_atom_index", "domain_sha256", "child_core_sha256", "child_interval"]
)
def test_child_provenance_tampering_refuses(field: str) -> None:
    inv = fixture()[2]
    refs = copy.deepcopy([inv.references[i] for i in [0, 4, 8]])
    refs[0][field] = True if field == "half" else "tampered"
    with pytest.raises(RefusalError):
        enhanced.selection_indices(refs, inv)


def test_fresh_replay_cannot_use_search_or_pair_cache(monkeypatch: pytest.MonkeyPatch) -> None:
    values = fixture()
    value = retained(values)

    def forbidden(*_: Any, **__: Any) -> Any:
        pytest.fail("replay called search/cache")

    monkeypatch.setattr(raw.LazySupports, "run", forbidden)
    monkeypatch.setattr(raw.LazySupports, "compatible", forbidden)
    replay = enhanced.verify_packet(value, values[2], values[8], values[7], budget())
    assert replay["supported_parent_rows"] == 3
    assert replay["fresh_pair_checks"] == 3
    assert replay["unsupported_rows_verified"] is False


@pytest.mark.parametrize(
    "field",
    [
        "selections",
        "seeds_freshly_prevalidated",
        "seed_selections",
        "initial_selections_revalidated",
        "initial_supported_rows",
        "supported_parent_rows",
        "unknown_parent_rows",
        "new_parent_rows",
        "derived_inventory_sha256",
    ],
)
def test_replay_metadata_tampering_refuses(field: str) -> None:
    values = fixture()
    value = retained(values)
    value[field] = (
        [[99, 99]] if field.endswith("rows") else [] if field == "selections" else "tampered"
    )
    with pytest.raises(RefusalError):
        enhanced.verify_packet(value, values[2], values[8], values[7], budget())


@pytest.mark.parametrize(
    "field",
    [
        "input_identity",
        "source_packet_sha256",
        "baseline_replay_sha256",
        "supported_parent_rows",
    ],
)
def test_h_seed_binding_refuses_drift(field: str) -> None:
    values = fixture()
    hpacket = copy.deepcopy(values[6])
    hpacket[field] = "tampered"
    with pytest.raises(RefusalError):
        enhanced.seeds(hpacket, values[4], values[5], values[2], values[1], identity=values[3])


def test_actual_guards_and_failed_post_query_are_not_cached(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    inv = fixture()[2]
    monkeypatch.setattr(enhanced, "peak_memory_bytes", lambda: enhanced.MAX_PEAK_BYTES + 1)
    with pytest.raises(IncompleteError, match="worker peak"):
        enhanced.remaining(budget())
    monkeypatch.setattr(enhanced, "peak_memory_bytes", lambda: 0)
    with pytest.raises(IncompleteError, match="wall ceiling"):
        enhanced.remaining(Budget(0, 1))

    def late(*_: Any) -> bool:
        monkeypatch.setattr(enhanced, "peak_memory_bytes", lambda: enhanced.MAX_PEAK_BYTES + 1)
        return False

    monkeypatch.setattr(enhanced, "incompatible", late)
    search = raw.LazySupports(inv.atoms, budget(), predicate=enhanced.bounded_incompatible)
    with pytest.raises(IncompleteError):
        search.compatible(0, 4)
    assert search.pair_tests == 1
    assert not search.cache


def test_non_boolean_query_never_enters_cache(monkeypatch: pytest.MonkeyPatch) -> None:
    inv = fixture()[2]
    monkeypatch.setattr(enhanced, "incompatible", lambda *_: None)
    search = raw.LazySupports(inv.atoms, budget(), predicate=enhanced.bounded_incompatible)
    with pytest.raises(RefusalError, match="exact bool"):
        search.compatible(0, 4)
    assert not search.cache


@pytest.mark.parametrize(("pairs", "nodes"), [(0, 100), (100, 0)])
def test_caps_are_unknown_not_exhaustive_unsupported(pairs: int, nodes: int) -> None:
    values = fixture()
    search = raw.LazySupports(values[2].atoms, budget(), max_pairs=pairs, max_nodes=nodes)
    snapshot = search.run(strategy="forward-mrv")
    value = enhanced.packet(snapshot, values[2], values[8], [], seeded=False)
    assert value["status"] == "INCOMPLETE"
    assert value["exhaustive_unverified_candidates"] == []
    assert value["unknown_parent_rows"] == [[0, 0], [1, 0], [2, 0]]
    assert value["unsupported_rows_verified"] is False


def test_exhaustion_retains_unknown_and_no_unsupported_claim() -> None:
    values = fixture()
    search = raw.LazySupports(values[2].atoms, budget(), predicate=lambda *_: True)
    value = enhanced.packet(
        search.run(strategy="forward-mrv"), values[2], values[8], [], seeded=False
    )
    assert value["status"] == "PARTIAL_SUPPORT"
    assert value["unknown_parent_rows"] == value["exhaustive_unverified_candidates"]
    assert value["unsupported_rows_verified"] is False


def test_derived_inventory_and_actual_serialized_size_guard(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    values = fixture()
    with pytest.raises(RefusalError, match="frozen fixture"):
        enhanced.fixture_inventory(values[2], values[6], endpoint=False)
    monkeypatch.setattr(enhanced, "MAX_CHILD_ATOMS", 10)
    with pytest.raises(RefusalError, match="child8192"):
        enhanced.build_inventory(values[0], values[2].raw, values[1], budget())
    value = {"a": [1, 2, 3]}
    compact, actual = (
        len(json.dumps(value).encode()),
        len((json.dumps(value, indent=2) + "\n").encode()),
    )
    assert compact < actual
    monkeypatch.setattr(enhanced, "MAX_PACKET_BYTES", compact)
    with pytest.raises(RefusalError, match="4MiB"):
        enhanced.safe_write(tmp_path / "refused.json", value)
    assert not (tmp_path / "refused.json").exists()


def test_endpoint_enclosure_child_control(monkeypatch: pytest.MonkeyPatch) -> None:
    values = fixture()
    inv = values[2]
    monkeypatch.setattr(enhanced, "endpoint_selection", lambda *_: [0, 2, 4])
    targets = {owner: SimpleNamespace(charts=[(Q(1, 1000), Q(2, 1000))]) for owner in range(3)}
    monkeypatch.setattr(
        enhanced, "load_endpoint", lambda _: SimpleNamespace(by_owner=lambda: targets)
    )
    enhanced.endpoint_children(values[0], values[1], inv, [[0, 4, 8]])
    with pytest.raises(RefusalError, match="crosses child"):
        enhanced.endpoint_children(values[0], values[1], inv, [[1, 5, 9]])


def test_raw_defaults_immutable() -> None:
    assert raw.MAX_ATOMS == 4096
    assert raw.MAX_PAIRS == 50000
    assert enhanced.MAX_CHILD_ATOMS == 8192
    assert enhanced.MAX_PAIRS == 100000
