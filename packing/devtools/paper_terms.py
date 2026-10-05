"""Every term a paper uses is defined before it is used, in reading order.

The n = 11 papers form one series read in order, and the owner's rule for it is that
each concept is defined before it is used (plan-2026-10-05-n11-explainer-series.md,
§1 principle 3 and §9.4). A rule a reviewer has to remember is one the next revision
breaks, so each paper declares its terms in a registry beside its article,
`templates/<slug>-terms.yaml`, and this module holds the rendered page to it.

It reads the page a reader meets, not the Markdown: placeholders are filled, figure
facts are numbers, and section anchors are the ids KPress generated. It walks the paper's
`<article>` in document order, headings, prose, list items, table cells and figure
captions, and skips what is not exposition: the front (title and credits), the formats
row, navigation, footnotes, the Version History section, `<svg>` drawings, scripts and
MathML. A typeset formula is read as the TeX source the page carries, so a symbol's
pattern is a TeX pattern and a word's is a prose pattern, and neither matches the other.

A registry entry names a term, a pattern for its uses, the exact sentence that defines
it, the heading id of the section that sentence must stand in, the terms it requires,
and the earlier uses it allows, each one an exact substring with a reason: a roadmap or
preamble naming a later concept, a heading, or a link to the definition. The rules, each
reported by its number:

1. Each definition occurs exactly once, inside the section its anchor names.
2. No use precedes the definition except inside a declared forward substring, and every
   declared forward substring is one such use.
3. Each required term is registered and defined no later than the term requiring it.
4. Every bold run in the exposition is part of some term's definition, so a new
   definition has to enter the registry. A run-in head (a bold run that opens its block
   and ends with a full stop or a colon, such as **Theorem.** or a lemma's name) and a
   caption's **Figure N.** label a block rather than define a word, and are exempt.
5. A paper may ban bare forms (`banned`), each with its reason.
6. Across the series, `templates/n11-series-terms.yaml` names each shared concept's
   owner and the anchor of its derivation. A paper that does not own a concept it uses
   first meets it in a block that links the owner's page, and a symbol two papers define
   with different meanings is refused unless the series registry lists that clash.
7. Every formula is typeset. No TeX reaches the reader as text: a `$` or a TeX command
   (`\\gt`, `\\binom`) in the prose, the captions or the title means a formula the page's
   math pipeline never saw, such as a display formula run into its sentence or a
   caption's `$...$` in an HTML block that is not passed to it. A display formula is a
   Markdown `$$` block in every paper, so every display has the same spacing, overflow
   and print behaviour; Part I's `.tex-d` wrapper is refused.

`check_paper` runs rules 1-5 on one page; `check_math` runs rule 7 on one page's HTML,
the hero title included; `check_series` runs rule 6 on any number of pages;
`check_paper_anchors` checks that every cross-paper link (`devtools.paper_links`)
names a heading the target paper has. `tests/test_paper_terms.py` runs them on every
paper, one entry per paper.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field, replace
from html.parser import HTMLParser
from pathlib import Path
from typing import Literal, cast

from devtools import paper_links
from sqpack.yamlio import load_yaml

TEMPLATES = Path(__file__).with_name("templates")
#: The series registry: shared concepts, their owners, and the symbol clashes allowed.
SERIES = TEMPLATES / "n11-series-terms.yaml"
#: Why an earlier use may stand before a definition (plan §9.4).
FORWARD_REASONS = frozenset({"roadmap", "heading", "link-to-definition"})
#: The section a paper's version history stands in: a record of earlier editions, read as
#: a record, not exposition.
HISTORY_SECTION = "version-history"
Rule = Literal[1, 2, 3, 4, 5, 6, 7]

_BLOCKS = frozenset(
    {"h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "td", "th", "figcaption", "dt", "dd"}
)
_HEADINGS = {f"h{level}": level for level in range(1, 7)}
_VOID = frozenset(
    {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param"}
    | {"source", "track", "wbr"}
)
#: Containers whose whole subtree is not exposition.
_SKIPPED_TAGS = frozenset({"svg", "script", "style", "nav", "math", "template", "canvas"})
_SKIPPED_CLASSES = frozenset(
    {"hero", "doc-links", "kpress-footnotes", "kpress-math-semantic", "kpress-footnote-ref"}
)
#: Elements that carry a formula's TeX as their text.
_MATH_CLASSES = frozenset({"kpress-math-render", "tex", "tex-d"})
_DELIMITERS = re.compile(r"^\s*\\[(\[](.*?)\\[)\]]\s*$", re.DOTALL)
_FIGURE_LABEL = re.compile(r"^Figure \d+\.$")
_WHITESPACE = re.compile(r"\s+")


@dataclass(frozen=True)
class Block:
    """One block of the exposition as a reader meets it.

    `text` is the block's words with each formula written `$TeX$`; `prose` and `tex` are
    the same string with the formulas, or everything but their TeX, blanked to spaces, so
    an offset means the same place in all three.
    """

    index: int
    kind: str
    sections: tuple[str, ...]
    text: str
    prose: str
    tex: str
    bold: tuple[tuple[int, int], ...] = ()
    links: tuple[str, ...] = ()


@dataclass(frozen=True)
class Page:
    """A rendered paper's exposition, in order, and every heading id the page has."""

    blocks: tuple[Block, ...]
    heading_ids: frozenset[str]


