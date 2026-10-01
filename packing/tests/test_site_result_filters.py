"""Hide superseded, the result filters' checkbox, in a browser.

Both tables of results sit under one filter bar (`overview_sections.result_filters`,
`templates/paper-design.md`, Result filters). Its one checkbox, Hide superseded, starts
checked on the overview and clear on the results page. This opens both rendered pages in
Chromium and uses the checkbox as a reader does, with the pointer on its label and with
the keyboard, and reads the table after each change through one probe: the rows showing
are the ones the register's standings say, the count follows, the checkbox narrows
Standing, and a fresh load of the page starts again from that page's own default. The
bar has no reset control, so a load is the only reset there is; the default a load
returns to is the checkbox's state in the HTML, which the probe reports too.

The page's clock is fixed at the register's reference date, the day the HTML's own
`hidden` rows are reckoned from (`overview_sections.reference_date`), so the rows Max age
keeps are the same in the browser as in the render, whatever day the test runs.

The checkbox and its label are also measured at the three widths the design is shot at:
the label on one line, inside the bar, its words level with the labels beside it.

Skipped where no Chromium can be launched; `SQPACK_CHROMIUM` names one the environment
supplies, as the other browser tools read it.
"""

from __future__ import annotations

import os
from collections.abc import Iterator
from datetime import datetime, time
from pathlib import Path
from typing import Any

import pytest

from devtools import overview_data, overview_sections, render_recent_results
from devtools.render_explainer_pdf import BROWSER_OVERRIDE
from sqpack.probes import probe
from tests import site_renders

PROBES = Path(__file__).resolve().parent / "probes"
STATE = probe(PROBES, "site_result_filters/state")

#: Each page with a table of results, and where its bar starts.
PAGES = {
    "index.html": overview_sections.RECENT_DEFAULTS,
    "all-results.html": overview_sections.RESULTS_DEFAULTS,
}
#: The widths the design is shot at: a desktop, a tablet and a phone.
WIDTHS = (1280, 768, 390)
LABEL = "Hide superseded"
STANDING = '.site-result-filters select[data-filter="standing"]'


@pytest.fixture(scope="module")
def overview() -> overview_data.Overview:
    return site_renders.overview()


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


def opened(
    browser: Any, path: Path, overview: overview_data.Overview, width: int = 1280
) -> Any:
    """The page at `path`, loaded on the register's reference date."""
    page = browser.new_page(viewport={"width": width, "height": 900})
    noon = datetime.combine(overview_sections.reference_date(overview), time(12))
    page.clock.set_fixed_time(noon)
    page.goto(path.as_uri(), wait_until="load")
    return page


def state(page: Any) -> dict[str, Any]:
    found = page.evaluate(STATE)
    assert found is not None, "the page has no results table under a filter bar"
    return found


def rows(
    overview: overview_data.Overview, defaults: overview_sections.FilterDefaults
) -> list[str]:
    """The ids of the rows a bar at `defaults` shows on the reference date, sorted."""
    reference = overview_sections.reference_date(overview)
    return sorted(
        result.id.lower()
        for result in overview.results
        if overview_sections.shown_by_default(result, defaults, reference)
    )


def count(shown: int, overview: overview_data.Overview) -> str:
    return overview_sections.count_text(shown, len(overview.results))


