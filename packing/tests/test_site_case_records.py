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
from tests import site_browser, site_renders


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
    record's own step move it to the next case in place; Escape closes it."""
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
        popover.locator('[data-case-body] a[data-case-step="14"]').click()
        popover.locator('[data-case-body] article.site-case[data-case="14"]').wait_for()
        assert popover.is_visible()
        page.keyboard.press("Escape")
        assert not popover.is_visible()


def test_an_atlas_cell_opens_the_same_record(browser: Any, served: str) -> None:
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


def test_without_scripts_a_record_file_is_read_where_it_is(browser: Any, served: str) -> None:
    with _page(browser, scripts=False) as page:
        page.goto(f"{served}cases/29.html", wait_until="load")
        assert page.url == f"{served}cases/29.html"
        assert page.locator('article.site-case[data-case="29"]').is_visible()
        assert page.locator("article.site-case figure svg").count() == 1
