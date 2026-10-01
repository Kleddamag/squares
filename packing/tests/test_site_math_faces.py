"""Every formula on the site's pages is set in the face its place asks for, in a browser.

Math takes the face of the text around it, serif in serif prose and sans in sans text,
and a headline of mathematics standing alone is serif though the headline is sans
(`templates/paper-design.md`, Math). The face is chosen in the browser, from the text's
computed face, so only a browser can say what a formula was set in. This renders the
pages that between them carry every sans surface (cards and their notes, popovers, chips,
tables and their disclosures, a case record's panels), opens each once in Chromium, has
its math typeset and walks every formula with the probe `devtools.preview_site` fails a
build on. A wrong face on any of them fails here; `preview_site --shots` is the same
walk over every page of a built site.

Each page is rendered and walked once, in a module fixture, so no test carries a page's
load in its own call time. Skipped where no Chromium can be launched; `SQPACK_CHROMIUM`
names one the environment supplies, as the other browser tools read it.
"""

from __future__ import annotations

import os
from collections.abc import Iterator, Sequence
from pathlib import Path
from typing import Any

import pytest

from devtools import render_case_pages, render_overview
from devtools import render_frontier_page as frontier
from devtools.measure_site_pages import MATH_FACES
from devtools.preview_site import MATH_FACE, press, settle_math
from devtools.render_explainer_pdf import BROWSER_OVERRIDE

SANS_TEXT = "Source Sans 3 Variable"
SERIF_MATH, SANS_MATH = "KPress Math Text", "KPress Math Text Sans"
#: The cases whose records stand in for the case records page, which is 9 MB whole: the
#: settled case, with a closed form in every panel, and an open one.
CASES = (11, 29)
ATLAS_CELL = '[data-atlas-n="11"]'
CASE_LINK = 'a[data-case="11"]'
EXPLAINER_CARD = '[popovertarget="pop-page-explainer"]'

#: A walk's findings: the formulas set in the wrong face, and every formula counted by
#: (surface, text face, math face).
Walk = tuple[list[str], dict[tuple[str, str, str], dict[str, Any]]]


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
def root(tmp_path_factory: pytest.TempPathFactory) -> Path:
    return tmp_path_factory.mktemp("site")


def walk(browser: Any, address: str, *, presses: Sequence[str], whole: bool) -> Walk:
    """Open `address`, press each of `presses`, and walk its formulas. `whole` first
    scrolls the page through to its foot, which places what it lays out lazily and
    typesets all its math; without it the walk reads what the page has typeset by the
    time the last press's own math is done."""
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    try:
        page.goto(address, wait_until="load")
        if whole:
            assert settle_math(page) == 0, "math left untypeset"
        for selector in presses:
            press(page, selector)
            page.keyboard.press("Escape")
        found: list[dict[str, Any]] = page.evaluate(MATH_FACES)
        rows = {(row["surface"], row["text"], row["math"]): row for row in found}
        return page.evaluate(MATH_FACE), rows
    finally:
        page.close()


@pytest.fixture(scope="module")
def overview_html() -> str:
    return render_overview.overview_page().html


@pytest.fixture(scope="module")
def overview(browser: Any, root: Path, overview_html: str) -> Walk:
    path = root / "index.html"
    path.write_text(overview_html, encoding="utf-8")
    return walk(browser, path.as_uri(), presses=(ATLAS_CELL,), whole=True)


@pytest.fixture(scope="module")
def results(browser: Any, root: Path) -> Walk:
    path = root / render_overview.RESULTS_PAGE
    path.write_text(render_overview.results_page().html, encoding="utf-8")
    return walk(browser, path.as_uri(), presses=(), whole=True)


@pytest.fixture(scope="module")
def frontier_atlas(browser: Any, root: Path) -> Walk:
    path = root / "frontier.html"
    path.write_text(render_overview.frontier_page().html, encoding="utf-8")
    return walk(browser, path.as_uri(), presses=(CASE_LINK,), whole=False)