@pytest.mark.parametrize("name", PAGES)
def test_the_checkbox_starts_at_its_pages_default_and_the_table_with_it(
    browser: Any, pages: dict[str, Path], overview: overview_data.Overview, name: str
) -> None:
    """On load the checkbox is checked on the overview and clear on the results page,
    as its HTML has it; the rows showing are the ones that page's defaults keep, and
    the count is theirs. The rows that carry the flag are, on both pages, every result
    that is not superseded: the current bests, the second certificates and the results
    that are not bounds."""
    defaults = PAGES[name]
    page = opened(browser, pages[name], overview)
    try:
        found = state(page)
    finally:
        page.close()
    assert found["type"] == "checkbox"
    assert found["label"] == LABEL
    assert found["checked"] is found["starts_checked"] is defaults.hide_superseded
    assert defaults.hide_superseded is (name == "index.html")
    expected = rows(overview, defaults)
    assert sorted(found["shown"]) == expected
    assert found["total"] == len(overview.results)
    assert found["count"] == count(len(expected), overview)
    current = sorted(
        result.id.lower()
        for result in overview.results
        if result.standing != render_recent_results.SUPERSEDED
    )
    assert sorted(found["current"]) == current
    assert {result.standing for result in overview.results if result.id.lower() in current} >= {
        render_recent_results.HOLDS,
        render_recent_results.HOLDS_REPORTED,
        render_recent_results.SECOND_CERTIFICATE,
        render_recent_results.NOT_A_BOUND,
    }
    if defaults.hide_superseded:
        assert set(found["shown"]) < set(found["current"])
    else:
        assert set(found["current"]) < set(found["shown"])


@pytest.mark.parametrize("name", PAGES)
def test_toggling_it_hides_and_shows_the_superseded_rows(
    browser: Any, pages: dict[str, Path], overview: overview_data.Overview, name: str
) -> None:
    """A click on the label toggles the checkbox, and so does the space bar with the
    checkbox focused, reached by Tab from Standing. Checked, the table shows the rows
    the page's other defaults keep that are not superseded; clear, all the rows those
    defaults keep. The count follows each time, and the rows hidden stay in the page."""
    defaults = PAGES[name]
    checked = rows(overview, defaults._replace(hide_superseded=True))
    clear = rows(overview, defaults._replace(hide_superseded=False))
    assert set(checked) < set(clear)
    page = opened(browser, pages[name], overview)
    try:
        expected = {True: checked, False: clear}
        now = defaults.hide_superseded
        # The label is the control: a click on its words toggles the checkbox.
        for _ in range(2):
            page.get_by_text(LABEL, exact=True).click()
            now = not now
            found = state(page)
            assert found["checked"] is now
            assert sorted(found["shown"]) == expected[now]
            assert found["count"] == count(len(expected[now]), overview)
            assert found["total"] == len(overview.results)
        # The keyboard: Tab from Standing lands on it, and the space bar toggles it.
        page.locator(STANDING).focus()
        page.keyboard.press("Tab")
        found = state(page)
        assert found["focused"]
        for _ in range(2):
            page.keyboard.press("Space")
            now = not now
            found = state(page)
            assert found["checked"] is now
            assert sorted(found["shown"]) == expected[now]
            assert found["count"] == count(len(expected[now]), overview)
        assert now is defaults.hide_superseded
        assert found["starts_checked"] is defaults.hide_superseded
    finally:
        page.close()


@pytest.mark.parametrize("name", PAGES)
def test_a_fresh_load_returns_to_the_pages_own_default(
    browser: Any, pages: dict[str, Path], overview: overview_data.Overview, name: str
) -> None:
    """The bar has no reset control. What a reader changed is undone by loading the page
    again, which starts from the HTML: the checkbox as that page's defaults have it, and
    the rows and the count with it."""
    defaults = PAGES[name]
    page = opened(browser, pages[name], overview)
    try:
        page.get_by_label(LABEL).set_checked(not defaults.hide_superseded)
        changed = state(page)
        assert changed["checked"] is not defaults.hide_superseded
        assert changed["starts_checked"] is defaults.hide_superseded
        assert sorted(changed["shown"]) != rows(overview, defaults)
        page.goto(pages[name].as_uri(), wait_until="load")
        found = state(page)
    finally:
        page.close()
    assert found["checked"] is defaults.hide_superseded
    assert sorted(found["shown"]) == rows(overview, defaults)
    assert found["count"] == count(len(rows(overview, defaults)), overview)


