"""Focused controls for the new shared one-feature field runner."""

from __future__ import annotations

import copy
import gzip
import time
from dataclasses import replace
from fractions import Fraction as Q
from typing import Any

import pytest

from devtools import check_n11_optimality_field_mask0 as kernel
from devtools import check_n11_optimality_field_mask202 as frozen202
from devtools import check_n11_optimality_field_runner as shared

RECEIPTS = shared.PACKET_ROOT / "receipts"
COVER = RECEIPTS / "d4-independent/objects" / f"{kernel.COVER_SHA}.gz"


@pytest.fixture(scope="module", params=(0, 202))
def source(
    request: pytest.FixtureRequest,
) -> tuple[shared.FieldSpec, dict[str, Any], dict[str, Any], dict[str, Any]]:
    mask_index = int(request.param)
    spec = shared.SPECS[mask_index]
    packet, audit, cover = shared.load_sources(
        spec, RECEIPTS / f"field-mask{mask_index}/objects", COVER
    )
    shared.admit(spec, packet, audit, cover)
    return spec, packet, audit, cover


def baseline() -> dict[str, Any]:
    return kernel.pinned_gzip(
        RECEIPTS / "case-census/objects" / f"{kernel.A1_SHA}.gz",
        packed_bytes=26100,
        packed_sha=kernel.A1_LFS_SHA,
        raw_bytes=122029,
        raw_sha=kernel.A1_SHA,
    )


def test_explicit_admission_and_closed_row_census(
    source: tuple[shared.FieldSpec, dict[str, Any], dict[str, Any], dict[str, Any]],
) -> None:
    spec, packet, audit, cover = source
    assert shared.canonical_masks(cover)[spec.mask_index] == tuple(packet["mask"])
    rows = shared.proposed_rows(spec, audit)
    assert len(rows) == sum(count for _, count in spec.row_counts)
    assert {cell for cell, _, _ in rows} == set(spec.positive_cells)
    assert sum(count for _, count in spec.owner_lengths) == (55 if spec.mask_index == 0 else 50)
    kernel.admit_d4_receipt()


def test_unsupported_feature_and_row_gap_refuse(
    source: tuple[shared.FieldSpec, dict[str, Any], dict[str, Any], dict[str, Any]],
) -> None:
    spec, packet, audit, cover = source
    extra = copy.deepcopy(packet)
    extra["certificate"]["features"].append({"kind": "unproved"})
    with pytest.raises(ValueError, match="unsupported field feature"):
        shared.admit(spec, extra, audit, cover)
    unsupported = replace(spec, site_count=7)
    with pytest.raises(ValueError, match="unsupported majority-site arity"):
        shared.admit(unsupported, packet, audit, cover)
    gap = copy.deepcopy(audit)
    gap["independent_row_proofs"][0]["interval"][1] = "1/997"
    with pytest.raises(ValueError, match="row gap or overlap"):
        shared.proposed_rows(spec, gap)


def test_first_exact_row_matches_frozen_geometry(
    source: tuple[shared.FieldSpec, dict[str, Any], dict[str, Any], dict[str, Any]],
) -> None:
    spec, packet, audit, cover = source
    cell, _, interval = shared.proposed_rows(spec, audit)[0]
    new = shared.row_geometry(
        spec, packet, cover, cell, interval, budget=kernel.Budget(time.monotonic() + 5, 10000)
    )
    old_checker = kernel if spec.mask_index == 0 else frozen202
    old = old_checker.row_geometry(
        packet, cover, cell, interval, budget=kernel.Budget(time.monotonic() + 5, 10000)
    )
    for key in (
        "cell",
        "interval",
        "core_side",
        "parent_center_halfwidth",
        "domain_area_twice",
        "eligible_regions",
        "events",
        "probes",
        "edge_segments",
    ):
        assert new[key] == old[key]
    assert new["selected_regions"] == (old.get("selected_regions") or old["eligible_regions"])
    if spec.mask_index == 202:
        assert new["selected_region_ids"] == old["selected_region_ids"]


