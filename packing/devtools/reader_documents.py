#!/usr/bin/env python3
"""The reader documents the overview lists as cards, read from the document map.

`docs/project/document-map.yaml` records every durable document's role, authority and
lifecycle, and a one-sentence `summary` for each document the overview shows. This
module turns those entries into the cards of the overview's Read Further section.

**Three groups, in the order the page shows them.** Where to start (the README, the
tutorial and the synopsis); the results and the policy they are held to (the results
register's view, the frontier's view, the epistemics and the conventions); and the
research reports under `docs/project/research/`, newest first by the date in the file
name, the maintained ones before those the map keeps as dated records (`retained`),
whose cards say so and give the date.

**What a card says.** Its title is the document's own first heading, so a card cannot
name a document differently from the document itself. Its summary is the map's: it says
what the document covers, never what it found, because several reports predate the
current bounds and a card must not restate a finding the record has moved past.
`check_documentation` requires a summary on every document listed here and refuses one
that states a bound, so the numbers on the page stay generated.

**Where a card goes.** A document links to GitHub on the default branch, so a reader
lands on the current text rather than on the build's copy; the tutorial is a site page
of its own. Record links elsewhere on the site stay permalinks at the build commit.
"""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from functools import cache
from pathlib import Path
from typing import Any, Literal

from devtools import site_kit
from sqpack.yamlio import safe_load

REPO = Path(__file__).resolve().parents[2]
DOCUMENT_MAP = REPO / "docs" / "project" / "document-map.yaml"

#: The branch a document card names, so the reader sees the document as it is now.
DEFAULT_BRANCH = "main"

Group = Literal["start", "results", "reports"]

#: Where a reader starts, in the order the cards stand.
START: tuple[str, ...] = ("README.md", "TUTORIAL.md", "SYNOPSIS.md")
#: The results and the policy they are held to, in the order the cards stand.
RESULTS: tuple[str, ...] = (
    "packing/frontier/RESULTS.md",
    "packing/frontier/STATUS.md",
    "epistemics.md",
    "conventions.md",
)
#: Every document the map records under this directory is a research report card.
REPORTS = "docs/project/research/"
#: Documents the site renders as pages of its own, by the key of their page in the bar.
SITE_PAGES: Mapping[str, str] = {"TUTORIAL.md": "tutorial"}

#: A report's date, from its file name: `research-2026-09-07-<topic>.md`.
_REPORT_DATE = re.compile(r"research-(\d{4}-\d{2}-\d{2})-[^/]+\.md")
_HEADING = re.compile(r"#[ \t]+(\S.*?)[ \t]*#*[ \t]*")
_FENCE = re.compile(r"(`{3,}|~{3,})")

#: The map, the module, and every document whose first heading a card reads.
RENDER_INPUTS: tuple[Path, ...] = (
    Path(__file__),
    DOCUMENT_MAP,
    *(REPO / path for path in (*START, *RESULTS)),
    REPO / REPORTS,
)


@dataclass(frozen=True)
class ReaderDocument:
    """One card of the overview's Read Further section, from the document map.

    `url` is the document on GitHub on the default branch, or a site page for the
    tutorial. `summary` says what the document covers, never what it found, and states no
    bound. `dated` marks a research report the map keeps as a dated record.
    """

    path: str
    title: str
    summary: str
    group: Group
    url: str
    date: str | None
    dated: bool


def load_map(path: Path = DOCUMENT_MAP) -> dict[str, Any]:
    """The document map's payload, without its softschema envelope."""
    document = safe_load(path.read_text(encoding="utf-8"))
    return {key: value for key, value in document.items() if key != "softschema"}


def shown_paths(document_map: Mapping[str, Any]) -> tuple[str, ...]:
    """Every document the overview lists, repository-relative, in no particular order.

    The start and results documents are fixed; the reports are whatever the map records
    under `REPORTS`, so a report added to the map gains a card, and the summary it needs
    for one, without an edit here.
    """
    reports = sorted(
        document["path"]
        for document in document_map["documents"]
        if document["path"].startswith(REPORTS)
    )
    return (*START, *RESULTS, *reports)


def title(path: Path) -> str:
    """A document's first level-one heading, outside its front matter and code fences."""
    lines = path.read_text(encoding="utf-8").splitlines()
    if lines and lines[0] == "---":
        closing = next((i for i, line in enumerate(lines[1:], 1) if line == "---"), None)
        if closing is None:
            raise ValueError(f"{path.name}: front matter is never closed")
        lines = lines[closing + 1 :]
    fence: str | None = None
    for line in lines:
        opening = _FENCE.match(line.lstrip())
        if opening:
            marker = opening.group(1)
            if fence is None:
                fence = marker[0] * 3
            elif marker.startswith(fence):
                fence = None
            continue
        heading = _HEADING.fullmatch(line)
        if fence is None and heading:
            return heading.group(1)
    raise ValueError(f"{path.name} has no level-one heading to title its card")


def report_date(path: str) -> str:
    """The date a research report's file name carries."""
    match = _REPORT_DATE.fullmatch(Path(path).name)
    if match is None:
        raise ValueError(f"{path}: a research report's name starts research-YYYY-MM-DD-")
    return match.group(1)


def document_url(path: str) -> str:
    """Where a card goes: the site page for a document the site renders, else GitHub."""
    key = SITE_PAGES.get(path)
    if key is not None:
        return next(item.href for item in site_kit.NAV_ITEMS if item.key == key)
    return f"{site_kit.REPO_URL}/blob/{DEFAULT_BRANCH}/{path}"


def _card(entry: Mapping[str, Any], group: Group, repo: Path) -> ReaderDocument:
    path = entry["path"]
    summary = entry.get("summary")
    if not isinstance(summary, str) or not summary.strip():
        raise ValueError(f"{path}: the overview lists it, so the document map needs a summary")
    reported = group == "reports"
    return ReaderDocument(
        path=path,
        title=title(repo / path),
        summary=summary,
        group=group,
        url=document_url(path),
        date=report_date(path) if reported else None,
        dated=reported and entry["lifecycle"] == "retained",
    )


def _report_order(entries: Sequence[Mapping[str, Any]]) -> list[Mapping[str, Any]]:
    """Maintained before retained; within each, newest first, then by path."""
    ordered = sorted(entries, key=lambda entry: entry["path"])
    ordered.sort(key=lambda entry: report_date(entry["path"]), reverse=True)
    ordered.sort(key=lambda entry: entry["lifecycle"] == "retained")
    return ordered


def documents_from(
    document_map: Mapping[str, Any], *, repo: Path = REPO
) -> tuple[ReaderDocument, ...]:
    """The cards for a document map, grouped and ordered as the overview shows them."""
    entries = {entry["path"]: entry for entry in document_map["documents"]}
    unmapped = [path for path in (*START, *RESULTS) if path not in entries]
    if unmapped:
        raise ValueError(f"the overview lists documents the map does not record: {unmapped}")
    fixed: tuple[tuple[Group, tuple[str, ...]], ...] = (("start", START), ("results", RESULTS))
    cards = [_card(entries[path], group, repo) for group, paths in fixed for path in paths]
    reports = [entry for path, entry in entries.items() if path.startswith(REPORTS)]
    cards.extend(_card(entry, "reports", repo) for entry in _report_order(reports))
    return tuple(cards)


@cache
def reader_documents() -> tuple[ReaderDocument, ...]:
    """Every document the overview lists, grouped and ordered as the spec describes."""
    return documents_from(load_map())
