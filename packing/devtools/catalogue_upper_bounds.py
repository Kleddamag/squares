#!/usr/bin/env python3
"""Certify the catalogue's September 2026 packings at ``n = 69, 83, 87`` exactly.

The Kingbird catalogue's capture of 30 September 2026 prints three packings this record
registers as results by others: David Ellsworth's at ``n = 69`` (T-088) and Allen
Chang's at ``n = 83`` and ``87`` (T-089). Their poses are retained as Witness/v2 facts in
``witnesses/known-best/``, read from Evan Daniel's binary64 parse of the catalogue's
pictures (each witness names the parse in ``source.revision``), because the pictures
could not be fetched when they were taken in.

This tool certifies each of those witnesses with the promotion
`devtools.upper_bound_packets` runs for T-056 and T-057, unchanged: the retained decimal
pose rounded to rationals of 36 digits, dilated about the container's centre by the
first of ``1, 1 + 10^-31, 1 + 10^-29, ...`` that makes every pair and wall pass
``sqpack.witness``'s exact separating-axis test, with the side the extent of the result
and at most ``1e-9`` above the witness's. Each certificate is then decided again by
`devtools.check_rational_witness_independent`, which shares no geometry or verification
code with the promotion.

The subcommands, run from ``packing/``:

``certify [--n N ...]``
    Promote each witness, store the certificate as
    ``witnesses/kingbird-2026/n-NNN-rational.yaml``, decide it again with the independent
    checker, and write ``receipts/kingbird-2026-09-certification.json`` in the
    known-best packet. Two mutations of the ``n = 69`` certificate, each of which must be
    refused by both checkers, go to ``receipts/kingbird-2026-09-negative-controls.json``.

``check``
    Fast and offline: each receipt row against its committed certificate (side, the
    allowed increase, the verified value and exact form derived from it) and the
    recorded verdicts. This is what the tests run.

``check --replay [--n N ...]``
    The evidence replay: regenerate every certificate from its retained witness, require
    its text to equal the committed one, and decide the committed one again with the
    independent checker and with ``sqpack.witness.exact_verify``. About fifteen seconds.

What a certificate proves is ``s(n)`` at most its own side. That side lies above the side
the catalogue prints, by the rounding of a truncated decimal and by the dilation the
binary64 pose needs, so the verified value a case record carries is the receipt's
`verified_value`: the larger of the printed side and the certified side rounded up at the
printed precision, as `devtools.upper_bound_packets.derived` computes it. Where that is
more than one unit of the printed last place above the printed side, the printed side is
not certified here and the case record says so.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
import time
from collections.abc import Mapping, Sequence
from fractions import Fraction
from pathlib import Path
from typing import Any

from strif import atomic_write_text

from devtools import check_rational_witness_independent as independent
from devtools import upper_bound_packets as packets
from devtools.check_source_coverage import parse_kingbird
from sqpack.kingbird_catalogue import CATALOGUE_HTML
from sqpack.witness import exact_verify, load_witness, promote_rational, witness_document

ROOT = Path(__file__).resolve().parent.parent
WITNESSES = ROOT / "witnesses"
WITNESS_SCHEMA = WITNESSES / "witness.schema.yaml"
CERTIFICATES = WITNESSES / "kingbird-2026"
RECEIPTS = ROOT / "resources/web/known-best-packings/receipts"
CERTIFICATION = RECEIPTS / "kingbird-2026-09-certification.json"
CONTROLS = RECEIPTS / "kingbird-2026-09-negative-controls.json"
#: The capture the register entries transcribe; its printed sides are the receipts'.
CAPTURE = "2026-09-30"

#: The counts certified here, and the register entry each belongs to.
RESULTS: dict[int, str] = {69: "T-088", 83: "T-089", 87: "T-089"}
#: The certificate the negative controls mutate, and the square the second one moves:
#: square 1 sits against the left wall and touches square 2 on its right.
CONTROL_N = 69
CONTROL_SHIFT_SQUARE = 1


def witness_path(n: int) -> Path:
    return WITNESSES / "known-best" / f"n-{n:03d}.yaml"


def certificate_path(n: int) -> Path:
    return CERTIFICATES / f"n-{n:03d}-rational.yaml"


def _relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def printed_side(n: int) -> str:
    """The side the retained capture prints at ``n``."""
    return parse_kingbird(ROOT / CATALOGUE_HTML, n, n)[n]


def certificate_text(n: int) -> tuple[str, dict[str, Any], dict[str, Any]]:
    """Promote one retained witness: the certificate's text, the result and the witness."""
    witness = load_witness(witness_path(n), fallback_schema=WITNESS_SCHEMA)
    result, promoted = promote_rational(
        witness,
        rational_digits=packets.RATIONAL_DIGITS,
        max_side_increase=packets.MAX_SIDE_INCREASE,
        source_path=_relative(witness_path(n)),
        replay_path=_relative(certificate_path(n)),
    )
    return witness_document(promoted, schema="../witness.schema.yaml"), result, witness