@dataclass(frozen=True)
class Forward:
    """An earlier use a definition allows: an exact substring, and why it may stand."""

    text: str
    reason: str


@dataclass(frozen=True)
class Term:
    """One registered term: how it is used, where it is defined, and what it needs."""

    term: str
    uses: str
    defined_by: str
    anchor: str
    symbol: bool = False
    requires: tuple[str, ...] = ()
    forward: tuple[Forward, ...] = ()
    series: str | None = None

    def pattern(self) -> re.Pattern[str]:
        return re.compile(self.uses)


@dataclass(frozen=True)
class Banned:
    """A bare form a paper refuses anywhere in its exposition (rule 5): a prose pattern,
    or a TeX pattern when `symbol` is true, such as a symbol the series renamed."""

    pattern: str
    reason: str
    symbol: bool = False


@dataclass(frozen=True)
class Registry:
    """A paper's term registry, `templates/<slug>-terms.yaml`."""

    paper: str
    terms: tuple[Term, ...]
    banned: tuple[Banned, ...] = ()

    def term(self, name: str) -> Term | None:
        return next((term for term in self.terms if term.term == name), None)


@dataclass(frozen=True)
class Concept:
    """A concept the series shares: the paper that derives it, and where."""

    concept: str
    owner: str
    anchor: str


@dataclass(frozen=True)
class Series:
    """The series registry: shared concepts, and the symbol clashes the series accepts."""

    concepts: tuple[Concept, ...]
    clashes: Mapping[str, str] = field(default_factory=dict[str, str])

    def concept(self, name: str) -> Concept | None:
        return next((item for item in self.concepts if item.concept == name), None)


@dataclass(frozen=True)
class Finding:
    """One broken rule, with the term or text it is about, and the paper it is in when it
    is one paper's (a symbol clash is the series')."""

    rule: Rule
    subject: str
    message: str
    paper: str = ""

    def __str__(self) -> str:
        where = f"{self.paper}: " if self.paper else ""
        return f"{where}rule {self.rule}: {self.subject}: {self.message}"


def _normal(text: str) -> str:
    return _WHITESPACE.sub(" ", text)


