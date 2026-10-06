"""Verify every replayed wand125 certificate with the clean-room verifier.

Two families, each covering every retained certificate of its formats, replayed by the
authors' checker here or not. `--family rectangles` (format T; Milestone A,
`think-d69e`) runs every `certified_candidate.json.gz` of the wand125 rectangle packets
and Tokoharu's three, at the threshold the files declare; `--family mixed` (formats M
and L; Milestone B, `think-4vf7`) runs every `mixed_n*` candidate of the wand125 mixed
and linear packets at the threshold they declare, with the authors' recorded CPU on the
directions they replayed beside ours on the same directions. `--summary` writes
`census-summary.json` and `census-summary.md` beside the two census folders: one row per
certificate with its verdict, CPU, least certified bound and whether the authors' replay
recorded here is complete, the input the records lane uses for evidence entries.

The replay receipts named below were the first census's case list; the rectangle
family now reads them only for the authors' replay status. They are
the ones this repository has already replayed with the authors' checker: every case in
the `receipts/replay/audit.json` of the wand125 rectangle packets, and Tokoharu's three
in the 22 September packet. Each runs through `sqverify-fast` at every direction of its
net, 201 unless a format M file declares its own (`proof_net`, jlevy/squares#366); its
per-direction receipts and summary are kept as `--out/PACKET/CERTIFICATE.jsonl.gz`.
The census records, per certificate, the verifier's status, node total, least
certified bound, CPU seconds (from `wait4`, user plus system), wall seconds and load
average, beside the binary's and the candidate's digests. On the least-bound
direction, the exact capture at the centre of the least-bound leaf is evaluated in
rationals and must clear the threshold.

A certificate counts as verified here only when the verifier's own summary says
`VERIFIED` (every direction verified and the direction set is the whole net) and its
exit status is zero. `--resume` keeps a case already `VERIFIED`, by whichever build: each
case records its own binary and source digests. `--check` re-reads the census and fails
unless every case is verified, exited zero, and passed the exact least-leaf test;
`--only` and `--packets` narrow it as they narrow a run.

`--control` (mixed family) puts negative controls on a verified certificate itself, at
its least-bound direction: the original must verify there, and two mutants must be
refused, every mass scaled by 99/100 (the stage-4 control of the authors' replays), and
every mass scaled so that the exact capture at the least-bound leaf's centre is at most
one part in a million below the threshold. That capture is evaluated again by
`check_sqverify_fast.mixed_exact`, an exact evaluator written apart from the crate, and
must equal the crate's; each refused mutant must capture less than 1 at that centre or at
the refusal's witness, evaluated the same way. The near-threshold mutant is named for
the centre it is scaled at: the verifier may refuse it at another centre, and its
discrimination near the threshold rests on the crate's own tests (IR-3 of the review
of 5 October). Each receipt is `--out/PACKET/CERTIFICATE.control.json`, with status
`CONTROLS_REFUSED` only when all of that holds. `--evidence` prints each selected
certificate's replay evidence entry, for a records lane to paste into the register.

From `packing/`:

    .venv/bin/python3 -m devtools.sqverify_fast_census \\
        --binary sqverify_fast/target/release/sqverify-fast \\
        --out benchmarks/measure-verifier/census --threads 2 --resume
    .venv/bin/python3 -m devtools.sqverify_fast_census --family mixed \\
        --binary sqverify_fast/target/release/sqverify-fast \\
        --out benchmarks/measure-verifier/census-mixed --threads 2 --resume
    .venv/bin/python3 -m devtools.sqverify_fast_census --family mixed --control \\
        --binary sqverify_fast/target/release/sqverify-fast \\
        --out benchmarks/measure-verifier/census-mixed --only mixed_n67_L848
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
import textwrap
import time
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from devtools.check_sqverify_fast import mixed_exact, mixed_mutant, read_raw
from sqpack import retained_json
from sqpack.yamlio import safe_load

PROJECT = Path(__file__).resolve().parents[1]
WEB = PROJECT / "resources/web"
PACKETS = ("2026-09-27", "2026-09-28", "2026-10-01", "2026-10-02")
THRESHOLD = "10001/10000"
TOKOHARU_PACKET = "2026-09-22"
TOKOHARU = WEB / "external-square-certificates-2026-09-22/tokoharu-density/certificates"
# The packets of formats M and L.
MIXED_PACKETS = (
    "wand125-point-and-mixed-2026-09-28",
    "wand125-point-and-mixed-2026-10-01",
    "wand125-mixed-bounds-2026-10-02",
    "wand125-mixed-bounds-n76-2026-10-02",
    "wand125-mixed-bounds-afternoon-2026-10-02",
    "wand125-linear-certificates-2026-10-02",
    "wand125-linear-n82-2026-10-02",
    "wand125-mixed-bounds-2026-10-03",
    "wand125-mixed-bounds-2026-10-04",
    "wand125-mixed-bounds-evening-2026-10-04",
    "wand125-mixed-bounds-2026-10-05",
    "wand125-mixed-bounds-finer-net-2026-10-05",
)
#: The standard net's direction count; a format M file may declare another.
STANDARD_DIRECTIONS = 201
CENSUS_ROOT = PROJECT / "benchmarks/measure-verifier"
# Tokoharu's three certificates, replayed in the 22 September packet's density receipt.
TOKOHARU_CASES = (
    ("cert_n11_L381", 11, "381/100"),
    ("cert_n26_L5508", 26, "1377/250"),
    ("cert_n29_L571", 29, "571/100"),
)


@dataclass(frozen=True)
class Case:
    """One retained certificate."""

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


def side_digits(side: Fraction) -> str:
    """The digits of a side as certificate names spell it: `447/50` is `894`."""
    text = f"{float(side):.6f}".rstrip("0").rstrip(".")
    return text.replace(".", "")


def named_side(name: str, side: Fraction) -> bool:
    """Whether a certificate's name (`..._L894`) spells its side."""
    digits = name.rsplit("_L", 1)[1]
    return digits.rstrip("0") == side_digits(side).rstrip("0")


