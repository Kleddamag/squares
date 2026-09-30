#!/usr/bin/env python3
"""Render the published site's own pages: the overview, the frontier atlas and the tutorial.

The site at `https://jlevy.github.io/squares/` opens on the overview, which says what the
problem is, what this project and others have proved, how far each result is verified,
and where every other page and document is. The explainer is rendered separately, by
`devtools.render_explainer`, and moves to `/explainer.html` when the Pages workflow
assembles the site.

**One registry, one module per part.** The pages come from `PAGE_MODULES` and the files
served beside them from `ASSET_MODULES`. Each module exposes `RENDER_INPUTS`, the
repository paths it reads, and `pages()` or `assets()`. This module owns only what they
share: the shell, the navigation bar, the footer, the kpress rendering of Markdown, and
the output. The typography, the math and the client behaviours are the explainer's own,
reached through its helpers, so a reader moving between the explainer and these pages
sees one publication.

**Its own output directory.** The explainer writes `packing/site/index.html`, and its PDF
build reads it there, so these pages go to `packing/site-overview/` and never overwrite
it; the Pages workflow's `publish` job and `devtools.preview_site` assemble the site from
the builders' directories. `--output` refuses the explainer's directory for that reason.

**Deterministic at a commit.** A render reads the checkout and the commit its repository
links name, and nothing else, so two renders of one commit are byte-identical; `--check`
compares a fresh render with the files on disk.

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m devtools.render_overview
    uv run --frozen --all-extras --group dev python -m devtools.render_overview --check
"""

from __future__ import annotations

import argparse
import base64
import json
import re
import sys
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from functools import cache
from html import escape
from pathlib import Path
from types import ModuleType

from strif import atomic_output_file

from devtools import overview_media, overview_page, render_explainer, site_kit, site_pages
from devtools.site_kit import SITE_NAME, SITE_URL, Asset, Page, base_for, nav_html
from sqpack.release import DATA_REVISION, PUBLICATION_EDITION

PACKING = render_explainer.PACKING
REPO = render_explainer.REPO
OUTPUT = PACKING / "site-overview"
EXPLAINER_OUTPUT = render_explainer.OUTPUT.parent
TEMPLATES = site_kit.TEMPLATES
SHELL = TEMPLATES / "site-shell.html"
SITE_CSS = TEMPLATES / "site.css"
SITE_NAV_CSS = render_explainer.SITE_NAV_CSS
REPO_URL = site_kit.REPO_URL

#: The parts of the site, each a module with `RENDER_INPUTS` and `pages()` or `assets()`.
PAGE_MODULES: tuple[ModuleType, ...] = (overview_page, site_pages)
ASSET_MODULES: tuple[ModuleType, ...] = (overview_media,)

#: The explainer's math scripts, which every site page carries so that its math is set
#: exactly as the explainer's is: the metrics switch before paint, the reservation that
#: holds each formula's box while KaTeX loads, and the pass that finishes it.
MATH_SCRIPTS = {
    key: render_explainer.INLINE_SCRIPT_ASSETS[key]
    for key in ("NATIVE_MATH_METRICS", "RESERVE_MATH", "FINISH_MATH")
}
KPRESS_CLIENT = render_explainer.INLINE_SCRIPT_ASSETS["KPRESS_CLIENT_SCRIPT"]
#: The explainer's kpress client modules plus the contents rail's, which the tutorial's
#: long page needs below kpress's wide breakpoint, where the rail becomes a toggled panel.
#: It follows the modules it imports from (overlay, runtime, viewport).
KPRESS_MODULES = (*render_explainer.KPRESS_MODULES, "toc.js")
#: The site pages' own classic scripts, checked by the browser floor under
#: `tsconfig.overview.json`. `site-math.js` typesets every formula through the runtime above.
SCRIPTS = Path(__file__).with_name("overview")
SITE_MATH = SCRIPTS / "site-math.js"

