"""Finite support cuts preserve every allowed closed-region assignment."""

from __future__ import annotations

import copy
import gzip
import itertools
import json
import time
from fractions import Fraction as Q

import pytest

from devtools import check_n11_baseline_d4_cuts as cuts


def baseline():
    path = cuts.PACKET / "receipts/case-census/objects" / f"{cuts.BASELINE_METADATA_SHA}.gz"
    return json.loads(gzip.decompress(path.read_bytes()))


def test_exact_baseline_complement_includes_both_half_turn_orientations() -> None:
    source = baseline()
    excluded, canonical, allowed = cuts.baseline_context(source)
    assert len(excluded) == 1931
    remaining = set(range(len(canonical))) - excluded
    expected = {canonical[index] for index in remaining}
    expected |= {cuts.d4.half_turn(mask) for mask in expected}
    assert set(allowed) == expected
    assert len(allowed) == 506
    changed = copy.deepcopy(source)
    changed["remaining_canonical_mask_indices"][0] = changed[
        "remaining_canonical_mask_indices"
    ][1]
    with pytest.raises(ValueError, match="complement"):
        cuts.baseline_context(changed)


def test_cut_vertex_equality_is_retained_and_any_strict_violation_is_queried() -> None:
    labels = [(0, 0, 0, 0), (0, 1, 1, 1), (1, 0, 1, 0)]
    vertices = [((Q(), Q()), (Q(1), Q())), ((Q(1), Q(1)),), ((Q(2), Q()),)]
    boundary = cuts.B * (Q(1, 2) + (cuts.d4.U - 1))
    plane = cuts.Cut(0, (Q(1), Q()), boundary)
    assert cuts.offending_regions(labels, vertices, (0, 1), [plane]) == []
    tighter = cuts.Cut(0, plane.normal, boundary - Q(1, 10**60))
    assert cuts.offending_regions(labels, vertices, (0, 1), [tighter]) == [0, 1]


def brute_force(labels, banned, allowed, source_mask, forced):
    domains = [[i for i, row in enumerate(labels) if row[0] == owner] for owner in source_mask]
    for assignment in itertools.product(*domains):
        if forced not in assignment:
            continue
        if any(tuple(sorted(pair)) in banned for pair in itertools.combinations(assignment, 2)):
            continue
        if all(
            len({labels[index][view] for index in assignment}) == len(source_mask)
            and tuple(sorted(labels[index][view] for index in assignment)) in allowed
            for view in range(4)
        ):
            return assignment
    return None


def test_forced_search_matches_independent_small_assignment_enumeration() -> None:
    labels = [(0, 0, 0, 0), (1, 1, 1, 1), (0, 2, 0, 0), (0, 0, 0, 1), (1, 2, 2, 2)]
    source_mask = (0, 1)
    for allowed in ([(0, 1)], [(0, 1), (1, 2)], [(0, 1), (0, 2), (1, 2)]):
        for banned in (set(), {(0, 1)}, {(1, 2), (0, 4)}):
            search = cuts.ForcedRegionSearch(
                labels, banned, allowed, cuts.SearchBudget(time.monotonic() + 3, 1000)
            )
            for forced in range(len(labels)):
                witness, nodes = search.solve(source_mask, forced)
                expected = brute_force(labels, banned, allowed, source_mask, forced)
                assert (witness is None) == (expected is None)
                assert nodes >= 1
                if witness is not None:
                    assert forced in witness


def test_expired_or_exhausted_search_cannot_report_unsat() -> None:
    labels = [(0, 0, 0, 0), (1, 1, 1, 1)]
    for budget in (
        cuts.SearchBudget(time.monotonic() - 1, 100),
        cuts.SearchBudget(time.monotonic() + 3, 1),
    ):
        search = cuts.ForcedRegionSearch(labels, set(), [(0, 1)], budget)
        with pytest.raises(cuts.geometry.IncompleteError):
            search.solve((0, 1), 0)


def test_execution_inventory_requires_exact_ids_not_a_sufficient_count() -> None:
    excluded, _, _ = cuts.baseline_context(baseline())
    required = set(range(2184)) - set(cuts.d4.SURVIVORS)
    accepted = sorted(excluded)
    record = {
        "status": "EXECUTION_RECORD_INVENTORY",
        "source_revision": cuts.geometry.SOURCE_REVISION,
        "global_optimality_proved": False,
        "geometry_rerun": False,
        "nonfield_manifest_sha256": cuts.MANIFEST_GZIP_SHA,
        "field_inventory_sha256": cuts.FIELD_INVENTORY_SHA,
        "accepted_case_ids": accepted,
        "accepted_case_count": len(accepted),
        "remaining_case_ids": sorted(required - set(accepted)),
        "remaining_case_count": len(required - set(accepted)),
        "required_case_count": 2180,
    }
    assert cuts.execution_missing(record, excluded) == []
    missing = accepted[0]
    replacement = min(required - excluded)
    changed = copy.deepcopy(record)
    changed["accepted_case_ids"] = sorted((excluded - {missing}) | {replacement})
    changed["remaining_case_ids"] = sorted(required - set(changed["accepted_case_ids"]))
    assert cuts.execution_missing(changed, excluded) == [missing]
    changed["accepted_case_ids"][1] = changed["accepted_case_ids"][0]
    with pytest.raises(ValueError, match="accepted"):
        cuts.execution_missing(changed, excluded)
