"""The separate T-060 paper remains complete when opened from a local file."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from devtools import render_n11_optimality_explainer as paper
from devtools.n11_optimality_figures import render_figures
from devtools.render_explainer import assert_self_contained

ARTICLE = paper.TEMPLATES / "n11-optimality-article.md"
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

{{WITNESS_SVG}}

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
    for name in ("HTML", "PDF", "Source"):
        assert f">{name}</a>" in html


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


def test_pdf_refuses_a_math_host_without_rendered_katex(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    pytest.importorskip("playwright.sync_api")
    html = tmp_path / "unrendered.html"
    html.write_text('<html><body><span class="kpress-math">raw TeX</span></body></html>')
    pdf = tmp_path / "unrendered.pdf"
    monkeypatch.setattr(paper, "MATH_WAIT_MS", 200)
    with pytest.raises(ValueError, match="unrendered math"):
        paper._print_pdf(html, pdf)  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
    assert not pdf.exists()


def test_radical_svg_has_print_geometry(tmp_path: Path) -> None:
    playwright = pytest.importorskip("playwright.sync_api")
    with playwright.sync_playwright() as driver:
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
