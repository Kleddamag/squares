"""Measure the Python, native, and resumable parallel n=17 BB search arms."""

from __future__ import annotations

import argparse
import json
import os
import platform
import resource
import signal
import subprocess
import sys
import tempfile
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

PROJECT = Path(__file__).resolve().parents[1]
REPO = PROJECT.parent
SCHEMA = "n17-bb-native-benchmark/v1"
PATTERNS = {
    "A": (
        "interior-SW",
        "interior-NW",
        "interior-W",
        "interior-S",
        "interior-N",
        "interior-SE",
    ),
    "F7": (
        "corner-SW",
        "corner-NW",
        "side-S0",
        "side-N0",
        "side-W0",
        "side-W2",
        "interior-W",
    ),
    "F6": (
        "side-E0",
        "side-S1",
        "side-N1",
        "interior-W",
        "interior-N",
        "interior-E",
    ),
}
ARMS = ("python", "native", "parallel")


def _git_revision() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()


def _machine() -> dict[str, str]:
    processor = platform.processor().strip()
    if not processor and platform.system() == "Darwin":
        completed = subprocess.run(
            ["sysctl", "-n", "machdep.cpu.brand_string"],
            capture_output=True,
            text=True,
            check=False,
        )
        processor = completed.stdout.strip()
    if not processor and platform.system() == "Linux":
        for line in Path("/proc/cpuinfo").read_text(encoding="utf-8").splitlines():
            if line.startswith(("model name", "Hardware")):
                processor = line.partition(":")[2].strip()
                break
    return {
        "system": platform.system(),
        "release": platform.release(),
        "architecture": platform.machine(),
        "processor": processor or "unknown",
        "python": platform.python_version(),
    }


def _run(command: list[str], timeout: float) -> tuple[dict[str, Any], str, str]:
    before = resource.getrusage(resource.RUSAGE_CHILDREN)
    started = time.perf_counter()
    process = subprocess.Popen(
        command,
        cwd=PROJECT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        start_new_session=True,
    )
    timed_out = False
    try:
        stdout, stderr = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        os.killpg(process.pid, signal.SIGKILL)
        stdout, stderr = process.communicate()
    after = resource.getrusage(resource.RUSAGE_CHILDREN)
    return (
        {
            "returncode": process.returncode,
            "timed_out": timed_out,
            "wrapper_wall_seconds": time.perf_counter() - started,
            "wrapper_cpu_seconds": (
                after.ru_utime + after.ru_stime - before.ru_utime - before.ru_stime
            ),
        },
        stdout,
        stderr,
    )


def _custom_pattern(specification: str, index: int) -> tuple[str, tuple[str, ...]]:
    cells = tuple(part for part in specification.split(",") if part)
    if not cells:
        raise ValueError("--cells requires a comma-separated cell list")
    return f"custom-{index}", cells


def _command(
    *,
    arm: str,
    native_dir: Path | None,
    cells: tuple[str, ...],
    label: str,
    max_seconds: float,
    workers: int,
    output: Path,
    state: Path,
) -> list[str]:
    common = [
        "--cells",
        ",".join(cells),
        "--label",
        label,
        "--max-seconds",
        str(max_seconds),
        "--output",
        str(output),
    ]
    if label in {"F7", "F6"}:
        common.append("--control")
    if arm == "python":
        return [sys.executable, "-m", "devtools.pilot_n17_subpattern_bb", *common]
    if native_dir is None:
        raise ValueError(f"--native-dir is required for the {arm} arm")
    if arm == "native":
        return [
            sys.executable,
            "-m",
            "devtools.n17_bb_native",
            "--native-dir",
            str(native_dir),
            *common,
        ]
    return [
        sys.executable,
        "-m",
        "devtools.run_n17_bb_parallel",
        "--native-dir",
        str(native_dir),
        "--workers",
        str(workers),
        "--state",
        str(state),
        *common,
    ]


def _read_result(path: Path, process: dict[str, Any], stderr: str) -> dict[str, Any]:
    if process["timed_out"] or not path.is_file():
        if stderr:
            print(stderr[-2_000:], file=sys.stderr)
        return {
            "verdict": "instrument-error",
            "nodes": None,
            "closed_tree_share": None,
            "cpu_seconds": process["wrapper_cpu_seconds"],
            "wall_seconds": process["wrapper_wall_seconds"],
        }
    result = json.loads(path.read_text(encoding="utf-8"))
    return {
        "verdict": result.get("verdict"),
        "nodes": result.get("nodes"),
        "closed_tree_share": result.get("closed_tree_share"),
        "cpu_seconds": result.get("cpu_seconds"),
        "search_cpu_seconds": result.get("search_cpu_seconds", result.get("cpu_seconds")),
        "wall_seconds": result.get("wall_seconds"),
        "resumed": result.get("resumed", False),
        "child_failed": process["returncode"] != 0,
        "cpu_seconds_complete": result.get("cpu_seconds_complete", True),
        "git_revisions": result.get("git_revisions"),
        "mixed_revision_resume": result.get("mixed_revision_resume", False),
    }


