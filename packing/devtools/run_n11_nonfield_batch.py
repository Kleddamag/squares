"""Run explicit non-field cases with bounded case and row parallelism.

Only complete executions receive case credit. This orchestration receipt does
not replace mathematical review of the checker or establish global optimality.
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
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

from strif import atomic_write_bytes, atomic_write_text

from devtools.prepare_n11_nonfield_manifest import PACKET, REPO, REVISION, require

CHECKER = REPO / "packing/devtools/check_n11_generic_sequential.py"


def source_archive_allowed(path: Path, repo: Path, common_dir: Path) -> bool:
    """Allow local inputs or the same Git repository's pinned shared archive."""
    resolved = path.resolve()
    shared = common_dir.resolve().parent / "attic/n11-proof-inputs" / REVISION / "objects"
    return resolved.is_relative_to(repo.resolve()) or (
        common_dir.name == ".git" and resolved.is_relative_to(shared.resolve())
    )


def source_archive_reference(path: Path, repo: Path, common_dir: Path) -> dict[str, str]:
    """Describe local and shared inputs without assuming checkout-local paths."""
    require(
        source_archive_allowed(path, repo, common_dir), "objects outside repository archive"
    )
    resolved = path.resolve()
    local = resolved.is_relative_to(repo.resolve())
    root = repo.resolve() if local else common_dir.resolve().parent
    return {
        "objects": resolved.relative_to(root).as_posix(),
        "objects_checkout": "execution" if local else "git_common_primary",
    }


def retain_receipt(path: Path, raw: bytes, *, remove_original: bool = True) -> tuple[Path, str]:
    """Losslessly compress large row ledgers while retaining their exact bytes."""
    if len(raw) < 16_384:
        return path, hashlib.sha256(raw).hexdigest()
    require(path.read_bytes() == raw, "receipt changed before retention")
    packed = gzip.compress(raw, mtime=0)
    target = path.with_suffix(path.suffix + ".gz")
    if target.exists():
        require(target.read_bytes() == packed, "different compressed receipt already exists")
    else:
        atomic_write_bytes(target, packed)
    require(gzip.decompress(target.read_bytes()) == raw, "receipt compression changed bytes")
    if remove_original:
        path.unlink()
    return target, hashlib.sha256(packed).hexdigest()


def complete_case(record: dict[str, Any], case: int, checker_sha: str, exit_code: int) -> bool:
    return (
        exit_code == 0
        and record.get("status") == "PASS_ONE_GENERIC_EXCLUSION"
        and record.get("geometry_verified") is True
        and record.get("global_optimality_proved") is False
        and record.get("excluded_case_ids") == [case]
        and record.get("mask_index") == case
        and all(
            key in record and record[key] is None
            for key in ("current_node", "current_step", "current_row")
        )
        and record.get("source_sha256", {}).get("checker") == checker_sha
    )


