#!/usr/bin/env python3
"""The structure of a rendered paper, and the two papers compared axis by axis.

The owner asked on 2026-10-01 that the two papers' "formats, formatting, and all
structure should be similar". This reads each paper as a reader meets it, from the page,
its Markdown edition and its PDF, and reports the two side by side on every structural
axis: the head and its dates, the formats row, the title, each line of the credits and
what is bold and what is linked in it, the version and dates lines, the heading case,
the figures and their captions, the tables, the footnotes, the closing and the
colophon, and the Markdown edition's opening. An axis is one of two kinds: a form,
which both papers set one way, and content, which is each paper's own, such as how
many figures it has. `compare` says which differ, and `tests/test_paper_structure.py`
fails when a form differs between the two.

Usage, from `packing/`, on a site `preview_site` has built, or on the published site:

    uv run --frozen --all-extras --group dev python -m devtools.paper_structure SITE --markdown
    uv run --frozen --all-extras --group dev python -m devtools.paper_structure https://jlevy.github.io/squares/

The audit this was written for (think-2cqu) found the credits in two orders, a bold
address on one paper and none on the other, the version before the dates on one and
after on the other, and chips rendered by KPress on one paper and written raw into the
shell of the other. The front of both is written by `devtools.paper_front` now; this
is what shows it stays so, and what finds the next difference.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, NamedTuple

from devtools.render_overview import (
    N11_LOWER_BOUNDS_EXPLAINER,
    N11_OPTIMALITY_REVIEW,
    PROJECT_NAME,
    TITLE_SEPARATOR,
    paper_path,
)

#: The two papers, in the order the audit reads them: the first paper is the reference.
PAPERS = (N11_LOWER_BOUNDS_EXPLAINER, N11_OPTIMALITY_REVIEW)
#: The lines a paper's credits may carry, in the order they stand, by what the line is.
CREDIT_KINDS = ("source", "address", "oversight", "agents", "version", "dates")
#: Elements with no content, which the parser must not wait for a closing tag of.
_VOID = frozenset(
    (
        *("area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta"),
        *("param", "source", "track", "wbr"),
        *("path", "circle", "rect", "line", "polyline", "polygon", "ellipse", "use", "stop"),
    )
)
_FIGURE_LEAD = re.compile(r"^Figure (\d+)\.")
_DATED = re.compile(r"^(.+?) ([A-Z][a-z]+ \d{1,2}, \d{4})$")
_PDF_PAGE = re.compile(rb"/Type\s*/Page(?![s/\w])")
_PDF_BOX = re.compile(rb"/MediaBox\s*\[\s*([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s*\]")
_PDF_DATE = re.compile(rb"/(CreationDate|ModDate)\s*\(D:([^)]*)\)")
_PDF_TITLE = re.compile(rb"/Title\s*(?:<([0-9A-Fa-f]+)>|\(((?:[^()\\]|\\.)*)\))")
_SMALL_WORDS = frozenset(
    (
        *("a", "an", "and", "as", "at", "but", "by", "for", "from", "in", "into"),
        *("nor", "of", "on", "or", "per", "the", "to", "vs", "via", "with"),
    )
)


@dataclass
class Node:
    """One element of a page, with its children, as the structure is read from it."""

    tag: str
    attrs: dict[str, str]
    children: list[Node | str] = field(default_factory=list)

    @property
    def classes(self) -> frozenset[str]:
        return frozenset(self.attrs.get("class", "").split())

    def text(self) -> str:
        """The element's text, with a typeset formula read as its source rather than as
        the MathML and the glyphs the page draws it with."""
        if "data-kpress-math-source" in self.attrs:
            return self.attrs["data-kpress-math-source"]
        parts = [child if isinstance(child, str) else child.text() for child in self.children]
        return re.sub(r"\s+", " ", "".join(parts)).strip()

    def walk(self) -> Iterable[Node]:
        """Every element under this one that the page shows: a hidden subtree, such as
        the explainer's copy of a figure for a certificate the page is not showing, is
        not what a reader meets and is left out."""
        for child in self.children:
            if isinstance(child, Node) and "hidden" not in child.attrs:
                yield child
                yield from child.walk()

    def find_all(self, tag: str | None = None, cls: str | None = None) -> list[Node]:
        return [
            node
            for node in self.walk()
            if (tag is None or node.tag == tag) and (cls is None or cls in node.classes)
        ]

    def find(self, tag: str | None = None, cls: str | None = None) -> Node | None:
        found = self.find_all(tag, cls)
        return found[0] if found else None


class _Tree(HTMLParser):
    """Builds the page as `Node`s; scripts and styles are left out of the text."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.root = Node("document", {})
        self.open = [self.root]
        self.quiet = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        node = Node(tag, {name: value or "" for name, value in attrs})
        self.open[-1].children.append(node)
        if tag in ("script", "style"):
            self.quiet += 1
        if tag not in _VOID:
            self.open.append(node)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.open[-1].children.append(Node(tag, {name: value or "" for name, value in attrs}))

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style"):
            self.quiet -= 1
        for depth in range(len(self.open) - 1, 0, -1):
            if self.open[depth].tag == tag:
                del self.open[depth:]
                return

    def handle_data(self, data: str) -> None:
        if not self.quiet and data:
            self.open[-1].children.append(data)


