"""Geometric controls for the one pinned mask-0 field certificate."""

from __future__ import annotations

import copy
import time
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import pytest

from devtools import check_n11_optimality_field_mask0 as field

OBJECTS = field.PACKET / "receipts/field-mask0/objects"
COVER = field.PACKET / "receipts/d4-independent/objects" / f"{field.COVER_SHA}.gz"


@pytest.fixture(scope="module")
def sources() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    packet, audit, cover = field.load_sources(OBJECTS, COVER)
    field.admit(packet, audit, cover)
    field.admit_d4_receipt()
    return packet, audit, cover


def square() -> field.Polygon:
    return [(Q(0), Q(0)), (Q(1), Q(0)), (Q(1), Q(1)), (Q(0), Q(1))]


def test_exact_arrangement_covers_closed_split_and_detects_tiny_gap() -> None:
    domain = square()
    left = field.clip(domain, (Q(1), Q(0), Q(1, 2)))
    right = field.clip(domain, (Q(-1), Q(0), Q(-1, 2)))
    budget = field.Budget(time.monotonic() + 5, 500)
    proof = field.exact_union_cover(domain, [left, right], budget=budget)
    assert proof["events"] >= 3
    tiny = Q(1, 10**50)
    shifted = field.clip(domain, (Q(-1), Q(0), -(Q(1, 2) + tiny)))
    with pytest.raises(ValueError, match="row uncovered"):
        field.exact_union_cover(domain, [left, shifted], budget=budget)


def test_degenerate_clipping_and_ceiling_are_explicit() -> None:
    edge = field.clip(square(), (Q(1), Q(0), Q(0)))
    assert edge
    assert field.area2(edge) == 0
    with pytest.raises(field.IncompleteError, match="row event ceiling"):
        field.exact_union_cover(
            square(), [square()], budget=field.Budget(time.monotonic() + 5, 1)
        )


def test_one_wall_point_and_one_complete_row_are_freshly_proved(
    sources: tuple[dict[str, Any], dict[str, Any], dict[str, Any]],
) -> None:
    packet, audit, cover = sources
    point = field.point(packet["ownership_points_field"][0][5])
    proof = field.ownership(
        field.cell_vertices(cover, 0), point, budget=field.Budget(time.monotonic() + 5, 5000)
    )
    assert proof["method"] == "strict_wall_interval_bound"
    assert proof["nodes"] > proof["leaves"] > 0
    assert Q(proof["minimum_margin"]) > 0
    row = next(r for r in audit["independent_row_proofs"] if r["cell"] == 1)
    interval = Q(row["interval"][0]), Q(row["interval"][1])
    complete = field.row_geometry(
        packet, cover, 1, interval, budget=field.Budget(time.monotonic() + 5, 5000)
    )
    assert complete["events"] > 0
    assert complete["probes"] > complete["events"]
    assert Q(complete["domain_area_twice"]) > 0


def test_proposed_rows_partition_both_closed_angle_domains(
    sources: tuple[dict[str, Any], dict[str, Any], dict[str, Any]],
) -> None:
    _, audit, _ = sources
    rows = field.proposed_rows(audit)
    assert len(rows) == 136
    assert {cell for cell, _, _ in rows} == {1, 2}
    changed = copy.deepcopy(audit)
    changed["independent_row_proofs"][0]["interval"][1] = "1/65"
    with pytest.raises(ValueError, match="row gap or overlap"):
        field.proposed_rows(changed)


def test_premise_and_source_identity_mutations_refuse(
    sources: tuple[dict[str, Any], dict[str, Any], dict[str, Any]], tmp_path: Path
) -> None:
    packet, audit, cover = sources
    changed = copy.deepcopy(packet)
    changed["conditional_owner_support"].pop()
    with pytest.raises(ValueError, match="owner support changed"):
        field.admit(changed, audit, cover)
    raw = bytearray((OBJECTS / f"{field.FIELD_SHA}.gz").read_bytes())
    raw[-1] ^= 1
    target = tmp_path / "changed.gz"
    target.write_bytes(raw)
    with pytest.raises(ValueError, match="compressed SHA mismatch"):
        field.pinned_gzip(
            target,
            packed_bytes=3749,
            packed_sha=field.FIELD_LFS_SHA,
            raw_bytes=28065,
            raw_sha=field.FIELD_SHA,
        )


def test_partial_global_run_never_claims_an_exclusion(
    sources: tuple[dict[str, Any], dict[str, Any], dict[str, Any]],
) -> None:
    packet, audit, cover = sources
    baseline = field.pinned_gzip(
        field.PACKET / "receipts/case-census/objects" / f"{field.A1_SHA}.gz",
        packed_bytes=26100,
        packed_sha=field.A1_LFS_SHA,
        raw_bytes=122029,
        raw_sha=field.A1_SHA,
    )
    result = field.all_geometry(
        packet, audit, cover, baseline, budget=field.Budget(time.monotonic() + 5, 1)
    )
    assert result["status"] == "INCOMPLETE"
    assert result["canonical_cases_excluded"] == 0
    assert result["geometry_verified"] is False
    assert len(result["ownership_checked"]) + len(result["ownership_pending"]) == 55
    assert len(result["rows_checked"]) + len(result["rows_pending"]) == 136


def test_final_row_cannot_overrun_the_global_work_ceiling(
    sources: tuple[dict[str, Any], dict[str, Any], dict[str, Any]],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    packet, audit, cover = sources
    baseline = field.pinned_gzip(
        field.PACKET / "receipts/case-census/objects" / f"{field.A1_SHA}.gz",
        packed_bytes=26100,
        packed_sha=field.A1_LFS_SHA,
        raw_bytes=122029,
        raw_sha=field.A1_SHA,
    )
    monkeypatch.setattr(field, "ownership", lambda *_args, **_kwargs: {"nodes": 0})
    monkeypatch.setattr(
        field, "row_geometry", lambda *_args, **_kwargs: {"events": 1, "probes": 1}
    )
    result = field.all_geometry(
        packet, audit, cover, baseline, budget=field.Budget(time.monotonic() + 5, 272)
    )
    assert result["status"] == "INCOMPLETE"
    assert result["work_units"] == 272
    assert len(result["rows_checked"]) == 136
    assert result["rows_pending"] == []
    assert result["canonical_cases_excluded"] == 0