def rectangle_cases() -> list[Case]:
    """Tokoharu's three replayed certificates and every wand125 rectangle certificate."""
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
        root = WEB / f"wand125-rectangle-certificates-{packet}/wand125-rectangles/certificates"
        for path in sorted(root.glob("rect_n*_L*/certified_candidate.json.gz")):
            name = path.parent.name
            data = json.loads(gzip.decompress(path.read_bytes()), parse_float=str)
            side = Fraction(str(data["L"]))
            if not named_side(name, side):
                raise SystemExit(f"{name}: the name does not spell the side {side}")
            n = int(name.split("_")[1].removeprefix("n"))
            cases.append(Case(packet, name, n, str(side), path))
    return cases


def mixed_cases() -> list[Case]:
    """Every format M or L certificate of the wand125 mixed and linear packets."""
    cases: list[Case] = []
    for packet in MIXED_PACKETS:
        root = WEB / packet / "square-packing-bounds/certificates"
        for path in sorted(root.glob("mixed_n*_L*/candidate.json.gz")):
            name = path.parent.name
            data = json.loads(gzip.decompress(path.read_bytes()), parse_float=str)
            side = Fraction(str(data["L"]))
            n = int(data["n"])
            if not named_side(name, side) or name.split("_")[1] != f"n{n}":
                raise SystemExit(f"{name}: the name does not spell n = {n} and L = {side}")
            cases.append(Case(packet, name, n, str(side), path, None))
    return cases


def net_directions(case: Case) -> int:
    """How many net directions a case's certificate has: its `proof_net`'s, else 201."""
    raw = case.candidate.read_bytes()
    data = json.loads(gzip.decompress(raw) if raw[:2] == b"\x1f\x8b" else raw)
    net = data.get("proof_net") if isinstance(data, dict) else None
    return int(net["last"]) + 1 if isinstance(net, dict) else STANDARD_DIRECTIONS


def replay_folders(case: Case) -> list[Path]:
    """A mixed case's receipt folders: `n76`, or `n85-L946` where two sides share n."""
    receipts = WEB / case.packet / "receipts"
    digits = case.certificate.rsplit("_L", 1)[1]
    named = receipts / f"n{case.n}-L{digits}"
    plain = receipts / f"n{case.n}"
    if named.is_dir():
        return [named]
    return [plain] if plain.is_dir() else []


def has_siblings(case: Case) -> bool:
    """Whether another certificate of the packet has the same n (and so `nN` is shared)."""
    return any(
        other.name != case.certificate
        for other in (WEB / case.packet / "square-packing-bounds/certificates").glob(
            f"mixed_n{case.n}_L*"
        )
    )


def mixed_reference(case: Case) -> dict[str, Any]:
    """The authors' replayed directions of one mixed case, with their CPU seconds.

    A full replay recorded only as a comparison (`full/compare.json`, the 28 September
    packet) counts as every direction of the case's net when its certificate digest is
    this case's.
    """
    rows: dict[int, dict[str, Any]] = {}
    complete_without_rows = False
    shared = has_siblings(case) and not any(
        folder.name.startswith(f"n{case.n}-L") for folder in replay_folders(case)
    )
    for folder in replay_folders(case):
        # A folder shared by two sides of the same n binds only through a digest.
        for path in [] if shared else sorted(folder.glob("range-*/directions.jsonl")):
            for line in path.read_text(encoding="utf-8").splitlines():
                row = json.loads(line)
                if row.get("status") == "REPLAYED":
                    rows[int(row["index"])] = row
        compare = folder / "full/compare.json"
        if compare.is_file():
            record = json.loads(compare.read_text(encoding="utf-8"))
            certificate = case.candidate.parent / "certificate.json.gz"
            digest = (
                hashlib.sha256(gzip.decompress(certificate.read_bytes())).hexdigest()
                if certificate.is_file()
                else None
            )
            # The replay's own digest is of a file not retained here; its inputs
            # receipt binds it instead, by the number of rectangle images it enclosed.
            inputs = folder / "inputs.json"
            images = (
                json.loads(inputs.read_text(encoding="utf-8")).get("rectangle_images")
                if inputs.is_file()
                else None
            )
            rows_here = json.loads(gzip.decompress(case.candidate.read_bytes())).get(
                "rectangles", []
            )
            complete_without_rows = record.get("status") == "FULL_REPLAY_MATCHES_SHIPPED" and (
                record.get("certificate_sha256") == digest or images == 8 * len(rows_here)
            )
    return {
        "directions": (
            list(range(net_directions(case))) if complete_without_rows else sorted(rows)
        ),
        "cpu_seconds": sum(float(row.get("cpu_seconds") or 0.0) for row in rows.values()),
        "nodes": sum(int((row.get("report") or {}).get("nodes") or 0) for row in rows.values()),
        "per_direction_cpu": not complete_without_rows,
    }