CARD = render_explainer.COMPOSITE_CARD
#: The one `<link>` besides the canonical one a page may carry: its favicon, inlined as a
#: data URI so the page still fetches nothing at view time.
_ICON_LINK = re.compile(r'<link rel="icon" href="data:image/svg\+xml;base64,[A-Za-z0-9+/=]+">')

#: Every repository path a render reads, repository-relative when printed. The Pages
#: workflow republishes on a change to any of them, and a test holds its `paths:` filter to
#: this list, as `test_the_pages_filter_covers_every_render_input` does for the explainer.
SKELETON_INPUTS: tuple[Path, ...] = (
    Path(__file__),
    Path(site_kit.__file__),
    Path(render_explainer.__file__),
    SHELL,
    site_kit.NAV_TEMPLATE,
    SITE_CSS,
    SITE_NAV_CSS,
    *MATH_SCRIPTS.values(),
    KPRESS_CLIENT,
    SCRIPTS,
    render_explainer.PROBES,
    CARD,
    TEMPLATES / "fonts",
    REPO / "vendor" / "kpress",
    PACKING / "src" / "sqpack",
    PACKING / "pyproject.toml",
    PACKING / "uv.lock",
)
RENDER_INPUTS: tuple[Path, ...] = tuple(
    dict.fromkeys(
        (
            *SKELETON_INPUTS,
            *(
                path
                for module in (*PAGE_MODULES, *ASSET_MODULES)
                for path in module.RENDER_INPUTS
            ),
        )
    )
)


@dataclass(frozen=True)
class ShellAssets:
    """The inlined CSS and scripts every page shares, computed once per render."""

    kpress_css: str
    relation_css: str
    site_css: str
    theme_bootstrap: str
    katex_js: str
    kpress_client: str
    math_scripts: Mapping[str, str]
    site_math: str
    icon_sprite: str
    favicon_href: str


@cache
def shell_assets() -> ShellAssets:
    static = render_explainer.kpress_static()
    return ShellAssets(
        kpress_css=render_explainer.kpress_css(static) + render_explainer.katex_css(static),
        relation_css=render_explainer.relation_face_css(static),
        site_css=SITE_NAV_CSS.read_text(encoding="utf-8")
        + "\n"
        + SITE_CSS.read_text(encoding="utf-8"),
        theme_bootstrap=render_explainer.theme_bootstrap(static),
        katex_js=render_explainer.katex_js(static),
        kpress_client=render_explainer.kpress_client_js(static, KPRESS_MODULES),
        math_scripts={
            key: path.read_text(encoding="utf-8") for key, path in MATH_SCRIPTS.items()
        },
        site_math=SITE_MATH.read_text(encoding="utf-8"),
        icon_sprite=render_explainer.icon_sprite(static),
        favicon_href="data:image/svg+xml;base64,"
        + base64.b64encode(overview_media.favicon_svg().encode("utf-8")).decode("ascii"),
    )


def markdown_html(source: str, *, title: str, where: str) -> str:
    """Render one page's Markdown with kpress, as the explainer renders its article.

    Trusted mode, because the templates are this repository's own and carry raw
    `<figure>`, `<div class>` and `<span class>` blocks; math is `auto`, so `$…$` and
    `$$…$$` are typeset by KaTeX with the explainer's math faces. A diagnostic of error
    severity refuses the page rather than publishing a half-rendered one, and so do the
    two kpress rates as warnings that would still publish a broken page: an in-page link
    to an id the page lacks, and a formula KaTeX cannot typeset
    (`site_pages.REFUSED_DIAGNOSTICS`).
    """
    from kpress.format.markdown import parse_markdown  # noqa: PLC0415

    document = parse_markdown(
        render_explainer.kerned_math_spans(source),
        title=title,
        trust_mode="trusted",
        math="auto",
    )
    for diagnostic in document.diagnostics:
        print(f"{where}: {diagnostic.severity}: {diagnostic.message}", file=sys.stderr)
    if any(
        d.severity == "error" or d.type in site_pages.REFUSED_DIAGNOSTICS
        for d in document.diagnostics
    ):
        raise SystemExit(f"{where} did not render cleanly; refusing to write the page")
    return document.html


