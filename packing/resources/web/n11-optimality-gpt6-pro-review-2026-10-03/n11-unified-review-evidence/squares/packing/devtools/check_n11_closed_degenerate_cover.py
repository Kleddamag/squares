"""Exact closed point/segment coverage by finite convex rational regions.

This is the lower-dimensional complement to the positive-area vertical sweep.
It never replaces area coverage and makes no capture or packing claim itself.
"""

from __future__ import annotations

import time
from fractions import Fraction as Q

from devtools import check_n11_optimality_field_mask0 as geometry

type Point = tuple[Q, Q]
type Polygon = list[Point]


def require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def cross(p: Point, q: Point, r: Point) -> Q:
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def convex_hull(region: Polygon) -> Polygon:
    require(bool(region), "empty coverage region")
    if len(region) >= 3:
        turns = [
            cross(p, q, r)
            for p, q, r in zip(
                region, region[1:] + region[:1], region[2:] + region[:2], strict=True
            )
        ]
        require(
            all(turn >= 0 for turn in turns) or all(turn <= 0 for turn in turns),
            "nonconvex coverage region",
        )
    ordered = sorted(set(region))
    if len(ordered) <= 2:
        return ordered
    lower: Polygon = []
    upper: Polygon = []
    for point in ordered:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], point) <= 0:
            lower.pop()
        lower.append(point)
    for point in reversed(ordered):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], point) <= 0:
            upper.pop()
        upper.append(point)
    result = lower[:-1] + upper[:-1]
    require(geometry.area2(region) == geometry.area2(result), "region differs from convex hull")
    return result


def convex_halfplanes(region: Polygon) -> list[tuple[Q, Q, Q]]:
    """Represent a closed convex area, segment, or point by halfplanes."""

    poly = convex_hull(region)
    if len(poly) == 1:
        x, y = poly[0]
        return [(Q(1), Q(), x), (Q(-1), Q(), -x), (Q(), Q(1), y), (Q(), Q(-1), -y)]
    if len(poly) == 2:
        (x0, y0), (x1, y1) = poly
        dx, dy = x1 - x0, y1 - y0
        line = (dy, -dx, dy * x0 - dx * y0)
        return [
            (Q(1), Q(), max(x0, x1)),
            (Q(-1), Q(), -min(x0, x1)),
            (Q(), Q(1), max(y0, y1)),
            (Q(), Q(-1), -min(y0, y1)),
            line,
            (-line[0], -line[1], -line[2]),
        ]
    return [
        (q[1] - p[1], p[0] - q[0], (q[1] - p[1]) * p[0] - (q[0] - p[0]) * p[1])
        for p, q in zip(poly, poly[1:] + poly[:1], strict=True)
    ]


def exact_cover_closed_degenerate(
    legal: Polygon, regions: list[Polygon], *, budget: geometry.Budget
) -> dict[str, int]:
    """Cover a closed point or segment by exact parameter intervals in [0,1]."""

    domain = convex_hull(legal)
    require(len(domain) <= 2, "expected point or segment domain")
    require(bool(regions), "no eligible charge regions")
    start, end = domain[0], domain[-1]
    dx, dy = end[0] - start[0], end[1] - start[1]
    intervals: list[tuple[Q, Q]] = []
    constraints = 0
    for region in regions:
        lower, upper = Q(), Q(1)
        for a, b, c in convex_halfplanes(region):
            constraints += 1
            if constraints > budget.max_nodes or time.monotonic() >= budget.deadline:
                raise geometry.IncompleteError("degenerate coverage event ceiling")
            base = a * start[0] + b * start[1] - c
            slope = a * dx + b * dy
            if slope > 0:
                upper = min(upper, -base / slope)
            elif slope < 0:
                lower = max(lower, -base / slope)
            elif base > 0:
                lower, upper = Q(1), Q()
                break
            if lower > upper:
                break
        if lower <= upper:
            intervals.append((lower, upper))
    intervals.sort()
    cursor = Q()
    for lower, upper in intervals:
        require(lower <= cursor, "uncovered degenerate legal domain")
        cursor = max(cursor, upper)
        if cursor >= 1:
            return {"events": constraints, "probes": len(intervals)}
    require(cursor >= 1, "uncovered degenerate legal domain")
    return {"events": constraints, "probes": len(intervals)}
