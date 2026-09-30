"""Receipt bookkeeping rejects invented credit, stale bytes and incomplete cases."""

from __future__ import annotations

import gzip
import hashlib
import json
from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest

from devtools.inventory_n11_exclusions import (
    PACKET,
    PILOTS,
    REPO,
    REVIEWED_CHECKERS,
    REVISION,
    admitted_batch,
    compact_batch,
    inventory,
)


def fixture_batch(tmp_path: Path) -> dict[str, Any]:
    checker = next(iter(REVIEWED_CHECKERS))
    receipt = {
        "status": "PASS_ONE_GENERIC_EXCLUSION",
        "geometry_verified": True,
        "global_optimality_proved": False,
        "excluded_case_ids": [2132],
        "mask_index": 2132,
        "current_node": None,
        "current_step": None,
        "current_row": None,
        "pending_row_indices": [],
        "source_sha256": {"checker": checker},
    }
    raw = json.dumps(receipt).encode()
    (tmp_path / "result.json").write_bytes(raw)
    return {
        "source_revision": REVISION,
        "checker_sha256": checker,
        "requested_case_ids": [2132],
        "excluded_case_ids": [2132],
        "remaining_case_ids": [],
        "global_optimality_proved": False,
        "results": [
            {
                "mask_index": 2132,
                "status": "COMPLETE_CASE",
                "exit_code": 0,
                "excluded_case_ids": [2132],
                "receipt": "result.json",
                "receipt_sha256": hashlib.sha256(raw).hexdigest(),
            }
        ],
    }


def test_complete_record_admits_only_its_exact_case(tmp_path: Path) -> None:
    batch = fixture_batch(tmp_path)
    assert admitted_batch(batch, tmp_path) == {2132}
    (tmp_path / "result.json").write_text("{}")
    with pytest.raises(ValueError, match="binding differs"):
        admitted_batch(batch, tmp_path)


def test_compaction_preserves_union_and_exact_decoded_receipt(tmp_path: Path) -> None:
    batch = fixture_batch(tmp_path)
    receipt = tmp_path / "result.json"
    raw = receipt.read_bytes() + b" " * 20_000
    receipt.write_bytes(raw)
    batch["results"][0]["receipt_sha256"] = hashlib.sha256(raw).hexdigest()
    path = tmp_path / "summary.json"
    path.write_text(json.dumps(batch))
    compact_batch(path, tmp_path)
    updated = json.loads(path.read_text())
    assert admitted_batch(updated, tmp_path) == {2132}
    assert gzip.decompress((tmp_path / updated["results"][0]["receipt"]).read_bytes()) == raw
    before = path.read_bytes()
    compact_batch(path, tmp_path)
    assert path.read_bytes() == before


@pytest.mark.parametrize(
    "mutation", ["checker", "missing", "duplicate", "exit", "partial", "union", "remainder"]
)
def test_inconsistent_execution_inventory_refuses(tmp_path: Path, mutation: str) -> None:
    batch = deepcopy(fixture_batch(tmp_path))
    if mutation == "checker":
        batch["checker_sha256"] = "unreviewed"
    elif mutation == "missing":
        batch["results"] = []
    elif mutation == "duplicate":
        batch["results"] *= 2
    elif mutation == "exit":
        batch["results"][0]["exit_code"] = 2
    elif mutation == "partial":
        batch["results"][0]["status"] = "INCOMPLETE"
    elif mutation == "union":
        batch["excluded_case_ids"] = [2132, 2135]
    else:
        batch["remaining_case_ids"] = [2132]
    with pytest.raises(ValueError, match=r"checker|execution|receipt|credit|union|remainder"):
        admitted_batch(batch, tmp_path)


def test_repeated_batch_credit_refuses_across_records() -> None:
    retained = json.loads((PACKET / "receipts/exclusion-inventory.json").read_text())
    relative = next(
        row["path"]
        for row in retained["execution_record_bindings"]
        if row["path"].endswith("/summary.json")
    )
    with pytest.raises(ValueError, match="duplicate accepted cases across records"):
        inventory([REPO / relative, REPO / relative])


def test_pilot_credit_cannot_reappear_in_a_batch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    pilot = next(iter(PILOTS.values()))[0]
    summary = tmp_path / "summary.json"
    summary.write_text("{}")
    monkeypatch.setattr(
        "devtools.inventory_n11_exclusions.admitted_batch", lambda _row: {pilot}
    )
    with pytest.raises(ValueError, match="duplicate accepted cases across records"):
        inventory([summary])
