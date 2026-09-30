"""Differential controls for the exact active-edge cover helper."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import json
import random
import time
from collections.abc import Callable
from fractions import Fraction as Q

from devtools import check_n11_generic_fresh as generic
from devtools import check_n11_optimality_field_mask0 as frozen
from devtools import n11_fast_exact_cover as fast


def _budget(nodes: int = 50_000) -> frozen.Budget:
    return frozen.Budget(time.monotonic() + 10, nodes)


def _outcome(
    cover: Callable[..., dict[str, int]],
    domain: frozen.Polygon,
    regions: list[frozen.Polygon],
    *,
    nodes: int = 50_000,
) -> tuple[str, object]:
    try:
        result = cover(domain, regions, budget=_budget(nodes))
    except (ValueError, frozen.IncompleteError) as error:
        return type(error).__name__, str(error)
    return "pass", result


def _square() -> frozen.Polygon:
    return [(Q(0), Q(0)), (Q(1), Q(0)), (Q(1), Q(1)), (Q(0), Q(1))]


def test_closed_intervals_match_at_vertices_segments_and_points() -> None:
    polygons: list[frozen.Polygon] = [
        [],
        [(Q(1), Q(2))],
        [(Q(1), Q(0)), (Q(1), Q(3))],
        [(Q(0), Q(0)), (Q(3), Q(3))],
        [(Q(0), Q(0)), (Q(2), Q(2)), (Q(0), Q(2)), (Q(2), Q(0))],
        [(Q(0), Q(0)), (Q(3), Q(0)), (Q(3), Q(2)), (Q(1), Q(1)), (Q(0), Q(2))],
    ]
    probes = [Q(-1), Q(0), Q(1, 2), Q(1), Q(3, 2), Q(2), Q(5, 2), Q(3), Q(4)]
    for polygon in polygons:
        compiled = fast._compile_polygon(polygon)  # noqa: SLF001
        for x in probes:
            assert compiled.interval(x) == frozen.vertical_interval(polygon, x)


def test_point_slice_needs_a_span_that_actually_contains_it() -> None:
    # The full checker refuses degenerate domains. Its endpoint slice predicate
    # should nevertheless distinguish a gap from legal closed contact directly.
    for low, high, expected in [(0, 1, False), (1, 2, True), (2, 3, True), (3, 4, False)]:
        target = fast._compile_polygon([(Q(0), Q(2))])  # noqa: SLF001
        span = fast._compile_polygon([(Q(0), Q(low)), (Q(0), Q(high))])  # noqa: SLF001
        assert fast._covers_vertical(target, [span], Q(0)) is expected  # noqa: SLF001


def test_closed_cover_and_tiny_gap_match_frozen_kernel() -> None:
    domain = _square()
    left = frozen.clip(domain, (Q(1), Q(0), Q(1, 2)))
    right = frozen.clip(domain, (Q(-1), Q(0), Q(-1, 2)))
    shifted = frozen.clip(domain, (Q(-1), Q(0), -(Q(1, 2) + Q(1, 10**50))))
    segment = [(Q(1, 2), Q(0)), (Q(1, 2), Q(1))]
    point = [(Q(1, 2), Q(1, 2))]
    examples = [
        (domain, [domain]),
        (domain, [left, right]),
        (domain, [right, left, segment, point]),
        (domain, [left, shifted]),
        (domain, [left, shifted, segment]),
        (domain, [segment, point]),
        (domain, []),
        (segment, [domain]),
    ]
    for region_domain, regions in examples:
        assert _outcome(fast.exact_union_cover, region_domain, regions) == _outcome(
            frozen.exact_union_cover, region_domain, regions
        )
    assert _outcome(fast.exact_union_cover, domain, [domain], nodes=1) == _outcome(
        frozen.exact_union_cover, domain, [domain], nodes=1
    )


def test_random_polygons_match_closed_cover_and_event_counts() -> None:
    rng = random.Random(97162)
    domain = [(Q(0), Q(0)), (Q(6), Q(0)), (Q(6), Q(6)), (Q(0), Q(6))]
    for _ in range(40):
        regions: list[frozen.Polygon] = []
        for _ in range(rng.randint(1, 5)):
            region = [
                (Q(rng.randint(-2, 8)), Q(rng.randint(-2, 8))) for _ in range(rng.randint(1, 6))
            ]
            regions.append(region)
        assert _outcome(fast.exact_union_cover, domain, regions) == _outcome(
            frozen.exact_union_cover, domain, regions
        )


def test_three_pinned_generic_rows_match_frozen_counts() -> None:
    source = generic._load_pin(  # noqa: SLF001
        generic.OBJECTS / f"{generic.SOURCE_PIN[0]}.gz", generic.SOURCE_PIN
    )
    receipt = json.loads(
        (generic.PACKET / "receipts/generic-mask2095-intake/full-result.json").read_text()
    )
    step = source["steps"][0]
    assert step["owner"] == 6
    for row_index in (0, 22, 31):
        row = step["rows"][row_index]
        domain = generic.convex(row["input_domain"])
        core = generic.convex(row["core_vertices"])
        prior = {
            int(owner): generic.hull(generic.points(group))
            for owner, group in step["prior_owned_hulls"].items()
        }
        forbidden = [
            generic.hull([(p[0] - q[0], p[1] - q[1]) for p in group for q in core])
            for owner, group in prior.items()
            if owner != step["owner"]
        ]
        residual = [generic.convex(value) for value in row["residual_polygons"]]
        frozen_result = frozen.exact_union_cover(domain, forbidden + residual, budget=_budget())
        fast_result = fast.exact_union_cover(domain, forbidden + residual, budget=_budget())
        assert fast_result == frozen_result
        expected = receipt["step_timings"][0]["row_timings"][row_index]
        assert (fast_result["events"], fast_result["probes"]) == (
            expected["events"],
            expected["probes"],
        )
