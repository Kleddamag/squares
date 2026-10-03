"""The two tables of results share their width sensibly, and no chip wraps, in a browser.

Recent Results on the overview and the table of the results page are one table
(`templates/paper-design.md`, Tables). How its columns share a window is the browser's to
say, from the faces, the typeset formulas and the floors `site.css` gives the columns, so
this opens both rendered pages in Chromium and measures each table with the probes
`devtools.measure_site_pages columns` and `chips` report from: at 1280 pixels, where the
table bleeds to 1200 pixels and fits; at 1024 and 768, where its eight columns' floors
outrun the window and it scrolls sideways in its wrap; and at 390, where each row is a
card.

What it holds: the table fits its track at 1280, and scrolls no further than its floors
ask at 1024 and 768; the id column is as narrow as an id; a long list of cases wraps
between its floor and its measure, no value of it cut, and sets no row taller than the
tallest stack of details; the result column gives way to its floor, which its widest
formula fits, and a formula ends a line only after a relation or a binary operator; the
credit column keeps room for its longest name, so no credit breaks inside a word; the
rungs column holds its widest kind chip and the status column its widest status chip;
both tables show each result's records, a link to a line in the Details column; and
every chip on either page is one line high, every kind and standing chip one size.

Each page is rendered and loaded once, in a module fixture, with every row showing, its
math typeset, and then resized for each width; the overview is then loaded as it opens,
for the one check that needs its own filters. The checks that need no browser, of the
list a cell holds and of the formulas' TeX, read the same render. The browser is launched
as `tests.site_browser` launches it: the pinned Chromium, or the one `SQPACK_CHROMIUM`
names, with its text unhinted so that the pixels pinned here read the same on Linux as on
macOS, where they were measured; skipped where none can be launched, unless the run
requires one.
"""

from __future__ import annotations

import html
import re
from collections.abc import Iterator
from pathlib import Path
from typing import Any, NamedTuple

import pytest

from devtools import overview_data, overview_sections, render_overview
from devtools.measure_site_pages import CHIPS, COLUMNS
from devtools.preview_site import settle_math
from tests import site_browser, site_renders

#: The pages that hold a table of results.
PAGES = ("index.html", render_overview.RESULTS_PAGE)
#: The widths a table is laid out at as a table, and the one where its rows are cards.
TABLE_WIDTHS = (1280, 1024, 768)
PHONE = 390
WIDTHS = (*TABLE_WIDTHS, PHONE)
#: Each page's address with every row of its table showing: the overview opens on what
#: is recent, significant and current, and its filters' query presets clear all three.
EVERY_ROW = {"index.html": "?s-min=&age=&current=false", render_overview.RESULTS_PAGE: ""}
#: The overview as it opens, under its own filters.
AS_OPENED = "index.html as it opens"
#: A view where no long list of cases shows: the results of one kind that each hold a
#: case or two. (The overview as it opens held only such rows until T-064, a family of
#: thirteen cases at S4, joined it.)
SHORT_LISTS = "index.html, one kind of short lists"
SHORT_LISTS_QUERY = "?s-min=&age=&current=false&kind=rigidity"
#: The credit column's floor, 11.5rem, in pixels (`site.css`).
CREDIT_MIN = 184
#: The result column's floor, 18rem, in pixels (`site.css`), and what four formulas no
#: line could end inside held the column to before a long quotient could end one.
RESULT_MIN = 288
RESULT_WAS = 411
#: The width a table of results bleeds to at 1280 pixels, from 74rem (`site.css`): the
#: frontier table's width there.
TABLE_AT_1280 = 1200
#: A long list of cases: the measure it wraps in, `--site-cases-measure`, 24 digits of
#: the table's face, with the cell's padding, in pixels; the least the column narrows
#: to, half the measure; and the most lines the longest list, T-056's 23 values, takes
#: at 1280 pixels with every row showing, where the eight columns leave the list 181 of
#: its 225 (six lines in the full measure, before the status and details columns).
CASES_MEASURE = 224.8
CASES_MIN = 120.4
CASES_LINES = 8
#: The result with the longest list of cases, and the four whose quotients are long.
MOST_CASES = "T-056"
LONG_QUOTIENTS = ("T-022", "T-024", "T-026", "T-033")
#: How far a table of results may run past its frame, with every row showing: at its
#: floors it is 1139 pixels, 195 more than the 944-pixel frame at 1024 and 451 more
#: than the 688-pixel one at 768 (measured with eight columns, 2026-10-02).
SCROLL_MAX = {1024: 205, 768: 460}
#: The id column: five characters and the cell's padding, well under KPress's 96.
ID_MAX = 64
#: The eight columns of a table of results, as `overview_sections.result_head` names them.
COLUMNS_SHOWN = ["Date", "Result", "n", "Credit", "Rungs", "Status", "Details", "ID"]
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
    sync_api = site_browser.api()
    site = Path(tmp_path_factory.mktemp("site"))
    with sync_api.sync_playwright() as driver:
        browser = site_browser.launch(driver)
        found: dict[tuple[str, int], Laid] = {}
        for name in PAGES:
            path = site / name
            path.write_text(site_renders.html(name), encoding="utf-8")
            page = browser.new_page(viewport={"width": TABLE_WIDTHS[0], "height": 900})
            # The overview opens on its recent, significant, current rows; the columns
            # and chips are measured with every row showing, which the filters' query
            # presets ask for.
            page.goto(f"{path.as_uri()}{EVERY_ROW[name]}", wait_until="load")
            settle_math(page)
            for width in WIDTHS:
                page.set_viewport_size({"width": width, "height": 900})
                page.wait_for_timeout(150)
                found[name, width] = _laid(page)
            if name == "index.html":
                page.set_viewport_size({"width": TABLE_WIDTHS[0], "height": 900})
                page.goto(path.as_uri(), wait_until="load")
                settle_math(page)
                found[AS_OPENED, TABLE_WIDTHS[0]] = _laid(page)
                page.goto(f"{path.as_uri()}{SHORT_LISTS_QUERY}", wait_until="load")
                settle_math(page)
                found[SHORT_LISTS, TABLE_WIDTHS[0]] = _laid(page)
            page.close()
        browser.close()
        yield found


