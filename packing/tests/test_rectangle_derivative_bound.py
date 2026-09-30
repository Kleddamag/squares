"""Exact controls for a diagnostic signed-edge rectangle-coverage bound."""

from __future__ import annotations

import time
from fractions import Fraction as F  # noqa: N817

import pytest

from devtools import rectangle_derivative_bound as bound
from sqpack import rectangle_density as density


def _box(
    left: F = F(),
    bottom: F = F(),
    right: F = F(),
    top: F = F(),
    *,
    angle: int = 1,
) -> density.PendingBox:
    return density.PendingBox(angle, left, bottom, right, top, 0, "diagnostic")


def _rectangle(
    left: int | F, bottom: int | F, right: int | F, top: int | F, rho: int = 1
) -> density.DensityRectangle:
    return density.DensityRectangle(F(left), F(bottom), F(right), F(top), F(rho))


def _edges(*rectangles: density.DensityRectangle) -> bound.DerivativeEdges:
    return bound.build_signed_edges(rectangles, deadline=time.monotonic() + 10)


def test_partly_coincident_signed_edges_split_and_cancel_exactly() -> None:
    edges = _edges(_rectangle(-1, 0, 0, 2), _rectangle(0, 1, 1, 3))
    shared = [edge for edge in edges.x if edge.fixed == 0]
    assert shared == [
        bound.SignedEdge("x", F(), F(0), F(1), F(-1)),
        bound.SignedEdge("x", F(), F(2), F(3), F(1)),
    ]
    duplicate = _edges(_rectangle(-1, -1, 0, 1), _rectangle(-1, -1, 0, 1))
    assert [edge.jump for edge in duplicate.x] == [F(2), F(-2)]


def test_constant_density_and_equal_adjacent_rectangles_cancel_the_gradient() -> None:
    left = _rectangle(-10, -10, 0, 10)
    right = _rectangle(0, -10, 10, 10)
    edges = _edges(left, right)
    assert all(edge.fixed != 0 for edge in edges.x)
    box = _box(F(-1, 10), F(-1, 10), F(1, 10), F(1, 10))
    gx, gy = bound.derivative_intervals(
        box, edges, cosine=F(3, 5), sine=F(4, 5), core_side=F(2), deadline=time.monotonic() + 10
    )
    assert gx == gy == bound.Interval(F(), F())
    merged = _edges(_rectangle(-10, -10, 10, 10))
    assert edges == merged
    candidate = density.RectangleDensityCandidate(
        3, F(20), F(2), F(4), None, F(400), (left, right)
    )
    result = bound.bound_pending(candidate, box, edges, deadline=time.monotonic() + 10)
    assert result.midpoint == result.combined == 4
    assert result.common < 4


def test_unequal_density_jump_has_both_exact_signed_directions() -> None:
    box = _box()
    for left_rho, right_rho, expected in ((1, 3, F(5)), (3, 1, F(-5))):
        edges = _edges(
            _rectangle(-10, -10, 0, 10, left_rho),
            _rectangle(0, -10, 10, 10, right_rho),
        )
        gx, gy = bound.derivative_intervals(
            box,
            edges,
            cosine=F(3, 5),
            sine=F(4, 5),
            core_side=F(2),
            deadline=time.monotonic() + 10,
        )
        assert gx == bound.Interval(expected, expected)
        assert gy == bound.Interval(F(), F())
        candidate = density.RectangleDensityCandidate(
            5,
            F(20),
            F(2),
            F(1),
            None,
            F(200 * (left_rho + right_rho)),
            (
                _rectangle(-10, -10, 0, 10, left_rho),
                _rectangle(0, -10, 10, 10, right_rho),
            ),
        )
        assert density.coverage_at_point(candidate, F(), F(), F(3, 5), F(4, 5)) == 8


def test_translated_horizontal_jump_has_both_exact_signed_directions() -> None:
    x, y = F(7, 3), F(-5, 4)
    box = _box(x, y, x, y)
    for lower_rho, upper_rho, expected in ((1, 3, F(5)), (3, 1, F(-5))):
        lower = _rectangle(x - 10, y - 10, x + 10, y, lower_rho)
        upper = _rectangle(x - 10, y, x + 10, y + 10, upper_rho)
        gx, gy = bound.derivative_intervals(
            box,
            _edges(lower, upper),
            cosine=F(3, 5),
            sine=F(4, 5),
            core_side=F(2),
            deadline=time.monotonic() + 10,
        )
        assert gx == bound.Interval(F(), F())
        assert gy == bound.Interval(expected, expected)
        candidate = density.RectangleDensityCandidate(
            5,
            F(20),
            F(2),
            F(1),
            None,
            F(200 * (lower_rho + upper_rho)),
            (lower, upper),
        )
        assert density.coverage_at_point(candidate, x, y, F(3, 5), F(4, 5)) == 8