def canonical_url(path: str) -> str:
    """The page's deployed address: the site root for `index.html`, else the path under it."""
    if path == "index.html":
        return SITE_URL
    if path.endswith("/index.html"):
        return SITE_URL + path.removesuffix("index.html")
    return SITE_URL + path


def footer_html(commit: str) -> str:
    """Edition, data revision, build commit and licence, on every page."""
    return (
        '<footer class="site-footer">\n'
        f"<p>{escape(SITE_NAME)} · edition "
        f'<span class="site-edition">{escape(PUBLICATION_EDITION)}</span>'
        f' · data <code class="site-data-revision">{escape(DATA_REVISION[:12])}</code>'
        f' · built from <a href="{REPO_URL}/commit/{commit}"><code>{commit[:12]}</code></a>'
        f' · <a href="{REPO_URL}/blob/{commit}/LICENSE">licence</a></p>\n'
        '<p class="site-colophon">Formatted and typeset with '
        '<a href="https://github.com/jlevy/flowmark">Flowmark</a> and '
        '<a href="https://github.com/jlevy/kpress">KPress</a></p>\n'
        "</footer>"
    )


def page_html(page: Page, *, commit: str) -> str:
    """One page in the shared shell, refused if it would fetch anything at view time."""
    shared = shell_assets()
    width, height = render_explainer.png_size(CARD)
    body = page.html
    if body is None:
        assert page.markdown is not None  # Page.__post_init__ holds exactly one
        body = markdown_html(page.markdown, title=page.title, where=page.path)
    base = base_for(page.path)
    values = {
        "PAGE_KEY": page.key,
        "PROSE_FONT": page.prose_font,
        "MONO_FONT": render_explainer.MONO_FONT,
        "PAGE_TITLE": escape(page.title),
        "PAGE_DESCRIPTION": escape(page.description),
        "CANONICAL_URL": canonical_url(page.path),
        "FAVICON_HREF": shared.favicon_href,
        "SITE_NAME": escape(SITE_NAME),
        "CARD_IMAGE_URL": SITE_URL + CARD.name,
        "CARD_IMAGE_WIDTH": str(width),
        "CARD_IMAGE_HEIGHT": str(height),
        "CARD_ALT": escape(render_explainer.CARD_ALT),
        "KPRESS_CSS": shared.kpress_css,
        "RELATION_CSS": shared.relation_css,
        "SITE_CSS": shared.site_css,
        "THEME_BOOTSTRAP": shared.theme_bootstrap,
        "KATEX_JS": shared.katex_js,
        "KPRESS_CLIENT_SCRIPT": shared.kpress_client,
        **shared.math_scripts,
        "SITE_MATH_SCRIPT": shared.site_math,
        "NAV_HTML": nav_html(page.key, base=base),
        "FOOTER_HTML": footer_html(commit),
        "PAGE_SCRIPTS": "\n".join(
            f"<script>{path.read_text(encoding='utf-8')}</script>" for path in page.scripts
        ),
        "DEFAULT_BRANCH_LINKS": json_island(site_pages.default_branch_links(body)),
        # Last, so no later value is substituted inside the rendered body.
        "BODY_HTML": f"{shared.icon_sprite}\n{body}",
    }
    html = render_explainer.fill(
        SHELL.read_text(encoding="utf-8"), values, where=f"{SHELL.name} for {page.path}"
    )
    # The explainer's guard refuses every `<link>` but the canonical one; the favicon
    # link is the one exception, and only as the data URI written above.
    render_explainer.assert_self_contained(_ICON_LINK.sub("", html, count=1))
    return html


def json_island(value: object) -> str:
    """JSON to sit inside a `<script type="application/json">`, which `</` would end."""
    return json.dumps(value, ensure_ascii=False, sort_keys=True).replace("</", "<\\/")