def parse(html: str) -> Node:
    """A page as a tree of `Node`s."""
    tree = _Tree()
    tree.feed(html)
    tree.close()
    return tree.root


class CreditLine(NamedTuple):
    """One line of the credits: what it is, its text, the names set in bold in it, and
    the links in it, each as its text and its address."""

    kind: str
    text: str
    bold: tuple[str, ...]
    links: tuple[tuple[str, str], ...]


class Chip(NamedTuple):
    label: str
    href: str
    title: str


@dataclass(frozen=True)
class Structure:
    """A paper's structure as read from its page, its Markdown edition and its PDF."""

    paper: str
    title: str
    name: str
    description: str
    kind: str
    published: str
    modified: str
    h1: tuple[str, ...]
    chips: tuple[Chip, ...]
    credits: tuple[CreditLine, ...]
    h2: tuple[str, ...]
    h3: tuple[str, ...]
    captions: tuple[str, ...]
    tables: int
    footnotes: int
    colophon: tuple[str, ...]
    markdown_head: tuple[str, ...]
    pdf: dict[str, str]


def _meta(root: Node, key: str) -> str:
    for node in root.find_all("meta"):
        if node.attrs.get("property") == key or node.attrs.get("name") == key:
            return node.attrs.get("content", "")
    return ""


def _credit_kind(line: Node, text: str) -> str:
    classes = line.classes
    if "publication-date" in classes:
        return "dates"
    if "edition" in classes:
        return "version"
    if text.startswith("Human oversight"):
        return "oversight"
    if text.startswith("Agents"):
        return "agents"
    if "credits-source" in classes:
        # The source's address is its link; its author's line has none.
        return "address" if line.find("a") else "source"
    return "other"


def _credit_lines(root: Node) -> tuple[CreditLine, ...]:
    block = root.find(cls="credits")
    if block is None:
        return ()
    lines = []
    for line in (child for child in block.children if isinstance(child, Node)):
        text = line.text()
        lines.append(
            CreditLine(
                _credit_kind(line, text),
                text,
                tuple(strong.text() for strong in line.find_all("strong")),
                tuple(
                    (anchor.text(), anchor.attrs.get("href", ""))
                    for anchor in line.find_all("a")
                ),
            )
        )
    return tuple(lines)


def _chips(root: Node) -> tuple[Chip, ...]:
    row = root.find(cls="doc-links")
    if row is None:
        return ()
    return tuple(
        Chip(chip.text(), chip.attrs.get("href", ""), chip.attrs.get("title", ""))
        for chip in row.find_all("a")
    )


