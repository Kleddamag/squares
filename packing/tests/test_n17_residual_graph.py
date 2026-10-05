"""Controls for the diagnostic's conservative graph abstraction."""

from __future__ import annotations

import random
import time
from itertools import combinations, product
from pathlib import Path

import pytest

from devtools import bounded_diagnostics
from devtools import probe_n17_residual_graph as graph
from devtools.check_n17_subpattern import load_certificate
from devtools.pilot_n17_capture import in_convex
from sqpack.hull_kernel.geometry import Budget, IncompleteError, RefusalError
from sqpack.hull_kernel.rational import Q


def budget() -> Budget:
    return Budget(time.monotonic() + 10, 15_360)


@pytest.fixture(autouse=True)
def isolated_worker_memory(monkeypatch: pytest.MonkeyPatch) -> None:
    # Pure graph controls share the CI worker with unrelated, larger tests. Its
    # historical process peak is not the standalone experiment's memory usage.
    monkeypatch.setattr(bounded_diagnostics, "current_memory_bytes", lambda: 128 * 1024 * 1024)


def test_worker_memory_guard_still_refuses_an_over_limit_reading(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        bounded_diagnostics, "current_memory_bytes", lambda: graph.MAX_PEAK_BYTES + 1
    )
    with pytest.raises(IncompleteError, match="actual worker current RSS exceeds"):
        graph.propagate([{0}, {1}], [{1}, {0}], budget(), path=True)


def test_path_consistency_detects_a_binary_odd_cycle_that_arc_consistency_misses() -> None:
    domains = [{0, 1}, {2, 3}, {4, 5}]
    edges = [set() for _ in range(6)]
    for left, right in ((0, 2), (1, 3), (2, 4), (3, 5), (0, 5), (1, 4)):
        edges[left].add(right)
        edges[right].add(left)
    graph.propagate(domains, edges, budget(), path=False)
    assert domains == [{0, 1}, {2, 3}, {4, 5}]
    graph.propagate(domains, edges, budget(), path=True)
    assert any(not domain for domain in domains)


@pytest.mark.parametrize("seed", range(12))
def test_all_complete_solutions_survive_against_exhaustive_enumeration(seed: int) -> None:
    rng = random.Random(seed)
    domains = [{0, 1}, {2, 3}, {4, 5}, {6, 7}]
    edges = [set() for _ in range(8)]
    planted = [0, 2, 4, 6]
    for left_domain, right_domain in combinations(domains, 2):
        for left, right in product(sorted(left_domain), sorted(right_domain)):
            if rng.random() < 0.6 or (left in planted and right in planted):
                edges[left].add(right)
                edges[right].add(left)
    solutions = [
        list(values)
        for values in product(*map(sorted, domains))
        if graph.selection_survives(list(values), domains, edges)
    ]
    assert planted in solutions
    graph.propagate(domains, edges, budget(), path=True)
    assert all(graph.selection_survives(values, domains, edges) for values in solutions)
    support = graph.finite_supports(domains, edges, budget())
    supported = {atom for solution in solutions for atom in solution}
    assert set(map(int, support["witnesses"])) == supported
    assert set(support["unsupported_atoms"]) == set().union(*domains) - supported
    assert support["status"] == "completed"
    if support["all_atoms_supported"]:
        assert graph.verify_complete_support_packet(support)
        first = next(iter(support["witnesses"]))
        support["witnesses"][first] = support["witnesses"][first][1:]
        assert not graph.verify_complete_support_packet(support)
    domains[0].remove(planted[0])
    assert not graph.selection_survives(planted, domains, edges)


def atom(x: Q) -> graph.Atom:
    # Strict cores of axis-aligned unit squares, so actual boundary contact is legal.
    side = Q(49, 100)
    core = [(-side, -side), (side, -side), (side, side), (-side, side)]
    return graph.Atom(0, 0, (0,), [(x, Q(0))], core)


def test_exact_collision_keeps_contact_and_refuses_empty_atoms() -> None:
    assert graph.incompatible(atom(Q(0)), atom(Q(1, 2)), budget())
    assert not graph.incompatible(atom(Q(0)), atom(Q(1)), budget())
    empty = atom(Q(0))
    empty.domain = []
    with pytest.raises(RefusalError, match="empty atom"):
        graph.incompatible(empty, atom(Q(1)), budget())


def test_degenerate_core_and_timeout_are_not_unknown_compatible_edges() -> None:
    invalid = atom(Q(0))
    invalid.core = [(Q(0), Q(0))]
    with pytest.raises(RefusalError, match="query core"):
        graph.incompatible(invalid, atom(Q(1)), budget())
    with pytest.raises(IncompleteError):
        graph.incompatible(atom(Q(0)), atom(Q(1)), Budget(0, 1))


def test_support_search_cap_never_means_unsupported() -> None:
    packet = graph.finite_supports([{0}, {1}], [{1}, {0}], budget(), max_nodes=1)
    assert packet["status"] == "guard-refused"
    assert not packet["all_atoms_supported"]
    assert packet["unsupported_atoms"] == []


def test_group_covers_keep_every_member_vertex_including_points_and_segments() -> None:
    directory = (
        Path(__file__).resolve().parents[1]
        / "campaign/explorations/X048-session-169-pilots/objects-W7"
    )
    _, document, _, _ = load_certificate(directory)
    owner, rows = next(iter(document["final_state"]["cells"].items()))
    document["final_state"]["cells"] = {owner: [rows[0]]}
    pieces = rows[0]["residual_polygons"]
    pieces.extend([pieces[0][:1], pieces[0][:2]])
    atoms = graph.atomize(graph.n17_unique_frame(), document, "two-cover")[int(owner)]
    assert len(atoms) == 2
    assert sorted(index for value in atoms for index in value.pieces) == list(
        range(len(pieces))
    )
    for value in atoms:
        assert all(
            in_convex(value.domain, point)
            for index in value.pieces
            for point in graph.points(pieces[index])
        )