def certificate_side(text: str) -> Fraction:
    """A certificate's exact side, read from its header line."""
    match = re.search(r"^  side: (\S+)$", text, flags=re.MULTILINE)
    if match is None:
        raise ValueError("certificate has no side line")
    return Fraction(match.group(1).strip("'"))


def exact_verify_passed(text: str) -> bool:
    """``sqpack.witness.exact_verify``'s verdict on a certificate's text."""
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "certificate.yaml"
        path.write_text(text, encoding="utf-8")
        _result, report = exact_verify(load_witness(path, fallback_schema=WITNESS_SCHEMA))
    return report.valid


def certify_one(n: int) -> dict[str, Any]:
    printed = printed_side(n)
    started = time.monotonic()
    text, result, witness = certificate_text(n)
    promote_seconds = time.monotonic() - started
    path = certificate_path(n)
    path.parent.mkdir(parents=True, exist_ok=True)
    atomic_write_text(path, text)
    started = time.monotonic()
    verdict = independent.check(path)
    independent_seconds = time.monotonic() - started
    side = certificate_side(text)
    revision = (witness.get("source") or {}).get("revision")
    return {
        "n": n,
        "result": RESULTS[n],
        "printed_side": printed,
        "capture": CAPTURE,
        "witness": _relative(witness_path(n)),
        "witness_side": witness["side"],
        "witness_revision": revision,
        "certificate": _relative(path),
        "certified_side": f"{side.numerator}/{side.denominator}",
        "certified_side_decimal": format(packets.ceiling_at(side, 40), "f"),
        "side_increase": f"{float(side - Fraction(printed)):.3e}",
        "side_increase_over_witness": f"{float(side - Fraction(witness['side'])):.3e}",
        "center_dilation": result["center_dilation"],
        "pairs_tested": result["pairs_tested"],
        "promotion": result["status"],
        "independent": {
            "verification_passed": verdict["verification_passed"],
            "pairs_tested": verdict["pairs_tested"],
            "minimum_containment_clearance": verdict["minimum_containment_clearance"],
            "minimum_best_pair_gap": verdict["minimum_best_pair_gap"],
            "failures": verdict["failures"],
        },
        **packets.derived(printed, side),
        "wall_seconds": {
            "promote": round(promote_seconds, 1),
            "independent": round(independent_seconds, 1),
        },
    }


def negative_controls() -> dict[str, Any]:
    """Two mutations of the committed ``n = 69`` certificate, each of which must fail."""
    text = certificate_path(CONTROL_N).read_text(encoding="utf-8")
    controls = {
        "side-shrunk-1e-15": packets.shrink_side(text),
        f"square-{CONTROL_SHIFT_SQUARE}-shifted-1e-6": packets.shift_square(
            text, CONTROL_SHIFT_SQUARE, Fraction(1, 10**6)
        ),
    }
    rows = []
    for name, mutated in controls.items():
        verdict = packets.independent_check(mutated)
        rows.append(
            {
                "control": name,
                "n": CONTROL_N,
                "independent_passed": verdict["verification_passed"],
                "independent_failures": [failure[:160] for failure in verdict["failures"]],
                "exact_verify_passed": exact_verify_passed(mutated),
            }
        )
    return {
        "tool": "python -m devtools.catalogue_upper_bounds certify",
        "certificate": _relative(certificate_path(CONTROL_N)),
        "expectation": "every control is refused by both checkers",
        "controls": rows,
    }


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    atomic_write_text(path, json.dumps(value, indent=2) + "\n")


def certification() -> dict[int, dict[str, Any]]:
    record = json.loads(CERTIFICATION.read_text(encoding="utf-8"))
    return {int(row["n"]): row for row in record["cases"]}