def site_pages_of(commit: str, modules: Iterable[ModuleType] = PAGE_MODULES) -> list[Page]:
    """Every part's pages, with their repository links at `commit`."""
    return [page for module in modules for page in module.pages(commit)]


def site_assets_of(modules: Iterable[ModuleType] = ASSET_MODULES) -> list[Asset]:
    return [asset for module in modules for asset in module.assets()]


def render(commit: str | None = None) -> dict[str, bytes]:
    """Every file of the overview's part of the site, keyed by its path under the root."""
    commit = commit or render_explainer.link_revision()
    files: dict[str, bytes] = {}

    def add(path: str, content: bytes) -> None:
        if path in files:
            raise SystemExit(f"two parts of the site both write {path}")
        files[path] = content

    for page in site_pages_of(commit):
        add(page.path, page_html(page, commit=commit).encode("utf-8"))
    for asset in site_assets_of():
        add(asset.path, asset.content)
    return dict(sorted(files.items()))


def link_report(files: Mapping[str, bytes], commit: str) -> list[str]:
    """Every page's broken links, proved offline against the build commit.

    Each repository path a page links must exist at `commit` (one `git ls-tree` listing,
    which a blobless clone answers without fetching), and each in-page anchor must name an
    id the page has. It runs from the command line, which renders at the checkout's own
    commit; `render()` itself stays a pure function of its commit, so tests can render at
    a placeholder.
    """
    return [
        f"{path}: {problem}"
        for path, content in files.items()
        if path.endswith(".html")
        for problem in site_pages.link_problems(content.decode("utf-8"), commit)
    ]


def _label(path: Path) -> str:
    return path.relative_to(REPO).as_posix() if path.is_relative_to(REPO) else str(path)


def check(output: Path, files: Mapping[str, bytes]) -> list[str]:
    """What differs between a fresh render and the files on disk, one line each."""
    problems = []
    for relative, content in files.items():
        path = output / relative
        if not path.is_file():
            problems.append(f"{_label(path)} has not been rendered")
        elif path.read_bytes() != content:
            problems.append(f"{_label(path)} is stale; rerender it")
    if output.is_dir():
        problems.extend(
            f"{_label(path)} is not part of the render; remove it"
            for path in sorted(p for p in output.rglob("*") if p.is_file())
            if path.relative_to(output).as_posix() not in files
        )
    return problems


def write(output: Path, files: Mapping[str, bytes]) -> None:
    """Write the render, and remove anything in the directory the render no longer makes."""
    output.mkdir(parents=True, exist_ok=True)
    for path in sorted(p for p in output.rglob("*") if p.is_file()):
        if path.relative_to(output).as_posix() not in files:
            path.unlink()
    for relative, content in files.items():
        path = output / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        with atomic_output_file(path) as temporary:
            temporary.write_bytes(content)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n", 1)[0])
    parser.add_argument("--output", type=Path, default=OUTPUT)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--update", action="store_true", help="write the render (the default)")
    mode.add_argument(
        "--check",
        action="store_true",
        help="exit non-zero if the files on disk differ from a fresh render",
    )
    args = parser.parse_args(argv)

    output = args.output.resolve()
    if output == EXPLAINER_OUTPUT.resolve():
        raise SystemExit(
            f"{_label(output)} is the explainer's output; the overview would overwrite its "
            "index.html, so it renders to its own directory"
        )
    commit = render_explainer.link_revision()
    files = render(commit)
    broken = link_report(files, commit)
    for problem in broken:
        print(problem, file=sys.stderr)
    if broken:
        return 1
    if args.check:
        problems = check(output, files)
        for problem in problems:
            print(problem, file=sys.stderr)
        if problems:
            return 1
        print(f"{_label(output)} is current ({len(files)} files)")
        return 0
    write(output, files)
    total = sum(len(content) for content in files.values())
    print(f"wrote {_label(output)}: {len(files)} files, {total / 1024:.0f} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
