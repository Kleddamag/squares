"""The separate T-060 paper remains complete when opened from a local file."""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Literal

import pytest

from devtools import n11_optimality_mechanism_figures as mechanism
from devtools import n11_optimality_overview_figures as overview
from devtools import render_n11_optimality_explainer as paper
from devtools.render_explainer import assert_self_contained
from sqpack.probes import probe

ARTICLE = paper.TEMPLATES / "n11-optimality-article.md"
PROBES = Path(__file__).with_name("probes")
REVISION = "a" * 40
SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2 2">'
    '<title>Exact diagram</title><rect width="2" height="2"/></svg>'
)
FIGURES: dict[str, str] = dict.fromkeys(paper.FIGURE_KEYS, SVG)
SOURCE = """# A Review of the Optimality Proof of the Trump Packing of 11 Squares

An exact formula is $x^2$.[^proof] See the
[review](../../../docs/project/reviews/review-2026-09-29-n11-optimality.md)
and the [record][register].

<figure>
{{WITNESS_SVG}}
<figcaption>See the
<a href="../../cases/trump11/verify_exact.py">exact witness check</a>.</figcaption>
</figure>

{{COVER_SVG}}

{{CAPTURE_SVG}}

{{MASK_SVG}}

[^proof]: The claim has a retained proof.

[register]: ../../frontier/results.yaml
"""

SOURCE += "\n" + "\n".join(
    "{{" + key + "}}" for key in paper.FIGURE_KEYS if "{{" + key + "}}" not in SOURCE
)


@pytest.fixture(scope="module")
def rendered() -> tuple[str, str]:
    return paper.render(SOURCE, figures=FIGURES, revision=REVISION, article=ARTICLE)


def test_rendered_page_is_offline_and_contains_proof_figures(rendered: tuple[str, str]) -> None:
    html, markdown = rendered
    assert_self_contained(html)
    assert html.count("<title>Exact diagram</title>") == len(paper.FIGURE_KEYS)
    assert '<span class="kpress-math kpress-math-inline"' in html
    assert 'class="kpress-footnotes"' in html
    assert "{{" not in markdown
    for name in ("MD", "PDF", "GITHUB"):
        assert f">{name}</a>" in html
    assert '<div class="doc-links screen-only">' in html
    assert 'href="https://github.com/jlevy/squares"' in html


def test_the_paper_ends_with_the_sites_closing_credit(rendered: tuple[str, str]) -> None:
    """The paper's closing paragraph holds the two lines every page's footer is made of,
    the project and its repository, then the version and the credit to the two tools.
    The version is pinned in `release.py`, which is therefore one of the paper's declared
    inputs, so a re-pin puts the paper in the Pages workflow's scope."""
    from devtools import render_overview  # noqa: PLC0415
    from sqpack.release import PUBLICATION_EDITION  # noqa: PLC0415

    html, _ = rendered
    footer = f'<p class="col colophon centred">{render_overview.colophon_lines()}</p>'
    assert html.count(footer) == 1
    assert html.count('class="site-colophon-line"') == 2
    assert f'<span class="site-colophon-part">{PUBLICATION_EDITION}</span>' in footer
    assert paper.PACKING / "src" / "sqpack" / "release.py" in paper.RENDER_INPUTS


def test_the_page_carries_the_sites_bar_with_papers_current(rendered: tuple[str, str]) -> None:
    """The paper is one of the site's papers, so it carries the site's navigation bar as
    the explainer does, through the shared helper: Papers is the current entry, the
    bar's links climb to the site's root from the directory the paper is served in, the
    gear's program and the embed script ride with it, and print hides the bar."""
    from devtools import render_overview  # noqa: PLC0415

    html, _ = rendered
    assert paper.SITE_PATH == "n11-optimality/t-060-explainer.html"
    assert paper.SITE_PATH in render_overview.SITE_PAGES
    assert paper.SITE_PATH.count("/") == paper.SITE_ROOT.count("../") == 1
    assert render_overview.nav_html("papers", root="../") in html
    assert '<a data-page="papers" aria-current="page" href="../papers.html">Papers</a>' in html
    # One link is current, the bar's entry: the format chips link the other formats.
    assert len(re.findall(r'<a\b[^>]*\saria-current="page"', html)) == 1
    main = html.split('<main class="kpress-page-main kpress-viewport">', 1)[1]
    assert main.lstrip().startswith('<nav class="site-nav"')
    nav_css = render_overview.SITE_NAV_CSS.read_text(encoding="utf-8")
    assert nav_css in html
    # The shared text tokens come first, then the bar, then the publication layer both
    # papers share, which reads both, then this paper's own diagram rules.
    type_css = render_overview.PAPER_TYPE_CSS.read_text(encoding="utf-8")
    publication_css = paper.render_explainer.PUBLICATION_STYLE.read_text(encoding="utf-8")
    paper_css = paper.STYLE.read_text(encoding="utf-8")
    order = [html.index(sheet) for sheet in (type_css, nav_css, publication_css, paper_css)]
    assert order == sorted(order)
    assert (
        "@media print {\n  .site-nav,\n  .kpress-site-header {\n    display: none;" in nav_css
    )
    for script in (render_overview.THEME_SCRIPT, render_overview.EMBED_SCRIPT):
        assert script.read_text(encoding="utf-8") in html, script.name
    for needed in (
        render_overview.PAPER_TYPE_CSS,
        render_overview.SITE_NAV,
        render_overview.SITE_NAV_CSS,
        render_overview.THEME_SCRIPT,
        render_overview.EMBED_SCRIPT,
    ):
        assert needed in paper.RENDER_INPUTS, needed.name
    # The page's hero starts the site's one space below the bar's rule, by the rule the
    # first paper's hero uses; this paper declares no top space of its own.
    assert "    padding-block-start: var(--site-page-top);\n" in publication_css
    assert "--site-page-top" not in paper_css


