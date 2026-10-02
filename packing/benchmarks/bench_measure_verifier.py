"""Time the clean-room measure verifier against builds of itself and verify.cpp.

The instrument of the measure-verifier performance campaign
(`benchmarks/measure-verifier/README.md`). It runs fixed benchmark cells (one
certificate, one net direction) under several arms and records, per run, the
child's CPU time from `wait4` (user plus system), its wall time, the load
average before and after, the verdict and the node count. Arms are interleaved
cell by cell and their order rotates every repeat, so a load swing on a shared
host lands on every arm alike.

An arm is either a `sqverify-fast` binary (`fast:LABEL=PATH`) or the authors'
checker `verify.cpp`, run as a black box through this repository's replay
command `devtools.audit_wand125_rectangles --control`. For that arm the CPU time
is the one the replay tool measured for the unchanged checker's own process on
the original certificate, which excludes the tool, the compiler and the two
mutation runs the control also performs. Nothing here reads or links the
checker's source.

From `packing/`, for example:

    .venv/bin/python3 -m benchmarks.bench_measure_verifier \\
        --arm fast:base=sqverify_fast/target/release/sqverify-fast \\
        --arm verify-cpp --repeats 3 --out /tmp/measure-bench.jsonl

`--callgrind` replaces CPU time by instruction counts for the fast arms
(valgrind's `Ir`), which do not depend on the host's load. `--whole NAMES` replays
whole certificates instead (all 201 directions, one worker): `verify.cpp` through
`devtools.audit_wand125_rectangles --replay --workers 1`, the fast arms through
`--directions all --threads 1`. This is the headline comparison; from `packing/`,
on an otherwise idle host:

    .venv/bin/python3 -m benchmarks.bench_measure_verifier \\
        --arm fast:candidate=sqverify_fast/target/release/sqverify-fast \\
        --arm verify-cpp --whole rect_n32_L595,rect_n31_L592 --out whole.jsonl
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from statistics import median
from typing import Any

PROJECT = Path(__file__).resolve().parents[1]
WEB = PROJECT / "resources/web"
THRESHOLD = "10001/10000"


@dataclass(frozen=True)
class Cell:
    """One benchmark cell: a standing certificate at one net direction."""

    packet: str
    certificate: str
    n: int
    direction: int

    @property
    def candidate(self) -> Path:
        return (
            WEB
            / f"wand125-rectangle-certificates-{self.packet}"
            / "wand125-rectangles/certificates"
            / self.certificate
            / "certified_candidate.json.gz"
        )

    @property
    def key(self) -> str:
        return f"{self.certificate}@r{self.direction}"


# The fixed benchmark (declared in the campaign README before any experiment):
# three certificates of 1,080, 3,000 and 6,496 expanded rectangles, at five
# directions spread over the net, plus the largest certificate of the 28
# September packet at three directions.
DIRECTIONS = (1, 50, 100, 150, 200)
CELLS: tuple[Cell, ...] = (
    *(Cell("2026-09-27", "rect_n32_L595", 32, r) for r in DIRECTIONS),
    *(Cell("2026-09-27", "rect_n61_L796", 61, r) for r in DIRECTIONS),
    *(Cell("2026-09-27", "rect_n78_L8955", 78, r) for r in DIRECTIONS),
    *(Cell("2026-09-28", "rect_n95_L98418", 95, r) for r in (1, 100, 200)),
)


def loadavg() -> float:
    try:
        return float(Path("/proc/loadavg").read_text(encoding="utf-8").split()[0])
    except OSError:
        return os.getloadavg()[0]


def run_with_rusage(argv: list[str]) -> dict[str, Any]:
    """Run `argv` from `packing/` with `os.wait4`, so the CPU time is the child's alone."""
    before = loadavg()
    start = time.monotonic()
    executable = argv[0] if Path(argv[0]).is_absolute() else shutil.which(argv[0])
    if executable is None:
        raise SystemExit(f"cannot find {argv[0]}")
    with tempfile.TemporaryFile() as out, tempfile.TemporaryFile() as err:
        pid = os.posix_spawn(
            executable,
            argv,
            os.environ,
            file_actions=[
                (os.POSIX_SPAWN_DUP2, out.fileno(), 1),
                (os.POSIX_SPAWN_DUP2, err.fileno(), 2),
            ],
        )
        _, status, usage = os.wait4(pid, 0)
        wall = time.monotonic() - start
        out.seek(0)
        err.seek(0)
        stdout = out.read().decode()
        stderr = err.read().decode()
    return {
        "returncode": os.waitstatus_to_exitcode(status),
        "stdout": stdout,
        "stderr": stderr,
        "cpu_seconds": usage.ru_utime + usage.ru_stime,
        "user_seconds": usage.ru_utime,
        "sys_seconds": usage.ru_stime,
        "max_rss_kib": usage.ru_maxrss,
        "wall_seconds": wall,
        "load_before": before,
        "load_after": loadavg(),
    }


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def search_instructions(outfile: Path) -> int | None:
    """Inclusive instructions of the direction search, excluding admission.

    Read from `callgrind_annotate --inclusive=yes`: the line of the one function
    that runs a direction (`rotated::verify_direction`, or `axis::verify_axis` at
    r = 0).
    """
    if not outfile.is_file():
        return None
    annotated = subprocess.run(
        ["callgrind_annotate", "--inclusive=yes", str(outfile)],
        capture_output=True,
        text=True,
        check=False,
    ).stdout
    for line in annotated.splitlines():
        if "rotated::verify_direction" in line or "axis::verify_axis" in line:
            match = re.match(r"\s*([\d,]+)", line)
            if match:
                return int(match.group(1).replace(",", ""))
    return None


