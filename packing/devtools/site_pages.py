#!/usr/bin/env python3
"""The frontier atlas and tutorial pages of the published site.

`devtools.render_overview` collects them from `pages()` and renders them into the shared
site shell.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from devtools.site_kit import Page

RENDER_INPUTS: tuple[Path, ...] = (Path(__file__),)


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
    group: Literal["start", "results", "reports"]
    url: str
    date: str | None
    dated: bool


def reader_documents() -> tuple[ReaderDocument, ...]:
    """Every document the overview lists, grouped and ordered as the spec describes."""
    raise NotImplementedError


def pages() -> Iterable[Page]:
    return ()
