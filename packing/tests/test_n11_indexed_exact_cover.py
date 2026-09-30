"""The indexed cover retains every closed exact crossing event."""

# pyright: reportPrivateUsage=false
# ruff: noqa: SLF001

from __future__ import annotations

import json
import random
import time
from fractions import Fraction as Q

import pytest

from devtools import check_n11_generic_fresh as generic
from devtools import check_n11_optimality_field_mask0 as geometry
from devtools import n11_fast_exact_cover as fast
from devtools import n11_indexed_exact_cover as indexed


def _budget(nodes: int = 50_000) -> geometry.Budget:
    return geometry.Budget(time.monotonic() + 10, nodes)


def _all_pair_events(
    polygons: list[fast.Polygon], lines: list[fast.Line], left: Q, right: Q
) -> list[Q]:
    events = {
        point[0] for polygon in polygons for point in polygon if left <= point[0] <= right
    }
    for number, (a0, a1, m, b) in enumerate(lines):
        for z0, z1, n, d in lines[number + 1 :]:
            if m == n:
                continue
            lo, hi = max(a0, z0, left), min(a1, z1, right)
            if lo <= hi:
                x = (d - b) / (m - n)
                if lo <= x <= hi:
                    events.add(x)
    return sorted(events)


def _outcome(domain: fast.Polygon, regions: list[fast.Polygon]) -> tuple[str, object]:
    try:
        return "pass", indexed.exact_union_cover(domain, regions, budget=_budget())
    except (ValueError, geometry.IncompleteError) as error:
        return type(error).__name__, str(error)


def _reference(domain: fast.Polygon, regions: list[fast.Polygon]) -> tuple[str, object]:
    try:
        return "pass", fast.exact_union_cover(domain, regions, budget=_budget())
    except (ValueError, geometry.IncompleteError) as error:
        return type(error).__name__, str(error)


def test_equal_endpoint_crossing_is_retained_but_disjoint_ranges_are_skipped() -> None:
    touch: list[fast.Line] = [
        (Q(0), Q(1), Q(1), Q(0)),
        (Q(1), Q(2), Q(-1), Q(2)),
    ]
    assert indexed.event_positions([], touch, Q(0), Q(2), budget=_budget()) == [Q(1)]
    apart: list[fast.Line] = [
        (Q(0), Q(1, 2), Q(1), Q(0)),
        (Q(1), Q(2), Q(-1), Q(2)),
    ]
    assert indexed.event_positions([], apart, Q(0), Q(2), budget=_budget()) == []


def test_exact_event_sets_match_all_pairs_with_closed_tangencies() -> None:
    domain = [(Q(0), Q(0)), (Q(3), Q(0)), (Q(3), Q(3)), (Q(0), Q(3))]
    region_sets: list[list[fast.Polygon]] = [
        [domain],
        [
            [(Q(0), Q(0)), (Q(1), Q(0)), (Q(1), Q(3)), (Q(0), Q(3))],
            [(Q(1), Q(0)), (Q(3), Q(0)), (Q(3), Q(3)), (Q(1), Q(3))],
            [(Q(1), Q(1))],
            [(Q(2), Q(0)), (Q(2), Q(3))],
        ],
        [[(Q(0), Q(0)), (Q(3), Q(3))], [(Q(0), Q(3)), (Q(3), Q(0))]],
    ]
    for regions in region_sets:
        polygons = [domain, *regions]
        lines = [line for polygon in polygons for line in fast._compile_polygon(polygon).edges]
        assert indexed.event_positions(polygons, lines, Q(0), Q(3), budget=_budget()) == (
            _all_pair_events(polygons, lines, Q(0), Q(3))
        )
        assert _outcome(domain, regions) == _reference(domain, regions)


def test_random_exact_events_and_closed_cover_outcomes_match() -> None:
    rng = random.Random(510234)
    domain = [(Q(0), Q(0)), (Q(6), Q(0)), (Q(6), Q(6)), (Q(0), Q(6))]
    for _ in range(50):
        regions: list[fast.Polygon] = []
        for _ in range(rng.randint(1, 6)):
            points = [
                (Q(rng.randint(-2, 8)), Q(rng.randint(-2, 8))) for _ in range(rng.randint(1, 6))
            ]
            regions.append(generic.hull(points))
        polygons = [domain, *regions]
        lines = [line for polygon in polygons for line in fast._compile_polygon(polygon).edges]
        assert indexed.event_positions(polygons, lines, Q(0), Q(6), budget=_budget()) == (
            _all_pair_events(polygons, lines, Q(0), Q(6))
        )
        assert _outcome(domain, regions) == _reference(domain, regions)


def test_expired_or_too_many_events_refuses() -> None:
    lines: list[fast.Line] = [
        (Q(0), Q(1), Q(1), Q(0)),
        (Q(0), Q(1), Q(-1), Q(1)),
    ]
    with pytest.raises(geometry.IncompleteError, match="timed out"):
        indexed.event_positions([], lines, Q(0), Q(1), budget=geometry.Budget(0, 10))
    with pytest.raises(geometry.IncompleteError, match="event ceiling"):
        indexed.event_positions([], lines, Q(0), Q(1), budget=_budget(0))


def test_frozen_dependencies_are_bound() -> None:
    assert indexed.dependencies_unchanged()


def test_retained_generic_rows_match_exact_events_and_acceptance() -> None:
    source = generic._load_pin(
        generic.OBJECTS / f"{generic.SOURCE_PIN[0]}.gz", generic.SOURCE_PIN
    )
    accepted = json.loads(
        (generic.PACKET / "receipts/generic-mask2095-intake/full-result.json").read_text()
    )
    step = source["steps"][0]
    prior = {
        int(owner): generic.hull(generic.points(group))
        for owner, group in step["prior_owned_hulls"].items()
    }
    for row_index in (0, 22, 31):
        row = step["rows"][row_index]
        domain = generic.convex(row["input_domain"])
        core = generic.convex(row["core_vertices"])
        forbidden = [
            generic.hull([(p[0] - q[0], p[1] - q[1]) for p in group for q in core])
            for owner, group in prior.items()
            if owner != step["owner"]
        ]
        regions = forbidden + [generic.convex(value) for value in row["residual_polygons"]]
        polygons = [domain, *regions]
        lines = [line for polygon in polygons for line in fast._compile_polygon(polygon).edges]
        lo, hi = min(point[0] for point in domain), max(point[0] for point in domain)
        assert indexed.event_positions(polygons, lines, lo, hi, budget=_budget()) == (
            _all_pair_events(polygons, lines, lo, hi)
        )
        result = indexed.exact_union_cover(domain, regions, budget=_budget())
        assert result == fast.exact_union_cover(domain, regions, budget=_budget())
        expected = accepted["step_timings"][0]["row_timings"][row_index]
        assert (result["events"], result["probes"]) == (
            expected["events"],
            expected["probes"],
        )
