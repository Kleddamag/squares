"""Decide evand's angle-net certificates by the native parent-core interval route.

evand/square-packing proves ``s(12) >= 15680/3951`` and ``s(21) >= 5000/1001`` with
weighted closed covers checked by its own Rust arrangement sweep, ``verify/``, over the
net ``theta_k = 2 arctan(k/N)``, ``N = 6000``. For bin ``k`` it tests the concentric
square of side ``sigma_k``, ``1/(cos d + sin d)`` for the bin's gap ``d`` rounded down
to a multiple of ``10^-6``, at ``theta_k``, over the centres where a unit square at some
angle of the bin fits. That is, row for row, this repository's adaptive parent-core
theorem (`sqpack.fractional.parent_core`) with parent side ``A = 1``: the row
``[k/N, (k+1)/N]`` of parent half-tangents, core half-tangent ``k/N`` and core side
``sigma_k``, minimum charge ``1``, and the point atoms as the source lists them.

So this reader builds that `ParentCoreCertificate` from the source's integer text file
(stored in the packet as deterministic gzip and read back as the upstream bytes by
`devtools.retained_data.read_retained_bytes`), without importing any source code, and
hands it to two separately reviewed pieces: `validate_parent_core`, which discharges the
exact premises (D4 invariance of the weighted points, the strict counting gap
``weight < n``, a contiguous half-tangent cover reaching ``tan(pi/8)``, and strict
containment of each core in every parent of its row), and `verify_parent_core_rows`, the
directed-rounding branch and bound over centre boxes that decides coverage. The coverage
decision shares nothing with the source's arrangement sweep, which is what makes a
complete pass a method-distinct confirmation.

The native theorem proves the strict ``s(n) > L``; the claim recorded is the source's
``s(n) >= L``.

Usage (from ``packing/``)::

    uv run --frozen --all-extras --group dev python -m devtools.verify_evand_angle_net_native \\
        --case s12 --pilot --output OUT.json
    ... --case s12 --all --workers 2 --output OUT.json

``--all`` writes an append-only row journal beside the receipt (``OUT.rows.jsonl``), and
``--resume JOURNAL`` skips the rows a previous journal of the same case and settings
already certified; a resumed receipt still requires every row certified before it says
``PASS_COMPLETE``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any, TextIO

from strif import atomic_output_file

from devtools.retained_data import read_retained_bytes
from sqpack.fractional.model import Atom
from sqpack.fractional.parent_core import (
    ParentCoreCertificate,
    ParentCoreRow,
    validate_parent_core,
)
from sqpack.fractional.parent_core_interval import verify_parent_core_rows

REPO = Path(__file__).resolve().parents[2]
PACKET = REPO / "packing/resources/web/evand-square-packing-2026-09-26/square-packing/s12"
SOURCE_URL = "https://github.com/evand/square-packing"
SOURCE_COMMIT = "167d842cd27ba1451cb2833773ea930c80b9e65b"
#: The source's net and its sigma rounding, as `verify/src/main.rs` `bin_geometry` has them.
NET = 6000
SIGMA_SCALE = 1_000_000
MAX_BYTES = 4 * 1024 * 1024


@dataclass(frozen=True, slots=True)
class Case:
    n: int
    path: Path
    sha256: str
    #: The source's recorded least captured weight and bin at N = 6000.
    source_minimum: str
    source_bin: int


CASES = {
    "s12": Case(
        12,
        PACKET / "certificates/s12_lower_3.9686.txt",
        "75f1cc891a8b8739b92b50c7ddbd85a493efa58cf2e921d58ce4ac7c2dcabe78",
        "10000056/10000000",
        0,
    ),
    "s21": Case(
        21,
        PACKET / "certificates/s21/s21_lower_4.9950.txt",
        "c8e8f878205f2da9c213e4a87c06f17c5a759dce7e695e676dd5c50e0994f2ef",
        "10000083/10000000",
        684,
    ),
}


def _require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def read_source(path: Path, expected_sha256: str | None) -> tuple[bytes, list[int]]:
    """The reviewed bytes and their integers, refusing anything else."""
    data = read_retained_bytes(path)
    _require(len(data) <= MAX_BYTES, "certificate file exceeds 4 MiB")
    if expected_sha256 is not None:
        _require(
            hashlib.sha256(data).hexdigest() == expected_sha256,
            "certificate bytes differ from the reviewed evand release",
        )
    tokens = data.split()
    _require(
        all(t.isdigit() for t in tokens), "the text format holds nonnegative integers only"
    )
    return data, [int(t) for t in tokens]


def sigma(k: int, net: int = NET) -> Fraction:
    """``1/(cos d + sin d)`` for bin ``k``'s gap, rounded down to ``1/SIGMA_SCALE``."""
    c0, s0, g0 = net * net - k * k, 2 * k * net, net * net + k * k
    k1 = k + 1
    c1, s1, g1 = net * net - k1 * k1, 2 * k1 * net, net * net + k1 * k1
    cd, sd = c0 * c1 + s0 * s1, c0 * s1 - s0 * c1
    return Fraction((g0 * g1 * SIGMA_SCALE) // (cd + sd), SIGMA_SCALE)


def net_rows(net: int = NET) -> tuple[ParentCoreRow, ...]:
    """The bins ``[k/N, (k+1)/N]`` up to the first right end reaching ``tan(pi/8)``."""
    rows: list[ParentCoreRow] = []
    k = 0
    while True:
        right = Fraction(k + 1, net)
        rows.append(ParentCoreRow(Fraction(k, net), right, Fraction(k, net), sigma(k, net)))
        if right * right + 2 * right >= 1:
            return tuple(rows)
        k += 1


def parse_certificate(n: int, values: list[int]) -> ParentCoreCertificate:
    """Build the native certificate from the source's ``s_num s_den D W m (X Y w)^m``."""
    _require(len(values) >= 5, "truncated header")
    s_num, s_den, denominator, weight_scale, count = values[:5]
    _require(min(s_num, s_den, denominator, weight_scale, count) > 0, "nonpositive header")
    _require(len(values) == 5 + 3 * count, "point count does not match the file")
    side = Fraction(s_num, s_den)
    _require((side * denominator).denominator == 1, "container is off the coordinate grid")
    atoms: list[Atom] = []
    for index in range(count):
        x, y, w = values[5 + 3 * index : 8 + 3 * index]
        point = Fraction(x, denominator), Fraction(y, denominator)
        _require(point[0] <= side and point[1] <= side, f"point {index} outside the container")
        if w:
            atoms.append(Atom(str(index), *point, Fraction(w, weight_scale)))
    return ParentCoreCertificate(
        n, side, Fraction(1), Fraction(1), tuple(atoms), (), net_rows()
    )


def load_case(name: str) -> tuple[Case, ParentCoreCertificate]:
    case = CASES[name]
    _, values = read_source(case.path, case.sha256)
    return case, parse_certificate(case.n, values)


def _git(*arguments: str) -> str:
    return subprocess.run(
        ["git", *arguments], cwd=REPO, check=True, capture_output=True, text=True
    ).stdout.strip()


def journal_certified(path: Path, name: str, batch_size: int) -> dict[int, dict[str, Any]]:
    """Rows a previous journal of this case and batch size recorded as certified."""
    lines = path.read_text(encoding="utf-8").splitlines()
    _require(bool(lines), "empty journal")
    head = json.loads(lines[0])
    _require(
        head.get("schema") == "EvandNativeRowJournal/v1"
        and head.get("case") == name
        and head.get("batch_size") == batch_size
        and head.get("certificate_sha256") == CASES[name].sha256,
        "journal is for another case, certificate or batch size",
    )
    certified: dict[int, dict[str, Any]] = {}
    for line in lines[1:]:
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue  # a torn last line from an interrupted run: that row is redone
        if row.get("status") == "certified" and not row.get("stalled"):
            certified[int(row["index"])] = row
    return certified


def run(
    name: str,
    rows: tuple[int, ...] | None,
    *,
    batch_size: int,
    workers: int,
    journal: TextIO | None,
    resumed: dict[int, dict[str, Any]],
    source_state: tuple[str, bool],
) -> dict[str, Any]:
    started = time.monotonic()
    case, certificate = load_case(name)
    premises = validate_parent_core(certificate)
    catalogue = len(certificate.rows)
    selected = tuple(range(catalogue)) if rows is None else rows
    todo = tuple(index for index in selected if index not in resumed)
    provenance = {
        "git_commit": source_state[0],
        "dirty": source_state[1],
        "python": sys.version,
        "platform": platform.platform(),
        "command": sys.argv,
        "source_url": SOURCE_URL,
        "source_commit": SOURCE_COMMIT,
        "certificate": str(case.path.relative_to(REPO)),
        "certificate_sha256": case.sha256,
    }
    if journal is not None:
        header = {
            "schema": "EvandNativeRowJournal/v1",
            "case": name,
            "batch_size": batch_size,
            "certificate_sha256": case.sha256,
            "provenance": provenance,
            "resumed_rows": len(resumed),
        }
        journal.write(json.dumps(header) + "\n")
        for index in sorted(set(selected) & set(resumed)):
            journal.write(json.dumps(dict(resumed[index], resumed=True)) + "\n")
        journal.flush()
    outcomes: dict[int, dict[str, Any]] = {
        index: resumed[index] for index in selected if index in resumed
    }

    def progress(index: int, outcome: Any, elapsed: float) -> None:
        record = dict(asdict(outcome), index=index, seconds=elapsed)
        outcomes[index] = record
        if journal is not None:
            journal.write(json.dumps(record, default=str) + "\n")
            journal.flush()
        if outcome.status != "certified" or outcome.stalled or index % 100 == 0:
            print(
                f"row {index}: {outcome.status}, {outcome.boxes} boxes, "
                f"{outcome.stalled} stalled, {elapsed:.2f}s",
                flush=True,
            )

    threshold_units = scale = None
    refutations: list[Any] = []
    if todo:
        verdict = verify_parent_core_rows(
            certificate, todo, batch_size=batch_size, workers=workers, progress=progress
        )
        threshold_units, scale = verdict.threshold_units, verdict.scale
        refutations = [asdict(witness) for witness in verdict.refutations]
    records = [outcomes[index] for index in selected]
    covered = all(
        r["status"] == "certified"
        and not r["budget_exhausted"]
        and r["stalled"] == 0
        and r["lower"] is not None
        and (threshold_units is None or int(r["lower"]) >= threshold_units)
        for r in records
    )
    complete = sorted(selected) == list(range(catalogue))
    least = (
        min(records, key=lambda r: -1 if r["lower"] is None else int(r["lower"]))
        if records
        else None
    )
    return {
        "schema": "EvandNativeParentCoreReceipt/v1",
        "status": "PASS_COMPLETE"
        if covered and complete and not refutations
        else "PASS_PARTIAL"
        if covered and not refutations
        else "UNRESOLVED",
        "method": "directed-rounding box branch-and-bound over parent-core rows",
        "case": name,
        "provenance": provenance,
        "claim": f"s({case.n}) >= {certificate.outer_side}",
        "native_bound": f"s({case.n}) > {certificate.outer_side / certificate.parent_side}",
        "net": NET,
        "sigma_scale": SIGMA_SCALE,
        "points": len(certificate.atoms),
        "budget": str(certificate.budget),
        "counting_gap": str(case.n * certificate.minimum_charge - certificate.budget),
        "premises": {
            "budget": str(premises.budget),
            "minimum_containment_numerator": str(premises.minimum_containment_numerator),
            "final_half_tangent": str(premises.final_half_tangent),
            "rows": premises.rows,
        },
        "catalogue_rows": catalogue,
        "selected_rows": len(selected),
        "resumed_rows": len(set(selected) & set(resumed)),
        "complete": complete,
        "batch_size": batch_size,
        "workers": workers,
        "scale": scale,
        "threshold_units": threshold_units,
        "boxes": sum(int(r["boxes"]) for r in records),
        "row_cpu_seconds": sum(float(r["seconds"]) for r in records),
        "least_lower": None
        if least is None
        else {"row": least["index"], "units": least["lower"]},
        "source_minimum": {"weight": case.source_minimum, "bin": case.source_bin},
        "refutations": refutations,
        "seconds": time.monotonic() - started,
        "rows": records if rows is not None and len(records) <= 64 else None,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", choices=sorted(CASES), required=True)
    select = parser.add_mutually_exclusive_group(required=True)
    select.add_argument("--rows", nargs="+", type=int)
    select.add_argument("--pilot", action="store_true", help="first, source-minimum, last row")
    select.add_argument("--premises", action="store_true", help="exact premises only")
    select.add_argument("--all", action="store_true")
    parser.add_argument("--batch-size", type=int, default=2048)
    parser.add_argument("--workers", type=int, choices=(1, 2), default=1)
    parser.add_argument("--resume", type=Path, help="a previous row journal of this case")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    source_state = _git("rev-parse", "HEAD"), bool(_git("status", "--porcelain"))
    if args.premises:
        case, certificate = load_case(args.case)
        premises = validate_parent_core(certificate)
        result: dict[str, Any] = {
            "schema": "EvandNativeParentCoreReceipt/v1",
            "status": "PREMISES_VERIFIED_COVERAGE_NOT_REQUESTED",
            "case": args.case,
            "certificate_sha256": case.sha256,
            "points": len(certificate.atoms),
            "premises": {k: str(v) for k, v in asdict(premises).items()},
        }
    else:
        case = CASES[args.case]
        rows: tuple[int, ...] | None
        if args.all:
            rows = None
        elif args.pilot:
            last = len(net_rows()) - 1
            rows = tuple(sorted({0, case.source_bin, last}))
        else:
            rows = tuple(args.rows)
        resumed = (
            journal_certified(args.resume, args.case, args.batch_size) if args.resume else {}
        )
        args.output.parent.mkdir(parents=True, exist_ok=True)
        journal_path = args.output.with_suffix(".rows.jsonl")
        with journal_path.open("x", encoding="utf-8") as journal:
            result = run(
                args.case,
                rows,
                batch_size=args.batch_size,
                workers=args.workers,
                journal=journal,
                resumed=resumed,
                source_state=source_state,
            )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with atomic_output_file(args.output) as handle:
        handle.write_text(json.dumps(result, indent=2, default=str) + "\n")
    print(f"{result['status']}: {args.output}")
    return 0 if result["status"] != "UNRESOLVED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
