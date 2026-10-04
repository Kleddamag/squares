"""Finite graph scheduling controls and accepted-seed provenance controls."""

from __future__ import annotations

import copy
import random
import time
from itertools import combinations, product
from typing import Any

import pytest

from devtools import probe_n17_enhanced_row_support as enhanced
from devtools import probe_n17_raw_row_support as raw
from devtools import probe_n17_scheduled_row_support as scheduled
from devtools.probe_n17_residual_graph import Atom
from sqpack.hull_kernel.geometry import Budget, IncompleteError, RefusalError
from sqpack.hull_kernel.rational import Q


def budget() -> Budget:
    return Budget(time.monotonic() + 10, 10000)


@pytest.fixture(autouse=True)
def isolate_shared_worker_peak(monkeypatch: pytest.MonkeyPatch) -> None:
    for module in (raw, enhanced, scheduled):
        monkeypatch.setattr(module, "peak_memory_bytes", lambda: 128 * 1024**2)


def inventory(owners: int = 6) -> enhanced.Inventory:
    atoms, refs, lookup = [], [], {}
    for owner in range(owners):
        for row in range(2):
            for half in range(2):
                index = len(atoms)
                atoms.append(Atom(owner, row, (0,), [(Q(owner), Q(row))], [(Q(0), Q(0))]))
                ref = {
                    "owner": owner,
                    "row": row,
                    "piece": 0,
                    "half": half,
                    "raw_atom_index": index // 2,
                }
                refs.append(ref)
                lookup[owner, row, 0, half] = index
    return enhanced.Inventory(atoms[::2], atoms, refs, lookup, "inventory-control")


def admitted(monkeypatch: pytest.MonkeyPatch) -> tuple[Any, ...]:
    inv = inventory()
    initial = [[4 * owner for owner in range(6)], [4 * owner + 2 for owner in range(6)]]
    h_initial = initial[:1]
    original = enhanced.header(inv, {"node_sha256": "control"}, {}, {}, {})
    search = raw.LazySupports(inv.atoms, budget(), predicate=lambda *_: False)
    enhanced.prevalidate(search, h_initial)
    snap = search.run(initial_selections=initial)
    value = enhanced.packet(snap, inv, original, h_initial, seeded=True)
    value.update(
        initial_selections_revalidated=1, initial_supported_rows=6, initial_unique_pairs=15
    )
    replay = {
        "status": "PASS_REPLAYED_ALL_PARENT_ROWS",
        "packet_sha256": raw.content_sha256(value),
        "input_identity": original["input_identity"],
        "H_packet_sha256": original["H_packet_sha256"],
        "derived_inventory_sha256": inv.digest,
        "live_parent_rows": 12,
        "supported_parent_rows": 12,
        "selections_checked": 2,
        "fresh_pair_checks": 30,
        "unsupported_rows_verified": False,
    }
    monkeypatch.setitem(scheduled.A_SHA, name=False, value=raw.content_sha256(value))
    monkeypatch.setitem(scheduled.A_REPLAY_SHA, name=False, value=raw.content_sha256(replay))
    monkeypatch.setitem(scheduled.A_FIXTURES, name=False, value=(2, 12))
    return inv, initial, h_initial, original, value, replay


@pytest.mark.parametrize("strategy", ["fixed", "forward-mrv"])
@pytest.mark.parametrize("seed", range(5))
def test_complete_permutations_preserve_exhaustive_support(strategy: str, seed: int) -> None:
    inv = inventory(3)
    rng = random.Random(seed)
    edges = {
        (a, b)
        for a, b in combinations(range(12), 2)
        if inv.atoms[a].owner != inv.atoms[b].owner and rng.random() < 0.4
    }
    ids = {id(atom): index for index, atom in enumerate(inv.atoms)}

    def incompatible(a: Atom, b: Atom, _: Budget) -> bool:
        return tuple(sorted((ids[id(a)], ids[id(b)]))) in edges

    expected = set()
    for selection in product(range(4), range(4, 8), range(8, 12)):
        if all(tuple(sorted(pair)) not in edges for pair in combinations(selection, 2)):
            expected.update((inv.atoms[i].owner, inv.atoms[i].row) for i in selection)
    rows = sorted(inv.parents(), reverse=True)
    search = raw.LazySupports(inv.atoms, budget(), predicate=incompatible)
    result = search.run(strategy=strategy, row_order=rows)
    assert set(search.supported) == expected
    assert set(search.unsupported) == inv.parents() - expected
    assert (result["status"] == "ALL_ROWS_SUPPORTED") == (expected == inv.parents())
    default = raw.LazySupports(inv.atoms, budget(), predicate=incompatible).run(
        strategy=strategy
    )
    numeric = raw.LazySupports(inv.atoms, budget(), predicate=incompatible).run(
        strategy=strategy, row_order=sorted(inv.parents())
    )
    assert default == numeric


@pytest.mark.parametrize(
    "bad",
    [
        [],
        [(0, 0)],
        [(0, 0)] * 6,
        [(o, r) for o in range(3) for r in range(2)] + [(9, 9)],
        [(False, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)],
        [[o, r] for o in range(3) for r in range(2)],
    ],
)
def test_invalid_permutation_refuses_before_seed_coverage(bad: Any) -> None:
    inv = inventory(3)
    search = raw.LazySupports(inv.atoms, budget(), predicate=lambda *_: False)
    with pytest.raises(RefusalError, match="row order"):
        search.run(row_order=bad, initial_selection=[0, 4, 8])
    assert not search.supported
    assert not search.cache
    assert not search.selections


