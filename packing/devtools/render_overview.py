#!/usr/bin/env python3
"""Render the site's own pages: the overview, the frontier atlas and the tutorial.

The published site used to have one top-level page, the n = 11 explainer. This renderer
adds the front door and the pages around it, as the plan in
`docs/project/specs/active/plan-2026-09-29-github-pages-overview.md` lays out:

- `index.html`, the overview: the problem, the headline and recent results and the
  verification statistics, generated from the register;
- `all-results.html`, every registered result in one table, which the overview's cards
  and recent list point into by row (`#t-018`);
- `frontier.html`, the frontier atlas: one row for every case, from its
  `SquarePackingCase/v2` record;
- `cases.html`, the case records: every case's full record at `cases.html#n-N`, which
  the atlas grid and the frontier atlas both open (`render_case_pages`);
- `papers.html`, the Papers section's page: one large card per paper, from the one list
  `overview_sections.PAPERS`. The optimality paper (`n11-optimality/`,
  `render_n11_optimality_explainer`), the explainer (`explainer.html`,
  `render_explainer`) and the tutorial are the section's papers, and the bar's Papers
  entry is current on all four;
- `tutorial.html`, the tutorial rendered as a page;
- `visualize.html`, the Visualize section's first tab: the n = 1 to 324 film at full
  size. Its second tab is the workbench at `workbench/`, which
  `workbench_tools.build_site` builds and gives the same tab bar (`visualize_tabs`).

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
from datetime import datetime
from functools import cache
from pathlib import Path
from typing import Literal, NamedTuple
from urllib.parse import quote

from devtools import repo_links
from devtools.repo_links import repo_url
from sqpack.release import PUBLICATION_EDITION, PUBLICATION_HISTORY

PACKING = Path(__file__).resolve().parents[1]
REPO = PACKING.parent
TEMPLATES = PACKING / "devtools" / "templates"
SITE_CSS = TEMPLATES / "site.css"
#: The result overview's styles, the popover body a result's row opens
#: (`devtools.result_overview`), kept apart from `site.css` and inlined after it.
SITE_RESULT_CSS = TEMPLATES / "site-result.css"
SITE_NAV = TEMPLATES / "site-nav.html"
SITE_NAV_CSS = TEMPLATES / "site-nav.css"
#: The text tokens every page shares with the explainer: its type base, reading measure,
#: heading scale and pinned faces. The explainer's shell inlines the same file.
PAPER_TYPE_CSS = TEMPLATES / "paper-type.css"
OVERVIEW_ARTICLE = TEMPLATES / "overview-article.md"
RESULTS_ARTICLE = TEMPLATES / "all-results-article.md"
VISUALIZE_ARTICLE = TEMPLATES / "visualize-article.md"
PAPERS_ARTICLE = TEMPLATES / "papers-article.md"
BROWSER = PACKING / "devtools" / "overview"
FORWARD_SCRIPT = BROWSER / "forward.js"
TABLE_SCRIPT = BROWSER / "table.js"
MATH_SCRIPT = BROWSER / "math.js"
POPOVER_SCRIPT = BROWSER / "popover.js"
ROW_POPOVER_SCRIPT = BROWSER / "row-popover.js"
ATLAS_GRID_SCRIPT = BROWSER / "atlas-grid.js"
EMBED_SCRIPT = BROWSER / "embed.js"
CASE_POPOVER_SCRIPT = BROWSER / "case-popover.js"
CASE_VIEW_SCRIPT = BROWSER / "case-view.js"
THEME_SCRIPT = BROWSER / "theme.js"
#: The frame the site's flattened kpress client modules are placed in.
KPRESS_CLIENT_FRAME = BROWSER / "kpress-client.js"
#: kpress's client modules a site page carries, in dependency order: the contents rail's
#: scroll-spy and drawer (`toc.js`) and hash-navigation history (`history.js`), with
#: the helpers they import.
KPRESS_CLIENT_MODULES = ("viewport.js", "overlay.js", "runtime.js", "toc.js", "history.js")
KPRESS_CLIENT_API = {"runtime.js": "behaviors", "toc.js": "initKpressToc"}
OUTPUT = PACKING / "site"

SITE_URL = "https://jlevy.github.io/squares/"
SITE_NAME = "Square Packing"
#: Where a reader reports a result the site does not have yet: a new issue on the
#: repository, which the overview's own statement links.
NEW_ISSUE_URL = f"{repo_links.REPO_URL}/issues/new"
OVERVIEW_DESCRIPTION = (
    "Packing unit squares in the smallest square: the problem, every current result, "
    "and how each one is verified."
)
RESULTS_DESCRIPTION = (
    "Every registered result on packing unit squares in the smallest square, this "
    "project's and others', with its significance, verification, confirmation, standing "
    "and records."
)
PAPERS_DESCRIPTION = (
    "The project's papers on packing unit squares in the smallest square: its "
    "explanations and proofs, written out in full."
)
VISUALIZE_DESCRIPTION = (
    "The best packings known of n unit squares, n = 1 to 324, built one square at a "
    "time in an eight-minute film, and a workbench to move the squares yourself."
)
#: The release the films are published on, and the two films on it.
FILM_RELEASE = "v0.4.2"
FILM_RELEASE_URL = f"https://github.com/jlevy/squares/releases/tag/{FILM_RELEASE}"
FILM_URL = (
    f"https://github.com/jlevy/squares/releases/download/{FILM_RELEASE}/"
    "ascent-n1-324-1080p60-citations.mp4"
)
SHORT_FILM_URL = FILM_URL.replace("n1-324", "n1-100")


def film_release_date() -> str:
    """The day `FILM_RELEASE` was first published, as the site writes a date without
    its year: 28 September. The films show the record as it stood that day."""
    entry = next(entry for entry in PUBLICATION_HISTORY if entry.version == FILM_RELEASE)
    day = datetime.strptime(entry.first_published, "%B %d, %Y").date()  # noqa: DTZ007
    return f"{day.day} {day:%B}"


#: The Visualize section's tabs, each its own page: its key, where it is served from the
#: site's root, and its label. The film is the section's first tab and the bar's target.
VISUALIZE_TABS: tuple[tuple[str, str, str], ...] = (
    ("film", "visualize.html", "Film"),
    ("workbench", "workbench/", "Workbench"),
)
FRONTIER_DESCRIPTION = (
    "Every tracked case of packing n unit squares in the smallest square, n = 1 to 324: "
    "the best known packing, the reported and verified bounds, and the records behind them."
)

#: The results table's page. `results.html` is `RESULTS.md` rendered, a reader document,
#: so the table's own page takes this name; its row ids are the results' (`#t-018`).
RESULTS_PAGE = "all-results.html"

#: The repository documents served as pages outside the navigation, reached from the
#: overview's cards; `site_documents` renders them.
DOCUMENT_PAGES: tuple[str, ...] = (
    "readme.html",
    "synopsis.html",
    "results.html",
    "status.html",
    "epistemics.html",
    "conventions.html",
    "development.html",
    "defects.html",
)
#: Every page the published site serves, by path under the site root, whichever build
#: writes it. The navigation bar links only to these, and tests hold it to that.
SITE_PAGES: tuple[str, ...] = (
    "index.html",
    "frontier.html",
    RESULTS_PAGE,
    "cases.html",
    "papers.html",
    "n11-optimality/t-060-explainer.html",
    "explainer.html",
    "tutorial.html",
    "visualize.html",
    "workbench/index.html",
    *DOCUMENT_PAGES,
)

#: Every file a render reads beside the record `overview_data.INPUTS` names; `inputs()`
#: is the two together. The Pages workflow's deploy filter and the scope tool are checked
#: against that, so a page cannot go stale because an input moved unseen. The record is
#: read through `sqpack`'s loaders and the pages are kpress pages, so the package, the
#: vendored kpress and the locked environment are inputs, as they are the explainer's.
RENDER_INPUTS: tuple[Path, ...] = (
    Path(__file__).resolve(),
    SITE_CSS,
    SITE_RESULT_CSS,
    SITE_NAV,
    SITE_NAV_CSS,
    PAPER_TYPE_CSS,
    OVERVIEW_ARTICLE,
    RESULTS_ARTICLE,
    VISUALIZE_ARTICLE,
    PAPERS_ARTICLE,
    BROWSER,
    PACKING / "src" / "sqpack",
    PACKING / "devtools" / "site_documents.py",
    PACKING / "devtools" / "result_overview.py",
    REPO / repo_links.TUTORIAL,
    REPO / repo_links.README,
    REPO / repo_links.SYNOPSIS,
    REPO / repo_links.CONVENTIONS,
    REPO / repo_links.DEVELOPMENT,
    REPO / repo_links.DEFECTS,
    PACKING / "devtools" / "repo_links.py",
    REPO / "vendor" / "kpress",
    PACKING / "pyproject.toml",
    PACKING / "uv.lock",
)

# The same refusal the explainer makes: a script or stylesheet with a source, a CSS
# import, or a url() or `<link>` that is not a data URI or a fragment is a fetch.
_EXTERNAL_REFERENCE = re.compile(
    r"<script[^>]*\ssrc="
    r'|<link(?![^>]*\srel="canonical")(?![^>]*\shref="data:)[^>]*\shref='
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
    from devtools.render_case_pages import CASES_INPUTS  # noqa: PLC0415
    from devtools.render_frontier_page import FRONTIER_INPUTS  # noqa: PLC0415

    return tuple(
        dict.fromkeys(
            (
                *RENDER_INPUTS,
                *overview_data.INPUTS,
                *FRONTIER_INPUTS,
                *CASES_INPUTS,
            )
        )
    )


class Page(NamedTuple):
    """One rendered page: where it is served and its bytes."""

    name: str
    html: str


def page_assets() -> tuple[str, str]:
    """The explainer's own inlined assets: head styles and the math pipeline.

    The stylesheets are the explainer's (`kpress_css`, `katex_css`, `relation_face_css`),
    faces already inlined as data URIs, so a reader moving between the explainer and
    these pages sees one design system; `paper-type.css`, the text tokens the explainer
    also carries, follows them. The script is the explainer's math pipeline,
    `render_explainer.katex_js`: KaTeX, kpress's metric tables and shared runtime, and
    the explainer's host adapter (`squaresMath`), without kpress's auto-render entry
    point and its whole-page synchronous pass. `overview/math.js`, which `kpress_page`
    places after it, drives the adapter over kpress's own math markup. The pipeline is
    described in `templates/paper-design.md`, under Math Loading.
    """
    from devtools.render_explainer import (  # noqa: PLC0415
        katex_css,
        katex_js,
        kpress_css,
        kpress_static,
        relation_face_css,
    )

    static = kpress_static()
    head = (
        f"<style>{kpress_css(static)}{katex_css(static)}</style>\n"
        f"<style>{relation_face_css(static)}</style>\n"
        f"<style>{PAPER_TYPE_CSS.read_text(encoding='utf-8')}</style>\n"
        f"<style>{SITE_NAV_CSS.read_text(encoding='utf-8')}</style>\n"
        f"<style>{SITE_CSS.read_text(encoding='utf-8')}</style>\n"
        f"<style>{SITE_RESULT_CSS.read_text(encoding='utf-8')}</style>"
    )
    return head, f"<script>{katex_js(static)}</script>"


def assert_self_contained(name: str, page: str) -> None:
    """Refuse a page that would fetch anything to be drawn: a script or stylesheet with
    a source, a CSS import, or a `url()` or `<link>` that is not a data URI or a
    fragment. What a reader opens afterwards is fetched then, from the site itself: a
    page a card's popover frames, and a result's overview (`result_fragments`)."""
    hit = _EXTERNAL_REFERENCE.search(page)
    if hit:
        excerpt = page[max(hit.start() - 60, 0) : hit.end() + 80]
        raise SystemExit(f"{name} is not self-contained: ...{excerpt}...")


def nav_html(current: str, *, root: str = "") -> str:
    """The navigation bar, with the current page marked."""
    nav = SITE_NAV.read_text(encoding="utf-8")
    nav = nav.replace("{{ROOT}}", root).replace("{{LOGO}}", site_logo())
    marker = f'data-page="{current}"'
    if marker not in nav:
        raise SystemExit(f"site-nav.html has no entry for {current!r}")
    return nav.replace(marker, f'{marker} aria-current="page"')


class NavShell(NamedTuple):
    """The navigation bar for a page kpress does not render, in the three places it goes.

    `head` opens the page's `<head>`: kpress's pre-paint theme bootstrap, kpress's design
    tokens with the one face the bar is set in, the text tokens every page shares
    (`paper-type.css`), and `site-nav.css`. `header` is the bar
    in the shell `site-nav.css` gives an application page, for the start of `<body>`,
    with the page's section tabs after the bar when it has them.
    `script` is the gear's program, `overview/theme.js`, for the end of `<body>`.
    """

    head: str
    header: str
    script: str


#: The face the bar is set in, the one `@font-face` of kpress's tokens an application page
#: needs: `--kpress-font-sans` leads with it.
_NAV_FACE = re.compile(r'font-family:\s*"Source Sans 3 Variable";\s*font-style:\s*normal;')


def nav_shell(current: str, *, root: str, tabs: str = "") -> NavShell:
    """The site's navigation bar, gear included, for an application page: the workbench.

    The same partial, stylesheet and theme program every kpress page carries, with the
    theme bootstrap kpress's standalone page runs before first paint, so the bar sits
    where it does on every page and one stored choice, `kpress.theme`, drives the theme
    on all of them. kpress's tokens come whole but for their faces, of which only the
    bar's own is kept and inlined; the page's own stylesheet, placed after them, keeps
    any of its own custom properties the tokens also name. `tabs`, a section's tab bar
    (`visualize_tabs`), follows the bar in the header, as on a kpress page.
    """
    from devtools.render_explainer import (  # noqa: PLC0415
        FONT_FACE_BLOCK,
        inline_font_urls,
        kpress_static,
        theme_bootstrap,
    )

    static = kpress_static()
    tokens = (static / "css" / "style-tokens.css").read_text(encoding="utf-8")
    tokens = FONT_FACE_BLOCK.sub(
        lambda match: match.group(0) if _NAV_FACE.search(match.group(0)) else "", tokens
    )
    if not _NAV_FACE.search(tokens):
        raise SystemExit("kpress's style-tokens.css no longer declares the bar's face")
    tokens = inline_font_urls(tokens, static / "css")
    head = (
        f"{favicon_html()}\n"
        f"<script>{theme_bootstrap(static)}</script>\n"
        f"<style>{tokens}</style>\n"
        f"<style>{PAPER_TYPE_CSS.read_text(encoding='utf-8')}</style>\n"
        f"<style>{SITE_NAV_CSS.read_text(encoding='utf-8')}</style>"
    )
    header = (
        '<div class="site-app-shell">\n<header class="kpress-site-header">\n'
        f"{nav_html(current, root=root)}{tabs}</header>\n</div>"
    )
    return NavShell(head, header, f"<script>{_script_text(THEME_SCRIPT)}</script>")


def visualize_tabs(current: str, *, root: str = "") -> str:
    """The Visualize section's tab bar, with the current tab marked.

    Each tab is a real link to its own page, so the bar needs no script and a tab can be
    opened, bookmarked and shared. Its look is `.site-tabs` in `site-nav.css`, the one
    stylesheet both the film's page and the workbench carry.
    """
    if current not in {key for key, _, _ in VISUALIZE_TABS}:
        raise SystemExit(f"the Visualize section has no tab {current!r}")
    links = "".join(
        f'<a data-tab="{key}"{' aria-current="page"' if key == current else ""} '
        f'href="{root}{href}">{html.escape(label)}</a>'
        for key, href, label in VISUALIZE_TABS
    )
    return f'<nav class="site-tabs" aria-label="Visualize">{links}</nav>'


#: The logo's size in the bar and the icon's in a tab, in CSS pixels: whole pixels, so
#: each drawing's one-pixel frame (`packing_svg(frame_px=)`) lands on the pixel grid.
#: `site-nav.css` sets the logo to the same size.
SITE_LOGO_PX = 18
FAVICON_PX = 16


@cache
def site_logo() -> str:
    """The site's mark beside its name in the bar: case 11, the drawing the tab's icon
    is, in the bar's own ink so it turns over with the theme."""
    from devtools.render_frontier_page import packing_svg  # noqa: PLC0415

    svg = packing_svg(11, units=200, frame_px=SITE_LOGO_PX)
    return svg.replace("<svg ", '<svg class="site-logo" ', 1)