def test_link_revision_is_the_commit_the_paper_is_built_from(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """The paper's citations name the checkout's `HEAD`, in full, and where git names no
    commit the renderer says so rather than writing a link no one can follow."""
    assert re.fullmatch(r"[0-9a-f]{40}", paper.link_revision())
    monkeypatch.setattr(paper, "REPO", tmp_path)
    with pytest.raises(SystemExit, match="give --revision"):
        paper.link_revision()


def test_local_citation_is_pinned(rendered: tuple[str, str]) -> None:
    html, markdown = rendered
    url = (
        "https://github.com/jlevy/squares/blob/"
        + REVISION
        + "/docs/project/reviews/review-2026-09-29-n11-optimality.md"
    )
    assert url in html
    assert url in markdown
    register_url = (
        "https://github.com/jlevy/squares/blob/" + REVISION + "/packing/frontier/results.yaml"
    )
    assert f"[register]: {register_url}" in markdown
    assert f'href="{register_url}"' in html
    witness_url = (
        "https://github.com/jlevy/squares/blob/"
        + REVISION
        + "/packing/cases/trump11/verify_exact.py"
    )
    assert f'<a href="{witness_url}"' in html
    assert ">exact witness check</a>" in html
    assert "[exact witness check](" not in html


@pytest.mark.parametrize(
    ("source", "figures"),
    [
        (SOURCE.replace("{{MASK_SVG}}", ""), FIGURES),
        (SOURCE + "\n{{MASK_SVG}}\n", FIGURES),
        (SOURCE, {**FIGURES, "EXTRA_SVG": SVG}),
        (SOURCE, {**FIGURES, "MASK_SVG": "<svg><script>bad</script></svg>"}),
    ],
)
def test_incomplete_or_active_figure_input_refuses(
    source: str, figures: dict[str, str]
) -> None:
    with pytest.raises(ValueError, match=r"figure|article|SVG"):
        paper.expanded_markdown(source, figures=figures, article=ARTICLE, revision=REVISION)


def test_relative_link_must_resolve_to_a_repo_file() -> None:
    unsafe = SOURCE.replace(
        "../../../docs/project/reviews/review-2026-09-29-n11-optimality.md",
        "../../../../etc/passwd",
    )
    with pytest.raises(ValueError, match="escapes repository"):
        paper.expanded_markdown(unsafe, figures=FIGURES, article=ARTICLE, revision=REVISION)


def test_missing_reference_target_refuses() -> None:
    missing = SOURCE.replace("../../frontier/results.yaml", "../../frontier/not-a-file.yaml")
    with pytest.raises(ValueError, match="does not exist"):
        paper.expanded_markdown(missing, figures=FIGURES, article=ARTICLE, revision=REVISION)


def test_output_names_and_landing_redirect(tmp_path: Path, rendered: tuple[str, str]) -> None:
    outputs = paper.output_files(tmp_path, *rendered)
    assert {path.name for path in outputs} == {
        "index.html",
        "t-060-explainer.html",
        "t-060-explainer.md",
    }
    assert "url=t-060-explainer.html" in outputs[tmp_path / "index.html"]


def test_actual_article_renders_all_retained_figures_and_pinned_sources() -> None:
    html, markdown = paper.render(
        paper.ARTICLE.read_text(encoding="utf-8"),
        figures=paper.render_all_figures(),
        revision=REVISION,
    )
    assert "A Review of the Optimality Proof of the Trump Packing of 11 Squares" in html
    assert len(re.findall(r"<figure\b", html)) == 11
    assert len(re.findall(r"<figcaption\b", html)) == 11
    assert (
        html.count("<svg") >= len(paper.FIGURE_KEYS) + 1
    )  # article figures and KPress icon sprite
    assert all(
        "$" not in caption
        for caption in re.findall(r"<figcaption>(.*?)</figcaption>", html, re.DOTALL)
    )
    assert "<pre><code><svg" not in html
    assert "kpress-math-render" in html
    assert "{{" not in markdown
    assert not re.search(r"[\ue000-\uf8ff]", html + markdown)
    assert "../../resources/" not in markdown
    assert f"/blob/{REVISION}/packing/resources/" in markdown
    assert markdown.count(f"/blob/{REVISION}/") >= 39


def test_a_diagram_drawn_in_fixed_ink_keeps_a_light_ground_on_the_dark_theme() -> None:
    """The page carries the site's theme control, so a diagram is read on the dark theme
    too. One drawn in the theme's tokens follows it; one whose labels are a fixed dark
    ink needs a light ground there, or its labels are dark on dark. The stylesheet's list
    of diagrams that take that ground is exactly the diagrams that carry fixed ink, and
    it keys on KPress's resolved theme, as every site stylesheet does."""
    fixed, themed = set(), set()
    for svg in paper.render_all_figures().values():
        found = re.match(r'<svg\b[^>]*\bclass="n11-diagram (n11-[a-z-]+)"', svg)
        if found is None:
            continue  # Figure 1, the atlas's rendering, which draws its own ground.
        ink = re.findall(r'<text\b[^>]*\bfill="(#[0-9a-fA-F]{3,6})"', svg)
        (fixed if ink else themed).add(found.group(1))
    assert fixed, "no diagram carries fixed ink: the ground rule has nothing to hold"
    assert themed, "no diagram follows the theme: the rule would apply to every diagram"
    css = paper.STYLE.read_text(encoding="utf-8")
    rule = re.search(
        r':root\[data-kpress-resolved-theme="dark"\]\s+\.n11-paper\s+:is\(([^)]*)\)\s*'
        r"\{\s*background: #fff;\s*\}",
        css,
    )
    assert rule is not None
    listed = {name.strip().removeprefix(".") for name in rule.group(1).split(",")}
    assert listed == fixed
    assert "prefers-color-scheme" not in css


def test_the_credits_are_one_column_no_wider_than_the_page() -> None:
    """The credits carry the original proof's address, one unbreakable word wider than a
    phone's column. As a grid's automatic column the credits took that width, and every
    credit was cut at the page's edge; the column is the page's width and the address
    may break."""
    css = paper.STYLE.read_text(encoding="utf-8")
    assert ".n11-paper .credits {\n  grid-template-columns: minmax(0, 1fr);\n}" in css
    assert ".n11-paper .credits a {\n  overflow-wrap: anywhere;\n}" in css
    parts = paper.ARTICLE.read_text(encoding="utf-8").split('<div class="credits centred">')
    assert len(parts) == 2
    block = parts[1].split("</div>", 1)[0]
    # The original proof leads, by its author's name in bold and then its address as a
    # plain link; this review's own credits follow a line's space below, names in bold,
    # and the draft's version is not bold.
    address = "github.com/Queuingtheorydotcom/11SquaresOptimal"
    oversight = '<a href="https://x.com/ojoshe"><strong>Joshua Levy</strong></a>'
    assert [line.strip() for line in block.strip().splitlines()][:5] == [
        "<span>From the original proof by <strong>Queuingtheorydotcom</strong></span>",
        f'<span><a href="https://{address}">{address}</a></span>',
        f'<span class="credits-review">Human oversight: {oversight}</span>',
        "<span>Agents: <strong>GPT-6 Astra</strong> and <strong>GPT-6 Sol</strong></span>",
        "<span>Draft v0.1.0</span>",
    ]
    assert ".n11-paper .credits .credits-review {\n  margin-block-start: 1lh;\n}" in css


def test_a_table_keeps_to_the_column_and_scrolls_inside_its_wrap() -> None:
    """The shared column rule caps a block at the measure, which outranks KPress's cap on
    a table's wrap, so on a phone the wrap ran past the article that clips it. The
    paper's own rule caps the wrap at the column too, later in the page and at a higher
    specificity than the shared rule, and the page has tables for it to hold.
    `preview_site --clips` measures the result in the browser."""
    css = paper.STYLE.read_text(encoding="utf-8")
    cap = "max-width: min(100%, calc(var(--kpress-measure) + 2 * var(--kpress-column-inset)));"
    assert f".cert-page.n11-paper > .kpress-table-wrap {{\n  {cap}\n}}" in css
    shared = paper.render_explainer.PUBLICATION_STYLE.read_text(encoding="utf-8")
    assert ".cert-page > :not(figure, .cert-figure, .kpress-figure),\n.col {" in shared
    html, _ = paper.render(
        paper.ARTICLE.read_text(encoding="utf-8"),
        figures=paper.render_all_figures(),
        revision=REVISION,
    )
    assert html.index(shared) < html.index(css)
    article = html.split('<article class="kpress kpress-doc kpress-prose cert-page n11-paper">')
    assert len(article) == 2
    assert len(re.findall(r'<div class="kpress-table-wrap"><table\b', article[1])) == 2


@pytest.mark.skipif(
    os.environ.get("SQPACK_N11_PAPER_BROWSER") != "1",
    reason="the dedicated T-060 Pages job sets SQPACK_N11_PAPER_BROWSER=1",
)
def test_pdf_refuses_a_math_host_without_rendered_katex(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    html = tmp_path / "unrendered.html"
    html.write_text('<html><body><span class="kpress-math">raw TeX</span></body></html>')
    pdf = tmp_path / "unrendered.pdf"
    monkeypatch.setattr(paper, "MATH_WAIT_MS", 200)
    with pytest.raises(ValueError, match="unrendered math"):
        paper._print_pdf(html, pdf)  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
    assert not pdf.exists()


@pytest.mark.skipif(
    os.environ.get("SQPACK_N11_PAPER_BROWSER") != "1",
    reason="the dedicated T-060 Pages job sets SQPACK_N11_PAPER_BROWSER=1",
)
def test_radical_svg_has_print_geometry(tmp_path: Path) -> None:
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    with sync_playwright() as driver:
        html, _ = paper.render(
            SOURCE.replace("$x^2$", r"$\sqrt2$"),
            figures=FIGURES,
            revision=REVISION,
            article=ARTICLE,
        )
        page_path = tmp_path / "radical.html"
        page_path.write_text(html, encoding="utf-8")
        browser = driver.chromium.launch()
        try:
            page = browser.new_page()
            page.goto(page_path.as_uri(), wait_until="networkidle")
            page.emulate_media(media="print")
            radical = page.locator(".katex .sqrt svg").first
            radical.wait_for(state="visible")
            box = radical.bounding_box()
            assert box is not None
            assert box["width"] > 1
            assert box["height"] > 1
        finally:
            browser.close()


@pytest.mark.skipif(
    os.environ.get("SQPACK_N11_PAPER_BROWSER") != "1",
    reason="the dedicated T-060 Pages job sets SQPACK_N11_PAPER_BROWSER=1",
)
def test_diagram_labels_keep_publication_sizes_through_viewbox_scale(tmp_path: Path) -> None:
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    html, _ = paper.render(
        paper.ARTICLE.read_text(encoding="utf-8"),
        figures=paper.render_all_figures(),
        revision=REVISION,
    )
    page_path = tmp_path / "diagram-roles.html"
    page_path.write_text(html, encoding="utf-8")
    measure = probe(PROBES, "n11_paper/diagram_roles")
    with sync_playwright() as driver:
        browser = driver.chromium.launch()
        try:
            views: tuple[tuple[int, Literal["screen", "print"]], ...] = (
                (1280, "screen"),
                (390, "screen"),
                (1280, "print"),
            )
            for width, media in views:
                page = browser.new_page(viewport={"width": width, "height": 900})
                page.goto(page_path.as_uri(), wait_until="networkidle")
                page.emulate_media(media=media)
                page.wait_for_function(measure, arg={"readyOnly": True})
                roles = page.evaluate(measure, {"readyOnly": False})
                assert len(roles) == len(paper.FIGURE_KEYS)
                for role in roles:
                    assert not role["overflowingLabels"], (width, media, role)
                    assert abs(role["label"] - role["support"]) < 0.1, (width, media, role)
                    if role["note"] is not None:
                        assert role["caption"] is not None
                        assert abs(role["note"] - role["caption"]) < 0.1, (
                            width,
                            media,
                            role,
                        )
                if width == 390:
                    assert any(role["scrollWidth"] > role["clientWidth"] for role in roles)
                page.close()
        finally:
            browser.close()


def test_new_figure_dependencies_are_declared_to_publication_scope() -> None:
    for source in (*mechanism.RENDER_INPUTS, *overview.RENDER_INPUTS):
        assert any(
            source == declared or (declared.is_dir() and source.is_relative_to(declared))
            for declared in paper.RENDER_INPUTS
        ), source
