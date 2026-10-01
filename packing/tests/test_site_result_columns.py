"""The two tables of results share their width sensibly, and no chip wraps, in a browser.

Recent Results on the overview and the table of the results page are one table
(`templates/paper-design.md`, Tables). How its columns share a window is the browser's to
say, from the faces, the typeset formulas and the floors `site.css` gives the columns, so
this opens both rendered pages in Chromium and measures each table with the probes
`devtools.measure_site_pages columns` and `chips` report from: at 1280 pixels, where the
table has its 1104-pixel track to itself; at 1024 and 768, where it scrolls sideways in
its wrap; and at 390, where each row is a card.

What it holds: the table fits its track at 1280; the id column is as narrow as an id; the
credit column keeps room for its longest name, so no credit breaks inside a word; the
rungs column holds its widest chip, a kind's or a standing's; the overview carries each
result's records without showing them; and every chip on either page is one line high,
every kind and standing chip one size.

Each page is rendered and loaded once, in a module fixture, its math typeset, and then
resized for each width. Skipped where no Chromium can be launched; `SQPACK_CHROMIUM`
names one the environment supplies, as the other browser tools read it.
"""

from __future__ import annotations

import os
from collections.abc import Iterator
from pathlib import Path
from typing import Any, NamedTuple

import pytest

from devtools import render_overview
from devtools.measure_site_pages import CHIPS, COLUMNS
from devtools.preview_site import settle_math
from devtools.render_n11_lower_bounds_explainer_pdf import BROWSER_OVERRIDE
from tests import site_renders

#: The pages that hold a table of results.
PAGES = ("index.html", render_overview.RESULTS_PAGE)
#: The widths a table is laid out at as a table, and the one where its rows are cards.
TABLE_WIDTHS = (1280, 1024, 768)
PHONE = 390
WIDTHS = (*TABLE_WIDTHS, PHONE)
#: The credit column's floor, 11.5rem, in pixels (`site.css`).
CREDIT_MIN = 184
#: The id column: five characters and the cell's padding, well under KPress's 96.
ID_MAX = 64
#: The six columns of a table of results, as `overview_sections.result_head` names them.
COLUMNS_SHOWN = ["ID", "n", "Result", "Credit", "Rungs", "Date"]
#: A cell's padding either side, 0.5rem, in pixels.
PADDING = 16


class Laid(NamedTuple):
    """One page's table of results at one width."""

    table: dict[str, Any]
    """The table, as the `columns` probe reports it."""
    chips: list[dict[str, Any]]
    """Every chip the page shows, as the `chips` probe reports them."""
    records: int
    """How many of the table's records lines show."""


@pytest.fixture(scope="module")
def laid(tmp_path_factory: pytest.TempPathFactory) -> Iterator[dict[tuple[str, int], Laid]]:
    """Each page's table of results and chips as laid out at each width."""
    sync_api = pytest.importorskip("playwright.sync_api")
    site = Path(tmp_path_factory.mktemp("site"))
    with sync_api.sync_playwright() as driver:
        try:
            browser = driver.chromium.launch(executable_path=os.environ.get(BROWSER_OVERRIDE))
        except sync_api.Error as error:
            pytest.skip(f"no Chromium to launch: {error.message.splitlines()[0]}")
        found: dict[tuple[str, int], Laid] = {}
        for name in PAGES:
            path = site / name
            path.write_text(site_renders.html(name), encoding="utf-8")
            page = browser.new_page(viewport={"width": TABLE_WIDTHS[0], "height": 900})
            # The overview hides superseded rows as loaded; the columns and chips are
            # measured with them showing, which the filter's query preset asks for.
            page.goto(f"{path.as_uri()}?current=false", wait_until="load")
            settle_math(page)
            for width in WIDTHS:
                page.set_viewport_size({"width": width, "height": 900})
                page.wait_for_timeout(150)
                (table,) = (
                    table
                    for table in page.evaluate(COLUMNS)
                    if "site-results" in table["table"].split(".")
                )
                records = page.locator("table.site-results .site-records:visible").count()
                found[name, width] = Laid(table, page.evaluate(CHIPS), records)
            page.close()
        browser.close()
        yield found


def _column(table: dict[str, Any], name: str) -> dict[str, Any]:
    (column,) = (column for column in table["columns"] if column["column"] == name)
    return column


@pytest.mark.parametrize("name", PAGES)
def test_a_table_of_results_fits_its_track_at_1280(
    laid: dict[tuple[str, int], Laid], name: str
) -> None:
    """At a 1280-pixel window the table is as wide as its track and no wider, so nothing
    scrolls sideways: the columns' floors, and the formulas that hold the result column
    to 411 pixels, leave room to spare."""
    table = laid[name, 1280].table
    assert table["layout"] == "table"
    assert table["scrolls"] == 0, table["table_width"]
    assert table["table_width"] == table["frame_width"]
    assert table["shown_rows"] > 0


