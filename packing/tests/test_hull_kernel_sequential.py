"""The sequential mode-A checker certifies what the simple producer proposes, and no more."""

from __future__ import annotations

import copy
import time
from fractions import Fraction as Q
from typing import Any

import pytest

from devtools import check_hull_kernel_mask0 as mask0_tool
from devtools import check_n17_subpattern as tool
from sqpack.hull_kernel import Budget, RefusalError, node, producer, sequential
from sqpack.hull_kernel.frame import Frame, make_frame
from sqpack.hull_kernel.geometry import Polygon


def budget() -> Budget:
    return Budget(time.monotonic() + 60, 200_000)


def box(x0: Q, x1: Q, y0: Q, y1: Q) -> Polygon:
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


@pytest.fixture(scope="module")
def pair() -> Frame:
    """Two small cells whose union has diameter below one: two centres cannot both fit."""
    return make_frame(
        name="pair",
        cap=Q(3),
        length=Q(3),
        cells=[
            box(Q(5, 4), Q(3, 2), Q(7, 5), Q(8, 5)),
            box(Q(3, 2), Q(7, 4), Q(7, 5), Q(8, 5)),
        ],
        cell_names=["west", "east"],
        occupancy=2,
        action_names=("r0",),
    )


@pytest.fixture(scope="module")
def n17_frame() -> Frame:
    return mask0_tool.n17_unique_frame()


def certify(frame: Frame, production: producer.Production, mask: list[int], bins: int) -> Any:
    seed = node.admit_seed(
        frame, production.seed, mask=mask, bins=bins, budget=budget(), allow_empty_groups=True
    )
    return sequential.replay_sequential(
        frame,
        production.node,
        seed,
        mask=mask,
        seed_sha256=producer.content_sha256(production.seed),
        budget=budget(),
    )


def test_a_pair_closer_than_one_closes_at_its_first_update(pair: Frame) -> None:
    production = producer.produce(pair, [0, 1], bins=8, max_rounds=2, budget=budget())
    assert production.outcome == "closed"
    trace = certify(pair, production, [0, 1], 8)
    assert trace.closure == {"kind": "all_parent_poses_forbidden", "owner": 0, "step": 0}
    assert pair.states_containing([0, 1]) == [0]


def test_a_declared_closure_must_be_the_derived_one(pair: Frame) -> None:
    production = producer.produce(pair, [0, 1], bins=8, max_rounds=2, budget=budget())
    production.node["contradiction"] = {
        "kind": "all_parent_poses_forbidden",
        "owner": 1,
        "step": 0,
    }
    with pytest.raises(RefusalError, match="declared closure differs"):
        certify(pair, production, [0, 1], 8)


def test_a_removed_residual_or_a_claimed_closure_on_a_stall_is_refused(
    n17_frame: Frame,
) -> None:
    mask = sorted(n17_frame.cell_names.index(cell) for cell in tool.PATTERNS["A"])
    production = producer.produce(
        n17_frame, mask, bins=4, max_rounds=1, budget=budget(), collision=False
    )
    trace = certify(n17_frame, production, mask, 4)
    assert trace.closure is None
    live = next(
        (index, row)
        for index, row in enumerate(production.node["steps"][0]["rows"])
        if row["residual_polygons"]
    )
    cut = copy.deepcopy(production)
    cut.node["steps"][0]["rows"][live[0]]["residual_polygons"] = []
    with pytest.raises(RefusalError, match=r"uncovered|facets"):
        certify(n17_frame, cut, mask, 4)
    claimed = copy.deepcopy(production)
    claimed.node["contradiction"] = {
        "kind": "all_parent_poses_forbidden",
        "owner": mask[0],
        "step": 0,
    }
    claimed.node["closed"] = claimed.node["terminal"] = True
    with pytest.raises(RefusalError, match="declared closure differs"):
        certify(n17_frame, claimed, mask, 4)


def test_pattern_a_stalls_at_four_bins_with_its_extents(n17_frame: Frame) -> None:
    result = tool.run(
        n17_frame,
        tool.PATTERNS["A"],
        name="A",
        bins=4,
        max_rounds=2,
        max_seconds=60,
        cover="indexed",
        collision=False,
    )
    assert result["status"] == "PASS_CERTIFIED_STALL"
    assert result["excluded_orbits"] == 0
    assert len(result["final_extents"]) == 6
    assert result["seed_points"]["interior-W"] == 0
    assert result["seed_points"]["interior-SW"] > 0


def test_the_endpoint_sub_pattern_stalls(n17_frame: Frame) -> None:
    result = tool.run(
        n17_frame,
        tool.PATTERNS["endpoint6"],
        name="endpoint6",
        bins=4,
        max_rounds=1,
        max_seconds=60,
        cover="indexed",
    )
    assert result["status"] == "PASS_CONTROL_STALLED"
    assert result["closure"] is None


@pytest.fixture(scope="module")
def blind_pair() -> Frame:
    """Two near-equilateral cells of side about 0.9 whose union has diameter below one.

    Each cell's least enclosing radius (about 0.52) exceeds one half, so no point is owned
    from either cell alone; two centres in them are under one apart, so the pair is
    infeasible, and only collision against the partner's pose cover can show it.
    """
    triangle = [(Q(1), Q(1)), (Q(19, 10), Q(1)), (Q(29, 20), Q(89, 50))]
    shifted = [(x + Q(1, 100), y) for x, y in triangle]
    return make_frame(
        name="blind-pair",
        cap=Q(3),
        length=Q(3),
        cells=[triangle, shifted],
        cell_names=["left", "right"],
        occupancy=2,
        action_names=("r0",),
    )


def test_a_blind_pair_closes_through_collision_alone(blind_pair: Frame) -> None:
    production = producer.produce(blind_pair, [0, 1], bins=16, max_rounds=2, budget=budget())
    assert production.seed["groups"] == {"0": [], "1": []}
    trace = certify(blind_pair, production, [0, 1], 16)
    assert trace.closure is not None
    assert trace.closure["kind"] == "all_parent_poses_forbidden"
    assert trace.groups == {0: [], 1: []}
    assert trace.steps[-1]["collision_regions"] > 0
    without = producer.produce(
        blind_pair, [0, 1], bins=16, max_rounds=2, budget=budget(), collision=False
    )
    assert certify(blind_pair, without, [0, 1], 16).closure is None


def test_a_forged_collision_region_or_partner_cover_is_refused(blind_pair: Frame) -> None:
    production = producer.produce(blind_pair, [0, 1], bins=16, max_rounds=2, budget=budget())
    step = production.node["steps"][-1]
    index, row = next(
        (index, row) for index, row in enumerate(step["rows"]) if row["collision_regions"]
    )
    forged = copy.deepcopy(production)
    region = forged.node["steps"][-1]["rows"][index]["collision_regions"][0]
    region["vertices"] = [[str(Q(x) + Q(1, 2)), y] for x, y in region["vertices"]]
    with pytest.raises(RefusalError, match="escapes"):
        certify(blind_pair, forged, [0, 1], 16)
    partner = str(row["collision_regions"][0]["partner"])
    shrunk = copy.deepcopy(production)
    cover = shrunk.node["steps"][-1]["prior_partner_pose_covers"][partner]
    live = next(item for item in cover if item["domain"])
    live["domain"] = live["domain"][:1]
    with pytest.raises(RefusalError, match="partner cover domain differs"):
        certify(blind_pair, shrunk, [0, 1], 16)
