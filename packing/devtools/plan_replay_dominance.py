"""Say which queued lower-bound replays would raise no verified lower bound.

A replay costs CPU; what it buys is a verified lower bound at its count. Since ``s(n)``
is nondecreasing in ``n``, a verified bound at ``m < n`` is also one at ``n``, so a
certificate at ``n`` whose bound does not exceed the best verified bound at any
``m <= n`` would raise nothing when it passes. This tool computes that, for a list of
queued certificates, against:

- the verified lower bound each case record carries now; and
- bounds the coordinator expects to verify first (``--assume N=VALUE``, an exact
  rational such as ``59=8``), for example an exact value whose cheap replay is already
  running. An assumed bound is a planning premise, and the report names every
  certificate whose skip rests on one, so the skip is revisited if that replay fails.

A certificate the queue itself would verify at a smaller count also counts, when
``--include-queue`` is given: the queue is then planned as if every member passes.

It decides nothing about any certificate's validity, and a skipped replay is a
deferral, not a refusal: the certificate stays reported, and replaying it later still
yields a second route.

Usage (from ``packing/``)::

    uv run --frozen --all-extras --group dev python -m devtools.plan_replay_dominance \\
        --queue rectangles-2026-10-01 --assume 59=8 --assume 77=9

``--queue`` names a built-in queue (the certificates of a packet's audit tool) or is a
path to a file of ``n bound`` lines (bound an exact rational). Prints JSON.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
from collections.abc import Iterable, Mapping, Sequence
from decimal import Decimal
from fractions import Fraction
from typing import Any

from devtools.audit_wand125_rectangles import CASES_2026_10_01
from sqpack.kingbird_catalogue import CatalogueParseError, evaluate_exact_form
from sqpack.yamlio import safe_load

ROOT = pathlib.Path(__file__).resolve().parent.parent
FRONTIER = ROOT / "frontier"
DIGITS = 40
#: How far a printed decimal is lowered when a case's exact form cannot be evaluated.
ROUNDING_MARGIN = Decimal("1e-9")


def builtin_queue(name: str) -> dict[int, Fraction]:
    """The certificates of a named queue, by count."""
    if name in BUILTIN:
        result_id, cases = BUILTIN[name]()
        scope = set(register_scope(result_id))
        return {n: bound for n, bound in cases.items() if n in scope}
    raise SystemExit(f"unknown queue {name!r}; built-in queues: {sorted(BUILTIN)}")


def _rectangles_2026_10_01() -> tuple[str, dict[int, Fraction]]:
    return "T-068", {n: bound for n, (_, bound) in CASES_2026_10_01.items()}


#: A queue is a register entry's scope, with each count's certificate bound.
BUILTIN = {"rectangles-2026-10-01": _rectangles_2026_10_01}


def register_scope(result_id: str) -> list[int]:
    """The counts a register entry's ``scope`` names."""
    document = safe_load((FRONTIER / "results.yaml").read_text(encoding="utf-8"))
    for result in document["results"]:
        if result["id"] == result_id:
            return [int(n) for n in result["scope"]["n_values"]]
    raise SystemExit(f"{result_id} is not in the register")


def read_queue(spec: str) -> dict[int, Fraction]:
    """A built-in queue, or a file of ``n bound`` lines."""
    path = pathlib.Path(spec)
    if not path.exists():
        return builtin_queue(spec)
    queue: dict[int, Fraction] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        fields = line.split("#", 1)[0].split()
        if fields:
            queue[int(fields[0])] = Fraction(fields[1])
    return queue


def verified_bounds() -> dict[int, Decimal]:
    """Each case's verified lower bound, evaluated from its exact form."""
    bounds: dict[int, Decimal] = {}
    for path in sorted(FRONTIER.glob("n-*.md")):
        packing = safe_load(path.read_text(encoding="utf-8").split("---\n")[1])["packing"]
        bound = packing.get("verified_lower_bound") or {}
        form = bound.get("exact_form")
        if not form:
            continue
        try:
            bounds[int(packing["n"])] = evaluate_exact_form(str(form), DIGITS)
        except CatalogueParseError:
            # An algebraic form such as ``root(P, approx)``: the printed decimal, lowered by
            # more than its rounding, so a skip never rests on an over-stated floor.
            bounds[int(packing["n"])] = Decimal(str(bound["value"])) - ROUNDING_MARGIN
    return bounds


def _decimal(value: Fraction) -> Decimal:
    return Decimal(value.numerator) / Decimal(value.denominator)


def plan(
    queue: Mapping[int, Fraction],
    verified: Mapping[int, Decimal],
    assumed: Mapping[int, Fraction],
    *,
    include_queue: bool,
) -> list[dict[str, Any]]:
    """One row per queued certificate: replay it, or skip it and why."""
    sources = [(n, v, "verified now") for n, v in verified.items()]
    sources += [(n, _decimal(v), f"assumed s({n}) >= {v}") for n, v in assumed.items()]
    if include_queue:
        sources += [(n, _decimal(v), f"queued at n = {n}") for n, v in queue.items()]
    rows: list[dict[str, Any]] = []
    for n in sorted(queue):
        best: tuple[Decimal, str, int] | None = None
        for m, value, why in sources:
            if m > n or (m == n and why.startswith("queued at")):
                continue
            if best is None or value > best[0]:
                best = (value, why, m)
        bound = _decimal(queue[n])
        row: dict[str, Any] = {"n": n, "bound": str(queue[n]), "bound_decimal": f"{bound:.6f}"}
        if best is not None and best[0] >= bound:
            row.update(
                action="skip",
                dominated_by=f"{best[1]} (n = {best[2]}, {best[0]:.6f})",
                rests_on_assumption=best[1].startswith("assumed"),
            )
        else:
            floor_value = f"{best[0]:.6f}" if best else None
            row.update(action="replay", raises_verified_from=floor_value)
        rows.append(row)
    return rows


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    parser.add_argument(
        "--queue", required=True, help="a built-in queue or a file of 'n bound' lines"
    )
    parser.add_argument(
        "--assume", action="append", default=[], help="N=VALUE, expected verified first"
    )
    parser.add_argument(
        "--include-queue", action="store_true", help="count the queue's smaller counts"
    )
    args = parser.parse_args(argv)
    assumed: dict[int, Fraction] = {}
    for item in args.assume:
        n, _, value = item.partition("=")
        assumed[int(n)] = Fraction(value)
    queue = read_queue(args.queue)
    rows = plan(queue, verified_bounds(), assumed, include_queue=args.include_queue)
    skipped: Iterable[dict[str, Any]] = [row for row in rows if row["action"] == "skip"]
    print(
        json.dumps(
            {
                "queue": args.queue,
                "assumed": {str(n): str(v) for n, v in assumed.items()},
                "replay": sum(1 for row in rows if row["action"] == "replay"),
                "skip": sum(1 for _ in skipped),
                "rows": rows,
            },
            indent=1,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
