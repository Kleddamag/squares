"""Controls for the flag diagnosis tool: survivors read from a saved node, survivor samples,
the constraint breakdown, the largest-side bisection and the exact check."""

from __future__ import annotations

import gzip
import json
import math
from fractions import Fraction
from functools import cache
from pathlib import Path

import numpy as np

from devtools import diagnose_n17_flag as diagnosis
from devtools import select_n17_sub_patterns as selector
from devtools.check_n17_subpattern import canonical_bytes


@cache
def cover() -> selector.Geometry:
    return selector.cover_geometry()


def box(x0: str, x1: str, y0: str, y1: str) -> list[list[str]]:
    return [[x0, y0], [x1, y0], [x1, y1], [x0, y1]]


def toy_node(path: Path) -> Path:
    """A saved node holding only what the survivors are read from, with one step after it:
    corner-SW live on its first row only, side-S0 live on both rows."""
    node = {
        "final_state": {
            "cells": {
                "0": [
                    {
                        "interval": ["0", "1/2"],
                        "residual_polygons": [box("1/2", "3/5", "1/2", "3/5")],
                    },
                    {"interval": ["1/2", "1"], "residual_polygons": []},
                ],
                "4": [
                    {
                        "interval": ["0", "1/2"],
                        "residual_polygons": [box("3/2", "8/5", "1/2", "3/5")],
                    },
                    {
                        "interval": ["1/2", "1"],
                        "residual_polygons": [box("3/2", "8/5", "1/2", "3/5")],
                    },
                ],
            },
            "groups": {"0": box("1/2", "1", "1/2", "1"), "4": box("3/2", "2", "1/2", "1")},
        },
        "mask": [0, 4],
        "node_id": "toy",
        "steps": [{"owner": 0}],
    }
    target = path / "node-toy.json.gz"
    target.write_bytes(gzip.compress(canonical_bytes(node), mtime=0))
    return target


def test_survivors_are_read_off_the_front_of_a_saved_node(tmp_path: Path) -> None:
    survivors = diagnosis.read_survivors(toy_node(tmp_path), cover().names)
    assert survivors.mask == (0, 4)
    corner, side = survivors.owners
    assert (corner.name, len(corner.live_rows()), len(side.live_rows())) == ("corner-SW", 1, 2)
    summary = diagnosis.summarise(survivors)
    assert summary["live_rows"] == 3
    (block,) = summary["owners"]["corner-SW"]["blocks"]
    assert {key: block[key] for key in ("degrees", "rows", "x", "y")} == {
        "degrees": [0.0, round(math.degrees(2 * math.atan(0.5)), 4)],
        "rows": 1,
        "x": [0.5, 0.6],
        "y": [0.5, 0.6],
    }
    assert math.isclose(block["largest_residual_area"], 0.01)
    assert summary["owners"]["side-S0"]["blocks"][0]["degrees"] == [0.0, 90.0]
    # The first row holds turns below 2 atan(1/2), about 53.13 degrees, and the second
    # row of corner-SW is dead, so the same centre at 60 degrees is outside.
    assert corner.holds((0.55, 0.55, math.radians(20)))
    assert not corner.holds((0.55, 0.55, math.radians(60)))
    assert not corner.holds((0.7, 0.55, math.radians(20)))
    # Angles are taken modulo a quarter turn.
    assert corner.holds((0.55, 0.55, math.radians(110)))


def test_survivor_samples_lie_in_the_survivors(tmp_path: Path) -> None:
    survivors = diagnosis.read_survivors(toy_node(tmp_path), cover().names)
    rng = np.random.default_rng(3)
    for _ in range(50):
        pose = diagnosis.sample_pose(survivors, rng)
        assert all(diagnosis.in_survivors(survivors, pose))
        assert pose[0, 2] <= 2 * math.atan(0.5) + 1e-12


def test_the_breakdown_names_the_selectors_violation() -> None:
    geometry = cover()
    cells = (0, 4, 6)
    problem = selector.Problem(geometry, cells)
    rng = np.random.default_rng(5)
    for _ in range(20):
        pose = problem.random_pose(rng)
        rows = diagnosis.breakdown(geometry, cells, pose, limit=1000)
        least = min(row["gap"] for row in rows)
        assert math.isclose(max(-least, 0.0), problem.violation(pose), abs_tol=2e-7)