class _Reader(HTMLParser):
    """Collects a page's exposition as `Block`s in document order."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.blocks: list[Block] = []
        self.heading_ids: set[str] = set()
        # The open elements: tag, whether it skips its subtree, whether it is a formula.
        self.stack: list[tuple[str, bool, bool]] = []
        self.skip_depth = 0
        self.math_depth = 0
        self.article_seen = False
        self.in_article = 0
        self.blocks_open: list[str] = []
        self.sections: list[tuple[int, str]] = []
        self.math_buffer: list[str] = []
        self.display = False
        self._reset()

    def _reset(self) -> None:
        self.text, self.prose, self.tex = "", "", ""
        self.bold_starts: list[int] = []
        self.bold: list[tuple[int, int]] = []
        self.links: list[str] = []

    def _append(self, piece: str, *, math: bool) -> None:
        if math:
            written = f"${piece}$"
            self.text += written
            self.prose += " " * len(written)
            self.tex += " " + piece + " "
            return
        piece = _normal(piece)
        if self.text.endswith(" ") and piece.startswith(" "):
            piece = piece[1:]
        if not self.text and piece.startswith(" "):
            piece = piece[1:]
        self.text += piece
        self.prose += piece
        self.tex += " " * len(piece)

    def _flush(self) -> None:
        in_history = any(anchor == HISTORY_SECTION for _, anchor in self.sections)
        if self.blocks_open and self.text.strip() and not in_history:
            self.blocks.append(
                Block(
                    index=len(self.blocks),
                    kind=self.blocks_open[-1],
                    sections=tuple(anchor for _, anchor in self.sections),
                    text=self.text,
                    prose=self.prose,
                    tex=self.tex,
                    bold=tuple(self.bold),
                    links=tuple(self.links),
                )
            )
        self._reset()

    def _active(self) -> bool:
        return (self.in_article > 0 or not self.article_seen) and self.skip_depth == 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = {name: value or "" for name, value in attrs}
        classes = frozenset(attributes.get("class", "").split())
        if tag in _HEADINGS and "id" in attributes:
            self.heading_ids.add(attributes["id"])
        if tag in _VOID:
            return
        if tag == "article" and self.skip_depth == 0:
            if not self.article_seen:
                self.blocks.clear()
                self._reset()
            self.article_seen = True
            self.in_article += 1
            self.stack.append((tag, False, False))
            return
        skipped = (
            tag in _SKIPPED_TAGS or bool(classes & _SKIPPED_CLASSES) or "hidden" in attributes
        )
        source = attributes.get("data-kpress-math-source")
        math = (bool(classes & _MATH_CLASSES) or source is not None) and not self.math_depth
        if skipped or not self._active():
            self.stack.append((tag, True, False))
            self.skip_depth += 1
            return
        if math:
            self.math_depth += 1
            if not self.blocks_open:
                # A displayed formula stands between blocks, as a block of its own.
                self._flush()
                self.blocks_open.append("math")
                self.display = True
            if source is not None:
                # A prepared formula names its source; its children are its geometry.
                self.math_buffer.append(source)
                self.skip_depth += 1
            self.stack.append((tag, source is not None, True))
            return
        self.stack.append((tag, False, False))
        if tag in _BLOCKS:
            self._flush()
            if tag in _HEADINGS:
                level = _HEADINGS[tag]
                while self.sections and self.sections[-1][0] >= level:
                    self.sections.pop()
                self.sections.append((level, attributes.get("id", "")))
            self.blocks_open.append(tag)
        elif tag in ("strong", "b"):
            self.bold_starts.append(len(self.text))
        elif tag == "a" and "href" in attributes:
            self.links.append(attributes["href"])

    def handle_endtag(self, tag: str) -> None:
        if tag in _VOID:
            return
        for depth in range(len(self.stack) - 1, -1, -1):
            if self.stack[depth][0] == tag:
                for closed, skipped, math in reversed(self.stack[depth:]):
                    self._close(closed, skipped=skipped, math=math)
                del self.stack[depth:]
                return

    def _close(self, tag: str, *, skipped: bool, math: bool) -> None:
        if skipped:
            self.skip_depth -= 1
        if math:
            self._end_math()
            return
        if skipped:
            return
        if tag == "article":
            self._flush()
            self.in_article -= 1
        elif tag in _BLOCKS:
            self._flush()
            if self.blocks_open:
                self.blocks_open.pop()
        elif tag in ("strong", "b") and self.bold_starts:
            self.bold.append((self.bold_starts.pop(), len(self.text)))

    def _end_math(self) -> None:
        self.math_depth = 0
        raw = "".join(self.math_buffer)
        self.math_buffer = []
        found = _DELIMITERS.match(raw)
        tex = _normal(found.group(1) if found else raw).strip()
        if tex and self.blocks_open:
            self._append(tex, math=True)
        if self.display:
            self._flush()
            self.blocks_open.pop()
            self.display = False

    def handle_data(self, data: str) -> None:
        if self.math_depth:
            if self.skip_depth == 0:
                self.math_buffer.append(data)
            return
        if self._active() and self.blocks_open:
            self._append(data, math=False)


def read_page(html: str) -> Page:
    """The exposition of a rendered paper, in reading order."""
    reader = _Reader()
    reader.feed(html)
    reader.close()
    blocks = tuple(
        Block(
            index=index,
            kind=block.kind,
            sections=block.sections,
            text=block.text,
            prose=block.prose,
            tex=block.tex,
            bold=block.bold,
            links=block.links,
        )
        for index, block in enumerate(reader.blocks)
    )
    return Page(blocks=blocks, heading_ids=frozenset(reader.heading_ids))


# --- registries ---


class RegistryError(ValueError):
    """A registry that is not in the form `devtools.paper_terms` reads."""


def _list(value: object, *, where: str) -> list[object]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise RegistryError(f"{where}: expected a list")
    return cast(list[object], value)


def _strings(value: object, *, where: str) -> tuple[str, ...]:
    items = _list(value, where=where)
    if not all(isinstance(item, str) for item in items):
        raise RegistryError(f"{where}: expected a list of strings")
    return tuple(cast(list[str], items))


def _mapping(value: object, *, where: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise RegistryError(f"{where}: expected a mapping")
    return cast(dict[str, object], value)


def _text(entry: Mapping[str, object], key: str, *, where: str) -> str:
    value = entry.get(key)
    if not isinstance(value, str) or not value.strip():
        raise RegistryError(f"{where}: {key} must be a nonempty string")
    return value


def _pattern(entry: Mapping[str, object], key: str, *, where: str) -> str:
    pattern = _text(entry, key, where=where)
    try:
        re.compile(pattern)
    except re.error as exc:
        raise RegistryError(f"{where}: {key} is not a pattern: {exc}") from exc
    return pattern


_TERM_FIELDS = frozenset(
    {"term", "uses", "defined_by", "anchor", "symbol", "requires", "forward", "series"}
)


def _term(raw: object, *, where: str) -> Term:
    entry = _mapping(raw, where=where)
    name = _text(entry, "term", where=where)
    place = f"{where}: {name}"
    unknown = set(entry) - _TERM_FIELDS
    if unknown:
        raise RegistryError(f"{place}: unknown fields {sorted(unknown)}")
    forwards: list[Forward] = []
    for item in _list(entry.get("forward"), where=place):
        allowed = _mapping(item, where=place)
        reason = _text(allowed, "reason", where=place)
        if reason not in FORWARD_REASONS:
            raise RegistryError(f"{place}: forward reason {reason!r} is not one of the three")
        forwards.append(Forward(_normal(_text(allowed, "text", where=place)), reason))
    series = entry.get("series")
    return Term(
        term=name,
        uses=_pattern(entry, "uses", where=place),
        defined_by=_normal(_text(entry, "defined_by", where=place)),
        anchor=_text(entry, "anchor", where=place),
        symbol=bool(entry.get("symbol", False)),
        requires=_strings(entry.get("requires"), where=place),
        forward=tuple(forwards),
        series=None if series is None else _text(entry, "series", where=place),
    )


def parse_registry(data: object, *, where: str = "registry") -> Registry:
    """A registry from its YAML document, refusing an unknown field or a bad pattern."""
    document = _mapping(data, where=where)
    terms = [_term(raw, where=where) for raw in _list(document.get("terms"), where=where)]
    names = [term.term for term in terms]
    duplicates = sorted({name for name in names if names.count(name) > 1})
    if duplicates:
        raise RegistryError(f"{where}: terms registered twice: {duplicates}")
    banned = [
        Banned(
            _pattern(entry, "pattern", where=where),
            _text(entry, "reason", where=where),
            symbol=bool(entry.get("symbol", False)),
        )
        for entry in (
            _mapping(raw, where=where) for raw in _list(document.get("banned"), where=where)
        )
    ]
    return Registry(
        paper=_text(document, "paper", where=where), terms=tuple(terms), banned=tuple(banned)
    )


def load_registry(slug: str, *, templates: Path = TEMPLATES) -> Registry:
    """A paper's registry from `templates/<slug>-terms.yaml`."""
    path = templates / f"{slug}-terms.yaml"
    registry = parse_registry(load_yaml(path.read_text(encoding="utf-8")), where=path.name)
    if registry.paper != slug:
        raise RegistryError(f"{path.name}: names paper {registry.paper!r}, not {slug!r}")
    return registry


