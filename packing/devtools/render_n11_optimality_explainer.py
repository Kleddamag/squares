"""Publish the T-060 paper as an offline HTML page and readable Markdown.

The article and exact-data figures are maintained separately. This renderer only
substitutes the declared reviewed figure slots, gives repository citations immutable
links, and uses KPress for Markdown, math, footnotes, typography, and PDF print.

The page is one of the site's papers (`overview_sections.PAPERS`), so it carries the
site's navigation bar, with Papers current, as the explainer does: the shared partial
and stylesheet through `render_overview.nav_html`, the gear's program, and the script
that drops the bar when the page is framed in a card's popover. It is served a level
below the site's root, so the bar's links climb one. The bar is hidden in print.
"""

from __future__ import annotations

import argparse
import re
import subprocess
from collections.abc import Mapping, Sequence
from html import escape
from pathlib import Path

from kpress.format.pdf import _await_print_fonts  # pyright: ignore[reportPrivateUsage]
from kpress.output import write_bytes_atomic
from strif import atomic_output_file

from devtools import render_explainer
from devtools.render_overview import (
    EMBED_SCRIPT,
    PAPER_TYPE_CSS,
    SITE_NAV,
    SITE_NAV_CSS,
    THEME_SCRIPT,
    favicon_html,
    nav_html,
)

PACKING = Path(__file__).resolve().parents[1]
REPO = PACKING.parent
TEMPLATES = Path(__file__).with_name("templates")
ARTICLE = TEMPLATES / "n11-optimality-article.md"
SHELL = TEMPLATES / "n11-optimality-shell.html"
STYLE = TEMPLATES / "n11-optimality.css"
FIGURES_MODULE = Path(__file__).with_name("n11_optimality_figures.py")
OUTPUT_DIR = PACKING / "site" / "n11-optimality"
STEM = "t-060-explainer"
#: Where the paper is served, from the site's root, and the way back up to the root.
SITE_PATH = f"{OUTPUT_DIR.name}/{STEM}.html"
SITE_ROOT = "../"
TITLE = "A Review of the Optimality Proof of the Trump Packing of 11 Squares"
DESCRIPTION = "A review of the optimality proof of the Trump packing of eleven squares."
FIGURE_KEYS = (
    "WITNESS_SVG",
    "ROADMAP_SVG",
    "COVER_SVG",
    "MASK_SVG",
    "CAPACITY_SVG",
    "POSE_SVG",
    "ROW_SVG",
    "CHARGE_SVG",
    "SYMMETRY_SVG",
    "CAPTURE_SVG",
    "LOCAL_SVG",
    "ENDPOINT_SVG",
)
MATH_WAIT_MS = 15_000
FIGURE_SLOT = re.compile(r"\{\{([A-Z_]+_SVG)\}\}")
LEFTOVER_SLOT = re.compile(r"\{\{[A-Z][A-Z_]*\}\}")
RELATIVE_LINK = re.compile(r"(?P<start>\]\()(?P<url>\.\.?/[^\s)]+)(?P<end>\))")
RELATIVE_REFERENCE = re.compile(r"(?m)^(?P<start>\[[^\]\n]+\]:[ \t]*)(?P<url>\.\.?/[^\s]+)")
RELATIVE_ANCHOR = re.compile(r'(?P<start><a\b[^>]*\bhref=")(?P<url>\.\.?/[^"]+)(?P<end>")')
ARCHIVED_CITATION_SOURCES = (
    PACKING / "resources/papers/kingbird-square-11-provenance.svg",
    PACKING / "resources/web/external-square-certificates-2026-09-22/kleddamag-11/README.md",
)
RENDER_INPUTS = (
    Path(__file__),
    ARTICLE,
    SHELL,
    STYLE,
    *ARCHIVED_CITATION_SOURCES,
    render_explainer.PUBLICATION_STYLE,
    FIGURES_MODULE,
    PACKING / "devtools/n11_optimality_overview_figures.py",
    PACKING / "devtools/n11_optimality_mechanism_figures.py",
    PACKING / "devtools" / "check_n11_optimality_d4.py",
    PACKING / "devtools" / "render_explainer.py",
    PACKING / "devtools" / "explainer" / "diagram-labels.js",
    PACKING / "devtools" / "render_overview.py",
    PAPER_TYPE_CSS,
    SITE_NAV,
    SITE_NAV_CSS,
    THEME_SCRIPT,
    EMBED_SCRIPT,
    PACKING / "atlas" / "rendering" / "trump11-overview.svg",
    PACKING / "devtools" / "packing_render_adapters.py",
    PACKING / "src" / "sqpack" / "render",
    PACKING / "cases" / "trump11" / "packing.py",
    PACKING / "resources/web/n11-optimality-2026-09-29/receipts/final-composition.json",
    PACKING / "resources/web/n11-optimality-2026-09-29/receipts/d4-independent/result.json",
    PACKING / "resources/web/n11-optimality-2026-09-29/receipts/d4-independent/objects",
    PACKING / "resources/web/n11-optimality-2026-09-29/receipts/source-graph/result.json",
    PACKING / "resources/web/n11-optimality-2026-09-29/receipts/exclusion-inventory.json",
    PACKING / "resources/web/n11-optimality-2026-09-29/receipts/local-isolation/result.json",
    PACKING / "resources/web/n11-optimality-2026-09-29/receipts/pose-inclusion/result.json",
    PACKING / "devtools/check_n11_generic_fresh.py",
    PACKING / "devtools/check_n11_optimality_field_mask0.py",
    PACKING
    / "resources/web/n11-optimality-2026-09-29/receipts/generic-mask2095-intake"
    / "provenance.json",
    PACKING
    / "resources/web/n11-optimality-2026-09-29/receipts/generic-mask2095-intake"
    / "full-result.json",
    PACKING
    / "resources/web/n11-optimality-2026-09-29/receipts/generic-mask2095-intake/objects",
    PACKING / "resources/web/n11-optimality-2026-09-29/receipts/field-mask0/result.json",
    PACKING / "resources/web/n11-optimality-2026-09-29/receipts/field-mask0/objects",
    REPO / "vendor" / "kpress",
)