def _laid(page: Any) -> Laid:
    """The page's table of results, its chips and its records, as it is laid out now."""
    (table,) = (
        table for table in page.evaluate(COLUMNS) if "site-results" in table["table"].split(".")
    )
    records = page.locator("table.site-results .site-records:visible").count()
    return Laid(table, page.evaluate(CHIPS), records)


def _column(table: dict[str, Any], name: str) -> dict[str, Any]:
    """A column of a table: by its header's words where it is laid out as a table, and
    by its cells' class where its rows are cards."""
    (column,) = (
        column
        for column in table["columns"]
        if name in (column["column"], column["column"].split()[-1])
    )
    return column


@pytest.mark.parametrize("name", PAGES)
def test_a_table_of_results_fits_its_track_at_1280(
    laid: dict[tuple[str, int], Laid], name: str
) -> None:
    """At a 1280-pixel window the table bleeds to 1200 pixels, as wide as its track and
    no wider, so nothing scrolls sideways, with every row showing: its eight columns'
    floors, 1139 pixels, leave room to spare, which the long list of cases takes."""
    table = laid[name, 1280].table
    assert table["layout"] == "table"
    assert table["scrolls"] == 0, table["table_width"]
    assert table["table_width"] == table["frame_width"] == TABLE_AT_1280
    assert table["shown_rows"] == len(site_renders.overview().results)


@pytest.mark.parametrize("name", PAGES)
def test_a_table_of_results_scrolls_at_1024_and_768_no_further_than_its_floors(
    laid: dict[tuple[str, int], Laid], name: str
) -> None:
    """Below 1220 pixels the eight columns' floors outrun the frame, so the table scrolls
    sideways in its wrap, every column at its floor and no further: by 195 pixels at
    1024 and 451 at 768. It fitted at 1024 with six columns, before the status and the
    details had columns of their own (2026-10-02, `think-ybt5`, `think-e4o3`)."""
    for width, most in SCROLL_MAX.items():
        table = laid[name, width].table
        assert table["layout"] == "table", width
        assert 0 < table["scrolls"] <= most, (width, table["table_width"])
        assert _column(table, "Result")["width"] == pytest.approx(RESULT_MIN, abs=0.5)
        assert _column(table, "n")["width"] == pytest.approx(CASES_MIN, abs=1)


@pytest.mark.parametrize("name", PAGES)
def test_a_long_list_of_cases_wraps_in_its_measure(
    laid: dict[tuple[str, int], Laid], name: str
) -> None:
    """With every row showing at 1280 pixels the n column takes what the other seven
    columns' floors leave it, between its floor and its measure, and the longest list,
    T-056's 23 values, takes eight lines in it, where a column as narrow as one value
    set them on fifteen. So the tallest row the list sets is those eight lines, no
    taller than the tallest stack of a result's details, and at no width is a value cut
    across two lines: a range keeps to one."""
    cases = _column(laid[name, 1280].table, "n")
    assert CASES_MIN < cases["width"] < CASES_MEASURE
    assert cases["lines"] == CASES_LINES
    longest = cases["tallest"]
    details = _column(laid[name, 1280].table, "Details")["tallest"]
    assert (longest["row"], longest["lines"]) == (MOST_CASES.lower(), CASES_LINES)
    assert longest["height"] <= details["height"]
    for width in TABLE_WIDTHS:
        column = _column(laid[name, width].table, "n")
        assert CASES_MIN - 0.5 <= column["width"] <= CASES_MEASURE + 1, width
        assert (column["split"], column["broken"]) == ([], []), width