def replay_status(directions: int, total: int = STANDARD_DIRECTIONS) -> str:
    """How much of a certificate's `total` directions the authors' replay here covers."""
    if directions >= total:
        return "complete"
    return f"partial ({directions} of {total})" if directions else "none"


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
        "status": (
            summary.get("status")
            if len(rows)
            == int((summary.get("premises") or {}).get("angle_count") or STANDARD_DIRECTIONS)
            else "INCOMPLETE"
        ),
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


#: The two mutations of `--control`: the stage-4 scaling, and a scaling to at most one
#: part in a million below the threshold at the least-bound leaf's centre.
CONTROL_SCALE = Fraction(99, 100)
NEAR_THRESHOLD = Fraction(1, 10**6)


def direction_row(binary: Path, candidate: Path, n: int, index: int) -> dict[str, Any]:
    """One direction of one candidate at its declared threshold, with `--confirm`."""
    argv = [str(binary.resolve()), "--candidate", str(candidate), "--n", str(n)]
    argv += ["--directions", str(index), "--confirm"]
    start = time.monotonic()
    result = subprocess.run(argv, capture_output=True, text=True, check=False, timeout=7200)
    lines = [json.loads(line) for line in result.stdout.splitlines() if line.startswith("{")]
    row = next((line for line in lines if line.get("r") == index), {})
    witness = row.get("witness") or {}
    return {
        "returncode": result.returncode,
        "verdict": row.get("verdict"),
        "nodes": row.get("nodes"),
        "min_certified_lower_bound": row.get("min_certified_lower_bound"),
        "exact_below_threshold": witness.get("exact_below_threshold"),
        "witness": witness or None,
        "seconds": round(time.monotonic() - start, 2),
        "stderr_tail": result.stderr[-500:],
    }


def control(binary: Path, case: Case, entry: dict[str, Any]) -> dict[str, Any]:
    """Negative controls on a verified mixed certificate, at its least-bound direction."""
    least = entry.get("least_bound_leaf_exact") or {}
    if entry.get("status") != "VERIFIED" or not least:
        raise SystemExit(f"{case.certificate}: control needs a verified census entry")
    index = int(least["r"])
    centre = [Fraction(value) for value in least["centre"]]
    crate = Fraction(least["exact_coverage"])
    raw = read_raw(case.candidate)
    exact = mixed_exact(raw, centre[0], centre[1], index)
    # Rounded down, so the capture at the centre is at most 1 - NEAR_THRESHOLD.
    near = Fraction(int((1 - NEAR_THRESHOLD) / exact * 10**15), 10**15)
    runs: list[dict[str, Any]] = []
    original = direction_row(binary, case.candidate, case.n, index)
    runs.append({"name": "original", "expect": "verified", **original})
    with tempfile.TemporaryDirectory(prefix="sqverify-fast-control-") as scratch:
        for name, factor in (("scaled-99-100", CONTROL_SCALE), ("near-threshold", near)):
            path = Path(scratch) / f"{case.certificate}-{name}.json"
            path.write_text(json.dumps(mixed_mutant(raw, factor=factor)), encoding="utf-8")
            row = direction_row(binary, path, case.n, index)
            # The refusal's witness, evaluated again apart from the crate: the mutant's
            # capture there is the factor times the original's.
            pose = (row.get("witness") or {}).get("exact_pose")
            witness = (
                factor * mixed_exact(raw, Fraction(pose[0]), Fraction(pose[1]), index)
                if pose
                else None
            )
            runs.append(
                {
                    "name": name,
                    "mutation": {
                        "factor": str(factor),
                        "capture_at_centre": str(exact * factor),
                        "capture_at_witness": None if witness is None else str(witness),
                    },
                    "expect": "refused",
                    **row,
                }
            )

    def held(run: dict[str, Any]) -> bool:
        if run["expect"] == "verified":
            return run["returncode"] == 0 and run["verdict"] == "verified"
        # Refused, and the mutant's claim is false at a centre this tool evaluated
        # exactly: the least-bound leaf's centre, or the refusal's witness.
        mutation = run["mutation"]
        uncovered = Fraction(mutation["capture_at_centre"]) < 1 or (
            mutation["capture_at_witness"] is not None
            and Fraction(mutation["capture_at_witness"]) < 1
        )
        return run["returncode"] == 1 and run["verdict"] not in (None, "verified") and uncovered

    agree = exact == crate
    return {
        "kind": "sqverify-fast-control/v1",
        "packet": case.packet,
        "certificate": case.certificate,
        "n": case.n,
        "L": case.side,
        "candidate_sha256": sha256(case.candidate),
        "binary_sha256": sha256(binary),
        "index": index,
        "centre": least["centre"],
        "exact_capture_crate": str(crate),
        "exact_capture_independent": str(exact),
        "captures_agree": agree,
        "runs": runs,
        "status": "CONTROLS_REFUSED" if all(map(held, runs)) and agree else "CONTROL_FAILED",
    }