@cache
def favicon_html() -> str:
    """The site's icon: case 11, Trump's packing of eleven squares, drawn small as a
    data URI, so it costs no fetch. It names its ink and paper, since a tab has no page
    colour to inherit."""
    from devtools.render_frontier_page import packing_svg  # noqa: PLC0415

    svg = packing_svg(11, units=200, ink="#17202a", paper="#ffffff", frame_px=FAVICON_PX)
    svg = svg.replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" ', 1)
    return f'<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,{quote(svg)}">'


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
    toc: bool | Literal["auto"],
    rewrite_body: Callable[[str], str] | None = None,
    page_scripts: Sequence[Path] = (),
    trust_mode: Literal["trusted", "sanitized"] = "trusted",
    strict_anchors: bool = False,
    tabs: str = "",
) -> Page:
    """One standalone kpress page with the site's layer, nav and colophon.

    `tabs`, a section's tab bar (`visualize_tabs`), follows the navigation bar in the
    header slot, where the workbench's shell also puts it, so it sits in one place on
    every page of its section.

    `page_scripts` are page programs in checked `.js` files, each placed in its own
    script element after the math scripts and the navigation bar's theme control
    (`overview/theme.js`); no script text is written here.
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
        include_toc="auto" if toc == "auto" else "on" if toc else "off",
        head_extra_html=(
            f"{favicon_html()}{head}<script>{_script_text(EMBED_SCRIPT)}</script>"
        ),
        header_html=nav_html(current) + tabs,
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
    page = _document_scrolls(name, page)
    if rewrite_body is not None:
        page = rewrite_body(page)
    programs = f"\n{kpress_client_script()}" + "".join(
        f"\n<script>{_script_text(path)}</script>"
        for path in (THEME_SCRIPT, MATH_SCRIPT, *page_scripts)
    )
    page = page.replace("</body>", f"{math_scripts}{programs}\n</body>", 1)
    assert_self_contained(name, page)
    return Page(name, page)


#: kpress's standalone shell marks `<main>` as the pane the document scrolls in.
_MAIN_VIEWPORT = '<main class="kpress-page-main kpress-viewport" data-kpress-viewport>'


def _document_scrolls(name: str, page: str) -> str:
    """Name the document as kpress's viewport, as the explainer's shell does.

    `site.css` lets a site page scroll the document rather than `<main>`, so the
    navigation bar can stick, and kpress has to be told: its scroll-spy observes and
    listens on the element marked `data-kpress-viewport`, and with `<main>` still marked
    it watched a pane that never scrolls and the contents rail never followed the
    reader. Its popovers place themselves against the same element.
    """
    if page.count(_MAIN_VIEWPORT) != 1 or page.count("<html ") != 1:
        raise SystemExit(f"{name}: kpress's shell no longer marks <main> as its viewport")
    page = page.replace(
        _MAIN_VIEWPORT, _MAIN_VIEWPORT.removesuffix(" data-kpress-viewport>") + ">"
    )
    return page.replace("<html ", "<html data-kpress-viewport ", 1)


def kpress_client_script() -> str:
    """kpress's contents-rail and history modules as one classic script element.

    Flattened by the explainer's checked flattener, since an inline module would fetch
    its siblings at view time; see `render_explainer.kpress_client_js`.
    """
    from devtools.render_explainer import kpress_client_js, kpress_static  # noqa: PLC0415

    script = kpress_client_js(
        kpress_static(),
        modules=KPRESS_CLIENT_MODULES,
        api=KPRESS_CLIENT_API,
        frame=KPRESS_CLIENT_FRAME,
    )
    return f"<script>{script}</script>"


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
    """The front door: prose from its template, every fact from the record.

    Its first section opens with README's first paragraph and its Recent Results with
    README's next two, read from README's `project-intro` and `recent-progress` blocks
    and their links rewritten for the site (`site_documents`).
    """
    from devtools import overview_data, overview_sections, site_documents  # noqa: PLC0415

    overview = overview_data.load()
    values = {
        "HERO": overview_sections.hero(),
        "README_INTRO": site_documents.overview_intro(),
        "README_PROGRESS": site_documents.overview_progress(),
        "NEW_ISSUE_URL": NEW_ISSUE_URL,
        "DOCUMENT_CARDS": overview_sections.document_cards(),
        "OTHER_PROJECTS": overview_sections.other_project_cards(),
        "ATLAS_GRID": overview_sections.atlas_grid(),
        "ATLAS_CARDS": overview_sections.atlas_cards(),
        "PAGE_CARDS": overview_sections.page_cards(),
        "VERIFICATION": overview_sections.verification_block(),
        "RECENT": overview_sections.recent_table(overview),
        "STAR_LEGEND": overview_sections.star_legend(),
        "AWAITING_REPLAY": overview_sections.awaiting_replay(overview),
        "SURVEY_COUNTS": overview_sections.survey_counts(overview),
        "ARROW_RIGHT": overview_sections.arrow_icon("right"),
    }
    markdown = fill(
        OVERVIEW_ARTICLE.read_text(encoding="utf-8"), values, where=OVERVIEW_ARTICLE.name
    )
    # The prose names a repository file as `repo:PATH`, which becomes its link on `main`
    # through the one helper every page links the repository with (`repo_links`).
    markdown = re.sub(
        r'(\]\(|href=")repo:([^)"\s#]+)',
        lambda match: match[1] + repo_url(match[2]),
        markdown,
    )
    return kpress_page(
        markdown,
        name="index.html",
        current="overview",
        title=SITE_NAME,
        description=OVERVIEW_DESCRIPTION,
        toc=False,
        rewrite_body=site_documents.rewrite_overview_blocks,
        page_scripts=(
            FORWARD_SCRIPT,
            TABLE_SCRIPT,
            POPOVER_SCRIPT,
            ROW_POPOVER_SCRIPT,
            ATLAS_GRID_SCRIPT,
        ),
    )


def results_page() -> Page:
    """Every registered result, one row each at its own id, sortable and filterable."""
    from devtools import overview_data, overview_sections  # noqa: PLC0415

    overview = overview_data.load()
    values = {
        "COUNT": str(len(overview.results)),
        "EPISTEMICS_URL": repo_url(repo_links.EPISTEMICS),
        "RESULTS_TABLE": overview_sections.results_table(overview),
        "STAR_LEGEND": overview_sections.star_legend(),
    }
    markdown = fill(
        RESULTS_ARTICLE.read_text(encoding="utf-8"), values, where=RESULTS_ARTICLE.name
    )
    return kpress_page(
        markdown,
        name=RESULTS_PAGE,
        current="results",
        title=f"Every Result · {SITE_NAME}",
        description=RESULTS_DESCRIPTION,
        toc=False,
        page_scripts=(TABLE_SCRIPT, POPOVER_SCRIPT, ROW_POPOVER_SCRIPT),
    )


def papers_page() -> Page:
    """The Papers section's page: a short introduction and one large card per paper,
    each opening a popover that frames the paper and expands to it."""
    from devtools import overview_sections  # noqa: PLC0415

    values = {"PAPER_CARDS": overview_sections.paper_cards()}
    markdown = fill(
        PAPERS_ARTICLE.read_text(encoding="utf-8"), values, where=PAPERS_ARTICLE.name
    )
    return kpress_page(
        markdown,
        name="papers.html",
        current="papers",
        title=f"Papers · {SITE_NAME}",
        description=PAPERS_DESCRIPTION,
        toc=False,
        page_scripts=(POPOVER_SCRIPT,),
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
        page_scripts=(TABLE_SCRIPT, POPOVER_SCRIPT, CASE_POPOVER_SCRIPT, ROW_POPOVER_SCRIPT),
    )


def cases_page() -> Page:
    """Every case's record, one page, one address per case (`cases.html#n-11`)."""
    from devtools.render_case_pages import cases_page as build  # noqa: PLC0415

    return build()