def test_largest_side_finds_the_spacing_of_two_cells() -> None:
    """Two point-like cells 0.9 apart on a line: squares of side above 0.9 cannot fit."""
    epsilon = 1e-3
    geometry = selector.make_geometry(
        [
            np.array(
                [
                    [2.0, 2.0],
                    [2.0 + epsilon, 2.0],
                    [2.0 + epsilon, 2.0 + epsilon],
                    [2.0, 2.0 + epsilon],
                ]
            ),
            np.array(
                [
                    [2.9, 2.0],
                    [2.9 + epsilon, 2.0],
                    [2.9 + epsilon, 2.0 + epsilon],
                    [2.9, 2.0 + epsilon],
                ]
            ),
        ],
        ["a", "b"],
        cap=5.0,
    )
    start = np.array([[2.0, 2.0, 0.3], [2.9, 2.0, 0.1]])
    result = diagnosis.largest_side(geometry, (0, 1), start, low=0.8, steps=10, starts=4)
    assert 0.89 < result["placed_side"] <= 0.9 + 2 * epsilon
    assert result["first_unplaced_side"] > result["placed_side"]
    roomy = diagnosis.largest_side(
        geometry, (0, 1), start, low=0.5, high=0.8, steps=4, starts=2
    )
    assert roomy["first_unplaced_side"] is None
    assert roomy["placed_side"] > 0.75


def test_the_exact_check_admits_touching_and_refuses_overlap() -> None:
    names = ["corner-SW", "side-S0"]
    half, one = Fraction(1, 2), Fraction(3, 2)
    touching = diagnosis.exact_check(
        names, [(half, half, Fraction(0)), (one, half, Fraction(0))], selector.DEFAULT_DESIGN
    )
    assert touching["valid"]
    assert touching["touching_pairs"] == 1
    assert touching["least_pair_gap"] == 0.0
    overlapping = diagnosis.exact_check(
        names,
        [(half, half, Fraction(0)), (one - Fraction(1, 10**9), half, Fraction(0))],
        selector.DEFAULT_DESIGN,
    )
    assert not overlapping["valid"]
    assert overlapping["packing_failures"][0][0] == "overlap"
    outside = diagnosis.exact_check(
        names,
        [(half, half, Fraction(0)), (Fraction(5, 2), half, Fraction(0))],
        selector.DEFAULT_DESIGN,
    )
    assert outside["centres_outside_cells"] == ["side-S0"]


def test_rational_poses_round_the_half_angle() -> None:
    pose = np.array([[1.0, 2.0, math.radians(30)], [1.5, 0.75, math.radians(100)]])
    rows = diagnosis.rational_pose(pose, angle_denominator=10**9)
    assert rows[0][:2] == (Fraction(1), Fraction(2))
    assert math.isclose(2 * math.atan(float(rows[0][2])), math.radians(30), abs_tol=1e-8)
    assert math.isclose(2 * math.atan(float(rows[1][2])), math.radians(10), abs_tol=1e-8)
    square = diagnosis.exact_square(*rows[0])
    edge = (square[1][0] - square[0][0]) ** 2 + (square[1][1] - square[0][1]) ** 2
    assert edge == 1


def test_row_losses_follow_the_row_width_and_the_walls() -> None:
    row = diagnosis.Row(0.0, 1 / 64, (np.array([[2.0, 2.0], [2.1, 2.0], [2.1, 2.1]]),))
    width = 2 * math.atan(1 / 64)
    losses = diagnosis.row_losses(row, selector.CAP)
    assert math.isclose(losses["core"], 0.5 - 0.5 / (math.cos(width / 2) + math.sin(width / 2)))
    assert losses["wall"] == 0.0
    near = diagnosis.Row(0.0, 1 / 64, (np.array([[0.5, 2.0], [0.6, 2.0], [0.6, 2.1]]),))
    assert math.isclose(
        diagnosis.row_losses(near, selector.CAP)["wall"],
        diagnosis.half_extent(width) - 0.5,
    )


def test_the_ideal_owned_region_shrinks_with_the_survivors(tmp_path: Path) -> None:
    survivors = diagnosis.read_survivors(toy_node(tmp_path), cover().names)
    corner, side = survivors.owners
    pinned = diagnosis.Row(0.0, 1e-9, (np.array([[0.55, 0.55], [0.55 + 1e-9, 0.55]]),))
    assert math.isclose(
        diagnosis.polygon_area(diagnosis.ideal_owned([pinned], angles_per_row=2)),
        1.0,
        rel_tol=1e-6,
    )
    one_row = diagnosis.polygon_area(diagnosis.ideal_owned(corner.live_rows()))
    every_turn = diagnosis.polygon_area(diagnosis.ideal_owned(side.live_rows()))
    assert 0.0 < every_turn < one_row < 1.0
    sectors = diagnosis.sector_owned(side)
    assert [sector["degrees"][0] for sector in sectors] == [0.0, 15.0, 30.0, 45.0, 60.0, 75.0]
    # The areas are recorded to six places.
    assert all(sector["ideal_owned_area"] >= every_turn - 1e-6 for sector in sectors)


