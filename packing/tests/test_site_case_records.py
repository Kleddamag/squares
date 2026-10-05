"""The case records in a browser, served as the deployed site serves them (think-t21m).

A case's record is fetched, by the record page and by every case popover, so these
checks need a server: a page read from a file cannot fetch another file. They hold the
three ways in to one record: a frontier row and an atlas cell open it in the case
popover, which steps to the neighbouring case in place; a record file sends a reader on
to the record page, which shows it and keeps the record's own address in the bar; and
the old one-page address, `cases.html#n-17`, still arrives at case 17. Without scripts,
a record file is read where it is.
"""

from __future__ import annotations

import contextlib
import socket
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest

from devtools import render_case_pages, render_overview
from devtools.preview_site import serve, settle_math
from sqpack.probes import probe
from tests import site_browser, site_renders

PROBES = Path(__file__).resolve().parent / "probes"
FIGURE = probe(PROBES, "case_popover_figure/figure")
CROSS = probe(PROBES, "case_popover_head/cross")


def _free_port() -> int:
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        return int(probe.getsockname()[1])


@pytest.fixture(scope="module")
def served(tmp_path_factory: pytest.TempPathFactory) -> Iterator[str]:
    """The overview, the frontier, the record page, every record file and the
    forwarders, served on a local address; the address, with its closing slash."""
    root = Path(tmp_path_factory.mktemp("cases"))
    files = [
        site_renders.page("index.html"),
        site_renders.page("frontier.html"),
        site_renders.page(render_case_pages.CASES_PAGE),
        *(
            render_overview.Page(name, text)
            for name, text in site_renders.case_records().items()
        ),
        *render_overview.forwarder_pages(),
    ]
    render_overview.write_site(root, files)
    server = serve(root, _free_port())
    try:
        yield f"http://127.0.0.1:{server.server_port}/"
    finally:
        server.shutdown()
        server.server_close()


@pytest.fixture(scope="module")
def browser() -> Iterator[Any]:
    sync_api = site_browser.api()
    with sync_api.sync_playwright() as driver:
        launched = site_browser.launch(driver)
        yield launched
        launched.close()


@contextlib.contextmanager
def _page(browser: Any, *, scripts: bool = True, width: int = 1280) -> Iterator[Any]:
    context = browser.new_context(
        java_script_enabled=scripts, viewport={"width": width, "height": 900}
    )
    try:
        yield context.new_page()
    finally:
        context.close()


def _shown_case(popover: Any) -> str | None:
    """The case the popover's record is, by its article."""
    return popover.locator("[data-case-body] article.site-case").get_attribute("data-case")


def test_a_frontier_row_opens_its_record_and_steps_to_the_next(
    browser: Any, served: str
) -> None:
    """Pressing a row anywhere opens the case popover on its record, the visual summary
    first, with the action to the record's own address; the right arrow key and the
    record's own step move it to the next case in place, and the row of the case shown
    reads as expanded; Escape closes it, every row reads as collapsed, and focus is back
    on the row that opened it. Enter on a row opens it too."""
    sync_api = site_browser.api()
    with _page(browser) as page:
        page.goto(f"{served}frontier.html", wait_until="load")
        row = page.locator("#n-12")
        row.scroll_into_view_if_needed()
        row.locator("td.site-thumb svg").click()
        popover = page.locator("#pop-case")
        popover.locator("[data-case-body] article.site-case").wait_for()
        assert popover.is_visible()
        assert _shown_case(popover) == "12"
        assert row.get_attribute("aria-expanded") == "true"
        assert popover.locator(".site-case-summary figure svg").count() == 1
        assert popover.locator(".site-case-summary .site-atlas-gap").count() == 1
        action = popover.locator("[data-case-open]").get_attribute("href") or ""
        assert action.endswith("cases/12.html")
        # The record's links were written from its own directory and are rebased here.
        frontier_link = popover.locator('.site-case-links a:has-text("In the frontier")')
        assert (frontier_link.get_attribute("href") or "").endswith("frontier.html#n-12")
        page.keyboard.press("ArrowRight")
        popover.locator('[data-case-body] article.site-case[data-case="13"]').wait_for()
        assert row.get_attribute("aria-expanded") == "false"
        assert page.locator("#n-13").get_attribute("aria-expanded") == "true"
        popover.locator('[data-case-body] a[data-case-step="14"]').click()
        popover.locator('[data-case-body] article.site-case[data-case="14"]').wait_for()
        assert popover.is_visible()
        page.keyboard.press("Escape")
        assert not popover.is_visible()
        assert page.locator('tr[data-case-row][aria-expanded="true"]').count() == 0
        sync_api.expect(row).to_be_focused()
        page.keyboard.press("Enter")
        popover.locator('[data-case-body] article.site-case[data-case="12"]').wait_for()
        assert popover.is_visible()


