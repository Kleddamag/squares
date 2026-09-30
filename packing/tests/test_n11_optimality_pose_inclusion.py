"""Closed-domain and omission controls for the conditional case-438 pose check."""

from __future__ import annotations

import copy
import gzip
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from unittest.mock import patch

import pytest

from devtools import check_n11_optimality_pose_inclusion as pose

Q = Fraction
RECEIPT = (
    Path(__file__).parents[1]
    / "resources/web/n11-optimality-2026-09-29/receipts/pose-inclusion"
)
FOCUSED = (
    Path(__file__).parents[1]
    / "resources/web/n11-optimality-2026-09-29/receipts/local-dual-residual/objects"
    / "9a9cf4e0fdcb1b1d226b9c07ec08d08cbbc572749cec9bc09cf3cd92bd4d88f3.gz"
)


def inputs() -> tuple[dict, dict, list[Q], Q, Q]:
    data = json.loads(gzip.decompress((RECEIPT / "derived-state.json.gz").read_bytes()))
    guard = json.loads((RECEIPT / "guard.json").read_text())
    focused = json.loads(gzip.decompress(FOCUSED.read_bytes()))
    lo, hi, _ = pose.root_interval()
    return data, guard, list(map(Q, focused["radii"])), lo, hi


def test_closed_angle_charts_and_inverse_center() -> None:
    assert pose.axis_angle_bound(Q(0), Q(0)) == 0
    assert pose.axis_angle_bound(Q(1), Q(1)) == 0
    assert pose.slanted_angle_bound(Q(1, 3), Q(1, 3), Q(1, 3), Q(1, 3)) == 0
    assert pose.inverse_center(["3", "4"], Q(1), Q(2)) == (Q(3), Q(-2))
    with pytest.raises(ValueError, match="remote chart"):
        pose.axis_angle_bound(Q(1, 3), Q(2, 3))
    with pytest.raises(ValueError, match="quarter-turn cut"):
        pose.slanted_angle_bound(Q(0), Q(2, 3), Q(1, 3), Q(1, 3))
    radius = Q(1, 4)
    assert pose.required_center_radius(radius, (Q(0), Q(0))) == radius
    assert pose.required_center_radius(radius + Q(1, 10**12), (Q(0), Q(0))) > radius
    assert pose.axis_angle_bound(Q(0), radius / 2 + Q(1, 10**12)) > radius


def test_complete_live_inventory_and_scope() -> None:
    data, guard, radii, lo, hi = inputs()
    checked = pose.check_pose(data, guard, radii, lo, hi)
    result = json.loads((RECEIPT / "result.json").read_text())
    assert checked["live_rows_checked"] == 136
    assert checked["vertices_checked"] == 1542
    assert checked["zero_endpoint_observed"]
    assert checked["one_endpoint_observed"]
    assert result["status"] == "PASS_POSE_INCLUSION"
    assert result["conditional_on_source_pose_domains"] is True
    assert result["source_geometry_ancestry_proved"] is False
    assert result["case_438_capture_proved"] is False
    assert result["global_optimality_proved"] is False
    assert (
        hashlib.sha256((RECEIPT / "derived-state.json.gz").read_bytes()).hexdigest()
        == result["derived_state_gzip_sha256"]
    )
    assert hashlib.sha256((RECEIPT / "guard.json").read_bytes()).hexdigest() == pose.GUARD_SHA


def test_unbound_pose_source_refuses(tmp_path: Path) -> None:
    altered = tmp_path / "near.json"
    altered.write_text('{"final_state": {}}')
    with pytest.raises(ValueError, match="identity mismatch"):
        pose.extract_source(altered, 1)


def test_missing_owner_row_vertex_and_duplicate_role_refuse() -> None:
    data, guard, radii, lo, hi = inputs()
    missing_owner = copy.deepcopy(data)
    del missing_owner["final_state"]["cells"]["3"]
    with pytest.raises(ValueError, match="owner inventory"):
        pose.check_pose(missing_owner, guard, radii, lo, hi)

    duplicate_role = copy.deepcopy(guard)
    duplicate_role["guards"] = [
        entry for entry in duplicate_role["guards"] if entry["mask"] == pose.MASK
    ]
    duplicate_role["guards"][0]["roles"][0]["label"] = 1
    with pytest.raises(ValueError, match="not bijective"):
        pose.check_pose(data, duplicate_role, radii, lo, hi)

    missing_row = copy.deepcopy(data)
    missing_row["final_state"]["cells"]["3"]["live_rows"].pop()
    with pytest.raises(ValueError, match="census mismatch"):
        pose.check_pose(missing_row, guard, radii, lo, hi)

    missing_vertex = copy.deepcopy(data)
    rows = missing_vertex["final_state"]["cells"]["3"]["live_rows"]
    polygon = next(poly for row in rows for poly in row["residual_polygons"] if len(poly) > 1)
    polygon.pop()
    with pytest.raises(ValueError, match="census mismatch"):
        pose.check_pose(missing_vertex, guard, radii, lo, hi)


def test_wrong_frame_and_outside_domain_refuse() -> None:
    data, guard, radii, lo, hi = inputs()
    wrong_frame = copy.deepcopy(data)
    wrong_frame["B"] = "1"
    with pytest.raises(ValueError, match="field scale"):
        pose.check_pose(wrong_frame, guard, radii, lo, hi)

    outside = copy.deepcopy(data)
    outside["final_state"]["cells"]["3"]["live_rows"][0]["residual_polygons"][0][0] = ["0", "0"]
    with pytest.raises(ValueError, match="exceeds accepted rectangle"):
        pose.check_pose(outside, guard, radii, lo, hi)


def test_singleton_row_and_polygon_are_kept_when_inside() -> None:
    data, guard, radii, lo, hi = inputs()
    cell = data["final_state"]["cells"]["3"]
    axis_row = next(row for row in cell["live_rows"] if row["interval"][0] == "0")
    axis_row["interval"] = ["0", "0"]
    polygon = next(
        poly for row in cell["live_rows"] for poly in row["residual_polygons"] if len(poly) > 1
    )
    removed = len(polygon) - 1
    del polygon[1:]
    with patch.object(pose, "VERTICES", pose.VERTICES - removed):
        checked = pose.check_pose(data, guard, radii, lo, hi)
    assert checked["vertices_checked"] == 1542 - removed
    assert checked["singleton_polygons_checked"] >= 1