def test_it_narrows_standing_and_never_sets_it(
    browser: Any, pages: dict[str, Path], overview: overview_data.Overview
) -> None:
    """Checked, with Standing at All, the results page shows every result but the
    superseded ones, and Standing then chooses among the standings left: each still
    shows all its rows. The one standing the box hides, superseded, leaves no row while
    it is checked, and the count says so; clearing the box brings those rows back.
    Neither control changes the other."""
    by_standing: dict[str, list[str]] = {}
    for result in overview.results:
        key = overview_sections.standing_key(result.standing)
        by_standing.setdefault(key, []).append(result.id.lower())
    kept = sorted(by_standing.keys() - {"superseded"})
    assert {
        "current-best",
        "current-best-reported",
        "second-certificate",
        "not-a-bound",
    } <= set(kept)
    page = opened(browser, pages["all-results.html"], overview)
    try:
        box = page.get_by_label(LABEL)
        box.check()
        found = state(page)
        assert sorted(found["shown"]) == sorted(
            entry for key in kept for entry in by_standing[key]
        )
        assert len(found["shown"]) == len(overview.results) - len(by_standing["superseded"])
        for key in kept:
            page.locator(STANDING).select_option(key)
            found = state(page)
            assert sorted(found["shown"]) == sorted(by_standing[key]), key
            assert found["checked"]
        page.locator(STANDING).select_option("superseded")
        found = state(page)
        assert found["shown"] == []
        assert found["count"] == count(0, overview)
        assert found["checked"]
        assert page.locator(STANDING).input_value() == "superseded"
        box.uncheck()
        found = state(page)
        assert sorted(found["shown"]) == sorted(by_standing["superseded"])
        assert page.locator(STANDING).input_value() == "superseded"
    finally:
        page.close()


def test_a_link_can_set_it_or_clear_it(
    browser: Any, pages: dict[str, Path], overview: overview_data.Overview
) -> None:
    """`current=true` opens the results page with the box checked, and `current=false` opens
    the overview with it clear, each with the rows that leaves."""
    opens = {
        "all-results.html": ("?current=true", True),
        "index.html": ("?current=false", False),
    }
    for name, (query, checked) in opens.items():
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        noon = datetime.combine(overview_sections.reference_date(overview), time(12))
        page.clock.set_fixed_time(noon)
        try:
            page.goto(pages[name].as_uri() + query, wait_until="load")
            found = state(page)
        finally:
            page.close()
        assert found["checked"] is checked, name
        assert found["starts_checked"] is PAGES[name].hide_superseded, name
        expected = rows(overview, PAGES[name]._replace(hide_superseded=checked))
        assert sorted(found["shown"]) == expected, name
        assert found["count"] == count(len(expected), overview), name


@pytest.mark.parametrize("width", WIDTHS)
@pytest.mark.parametrize("name", PAGES)
def test_the_checkbox_and_its_label_sit_in_the_bar_at_every_width(
    browser: Any,
    pages: dict[str, Path],
    overview: overview_data.Overview,
    name: str,
    width: int,
) -> None:
    """At a desktop's, a tablet's and a phone's width the label's words are on one line
    and inside the bar, as every control's label is, and the bar has nothing running
    past it. The words are level with those of the labels on the same line, whose
    controls are taller. The checkbox takes the site's accent and is reached by Tab."""
    page = opened(browser, pages[name], overview, width)
    try:
        found = state(page)
    finally:
        page.close()
    assert found["reachable"]
    assert found["accent"] not in {"", "auto"}
    assert len(found["label_lines"]) == 1, found["label_lines"]
    assert found["label_before"] <= 0.5
    assert found["label_after"] <= 0.5
    assert found["bar_overflow"] <= 0
    (line,) = found["label_lines"]
    beside = 0
    for other in found["labels"]:
        assert other["after"] <= 0.5, other
        assert len(other["lines"]) >= 1, other
        first = other["lines"][0]
        if (
            other["filter"] != "current"
            and first["top"] < line["bottom"]
            and line["top"] < first["bottom"]
        ):
            assert first["bottom"] == pytest.approx(line["bottom"], abs=1), other
            beside += 1
    assert [other["filter"] for other in found["labels"]].count("current") == 1
    assert beside >= 1, "no label shares the checkbox's line"
