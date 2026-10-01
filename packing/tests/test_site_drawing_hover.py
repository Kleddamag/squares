"""A packing drawing inside a link keeps its ink when the link is hovered, in a browser.

The atlas grid's cells and the homepage's picture are links that hold a drawing stroked
in `currentColor`. KPress turns a hovered link's text to its lighter accent, and a cell
took that colour with it: its black outlines went teal against the green squares and all
but vanished, in both themes (think-8eb4). A cell's hover is the wash behind the drawing
and nothing else (`templates/paper-design.md`, Atlas grid), so the drawing names its own
ink.

Which rule wins a cascade, and what a stroke over a wash comes out as, are the browser's
to say. So this opens the rendered overview in Chromium, in the light theme and the dark,
and reads one cell at rest, under the pointer, on keyboard focus and while pressed: the
stroke the browser computes for the drawing, and the pixels a screenshot has on the
frame's edge and in the cell's own padding. The screenshot is taken at two device pixels
to one, where the frame's stroke is over two pixels wide and so covers one whole.

Skipped where no Chromium can be launched; `SQPACK_CHROMIUM` names one the environment
supplies, as the other browser tools read it.
"""

from __future__ import annotations

import io
import os
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pytest
from PIL import Image

from devtools.render_explainer_pdf import BROWSER_OVERRIDE
from sqpack.probes import probe
from tests import site_renders

PROBES = Path(__file__).resolve().parent / "probes"
DRAWING = probe(PROBES, "site_drawing_hover/drawing")

#: The case whose cell is read, and the cell before it, which keyboard focus leaves.
CASE = 11
CELL = f'.site-atlas-cell[data-atlas-n="{CASE}"]'
BEFORE = f'.site-atlas-cell[data-atlas-n="{CASE - 1}"]'
HERO = ".site-hero-figure a"
SCHEMES = ("light", "dark")
#: The states a cell is washed in, and the pseudo-classes each must be in.
WASHED = {
    "hover": {"hover": True, "focus_visible": False, "active": False},
    "focus": {"hover": False, "focus_visible": True, "active": False},
    "pressed": {"hover": True, "active": True},
}
#: Longer than `--site-hover-duration` (150ms at most), so a wash has finished.
SETTLE_MS = 400
#: A point of the page no drawing is under: the window's corner, in the bar's margin.
AWAY = (1, 1)
#: How far apart, summed over the three channels, a line and what it is drawn on must be
#: for the line to read. The page's ink is 594 or more from its ground in either theme,
#: washed or not; the teal a hovered link's text takes was 481 from the light wash and
#: 377 from the dark one.
READABLE = 540

type Pixel = tuple[int, int, int]
#: Every reading of the overview's drawings, by theme and then by state.
type Readings = dict[str, dict[str, Painted]]


@dataclass(frozen=True)
class Painted:
    """One reading of a drawing and its holder: what the probe reports, the pixel on the
    frame's left edge farthest in colour from the ground, and the ground, which is the
    pixel just inside the holder's top left corner (a cell's padding)."""

    state: dict[str, Any]
    ink: Pixel
    ground: Pixel


def _apart(one: Pixel, other: Pixel) -> int:
    return sum(abs(a - b) for a, b in zip(one, other, strict=True))


def _read(page: Any, holder: str) -> Painted:
    page.wait_for_timeout(SETTLE_MS)
    state = page.evaluate(DRAWING, {"holder": holder})
    assert state is not None, holder
    box, edge = state["box"], state["edge"]
    shot = Image.open(io.BytesIO(page.screenshot(clip=box))).convert("RGB")
    scale = shot.width / box["width"]

    def pixel(x: float, y: float) -> Pixel:
        found = shot.getpixel((round((x - box["x"]) * scale), round((y - box["y"]) * scale)))
        assert isinstance(found, tuple)
        red, green, blue = found
        return int(red), int(green), int(blue)

    ground = pixel(box["x"] + 2, box["y"] + 2)
    across = [pixel(edge["x"] + step / scale, edge["y"]) for step in range(-6, 7)]
    return Painted(state, max(across, key=lambda found: _apart(found, ground)), ground)