def test_the_n_column_is_as_narrow_as_its_lists_where_none_is_long(
    laid: dict[tuple[str, int], Laid],
) -> None:
    """Where every row shown holds a case or two, the n column is as narrow as what it
    holds, each cell one line, under KPress's 6rem: the measure is a long list's alone,
    so a single case has no empty column beside it."""
    table = laid[SHORT_LISTS, 1280].table
    cases = _column(table, "n")
    assert 0 < table["shown_rows"] < len(site_renders.overview().results)
    assert cases["lines"] == 1
    assert cases["width"] < 96
    assert table["scrolls"] == 0


@pytest.mark.parametrize("name", PAGES)
def test_on_a_phone_a_long_list_of_cases_takes_a_line_of_its_own(
    laid: dict[tuple[str, int], Laid], name: str
) -> None:
    """On a phone the longest list runs the card's width under the id and the rungs, in
    four lines where it had eight between them, and no value of it is cut."""
    cases = _column(laid[name, PHONE].table, "site-col-n")
    assert 1 < cases["lines"] <= 4
    assert cases["split"] == []


@pytest.mark.parametrize("name", PAGES)
def test_the_result_column_gives_way_to_its_floor(
    laid: dict[tuple[str, int], Laid], name: str
) -> None:
    """The result column narrows to its 18rem floor where the window is short of room,
    well under the 411 pixels it was held to, as it is with every row showing at every
    width now the table has eight columns; with the overview's own filters it has room
    to spare at 1280. Its widest piece of typeset math, the numerator of T-033's
    quotient, fits that floor with the cell's padding: so nothing the column holds is
    wider than it at any width."""
    for width in TABLE_WIDTHS:
        result = _column(laid[name, width].table, "Result")
        assert result["width"] == pytest.approx(RESULT_MIN, abs=0.5), width
    opened = _column(laid[AS_OPENED, 1280].table, "Result")
    assert RESULT_MIN < opened["width"] < RESULT_WAS
    wide = _column(laid[name, 1280].table, "Result")
    assert wide["piece"]["row"] == "t-033"
    assert wide["piece"]["width"] + PADDING <= RESULT_MIN
    phone = _column(laid[name, PHONE].table, "site-col-result")
    assert phone["piece"]["width"] <= laid[name, PHONE].table["table_width"] - PADDING


@pytest.mark.parametrize("width", WIDTHS)
@pytest.mark.parametrize("name", PAGES)
def test_a_formula_ends_a_line_only_where_it_may(
    laid: dict[tuple[str, int], Laid], name: str, width: int
) -> None:
    """A formula in a result's summary ends a line only after a relation or a binary
    operator at its top level, and the words after it follow on: no line of a summary
    begins with the comma after its formula, and no word of one is cut. Below 1280
    pixels some formulas do wrap, so this is measured and not vacuous."""
    result = _column(laid[name, width].table, "Result" if width != PHONE else "site-col-result")
    assert (result["cuts"], result["stranded"], result["broken"]) == ([], [], [])
    if width < 1280:
        assert result["wrapped"] > 0


def test_a_cell_of_cases_holds_each_value_in_a_box_and_reads_as_the_register_does() -> None:
    """A result's n cell holds each count or range in a box of its own, the comma with
    it, and reads as the register's scope does, ranges and all. The column sorts on the
    first case and the Case filter reads the row's own list, as before."""
    overview = site_renders.overview()
    boxes = re.compile(r'<span class="site-n-value">([^<]*)</span>')
    for result in overview.results:
        cell = overview_sections.case_list(result)
        assert html.unescape(re.sub(r"<[^>]+>", "", cell)) == result.scope
        values = boxes.findall(cell)
        assert " ".join(values) == html.escape(result.scope, quote=False)
        assert all(" " not in value for value in values)
    most = max(overview.results, key=lambda result: len(result.scope.split(", ")))
    assert (most.id, len(most.scope.split(", "))) == (MOST_CASES, 23)
    row, _ = overview_sections.result_table_row(most, overview, here=True, shown=True)
    assert f'<td class="num site-col-n site-n-wraps" data-value="{most.first_n}">' in row
    # A list wraps from five values, and a shorter one too where it is longer than half
    # the measure: four values with two ranges among them would hold the column wider
    # than the floor it narrows to (T-075 on 3 October 2026).
    for result in overview.results:
        values = result.scope.split(", ")
        wraps = len(values) >= 5 or len(result.scope) > overview_sections.CASES_ONE_LINE
        assert ("site-n-wraps" in overview_sections.case_cell_class(result)) is wraps
    assert any(
        len(result.scope.split(", ")) < 5
        and "site-n-wraps" in overview_sections.case_cell_class(result)
        for result in overview.results
    )
    assert f'data-n="{overview_sections.result_cases(most)}"' in row
    assert overview_data.EN_DASH in most.scope
    assert overview_data.EN_DASH not in overview_sections.result_cases(most)