def render_all_figures() -> dict[str, str]:
    """Load the figure renderers only in a full publication checkout."""
    from devtools.n11_optimality_figures import render_figures  # noqa: PLC0415
    from devtools.n11_optimality_mechanism_figures import (  # noqa: PLC0415
        render_mechanism_figures,
    )
    from devtools.n11_optimality_overview_figures import (  # noqa: PLC0415
        render_overview_figures,
    )

    groups = (render_figures(), render_overview_figures(), render_mechanism_figures())
    figures: dict[str, str] = {}
    for group in groups:
        if figures.keys() & group.keys():
            raise ValueError("figure renderers supplied duplicate slots")
        figures.update(group)
    return figures


def link_revision() -> str:
    """The commit the paper's repository citations name: the one it is built from.

    The paper pins each citation to a commit, so a cited receipt reads as it did when
    the paper was typeset; the site's own pages link `main` instead (`repo_links`). The
    deploy renders from `main`, so `HEAD` there is a commit `main` keeps. Where git
    cannot answer (a source tarball), `--revision` has to say which commit it is.
    """
    found = subprocess.run(
        ("git", "rev-parse", "HEAD"), cwd=REPO, capture_output=True, text=True, check=False
    )
    revision = found.stdout.strip()
    if found.returncode != 0 or not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise SystemExit("git names no HEAD here: give --revision, a full commit ID")
    return revision


def _fill(template: str, values: Mapping[str, str], *, source: Path) -> str:
    rendered = template
    for key, value in values.items():
        rendered = rendered.replace("{{" + key + "}}", value)
    remaining = LEFTOVER_SLOT.findall(rendered)
    if remaining:
        raise ValueError(f"{source.name}: unresolved placeholders: {sorted(set(remaining))}")
    return rendered