def case_records_page() -> str:
    """The records of `CASES` as the case records page sets them, without the other 322."""
    cases = {case["n"]: case for case in frontier.frontier_cases()}
    recent = frontier.recent_lower_bounds()
    records = "\n\n".join(
        render_case_pages.record_markdown(
            cases[n], recent=recent.get(n, False), first=min(cases), last=max(cases)
        )
        for n in CASES
    )
    return render_overview.kpress_page(
        f'<div class="site-case-records" data-case-records>\n\n{records}\n\n</div>',
        name=render_case_pages.CASES_PAGE,
        current="frontier",
        title="Case Records",
        description="Case records",
        toc=False,
        page_scripts=(render_case_pages.CASE_VIEW_SCRIPT,),
    ).html


@pytest.fixture(scope="module")
def case_records(browser: Any, root: Path) -> dict[int, Walk]:
    path = root / "case-records.html"
    path.write_text(case_records_page(), encoding="utf-8")
    return {n: walk(browser, f"{path.as_uri()}#n-{n}", presses=(), whole=True) for n in CASES}


def test_the_overviews_sans_surfaces_set_sans_math_and_its_math_headline_serif(
    overview: Walk,
) -> None:
    """The overview's cards, notes, popovers and tables are sans text with sans math; the
    atlas popover's headline, `n = 11` alone, is serif; and nothing is set wrongly."""
    wrong, rows = overview
    assert wrong == []
    for surface in ("card headline", "card note", "popover headline", "table cell"):
        assert rows[(surface, SANS_TEXT, SANS_MATH)]["count"] > 0, surface
        assert rows[(surface, SANS_TEXT, SANS_MATH)]["alone"] == 0, surface
    headline = rows[("popover headline", SANS_TEXT, SERIF_MATH)]
    assert headline["count"] == headline["alone"] == 1
    assert headline["example"] == "n = 11"
    assert ("card headline", SANS_TEXT, SERIF_MATH) not in rows


def test_the_results_table_sets_sans_math(results: Walk) -> None:
    wrong, rows = results
    assert wrong == []
    assert rows[("summary", SANS_TEXT, SANS_MATH)]["count"] > 0
    assert {key[2] for key in rows if key[1] == SANS_TEXT} == {SANS_MATH}


def test_the_case_popovers_headline_is_serif_math(frontier_atlas: Walk) -> None:
    """The frontier atlas's table is sans math, and its case popover's headline, set by
    script as `n = 11`, is typeset and serif."""
    wrong, rows = frontier_atlas
    assert wrong == []
    assert rows[("table cell", SANS_TEXT, SANS_MATH)]["count"] > 0
    headline = rows[("popover headline", SANS_TEXT, SERIF_MATH)]
    assert headline["count"] == headline["alone"] == 1
    assert headline["example"] == "n = 11"


@pytest.mark.parametrize("n", CASES)
def test_a_case_records_panels_set_sans_math(case_records: dict[int, Walk], n: int) -> None:
    wrong, rows = case_records[n]
    assert wrong == []
    for surface in ("case head", "case bounds"):
        assert rows[(surface, SANS_TEXT, SANS_MATH)]["count"] > 0, surface
    assert not [key for key in rows if key[0].startswith("case") and key[2] != SANS_MATH]


def test_the_walk_catches_serif_math_in_a_sans_headline(
    browser: Any, root: Path, overview_html: str
) -> None:
    """The control: mark a headline that has words in it for serif mathematics, as every
    popover's headline once was, and the walk names it."""
    plain = '<p class="site-popover-value">Earlier '
    assert overview_html.count(plain) == 1
    marked = root / "marked.html"
    marked.write_text(
        overview_html.replace(
            plain, '<p class="site-popover-value" data-math-face="serif">Earlier '
        ),
        encoding="utf-8",
    )
    wrong, _ = walk(browser, marked.as_uri(), presses=(EXPLAINER_CARD,), whole=False)
    assert wrong == [
        "serif math in sans text: p.site-popover-value in #pop-page-explainer: n = 11"
    ]
