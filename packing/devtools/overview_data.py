#!/usr/bin/env python3
"""The data the overview shows, as one typed model read from the record.

Nothing here is typed by hand: every result comes from `frontier/results.yaml`, every
case bound from `frontier/n-NNN.md`, every credit from `resources/bibliography.yaml`,
and every notable source from `resources/notable-sources.yaml`. What is recent, how a
result relates to this project, and whether it still holds a case bound are decided by
`devtools.render_recent_results`, the functions README's generated blocks use, so the
overview and README cannot disagree.

The types below are the contract the overview page renders from, and `load()` fills them:

- **Recent results** are README's two generated lists, selected and ordered by the same
  `ours` and `by_others`; a result's relation to this project is `relation`, its standing
  `standing`, and a superseded result names the case's current holder from
  `verified_lane`.
- **The results table** is `RESULTS.md`'s grouping and order, `render_results.grouped_results`.
- **Credit** is `result_credit.credit_line`, printed whole, and a source's own statement of
  AI assistance is the bibliography's `ai_assistance`, the field the case-record tool reads.
- **A bound** is read from the register's claim, which keeps its relation: `T-037` claims
  `s(11) > 31/8`, strictly, where the case record states only the value. A case record's
  bound is shown with `≥` unless a register entry carrying its evidence claims it strictly.
  Decimals are cut, never rounded (`render_recent_results.digits`), since a lower bound
  shown rounded up would claim more than the record proves.
- **The counts** are of declared rungs, never re-derived ones: `check_results` accepts a
  declared rung below the derived one where a composition note explains it. Their labels
  and definitions are `epistemics.md`'s own, through `significance.rungs`.
- **Record links** are permalinks at the build commit (`render_explainer.repo_file`), an
  evidence entry at its line in `evidence.yaml` and a register entry at its line in
  `results.yaml`. Whether a link is a `tree/` or a `blob/` is decided from the path as the
  record writes it, a directory with a trailing slash, never from the filesystem: the
  Pages checkout leaves out `packing/resources/*/`, and the page must render the same
  there as in a full clone.

Nothing here reads a file under `packing/resources/*/` or `packing/campaign/*/`.
"""

from __future__ import annotations

import json
import re
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from datetime import date
from decimal import ROUND_DOWN, ROUND_HALF_EVEN, ROUND_HALF_UP, Decimal, localcontext
from fractions import Fraction
from functools import cache
from pathlib import Path, PurePosixPath
from typing import Any, Literal, NamedTuple, cast

from devtools import build_bound_citations as citations
from devtools import render_explainer, render_results, significance
from devtools import render_recent_results as recent
from devtools.check_results import scope_values
from devtools.result_credit import credit_line, source_lineage
from devtools.state_ai_assistance import said
from sqpack.release import DATA_REVISION, PUBLICATION_EDITION, PUBLICATION_HISTORY
from sqpack.yamlio import safe_load

PACKING = Path(__file__).resolve().parent.parent
REPO = PACKING.parent
DEVTOOLS = PACKING / "devtools"
FRONTIER = PACKING / "frontier"
RESULTS = FRONTIER / "results.yaml"
EVIDENCE = FRONTIER / "evidence.yaml"
COVERAGE = FRONTIER / "source-coverage.yaml"
BIBLIOGRAPHY = PACKING / "resources" / "bibliography.yaml"
NOTABLE_SOURCES = PACKING / "resources" / "notable-sources.yaml"
COMPOSITE = PACKING / "atlas" / "known-best" / "composite-figure.json"
EPISTEMICS = REPO / "epistemics.md"

#: Every path a render of this model reads: the records, and the code that reads them.
#: The frontier directory stands for the case records, `n-001.md` to `n-324.md`.
RENDER_INPUTS: tuple[Path, ...] = (
    Path(__file__),
    FRONTIER,
    RESULTS,
    EVIDENCE,
    COVERAGE,
    BIBLIOGRAPHY,
    NOTABLE_SOURCES,
    COMPOSITE,
    EPISTEMICS,
    DEVTOOLS / "render_recent_results.py",
    DEVTOOLS / "render_results.py",
    DEVTOOLS / "result_credit.py",
    DEVTOOLS / "significance.py",
    DEVTOOLS / "build_bound_citations.py",
    DEVTOOLS / "check_results.py",
    DEVTOOLS / "render_research_tables.py",
    DEVTOOLS / "state_ai_assistance.py",
    DEVTOOLS / "render_explainer.py",
    PACKING / "src" / "sqpack" / "release.py",
    PACKING / "src" / "sqpack" / "yamlio.py",
)

