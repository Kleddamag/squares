"""Focused independent controls for the mask-202 field adapter."""

from __future__ import annotations

import copy
import time
from fractions import Fraction as Q
from typing import Any

import pytest

from devtools import check_n11_optimality_field_mask0 as kernel
from devtools import check_n11_optimality_field_mask202 as field

OBJECTS = field.PACKET / "receipts/field-mask202/objects"
COVER = field.PACKET / "receipts/d4-independent/objects" / f"{kernel.COVER_SHA}.gz"


@pytest.fixture(scope="module")
def sources() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    packet, audit, cover = field.load_sources(OBJECTS, COVER)
    field.admit(packet, audit, cover)
    kernel.admit_d4_receipt()
    return packet, audit, cover


def baseline() -> dict[str, Any]:
    return kernel.pinned_gzip(
        field.PACKET / "receipts/case-census/objects" / f"{kernel.A1_SHA}.gz",
        packed_bytes=26100,
        packed_sha=kernel.A1_LFS_SHA,
        raw_bytes=122029,
        raw_sha=kernel.A1_SHA,
    )


def test_three_site_collinear_median_is_exact_center_capture_box() -> None:
    sites = [(Q(-2), Q(0)), (Q(0), Q(0)), (Q(2), Q(0))]
    domain = [(Q(-1), Q(-1)), (Q(1), Q(-1)), (Q(1), Q(1)), (Q(-1), Q(1))]
    region = kernel.intersect(domain, field.majority_halfplanes(sites, Q(1, 2)))
    expected = kernel.intersect(domain, kernel.box_halfplanes((Q(0), Q(0)), Q(1, 2)))
    assert kernel.area2(region) == kernel.area2(expected) == Q(2)
    assert set(region) == set(expected)


def test_source_rows_partition_both_closed_angle_charts_and_mutation_refuses(
    sources: tuple[dict[str, Any], dict[str, Any], dict[str, Any]],
) -> None:
    _, audit, _ = sources
    rows = field.proposed_rows(audit)
    assert len(rows) == 439
    assert sum(cell == 4 for cell, _, _ in rows) == 85
    assert sum(cell == 8 for cell, _, _ in rows) == 354
    changed = copy.deepcopy(audit)
    changed["independent_row_proofs"][0]["interval"][1] = "1/257"
    with pytest.raises(ValueError, match="row gap or overlap"):
        field.proposed_rows(changed)


def test_one_wall_owner_and_one_row_freshly_pass_without_case_promotion(
    sources: tuple[dict[str, Any], dict[str, Any], dict[str, Any]],
) -> None:
    packet, audit, cover = sources
    ownership = kernel.ownership(
        kernel.cell_vertices(cover, 0),
        kernel.point(packet["ownership_points_field"][0][5]),
        budget=kernel.Budget(time.monotonic() + 5, 5000),
    )
    assert ownership["method"] == "strict_wall_interval_bound"
    assert Q(ownership["minimum_margin"]) > 0
    row = next(row for row in audit["independent_row_proofs"] if row["cell"] == 4)
    interval = Q(row["interval"][0]), Q(row["interval"][1])
    proof = field.row_geometry(
        packet, cover, 4, interval, budget=kernel.Budget(time.monotonic() + 5, 5000)
    )
    assert proof["selected_regions"] == 12
    assert len(proof["selected_region_ids"]) == 12
    assert proof["probes"] > proof["events"] > 0


def test_transfer_sets_match_pinned_a1_and_prior_mask0(
    sources: tuple[dict[str, Any], dict[str, Any], dict[str, Any]],
) -> None:
    packet, _, cover = sources
    transfer = field.transfer_cases(packet, cover, baseline())
    assert len(transfer["transferred_case_ids"]) == 764
    assert len(transfer["new_beyond_mask0_case_ids"]) == 653
    changed = copy.deepcopy(packet)
    changed["conditional_owner_support"].pop()
    with pytest.raises(ValueError, match="conditional owners changed"):
        field.admit(changed, sources[1], cover)


def test_partial_scope_keeps_exact_pending_counts_and_zero_exclusions(
    sources: tuple[dict[str, Any], dict[str, Any], dict[str, Any]],
) -> None:
    packet, audit, cover = sources
    result = field.all_geometry(
        packet, audit, cover, baseline(), budget=kernel.Budget(time.monotonic() + 5, 1)
    )
    assert result["status"] == "INCOMPLETE"
    assert result["canonical_cases_excluded"] == 0
    assert result["geometry_verified"] is False
    assert len(result["ownership_checked"]) + len(result["ownership_pending"]) == 50
    assert len(result["rows_checked"]) + len(result["rows_pending"]) == 439