def test_a_record_opens_a_case_its_prose_links_in_place(browser: Any, served: str) -> None:
    """A case file's link to another case file is marked for the case popover
    (`mark_case_links`): in the popover it loads that case in place, and the page stays
    where it is."""
    with _page(browser) as page:
        page.goto(f"{served}frontier.html", wait_until="load")
        page.locator("#n-13 td.site-col-n a").click()
        popover = page.locator("#pop-case")
        popover.locator('[data-case-body] article.site-case[data-case="13"]').wait_for()
        prose = popover.locator('[data-case-body] .site-case-prose a[data-case="32"]').first
        prose.scroll_into_view_if_needed()
        prose.click()
        popover.locator('[data-case-body] article.site-case[data-case="32"]').wait_for()
        assert page.url == f"{served}frontier.html"


def test_an_atlas_cell_opens_the_same_record(browser: Any, served: str) -> None:
    """A tile opens the case popover on its record; Escape closes it and focus is back
    on the tile."""
    sync_api = site_browser.api()
    with _page(browser) as page:
        page.goto(served, wait_until="load")
        page.locator("[data-atlas-grid]").scroll_into_view_if_needed()
        cell = page.locator('.site-atlas-cell[data-case="11"]')
        cell.wait_for()
        cell.click()
        popover = page.locator("#pop-case")
        popover.locator('[data-case-body] article.site-case[data-case="11"]').wait_for()
        assert popover.is_visible()
        assert popover.locator(".site-case-summary figure svg").count() == 1
        page.keyboard.press("Escape")
        assert not popover.is_visible()
        sync_api.expect(cell).to_be_focused()


@pytest.mark.parametrize("width", [1280, 390])
@pytest.mark.parametrize("opener", ["frontier", "atlas"])
def test_the_popovers_drawing_fills_its_width_at_its_own_line_weight(
    browser: Any, served: str, opener: str, width: int
) -> None:
    """Opened from a frontier row or an atlas cell, on a laptop's window and a phone's,
    the case popover's drawing is square and as wide as the panel's body, short of the
    panel's height less 8rem (`think-u214`), and the page is no wider than the window.
    Its frame and outlines are drawn in the page's own units, as heavy as at the
    drawing's own share of its width up to 12rem across and no heavier (`think-pkz0`):
    2.3 and 1.1 pixels in a 700px drawing, not the 8.2 and 4.1 the drawing's own units
    would give them. Case 10's caption, side 3 + ½√2, keeps its radical, which the
    drawing's sizing once collapsed."""
    with _page(browser, width=width) as page:
        if opener == "frontier":
            page.goto(f"{served}frontier.html", wait_until="load")
            row = page.locator("#n-10")
            row.scroll_into_view_if_needed()
            row.locator("td.site-thumb svg").click()
        else:
            page.goto(served, wait_until="load")
            page.locator("[data-atlas-grid]").scroll_into_view_if_needed()
            cell = page.locator('.site-atlas-cell[data-case="10"]')
            cell.wait_for()
            cell.scroll_into_view_if_needed()
            cell.click()
        popover = page.locator("#pop-case")
        popover.locator('[data-case-body] article.site-case[data-case="10"]').wait_for()
        popover.locator(".site-case-figure > figcaption .katex svg").first.wait_for()
        drawn = page.evaluate(FIGURE)
        assert drawn is not None
        assert drawn["caption_math"], drawn
        assert min(drawn["caption_math"]) > 0.5 * drawn["rem"], drawn
        tallest = drawn["panel_height"] - 8 * drawn["rem"]
        assert drawn["width"] == pytest.approx(min(drawn["body"], tallest), abs=1), drawn
        assert drawn["height"] == pytest.approx(drawn["width"], abs=0.5), drawn
        if width == 1280:
            assert drawn["width"] == pytest.approx(tallest, abs=1), drawn
            assert drawn["width"] > 1.5 * 24 * drawn["rem"], drawn
        else:
            assert drawn["width"] == pytest.approx(drawn["body"], abs=1), drawn
        assert drawn["frame_effect"] == drawn["outline_effect"] == "non-scaling-stroke"
        lines = min(drawn["width"], 12 * drawn["rem"])
        assert drawn["frame"] == pytest.approx(lines * 1.2 / 102, abs=0.01), drawn
        assert drawn["outline"] == pytest.approx(lines * 0.6 / 102, abs=0.01), drawn
        assert drawn["page_width"] <= drawn["window_width"], drawn
        assert drawn["popover_right"] <= drawn["window_width"], drawn


