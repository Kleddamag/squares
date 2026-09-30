"""Focused controls for the independent conditional n=11 D4 checker."""

from __future__ import annotations

import copy
import itertools
import time
from fractions import Fraction

import pytest

from devtools import check_n11_optimality_d4 as d4

F = Fraction


def test_canonical_universe_and_survivor_masks() -> None:
    raw, canonical = d4.canonical_masks()
    assert len(raw) == 4368
    assert len(canonical) == 2184
    assert all(mask != d4.half_turn(mask) for mask in raw)
    assert {min(mask, d4.half_turn(mask)) for mask in raw} == set(canonical)
    assert {index: canonical[index] for index in d4.SURVIVORS} == d4.EXPECTED_MASKS


def test_closed_intersection_retains_boundary_point_and_segment() -> None:
    left = d4.hull(((F(0), F(0)), (F(1), F(0)), (F(1), F(1)), (F(0), F(1))))
    touching_point = d4.hull(((F(1), F(1)), (F(2), F(1)), (F(2), F(2)), (F(1), F(2))))
    touching_segment = d4.hull(((F(1), F(0)), (F(2), F(0)), (F(2), F(1)), (F(1), F(1))))
    assert d4.intersection(left, touching_point) == ((F(1), F(1)),)
    assert d4.intersection(left, touching_segment) == ((F(1), F(0)), (F(1), F(1)))


def test_strict_distance_keeps_equality_allowed() -> None:
    origin = ((F(0), F(0)),)
    equal = ((1 / (d4.U - 1), F(0)),)
    closer = ((1 / (2 * (d4.U - 1)), F(0)),)
    assert d4.strict_distance_ban(origin, equal) == (False, F(1))
    assert d4.strict_distance_ban(origin, closer) == (True, F(1, 4))


def test_distance_inventory_rejects_omission_duplicate_and_false_ban() -> None:
    vertices = [((F(0), F(0)),)] * 57
    pairs = list(itertools.islice(itertools.combinations(range(57), 2), 1572))
    rows = [
        {"regions": [first, second], "maximum_squared_center_distance": "0"}
        for first, second in pairs
    ]
    data = {"U": str(d4.U), "pairs": rows}
    assert len(d4.check_bans(vertices, data)) == 1572
    with pytest.raises(ValueError, match="omission"):
        d4.check_bans(vertices, {"U": str(d4.U), "pairs": rows[:-1]})
    duplicate = copy.deepcopy(data)
    duplicate["pairs"][1] = duplicate["pairs"][0]
    with pytest.raises(ValueError, match="duplicate"):
        d4.check_bans(vertices, duplicate)
    invalid = copy.deepcopy(data)
    invalid["pairs"][0]["maximum_squared_center_distance"] = "1"
    with pytest.raises(ValueError, match="not exact"):
        d4.check_bans(vertices, invalid)


def test_overlay_inventory_rejects_omission_duplicate_and_wrong_vertices() -> None:
    expected = {
        (0, 0): ((F(0), F(0)),),
        (0, 1): ((F(0), F(0)), (F(1), F(0))),
    }
    rows = [
        {"index": 0, "labels": [0, 0], "vertices": [["0", "0"]], "dimension": 0},
        {
            "index": 1,
            "labels": [0, 1],
            "vertices": [["0", "0"], ["1", "0"]],
            "dimension": 1,
        },
    ]
    assert d4.check_inventory(expected, rows)[2] == {0: 1, 1: 1}
    with pytest.raises(ValueError, match="omission"):
        d4.check_inventory(expected, rows[:1])
    duplicate = copy.deepcopy(rows)
    duplicate[1]["labels"] = [0, 0]
    with pytest.raises(ValueError, match="duplicate"):
        d4.check_inventory(expected, duplicate)
    wrong = copy.deepcopy(rows)
    wrong[1]["vertices"][1][0] = "2"
    with pytest.raises(ValueError, match="vertices"):
        d4.check_inventory(expected, wrong)


def test_surviving_assignment_is_not_reported_unsat() -> None:
    _, canonical = d4.canonical_masks()
    labels = [(cell, cell, cell, cell) for cell in range(16)]
    with pytest.raises(ValueError, match="assignment survives case 999"):
        d4.solve_non_target_cases(labels, set(), canonical, time.monotonic() + 2)


def test_finite_deadline_rejects_expired_work() -> None:
    with pytest.raises(TimeoutError, match="wall ceiling"):
        d4.check_deadline(time.monotonic() - 1)
