"""The separate T-060 paper remains complete when opened from a local file."""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Literal

import pytest

from devtools import render_n11_optimality_explainer as paper
from devtools.n11_optimality_figures import render_figures
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
SOURCE = """# Why Eleven Squares Need This Much Room

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


@pytest.fixture(scope="module")
def rendered() -> tuple[str, str]:
    return paper.render(SOURCE, figures=FIGURES, revision=REVISION, article=ARTICLE)


def test_rendered_page_is_offline_and_contains_proof_figures(rendered: tuple[str, str]) -> None:
    html, markdown = rendered
    assert_self_contained(html)
    assert html.count("<title>Exact diagram</title>") == 4
    assert '<span class="kpress-math kpress-math-inline"' in html
    assert 'class="kpress-footnotes"' in html
    assert "{{" not in markdown
    for name in ("MD", "PDF", "GITHUB"):
        assert f">{name}</a>" in html
    assert '<div class="doc-links screen-only">' in html
    assert 'href="https://github.com/jlevy/squares"' in html


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
        figures=render_figures(),
        revision=REVISION,
    )
    assert "Why Eleven Squares Need This Much Room" in html
    assert len(re.findall(r"<figure\b", html)) == 3
    assert len(re.findall(r"<figcaption\b", html)) == 3
    assert html.count("<svg") >= 5  # four paper figures plus KPress's icon sprite
    assert "<pre><code><svg" not in html
    assert "kpress-math-render" in html
    assert "{{" not in markdown
    assert not re.search(r"[\ue000-\uf8ff]", html + markdown)
    assert "../../resources/" not in markdown
    assert f"/blob/{REVISION}/packing/resources/" in markdown
    assert markdown.count(f"/blob/{REVISION}/") >= 39


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
        figures=render_figures(),
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
                assert len(roles) == 4
                for role in roles:
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
