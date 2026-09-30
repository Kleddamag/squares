"""Compare two exact rectangle kernels on the same bounded native CLI work."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import subprocess
import sys
import tempfile
from fractions import Fraction
from pathlib import Path
from typing import Any

from strif import atomic_write_bytes, atomic_write_text

from benchmarks.bench_rectangle_verifier_parity import run_command

REPO = Path(__file__).resolve().parents[2]
PACKING = REPO / "packing"
KERNEL = PACKING / "src/sqpack/rectangle_density.py"
CLI = PACKING / "devtools/verify_rectangle_density.py"
VOLUME = Path("/Volumes/spud-ext1")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def normalized(report: dict[str, Any]) -> dict[str, Any]:
    return {
        key: value
        for key, value in report.items()
        if key not in {"candidate", "checker_source_sha256", "timing"}
    }


def run(args: argparse.Namespace) -> dict[str, Any]:
    require(VOLUME.is_mount(), "external scratch volume is not mounted")
    scratch = args.scratch_root.resolve()
    require(scratch.is_relative_to(VOLUME / "agent-scratch"), "scratch must be external")
    scratch.mkdir(parents=True, exist_ok=True)
    require(0 < args.internal_seconds <= args.outer_seconds - 2, "need shutdown allowance")
    require(0 < args.outer_seconds <= 15, "outer ceiling must be <=15 seconds")
    expected_angles = set(range(201)) if args.angles == "all" else {int(args.angles)}
    require(
        expected_angles and min(expected_angles) >= 0 and max(expected_angles) < 201,
        "bad angles",
    )
    require(not args.out.exists(), "receipt directory already exists")
    source = args.candidate.resolve()
    require(source.is_relative_to(REPO), "candidate must be retained in repository")
    raw = source.read_bytes()
    relative = str(source.relative_to(REPO))
    require(digest(raw) == args.candidate_sha256, "candidate SHA differs")
    blob = subprocess.check_output(
        ["git", "-C", str(REPO), "hash-object", str(source)], text=True
    ).strip()
    committed = subprocess.check_output(
        ["git", "-C", str(REPO), "rev-parse", f"HEAD:{relative}"], text=True
    ).strip()
    require(blob == committed, "candidate bytes differ from committed HEAD")
    baseline = subprocess.check_output(
        [
            "git",
            "-C",
            str(REPO),
            "show",
            f"{args.baseline_ref}:packing/src/sqpack/rectangle_density.py",
        ]
    )
    current = KERNEL.read_bytes()
    cli_source = CLI.read_bytes()
    tool_source = Path(__file__).read_bytes()
    args.out.mkdir(parents=True)
    result: dict[str, Any] = {
        "status": "REFUSED",
        "scope": "same_fixed_work_native_cli_not_full_cpp_parity",
        "baseline_ref": args.baseline_ref,
        "baseline_kernel_sha256": digest(baseline),
        "current_kernel_sha256": digest(current),
        "cli_sha256": digest(cli_source),
        "runner_sha256": digest(tool_source),
        "candidate_path": relative,
        "candidate_sha256": digest(raw),
        "candidate_git_blob": blob,
        "n": args.n,
        "side": str(args.side),
        "threshold": str(args.threshold),
        "angles": args.angles,
        "max_nodes_per_angle": args.max_nodes,
        "max_depth": args.max_depth,
        "retain_pending_boxes": args.retain_pending_boxes,
        "internal_seconds": args.internal_seconds,
        "outer_seconds": args.outer_seconds,
        "speed_parity_established": False,
    }
    with tempfile.TemporaryDirectory(dir=scratch) as temporary:
        work = Path(temporary)
        candidate = work / "candidate.json"
        candidate.write_bytes(raw)
        reports: dict[str, dict[str, Any]] = {}
        for name, kernel_source in (("baseline", baseline), ("current", current)):
            overlay = work / name / "sqpack"
            overlay.mkdir(parents=True)
            (overlay / "__init__.py").write_text("", encoding="utf-8")
            (overlay / "rectangle_density.py").write_bytes(kernel_source)
            command = [
                "env",
                f"PYTHONPATH={overlay.parent}:{PACKING}",
                sys.executable,
                "-m",
                "devtools.verify_rectangle_density",
                str(candidate),
                "--n",
                str(args.n),
                "--side",
                str(args.side),
                "--threshold",
                str(args.threshold),
                "--angles",
                args.angles,
                "--max-nodes-per-angle",
                str(args.max_nodes),
                "--max-depth",
                str(args.max_depth),
                "--max-seconds",
                str(args.internal_seconds),
                "--timing",
            ]
            if args.retain_pending_boxes:
                command.append("--retain-pending-boxes")
            timing, stdout, stderr = run_command(
                command, cwd=PACKING, timeout=args.outer_seconds
            )
            atomic_write_bytes(
                args.out / f"{name}.stdout.json.gz", gzip.compress(stdout.encode(), mtime=0)
            )
            atomic_write_text(args.out / f"{name}.stderr", stderr)
            require(not timing["timed_out"], f"{name} exceeded outer ceiling")
            require(timing["exit_code"] in (0, 2), f"{name} refused or failed")
            report = json.loads(stdout)
            require(isinstance(report, dict), f"{name} did not return a JSON object")
            require(
                report.get("candidate_sha256") == digest(raw)
                and report.get("checker_source_sha256") == digest(kernel_source),
                f"{name} source or candidate binding differs",
            )
            rows = report.get("angles")
            require(
                isinstance(rows, list)
                and len(rows) == len(expected_angles)
                and {row.get("index") for row in rows if isinstance(row, dict)}
                == expected_angles
                and report.get("status") in {"VERIFIED", "INCONCLUSIVE"}
                and all(
                    isinstance(row, dict)
                    and row.get("status") in {"VERIFIED", "INCONCLUSIVE"}
                    and row.get("stop_cause") != "time_limit"
                    for row in rows
                ),
                f"{name} did not complete the requested fixed work",
            )
            reports[name] = report
            result[name] = {
                "process": timing,
                "status": report.get("status"),
                "angle_count": len(rows),
                "nodes": sum(row["nodes"] for row in rows),
                "accepted_leaves": sum(row["accepted_leaves"] for row in rows),
                "unresolved_leaves": sum(row["unresolved_leaves"] for row in rows),
                "stop_causes": [row.get("stop_cause") for row in rows],
                "verification_phase": report.get("timing", {})
                .get("phases", {})
                .get("verification"),
                "stdout_decoded_sha256": digest(stdout.encode()),
            }
        require(
            source.read_bytes() == raw
            and KERNEL.read_bytes() == current
            and CLI.read_bytes() == cli_source
            and Path(__file__).read_bytes() == tool_source
            and candidate.read_bytes() == raw,
            "input or source changed during paired run",
        )
        result["normalized_outcomes_equal"] = normalized(reports["baseline"]) == normalized(
            reports["current"]
        )
        result["status"] = (
            "MATCHED_FIXED_WORK"
            if result["normalized_outcomes_equal"]
            else "DIFFERENT_OUTCOMES"
        )
    atomic_write_text(
        args.out / "result.json", json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--candidate-sha256", required=True)
    parser.add_argument("--baseline-ref", required=True)
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--side", type=Fraction, required=True)
    parser.add_argument("--threshold", type=Fraction, required=True)
    parser.add_argument("--angles", required=True)
    parser.add_argument("--max-nodes", type=int, required=True)
    parser.add_argument("--max-depth", type=int, default=48)
    parser.add_argument("--retain-pending-boxes", action="store_true")
    parser.add_argument("--internal-seconds", type=float, default=12)
    parser.add_argument("--outer-seconds", type=float, default=15)
    parser.add_argument("--scratch-root", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    result = run(parser.parse_args())
    print(json.dumps({key: result.get(key) for key in ("status", "normalized_outcomes_equal")}))
    return 0 if result["status"] == "MATCHED_FIXED_WORK" else 2


if __name__ == "__main__":
    raise SystemExit(main())
