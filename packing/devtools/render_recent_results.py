"""Read the recent results and each register entry's standing from the record.

This module once spliced three results tables into README. Those tables, and README's
New Results, Results by Others and survey sections with them, moved to the site's
overview (`devtools.render_overview`, `devtools.overview_data`), which reads its rows,
counts and standings from the functions here, as `frontier/RESULTS.md`
(`devtools.render_results`) reads `standing`. README now points at the site.

- **`recent_rows`**: one `Row` for every case `n <= 100` whose verified or reported
  lower bound is a recent result, with both lanes, and **`recent_counts`**, the four
  counts the site's survey section quotes.
- **`standing`**: whether a register entry holds a case bound now, and if not, why not.
- **`relation`** and `LINEAGES`: the relation of a result by others to this project,
  read from the bibliography's typed lineage.

**Standing is derived from the case records, never stored** (epistemics.md, "Results by
Others"). An entry is the *current best* where a case in its scope has a bound that
rests on it (the code calls this `HOLDS`), read the way the per-case rows credit a
bound: the one first-party result behind a bound of this project's (`project_result`),
else every entry carrying the bound's own evidence (`results_carrying` over
`own_evidence`, which leaves the grid and area bounds out). So a shared checker, such as
the interval decision several first-party certificates cite, does not make every rung it
decided hold the bound. Where only a reported bound rests on an entry, it is the current
best as reported. An entry that holds no bound is a *second certificate* where it proves
the exact value of a proved case (it cites that case's verified upper bound beside a
lower bound of its own) and *superseded* where it is any other bound.

**Standing is about bounds, so an entry whose evidence claims none has no standing**
(`NO_STANDING`): nothing supersedes a rigidity or a case exclusion. The views show such
an entry's `kind` (epistemics.md, Result Kinds) and no standing, and
`devtools.check_results` holds it to a kind that is no bound.

**Recent is decided where the record already decides it; nothing here defines it.** A
verified lower bound is recent where the stage and the atlas star it,
`build_bound_citations.lower_origin`: this project's own new bound, or an external
source dated on or after `RECENT_SINCE`. A reported one is recent where the register's
coverage gate, `check_results.recent_evidence`, says a register entry must hold it, the
definition written for both lanes. So the verified rows and the stars cannot disagree,
and every recent reported bound has a register entry to show.

**Nothing about a source is restated in a row either.** The holder is the
bibliography's credit line as the stage prints it (`Source.credited`), or
`Square Packing Project (Levy)` for this project's own bound; the lineage is the bibliography's
typed `lineage`; the results are those that carry the bound's own evidence for this `n`,
as the stage lists them, each with its register `V` and `C`. The date is the register's
`published` for a source release it registers on its own, the release's `dated` where one
entry spans several releases (its `published` is the earliest of them), and for this
project's own bound the day the result was `established`.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Any, NamedTuple

from devtools.build_bound_citations import (
    BIBLIOGRAPHY,
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
    results_carrying,
)
from devtools.check_results import recent_evidence, scope_values
from devtools.result_credit import source_lineage
from sqpack.assurance import bounds_agree_at_declared_precision
from sqpack.yamlio import safe_load

#: The cases the recent rows cover. The survey counts they back are about "the hundred
#: cases", so they are held to `n <= 100` however far the corpus runs.
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
ELLIPSIS = "…"

#: An entry's standing, derived from the case records (see the module docstring).
HOLDS = "current best"
HOLDS_REPORTED = "current best, reported"
SECOND_CERTIFICATE = "second certificate"
#: A second route to a proved value that this repository has not replayed: the same word
#: as a replayed one would say it had been checked here.
SECOND_CERTIFICATE_REPORTED = "second certificate, reported"
SUPERSEDED = "superseded"
STANDINGS = (
    HOLDS,
    HOLDS_REPORTED,
    SECOND_CERTIFICATE,
    SECOND_CERTIFICATE_REPORTED,
    SUPERSEDED,
)
#: What `standing` returns for an entry whose evidence claims no bound: it has none.
NO_STANDING = ""
#: The confirmation rungs at which a certificate has been replayed here (epistemics.md).
REPLAYED_RUNGS = frozenset({"C3", "C4", "C5"})
#: The evidence claims that make an entry a bound on `s(n)`, as the evidence schema types
#: them; `derived-structure` and the witness claims are not bounds.
BOUND_CLAIMS = frozenset({"lower-bound", "upper-bound", "exact-value"})


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
    bound: Mapping[str, Any] = field(default_factory=dict[str, Any], compare=False, repr=False)
    """The case record's bound the lane was read from, its `value` and `exact_form` as
    written, for the register's own test of whether two bounds are one value."""

    def same_value(self, other: Lane) -> bool:
        """Whether two lanes state one value: equal as numbers, or equal at the precision
        their records print, by `bounds_agree_at_declared_precision`, the rule the case
        pages and the stage's citations already apply to a reported and a verified bound.
        """
        return self.value == other.value or bounds_agree_at_declared_precision(
            self.bound, other.bound
        )


