"""Finite search/replay controls; no target source or expensive producer run."""

from __future__ import annotations

import copy
import gzip
import json
import random
import time
from itertools import combinations, product
from pathlib import Path
from typing import Any

import pytest

from devtools import probe_n17_raw_row_support as raw
from sqpack.hull_kernel.frame import Frame, make_frame
from sqpack.hull_kernel.geometry import Budget, IncompleteError, RefusalError
from sqpack.hull_kernel.rational import Q


def budget() -> Budget:
    return Budget(time.monotonic() + 10, raw.MAX_NODES)


@pytest.fixture(autouse=True)
def isolated_worker_memory(monkeypatch: pytest.MonkeyPatch) -> None:
    # Pure controls share a CI process; explicitly test the production guard below.
    monkeypatch.setattr(raw, "peak_memory_bytes", lambda: 128 * 1024 * 1024)


def point_atom(owner: int, row: int) -> raw.Atom:
    half = Q(49, 100)
    core = [(-half, -half), (half, -half), (half, half), (-half, half)]
    return raw.Atom(owner, row, (0,), [(Q(owner) + Q(1, 2), Q(3, 2))], core)


@pytest.mark.parametrize("seed", range(8))
def test_lazy_rows_agree_with_exhaustive_finite_cases(seed: int) -> None:
    atoms = [point_atom(owner, row) for owner in range(3) for row in range(2)]
    rng = random.Random(seed)
    edges = {
        (left, right)
        for left, right in combinations(range(len(atoms)), 2)
        if atoms[left].owner != atoms[right].owner and rng.random() < 0.5
    }
    indices = {id(atom): index for index, atom in enumerate(atoms)}

    def predicate(a: raw.Atom, b: raw.Atom, _budget: Budget) -> bool:
        assert a.owner < b.owner
        return (indices[id(a)], indices[id(b)]) not in edges

    solutions = [
        values
        for values in product((0, 1), (2, 3), (4, 5))
        if all(tuple(sorted(pair)) in edges for pair in combinations(values, 2))
    ]
    supported = {
        (atoms[index].owner, atoms[index].row) for values in solutions for index in values
    }
    result = raw.LazySupports(atoms, budget(), predicate=predicate).run()
    assert {(item["owner"], item["row"]) for item in result["row_support"]} == supported
    assert (
        set(map(tuple, result["exhaustive_unsupported_rows"]))
        == {(atom.owner, atom.row) for atom in atoms} - supported
    )
    assert result["status"] != "INCOMPLETE"
    assert all(
        tuple(sorted(pair)) in edges
        for values in result["selections"]
        for pair in combinations(values, 2)
    )


@pytest.mark.parametrize(("pairs", "nodes"), [(0, 100), (100, 0)])
def test_caps_never_become_exhaustive_unsupported(pairs: int, nodes: int) -> None:
    search = raw.LazySupports(
        [point_atom(0, 0), point_atom(1, 0)], budget(), max_pairs=pairs, max_nodes=nodes
    )
    result = search.run()
    assert result["status"] == "INCOMPLETE"
    assert result["exhaustive_unsupported_rows"] == []


def test_timeout_failure_never_enters_compatible_cache() -> None:
    def timed_out(_a: raw.Atom, _b: raw.Atom, _budget: Budget) -> bool:
        raise IncompleteError("injected time ceiling")

    search = raw.LazySupports(
        [point_atom(0, 0), point_atom(1, 0)], budget(), predicate=timed_out
    )
    assert search.run()["status"] == "INCOMPLETE"
    assert search.cache == {}
    assert search.pair_tests == 1


