#!/usr/bin/env python3
"""Build the whole published site into one directory, serve it, and screenshot it.

The Pages workflow assembles the site from four builds on four runners: the explainer
(renamed to `explainer.html` when it is published), the site pages from
`devtools.render_overview`, the workbench, and the optimality paper under
`n11-optimality/`. This puts the same four side by side on one machine, so the site can
be looked at, and its navigation followed, before anything is deployed. It never deploys
and never writes into `packing/site/`.

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m devtools.preview_site
    uv run --frozen --all-extras --group dev python -m devtools.preview_site --serve
    uv run --frozen --all-extras --group dev python -m devtools.preview_site --shots DIR
    uv run --frozen --all-extras --group dev python -m devtools.preview_site --clips

`--skip explainer`, `--skip workbench` or `--skip optimality` leaves a slow build out;
a link to it then points at a missing page, which the link check reports rather than
fails on, and a build already in `--output` stays. `--page` shoots only the pages it
names, each with any fragment (`cases.html#n-11` is one case's record), and `--press`
names an element to press on each page that has one (a card, an atlas cell), so what it
opens is checked and shot too. Every page is also laid out at `CLIP_WIDTHS`, with and
without a scrollbar's width taken from the layout, and fails where a table, a filter
bar, a count or any other wide block runs past an ancestor that clips or scrolls
sideways. Set `SQPACK_CHROMIUM` to use a browser the environment supplies, as the
explainer's own tools do.
"""

from __future__ import annotations

import argparse
import contextlib
import functools
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from collections.abc import Sequence
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal

from devtools import render_overview

if TYPE_CHECKING:
    from playwright.sync_api import Page
from devtools.render_explainer_pdf import BROWSER_OVERRIDE
from sqpack.probes import probe

PACKING = Path(__file__).resolve().parents[1]
REPO = PACKING.parent
DEFAULT_OUTPUT = Path(tempfile.gettempdir()) / "squares-site-preview"
BUILDS = ("explainer", "pages", "workbench", "optimality")
WIDTHS = (1280, 390)
PROBES = PACKING / "devtools" / "probes"
_OVERFLOW = probe(PROBES, "preview_site/overflow")
_MATH_PENDING = probe(PROBES, "preview_site/math_pending")
MATH_FACE = probe(PROBES, "preview_site/math_face")
_SCROLL_TOP = probe(PROBES, "preview_site/scroll_top")
_AT_FOOT = probe(PROBES, "preview_site/at_foot")
_CARDS = probe(PROBES, "measure_site_pages/cards")
CLIPPED = probe(PROBES, "preview_site/clipped")
HEADER = probe(PROBES, "preview_site/header")
#: The widths every page is laid out at to look for a clipped wide block, beside the
#: two it is shot at: a tablet upright and on its side, where a narrow page clips at the
#: document's edge and a wide block has no room to spare.
CLIP_WIDTHS = (1024, 768)
#: A classic scrollbar's width, taken from the layout but not from the window: `100vw`
#: and a media query still see the whole window, which is what a block sized from the
#: window gets wrong. A headless browser draws its scrollbar over the page, so the check
#: narrows the page by this much itself.
SCROLLBAR_PX = 15
#: How far, in CSS pixels, a row of cards may sit off the centre of its line.
CENTRE_TOLERANCE = 1.0
#: How long a page may take to typeset all its math before it is shot as it stands. The
#: site typesets the formulas near the viewport first and the rest in idle time
#: (`overview/math.js`); the synopsis's 1,357 took 40 to 50 seconds of scrolling in all.
MATH_WAIT_MS = 60_000
#: How long the pictures a page loads as it is scrolled may take to arrive.
LAZY_WAIT_MS = 5_000
#: How long what a press opens may take to typeset its math.
PRESS_WAIT_MS = 5_000
HREF = re.compile(r'<nav class="site-nav".*?</nav>', re.DOTALL)
#: The motion preference a tool opens the site's pages under: a reader's who asks for
#: reduced motion. The Visualize page starts its film on a visit unless the reader asks
#: that (`overview/film.js`), and the film is a 216 MB release download a page would wait
#: on and a shot would catch mid-frame; under this it stands at its poster and nothing
#: is fetched. The only other difference is that a hover's colour changes at once.
REDUCED_MOTION: Literal["reduce"] = "reduce"