def control_status(case: Case, out: Path) -> str | None:
    """A control receipt's status, or None where none is kept."""
    path = out / case.packet / f"{case.certificate}.control.json"
    if not path.is_file():
        return None
    return str(json.loads(path.read_text(encoding="utf-8")).get("status"))


#: The register's evidence, read by `--evidence` for each certificate's reported entry.
EVIDENCE = PROJECT / "frontier/evidence.yaml"
#: What `--evidence` says of the build, whose crate source is the reviewed one.
REVIEWED_BUILD = "4ddf37d9c"
#: The review that accepted a census row and a control receipt as a complete replay here,
#: and says which certificates the route carries to (Carrying the Route).
ROUTE_REVIEW = (
    "docs/project/reviews/review-2026-10-05-wand125-october-5-and-independent-replays.md"
)
#: That build's `source_sha256`, which `build.rs` takes over src/, Cargo.toml, Cargo.lock
#: and itself; the gate's test profile in Cargo.toml has changed it since.
REVIEWED_SOURCE = "9985c465"
#: The assumptions every format M replay entry states beside its mass.
ASSUMPTIONS = (
    (
        "Every angle and legal centre is covered by the net of 201 half-angles of step"
        " 83/40000 at core side 9977/10000 and format M's per-bin centre domains, which"
        " admission checks in exact rationals."
    ),
    (
        "Binary64 arithmetic has IEEE-754 semantics with directed rounding per operation,"
        " as SOUNDNESS.md's Floating Point section uses it."
    ),
    (
        "The candidate is the retained file whose decompressed SHA-256 the packet's"
        " acquisition record pins, which mixed-fetch found identical to the proof bundle's."
    ),
)


def folded(key: str, text: str, indent: int = 4) -> list[str]:
    """A YAML folded block, wrapped as the register's hand-written entries are."""
    body = textwrap.wrap(
        text, width=90 - indent, break_long_words=False, break_on_hyphens=False
    )
    return [f"{' ' * indent}{key}: >-", *(f"{' ' * (indent + 2)}{line}" for line in body)]


def uncovered(run: dict[str, Any]) -> str:
    """Where a control's mutant was shown, exactly, to capture less than 1."""
    mutation = run["mutation"]
    if Fraction(mutation["capture_at_centre"]) < 1:
        return "exact capture below 1 at the least-bound leaf's centre"
    return "exact capture below 1 at its witness"


