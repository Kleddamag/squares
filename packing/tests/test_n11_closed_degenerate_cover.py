"""Exact closed point and segment union-coverage controls."""

from __future__ import annotations

from fractions import Fraction as Q

import pytest

from devtools import check_n11_closed_degenerate_cover as cover
from devtools import check_n11_optimality_field_mask0 as geometry

BUDGET = geometry.Budget(float("inf"), 1000)


def rectangle(left: Q, bottom: Q, right: Q, top: Q) -> cover.Polygon:
    return [(left, bottom), (right, bottom), (right, top), (left, top)]


def test_closed_intervals_cover_segment_with_tied_endpoint_in_both_orientations() -> None:
    domain = [(Q(), Q()), (Q(2), Q())]
    left = rectangle(Q(), Q(-1), Q(1), Q(1))
    right = list(reversed(rectangle(Q(1), Q(-1), Q(2), Q(1))))
    assert cover.exact_cover_closed_degenerate(domain, [left, right], budget=BUDGET)
    assert cover.exact_cover_closed_degenerate(
        list(reversed(domain)), [right, left], budget=BUDGET
    )


def test_positive_gap_is_not_closed_by_a_singleton_or_tangent() -> None:
    domain = [(Q(), Q()), (Q(2), Q())]
    regions = [
        rectangle(Q(), Q(-1), Q(3, 4), Q(1)),
        [(Q(1), Q())],
        rectangle(Q(5, 4), Q(-1), Q(2), Q(1)),
    ]
    with pytest.raises(ValueError, match="uncovered"):
        cover.exact_cover_closed_degenerate(domain, regions, budget=BUDGET)


def test_exact_point_and_collinear_segment_regions() -> None:
    point = [(Q(7, 3), Q(5, 7))]
    assert cover.exact_cover_closed_degenerate(point, [point], budget=BUDGET)
    segment = [(Q(1, 3), Q(2, 5)), (Q(4, 3), Q(2, 5))]
    assert cover.exact_cover_closed_degenerate(
        segment, [list(reversed(segment))], budget=BUDGET
    )
    with pytest.raises(ValueError, match="uncovered"):
        cover.exact_cover_closed_degenerate(point, [[(Q(7, 3), Q(6, 7))]], budget=BUDGET)


def test_area_domain_or_nonconvex_region_refuses() -> None:
    square = rectangle(Q(), Q(), Q(1), Q(1))
    with pytest.raises(ValueError, match="point or segment"):
        cover.exact_cover_closed_degenerate(square, [square], budget=BUDGET)
    bowtie = [(Q(), Q()), (Q(1), Q(1)), (Q(), Q(1)), (Q(1), Q())]
    with pytest.raises(ValueError, match="nonconvex"):
        cover.exact_cover_closed_degenerate([(Q(), Q())], [bowtie], budget=BUDGET)
    star = [(Q(), Q(3)), (Q(2), Q(-3)), (Q(-3), Q(1)), (Q(3), Q(1)), (Q(-2), Q(-3))]
    with pytest.raises(ValueError, match="differs from convex hull"):
        cover.exact_cover_closed_degenerate([(Q(), Q())], [star], budget=BUDGET)