@dataclass(frozen=True, slots=True)
class Row:
    """One case with a recent lower bound in either lane."""

    n: int
    exact: bool
    verified: Lane
    reported: Lane

    @property
    def shows_reported(self) -> bool:
        """The reported lane is its own entry only where it says something else.

        It says nothing else where it carries the same register entries as the verified
        lane, which is one result reported and then verified, or where the same holder
        reports the verified value at the precision its record prints. A record may keep
        a source's rounded display beside the exact verified value: n = 11 reports
        `3.87708359002281` for T, which the verified lane carries to 32 places, and
        comparing the two as numbers listed T-060 as awaiting its own replay, with a
        reported value below the verified one (think-pd2g).
        """
        reported, verified = self.reported, self.verified
        if reported.results and reported.results == verified.results:
            return False
        return reported.holder != verified.holder or not reported.same_value(verified)

    @property
    def described(self) -> list[Lane]:
        """The recent lanes the lineage and date columns describe, verified first."""
        shown = [self.verified, *([self.reported] if self.shows_reported else [])]
        return [lane for lane in shown if lane.recent] or [self.reported]


class RecentCounts(NamedTuple):
    """The four counts the site's survey section quotes."""

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
        return Lane(
            value,
            cell,
            "",
            "",
            recent=False,
            ours=False,
            lineage=None,
            published=None,
            bound=bound,
        )
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
            bound=bound,
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
        bound=bound,
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
    """Whether an entry holds a case bound now, and if not, why not. An entry whose
    evidence claims no bound has no standing, `NO_STANDING`."""
    entry = str(record["id"])
    cases = [held(n, records) for n in _scope(record) if n in records.cases]
    if any(entry in case.verified for case in cases):
        return HOLDS
    if any(entry in case.reported for case in cases):
        return HOLDS_REPORTED
    cited = {str(item) for item in record["evidence"]}
    claims = {records.register.evidence[item].get("claim") for item in cited}
    if not claims & BOUND_CLAIMS:
        return NO_STANDING
    if "lower-bound" in claims and any(case.proved and cited & case.upper for case in cases):
        if str(record["confirmation"]) in REPLAYED_RUNGS:
            return SECOND_CERTIFICATE
        return SECOND_CERTIFICATE_REPORTED
    return SUPERSEDED


def is_recent_by_others(record: Mapping[str, Any]) -> bool:
    """An entry by others published on or after `RECENT_SINCE`."""
    attribution = record.get("attribution")
    return bool(attribution) and str(attribution["published"]) >= RECENT_SINCE.isoformat()


def relation(record: Mapping[str, Any], records: Records) -> str:
    lineage = source_lineage(record, records.sources)
    if lineage not in LINEAGES:
        raise ValueError(
            f"{record['id']}: a recent result by others whose sources give no lineage"
        )
    return LINEAGES[lineage]
