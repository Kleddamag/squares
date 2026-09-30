"""Focused reference and closed-angle controls for root-node continuation."""

from __future__ import annotations

import time
from fractions import Fraction as Q

import pytest

from devtools import check_n11_capture_root_node as node
from devtools import check_n11_optimality_field_mask0 as geometry


def reference() -> dict[str, object]:
    return {"kind": "phase3", "node": "root-self-240", "step": 0, "row": 0}


def predecessor() -> dict[str, object]:
    return {
        "reference": reference(),
        "interval": ["0", "1"],
        "outer_domain": [["0", "0"], ["1", "0"], ["1", "1"], ["0", "1"]],
        "residual_polygons": [],
    }


def test_phase_three_predecessor_reference_and_closed_interval() -> None:
    lookup = node.row_lookup([predecessor()])
    row = {
        "prior_reference": reference(),
        "interval": ["1/4", "1/2"],
        "self_hull_cuts": [],
    }
    lo, hi, domain = node.inherited_domain(row, lookup, [(Q(), Q())])
    assert (lo, hi) == (Q(1, 4), Q(1, 2))
    assert domain == [(Q(), Q()), (Q(1), Q()), (Q(1), Q(1)), (Q(), Q(1))]

    with pytest.raises(ValueError, match="unaccepted predecessor"):
        node.inherited_domain(
            {**row, "prior_reference": {**reference(), "row": 1}}, lookup, [(Q(), Q())]
        )
    with pytest.raises(ValueError, match="escapes prior"):
        node.inherited_domain({**row, "interval": ["1/2", "5/4"]}, lookup, [(Q(), Q())])


def test_partner_cover_requires_complete_partition_and_strict_cores() -> None:
    prior = [predecessor()]
    core = [["-1/10", "-1/10"], ["1/10", "-1/10"], ["1/10", "1/10"], ["-1/10", "1/10"]]
    domain = prior[0]["outer_domain"]
    rows = [
        {
            "reference": reference(),
            "interval": ["0", "1/2"],
            "domain": domain,
            "core": core,
            "self_hull_cuts": [],
        },
        {
            "reference": reference(),
            "interval": ["1/2", "1"],
            "domain": domain,
            "core": core,
            "self_hull_cuts": [],
        },
    ]
    budget = geometry.Budget(time.monotonic() + 3, 1000)
    live, count = node.partner_cover(rows, prior, [(Q(), Q())], budget=budget)
    assert count == 2
    assert len(live) == 2
    with pytest.raises(ValueError, match="gap or overlap"):
        node.partner_cover(
            [rows[0], {**rows[1], "interval": ["3/4", "1"]}], prior, [(Q(), Q())], budget=budget
        )
    with pytest.raises(ValueError, match="unaccepted predecessor"):
        node.partner_cover(
            [{**rows[0], "reference": {**reference(), "row": 9}}, rows[1]],
            prior,
            [(Q(), Q())],
            budget=budget,
        )