Lineage = Literal["this-project", "builds-on-project", "credits-project", "independent"]

#: The atlas composite whose totals the overview quotes: the hundred cases.
ATLAS_STEM = "known-best-1-100"
#: The typographic apostrophe, written as an escape for the reason
#: `tests/test_generated_table_typography.py` gives.
APOSTROPHE = "\u2019"
#: What a result's lineage is when it is this project's own.
THIS_PROJECT: Lineage = "this-project"
#: The lineage of a result by others whose sources type none, which only a source that
#: predates this project can lack: it is independent of a project that did not yet exist.
PREDATES: Lineage = "independent"


@dataclass(frozen=True)
class Link:
    """A labelled link: a record permalink, a case file, a source.

    `kind` says what it points at, for a page that styles them apart: `case` (a case
    record), `cases` (a run of them), `register` (the entry's line in `results.yaml`),
    `evidence` (an entry's line in `evidence.yaml`), `review`, `source` (a retained source
    copy), `artifact`, `control`, `archive` (a notable source's retained copy) or `record`
    (any other record file).
    """

    label: str
    url: str
    kind: str = ""


@dataclass(frozen=True)
class Bound:
    """One bound as the page prints it, with the relation its claim states.

    `relation` is `≥`, `>`, `≤`, `<` or `=`. `tex` is the bound as LaTeX, for example
    `s(11) > \\frac{31}{8}`; `decimal` is the value cut, never rounded, to the places the
    record states, ending in `…` when it does not terminate.

    `exact` is the exact form as the record writes it (`31/8`,
    `955000*sqrt(518400042893309449)/179696714646249`), and `value` is it as a number where
    it is rational, else None. In `tex`, `>` and `<` are written `\\gt` and `\\lt`, which
    survive HTML and Markdown unescaped.
    """

    n: int
    relation: str
    exact: str
    decimal: str
    tex: str
    value: Fraction | None


@dataclass(frozen=True)
class Result:
    """One register entry, with everything a card or a table row shows.

    `cases` is the `n` column, compressed to ranges as README's tables compress it.
    `credit` is `Squares Project (Levy)` for this project's results and
    `result_credit.credit_line` for others', printed whole. `relation` is README's relation
    to this project, for a recent result by others only. Where `standing` is `superseded`,
    `superseded_by` names the case's current holder and `superseded_by_results` the ids it
    rests on. `reported` marks a `V0` result, which a page labels reported and never
    verified; `exact_value` a result that proves an exact value, where `bound.relation` is
    `=`. `records` lists, in order, the case files (for at most four `n`; a wider scope is
    the frontier atlas's), the register entry, each evidence entry, the review, and each
    retained source copy.
    """

    id: str
    n_values: tuple[int, ...]
    cases: str
    headline: str
    claim: str
    bound: Bound | None
    verification: str
    confirmation: str
    significance: int
    novelty: str
    ours: bool
    credit: str
    ai_assistance: str | None
    lineage: Lineage
    relation: str | None
    standing: str
    superseded_by: str | None
    reported: bool
    exact_value: bool
    recent: bool
    established: str | None
    published: str | None
    registered: str
    next_rung: str
    composition: str | None
    records: tuple[Link, ...]
    artifacts: tuple[Link, ...]
    controls: tuple[Link, ...] = ()
    superseded_by_results: tuple[str, ...] = ()


@dataclass(frozen=True)
class ResultGroup:
    """A heading and its results, in the order `RESULTS.md` gives them."""

    key: str
    title: str
    results: tuple[Result, ...]


@dataclass(frozen=True)
class RungCount:
    """How many results stand at one rung of one axis, this project's and others'."""

    axis: Literal["V", "C", "S"]
    rung: int
    label: str
    definition: str
    ours: int
    others: int


@dataclass(frozen=True)
class AtlasTotals:
    """The hundred-case atlas's totals, read from `composite-figure.json`."""

    cases: int
    proved: int
    open: int
    recent_verified_lower: int


@dataclass(frozen=True)
class SourceRelease:
    """One reviewed release of a notable source.

    `archive` is its retained copy and `published` the source's own date for it, where
    `source-coverage.yaml` records one.
    """

    title: str
    url: str
    reviewed: str
    superseded: bool
    archive: Link | None = None
    published: str | None = None


@dataclass(frozen=True)
class NotableSource:
    """One card of Other Square Packing Projects."""

    id: str
    title: str
    kind: Literal["website", "catalogue", "release", "repository"]
    url: str
    credit: str
    summary: str
    archive: Link | None
    releases: tuple[SourceRelease, ...]
    cases: tuple[Link, ...]


