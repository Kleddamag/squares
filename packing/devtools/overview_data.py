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
- evidence, retained source copies and reviews: `frontier/evidence.yaml`.

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
from devtools.render_explainer import repo_file
from devtools.render_research_tables import load_cases
from devtools.significance import headline as first_sentence
from devtools.significance import scope_label
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
    PACKING / "devtools" / "significance.py",
    PACKING / "devtools" / "render_research_tables.py",
    REPO / "epistemics.md",
)

#: The ASCII relations the register's prose uses, and their LaTeX.
_RELATIONS = {">=": r"\ge", "<=": r"\le", ">": ">", "<": "<", "=": "="}
_BOUND = re.compile(
    r"\bs\((\d+)\)\s*(>=|<=|>|<|=)\s*([0-9]+(?:/[0-9]+|\.[0-9]+(?:\.\.\.|…)?)?)"
)


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


def tex_bounds(text: str) -> str:
    """Escape prose for HTML and set each `s(n) >= a/b` run in it as inline math."""

    def math(match: re.Match[str]) -> str:
        value = match.group(3).replace("...", r"\ldots").replace("…", r"\ldots")
        return math_html(f"s({match.group(1)}) {_RELATIONS[match.group(2)]} {value}")

    parts: list[str] = []
    last = 0
    for match in _BOUND.finditer(text):
        parts.append(html.escape(text[last : match.start()], quote=False))
        parts.append(math(match))
        last = match.end()
    parts.append(html.escape(text[last:], quote=False))
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
    def scope(self) -> str:
        return scope_label(self.record)


@dataclass
class Overview:
    results: list[Result]
    cases: dict[int, dict]
    recent_lower: frozenset[int]
    groups: list[tuple[str, list[Result]]]


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
    if "n_values" in scope:
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
    links.extend(sorted(extra, key=lambda link: link.label == "review"))
    return links


def load() -> Overview:
    """Everything the overview shows, grouped as `RESULTS.md` groups it."""
    register = safe_load(RESULTS.read_text(encoding="utf-8"))
    sources = render_results.load_sources()
    evidence = _evidence()
    results: list[Result] = []
    groups: list[tuple[str, list[Result]]] = []
    for title, members in render_results.grouped_results(register, sources):
        group = [
            Result(
                r,
                group=title,
                credit=(
                    render_results.credit(r, sources).replace(r"\|", "|")
                    if r.get("attribution")
                    else "This project"
                ),
                ours=not r.get("attribution"),
                records=_records(r, evidence),
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
    return Overview(results=results, cases=cases, recent_lower=recent, groups=groups)


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
