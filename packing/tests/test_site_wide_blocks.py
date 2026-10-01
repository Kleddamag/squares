"""No wide block of a site page is cut off by an ancestor that clips, in a browser.

A wide block (a table with its filter bar and count, a row of cards, the atlas grid,
the film) is wider than the reading column, and a narrow page clips at the document's
edge. A block sized from the window ran under that clip: the window counts a scrollbar
the layout does not, so the first letters of the filter labels and the last of the count
were cut. `preview_site.clipped` finds any such block, and this holds the site's pages to
none, at the widths a tablet and a phone have, with and without a scrollbar's width
taken from the layout (`templates/paper-design.md`, Spacing).

The same browser holds the Visualize section's tabs to their place on both its pages:
under the rule that runs under the navigation bar, never over it, with the content the
shared space under them (`preview_site.tabs_problems`, `templates/paper-design.md`,
Section tabs).

Every page that may be the film's is opened as for a reader who asks for reduced motion
(`preview_site.REDUCED_MOTION`), so its film stands at its poster and no test starts the
film's download.

Skipped where no Chromium can be launched; `SQPACK_CHROMIUM` names one the environment
supplies, as the other browser tools read it.
"""

from __future__ import annotations

import os
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest

from devtools.preview_site import (
    CLIP_WIDTHS,
    CLIPPED,
    HEADER,
    REDUCED_MOTION,
    SCROLLBAR_PX,
    clipped,
    tabs_problems,
)
from devtools.render_explainer_pdf import BROWSER_OVERRIDE
from tests import site_renders

PAGES = ("index.html", "all-results.html", "frontier.html", "visualize.html", "tutorial.html")
WIDTHS = (*CLIP_WIDTHS, 390)
#: The rule the wide track had: its room measured from the window, a rem a side.
FROM_THE_WINDOW = ".site-page .site-wide { --site-wide-room: calc(100vw - 2rem) !important; }"
#: The rule the header had: its own lower border, under the tabs it holds.
RULE_UNDER_THE_TABS = (
    ".kpress-site-header:has(> .site-tabs) { border-block-end: 1px solid !important; }"
)
#: A root em in CSS pixels, and the two spaces the tabs stand in, in rem: under the rule
#: (`--site-tabs-space`) and over a page's first block (`--site-page-top`).
REM = 16
TABS_SPACE, PAGE_TOP = 0.7, 4


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
        page = browser.new_page(
            viewport={"width": width, "height": 900}, reduced_motion=REDUCED_MOTION
        )
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


@pytest.fixture(scope="module")
def section_pages(pages: dict[str, Path]) -> dict[str, tuple[Path, str, float]]:
    """The Visualize section's two pages, each with its current tab and the space its
    content starts under the tabs, in rem: the film's page as the site renders it, and
    the workbench's shell on its template with its own stylesheet and no program, which
    is all of that page the header's place needs."""
    from workbench_tools import build_site  # noqa: PLC0415

    assets = build_site.WORKBENCH_PACKAGE / "assets"
    shell = build_site.with_nav((assets / "template.html").read_text(encoding="utf-8"))
    styles = (assets / "workbench.css").read_text(encoding="utf-8")
    assert shell.count("__WORKBENCH_CSS__") == 1
    workbench = pages["visualize.html"].with_name("workbench.html")
    workbench.write_text(shell.replace("__WORKBENCH_CSS__", styles), encoding="utf-8")
    return {
        "visualize.html": (pages["visualize.html"], "Film", PAGE_TOP),
        "workbench/": (workbench, "Workbench", TABS_SPACE),
    }


@pytest.mark.parametrize("width", [1280, 390])
def test_the_section_tabs_stand_under_the_bars_rule(
    browser: Any, section_pages: dict[str, tuple[Path, str, float]], width: int
) -> None:
    """On the film's page and on the workbench, from the top: the bar, the rule under it,
    the tabs, the content. The rule is the bar's own, at the bar's foot and as long as
    the bar, where it is on every other page; the tabs start `--site-tabs-space` under
    it with their own tab current; the film starts `--site-page-top` under the tabs, and
    the application the tabs' own space under them."""
    for name, (path, current, below) in section_pages.items():
        page = browser.new_page(
            viewport={"width": width, "height": 900}, reduced_motion=REDUCED_MOTION
        )
        try:
            page.goto(path.as_uri(), wait_until="load")
            found = page.evaluate(HEADER)
        finally:
            page.close()
        where = f"{name} at {width}"
        assert tabs_problems(found) == [], where
        nav, rule, tabs, first = (found[part] for part in ("nav", "rule", "tabs", "first"))
        assert rule["on"] == "nav.site-nav", where
        assert rule["bottom"] == nav["bottom"], where
        assert (rule["left"], rule["right"]) == (nav["left"], nav["right"]), where
        assert tabs["current"] == current, where
        assert tabs["top"] - rule["bottom"] == pytest.approx(TABS_SPACE * REM, abs=0.05), where
        assert first["top"] - tabs["bottom"] == pytest.approx(below * REM, abs=0.05), where


def test_tabs_over_the_rule_are_caught(
    browser: Any, section_pages: dict[str, tuple[Path, str, float]]
) -> None:
    """The control: give the header that holds the tabs its lower border back, as it had
    while the tabs stood over the rule, and the check names the tabs on both pages."""
    for name, (path, _, _) in section_pages.items():
        page = browser.new_page(
            viewport={"width": 1280, "height": 900}, reduced_motion=REDUCED_MOTION
        )
        try:
            page.goto(path.as_uri(), wait_until="load")
            page.add_style_tag(content=RULE_UNDER_THE_TABS)
            problems = tabs_problems(page.evaluate(HEADER))
        finally:
            page.close()
        assert len(problems) == 1, name
        assert problems[0].startswith("the section tabs start "), name
        assert problems[0].endswith("which is on header"), name
