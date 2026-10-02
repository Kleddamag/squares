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
    production = producer.produce(n17_frame, mask, bins=4, max_rounds=1, budget=budget())
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
        max_rounds=2,
        max_seconds=60,
        cover="indexed",
    )
    assert result["status"] == "PASS_CONTROL_STALLED"
    assert result["closure"] is None
