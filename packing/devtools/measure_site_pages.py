#!/usr/bin/env python3
"""Measure a built site's pages against the explainer: load and math timing, text, faces.

Three measurements, each over pages of a directory `preview_site` has built:

- `load` serves the directory on a local port and opens each page in a fresh Chromium
  context, cold cache, at a desktop or phone width. An init script (a probe) records
  long tasks and, on every animation frame, how many displayed formulas are typeset
  and showing. It reports DOMContentLoaded, load, first contentful paint, the first
  frame at which every formula in the first viewport is readable and the first at which
  every displayed formula is, the long tasks and their blocking time over 50 ms, and the
  document's bytes. Times are milliseconds from navigation start; `--runs` repeats each
  load and reports the median. An animation frame is an opportunity to paint, not a
  presented frame, and the per-frame scan is observer overhead every page pays alike.
- `type` reports the reading column's resolved typography, role by role (paragraph,
  h1 to h4, list item, table cell, code, inline math), and every `--kpress-*`,
  `--site-*`, `--paper-*` and `--cert-*` token the root and the column resolve.
- `faces` needs no browser: it lists every `@font-face` block each page inlines, by
  family, and whether the block is byte-identical to the explainer's.

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m devtools.measure_site_pages load SITE
    uv run --frozen --all-extras --group dev python -m devtools.measure_site_pages type SITE
    uv run --frozen --all-extras --group dev python -m devtools.measure_site_pages faces SITE

`SITE` is a directory holding `explainer.html` and the kpress pages. Set
`SQPACK_CHROMIUM` to use a browser the environment supplies, as the other tools do.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import statistics
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from devtools.preview_site import serve
from devtools.render_explainer_pdf import BROWSER_OVERRIDE
from sqpack.probes import applied, probe

PROBES = Path(__file__).resolve().parent / "probes"
_INSTRUMENT = applied(probe(PROBES, "measure_site_pages/instrument"))
_DONE = probe(PROBES, "measure_site_pages/done")
_REPORT = probe(PROBES, "measure_site_pages/report")
TYPOGRAPHY = probe(PROBES, "measure_site_pages/typography")

#: The pages compared by default: the explainer, the long reports, a short one, the
#: homepage and one case record.
DEFAULT_PAGES = (
    "explainer.html",
    "tutorial.html",
    "synopsis.html",
    "results.html",
    "readme.html",
    "index.html",
    "cases.html#n-11",
)
#: How long a load may take to finish its math before it is reported as it stands.
WAIT_MS = 35_000
FONT_FACE = re.compile(r"@font-face\s*\{[^}]*\}")
FAMILY = re.compile(r"font-family:\s*(\"[^\"]+\"|[^;]+);")


def _launch(driver: Any) -> Any:
    return driver.chromium.launch(executable_path=os.environ.get(BROWSER_OVERRIDE))


def measure_load(
    base: str, pages: Sequence[str], *, widths: Sequence[int], runs: int
) -> list[dict[str, Any]]:
    """Each page's load report at each width, the median of `runs` cold loads."""
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    results: list[dict[str, Any]] = []
    with sync_playwright() as driver:
        browser = _launch(driver)
        for width in widths:
            for name in pages:
                samples: list[dict[str, Any]] = []
                for _ in range(runs):
                    context = browser.new_context(viewport={"width": width, "height": 900})
                    context.add_init_script(_INSTRUMENT)
                    page = context.new_page()
                    page.goto(f"{base}/{name}", wait_until="load")
                    page.wait_for_function(_DONE, timeout=WAIT_MS)
                    samples.append(page.evaluate(_REPORT))
                    context.close()
                results.append({"page": name, "width": width, **_median(samples)})
        browser.close()
    return results


def _median(samples: list[dict[str, Any]]) -> dict[str, Any]:
    merged: dict[str, Any] = {}
    for key, first in samples[0].items():
        values = [sample[key] for sample in samples]
        if isinstance(first, (int, float)) and not isinstance(first, bool):
            present = [value for value in values if value is not None]
            merged[key] = round(statistics.median(present), 1) if present else None
        else:
            merged[key] = values[-1]
    return merged


def measure_type(
    base: str, pages: Sequence[str], *, widths: Sequence[int]
) -> list[dict[str, Any]]:
    """Each page's reading typography and resolved tokens at each width."""
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    results: list[dict[str, Any]] = []
    with sync_playwright() as driver:
        browser = _launch(driver)
        for width in widths:
            for name in pages:
                page = browser.new_page(viewport={"width": width, "height": 900})
                page.goto(f"{base}/{name}", wait_until="load")
                page.wait_for_timeout(300)
                results.append({"page": name, "width": width, **page.evaluate(TYPOGRAPHY)})
                page.close()
        browser.close()
    return results


