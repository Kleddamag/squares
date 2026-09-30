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


def test_weighted_closed_sweep_matches_distinct_pair_union() -> None:
    def box(left: Q, bottom: Q, right: Q, top: Q) -> kernel.Polygon:
        return [(left, bottom), (right, bottom), (right, top), (left, top)]

    domain = box(Q(0), Q(0), Q(2), Q(2))
    whole = (1, "whole", domain)
    left = (1, "left", box(Q(0), Q(0), Q(1), Q(2)))
    right = (1, "right", box(Q(1), Q(0), Q(2), Q(2)))
    # Closed seam x=1 is covered; either adjacent region plus whole has charge 2.
    weighted = shared.weighted_union_cover(
        domain, [whole, left, right], 2, budget=kernel.Budget(time.monotonic() + 2, 10000)
    )
    unweighted = kernel.exact_union_cover(
        domain, [left[2], right[2]], budget=kernel.Budget(time.monotonic() + 2, 10000)
    )
    assert weighted["events"] == unweighted["events"] == 3
    gap = (1, "right", box(Q(1001, 1000), Q(0), Q(2), Q(2)))
    with pytest.raises(ValueError, match="weighted row uncovered"):
        shared.weighted_union_cover(
            domain, [whole, left, gap], 2, budget=kernel.Budget(time.monotonic() + 2, 10000)
        )
    # Reusing one physical atom twice must not manufacture an extra unit of charge.
    with pytest.raises(ValueError, match="duplicate weighted atom"):
        shared.weighted_union_cover(
            domain, [whole, whole], 2, budget=kernel.Budget(time.monotonic() + 2, 10000)
        )
    with pytest.raises(kernel.IncompleteError):
        shared.weighted_union_cover(
            domain, [whole, left, right], 2, budget=kernel.Budget(time.monotonic() + 2, 1)
        )


def test_weighted_packet_budget_transfer_and_first_row() -> None:
    spec = shared.SPECS[1155]
    packet, audit, cover = shared.load_sources(spec, RECEIPTS / "field-mask1155/objects", COVER)
    shared.admit(spec, packet, audit, cover)
    assert spec.charge_budget == 5
    assert sum(packet["threshold_units"]) == 6
    assert len(shared.proposed_rows(spec, audit)) == 522
    assert sum(count for _, count in spec.owner_lengths) == 71
    transfer = shared.transfer_cases(spec, packet, cover, baseline())
    assert len(transfer["direct_case_ids"]) == 85
    assert len(transfer["transferred_case_ids"]) == 252
    cell, _, interval = shared.proposed_rows(spec, audit)[0]
    proof = shared.row_geometry(
        spec, packet, cover, cell, interval, budget=kernel.Budget(time.monotonic() + 3, 100000)
    )
    assert proof["required_charge"] == 2
    assert proof["events"] > 0
    bad = copy.deepcopy(packet)
    bad["certificate"]["budget_units"] = 4
    with pytest.raises(ValueError, match="field budget changed"):
        shared.admit(spec, bad, audit, cover)
    bad = copy.deepcopy(packet)
    bad["certificate"]["point_weights"][7] = -1
    with pytest.raises(ValueError, match="point charges changed"):
        shared.admit(spec, bad, audit, cover)