def parse_series(data: object, *, where: str = "series") -> Series:
    """The series registry from its YAML document."""
    document = _mapping(data, where=where)
    concepts: list[Concept] = []
    for raw in _list(document.get("concepts"), where=where):
        entry = _mapping(raw, where=where)
        concept = Concept(
            concept=_text(entry, "concept", where=where),
            owner=_text(entry, "owner", where=where),
            anchor=_text(entry, "anchor", where=where),
        )
        if concept.owner not in paper_links.PAPER_SLUGS:
            message = f"{where}: {concept.concept}: owner {concept.owner!r} is no paper"
            raise RegistryError(message)
        concepts.append(concept)
    clashes = {
        _text(entry, "symbol", where=where): _text(entry, "reason", where=where)
        for entry in (
            _mapping(raw, where=where) for raw in _list(document.get("clashes"), where=where)
        )
    }
    return Series(concepts=tuple(concepts), clashes=clashes)


def load_series(path: Path = SERIES) -> Series:
    return parse_series(load_yaml(path.read_text(encoding="utf-8")), where=path.name)


# --- the rules ---


@dataclass(frozen=True)
class Place:
    """Where a match stands: its block, and its span in that block's text."""

    block: int
    start: int
    end: int

    def __le__(self, other: Place) -> bool:
        return (self.block, self.start) <= (other.block, other.start)

    def __lt__(self, other: Place) -> bool:
        return (self.block, self.start) < (other.block, other.start)