@dataclass(frozen=True)
class ExplainerEdition:
    """How the explainer's lead result compares with the case record now.

    The dates are ISO days, read from `sqpack.release.PUBLICATION_HISTORY`:
    `first_published` is the page's first edition, and `edition` the edition that
    introduced the lead result, with the day it was first published.
    """

    lead_result: str
    lead_bound: Bound
    current_bound: Bound
    current_credit: str
    current_results: tuple[str, ...]
    is_current: bool
    first_published: str
    edition: str
    edition_first_published: str

    @property
    def note(self) -> str:
        """The generated line, as plain text with LaTeX math in `$…$`."""
        lead = f"{self.lead_result}{APOSTROPHE}s ${inline(self.lead_bound)}$"
        if self.is_current:
            return (
                f"This edition{APOSTROPHE}s lead result, {lead}, is the current verified "
                f"lower bound on $s({self.lead_bound.n})$."
            )
        holders = ", ".join(self.current_results)
        return (
            f"This edition leads with {lead}; the verified lower bound is now "
            f"${inline(self.current_bound)}$, {holders}, by {self.current_credit}."
        )


@dataclass(frozen=True)
class OverviewData:
    """Everything the overview page renders from, at one commit."""

    edition: str
    data_revision: str
    recent_ours: tuple[Result, ...]
    recent_others: tuple[Result, ...]
    groups: tuple[ResultGroup, ...]
    rung_counts: tuple[RungCount, ...]
    atlas: AtlasTotals
    sources: tuple[NotableSource, ...]
    explainer: ExplainerEdition


# --- Bounds -------------------------------------------------------------------------------

#: The relations a claim writes, as the page prints them and as LaTeX sets them.
RELATIONS = {">=": "≥", ">": ">", "<=": "≤", "<": "<", "=": "="}
TEX_RELATIONS = {"≥": r"\ge", ">": r"\gt", "≤": r"\le", "<": r"\lt", "=": "="}
#: `s(11) >= `, where a claim states a bound on one `s(n)`.
_CLAIMED = re.compile(r"\bs\((\d+)\)\s*(>=|<=|>|<|=)\s*")
#: One token of a closed form as the register writes one: a number, `sqrt`, an operator.
_TOKEN = re.compile(r"\s*(sqrt|\d+(?:\.\d+)?|[()+\-*/])")
#: The decimal a claim may state after the exact form: `= 3.826447410572939`, or cut short.
_STATED = re.compile(r"\s*=\s*(\d+\.\d+)(?:\.\.\.|…)?")
#: Enough digits that cutting a closed form's decimal at a few places is exact.
_PRECISION = 60


class _Form(NamedTuple):
    """A parsed closed form: its LaTeX, and its value, exactly where it is rational."""

    tex: str
    exact: Fraction | None
    approximate: Decimal
    grouped: bool = False


class _Parser:
    """Recursive descent over `+ - * /`, parentheses, `sqrt(...)` and decimal numbers."""

    def __init__(self, tokens: Sequence[str]) -> None:
        self.tokens = tokens
        self.position = 0

    def _peek(self) -> str | None:
        return self.tokens[self.position] if self.position < len(self.tokens) else None

    def _take(self, expected: str | None = None) -> str:
        token = self._peek()
        if token is None or (expected is not None and token != expected):
            raise ValueError(f"expected {expected or 'a token'} at {self.position}")
        self.position += 1
        return token

    def whole(self) -> _Form:
        form = self._sum()
        if self._peek() is not None:
            raise ValueError(f"unparsed {self.tokens[self.position :]}")
        return form

    def _sum(self) -> _Form:
        form = self._product()
        while self._peek() in {"+", "-"}:
            operator = self._take()
            right = self._product()
            sign = 1 if operator == "+" else -1
            exact = None
            if form.exact is not None and right.exact is not None:
                exact = form.exact + sign * right.exact
            approximate = form.approximate + sign * right.approximate
            form = _Form(f"{form.tex} {operator} {right.tex}", exact, approximate)
        return form

    def _product(self) -> _Form:
        form = self._factor()
        while self._peek() in {"*", "/"}:
            operator = self._take()
            right = self._factor()
            both = form.exact is not None and right.exact is not None
            if operator == "*":
                # `955000*sqrt(...)` is set as `955000\sqrt{...}`, as a page writes it.
                joiner = "" if right.tex.startswith("\\sqrt") else " \\cdot "
                form = _Form(
                    f"{form.tex}{joiner}{right.tex}",
                    cast("Fraction", form.exact) * cast("Fraction", right.exact)
                    if both
                    else None,
                    form.approximate * right.approximate,
                )
            else:
                form = _Form(
                    f"\\frac{{{_bare(form)}}}{{{_bare(right)}}}",
                    cast("Fraction", form.exact) / cast("Fraction", right.exact)
                    if both
                    else None,
                    form.approximate / right.approximate,
                )
        return form

    def _factor(self) -> _Form:
        token = self._take()
        if token == "sqrt":
            self._take("(")
            inner = self._sum()
            self._take(")")
            return _Form(f"\\sqrt{{{inner.tex}}}", None, inner.approximate.sqrt())
        if token == "(":
            inner = self._sum()
            self._take(")")
            return _Form(f"({inner.tex})", inner.exact, inner.approximate, grouped=True)
        if token[0].isdigit():
            return _Form(token, Fraction(token), Decimal(token))
        raise ValueError(f"unexpected {token!r}")