def test_weighted_sloped_crossings_detect_a_gap_between_coarse_probes() -> None:
    domain = [(Q(0), Q(0)), (Q(1), Q(0)), (Q(1), Q(1)), (Q(0), Q(1))]
    rising = [
        (Q(0), Q(0)),
        (Q(1), Q(0)),
        (Q(1), Q(1)),
        (Q(3, 4), Q(1)),
        (Q(0), Q(1, 4)),
    ]
    falling = [(Q(0), Q(0)), (Q(3, 4), Q(0)), (Q(0), Q(3, 4))]

    def atoms(top_start: Q) -> list[tuple[int, str, kernel.Polygon]]:
        upper = [(Q(0), top_start), (Q(1), top_start), (Q(1), Q(1)), (Q(0), Q(1))]
        return [
            (1, "whole", domain),
            (1, "rising", rising),
            (1, "falling", falling),
            (1, "upper", upper),
        ]

    # The lower edges meet at (1/4, 1/2); their closed union reaches the upper atom.
    shared.weighted_union_cover(
        domain, atoms(Q(1, 2)), 2, budget=kernel.Budget(time.monotonic() + 2, 10000)
    )
    # Moving the upper atom to 9/16 leaves a gap only for 3/16 < x < 5/16.
    # Vertex abscissae {0, 3/4, 1} and their midpoints all miss that gap.
    with pytest.raises(ValueError, match="weighted row uncovered"):
        shared.weighted_union_cover(
            domain, atoms(Q(9, 16)), 2, budget=kernel.Budget(time.monotonic() + 2, 10000)
        )


def test_weighted_coverage_refuses_a_full_domain_with_insufficient_charge() -> None:
    domain = [(Q(0), Q(0)), (Q(1), Q(0)), (Q(1), Q(1)), (Q(0), Q(1))]
    with pytest.raises(ValueError, match="weighted row uncovered"):
        shared.weighted_union_cover(
            domain,
            [(1, "one_unit", domain)],
            2,
            budget=kernel.Budget(time.monotonic() + 2, 10000),
        )


def test_collision_pruning_preserves_maximal_boxes_and_one_equal_copy() -> None:
    domain = [(Q(0), Q(0)), (Q(3), Q(0)), (Q(0), Q(3))]
    regions = []
    for name, center, radius in (
        ("large", (Q(1), Q(1)), Q(1)),
        ("equal", (Q(1), Q(1)), Q(1)),
        ("small", (Q(1), Q(1)), Q(1, 2)),
        ("incomparable", (Q(2), Q(0)), Q(1)),
    ):
        poly = kernel.intersect(domain, kernel.box_halfplanes(center, radius))
        regions.append((kernel.area2(poly), name, poly))
    reduced = shared.maximal_collision_regions(regions)
    assert [name for _, name, _ in reduced] == ["large", "incomparable"]
    for x in (Q(0), Q(1, 2), Q(1), Q(2), Q(3)):
        assert kernel.covers_vertical(
            domain, [p for _, _, p in regions], x
        ) == kernel.covers_vertical(domain, [p for _, _, p in reduced], x)


def test_descriptor_derivation_refuses_a_missing_whole_cell_and_bad_charges() -> None:
    spec = shared.SPECS[612]
    packet, audit, cover = shared.load_sources(spec, RECEIPTS / "field-mask612/objects", COVER)

    def derive(p: dict[str, Any], a: dict[str, Any]) -> shared.FieldSpec:
        return shared.derive_spec(
            mask_index=612,
            packet_pin=spec.packet,
            audit_pin=spec.audit,
            packet=p,
            audit=a,
            expected_cases=459,
        )

    generated = derive(packet, audit)
    assert replace(generated, expected_direct=453) == spec
    shared.admit(generated, packet, audit, cover)
    missing = copy.deepcopy(audit)
    missing["independent_row_proofs"] = [
        row for row in missing["independent_row_proofs"] if row["cell"] != 2
    ]
    with pytest.raises(ValueError, match="positive cell has no proposed rows"):
        derive(packet, missing)
    bad = copy.deepcopy(packet)
    bad["certificate"]["features"][0]["weight"] = True
    with pytest.raises(ValueError, match="unsupported weighted feature"):
        derive(bad, audit)
    bad = copy.deepcopy(packet)
    bad["certificate"]["features"][0]["indices"][0] = bad["certificate"]["features"][0][
        "indices"
    ][1]
    with pytest.raises(ValueError, match="unsupported weighted feature"):
        derive(bad, audit)
    bad = copy.deepcopy(packet)
    bad["conditional_owner_support"].append(
        next(owner for owner in range(16) if owner not in bad["mask"])
    )
    with pytest.raises(ValueError, match="invalid owner support"):
        derive(bad, audit)