def run_case(
    case: int, args: argparse.Namespace, checker_sha: str, deadline: float
) -> dict[str, Any]:
    available = min(args.seconds, deadline - time.monotonic() - 5)
    if available <= 0:
        return {"mask_index": case, "status": "BATCH_DEADLINE", "excluded_case_ids": []}
    target = args.out_dir / f"case-{case}.json"
    command = [
        sys.executable,
        "-m",
        "devtools.check_n11_generic_sequential",
        "--case-id",
        str(case),
        "--manifest",
        str(args.manifest.resolve()),
        "--objects",
        str(args.objects.resolve()),
        "--workers",
        str(args.workers),
        "--cover-backend",
        args.cover_backend,
        "--collision-backend",
        args.collision_backend,
        "--max-seconds",
        str(available),
        "--max-events",
        "50000",
        "--out",
        str(target),
    ]
    started = time.monotonic()
    with subprocess.Popen(
        command,
        cwd=REPO / "packing",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        start_new_session=True,
    ) as process:
        try:
            _output, error = process.communicate(timeout=available + 5)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            process.communicate()
            return {"mask_index": case, "status": "OUTER_TIMEOUT", "excluded_case_ids": []}
    summary: dict[str, Any] = {
        "mask_index": case,
        "exit_code": process.returncode,
        "invocation_wall_seconds": time.monotonic() - started,
        "status": "PROCESS_REFUSED",
        "excluded_case_ids": [],
        "invocation": {
            "module": "devtools.check_n11_generic_sequential",
            "working_directory": "packing",
            "manifest": args.manifest.resolve().relative_to(REPO).as_posix(),
            **args.objects_reference,
            "workers": args.workers,
            "cover_backend": args.cover_backend,
            "collision_backend": args.collision_backend,
            "max_seconds": available,
            "max_events": 50000,
        },
    }
    if error:
        summary["stderr"] = error.decode(errors="replace")[-4000:]
    if target.is_file() and target.stat().st_size <= 10_000_000:
        raw = target.read_bytes()
        retained, retained_sha = retain_receipt(target, raw)
        summary["receipt_sha256"] = retained_sha
        summary["receipt_decoded_sha256"] = hashlib.sha256(raw).hexdigest()
        summary["receipt"] = retained.relative_to(REPO).as_posix()
        try:
            record = json.loads(raw)
            accepted = not error and complete_case(
                record, case, checker_sha, process.returncode
            )
            if accepted:
                summary["status"] = "COMPLETE_CASE"
                summary["excluded_case_ids"] = [case]
            else:
                summary["checker_status"] = record.get("status")
                summary["reason"] = record.get("reason", record.get("error"))
        except (ValueError, AttributeError, TypeError) as exc:
            summary["reason"] = str(exc)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--objects", type=Path, required=True)
    parser.add_argument("--cases", type=int, nargs="+", required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    available_cpus = os.process_cpu_count() or 1
    parser.add_argument("--jobs", type=int, choices=range(1, 9), default=2)
    parser.add_argument("--workers", type=int, choices=range(1, 4), default=1)
    parser.add_argument("--cover-backend", choices=("reference", "fast"), default="reference")
    parser.add_argument(
        "--collision-backend", choices=("reference", "integer"), default="reference"
    )
    parser.add_argument("--cpu-budget", type=int, default=min(8, available_cpus))
    parser.add_argument("--seconds", type=float, default=55)
    parser.add_argument("--batch-seconds", type=float, default=300)
    args = parser.parse_args()
    require(
        1 <= args.cpu_budget <= available_cpus and args.jobs * args.workers <= args.cpu_budget,
        "case and row pools exceed the selected host CPU budget",
    )
    require(0 < args.seconds <= 3600 and 0 < args.batch_seconds <= 14400, "wall ceiling")
    require(1 <= len(args.cases) <= 32 and len(set(args.cases)) == len(args.cases), "case list")
    require(all(0 <= case < 2184 for case in args.cases), "case index outside census")
    require(args.manifest.resolve().is_relative_to(PACKET), "manifest outside pinned packet")
    common = subprocess.run(
        ["git", "rev-parse", "--path-format=absolute", "--git-common-dir"],
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
        timeout=5,
    )
    require(
        source_archive_allowed(args.objects, REPO, Path(common.stdout.strip())),
        "objects outside repository archive",
    )
    args.objects_reference = source_archive_reference(
        args.objects, REPO, Path(common.stdout.strip())
    )
    args.out_dir = args.out_dir.resolve()
    require(args.out_dir.is_relative_to(PACKET), "retain receipts in the source packet")
    require(not args.out_dir.exists(), "use a new attempt directory")
    before = Path(__file__).read_bytes()
    checker_before = CHECKER.read_bytes()
    checker_sha = hashlib.sha256(checker_before).hexdigest()
    args.out_dir.mkdir(parents=True)
    started = time.monotonic()
    deadline = started + args.batch_seconds
    results = []
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures = {
            pool.submit(run_case, case, args, checker_sha, deadline): case
            for case in args.cases
        }
        for future in as_completed(futures):
            try:
                result = future.result()
            except (OSError, ValueError, RuntimeError) as exc:
                result = {
                    "mask_index": futures[future],
                    "status": "PROCESS_REFUSED",
                    "excluded_case_ids": [],
                    "reason": str(exc),
                }
            results.append(result)
            print(
                json.dumps({key: result[key] for key in ("mask_index", "status")}), flush=True
            )
    require(Path(__file__).read_bytes() == before, "batch runner changed during execution")
    require(CHECKER.read_bytes() == checker_before, "checker changed during execution")
    accepted = sorted(case for result in results for case in result["excluded_case_ids"])
    report = {
        "status": "COMPLETE_SELECTED_CASES"
        if accepted == sorted(args.cases)
        else "INCOMPLETE_BATCH",
        "source_revision": REVISION,
        "runner_sha256": hashlib.sha256(before).hexdigest(),
        "checker_sha256": checker_sha,
        "requested_case_ids": sorted(args.cases),
        "excluded_case_ids": accepted,
        "remaining_case_ids": sorted(set(args.cases) - set(accepted)),
        "global_optimality_proved": False,
        "wall_seconds": time.monotonic() - started,
        "max_batch_seconds": args.batch_seconds,
        "jobs": args.jobs,
        "workers_per_case": args.workers,
        "cpu_budget": args.cpu_budget,
        "host_process_cpu_count": available_cpus,
        "results": sorted(results, key=lambda result: result["mask_index"]),
    }
    atomic_write_text(args.out_dir / "summary.json", json.dumps(report, indent=2) + "\n")
    return 0 if report["status"] == "COMPLETE_SELECTED_CASES" else 2


if __name__ == "__main__":
    raise SystemExit(main())
