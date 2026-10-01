"""The tutorial page: links rewritten for the site, and every one resolved."""

from __future__ import annotations

import re

import pytest

from devtools import render_overview, site_documents
from devtools.repo_links import RAW_URL, REPO_URL, RepositoryTree
from devtools.site_documents import (
    LinkContext,
    LinkReport,
    rewrite_article,
    rewrite_link,
    unresolved,
)

#: Every repository link on the site names the default branch, never a commit.
BRANCH = "main"
TREE = RepositoryTree(
    files=frozenset(
        {"README.md", "SYNOPSIS.md", "conventions.md", "packing/atlas/n5.svg", "docs/a b.md"}
    ),
    directories=frozenset({"", "packing", "packing/atlas", "docs", "vendor/kpress"}),
    submodules={"vendor/kpress": ("https://github.com/jlevy/kpress", "1" * 40)},
)


def context(page: str = "tutorial.html", base: str = "") -> LinkContext:
    return LinkContext(page, TREE, base)


def rewrite(
    url: str, *, tag: str = "a", page: str = "tutorial.html", base: str = ""
) -> tuple[str, LinkReport]:
    report = LinkReport()
    return rewrite_link(url, tag=tag, context=context(page, base), report=report), report


@pytest.mark.parametrize(
    ("url", "expected"),
    [
        ("README.md", "readme.html"),
        ("README.md#the-problem", "readme.html#the-problem"),
        ("conventions.md#4-evidence", "conventions.html#4-evidence"),
        ("./conventions.md", "conventions.html"),
        ("packing/atlas/", f"{REPO_URL}/tree/{BRANCH}/packing/atlas"),
        ("packing", f"{REPO_URL}/tree/{BRANCH}/packing"),
        ("docs/a%20b.md?plain=1#L3", f"{REPO_URL}/blob/{BRANCH}/docs/a%20b.md?plain=1#L3"),
        ("docs/a%20b.md", f"{REPO_URL}/blob/{BRANCH}/docs/a%20b.md"),
        ("SYNOPSIS.md#terminology", "synopsis.html#terminology"),
        (
            "vendor/kpress/docs/x.md",
            f"https://github.com/jlevy/kpress/blob/{'1' * 40}/docs/x.md",
        ),
        ("TUTORIAL.md#start", "#start"),
        ("TUTORIAL.md", "tutorial.html"),
        ("#local", "#local"),
        ("https://example.org/x.md", "https://example.org/x.md"),
        ("mailto:someone@example.org", "mailto:someone@example.org"),
    ],
)
def test_a_link_is_rewritten_for_the_site(url: str, expected: str) -> None:
    rewritten, report = rewrite(url)
    assert rewritten == expected
    assert not report.missing


def test_an_image_becomes_its_raw_file_on_main() -> None:
    rewritten, _ = rewrite("packing/atlas/n5.svg", tag="img")
    assert rewritten == f"{RAW_URL}/{BRANCH}/packing/atlas/n5.svg"


def test_anchors_into_the_documents_are_recorded_for_checking() -> None:
    _, report = rewrite("TUTORIAL.md#start", page="frontier.html")
    assert report.anchors == [("tutorial.html", "start", "TUTORIAL.md#start")]
    _, report = rewrite("conventions.md#4-evidence")
    assert report.anchors == [("conventions.html", "4-evidence", "conventions.md#4-evidence")]


def test_a_relative_link_resolves_from_the_documents_directory() -> None:
    rewritten, report = rewrite("../README.md", base="packing")
    assert rewritten == "readme.html"
    assert not report.missing
    rewritten, _ = rewrite("n5.svg", tag="img", base="packing/atlas")
    assert rewritten == f"{RAW_URL}/{BRANCH}/packing/atlas/n5.svg"


@pytest.mark.parametrize("url", ["missing.md", "packing/nowhere/", "../outside.md"])
def test_an_unresolved_target_is_reported(url: str) -> None:
    rewritten, report = rewrite(url)
    assert rewritten == url
    assert len(report.missing) == 1


def test_unresolved_lists_missing_paths_and_anchors() -> None:
    report = LinkReport(
        missing=["missing.md"], anchors=[("tutorial.html", "gone", "TUTORIAL.md#gone")]
    )
    page = render_overview.Page("tutorial.html", '<article><h2 id="here">x</h2></article>')
    problems = unresolved({"tutorial.html": page}, report)
    assert problems == [
        "no heading #gone in tutorial.html: TUTORIAL.md#gone",
        "no such path in the tree: missing.md",
    ]