def _pdf(pdf: bytes) -> dict[str, str]:
    if not pdf:
        return {}
    title = _PDF_TITLE.search(pdf)
    if title is None:
        name = ""
    elif title.group(1) is not None:
        raw = bytes.fromhex(title.group(1).decode())
        name = raw.decode("utf-16") if raw.startswith(b"\xfe\xff") else raw.decode("latin-1")
    else:
        # A literal string escapes its parentheses and backslashes.
        name = re.sub(rb"\\(.)", rb"\1", title.group(2)).decode("latin-1")
    box = _PDF_BOX.search(pdf)
    return {
        "title": name,
        "pages": str(len(_PDF_PAGE.findall(pdf))),
        "size": f"{float(box.group(3)):g} x {float(box.group(4)):g} pt" if box else "",
        **{key.decode(): value.decode() for key, value in _PDF_DATE.findall(pdf)},
    }


def _markdown_head(markdown: str) -> tuple[str, ...]:
    """The Markdown edition's opening: its first line and the list that follows it, up
    to the first paragraph."""
    lines = markdown.strip().split("\n")
    head: list[str] = [lines[0]] if lines else []
    for line in lines[1:]:
        if line.startswith("- "):
            head.append(line)
        elif line.strip() and head[1:]:
            break
    return tuple(head)


def read(paper: str, html: str, markdown: str = "", pdf: bytes = b"") -> Structure:
    """A paper's structure, from its rendered page and, where given, its Markdown
    edition and its PDF."""
    root = parse(html)
    title = root.find("title")
    footnotes = root.find("section", "kpress-footnotes")
    colophon = root.find(cls="colophon")
    return Structure(
        paper=paper,
        title=title.text() if title else "",
        name=_meta(root, "og:title"),
        description=_meta(root, "description"),
        kind=_meta(root, "og:type"),
        published=_meta(root, "article:published_time"),
        modified=_meta(root, "article:modified_time"),
        h1=tuple(node.text() for node in root.find_all("h1")),
        chips=_chips(root),
        credits=_credit_lines(root),
        h2=tuple(node.text() for node in root.find_all("h2")),
        h3=tuple(node.text() for node in root.find_all("h3")),
        captions=tuple(node.text() for node in root.find_all("figcaption")),
        tables=len(root.find_all("table")),
        footnotes=len(footnotes.find_all("li")) if footnotes else 0,
        colophon=tuple(line.text() for line in colophon.find_all(cls="site-colophon-line"))
        if colophon
        else (),
        markdown_head=_markdown_head(markdown),
        pdf=_pdf(pdf),
    )


def heading_case(headings: Sequence[str]) -> str:
    """`Title Case` where every word of every heading that is not a small word or a
    number begins with a capital; `sentence case` where only the first does; `mixed`
    where the headings disagree; `none` where there is no heading."""
    found = set()
    for heading in headings:
        words = [w for w in re.split(r"[\s:]+", heading) if re.match(r"[A-Za-z]", w)]
        later = [w for w in words[1:] if w.lower() not in _SMALL_WORDS and len(w) > 1]
        if not later:
            continue
        capitals = sum(1 for w in later if w[0].isupper())
        found.add("Title Case" if capitals == len(later) else "sentence case")
    if not found:
        return "none"
    return found.pop() if len(found) == 1 else "mixed"


def caption_form(captions: Sequence[str]) -> str:
    """`Figure N. …` numbered from 1 without a gap, or what departs from it."""
    numbers = [_FIGURE_LEAD.match(caption) for caption in captions]
    if not captions:
        return "no figures"
    if any(number is None for number in numbers):
        return "a caption without a `Figure N.` lead"
    found = [int(number.group(1)) for number in numbers if number]
    if found != list(range(1, len(found) + 1)):
        return f"numbered {found}"
    return "Figure N. lead, numbered from 1"


def _dates(line: CreditLine | None) -> list[tuple[str, str]]:
    if line is None:
        return []
    found = []
    for part in line.text.split(" · "):
        dated = _DATED.match(part.strip())
        found.append((dated.group(1), dated.group(2)) if dated else (part, ""))
    return found


