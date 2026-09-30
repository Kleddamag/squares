"""Focused controls for the accepted root-to-capture input bridge."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

import pytest

from devtools import check_n11_capture_root_bridge as bridge
from devtools import check_n11_capture_root_pilot as pilot


def fixture() -> tuple[dict[str, Any], list[list[list[str]]], dict[int, int]]:
    groups = {str(owner): [[str(owner), "0"]] for owner in pilot.MASK}
    counts: dict[int, int] = dict.fromkeys(pilot.MASK, 2)
    refs = {
        str(owner): [
            {"kind": "phase2", "round": 14, "owner": owner, "row": row} for row in range(2)
        ]
        for owner in pilot.MASK
    }
    owned = [[str(owner), "0"] for owner in range(16)]
    return {"groups": groups, "cell_references": refs}, [[point] for point in owned], counts


def test_exact_hulls_and_full_row_references() -> None:
    initial, owned, counts = fixture()
    census = bridge.check_hulls_and_refs(initial, owned, counts)
    assert len(census) == len(pilot.MASK)
    assert sum(item["rows"] for item in census) == 2 * len(pilot.MASK)

    altered = deepcopy(initial)
    altered["groups"]["15"] = [["16", "0"]]
    with pytest.raises(ValueError, match="initial hull differs"):
        bridge.check_hulls_and_refs(altered, owned, counts)

    omitted = deepcopy(initial)
    omitted["cell_references"]["15"].pop()
    with pytest.raises(ValueError, match="row references differ"):
        bridge.check_hulls_and_refs(omitted, owned, counts)

    reordered = deepcopy(initial)
    reordered["cell_references"]["15"].reverse()
    with pytest.raises(ValueError, match="row references differ"):
        bridge.check_hulls_and_refs(reordered, owned, counts)