def test_only_the_article_is_rewritten() -> None:
    page = (
        '<nav><a href="frontier.html">F</a></nav>'
        '<article><a href="docs/a%20b.md">c</a>'
        '<img src="packing/atlas/n5.svg" alt=""></article>'
        '<footer><a href="conventions.md">c</a></footer>'
    )
    out = rewrite_article(page, context=context(), report=LinkReport())
    assert '<a href="frontier.html">' in out
    assert f'href="{REPO_URL}/blob/{BRANCH}/docs/a%20b.md"' in out
    assert f'src="{RAW_URL}/{BRANCH}/packing/atlas/n5.svg"' in out
    assert '<footer><a href="conventions.md">' in out


def test_the_build_fails_on_an_unresolved_link(monkeypatch: pytest.MonkeyPatch) -> None:
    """A broken link in a document stops the render and names the link."""
    original = site_documents.render_document

    def with_a_broken_link(document: site_documents.SiteDocument, **kwargs: object) -> object:
        report = kwargs["report"]
        assert isinstance(report, LinkReport)
        report.missing.append("no/such/file.md")
        return original(document, **kwargs)  # pyright: ignore[reportArgumentType]

    site_documents.site_documents.cache_clear()
    monkeypatch.setattr(site_documents, "render_document", with_a_broken_link)
    try:
        with pytest.raises(SystemExit, match=r"no such path in the tree: no/such/file\.md"):
            site_documents.site_documents()
    finally:
        site_documents.site_documents.cache_clear()


@pytest.fixture(scope="module")
def pages() -> dict[str, render_overview.Page]:
    return {name: render_overview.PAGES[name]() for name in ("tutorial.html",)}


def test_the_pages_render_self_contained_with_a_toc(
    pages: dict[str, render_overview.Page],
) -> None:
    for name, page in pages.items():
        render_overview.assert_self_contained(name, page.html)
        assert "data-kpress-toc" in page.html, name
        assert 'aria-current="page"' in page.html, name


def test_no_relative_repository_link_survives(pages: dict[str, render_overview.Page]) -> None:
    served = {"./", *render_overview.SITE_PAGES}
    for name, page in pages.items():
        article = re.search(r"<article\b.*?</article>", page.html, re.DOTALL)
        assert article is not None
        for url in re.findall(r'\s(?:href|src)="([^"]*)"', article.group(0)):
            if url.startswith(("#", "https://", "http://", "data:", "mailto:")):
                continue
            assert url.split("#")[0] in served, f"{name}: {url}"


def test_the_tutorial_math_is_kpress_math(pages: dict[str, render_overview.Page]) -> None:
    """Each `$…$` span reaches the page as kpress math markup, which KaTeX renders on load."""
    body = pages["tutorial.html"].html
    assert len(re.findall(r'data-kpress-math="inline"', body)) >= 14
    assert 'data-kpress-math-error="true">' not in body


def test_long_reports_get_a_contents_rail_and_short_ones_do_not() -> None:
    """kpress's own length rule decides, so a short report keeps the one centred
    column and a long one adds the rail beside it."""
    short = "\n\n".join(f"## Part {i}\n\nA line of text." for i in range(3))

    def rail(markdown: str) -> bool:
        page = render_overview.kpress_page(
            markdown,
            name="short.html",
            current="papers",
            title="T",
            description="D",
            toc="auto",
        )
        return 'class="kpress-toc ' in page.html

    assert not rail(short)
    assert 'class="kpress-toc ' in render_overview.PAGES["tutorial.html"]().html


def test_a_hand_written_contents_list_is_dropped_from_the_page() -> None:
    """The tutorial's own Contents list, written for GitHub, is not on its page, where
    the contents rail lists the headings; the text around it stays."""
    markdown = "Intro.\n\n## Contents\n\n1. [One](#one)\n2. [Two](#two)\n\n## One\n\nBody.\n"
    assert site_documents.without_manual_contents(markdown) == "Intro.\n\n## One\n\nBody.\n"
    page = site_documents.tutorial_page().html
    assert 'id="contents"' not in page
    assert 'href="#contents"' not in page
