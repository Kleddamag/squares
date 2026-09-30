#!/usr/bin/env python3
"""The frontier atlas and tutorial pages of the published site.

`devtools.render_overview` collects them from `pages()` and renders them into the shared
site shell.
"""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

from devtools.site_kit import Page

RENDER_INPUTS: tuple[Path, ...] = (Path(__file__),)


def pages() -> Iterable[Page]:
    return ()