def test_a_long_quotient_may_end_a_line_after_its_solidus() -> None:
    """A quotient of more than 24 digits sets its solidus as a binary operator, after
    which a line may end; a shorter one, a decimal and a quotient inside a group are left
    alone. Four results' summaries hold such a quotient, and each is set so in both
    tables of results, with no TeX left in the MathML a screen reader is given."""
    breakable = overview_data.breakable_quotients
    long = r"s(11) \ge 955000\sqrt{2073600042893309449}/359341754646249 = 3.8269975\ldots"
    assert breakable(long) == long.replace("/", r"\mathbin{/}")
    for kept in (
        r"s(11) > 3875000000/999999999 = 3.875000003875\ldots",
        r"\sqrt{955000000000000000000/359341754646249}",
        r"x = 1.955000207360004289330944/9",
    ):
        assert breakable(kept) == kept
    overview = site_renders.overview()
    for result in overview.results:
        cell = overview_sections.result_text(result)
        assert (r"\mathbin{/}" in cell) is (result.id in LONG_QUOTIENTS), result.id
        spoken = re.findall(r'<span class="kpress-math-semantic">(.*?)</span>', cell)
        assert not any("\\" in semantic for semantic in spoken), result.id
        if result.id in LONG_QUOTIENTS:
            assert "<mo>&#x0002F;</mo>" in spoken[0]


@pytest.mark.parametrize("width", TABLE_WIDTHS)
@pytest.mark.parametrize("name", PAGES)
def test_both_tables_lay_out_the_same_columns(
    laid: dict[tuple[str, int], Laid], name: str, width: int
) -> None:
    """Both tables are laid out with the eight columns in one order. The id's is as
    narrow as an id; the rungs' holds its widest chip with the cell's padding, so its
    three rung chips share a line and no kind chip is cut or wrapped; and the status
    column, the status line's own since 2026-10-02, holds its widest chip the same way."""
    table, chips, _ = laid[name, width]
    assert [column["column"] for column in table["columns"]] == COLUMNS_SHOWN
    assert 0 < _column(table, "ID")["width"] <= ID_MAX
    in_table = [chip for chip in chips if chip["surface"] == "table"]
    for column, held in (("Rungs", {"rung", "kind"}), ("Status", {"standing"})):
        widest = max(chip["inline_size"] for chip in in_table if chip["chip"] in held)
        assert _column(table, column)["width"] >= widest + PADDING - 0.5, column
    # Every row shows its kind: one kind chip to a row showing.
    kinds = [chip for chip in in_table if chip["chip"] == "kind"]
    assert len(kinds) == table["shown_rows"]


@pytest.mark.parametrize("width", WIDTHS)
def test_both_tables_show_each_results_records(
    laid: dict[tuple[str, int], Laid], width: int
) -> None:
    """A result's records are a line under its summary at every width, on the results
    page and on the overview alike, which is the same table under other filters: one
    line of records to each row showing. So with every row showing the two tables are
    laid out the same, column for column and row for row."""
    recent = laid["index.html", width]
    results = laid[render_overview.RESULTS_PAGE, width]
    assert recent.records == recent.table["shown_rows"] > 0
    assert results.records == results.table["shown_rows"] > 0
    assert recent.table["columns"] == results.table["columns"]
    assert recent.table["tallest_row"] == results.table["tallest_row"]
    if width == TABLE_WIDTHS[0]:
        opened = laid[AS_OPENED, width]
        assert opened.records == opened.table["shown_rows"] > 0


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
    """`lower bound`, `case exclusion`, `confirmed`, `recorded`, `superseded` and the
    rest are the one chip: one font size, one line height and one block size, the rung
    chips' own, and they differ only in their words. Every row draws its kind and its
    status, and a result that is the current best draws no chip for that."""
    chips = laid[name, width].chips
    standing = [chip for chip in chips if chip["chip"] == "standing"]
    kinds = [chip for chip in chips if chip["chip"] == "kind"]
    rungs = [chip for chip in chips if chip["chip"] == "rung"]
    assert {chip["text"] for chip in standing} >= {"confirmed", "superseded"}
    gone = {"current best", "reported", "not a bound", "second certificate"}
    assert not gone & {chip["text"] for chip in standing}
    assert {chip["text"] for chip in kinds} >= {"lower bound", "optimality"}
    for measure in ("font_size", "line_height", "block_size"):
        sizes = {chip[measure] for chip in (*standing, *kinds)}
        assert len(sizes) == 1, (measure, sizes)
        assert sizes == {chip[measure] for chip in rungs}, measure
