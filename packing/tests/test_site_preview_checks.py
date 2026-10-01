"""The site preview's layout checks, on reports shaped as its probes return them.

`devtools.preview_site` fails a built page on what its probes find, and
`devtools.measure_site_pages cards` prints the same card report as a table, as `space`
does the space around tables and headings. All read a probe's output in Python, so the
decisions are tested here without a browser.
"""

from __future__ import annotations

from devtools.measure_site_pages import card_rows, markdown_table, space_rows
from devtools.preview_site import (
    LONG_TOKEN,
    SCROLLBAR_PX,
    clip_problem,
    off_centre,
    shot_stem,
    split_problem,
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


def _split(*pieces: str, **over: object) -> dict[str, object]:
    return {
        "word": "".join(pieces),
        "pieces": list(pieces),
        "host": "dd",
        "block": "dd",
        "code": False,
        "prose": False,
        "width": 40.0,
        "line": 320.0,
        "frame": "",
        **over,
    }


def test_a_word_cut_between_two_letters_is_reported() -> None:
    """What `overflow-wrap: anywhere` does to a label in a column squeezed narrower than
    the word: the break falls between two letters, and the report names the pieces, the
    element, and the word's width against the line it was set on."""
    squeezed = _split("low", "er", host="span.site-atlas-pop-which", block="p", line=24.0)
    assert split_problem(squeezed) == (
        '"low | er" is one word on 2 lines in span.site-atlas-pop-which in p: '
        "40px wide on a 24px line"
    )
    letters = _split("l", "o", "w", "e", "r", line=8.0)
    assert split_problem(letters) == (
        '"l | o | w | e | r" is one word on 5 lines in dd: 40px wide on a 8px line'
    )
    digits = _split("3.8770", "8359", width=70.0, line=48.0)
    assert split_problem(digits) is not None


def test_a_name_cut_at_its_hyphen_is_reported_where_the_site_sets_it() -> None:
    """An evidence identifier is one word: a line that ends on one of its hyphens, in a
    popover or a block the site builds, is reported, a framed page's named with its
    frame. The same break in a document's own prose is KPress's and passes."""
    name = _split("E-nagamochi-", "lower", host="code", code=True, width=144.8, line=518.0)
    assert split_problem(name) == (
        '"E-nagamochi- | lower" is one word on 2 lines in code in dd: '
        "144.8px wide on a 518px line"
    )
    framed = split_problem({**name, "block": "p", "frame": "iframe.site-popover-frame"})
    assert framed is not None
    assert "in code in p, framed in iframe.site-popover-frame: 144.8px wide" in framed
    assert split_problem({**name, "prose": True}) is None


def test_an_ordinary_break_is_not_a_split_word() -> None:
    """Running text ends a line on the hyphen of a compound, a path on its slash, and a
    formula written in characters at a bracket; none of them cuts a word."""
    assert split_problem(_split("computer-", "assisted")) is None
    assert split_problem(_split("docs/project/", "reviews", host="code", code=True)) is None
    assert split_problem(_split("T=", "(6u+4)/(1+2u-u^2),")) is None
    assert split_problem(_split("280af3d4\u2026", "e6e5", host="code", code=True)) is None


def test_a_long_token_wider_than_its_line_may_break() -> None:
    """An exact decimal or an identifier of `LONG_TOKEN` characters or more that cannot
    fit on one line has to break somewhere; one that would have fitted does not, and
    neither does anything shorter, however narrow its column."""
    decimal = "3.8770835900228141773078970601009"
    assert len(decimal) >= LONG_TOKEN
    cut = _split(decimal[:-1], decimal[-1], width=283.0, line=270.0)
    assert split_problem(cut) is None
    assert split_problem({**cut, "line": 300.0}) is not None
    name = _split("E-n011-global-optimality-", "independent", host="code", code=True)
    assert split_problem({**name, "width": 317.0, "line": 300.0}) is None
    assert split_problem({**name, "width": 317.0, "line": 518.0}) is not None
    short = _split("E-nagamochi-", "lower", host="code", code=True, width=155.0, line=120.0)
    assert len("E-nagamochi-lower") < LONG_TOKEN
    assert split_problem(short) is not None


def test_the_popover_table_has_one_line_a_popover_with_its_count_of_split_words() -> None:
    """`measure_site_pages popover` prints a popover's box, margins and visible share on
    one line; the broken words themselves are a list, which the JSON report keeps."""
    row = {
        "page": "frontier.html",
        "width": 1280,
        "press": 'a[data-case="79"]',
        "popover": "#pop-case",
        "window_height": 1200,
        "inline": 736,
        "block": 896,
        "above": 152,
        "below": 152,
        "beside": 272,
        "scrolls": "its frame",
        "shown": 710,
        "content": 3070,
        "share": 0.23,
        "split_words": 1,
        "split": ['"E-nagamochi- | lower" is one word on 2 lines in code in dd'],
    }
    head, _, line = markdown_table([row]).splitlines()
    assert head.endswith("| shown | content | share | split_words |")
    assert line.endswith("| its frame | 710 | 3070 | 0.23 | 1 |")
