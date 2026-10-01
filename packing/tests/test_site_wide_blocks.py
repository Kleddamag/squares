"""No wide block of a site page is cut off by an ancestor that clips, in a browser.

A wide block (a table with its filter bar and count, a row of cards, the atlas grid,
the film) is wider than the reading column, and a narrow page clips at the document's
edge. A block sized from the window ran under that clip: the window counts a scrollbar
the layout does not, so the first letters of the filter labels and the last of the count
were cut. `preview_site.clipped` finds any such block, and this holds the site's pages to
none, at the widths a tablet and a phone have, with and without a scrollbar's width
taken from the layout (`templates/paper-design.md`, Spacing).

Skipped where no Chromium can be launched; `SQPACK_CHROMIUM` names one the environment
supplies, as the other browser tools read it.
"""

from __future__ import annotations

import os
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest

from devtools.preview_site import CLIP_WIDTHS, CLIPPED, SCROLLBAR_PX, clipped
from devtools.render_explainer_pdf import BROWSER_OVERRIDE
from tests import site_renders

PAGES = ("index.html", "all-results.html", "frontier.html", "visualize.html", "tutorial.html")
WIDTHS = (*CLIP_WIDTHS, 390)
#: The rule the wide track had: its room measured from the window, a rem a side.
FROM_THE_WINDOW = ".site-page .site-wide { --site-wide-room: calc(100vw - 2rem) !important; }"


@pytest.fixture(scope="module")
def browser() -> Iterator[Any]:
    sync_api = pytest.importorskip("playwright.sync_api")
    with sync_api.sync_playwright() as driver:
        try:
            launched = driver.chromium.launch(executable_path=os.environ.get(BROWSER_OVERRIDE))
        except sync_api.Error as error:
            pytest.skip(f"no Chromium to launch: {error.message.splitlines()[0]}")
        yield launched
        launched.close()


@pytest.fixture(scope="module")
def pages(tmp_path_factory: pytest.TempPathFactory) -> dict[str, Path]:
    root = tmp_path_factory.mktemp("site")
    written: dict[str, Path] = {}
    for name in PAGES:
        path = root / name
        path.write_text(site_renders.html(name), encoding="utf-8")
        written[name] = path
    return written


@pytest.mark.parametrize("name", PAGES)
def test_no_wide_block_runs_past_an_ancestor_that_clips_it(
    browser: Any, pages: dict[str, Path], name: str
) -> None:
    for width in WIDTHS:
        page = browser.new_page(viewport={"width": width, "height": 900})
        try:
            page.goto(pages[name].as_uri(), wait_until="load")
            assert clipped(page) == [], f"{name} at {width}"
        finally:
            page.close()


def test_a_block_sized_from_the_window_is_caught(browser: Any, pages: dict[str, Path]) -> None:
    """The control: with the wide track sized from the window again, the results table,
    its filter bar and its count run past the document's clip on a tablet, further still
    once a scrollbar takes its width from the layout, and the check names each."""
    page = browser.new_page(viewport={"width": 768, "height": 900})
    try:
        page.goto(pages["all-results.html"].as_uri(), wait_until="load")
        page.add_style_tag(content=FROM_THE_WINDOW)
        plain = page.evaluate(CLIPPED, {"scrollbar": 0})
        narrowed = page.evaluate(CLIPPED, {"scrollbar": SCROLLBAR_PX})
    finally:
        page.close()
    for found, past in ((plain, 16), (narrowed, 16 + SCROLLBAR_PX / 2)):
        by_block = {row["block"]: row for row in found}
        for block in ("div.site-table-tools.site-result-filters", "div.site-table-wrap"):
            assert (by_block[block]["left"], by_block[block]["right"]) == (past, past), block
        assert by_block["span.site-count"]["right"] == past
        assert {row["frame"] for row in found} == {"article.kpress"}
