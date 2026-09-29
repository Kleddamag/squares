"""What a card's popover shows of the page or document it leads to.

Every card on the overview opens a popover that previews its target before the reader
goes there: for a page or a document, its opening paragraph and the sections it holds,
read here from the source itself so the preview never drifts from what it previews.
The previews are HTML, with Markdown's inline marks reduced to text and its `$…$` set
as math.
"""

from __future__ import annotations

import html
import re
from pathlib import Path

from devtools.overview_data import REPO, math_html

PACKING = Path(__file__).resolve().parents[1]
TEMPLATES = PACKING / "devtools" / "templates"

#: The site pages a card previews, by where the card leads, and the source each reads.
PAGE_SOURCES: dict[str, Path] = {
    "explainer.html": TEMPLATES / "explainer-article.md",
    "tutorial.html": REPO / "TUTORIAL.md",
    "frontier.html": TEMPLATES / "frontier-article.md",
}

#: The repository documents a card previews, as the overview's document cards list them.
DOCUMENT_SOURCES: tuple[str, ...] = (
    "README.md",
    "SYNOPSIS.md",
    "packing/frontier/RESULTS.md",
    "packing/frontier/STATUS.md",
    "epistemics.md",
    "conventions.md",
    "development.md",
    "defects.md",
)

#: Every file a preview reads, for the render's declared inputs.
INPUTS: tuple[Path, ...] = (
    Path(__file__).resolve(),
    *PAGE_SOURCES.values(),
    *(REPO / path for path in DOCUMENT_SOURCES),
)

#: Sections a preview leaves out: navigation and apparatus, not content.
_SKIPPED = {"Contents", "Version History", "Acknowledgments", "Further Reading"}
#: How many sections a preview names before summing up the rest.
SECTIONS_SHOWN = 8
#: About how long a preview's opening may run, in characters, before it is cut at a
#: sentence.
OPENING_LENGTH = 320

_LINK = re.compile(r"!?\[([^\]]*)\]\([^)]*\)")
_EMPHASIS = re.compile(r"(\*\*|__|\*|_)(?=\S)(.+?)(?<=\S)\1")
_CODE = re.compile(r"`([^`]+)`")
_MATH = re.compile(r"\$([^$\n]+)\$")
_PLACEHOLDER = re.compile(r"\{\{[A-Z0-9_]+\}\}")
_OPENING_SKIP = ("#", "<", "|", "-", "*", ">", "!", "```", "[")


def inline(text: str) -> str:
    """One line of Markdown as HTML: links and emphasis reduced to their text, code
    spans kept as code, and `$…$` set as math; everything else escaped."""
    text = _EMPHASIS.sub(r"\2", _LINK.sub(r"\1", text))
    parts: list[str] = []
    last = 0
    for match in re.finditer(f"{_MATH.pattern}|{_CODE.pattern}", text):
        parts.append(html.escape(text[last : match.start()], quote=False))
        if match.group(1) is not None:
            parts.append(math_html(match.group(1)))
        else:
            parts.append(f"<code>{html.escape(match.group(2), quote=False)}</code>")
        last = match.end()
    parts.append(html.escape(text[last:], quote=False))
    return "".join(parts)


def sections(markdown: str) -> list[str]:
    """The document's second-level headings, apparatus and templated ones left out."""
    found = []
    for heading in re.findall(r"^## (.+)$", markdown, flags=re.MULTILINE):
        title = heading.strip()
        bare = re.sub(r"^[0-9]+\.\s*", "", title)
        if bare in _SKIPPED or _PLACEHOLDER.search(title):
            continue
        found.append(title)
    return found


def opening(markdown: str) -> str:
    """The first paragraph of prose after the title, cut at a sentence near
    `OPENING_LENGTH` characters."""
    body = re.sub(r"^---\n.*?\n---\n", "", markdown, flags=re.DOTALL)
    paragraph: list[str] = []
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped:
            if paragraph:
                break
            continue
        if not paragraph and (stripped.startswith(_OPENING_SKIP) or "{{" in stripped):
            continue
        paragraph.append(stripped)
    text = " ".join(paragraph)
    if len(text) <= OPENING_LENGTH:
        return text
    cut = text.rfind(". ", 0, OPENING_LENGTH)
    return text[: cut + 1] if cut > 0 else text[:OPENING_LENGTH].rsplit(" ", 1)[0] + "…"


def preview(markdown: str, *, lead: str = "") -> str:
    """A popover's preview of a document: `lead` or its opening, then its sections."""
    first = lead or inline(opening(markdown))
    listed = sections(markdown)
    shown = listed[:SECTIONS_SHOWN]
    items = "".join(f"<li>{inline(title)}</li>" for title in shown)
    more = len(listed) - len(shown)
    if more > 0:
        items += f'<li class="site-popover-more">and {more} more</li>'
    inside = f'<p class="site-popover-heading">Inside</p><ul>{items}</ul>' if shown else ""
    return f"<p>{first}</p>{inside}"


def page_preview(href: str, lead: str) -> str:
    """The preview of a site page: its sections under `lead`, or `lead` alone for a page
    with no Markdown source, such as the visualizer."""
    source = PAGE_SOURCES.get(href)
    if source is None:
        return f"<p>{lead}</p>"
    return preview(source.read_text(encoding="utf-8"), lead=lead)


def document_preview(path: str) -> str:
    """The preview of a repository document: its opening and its sections."""
    return preview((REPO / path).read_text(encoding="utf-8"))
