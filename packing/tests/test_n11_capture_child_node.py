"""Closed branch, parent-binding, and terminal controls for child replay."""

from __future__ import annotations

import copy
from fractions import Fraction as Q
from typing import Any

import pytest

from devtools import check_n11_capture_child_node as child
from devtools import check_n11_capture_root_pilot as pilot


def sample_cells() -> dict[int, list[dict[str, Any]]]:
    cells: dict[int, list[dict[str, Any]]] = {}
    for owner in pilot.MASK:
        intervals = [("0", "1/2"), ("1/2", "1")] if owner == 13 else [("0", "1")]
        cells[owner] = [
            {
                "reference": {"kind": "phase3", "node": "parent", "step": 0, "row": index},
                "interval": [lo, hi],
                "outer_domain": [["0", "0"], ["4", "0"], ["4", "4"], ["0", "4"]],
                "residual_polygons": [],
            }
            for index, (lo, hi) in enumerate(intervals)
        ]
    return cells


def test_closed_angle_boundary_and_center_cut_reapplied() -> None:
    cells = sample_cells()
    original = copy.deepcopy(cells)
    conditions = [child.center_constraint("ge"), child.angle_constraint(13, Q(1, 2), "ge")]
    visible = child.conditional_view(cells, conditions)
    assert cells == original
    assert [row["interval"] for row in visible[13]] == [["1/2", "1"]]
    assert visible[13][0]["reference"] == original[13][1]["reference"]
    bound = -Q(child.center_constraint("ge")["upper_field"])
    assert all(Q(y) >= bound for _, y in visible[15][0]["outer_domain"])
    assert any(Q(y) == bound for _, y in visible[15][0]["outer_domain"])

    # A zero-width touching row cannot replace the positive-width closed cover.
    cells[13] = cells[13][:1]
    with pytest.raises(ValueError, match="inherited closed angle incomplete"):
        child.conditional_view(cells, conditions)


def test_terminal_requires_every_residual_and_outer_domain_empty() -> None:
    empty = {"residual_polygons": [], "outer_domain": []}
    assert child.terminal_rows_empty([empty, empty])
    assert not child.terminal_rows_empty([empty, {**empty, "residual_polygons": [["0", "0"]]}])
    assert not child.terminal_rows_empty([empty, {**empty, "outer_domain": [["0", "0"]]}])


def test_pin_requires_actual_parent_checker_and_scope() -> None:
    pin = child.PINS["r10"]
    accepted = {
        "status": pin.parent_status,
        "r1_node_state_checked": True,
        "capture_tree_proved": False,
        "candidate_capture_proved": False,
        "global_optimality_proved": False,
        "checker_sha256": pin.parent_checker_sha,
        "r1_source_sha256": pin.parent_source_sha,
        "root_result_sha256": child.branch.ROOT_RESULT_SHA,
        "steps_checked": 9,
        "steps": [{"index": index, "complete": index < 8} for index in range(9)],
    }
    child.admit_parent(accepted, pin)
    with pytest.raises(ValueError, match="checker or accepted scope"):
        child.admit_parent({**accepted, "checker_sha256": "wrong"}, pin)
    with pytest.raises(ValueError, match="accepted complete r1"):
        child.admit_parent({**accepted, "steps_checked": 8}, pin)


def test_grandchild_requires_complete_reviewed_parent_shape() -> None:
    pin = child.PINS["far13"]
    accepted = {
        "status": pin.parent_status,
        "child_node_state_checked": True,
        "terminal_empty_pose_checked": False,
        "capture_tree_proved": False,
        "candidate_capture_proved": False,
        "global_optimality_proved": False,
        "checker_sha256": pin.parent_checker_sha,
        "child_source_sha256": pin.parent_source_sha,
        "final_state_canonical_sha256": pin.parent_final_sha,
        "node_id": "r10-portable-v1",
        "steps_checked": 13,
        "steps": [{"index": index, "complete": index < 12} for index in range(13)],
    }
    child.admit_parent(accepted, pin)
    with pytest.raises(ValueError, match="accepted complete pinned child"):
        child.admit_parent({**accepted, "node_id": "near13-self-180"}, pin)
    with pytest.raises(ValueError, match="accepted complete pinned child"):
        child.admit_parent({**accepted, "steps": accepted["steps"][:-1]}, pin)
    with pytest.raises(ValueError, match="accepted complete pinned child"):
        child.admit_parent(
            {**accepted, "steps": [*accepted["steps"][:-1], {"index": 12, "complete": True}]},
            pin,
        )


def test_last_complete_update_uses_final_state_instead_of_missing_successor() -> None:
    pin = child.PINS["near13"]
    groups = {owner: [(Q(owner), Q())] for owner in pilot.MASK}
    next_group = [(Q(3), Q()), (Q(4), Q())]
    child.check_next_prior(None, groups, 3, next_group, index=pin.steps - 1, pin=pin)
    with pytest.raises(ValueError, match="unsupported successor"):
        child.check_next_prior({}, groups, 3, next_group, index=pin.steps - 1, pin=pin)
    with pytest.raises(ValueError, match="missing next"):
        child.check_next_prior(None, groups, 3, next_group, index=pin.steps - 2, pin=pin)
