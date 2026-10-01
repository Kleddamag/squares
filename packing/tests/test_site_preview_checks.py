"""The site preview's layout checks, on reports shaped as its probes return them.

`devtools.preview_site` fails a built page on what its probes find, and
`devtools.measure_site_pages cards` prints the same card report as a table, as `space`
does the space around tables and headings and `columns` the columns of the data tables.
All read a probe's output in Python, so the decisions are tested here without a browser.
"""

from __future__ import annotations

from devtools.measure_site_pages import (
    card_rows,
    chip_rows,
    column_rows,
    markdown_table,
    space_rows,
)
from devtools.preview_site import SCROLLBAR_PX, clip_problem, off_centre, shot_stem


def _section(*rows: tuple[int, float, float]) -> dict[str, object]:
    return {
        "section": "Squares Project Documentation",
        "block_width": 1104,
        "rows": [
            {"cards": n, "sizes": [""] * n, "widths": [264] * n, "start": a, "end": b}
            for n, a, b in rows
        ],
        "headlines": [],
    }


def test_a_row_off_the_centre_of_its_line_is_reported() -> None:
    """A full line and a centred partial line pass; a partial line hanging to the start,
    as a grid's last row does, is named with its two slacks."""
    report = [_section((4, 0, 0), (2, 280, 280), (2, 0, 560))]
    assert off_centre(report) == [
        (
            "a row of 2 cards in Squares Project Documentation is off centre: 0px before it, "
            "560px after"
        )
    ]


def test_a_rounding_pixel_is_not_off_centre() -> None:
    assert off_centre([_section((3, 140, 140.9))]) == []


def test_the_card_table_has_one_line_a_row() -> None:
    report = [{"page": "index.html", "width": 1280, **_section((4, 0, 0), (2, 280, 280))}]
    rows = card_rows(report)
    assert [row["row"] for row in rows] == [1, 2]
    assert rows[1]["widths"] == "264 264"
    assert rows[1]["sizes"] == "- -"
    assert (rows[1]["start"], rows[1]["end"]) == (280, 280)


def _table(above: float, below: float, **over: object) -> dict[str, object]:
    return {
        "page": "index.html",
        "width": 1280,
        "state": "page",
        "kind": "table",
        "table": "table.site-table",
        "section": "Recent Results",
        "component": "div.site-table-wrap",
        "bar": True,
        "above": above,
        "above_to": "p",
        "below": below,
        "below_to": "p.site-more",
        **over,
    }


def _heading(role: str, above: float, below: float, **over: object) -> dict[str, object]:
    return {
        "page": "index.html",
        "width": 1280,
        "state": "page",
        "kind": "heading",
        "role": role,
        "text": "Recent Results",
        "size": 21.6,
        "line_height": 24.8,
        "leading": 1.15,
        "lines": 1,
        "overflow": 0,
        "clips": False,
        "above": above,
        "above_to": "p",
        "below": below,
        "below_to": "p",
        **over,
    }


def test_the_space_table_has_one_line_a_table_and_one_a_heading_role() -> None:
    """Tables come first, each on its own line; headings of one role on one page at one
    width share a line that gives the least and most space found, the most lines one
    takes, and what a clipping box cannot show."""
    report = [
        _heading("h2", 48.6, 27.2),
        _table(32, 32),
        _heading("h2", 48.6, 32, lines=2),
        _heading("span.site-card-value", 3.2, 3.2, overflow=4, clips=True, lines=3),
        _heading("span.site-card-value", 3.2, 3.2, overflow=9, clips=False),
    ]
    rows = space_rows(report)
    assert [row["what"] for row in rows] == [
        "div.site-table-wrap with bar",
        "h2",
        "span.site-card-value",
    ]
    table, section, headline = rows
    assert (table["above"], table["below"], table["where"]) == ("32", "32", "Recent Results")
    assert (section["count"], section["above"], section["below"]) == (2, "48.6", "27.2 to 32")
    assert (section["leading"], section["lines"], section["overflow"]) == ("1.15", 2, 0)
    # Only a box that hides its overflow counts as clipping what it cannot show.
    assert (headline["lines"], headline["overflow"]) == (3, 4)
    assert markdown_table(report).splitlines()[0].startswith("| page | width | state | what |")