def test_median_grammar_is_exact_for_five_and_three_sites() -> None:
    five = [(Q(-2), Q(0)), (Q(-1), Q(0)), (Q(0), Q(0)), (Q(1), Q(0)), (Q(2), Q(0))]
    three = [five[0], five[2], five[4]]
    assert shared.majority_halfplanes(five, Q(1, 2)) == kernel.true_halfplanes(five, Q(1, 2))
    assert shared.majority_halfplanes(three, Q(1, 2)) == frozen202.majority_halfplanes(
        three, Q(1, 2)
    )


def test_partial_budget_preserves_every_pending_obligation_and_excludes_zero(
    source: tuple[shared.FieldSpec, dict[str, Any], dict[str, Any], dict[str, Any]],
) -> None:
    spec, packet, audit, cover = source
    result = shared.all_geometry(
        spec, packet, audit, cover, baseline(), budget=kernel.Budget(time.monotonic() + 5, 1)
    )
    assert result["status"] == "INCOMPLETE"
    assert result["geometry_verified"] is False
    assert result["canonical_cases_excluded"] == 0
    assert len(result["ownership_checked"]) + len(result["ownership_pending"]) == sum(
        count for _, count in spec.owner_lengths
    )
    assert len(result["rows_checked"]) + len(result["rows_pending"]) == sum(
        count for _, count in spec.row_counts
    )


def test_exact_transfer_ids_match_frozen_result_sets(
    source: tuple[shared.FieldSpec, dict[str, Any], dict[str, Any], dict[str, Any]],
) -> None:
    spec, packet, _, cover = source
    transfer = shared.transfer_cases(spec, packet, cover, baseline())
    assert len(transfer["direct_case_ids"]) == spec.expected_direct
    assert len(transfer["transferred_case_ids"]) == spec.expected_transferred
    if spec.mask_index == 0:
        saved = kernel.strict_json((RECEIPTS / "field-mask0/result.json").read_bytes())
    else:
        saved = kernel.strict_json(
            gzip.decompress((RECEIPTS / "field-mask202/result.json.gz").read_bytes())
        )
    assert transfer["direct_case_ids"] == saved["transfer"]["direct_case_ids"]
    assert transfer["transferred_case_ids"] == saved["transfer"]["transferred_case_ids"]


def test_actual_two_field_union_has_1112_distinct_ids() -> None:
    accepted: list[set[int]] = []
    source_baseline = baseline()
    for mask_index in (0, 202):
        spec = shared.SPECS[mask_index]
        packet, audit, cover = shared.load_sources(
            spec, RECEIPTS / f"field-mask{mask_index}/objects", COVER
        )
        shared.admit(spec, packet, audit, cover)
        ids = shared.transfer_cases(spec, packet, cover, source_baseline)[
            "transferred_case_ids"
        ]
        accepted.append(set(ids))
    assert len(accepted[1] - accepted[0]) == 653
    assert len(accepted[0] | accepted[1]) == 1112


def test_selected_subset_miss_is_incomplete_not_a_false_exclusion(
    monkeypatch: pytest.MonkeyPatch,
    source: tuple[shared.FieldSpec, dict[str, Any], dict[str, Any], dict[str, Any]],
) -> None:
    spec, packet, audit, cover = source
    cell, _, interval = shared.proposed_rows(spec, audit)[0]

    def miss(*_args: object, **_kwargs: object) -> dict[str, int]:
        raise ValueError("row uncovered at exact x=1/2")

    monkeypatch.setattr(kernel, "exact_union_cover", miss)
    if spec.max_regions is None:
        with pytest.raises(ValueError, match="row uncovered"):
            shared.row_geometry(
                spec,
                packet,
                cover,
                cell,
                interval,
                budget=kernel.Budget(time.monotonic() + 5, 10000),
            )
    else:
        with pytest.raises(kernel.IncompleteError, match="selected 12-region subset"):
            shared.row_geometry(
                spec,
                packet,
                cover,
                cell,
                interval,
                budget=kernel.Budget(time.monotonic() + 5, 10000),
            )
