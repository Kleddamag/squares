"""Exact closed-interval cover controls, and the historical singleton false accept (C2)."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import time
from decimal import Decimal
from fractions import Fraction as Q
from itertools import combinations_with_replacement, pairwise
from typing import Any

import pytest

from devtools import check_n11_optimality_field_mask0 as frozen
from devtools import n11_closed_interval_cover as cover
from devtools import n11_fast_exact_cover as fast

Interval = cover.Interval

ENDPOINTS = [Q(value) for value in range(-3, 4)]
INTERVALS: list[Interval] = [(lo, hi) for lo in ENDPOINTS for hi in ENDPOINTS if lo <= hi]
FAMILIES: list[tuple[Interval, ...]] = [
    (),
    *((interval,) for interval in INTERVALS),
    *combinations_with_replacement(INTERVALS, 2),
]
HISTORICAL_FALSE_ACCEPTS = 616


def _oracle(target: Interval, covers: tuple[Interval, ...]) -> bool:
    """Check every breakpoint in the target and every midpoint between consecutive ones."""
    lo, hi = target
    marks = sorted({lo, hi, *(end for span in covers for end in span if lo <= end <= hi)})
    probes = [*marks, *((a + b) / 2 for a, b in pairwise(marks))]
    return all(any(a <= y <= b for a, b in covers) for y in probes)


def _slab(interval: Interval) -> frozen.Polygon:
    """A polygon whose closed vertical section at x = 0 is exactly `interval`."""
    lo, hi = interval
    return [(Q(0), lo), (Q(1), lo), (Q(1), hi), (Q(0), hi)]


def _historical(target: Interval, covers: tuple[Interval, ...]) -> bool:
    """Call the pinned `covers_vertical` itself, through polygons with these sections."""
    return frozen.covers_vertical(_slab(target), [_slab(span) for span in covers], Q(0))


# A compiled sweep only moves forward in x. Every probe here is x = 0, so one
# compilation per interval serves every call and keeps the enumeration fast.
COMPILED = {interval: fast._compile_polygon(_slab(interval)) for interval in INTERVALS}  # noqa: SLF001


def _fast(target: Interval, covers: tuple[Interval, ...]) -> bool:
    """Call the corrected fast kernel's slice predicate on the same sections."""
    spans = [COMPILED[span] for span in covers]
    return fast._covers_vertical(COMPILED[target], spans, Q(0))  # noqa: SLF001


def test_enumeration_is_the_reviewed_12180_cases() -> None:
    assert len(INTERVALS) == 28
    assert len(FAMILIES) == 1 + 28 + 28 * 29 // 2 == 435
    assert len(INTERVALS) * len(FAMILIES) == 12_180
    for interval in INTERVALS:
        assert frozen.vertical_interval(_slab(interval), Q(0)) == interval


def test_corrected_rule_and_historical_rule_against_the_exact_oracle() -> None:
    corrected_errors: list[tuple[Interval, tuple[Interval, ...]]] = []
    fast_errors: list[tuple[Interval, tuple[Interval, ...]]] = []
    historical_false_accepts: list[tuple[Interval, tuple[Interval, ...]]] = []
    historical_false_refusals: list[tuple[Interval, tuple[Interval, ...]]] = []
    for target in INTERVALS:
        for covers in FAMILIES:
            truth = _oracle(target, covers)
            if cover.covers_closed_interval(target, covers) is not truth:
                corrected_errors.append((target, covers))
            if _fast(target, covers) is not truth:
                fast_errors.append((target, covers))
            historical = _historical(target, covers)
            if historical and not truth:
                historical_false_accepts.append((target, covers))
            elif truth and not historical:
                historical_false_refusals.append((target, covers))
    assert corrected_errors == []
    assert fast_errors == []
    assert historical_false_refusals == []
    assert len(historical_false_accepts) == HISTORICAL_FALSE_ACCEPTS
    assert all(target[0] == target[1] for target, _ in historical_false_accepts)