def test_pair_gaps_are_the_breakdowns_pair_gaps() -> None:
    geometry = cover()
    cells = (0, 4)
    problem = selector.Problem(geometry, cells)
    rng = np.random.default_rng(11)
    for _ in range(20):
        pose = problem.random_pose(rng)
        (pair,) = [
            row
            for row in diagnosis.breakdown(geometry, cells, pose, limit=1000)
            if row["kind"] == "pair"
        ]
        gap = float(diagnosis.pair_gaps(pose[0], pose[1:])[0])
        assert math.isclose(gap, pair["gap"], abs_tol=1e-6)


def test_support_finds_a_clear_partner_and_measures_a_crowded_one(tmp_path: Path) -> None:
    survivors = diagnosis.read_survivors(toy_node(tmp_path), cover().names)
    _, side = survivors.owners
    rng = np.random.default_rng(2)
    pool = diagnosis.make_pool(side, rng)
    assert len(pool.poses) == 2 * 7 * 3
    # Corner-SW upright at x = 0.55: side-S0 upright at x >= 1.55 clears it.
    clear = diagnosis.best_support(np.array([0.55, 0.55, 0.0]), side, pool, rng, refine=50)
    assert clear >= 0.0
    # Turned 30 degrees at x = 0.6 it reaches past 1.28, and every side-S0 pose is in
    # [1.5, 1.6] x [0.5, 0.6]: no pose of the partner clears it.
    crowded = diagnosis.best_support(
        np.array([0.6, 0.55, math.radians(30)]), side, pool, rng, refine=50
    )
    assert crowded < 0.0
    record = diagnosis.pairwise_support(cover(), survivors, samples=10, seed=1, refine=10)
    assert set(record["owners"]) == {"corner-SW", "side-S0"}
    assert all(0.0 <= owner["supported_share"] <= 1.0 for owner in record["owners"].values())


def test_the_searches_and_the_profile_run_from_the_survivors(tmp_path: Path) -> None:
    geometry = cover()
    survivors = diagnosis.read_survivors(toy_node(tmp_path), geometry.names)
    spread = diagnosis.multistart(geometry, survivors, starts=3, seed=1)
    assert spread["placed"]
    found = diagnosis.selector_search(
        geometry,
        survivors,
        warm_count=2,
        seed=1,
        budget=selector.Budget(starts=2, hops=2, deep_starts=2, deep_hops=2),
    )
    assert found["placed"]
    assert found["found_by"] == "warm"
    profile = diagnosis.angle_profile(
        geometry,
        survivors,
        1,
        [0.0, 30.0],
        best_pose=np.array(found["best_pose"]),
        starts=2,
        seed=1,
    )
    assert [point["degrees"] for point in profile] == [0.0, 30.0]
    assert profile[0]["violation"] <= selector.MARGIN


def test_a_rounded_placement_is_recorded_and_rechecked_exactly(tmp_path: Path) -> None:
    pose = np.array([[0.6, 0.6, 0.0], [1.7, 0.6, 0.1]])
    record = diagnosis.placement_record(cover(), (0, 4), pose, selector.DEFAULT_DESIGN)
    assert record["schema"] == diagnosis.PLACEMENT_SCHEMA
    assert record["exact"]["valid"]
    receipt = tmp_path / "placement.json"
    receipt.write_text(json.dumps({"placement": record}), encoding="utf-8")
    assert diagnosis.main(["check", str(receipt)]) == 0
    record["squares"][1]["x"] = "3/2"
    receipt.write_text(json.dumps(record), encoding="utf-8")
    assert diagnosis.main(["check", str(receipt)]) == 2


def test_the_domains_command_names_the_node_by_its_file(tmp_path: Path) -> None:
    output = tmp_path / "domains.json"
    assert diagnosis.main(["domains", str(toy_node(tmp_path)), "--output", str(output)]) == 0
    summary = json.loads(output.read_text(encoding="utf-8"))
    assert summary["node_file"] == "node-toy.json.gz"
    assert summary["owners"]["side-S0"]["rows_by_chart_width"] == {"1/2": 2}