def _repository_links(markdown: str, *, source: Path, revision: str) -> str:
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ValueError("repository-link revision must be a full lowercase Git commit ID")

    def pin(url: str) -> str:
        path_text, mark, fragment = url.partition("#")
        target = (source.parent / path_text).resolve()
        if not target.is_relative_to(REPO):
            raise ValueError(f"{source.name}: link escapes repository: {path_text}")
        if not target.is_file():
            raise ValueError(f"{source.name}: linked source does not exist: {path_text}")
        path = target.relative_to(REPO).as_posix()
        result = f"https://github.com/jlevy/squares/blob/{revision}/{path}"
        if mark:
            result += "#" + fragment
        return result

    markdown = RELATIVE_LINK.sub(
        lambda match: match.group("start") + pin(match.group("url")) + match.group("end"),
        markdown,
    )
    markdown = RELATIVE_REFERENCE.sub(
        lambda match: match.group("start") + pin(match.group("url")), markdown
    )
    return RELATIVE_ANCHOR.sub(
        lambda match: (
            match.group("start")
            + escape(pin(match.group("url")), quote=True)
            + match.group("end")
        ),
        markdown,
    )


def expanded_markdown(
    source: str, *, figures: Mapping[str, str], article: Path = ARTICLE, revision: str
) -> str:
    """Fill only declared figure slots and pin local source citations to a Git commit."""
    if set(figures) != set(FIGURE_KEYS):
        raise ValueError("figures must provide exactly the declared SVG slots")
    if set(FIGURE_SLOT.findall(source)) != set(FIGURE_KEYS):
        raise ValueError("article must use every declared figure slot exactly by name")
    if any(source.count("{{" + key + "}}") != 1 for key in FIGURE_KEYS):
        raise ValueError("article must use each figure slot exactly once")
    for key, svg in figures.items():
        if not svg.lstrip().startswith("<svg") or "</svg>" not in svg:
            raise ValueError(f"{key} is not a complete SVG")
        if re.search(
            r"<script\b|<foreignObject\b|\b(?:href|src)=[\"']https?://",
            svg,
            re.IGNORECASE,
        ):
            raise ValueError(f"{key} contains active or remote SVG content")
    filled = _fill(source, figures, source=article)
    return _repository_links(filled, source=article, revision=revision)


def _katex_js(static: Path) -> str:
    from kpress.format.assets import KATEX_JS_ASSETS  # noqa: PLC0415

    parts = [(static / name).read_text(encoding="utf-8") for name in KATEX_JS_ASSETS]
    joined = "\n".join(parts)
    if "</script" in joined.lower():
        raise ValueError("KaTeX asset closes its inline script")
    return joined


def render(
    source: str,
    *,
    figures: Mapping[str, str],
    revision: str,
    article: Path = ARTICLE,
) -> tuple[str, str]:
    """Return self-contained HTML and the expanded Markdown it typesets."""
    from kpress.format.markdown import parse_markdown  # noqa: PLC0415

    markdown = expanded_markdown(source, figures=figures, article=article, revision=revision)
    document = parse_markdown(markdown, title=TITLE, trust_mode="trusted", math="auto")
    errors = [item.message for item in document.diagnostics if item.severity == "error"]
    if errors:
        raise ValueError(f"{article.name}: KPress refused the article: {'; '.join(errors)}")
    static = render_explainer.kpress_static()
    values = {
        "PAGE_TITLE": escape(TITLE),
        "PAGE_DESCRIPTION": escape(DESCRIPTION),
        "KPRESS_CSS": render_explainer.kpress_css(static),
        "KATEX_CSS": render_explainer.katex_css(static) if document.has_math else "",
        "RELATION_CSS": render_explainer.relation_face_css(static),
        "PAPER_TYPE_CSS": PAPER_TYPE_CSS.read_text(encoding="utf-8"),
        "PUBLICATION_CSS": render_explainer.PUBLICATION_STYLE.read_text(encoding="utf-8"),
        "PAPER_CSS": STYLE.read_text(encoding="utf-8"),
        "SITE_FAVICON": favicon_html(),
        "SITE_NAV_CSS": SITE_NAV_CSS.read_text(encoding="utf-8"),
        "SITE_NAV": nav_html("papers", root=SITE_ROOT),
        "SITE_EMBED": EMBED_SCRIPT.read_text(encoding="utf-8"),
        "SITE_THEME": THEME_SCRIPT.read_text(encoding="utf-8"),
        "THEME_BOOTSTRAP": render_explainer.theme_bootstrap(static),
        "BODY_HTML": document.html,
        "KATEX_JS": _katex_js(static) if document.has_math else "",
        "DIAGRAM_LABEL_SCRIPT": render_explainer.INLINE_SCRIPT_ASSETS[
            "DIAGRAM_LABEL_SCRIPT"
        ].read_text(encoding="utf-8"),
        "PDF_NAME": STEM + ".pdf",
        "MARKDOWN_NAME": STEM + ".md",
        "REPO_URL": render_explainer.REPO_URL,
    }
    page = _fill(SHELL.read_text(encoding="utf-8"), values, source=SHELL)
    render_explainer.assert_self_contained(page)
    return page, markdown


