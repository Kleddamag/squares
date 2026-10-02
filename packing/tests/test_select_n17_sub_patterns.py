"""Controls for the H-267 sub-pattern selector, a heuristic and not a certificate."""

from __future__ import annotations

import itertools
from functools import cache
from typing import Any

import numpy as np

from devtools.select_n17_sub_patterns import (
    MARGIN,
    Budget,
    Geometry,
    Problem,
    canonical,
    consume,
    contact_clusters,
    cover_geometry,
    endpoint_pose,
    endpoint_witnesses,
    greedy_order,
    image_mask,
    make_geometry,
    mask_of,
    pattern_rng,
    polygon_distance,
    search,
    sweep,
    tight_control,
    transform_pose,
)

QUICK = Budget(starts=4, hops=4, deep_starts=4, deep_hops=4)


def box(x0: float, x1: float, y0: float, y1: float) -> np.ndarray:
    return np.array([[x0, y0], [x1, y0], [x1, y1], [x0, y1]])


@cache
def cover() -> Geometry:
    return cover_geometry()


@cache
def endpoint() -> dict[str, Any]:
    return endpoint_pose()


@cache
def strip() -> Geometry:
    """Three cells on the bottom wall: each adjacent pair fits only touching, all three never.

    A centre at height at most 0.6 allows a turn of about 0.2 rad, so the squares are
    nearly upright and need about one unit of `x` each; A and C are at most 1.6 apart.
    """
    return make_geometry(
        [box(0.5, 0.7, 0.5, 0.6), box(1.1, 1.5, 0.5, 0.6), box(1.9, 2.1, 0.5, 0.6)],
        ["A", "B", "C"],
    )


def ring_group() -> tuple[tuple[int, ...], ...]:
    """D4 on the eight boundary cells of a 3 x 3 grid, as permutations."""
    cells = [(x, y) for x in (-1, 0, 1) for y in (-1, 0, 1) if (x, y) != (0, 0)]
    index = {cell: k for k, cell in enumerate(cells)}
    group: list[tuple[int, ...]] = []
    for reflect in (False, True):
        for turns in range(4):
            images = []
            for x, y in cells:
                u, v = (-x, y) if reflect else (x, y)
                for _ in range(turns):
                    u, v = -v, u
                images.append(index[(u, v)])
            group.append(tuple(images))
    return tuple(group)


def test_polygon_distance_sees_crossings_and_not_collinear_edges() -> None:
    assert polygon_distance(box(0, 3, 1, 2), box(1, 2, 0, 3)) == 0.0  # a plus, no vertex inside
    assert abs(polygon_distance(box(0, 1, 0, 1), box(3, 4, 0, 1)) - 2.0) < 1e-12
    assert int(np.count_nonzero(np.triu(cover().interact, 1))) == 212


def test_endpoint_pose_is_a_witness_in_its_own_state() -> None:
    point = endpoint()
    cells = point["cells"]
    assert len(set(cells)) == 17
    violations = Problem(cover(), cells).violations(point["pose"])
    assert max(violations.values()) <= 1e-12
    names = dict(zip(point["labels"], (cover().names[c] for c in cells), strict=True))
    assert names[13] == "side-S1"  # the unique-state design moved square 13 into S1


def test_endpoint_sub_patterns_are_witnessed_before_any_search() -> None:
    witnessed, record = endpoint_witnesses(cover(), endpoint(), 3)
    expected = {
        canonical(mask_of(sub), cover().group)
        for arity in (1, 2, 3)
        for sub in itertools.combinations(endpoint()["cells"], arity)
    }
    assert record["passed"]
    assert witnessed == expected


def test_penalty_gradient_matches_central_differences() -> None:
    problem = Problem(cover(), (0, 4, 16, 18))
    rng = np.random.default_rng(5)
    z = problem.pack(problem.random_pose(rng)) + rng.normal(0.0, 0.05, 12 + 2 * problem.p)
    _, gradient = problem.penalty(z)
    step = 1e-6
    numeric = [
        (problem.penalty(z + step * unit)[0] - problem.penalty(z - step * unit)[0]) / (2 * step)
        for unit in np.eye(len(z))
    ]
    assert np.max(np.abs(np.array(numeric) - gradient)) < 1e-6


