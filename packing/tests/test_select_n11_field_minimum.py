"""The minimum field selection is exact, refuses weak receipts, and matches the record."""

from __future__ import annotations

import gzip
import hashlib
import json
import random
from itertools import combinations
from pathlib import Path
from typing import Any

import pytest

from devtools.select_n11_field_minimum import INVENTORY, PASS, minimum_covers, select

RETAINED = INVENTORY.parent / "minimal-selection.json"
OMITTED = {
    "72e06f08ab0775ec073aa444ac9b698b1ef6746351b5d40435d4a03db231db6b",
    "a323908f1c75407dd57042df054434401df05fdf9332bc5c71271cd54869890d",
}
CASE_1456_PACKET = "59db0f81f262d5cbe27607cd6a45d464caeb8981645bed45d03b81b30d82dc65"


def receipt(packet: str, mask: int, cases: list[int], rows: int) -> dict[str, Any]:
    return {
        "status": PASS,
        "geometry_verified": True,
        "global_optimality_proved": False,
        "rows_pending": [],
        "ownership_pending": [],
        "packet_sha256": packet,
        "checker_sha256": "c" * 64,
        "audit_proposal_sha256": "a" * 64,
        "mask_index": mask,
        "canonical_cases_excluded": len(cases),
        "transfer": {"transferred_case_ids": cases, "direct_case_ids": cases[:1]},
        "positive_cell_rows": rows,
        "rows_checked": [{}] * rows,
        "ownership_points": 1,
        "ownership_checked": [{}],
    }


def write_family(
    root: Path, family: dict[str, tuple[list[int], int]], *, declared: list[int] | None = None
) -> Path:
    """Write a synthetic inventory whose packets are named by single letters."""
    records = []
    union: set[int] = set()
    for name, (cases, rows) in sorted(family.items()):
        packet = name * 64
        raw = json.dumps(receipt(packet, ord(name), cases, rows)).encode()
        path = root / "receipts" / name / "result.json.gz"
        path.parent.mkdir(parents=True)
        path.write_bytes(gzip.compress(raw, mtime=0))
        records.append(
            {
                "checker_sha256": "c" * 64,
                "decoded_sha256": hashlib.sha256(raw).hexdigest(),
                "packet_sha256": packet,
                "path": path.relative_to(root).as_posix(),
            }
        )
        union |= set(cases)
    inventory = root / "inventory.json"
    inventory.write_text(
        json.dumps(
            {
                "accepted_receipts": records,
                "previously_accepted_field_case_ids": sorted(union)
                if declared is None
                else declared,
            }
        )
    )
    return inventory


# Case 0 is private to "p". Of the rest, a greedy pick of the largest set "g" still needs
# "m", and "l"+"r" is the same size with fewer rows, so the tie-break must see both.
SYNTHETIC = {
    "p": ([0, 1], 5),
    "g": ([1, 2, 3, 4], 100),
    "l": ([1, 2, 5], 40),
    "r": ([3, 4, 6], 40),
    "m": ([5, 6], 10),
    "s": ([5], 1),
    "t": ([6], 1),
}


def test_synthetic_family_has_exact_minimum_and_tie_break(tmp_path: Path) -> None:
    manifest = select(write_family(tmp_path, SYNTHETIC), repo=tmp_path, expected_sha=None)
    assert manifest["distinct_accepted_packets"] == 7
    assert manifest["union_check"]["case_count"] == 7
    assert manifest["mandatory_count"] == 1
    assert manifest["mandatory_witnesses"][0]["private_case_ids"] == [0]
    assert manifest["remainder_case_ids"] == [2, 3, 4, 5, 6]
    assert manifest["remainder_minimum_size"] == 2
    assert manifest["minimum_size"] == 3
    assert manifest["minimum_selection_count"] == 2
    selected = {row["packet_sha256"][0] for row in manifest["selected_receipts"]}
    assert selected == {"p", "l", "r"}
    assert manifest["totals"]["selected"]["complete_angle_rows"] == 85
    assert "There are 2 minimum selections" in manifest["minimality"]


def test_search_agrees_with_brute_force() -> None:
    generator = random.Random(20261003)
    for _ in range(200):
        universe = frozenset(range(generator.randint(1, 9)))
        sets = {
            f"s{index}": frozenset(
                generator.sample(sorted(universe), generator.randint(1, min(4, len(universe))))
            )
            for index in range(generator.randint(1, 7))
        }
        covered = frozenset().union(*sets.values())
        universe &= covered
        cover = minimum_covers(universe, sets, max_nodes=100_000)
        brute: list[frozenset[str]] = []
        for size in range(len(sets) + 1):
            brute = [
                frozenset(keys)
                for keys in combinations(sorted(sets), size)
                if universe <= frozenset().union(*(sets[key] for key in keys))
            ]
            if brute:
                break
        assert cover.size == len(next(iter(brute)))
        assert set(cover.selections) == set(brute)


def test_node_ceiling_refuses_rather_than_truncating() -> None:
    sets = {f"s{index}": frozenset({index, index + 1}) for index in range(12)}
    with pytest.raises(ValueError, match="node ceiling"):
        minimum_covers(frozenset(range(13)), sets, max_nodes=5)


def test_refuses_incomplete_or_altered_receipts(tmp_path: Path) -> None:
    inventory = write_family(tmp_path, {"a": ([0, 1], 3), "b": ([1, 2], 3)})
    path = tmp_path / "receipts/b/result.json.gz"
    record = receipt("b" * 64, ord("b"), [1, 2], 3)
    path.write_bytes(gzip.compress(json.dumps({**record, "rows_pending": [7]}).encode()))
    with pytest.raises(ValueError, match="receipt bytes differ"):
        select(inventory, repo=tmp_path, expected_sha=None)
    data = json.loads(inventory.read_text())
    data["accepted_receipts"][1]["decoded_sha256"] = hashlib.sha256(
        gzip.decompress(path.read_bytes())
    ).hexdigest()
    inventory.write_text(json.dumps(data))
    with pytest.raises(ValueError, match="not a complete field PASS"):
        select(inventory, repo=tmp_path, expected_sha=None)


def test_refuses_a_union_that_differs_from_the_declared_one(tmp_path: Path) -> None:
    inventory = write_family(tmp_path, {"a": ([0, 1], 3)}, declared=[0, 1, 2])
    with pytest.raises(ValueError, match="declared field union"):
        select(inventory, repo=tmp_path, expected_sha=None)


def test_real_inventory_counts_and_retained_manifest() -> None:
    manifest = select(INVENTORY)
    assert manifest["accepted_receipt_records"] == 46
    assert manifest["distinct_accepted_packets"] == 46
    assert manifest["union_check"] == {
        "case_count": 1904,
        "equals_inventory_field_case_ids": True,
        "selected_union_equals_full_union": True,
    }
    assert manifest["coverage_histogram"]["1"] == 858
    assert manifest["mandatory_count"] == 44
    assert manifest["mandatory_union_case_count"] == 1904
    assert manifest["remainder_case_ids"] == []
    assert manifest["minimum_size"] == 44
    assert manifest["minimum_selection_count"] == 1
    assert {row["packet_sha256"] for row in manifest["omitted_receipts"]} == OMITTED
    witness = next(
        row
        for row in manifest["mandatory_witnesses"]
        if row["packet_sha256"] == CASE_1456_PACKET
    )
    assert witness["private_case_ids"] == [1456]
    assert manifest["totals"]["selected"] == {
        "packets": 44,
        "complete_angle_rows": 17963,
        "ownership_points": 4233,
    }
    assert json.loads(RETAINED.read_text()) == manifest