def fast_run(binary: Path, cell: Cell, *, callgrind: bool) -> dict[str, Any]:
    argv = [
        str(binary.resolve()),
        "--candidate",
        str(cell.candidate),
        "--n",
        str(cell.n),
        "--directions",
        str(cell.direction),
        "--threshold",
        THRESHOLD,
    ]
    if callgrind:
        with tempfile.TemporaryDirectory() as scratch:
            outfile = Path(scratch) / "cg.out"
            argv = [
                "/usr/bin/valgrind",
                "--tool=callgrind",
                f"--callgrind-out-file={outfile}",
                *argv,
            ]
            result = run_with_rusage(argv)
            match = re.search(r"Collected\s*:\s*(\d+)", result["stderr"]) or re.search(
                r"refs:\s*([\d,]+)", result["stderr"]
            )
            result["instructions"] = int(match.group(1).replace(",", "")) if match else None
            result["search_instructions"] = search_instructions(outfile)
    else:
        result = run_with_rusage(argv)
    lines = [json.loads(line) for line in result.pop("stdout").splitlines() if line.strip()]
    row = next((line for line in lines if line.get("r") == cell.direction), {})
    summary = lines[-1] if lines else {}
    result["verdict"] = row.get("verdict")
    result["nodes"] = row.get("nodes", row.get("vertices"))
    result["leaves"] = row.get("leaves")
    result["min_certified_lower_bound"] = row.get("min_certified_lower_bound")
    result["direction_seconds"] = row.get("seconds")
    result["summary_status"] = summary.get("status")
    if result["returncode"] != 0:
        result["stderr_tail"] = result["stderr"][-2000:]
    result.pop("stderr")
    return result


def reference_run(cell: Cell) -> dict[str, Any]:
    """Run verify.cpp on one direction through the replay tool's control mode."""
    with tempfile.TemporaryDirectory() as scratch:
        argv = [
            sys.executable,
            "-m",
            "devtools.audit_wand125_rectangles",
            "--packet",
            cell.packet,
            "--control",
            "--n",
            str(cell.n),
            "--direction",
            str(cell.direction),
            "--out",
            scratch,
        ]
        wrapper = run_with_rusage(argv)
        receipts = list(Path(scratch).glob("*.json"))
        if wrapper["returncode"] != 0 or len(receipts) != 1:
            return {
                "returncode": wrapper["returncode"],
                "verdict": None,
                "stderr_tail": wrapper["stderr"][-2000:],
                "load_before": wrapper["load_before"],
                "load_after": wrapper["load_after"],
            }
        receipt = json.loads(receipts[0].read_text(encoding="utf-8"))
    original = next(run for run in receipt["runs"] if run["name"] == "original")["run"]
    rows = original.get("rows") or [{}]
    return {
        "returncode": original["returncode"],
        "verdict": rows[0].get("status"),
        "nodes": rows[0].get("nodes"),
        "leaves": rows[0].get("leaves"),
        "min_certified_lower_bound": rows[0].get("lower_bound"),
        "cpu_seconds": original.get("cpu_seconds"),
        "wall_seconds": original.get("wall_seconds"),
        "wrapper_cpu_seconds": wrapper["cpu_seconds"],
        "load_before": wrapper["load_before"],
        "load_after": wrapper["load_after"],
        "controls_status": receipt.get("status"),
        "compiler": receipt.get("checker", {}).get("compiler"),
    }


