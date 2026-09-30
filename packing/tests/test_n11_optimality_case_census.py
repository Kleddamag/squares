"""Independent controls for the reported n=11 case census only."""

from __future__ import annotations

import copy
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest

from devtools import check_n11_optimality_case_census as census

RECEIPT = census.PACKET / "receipts/case-census"
OBJECTS = RECEIPT / "objects"
COVER = census.PACKET / "receipts/d4-independent/objects" / f"{census.COVER_SHA256}.gz"


@pytest.fixture(scope="module")
def published() -> tuple[dict[str, Any], dict[str, Any]]:
    return census.load_inputs(census.PACKET, OBJECTS, COVER)


def audit(records: dict[str, Any], cover: dict[str, Any]) -> dict[str, Any]:
    return census.audit_records(records, cover, time.monotonic() + 15)


def make_case_id_boolean(row: dict[str, Any]) -> None:
    row["extension_entries"][0]["mask"] = True


def test_complete_reported_case_census_has_no_geometry_claim(
    published: tuple[dict[str, Any], dict[str, Any]],
) -> None:
    records, cover = published
    result = audit(records, cover)
    assert result["status"] == "PASS_CASE_CENSUS_ONLY"
    assert result["geometry_verified"] is False
    assert result["global_optimality_proved"] is False
    assert result["census_checked_case_ids"] == list(range(2184))
    assert result["census_unresolved_case_ids"] == []
    assert result["surviving_canonical_case_ids"] == list(census.SURVIVORS)
    assert result["geometrically_unverified_case_count"] == 2184
    assert len(result["reported_excluded_case_ids"]) == 2180


@pytest.mark.parametrize(
    ("object_name", "mutation", "message"),
    [
        (
            "A1",
            lambda row: row["excluded_canonical_mask_indices"].append(0),
            "duplicate case IDs",
        ),
        (
            "A1",
            lambda row: row.__setitem__("parent_side", "1/2"),
            "B=L/U premise changed",
        ),
        (
            "A2",
            make_case_id_boolean,
            "noninteger or out-of-range case ID",
        ),
        (
            "A2",
            lambda row: row["extension_entries"][0].__setitem__(
                "mask", row["extension_entries"][1]["mask"]
            ),
            "not one new case",
        ),
        (
            "A3",
            lambda row: row["cases"][0].__setitem__("job_id", "wrong-job"),
            "job differs",
        ),
        (
            "A3",
            lambda row: row["cases"][0].__setitem__("source_sha256", "0" * 64),
            "source/audit member binding differs",
        ),
        (
            "A4",
            lambda row: row["jobs"][1]["mask_indices"].append(
                row["jobs"][0]["mask_indices"][0]
            ),
            "mask map differs",
        ),
        (
            "A5",
            lambda row: row["unresolved_cases"].append(438),
            "expected 0 IDs",
        ),
    ],
)
def test_mutated_source_census_refuses(
    published: tuple[dict[str, Any], dict[str, Any]],
    object_name: str,
    mutation: Callable[[dict[str, Any]], None],
    message: str,
) -> None:
    records, cover = published
    changed = copy.deepcopy(records)
    mutation(changed[object_name])
    with pytest.raises(ValueError, match=message):
        audit(changed, cover)


def test_reordered_cover_and_expired_deadline_refuse(
    published: tuple[dict[str, Any], dict[str, Any]],
) -> None:
    records, cover = published
    changed = copy.deepcopy(cover)
    changed["canonical_eleven_cell_subsets"][0], changed["canonical_eleven_cell_subsets"][1] = (
        changed["canonical_eleven_cell_subsets"][1],
        changed["canonical_eleven_cell_subsets"][0],
    )
    with pytest.raises(ValueError, match="cover canonical mask array changed"):
        audit(records, changed)
    with pytest.raises(TimeoutError, match="baseline audit"):
        census.audit_records(records, cover, time.monotonic() - 1)


def test_object_tamper_refuses_before_json_parse(tmp_path: Path) -> None:
    pin = census.PINS["A5"]
    source = OBJECTS / f"{pin.decoded_sha256}.gz"
    changed = bytearray(source.read_bytes())
    changed[-1] ^= 1
    target = tmp_path / source.name
    target.write_bytes(changed)
    with pytest.raises(ValueError, match="compressed SHA-256 mismatch"):
        census.packed_json(
            target,
            compressed_sha=pin.lfs_sha256,
            compressed_size=pin.compressed_bytes,
            decoded_sha=pin.decoded_sha256,
            decoded_size=pin.decoded_bytes,
        )
