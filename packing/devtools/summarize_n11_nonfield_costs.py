"""Summarize selected, retained non-field batch execution receipts.

Case-wall sums overlap when jobs run in parallel. Only each batch summary's
wall_seconds measures its executor's elapsed wall time; neither number measures
agent analysis or the full campaign.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import math
from pathlib import Path
from typing import Any

from strif import atomic_write_text

REPO = Path(__file__).resolve().parents[2]
MAX_SUMMARY_BYTES = 2_000_000
MAX_RECEIPT_BYTES = 10_000_000


def require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def unique_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        require(key not in value, f"duplicate JSON key: {key}")
        value[key] = item
    return value


def reject_constant(value: str) -> None:
    raise ValueError(f"invalid JSON constant: {value}")


def strict_json(raw: bytes) -> dict[str, Any]:
    value = json.loads(
        raw,
        object_pairs_hook=unique_pairs,
        parse_constant=reject_constant,
    )
    require(isinstance(value, dict), "JSON root is not an object")
    return value


def bounded_bytes(path: Path, limit: int) -> bytes:
    with path.open("rb") as stream:
        raw = stream.read(limit + 1)
    require(len(raw) <= limit, f"oversized input: {path}")
    return raw


def seconds(value: Any, field: str) -> float:
    require(type(value) in (int, float), f"invalid {field}")
    try:
        number = float(value)
    except OverflowError as error:
        raise ValueError(f"invalid {field}") from error
    require(math.isfinite(number) and number >= 0, f"invalid {field}")
    return number


def count(value: Any, field: str) -> int:
    require(type(value) is int and value >= 0, f"invalid {field}")
    return value


def sha(value: Any, field: str) -> str:
    require(
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value),
        f"invalid {field}",
    )
    return value


def receipt(record: dict[str, Any], case: int, checker_sha: str, repo: Path) -> dict[str, Any]:
    declared = record["receipt"]
    require(isinstance(declared, str) and not Path(declared).is_absolute(), "receipt path")
    path = (repo / declared).resolve()
    require(path.is_relative_to(repo.resolve()), "receipt outside repository")
    packed = bounded_bytes(path, MAX_RECEIPT_BYTES)
    require(digest(packed) == sha(record["receipt_sha256"], "receipt SHA"), "receipt SHA")
    if path.suffix == ".gz":
        with gzip.GzipFile(fileobj=io.BytesIO(packed)) as stream:
            raw = stream.read(MAX_RECEIPT_BYTES + 1)
        require(len(raw) <= MAX_RECEIPT_BYTES, "oversized decoded receipt")
    else:
        raw = packed
    require(
        digest(raw) == sha(record["receipt_decoded_sha256"], "decoded receipt SHA"),
        "decoded receipt SHA",
    )
    result = strict_json(raw)
    require(result.get("mask_index") == case, "receipt case identity")
    require(
        result.get("source_sha256", {}).get("checker") == checker_sha,
        "receipt checker identity",
    )
    return result


def case_cost(record: dict[str, Any], checker_sha: str, repo: Path) -> dict[str, Any]:
    case = count(record.get("mask_index"), "case ID")
    status = record.get("status")
    require(isinstance(status, str), "case status")
    invocation = (
        seconds(record["invocation_wall_seconds"], "invocation wall")
        if "invocation_wall_seconds" in record
        else None
    )
    output: dict[str, Any] = {
        "mask_index": case,
        "status": status,
        "invocation_wall_seconds": invocation,
        "checker_wall_seconds": None,
        "checker_cpu_seconds": None,
        "invocation_minus_checker_wall_seconds": None,
        "rows_checked": None,
        "completed_step_facets": None,
        "receipt_present": "receipt" in record,
    }
    if "receipt" not in record:
        require(status != "COMPLETE_CASE", "complete case lacks receipt")
        return output
    checked = receipt(record, case, checker_sha, repo)
    if status == "COMPLETE_CASE":
        require(
            record.get("exit_code") == 0
            and record.get("excluded_case_ids") == [case]
            and checked.get("status") == "PASS_ONE_GENERIC_EXCLUSION"
            and checked.get("geometry_verified") is True
            and checked.get("excluded_case_ids") == [case]
            and checked.get("global_optimality_proved") is False,
            "complete-case receipt disagreement",
        )
    wall = seconds(checked.get("wall_seconds"), "checker wall")
    parent_cpu = seconds(checked.get("coordinator_process_cpu_seconds"), "parent CPU")
    child_cpu = seconds(checked.get("child_process_cpu_seconds"), "child CPU")
    rows = count(checked.get("rows_checked", 0), "rows checked")
    timings = checked.get("step_timings", [])
    require(isinstance(timings, list), "step timing inventory")
    timed_rows = [row for step in timings for row in step["row_timings"]]
    facets = (
        sum(count(row["collision_facet_checks"], "facet count") for row in timed_rows)
        if all("collision_facet_checks" in row for row in timed_rows)
        else None
    )
    output.update(
        checker_wall_seconds=wall,
        checker_cpu_seconds=parent_cpu + child_cpu,
        invocation_minus_checker_wall_seconds=(
            invocation - wall if invocation is not None else None
        ),
        rows_checked=rows,
        completed_step_facets=facets,
        checker_status=checked.get("status"),
        receipt_sha256=record["receipt_sha256"],
    )
    return output


def batch_cost(path: Path, repo: Path = REPO) -> dict[str, Any]:
    summary_path = path.resolve()
    require(summary_path.is_relative_to(repo.resolve()), "batch outside repository")
    raw = bounded_bytes(summary_path, MAX_SUMMARY_BYTES)
    summary = strict_json(raw)
    requested = summary.get("requested_case_ids")
    records = summary.get("results")
    if not isinstance(requested, list) or not isinstance(records, list):
        raise TypeError("batch inventory")
    require(
        all(type(case) is int and 0 <= case < 2184 for case in requested)
        and len(requested) == len(set(requested)),
        "requested case inventory",
    )
    checker_sha = sha(summary.get("checker_sha256"), "checker SHA")
    runner_sha = sha(summary.get("runner_sha256"), "runner SHA")
    cases = [case_cost(record, checker_sha, repo) for record in records]
    require(
        sorted(item["mask_index"] for item in cases) == sorted(requested),
        "batch case inventory differs from requested",
    )
    complete = sorted(item["mask_index"] for item in cases if item["status"] == "COMPLETE_CASE")
    require(
        summary.get("excluded_case_ids") == complete
        and summary.get("remaining_case_ids") == sorted(set(requested) - set(complete))
        and summary.get("global_optimality_proved") is False,
        "batch exclusion inventory differs from case receipts",
    )
    expected_status = (
        "COMPLETE_SELECTED_CASES" if len(complete) == len(requested) else "INCOMPLETE_BATCH"
    )
    require(
        summary.get("status") == expected_status, "batch status differs from case inventory"
    )
    batch_wall = seconds(summary.get("wall_seconds"), "batch wall")

    def total(field: str) -> float | None:
        values = [item[field] for item in cases if item[field] is not None]
        return sum(values) if values else None

    return {
        "summary": summary_path.relative_to(repo.resolve()).as_posix(),
        "summary_sha256": digest(raw),
        "runner_sha256": runner_sha,
        "checker_sha256": checker_sha,
        "source_revision": summary.get("source_revision"),
        "batch_status": summary.get("status"),
        "jobs": count(summary.get("jobs"), "jobs"),
        "workers_per_case": count(summary.get("workers_per_case"), "workers per case"),
        "batch_executor_wall_seconds": batch_wall,
        "sum_case_invocation_wall_seconds": total("invocation_wall_seconds"),
        "sum_checker_wall_seconds": total("checker_wall_seconds"),
        "sum_checker_cpu_seconds": total("checker_cpu_seconds"),
        "sum_invocation_minus_checker_wall_seconds": total(
            "invocation_minus_checker_wall_seconds"
        ),
        "complete_case_ids": complete,
        "not_complete_case_ids": sorted(set(requested) - set(complete)),
        "case_receipts_present": sum(item["receipt_present"] for item in cases),
        "case_receipts_missing": sum(not item["receipt_present"] for item in cases),
        "case_facet_counts_missing": sum(
            item["completed_step_facets"] is None for item in cases
        ),
        "rows_checked_in_completed_steps": sum(
            item["rows_checked"] for item in cases if item["rows_checked"] is not None
        ),
        "facets_checked_in_completed_steps": (
            sum(item["completed_step_facets"] for item in cases)
            if all(item["completed_step_facets"] is not None for item in cases)
            else None
        ),
        "cases": cases,
    }


def summarize(paths: list[Path], repo: Path = REPO) -> dict[str, Any]:
    require(paths and len({path.resolve() for path in paths}) == len(paths), "batch selection")
    batches = [batch_cost(path, repo) for path in paths]
    return {
        "schema": "n11_nonfield_selected_costs_v1",
        "status": "MEASURED_SELECTED_BATCHES_ONLY",
        "tool_sha256": digest(Path(__file__).read_bytes()),
        "global_optimality_proved": False,
        "batch_walls_are_parallel_executor_elapsed_not_additive_campaign_wall": True,
        "case_wall_sums_overlap_when_jobs_exceed_one": True,
        "agent_analysis_time_measured": False,
        "batches": batches,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch", type=Path, action="append", required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    require(not args.out.exists(), "use a new cost-summary path")
    report = summarize(args.batch)
    atomic_write_text(args.out, json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": report["status"], "batches": len(report["batches"])}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
