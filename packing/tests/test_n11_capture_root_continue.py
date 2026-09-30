"""Focused controls for inherited closed-angle residual restrictions."""

from __future__ import annotations

from fractions import Fraction as Q

import pytest

from devtools import check_n11_capture_root_continue as continuation
from devtools import check_n11_optimality_field_mask0 as geometry

WORLD = [(Q(), Q()), (Q(2), Q()), (Q(2), Q(2)), (Q(), Q(2))]
NORMALS = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1))


def encoded(poly: list[tuple[Q, Q]]) -> list[list[str]]:
    return [[str(x), str(y)] for x, y in poly]


def support_row() -> tuple[dict[str, object], list[dict[str, object]]]:
    previous = [{"interval": ["0", "1"], "residual_polygons": [[["1/2", "1/2"]]]}]
    bounds = [
        {"normal": list(normal), "upper": "1" if normal == (1, 0) else "100"}
        for normal in NORMALS
    ]
    domain = geometry.intersect(WORLD, [(Q(1), Q(), Q(1))])
    row: dict[str, object] = {
        "interval": ["1/4", "1/2"],
        "input_domain": encoded(domain),
        "domain_restriction": {
            "kind": "previous_residual_outer_support",
            "previous_round": 1,
            "previous_row": 0,
            "bounds": bounds,
        },
    }
    return row, previous


def test_support_contains_every_previous_vertex_and_preserves_closed_domain() -> None:
    row, previous = support_row()
    assert continuation.inherited_domain(row, previous, WORLD, 2) == geometry.intersect(
        WORLD, [(Q(1), Q(), Q(1))]
    )
    restriction = row["domain_restriction"]
    assert isinstance(restriction, dict)
    bounds = restriction["bounds"]
    assert isinstance(bounds, list)
    bounds[0]["upper"] = "1/4"
    with pytest.raises(ValueError, match="cuts accepted previous residual"):
        continuation.inherited_domain(row, previous, WORLD, 2)


def test_angle_must_fit_cited_previous_closed_row() -> None:
    row, previous = support_row()
    row["interval"] = ["1/4", "5/4"]
    with pytest.raises(ValueError, match="angle interval escapes"):
        continuation.inherited_domain(row, previous, WORLD, 2)


def test_empty_previous_residual_excludes_entire_cited_subinterval() -> None:
    previous = [{"interval": ["0", "1"], "residual_polygons": []}]
    row = {
        "interval": ["1/4", "1/2"],
        "input_domain": [],
        "residual_polygons": [],
        "common_core_strips": [],
        "domain_restriction": {
            "kind": "previous_angle_excluded",
            "previous_round": 1,
            "previous_row": 0,
        },
    }
    assert continuation.inherited_domain(row, previous, WORLD, 2) == []
    row["residual_polygons"] = [[["0", "0"]]]
    with pytest.raises(ValueError, match="excluded angle retains geometry"):
        continuation.inherited_domain(row, previous, WORLD, 2)
