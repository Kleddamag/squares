#!/usr/bin/env python3
"""The reader documents the overview lists as cards, read from the document map.

`docs/project/document-map.yaml` records every durable document's role, authority and
lifecycle, and a one-sentence `summary` for each document the overview shows. This
module turns those entries into the cards of the overview's Read Further section.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

REPO = Path(__file__).resolve().parents[2]
DOCUMENT_MAP = REPO / "docs" / "project" / "document-map.yaml"

RENDER_INPUTS: tuple[Path, ...] = (Path(__file__), DOCUMENT_MAP)


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