@pytest.mark.parametrize("width", TABLE_WIDTHS)
@pytest.mark.parametrize("name", PAGES)
def test_both_tables_lay_out_the_same_columns(
    laid: dict[tuple[str, int], Laid], name: str, width: int
) -> None:
    """Both tables are laid out with the six columns in one order. The id's is as narrow
    as an id, and the rungs' holds its widest chip with the cell's padding, so its three
    rung chips share a line and no kind or standing chip is cut or wrapped."""
    table, chips, _ = laid[name, width]
    assert [column["column"] for column in table["columns"]] == COLUMNS_SHOWN
    assert 0 < _column(table, "ID")["width"] <= ID_MAX
    in_table = [chip for chip in chips if chip["surface"] == "table"]
    under = [chip for chip in in_table if chip["chip"] in {"kind", "standing"}]
    widest = max(chip["inline_size"] for chip in under)
    assert _column(table, "Rungs")["width"] >= widest + PADDING - 0.5
    # Every row shows its kind: one kind chip to a row showing.
    kinds = [chip for chip in in_table if chip["chip"] == "kind"]
    assert len(kinds) == table["shown_rows"]


@pytest.mark.parametrize("width", WIDTHS)
def test_the_overview_carries_the_records_and_shows_none(
    laid: dict[tuple[str, int], Laid], width: int
) -> None:
    """A result's records are a line under its summary on the results page, at every
    width, and the overview's table, which is the same table, shows none of them."""
    assert laid["index.html", width].records == 0
    results = laid[render_overview.RESULTS_PAGE, width]
    assert results.records == results.table["shown_rows"] > 0


@pytest.mark.parametrize("width", TABLE_WIDTHS)
@pytest.mark.parametrize("name", PAGES)
def test_a_credit_wraps_between_names_and_never_inside_one(
    laid: dict[tuple[str, int], Laid], name: str, width: int
) -> None:
    """The credit column is at least its floor at every width, which holds the longest
    name on one line, so no word of a credit is split across lines: a credit reads two or
    three names to a line, where KPress's floor set it a word to a line."""
    credit = _column(laid[name, width].table, "Credit")
    assert credit["width"] >= CREDIT_MIN - 0.5
    assert credit["broken"] == []
    assert credit["lines"] >= 1


@pytest.mark.parametrize("name", PAGES)
def test_on_a_phone_each_row_is_a_card_that_fits(
    laid: dict[tuple[str, int], Laid], name: str
) -> None:
    """At 390 pixels each row is a card as wide as the page's column, the floors of the
    wide table do not apply, and no credit breaks inside a word."""
    table = laid[name, PHONE].table
    assert table["layout"] == "cards"
    assert table["scrolls"] == 0
    credit = next(c for c in table["columns"] if c["column"].startswith("site-col-credit"))
    assert credit["broken"] == []
    assert credit["lines"] >= 1


@pytest.mark.parametrize("width", WIDTHS)
@pytest.mark.parametrize("name", PAGES)
def test_no_chip_wraps(laid: dict[tuple[str, int], Laid], name: str, width: int) -> None:
    """Every chip a page shows, in a table, the rating ladders or the prose, is one line
    high at every width: the one chip rule keeps its words together, and what holds a
    chip is wide enough for it."""
    chips = laid[name, width].chips
    assert chips
    assert {chip["chip"] for chip in chips} >= {"rung", "kind", "standing"}
    wrapped = [(chip["surface"], chip["text"]) for chip in chips if chip["lines"] != 1]
    assert wrapped == []
    assert {chip["white_space"] for chip in chips} == {"nowrap"}


@pytest.mark.parametrize("width", WIDTHS)
@pytest.mark.parametrize("name", PAGES)
def test_every_kind_and_standing_chip_is_one_size(
    laid: dict[tuple[str, int], Laid], name: str, width: int
) -> None:
    """`lower bound`, `case exclusion`, `superseded`, `reported` and the rest are the one
    chip: one font size, one line height and one block size, the rung chips' own, and
    they differ only in their words. A result that still stands draws no standing chip
    at all."""
    chips = laid[name, width].chips
    standing = [chip for chip in chips if chip["chip"] == "standing"]
    kinds = [chip for chip in chips if chip["chip"] == "kind"]
    rungs = [chip for chip in chips if chip["chip"] == "rung"]
    assert {chip["text"] for chip in standing} >= {"superseded"}
    assert "current best" not in {chip["text"] for chip in standing}
    assert {chip["text"] for chip in kinds} >= {"lower bound", "optimality"}
    for measure in ("font_size", "line_height", "block_size"):
        sizes = {chip[measure] for chip in (*standing, *kinds)}
        assert len(sizes) == 1, (measure, sizes)
        assert sizes == {chip[measure] for chip in rungs}, measure