def test_the_columns_table_has_one_line_a_column() -> None:
    """Each column of each table is a line: its width and share of the table, the most
    lines a cell takes, how many words a line break splits, and the tallest row it
    sets, a dash where it sets none. A column that is not shown has no width."""
    report: list[dict[str, object]] = [
        {
            "page": "all-results.html",
            "width": 1280,
            "table": "site-table.site-results",
            "section": "Every Result",
            "layout": "table",
            "table_width": 1104,
            "frame_width": 1104,
            "scrolls": 0,
            "shown_rows": 61,
            "top": 400,
            "height": 8423,
            "tallest_row": {"row": "t-056", "height": 385.6},
            "columns": [
                {"column": "Result", "width": 412.8, "lines": 3, "broken": [], "tallest": None},
                {
                    "column": "Credit",
                    "width": 102.6,
                    "lines": 9,
                    "broken": ["Queuingtheorydotcom", "Guzhou0806"],
                    "tallest": {"row": "t-048", "height": 238.8, "lines": 9},
                },
                {
                    "column": "site-records",
                    "width": None,
                    "lines": 3,
                    "broken": [],
                    "tallest": None,
                },
            ],
        }
    ]
    result, credit, cards = column_rows(report)
    assert (result["col_width"], result["share"], result["tallest_row"]) == (
        "412.8",
        "37%",
        "-",
    )
    assert (credit["col_width"], credit["share"], credit["max_lines"]) == ("102.6", "9%", 9)
    assert (credit["broken_words"], credit["tallest_row"]) == (2, "t-048")
    assert (credit["row_height"], credit["its_lines"]) == ("238.8", 9)
    assert (credit["table"], credit["past_frame"], credit["shown"]) == ("1104", "0", 61)
    assert (cards["col_width"], cards["share"]) == ("-", "-")
    head = markdown_table(report).splitlines()[0]
    assert head.startswith("| page | width | section | layout | shown | table | past_frame |")


def test_the_chips_table_has_one_line_a_kind_of_chip_on_a_surface() -> None:
    """Chips of one kind on one surface share a line that gives how many there are, the
    distinct sizes found, the most lines one takes, and the words of each that wraps."""

    def chip(kind: str, text: str, block: float, lines: int) -> dict[str, object]:
        return {
            "page": "all-results.html",
            "width": 1280,
            "state": "page",
            "chip": kind,
            "text": text,
            "surface": "table",
            "font_size": 17.5,
            "line_height": 25.3,
            "inline_size": 98,
            "block_size": block,
            "lines": lines,
            "white_space": "normal",
        }

    report = [
        chip("rung", "S5", 25.3, 1),
        chip("standing", "superseded", 25.3, 1),
        chip("standing", "current best", 50.7, 2),
        chip("standing", "current best", 50.7, 2),
    ]
    rungs, standing = chip_rows(report)
    # A chip's own width is its `inline_size`, so `width` stays the window's.
    assert (rungs["width"], standing["width"]) == (1280, 1280)
    assert (rungs["chip"], rungs["count"], rungs["block_size"], rungs["wrapped"]) == (
        "rung",
        1,
        "25.3",
        "-",
    )
    assert (standing["count"], standing["font_size"], standing["block_size"]) == (
        3,
        "17.5",
        "25.3 50.7",
    )
    assert (standing["max_lines"], standing["wrapped"]) == (2, "current best")
    head = markdown_table(report).splitlines()[0]
    assert head.startswith("| page | width | state | surface | chip | count | font_size |")


def test_a_heading_with_no_resolved_line_height_still_has_a_line() -> None:
    row = _heading("h1", 64, 20, line_height="normal", leading=None, lines=None)
    (only,) = space_rows([row])
    assert (only["line_height"], only["leading"], only["lines"]) == ("", "", 0)


def test_a_clipped_block_is_named_with_how_far_it_runs_past_each_side() -> None:
    """The preview reports a wide block an ancestor cuts off by naming both, each side
    it runs past, and whether it took a scrollbar's width to show it."""
    cut = {"block": "div.site-table-wrap", "frame": "article.kpress", "left": 7.5, "right": 7.5}
    assert clip_problem(cut, scrollbar=SCROLLBAR_PX) == (
        "div.site-table-wrap runs 7.5px past its left edge and 7.5px past its right edge of "
        "article.kpress, which clips it, with a 15px scrollbar"
    )
    count = {"block": "span.site-count", "frame": "article.kpress", "left": 0, "right": 16}
    assert clip_problem(count) == (
        "span.site-count runs 16px past its right edge of article.kpress, which clips it"
    )


def test_a_shot_is_named_for_its_page_and_fragment() -> None:
    assert shot_stem("index.html") == "index"
    assert shot_stem("workbench/index.html") == "workbench"
    assert shot_stem("cases.html#n-11") == "cases-n-11"
    assert shot_stem("n11-optimality/t-060-explainer.html") == "n11-optimality-t-060-explainer"
