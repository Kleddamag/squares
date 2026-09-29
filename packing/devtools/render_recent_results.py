#!/usr/bin/env python3
"""Generate README's three results tables from the register and the case records.

README's New Results and Results by Others were a paragraph of prose per result, and its
survey carried a listing of recent lower bounds kept by hand that drifted three times
(`think-ti71`). All three are rendered here instead, each spliced into README between its
own pair of `BEGIN GENERATED` markers:

- **`new-results`**, under New Results: every result of this project (`apparently-novel`
  or `confirmed-novel`), one row per `T-NNN`, highest `S` first, then newest.
- **`results-by-others`**, under Results by Others: every register entry by others
  published on or after `RECENT_SINCE`, newest first.
- **`recent-results`**, under the survey: one row for every case `n <= 100` whose
  verified or reported lower bound is a recent result, with both lanes where they differ.

**A register row states nothing by hand.** The headline, the rungs, the significance and
the date are the entry's own fields: `established` for this project's results,
`attribution.published` for others'. The credit and the relation to this project are
`render_results.credit_line` and `render_results.source_lineage`, the functions that
print them in `RESULTS.md`, so the two views cannot credit a result differently.
The records cell links the retained packet READMEs and the reviews among the entry's
`artifacts`, and its `review_artifact`.

**Standing is derived from the case records, never stored** (epistemics.md, "Results by
Others"). An entry *holds* where a case in its scope has a bound that rests on it, read
the way the per-case table credits a bound: the one first-party result behind a bound of
this project's (`project_result`), else every entry carrying the bound's own evidence
(`results_carrying` over `own_evidence`, which leaves the grid and area bounds out). So a
shared checker, such as the interval decision several first-party certificates cite, does
not make every rung it decided hold the bound. Where only a reported bound rests on an
entry, it holds as reported. An entry that holds nothing is a *second certificate* where
it proves the exact value of a proved case (it cites that case's verified upper bound
beside a lower bound of its own), *superseded* where it is any other bound, and not a
bound at all where its evidence claims none.

**Recent is decided where the record already decides it; nothing here defines it.** A
verified lower bound is recent where the stage and the atlas star it,
`build_bound_citations.lower_origin`: this project's own new bound, or an external
source dated on or after `RECENT_SINCE`. A reported one is recent where the register's
coverage gate, `check_results.recent_evidence`, says a register entry must hold it, the
definition written for both lanes. So the verified rows and the stars cannot disagree,
and every recent reported bound has a register entry to show.

**Nothing about a source is restated in the per-case table either.** The holder is the
bibliography's credit line as the stage prints it (`Source.credited`), or
`Squares Project (Levy)` for this project's own bound; the lineage is the bibliography's
typed `lineage`; the results are those that carry the bound's own evidence for this `n`,
as the stage lists them, each with its register `V` and `C`. The date is the register's
`published` for a source release it registers on its own, the release's `dated` where one
entry spans several releases (its `published` is the earliest of them), and for this
project's own bound the day the result was `established`.

The counts the survey summary quotes are computed here, by `recent_counts`, and held by
`devtools.check_readme` in the shape of `check_nagamochi_bounds._README_COUNT`.

Staleness is decided on what a block says rather than on its bytes, as for the synopsis
headline: README is prose the Markdown formatter owns, so a generated block inside it is
compared through `render_research_tables.fold`, and a row whose content did not move is
written back as the document already has it. `--check` fails when any of the three
blocks differs from its rendering, so a hand edit inside one fails the gate.

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m devtools.render_recent_results --update
    uv run --frozen --all-extras --group dev python -m devtools.render_recent_results --check
"""

from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any, NamedTuple

from strif import atomic_output_file

from devtools.build_bound_citations import (
    BIBLIOGRAPHY,
    NOVEL,
    PROJECT_NAME,
    RECENT_SINCE,
    LowerOrigin,
    Register,
    Source,
    load_case,
    load_register,
    lower_origin,
    own_evidence,
    project_result,
    record_name,
    result_order,
    results_carrying,
)
from devtools.check_results import recent_evidence, scope_values
from devtools.render_research_tables import fold, keep_document_typography
from devtools.render_results import credit_line, source_lineage
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
# The repository root. The reader-facing documents live there, not under packing/.
REPO = ROOT.parent
README = REPO / "README.md"
GENERATOR = "devtools.render_recent_results"


