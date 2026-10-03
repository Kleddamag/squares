"""Exact closed vertical cover with precompiled polygon edges.

The frozen n=11 kernel remains the reference implementation. This module keeps
its event/probe construction and evaluates the same closed vertical intervals
with active affine edges, including vertical edges and degenerate regions.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from fractions import Fraction as Q
from itertools import pairwise

from devtools import check_n11_optimality_field_mask0 as reference

Point = tuple[Q, Q]
Polygon = list[Point]
Line = tuple[Q, Q, Q, Q]


@dataclass(slots=True)
class _PolygonSweep:
    x_min: Q | None
    x_max: Q | None
    edges: list[Line]
    starts: list[tuple[Q, int]]
    ends: list[tuple[Q, int]]
    verticals: dict[Q, tuple[Q, Q]]
    active: set[int] = field(default_factory=set)
    start_cursor: int = 0
    end_cursor: int = 0

    def interval(self, x: Q) -> tuple[Q, Q] | None:
        """Match the reference's closed extrema over all edges crossing `x`."""
        x_min, x_max = self.x_min, self.x_max
        if x_min is None or x_max is None or x < x_min or x > x_max:
            return None
        while self.start_cursor < len(self.starts) and self.starts[self.start_cursor][0] <= x:
            self.active.add(self.starts[self.start_cursor][1])
            self.start_cursor += 1
        while self.end_cursor < len(self.ends) and self.ends[self.end_cursor][0] < x:
            self.active.remove(self.ends[self.end_cursor][1])
            self.end_cursor += 1
        vertical = self.verticals.get(x)
        low, high = vertical if vertical is not None else (None, None)
        for index in self.active:
            _, _, slope, intercept = self.edges[index]
            ordinate = slope * x + intercept
            if low is None or ordinate < low:
                low = ordinate
            if high is None or ordinate > high:
                high = ordinate
        return (low, high) if low is not None and high is not None else None


def _compile_polygon(poly: Polygon) -> _PolygonSweep:
    if not poly:
        return _PolygonSweep(None, None, [], [], [], {})
    edges: list[Line] = []
    starts: list[tuple[Q, int]] = []
    ends: list[tuple[Q, int]] = []
    verticals: dict[Q, tuple[Q, Q]] = {}
    for p, q in zip(poly, poly[1:] + poly[:1], strict=True):
        if p[0] == q[0]:
            x = p[0]
            lo, hi = min(p[1], q[1]), max(p[1], q[1])
            previous = verticals.get(x)
            verticals[x] = (
                (min(lo, previous[0]), max(hi, previous[1])) if previous else (lo, hi)
            )
            continue
        left, right = min(p[0], q[0]), max(p[0], q[0])
        slope = (q[1] - p[1]) / (q[0] - p[0])
        edges.append((left, right, slope, p[1] - slope * p[0]))
        starts.append((left, len(edges) - 1))
        ends.append((right, len(edges) - 1))
    starts.sort()
    ends.sort()
    return _PolygonSweep(
        min(point[0] for point in poly),
        max(point[0] for point in poly),
        edges,
        starts,
        ends,
        verticals,
    )


def _covers_vertical(domain: _PolygonSweep, regions: list[_PolygonSweep], x: Q) -> bool:
    target = domain.interval(x)
    if target is None:
        raise ValueError("coverage probe outside domain")
    spans = [span for poly in regions if (span := poly.interval(x)) is not None]
    spans.sort()
    cursor = target[0]
    for low, high in spans:
        if high < cursor:
            continue
        if low > cursor:
            return False
        cursor = max(cursor, high)
        if cursor >= target[1]:
            return True
    return False


def exact_union_cover(
    domain: Polygon, regions: list[Polygon], *, budget: reference.Budget
) -> dict[str, int]:
    """Check closed coverage for a convex domain and convex closed regions.

    Callers establish convexity. The domain must have positive area; regions may
    be empty, points or segments. Probes are visited in increasing order, as the
    compiled edge state requires. No approximate arithmetic is used.
    """
    reference.require(
        reference.area2(domain) > 0, "degenerate row domain needs a separate proof"
    )
    reference.require(bool(regions), "no eligible charge regions")
    polygons = [domain, *regions]
    left, right = min(p[0] for p in domain), max(p[0] for p in domain)
    events = {p[0] for poly in polygons for p in poly if left <= p[0] <= right}
    compiled = [_compile_polygon(poly) for poly in polygons]
    lines = [line for poly in compiled for line in poly.edges]
    for number, (a0, a1, m, b) in enumerate(lines):
        if time.monotonic() >= budget.deadline:
            raise reference.IncompleteError(
                f"row event construction timed out after {number} edges"
            )
        for z0, z1, n, d in lines[number + 1 :]:
            if m == n:
                continue
            start, stop = max(a0, z0, left), min(a1, z1, right)
            if start <= stop:
                crossing = (d - b) / (m - n)
                if start <= crossing <= stop:
                    events.add(crossing)
        if len(events) > budget.max_nodes:
            raise reference.IncompleteError(f"row event ceiling: events={len(events)}")
    positions = sorted(events)
    reference.require(
        positions[0] == left and positions[-1] == right, "row domain endpoint missing"
    )
    probes = [positions[0]]
    for a, b in pairwise(positions):
        probes.extend(((a + b) / 2, b))
    if len(probes) > budget.max_nodes:
        raise reference.IncompleteError(f"row probe ceiling: probes={len(probes)}")
    for number, x in enumerate(probes):
        if time.monotonic() >= budget.deadline:
            raise reference.IncompleteError(
                f"row sweep timeout: checked={number}, total={len(probes)}"
            )
        reference.require(
            _covers_vertical(compiled[0], compiled[1:], x), f"row uncovered at exact x={x}"
        )
    return {"events": len(positions), "probes": len(probes), "edge_segments": len(lines)}
