#!/usr/bin/env python3
"""Generate README's recent-results table from the case records and the register.

README's survey summary counts the cases whose lower bound is recent, and the listing
behind those counts was kept by hand and drifted three times (`think-ti71`). This renders
it instead: one row for every case `n <= 100` whose verified or reported lower bound is a
recent result, with both lanes where they differ, spliced into README between
`BEGIN GENERATED: recent-results` markers.

**Recent is decided where the record already decides it; nothing here defines it.** A
verified lower bound is recent where the stage and the atlas star it,
`build_bound_citations.lower_origin`: this project's own new bound, or an external
source dated on or after `RECENT_SINCE`. A reported one is recent where the register's
coverage gate, `check_results.recent_evidence`, says a register entry must hold it, the
definition written for both lanes. So the verified rows and the stars cannot disagree,
and every recent reported bound has a register entry to show.

**Nothing about a source is restated.** The holder is the bibliography's credit line as
the stage prints it (`Source.credited`), or `Squares Project (Levy)` for this project's
own bound; the lineage is the bibliography's typed `lineage`; the results are those that
carry the bound's own evidence for this `n`, as the stage lists them, each with its
register `V` and `C`. The date is the register's `published` for a source release it
registers on its own, the release's `dated` where one entry spans several releases (its
`published` is the earliest of them), and for this project's own bound the day the
register scored the result, the date the stage reads its year from.

The counts the survey summary quotes are computed here, by `recent_counts`, and held by
`devtools.check_readme` in the shape of `check_nagamochi_bounds._README_COUNT`.

Staleness is decided on what the block says rather than on its bytes, as for the
synopsis headline: README is prose the Markdown formatter owns, so a generated block
inside it is compared through `render_research_tables.fold`, and a row whose content did
not move is written back as the document already has it.

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m devtools.render_recent_results --update
    uv run --frozen --all-extras --group dev python -m devtools.render_recent_results --check
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any, NamedTuple

from strif import atomic_output_file

from devtools.build_bound_citations import (
    BIBLIOGRAPHY,
    PROJECT_NAME,
    LowerOrigin,
    Register,
    Source,
    load_case,
    load_register,
    lower_origin,
    project_result,
    record_name,
    results_carrying,
)
from devtools.check_results import recent_evidence
from devtools.render_research_tables import fold, keep_document_typography
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
# The repository root. The reader-facing documents live there, not under packing/.
REPO = ROOT.parent
README = REPO / "README.md"
BEGIN = "<!-- BEGIN GENERATED: recent-results (devtools.render_recent_results) -->"
END = "<!-- END GENERATED: recent-results -->"

#: The cases the table covers. The survey summary it backs is about "its hundred cases",
#: so it is held to `n <= 100` however far the corpus runs.
HUNDRED = 100

#: What a row calls this project's own bound, and each lineage the bibliography types.
PROJECT_LINEAGE = "this project"
LINEAGES = {
    "builds-on-project": "builds on",
    "credits-project": "credits second-hand",
    "independent": "independent",
}

#: A decimal that does not terminate within `EXACT_PLACES` is cut at `PLACES` and ends in
#: an ellipsis, written as an escape for the reason
#: `tests/test_generated_table_typography.py` gives. Cut, never rounded: a lower bound
#: shown rounded up would claim more than the record proves.
EXACT_PLACES = 6
PLACES = 4
ELLIPSIS = "\u2026"

HEADER = (
    "| `n` | Verified lower bound | Holder | Result | Reported, where different "
    "| Holder | Result | Lineage | Published |"
)
RULE = "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"


@dataclass(frozen=True, slots=True)
class Lane:
    """One lower bound of a case, reported or verified, as a row shows it."""

    value: Fraction
    shown: str
    holder: str
    results: str
    recent: bool
    ours: bool
    lineage: str | None
    published: str | None


@dataclass(frozen=True, slots=True)
class Row:
    """One case with a recent lower bound in either lane."""

    n: int
    exact: bool
    verified: Lane
    reported: Lane

    @property
    def shows_reported(self) -> bool:
        """The reported lane is its own entry only where it says something else."""
        return (self.reported.value, self.reported.holder) != (
            self.verified.value,
            self.verified.holder,
        )

    @property
    def described(self) -> list[Lane]:
        """The recent lanes the lineage and date columns describe, verified first."""
        shown = [self.verified, *([self.reported] if self.shows_reported else [])]
        return [lane for lane in shown if lane.recent] or [self.reported]


class RecentCounts(NamedTuple):
    """The four counts README's survey summary quotes."""

    cases: int
    """Cases with a recent lower bound, reported or verified: the table's rows."""
    verified: int
    """Of those, the cases whose verified bound itself is recent: the atlas's stars."""
    ours: int
    """Of those, this project's own."""
    exact: int
    """Of those, the proved cases: new exact values."""