def evidence_entry(
    case: Case, out: Path, entry: dict[str, Any], *, audit_record: str, date: str
) -> str:
    """The replay evidence entry for one verified, controlled certificate, as YAML text.

    It names the certificate's reported entry, takes its source key and scope, and states
    the census row and the control receipt in its limitations. A records lane pastes it
    into `frontier/evidence.yaml` and widens the scope where the bound carries by mass.
    """
    register = safe_load(EVIDENCE.read_text(encoding="utf-8"))
    certificate = str(case.candidate.relative_to(PROJECT))
    (report,) = (
        item
        for item in register["evidence"]
        if item.get("assurance") == "reported" and item.get("certificate") == certificate
    )
    receipt = json.loads((out / case.packet / f"{case.certificate}.control.json").read_text())
    if entry.get("status") != "VERIFIED" or receipt.get("status") != "CONTROLS_REFUSED":
        raise SystemExit(f"{case.certificate}: not verified and controlled")
    rows = [
        json.loads(line)
        for line in gzip.decompress(
            (out / case.packet / f"{case.certificate}.jsonl.gz").read_bytes()
        )
        .decode()
        .splitlines()
    ]
    axis = next(row for row in rows if row.get("r") == 0)
    oblique = min(
        (row for row in rows if int(row.get("r", 0)) >= 1),
        key=lambda row: row["min_certified_lower_bound"],
    )
    premises = entry["premises"]
    runs = {run["name"]: run for run in receipt["runs"]}
    side = Fraction(case.side)
    mass = Fraction(premises["mass_exact"])
    identifier = str(report["id"]).removesuffix("-report") + "-sqverify-fast-replay"
    packet_path = f"benchmarks/measure-verifier/census-mixed/{case.packet}/{case.certificate}"
    replay = (
        "From packing/, after cargo build --release in sqverify_fast/ (toolchain 1.98.0): "
        ".venv/bin/python3 -m devtools.sqverify_fast_census --family mixed --binary "
        "sqverify_fast/target/release/sqverify-fast --out "
        f"benchmarks/measure-verifier/census-mixed --threads 2 --only {case.certificate} "
        "runs sqverify-fast on the retained candidate at all 201 net directions at the "
        "threshold it declares, 1, and records the case in census.json there; "
        f"--check --only {case.certificate} must then print 1 of 1 retained certificates "
        "VERIFIED (every direction verified, summary VERIFIED, exit 0, and the exact capture "
        "at the least-bound leaf's centre at least 1). The same command with --control in "
        "place of --threads 2 must write status CONTROLS_REFUSED. The receipts are "
        f"{packet_path}.jsonl.gz and {packet_path}.control.json, held by "
        "tests/test_sqverify_fast_census.py."
    )
    least = entry["least_bound_leaf_exact"]
    stored = str(entry["candidate_sha256"])
    pinned = hashlib.sha256(gzip.decompress(case.candidate.read_bytes())).hexdigest()
    built = str((entry.get("build") or {}).get("source_sha256", ""))
    limitations = (
        "sqverify-fast, this repository's clean-room measure verifier, decided the retained "
        f"candidate {case.certificate} at all 201 net directions on {date}. The receipts "
        f"name the stored gzip file's SHA-256 {stored[:8]}..., which decompresses to the "
        f"SHA-256 {pinned[:8]}... the packet's acquisition record pins "
        "(devtools.retained_data check ties the two). Admission recomputed in exact "
        f"rationals n = {case.n}, L = {side}, the total mass {mass} < {case.n}, the core "
        f"side {premises['B']} with B(1 + D/(1 - D^2/4)) < 1 and the net of 201 "
        f"half-angles of step {premises['D']}, from {premises['source_rectangles']} "
        f"rectangle rows ({premises['expanded_rectangles']:,} distinct images) and no point "
        "or segment, and took format M's per-bin centre domain, at threshold 1. The axis "
        f"direction was decided by an exact-event vertex sweep over {axis['vertices']:,} "
        f"vertices, least certified capture {axis['min_certified_lower_bound']!r}; the other "
        f"200 by interval branch and bound over {entry['nodes']:,} boxes, least certified "
        f"lower bound {oblique['min_certified_lower_bound']!r} at index {oblique['r']}; "
        f"the exact capture at the least-bound leaf's centre (index {least['r']}) is "
        f"{float(Fraction(least['exact_coverage'])):.10f}. Every direction verified, "
        f"summary VERIFIED, exit 0, {float(entry['cpu_seconds']):,.0f} CPU seconds at two "
        f"threads and {float(entry['wall_seconds']):,.0f} seconds of wall time on a shared "
        "4-core x86-64 Linux container under load. The build is rustc 1.98.0, release, "
        f"x86-64 Linux, source_sha256 {built[:8]}...; its src/, Cargo.lock and build.rs are "
        f"unchanged since {REVIEWED_BUILD}, the build the two reviews of 3 October accepted, "
        f"and the digest differs from that build's {REVIEWED_SOURCE[:8]}... only because "
        "Cargo.toml gained the gate's test profile, which the release binary does not use. "
        "It decides coverage independently of the source's checker: the crate was written "
        "without opening it (packing/sqverify_fast/INDEPENDENCE.md) and shares no code with "
        "it. It shares the theorem, the net, the core side, the per-bin domain lemma and the "
        "threshold, so a defect in that mathematics would affect both: a second "
        "implementation, not a second method. Its node counts and bounds are its own, not "
        "the certificate's records. Controls at index "
        f"{receipt['index']}: the original verified again, every mass scaled by 99/100 "
        f"refused ({runs['scaled-99-100']['verdict']}, {uncovered(runs['scaled-99-100'])}), "
        "and every mass scaled so that the exact capture at the least-bound leaf's centre is "
        f"at most 1 - 10^-6 refused ({runs['near-threshold']['verdict']}, "
        f"{uncovered(runs['near-threshold'])}); each capture below 1 was evaluated "
        "again by an exact evaluator written apart from the crate, and "
        "tests/test_sqverify_fast_census.py holds the receipts. The source's own checker "
        "was not run here on this certificate, and its tarball is pinned by digest and not "
        "retained."
    )
    scope = ", ".join(str(n) for n in report["scope"]["n_values"])
    lines = [
        f"  - id: {identifier}",
        "    claim: lower-bound",
        f"    scope: {{n_values: [{scope}]}}",
        "    assurance: verified",
        "    method: interval-certified",
        "    performed_by: repository",
        "    relationship_to_generator: independent-implementation",
        "    origin: replayed-here",
        "    novelty: previously-published",
        f"    source_key: '{report['source_key']}'",
        f"    certificate: {certificate}",
        *folded("replay", replay),
        "    replay_status: passed",
        "    verifiers: [V-sqverify-fast]",
        "    proof:",
        "      source: packing/sqverify_fast/SOUNDNESS.md",
        *folded(
            "theorem",
            "The net-and-shrink measure-capture obstruction of SOUNDNESS.md (The Claim; "
            "Formats M and L, lemma D for format M's per-bin domain), applied to wand125's "
            f"{case.certificate}: no {case.n} unit squares pack in a square of side {side}, "
            f"so s({case.n}) >= {side}.",
            indent=6,
        ),
        (
            "      scope: Unrestricted square packing with disjoint interiors and arbitrary"
            " rotations."
        ),
        *folded(
            "pinpoints",
            "SOUNDNESS.md's theorem and lemmas, accepted with the crate by "
            "docs/project/reviews/review-2026-10-03-sqverify-fast-soundness.md; the "
            f"certificate's mathematics read in {audit_record}; "
            + (
                ""
                if audit_record == ROUTE_REVIEW
                else f"the census route accepted as a complete replay here in {ROUTE_REVIEW}; "
            )
            + "the census row, receipts and control receipt named in replay.",
            indent=6,
        ),
        "      assumptions:",
        (
            f"        - The density is nonnegative and exact, of total mass {mass} < {case.n},"
            " which admission recomputes from the retained candidate."
        ),
        *(f"        - {assumption}" for assumption in ASSUMPTIONS),
        f"      audit_record: {audit_record}",
        *folded("limitations", limitations),
        f"    source_reviewed: '{date}'",
    ]
    return "\n".join(lines) + "\n"


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
        folder = WEB / f"wand125-rectangle-certificates-{packet}/receipts/replay"
        for name in ("audit.json", "audit.json.gz"):
            receipt = folder / name
            if not receipt.is_file():
                continue
            raw = receipt.read_bytes()
            text = gzip.decompress(raw) if name.endswith(".gz") else raw
            for case in json.loads(text)["cases"]:
                replay = case.get("replay")
                if isinstance(replay, dict) and (
                    (replay.get("summary") or {}).get("status") == "VERIFIED"
                ):
                    reference[case["certificate"]] = replay
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
        "Every retained rectangle-density certificate (format T), verified by",
        "`sqverify-fast` at all 201 net directions at the threshold",
        f"{census['threshold']}. *Authors' replay here* says whether this repository holds a",
        "complete replay by the authors' checker; where it holds none, this census is the",
        "first complete check here. *Nodes* counts boxes at $r \\ge 1$; the authors' count",
        "also includes the axis direction's vertices, given here as *axis vertices*.",
        "*Exact leaf* is the exact rational capture at the centre of the least-bound leaf",
        "of the least-bound direction, which must clear the threshold. CPU is user plus system",
        "time of the whole process (`wait4`), on a shared host whose load average is given.",
        "The replay wall is the authors' checker's recorded wall time with the worker count",
        "it ran with, so it is not a CPU figure.",
        "",
        (
            "| Certificate | n | Status | Directions | Nodes | Axis vertices | Authors' nodes"
            " | Least certified bound | Exact leaf | CPU s | Load | Authors' replay here"
            " | Authors' replay wall s (workers) |"
        ),
        "|" + "|".join(f" {align} " for align in RECT_ALIGN.split()) + "|",
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
            f"{int(summary.get('nodes', 0)):,}" if summary else "-",
            str(case.get("least_certified_bound")),
            "clears" if least.get("clears_threshold") else "FAILS",
            f"{cpu:.1f}",
            f"{float(case.get('load_before') or 0.0):.1f}",
            "complete" if summary else "none: first complete check here",
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