def _bare(form: _Form) -> str:
    """A fraction's numerator or denominator, without the parentheses the claim needed."""
    return form.tex[1:-1] if form.grouped else form.tex


def closed_form(text: str) -> tuple[_Form, int]:
    """The longest closed form at the start of `text`, and how many characters it takes.

    A claim runs on into prose (`s(46) >= 7 is correct`), so tokens are read while they
    can be, and the longest run of them that parses is the form.
    """
    tokens: list[str] = []
    ends: list[int] = []
    position = 0
    while match := _TOKEN.match(text, position):
        tokens.append(match.group(1))
        position = match.end()
        ends.append(position)
    with localcontext() as context:
        context.prec = _PRECISION
        for count in range(len(tokens), 0, -1):
            try:
                return _Parser(tokens[:count]).whole(), ends[count - 1]
            except ValueError, ArithmeticError:
                continue
    raise ValueError(f"no closed form at {text[:40]!r}")


def cut(form: _Form) -> str:
    """The value's decimal, cut and never rounded, as README's tables cut it."""
    if form.exact is not None:
        return recent.digits(form.exact)
    return recent.digits(Fraction(form.approximate))


def _tex_decimal(decimal: str) -> str:
    return decimal.replace(recent.ELLIPSIS, "\\ldots")


def _bound(n: int, relation: str, text: str, form: _Form) -> Bound:
    decimal = cut(form)
    return Bound(
        n=n,
        relation=relation,
        exact=" ".join(text.split()),
        decimal=decimal,
        tex=f"s({n}) {TEX_RELATIONS[relation]} {form.tex}",
        value=form.exact,
    )


def _agrees(form: _Form, stated: str) -> bool:
    """Whether a claim's decimal is the form's, rounded or cut at the claim's places."""
    step = Decimal(10) ** -len(stated.split(".", 1)[1])
    with localcontext() as context:
        context.prec = _PRECISION
        written = {
            form.approximate.quantize(step, rounding=rounding)
            for rounding in (ROUND_DOWN, ROUND_HALF_UP, ROUND_HALF_EVEN)
        }
    return Decimal(stated) in written


def claimed_bound(claim: str, n: int) -> Bound | None:
    """The first bound the claim states on `s(n)`, with the claim's own relation.

    None where the claim states none on this `n` in a form this reads. A decimal the claim
    states beside the form (`= 3.826447410572939`) is checked against it, so a misread form
    fails the render rather than printing a wrong number.
    """
    text = " ".join(claim.split())
    for match in _CLAIMED.finditer(text):
        if int(match.group(1)) != n:
            continue
        try:
            form, length = closed_form(text[match.end() :])
        except ValueError:
            continue
        written = text[match.end() : match.end() + length]
        stated = _STATED.match(text, match.end() + length)
        if stated and not _agrees(form, stated.group(1)):
            raise ValueError(f"s({n}): {written!r} is not the stated {stated.group(1)}")
        return _bound(n, RELATIONS[match.group(2)], written, form)
    return None


def inline(bound: Bound) -> str:
    """A bound for running text: a short rational with its slash, else its decimal."""
    relation = TEX_RELATIONS[bound.relation]
    if bound.value is not None and len(bound.exact) <= 16:
        if bound.exact == bound.decimal:
            return f"s({bound.n}) {relation} {bound.exact}"
        return f"s({bound.n}) {relation} {bound.exact} = {_tex_decimal(bound.decimal)}"
    return f"s({bound.n}) {relation} {_tex_decimal(bound.decimal)}"


# --- The record ---------------------------------------------------------------------------


@cache
def cached_records() -> recent.Records:
    """The register, bibliography and case records, read once per process."""
    return recent.load_records()


