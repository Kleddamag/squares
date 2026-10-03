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

import html
import os
import re
import socket
from collections.abc import Iterator, Sequence
from pathlib import Path
from typing import Any

import pytest

from devtools import render_case_pages, render_overview
from devtools.measure_site_pages import MATH_FACES
from devtools.preview_site import MATH_FACE, press, serve, settle_math
from devtools.render_n11_lower_bounds_explainer_pdf import BROWSER_OVERRIDE
from tests import site_renders

SANS_TEXT = "Source Sans 3 Variable"
SERIF_MATH, SANS_MATH = "KPress Math Text", "KPress Math Text Sans"
#: The cases whose records are walked: the settled case, with a closed form in every
#: panel, and an open one.
CASES = (11, 29)
#: A result row's popover headline on the results page, as `row_detail` writes one that
#: is not mathematics alone (so unmarked): the popover's id and the headline's HTML.
#: These are the popovers whose headlines have words and a formula; the page and paper
#: cards navigate and open none.
ROW_HEADLINE = re.compile(
    r'<p class="site-popover-value" id="(pop-result-t-\d+)-title">(.*?)</p>', re.DOTALL
)
#: A formula as the page carries it before it is typeset: its TeX, HTML-escaped.
FORMULA = re.compile(
    r'<span class="kpress-math-render" aria-hidden="true">\\\((.*?)\\\)</span>'
)

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


def walk(
    browser: Any, address: str, *, presses: Sequence[str], whole: bool, ready: str = ""
) -> Walk:
    """Open `address`, press each of `presses`, and walk its formulas. `whole` first
    scrolls the page through to its foot, which places what it lays out lazily and
    typesets all its math; without it the walk reads what the page has typeset by the
    time the last press's own math is done. `ready` names what a page fetches, which the
    walk waits for first."""
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    try:
        page.goto(address, wait_until="load")
        if ready:
            page.locator(ready).wait_for()
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
    return site_renders.html("index.html")


@pytest.fixture(scope="module")
def overview(browser: Any, root: Path, overview_html: str) -> Walk:
    path = root / "index.html"
    path.write_text(overview_html, encoding="utf-8")
    return walk(browser, path.as_uri(), presses=(), whole=True)


@pytest.fixture(scope="module")
def results(browser: Any, root: Path) -> Walk:
    path = root / render_overview.RESULTS_PAGE
    path.write_text(site_renders.html(render_overview.RESULTS_PAGE), encoding="utf-8")
    return walk(browser, path.as_uri(), presses=(), whole=True)


@pytest.fixture(scope="module")
def frontier_atlas(browser: Any, root: Path) -> Walk:
    path = root / "frontier.html"
    path.write_text(site_renders.html("frontier.html"), encoding="utf-8")
    return walk(browser, path.as_uri(), presses=(), whole=False)


@pytest.fixture(scope="module")
def served(root: Path) -> Iterator[str]:
    """The frontier page, the record page and the records of `CASES`, served, since a
    record is fetched; the address, with its closing slash."""
    files = [
        site_renders.page("frontier.html"),
        site_renders.page(render_case_pages.CASES_PAGE),
        *(
            render_overview.Page(
                render_case_pages.case_url(n),
                site_renders.case_records()[render_case_pages.case_url(n)],
            )
            for n in CASES
        ),
    ]
    directory = root / "served"
    render_overview.write_site(directory, files)
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        port = int(probe.getsockname()[1])
    server = serve(directory, port)
    try:
        yield f"http://127.0.0.1:{port}/"
    finally:
        server.shutdown()
        server.server_close()


@pytest.fixture(scope="module")
def case_records(browser: Any, served: str) -> dict[int, Walk]:
    """Each of `CASES` as a reader opens its record file, shown in the record page."""
    return {
        n: walk(
            browser,
            f"{served}{render_case_pages.case_url(n)}",
            presses=(),
            whole=True,
            ready=f'[data-case-reader] article.site-case[data-case="{n}"]',
        )
        for n in CASES
    }


@pytest.fixture(scope="module")
def frontier_popover(browser: Any, served: str) -> Walk:
    """The frontier page with case 11's row pressed: its record in the case popover."""
    return walk(
        browser, f"{served}frontier.html", presses=("#n-11 td.site-thumb svg",), whole=False
    )


