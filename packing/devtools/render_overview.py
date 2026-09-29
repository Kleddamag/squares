#!/usr/bin/env python3
"""Render the site's own pages: the overview, the frontier atlas and the tutorial.

The published site used to have one top-level page, the n = 11 explainer. This renderer
adds the front door and the pages around it, as the plan in
`docs/project/specs/active/plan-2026-09-29-github-pages-overview.md` lays out:

- `index.html`, the overview: the problem, the headline results, the results table and
  the verification statistics, generated from the register;
- `frontier.html`, the frontier atlas: one row for every case, from its
  `SquarePackingCase/v2` record;
- `tutorial.html`, the tutorial rendered as a page.

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
from typing import Literal, NamedTuple

from sqpack.release import PUBLICATION_EDITION

PACKING = Path(__file__).resolve().parents[1]
REPO = PACKING.parent
TEMPLATES = PACKING / "devtools" / "templates"
SITE_CSS = TEMPLATES / "site.css"
SITE_NAV = TEMPLATES / "site-nav.html"
SITE_NAV_CSS = TEMPLATES / "site-nav.css"
OVERVIEW_ARTICLE = TEMPLATES / "overview-article.md"
BROWSER = PACKING / "devtools" / "overview"
FORWARD_SCRIPT = BROWSER / "forward.js"
TABLE_SCRIPT = BROWSER / "table.js"
MATH_RETRY_SCRIPT = BROWSER / "math-retry.js"
POPOVER_SCRIPT = BROWSER / "popover.js"
OUTPUT = PACKING / "site"

SITE_URL = "https://jlevy.github.io/squares/"
REPO_URL = "https://github.com/jlevy/squares"
SITE_NAME = "Square Packing"
OVERVIEW_DESCRIPTION = (
    "Packing unit squares in the smallest square: the problem, every current result, "
    "and how each one is verified."
)
FRONTIER_DESCRIPTION = (
    "Every tracked case of packing n unit squares in the smallest square, n = 1 to 324: "
    "the best known packing, the reported and verified bounds, and the records behind them."
)

#: Every page the published site serves, by path under the site root, whichever build
#: writes it. The navigation bar links only to these, and tests hold it to that.
SITE_PAGES: tuple[str, ...] = (
    "index.html",
    "frontier.html",
    "explainer.html",
    "tutorial.html",
    "workbench/index.html",
)

#: Every file a render reads beside the record `overview_data.INPUTS` names; `inputs()`
#: is the two together. The Pages workflow's deploy filter and the scope tool are checked
#: against that, so a page cannot go stale because an input moved unseen. The record is
#: read through `sqpack`'s loaders and the pages are kpress pages, so the package, the
#: vendored kpress and the locked environment are inputs, as they are the explainer's.
RENDER_INPUTS: tuple[Path, ...] = (
    Path(__file__).resolve(),
    SITE_CSS,
    SITE_NAV,
    SITE_NAV_CSS,
    OVERVIEW_ARTICLE,
    BROWSER,
    PACKING / "src" / "sqpack",
    PACKING / "devtools" / "site_documents.py",
    REPO / "TUTORIAL.md",
    REPO / "vendor" / "kpress",
    PACKING / "pyproject.toml",
    PACKING / "uv.lock",
)

# The same refusal the explainer makes: a script or stylesheet with a source, a CSS
# import, or a url() that is not a data URI or a fragment is a fetch.
_EXTERNAL_REFERENCE = re.compile(
    r"<script[^>]*\ssrc="
    r'|<link(?![^>]*\srel="canonical")[^>]*\shref='
    r"|@import\b"
    r"""|url\(\s*(?!["']?(?:data:|#))"""
)


def canonical_url(name: str) -> str:
    """A served page's canonical URL: the site's root for the overview, else its name."""
    return SITE_URL if name == "index.html" else SITE_URL + name


def inputs() -> tuple[Path, ...]:
    """Every file any page this module renders reads: its own inputs and the record's.

    The page modules are imported here rather than at the top because
    `render_frontier_page` reads `render_explainer`, which imports this module.
    """
    from devtools import overview_data  # noqa: PLC0415
    from devtools.render_frontier_page import FRONTIER_INPUTS  # noqa: PLC0415

    return tuple(dict.fromkeys((*RENDER_INPUTS, *overview_data.INPUTS, *FRONTIER_INPUTS)))


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
        f"<style>{SITE_NAV_CSS.read_text(encoding='utf-8')}</style>\n"
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
    nav = nav.replace("{{ROOT}}", root)
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
    page_scripts: Sequence[Path] = (),
    trust_mode: Literal["trusted", "sanitized"] = "trusted",
    strict_anchors: bool = False,
) -> Page:
    """One standalone kpress page with the site's layer, nav and colophon.

    `page_scripts` are page programs in checked `.js` files, each placed in its own
    script element after the math scripts; no script text is written here.
    `strict_anchors` raises kpress's `broken_anchor` warning, an in-page `#…` link
    with no target, to a failure; the reader documents are rendered that way.
    """
    from kpress.format.model import DocumentInput, RenderOptions  # noqa: PLC0415
    from kpress.format.render import render_page  # noqa: PLC0415

    canonical = canonical_url(name)
    document = DocumentInput(
        title=title,
        source_text=markdown,
        source_path=name,
        body_markdown=markdown,
        trust_mode=trust_mode,
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
    errors = [
        d
        for d in rendered.diagnostics
        if d.get("severity") == "error" or (strict_anchors and d.get("type") == "broken_anchor")
    ]
    if errors:
        raise SystemExit(f"{name}: kpress reported errors: {errors[:3]}")
    prose = 'class="kpress-prose kpress-long-text'
    page = rendered.html.replace(prose + '"', prose + ' site-page"', 1)
    if rewrite_body is not None:
        page = rewrite_body(page)
    programs = "".join(
        f"\n<script>{_script_text(path)}</script>"
        for path in (MATH_RETRY_SCRIPT, *page_scripts)
    )
    page = page.replace("</body>", f"{math_scripts}{programs}\n</body>", 1)
    assert_self_contained(name, page)
    return Page(name, page)


def _script_text(path: Path) -> str:
    """A page program's text, refused if it would close its own script element early."""
    script = path.read_text(encoding="utf-8")
    if "</script" in script.lower():
        raise SystemExit(f"{path.name} contains a closing script tag")
    return script


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
    from devtools import overview_data, overview_sections  # noqa: PLC0415
    from devtools.render_explainer import repo_file  # noqa: PLC0415

    overview = overview_data.load()
    stats = overview_data.stats(overview)
    values = {
        "EPISTEMICS_URL": repo_file(REPO / "epistemics.md"),
        "DOCUMENT_CARDS": overview_sections.document_cards(),
        "PAGE_CARDS": overview_sections.page_cards(),
        **overview_sections.bracket_11(overview),
        "HEADLINE_CARDS": overview_sections.headline_cards(overview),
        "EXACT_CARDS": overview_sections.exact_value_cards(overview),
        "RESULTS_TABLE": overview_sections.results_table(overview),
        "VERIFICATION": overview_sections.verification_block(stats),
        "RECENT": overview_sections.recent_list(overview),
    }
    values.pop("S11_LOWER_DECIMAL")
    markdown = fill(
        OVERVIEW_ARTICLE.read_text(encoding="utf-8"), values, where=OVERVIEW_ARTICLE.name
    )
    return kpress_page(
        markdown,
        name="index.html",
        current="overview",
        title=SITE_NAME,
        description=OVERVIEW_DESCRIPTION,
        toc=False,
        page_scripts=(FORWARD_SCRIPT, TABLE_SCRIPT, POPOVER_SCRIPT),
    )


def tutorial_page() -> Page:
    """`TUTORIAL.md` as a page; `site_documents` rewrites and checks its links."""
    from devtools.site_documents import tutorial_page as build  # noqa: PLC0415

    return build()


def frontier_page() -> Page:
    """The frontier atlas: one row per case, from its `SquarePackingCase/v2` record."""
    from devtools.render_frontier_page import frontier_markdown  # noqa: PLC0415

    return kpress_page(
        frontier_markdown(fill),
        name="frontier.html",
        current="frontier",
        title=f"The Frontier Atlas · {SITE_NAME}",
        description=FRONTIER_DESCRIPTION,
        toc=False,
        page_scripts=(TABLE_SCRIPT,),
    )


#: The pages this renderer owns, by served name.
PAGES: dict[str, Callable[[], Page]] = {
    "index.html": overview_page,
    "frontier.html": frontier_page,
    "tutorial.html": tutorial_page,
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