def _lines(path: Path, pattern: str) -> dict[str, int]:
    """The line on which each id is opened, by id: where a permalink should land."""
    found: dict[str, int] = {}
    compiled = re.compile(pattern)
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if (match := compiled.match(line)) and match.group(1) not in found:
            found[match.group(1)] = number
    return found


@cache
def _evidence_lines() -> dict[str, int]:
    return _lines(EVIDENCE, r"^  - id: (E-[a-z0-9-]+)$")


@cache
def _result_lines() -> dict[str, int]:
    return _lines(RESULTS, r"^  - id: (T-\d{3})$")


def _link(relative: str) -> str:
    """A repository path's permalink at the build commit.

    `tree/` for a directory, which the record writes with a trailing slash, else `blob/`:
    decided from the path, never from the checkout, which may leave the path out.
    """
    if relative.endswith("/"):
        path = relative.rstrip("/")
        return f"{render_explainer.REPO_URL}/tree/{render_explainer.link_revision()}/{path}"
    return render_explainer.repo_file(REPO / relative)


def _anchored(path: Path, line: int) -> str:
    return f"{_link(path.relative_to(REPO).as_posix())}#L{line}"


def _case_file(n: int) -> str:
    return f"{citations.record_name(n)}.md"


def _case_link(n: int) -> Link:
    return Link(_case_file(n), _link(f"packing/frontier/{_case_file(n)}"), "case")


def _declared(path: str) -> str | None:
    """A retained source path as a repository path, a directory with its slash; else None.

    Evidence writes these packing-relative (`resources/web/...`) or repository-relative,
    sometimes followed by prose, and a directory without its slash: a path whose last part
    has no suffix is a directory.
    """
    head = path.split(maxsplit=1)[0].rstrip(",;") if path.strip() else ""
    relative = head if head.startswith("packing/") else f"packing/{head}"
    if not relative.startswith("packing/resources/"):
        return None
    if not relative.endswith("/") and not PurePosixPath(relative).suffix:
        relative += "/"
    return relative


def _retained(entry: Mapping[str, Any]) -> list[str]:
    proof = entry.get("proof")
    paths = [entry.get("certificate"), proof.get("source") if isinstance(proof, dict) else None]
    return [found for path in paths if path and (found := _declared(str(path))) is not None]


def _label(relative: str) -> str:
    for prefix in ("packing/resources/web/", "packing/resources/"):
        if relative.startswith(prefix):
            return relative.removeprefix(prefix)
    return relative


def _scope(record: Mapping[str, Any]) -> tuple[int, ...]:
    return tuple(sorted(scope_values(dict(record["scope"]))))


def cases_text(values: Sequence[int]) -> str:
    """README's `n` cell as plain text: its ranges and counts, without the case link."""
    return re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", recent.cases_cell(list(values)))


def _record_links(record: Mapping[str, Any], records: recent.Records) -> tuple[Link, ...]:
    rid = str(record["id"])
    values = _scope(record)
    links: list[Link] = []
    if len(values) <= recent.SHORT_LIST:
        links.extend(_case_link(n) for n in values)
    links.append(Link("results.yaml", _anchored(RESULTS, _result_lines()[rid]), "register"))
    evidence_lines = _evidence_lines()
    links.extend(
        Link(str(item), _anchored(EVIDENCE, evidence_lines[str(item)]), "evidence")
        for item in record["evidence"]
    )
    review = record.get("review_artifact")
    if review:
        links.append(Link(PurePosixPath(str(review)).name, _link(str(review)), "review"))
    retained: dict[str, None] = {}
    for item in record["evidence"]:
        retained.update(dict.fromkeys(_retained(records.register.evidence[str(item)])))
    links.extend(Link(_label(path), _link(path), "source") for path in retained)
    return tuple(links)


def _paths(record: Mapping[str, Any], field: str, kind: str) -> tuple[Link, ...]:
    return tuple(Link(str(path), _link(str(path)), kind) for path in record.get(field) or [])


def _prose(value: object) -> str:
    return " ".join(str(value).split())


def bound_of(record: Mapping[str, Any], records: recent.Records) -> Bound | None:
    """The one bound a register entry states, for an entry about one `n`, else None.

    An entry is a bound where its evidence claims one (`render_recent_results.BOUND_CLAIMS`)
    and its claim states it on its `n`; a rigidity, an exclusion or a whole family is not.
    """
    values = _scope(record)
    if len(values) != 1:
        return None
    claims = {records.register.evidence[str(item)].get("claim") for item in record["evidence"]}
    if not claims & recent.BOUND_CLAIMS:
        return None
    return claimed_bound(str(record["claim"]), values[0])


