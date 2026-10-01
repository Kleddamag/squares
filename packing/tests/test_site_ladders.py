"""The rating ladders hold their rows at every width, in a browser.

Verification at a Glance is one diagram of three ladders (`templates/paper-design.md`,
Rating ladders): every rung is the same height, and its description is a box of exactly
two lines that its words never run past. Whether a text takes two lines is the browser's
to say, from the face and the cell's width, so this opens the rendered overview in
Chromium and measures the diagram with the probe `devtools.measure_site_pages ladders`
reports from, at the widths the design is shot at and at the ones where a description is
narrowest: 716 pixels, the least window that sets three columns, and 715, where the
ladders stack; 768, where the page's margin widens and the wide track is 4 pixels more
than at 716; 1100, the least that sets a rung's description beside its rail in three
columns; and 360 and 320, a phone's. At each the diagram also stands inside whatever
clips the page sideways, with the wide track's gutter either side.

The page is rendered and loaded once, in a module fixture, and resized for each width.
Skipped where no Chromium can be launched; `SQPACK_CHROMIUM` names one the environment
supplies, as the other browser tools read it.
"""

from __future__ import annotations

import os
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest

from devtools import overview_sections
from devtools.measure_site_pages import LADDERS
from devtools.render_explainer_pdf import BROWSER_OVERRIDE
from tests import site_renders

#: Each width measured, and how many columns the rungs stand in there.
WIDTHS = {1280: 3, 1100: 3, 1024: 3, 768: 3, 716: 3, 715: 1, 390: 1, 360: 1, 320: 1}
#: The widths at which a cell has 20.5rem, so a rung's description stands beside its
#: chip and count; at the others it lies under them, across the cell.
BESIDE = frozenset({1280, 1100, 715, 390, 360})
#: `--site-ladders-meaning-min`, 13.5rem, in pixels: the narrowest a description is set.
MEANING_MIN = 216
#: `--site-wide-gutter`, 0.5rem, in pixels: the least room either side of a wide block.
GUTTER = 8


@pytest.fixture(scope="module")
def diagrams(tmp_path_factory: pytest.TempPathFactory) -> Iterator[dict[int, dict[str, Any]]]:
    """The overview's one ladder diagram as laid out at each of `WIDTHS`."""
    sync_api = pytest.importorskip("playwright.sync_api")
    path = Path(tmp_path_factory.mktemp("site")) / "index.html"
    path.write_text(site_renders.html("index.html"), encoding="utf-8")
    with sync_api.sync_playwright() as driver:
        try:
            browser = driver.chromium.launch(executable_path=os.environ.get(BROWSER_OVERRIDE))
        except sync_api.Error as error:
            pytest.skip(f"no Chromium to launch: {error.message.splitlines()[0]}")
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.goto(path.as_uri(), wait_until="load")
        page.wait_for_timeout(300)
        found: dict[int, dict[str, Any]] = {}
        for width in WIDTHS:
            page.set_viewport_size({"width": width, "height": 900})
            page.wait_for_timeout(100)
            (found[width],) = page.evaluate(LADDERS)
        browser.close()
        yield found


@pytest.mark.parametrize("width", WIDTHS)
def test_every_rung_is_one_height_and_its_description_two_lines(
    diagrams: dict[int, dict[str, Any]], width: int
) -> None:
    """At every width each rung's cell is the same height, its description's box is two
    lines tall and at least the least width, and no description takes a third line or
    runs past its box, so nothing has to be clipped."""
    diagram = diagrams[width]
    rungs = diagram["rungs"]
    assert len(rungs) == len(overview_sections.rung_meanings())
    assert diagram["columns"] == WIDTHS[width]
    assert len(diagram["heights"]) == 1, diagram["heights"]
    assert {rung["beside"] for rung in rungs} == {width in BESIDE}
    assert len({rung["meaning_width"] for rung in rungs}) == 1
    for rung in rungs:
        assert rung["meaning"] == overview_sections.rung_short_meanings()[rung["rung"]]
        assert rung["title"] == overview_sections.rung_meanings()[rung["rung"]]
        assert rung["meaning_height"] == pytest.approx(2 * rung["line_height"], abs=0.2), rung
        assert rung["meaning_width"] >= MEANING_MIN - 0.5, rung
        assert 1 <= rung["lines"] <= 2, rung
        assert rung["overflow"] == 0, rung


@pytest.mark.parametrize("width", WIDTHS)
def test_the_rungs_line_up_across_three_columns_and_stack_by_ladder_on_a_phone(
    diagrams: dict[int, dict[str, Any]], width: int
) -> None:
    """In three columns the rungs of one level share a row, significance first and the
    highest level at the top, and the level significance lacks leaves an empty cell as
    tall as its row. On a phone each ladder is a block of its own in the same order, and
    the missing rung takes no room."""
    diagram = diagrams[width]
    rungs = diagram["rungs"]
    assert diagram["heads"] == [name for _, name, _, _ in overview_sections.DIMENSIONS]
    order = [scale for scale, *_ in overview_sections.DIMENSIONS]
    by_place = sorted(rungs, key=lambda rung: (rung["top"], rung["column"]))
    if WIDTHS[width] == 3:
        assert all(rung["column"] == order.index(rung["ladder"]) + 1 for rung in rungs)
        tops = {int(rung["rung"][1]): set[int]() for rung in rungs}
        for rung in rungs:
            tops[int(rung["rung"][1])].add(rung["top"])
        assert all(len(found) == 1 for found in tops.values()), tops
        assert sorted(tops, key=lambda level: min(tops[level])) == [5, 4, 3, 2, 1, 0]
        assert diagram["empty"] == diagram["heights"]
    else:
        ladders = [rung["rung"] for rung in by_place]
        assert ladders == [
            f"{scale}{level}"
            for scale in order
            for level in range(5, -1, -1)
            if f"{scale}{level}" in overview_sections.rung_meanings()
        ]
        assert all(height <= 1 for height in diagram["empty"])


@pytest.mark.parametrize("width", WIDTHS)
def test_the_diagram_stands_inside_what_clips_the_page_with_a_gutter_either_side(
    diagrams: dict[int, dict[str, Any]], width: int
) -> None:
    """At every width the diagram is centred, and it stops at least the wide track's
    gutter short of the nearest ancestor that clips sideways, or of the page's edge where
    none does, so no rule and no letter of it is cut or set flush to the edge."""
    diagram = diagrams[width]
    assert diagram["gutter_left"] >= GUTTER - 0.5, diagram["frame"]
    assert diagram["gutter_right"] >= GUTTER - 0.5, diagram["frame"]
    assert diagram["gutter_left"] == pytest.approx(diagram["gutter_right"], abs=0.5)