def certify(numbers: set[int] | None) -> None:
    chosen = sorted(n for n in RESULTS if numbers is None or n in numbers)
    rows = {n: certify_one(n) for n in chosen}
    previous = certification() if CERTIFICATION.is_file() else {}
    merged = {**previous, **rows}
    _write_json(
        CERTIFICATION,
        {
            "tool": "python -m devtools.catalogue_upper_bounds certify",
            "promotion": {
                "strategy": "robust-rational",
                "rational_digits": packets.RATIONAL_DIGITS,
                "max_side_increase": packets.MAX_SIDE_INCREASE,
            },
            "independent_checker": "devtools.check_rational_witness_independent",
            "cases": [merged[n] for n in sorted(merged)],
        },
    )
    print(f"certified {chosen}")
    if CONTROL_N in rows:
        _write_json(CONTROLS, negative_controls())
        print("negative controls written")


# --------------------------------------------------------------------------------------
# Checks
# --------------------------------------------------------------------------------------


def _row_problems(n: int, row: Mapping[str, Any]) -> list[str]:
    path = certificate_path(n)
    if not path.is_file():
        return ["certificate missing"]
    text = path.read_text(encoding="utf-8")
    side = certificate_side(text)
    problems = []
    if row["result"] != RESULTS[n] or row["certificate"] != _relative(path):
        problems.append("receipt names another result or certificate")
    if f"{side.numerator}/{side.denominator}" != row["certified_side"]:
        problems.append("certified side differs from its receipt")
    if side - Fraction(row["witness_side"]) > Fraction(packets.MAX_SIDE_INCREASE):
        problems.append("certified side exceeds the allowed increase")
    derived = packets.derived(row["printed_side"], side)
    if {key: row.get(key) for key in derived} != derived:
        problems.append("receipt's verified value or units above do not follow from it")
    if not row["independent"]["verification_passed"] or row["promotion"] != (
        "certificate-produced"
    ):
        problems.append("a checker refused the certificate")
    return problems


def fast_problems() -> list[str]:
    """What is wrong with the certificates and receipts, from the retained files alone."""
    if not CERTIFICATION.is_file():
        return ["no certification receipt"]
    receipts = certification()
    problems = []
    if set(receipts) != set(RESULTS):
        problems.append(f"receipts cover {sorted(receipts)}, not {sorted(RESULTS)}")
    for n, row in sorted(receipts.items()):
        problems.extend(f"n={n}: {problem}" for problem in _row_problems(n, row))
    controls = json.loads(CONTROLS.read_text(encoding="utf-8"))["controls"]
    if len(controls) < 2 or any(
        row["independent_passed"] or row["exact_verify_passed"] for row in controls
    ):
        problems.append("a negative control was accepted")
    return problems


def replay_one(n: int) -> dict[str, Any]:
    """Regenerate one certificate and decide the committed one again, twice."""
    committed = certificate_path(n).read_text(encoding="utf-8")
    started = time.monotonic()
    regenerated, _result, _witness = certificate_text(n)
    verdict = independent.check(certificate_path(n))
    return {
        "n": n,
        "regenerated_identical": regenerated == committed,
        "independent_passed": verdict["verification_passed"],
        "exact_verify_passed": exact_verify_passed(committed),
        "seconds": round(time.monotonic() - started, 1),
    }


def replay(numbers: set[int] | None) -> list[str]:
    problems = []
    for n in sorted(n for n in RESULTS if numbers is None or n in numbers):
        row = replay_one(n)
        passed = (
            row["regenerated_identical"]
            and row["independent_passed"]
            and row["exact_verify_passed"]
        )
        print(
            f"  n={n}: "
            + ("VERIFIED" if passed else "FAILED")
            + f" (regenerated identical: {row['regenerated_identical']}, independent: "
            f"{row['independent_passed']}, exact_verify: {row['exact_verify_passed']}, "
            f"{row['seconds']} s)",
            flush=True,
        )
        if not passed:
            problems.append(f"n={n}: replay failed")
    return problems


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name, text in (("certify", "write certificates and receipts"), ("check", "check")):
        command = commands.add_parser(name, help=text)
        command.add_argument("--n", type=int, action="append", choices=sorted(RESULTS))
    commands.choices["check"].add_argument(
        "--replay", action="store_true", help="regenerate and re-decide every certificate"
    )
    args = parser.parse_args(argv)
    numbers = set(args.n) if args.n else None
    if args.command == "certify":
        certify(numbers)
        return 0
    problems = fast_problems()
    if args.replay and not problems:
        problems = replay(numbers)
    for problem in problems:
        print(f"FAIL {problem}", file=sys.stderr)
    if problems:
        return 1
    what = "replayed from the retained witnesses" if args.replay else "checked"
    print(f"catalogue upper bounds: {len(RESULTS)} certificates {what}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
