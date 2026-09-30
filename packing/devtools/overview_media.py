#!/usr/bin/env python3
"""The files the site's pages serve beside them: previews, drawings and the favicon.

`devtools.render_overview` collects them from `assets()` and writes them into its output
directory; nothing here is committed, so no file under `DATA_PATHS` changes.
"""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

from devtools.site_kit import Asset

RENDER_INPUTS: tuple[Path, ...] = (Path(__file__),)


def favicon_svg() -> str:
    """The site's favicon, inlined into every page as a data URI."""
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16">'
        '<rect width="16" height="16" fill="#444"/></svg>'
    )


def assets() -> Iterable[Asset]:
    return ()