def _index() -> str:
    destination = STEM + ".html"
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        f'<meta http-equiv="refresh" content="0; url={destination}">'
        f'<link rel="canonical" href="{destination}">'
        f"<title>{escape(TITLE)}</title></head><body>"
        f'<p><a href="{destination}">Read the T-060 paper</a>.</p></body></html>\n'
    )


def output_files(output_dir: Path, html: str, markdown: str) -> dict[Path, str]:
    return {
        output_dir / (STEM + ".html"): html,
        output_dir / (STEM + ".md"): markdown,
        output_dir / "index.html": _index(),
    }


def _print_pdf(html_path: Path, pdf_path: Path) -> None:
    """Print only after KPress math and its print fonts have settled."""
    from playwright.sync_api import expect, sync_playwright  # noqa: PLC0415

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = None
        try:
            page = browser.new_page()
            page.goto(html_path.as_uri(), wait_until="networkidle")
            page.emulate_media(media="print")
            hosts = page.locator(".kpress-math")
            if hosts.count() == 0:
                raise ValueError("the paper has no typeset math")
            try:
                expect(page.locator(".kpress-math:not(:has(.katex))")).to_have_count(
                    0, timeout=MATH_WAIT_MS
                )
            except AssertionError as exc:
                raise ValueError("the paper has unrendered math") from exc
            if page.locator(".katex-error, math merror").count():
                raise ValueError("the paper contains a math rendering error")
            _await_print_fonts(page)  # pyright: ignore[reportArgumentType]
            write_bytes_atomic(
                pdf_path,
                page.pdf(format="Letter", prefer_css_page_size=True, print_background=True),
            )
        finally:
            if page is not None:
                page.close()
            browser.close()


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)
    parser.add_argument("--revision", default=None, help="full Git commit for source links")
    parser.add_argument("--pdf", action="store_true", help="also print the HTML with KPress")
    parser.add_argument("--check", action="store_true", help="compare current HTML/Markdown")
    args = parser.parse_args(argv)
    html, markdown = render(
        ARTICLE.read_text(encoding="utf-8"),
        figures=render_all_figures(),
        revision=args.revision or link_revision(),
    )
    output_dir = args.output_dir.resolve()
    outputs = output_files(output_dir, html, markdown)
    if args.check:
        if args.pdf:
            parser.error("--check compares HTML and Markdown; use --pdf for a fresh PDF")
        stale = [
            path
            for path, content in outputs.items()
            if not path.is_file() or path.read_text(encoding="utf-8") != content
        ]
        if stale:
            raise SystemExit(
                "stale n11 explainer output: " + ", ".join(str(path) for path in stale)
            )
        return 0
    output_dir.mkdir(parents=True, exist_ok=True)
    for path, content in outputs.items():
        with atomic_output_file(path) as temporary:
            temporary.write_text(content, encoding="utf-8")
    if args.pdf:
        _print_pdf(output_dir / (STEM + ".html"), output_dir / (STEM + ".pdf"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