def axes(structure: Structure) -> dict[str, str]:
    """Each axis of a paper's structure, as one line a reader can compare: a form the
    two papers share, or the content that is this paper's own (`CONTENT_AXES`)."""
    lines = {line.kind: line for line in structure.credits}
    slug = structure.paper
    expected_title = f"{structure.name}{TITLE_SEPARATOR}{PROJECT_NAME}"
    dates = _dates(lines.get("dates"))
    named = [
        line for line in structure.credits if line.kind in ("source", "oversight", "agents")
    ]
    plain = [line for line in structure.credits if line.kind in ("address", "version", "dates")]
    version = lines.get("version")
    pdf = structure.pdf
    return {
        "head: title": "name · project"
        if structure.title == expected_title
        else structure.title,
        "head: og:type": structure.kind,
        "head: article dates": " and ".join(
            key
            for key, value in (
                ("published", structure.published),
                ("modified", structure.modified),
            )
            if value
        )
        or "none",
        "head: modified is the revised date": "yes"
        if dates and structure.modified == _iso(dates[-1][1])
        else "no",
        "formats row": " · ".join(
            f"{chip.label} → {chip.href.replace(slug, '<slug>')}" for chip in structure.chips
        )
        or "none",
        "formats row: titles": " · ".join(chip.title for chip in structure.chips) or "none",
        "title: h1": f"{len(structure.h1)}, {heading_case(structure.h1)}",
        "title: text": structure.h1[0] if structure.h1 else "",
        "credits: lines": " · ".join(line.kind for line in structure.credits) or "none",
        "credits: names bold": "yes"
        if named and all(line.bold for line in named) and not any(line.bold for line in plain)
        else "no",
        "credits: addresses plain": "yes"
        if all(not line.bold for line in structure.credits if line.kind == "address")
        else "no",
        "credits: version line": (
            "plain, linking the version history"
            if version and version.links and not version.bold
            else "plain, no history"
            if version and not version.bold
            else "none"
            if version is None
            else "bold"
        ),
        "credits: version": version.text if version else "",
        "credits: dates grammar": " · ".join(f"{label} <day>" for label, _ in dates) or "none",
        "credits: dates end with": dates[-1][0] if dates else "none",
        "credits: dates": lines["dates"].text if "dates" in lines else "",
        "credits: oversight": lines["oversight"].text if "oversight" in lines else "",
        "credits: agents": lines["agents"].text if "agents" in lines else "",
        "credits: source": " · ".join(
            line.text for line in structure.credits if line.kind in ("source", "address")
        )
        or "none",
        "sections: h2 case": heading_case(structure.h2),
        "sections: h3 case": heading_case(structure.h3),
        "sections: count": f"{len(structure.h2)} h2, {len(structure.h3)} h3",
        "figures: captions": caption_form(structure.captions),
        "figures: count": str(len(structure.captions)),
        "tables": str(structure.tables),
        "footnotes": "a footnotes section" if structure.footnotes else "none",
        "footnotes: count": str(structure.footnotes),
        "closing: last section": structure.h2[-1] if structure.h2 else "",
        "closing: colophon": " / ".join(structure.colophon) or "none",
        "markdown: opening": _markdown_form(structure),
        "pdf: page size": pdf.get("size", "no PDF"),
        "pdf: title": "the page's title"
        if pdf and pdf.get("title") == structure.title
        else pdf.get("title", "no PDF"),
        "pdf: dates": (
            "the revised date, at noon UTC"
            if pdf
            and dates
            and {pdf.get("CreationDate"), pdf.get("ModDate")}
            == {_iso(dates[-1][1]).replace("-", "") + "120000+00'00'"}
            else ", ".join(sorted({pdf.get("CreationDate", ""), pdf.get("ModDate", "")}))
            if pdf
            else "no PDF"
        ),
        "pdf: pages": pdf.get("pages", "no PDF"),
    }


def _iso(day: str) -> str:
    from devtools.paper_front import iso_date  # noqa: PLC0415

    try:
        return iso_date(day)
    except ValueError:
        return ""