@dataclass(frozen=True, slots=True)
class Block:
    """One generated table in README: its marker name and what a message calls it."""

    name: str
    title: str

    @property
    def begin(self) -> str:
        return f"<!-- BEGIN GENERATED: {self.name} ({GENERATOR}) -->"

    @property
    def end(self) -> str:
        return f"<!-- END GENERATED: {self.name} -->"


NEW = Block("new-results", "new results")
OTHERS = Block("results-by-others", "results by others")
RECENT = Block("recent-results", "recent results")
#: README order, which is also the order `--check` reports them in.
BLOCKS = (NEW, OTHERS, RECENT)
BEGIN = RECENT.begin
END = RECENT.end

#: The cases the per-case table covers. The survey summary it backs is about "its hundred
#: cases", so it is held to `n <= 100` however far the corpus runs.
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
#: The range dash in an `n` cell, and the dot between a row's record links, written as
#: escapes for the same reason.
DASH = "\u2013"
DOT = "\u00b7"
#: The standing cell of an entry that is not a bound: a rigidity, an exclusion, an erratum.
NOT_A_BOUND = "\u2014"

#: An entry's standing, derived from the case records (see the module docstring).
HOLDS = "holds"
HOLDS_REPORTED = "holds, reported"
SECOND_CERTIFICATE = "second certificate"
SUPERSEDED = "superseded"
STANDINGS = (HOLDS, HOLDS_REPORTED, SECOND_CERTIFICATE, SUPERSEDED, NOT_A_BOUND)
#: The evidence claims that make an entry a bound on `s(n)`, as the evidence schema types
#: them; `derived-structure` and the witness claims are not bounds.
BOUND_CLAIMS = frozenset({"lower-bound", "upper-bound", "exact-value"})

#: An `n` cell names at most this many values or ranges before it gives a count instead.
SHORT_LIST = 4

#: Where an entry's retained packet README and its reviews live, among its `artifacts`.
PACKET = re.compile(r"^packing/resources/web/[^/]+/README\.md$")
REVIEWS = "docs/project/reviews/"
RESULTS_VIEW = "packing/frontier/RESULTS.md"

NEW_HEADER = "| Result | `n` | Headline | V | C | S | Established | Standing |"
NEW_RULE = "| --- | --- | --- | --- | --- | --- | --- | --- |"
OTHERS_HEADER = (
    "| Published | Result | `n` | Headline | Credit | Relation | V/C | Standing | Records |"
)
OTHERS_RULE = "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"
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


class Held(NamedTuple):
    """Which register entries one case's bounds rest on, and what standing needs besides."""

    verified: frozenset[str]
    """Entries a verified bound, lower or upper, rests on."""
    reported: frozenset[str]
    """Entries a reported bound, lower or upper, rests on."""
    upper: frozenset[str]
    """The verified upper bound's evidence, the grid's included: an exact value's top."""
    proved: bool
    """Whether the case is proved, so its verified bounds meet at an exact value."""


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
    """What every row is read from, loaded once per render."""

    register: Register
    results: Mapping[str, Mapping[str, Any]]
    sources: Mapping[str, Mapping[str, Any]]
    cases: Mapping[int, Mapping[str, Any]]


def _scope(record: Mapping[str, Any]) -> list[int]:
    return sorted(scope_values(dict(record["scope"])))