@pytest.mark.parametrize("width", [1280, 390])
def test_the_popovers_cross_stands_in_its_corner_clear_of_the_steps(
    browser: Any, served: str, width: int
) -> None:
    """On a laptop's window and a phone's, the case popover's close cross stands inside
    the panel at its corner, and the record's steps end before it: the next case's link
    once ended under the cross, which the card's horizontal inset, read by the sticky
    cross as a second limit, had set a padding's width in from the corner
    (`think-0dxa`)."""
    with _page(browser, width=width) as page:
        page.goto(f"{served}frontier.html", wait_until="load")
        row = page.locator("#n-10")
        row.scroll_into_view_if_needed()
        row.locator("td.site-thumb svg").click()
        popover = page.locator("#pop-case")
        popover.locator('[data-case-body] article.site-case[data-case="10"]').wait_for()
        head = page.evaluate(CROSS)
        assert head is not None
        assert head["cross_right"] <= head["panel_right"] + 0.5, head
        assert head["panel_right"] - head["cross_right"] <= 16, head
        assert head["next_right"] <= head["cross_left"] + 0.5, head


def test_a_record_file_shows_in_the_record_page_at_its_own_address(
    browser: Any, served: str
) -> None:
    """A shared link to `cases/11.html` lands on the record page showing case 11, with
    `cases/11.html` still in the bar and the record's own title; its steps move to the
    neighbouring case in place, and All cases goes back to the index."""
    with _page(browser) as page:
        page.goto(f"{served}cases/11.html", wait_until="load")
        page.wait_for_url(f"{served}cases/11.html")
        reader = page.locator("[data-case-reader]")
        reader.locator('article.site-case[data-case="11"]').wait_for()
        settle_math(page)
        assert page.title() == "n = 11 · Case Records · The Squares Project"
        assert not page.locator(".site-case-front").is_visible()
        reader.locator('a[data-case-step="12"]').click()
        reader.locator('article.site-case[data-case="12"]').wait_for()
        assert page.url == f"{served}cases/12.html"
        page.go_back()
        reader.locator('article.site-case[data-case="11"]').wait_for()
        assert page.url == f"{served}cases/11.html"
        reader.locator("a[data-case-index]").click()
        page.locator("nav[data-case-index]").wait_for()
        assert page.url == f"{served}cases/"
        assert page.locator(".site-case-front").is_visible()


def test_the_old_one_page_address_arrives_at_the_case(browser: Any, served: str) -> None:
    with _page(browser) as page:
        page.goto(f"{served}cases.html#n-17", wait_until="load")
        page.wait_for_url(f"{served}cases/17.html")
        page.locator('[data-case-reader] article.site-case[data-case="17"]').wait_for()


def test_a_record_that_cannot_be_fetched_does_not_trap_back(browser: Any, served: str) -> None:
    """An address naming a case with no record file sends the reader to the file itself,
    in place of the address, so Back returns to where the reader came from."""
    with _page(browser) as page:
        page.goto(f"{served}frontier.html", wait_until="load")
        page.goto(f"{served}cases/?n=999", wait_until="load")
        page.wait_for_url(f"{served}cases/999.html?raw")
        page.go_back(wait_until="load")
        assert page.url == f"{served}frontier.html"


def test_without_scripts_a_record_file_is_read_where_it_is(browser: Any, served: str) -> None:
    with _page(browser, scripts=False) as page:
        page.goto(f"{served}cases/29.html", wait_until="load")
        assert page.url == f"{served}cases/29.html"
        assert page.locator('article.site-case[data-case="29"]').is_visible()
        assert page.locator("article.site-case figure svg").count() == 1