def font_faces(path: Path) -> dict[str, str]:
    """Every `@font-face` block a page inlines, keyed by its digest, valued by family."""
    faces: dict[str, str] = {}
    for block in FONT_FACE.findall(path.read_text(encoding="utf-8")):
        family = FAMILY.search(block)
        name = family.group(1).strip().strip('"') if family else "?"
        faces[hashlib.sha256(block.encode()).hexdigest()[:12]] = name
    return faces


def compare_faces(site: Path, pages: Sequence[str]) -> list[dict[str, Any]]:
    """Per page and family: blocks shared with the explainer, and blocks it lacks or adds."""
    reference = font_faces(site / "explainer.html")
    rows: list[dict[str, Any]] = []
    for name in pages:
        path = site / name.split("#")[0]
        faces = font_faces(path)
        families = sorted(set(faces.values()) | set(reference.values()))
        for family in families:
            mine = {digest for digest, value in faces.items() if value == family}
            theirs = {digest for digest, value in reference.items() if value == family}
            rows.append(
                {
                    "page": name,
                    "family": family,
                    "shared": len(mine & theirs),
                    "only_here": len(mine - theirs),
                    "only_explainer": len(theirs - mine),
                }
            )
    return rows


def type_rows(report: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """A `type` report flattened to one row per page, width and role."""
    return [
        {"page": row["page"], "width": row["width"], "role": role, **values}
        for row in report
        for role, values in row["roles"].items()
        if values is not None
    ]


def token_rows(
    report: list[dict[str, Any]], *, scope: str = "root_tokens"
) -> list[dict[str, Any]]:
    """Every `--kpress-*` token whose value differs between pages at one width, by page.

    The first page of each width is the reference, which is the explainer by default. A
    token a page does not resolve at all is shown as `-`.
    """
    rows: list[dict[str, Any]] = []
    for width in dict.fromkeys(row["width"] for row in report):
        at = [row for row in report if row["width"] == width]
        names = sorted(
            {name for row in at for name in row[scope] if name.startswith("--kpress-")}
        )
        for name in names:
            values = [" ".join(row[scope].get(name, "-").split()) for row in at]
            if len(set(values)) > 1:
                rows.append(
                    {
                        "width": width,
                        "token": name,
                        **{row["page"]: value for row, value in zip(at, values, strict=True)},
                    }
                )
    return rows


def markdown_table(report: list[dict[str, Any]]) -> str:
    """A report's flat columns as a Markdown table, for a design note or a pull request."""
    if report and "roles" in report[0]:
        report = type_rows(report)
    columns = [key for key, value in report[0].items() if not isinstance(value, (dict, list))]
    lines = ["| " + " | ".join(columns) + " |", "|" + " --- |" * len(columns)]
    lines.extend("| " + " | ".join(str(row[key]) for key in columns) + " |" for row in report)
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("mode", choices=("load", "type", "faces"))
    parser.add_argument("site", type=Path)
    parser.add_argument(
        "--page", action="append", help="a page, with any #fragment; repeatable"
    )
    parser.add_argument("--width", type=int, action="append", help="viewport width; repeatable")
    parser.add_argument("--runs", type=int, default=3)
    parser.add_argument("--port", type=int, default=18961)
    parser.add_argument("--json", type=Path, help="read a saved report rather than measuring")
    parser.add_argument("--markdown", action="store_true", help="print a table, not JSON")
    parser.add_argument(
        "--tokens",
        choices=("root_tokens", "column_tokens"),
        help="with `type`: list only the `--kpress-*` tokens that differ between pages",
    )
    args = parser.parse_args(argv)
    site = args.site.resolve()
    pages = tuple(args.page or DEFAULT_PAGES)
    widths = tuple(args.width or (1280,))
    if args.json is not None:
        report: list[dict[str, Any]] = json.loads(args.json.read_text(encoding="utf-8"))
    elif args.mode == "faces":
        report = compare_faces(site, pages)
    else:
        server = serve(site, args.port)
        base = f"http://127.0.0.1:{args.port}"
        try:
            if args.mode == "type":
                report = measure_type(base, pages, widths=widths)
            else:
                report = measure_load(base, pages, widths=widths, runs=args.runs)
        finally:
            server.shutdown()
            server.server_close()
    if args.tokens:
        report = token_rows(report, scope=args.tokens)
    if args.markdown:
        print(markdown_table(report))
    else:
        json.dump(report, sys.stdout, indent=2)
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
