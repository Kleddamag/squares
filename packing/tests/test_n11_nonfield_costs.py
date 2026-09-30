"""Retained batch walls and overlapping case costs keep distinct meanings."""

from __future__ import annotations

import gzip
import hashlib
import json
from pathlib import Path
from typing import Any

import pytest

from devtools import summarize_n11_nonfield_costs as costs


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _record(root: Path, case: int, checker: str, *, complete: bool) -> dict[str, Any]:
    receipt = {
        "status": "PASS_ONE_GENERIC_EXCLUSION" if complete else "REFUSED",
        "mask_index": case,
        "source_sha256": {"checker": checker},
        "geometry_verified": complete,
        "global_optimality_proved": False,
        "excluded_case_ids": [case] if complete else [],
        "wall_seconds": 8.0,
        "coordinator_process_cpu_seconds": 5.0,
        "child_process_cpu_seconds": 2.0,
        "rows_checked": 2,
        "step_timings": [
            {
                "row_timings": [
                    {"collision_facet_checks": 4},
                    {"collision_facet_checks": 5},
                ]
            }
        ],
    }
    raw = json.dumps(receipt).encode()
    packed = gzip.compress(raw, mtime=0)
    name = f"batch/case-{case}.json.gz"
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(packed)
    return {
        "mask_index": case,
        "exit_code": 0 if complete else 2,
        "status": "COMPLETE_CASE" if complete else "PROCESS_REFUSED",
        "excluded_case_ids": [case] if complete else [],
        "invocation_wall_seconds": 9.0,
        "receipt": name,
        "receipt_sha256": _sha(packed),
        "receipt_decoded_sha256": _sha(raw),
    }


def _summary(root: Path, records: list[dict[str, Any]], *, wall: float = 10.0) -> Path:
    requested = sorted(record["mask_index"] for record in records)
    complete = [
        record["mask_index"] for record in records if record["status"] == "COMPLETE_CASE"
    ]
    summary = {
        "status": (
            "COMPLETE_SELECTED_CASES" if len(complete) == len(records) else "INCOMPLETE_BATCH"
        ),
        "source_revision": "pinned-source",
        "runner_sha256": "1" * 64,
        "checker_sha256": "2" * 64,
        "requested_case_ids": requested,
        "excluded_case_ids": sorted(complete),
        "remaining_case_ids": sorted(set(requested) - set(complete)),
        "global_optimality_proved": False,
        "wall_seconds": wall,
        "jobs": 2,
        "workers_per_case": 1,
        "results": records,
    }
    path = root / "batch/summary.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(summary))
    return path


def test_parallel_case_wall_sum_is_not_batch_wall(tmp_path: Path) -> None:
    checker = "2" * 64
    source = _summary(
        tmp_path,
        [
            _record(tmp_path, 3, checker, complete=True),
            _record(tmp_path, 5, checker, complete=False),
        ],
    )
    batch = costs.batch_cost(source, tmp_path)
    assert batch["batch_executor_wall_seconds"] == 10
    assert batch["sum_case_invocation_wall_seconds"] == 18
    assert batch["sum_checker_wall_seconds"] == 16
    assert batch["sum_checker_cpu_seconds"] == 14
    assert batch["sum_invocation_minus_checker_wall_seconds"] == 2
    assert batch["complete_case_ids"] == [3]
    assert batch["not_complete_case_ids"] == [5]
    assert batch["rows_checked_in_completed_steps"] == 4
    assert batch["facets_checked_in_completed_steps"] == 18
    report = costs.summarize([source], tmp_path)
    assert report["agent_analysis_time_measured"] is False
    assert report["case_wall_sums_overlap_when_jobs_exceed_one"] is True


def test_missing_receipt_is_explicitly_unknown(tmp_path: Path) -> None:
    record = {
        "mask_index": 7,
        "status": "BATCH_DEADLINE",
        "excluded_case_ids": [],
    }
    batch = costs.batch_cost(_summary(tmp_path, [record]), tmp_path)
    assert batch["case_receipts_missing"] == 1
    assert batch["cases"][0]["checker_wall_seconds"] is None
    assert batch["sum_checker_wall_seconds"] is None
    assert batch["complete_case_ids"] == []


def test_tampered_or_misbound_receipt_refuses(tmp_path: Path) -> None:
    record = _record(tmp_path, 3, "2" * 64, complete=True)
    source = _summary(tmp_path, [record])
    (tmp_path / record["receipt"]).write_bytes(b"changed")
    with pytest.raises(ValueError, match="receipt SHA"):
        costs.batch_cost(source, tmp_path)
    record["receipt_sha256"] = _sha(b"changed")
    with pytest.raises((ValueError, gzip.BadGzipFile, EOFError)):
        costs.batch_cost(_summary(tmp_path, [record]), tmp_path)


def test_complete_case_without_receipt_refuses(tmp_path: Path) -> None:
    source = _summary(
        tmp_path,
        [{"mask_index": 3, "status": "COMPLETE_CASE", "excluded_case_ids": [3]}],
    )
    with pytest.raises(ValueError, match="lacks receipt"):
        costs.batch_cost(source, tmp_path)


def test_older_receipt_without_facet_metric_stays_unknown(tmp_path: Path) -> None:
    record = _record(tmp_path, 3, "2" * 64, complete=True)
    path = tmp_path / record["receipt"]
    result = json.loads(gzip.decompress(path.read_bytes()))
    del result["step_timings"][0]["row_timings"][0]["collision_facet_checks"]
    raw = json.dumps(result).encode()
    packed = gzip.compress(raw, mtime=0)
    path.write_bytes(packed)
    record["receipt_sha256"] = _sha(packed)
    record["receipt_decoded_sha256"] = _sha(raw)
    batch = costs.batch_cost(_summary(tmp_path, [record]), tmp_path)
    assert batch["cases"][0]["completed_step_facets"] is None
    assert batch["case_facet_counts_missing"] == 1
    assert batch["facets_checked_in_completed_steps"] is None