def test_nonzero_box_lower_bound_is_below_exact_coverage_at_selected_points() -> None:
    lower = _rectangle(-10, -10, 10, 0, 1)
    upper = _rectangle(-10, 0, 10, 10, 3)
    candidate = density.RectangleDensityCandidate(
        5, F(20), F(2), F(1), None, F(800), (lower, upper)
    )
    box = _box(F(-1, 10), F(-1, 10), F(1, 10), F(1, 10))
    edges = _edges(lower, upper)
    cosine, sine = F(3, 5), F(4, 5)
    gx, gy = bound.derivative_intervals(
        box,
        edges,
        cosine=cosine,
        sine=sine,
        core_side=F(2),
        deadline=time.monotonic() + 10,
    )
    middle = density.coverage_at_point(candidate, F(), F(), cosine, sine)
    lower_bound = middle - F(1, 10) * (gx.max_abs + gy.max_abs)
    for x, y in (
        (box.left, box.bottom),
        (box.left, box.top),
        (box.right, box.bottom),
        (box.right, box.top),
        (F(), F()),
    ):
        assert lower_bound <= density.coverage_at_point(candidate, x, y, cosine, sine)


def test_interior_chord_maximum_is_not_inferred_from_corner_chords() -> None:
    edge = bound.SignedEdge("x", F(), F(-10), F(10), F(1))
    box = _box(F(-2), F(-1, 10), F(2), F(1, 10))
    edges = bound.DerivativeEdges((edge,), ())
    gx, _ = bound.derivative_intervals(
        box, edges, cosine=F(3, 5), sine=F(4, 5), core_side=F(2), deadline=time.monotonic() + 10
    )
    assert gx.lower == 0
    assert gx.upper == F(5, 2)
    for x in (box.left, box.right):
        point = _box(x, F(), x, F())
        point_gx, _ = bound.derivative_intervals(
            point,
            edges,
            cosine=F(3, 5),
            sine=F(4, 5),
            core_side=F(2),
            deadline=time.monotonic() + 10,
        )
        assert point_gx == bound.Interval(F(), F())


def test_tangency_point_box_near_axis_and_closed_interval_refusals() -> None:
    edge = bound.SignedEdge("x", F(7, 5), F(-10), F(10), F(1))
    edges = bound.DerivativeEdges((edge,), ())
    tangent, _ = bound.derivative_intervals(
        _box(),
        edges,
        cosine=F(3, 5),
        sine=F(4, 5),
        core_side=F(2),
        deadline=time.monotonic() + 10,
    )
    assert tangent == bound.Interval(F(), F())
    u = F(1, 100_000)
    cosine, sine = (1 - u * u) / (1 + u * u), 2 * u / (1 + u * u)
    small, _ = bound.derivative_intervals(
        _box(F(-1, 1000), F(), F(1, 1000), F()),
        _edges(_rectangle(-10, -10, 10, 10)),
        cosine=cosine,
        sine=sine,
        core_side=F(2),
        deadline=time.monotonic() + 10,
    )
    assert small == bound.Interval(F(), F())
    with pytest.raises(ValueError, match="invalid derivative"):
        bound.derivative_intervals(
            _box(F(1), F(), F(), F()),
            edges,
            cosine=F(3, 5),
            sine=F(4, 5),
            core_side=F(2),
            deadline=time.monotonic() + 10,
        )
    with pytest.raises(ValueError, match="invalid derivative"):
        bound.derivative_intervals(
            _box(),
            edges,
            cosine=F(3, 5),
            sine=F(3, 5),
            core_side=F(2),
            deadline=time.monotonic() + 10,
        )
    for cosine, sine in ((F(), F(1)), (F(1), F())):
        with pytest.raises(ValueError, match="invalid derivative"):
            bound.derivative_intervals(
                _box(),
                edges,
                cosine=cosine,
                sine=sine,
                core_side=F(2),
                deadline=time.monotonic() + 10,
            )


def test_deadline_and_negative_density_refuse_without_partial_bound() -> None:
    with pytest.raises(ValueError, match="invalid density"):
        _edges(_rectangle(-1, -1, 1, 1, -1))
    with pytest.raises(bound.DiagnosticDeadlineError):
        bound.build_signed_edges((_rectangle(-1, -1, 1, 1),), deadline=time.monotonic() - 1)
    with pytest.raises(bound.DiagnosticDeadlineError):
        bound.derivative_intervals(
            _box(),
            _edges(_rectangle(-1, -1, 1, 1)),
            cosine=F(3, 5),
            sine=F(4, 5),
            core_side=F(2),
            deadline=time.monotonic() - 1,
        )
