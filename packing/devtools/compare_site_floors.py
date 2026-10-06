"""Compare a published table of proven floors with the case records' lower bounds.

Evan Daniel's Square Packing Atlas publishes, for every n up to 100, the best proven
floor it knows (``site/data/lower_bounds.json``, served as
``site/www/data/lower_bounds.json``), and marks some floors ``register: verified``: the
2026 results it takes as verified by this record. Its overview then draws those counts
as settled. This command reads a retained copy of that table beside the case records
and reports, for each n, how the table's floor stands to the record's verified and
reported lower bounds, and whether each ``verified`` mark names a value the verified
lane holds.

It decides nothing about any floor. A floor the table holds above the verified lane is
a claim this record has not replayed, or one it has not taken in at all, and which of
the two is read from the evidence, not from here.

Values are compared exactly where both sides write a rational (``939/200``, ``8``), and
otherwise as numbers to `TOLERANCE`, since the table stores each value as a double and
the records as a decimal string.

The overview also rings every count past the table that one of the families
``s(k^2 - c) = k`` covers, from a smallest ``k`` it names per ``c``
(``site/www/js/overview.js``, ``FAMILIES``). ``--families c:k0,...`` checks those
counts the same way, up to the case corpus's largest n: each must have ``k`` as its
verified lower bound.

Usage, from ``packing/``::

    uv run --frozen --all-extras --group dev python -m devtools.compare_site_floors \\
        TABLE [--families 1:3,2:2,3:6] [--json OUT]

``TABLE`` may be a retained ``.json.gz``; it is read by its upstream name or its stored
one. ``--json`` writes the comparison as a receipt in the layout of
`sqpack.retained_json`.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from fractions import Fraction
from pathlib import Path
from typing import cast

from strif import atomic_output_file

from devtools.audit_kingbird_catalogue import load_frontier_cases
from devtools.retained_data import GZIP_SUFFIX, read_retained_bytes
from sqpack import retained_json

ROOT = Path(__file__).resolve().parent.parent
FRONTIER = ROOT / "frontier"
REPO = ROOT.parent

#: Two values that are not both rational agree when they differ by less than this.
TOLERANCE = Decimal("1e-9")

_RATIONAL = re.compile(r"\s*(\d+)\s*(?:/\s*(\d+))?\s*")

# How the table's floor stands to one lane of the record.
SAME = "same"
ABOVE = "above"
BELOW = "below"
ABSENT = "no-bound"


@dataclass(frozen=True)
class Bound:
    """One lower bound: its value, and its exact form where one is written."""

    value: Decimal
    exact_form: str | None

    def rational(self) -> Fraction | None:
        if self.exact_form is None:
            return None
        match = _RATIONAL.fullmatch(self.exact_form)
        if match is None:
            return None
        numerator, denominator = match.groups()
        return Fraction(int(numerator), int(denominator or 1))

    def as_json(self) -> dict[str, str | None]:
        return {"value": str(self.value), "exact_form": self.exact_form}


def relation(table: Bound, record: Bound | None) -> str:
    """Whether the table's floor is the record's, above it or below it."""
    if record is None:
        return ABSENT
    left, right = table.rational(), record.rational()
    if left is not None and right is not None:
        if left == right:
            return SAME
        return ABOVE if left > right else BELOW
    difference = table.value - record.value
    if abs(difference) < TOLERANCE:
        return SAME
    return ABOVE if difference > 0 else BELOW


def _decimal(value: object) -> Decimal | None:
    if isinstance(value, bool) or not isinstance(value, int | float | str):
        return None
    try:
        return Decimal(str(value))
    except InvalidOperation:
        return None


def _bound(field: object) -> Bound | None:
    if not isinstance(field, Mapping):
        return None
    payload = cast("Mapping[str, object]", field)
    value = _decimal(payload.get("value"))
    if value is None:
        return None
    exact = payload.get("exact_form")
    return Bound(value, exact if isinstance(exact, str) and exact else None)


def read_table(path: Path) -> tuple[dict[str, object], str]:
    """The table and the SHA-256 of its upstream bytes."""
    upstream = path.with_name(path.name.removesuffix(GZIP_SUFFIX))
    data = read_retained_bytes(upstream)
    document: object = json.loads(data)
    if not isinstance(document, dict):
        raise TypeError(f"{path}: the table is not a JSON object")
    return cast("dict[str, object]", document), hashlib.sha256(data).hexdigest()


def compare(
    table: Mapping[str, object], cases: Mapping[int, Mapping[str, object]]
) -> list[dict[str, object]]:
    """One row for each n the table gives a floor for, in order of n."""
    rows: list[dict[str, object]] = []
    for key in sorted((key for key in table if key.isdigit()), key=int):
        entry = table[key]
        best = (
            cast("Mapping[str, object]", entry).get("best")
            if isinstance(entry, Mapping)
            else None
        )
        floor = _bound(best)
        if floor is None:
            continue
        payload = cast("Mapping[str, object]", best)
        n = int(key)
        case = cases.get(n, {})
        verified = _bound(case.get("verified_lower_bound"))
        reported = _bound(case.get("reported_lower_bound"))
        to_verified = relation(floor, verified)
        marked = payload.get("register") == "verified"
        rows.append(
            {
                "n": n,
                "table": {
                    **floor.as_json(),
                    "source": payload.get("source"),
                    "status": payload.get("status"),
                    "register": payload.get("register"),
                    "date": payload.get("date"),
                },
                "verified": verified.as_json() if verified else None,
                "reported": reported.as_json() if reported else None,
                "to_verified": to_verified,
                "to_reported": relation(floor, reported),
                "mark_held": (to_verified == SAME) if marked else None,
            }
        )
    return rows


def summary(rows: Sequence[Mapping[str, object]]) -> dict[str, object]:
    """Counts of each relation, and the counts whose rows a reader should look at."""
    lanes = Counter(f"{row['to_verified']}/{row['to_reported']}" for row in rows)
    return {
        "counts": len(rows),
        "verified_reported": dict(sorted(lanes.items())),
        "marked_verified": sum(row["mark_held"] is not None for row in rows),
        "mark_not_held": [row["n"] for row in rows if row["mark_held"] is False],
        "above_verified": [row["n"] for row in rows if row["to_verified"] == ABOVE],
        "above_both_lanes": [
            row["n"]
            for row in rows
            if row["to_verified"] == ABOVE and row["to_reported"] in (ABOVE, ABSENT)
        ],
        "below_verified": [row["n"] for row in rows if row["to_verified"] == BELOW],
    }


def parse_families(text: str) -> dict[int, int]:
    """``"1:3,2:2"`` as the deficit ``c`` and the smallest ``k`` the overview rings from."""
    families: dict[int, int] = {}
    for item in text.split(","):
        deficit, _, smallest = item.partition(":")
        families[int(deficit)] = int(smallest)
    return families


def family_rows(
    families: Mapping[int, int], cases: Mapping[int, Mapping[str, object]], above: int
) -> list[dict[str, object]]:
    """Each count past ``above`` that a ringed family covers, with its verified floor.

    A count is held when its verified lower bound is exactly the family's ``k``.
    """
    rows: list[dict[str, object]] = []
    largest = max(cases, default=0)
    for deficit, smallest in sorted(families.items()):
        k = smallest
        while k * k - deficit <= largest:
            n = k * k - deficit
            if n > above:
                verified = _bound(cases.get(n, {}).get("verified_lower_bound"))
                rows.append(
                    {
                        "n": n,
                        "c": deficit,
                        "k": k,
                        "verified": verified.as_json() if verified else None,
                        "held": relation(Bound(Decimal(k), str(k)), verified) == SAME,
                    }
                )
            k += 1
    return rows


def report(
    path: Path,
    cases: Mapping[int, Mapping[str, object]],
    families: Mapping[int, int] | None = None,
) -> dict[str, object]:
    table, digest = read_table(path)
    rows = compare(table, cases)
    largest = max((row["n"] for row in rows if isinstance(row["n"], int)), default=0)
    ringed = family_rows(families, cases, largest) if families else []
    try:
        shown = path.resolve().relative_to(REPO).as_posix()
    except ValueError:
        shown = path.as_posix()
    return {
        "format": "site-floor-comparison-v1",
        "table": shown,
        "table_sha256": digest,
        "tolerance": str(TOLERANCE),
        "summary": summary(rows),
        "families": {str(c): k for c, k in sorted((families or {}).items())},
        "family_counts_not_held": [row["n"] for row in ringed if not row["held"]],
        "rows": rows,
        "family_rows": ringed,
    }


def _text(result: Mapping[str, object]) -> str:
    totals = cast("dict[str, object]", result["summary"])
    digest = str(result["table_sha256"])[:12]
    ringed = len(cast("list[object]", result["family_rows"]))
    lines = [
        f"{result['table']} (sha256 {digest}...): {totals['counts']} floors",
        f"  verified/reported lane relations: {totals['verified_reported']}",
        f"  marked verified: {totals['marked_verified']}",
        f"  mark not held: {totals['mark_not_held']}",
        f"  above the verified lane: {totals['above_verified']}",
        f"  above both lanes: {totals['above_both_lanes']}",
        f"  below the verified lane: {totals['below_verified']}",
        f"  family rings {result['families']}: {ringed} counts past the table",
        f"  family counts not held: {result['family_counts_not_held']}",
    ]
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("table", type=Path, help="the table, lower_bounds.json or .json.gz")
    parser.add_argument("--families", help="the overview's ringed families, as c:k0,c:k0")
    parser.add_argument("--json", type=Path, help="write the comparison here")
    args = parser.parse_args(argv)
    families = parse_families(cast("str", args.families)) if args.families else None
    result = report(cast("Path", args.table), load_frontier_cases(FRONTIER), families)
    if args.json is not None:
        # Atomically: the path is usually a receipt a packet retains, and a write cut off
        # part way would leave neither the old receipt nor the new one.
        with atomic_output_file(cast("Path", args.json)) as temporary:
            temporary.write_text(
                retained_json.dumps(result, ensure_ascii=False), encoding="utf-8"
            )
    sys.stdout.write(_text(result) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