def test_the_overviews_sans_surfaces_set_sans_math_and_its_math_headline_serif(
    overview: Walk,
) -> None:
    """The overview's cards, notes, popovers and tables are sans text with sans math; a
    popover headline that is mathematics alone is serif, each result row's whose summary
    is one bound; and nothing is set wrongly."""
    wrong, rows = overview
    assert wrong == []
    for surface in ("card headline", "card note", "popover headline", "table cell"):
        assert rows[(surface, SANS_TEXT, SANS_MATH)]["count"] > 0, surface
        assert rows[(surface, SANS_TEXT, SANS_MATH)]["alone"] == 0, surface
    headline = rows[("popover headline", SANS_TEXT, SERIF_MATH)]
    assert headline["count"] == headline["alone"] >= 1
    assert ("card headline", SANS_TEXT, SERIF_MATH) not in rows


def test_the_results_table_sets_sans_math(results: Walk) -> None:
    """The results table's cells and its row popovers are sans text with sans math, and
    the only serif math in sans text is a popover headline that is mathematics alone."""
    wrong, rows = results
    assert wrong == []
    assert rows[("table cell", SANS_TEXT, SANS_MATH)]["count"] > 0
    serif = {key[0]: row for key, row in rows.items() if key[1:] == (SANS_TEXT, SERIF_MATH)}
    assert set(serif) <= {"popover headline"}
    assert all(row["count"] == row["alone"] for row in serif.values())


def test_the_frontier_table_sets_sans_math(frontier_atlas: Walk) -> None:
    """The frontier atlas's table is sans math. The page has no subtitle: its range of
    cases, set as sans math under the title, went on 2026-10-02 (the owner,
    `think-wz9d`). Its case popover, which fetches a record, is walked where the
    records are served (`frontier_popover`)."""
    wrong, rows = frontier_atlas
    assert wrong == []
    assert rows[("table cell", SANS_TEXT, SANS_MATH)]["count"] > 0
    assert not [key for key in rows if key[0] == "subtitle"]


def test_the_case_popover_sets_its_records_math_sans(frontier_popover: Walk) -> None:
    """A case's record in the frontier's case popover is set as on its own page: its
    head, panels and visual summary are sans text with sans math, the case file's prose
    serif with serif math, and nothing is set wrongly. In the popover the probe counts
    the record's head and panels under the popover's surface."""
    wrong, rows = frontier_popover
    assert wrong == []
    assert rows[("popover", SANS_TEXT, SANS_MATH)]["count"] > 0
    assert rows[("visual summary", SANS_TEXT, SANS_MATH)]["count"] > 0
    for surface, text, face in rows:
        if surface in {"popover", "visual summary"}:
            assert (text == SANS_TEXT) == (face == SANS_MATH), (surface, text, face)


@pytest.mark.parametrize("n", CASES)
def test_a_case_records_panels_set_sans_math(case_records: dict[int, Walk], n: int) -> None:
    wrong, rows = case_records[n]
    assert wrong == []
    for surface in ("case head", "case bounds", "visual summary"):
        assert rows[(surface, SANS_TEXT, SANS_MATH)]["count"] > 0, surface
    assert not [key for key in rows if key[0].startswith("case") and key[2] != SANS_MATH]


def test_the_walk_catches_serif_math_in_a_sans_headline(browser: Any, root: Path) -> None:
    """The control: mark a headline that has words in it for serif mathematics, as every
    popover's headline once was, and the walk names it. The headline is a result row's
    on the results page, the first whose words carry one formula: its popover is opened
    by its row's own trigger."""
    results = site_renders.html(render_overview.RESULTS_PAGE)
    target, tex = next(
        (target, FORMULA.findall(headline)[0])
        for target, headline in ROW_HEADLINE.findall(results)
        if len(FORMULA.findall(headline)) == 1 and re.match(r"\s*\w", headline)
    )
    plain = f'<p class="site-popover-value" id="{target}-title">'
    assert results.count(plain) == 1
    marked = root / "marked.html"
    marked.write_text(
        results.replace(plain, plain.replace(" id=", ' data-math-face="serif" id=', 1)),
        encoding="utf-8",
    )
    trigger = f'.site-row-open[popovertarget="{target}"]'
    wrong, _ = walk(browser, marked.as_uri(), presses=(trigger,), whole=False)
    where = f"p.site-popover-value in #{target}-title"
    assert wrong == [f"serif math in sans text: {where}: {html.unescape(tex)[:40]}"]
