"""The overview page's facts, read from the record and nowhere else.

The overview states the problem's central bracket, the headline results, a table of
every registered result, and counts of how each is verified. Each of those is a view of
something the repository already records and already gates:

- results, their rungs, credit and grouping: `frontier/results.yaml`, grouped and
  ordered by `devtools.render_results` so the page and `RESULTS.md` cannot disagree;
- case bounds and status: the `SquarePackingCase/v2` records in `frontier/n-NNN.md`,
  loaded by `devtools.render_research_tables.load_cases`;
- which lower bounds are recent: `atlas/known-best/bound-citations.json`, which the
  atlas star reads too;
- evidence, retained source copies and reviews: `frontier/evidence.yaml`;
- each result's standing, the survey's counts and the reported bounds awaiting a replay:
  `devtools.render_recent_results`, the functions README's generated tables use, so the
  page and README cannot disagree about any of them.

Counts are of *declared* rungs. `check_results` accepts a declared rung below the one
it derives when a `composition` note explains why, so re-deriving here would disagree
with the record; the page runs after that gate instead.
"""

from __future__ import annotations

import html
import json
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

from devtools import render_results
from devtools.migrate_math import classify
from devtools.render_explainer import repo_file
from devtools.render_recent_results import (
    RecentCounts,
    Row,
    load_records,
    recent_counts,
    recent_rows,
    standing,
)
from devtools.render_research_tables import load_cases
from devtools.result_credit import credit_line
from devtools.significance import headline as first_sentence
from sqpack.yamlio import safe_load

PACKING = Path(__file__).resolve().parents[1]
REPO = PACKING.parent
RESULTS = PACKING / "frontier" / "results.yaml"
EVIDENCE = PACKING / "frontier" / "evidence.yaml"
BIBLIOGRAPHY = PACKING / "resources" / "bibliography.yaml"
CITATIONS = PACKING / "atlas" / "known-best" / "bound-citations.json"
FRONTIER = PACKING / "frontier"

#: Typography the page prints, written as escapes for the reason `render_results` gives:
#: a literal one is invisible in a diff and ambiguous on sight.
APOSTROPHE = "\u2019"
EN_DASH = "\u2013"

#: Every file this module reads, for the renderer's declared inputs.
INPUTS: tuple[Path, ...] = (
    Path(__file__).resolve(),
    RESULTS,
    EVIDENCE,
    BIBLIOGRAPHY,
    CITATIONS,
    FRONTIER,
    PACKING / "devtools" / "render_results.py",
    PACKING / "devtools" / "result_credit.py",
    PACKING / "devtools" / "render_recent_results.py",
    PACKING / "devtools" / "migrate_math.py",
    PACKING / "devtools" / "significance.py",
    PACKING / "devtools" / "render_research_tables.py",
    REPO / "epistemics.md",
)

#: A result about more cases than this links to the frontier atlas, not to each case.
CASE_LINKS = 4

#: The ASCII relations the register's prose uses, and their LaTeX.
_RELATIONS = {">=": r"\ge", "<=": r"\le", ">": ">", "<": "<", "=": "="}
_NUMBER = r"[0-9]+(?:/[0-9]+|\.[0-9]+(?:\.\.\.|…)?)?"
_VALUE = rf"{_NUMBER}(?:\s*\+\s*[0-9]+/sqrt\([0-9]+\))?"
_RELATION = r"(?:>=|<=|>|<|=)"
#: The runs of register prose that are mathematics: a bound on one or more `s(n)`, a
#: range of `N`, a grid's `k x k`, a side compared with a value, a bare `s(n)`, and `n = 5`.
MATH = re.compile(
    rf"(?:s\([0-9]+\),\s*)*s\([0-9]+\)\s*{_RELATION}\s*{_VALUE}"
    rf"|\b[0-9]+\s*<=\s*N\s*<=\s*[0-9]+"
    rf"|\b[0-9]+ x [0-9]+(?= grid)"
    rf"|(?<=side )>=\s*{_VALUE}"
    r"|\bs\((?:[0-9]+|N|n)\)"
    r"|\b[nN] = [0-9]+\b"
)


def prose_tex(run: str) -> str:
    """One run matched by `MATH`, rewritten from the register's ASCII into TeX."""
    run = re.sub(r"([0-9]+)/sqrt\(([0-9]+)\)", r"\1/\\sqrt{\2}", run)
    run = re.sub(r"(?<=[0-9]) x (?=[0-9])", r" \\times ", run)
    run = re.sub(r"\s*(>=|<=|>|<|=)\s*", lambda m: f" {_RELATIONS[m.group(1)]} ", run)
    return run.replace("...", r"\ldots").replace("…", r"\ldots").strip()


def math_html(tex: str, *, display: bool = False) -> str:
    """kpress's own math markup for `tex`, for math inside a raw HTML block.

    kpress sets `$…$` as math only in Markdown text; inside an HTML block it stays
    literal. This is the span its Markdown renderer emits: TeX that the page's KaTeX
    scripts enhance, with server-rendered MathML as the no-script fallback.
    """
    from kpress.format.markdown import (  # noqa: PLC0415
        _render_math,  # pyright: ignore[reportPrivateUsage]
    )

    return _render_math(tex, display="display" if display else "inline", math="auto", env={})