def _occurrences(page: Page, needle: str) -> list[Place]:
    found: list[Place] = []
    for block in page.blocks:
        start = block.text.find(needle)
        while start >= 0:
            found.append(Place(block.index, start, start + len(needle)))
            start = block.text.find(needle, start + 1)
    return found


def _uses(page: Page, term: Term) -> list[Place]:
    pattern = term.pattern()
    found: list[Place] = []
    for block in page.blocks:
        haystack = block.tex if term.symbol else block.prose
        found.extend(
            Place(block.index, match.start(), match.end())
            for match in pattern.finditer(haystack)
            if match.end() > match.start()
        )
    return found


def definitions(page: Page, registry: Registry) -> dict[str, Place]:
    """Where each term's definition stands, for the terms whose definition occurs once."""
    places: dict[str, Place] = {}
    for term in registry.terms:
        found = _occurrences(page, term.defined_by)
        if len(found) == 1:
            places[term.term] = found[0]
    return places


def first_use(page: Page, term: Term, defined: Place | None) -> Place | None:
    """The first place a reader meets the term: its first use, or its definition."""
    candidates = _uses(page, term)
    if defined is not None:
        candidates.append(defined)
    return min(candidates, default=None)


def check_paper(page: Page, registry: Registry) -> list[Finding]:
    """Rules 1-5 on one paper's rendered page."""
    findings = _check_paper(page, registry)
    return [replace(finding, paper=registry.paper) for finding in findings]


