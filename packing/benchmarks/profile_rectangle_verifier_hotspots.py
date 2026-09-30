"""Retain a bounded cProfile of one exact rectangle-verifier angle.

Profiled CPU and node rates include instrumentation overhead and are never a
substitute for the unprofiled paired benchmark.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import pstats
import resource
import signal
import subprocess
import sys
import tempfile
import time
from fractions import Fraction
from pathlib import Path
from typing import Any, cast

from strif import atomic_write_bytes, atomic_write_text

REPO = Path(__file__).resolve().parents[2]
KERNEL = REPO / "packing/src/sqpack/rectangle_density.py"
CLI = REPO / "packing/devtools/verify_rectangle_density.py"
KERNEL_SHA = "1d41fa6aaa9cd9d5dfb95b54fe0cc3598af52c3d3c3f400fd78d83ccf98ca7aa"
CLI_SHA = "db18d19c434ad17370521c4a3d88ba74ebf4e61515ff3861ea636f0265e3a538"
THRESHOLD = Fraction(2252024993666617, 2251799813685248)
VOLUME = Path("/Volumes/spud-ext1")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def top_functions(profile: Path, *, limit: int = 25) -> dict[str, list[dict[str, object]]]:
    stats = cast(
        dict[tuple[str, int, str], tuple[int, int, float, float, object]],
        vars(pstats.Stats(str(profile)))["stats"],
    )
    rows = [
        {
            "source": source,
            "line": line,
            "function": function,
            "primitive_calls": primitive,
            "total_calls": calls,
            "self_seconds": self_seconds,
            "cumulative_seconds": cumulative,
        }
        for (source, line, function), (
            primitive,
            calls,
            self_seconds,
            cumulative,
            _callers,
        ) in stats.items()
    ]
    return {
        "cumulative": sorted(rows, key=lambda row: -float(row["cumulative_seconds"]))[:limit],
        "self": sorted(rows, key=lambda row: -float(row["self_seconds"]))[:limit],
    }


def parse_report(stdout: str) -> dict[str, Any]:
    value = json.loads(stdout)
    if not isinstance(value, dict):
        raise TypeError("profiled verifier did not emit a JSON object")
    return value


def run(args: argparse.Namespace) -> dict[str, Any]:
    require(VOLUME.is_mount(), "external scratch volume is not mounted")
    scratch = args.scratch_root.resolve()
    require(scratch.is_relative_to(VOLUME / "agent-scratch"), "scratch must be external")
    scratch.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=scratch) as probe:
        probe.write(b"writable")
        probe.flush()
    require(0 < args.internal_seconds <= args.outer_seconds - 2, "need shutdown allowance")
    require(0 < args.outer_seconds <= 15, "profile process ceiling must be <=15 seconds")
    require(0 <= args.angle <= 200, "angle must be in 0..200")
    require(not args.out.exists(), "profile receipt directory already exists")
    args.out.mkdir(parents=True)
    started = time.perf_counter()
    result: dict[str, Any] = {
        "status": "REFUSED",
        "profiled_not_baseline": True,
        "speed_parity_established": False,
        "kernel_sha256": KERNEL_SHA,
        "cli_sha256": CLI_SHA,
        "profiler_sha256": digest(Path(__file__)),
        "threshold": str(THRESHOLD),
        "angle": args.angle,
        "internal_seconds": args.internal_seconds,
        "outer_seconds": args.outer_seconds,
    }
    try:
        require(digest(KERNEL) == KERNEL_SHA and digest(CLI) == CLI_SHA, "checker source drift")
        source = args.candidate.resolve()
        require(source.is_relative_to(REPO), "candidate must be retained in repository")
        raw = source.read_bytes()
        candidate_sha = hashlib.sha256(raw).hexdigest()
        require(candidate_sha == args.candidate_sha256, "candidate identity differs")
        relative = str(source.relative_to(REPO))
        blob = subprocess.check_output(
            ["git", "-C", str(REPO), "hash-object", str(source)], text=True
        ).strip()
        committed = subprocess.check_output(
            ["git", "-C", str(REPO), "rev-parse", f"HEAD:{relative}"], text=True
        ).strip()
        require(blob == committed, "candidate bytes differ from committed HEAD blob")
        result.update(
            candidate_path=relative,
            candidate_sha256=candidate_sha,
            candidate_bytes=len(raw),
            candidate_git_blob=blob,
        )
        with tempfile.TemporaryDirectory(dir=scratch) as temporary:
            work = Path(temporary)
            snapshot = work / "candidate.json"
            profile = work / "profile.prof"
            snapshot.write_bytes(raw)
            command = [
                sys.executable,
                "-m",
                "cProfile",
                "-o",
                str(profile),
                "-m",
                "devtools.verify_rectangle_density",
                str(snapshot),
                "--n",
                str(args.n),
                "--side",
                str(args.side),
                "--threshold",
                str(THRESHOLD),
                "--angles",
                str(args.angle),
                "--max-nodes-per-angle",
                "10000000",
                "--max-depth",
                "48",
                "--max-seconds",
                str(args.internal_seconds),
                "--bound-mode",
                "common-core",
            ]
            result["command"] = command
            before = resource.getrusage(resource.RUSAGE_CHILDREN)
            launched = time.perf_counter()
            process = subprocess.Popen(
                command,
                cwd=REPO / "packing",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                start_new_session=True,
            )
            expired = False
            try:
                stdout, stderr = process.communicate(timeout=args.outer_seconds)
            except subprocess.TimeoutExpired:
                expired = True
                os.killpg(process.pid, signal.SIGKILL)
                stdout, stderr = process.communicate()
            after = resource.getrusage(resource.RUSAGE_CHILDREN)
            result.update(
                exit_code=process.returncode,
                timed_out=expired,
                profiled_wall_seconds=time.perf_counter() - launched,
                profiled_process_cpu_seconds=(
                    after.ru_utime + after.ru_stime - before.ru_utime - before.ru_stime
                ),
                profiled_process_user_seconds=after.ru_utime - before.ru_utime,
                profiled_process_system_seconds=after.ru_stime - before.ru_stime,
            )
            atomic_write_bytes(
                args.out / "profiled.stdout.json.gz", gzip.compress(stdout.encode(), mtime=0)
            )
            atomic_write_text(args.out / "profiled.stderr", stderr)
            result["stdout_decoded_sha256"] = hashlib.sha256(stdout.encode()).hexdigest()
            parsed = parse_report(stdout)
            result["verifier_status"] = parsed.get("status")
            angles = parsed.get("angles")
            require(
                isinstance(angles, list)
                and len(angles) == 1
                and isinstance(angles[0], dict)
                and angles[0].get("index") == args.angle,
                "profiled angle inventory differs",
            )
            assert isinstance(angles, list)
            assert isinstance(angles[0], dict)
            result["verifier_angle_summary"] = {
                key: angles[0].get(key)
                for key in (
                    "index",
                    "status",
                    "nodes",
                    "accepted_leaves",
                    "unresolved_leaves",
                    "stop_cause",
                )
            }
            result["verifier_candidate_sha256"] = parsed.get("candidate_sha256")
            require(parsed.get("candidate_sha256") == candidate_sha, "profiled input drift")
            require(profile.is_file(), "cProfile did not write statistics")
            profile_data = profile.read_bytes()
            atomic_write_bytes(
                args.out / "profile.prof.gz", gzip.compress(profile_data, mtime=0)
            )
            result["profile_decoded_sha256"] = hashlib.sha256(profile_data).hexdigest()
            result["profile_gzip_sha256"] = digest(args.out / "profile.prof.gz")
            result["top_functions"] = top_functions(profile)
            require(
                digest(source) == candidate_sha
                and digest(snapshot) == candidate_sha
                and digest(KERNEL) == KERNEL_SHA
                and digest(CLI) == CLI_SHA
                and digest(Path(__file__)) == result["profiler_sha256"],
                "source changed during profile",
            )
            result["status"] = "PROFILE_RETAINED" if not expired else "PROFILE_TIMEOUT"
    except (
        OSError,
        ValueError,
        TypeError,
        subprocess.CalledProcessError,
        json.JSONDecodeError,
    ) as error:
        result["error"] = str(error)
    result["outer_wall_seconds"] = time.perf_counter() - started
    atomic_write_text(
        args.out / "result.json", json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--candidate-sha256", required=True)
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--side", type=Fraction, required=True)
    parser.add_argument("--angle", type=int, required=True)
    parser.add_argument("--internal-seconds", type=float, default=10.0)
    parser.add_argument("--outer-seconds", type=float, default=15.0)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--scratch-root", type=Path, required=True)
    result = run(parser.parse_args())
    print(
        json.dumps(
            {
                key: result.get(key)
                for key in ("status", "verifier_status", "outer_wall_seconds")
            }
        )
    )
    return 0 if result["status"] == "PROFILE_RETAINED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
