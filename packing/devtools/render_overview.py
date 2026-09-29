#!/usr/bin/env python3
"""Render the site's own pages: the overview, the frontier atlas, the tutorial and the synopsis.

The published site used to have one top-level page, the n = 11 explainer. This renderer
adds the front door and the pages around it, as the plan in
`docs/project/specs/active/plan-2026-09-29-github-pages-overview.md` lays out:

- `index.html`, the overview: the problem, the headline results, the results table and
  the verification statistics, generated from the register;
- `frontier.html`, the frontier atlas: one row for every case, from its
  `SquarePackingCase/v2` record;
- `tutorial.html` and `synopsis.html`, the two reader documents rendered as pages.

Every page is a kpress standalone page with its assets inlined, so it opens the same
way from a file, from GitHub Pages and from an artifact host. The explainer's paper
typography and accent are carried by `templates/site.css`, and one navigation partial,
`templates/site-nav.html`, joins the pages. No value on a page is typed into a template:
bounds, rungs, credits and counts are read from the record at render time.

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m devtools.render_overview
    uv run --frozen --all-extras --group dev python -m devtools.render_overview --check
    uv run --frozen --all-extras --group dev python -m devtools.render_overview --output DIR
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import NamedTuple

from devtools.render_frontier_page import FRONTIER_INPUTS
from sqpack.release import PUBLICATION_EDITION

PACKING = Path(__file__).resolve().parents[1]
REPO = PACKING.parent
TEMPLATES = PACKING / "devtools" / "templates"
SITE_CSS = TEMPLATES / "site.css"
SITE_NAV = TEMPLATES / "site-nav.html"
OVERVIEW_ARTICLE = TEMPLATES / "overview-article.md"
OUTPUT = PACKING / "site"

SITE_URL = "https://jlevy.github.io/squares/"
REPO_URL = "https://github.com/jlevy/squares"
SITE_NAME = "The Squares Project"
OVERVIEW_DESCRIPTION = (
    "Packing unit squares in the smallest square: the problem, every current result, "
    "and how each one is verified."
)
FRONTIER_DESCRIPTION = (
    "Every tracked case of packing n unit squares in the smallest square, n = 1 to 324: "
    "the best known packing, the reported and verified bounds, and the records behind them."
)

#: Every file a render reads. The Pages workflow's deploy filter and the scope tool are
#: checked against this list, so a page cannot go stale because an input moved unseen.
RENDER_INPUTS: tuple[Path, ...] = (
    Path(__file__).resolve(),
    SITE_CSS,
    SITE_NAV,
    OVERVIEW_ARTICLE,
    PACKING / "src" / "sqpack" / "release.py",
    *FRONTIER_INPUTS,
)

# The same refusal the explainer makes: a script or stylesheet with a source, a CSS
# import, or a url() that is not a data URI or a fragment is a fetch.
_EXTERNAL_REFERENCE = re.compile(
    r"<script[^>]*\ssrc="
    r'|<link(?![^>]*\srel="canonical")[^>]*\shref='
    r"|@import\b"
    r"""|url\(\s*(?!["']?(?:data:|#))"""
)


class Page(NamedTuple):
    """One rendered page: where it is served and its bytes."""

    name: str
    html: str


def page_assets() -> tuple[str, str]:
    """The explainer's own inlined assets: head styles and the math scripts.

    The stylesheets are the explainer's (`kpress_css`, `katex_css`, `relation_face_css`),
    faces already inlined as data URIs, so a reader moving between the explainer and
    these pages sees one design system. The scripts are kpress's KaTeX assets as classic
    scripts, which render `$…$` once the page loads; kpress's module scripts are left
    out, because an inline module still fetches its siblings.
    """
    from kpress.format.assets import KATEX_JS_ASSETS  # noqa: PLC0415

    from devtools.render_explainer import (  # noqa: PLC0415
        katex_css,
        kpress_css,
        kpress_static,
        relation_face_css,
    )

    static = kpress_static()
    head = (
        f"<style>{kpress_css(static)}{katex_css(static)}</style>\n"
        f"<style>{relation_face_css(static)}</style>\n"
        f"<style>{SITE_CSS.read_text(encoding='utf-8')}</style>"
    )
    scripts = "\n".join(
        f"<script>{(static / name).read_text(encoding='utf-8')}</script>"
        for name in KATEX_JS_ASSETS
    )
    return head, scripts


def assert_self_contained(name: str, page: str) -> None:
    """Refuse a page that would fetch anything at view time."""
    hit = _EXTERNAL_REFERENCE.search(page)
    if hit:
        excerpt = page[max(hit.start() - 60, 0) : hit.end() + 80]
        raise SystemExit(f"{name} is not self-contained: ...{excerpt}...")


def nav_html(current: str, *, root: str = "") -> str:
    """The navigation bar, with the current page marked."""
    nav = SITE_NAV.read_text(encoding="utf-8")
    nav = nav.replace("{{ROOT}}", root).replace("{{EDITION}}", html.escape(PUBLICATION_EDITION))
    marker = f'data-page="{current}"'
    if marker not in nav:
        raise SystemExit(f"site-nav.html has no entry for {current!r}")
    return nav.replace(marker, f'{marker} aria-current="page"')


def colophon_html() -> str:
    """The closing line every page carries, as the explainer's does."""
    return (
        '<p class="site-colophon">'
        f"{html.escape(SITE_NAME)} · {html.escape(PUBLICATION_EDITION)} · "
        'Formatted and typeset with <a href="https://github.com/jlevy/flowmark">Flowmark</a> '
        'and <a href="https://github.com/jlevy/kpress">KPress</a></p>'
    )


def kpress_page(
    markdown: str,
    *,
    name: str,
    current: str,
    title: str,
    description: str,
    toc: bool,
    rewrite_body: Callable[[str], str] | None = None,
    scripts: Sequence[str] = (),
) -> Page:
    """One standalone kpress page with the site's layer, nav and colophon.

    `scripts` are page programs read from their checked `.js` files, each placed in its own
    script element after the math scripts; no script text is written here.
    """
    from kpress.format.model import DocumentInput, RenderOptions  # noqa: PLC0415
    from kpress.format.render import render_page  # noqa: PLC0415

    canonical = SITE_URL if name == "index.html" else SITE_URL + name
    document = DocumentInput(
        title=title,
        source_text=markdown,
        source_path=name,
        body_markdown=markdown,
        trust_mode="trusted",
        metadata={"description": description, "url": canonical, "site_name": SITE_NAME},
    )
    head, math_scripts = page_assets()
    options = RenderOptions(
        asset_mode="inline",
        asset_policy="none",
        content_card=False,
        show_doc_header=False,
        include_toc="on" if toc else "off",
        head_extra_html=head,
        header_html=nav_html(current),
        footer_html=colophon_html(),
    )
    rendered = render_page(document, options)
    errors = [d for d in rendered.diagnostics if d.get("severity") == "error"]
    if errors:
        raise SystemExit(f"{name}: kpress reported errors: {errors[:3]}")
    prose = 'class="kpress-prose kpress-long-text'
    page = rendered.html.replace(prose + '"', prose + ' site-page"', 1)
    if rewrite_body is not None:
        page = rewrite_body(page)
    programs = "".join(f"\n<script>{script}</script>" for script in scripts)
    page = page.replace("</body>", f"{math_scripts}{programs}\n</body>", 1)
    assert_self_contained(name, page)
    return Page(name, page)


def fill(template: str, values: dict[str, str], *, where: str) -> str:
    """Substitute every `{{NAME}}`; a placeholder left over or a value unused fails."""
    unused = [key for key in values if "{{" + key + "}}" not in template]
    if unused:
        raise SystemExit(f"{where}: values with no placeholder: {', '.join(unused)}")
    for key, value in values.items():
        template = template.replace("{{" + key + "}}", value)
    left = re.findall(r"\{\{[A-Z_]+\}\}", template)
    if left:
        raise SystemExit(f"{where}: unfilled placeholders: {', '.join(sorted(set(left)))}")
    return template


def overview_page() -> Page:
    """The front door: prose from its template, every fact from the record."""
    markdown = fill(
        OVERVIEW_ARTICLE.read_text(encoding="utf-8"),
        {"EDITION": html.escape(PUBLICATION_EDITION)},
        where=OVERVIEW_ARTICLE.name,
    )
    return kpress_page(
        markdown,
        name="index.html",
        current="overview",
        title=SITE_NAME,
        description=OVERVIEW_DESCRIPTION,
        toc=False,
    )


def frontier_page() -> Page:
    """The frontier atlas: one row per case, from its `SquarePackingCase/v2` record."""
    from devtools.render_frontier_page import (  # noqa: PLC0415
        frontier_markdown,
        table_script,
    )

    return kpress_page(
        frontier_markdown(fill, PUBLICATION_EDITION),
        name="frontier.html",
        current="frontier",
        title=f"The Frontier Atlas · {SITE_NAME}",
        description=FRONTIER_DESCRIPTION,
        toc=False,
        scripts=(table_script(),),
    )


#: The pages this renderer owns, by served name.
PAGES: dict[str, Callable[[], Page]] = {
    "index.html": overview_page,
    "frontier.html": frontier_page,
}


def render_all() -> list[Page]:
    """Every page, in a fixed order."""
    return [build() for build in PAGES.values()]


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument(
        "--check",
        action="store_true",
        help="exit non-zero if a page on disk differs from a fresh render",
    )
    args = parser.parse_args(argv)
    output = args.output.resolve()
    pages = render_all()
    if args.check:
        stale = [
            p.name
            for p in pages
            if not (output / p.name).is_file()
            or (output / p.name).read_text(encoding="utf-8") != p.html
        ]
        if stale:
            print(f"stale or missing: {', '.join(stale)}", file=sys.stderr)
            return 1
        print(f"{len(pages)} pages match a fresh render")
        return 0
    output.mkdir(parents=True, exist_ok=True)
    for page in pages:
        (output / page.name).write_text(page.html, encoding="utf-8")
        print(f"wrote {output / page.name} ({len(page.html) // 1024} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
