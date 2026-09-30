"""Exact partner-cover ancestry controls, independent of case credit."""

from __future__ import annotations

import copy
import time
from fractions import Fraction as Q
from typing import Any

import pytest

from devtools import check_n11_optimality_field_mask0 as geometry
from devtools import n11_nonfield_partner as partner


def _fixture() -> tuple[dict[str, Any], dict[int, list[dict[str, Any]]]]:
    center = geometry.L / 2
    radius = geometry.B / 8
    outer = [
        [str(center - Q(1, 100)), str(center - Q(1, 100))],
        [str(center + Q(1, 100)), str(center - Q(1, 100))],
        [str(center + Q(1, 100)), str(center + Q(1, 100))],
        [str(center - Q(1, 100)), str(center + Q(1, 100))],
    ]
    core = [
        [str(-radius), str(-radius)],
        [str(radius), str(-radius)],
        [str(radius), str(radius)],
        [str(-radius), str(radius)],
    ]
    reference = {"kind": "wall_seed", "owner": 1, "row": 0}
    proposed: dict[str, Any] = {
        "1": [{"interval": ["0", "1"], "reference": reference, "domain": outer, "core": core}]
    }
    accepted = {1: [{"interval": ["0", "1"], "reference": reference, "outer_domain": outer}]}
    return proposed, accepted


def _check(
    proposed: dict[str, Any], accepted: dict[int, list[dict[str, Any]]]
) -> tuple[dict[int, list[tuple[partner.Polygon, partner.Polygon]]], dict[str, int]]:
    return partner.admitted_partner_covers(
        proposed,
        query_owner=0,
        mask=(0, 1),
        accepted_groups={0: [(Q(), Q())], 1: [(Q(1), Q(1))]},
        accepted_rows=accepted,
        budget=geometry.Budget(time.monotonic() + 30, 50_000),
    )


def test_partner_cover_binds_complete_closed_angle_and_strict_core() -> None:
    proposed, accepted = _fixture()
    live, counts = _check(proposed, accepted)
    assert counts == {"rows": 1, "empty_rows": 0, "live_rows": 1}
    assert len(live[1]) == 1


def test_partner_cover_refuses_reference_gap_and_domain_shrink() -> None:
    proposed, accepted = _fixture()
    wrong = copy.deepcopy(proposed)
    wrong["1"][0]["reference"]["row"] = 1
    with pytest.raises(ValueError, match="predecessor"):
        _check(wrong, accepted)
    wrong = copy.deepcopy(proposed)
    wrong["1"][0]["interval"] = ["0", "1/2"]
    with pytest.raises(ValueError, match="incomplete"):
        _check(wrong, accepted)
    wrong = copy.deepcopy(proposed)
    wrong["1"][0]["domain"] = [["1", "1"]]
    with pytest.raises(ValueError, match="domain differs"):
        _check(wrong, accepted)


def test_empty_partner_row_still_covers_its_full_angle() -> None:
    proposed, accepted = _fixture()
    accepted[1][0]["outer_domain"] = []
    proposed["1"][0]["domain"] = []
    proposed["1"][0]["core"] = []
    live, counts = _check(proposed, accepted)
    assert live[1] == []
    assert counts == {"rows": 1, "empty_rows": 1, "live_rows": 0}


def test_universal_collision_region_is_checked_against_every_partner_pose() -> None:
    proposed, accepted = _fixture()
    live, _ = _check(proposed, accepted)
    center = geometry.L / 2
    radius = geometry.B / 8
    core = [(-radius, -radius), (radius, -radius), (radius, radius), (-radius, radius)]
    query = live[1][0][0]
    region = {
        "partner": 1,
        "status": "EXACT_UNIVERSAL_COLLISION_KERNEL",
        "live_rows": 1,
        "vertices": [[str(x), str(y)] for x, y in query],
    }
    regions, checks = partner.admitted_collision_regions(
        [region],
        query_core=core,
        query_pre_wall_domain=query,
        partners=live,
        budget=geometry.Budget(time.monotonic() + 30, 50_000),
    )
    assert regions == [query]
    assert checks > 0
    wrong = copy.deepcopy(region)
    wrong["vertices"] = [[str(center + 1), str(center + 1)]]
    with pytest.raises(ValueError, match="query domain"):
        partner.admitted_collision_regions(
            [wrong],
            query_core=core,
            query_pre_wall_domain=query,
            partners=live,
            budget=geometry.Budget(time.monotonic() + 30, 50_000),
        )