def load_records() -> Records:
    """The register, the bibliography, and every case a table row can name."""
    register = load_register()
    bibliography = safe_load(BIBLIOGRAPHY.read_text(encoding="utf-8"))
    wanted = set(range(1, HUNDRED + 1))
    for record in register.results:
        wanted.update(_scope(record))
    return Records(
        register=register,
        results={str(record["id"]): record for record in register.results},
        sources={str(source["key"]): source for source in bibliography["sources"]},
        cases={n: load_case(n) for n in sorted(wanted)},
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
            published=str(result["established"]),
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
        case = records.cases[n]
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


def _lower_holders(n: int, bound: Mapping[str, Any], records: Records, label: str) -> set[str]:
    """The entries a lower bound rests on, credited as the per-case table credits it."""
    register = records.register
    try:
        origin = lower_origin(n, bound, register, label)
    except ValueError:
        # A historical report whose evidence names several sources: every entry that
        # carries any of it, since no one source is its holder.
        own = own_evidence(bound["evidence"], register)
        return set(results_carrying(n, own, register.results))
    if origin is None:
        return set()
    if origin.source is None:
        return {str(project_result(n, origin.novel, register.results)["id"])}
    return set(results_carrying(n, origin.own, register.results))


def _upper_holders(n: int, bound: Mapping[str, Any] | None, records: Records) -> set[str]:
    """The entries an upper bound rests on: those carrying its own, non-grid evidence."""
    evidence = (bound or {}).get("evidence") or []
    own = own_evidence(evidence, records.register)
    return set(results_carrying(n, own, records.register.results))


def held(n: int, records: Records) -> Held:
    """Which entries case `n`'s four bounds rest on."""
    case = records.cases[n]
    upper = case.get("verified_upper_bound")
    verified = _lower_holders(n, case["verified_lower_bound"], records, "lower")
    verified |= _upper_holders(n, upper, records)
    reported = _lower_holders(n, case["reported_lower_bound"], records, "reported lower")
    reported |= _upper_holders(n, case.get("reported_upper_bound"), records)
    return Held(
        verified=frozenset(verified),
        reported=frozenset(reported),
        upper=frozenset(str(item) for item in (upper or {}).get("evidence") or []),
        proved=case["status"] == "proved",
    )


def standing(record: Mapping[str, Any], records: Records) -> str:
    """Whether an entry holds a case bound now, and if not, why not."""
    entry = str(record["id"])
    cases = [held(n, records) for n in _scope(record) if n in records.cases]
    if any(entry in case.verified for case in cases):
        return HOLDS
    if any(entry in case.reported for case in cases):
        return HOLDS_REPORTED
    cited = {str(item) for item in record["evidence"]}
    claims = {records.register.evidence[item].get("claim") for item in cited}
    if not claims & BOUND_CLAIMS:
        return NOT_A_BOUND
    if "lower-bound" in claims and any(case.proved and cited & case.upper for case in cases):
        return SECOND_CERTIFICATE
    return SUPERSEDED


def ours(records: Records) -> list[Mapping[str, Any]]:
    """This project's results in table order: highest `S` first, then newest."""
    return sorted(
        (record for record in records.register.results if record["novelty"] in NOVEL),
        key=lambda record: (
            record["significance"]["score"],
            str(record["established"]),
            result_order(str(record["id"])),
        ),
        reverse=True,
    )


def is_recent_by_others(record: Mapping[str, Any]) -> bool:
    """An entry by others published on or after `RECENT_SINCE`."""
    attribution = record.get("attribution")
    return bool(attribution) and str(attribution["published"]) >= RECENT_SINCE.isoformat()


def by_others(records: Records) -> list[Mapping[str, Any]]:
    """Recent results by others in table order: newest first."""
    return sorted(
        (record for record in records.register.results if is_recent_by_others(record)),
        key=lambda record: (
            str(record["attribution"]["published"]),
            result_order(str(record["id"])),
        ),
        reverse=True,
    )


def _cell(text: str) -> str:
    return text.replace("|", r"\|")


def _joined(values: Iterable[str | None]) -> str:
    return "; ".join(dict.fromkeys(value for value in values if value))


def _runs(values: Sequence[int]) -> list[tuple[int, int]]:
    runs: list[tuple[int, int]] = []
    for n in values:
        if runs and runs[-1][1] == n - 1:
            runs[-1] = (runs[-1][0], n)
        else:
            runs.append((n, n))
    return runs


def cases_cell(values: Sequence[int]) -> str:
    """One `n` linked to its case record; a few as a list with ranges; many as a count."""
    if len(values) == 1:
        return f"[{values[0]}](packing/frontier/{record_name(values[0])}.md)"
    parts: list[str] = []
    for first, last in _runs(values):
        if last - first >= 2:
            parts.append(f"{first}{DASH}{last}")
        else:
            parts.extend(str(n) for n in range(first, last + 1))
    if len(parts) <= SHORT_LIST:
        return ", ".join(parts)
    return f"{len(values)} in {values[0]}{DASH}{values[-1]}"


def result_cell(record: Mapping[str, Any]) -> str:
    return f"[{record['id']}]({RESULTS_VIEW})"


def _numbered(label: str, paths: Sequence[str]) -> list[str]:
    if len(paths) == 1:
        return [f"[{label}]({paths[0]})"]
    return [f"[{label} {index}]({path})" for index, path in enumerate(paths, start=1)]


def records_cell(record: Mapping[str, Any]) -> str:
    """The retained packet READMEs and the reviews an entry names, as links."""
    artifacts = [str(item) for item in record["artifacts"]]
    review = record.get("review_artifact")
    packets = [item for item in artifacts if PACKET.match(item)]
    listed = [item for item in artifacts if item.startswith(REVIEWS)]
    if review:
        listed.append(str(review))
    reviews: list[str] = list(dict.fromkeys(listed))
    return f" {DOT} ".join([*_numbered("packet", packets), *_numbered("review", reviews)])


def relation(record: Mapping[str, Any], records: Records) -> str:
    lineage = source_lineage(record, records.sources)
    if lineage not in LINEAGES:
        raise ValueError(
            f"{record['id']}: a recent result by others whose sources give no lineage"
        )
    return LINEAGES[lineage]


def new_row(record: Mapping[str, Any], records: Records) -> str:
    cells = (
        result_cell(record),
        cases_cell(_scope(record)),
        _cell(str(record["headline"])),
        str(record["verification"]),
        str(record["confirmation"]),
        f"S{record['significance']['score']}",
        str(record["established"]),
        standing(record, records),
    )
    return "| " + " | ".join(cells) + " |"


def others_row(record: Mapping[str, Any], records: Records) -> str:
    cells = (
        str(record["attribution"]["published"]),
        result_cell(record),
        cases_cell(_scope(record)),
        _cell(str(record["headline"])),
        credit_line(record, records.sources),
        relation(record, records),
        f"{record['verification']}/{record['confirmation']}",
        standing(record, records),
        records_cell(record),
    )
    return "| " + " | ".join(cells) + " |"


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
    """The per-case block body. Every line is a table row, which the formatter never wraps."""
    return [HEADER, RULE, *(table_row(row) for row in rows)]


def render_new(records: Records) -> list[str]:
    """The New Results block body: one row per result of this project."""
    return [NEW_HEADER, NEW_RULE, *(new_row(record, records) for record in ours(records))]


def render_others(records: Records) -> list[str]:
    """The Results by Others block body: one row per recent register entry by others."""
    return [
        OTHERS_HEADER,
        OTHERS_RULE,
        *(others_row(record, records) for record in by_others(records)),
    ]


def rendered(records: Records | None = None) -> dict[Block, list[str]]:
    """Every block's body, in README order."""
    records = records or load_records()
    return {
        NEW: render_new(records),
        OTHERS: render_others(records),
        RECENT: render_lines(recent_rows(records)),
    }


def block(text: str, which: Block = RECENT) -> str:
    """A block's current body, refusing a document whose markers cannot be trusted."""
    begin, end = which.begin, which.end
    if text.count(begin) != 1 or text.count(end) != 1 or text.index(begin) > text.index(end):
        raise ValueError(f"{README.name} needs exactly one ordered {which.name} marker pair")
    return text[text.index(begin) + len(begin) : text.index(end)]


def says(text: str) -> list[str]:
    """What a block's lines state, with formatter-owned typography folded away."""
    return [fold(line) for line in text.splitlines() if line.strip()]


def stale(text: str, lines: Sequence[str], which: Block = RECENT) -> bool:
    return says(block(text, which)) != says("\n".join(lines))


def spliced(text: str, lines: Sequence[str], which: Block = RECENT) -> str:
    """Replace one generated block, keeping each unchanged row as README has it."""
    kept = keep_document_typography(block(text, which), list(lines))
    start = text.index(which.begin)
    end = text.index(which.end) + len(which.end)
    body = "\n".join(kept)
    return f"{text[:start]}{which.begin}\n\n{body}\n\n{which.end}{text[end:]}"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--update", action="store_true", help="rewrite README's blocks")
    group.add_argument("--check", action="store_true", help="fail if a README block is stale")
    arguments = parser.parse_args(argv)
    try:
        records = load_records()
        blocks = rendered(records)
        current = README.read_text(encoding="utf-8")
        counts = recent_counts(recent_rows(records))
        if arguments.check:
            drifted = [which for which, lines in blocks.items() if stale(current, lines, which)]
            for which in drifted:
                print(f"{README.name} {which.title} are stale", file=sys.stderr)
            if drifted:
                print(
                    "  run: uv run --frozen python -m devtools.render_recent_results --update",
                    file=sys.stderr,
                )
                return 1
            print(
                f"  README results tables carry all {len(ours(records))} results of this "
                f"project, {len(by_others(records))} recent results by others, and "
                f"{counts.cases} cases with a recent lower bound, {counts.verified} of them "
                "verified"
            )
            return 0
        expected = current
        for which, lines in blocks.items():
            expected = spliced(expected, lines, which)
        if expected != current:
            with atomic_output_file(README) as temporary:
                temporary.write_text(expected, encoding="utf-8")
            print(
                f"rendered README results tables ({len(ours(records))} new, "
                f"{len(by_others(records))} by others, {counts.cases} cases)"
            )
        else:
            print("README results tables already current")
    except (OSError, ValueError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
