"""Focused repeated-condition controls for the full r1 node adapter."""

from __future__ import annotations

import copy
import time
from fractions import Fraction as Q
from typing import Any

import pytest

from devtools import check_n11_capture_branch_r1 as branch
from devtools import check_n11_capture_branch_r1_node as node
from devtools import check_n11_capture_root_pilot as pilot
from devtools import check_n11_optimality_field_mask0 as geometry


def source_cells() -> dict[int, list[dict[str, Any]]]:
    cells: dict[int, list[dict[str, Any]]] = {}
    for owner in pilot.MASK:
        cells[owner] = [
            {
                "reference": {"kind": "phase3", "node": branch.R1_NODE, "step": 0, "row": 0},
                "interval": ["0", "1"],
                "outer_domain": [["0", "0"], ["4", "0"], ["4", "4"], ["0", "4"]],
                "residual_polygons": [],
            }
        ]
    return cells


def test_condition_reapplied_without_mutating_accepted_rows() -> None:
    cells = source_cells()
    original = copy.deepcopy(cells)
    visible = node.conditional_view(cells)
    bound = -branch.center_cut()[2]
    assert cells == original
    assert all(Q(y) >= bound for _, y in visible[15][0]["outer_domain"])
    assert visible[13] == original[13]

    # A later promoted support may overreach the branch. The next view clips it again.
    cells[15][0]["outer_domain"] = [["0", "0"], ["4", "0"], ["4", "4"], ["0", "4"]]
    assert all(Q(y) >= bound for _, y in node.conditional_view(cells)[15][0]["outer_domain"])


def test_wrong_step_prior_refuses_before_row_work() -> None:
    groups = {owner: [(Q(), Q())] for owner in pilot.MASK}
    cells = source_cells()
    worlds = {owner: [(Q(), Q())] for owner in range(16)}
    source = {
        "step": {
            "index": 0,
            "owner": 15,
            "allowed_half_angle": ["0", "1"],
            "prior_owned_hulls": {str(owner): [["1", "1"]] for owner in pilot.MASK},
            "rows": [],
        }
    }
    with pytest.raises(ValueError, match="prior ownership"):
        node.check_step(
            source,
            groups,
            cells,
            worlds,
            workers=1,
            budget=geometry.Budget(time.monotonic() + 2, 1000),
            progress={"steps": []},
        )
