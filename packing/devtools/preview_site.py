#!/usr/bin/env python3
"""Build the whole published site into one directory, serve it, and screenshot it.

The Pages workflow assembles the site from three builds on three runners: the explainer
(renamed to `explainer.html` when it is published), the site pages from
`devtools.render_overview`, and the workbench. This puts the same three side by side on
one machine, so the site can be looked at, and its navigation followed, before anything
is deployed. It never deploys and never writes into `packing/site/`.

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m devtools.preview_site
    uv run --frozen --all-extras --group dev python -m devtools.preview_site --serve
    uv run --frozen --all-extras --group dev python -m devtools.preview_site --shots DIR

`--skip explainer` or `--skip workbench` leaves a slow build out; its nav link then
points at a missing page, which the link check reports rather than fails on, and a build
already in `--output` stays. `--page` shoots only the pages it names, each with any
fragment (`cases.html#n-11` is one case's record), and `--press` names an element to
press on each page that has one (a card, an atlas cell), so what it opens is checked and
shot too. Set
`SQPACK_CHROMIUM` to use a browser the environment supplies, as the explainer's own
tools do.
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
from typing import TYPE_CHECKING, Any

from devtools import render_overview

if TYPE_CHECKING:
    from playwright.sync_api import Page
from devtools.render_explainer_pdf import BROWSER_OVERRIDE
from sqpack.probes import probe

PACKING = Path(__file__).resolve().parents[1]
REPO = PACKING.parent
DEFAULT_OUTPUT = Path(tempfile.gettempdir()) / "squares-site-preview"
BUILDS = ("explainer", "pages", "workbench")
WIDTHS = (1280, 390)
PROBES = PACKING / "devtools" / "probes"
_OVERFLOW = probe(PROBES, "preview_site/overflow")
_MATH_PENDING = probe(PROBES, "preview_site/math_pending")
MATH_FACE = probe(PROBES, "preview_site/math_face")
_SCROLL_TOP = probe(PROBES, "preview_site/scroll_top")
_AT_FOOT = probe(PROBES, "preview_site/at_foot")
_CARDS = probe(PROBES, "measure_site_pages/cards")
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
    and `cases.html#n-11` is `cases-n-11`."""
    return name.replace("/index.html", "").replace(".html", "").replace("#", "-")


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
    cards off the centre of its line, and any page wider than its viewport. Each
    selector in `presses` is then pressed on every page that has a match, its math checked
    the same way, and the window shot as `<page>-<width>-press<n>.png`."""
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
                    page = browser.new_page(viewport={"width": width, "height": 900})
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
                        target = shots / f"{stem}-{width}-press{index}.png"
                        page.screenshot(path=str(target))
                        print(f"shot {target}")
                        page.keyboard.press("Escape")
                    page.close()
            browser.close()
    finally:
        server.shutdown()
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
        help="with --shots: shoot only this page, with any #fragment; repeatable",
    )
    parser.add_argument(
        "--press",
        action="append",
        default=[],
        metavar="SELECTOR",
        help="with --shots: press the first element this CSS selector matches on each page "
        "that has one, then check and shoot what it opens; repeatable",
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
        for error in screenshots(output, args.shots.resolve(), args.port, pages, args.press):
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