def _run(*args: str) -> None:
    print("+", " ".join(args), flush=True)
    subprocess.run([sys.executable, "-m", *args], cwd=PACKING, check=True)


def build_explainer(output: Path) -> None:
    """The explainer as `publish` leaves it: `index.html` renamed, assets beside it."""
    with tempfile.TemporaryDirectory() as scratch:
        page = Path(scratch) / "index.html"
        _run("devtools.render_explainer", "--prepare-math", "--output", str(page))
        for built in Path(scratch).iterdir():
            target = output / ("explainer.html" if built == page else built.name)
            shutil.copyfile(built, target)


def build_workbench(output: Path) -> None:
    _run("workbench_tools.build_site", "--out", str(output / "workbench"))


def build_optimality(output: Path) -> None:
    """The optimality paper as its Pages job leaves it: the page, its Markdown and its
    PDF, in the directory it is served from."""
    from devtools.render_n11_optimality_explainer import OUTPUT_DIR  # noqa: PLC0415

    _run(
        "devtools.render_n11_optimality_explainer",
        "--output-dir",
        str(output / OUTPUT_DIR.name),
        "--pdf",
    )


def build(output: Path, skip: set[str]) -> None:
    output.mkdir(parents=True, exist_ok=True)
    if "explainer" not in skip:
        build_explainer(output)
    if "pages" not in skip:
        pages = render_overview.render_all()
        fragments = render_overview.result_fragments()
        render_overview.write_site(output, [*pages, *fragments])
        for page in pages:
            print(f"wrote {output / page.name}")
        print(f"wrote {len(fragments)} result overviews beside them")
    if "workbench" not in skip:
        build_workbench(output)
    if "optimality" not in skip:
        build_optimality(output)


def missing_links(output: Path) -> list[str]:
    """Every nav link on every built page that names a page this build lacks."""
    missing = []
    for name in render_overview.SITE_PAGES:
        path = output / name
        if not path.is_file():
            continue
        nav = HREF.search(path.read_text(encoding="utf-8"))
        if nav is None:
            missing.append(f"{name}: no site nav")
            continue
        base = path.parent
        for href in re.findall(r'href="([^"#?]+)', nav.group(0)):
            if href.startswith("https://"):
                continue
            target = (base / href).resolve()
            if target.is_dir():
                target /= "index.html"
            if not target.is_file():
                missing.append(f"{name}: {href}")
    return missing


class _Handler(SimpleHTTPRequestHandler):
    """A quiet static server. `/favicon.ico` gets an empty answer: no page declares an
    icon, so a browser's automatic request would otherwise log a 404 as a page error."""

    def do_GET(self) -> None:
        if self.path == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
            return
        super().do_GET()

    def log_message(self, format: str, *args: object) -> None:  # noqa: A002
        pass


