"""Receipt bookkeeping rejects invented credit, stale bytes and incomplete cases."""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest

from devtools.inventory_n11_exclusions import REVIEWED_CHECKERS, REVISION, admitted_batch


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