def _check_paper(page: Page, registry: Registry) -> list[Finding]:
    findings: list[Finding] = []
    places = definitions(page, registry)
    # Rule 1: one definition, in its section.
    for term in registry.terms:
        found = _occurrences(page, term.defined_by)
        if len(found) != 1:
            findings.append(
                Finding(
                    1, term.term, f"definition occurs {len(found)} times: {term.defined_by!r}"
                )
            )
            continue
        if term.anchor not in page.heading_ids:
            findings.append(Finding(1, term.term, f"anchor {term.anchor!r} is no heading id"))
        elif term.anchor not in page.blocks[found[0].block].sections:
            findings.append(
                Finding(1, term.term, f"defined outside its section {term.anchor!r}")
            )
    # Rule 2: nothing before the definition but the declared forward uses.
    for term in registry.terms:
        defined = places.get(term.term)
        if defined is None:
            continue
        allowances = {
            forward: [place for place in _occurrences(page, forward.text) if place < defined]
            for forward in term.forward
        }
        used: set[Forward] = set()
        for use in _uses(page, term):
            if not use < defined or (
                use.block == defined.block and defined.start <= use.start < defined.end
            ):
                continue
            covering = next(
                (
                    forward
                    for forward, spans in allowances.items()
                    for span in spans
                    if span.block == use.block and span.start <= use.start
                    if use.end <= span.end
                ),
                None,
            )
            if covering is None:
                block = page.blocks[use.block]
                context = block.text[max(use.start - 40, 0) : use.end + 40]
                findings.append(
                    Finding(2, term.term, f"used before its definition: {context!r}")
                )
            else:
                used.add(covering)
        findings.extend(
            Finding(2, term.term, f"forward allowance covers no earlier use: {forward.text!r}")
            for forward in term.forward
            if forward not in used
        )
    # Rule 3: prerequisites registered and defined first.
    for term in registry.terms:
        for required in term.requires:
            if registry.term(required) is None:
                findings.append(Finding(3, term.term, f"requires unregistered {required!r}"))
            elif (
                required in places
                and term.term in places
                and not places[required] <= places[term.term]
            ):
                findings.append(
                    Finding(3, term.term, f"requires {required!r}, defined after it")
                )
    # Rule 4: every bold run is a definition, a run-in head or a figure label.
    spans = [(place, term) for term in registry.terms if (place := places.get(term.term))]
    for block in page.blocks:
        for start, end in block.bold:
            words = block.text[start:end].strip()
            if not words:
                continue
            opening = block.text[:start].strip() == ""
            if opening and (words.endswith((".", ":")) or _FIGURE_LABEL.match(words)):
                continue
            inside = any(
                place.block == block.index and place.start <= start and end <= place.end
                for place, _ in spans
            )
            if not inside:
                findings.append(Finding(4, words, "a bold run that is no term's definition"))
    # Rule 5: banned bare forms.
    for banned in registry.banned:
        pattern = re.compile(banned.pattern)
        for block in page.blocks:
            for match in pattern.finditer(block.tex if banned.symbol else block.prose):
                context = block.text[max(match.start() - 40, 0) : match.end() + 40]
                findings.append(Finding(5, match.group(0), f"{banned.reason}: {context!r}"))
    return findings


def _links_to(block: Block, owner: str) -> bool:
    return any(
        re.search(rf"(?:^|/){re.escape(owner)}\.html(?:#|$)", href) for href in block.links
    )


def check_series(
    pages: Mapping[str, Page], registries: Mapping[str, Registry], series: Series
) -> list[Finding]:
    """Rule 6 over the papers given: owners, links to owners, and symbol clashes."""
    findings: list[Finding] = []
    for slug, registry in registries.items():
        page = pages.get(slug)
        places = definitions(page, registry) if page is not None else {}
        for term in registry.terms:
            if term.series is None:
                continue
            concept = series.concept(term.series)
            if concept is None:
                findings.append(
                    Finding(
                        6, term.term, f"names unregistered series concept {term.series!r}", slug
                    )
                )
                continue
            if concept.owner == slug:
                if term.anchor != concept.anchor:
                    message = (
                        f"owner defines it at {term.anchor!r}, not at the series anchor "
                        f"{concept.anchor!r}"
                    )
                    findings.append(Finding(6, term.term, message, slug))
                continue
            if page is None:
                continue
            first = first_use(page, term, places.get(term.term))
            if first is not None and not _links_to(page.blocks[first.block], concept.owner):
                message = (
                    f"first used in a block that does not link its owner, {concept.owner}: "
                    f"{page.blocks[first.block].text[:80]!r}"
                )
                findings.append(Finding(6, term.term, message, slug))
    for concept in series.concepts:
        owner_page = pages.get(concept.owner)
        if owner_page is not None and concept.anchor not in owner_page.heading_ids:
            message = f"the owner has no heading {concept.anchor!r}"
            findings.append(Finding(6, concept.concept, message, concept.owner))
    meanings: dict[str, dict[str, str | None]] = {}
    for slug, registry in registries.items():
        for term in registry.terms:
            if term.symbol:
                meanings.setdefault(term.term, {})[slug] = term.series
    for symbol, by_paper in sorted(meanings.items()):
        if len(by_paper) < 2 or symbol in series.clashes:
            continue
        senses = set(by_paper.values())
        if len(senses) > 1 or None in senses:
            message = (
                f"defined with different meanings in {sorted(by_paper)}, listed as no clash"
            )
            findings.append(Finding(6, symbol, message))
    return findings