def serve(output: Path, port: int) -> ThreadingHTTPServer:
    handler = functools.partial(_Handler, directory=str(output))
    server = ThreadingHTTPServer(("127.0.0.1", port), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def shot_stem(name: str) -> str:
    """A page's screenshot name, less its width: `workbench/index.html` is `workbench`,
    `cases.html#n-11` is `cases-n-11`, and a page in a directory keeps the directory's
    name, so every shot lands in the one folder."""
    stem = name.replace("/index.html", "").replace(".html", "")
    return stem.replace("#", "-").replace("/", "-")


def off_centre(sections: list[dict[str, Any]]) -> list[str]:
    """Every row of cards, in a `measure_site_pages cards` report of one page, that does
    not sit centred on its line: its slack at the start and at the end differ."""
    return [
        f"a row of {row['cards']} cards in {section['section'] or 'the page'} is off centre: "
        f"{row['start']}px before it, {row['end']}px after"
        for section in sections
        for row in section["rows"]
        if abs(row["start"] - row["end"]) > CENTRE_TOLERANCE
    ]


def tabs_problems(found: dict[str, Any]) -> list[str]:
    """What is wrong with where a page's section tabs stand, in a `preview_site/header`
    report. From the top a page of a section reads bar, rule, tabs, content: the tabs
    start at or below the foot of the rule under the navigation bar, and the content
    starts at or below the foot of the tabs. A page with no tabs has nothing to say."""
    tabs, rule, first = found["tabs"], found["rule"], found["first"]
    if tabs is None:
        return []
    if rule is None:
        return ["the section tabs have no rule over them, under the navigation bar"]
    problems: list[str] = []
    if tabs["top"] < rule["bottom"]:
        problems.append(
            f"the section tabs start {rule['bottom'] - tabs['top']:g}px above the foot of "
            f"the rule under the navigation bar, which is on {rule['on']}"
        )
    if first is not None and first["top"] < tabs["bottom"]:
        problems.append(
            f"{first['block']} starts {tabs['bottom'] - first['top']:g}px above the foot of "
            "the section tabs"
        )
    return problems


def type_problems(found: dict[str, Any]) -> list[str]:
    """What is wrong with the size of the bar's type, in a `preview_site/header` report,
    held against the body's and never against a pixel value. A link in the bar, and a
    section tab, is one step below the body on the paper's scale and no more: smaller
    than the prose base, and no smaller than the largest step of the scale under it. The
    two are one size. The site's name is at least the body's size. A page with no bar has
    nothing to say, and nor does one that does not carry the paper's scale, the
    optimality paper, whose body is its own."""
    sizes = found["type"]
    if sizes["link"] is None or sizes["scale"] is None:
        return []
    body = sizes["scale"]["prose"]
    below = max(step for step in sizes["scale"].values() if step < body)
    problems: list[str] = []
    for part in ("link", "tab"):
        size = sizes[part]
        if size is None:
            continue
        if not below <= size < body:
            problems.append(
                f"a {part} in the header is {size:g}px: it should be under the body's "
                f"{body:g}px and no smaller than the step below it, {below:g}px"
            )
    if sizes["tab"] is not None and sizes["tab"] != sizes["link"]:
        problems.append(
            f"a section tab is {sizes['tab']:g}px and a link in the bar {sizes['link']:g}px"
        )
    if sizes["name"] is not None and sizes["name"] < body:
        problems.append(f"the site's name is {sizes['name']:g}px, under the body's {body:g}px")
    return problems


def clipped(page: Page) -> list[str]:
    """Every wide block on the page as it stands that runs past an ancestor which clips
    or scrolls sideways, as laid out now and again with a scrollbar's width taken from
    the layout; each named once, with how far it runs past either side."""
    problems: list[str] = []
    for scrollbar in (0, SCROLLBAR_PX):
        for found in page.evaluate(CLIPPED, {"scrollbar": scrollbar}):
            problem = clip_problem(found, scrollbar=scrollbar)
            if problem not in problems:
                problems.append(problem)
    return problems


def clip_problem(found: dict[str, Any], *, scrollbar: int = 0) -> str:
    """One clipped block, as the probe reports it, in words."""
    sides = " and ".join(
        f"{found[side]:g}px past its {side} edge" for side in ("left", "right") if found[side]
    )
    under = f", with a {scrollbar}px scrollbar" if scrollbar else ""
    return f"{found['block']} runs {sides} of {found['frame']}, which clips it{under}"


def clip_check(
    output: Path, port: int, pages: Sequence[str], widths: Sequence[int] = CLIP_WIDTHS
) -> list[str]:
    """Every clipped wide block on every built page at each of `widths`. A page is only
    laid out here, not walked or shot, since a block's box does not wait on its math."""
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    errors: list[str] = []
    server = serve(output, port)
    try:
        with sync_playwright() as driver:
            browser = driver.chromium.launch(executable_path=os.environ.get(BROWSER_OVERRIDE))
            for name in pages:
                if not (output / name.partition("#")[0]).is_file():
                    continue
                for width in widths:
                    page = browser.new_page(
                        viewport={"width": width, "height": 900},
                        reduced_motion=REDUCED_MOTION,
                    )
                    page.goto(f"http://127.0.0.1:{port}/{name}", wait_until="load")
                    page.wait_for_timeout(200)
                    errors.extend(f"{name} @{width}: {problem}" for problem in clipped(page))
                    page.close()
            browser.close()
    finally:
        server.shutdown()
        server.server_close()
    return errors


def settle_math(page: Page) -> int:
    """Scroll the page through once, a screen at a time, to its foot, and on until every
    formula is typeset, then return to the top; returns how many were still untypeset
    when the wait ran out. Reaching the foot is what places whatever a page lays out or
    loads only as it nears the window, the atlas grid and a card's picture among them,
    even on a page whose math was done at once; what that starts loading is given
    `LAZY_WAIT_MS` to arrive, and a page that keeps the network busy is shot as it
    stands. The return is instant and waited for: the wheel's own scroll animates, and a
    screenshot taken during it was drawn offset."""
    from playwright.sync_api import TimeoutError as PlaywrightTimeout  # noqa: PLC0415

    deadline = time.monotonic() + MATH_WAIT_MS / 1000
    while time.monotonic() < deadline:
        if not page.evaluate(_MATH_PENDING) and page.evaluate(_AT_FOOT):
            break
        page.mouse.wheel(0, 800)
        page.wait_for_timeout(100)
    pending = page.evaluate(_MATH_PENDING)
    with contextlib.suppress(PlaywrightTimeout):
        page.wait_for_load_state("networkidle", timeout=LAZY_WAIT_MS)
    page.wait_for_timeout(200)
    page.wait_for_function(_SCROLL_TOP)
    return pending


def press(page: Page, selector: str) -> list[str]:
    """Press the first element `selector` matches and wait for what it opens to typeset
    its math; returns the formulas then set in the wrong face. A popover's math is only
    typeset once it opens, so the page's own check cannot see it."""
    page.locator(selector).first.click()
    deadline = time.monotonic() + PRESS_WAIT_MS / 1000
    while page.evaluate(_MATH_PENDING) and time.monotonic() < deadline:
        page.wait_for_timeout(100)
    page.wait_for_timeout(300)
    return page.evaluate(MATH_FACE)


def screenshots(
    output: Path,
    shots: Path,
    port: int,
    pages: Sequence[str] = render_overview.SITE_PAGES,
    presses: Sequence[str] = (),
) -> list[str]:
    """A full-page screenshot of every built page at each width, with what went wrong:
    console errors, math left untypeset or set in the other face from its text, a row of
    cards off the centre of its line, any page wider than its viewport, section tabs
    that do not stand under the bar's rule (`tabs_problems`), a bar whose type is not
    one step under the body's (`type_problems`), and any wide block that
    runs past an ancestor which clips it (`clipped`). Each selector in
    `presses` is then pressed on every page that has a match, its math and its blocks
    checked the same way, and the window shot as `<page>-<width>-press<n>.png`. Every
    page is opened as for a reader who asks for reduced motion (`REDUCED_MOTION`), so
    the Visualize page's film is shot at its poster and its download never starts."""
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    shots.mkdir(parents=True, exist_ok=True)
    errors: list[str] = []
    server = serve(output, port)
    try:
        with sync_playwright() as driver:
            browser = driver.chromium.launch(executable_path=os.environ.get(BROWSER_OVERRIDE))
            for name in pages:
                if not (output / name.partition("#")[0]).is_file():
                    continue
                for width in WIDTHS:
                    page = browser.new_page(
                        viewport={"width": width, "height": 900},
                        reduced_motion=REDUCED_MOTION,
                    )
                    page.on(
                        "console",
                        lambda message, name=name, width=width: (
                            errors.append(f"{name} @{width}: {message.text}")
                            if message.type == "error"
                            else None
                        ),
                    )
                    page.goto(f"http://127.0.0.1:{port}/{name}", wait_until="networkidle")
                    pending = settle_math(page)
                    if pending:
                        errors.append(f"{name} @{width}: {pending} math spans never typeset")
                    faces: list[str] = page.evaluate(MATH_FACE)
                    errors.extend(f"{name} @{width}: {mismatch}" for mismatch in faces)
                    errors.extend(
                        f"{name} @{width}: {problem}"
                        for problem in off_centre(page.evaluate(_CARDS))
                    )
                    overflow = page.evaluate(_OVERFLOW)
                    if overflow > 0:
                        errors.append(f"{name} @{width}: {overflow}px wider than the viewport")
                    header = page.evaluate(HEADER)
                    errors.extend(
                        f"{name} @{width}: {problem}"
                        for problem in (*tabs_problems(header), *type_problems(header))
                    )
                    cut = clipped(page)
                    errors.extend(f"{name} @{width}: {problem}" for problem in cut)
                    stem = shot_stem(name)
                    target = shots / f"{stem}-{width}.png"
                    page.screenshot(path=str(target), full_page=True)
                    print(f"shot {target}")
                    for index, selector in enumerate(presses, start=1):
                        if not page.locator(selector).count():
                            continue
                        errors.extend(
                            f"{name} @{width}, {selector} pressed: {mismatch}"
                            for mismatch in press(page, selector)
                            if mismatch not in faces
                        )
                        errors.extend(
                            f"{name} @{width}, {selector} pressed: {problem}"
                            for problem in clipped(page)
                            if problem not in cut
                        )
                        target = shots / f"{stem}-{width}-press{index}.png"
                        page.screenshot(path=str(target))
                        print(f"shot {target}")
                        page.keyboard.press("Escape")
                    page.close()
            browser.close()
    finally:
        server.shutdown()
        server.server_close()
    return errors


def _site_page(name: str) -> str:
    """A `--page` value: a page the site serves, with any fragment."""
    if name.partition("#")[0] not in render_overview.SITE_PAGES:
        served = ", ".join(render_overview.SITE_PAGES)
        raise argparse.ArgumentTypeError(f"{name} is not a page the site serves: {served}")
    return name


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--skip", action="append", choices=BUILDS, default=[])
    parser.add_argument("--shots", type=Path, help="write screenshots of every page here")
    parser.add_argument(
        "--page",
        action="append",
        type=_site_page,
        metavar="PAGE",
        help="with --shots or --clips: only this page, with any #fragment; repeatable",
    )
    parser.add_argument(
        "--press",
        action="append",
        default=[],
        metavar="SELECTOR",
        help="with --shots: press the first element this CSS selector matches on each page "
        "that has one, then check and shoot what it opens; repeatable",
    )
    parser.add_argument(
        "--clips",
        action="store_true",
        help="lay every page out at 1024, 768 and 390 pixels and report each wide block an "
        "ancestor clips, without shooting anything; --page narrows it",
    )
    parser.add_argument("--serve", action="store_true", help="serve the site until stopped")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args(argv)
    output = args.output.resolve()
    if output == (PACKING / "site").resolve():
        parser.error("the preview never writes into packing/site/")

    build(output, set(args.skip))
    status = 0
    for problem in missing_links(output):
        print(f"missing: {problem}", file=sys.stderr)
    if args.shots:
        pages = tuple(args.page or render_overview.SITE_PAGES)
        problems = screenshots(output, args.shots.resolve(), args.port, pages, args.press)
        problems += clip_check(output, args.port, pages)
        for error in problems:
            print(f"problem: {error}", file=sys.stderr)
            status = 1
    if args.clips:
        pages = tuple(args.page or render_overview.SITE_PAGES)
        for error in clip_check(output, args.port, pages, (*CLIP_WIDTHS, WIDTHS[-1])):
            print(f"problem: {error}", file=sys.stderr)
            status = 1
    if args.serve:
        server = serve(output, args.port)
        print(f"serving {output} at http://127.0.0.1:{args.port}/ (Ctrl-C to stop)")
        try:
            threading.Event().wait()
        except KeyboardInterrupt:
            server.shutdown()
    return status


if __name__ == "__main__":
    raise SystemExit(main())
