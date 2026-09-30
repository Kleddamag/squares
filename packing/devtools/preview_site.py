#!/usr/bin/env python3
"""Assemble the published site locally, serve it, and look at every page in a browser.

The Pages workflow publishes one artifact built by three builders: the explainer
(`devtools.render_explainer`, into `packing/site/`, renamed to `explainer.html` at
publication), the site's own pages (`devtools.render_overview`, into
`packing/site-overview/`), and the Visualizer (`workbench_tools.build_site`, into
`packing/site/workbench/`). Nothing deploys until the owner has reviewed the whole site,
so this tool puts the same tree together locally, serves it over HTTP the way Pages does,
and checks each page for what a reader would notice first and a render test cannot see.

**Two modes.**

- `--smoke DIR` is what the workflow's `overview` job runs on its own render: every page
  under DIR is opened at desktop and phone widths, and the run fails on a script error, on
  math that never finishes typesetting, and on a page wider than its viewport.
- By default it assembles `packing/site-preview/` from the builders' directories (with
  `--build` it renders the explainer and the overview first), serves it, runs the smoke
  checks on every page in light and dark, resolves every relative link and embedded
  resource against the assembled tree, runs the explainer's own math-face check
  (`devtools.check_math_faces`) on each of the site's pages, and saves full-page
  screenshots at 1,280 and 390 pixels wide in both themes to `--screenshots`.

The films are copied into the site only on `main`, so locally a link to `films/…` is
reported as expected-missing unless `--films DIR` names a directory holding them.

The browser code lives in `probes/preview_site/`, one expression per file.

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m devtools.preview_site --build
    uv run --frozen --all-extras --group dev python -m devtools.preview_site \\
        --smoke site-overview
"""

from __future__ import annotations

import argparse
import functools
import os
import posixpath
import shutil
import subprocess
import sys
import threading
from collections.abc import Iterator, Sequence
from contextlib import contextmanager
from dataclasses import dataclass, field
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from devtools.render_explainer_pdf import BROWSER_OVERRIDE
from sqpack.probes import probe

PACKING = Path(__file__).resolve().parents[1]
REPO = PACKING.parent
EXPLAINER_SITE = PACKING / "site"
OVERVIEW_SITE = PACKING / "site-overview"
WORKBENCH_SITE = EXPLAINER_SITE / "workbench"
PREVIEW = PACKING / "site-preview"
SCREENSHOTS = PACKING / "site-preview-screenshots"
PROBES = Path(__file__).resolve().parent / "probes"

#: The widths every page is opened at: the desktop reference and the narrowest phone the
#: explainer's own geometry checks use.
WIDTHS = (1280, 390)
SCHEMES = ("light", "dark")
READY_TIMEOUT_MS = 30_000
#: A page may be one pixel wider than its viewport from subpixel rounding; more scrolls.
OVERFLOW_TOLERANCE = 1
#: Present only on `main`, where `publish` copies the release's films into the site.
FILMS_PREFIX = "films/"


@dataclass
class Findings:
    """What the run objects to, and what it notes without failing."""

    problems: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


class _QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: Any) -> None:  # noqa: A002
        del format, args


@contextmanager
def served(root: Path) -> Iterator[str]:
    """Serve `root` over HTTP on a free local port, as Pages serves the artifact."""
    handler = functools.partial(_QuietHandler, directory=str(root))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_address[1]}/"
    finally:
        server.shutdown()
        server.server_close()


def pages_under(root: Path) -> list[str]:
    """Every HTML page under `root`, site-relative, the Visualizer's app shell included."""
    return sorted(path.relative_to(root).as_posix() for path in root.rglob("*.html"))


def _resolve(page: str, reference: str) -> str | None:
    """A site-relative path for a relative reference on `page`, or None if it is not one."""
    parts = urlsplit(reference)
    if parts.scheme or parts.netloc or not parts.path:
        return None
    joined = posixpath.normpath(posixpath.join(posixpath.dirname(page), parts.path))
    if joined == ".":
        return "index.html"
    if parts.path.endswith("/"):
        return posixpath.join(joined, "index.html")
    return joined


def missing_references(
    root: Path, page: str, references: Sequence[str], findings: Findings, *, films: bool
) -> None:
    """Report every relative reference on `page` that the assembled site does not hold."""
    for reference in references:
        target = _resolve(page, reference)
        if target is None:
            continue
        if target.startswith(".."):
            findings.problems.append(f"{page}: {reference} leaves the site")
            continue
        if (root / target).is_file():
            continue
        if target.startswith(FILMS_PREFIX) and not films:
            findings.notes.append(f"{page}: {reference} is copied into the site on main only")
            continue
        findings.problems.append(f"{page}: {reference} names {target}, which the site lacks")


