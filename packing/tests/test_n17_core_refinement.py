"""Exact finite-network and provenance controls for the frozen augmentation."""

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

from devtools import bounded_diagnostics
from devtools import probe_n17_core_refinement as core
from devtools import probe_n17_raw_row_support as raw
from sqpack.hull_kernel.frame import make_frame
from sqpack.hull_kernel.geometry import Budget, IncompleteError, RefusalError, area2
from sqpack.hull_kernel.rational import Q


def budget() -> Budget:
    return Budget(time.monotonic() + 10, 10000)


@pytest.fixture(autouse=True)
def isolate_shared_test_worker_memory(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(bounded_diagnostics, "current_memory_bytes", lambda: 128 * 1024 * 1024)
    monkeypatch.setattr(bounded_diagnostics, "current_memory_bytes", lambda: 128 * 1024 * 1024)


def fixture() -> tuple[Any, ...]:
    def box(lo: Q, hi: Q) -> list[tuple[Q, Q]]:
        return [(lo, lo), (hi, lo), (hi, hi), (lo, hi)]

    frame = make_frame(
        name="core-controls",
        cap=Q(3),
        length=Q(3),
        cells=[box(Q(1, 2), Q(3, 5)), box(Q(3, 2), Q(8, 5)), box(Q(12, 5), Q(5, 2))],
        cell_names=["a", "b", "c"],
        occupancy=3,
        action_names=("r0",),
    )
    steps, cells = [], {}
    for owner in range(3):
        half = Q(47, 100)
        old = [(-half, -half), (half, -half), (half, half), (-half, half)]
        domain = [(Q(owner) + Q(1, 2), Q(3, 2))]
        reference = {"kind": "phase3", "node": "controls", "step": owner, "row": 0}
        row = {
            "interval": ["0", "1/100"],
            "reference": reference,
            "residual_polygons": [raw.encode(domain)],
            "outer_domain": raw.encode(domain),
        }
        steps.append(
            {"owner": owner, "rows": [{**copy.deepcopy(row), "core_vertices": raw.encode(old)}]}
        )
        cells[str(owner)] = [row]
    document = {
        "node_id": "controls",
        "U": "3",
        "B": "1",
        "mask": [0, 1, 2],
        "steps": steps,
        "final_state": {"mask": [0, 1, 2], "cells": cells},
    }
    atoms = raw.raw_atoms(frame, document)
    identity = {"seed_sha256": "control-seed", "node_sha256": raw.content_sha256(document)}
    source = raw.packet(raw.LazySupports(atoms, budget()).run(), atoms, document, identity)
    baseline = {
        "diagnostic_only": True,
        "new_exclusions": 0,
        **raw.verify_packet(source, atoms, document, identity, budget()),
    }
    selections = core.bound_source(source, baseline, atoms, document, identity)
    refined, growth = core.children(frame, atoms, selections, document, budget())
    return frame, document, atoms, identity, source, baseline, selections, refined, growth


def retained(
    values: tuple[Any, ...], predicate: core.Predicate = core.incompatible
) -> dict[str, Any]:
    _, document, atoms, identity, source, baseline, selections, refined, growth = values
    search = core.Refiner(selections, refined, budget(), predicate=predicate)
    status, reason = search.run()
    return core.packet(
        search,
        atoms,
        document,
        identity,
        source,
        baseline=baseline,
        growth=growth,
        status=status,
        reason=reason,
        endpoint=None,
    )


def replay(value: dict[str, Any], values: tuple[Any, ...]) -> dict[str, Any]:
    frame, document, atoms, identity, source, baseline, selections, refined, growth = values
    return core.verify_packet(
        value,
        atoms,
        document,
        identity,
        source,
        baseline=baseline,
        selections=selections,
        refined=refined,
        growth=growth,
        budget=budget(),
        frame=frame,
    )


def test_exact_half_cover_monotone_strict_growth_and_frozen_domains() -> None:
    _, _, atoms, _, _, _, _, refined, growth = fixture()
    assert core.halves(Q(0), Q(1, 100)) == ((Q(0), Q(1, 200)), (Q(1, 200), Q(1, 100)))
    assert all(Q(item["area_gain2"]) > 0 for item in growth)
    for child in refined.values():
        assert child.atom.domain is atoms[child.parent].domain
        assert child.atom.pieces == atoms[child.parent].pieces
        assert all(core.in_convex(child.atom.core, p) for p in atoms[child.parent].core)
        assert area2(child.atom.core) > area2(atoms[child.parent].core)


@pytest.mark.parametrize(("lo", "hi"), [(Q(0), Q(0)), (Q(1), Q(0))])
def test_invalid_intervals_refuse(lo: Q, hi: Q) -> None:
    with pytest.raises(RefusalError, match="nondegenerate"):
        core.halves(lo, hi)


@pytest.mark.parametrize("seed", range(8))
def test_deterministic_child_choice_agrees_with_exhaustive_finite_cases(seed: int) -> None:
    values = fixture()
    refined = values[7]
    keys = sorted(refined)
    ids = {id(child.atom): key for key, child in refined.items()}
    rng = random.Random(seed)
    edges = {
        tuple(sorted((a, b)))
        for a, b in combinations(keys, 2)
        if refined[a].atom.owner != refined[b].atom.owner and rng.random() < 0.6
    }

    def predicate(a: raw.Atom, b: raw.Atom, _budget: Budget) -> bool:
        assert a.owner < b.owner
        return tuple(sorted((ids[id(a)], ids[id(b)]))) not in edges

    expected = [
        choice
        for choice in product((0, 1), repeat=3)
        if all(
            tuple(sorted(pair)) in edges
            for pair in combinations(list(zip(values[6][0], choice, strict=True)), 2)
        )
    ]
    result = retained(values, predicate)
    if expected:
        assert result["status"] == "ALL_PARENT_ROWS_SUPPORTED"
        assert (
            tuple(ref["half"] for ref in result["enhanced_selections"][0]["atoms"])
            == expected[0]
        )
    else:
        assert result["status"] == "LOST_KNOWN_SUPPORT"
        assert len(result["unknown_parent_rows"]) == 3
        assert "unsupported_rows" not in result


@pytest.mark.parametrize(
    "field",
    ["input_identity", "selections_checked", "fresh_pair_checks", "status"],
)
def test_baseline_identity_and_inventory_cannot_drift(field: str) -> None:
    _, document, atoms, identity, source, baseline, _, _, _ = fixture()
    mutated = copy.deepcopy(baseline)
    mutated[field] = "mutation"
    with pytest.raises(RefusalError, match=r"baseline|input identity"):
        core.bound_source(source, mutated, atoms, document, identity)


def test_source_provenance_refuses_a_changed_piece() -> None:
    _, document, atoms, identity, source, baseline, _, _, _ = fixture()
    source["selections"][0][0]["domain_sha256"] = "mutation"
    with pytest.raises(RefusalError, match="provenance"):
        core.bound_source(source, baseline, atoms, document, identity)


def test_caps_and_failed_predicate_never_cache_unknown() -> None:
    *_, selections, refined, _growth = fixture()
    search = core.Refiner(
        selections, refined, budget(), predicate=lambda _a, _b, _c: False, max_pairs=1
    )
    assert search.run()[0] == "INCOMPLETE"
    assert search.pair_tests == len(search.cache) == 1
    assert search.kept == []
    assert search.lost == []
    guard = core.Refiner(selections, refined, budget(), max_assignments=0)
    assert guard.run()[0] == "INCOMPLETE"
    assert guard.assignments == 0

    def failed(_a: raw.Atom, _b: raw.Atom, _c: Budget) -> bool:
        raise IncompleteError("injected guard")

    incomplete = core.Refiner(selections, refined, budget(), predicate=failed)
    assert incomplete.run()[0] == "INCOMPLETE"
    assert incomplete.cache == {}
    assert incomplete.pair_tests == 1
    assert incomplete.lost == []


def test_cache_reuses_success_with_canonical_owner_direction() -> None:
    *_, selections, refined, _growth = fixture()
    calls = []

    def predicate(a: raw.Atom, b: raw.Atom, _c: Budget) -> bool:
        calls.append((a.owner, b.owner))
        return False

    search = core.Refiner(selections, refined, budget(), predicate=predicate)
    assert search.compatible((1, 0), (0, 1))
    assert search.compatible((0, 1), (1, 0))
    assert calls == [(0, 1)]
    assert search.pair_tests == 1


def test_fresh_replay_avoids_enumeration_and_checks_exact_provenance(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    values = fixture()
    value = retained(values)

    def forbidden(*_args: Any, **_kwargs: Any) -> Any:
        raise AssertionError("replay invoked enumeration")

    monkeypatch.setattr(core.Refiner, "run", forbidden)
    result = replay(value, values)
    assert result["status"] == "PASS_REPLAYED_ALL_PARENT_ROWS"
    assert result["fresh_pair_checks"] == 3
    assert result["observed_supported_child_rows"] == 3
    assert value["child_coverage_is_lower_bound"]


@pytest.mark.parametrize(
    ("field", "mutation"),
    [
        ("half", 2),
        ("child_interval", ["0", "0"]),
        ("child_core_sha256", "mutation"),
        ("domain_sha256", "mutation"),
        ("source_reference", {}),
    ],
)
def test_child_reference_tampering_refused(field: str, mutation: Any) -> None:
    values = fixture()
    value = retained(values)
    value["enhanced_selections"][0]["atoms"][0][field] = mutation
    with pytest.raises(RefusalError, match=r"half|provenance"):
        replay(value, values)


def test_support_coverage_tampering_refused() -> None:
    values = fixture()
    value = retained(values)
    value["supported_parent_rows"].pop()
    with pytest.raises(RefusalError, match="coverage"):
        replay(value, values)


def test_endpoint_children_contain_exact_angle_enclosure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    frame, document, atoms, _, _, _, selections, refined, _ = fixture()
    monkeypatch.setattr(core, "endpoint_selection", lambda *_args: selections[0])
    targets = {owner: SimpleNamespace(charts=((Q(1, 400), Q(1, 400)),)) for owner in range(3)}
    monkeypatch.setattr(
        core, "load_endpoint", lambda _frame: SimpleNamespace(by_owner=lambda: targets)
    )
    assert core.endpoint_choices(frame, atoms, selections, document, refined) == (0, 0, 0)
    targets[0].charts = ((Q(1, 250), Q(3, 500)),)
    with pytest.raises(RefusalError, match="crosses child split"):
        core.endpoint_choices(frame, atoms, selections, document, refined)


def test_production_memory_and_time_guards(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        bounded_diagnostics,
        "current_memory_bytes",
        lambda: bounded_diagnostics.MAX_MEMORY_BYTES + 1,
    )
    with pytest.raises(IncompleteError, match="512 MiB"):
        core.remaining(budget())
    with pytest.raises(IncompleteError, match="wall ceiling"):
        core.remaining(Budget(time.monotonic() - 1, 100))


def test_no_growth_cli_stops_before_pair_target(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    frame, document, atoms, identity, source, baseline, *_ = fixture()
    source_path, baseline_path, out = (
        tmp_path / "source.json",
        tmp_path / "baseline.json",
        tmp_path / "out.json",
    )
    source_path.write_text(json.dumps(source))
    baseline_path.write_text(json.dumps(baseline))
    monkeypatch.setattr(core, "checked_inputs", lambda *_args: (document, identity))
    monkeypatch.setattr(core, "n17_unique_frame", lambda: frame)
    monkeypatch.setattr(core, "octagon_core", lambda *_args: atoms[0].core)
    monkeypatch.setattr(
        "sys.argv",
        [
            "probe",
            str(tmp_path),
            "--checked-receipt",
            str(tmp_path / "unused"),
            "--source-packet",
            str(source_path),
            "--baseline-replay",
            str(baseline_path),
            "--output",
            str(out),
        ],
    )
    assert core.main() == 0
    result = json.loads(out.read_text())
    assert result["status"] == "NO_CORE_GROWTH"
    assert result["unique_pair_tests"] == 0
