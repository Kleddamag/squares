"""Verify every replayed wand125 rectangle certificate with the clean-room verifier.

Milestone A of the independent measure verifier (`think-d69e`). The certificates are
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
        --out benchmarks/measure-verifier/census --threads 3 --resume
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

    @property
    def candidate(self) -> Path:
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
        "--threshold",
        THRESHOLD,
        "--threads",
        str(threads),
        "--confirm",
    ]
    before = loadavg()
    start = time.monotonic()
    raw = out / f"{case.certificate}.jsonl"
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
    raw.unlink()
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
            "clears_threshold": exact is not None and Fraction(exact) >= Fraction(THRESHOLD),
        }
    return {
        "least_bound_leaf_exact": least_check,
        "packet": case.packet,
        "certificate": case.certificate,
        "n": case.n,
        "L": case.side,
        "returncode": os.waitstatus_to_exitcode(status),
        "stderr_tail": error_text[-2000:],
        "status": summary.get("status"),
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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    parser.add_argument("--binary", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--threads", type=int, default=1)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--only", default="", help="comma-separated certificate names")
    args = parser.parse_args(argv)
    census_path = args.out / "census.json"
    binary_sha = sha256(args.binary)
    census: dict[str, Any] = (
        json.loads(census_path.read_text(encoding="utf-8"))
        if census_path.is_file()
        else {"kind": "sqverify-fast-census/v1", "threshold": THRESHOLD, "cases": {}}
    )
    cases = replayed_cases()
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