def _readings(page: Any) -> dict[str, Painted]:
    """The cell at rest and in each washed state, then the hero's link at rest and under
    the pointer. The press is last and is never released, so nothing is followed."""
    page.locator("[data-atlas-grid]").scroll_into_view_if_needed()
    cell = page.locator(CELL)
    cell.wait_for()
    cell.scroll_into_view_if_needed()
    page.mouse.move(*AWAY)
    found = {"rest": _read(page, CELL)}
    cell.hover()
    found["hover"] = _read(page, CELL)
    page.mouse.move(*AWAY)
    page.locator(BEFORE).focus()
    page.keyboard.press("Tab")
    found["focus"] = _read(page, CELL)
    hero = page.locator(HERO)
    hero.scroll_into_view_if_needed()
    page.mouse.move(*AWAY)
    found["hero rest"] = _read(page, HERO)
    hero.hover()
    found["hero hover"] = _read(page, HERO)
    cell.scroll_into_view_if_needed()
    cell.hover()
    page.mouse.down()
    found["pressed"] = _read(page, CELL)
    return found


@pytest.fixture(scope="module")
def painted(tmp_path_factory: pytest.TempPathFactory) -> Iterator[Readings]:
    """Every reading of the overview's drawings, by theme and then by state."""
    sync_api = pytest.importorskip("playwright.sync_api")
    path = Path(tmp_path_factory.mktemp("site")) / "index.html"
    path.write_text(site_renders.html("index.html"), encoding="utf-8")
    with sync_api.sync_playwright() as driver:
        try:
            browser = driver.chromium.launch(executable_path=os.environ.get(BROWSER_OVERRIDE))
        except sync_api.Error as error:
            pytest.skip(f"no Chromium to launch: {error.message.splitlines()[0]}")
        found: Readings = {}
        for scheme in SCHEMES:
            page = browser.new_page(
                viewport={"width": 1280, "height": 900},
                device_scale_factor=2,
                color_scheme=scheme,
            )
            page.goto(path.as_uri(), wait_until="load")
            assert page.locator("html").get_attribute("data-kpress-resolved-theme") == scheme
            found[scheme] = _readings(page)
            page.close()
        browser.close()
        yield found


@pytest.mark.parametrize("scheme", SCHEMES)
def test_a_cell_at_rest_is_drawn_in_the_pages_ink_on_bare_paper(
    painted: Readings, scheme: str
) -> None:
    """At rest the cell has no background, its frame and its squares' outlines are
    stroked in the page's text colour, and the frame's edge reads against the paper."""
    rest = painted[scheme]["rest"]
    assert rest.state["background"] == "rgba(0, 0, 0, 0)"
    assert not any(rest.state[name] for name in ("hover", "focus_visible", "active"))
    assert rest.state["frame_stroke"] == rest.state["outline_stroke"] == rest.state["color"]
    assert _apart(rest.ink, rest.ground) > READABLE, rest


@pytest.mark.parametrize("state", WASHED)
@pytest.mark.parametrize("scheme", SCHEMES)
def test_a_washed_cell_changes_its_background_and_keeps_every_line(
    painted: Readings, scheme: str, state: str
) -> None:
    """Under the pointer, on keyboard focus and while pressed, the cell's background is
    the wash and the drawing is stroked exactly as at rest: the same computed stroke on
    the frame and on the outlines, and the same pixel on the frame's edge."""
    rest, washed = painted[scheme]["rest"], painted[scheme][state]
    assert {name: washed.state[name] for name in WASHED[state]} == WASHED[state]
    assert washed.state["background"] != rest.state["background"]
    assert washed.ground != rest.ground
    assert washed.state["frame_stroke"] == rest.state["frame_stroke"]
    assert washed.state["outline_stroke"] == rest.state["outline_stroke"]
    assert washed.ink == rest.ink, (washed.ink, rest.ink)
    assert _apart(washed.ink, washed.ground) > READABLE, washed


@pytest.mark.parametrize("scheme", SCHEMES)
def test_the_homepage_picture_keeps_its_ink_under_the_pointer(
    painted: Readings, scheme: str
) -> None:
    """The hero is the same drawing in a link, with no wash: hovered, its strokes and the
    pixel on its frame's edge are what they are at rest."""
    rest, over = painted[scheme]["hero rest"], painted[scheme]["hero hover"]
    assert over.state["hover"]
    assert not rest.state["hover"]
    assert over.state["frame_stroke"] == rest.state["frame_stroke"] == rest.state["color"]
    assert over.state["outline_stroke"] == rest.state["outline_stroke"]
    assert over.ink == rest.ink, (over.ink, rest.ink)