# Whole-certificate comparison: every one of the 201 directions, one worker each, so the
# CPU is the cost of replaying the certificate. `verify.cpp` runs through the replay
# tool's own `--replay` (compile, exact preflight, all directions); its CPU from `wait4`
# includes those children, and its per-direction receipt rows are kept beside it.
WHOLE: dict[str, Cell] = {
    "rect_n32_L595": Cell("2026-09-27", "rect_n32_L595", 32, -1),
    "rect_n31_L592": Cell("2026-09-27", "rect_n31_L592", 31, -1),
    "rect_n27_L56": Cell("2026-09-27", "rect_n27_L56", 27, -1),
    "rect_n78_L8955": Cell("2026-09-27", "rect_n78_L8955", 78, -1),
}


def whole_fast(binary: Path, cell: Cell) -> dict[str, Any]:
    argv = [
        str(binary.resolve()),
        "--candidate",
        str(cell.candidate),
        "--n",
        str(cell.n),
        "--directions",
        "all",
        "--threshold",
        THRESHOLD,
        "--threads",
        "1",
    ]
    result = run_with_rusage(argv)
    lines = [json.loads(line) for line in result.pop("stdout").splitlines() if line.strip()]
    summary = lines[-1] if lines else {}
    rows = [line for line in lines if "r" in line]
    result["verdict"] = summary.get("status")
    result["nodes"] = summary.get("nodes")
    result["directions"] = len(rows)
    result["axis_cpu_seconds"] = next(
        (row.get("cpu_seconds") for row in rows if row.get("r") == 0), None
    )
    result.pop("stderr")
    return result


