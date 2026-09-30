"""Run the pinned C++ and native rectangle checkers on one admitted candidate.

The program retains complete outcomes and phase costs. Only two complete 201-angle
VERIFIED results support a throughput comparison; bounded probes are diagnostics.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import importlib.util
import json
import math
import os
import platform
import resource
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from fractions import Fraction
from pathlib import Path
from types import ModuleType
from typing import Any

from strif import atomic_write_bytes, atomic_write_text

from sqpack import rectangle_density
from sqpack.rectangle_density import ANGLE_COUNT, CandidateError, load_candidate_bytes

REPO = Path(__file__).resolve().parents[2]
UPSTREAM = REPO / "attic/wand125-tools"
VERIFY_CPP = UPSTREAM / "solver/verify.cpp"
CERTIFY_PY = UPSTREAM / "solver/certify.py"
NATIVE_CLI = REPO / "packing/devtools/verify_rectangle_density.py"
UPSTREAM_COMMIT = "3eb08e6c675d8d5aa953cb93da049a3f3cdc6123"
CPP_SHA = "a75140df1b484ad104a214d2e8de87afda9fca5929341ec40121afde0c1af602"
ADAPTER_SHA = "f86cb9c1444f98ae0b13190d0ee9a343064e68e1fb2a2ecd6e203eca8e5b8cf3"
NOMINAL_THRESHOLD = Fraction(10001, 10000)
EFFECTIVE_THRESHOLD = Fraction(math.nextafter(10001 / 10000, math.inf))
COMPILE_FLAGS = ("-O2", "-std=c++17", "-fno-fast-math", "-ffp-contract=off")
VOLUME = Path("/Volumes/spud-ext1")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def timed(action: Any) -> tuple[Any, dict[str, float]]:
    wall, cpu = time.perf_counter(), time.process_time()
    value = action()
    return value, {
        "wall_seconds": time.perf_counter() - wall,
        "process_cpu_seconds": time.process_time() - cpu,
    }


def run_command(
    command: list[str], *, cwd: Path, timeout: float
) -> tuple[dict[str, object], str, str]:
    before = resource.getrusage(resource.RUSAGE_CHILDREN)
    start = time.perf_counter()
    process = subprocess.Popen(
        command,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        start_new_session=True,
    )
    expired = False
    try:
        stdout, stderr = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        expired = True
        os.killpg(process.pid, signal.SIGKILL)
        stdout, stderr = process.communicate()
    after = resource.getrusage(resource.RUSAGE_CHILDREN)
    return (
        {
            "command": command,
            "exit_code": process.returncode,
            "timed_out": expired,
            "wall_seconds": time.perf_counter() - start,
            "process_user_seconds": after.ru_utime - before.ru_utime,
            "process_system_seconds": after.ru_stime - before.ru_stime,
            "process_cpu_seconds": (
                after.ru_utime + after.ru_stime - before.ru_utime - before.ru_stime
            ),
        },
        stdout,
        stderr,
    )


def checked_rows(stdout: str, first: int, last: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in stdout.splitlines():
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(row, dict) or "r" not in row:
            continue
        rows.append(row)
    indices = [row["r"] for row in rows]
    if len(indices) != len(set(indices)) or any(
        not isinstance(index, int) or not first <= index <= last for index in indices
    ):
        raise ValueError("C++ output has duplicate or out-of-range angle indices")
    return rows


def _encloses(pair: list[str], exact: Fraction) -> bool:
    if len(pair) != 2:
        return False
    low, high = (Fraction(float.fromhex(token)) for token in pair)
    return low <= exact <= high


def check_interval_adapter(raw: bytes, encoded: str) -> dict[str, int]:
    """Bind every C++ interval row and axis center to the exact source candidate."""

    source = json.loads(raw, parse_float=Fraction)
    side, core = Fraction(source["L"]), Fraction(source["B"])
    lines = encoded.splitlines()
    if (
        len(lines) < 4
        or not _encloses(lines[0].split(), side)
        or not _encloses(lines[1].split(), core)
    ):
        raise ValueError("adapter side/core interval differs from exact candidate")
    expected: list[tuple[Fraction, Fraction, Fraction, Fraction, Fraction]] = []
    for row, weight_text in zip(source["rectangles"], source["weights"], strict=True):
        weight = Fraction(weight_text)
        if not weight:
            continue
        x0, y0, x1, y1 = map(Fraction, row)
        rho = weight / (8 * (x1 - x0) * (y1 - y0))
        for swap in (False, True):
            a, b, c, d = (y0, x0, y1, x1) if swap else (x0, y0, x1, y1)
            for sx, sy in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
                left, right = (a, c) if sx == 1 else (side - c, side - a)
                bottom, top = (b, d) if sy == 1 else (side - d, side - b)
                expected.append((left, bottom, right, top, rho))
    count = int(lines[2])
    if count != len(expected) or len(lines) < 4 + count:
        raise ValueError("adapter expanded rectangle count differs")
    for line, values in zip(lines[3 : 3 + count], expected, strict=True):
        tokens = line.split()
        if len(tokens) != 10 or any(
            not _encloses(tokens[2 * index : 2 * index + 2], value)
            for index, value in enumerate(values)
        ):
            raise ValueError("adapter rectangle interval differs from exact source")
    centers = {side / 2, side - core / 2}
    for left, _bottom, right, _top, _rho in expected:
        for edge in (left, right):
            for sign in (-1, 1):
                center = edge + sign * core / 2
                if side / 2 <= center <= side - core / 2:
                    centers.add(center)
    center_index = 3 + count
    center_count = int(lines[center_index])
    if center_count != len(centers) or len(lines) != center_index + 1 + center_count:
        raise ValueError("adapter axis-center inventory differs")
    if any(
        not _encloses(line.split(), center)
        for line, center in zip(lines[center_index + 1 :], sorted(centers), strict=True)
    ):
        raise ValueError("adapter axis-center interval differs")
    return {"expanded_rectangles": count, "axis_centers": center_count}


def classify(
    *,
    first: int,
    last: int,
    cpp_exit: int | None,
    cpp_timeout: bool,
    cpp_rows: list[dict[str, Any]],
    native_exit: int | None,
    native_report: dict[str, Any] | None,
    native_timeout: bool,
) -> str:
    expected = set(range(first, last + 1))
    cpp_valid_rows = all(
        isinstance(row, dict)
        and type(row.get("r")) is int
        and row.get("r") in expected
        and row.get("status") == "verified"
        and (lower := _printed_cpp_lower(row.get("lower_bound"))) is not None
        and lower >= EFFECTIVE_THRESHOLD
        and type(row.get("nodes")) is int
        and type(row.get("leaves")) is int
        and row["nodes"] >= row["leaves"] > 0
        for row in cpp_rows
    )
    cpp_complete = (
        not cpp_timeout
        and cpp_exit == 0
        and len(cpp_rows) == len(expected)
        and cpp_valid_rows
        and {row["r"] for row in cpp_rows} == expected
    )
    native_angles = native_report.get("angles", []) if native_report else []
    native_valid_rows = isinstance(native_angles, list) and all(
        isinstance(row, dict)
        and type(row.get("index")) is int
        and row.get("index") in expected
        and row.get("status") == "VERIFIED"
        and (lower := _exact_native_lower(row.get("lower_bound"))) is not None
        and lower >= EFFECTIVE_THRESHOLD
        and type(row.get("unresolved_leaves")) is int
        and row["unresolved_leaves"] == 0
        and type(row.get("nodes")) is int
        and row["nodes"] > 0
        for row in native_angles
    )
    native_complete = (
        not native_timeout
        and native_exit == (0 if len(expected) == ANGLE_COUNT else 2)
        and native_report is not None
        and native_report.get("status")
        == ("VERIFIED" if len(expected) == ANGLE_COUNT else "PARTIAL")
        and native_valid_rows
        and {row["index"] for row in native_angles} == expected
        and len(native_angles) == len(expected)
    )
    if cpp_complete and native_complete:
        return (
            "MATCHED_COMPLETE_VERIFIED"
            if len(expected) == ANGLE_COUNT
            else "MATCHED_SUBSET_ONLY"
        )
    return "INCOMPLETE_NO_PARITY_CLAIM"


def ensure_external_scratch(path: Path) -> None:
    if not VOLUME.is_mount():
        raise ValueError("external scratch volume is not mounted")
    resolved = path.resolve()
    if not resolved.is_relative_to(VOLUME / "agent-scratch"):
        raise ValueError("scratch root must be on the external agent-scratch volume")
    resolved.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=resolved) as probe:
        probe.write(b"writable")
        probe.flush()


def load_adapter() -> ModuleType:
    spec = importlib.util.spec_from_file_location("pinned_wand125_certify", CERTIFY_PY)
    if spec is None or spec.loader is None:
        raise ValueError("cannot load pinned C++ adapter")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse_native(stdout: str) -> dict[str, Any] | None:
    try:
        value = json.loads(stdout)
    except json.JSONDecodeError:
        return None
    return value if isinstance(value, dict) else None


def _printed_cpp_lower(value: object) -> Fraction | None:
    try:
        binary = float(str(value))
    except ValueError, TypeError, OverflowError:
        return None
    return Fraction(binary) if math.isfinite(binary) else None


def _exact_native_lower(value: object) -> Fraction | None:
    try:
        return Fraction(str(value))
    except ValueError, ZeroDivisionError, TypeError, OverflowError:
        return None


def run(args: argparse.Namespace) -> dict[str, object]:
    ensure_external_scratch(args.scratch_root)
    if args.out.exists():
        raise ValueError("output directory already exists; use a new receipt path")
    args.out.mkdir(parents=True)
    phases: dict[str, Any] = {}
    started = time.perf_counter()
    parent_cpu = time.process_time()
    result: dict[str, Any] = {
        "status": "REFUSED",
        "matched_complete_scope": False,
        "performance_comparable": False,
        "speed_parity_established": False,
        "scope": (
            "Both checkers must complete the same 201 angles before a "
            "proof-throughput comparison."
        ),
        "nominal_threshold": str(NOMINAL_THRESHOLD),
        "effective_binary64_threshold": str(EFFECTIVE_THRESHOLD),
        "upstream_commit": UPSTREAM_COMMIT,
        "cpp_source_sha256": CPP_SHA,
        "adapter_source_sha256": ADAPTER_SHA,
        "native_checker_source_sha256": digest(Path(rectangle_density.__file__)),
        "native_cli_source_sha256": digest(NATIVE_CLI),
        "benchmark_source_sha256": digest(Path(__file__)),
        "first_angle": args.first_angle,
        "last_angle": args.last_angle,
        "cpp_timeout_seconds": args.cpp_timeout,
        "native_timeout_seconds": args.native_timeout,
        "native_internal_max_seconds": max(0.1, args.native_timeout - 2.0),
        "native_max_nodes_per_angle": args.max_nodes_per_angle,
        "native_max_depth": args.max_depth,
        "cpp_internal_node_limit": "nodes > 10000000 after a failed box",
        "cpp_internal_box_floor": "min halfwidth < 2^-45",
        "native_bound_mode": args.bound_mode,
        "compiler_flags": list(COMPILE_FLAGS),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "logical_cpu_count": os.cpu_count(),
        "peak_rss_bytes": "unmeasured",
        "phases": phases,
    }
    try:
        actual_commit = subprocess.check_output(
            ["git", "-C", str(UPSTREAM), "rev-parse", "HEAD"], text=True
        ).strip()
        require(
            actual_commit == UPSTREAM_COMMIT
            and digest(VERIFY_CPP) == CPP_SHA
            and digest(CERTIFY_PY) == ADAPTER_SHA,
            "pinned upstream source differs",
        )
        require(
            0 <= args.first_angle <= args.last_angle < ANGLE_COUNT,
            "requested angle range must lie in 0..200",
        )
        require(
            0 < args.compile_timeout <= 60,
            "compile requires a positive <=60-second supervisor ceiling",
        )
        require(
            0 < args.cpp_timeout <= 60 and 0 < args.native_timeout <= 60,
            "each verifier requires a positive <=60-second supervisor ceiling",
        )
        require(
            args.candidate.suffix != ".gz", "paired adapter requires a plain JSON candidate"
        )
        raw, phases["candidate_read"] = timed(args.candidate.read_bytes)
        result["candidate_sha256"] = hashlib.sha256(raw).hexdigest()
        result["candidate_bytes"] = len(raw)
        candidate_path = args.candidate.resolve()
        require(
            candidate_path.is_relative_to(REPO), "candidate must be a retained repository file"
        )
        result["candidate_repository_path"] = str(candidate_path.relative_to(REPO))
        result["candidate_git_blob"] = subprocess.check_output(
            ["git", "-C", str(REPO), "hash-object", str(candidate_path)], text=True
        ).strip()
        subprocess.run(
            [
                "git",
                "-C",
                str(REPO),
                "ls-files",
                "--error-unmatch",
                result["candidate_repository_path"],
            ],
            check=True,
            capture_output=True,
        )
        candidate, phases["native_admission"] = timed(
            lambda: load_candidate_bytes(
                raw,
                n=args.n,
                expected_side=args.side,
                target=EFFECTIVE_THRESHOLD,
            )
        )
        result["mass_exact"] = str(candidate.mass)
        result["mass_below_n"] = str(candidate.n - candidate.mass)
        result["native_expanded_rectangle_count"] = len(candidate.rectangles)
        with tempfile.TemporaryDirectory(dir=args.scratch_root) as temporary:
            work = Path(temporary)
            snapshot = work / "candidate.json"
            snapshot.write_bytes(raw)
            require(
                digest(snapshot) == result["candidate_sha256"], "candidate snapshot differs"
            )
            adapter = load_adapter()
            metadata, phases["cpp_adapter"] = timed(lambda: adapter.prepare(snapshot, work))
            result["cpp_adapter_metadata"] = metadata
            result["cpp_interval_input_sha256"] = digest(work / "certificate_input.txt")
            require(
                metadata["input_sha256"] == result["cpp_interval_input_sha256"],
                "adapter interval input hash differs from metadata",
            )
            adapter_check, phases["adapter_exact_binding"] = timed(
                lambda: check_interval_adapter(
                    raw, (work / "certificate_input.txt").read_text()
                )
            )
            result["adapter_exact_binding"] = adapter_check
            require(
                metadata["source_sha256"] == result["candidate_sha256"]
                and digest(snapshot) == result["candidate_sha256"],
                "adapter consumed a changed candidate snapshot",
            )
            result["cpp_expanded_rectangle_count"] = adapter_check["expanded_rectangles"]
            compiler = shutil.which("g++")
            require(compiler is not None, "g++ unavailable")
            assert compiler is not None
            result["compiler"] = compiler
            result["compiler_version"] = subprocess.check_output(
                [compiler, "--version"], text=True
            ).splitlines()[0]
            compile_cmd = [
                compiler,
                *COMPILE_FLAGS,
                str(VERIFY_CPP),
                "-o",
                str(work / "verify"),
            ]
            compiled, compile_out, compile_err = run_command(
                compile_cmd, cwd=work, timeout=args.compile_timeout
            )
            phases["compile"] = compiled
            atomic_write_text(args.out / "compile.stdout", compile_out)
            atomic_write_text(args.out / "compile.stderr", compile_err)
            require(
                compiled["exit_code"] == 0 and not compiled["timed_out"],
                "pinned C++ verifier did not compile within ceiling",
            )
            cpp, cpp_out, cpp_err = run_command(
                [str(work / "verify"), str(args.first_angle), str(args.last_angle)],
                cwd=work,
                timeout=args.cpp_timeout,
            )
            phases["cpp_verification"] = cpp
            atomic_write_text(args.out / "cpp.stdout.jsonl", cpp_out)
            atomic_write_text(args.out / "cpp.stderr", cpp_err)
            cpp_rows = checked_rows(cpp_out, args.first_angle, args.last_angle)
            result["cpp_angles_completed"] = len(cpp_rows)
            result["cpp_journal_sha256"] = digest(args.out / "cpp.stdout.jsonl")
            result["cpp_nodes_completed"] = sum(int(row["nodes"]) for row in cpp_rows)
            result["cpp_angle_seconds_sum"] = sum(float(row["seconds"]) for row in cpp_rows)
            native_cmd = [
                sys.executable,
                "-m",
                "devtools.verify_rectangle_density",
                str(snapshot),
                "--n",
                str(args.n),
                "--side",
                str(args.side),
                "--threshold",
                str(EFFECTIVE_THRESHOLD),
                "--angles",
                f"{args.first_angle}-{args.last_angle}",
                "--max-nodes-per-angle",
                str(args.max_nodes_per_angle),
                "--max-depth",
                str(args.max_depth),
                "--max-seconds",
                str(result["native_internal_max_seconds"]),
                "--bound-mode",
                args.bound_mode,
                "--timing",
            ]
            native, native_out, native_err = run_command(
                native_cmd,
                cwd=REPO / "packing",
                timeout=args.native_timeout,
            )
            phases["native_verification"] = native
            compressed_native = args.out / "native.stdout.json.gz"
            atomic_write_bytes(compressed_native, gzip.compress(native_out.encode(), mtime=0))
            atomic_write_text(args.out / "native.stderr", native_err)
            native_report = parse_native(native_out)
            result["native_stdout_decoded_sha256"] = hashlib.sha256(
                native_out.encode()
            ).hexdigest()
            result["native_stdout_gzip_sha256"] = digest(compressed_native)
            result["native_status"] = native_report.get("status") if native_report else None
            result["native_angles_completed"] = (
                len(native_report.get("angles", [])) if native_report else 0
            )
            result["native_nodes_completed"] = (
                sum(int(row["nodes"]) for row in native_report.get("angles", []))
                if native_report
                else 0
            )
            result["native_timing_phases"] = (
                native_report.get("timing") if native_report else None
            )
            require(
                digest(snapshot) == result["candidate_sha256"],
                "candidate snapshot changed during verifier runs",
            )
            require(
                digest(candidate_path) == result["candidate_sha256"]
                and digest(work / "certificate_input.txt")
                == result["cpp_interval_input_sha256"]
                and digest(VERIFY_CPP) == CPP_SHA
                and digest(CERTIFY_PY) == ADAPTER_SHA
                and digest(NATIVE_CLI) == result["native_cli_source_sha256"]
                and digest(Path(rectangle_density.__file__))
                == result["native_checker_source_sha256"]
                and digest(Path(__file__)) == result["benchmark_source_sha256"],
                "candidate, adapter, or verifier source changed during paired run",
            )
            require(
                not native_report
                or (
                    native_report.get("candidate_sha256") == result["candidate_sha256"]
                    and native_report.get("checker_source_sha256")
                    == result["native_checker_source_sha256"]
                    and native_report.get("n") == args.n
                    and native_report.get("L") == str(candidate.side)
                    and native_report.get("B") == str(candidate.core_side)
                    and native_report.get("threshold") == str(EFFECTIVE_THRESHOLD)
                    and native_report.get("max_seconds")
                    == result["native_internal_max_seconds"]
                    and native_report.get("requested_angle_count")
                    == args.last_angle - args.first_angle + 1
                ),
                "native result differs from matched input or checker",
            )
            verdict = classify(
                first=args.first_angle,
                last=args.last_angle,
                cpp_exit=cpp["exit_code"] if isinstance(cpp["exit_code"], int) else None,
                cpp_timeout=bool(cpp["timed_out"]),
                cpp_rows=cpp_rows,
                native_exit=native["exit_code"]
                if isinstance(native["exit_code"], int)
                else None,
                native_report=native_report,
                native_timeout=bool(native["timed_out"]),
            )
            result["status"] = verdict
            result["matched_complete_scope"] = verdict == "MATCHED_COMPLETE_VERIFIED"
            result["performance_comparable"] = verdict == "MATCHED_COMPLETE_VERIFIED"
    except (CandidateError, OSError, ValueError, subprocess.CalledProcessError) as error:
        result["error"] = str(error)
    result["total_wall_seconds"] = time.perf_counter() - started
    result["benchmark_process_cpu_seconds"] = time.process_time() - parent_cpu
    result["subprocess_cpu_seconds"] = sum(
        float(phases[key].get("process_cpu_seconds", 0.0))
        for key in ("compile", "cpp_verification", "native_verification")
        if isinstance(phases.get(key), dict)
    )
    atomic_write_text(
        args.out / "result.json", json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--side", type=Fraction, required=True)
    parser.add_argument("--first-angle", type=int, default=0)
    parser.add_argument("--last-angle", type=int, default=200)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--scratch-root", type=Path, required=True)
    parser.add_argument("--compile-timeout", type=float, default=30.0)
    parser.add_argument("--cpp-timeout", type=float, default=60.0)
    parser.add_argument("--native-timeout", type=float, default=60.0)
    parser.add_argument("--max-nodes-per-angle", type=int, default=10_000_000)
    parser.add_argument("--max-depth", type=int, default=48)
    parser.add_argument(
        "--bound-mode", choices=("common-core", "corner-min"), default="common-core"
    )
    args = parser.parse_args(argv)
    result = run(args)
    print(
        json.dumps(
            {
                key: result[key]
                for key in ("status", "matched_complete_scope", "total_wall_seconds")
            }
        )
    )
    return 0 if result["matched_complete_scope"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