def _append(path: Path, record: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(record, sort_keys=True) + "\n")
        stream.flush()
        os.fsync(stream.fileno())


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--native-dir", type=Path)
    parser.add_argument(
        "--arms",
        default=",".join(ARMS),
        help="comma-separated subset of python,native,parallel",
    )
    parser.add_argument(
        "--patterns",
        default="A",
        help="comma-separated subset of A,F7,F6 (default: A)",
    )
    parser.add_argument(
        "--cells",
        action="append",
        default=[],
        help="also measure one custom comma-separated cell list; may be repeated",
    )
    parser.add_argument("--max-seconds", type=float, required=True)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--state-dir", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    arms = tuple(part for part in args.arms.split(",") if part)
    unknown = sorted(set(arms) - set(ARMS))
    if unknown or not arms:
        raise SystemExit(f"unknown or empty --arms selection: {unknown}")
    if args.max_seconds <= 0 or args.workers <= 0:
        raise SystemExit("--max-seconds and --workers must be positive")
    if args.native_dir is None and any(arm != "python" for arm in arms):
        raise SystemExit("--native-dir is required for native and parallel arms")
    pattern_names = tuple(part for part in args.patterns.split(",") if part)
    unknown_patterns = sorted(set(pattern_names) - set(PATTERNS))
    if unknown_patterns or not pattern_names:
        raise SystemExit(f"unknown or empty --patterns selection: {unknown_patterns}")
    patterns = [(name, PATTERNS[name]) for name in pattern_names]
    patterns.extend(
        _custom_pattern(specification, index)
        for index, specification in enumerate(args.cells, start=1)
    )
    revision = _git_revision()
    machine = _machine()
    state_dir = args.state_dir or args.out.with_name(f"{args.out.stem}-state")
    failed = False
    with tempfile.TemporaryDirectory(prefix="n17-bb-benchmark-") as scratch_name:
        scratch = Path(scratch_name)
        for label, cells in patterns:
            safe_label = "-".join(part.replace("/", "_") for part in label.split(","))
            for arm in arms:
                output = scratch / f"{safe_label}-{arm}.json"
                state = state_dir / f"{safe_label}-w{args.workers}.json"
                command = _command(
                    arm=arm,
                    native_dir=args.native_dir,
                    cells=cells,
                    label=label,
                    max_seconds=args.max_seconds,
                    workers=args.workers,
                    output=output,
                    state=state,
                )
                process, _stdout, stderr = _run(
                    command, timeout=args.max_seconds + max(60.0, args.max_seconds * 0.5)
                )
                result = _read_result(output, process, stderr)
                workers = args.workers if arm == "parallel" else 1
                record = {
                    "schema": SCHEMA,
                    "recorded_at": datetime.now(UTC).isoformat(),
                    "arm": arm,
                    "pattern": label,
                    "control": label in {"F7", "F6"},
                    "cells": list(cells),
                    "verdict": result["verdict"],
                    "nodes": result["nodes"],
                    "closed_share": result["closed_tree_share"],
                    "cpu_seconds": result["cpu_seconds"],
                    "search_cpu_seconds": result.get("search_cpu_seconds"),
                    "wall_seconds": result["wall_seconds"],
                    "workers": workers,
                    "machine": machine,
                    "git_revision": revision,
                    "max_seconds": args.max_seconds,
                    "resumed": result.get("resumed", False),
                    "returncode": process["returncode"],
                    "timed_out": process["timed_out"],
                    "child_failed": result.get("child_failed", False),
                    "cpu_seconds_complete": result.get("cpu_seconds_complete", True),
                    "search_git_revisions": result.get("git_revisions"),
                    "mixed_revision_resume": result.get("mixed_revision_resume", False),
                }
                _append(args.out, record)
                print(json.dumps(record, sort_keys=True), flush=True)
                failed = (
                    failed
                    or record["verdict"] == "instrument-error"
                    or bool(record["child_failed"])
                )
                if label in {"F7", "F6"} and record["verdict"] == "certified-infeasible":
                    failed = True
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
