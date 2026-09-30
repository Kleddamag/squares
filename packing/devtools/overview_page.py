#!/usr/bin/env python3
"""The overview page, the site's front door, rendered into the shared site shell.

Its prose lives in `templates/overview-article.md`, reviewed as prose and formatted by
flowmark; every fact in it is a placeholder filled from the record, so no bound is ever a
literal in the template. `devtools.render_overview` collects the page from `pages()`.
"""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

from devtools.site_kit import SITE_NAME, TEMPLATES, Page

TEMPLATE = TEMPLATES / "overview-article.md"

RENDER_INPUTS: tuple[Path, ...] = (Path(__file__), TEMPLATE)

DESCRIPTION = (
    "The square packing problem, and every current result on it, by this project and "
    "by others, with how far each has been verified."
)


def pages() -> Iterable[Page]:
    yield Page(
        key="overview",
        path="index.html",
        title=SITE_NAME,
        description=DESCRIPTION,
        markdown=TEMPLATE.read_text(encoding="utf-8"),
    )