def test_priority_is_derived_from_unique_parents_and_includes_all_rows() -> None:
    inv = inventory(3)
    initial = [[0, 4, 8], [2, 4, 8], [0, 4, 10]]
    priority, rows = scheduled.schedule(inv, initial)
    assert priority == [1, 0, 2]
    assert rows == [(1, 0), (1, 1), (0, 0), (0, 1), (2, 0), (2, 1)]
    assert scheduled.schedule(inv, initial * 2) == (priority, rows)


def test_accepted_prefix_and_metadata_replay(monkeypatch: pytest.MonkeyPatch) -> None:
    inv, initial, h_initial, original, value, replay = admitted(monkeypatch)
    assert (
        scheduled.accepted_seeds(value, replay, inv, original, h_initial, endpoint=False)
        == initial
    )
    common = scheduled.header(original, value, replay, inv, initial)
    assert common["schema"] == scheduled.SCHEMA
    assert common["row_order"] == [list(row) for row in sorted(inv.parents())]
    assert common["scheduling_effect_isolated"] is False
    search = raw.LazySupports(inv.atoms, budget(), predicate=lambda *_: False)
    enhanced.prevalidate(search, initial)
    assert search.pair_tests == 30
    assert not search.supported
    snap = search.run(initial_selections=initial, row_order=sorted(inv.parents()))
    result = enhanced.packet(snap, inv, common, initial, seeded=True)
    monkeypatch.setattr(enhanced, "incompatible", lambda *_: False)
    checked = enhanced.verify_packet(result, inv, common, initial, budget())
    assert checked["supported_parent_rows"] == 12
    assert checked["fresh_pair_checks"] == 30
    result["selections"].pop()
    with pytest.raises(RefusalError, match="full seed prefix"):
        enhanced.verify_packet(result, inv, common, initial, budget())


@pytest.mark.parametrize(
    "field",
    [
        "packet_sha256",
        "input_identity",
        "derived_inventory_sha256",
        "selections_checked",
        "supported_parent_rows",
        "fresh_pair_checks",
        "unsupported_rows_verified",
    ],
)
def test_replay_tampering_refuses_even_if_hash_is_updated(
    monkeypatch: pytest.MonkeyPatch, field: str
) -> None:
    inv, _, h_initial, original, value, replay = admitted(monkeypatch)
    replay[field] = "tampered"
    monkeypatch.setitem(scheduled.A_REPLAY_SHA, name=False, value=raw.content_sha256(replay))
    with pytest.raises(RefusalError, match="A replay"):
        scheduled.accepted_seeds(value, replay, inv, original, h_initial, endpoint=False)


@pytest.mark.parametrize(
    "field",
    [
        "supported_parent_rows",
        "initial_supported_rows",
        "seeds_freshly_prevalidated",
        "schema",
        "derived_inventory_sha256",
    ],
)
def test_packet_tampering_refuses_even_if_hash_is_updated(
    monkeypatch: pytest.MonkeyPatch, field: str
) -> None:
    inv, _, h_initial, original, value, replay = admitted(monkeypatch)
    value[field] = "tampered"
    monkeypatch.setitem(scheduled.A_SHA, name=False, value=raw.content_sha256(value))
    with pytest.raises(RefusalError):
        scheduled.accepted_seeds(value, replay, inv, original, h_initial, endpoint=False)


def test_fixed_hash_and_half_refusal(monkeypatch: pytest.MonkeyPatch) -> None:
    inv, _, h_initial, original, value, replay = admitted(monkeypatch)
    changed = copy.deepcopy(value)
    changed["selections"][1][0]["half"] = 1
    with pytest.raises(RefusalError, match="frozen A"):
        scheduled.accepted_seeds(changed, replay, inv, original, h_initial, endpoint=False)
    monkeypatch.setitem(scheduled.A_SHA, name=False, value=raw.content_sha256(changed))
    changed["selections"][1][0]["child_core_sha256"] = "wrong"
    monkeypatch.setitem(scheduled.A_SHA, name=False, value=raw.content_sha256(changed))
    with pytest.raises(RefusalError, match="child provenance differs"):
        scheduled.accepted_seeds(changed, replay, inv, original, h_initial, endpoint=False)


def test_seed_pair_guard_does_not_mark_partial_baseline(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    inv, initial, *_ = admitted(monkeypatch)
    search = raw.LazySupports(inv.atoms, budget(), predicate=lambda *_: False, max_pairs=20)
    with pytest.raises(IncompleteError, match="pair ceiling"):
        enhanced.prevalidate(search, initial)
    assert search.pair_tests == 20
    assert not search.supported
    assert not search.selections


def test_scheduled_partial_and_final_headers_agree(monkeypatch: pytest.MonkeyPatch) -> None:
    inv, initial, _, original, value, replay = admitted(monkeypatch)
    common = scheduled.header(original, value, replay, inv, initial[:1])
    snapshots = []
    search = raw.LazySupports(inv.atoms, budget(), predicate=lambda *_: False, max_pairs=15)
    enhanced.prevalidate(search, initial[:1])
    _, order = scheduled.schedule(inv, initial[:1])
    snap = search.run(
        initial_selections=initial[:1],
        strategy="forward-mrv",
        row_order=order,
        checkpoint=snapshots.append,
    )
    assert snap["status"] == "INCOMPLETE"
    for item in [*snapshots, snap]:
        packet = enhanced.packet(item, inv, common, initial[:1], seeded=True)
        assert packet["row_order"] == [list(row) for row in order]
        assert packet["limits"]["unique_pairs"] == 100000
        assert packet["schema"] == scheduled.SCHEMA