RECT_ALIGN = "--- ---: --- ---: ---: ---: ---: --- --- ---: ---: --- ---:"
MIXED_ALIGN = "--- ---: --- --- ---: ---: --- --- ---: ---: --- ---: ---: ---: ---"


def render_mixed_report(census: dict[str, Any], out: Path) -> str:
    """The mixed census as a Markdown table, beside the authors' replays."""
    cases = {case.certificate: case for case in mixed_cases()}
    lines = [
        "# Milestone B Census",
        "",
        "Generated by `python -m devtools.sqverify_fast_census --family mixed --report`;",
        "do not edit by hand.",
        "",
        "Every retained certificate of formats M (rectangle rows, per-bin centre domain) and L",
        "(points, segments and rectangles, Tokoharu's domain), verified by `sqverify-fast` at",
        "every direction of its net (201, unless the file declares its own) at the threshold",
        "the certificate declares, 1. *Replayed directions* are those the authors' checker",
        "replayed in this repository; where there are none, this census is the first",
        "complete check here. *Exact leaf* is the exact rational capture at the centre of",
        "the least-bound leaf of the least-bound direction.",
        "*Authors' CPU* is the authors' checker's recorded CPU seconds on the directions this",
        "repository replayed; *ours, same directions* is `sqverify-fast`'s thread CPU on",
        "exactly those directions. CPU on a shared host whose load average is given.",
        "*Control* is the status of the `--control` receipt on the certificate itself, where",
        "one is kept: the original verified at its least-bound direction and two mutants",
        "refused there.",
        "",
        (
            "| Certificate | n | Format | Status | Directions | Nodes | Least certified bound"
            " | Exact leaf | CPU s, all directions | Load | Replayed directions"
            " | Authors' CPU s | Ours, same directions | Ratio | Control |"
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
        span = (
            f"all {len(replayed)}"
            if case is not None and len(replayed) == net_directions(case)
            else ", ".join(str(r) for r in replayed) or "none: first complete check here"
        )
        if not reference.get("per_direction_cpu", True):
            ours = 0.0
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
            f"{authors:,.0f}" if authors > 0 else "-",
            f"{ours:.1f}" if ours > 0 else "-",
            f"{authors / ours:,.0f}x" if ours > 0 and authors > 0 else "-",
            (control_status(case, out) or "-") if case is not None else "-",
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


def summary_rows() -> list[dict[str, Any]]:
    """One row per certificate of both censuses, for records and the summary table."""
    rows: list[dict[str, Any]] = []
    rectangles = json.loads((CENSUS_ROOT / "census/census.json").read_text(encoding="utf-8"))
    mixed = json.loads((CENSUS_ROOT / "census-mixed/census.json").read_text(encoding="utf-8"))
    reference = replay_reference()
    families = (
        ("census", rectangles, {case.certificate: case for case in rectangle_cases()}),
        ("census-mixed", mixed, {case.certificate: case for case in mixed_cases()}),
    )
    for folder, census, cases in families:
        for name, entry in census["cases"].items():
            case = cases.get(name)
            if folder == "census":
                replay = "complete" if name in reference else "none"
                source = (
                    "tokoharu-density"
                    if entry.get("packet") == TOKOHARU_PACKET
                    else f"wand125-rectangle-certificates-{entry.get('packet')}"
                )
            else:
                replayed = mixed_reference(case)["directions"] if case is not None else []
                replay = (
                    replay_status(len(replayed), net_directions(case))
                    if case is not None
                    else "none"
                )
                source = str(entry.get("packet"))
            least = entry.get("least_bound_leaf_exact") or {}
            verified = (
                entry.get("status") == "VERIFIED"
                and entry.get("returncode") == 0
                and least.get("clears_threshold") is True
            )
            rows.append(
                {
                    "certificate": name,
                    "packet": source,
                    "candidate": str(case.candidate.relative_to(PROJECT.parent))
                    if case is not None
                    else None,
                    "format": (entry.get("premises") or {}).get("format", "T"),
                    "n": entry.get("n"),
                    "L": entry.get("L"),
                    "verdict": "VERIFIED" if verified else str(entry.get("status")),
                    "directions_verified": entry.get("directions_verified"),
                    "threshold": entry.get("threshold") or census.get("threshold"),
                    "least_certified_bound": entry.get("least_certified_bound"),
                    "least_leaf_exact_clears": least.get("clears_threshold") is True,
                    "cpu_seconds": round(float(entry.get("cpu_seconds") or 0.0), 1),
                    "nodes": entry.get("nodes"),
                    "authors_replay_here": replay,
                    "first_complete_check_here": verified and replay != "complete",
                    "receipts": (
                        f"packing/benchmarks/measure-verifier/{folder}/"
                        f"{entry.get('packet')}/{name}.jsonl.gz"
                    ),
                    "candidate_sha256": entry.get("candidate_sha256"),
                    "binary_sha256": entry.get("binary_sha256"),
                    "source_sha256": (entry.get("build") or {}).get("source_sha256"),
                }
            )
    rows.sort(key=lambda row: (int(row["n"] or 0), str(row["certificate"])))
    return rows


def render_summary(rows: list[dict[str, Any]]) -> str:
    """The census summary as a Markdown table."""
    verified = sum(row["verdict"] == "VERIFIED" for row in rows)
    first = sum(bool(row["first_complete_check_here"]) for row in rows)
    lines = [
        "# Census Summary",
        "",
        "Generated by `python -m devtools.sqverify_fast_census --summary`; do not edit by",
        "hand. The same rows, with receipt paths and digests, are in `census-summary.json`.",
        "",
        "Every retained certificate that `sqverify-fast` decides (formats T, M and L), from",
        "the two census folders: [census/](census/README.md) and",
        "[census-mixed/](census-mixed/README.md). *Verdict* is `VERIFIED` only when every",
        "direction of its net verified, the process exited zero, and the exact capture at the",
        "least-bound leaf's centre cleared the threshold. *Authors' replay here* is what",
        "this repository holds of a replay by the authors' own checker; where it holds less",
        "than a complete replay, this census is the first complete check of the certificate",
        "here, which the last column says.",
        "",
        (
            "| Certificate | Format | n | L | Verdict | CPU s | Least certified bound"
            " | Authors' replay here | First complete check here |"
        ),
        "| --- | --- | ---: | --- | --- | ---: | --- | --- | --- |",
    ]
    for row in rows:
        cells = [
            f"`{row['certificate']}`",
            str(row["format"]),
            str(row["n"]),
            str(row["L"]),
            str(row["verdict"]),
            f"{row['cpu_seconds']:.1f}",
            str(row["least_certified_bound"]),
            str(row["authors_replay_here"]),
            "yes" if row["first_complete_check_here"] else "no",
        ]
        lines.append("| " + " | ".join(cells) + " |")
    lines += [
        "",
        f"{verified} of {len(rows)} certificates verified; {first} of them are the first",
        "complete check of their certificate in this repository.",
        "",
        "<!-- This document follows common-doc-guidelines.md.",
        "See github.com/jlevy/practical-prose and review guidelines before editing.",
        "-->",
        "",
    ]
    return "\n".join(lines)


def census_delta(old: dict[str, Any], new: dict[str, Any]) -> list[str]:
    """Every difference in verdict, nodes or least certified bound between two runs."""
    fields = ("status", "nodes", "least_certified_bound", "directions_verified")
    return [
        f"{name}: {field} {old['cases'][name].get(field)} -> {new['cases'][name].get(field)}"
        for name in sorted(set(old["cases"]) & set(new["cases"]))
        for field in fields
        if old["cases"][name].get(field) != new["cases"][name].get(field)
    ]


def records_mode(args: argparse.Namespace, census: dict[str, Any], selected: list[Case]) -> int:
    """`--evidence` prints each selected case's entry; `--control` writes its receipt."""
    if args.evidence:
        if not (args.audit_record and args.date):
            raise SystemExit("--evidence needs --audit-record and --date")
        for case in selected:
            entry = census["cases"].get(case.certificate, {})
            text = evidence_entry(
                case, args.out, entry, audit_record=args.audit_record, date=args.date
            )
            sys.stdout.write(text)
        return 0
    failed = 0
    for case in selected:
        receipt = control(args.binary, case, census["cases"].get(case.certificate, {}))
        target = args.out / case.packet / f"{case.certificate}.control.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(retained_json.dumps(receipt, sort_keys=True))
        failed += receipt["status"] != "CONTROLS_REFUSED"
        verdicts = ", ".join(f"{run['name']} {run['verdict']}" for run in receipt["runs"])
        print(f"{case.certificate:18} {receipt['status']} r={receipt['index']}: {verdicts}")
    return 1 if failed else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    parser.add_argument("--family", choices=("rectangles", "mixed"), default="rectangles")
    parser.add_argument("--binary", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--threads", type=int, default=1)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument(
        "--same-build",
        action="store_true",
        help="with --resume, keep only cases this binary verified (a re-run after a fix)",
    )
    parser.add_argument("--check", action="store_true")
    parser.add_argument(
        "--control",
        action="store_true",
        help="mixed family: negative controls on each selected verified certificate",
    )
    parser.add_argument(
        "--evidence",
        action="store_true",
        help="mixed family: print each selected certificate's replay evidence entry",
    )
    parser.add_argument("--audit-record", help="with --evidence: the mapped review's path")
    parser.add_argument("--date", help="with --evidence: the day the replay ran")
    parser.add_argument(
        "--report", action="store_true", help="render --out/README.md from the census"
    )
    parser.add_argument("--only", default="", help="comma-separated certificate names")
    parser.add_argument(
        "--packets", default="", help="comma-separated packets (the folder under --out)"
    )
    parser.add_argument(
        "--delta",
        type=Path,
        help="an earlier census.json: print every case whose verdict, nodes or bound moved",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="write census-summary.json and census-summary.md from both census folders",
    )
    args = parser.parse_args(argv)
    if args.summary:
        rows = summary_rows()
        (CENSUS_ROOT / "census-summary.json").write_text(
            json.dumps(
                {"kind": "sqverify-fast-census-summary/v1", "certificates": rows},
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        (CENSUS_ROOT / "census-summary.md").write_text(render_summary(rows), encoding="utf-8")
        return 0
    census_path = args.out / "census.json"
    binary_sha = sha256(args.binary)
    census: dict[str, Any] = (
        json.loads(census_path.read_text(encoding="utf-8"))
        if census_path.is_file()
        else {"kind": "sqverify-fast-census/v1", "threshold": THRESHOLD, "cases": {}}
    )
    if args.delta is not None:
        old = json.loads(args.delta.read_text(encoding="utf-8"))
        changes = census_delta(old, census)
        common = len(set(old["cases"]) & set(census["cases"]))
        print(f"{common} cases in both runs; {len(changes)} differences")
        for line in changes:
            print(f"  {line}")
        return 1 if changes else 0
    mixed = args.family == "mixed"
    if mixed:
        census["family"] = "mixed"
        census["threshold"] = "declared"
    cases = mixed_cases() if mixed else rectangle_cases()
    only = {name for name in args.only.split(",") if name}
    packets = {name for name in args.packets.split(",") if name}
    selected = [
        case
        for case in cases
        if (not only or case.certificate in only) and (not packets or case.packet in packets)
    ]
    if args.report:
        text = render_mixed_report(census, args.out) if mixed else render_report(census)
        (args.out / "README.md").write_text(text, encoding="utf-8")
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
            for case in selected
            if not passed(census["cases"].get(case.certificate, {}))
        ]
        print(
            f"{len(selected) - len(missing)} of {len(selected)} retained certificates VERIFIED"
        )
        for name in missing:
            print(f"  not verified: {name}")
        return 1 if missing else 0
    if args.evidence or args.control:
        if not mixed:
            raise SystemExit("--evidence and --control are for the mixed family")
        return records_mode(args, census, selected)
    for case in selected:
        held = census["cases"].get(case.certificate)
        # A verified case is kept whichever build verified it: each case records its
        # own binary and source digests, so a census may span builds honestly.
        # --same-build keeps only this binary's, to re-run everything after a fix.
        if (
            args.resume
            and held is not None
            and held.get("status") == "VERIFIED"
            and (not args.same_build or held.get("binary_sha256") == binary_sha)
        ):
            continue
        result = run(args.binary, case, args.out / case.packet, args.threads)
        result["binary_sha256"] = binary_sha
        census["cases"][case.certificate] = result
        census_path.parent.mkdir(parents=True, exist_ok=True)
        census_path.write_text(retained_json.dumps(census, sort_keys=True))
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
