#!/usr/bin/env python3
"""The files the site's pages serve beside them: previews, drawings and the favicon.

`devtools.render_overview` collects them from `assets()` and writes them into its output
directory; nothing here is committed, so no file under `DATA_PATHS` changes.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

from devtools.site_kit import Asset

RENDER_INPUTS: tuple[Path, ...] = (Path(__file__),)


@dataclass(frozen=True)
class Preview:
    """An atlas preview image and the PDF it links to, both site-relative.

    `image` is the preview PNG this module writes; `pdf` is the composite PDF served beside
    the pages. `size` and `pages` are for the caption, for example `87 KB` and
    `25 by 30 in`.
    """

    image: str
    width: int
    height: int
    alt: str
    pdf: str
    size: str
    pages: str
    edition: str


@dataclass(frozen=True)
class Film:
    """The overview's one embedded film: the full `n = 1…324` ascent, never autoplayed.

    `src` and `poster` are site-relative; `type` is the `<source>` type attribute.
    """

    src: str
    type: str
    poster: str
    width: int
    height: int
    size: str
    duration: str
    edition: str
    release: str


def atlas_previews() -> tuple[Preview, ...]:
    """The `n = 1…100` and `n = 1…324` previews, in that order."""
    raise NotImplementedError


def atlas_film() -> Film:
    """The `n = 1…324` film as the overview embeds it."""
    raise NotImplementedError


def hero_svg() -> str:
    """The `n = 53` packing, stripped of ids, titles and descriptions, to inline."""
    raise NotImplementedError


def thumbnail_path(n: int) -> str:
    """The site-relative path of case `n`'s thumbnail, for the frontier atlas page."""
    return f"thumbs/n-{n:03d}.svg"


def favicon_svg() -> str:
    """The site's favicon, inlined into every page as a data URI."""
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16">'
        '<rect width="16" height="16" fill="#444"/></svg>'
    )


def assets() -> Iterable[Asset]:
    return ()