def verified_lower(n: int, records: recent.Records) -> Bound:
    """A case's verified lower bound, with the relation the register claims for it.

    A case record states a value, not a relation, so the bound reads `≥` unless a register
    entry carrying the bound's own evidence claims that same value strictly, as `T-037`
    claims `s(11) > 31/8`. `value` is the exact form where it is rational; a closed form
    this does not read, such as a `root(...)`, is shown by its decimal.
    """
    bound = records.cases[n]["verified_lower_bound"]
    magnitude = recent.magnitude(bound)
    exact = bound.get("exact_form")
    written = str(exact if exact is not None else bound["value"])
    form = _whole(str(exact)) if exact is not None else None
    relation = "≥"
    register = records.register
    own = citations.own_evidence(bound["evidence"], register)
    for rid in citations.results_carrying(n, own, register.results):
        claimed = bound_of(records.results[rid], records)
        if claimed is None or claimed.n != n or claimed.relation != ">":
            continue
        if claimed.value == magnitude or claimed.exact == written:
            relation = ">"
    decimal = recent.digits(magnitude)
    shown = form.tex if form is not None else _tex_decimal(decimal)
    return Bound(
        n=n,
        relation=relation,
        exact=written,
        decimal=decimal,
        tex=f"s({n}) {TEX_RELATIONS[relation]} {shown}",
        value=form.exact if form is not None else None,
    )


def _whole(text: str) -> _Form | None:
    """The closed form `text` is, entire, or None where this does not read it (a root)."""
    try:
        form, length = closed_form(text)
    except ValueError:
        return None
    return form if length == len(text) else None


#: The holder named where a case's bound is derived from others rather than held by one.
DERIVED = "a bound derived from others"


class Holder(NamedTuple):
    """Who holds a case's bound now: the credit, and the register entries it rests on."""

    credit: str
    results: tuple[str, ...]

    def __str__(self) -> str:
        return f"{', '.join(self.results)}, {self.credit}" if self.results else self.credit


def _lower_holder(n: int, records: recent.Records) -> Holder:
    """The verified lower bound's holder and results, as `verified_lane` credits them."""
    lane = recent.verified_lane(n, records.cases[n], records)
    return Holder(lane.holder or DERIVED, tuple(re.findall(r"T-\d{3}", lane.results)))


def _upper_holder(n: int, records: recent.Records) -> Holder:
    """The verified upper bound's holder: the entries carrying its own evidence.

    The evidence is read through `render_recent_results.held`, whose `upper` is what the
    standing column reads, so no value is taken from the ceiling.
    """
    register = records.register
    own = citations.own_evidence(sorted(recent.held(n, records).upper), register)
    ids = tuple(citations.results_carrying(n, own, register.results))
    named = [
        credit_line(records.results[rid], records.sources)
        if records.results[rid].get("attribution")
        else citations.PROJECT_NAME
        for rid in ids
    ]
    return Holder("; ".join(dict.fromkeys(named)) or DERIVED, ids)


def superseded_by(
    record: Mapping[str, Any], records: recent.Records
) -> tuple[str, tuple[str, ...]]:
    """The case's current holder, for an entry whose bound no longer holds it, and its results.

    Read from the lane the entry's bound belongs to: the verified lower bound's holder from
    `verified_lane`, for a lower bound or an exact value, else the verified upper bound's.
    A holder of every `n` in scope is named once (`T-043, Guzhou0806 after ...`); different
    holders are named case by case (`n = 17: ...; n = 18: ...`).
    """
    claims = {records.register.evidence[str(item)].get("claim") for item in record["evidence"]}
    lower = bool(claims & {"lower-bound", "exact-value"})
    holders = {
        n: _lower_holder(n, records) if lower else _upper_holder(n, records)
        for n in _scope(record)
        if n in records.cases
    }
    distinct = list(dict.fromkeys(holders.values()))
    results = tuple(dict.fromkeys(rid for holder in distinct for rid in holder.results))
    if len(distinct) == 1:
        return str(distinct[0]), results
    return "; ".join(f"n = {n}: {holder}" for n, holder in holders.items()), results


def _ai_assistance(record: Mapping[str, Any], sources: Mapping[str, Any]) -> str | None:
    keys = (record.get("attribution") or {}).get("source_keys") or []
    statements = [statement for key in keys if (statement := said(sources[key])) is not None]
    return " ".join(dict.fromkeys(sentence for sentence, _ in statements)) or None


def _lineage(record: Mapping[str, Any], sources: Mapping[str, Any]) -> Lineage:
    if not record.get("attribution"):
        return THIS_PROJECT
    lineage = source_lineage(record, sources)
    if lineage is None:
        typed = [
            sources[key].get("lineage")
            for key in record["attribution"]["source_keys"]
            if sources[key].get("lineage")
        ]
        lineage = typed[0] if typed else PREDATES
    return cast("Lineage", lineage)