def check_paper_anchors(
    sources: Mapping[str, str], pages: Mapping[str, Page]
) -> tuple[list[Finding], list[tuple[str, str, str]]]:
    """Every `{{PAPER:slug#anchor}}` in each article against the target's headings.

    Returns the findings, and the links whose target paper is not among `pages`, which
    a caller decides whether to accept as pending."""
    findings: list[Finding] = []
    pending: list[tuple[str, str, str]] = []
    for slug, source in sources.items():
        for target, anchor in paper_links.paper_link_targets(source):
            if anchor is None:
                continue
            page = pages.get(target)
            if page is None:
                pending.append((slug, target, anchor))
            elif anchor not in page.heading_ids:
                findings.append(Finding(6, f"{target}#{anchor}", "no such heading", slug))
    return findings, pending


#: TeX as the reader would see it in prose: a math delimiter or a control word.
_RAW_TEX = re.compile(r"\\[A-Za-z]+|\$")
#: A display formula wrapped by hand rather than written as a `$$` block.
_HAND_DISPLAY = re.compile(
    r'<[a-z]+\b[^>]*\bclass="[^"]*\btex-d\b[^"]*"[^>]*>(.*?)</', re.DOTALL
)
#: The paper's title, which the exposition reader skips with the rest of the front.
_HERO_TITLE = re.compile(r'<div class="hero">\s*(<h1\b.*?</h1>)', re.DOTALL)


def _raw_tex(page: Page, where: str) -> list[Finding]:
    findings: list[Finding] = []
    for block in page.blocks:
        for found in _RAW_TEX.finditer(block.prose):
            context = _WHITESPACE.sub(
                " ", block.text[max(0, found.start() - 40) : found.end() + 40]
            ).strip()
            section = block.sections[-1] if block.sections else where
            findings.append(
                Finding(7, found.group(0), f"TeX printed as text in {section}: ...{context}...")
            )
    return findings


def check_math(html: str) -> list[Finding]:
    """Rule 7 on one rendered paper: no TeX in its prose, captions or title, and every
    display formula a `$$` block."""
    findings = _raw_tex(read_page(html), "the exposition")
    for display in _HAND_DISPLAY.finditer(html):
        context = _WHITESPACE.sub(" ", display.group(1))[:60].strip()
        findings.append(
            Finding(7, "tex-d", f"display formula outside a $$ block: {context}...")
        )
    for title in _HERO_TITLE.finditer(html):
        findings.extend(_raw_tex(read_page(title.group(1)), "the title"))
    return findings


def report(findings: Iterable[Finding]) -> str:
    return "\n".join(str(finding) for finding in findings)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    parser.add_argument(
        "site", type=Path, help="a built site's root, with the papers under papers/"
    )
    parser.add_argument(
        "--paper",
        action="append",
        help="a paper's slug; repeatable (default: every paper with a registry)",
    )
    args = parser.parse_args(argv)
    slugs: list[str] = args.paper or sorted(
        slug for slug in paper_links.PAPER_SLUGS if (TEMPLATES / f"{slug}-terms.yaml").is_file()
    )
    pages: dict[str, Page] = {}
    registries: dict[str, Registry] = {}
    findings: list[Finding] = []
    for slug in slugs:
        path = args.site / "papers" / f"{slug}.html"
        if not path.is_file():
            print(f"{slug}: not built at {path}", file=sys.stderr)
            continue
        html = path.read_text(encoding="utf-8")
        pages[slug] = read_page(html)
        registries[slug] = load_registry(slug)
        found = check_paper(pages[slug], registries[slug])
        found += [replace(finding, paper=slug) for finding in check_math(html)]
        findings.extend(found)
        print(f"{slug}: {len(found)} findings")
    findings.extend(check_series(pages, registries, load_series()))
    if findings:
        print(report(findings))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
