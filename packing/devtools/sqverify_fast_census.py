"""Verify every replayed wand125 certificate with the clean-room verifier.

Two families. `--family rectangles` is Milestone A of the independent measure verifier
(`think-d69e`); `--family mixed` is Milestone B (`think-4vf7`): every certificate of
formats M and L whose directions this repository has replayed with the authors' checker
(a `range-*` directory under the packet's `receipts/`), at all 201 directions and the
threshold the certificate declares, with the authors' recorded CPU on the directions
they replayed beside ours on the same directions.

For the rectangles family the certificates are
the ones this repository has already replayed with the authors' checker: every case in
the `receipts/replay/audit.json` of the wand125 rectangle packets, and Tokoharu's three
in the 22 September packet. Each runs through `sqverify-fast` at all 201 net
directions; its per-direction receipts and summary are kept as
`--out/PACKET/CERTIFICATE.jsonl.gz`. The census records, per certificate, the
verifier's status, node total, least certified bound, CPU seconds (from `wait4`, user
plus system), wall seconds and load average, beside the binary's and the candidate's
digests. On the least-bound direction, the exact capture at the centre of the
least-bound leaf is evaluated in rationals and must clear the threshold.

A certificate counts as verified here only when the verifier's own summary says
`VERIFIED` (every direction verified and the direction set is the whole net) and its
exit status is zero. `--resume` keeps a case already `VERIFIED`, by whichever build: each
case records its own binary and source digests. `--check` re-reads the census and fails
unless every case is verified, exited zero, and passed the exact least-leaf test.

From `packing/`:

    .venv/bin/python3 -m devtools.sqverify_fast_census \\
        --binary sqverify_fast/target/release/sqverify-fast \\
        --out benchmarks/measure-verifier/census --threads 2 --resume
    .venv/bin/python3 -m devtools.sqverify_fast_census --family mixed \\
        --binary sqverify_fast/target/release/sqverify-fast \\
        --out benchmarks/measure-verifier/census-mixed --threads 2 --resume
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

PROJECT = Path(__file__).resolve().parents[1]
WEB = PROJECT / "resources/web"
PACKETS = ("2026-09-27", "2026-09-28")
THRESHOLD = "10001/10000"
TOKOHARU_PACKET = "2026-09-22"
TOKOHARU = WEB / "external-square-certificates-2026-09-22/tokoharu-density/certificates"
# The packets of formats M and L whose receipts hold replays.
MIXED_PACKETS = (
    "wand125-point-and-mixed-2026-10-01",
    "wand125-mixed-bounds-2026-10-02",
    "wand125-mixed-bounds-n76-2026-10-02",
    "wand125-linear-certificates-2026-10-02",
)
# Tokoharu's three certificates, replayed in the 22 September packet's density receipt.
TOKOHARU_CASES = (
    ("cert_n11_L381", 11, "381/100"),
    ("cert_n26_L5508", 26, "1377/250"),
    ("cert_n29_L571", 29, "571/100"),
)


@dataclass(frozen=True)
class Case:
    """One replayed standing certificate."""

    packet: str
    certificate: str
    n: int
    side: str
    # Mixed family: the candidate's path, and None for the declared threshold.
    path: Path | None = None
    threshold: str | None = THRESHOLD

    @property
    def candidate(self) -> Path:
        if self.path is not None:
            return self.path
        if self.packet == TOKOHARU_PACKET:
            return TOKOHARU / self.certificate / "certified_candidate.json"
        for packet in (self.packet, *PACKETS):
            path = (
                WEB
                / f"wand125-rectangle-certificates-{packet}"
                / "wand125-rectangles/certificates"
                / self.certificate
                / "certified_candidate.json.gz"
            )
            if path.is_file():
                return path
        raise SystemExit(f"no retained candidate for {self.certificate}")


def replayed_cases() -> list[Case]:
    receipt = WEB / "external-square-certificates-2026-09-22/receipts/density/audit.json"
    passed = {
        (int(case["n"]), str(case["L"]))
        for case in json.loads(receipt.read_text(encoding="utf-8"))["cases"]
        if case.get("status") == "PASS"
    }
    cases: list[Case] = [
        Case(TOKOHARU_PACKET, name, n, side)
        for name, n, side in TOKOHARU_CASES
        if (n, side) in passed
    ]
    for packet in PACKETS:
        receipt = WEB / f"wand125-rectangle-certificates-{packet}/receipts/replay/audit.json"
        data = json.loads(receipt.read_text(encoding="utf-8"))
        for case in data["cases"]:
            if case.get("status") != "PASS":
                continue
            cases.append(Case(packet, case["certificate"], int(case["n"]), str(case["L"])))
    return cases


def mixed_cases() -> list[Case]:
    """Every format M or L certificate with at least one replayed direction."""
    cases: list[Case] = []
    for packet in MIXED_PACKETS:
        receipts = WEB / packet / "receipts"
        for folder in sorted(receipts.iterdir()):
            if not folder.is_dir() or not any(folder.glob("range-*/directions.jsonl")):
                continue
            n = int(folder.name.removeprefix("n"))
            found = sorted(
                (WEB / packet / "square-packing-bounds/certificates").glob(
                    f"mixed_n{n}_L*/candidate.json.gz"
                )
            )
            if len(found) != 1:
                raise SystemExit(f"{packet}: no single candidate for n{n}")
            data = json.loads(gzip.decompress(found[0].read_bytes()))
            side = str(Fraction(str(data["L"])))
            cases.append(Case(packet, found[0].parent.name, n, side, found[0], None))
    return cases


def mixed_reference(case: Case) -> dict[str, Any]:
    """The authors' replayed directions of one mixed case, with their CPU seconds."""
    folder = WEB / case.packet / "receipts" / f"n{case.n}"
    rows: dict[int, dict[str, Any]] = {}
    for path in sorted(folder.glob("range-*/directions.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            row = json.loads(line)
            if row.get("status") == "REPLAYED":
                rows[int(row["index"])] = row
    return {
        "directions": sorted(rows),
        "cpu_seconds": sum(float(row.get("cpu_seconds") or 0.0) for row in rows.values()),
        "nodes": sum(int((row.get("report") or {}).get("nodes") or 0) for row in rows.values()),
    }


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def loadavg() -> float:
    return os.getloadavg()[0]


def run(binary: Path, case: Case, out: Path, threads: int) -> dict[str, Any]:
    """Run all directions of one case; keep the receipts as deterministic gzip JSONL."""
    out.mkdir(parents=True, exist_ok=True)
    argv = [
        str(binary.resolve()),
        "--candidate",
        str(case.candidate),
        "--n",
        str(case.n),
        "--side",
        case.side,
        "--directions",
        "all",
        *(["--threshold", case.threshold] if case.threshold is not None else []),
        "--threads",
        str(threads),
        "--confirm",
    ]
    before = loadavg()
    start = time.monotonic()
    # The live output goes to a file outside the tree: a commit hook that hides
    # unstaged changes once replaced a half-written receipt file under a running
    # verifier, which kept writing to the orphaned file (rect_n69_L8575, first run).
    scratch = tempfile.TemporaryDirectory(prefix="sqverify-fast-census-")
    raw = Path(scratch.name) / f"{case.certificate}.jsonl"
    with raw.open("wb") as stdout, tempfile.TemporaryFile() as stderr:
        pid = os.posix_spawn(
            argv[0],
            argv,
            os.environ,
            file_actions=[
                (os.POSIX_SPAWN_DUP2, stdout.fileno(), 1),
                (os.POSIX_SPAWN_DUP2, stderr.fileno(), 2),
            ],
        )
        _, status, usage = os.wait4(pid, 0)
        stderr.seek(0)
        error_text = stderr.read().decode(errors="replace")
    wall = time.monotonic() - start
    lines = [json.loads(line) for line in raw.read_text(encoding="utf-8").splitlines() if line]
    rows = sorted((line for line in lines if "r" in line), key=lambda row: int(row["r"]))
    summary = next(
        (line for line in lines if line.get("kind") == "sqverify-fast-summary/v1"), {}
    )
    body = "".join(json.dumps(line, sort_keys=True) + "\n" for line in [*rows, summary])
    with gzip.GzipFile(out / f"{case.certificate}.jsonl.gz", "wb", mtime=0) as packed:
        packed.write(body.encode())
    scratch.cleanup()
    bounds = [
        row["min_certified_lower_bound"]
        for row in rows
        if row.get("min_certified_lower_bound") is not None
    ]
    least = min(
        (row for row in rows if row.get("least_bound_box") is not None),
        key=lambda row: row["min_certified_lower_bound"],
        default=None,
    )
    threshold = Fraction(str(summary.get("threshold") or case.threshold or THRESHOLD))
    least_check: dict[str, Any] | None = None
    if least is not None:
        box = least["least_bound_box"]
        spec = f"{least['r']},{box['x']!r},{box['y']!r}"
        probe = subprocess.run(
            [argv[0], "--candidate", str(case.candidate), "--n", str(case.n), "--probe", spec],
            capture_output=True,
            text=True,
            check=False,
        )
        reading = json.loads(probe.stdout) if probe.returncode == 0 else {}
        exact = reading.get("exact_coverage")
        least_check = {
            "r": least["r"],
            "centre": [box["x"], box["y"]],
            "exact_coverage": exact,
            "clears_threshold": exact is not None and Fraction(exact) >= threshold,
        }
    return {
        "least_bound_leaf_exact": least_check,
        "threshold": str(threshold),
        "direction_cpu_seconds": {
            str(row["r"]): row.get("cpu_seconds") for row in rows if "cpu_seconds" in row
        },
        "packet": case.packet,
        "certificate": case.certificate,
        "n": case.n,
        "L": case.side,
        "returncode": os.waitstatus_to_exitcode(status),
        "stderr_tail": error_text[-2000:],
        "status": summary.get("status") if len(rows) == 201 else "INCOMPLETE",
        "directions_verified": sum(1 for row in rows if row.get("verdict") == "verified"),
        "refused_directions": summary.get("refused_directions"),
        "nodes": summary.get("nodes"),
        "least_certified_bound": min(bounds) if bounds else None,
        "axis_vertices": next((row.get("vertices") for row in rows if row.get("r") == 0), None),
        "cpu_seconds": usage.ru_utime + usage.ru_stime,
        "wall_seconds": wall,
        "threads": threads,
        "load_before": before,
        "load_after": loadavg(),
        "candidate_sha256": sha256(case.candidate),
        "premises": summary.get("premises"),
        "build": summary.get("build"),
    }


def replay_reference() -> dict[str, dict[str, Any]]:
    """The authors' checker's replay summaries, by certificate name."""
    reference: dict[str, dict[str, Any]] = {}
    density = WEB / "external-square-certificates-2026-09-22/receipts/density/audit.json"
    names = {(n, side): name for name, n, side in TOKOHARU_CASES}
    for case in json.loads(density.read_text(encoding="utf-8"))["cases"]:
        name = names.get((int(case["n"]), str(case["L"])))
        if name is not None:
            reference[name] = case["replay"]
    for packet in PACKETS:
        receipt = WEB / f"wand125-rectangle-certificates-{packet}/receipts/replay/audit.json"
        for case in json.loads(receipt.read_text(encoding="utf-8"))["cases"]:
            reference[case["certificate"]] = case["replay"]
    return reference


def workers_of(command: object) -> str:
    if isinstance(command, list):
        words = [str(word) for word in command]
        if "--workers" in words:
            return words[words.index("--workers") + 1]
    return "?"


def render_report(census: dict[str, Any]) -> str:
    """The census as a Markdown table, generated from census.json and the receipts."""
    reference = replay_reference()
    lines = [
        "# Milestone A Census",
        "",
        "Generated by `python -m devtools.sqverify_fast_census --report`; do not edit by hand.",
        "",
        "Every rectangle-density certificate this repository has replayed with the authors'",
        "checker, verified by `sqverify-fast` at all 201 net directions at the threshold",
        f"{census['threshold']}. *Nodes* counts boxes at $r \\ge 1$; the authors' count also",
        "includes the axis direction's vertices, given here as *axis vertices*. *Exact leaf*",
        "is the exact rational capture at the centre of the least-bound leaf of the",
        "least-bound direction, which must clear the threshold. CPU is user plus system",
        "time of the whole process (`wait4`), on a shared host whose load average is given.",
        "The replay wall is the authors' checker's recorded wall time with the worker count",
        "it ran with, so it is not a CPU figure.",
        "",
        (
            "| Certificate | n | Status | Directions | Nodes | Axis vertices | Authors' nodes"
            " | Least certified bound | Exact leaf | CPU s | Load | Authors' replay wall s"
            " (workers) |"
        ),
        "| --- | ---: | --- | ---: | ---: | ---: | ---: | --- | --- | ---: | ---: | ---: |",
    ]
    total_cpu = 0.0
    verified = 0
    for name in sorted(census["cases"], key=lambda key: (census["cases"][key]["n"], key)):
        case = census["cases"][name]
        replay = reference.get(name, {})
        summary = replay.get("summary", {})
        least = case.get("least_bound_leaf_exact") or {}
        wall = summary.get("wall_seconds")
        wall_text = (
            f"{float(Fraction(wall)):.0f} ({workers_of(replay.get('command'))})"
            if wall
            else "-"
        )
        total_cpu += float(case.get("cpu_seconds") or 0.0)
        verified += case.get("status") == "VERIFIED"
        cpu = float(case.get("cpu_seconds") or 0.0)
        cells = [
            f"`{name}`",
            str(case["n"]),
            str(case.get("status")),
            str(case.get("directions_verified")),
            f"{case.get('nodes'):,}",
            f"{case.get('axis_vertices') or 0:,}",
            f"{int(summary.get('nodes', 0)):,}",
            str(case.get("least_certified_bound")),
            "clears" if least.get("clears_threshold") else "FAILS",
            f"{cpu:.1f}",
            f"{float(case.get('load_before') or 0.0):.1f}",
            wall_text,
        ]
        lines.append("| " + " | ".join(cells) + " |")
    count = len(census["cases"])
    lines += [
        "",
        f"{verified} of {count} certificates verified; {total_cpu:.0f} CPU seconds in all.",
        "",
        "<!-- This document follows common-doc-guidelines.md.",
        "See github.com/jlevy/practical-prose and review guidelines before editing.",
        "-->",
        "",
    ]
    return "\n".join(lines)


MIXED_ALIGN = "--- ---: --- --- ---: ---: --- --- ---: ---: --- ---: ---: ---:"


def render_mixed_report(census: dict[str, Any]) -> str:
    """The mixed census as a Markdown table, beside the authors' replays."""
    cases = {case.certificate: case for case in mixed_cases()}
    lines = [
        "# Milestone B Census",
        "",
        "Generated by `python -m devtools.sqverify_fast_census --family mixed --report`;",
        "do not edit by hand.",
        "",
        "Every certificate of formats M (rectangle rows, per-bin centre domain) and L (points,",
        "segments and rectangles, Tokoharu's domain) with at least one direction replayed by",
        "the authors' checker in this repository, verified by `sqverify-fast` at all 201 net",
        "directions at the threshold the certificate declares, 1. *Exact leaf* is the exact",
        "rational capture at the centre of the least-bound leaf of the least-bound direction.",
        "*Authors' CPU* is the authors' checker's recorded CPU seconds on the directions this",
        "repository replayed; *ours, same directions* is `sqverify-fast`'s thread CPU on",
        "exactly those directions. CPU on a shared host whose load average is given.",
        "",
        (
            "| Certificate | n | Format | Status | Directions | Nodes | Least certified bound"
            " | Exact leaf | CPU s, all 201 | Load | Replayed directions | Authors' CPU s"
            " | Ours, same directions | Ratio |"
        ),
        "|" + "|".join(f" {align} " for align in MIXED_ALIGN.split()) + "|",
    ]
    total_cpu = 0.0
    verified = 0
    for name in sorted(census["cases"], key=lambda key: (census["cases"][key]["n"], key)):
        entry = census["cases"][name]
        case = cases.get(name)
        reference: dict[str, Any] = (
            mixed_reference(case) if case is not None else {"directions": []}
        )
        replayed = reference["directions"]
        ours = sum(
            float((entry.get("direction_cpu_seconds") or {}).get(str(r)) or 0.0)
            for r in replayed
        )
        authors = float(reference.get("cpu_seconds") or 0.0)
        span = "all 201" if len(replayed) == 201 else ", ".join(str(r) for r in replayed)
        least = entry.get("least_bound_leaf_exact") or {}
        cpu = float(entry.get("cpu_seconds") or 0.0)
        total_cpu += cpu
        verified += entry.get("status") == "VERIFIED"
        cells = [
            f"`{name}`",
            str(entry["n"]),
            str((entry.get("premises") or {}).get("format")),
            str(entry.get("status")),
            str(entry.get("directions_verified")),
            f"{entry.get('nodes'):,}",
            str(entry.get("least_certified_bound")),
            "clears" if least.get("clears_threshold") else "FAILS",
            f"{cpu:.1f}",
            f"{float(entry.get('load_before') or 0.0):.1f}",
            span,
            f"{authors:,.0f}",
            f"{ours:.1f}",
            f"{authors / ours:,.0f}x" if ours > 0 else "-",
        ]
        lines.append("| " + " | ".join(cells) + " |")
    lines += [
        "",
        (
            f"{verified} of {len(census['cases'])} certificates verified;"
            f" {total_cpu:.0f} CPU seconds in all."
        ),
        "",
        "<!-- This document follows common-doc-guidelines.md.",
        "See github.com/jlevy/practical-prose and review guidelines before editing.",
        "-->",
        "",
    ]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    parser.add_argument("--family", choices=("rectangles", "mixed"), default="rectangles")
    parser.add_argument("--binary", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--threads", type=int, default=1)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument(
        "--report", action="store_true", help="render --out/README.md from the census"
    )
    parser.add_argument("--only", default="", help="comma-separated certificate names")
    args = parser.parse_args(argv)
    census_path = args.out / "census.json"
    binary_sha = sha256(args.binary)
    census: dict[str, Any] = (
        json.loads(census_path.read_text(encoding="utf-8"))
        if census_path.is_file()
        else {"kind": "sqverify-fast-census/v1", "threshold": THRESHOLD, "cases": {}}
    )
    mixed = args.family == "mixed"
    if mixed:
        census["family"] = "mixed"
        census["threshold"] = "declared"
    cases = mixed_cases() if mixed else replayed_cases()
    if args.report:
        render = render_mixed_report if mixed else render_report
        (args.out / "README.md").write_text(render(census), encoding="utf-8")
        return 0
    if args.check:

        def passed(entry: dict[str, Any]) -> bool:
            least = entry.get("least_bound_leaf_exact") or {}
            return (
                entry.get("status") == "VERIFIED"
                and entry.get("returncode") == 0
                and least.get("clears_threshold") is True
            )

        missing = [
            case.certificate
            for case in cases
            if not passed(census["cases"].get(case.certificate, {}))
        ]
        print(f"{len(cases) - len(missing)} of {len(cases)} replayed certificates VERIFIED")
        for name in missing:
            print(f"  not verified: {name}")
        return 1 if missing else 0
    only = {name for name in args.only.split(",") if name}
    for case in cases:
        if only and case.certificate not in only:
            continue
        held = census["cases"].get(case.certificate)
        # A verified case is kept whichever build verified it: each case records its
        # own binary and source digests, so a census may span builds honestly.
        if args.resume and held is not None and held.get("status") == "VERIFIED":
            continue
        result = run(args.binary, case, args.out / case.packet, args.threads)
        result["binary_sha256"] = binary_sha
        census["cases"][case.certificate] = result
        census_path.parent.mkdir(parents=True, exist_ok=True)
        census_path.write_text(json.dumps(census, indent=2, sort_keys=True) + "\n")
        print(
            f"{case.certificate:18} {result['status']} dirs={result['directions_verified']} "
            f"nodes={result['nodes']} least={result['least_certified_bound']} "
            f"cpu={result['cpu_seconds']:.1f}s wall={result['wall_seconds']:.1f}s "
            f"load={result['load_before']:.1f}",
            flush=True,
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