def _markdown_form(structure: Structure) -> str:
    """How the Markdown edition opens, against the page: the title as a heading, then
    the page's credits as a list, one item a line, bold where the page is bold."""
    head = structure.markdown_head
    if not head:
        return "no Markdown edition"
    if not head[0].startswith("# "):
        return f"opens with {head[0][:40]!r}"
    items = [line.removeprefix("- ") for line in head[1:] if line.startswith("- ")]
    if any("chip" in line or ".pdf)" in line for line in items):
        return "a title, then a list that carries the formats row"
    if len(items) != len(structure.credits):
        return f"a title, then {len(items)} list items for {len(structure.credits)} credits"
    off = [
        line.kind
        for item, line in zip(items, structure.credits, strict=True)
        if any(f"**{name}**" not in item for name in line.bold)
        or ("**" in item) != bool(line.bold)
    ]
    if off:
        return f"a title, then a list whose {off[0]} line is not bold as the page's is"
    return "a title, then the credits as a list, one item a line, bold as the page's"


#: The axes that are each paper's own content, which may differ; every other axis is a
#: form, which the two papers set one way.
CONTENT_AXES = frozenset(
    {
        "title: text",
        "credits: version",
        "credits: dates grammar",
        "credits: dates",
        "credits: oversight",
        "credits: agents",
        "credits: source",
        "credits: lines",
        "credits: version line",
        "head: article dates",
        "sections: count",
        "figures: count",
        "tables",
        "footnotes: count",
        "closing: last section",
        "pdf: pages",
    }
)


def compare(first: Structure, second: Structure) -> list[dict[str, Any]]:
    """Every axis, with both papers' values and whether they are the same, the form
    axes first."""
    one, two = axes(first), axes(second)
    return [
        {
            "axis": axis,
            "compared": "content" if axis in CONTENT_AXES else "form",
            first.paper: one[axis],
            second.paper: two[axis],
            "same": one[axis] == two[axis],
        }
        for axis in sorted(one, key=lambda axis: (axis in CONTENT_AXES, axis))
    ]


def differences(rows: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    """The form axes the two papers set differently: what fails the test. A PDF axis
    is compared only where both papers have a PDF: a preview draws the second paper's
    and never the first's, which its own Pages job draws (`preview_site`)."""
    return [
        row
        for row in rows
        if row["compared"] == "form" and not row["same"] and "no PDF" not in row.values()
    ]


def _fetch(site: str, path: str) -> bytes:
    if site.startswith(("http://", "https://")):
        with urllib.request.urlopen(site.rstrip("/") + "/" + path) as response:
            return response.read()
    found = Path(site) / path
    return found.read_bytes() if found.is_file() else b""


def read_site(site: str, papers: Sequence[str] = PAPERS) -> list[Structure]:
    """Each paper as a built site, or the published site, serves it."""
    found = []
    for paper in papers:
        html = _fetch(site, paper_path(paper)).decode("utf-8")
        if not html:
            raise SystemExit(f"{site} has no {paper_path(paper)}")
        markdown = _fetch(site, paper_path(paper, ".md")).decode("utf-8")
        found.append(read(paper, html, markdown, _fetch(site, paper_path(paper, ".pdf"))))
    return found


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("site", help="a built site's directory, or the address it is served at")
    parser.add_argument("--markdown", action="store_true", help="print a table, not JSON")
    arguments = parser.parse_args(argv)
    first, second = read_site(arguments.site)
    rows = compare(first, second)
    if arguments.markdown:
        from devtools.measure_site_pages import markdown_table  # noqa: PLC0415

        print(markdown_table(rows))
    else:
        json.dump(rows, sys.stdout, indent=2)
        print()
    differing = differences(rows)
    if differing:
        print(
            f"{len(differing)} form {'axes differ' if len(differing) > 1 else 'axis differs'}: "
            + "; ".join(row["axis"] for row in differing),
            file=sys.stderr,
        )
    return 1 if differing else 0


if __name__ == "__main__":
    raise SystemExit(main())
