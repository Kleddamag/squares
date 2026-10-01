"""The site preview's layout checks, on reports shaped as its probes return them.

`devtools.preview_site` fails a built page on what its probes find, and
`devtools.measure_site_pages cards` prints the same card report as a table, as `space`
does the space around tables and headings. All read a probe's output in Python, so the
decisions are tested here without a browser.
"""

from __future__ import annotations

from devtools.measure_site_pages import card_rows, markdown_table, space_rows
from devtools.preview_site import (
    SCROLLBAR_PX,
    clip_problem,
    off_centre,
    shot_stem,
    tabs_problems,
    type_problems,
)


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


def _header(*, rule: tuple[float, float] | None, tabs: tuple[float, float] | None) -> dict:
    """A `preview_site/header` report: the bar from 16 to 68.59, the rule and the tabs as
    given, each a top and a bottom, and the film 64px under whichever ends lower."""
    foot = max([68.59, *(part[1] for part in (rule, tabs) if part)])
    return {
        "nav": {"top": 16, "bottom": 68.59},
        "rule": rule and {"top": rule[0], "bottom": rule[1], "on": "nav.site-nav"},
        "tabs": tabs and {"top": tabs[0], "bottom": tabs[1], "current": "Film"},
        "first": {"top": foot + 64, "bottom": 900, "block": "figure.site-film-frame"},
    }


def test_section_tabs_under_the_bars_rule_pass_and_tabs_over_it_are_reported() -> None:
    """From the top a page of a section reads bar, rule, tabs, content. Tabs standing
    above the rule, as they did while the rule was the foot of the header that holds
    them, are named with how far; a page with no tabs has nothing to check."""
    assert tabs_problems(_header(rule=(67.59, 68.59), tabs=(79.78, 112.38))) == []
    assert tabs_problems(_header(rule=(67.59, 68.59), tabs=None)) == []
    over = _header(rule=(113.77, 114.77), tabs=(69.98, 102.58))
    over["rule"]["on"] = "header"
    assert tabs_problems(over) == [
        (
            "the section tabs start 44.79px above the foot of the rule under the "
            "navigation bar, which is on header"
        )
    ]
    assert tabs_problems(_header(rule=None, tabs=(79.78, 112.38))) == [
        "the section tabs have no rule over them, under the navigation bar"
    ]
    under = _header(rule=(67.59, 68.59), tabs=(79.78, 112.38))
    under["first"]["top"] = 100.38
    assert tabs_problems(under) == [
        "figure.site-film-frame starts 12px above the foot of the section tabs"
    ]


#: The paper's scale as a page resolves it: the prose base, the sans base beside it, and
#: the three steps under the sans base.
SCALE = {"prose": 18, "sans": 19, "support": 18.05, "note": 17.48, "colophon": 16.15}


def _type(link: float | None, tab: float | None, name: float | None = 19) -> dict:
    """A `preview_site/header` report's type: a link's size, a tab's and the name's."""
    return {"type": {"body": 18, "name": name, "link": link, "tab": tab, "scale": SCALE}}


def test_the_bars_type_is_one_step_under_the_bodys_and_no_more() -> None:
    """A link in the bar and a section tab are under the prose base and no smaller than
    the first step of the scale under it, whatever those are in pixels; the two are one
    size; and the site's name is at least the body's. The sizes the bar had, 16px links
    and 14.4px tabs under a 16px name, are each named."""
    assert type_problems(_type(17.48, 17.48)) == []
    assert type_problems(_type(17.48, None)) == []
    assert type_problems(_type(None, None, None)) == []
    unscaled = _type(17.48, None)
    unscaled["type"]["scale"] = None
    assert type_problems(unscaled) == []
    wide = "it should be under the body's 18px and no smaller than the step below it, 17.48px"
    assert type_problems(_type(16, 14.4, 16)) == [
        f"a link in the header is 16px: {wide}",
        f"a tab in the header is 14.4px: {wide}",
        "a section tab is 14.4px and a link in the bar 16px",
        "the site's name is 16px, under the body's 18px",
    ]
    # The support size is a step of the scale, but not one under the body.
    assert type_problems(_type(18.05, 18.05)) == [
        f"a link in the header is 18.05px: {wide}",
        f"a tab in the header is 18.05px: {wide}",
    ]
    # A body of another size moves the step with it.
    larger = _type(18.05, 18.05, 20)
    larger["type"]["scale"] = {**SCALE, "prose": 19}
    assert type_problems(larger) == []
