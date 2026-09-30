"""Run admitted field proposals concurrently with independent per-field deadlines.

Retain each complete or incomplete checker result. The batch never promotes a
partial field and never claims global optimality. Receipt review is separate.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import signal
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

from devtools import check_n11_optimality_field_mask0 as kernel
from devtools import check_n11_optimality_field_runner as runner

REPO = Path(__file__).resolve().parents[2]
PACKING = REPO / "packing"


def run_field(
    entry: dict[str, Any], seconds: float, workers: int, attempt: str | None
) -> dict[str, Any]:
    descriptor = (REPO / entry["descriptor"]).resolve()
    runner.require(
        descriptor.is_relative_to(kernel.PACKET), "descriptor outside retained packet"
    )
    root = descriptor.parent
    output_root = root if attempt is None else root / attempt
    output_root.mkdir(exist_ok=True)
    target = output_root / "result.json.gz"
    runner.require(
        not target.exists(), "result exists; review it before selecting a new receipt directory"
    )
    command = [
        sys.executable,
        "-m",
        "devtools.check_n11_optimality_field_runner",
        "--descriptor",
        str(descriptor),
        "--mask-index",
        str(entry["mask_index"]),
        "--objects",
        str(root / "objects"),
        "--cover",
        str(kernel.PACKET / "receipts/d4-independent/objects" / f"{kernel.COVER_SHA}.gz"),
        "--all",
        "--workers",
        str(workers),
        "--max-seconds",
        str(seconds),
        "--max-work",
        "5000000",
    ]
    started = time.monotonic()
    with subprocess.Popen(
        command,
        cwd=PACKING,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        start_new_session=True,
    ) as process:
        try:
            output, error = process.communicate(timeout=seconds + 3)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            process.communicate()
            return {
                "mask_index": entry["mask_index"],
                "status": "OUTER_TIMEOUT",
                "canonical_cases_excluded": 0,
            }
    if process.returncode not in (0, 2) or error:
        return {
            "mask_index": entry["mask_index"],
            "status": "PROCESS_REFUSED",
            "canonical_cases_excluded": 0,
            "exit_code": process.returncode,
            "stderr": error.decode(errors="replace"),
        }
    result = kernel.strict_json(output)
    complete = result.get("status") == "PASS_ONE_FIELD_GEOMETRY_AND_TRANSFER"
    runner.require(
        not complete
        or (
            process.returncode == 0
            and result.get("geometry_verified") is True
            and result.get("ownership_pending") == []
            and result.get("rows_pending") == []
        ),
        "inconsistent complete result",
    )
    packed = gzip.compress(output, mtime=0)
    target.open("xb").write(packed)
    summary = {
        key: value
        for key, value in result.items()
        if key
        not in {
            "ownership_checked",
            "rows_checked",
            "transfer",
            "ownership_pending",
            "rows_pending",
        }
    }
    summary.update(
        full_result_path="result.json.gz",
        full_result_decoded_sha256=hashlib.sha256(output).hexdigest(),
        full_result_compressed_sha256=hashlib.sha256(packed).hexdigest(),
        invocation_wall_seconds=time.monotonic() - started,
        command=command,
    )
    (output_root / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n"
    )
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("selection", type=Path)
    parser.add_argument("--jobs", type=int, choices=range(1, 5), default=3)
    parser.add_argument("--seconds", type=float, default=55)
    parser.add_argument("--field-workers", type=int, choices=range(1, 5), default=1)
    parser.add_argument("--attempt-name")
    parser.add_argument("--retry-incomplete-only", action="store_true")
    args = parser.parse_args()
    runner.require(args.jobs * args.field_workers <= 4, "total worker ceiling is four")
    runner.require(
        args.attempt_name is None
        or (
            args.attempt_name not in {".", ".."}
            and args.attempt_name.isascii()
            and all(c.isalnum() or c in "-_" for c in args.attempt_name)
            and bool(args.attempt_name)
        ),
        "attempt name must be a simple directory name",
    )
    runner.require(
        not args.retry_incomplete_only or args.attempt_name is not None,
        "retries must preserve prior receipts in a named attempt directory",
    )
    runner.require(0 < args.seconds <= 55, "field ceiling must be positive and <=55 seconds")
    selection = kernel.strict_json(args.selection.read_bytes())
    runner.require(
        selection.get("source_revision") == kernel.SOURCE_REVISION, "selection source differs"
    )
    entries = [
        entry
        for entry in selection["fields"]
        if entry.get("status") == "SUPPORTED_PROPOSAL_ONLY"
    ]
    if args.retry_incomplete_only:
        entries = [
            entry
            for entry in entries
            if kernel.strict_json(
                gzip.decompress(
                    (REPO / entry["descriptor"]).with_name("result.json.gz").read_bytes()
                )
            ).get("status")
            == "INCOMPLETE"
        ]
    runner.require(bool(entries), "selection has no admitted proposals")
    source = Path(runner.__file__).read_bytes()
    start = time.monotonic()
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        results = list(
            pool.map(
                lambda entry: run_field(
                    entry, args.seconds, args.field_workers, args.attempt_name
                ),
                entries,
            )
        )
    runner.require(Path(runner.__file__).read_bytes() == source, "runner changed during batch")
    complete = all(
        value.get("status") == "PASS_ONE_FIELD_GEOMETRY_AND_TRANSFER" for value in results
    )
    report = {
        "status": "COMPLETE_SELECTED_FIELDS" if complete else "INCOMPLETE_SELECTED_FIELDS",
        "global_optimality_proved": False,
        "wall_seconds": time.monotonic() - start,
        "jobs": args.jobs,
        "field_workers": args.field_workers,
        "attempt_name": args.attempt_name,
        "fields": [
            {
                key: value.get(key)
                for key in (
                    "mask_index",
                    "status",
                    "canonical_cases_excluded",
                    "wall_seconds",
                    "process_cpu_seconds",
                    "invocation_wall_seconds",
                )
            }
            for value in results
        ],
    }
    suffix = "" if args.attempt_name is None else "-" + args.attempt_name
    args.selection.with_name(args.selection.stem + suffix + "-result.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(report, indent=2))
    sys.exit(0 if complete else 2)


if __name__ == "__main__":
    main()
