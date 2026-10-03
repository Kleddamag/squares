"""Exact closed cover with line-crossing events indexed by x overlap.

This is an opt-in arithmetic primitive, not a geometric certificate. It uses
the reviewed precompiled vertical sweep and discards an edge pair only when
its closed x projections are disjoint. Equality at a shared endpoint remains
an event candidate.
"""

# pyright: reportPrivateUsage=false
# ruff: noqa: SLF001

from __future__ import annotations

import hashlib
import heapq
import time
from fractions import Fraction as Q
from itertools import pairwise
from pathlib import Path

from devtools import n11_fast_exact_cover as fast

Polygon = fast.Polygon
Line = fast.Line
FAST_SOURCE_SHA = "eb21b1acda671b9f858039d077b0c8a30d035ee5920e083887952bf44b156904"
GEOMETRY_SOURCE_SHA = "75fc0238f2ac91af9dc9cf57bd00792343dcf3321c395adddebf0f3465113ce5"


def dependencies_unchanged() -> bool:
    """Bind the reviewed vertical-sweep and geometry implementations."""
    path = Path(fast.__file__)
    return (
        hashlib.sha256(path.read_bytes()).hexdigest() == FAST_SOURCE_SHA
        and hashlib.sha256(Path(fast.reference.__file__).read_bytes()).hexdigest()
        == GEOMETRY_SOURCE_SHA
    )


def event_positions(
    polygons: list[Polygon],
    lines: list[Line],
    left: Q,
    right: Q,
    *,
    budget: fast.reference.Budget,
) -> list[Q]:
    """Return the reference's complete vertex and crossing abscissae."""
    events = {
        point[0] for polygon in polygons for point in polygon if left <= point[0] <= right
    }
    if len(events) > budget.max_nodes:
        raise fast.reference.IncompleteError(f"row event ceiling: events={len(events)}")
    active: dict[int, None] = {}
    ending: list[tuple[Q, int]] = []
    pairs = 0
    order = sorted(range(len(lines)), key=lambda item: (lines[item][0], item))
    for number, index in enumerate(order):
        if time.monotonic() >= budget.deadline:
            raise fast.reference.IncompleteError(
                f"indexed event construction timed out after {number} edges"
            )
        a0, a1, m, b = lines[index]
        if a1 < left or a0 > right:
            continue
        while ending and ending[0][0] < a0:
            _, expired = heapq.heappop(ending)
            active.pop(expired, None)
        for other in active:
            pairs += 1
            if pairs % 1024 == 0 and time.monotonic() >= budget.deadline:
                raise fast.reference.IncompleteError(
                    f"indexed event construction timed out after {pairs} candidate pairs"
                )
            z0, z1, n, d = lines[other]
            if m == n:
                continue
            start, stop = max(a0, z0, left), min(a1, z1, right)
            if start <= stop:
                crossing = (d - b) / (m - n)
                if start <= crossing <= stop:
                    events.add(crossing)
                    if len(events) > budget.max_nodes:
                        raise fast.reference.IncompleteError(
                            f"row event ceiling: events={len(events)}"
                        )
        active[index] = None
        heapq.heappush(ending, (a1, index))
    return sorted(events)


def exact_union_cover(
    domain: Polygon, regions: list[Polygon], *, budget: fast.reference.Budget
) -> dict[str, int]:
    """Prove the same closed convex-region union as the all-pairs reference."""
    fast.reference.require(
        fast.reference.area2(domain) > 0, "degenerate row domain needs a separate proof"
    )
    fast.reference.require(bool(regions), "no eligible charge regions")
    polygons = [domain, *regions]
    left, right = min(point[0] for point in domain), max(point[0] for point in domain)
    compiled = [fast._compile_polygon(polygon) for polygon in polygons]
    lines = [line for polygon in compiled for line in polygon.edges]
    positions = event_positions(polygons, lines, left, right, budget=budget)
    fast.reference.require(
        positions[0] == left and positions[-1] == right, "row domain endpoint missing"
    )
    probes = [positions[0]]
    for a, b in pairwise(positions):
        probes.extend(((a + b) / 2, b))
    if len(probes) > budget.max_nodes:
        raise fast.reference.IncompleteError(f"row probe ceiling: probes={len(probes)}")
    for number, x in enumerate(probes):
        if time.monotonic() >= budget.deadline:
            raise fast.reference.IncompleteError(
                f"row sweep timeout: checked={number}, total={len(probes)}"
            )
        fast.reference.require(
            fast._covers_vertical(compiled[0], compiled[1:], x),
            f"row uncovered at exact x={x}",
        )
    return {"events": len(positions), "probes": len(probes), "edge_segments": len(lines)}