#: One inline code span in register prose. Headlines write their mathematics this way
#: (`s(11) ≥ 31/8`), as README and `RESULTS.md` print them.
_CODE_SPAN = re.compile(r"`([^`\n]+)`")


def _prose_html(text: str) -> str:
    """Escape plain register prose, setting each ASCII mathematical run as inline math."""
    parts: list[str] = []
    last = 0
    for match in MATH.finditer(text):
        parts.append(html.escape(text[last : match.start()], quote=False))
        parts.append(math_html(prose_tex(match.group(0))))
        last = match.end()
    parts.append(html.escape(text[last:], quote=False))
    return "".join(parts)


def _code_span_html(content: str) -> str:
    """A code span as math when `migrate_math` reads it as mathematics, else as code."""
    classified = classify(content)
    if classified.kind == "math" and classified.latex:
        return math_html(classified.latex)
    return f"<code>{html.escape(content, quote=False)}</code>"


def tex_bounds(text: str) -> str:
    """Escape register prose for HTML and set each mathematical run in it as inline math.

    A code span is judged by `devtools.migrate_math.classify`, the rule the reader
    documents were migrated by, so a headline's `` `s(11) ≥ 31/8` `` is set as math and
    an identifier stays code; prose outside code spans is read as before.
    """
    parts: list[str] = []
    last = 0
    for match in _CODE_SPAN.finditer(text):
        parts.append(_prose_html(text[last : match.start()]))
        parts.append(_code_span_html(match.group(1)))
        last = match.end()
    parts.append(_prose_html(text[last:]))
    return "".join(parts)


def _line_of(path: Path, needle: str) -> int:
    """The 1-based line of the first line containing `needle`, for a permalink anchor."""
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if needle in line:
            return number
    raise SystemExit(f"{path.name} has no line containing {needle!r}")


def line_link(path: Path, needle: str) -> str:
    """A permalink to the line of `path` where `needle` first appears."""
    return f"{repo_file(path)}?plain=1#L{_line_of(path, needle)}"


@dataclass(frozen=True)
class Link:
    label: str
    url: str
    title: str = ""


@dataclass
class Result:
    """One register entry as the overview shows it."""

    record: dict
    group: str
    credit: str
    ours: bool
    records: list[Link] = field(default_factory=list)
    standing: str = ""
    """Whether a case bound rests on the result now, and if not, why not:
    `render_recent_results.standing`, the word README's and `RESULTS.md`'s tables print."""

    @property
    def id(self) -> str:
        return self.record["id"]

    @property
    def summary(self) -> str:
        return self.record.get("headline") or first_sentence(self.record)

    @property
    def date(self) -> str:
        record = self.record
        return str(
            record.get("registered")
            or record.get("attribution", {}).get("published")
            or record["significance"]["scored"]
        )

    @property
    def published(self) -> str | None:
        """When a result by others was published, as its attribution records it."""
        attribution = self.record.get("attribution")
        return str(attribution["published"]) if attribution else None

    @property
    def dated(self) -> tuple[str, str]:
        """The date a reader is shown and what it is: publication for a result by
        others, as README's Results by Others dates it; establishment for this
        project's, as its New Results does."""
        if self.published is not None:
            return "published", self.published
        return "established", str(self.record.get("established") or self.date)

    @property
    def novelty(self) -> str:
        return str(self.record["novelty"])

    @property
    def scope(self) -> str:
        """The result's `n`, with runs of three or more consecutive counts as ranges."""
        scope = self.record["scope"]
        if "n_values" not in scope:
            return f"{scope['n_min']}{EN_DASH}{scope['n_max']}"
        return compress(scope["n_values"])

    @property
    def first_n(self) -> int:
        scope = self.record["scope"]
        return min(scope["n_values"]) if "n_values" in scope else scope["n_min"]


def compress(values: list[int]) -> str:
    """`18, 19, 20, 21, 26` as `18-21, 26` (en dash): a run of three or more becomes a range."""
    runs: list[list[int]] = []
    for n in sorted(values):
        if runs and n == runs[-1][-1] + 1:
            runs[-1].append(n)
        else:
            runs.append([n])
    return ", ".join(
        f"{run[0]}{EN_DASH}{run[-1]}" if len(run) >= 3 else ", ".join(map(str, run))
        for run in runs
    )


@dataclass
class Overview:
    results: list[Result]
    cases: dict[int, dict]
    recent_lower: frozenset[int]
    groups: list[tuple[str, list[Result]]]
    recent: list[Row] = field(default_factory=list)
    """Every case `n <= 100` with a recent lower bound in either lane, as README's survey
    table lists them: `render_recent_results.recent_rows`."""

    @property
    def counts(self) -> RecentCounts:
        """The survey's four counts, as README's summary quotes them."""
        return recent_counts(self.recent)

    @property
    def awaiting_replay(self) -> list[Row]:
        """The recent cases whose reported lower bound says something the verified one
        does not: a source's claim still waiting on a replay here."""
        return [row for row in self.recent if row.shows_reported]


