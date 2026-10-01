"""The site preview's layout checks, on reports shaped as its probes return them.

`devtools.preview_site` fails a built page on what its probes find, and
`devtools.measure_site_pages cards` prints the same card report as a table. Both read
the probe's output in Python, so the decisions are tested here without a browser.
"""

from __future__ import annotations

from devtools.measure_site_pages import card_rows
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


def test_a_shot_is_named_for_its_page_and_fragment() -> None:
    assert shot_stem("index.html") == "index"
    assert shot_stem("workbench/index.html") == "workbench"
    assert shot_stem("cases.html#n-11") == "cases-n-11"
    assert shot_stem("n11-optimality/t-060-explainer.html") == "n11-optimality-t-060-explainer"