def test_actual_memory_guard_and_wall_guard_refuse(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(raw, "peak_memory_bytes", lambda: raw.MAX_PEAK_BYTES + 1)
    with pytest.raises(IncompleteError, match="worker peak"):
        raw.remaining(budget())
    with pytest.raises(IncompleteError, match="wall ceiling"):
        raw.remaining(Budget(0, 1))


def fixture_document() -> tuple[Frame, dict[str, Any]]:
    def box(left: Q, right: Q) -> list[tuple[Q, Q]]:
        return [(left, Q(1)), (right, Q(1)), (right, Q(2)), (left, Q(2))]

    frame = make_frame(
        name="raw-controls",
        cap=Q(3),
        length=Q(3),
        cells=[box(Q(1, 2), Q(3, 5)), box(Q(3, 2), Q(8, 5)), box(Q(12, 5), Q(5, 2))],
        cell_names=["a", "b", "c"],
        occupancy=3,
        action_names=("r0",),
    )
    steps, cells = [], {}
    for owner in range(3):
        atom = point_atom(owner, 0)
        reference = {"kind": "phase3", "node": "controls", "step": owner, "row": 0}
        row = {
            "interval": ["0", "0"],
            "reference": reference,
            "residual_polygons": [raw.encode(atom.domain)],
            "outer_domain": raw.encode(atom.domain),
        }
        source = {**copy.deepcopy(row), "core_vertices": raw.encode(atom.core)}
        steps.append({"owner": owner, "rows": [source]})
        cells[str(owner)] = [row]
    return frame, {
        "node_id": "controls",
        "U": "3",
        "B": "1",
        "mask": [0, 1, 2],
        "steps": steps,
        "final_state": {"mask": [0, 1, 2], "cells": cells},
    }


def test_direct_replay_reconstructs_provenance_without_search(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    frame, document = fixture_document()
    atoms = raw.raw_atoms(frame, document)
    identity = {"node_sha256": raw.content_sha256(document)}
    search = raw.LazySupports(atoms, budget())
    retained = raw.packet(search.run(), atoms, document, identity)
    assert retained["status"] == "ALL_ROWS_SUPPORTED"

    def forbidden_run(_self: raw.LazySupports, **_kwargs: Any) -> dict[str, Any]:
        raise AssertionError("fresh replay invoked DFS")

    monkeypatch.setattr(raw.LazySupports, "run", forbidden_run)
    checked = raw.verify_packet(retained, atoms, document, identity, budget())
    assert checked["status"] == "PASS_REPLAYED_ALL_ROWS"
    assert checked["fresh_pair_checks"] == 3
    for field in ("piece", "domain_sha256", "core_sha256", "source_reference"):
        mutated = copy.deepcopy(retained)
        mutated["selections"][0][0][field] = -1 if field == "piece" else "mutation"
        with pytest.raises(
            (RefusalError, KeyError), match=r"invalid atom key|provenance|mutation"
        ):
            raw.verify_packet(mutated, atoms, document, identity, budget())
    omitted = copy.deepcopy(retained)
    omitted["row_support"].pop()
    with pytest.raises(RefusalError, match="omits rows"):
        raw.verify_packet(omitted, atoms, document, identity, budget())


def test_touching_is_unknown_compatible_and_empty_core_is_refused() -> None:
    a, b = point_atom(0, 0), point_atom(1, 0)
    assert not raw.incompatible(a, b, budget())
    a.domain = []
    with pytest.raises(RefusalError, match="empty atom"):
        raw.incompatible(a, b, budget())
    a = point_atom(0, 0)
    a.core = [(Q(0), Q(0))]
    with pytest.raises(RefusalError, match="query core"):
        raw.incompatible(a, b, budget())


def test_source_mutations_and_degenerate_pieces() -> None:
    frame, document = fixture_document()
    row = document["final_state"]["cells"]["0"][0]
    source = document["steps"][0]["rows"][0]
    segment = [["1/2", "3/2"], ["1/2", "8/5"]]
    row["residual_polygons"].append(segment)
    source["residual_polygons"].append(copy.deepcopy(segment))
    atoms = raw.raw_atoms(frame, document)
    assert len(atoms) == 4
    assert len(atoms[1].domain) == 2
    row["reference"]["step"] = -1
    with pytest.raises(RefusalError, match="invalid source step"):
        raw.raw_atoms(frame, document)


def test_cold_receipt_hash_and_packet_size_refusals(tmp_path: Path) -> None:
    _, document = fixture_document()
    seed = {"mask": document["mask"]}
    for kind, value in (("seed", seed), ("node", document)):
        (tmp_path / f"{kind}-{raw.content_sha256(value)}.json.gz").write_bytes(
            gzip.compress(json.dumps(value).encode())
        )
    receipt = {
        "status": "PASS_SAVED_STALL",
        "seed_sha256": raw.content_sha256(seed),
        "node_sha256": raw.content_sha256(document),
    }
    path = tmp_path / "checked.json"
    path.write_text(json.dumps(receipt))
    loaded, _ = raw.checked_inputs(tmp_path, path)
    assert loaded == document
    receipt["node_sha256"] = "mutation"
    path.write_text(json.dumps(receipt))
    with pytest.raises(RefusalError, match="node receipt differs"):
        raw.checked_inputs(tmp_path, path)
    path.write_bytes(b" " * (raw.MAX_PACKET_BYTES + 1))
    with pytest.raises(RefusalError, match="exceeds 4 MiB"):
        raw.bounded_json(path)