def whole_reference(cell: Cell) -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as scratch:
        argv = [
            sys.executable,
            "-m",
            "devtools.audit_wand125_rectangles",
            "--packet",
            cell.packet,
            "--n",
            str(cell.n),
            "--replay",
            "--workers",
            "1",
            "--out",
            scratch,
        ]
        result = run_with_rusage(argv)
        receipt_path = Path(scratch) / "audit.json"
        receipt = (
            json.loads(receipt_path.read_text(encoding="utf-8"))
            if receipt_path.is_file()
            else {}
        )
        rows: list[dict[str, Any]] = []
        for path in Path(scratch).rglob("verified_angles.jsonl"):
            rows += [
                json.loads(line)
                for line in path.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
    result.pop("stdout")
    result["stderr_tail"] = result.pop("stderr")[-2000:]
    result["verdict"] = receipt.get("status")
    result["nodes"] = sum(int(row.get("nodes", 0)) for row in rows)
    result["directions"] = len(rows)
    result["axis_seconds"] = next(
        (row.get("seconds") for row in rows if row.get("r") == 0), None
    )
    result["direction_seconds"] = sum(float(row.get("seconds", 0.0)) for row in rows)
    return result


def run_whole(arms: list[tuple[str, Path | None]], names: list[str], out: Path) -> int:
    rows: list[dict[str, Any]] = []
    with out.open("a", encoding="utf-8") as sink:
        for name in names:
            cell = WHOLE[name]
            for label, path in arms:
                result = whole_reference(cell) if path is None else whole_fast(path, cell)
                row = {
                    "arm": label,
                    "cell": f"{name}@all",
                    "host": os.uname().nodename,
                    "cpus": os.cpu_count(),
                    **result,
                }
                rows.append(row)
                sink.write(json.dumps(row, sort_keys=True) + "\n")
                sink.flush()
                print(
                    f"{name:18} {label:12} cpu={row.get('cpu_seconds')} "
                    f"verdict={row.get('verdict')} directions={row.get('directions')} "
                    f"nodes={row.get('nodes')} load={row.get('load_before')}",
                    flush=True,
                )
    print("\n".join(summarize(rows)))
    return 0


def parse_arm(text: str) -> tuple[str, Path | None]:
    if text == "verify-cpp":
        return ("verify-cpp", None)
    if text.startswith("fast:") and "=" in text:
        label, path = text[len("fast:") :].split("=", 1)
        return (label, Path(path))
    raise SystemExit(f"bad --arm {text!r}: use verify-cpp or fast:LABEL=PATH")


def summarize(rows: list[dict[str, Any]]) -> list[str]:
    arms = sorted({row["arm"] for row in rows})
    cells = list(dict.fromkeys(row["cell"] for row in rows))
    metric = (
        "search_instructions"
        if any(row.get("search_instructions") for row in rows)
        else "instructions"
        if any(row.get("instructions") for row in rows)
        else "cpu_seconds"
    )
    lines = [f"metric: {metric}", "cell".ljust(26) + "".join(arm.rjust(28) for arm in arms)]
    totals = dict.fromkeys(arms, 0.0)
    complete = dict.fromkeys(arms, True)
    for cell in cells:
        text = cell.ljust(26)
        for arm in arms:
            values = [
                row[metric]
                for row in rows
                if row["arm"] == arm and row["cell"] == cell and row.get(metric) is not None
            ]
            if not values:
                text += "-".rjust(28)
                complete[arm] = False
                continue
            mid = median(values)
            totals[arm] += mid
            text += f"{mid:.4g} [{min(values):.4g},{max(values):.4g}]".rjust(28)
        lines.append(text)
    lines.append(
        "total of medians".ljust(26)
        + "".join(
            (f"{totals[arm]:.4g}" + ("" if complete[arm] else " (partial)")).rjust(28)
            for arm in arms
        )
    )
    verdicts = {
        arm: sorted({str(row.get("verdict")) for row in rows if row["arm"] == arm})
        for arm in arms
    }
    lines.append(f"verdicts: {verdicts}")
    loads: list[float] = [
        float(row["load_before"]) for row in rows if row.get("load_before") is not None
    ]
    if loads:
        lines.append(f"load average: median {median(loads):.2f}, max {max(loads):.2f}")
    return lines


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    parser.add_argument("--arm", action="append", required=True)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--cells", default="all", help="'all' or comma-separated cell keys")
    parser.add_argument("--out", type=Path, required=True, help="JSONL of raw runs")
    parser.add_argument("--callgrind", action="store_true")
    parser.add_argument("--summarize", action="store_true", help="only summarize --out")
    parser.add_argument(
        "--whole",
        default="",
        help="comma-separated certificates to replay whole, e.g. rect_n32_L595",
    )
    args = parser.parse_args(argv)
    os.chdir(PROJECT)
    if args.summarize:
        rows = [json.loads(line) for line in args.out.read_text(encoding="utf-8").splitlines()]
        print("\n".join(summarize(rows)))
        return 0
    arms = [parse_arm(text) for text in args.arm]
    if args.whole:
        return run_whole(arms, [name for name in args.whole.split(",") if name], args.out)
    cells = (
        CELLS
        if args.cells == "all"
        else tuple(cell for cell in CELLS if cell.key in set(args.cells.split(",")))
    )
    if not cells:
        raise SystemExit("no benchmark cell selected")
    identities = {
        label: (sha256(path) if path is not None else "verify.cpp via devtools replay")
        for label, path in arms
    }
    rows: list[dict[str, Any]] = []
    with args.out.open("a", encoding="utf-8") as sink:
        for repeat in range(args.repeats):
            for position, cell in enumerate(cells):
                shift = (repeat + position) % len(arms)
                for label, path in arms[shift:] + arms[:shift]:
                    if path is None:
                        if args.callgrind:
                            continue
                        result = reference_run(cell)
                    else:
                        result = fast_run(path, cell, callgrind=args.callgrind)
                    row = {
                        "arm": label,
                        "identity": identities[label],
                        "cell": cell.key,
                        "repeat": repeat,
                        "host": os.uname().nodename,
                        "cpus": os.cpu_count(),
                        **result,
                    }
                    rows.append(row)
                    sink.write(json.dumps(row, sort_keys=True) + "\n")
                    sink.flush()
                    print(
                        f"{cell.key:26} {label:12} r{repeat} "
                        f"cpu={row.get('cpu_seconds')} instr={row.get('instructions')} "
                        f"verdict={row.get('verdict')} nodes={row.get('nodes')} "
                        f"load={row.get('load_before')}",
                        flush=True,
                    )
    print("\n".join(summarize(rows)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
