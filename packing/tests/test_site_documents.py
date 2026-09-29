"""The tutorial page: links rewritten for the site, and every one resolved."""

from __future__ import annotations

import re

import pytest

from devtools import render_overview, site_documents
from devtools.site_documents import (
    RAW_URL,
    LinkContext,
    LinkReport,
    RepositoryTree,
    rewrite_article,
    rewrite_link,
    unresolved,
)

REPO_URL = render_overview.REPO_URL
COMMIT = "0" * 40
TREE = RepositoryTree(
    files=frozenset(
        {"README.md", "SYNOPSIS.md", "conventions.md", "packing/atlas/n5.svg", "docs/a b.md"}
    ),
    directories=frozenset({"", "packing", "packing/atlas", "docs"}),
)


def context(page: str = "tutorial.html") -> LinkContext:
    return LinkContext(page, COMMIT, TREE, frozenset({"the-problem"}))


def rewrite(url: str, *, tag: str = "a", page: str = "tutorial.html") -> tuple[str, LinkReport]:
    report = LinkReport()
    return rewrite_link(url, tag=tag, context=context(page), report=report), report


@pytest.mark.parametrize(
    ("url", "expected"),
    [
        ("README.md", "./"),
        ("README.md#the-problem", "./#the-problem"),
        (
            "README.md#results-by-others",
            f"{REPO_URL}/blob/{COMMIT}/README.md#results-by-others",
        ),
        ("conventions.md#4-evidence", f"{REPO_URL}/blob/{COMMIT}/conventions.md#4-evidence"),
        ("./conventions.md", f"{REPO_URL}/blob/{COMMIT}/conventions.md"),
        ("packing/atlas/", f"{REPO_URL}/tree/{COMMIT}/packing/atlas"),
        ("packing", f"{REPO_URL}/tree/{COMMIT}/packing"),
        ("docs/a%20b.md", f"{REPO_URL}/blob/{COMMIT}/docs/a%20b.md"),
        ("SYNOPSIS.md#terminology", f"{REPO_URL}/blob/{COMMIT}/SYNOPSIS.md#terminology"),
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


def test_an_image_becomes_a_raw_permalink() -> None:
    rewritten, _ = rewrite("packing/atlas/n5.svg", tag="img")
    assert rewritten == f"{RAW_URL}/{COMMIT}/packing/atlas/n5.svg"


def test_anchors_into_the_documents_are_recorded_for_checking() -> None:
    _, report = rewrite("TUTORIAL.md#start", page="frontier.html")
    assert report.anchors == [("tutorial.html", "start", "TUTORIAL.md#start")]


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
        "no such path at the build commit: missing.md",
    ]


def test_only_the_article_is_rewritten() -> None:
    page = (
        '<nav><a href="frontier.html">F</a></nav>'
        '<article><a href="conventions.md">c</a>'
        '<img src="packing/atlas/n5.svg" alt=""></article>'
        '<footer><a href="conventions.md">c</a></footer>'
    )
    out = rewrite_article(page, context=context(), report=LinkReport())
    assert '<a href="frontier.html">' in out
    assert f'href="{REPO_URL}/blob/{COMMIT}/conventions.md"' in out
    assert f'src="{RAW_URL}/{COMMIT}/packing/atlas/n5.svg"' in out
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
        with pytest.raises(
            SystemExit, match=r"no such path at the build commit: no/such/file\.md"
        ):
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
    served = {"./", "tutorial.html"}
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
