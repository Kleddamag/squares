"""Exact signed-edge derivative lower bound for diagnostic centre boxes only.

This module never changes rectangle-verifier acceptance. It encloses every affine
chord endpoint over a whole closed centre box, including endpoint-event crossings.
"""

from __future__ import annotations

import time
from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction
from typing import TYPE_CHECKING

from sqpack import rectangle_density as density

if TYPE_CHECKING:
    from collections.abc import Sequence


class DiagnosticDeadlineError(TimeoutError):
    """The exact diagnostic did not finish before its deadline."""


@dataclass(frozen=True, slots=True)
class Interval:
    lower: Fraction
    upper: Fraction

    def __post_init__(self) -> None:
        if self.lower > self.upper:
            raise ValueError("reversed exact interval")

    def scaled(self, weight: Fraction) -> Interval:
        if weight >= 0:
            return Interval(weight * self.lower, weight * self.upper)
        return Interval(weight * self.upper, weight * self.lower)

    @property
    def max_abs(self) -> Fraction:
        return max(abs(self.lower), abs(self.upper))


@dataclass(frozen=True, slots=True)
class SignedEdge:
    axis: str
    fixed: Fraction
    low: Fraction
    high: Fraction
    jump: Fraction


@dataclass(frozen=True, slots=True)
class DerivativeEdges:
    x: tuple[SignedEdge, ...]
    y: tuple[SignedEdge, ...]


@dataclass(frozen=True, slots=True)
class BoxBound:
    common: Fraction
    midpoint: Fraction
    gx: Interval
    gy: Interval
    gradient: Fraction
    combined: Fraction

    def as_dict(self) -> dict[str, str]:
        return {
            "common_core_bound": str(self.common),
            "midpoint_coverage": str(self.midpoint),
            "gx_lower": str(self.gx.lower),
            "gx_upper": str(self.gx.upper),
            "gy_lower": str(self.gy.lower),
            "gy_upper": str(self.gy.upper),
            "gradient_bound": str(self.gradient),
            "combined_bound": str(self.combined),
        }


@dataclass(frozen=True, slots=True)
class _Affine:
    x: Fraction
    y: Fraction
    constant: Fraction

    def range_on(self, box: density.PendingBox) -> Interval:
        lo_x, hi_x = (box.left, box.right) if self.x >= 0 else (box.right, box.left)
        lo_y, hi_y = (box.bottom, box.top) if self.y >= 0 else (box.top, box.bottom)
        return Interval(
            self.x * lo_x + self.y * lo_y + self.constant,
            self.x * hi_x + self.y * hi_y + self.constant,
        )


def _check_deadline(deadline: float) -> None:
    if time.monotonic() >= deadline:
        raise DiagnosticDeadlineError("exact derivative diagnostic reached its deadline")


def _add_event(
    events: dict[tuple[str, Fraction], dict[Fraction, Fraction]],
    *,
    axis: str,
    fixed: Fraction,
    low: Fraction,
    high: Fraction,
    jump: Fraction,
) -> None:
    if low >= high or jump == 0:
        raise ValueError("invalid signed density edge")
    row = events[(axis, fixed)]
    row[low] += jump
    row[high] -= jump


def build_signed_edges(
    rectangles: Sequence[density.DensityRectangle], *, deadline: float
) -> DerivativeEdges:
    """Split coincident, partly overlapping edges into exact constant-jump spans."""
    events: dict[tuple[str, Fraction], dict[Fraction, Fraction]] = defaultdict(
        lambda: defaultdict(Fraction)
    )
    for rectangle in rectangles:
        _check_deadline(deadline)
        if (
            rectangle.left >= rectangle.right
            or rectangle.bottom >= rectangle.top
            or rectangle.density <= 0
        ):
            raise ValueError("invalid density rectangle")
        _add_event(
            events,
            axis="x",
            fixed=rectangle.left,
            low=rectangle.bottom,
            high=rectangle.top,
            jump=rectangle.density,
        )
        _add_event(
            events,
            axis="x",
            fixed=rectangle.right,
            low=rectangle.bottom,
            high=rectangle.top,
            jump=-rectangle.density,
        )
        _add_event(
            events,
            axis="y",
            fixed=rectangle.bottom,
            low=rectangle.left,
            high=rectangle.right,
            jump=rectangle.density,
        )
        _add_event(
            events,
            axis="y",
            fixed=rectangle.top,
            low=rectangle.left,
            high=rectangle.right,
            jump=-rectangle.density,
        )
    by_axis: dict[str, list[SignedEdge]] = {"x": [], "y": []}
    for (axis, fixed), row in sorted(events.items()):
        _check_deadline(deadline)
        running = Fraction()
        previous: Fraction | None = None
        spans = by_axis[axis]
        for coordinate in sorted(row):
            if previous is not None and previous < coordinate and running:
                if (
                    spans
                    and spans[-1].fixed == fixed
                    and spans[-1].high == previous
                    and spans[-1].jump == running
                ):
                    last = spans.pop()
                    spans.append(SignedEdge(axis, fixed, last.low, coordinate, running))
                else:
                    spans.append(SignedEdge(axis, fixed, previous, coordinate, running))
            running += row[coordinate]
            previous = coordinate
        if running:
            raise ValueError("signed edge events did not balance")
    _check_deadline(deadline)
    return DerivativeEdges(tuple(by_axis["x"]), tuple(by_axis["y"]))


