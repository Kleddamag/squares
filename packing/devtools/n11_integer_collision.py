"""Exact universal-collision containment using integer homogeneous coordinates.

Each point (X,Y,Z) represents (X/Z,Y/Z), with Z strictly positive. Hull
orientations and facet inequalities cross-multiply positive denominators; no
rounding, division or repeated rational normalization occurs in the hot loop.
The caller must independently establish the complete partner pose cover and
strict whole-angle core ownership before these collision regions can prune.
"""

from __future__ import annotations

from fractions import Fraction
from functools import cmp_to_key
from math import lcm

from devtools import check_n11_capture_transition_pilot as reference
from devtools import check_n11_optimality_field_mask0 as geometry

Point = tuple[int, int, int]
Polygon = list[tuple[Fraction, Fraction]]


def encode(point: tuple[Fraction, Fraction]) -> Point:
    """Lift a rational point with a positive common denominator."""
    x, y = point
    z = lcm(x.denominator, y.denominator)
    return x.numerator * (z // x.denominator), y.numerator * (z // y.denominator), z


def compare(a: Point, b: Point) -> int:
    """Compare exact affine coordinates lexicographically."""
    dx = a[0] * b[2] - b[0] * a[2]
    dy = a[1] * b[2] - b[1] * a[2]
    value = dx or dy
    return (value > 0) - (value < 0)


def orientation(a: Point, b: Point, c: Point) -> int:
    """Return a determinant with the exact affine orientation sign."""
    return (
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - a[1] * (b[0] * c[2] - b[2] * c[0])
        + a[2] * (b[0] * c[1] - b[1] * c[0])
    )


def hull(points: list[Point]) -> list[Point]:
    """Return the exact CCW convex hull, removing affine duplicates and collinearity."""
    ordered = sorted(points, key=cmp_to_key(compare))
    unique: list[Point] = []
    for point in ordered:
        reference.require(point[2] > 0, "nonpositive homogeneous denominator")
        if not unique or compare(unique[-1], point):
            unique.append(point)
    if len(unique) <= 1:
        return unique
    lower: list[Point] = []
    upper: list[Point] = []
    for point in unique:
        while len(lower) > 1 and orientation(lower[-2], lower[-1], point) <= 0:
            lower.pop()
        lower.append(point)
    for point in reversed(unique):
        while len(upper) > 1 and orientation(upper[-2], upper[-1], point) <= 0:
            upper.pop()
        upper.append(point)
    return lower[:-1] + upper[:-1]


def universal_collision(
    query_core: Polygon,
    query_domain: Polygon,
    partner_rows: list[tuple[Polygon, Polygon]],
    region: Polygon,
    *,
    budget: geometry.Budget,
) -> int:
    """Prove every proposed vertex lies in every partner's collision polytope."""
    reference.require(
        bool(partner_rows), "empty partner family requires separate contradiction"
    )
    reference.require(geometry.area2(query_core) > 0, "query core")
    query_lines = reference.degenerate.convex_halfplanes(query_domain)
    reference.require(
        all(nx * x + ny * y <= bound for x, y in region for nx, ny, bound in query_lines),
        "collision region escapes query domain",
    )
    query = [encode(point) for point in query_core]
    vertices = [encode(point) for point in region]
    checks = 0
    for domain, core in partner_rows:
        reference.remaining(budget)
        reference.require(bool(domain) and geometry.area2(core) > 0, "partner core or domain")
        partner = [encode(point) for point in core]
        centers = [encode(point) for point in domain]
        difference = hull(
            [
                (x * qz - qx * z, y * qz - qy * z, z * qz)
                for x, y, z in partner
                for qx, qy, qz in query
            ]
        )
        reference.require(len(difference) >= 3, "degenerate collision hull")
        for a, b in zip(difference, difference[1:] + difference[:1], strict=True):
            nx = b[1] * a[2] - a[1] * b[2]
            ny = a[0] * b[2] - b[0] * a[2]
            upper = a[0] * b[1] - a[1] * b[0]
            minimum: tuple[int, int] | None = None
            for x, y, z in centers:
                value = nx * x + ny * y
                if minimum is None or value * minimum[1] < minimum[0] * z:
                    minimum = value, z
            reference.require(minimum is not None, "empty partner domain")
            assert minimum is not None
            value, denominator = minimum
            rhs = upper * denominator + value
            for x, y, z in vertices:
                checks += 1
                reference.require(
                    (nx * x + ny * y) * denominator <= rhs * z,
                    "region escapes universal collision set",
                )
    return checks