def build_result(
    record: Mapping[str, Any], records: recent.Records, recent_ids: set[str]
) -> Result:
    """One register entry as the page shows it."""
    sources = records.sources
    ours = not record.get("attribution")
    values = _scope(record)
    bound = bound_of(record, records)
    standing = recent.standing(record, records)
    superseded = superseded_by(record, records) if standing == recent.SUPERSEDED else None
    attribution = record.get("attribution") or {}
    return Result(
        id=str(record["id"]),
        n_values=values,
        cases=cases_text(values),
        headline=str(record["headline"]),
        claim=_prose(record["claim"]),
        bound=bound,
        verification=str(record["verification"]),
        confirmation=str(record["confirmation"]),
        significance=int(record["significance"]["score"]),
        novelty=str(record["novelty"]),
        ours=ours,
        credit=citations.PROJECT_NAME if ours else credit_line(record, sources),
        ai_assistance=None if ours else _ai_assistance(record, sources),
        lineage=_lineage(record, sources),
        relation=recent.relation(record, records)
        if recent.is_recent_by_others(record)
        else None,
        standing=standing,
        superseded_by=superseded[0] if superseded else None,
        reported=str(record["verification"]) == "V0",
        exact_value=bound is not None and bound.relation == "=",
        recent=str(record["id"]) in recent_ids,
        established=str(record["established"]) if record.get("established") else None,
        published=str(attribution["published"]) if attribution else None,
        registered=str(record["registered"]),
        next_rung=_prose(record["next_rung"]),
        composition=_prose(record["composition"]) if record.get("composition") else None,
        records=_record_links(record, records),
        artifacts=_paths(record, "artifacts", "artifact"),
        controls=_paths(record, "controls", "control"),
        superseded_by_results=superseded[1] if superseded else (),
    )


def _declared_rung(record: Mapping[str, Any], axis: str) -> int:
    if axis == "S":
        return int(record["significance"]["score"])
    return int(str(record["verification" if axis == "V" else "confirmation"])[1:])


def rung_counts(results: Iterable[Mapping[str, Any]]) -> tuple[RungCount, ...]:
    """How many results stand at each declared rung of each axis, ours and others' apart."""
    listed = list(results)
    counts: list[RungCount] = []
    for axis in ("V", "C", "S"):
        ladder = significance.rungs(axis)
        undefined = {_declared_rung(record, axis) for record in listed} - set(ladder)
        if undefined:
            raise ValueError(f"epistemics.md defines no {axis} rung {sorted(undefined)}")
        for rung, row in sorted(ladder.items()):
            at = [record for record in listed if _declared_rung(record, axis) == rung]
            counts.append(
                RungCount(
                    axis=cast("Literal['V', 'C', 'S']", axis),
                    rung=rung,
                    label=row.meaning,
                    definition=row.support or row.meaning,
                    ours=sum(not record.get("attribution") for record in at),
                    others=sum(bool(record.get("attribution")) for record in at),
                )
            )
    return tuple(counts)


def atlas_totals() -> AtlasTotals:
    """The hundred-case totals the atlas composite states, read rather than recounted."""
    figure = json.loads(COMPOSITE.read_text(encoding="utf-8"))["figure"]
    composite = next(item for item in figure["composites"] if item["stem"] == ATLAS_STEM)
    cases = int(composite["range"]["count"])
    proved = int(composite["totals"]["proved_optimal"])
    return AtlasTotals(
        cases=cases,
        proved=proved,
        open=cases - proved,
        recent_verified_lower=int(composite["totals"]["lower_bound_recent_result"]),
    )


# --- Notable sources ----------------------------------------------------------------------


def _represented(item: str) -> Link:
    """A coverage entry's `represented_by` path, packing-relative, as a link."""
    if " through " in item:
        first, last = (PurePosixPath(part.strip()).name for part in item.split(" through "))
        return Link(f"{first} to {last}", _link("packing/frontier/"), "cases")
    relative = f"packing/{item}"
    name = PurePosixPath(item).name
    if re.fullmatch(r"n-\d{3}\.md", name):
        return Link(name, _link(relative), "case")
    return Link(name + ("/" if item.endswith("/") else ""), _link(relative), "record")


