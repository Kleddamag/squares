"""The site preview's layout checks, on reports shaped as its probes return them.

`devtools.preview_site` fails a built page on what its probes find, and
`devtools.measure_site_pages cards` prints the same card report as a table, as `space`
does the space around tables and headings. All read a probe's output in Python, so the
decisions are tested here without a browser.
"""

from __future__ import annotations

from devtools.measure_site_pages import card_rows, markdown_table, space_rows
from devtools.preview_site import off_centre, shot_stem


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


def test_a_heading_with_no_resolved_line_height_still_has_a_line() -> None:
    row = _heading("h1", 64, 20, line_height="normal", leading=None, lines=None)
    (only,) = space_rows([row])
    assert (only["line_height"], only["leading"], only["lines"]) == ("", "", 0)


def test_a_shot_is_named_for_its_page_and_fragment() -> None:
    assert shot_stem("index.html") == "index"
    assert shot_stem("workbench/index.html") == "workbench"
    assert shot_stem("cases.html#n-11") == "cases-n-11"
    assert shot_stem("n11-optimality/t-060-explainer.html") == "n11-optimality-t-060-explainer"