def visualize_page() -> Page:
    """The Visualize section's first tab: the film of the ascent at full size."""
    values = {
        "FILM_URL": FILM_URL,
        "SHORT_FILM_URL": SHORT_FILM_URL,
        "RELEASE_URL": FILM_RELEASE_URL,
        "RELEASE": FILM_RELEASE,
        "RELEASE_DATE": film_release_date(),
    }
    markdown = fill(
        VISUALIZE_ARTICLE.read_text(encoding="utf-8"), values, where=VISUALIZE_ARTICLE.name
    )
    return kpress_page(
        markdown,
        name="visualize.html",
        current="visualize",
        title=f"Visualize · {SITE_NAME}",
        description=VISUALIZE_DESCRIPTION,
        toc=False,
        tabs=visualize_tabs("film"),
    )


def _document_page(name: str) -> Callable[[], Page]:
    def build() -> Page:
        from devtools.site_documents import document_page  # noqa: PLC0415

        return document_page(name)

    return build


#: The pages this renderer owns, by served name.
PAGES: dict[str, Callable[[], Page]] = {
    "index.html": overview_page,
    "frontier.html": frontier_page,
    RESULTS_PAGE: results_page,
    "cases.html": cases_page,
    "papers.html": papers_page,
    "tutorial.html": tutorial_page,
    "visualize.html": visualize_page,
    **{name: _document_page(name) for name in DOCUMENT_PAGES},
}