def test_singleton_below_cover_is_refused_but_was_historically_accepted() -> None:
    target, covers = (Q(1), Q(1)), ((Q(0), Q(0)),)
    assert _historical(target, covers) is True
    assert cover.covers_closed_interval(target, covers) is False
    assert cover.covers_closed_interval((1, 1), [(0, 0)]) is False


def test_covered_singleton_is_accepted() -> None:
    assert cover.covers_closed_interval((Q(1), Q(1)), [(Q(0), Q(0)), (Q(1, 2), Q(1))])
    assert cover.covers_closed_interval((Q(1), Q(1)), [(Q(1), Q(1))])
    assert cover.covers_closed_interval((Q(1), Q(1)), [(Q(1), Q(3))])
    assert not cover.covers_closed_interval((Q(1), Q(1)), [])


def test_closed_seam_covers_and_tiny_gap_does_not() -> None:
    half = Q(1, 2)
    assert cover.covers_closed_interval((Q(0), Q(1)), [(half, Q(1)), (Q(0), half)])
    gap = Q(1, 10**50)
    assert not cover.covers_closed_interval((Q(0), Q(1)), [(Q(0), half), (half + gap, Q(1))])
    assert not cover.covers_closed_interval((Q(0), Q(1)), [(Q(0), half - gap), (half, Q(1))])
    assert not cover.covers_closed_interval((Q(0), Q(1)), [(gap, Q(1))])
    assert not cover.covers_closed_interval((Q(0), Q(1)), [(Q(0), Q(1) - gap)])


def test_containing_interval_covers() -> None:
    assert cover.covers_closed_interval((Q(0), Q(1)), [(Q(0), Q(2))])
    assert cover.covers_closed_interval((Q(0), Q(1)), [(Q(-5), Q(-4)), (Q(-1), Q(1))])
    assert not cover.covers_closed_interval((Q(0), Q(1)), [])


@pytest.mark.parametrize(
    ("target", "covers"),
    [
        ((Q(1), Q(0)), []),
        ((Q(0), Q(1)), [(Q(1), Q(0))]),
        ((0.0, 1.0), []),
        ((Q(0), Q(1)), [(Q(0), float("nan"))]),
        ((float("nan"), float("nan")), [(Q(0), Q(1))]),
        ((Decimal("NaN"), Q(1)), [(Q(0), Q(1))]),
        ((False, True), [(Q(0), Q(1))]),
        (("0", "1"), [(Q(0), Q(1))]),
        ((Q(0), None), [(Q(0), Q(1))]),
        ((Q(0), Q(1), Q(2)), [(Q(0), Q(2))]),
        ((Q(0), Q(1)), [(Q(0),)]),
        (Q(0), [(Q(0), Q(1))]),
    ],
)
def test_malformed_input_is_refused(target: Any, covers: Any) -> None:
    with pytest.raises(ValueError, match=r"endpoint|pair"):
        cover.covers_closed_interval(target, covers)


def test_positive_area_triangle_endpoint_slice_is_not_a_full_cover_result() -> None:
    """The helper's endpoint error is real; the frozen full sweep still refuses."""
    domain = [(Q(0), Q(1)), (Q(1), Q(0)), (Q(1), Q(2))]
    below = [(Q(0), Q(-1)), (Q(1), Q(-1)), (Q(1), Q(0)), (Q(0), Q(0))]
    assert frozen.vertical_interval(domain, Q(0)) == (Q(1), Q(1))
    assert frozen.vertical_interval(below, Q(0)) == (Q(-1), Q(0))
    assert frozen.covers_vertical(domain, [below], Q(0)) is True
    assert not cover.covers_closed_interval((Q(1), Q(1)), [(Q(-1), Q(0))])
    budget = frozen.Budget(time.monotonic() + 10, 1000)
    with pytest.raises(ValueError, match=r"row uncovered at exact x=1/2"):
        frozen.exact_union_cover(domain, [below], budget=budget)