def _chord_interval(
    edge: SignedEdge,
    box: density.PendingBox,
    *,
    cosine: Fraction,
    sine: Fraction,
    half_side: Fraction,
) -> Interval:
    zero = Fraction()
    if edge.axis == "x":
        fixed = edge.fixed
        lower = (
            _Affine(zero, zero, edge.low),
            _Affine(cosine / sine, Fraction(1), (-half_side - cosine * fixed) / sine),
            _Affine(-sine / cosine, Fraction(1), (-half_side + sine * fixed) / cosine),
        )
        upper = (
            _Affine(zero, zero, edge.high),
            _Affine(cosine / sine, Fraction(1), (half_side - cosine * fixed) / sine),
            _Affine(-sine / cosine, Fraction(1), (half_side + sine * fixed) / cosine),
        )
    elif edge.axis == "y":
        fixed = edge.fixed
        lower = (
            _Affine(zero, zero, edge.low),
            _Affine(Fraction(1), sine / cosine, (-half_side - sine * fixed) / cosine),
            _Affine(Fraction(1), -cosine / sine, (-half_side + cosine * fixed) / sine),
        )
        upper = (
            _Affine(zero, zero, edge.high),
            _Affine(Fraction(1), sine / cosine, (half_side - sine * fixed) / cosine),
            _Affine(Fraction(1), -cosine / sine, (half_side + cosine * fixed) / sine),
        )
    else:
        raise ValueError("signed edge axis must be x or y")
    lower_ranges = tuple(form.range_on(box) for form in lower)
    upper_ranges = tuple(form.range_on(box) for form in upper)
    minimum = max(
        zero,
        min(value.lower for value in upper_ranges) - max(value.upper for value in lower_ranges),
    )
    maximum = max(
        zero,
        min(value.upper for value in upper_ranges) - max(value.lower for value in lower_ranges),
    )
    # Either oriented-square slab bounds a chord, independently of edge position.
    maximum = min(maximum, 2 * half_side / cosine, 2 * half_side / sine)
    return Interval(minimum, maximum)


def derivative_intervals(
    box: density.PendingBox,
    edges: DerivativeEdges,
    *,
    cosine: Fraction,
    sine: Fraction,
    core_side: Fraction,
    deadline: float,
) -> tuple[Interval, Interval]:
    """Enclose the x/y derivatives almost everywhere on a whole closed box."""
    if (
        not box.left <= box.right
        or not box.bottom <= box.top
        or cosine <= 0
        or sine <= 0
        or cosine * cosine + sine * sine != 1
        or core_side <= 0
    ):
        raise ValueError("invalid derivative box, angle, or core side")
    half_side = core_side / 2
    answer: list[Interval] = []
    for axis_edges in (edges.x, edges.y):
        lower = Fraction()
        upper = Fraction()
        for edge in axis_edges:
            _check_deadline(deadline)
            term = _chord_interval(
                edge, box, cosine=cosine, sine=sine, half_side=half_side
            ).scaled(edge.jump)
            lower += term.lower
            upper += term.upper
        answer.append(Interval(lower, upper))
    _check_deadline(deadline)
    return answer[0], answer[1]


def bound_pending(
    candidate: density.RectangleDensityCandidate,
    pending: density.PendingBox,
    edges: DerivativeEdges,
    *,
    deadline: float,
) -> BoxBound:
    """Compare old and derivative bounds; do not grant this box proof authority."""
    if not 1 <= pending.angle < density.ANGLE_COUNT:
        raise ValueError("derivative diagnostic requires a nonaxis angle")
    _check_deadline(deadline)
    cosine, sine = density._angle(pending.angle)  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
    common = density.pending_common_core_bound(candidate, pending)
    _check_deadline(deadline)
    middle_x = (pending.left + pending.right) / 2
    middle_y = (pending.bottom + pending.top) / 2
    midpoint = density.coverage_at_point(candidate, middle_x, middle_y, cosine, sine)
    gx, gy = derivative_intervals(
        pending,
        edges,
        cosine=cosine,
        sine=sine,
        core_side=candidate.core_side,
        deadline=deadline,
    )
    half_x = (pending.right - pending.left) / 2
    half_y = (pending.top - pending.bottom) / 2
    gradient = midpoint - half_x * gx.max_abs - half_y * gy.max_abs
    result = BoxBound(common, midpoint, gx, gy, gradient, max(Fraction(), common, gradient))
    _check_deadline(deadline)
    return result