def _release(source: Mapping[str, Any]) -> SourceRelease:
    local = f"packing/{source['local']}"
    return SourceRelease(
        title=str(source["title"]),
        url=str(source["url"]),
        reviewed=str(source["reviewed"]),
        superseded=source["disposition"] == "superseded-covered",
        archive=Link(_label(local), _link(local), "archive"),
        published=str(source["source_date"]) if source.get("source_date") else None,
    )


def notable_sources(sources: Mapping[str, Mapping[str, Any]]) -> tuple[NotableSource, ...]:
    """The registry's cards, with their reviewed releases and the records citing them."""
    registry = safe_load(NOTABLE_SOURCES.read_text(encoding="utf-8"))["sources"]
    coverage = {
        str(source["id"]): source
        for source in safe_load(COVERAGE.read_text(encoding="utf-8"))["sources"]
    }
    cards: list[NotableSource] = []
    for entry in registry:
        covered = sorted(
            (coverage[str(item)] for item in entry.get("coverage") or []),
            key=lambda source: str(source.get("source_date") or source["reviewed"]),
            reverse=True,
        )
        cited = [key for key in entry["keys"] if key in sources]
        credit = entry.get("credit") or credit_line(
            {"attribution": {"source_keys": cited}}, sources
        )
        cases = dict.fromkeys(
            _represented(str(item)) for source in covered for item in source["represented_by"]
        )
        retained = str(entry["retained"])
        cards.append(
            NotableSource(
                id=str(entry["id"]),
                title=str(entry["title"]),
                kind=entry["kind"],
                url=str(entry["url"]),
                credit=str(credit),
                summary=_prose(entry["summary"]),
                archive=Link(_label(retained), _link(retained), "archive"),
                releases=tuple(_release(source) for source in covered),
                cases=tuple(cases),
            )
        )
    return tuple(cards)


# --- The explainer ------------------------------------------------------------------------


#: The months `PUBLICATION_HISTORY` spells out, in English whatever the locale.
MONTHS = (
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
)


def iso_day(text: str) -> str:
    """A `PUBLICATION_HISTORY` date, `September 5, 2026`, as an ISO day."""
    match = re.fullmatch(r"([A-Z][a-z]+) (\d{1,2}), (\d{4})", text)
    if match is None or match.group(1) not in MONTHS:
        raise ValueError(f"PUBLICATION_HISTORY date {text!r} is not written `Month D, YYYY`")
    month = MONTHS.index(match.group(1)) + 1
    return date(int(match.group(3)), month, int(match.group(2))).isoformat()


@cache
def explainer_edition() -> ExplainerEdition:
    """The explainer's lead result against the case record, for its card and its notice."""
    records = cached_records()
    lead = render_explainer.LEAD_RESULT
    lead_bound = bound_of(records.results[lead], records)
    if lead_bound is None:
        raise ValueError(f"{lead}, the explainer's lead result, states no bound on one s(n)")
    n = lead_bound.n
    lane = recent.verified_lane(n, records.cases[n], records)
    current = tuple(re.findall(r"T-\d{3}", lane.results))
    history = sorted(PUBLICATION_HISTORY, key=lambda entry: iso_day(entry.first_published))
    introduced = next(
        (entry for entry in history if re.search(rf"\b{lead}\b", entry.result_scope)), None
    )
    if introduced is None:
        raise ValueError(f"no edition in PUBLICATION_HISTORY names {lead}")
    return ExplainerEdition(
        lead_result=lead,
        lead_bound=lead_bound,
        current_bound=verified_lower(n, records),
        current_credit=lane.holder,
        current_results=current,
        is_current=lead in current,
        first_published=iso_day(history[0].first_published),
        edition=introduced.version,
        edition_first_published=iso_day(introduced.first_published),
    )


# --- The model ----------------------------------------------------------------------------


@cache
def load() -> OverviewData:
    """Read the record once and return the model; cached per process."""
    records = cached_records()
    register = records.register.results
    ours = recent.ours(records)
    others = recent.by_others(records)
    recent_ids = {str(record["id"]) for record in (*ours, *others)}
    results = {
        str(record["id"]): build_result(record, records, recent_ids) for record in register
    }
    groups = tuple(
        ResultGroup(
            key=group.key,
            title=group.title,
            results=tuple(results[str(record["id"])] for record in group.records),
        )
        for group in render_results.grouped_results(register, records.sources)
    )
    return OverviewData(
        edition=PUBLICATION_EDITION,
        data_revision=DATA_REVISION,
        recent_ours=tuple(results[str(record["id"])] for record in ours),
        recent_others=tuple(results[str(record["id"])] for record in others),
        groups=groups,
        rung_counts=rung_counts(register),
        atlas=atlas_totals(),
        sources=notable_sources(records.sources),
        explainer=explainer_edition(),
    )