def render_all() -> list[Page]:
    """Every page, in a fixed order."""
    return [build() for build in PAGES.values()]


def result_fragments() -> list[Page]:
    """Each registered result's overview, in the register's order, as the file its row's
    popover fetches (`overview_sections.result_fragment`).

    A fragment is not a page: it is one `.site-result` block and nothing else, with no
    shell, styles or scripts of its own, placed by `overview/row-popover.js` into the
    popover of a page that has them. The overviews are 2.8 MB between them and two pages
    list every result, so they are written once, here, rather than into either page.
    """
    from devtools import overview_data, overview_sections  # noqa: PLC0415

    overview = overview_data.load()
    return [
        Page(
            overview_sections.result_fragment(result.id),
            overview_sections.result_row_popover_body(result, overview) + "\n",
        )
        for result in overview.results
    ]


def render_site() -> list[Page]:
    """Every file this module writes: the pages, then the result fragments."""
    return [*render_all(), *result_fragments()]


def write_site(output: Path, files: Sequence[Page]) -> None:
    """Write `files` under `output`, and drop any result fragment already there that is
    not among them, so a directory built before a result was withdrawn does not keep
    serving it."""
    from devtools.overview_sections import RESULT_FRAGMENTS  # noqa: PLC0415

    output.mkdir(parents=True, exist_ok=True)
    kept = {output / file.name for file in files}
    for stale in sorted((output / RESULT_FRAGMENTS).glob("*.html")):
        if stale not in kept:
            stale.unlink()
    for file in files:
        target = output / file.name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(file.html, encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument(
        "--check",
        action="store_true",
        help="exit non-zero if a file on disk differs from a fresh render",
    )
    args = parser.parse_args(argv)
    output = args.output.resolve()
    pages = render_all()
    fragments = result_fragments()
    if args.check:
        stale = [
            p.name
            for p in (*pages, *fragments)
            if not (output / p.name).is_file()
            or (output / p.name).read_text(encoding="utf-8") != p.html
        ]
        if stale:
            print(f"stale or missing: {', '.join(stale)}", file=sys.stderr)
            return 1
        print(f"{len(pages)} pages and {len(fragments)} result overviews match a fresh render")
        return 0
    write_site(output, [*pages, *fragments])
    for page in pages:
        print(f"wrote {output / page.name} ({len(page.html) // 1024} KB)")
    total = sum(len(fragment.html.encode("utf-8")) for fragment in fragments)
    places = sorted({(output / fragment.name).parent for fragment in fragments})
    print(
        f"wrote {len(fragments)} result overviews under "
        f"{', '.join(f'{place}/' for place in places)} ({total // 1024} KB in all)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