def _evidence() -> dict[str, dict]:
    return {
        entry["id"]: entry
        for entry in safe_load(EVIDENCE.read_text(encoding="utf-8"))["evidence"]
    }


def _repo_path(path: str) -> Path | None:
    """A record's path, which may be packing-relative or repository-relative."""
    for base in (REPO, PACKING):
        candidate = base / path
        if candidate.exists():
            return candidate
    return None


def _records(record: dict, evidence: dict[str, dict]) -> list[Link]:
    """The places a reader checks a result: case files, evidence, sources, reviews."""
    links: list[Link] = []
    scope = record["scope"]
    if "n_values" in scope and len(scope["n_values"]) > CASE_LINKS:
        links.append(Link(f"{len(scope['n_values'])} cases", "frontier.html"))
    elif "n_values" in scope:
        links.extend(
            Link(f"n = {n}", repo_file(FRONTIER / f"n-{n:03d}.md")) for n in scope["n_values"]
        )
    else:
        links.append(Link(f"n = {scope['n_min']}{EN_DASH}{scope['n_max']}", "frontier.html"))
    links.append(Link("register", line_link(RESULTS, f"id: {record['id']}"), record["id"]))
    seen: set[str] = set()
    extra: list[Link] = []
    for number, evidence_id in enumerate(record["evidence"], start=1):
        entry = evidence.get(evidence_id)
        if entry is None:
            continue
        links.append(
            Link(f"evidence {number}", line_link(EVIDENCE, f"id: {evidence_id}"), evidence_id)
        )
        proof = entry.get("proof") or {}
        for label, path in (
            ("source", proof.get("source")),
            ("review", proof.get("audit_record")),
        ):
            if path and path not in seen and (resolved := _repo_path(path)) is not None:
                seen.add(path)
                extra.append(Link(label, repo_file(resolved), path))
    review = record.get("review_artifact")
    if review and review not in seen and (resolved := _repo_path(review)) is not None:
        extra.append(Link("review", repo_file(resolved), review))
    extra.sort(key=lambda link: link.label == "review")
    for label in ("source", "review"):
        same = [i for i, link in enumerate(extra) if link.label == label]
        if len(same) > 1:
            for number, i in enumerate(same, start=1):
                extra[i] = Link(f"{label} {number}", extra[i].url, extra[i].title)
    links.extend(extra)
    return links


def load() -> Overview:
    """Everything the overview shows, grouped as `RESULTS.md` groups it."""
    register = safe_load(RESULTS.read_text(encoding="utf-8"))
    sources = render_results.load_sources()
    evidence = _evidence()
    records = load_records()
    results: list[Result] = []
    groups: list[tuple[str, list[Result]]] = []
    for title, members in render_results.grouped_results(register, sources):
        group = [
            Result(
                r,
                group=title,
                credit=(
                    credit_line(r, sources).replace(r"\|", "|")
                    if r.get("attribution")
                    else "This project"
                ),
                ours=not r.get("attribution"),
                records=_records(r, evidence),
                standing=standing(r, records),
            )
            for r in members
        ]
        groups.append((title, group))
        results.extend(group)

    cases = {case["n"]: case for case in load_cases()}
    citations = json.loads(CITATIONS.read_text(encoding="utf-8"))["citations"]["entries"]
    recent = frozenset(
        entry["n"] for entry in citations if entry["lower"] and entry["lower"]["recent"]
    )
    return Overview(
        results=results,
        cases=cases,
        recent_lower=recent,
        groups=groups,
        recent=recent_rows(records),
    )


@dataclass(frozen=True)
class Stats:
    total: int
    ours: int
    others: int
    verification: Counter[str]
    confirmation_ours: Counter[str]
    confirmation_others: Counter[str]
    cases_1_100_proved: int
    cases_1_100_open: int
    cases_total: int
    cases_proved: int
    recent_lower_1_100: int
    recent_lower_total: int


def stats(overview: Overview) -> Stats:
    """Declared-rung counts and case counts; nothing re-derived."""
    ours = [r for r in overview.results if r.ours]
    others = [r for r in overview.results if not r.ours]
    status = {n: case["status"] for n, case in overview.cases.items()}
    first_hundred = [n for n in status if n <= 100]
    return Stats(
        total=len(overview.results),
        ours=len(ours),
        others=len(others),
        verification=Counter(r.record["verification"] for r in overview.results),
        confirmation_ours=Counter(r.record["confirmation"] for r in ours),
        confirmation_others=Counter(r.record["confirmation"] for r in others),
        cases_1_100_proved=sum(status[n] == "proved" for n in first_hundred),
        cases_1_100_open=sum(status[n] != "proved" for n in first_hundred),
        cases_total=len(status),
        cases_proved=sum(s == "proved" for s in status.values()),
        recent_lower_1_100=sum(n <= 100 for n in overview.recent_lower),
        recent_lower_total=len(overview.recent_lower),
    )