def open_pages(
    base_url: str,
    root: Path,
    pages: Sequence[str],
    findings: Findings,
    *,
    schemes: Sequence[str] = ("light",),
    screenshots: Path | None = None,
    check_links: bool = False,
    films: bool = False,
) -> None:
    """Open every page at each width and scheme, and record what it objects to."""
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    overflow = probe(PROBES, "preview_site/overflow")
    ready = probe(PROBES, "preview_site/ready")
    links = probe(PROBES, "preview_site/links")
    with sync_playwright() as driver:
        browser = driver.chromium.launch(executable_path=os.environ.get(BROWSER_OVERRIDE))
        try:
            for scheme in schemes:
                for width in WIDTHS:
                    context = browser.new_context(
                        viewport={"width": width, "height": 900},
                        color_scheme="dark" if scheme == "dark" else "light",
                        reduced_motion="reduce",
                    )
                    try:
                        for page_path in pages:
                            where = f"{page_path} at {width} px, {scheme}"
                            page = context.new_page()
                            errors: list[str] = []
                            page.on(
                                "pageerror",
                                lambda error, errors=errors: errors.append(str(error)),
                            )
                            page.on(
                                "console",
                                lambda message, errors=errors: (
                                    errors.append(message.text)
                                    if message.type == "error"
                                    else None
                                ),
                            )
                            page.goto(base_url + page_path, wait_until="load")
                            try:
                                page.wait_for_function(ready, timeout=READY_TIMEOUT_MS)
                            except Exception:  # noqa: BLE001 -- Playwright's timeout, reported
                                findings.problems.append(f"{where}: math never finished")
                            box = page.evaluate(overflow)
                            if box["scrollWidth"] > box["clientWidth"] + OVERFLOW_TOLERANCE:
                                findings.problems.append(
                                    f"{where}: {box['scrollWidth']} px wide in a "
                                    f"{box['clientWidth']} px viewport"
                                )
                            findings.problems.extend(f"{where}: {error}" for error in errors)
                            if check_links and width == WIDTHS[0] and scheme == schemes[0]:
                                named = page.evaluate(links)
                                missing_references(
                                    root,
                                    page_path,
                                    [*named["hrefs"], *named["sources"], *named["posters"]],
                                    findings,
                                    films=films,
                                )
                            if screenshots is not None:
                                name = page_path.replace("/", "_").removesuffix(".html")
                                page.screenshot(
                                    path=screenshots / f"{name}-{width}-{scheme}.png",
                                    full_page=True,
                                )
                            page.close()
                    finally:
                        context.close()
        finally:
            browser.close()


def assemble(output: Path, *, films: Path | None = None) -> None:
    """Put the site together as `publish` does, from the builders' directories."""
    index = EXPLAINER_SITE / "index.html"
    if not index.is_file():
        raise SystemExit("the explainer has not been rendered; run with --build")
    if not (OVERVIEW_SITE / "index.html").is_file():
        raise SystemExit("the overview has not been rendered; run with --build")
    if output.exists():
        shutil.rmtree(output)
    shutil.copytree(EXPLAINER_SITE, output, ignore=shutil.ignore_patterns("workbench"))
    (output / "index.html").rename(output / "explainer.html")
    shutil.copytree(OVERVIEW_SITE, output, dirs_exist_ok=True)
    if WORKBENCH_SITE.is_dir():
        shutil.copytree(WORKBENCH_SITE, output / "workbench")
    if films is not None:
        shutil.copytree(films, output / "films")


def build() -> None:
    """Render the explainer and the overview, as their jobs do, before assembling."""
    for module in ("devtools.render_explainer", "devtools.render_overview"):
        subprocess.run((sys.executable, "-m", module), cwd=PACKING, check=True)


def report(findings: Findings) -> int:
    for note in findings.notes:
        print(f"note: {note}")
    for problem in findings.problems:
        print(f"FAIL {problem}", file=sys.stderr)
    if findings.problems:
        print(f"{len(findings.problems)} problems", file=sys.stderr)
        return 1
    print("every page opened cleanly")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n", 1)[0])
    parser.add_argument("--smoke", type=Path, help="check every page under this directory")
    parser.add_argument("--build", action="store_true", help="render the pages first")
    parser.add_argument("--output", type=Path, default=PREVIEW)
    parser.add_argument("--screenshots", type=Path, default=SCREENSHOTS)
    parser.add_argument("--films", type=Path, help="a directory holding the two films")
    parser.add_argument(
        "--no-math-faces", action="store_true", help="skip the math-face check (faster)"
    )
    args = parser.parse_args(argv)

    findings = Findings()
    if args.smoke is not None:
        root = args.smoke.resolve()
        pages = pages_under(root)
        if not pages:
            raise SystemExit(f"{root} holds no pages")
        with served(root) as url:
            open_pages(url, root, pages, findings)
        return report(findings)

    if args.build:
        build()
    output = args.output.resolve()
    assemble(output, films=args.films)
    screenshots = args.screenshots.resolve()
    screenshots.mkdir(parents=True, exist_ok=True)
    pages = pages_under(output)
    with served(output) as url:
        open_pages(
            url,
            output,
            pages,
            findings,
            schemes=SCHEMES,
            screenshots=screenshots,
            check_links=True,
            films=args.films is not None,
        )
        if not args.no_math_faces:
            from devtools import check_math_faces  # noqa: PLC0415

            for page_path in pages:
                if page_path.startswith("workbench/"):
                    continue
                result = check_math_faces.check(url + page_path)
                findings.problems.extend(
                    f"{page_path}: {finding}" for finding in result["findings"]
                )
    print(f"screenshots in {screenshots}")
    return report(findings)


if __name__ == "__main__":
    raise SystemExit(main())