def _rational(text: object) -> Fraction | None:
    """An exact form as a number, or None where it is a closed form such as a root."""
    if text is None:
        return None
    try:
        return Fraction(str(text))
    except ValueError, ZeroDivisionError:
        return None


def _fixed(scaled: int, places: int) -> str:
    whole, part = divmod(scaled, 10**places)
    return f"{whole}.{part:0{places}d}" if places else str(whole)


def digits(value: Fraction) -> str:
    """The value in decimals, exactly where it terminates soon, else cut and marked."""
    for places in range(EXACT_PLACES + 1):
        scaled = value * 10**places
        if scaled.denominator == 1:
            return _fixed(scaled.numerator, places)
    return _fixed(value.numerator * 10**PLACES // value.denominator, PLACES) + ELLIPSIS


def magnitude(bound: Mapping[str, Any]) -> Fraction:
    """A bound's value: its exact form where that is a number, else its recorded value."""
    rational = _rational(bound.get("exact_form"))
    return rational if rational is not None else Fraction(str(bound["value"]))


def shown(bound: Mapping[str, Any]) -> str:
    """The value cell: the exact form and its decimals, or a closed form's decimals."""
    exact = bound.get("exact_form")
    value = magnitude(bound)
    if _rational(exact) is None:
        return digits(value)
    if value.denominator == 1 or str(exact) == digits(value):
        return f"`{exact}`"
    return f"`{exact}` = {digits(value)}"


def rungs(records: Iterable[Mapping[str, Any]]) -> str:
    return ", ".join(
        f"{record['id']} `{record['verification']}/{record['confirmation']}`"
        for record in records
    )


def published(source: Source, carrying: Sequence[Mapping[str, Any]]) -> str | None:
    """When the source published the bound, by the register where it can say."""
    dates = [
        str(record["attribution"]["published"])
        for record in carrying
        if (record.get("attribution") or {}).get("source_keys") == [source.key]
    ]
    if dates:
        return min(dates)
    if source.dated is not None:
        return source.dated.isoformat()
    return None if source.year is None else str(source.year)


@dataclass(frozen=True, slots=True)
class Records:
    """What every lane is read from, loaded once per render."""

    register: Register
    results: Mapping[str, Mapping[str, Any]]
    sources: Mapping[str, Mapping[str, Any]]


def load_records() -> Records:
    register = load_register()
    bibliography = safe_load(BIBLIOGRAPHY.read_text(encoding="utf-8"))
    return Records(
        register=register,
        results={str(record["id"]): record for record in register.results},
        sources={str(source["key"]): source for source in bibliography["sources"]},
    )


def lane(
    n: int,
    bound: Mapping[str, Any],
    origin: LowerOrigin | None,
    records: Records,
    *,
    recent: bool,
    label: str,
) -> Lane:
    """One lane's value, holder, results, lineage and date, given whether it is recent."""
    value, cell = magnitude(bound), shown(bound)
    if origin is None:
        if recent:
            raise ValueError(f"n={n} {label}: a recent bound whose evidence names no source")
        # A derived bound, or a historical report whose evidence names no one source.
        return Lane(value, cell, "", "", recent=False, ours=False, lineage=None, published=None)
    register = records.register
    if origin.source is None:
        result = project_result(n, origin.novel, register.results)
        return Lane(
            value,
            cell,
            PROJECT_NAME,
            rungs([result]),
            recent=recent,
            ours=True,
            lineage=PROJECT_LINEAGE,
            published=str(result["significance"]["scored"]),
        )
    source = origin.source
    carrying = [
        records.results[item] for item in results_carrying(n, origin.own, register.results)
    ]
    if source.lineage is not None and source.lineage not in LINEAGES:
        raise ValueError(f"n={n} {label}: {source.key} has unknown lineage {source.lineage}")
    lineage = LINEAGES.get(source.lineage or "")
    if recent and lineage is None:
        raise ValueError(
            f"n={n} {label}: {source.key} is a recent source and the bibliography "
            "gives it no lineage"
        )
    return Lane(
        value,
        cell,
        source.credited,
        rungs(carrying),
        recent=recent,
        ours=False,
        lineage=lineage,
        published=published(source, carrying),
    )


def verified_lane(n: int, case: Mapping[str, Any], records: Records) -> Lane:
    """The verified lower bound, recent where the atlas stars it."""
    bound = case["verified_lower_bound"]
    origin = lower_origin(n, bound, records.register)
    recent = origin is not None and origin.recent
    return lane(n, bound, origin, records, recent=recent, label="lower")


def reported_lane(n: int, case: Mapping[str, Any], records: Records) -> Lane:
    """The reported lower bound, recent where the register's coverage gate says so.

    The star is decided for verified bounds, whose evidence always names its source. A
    reported bound can rest on a historical report the migration carried without one
    (`E-migrated-lower-report`), which the star cannot be asked about; the coverage gate,
    `check_results.recent_evidence`, is the definition written for both lanes, and it is
    the one that guarantees a recent reported bound a register entry to show.
    """
    bound = case["reported_lower_bound"]
    evidence = records.register.evidence
    recent = any(recent_evidence(evidence[item], records.sources) for item in bound["evidence"])
    try:
        origin = lower_origin(n, bound, records.register, "reported lower")
    except ValueError:
        if recent:
            raise
        origin = None
    return lane(n, bound, origin, records, recent=recent, label="reported lower")


def recent_rows(records: Records | None = None) -> list[Row]:
    """Every case `n <= 100` with a recent lower bound in either lane, in `n` order."""
    records = records or load_records()
    rows: list[Row] = []
    for n in range(1, HUNDRED + 1):
        case = load_case(n)
        verified = verified_lane(n, case, records)
        reported = reported_lane(n, case, records)
        if verified.recent or reported.recent:
            rows.append(Row(n, case["status"] == "proved", verified, reported))
    return rows


def recent_counts(rows: Sequence[Row]) -> RecentCounts:
    verified = [row for row in rows if row.verified.recent]
    return RecentCounts(
        cases=len(rows),
        verified=len(verified),
        ours=sum(row.verified.ours for row in verified),
        exact=sum(row.exact for row in verified),
    )


def _cell(text: str) -> str:
    return text.replace("|", r"\|")


def _joined(values: Iterable[str | None]) -> str:
    return "; ".join(dict.fromkeys(value for value in values if value))


def table_row(row: Row) -> str:
    verified, reported = row.verified, row.reported
    value = f"{verified.shown}, exact" if row.exact else verified.shown
    other = (
        (reported.shown, _cell(reported.holder), reported.results)
        if row.shows_reported
        else ("", "", "")
    )
    cells = (
        f"[{row.n}](packing/frontier/{record_name(row.n)}.md)",
        value,
        _cell(verified.holder),
        verified.results,
        *other,
        _joined(item.lineage for item in row.described),
        _joined(item.published for item in row.described),
    )
    return "| " + " | ".join(cells) + " |"


def render_lines(rows: Sequence[Row]) -> list[str]:
    """The block body. Every line is a table row, which the formatter never rewraps."""
    return [HEADER, RULE, *(table_row(row) for row in rows)]


def block(text: str) -> str:
    """The current block body, refusing a document whose markers cannot be trusted."""
    if text.count(BEGIN) != 1 or text.count(END) != 1 or text.index(BEGIN) > text.index(END):
        raise ValueError(f"{README.name} needs exactly one ordered recent-results marker pair")
    return text[text.index(BEGIN) + len(BEGIN) : text.index(END)]


def says(text: str) -> list[str]:
    """What a block's lines state, with formatter-owned typography folded away."""
    return [fold(line) for line in text.splitlines() if line.strip()]


def stale(text: str, lines: Sequence[str]) -> bool:
    return says(block(text)) != says("\n".join(lines))


def spliced(text: str, lines: Sequence[str]) -> str:
    """Replace the one generated block, keeping each unchanged row as README has it."""
    kept = keep_document_typography(block(text), list(lines))
    start = text.index(BEGIN)
    end = text.index(END) + len(END)
    return text[:start] + f"{BEGIN}\n\n" + "\n".join(kept) + f"\n\n{END}" + text[end:]


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--update", action="store_true", help="rewrite README's block")
    group.add_argument("--check", action="store_true", help="fail if README's block is stale")
    arguments = parser.parse_args(argv)
    try:
        rows = recent_rows()
        lines = render_lines(rows)
        current = README.read_text(encoding="utf-8")
        counts = recent_counts(rows)
        if arguments.check:
            if stale(current, lines):
                print(f"{README.name} recent results are stale", file=sys.stderr)
                print(
                    "  run: uv run --frozen python -m devtools.render_recent_results --update",
                    file=sys.stderr,
                )
                return 1
            print(
                f"  README recent results carry all {counts.cases} cases with a recent "
                f"lower bound, {counts.verified} of them verified"
            )
            return 0
        expected = spliced(current, lines)
        if expected != current:
            with atomic_output_file(README) as temporary:
                temporary.write_text(expected, encoding="utf-8")
            print(f"rendered README recent results ({counts.cases} cases)")
        else:
            print("README recent results already current")
    except (OSError, ValueError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