def test_touching_pairs_pass_and_the_crowded_triple_is_flagged() -> None:
    geometry = strip()
    for pair in ((0, 1), (1, 2)):
        verdict = search(geometry, pair, pattern_rng(3, mask_of(pair)), QUICK)
        assert verdict.feasible
        assert verdict.violation <= MARGIN
    triple = search(geometry, (0, 1, 2), pattern_rng(3, 7), QUICK)
    assert not triple.feasible
    assert triple.violation > 0.1


def test_sweep_is_deterministic_under_a_seed() -> None:
    first = sweep(strip(), max_arity=3, seed=11, budget=QUICK)
    second = sweep(strip(), max_arity=3, seed=11, budget=QUICK)
    for record in (first, second):
        for level in record["levels"].values():
            level.pop("seconds")
        record.pop("seconds")
    assert first == second
    assert first["flagged_masks"] == [0b111]
    rng_a, rng_b = pattern_rng(1, 0b10001), pattern_rng(1, 0b10001)
    a = search(cover(), (0, 4), rng_a, QUICK)
    b = search(cover(), (0, 4), rng_b, QUICK)
    assert np.array_equal(a.pose, b.pose)


def test_a_witnessed_pattern_is_never_flagged() -> None:
    record = sweep(strip(), max_arity=3, seed=11, budget=QUICK, witnessed={0b111})
    assert record["flagged"] == []
    assert [entry["indices"] for entry in record["false_flags"]] == [[0, 1, 2]]


def test_tight_endpoint_cluster_reaches_the_margin() -> None:
    rows = contact_clusters(endpoint(), 3)[0]
    record = tight_control(cover(), endpoint(), rows, seed=1, budget=QUICK)
    assert record["passed"]
    assert record["best_violation"] <= MARGIN


def test_witnesses_travel_under_d4() -> None:
    point = endpoint()
    rows = list(range(6))
    cells = tuple(point["cells"][row] for row in rows)
    for element, permutation in enumerate(cover().group):
        image_cells, image_pose = transform_pose(cover(), cells, point["pose"][rows], element)
        assert mask_of(image_cells) == image_mask(mask_of(cells), permutation)
        assert Problem(cover(), image_cells).violation(image_pose) <= 1e-12


def brute_force(
    group: tuple[tuple[int, ...], ...], size: int, flagged: list[int]
) -> tuple[int, int]:
    forbidden = [
        frozenset(permutation[c] for c in range(8) if mask >> c & 1)
        for mask in flagged
        for permutation in group
    ]
    alive = [
        frozenset(subset)
        for subset in itertools.combinations(range(8), size)
        if not any(pattern <= frozenset(subset) for pattern in forbidden)
    ]
    orbits = {
        min(tuple(sorted(permutation[c] for c in state)) for permutation in group)
        for state in alive
    }
    return len(alive), len(orbits)


def test_consumer_matches_brute_force_on_a_toy_cover() -> None:
    group = ring_group()
    for flagged in ([], [0b11], [0b11, 0b10100], [0b1001001]):
        record = consume(8, group, flagged, size=4)
        assert (record["surviving_states"], record["orbits"]) == brute_force(group, 4, flagged)
    # Burnside on the ring: (70 + 2 + 6 + 2 + 4 * 6) / 8 for identity, turns, reflections.
    assert consume(8, group, [], size=4)["orbits"] == 13
    order = greedy_order(8, group, [0b11, 0b10100], size=4)
    assert order[0]["removes"] >= order[-1]["removes"]


def test_consumer_without_flags_reproduces_the_h266_census() -> None:
    record = consume(24, cover().group, [], endpoint_state=mask_of(endpoint()["cells"]))
    assert record["states"] == 346104
    assert record["orbits"] == 43593
    assert record["endpoint_survives"]
