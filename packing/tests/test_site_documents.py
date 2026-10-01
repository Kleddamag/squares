"""The tutorial page: links rewritten for the site, and every one resolved."""

from __future__ import annotations

import re

import pytest

from devtools import render_overview, site_documents
from devtools.repo_links import RAW_URL, REPO_URL, RepositoryTree
from devtools.site_documents import (
    INTRO,
    INTRO_BEGIN,
    INTRO_END,
    OVERVIEW_INTRO_CLOSE,
    OVERVIEW_INTRO_OPEN,
    PROGRESS,
    LinkContext,
    LinkReport,
    intro_block,
    progress_block,
    rewrite_article,
    rewrite_link,
    rewrite_overview_blocks,
    shared_blocks,
    unresolved,
)
from tests import site_renders

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
    return {name: site_renders.page(name) for name in ("tutorial.html",)}


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


def test_long_reports_get_a_contents_rail_and_short_ones_do_not(
    pages: dict[str, render_overview.Page],
) -> None:
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
    assert 'class="kpress-toc ' in pages["tutorial.html"].html


def test_a_hand_written_contents_list_is_dropped_from_the_page(
    pages: dict[str, render_overview.Page],
) -> None:
    """The tutorial's own Contents list, written for GitHub, is not on its page, where
    the contents rail lists the headings; the text around it stays."""
    markdown = "Intro.\n\n## Contents\n\n1. [One](#one)\n2. [Two](#two)\n\n## One\n\nBody.\n"
    assert site_documents.without_manual_contents(markdown) == "Intro.\n\n## One\n\nBody.\n"
    page = pages["tutorial.html"].html
    assert 'id="contents"' not in page
    assert 'href="#contents"' not in page


def _readme(body: str, progress: str = "What the project covers.") -> str:
    return (
        f"# Title\n\n{INTRO_BEGIN}\n\n{body}\n\n{INTRO_END}\n"
        f"{PROGRESS.begin}\n\n{progress}\n\n{PROGRESS.end}\n\nThe rest.\n"
    )


def test_the_introduction_is_the_block_between_readmes_markers() -> None:
    body = "One paragraph about $s(n)$.\n\nA second, with [a link](packing/atlas/)."
    assert intro_block(_readme(body)) == body


def test_readmes_two_shared_blocks_are_read_by_name_and_in_order() -> None:
    """The introduction is two blocks, each between its own markers: what the project
    studies, and what it covers with its newest result. They follow one another."""
    progress = "It covers every $n$.\n\nA recent result, [T-060](packing/frontier/RESULTS.md)."
    readme = _readme("What the project studies.", progress)
    assert progress_block(readme) == progress
    assert shared_blocks(readme) == {
        "project-intro": "What the project studies.",
        "recent-progress": progress,
    }
    assert (INTRO.name, PROGRESS.name) == ("project-intro", "recent-progress")
    assert (
        INTRO.begin
        == INTRO_BEGIN
        == ("<!-- BEGIN SHARED: project-intro (devtools.site_documents) -->")
    )
    assert PROGRESS.end == "<!-- END SHARED: recent-progress -->"
    assert (PROGRESS.opened, PROGRESS.closed) == (
        "<!-- README recent-progress -->",
        "<!-- /README recent-progress -->",
    )


@pytest.mark.parametrize(
    ("readme", "refusal"),
    [
        (
            _readme("Prose.").replace(f"{INTRO_END}\n", f"{INTRO_END}\n\nA stray line.\n\n"),
            "the recent-progress block must follow the project-intro block directly",
        ),
        (
            (
                f"{PROGRESS.begin}\n\nCovers.\n\n{PROGRESS.end}\n"
                f"{INTRO_BEGIN}\n\nStudies.\n\n{INTRO_END}\n"
            ),
            "the recent-progress block must follow the project-intro block directly",
        ),
        (
            f"{INTRO_BEGIN}\n\nStudies.\n\n{INTRO_END}\n",
            "the recent-progress markers must each appear exactly once",
        ),
        (_readme("Prose.", ""), "the recent-progress block is empty"),
        (_readme("Prose.", "Covers.\n\n### Newest\n\nMore."), "a heading or a comment"),
        (
            _readme("Prose.", "Eleven squares is the central case."),
            "the recent-progress block calls a case the central one",
        ),
        (
            _readme("Eleven squares is its central open case."),
            "the project-intro block calls a case the central one",
        ),
    ],
)
def test_a_malformed_pair_of_shared_blocks_is_refused(readme: str, refusal: str) -> None:
    with pytest.raises(ValueError, match=refusal):
        shared_blocks(readme)


@pytest.mark.parametrize(
    ("readme", "refusal"),
    [
        ("# Title\n\nNo markers.\n", "exactly once"),
        (_readme("Prose.") + _readme("Prose again."), "exactly once"),
        (f"{INTRO_END}\n\nProse.\n\n{INTRO_BEGIN}\n", "ends before it begins"),
        (_readme(""), "is empty"),
        (_readme("Prose.\n\n## A Heading\n\nMore."), "a heading or a comment"),
        (_readme("Prose.\n\n<!-- a note -->"), "a heading or a comment"),
        # A block that runs on into the next one holds that block's marker, a comment.
        (
            _readme("Prose.").replace(f"{INTRO_END}\n", "") + f"\n{INTRO_END}\n",
            "a heading or a comment",
        ),
        (_readme(f"See [the site]({render_overview.SITE_URL})."), "links the site"),
    ],
)
def test_a_malformed_introduction_block_is_refused(readme: str, refusal: str) -> None:
    with pytest.raises(ValueError, match=refusal):
        intro_block(readme)


#: A tree with what README's introduction links: the registers, a case file, a document
#: served as a page, and a review that is only in the repository.
INTRO_TREE = RepositoryTree(
    files=frozenset(
        {
            "packing/frontier/RESULTS.md",
            "packing/frontier/STATUS.md",
            "packing/frontier/n-011.md",
            "docs/review.md",
            "epistemics.md",
        }
    ),
    directories=frozenset({"", "docs", "packing", "packing/frontier"}),
)


def _overview(intro: str, progress: str = "<p>What the project covers.</p>") -> str:
    outside = '<p><a href="packing/frontier/RESULTS.md">outside the block</a></p>'
    return (
        f"{outside}{OVERVIEW_INTRO_OPEN}{intro}{OVERVIEW_INTRO_CLOSE}{outside}"
        f"{PROGRESS.opened}{progress}{PROGRESS.closed}{outside}"
    )


def test_the_introductions_links_reach_the_sites_own_pages(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A result's id goes to its row, the registers to the results table and the
    frontier atlas, a case file to its record, a served document to its page, and any
    other path to `main`; nothing outside the block is touched."""
    monkeypatch.setattr(site_documents, "repository_tree", lambda: INTRO_TREE)
    out = rewrite_overview_blocks(
        _overview(
            '<p><a href="packing/frontier/RESULTS.md">T-060</a> '
            '<a href="packing/frontier/RESULTS.md">results register</a> '
            '<a href="packing/frontier/STATUS.md">frontier</a> '
            '<a href="packing/frontier/n-011.md">case record</a> '
            '<a href="epistemics.md">the rungs</a> '
            '<a href="docs/review.md">review</a> '
            '<a href="https://example.org/proof">the proof</a></p>'
        )
    )
    intro = out.split(OVERVIEW_INTRO_OPEN, 1)[1].split(OVERVIEW_INTRO_CLOSE, 1)[0]
    assert re.findall(r'<a href="([^"]+)">([^<]+)</a>', intro) == [
        ("all-results.html#t-060", "T-060"),
        ("all-results.html", "results register"),
        ("frontier.html", "frontier"),
        ("cases.html#n-11", "case record"),
        ("epistemics.html", "the rungs"),
        (f"{REPO_URL}/blob/{BRANCH}/docs/review.md", "review"),
        ("https://example.org/proof", "the proof"),
    ]
    assert out.count('<a href="packing/frontier/RESULTS.md">outside the block</a>') == 3


def test_both_shared_blocks_have_their_links_rewritten(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The block that opens Recent Results is rewritten as the first section's is, and
    what lies between the two blocks is left as it was."""
    monkeypatch.setattr(site_documents, "repository_tree", lambda: INTRO_TREE)
    out = rewrite_overview_blocks(
        _overview(
            '<p><a href="packing/frontier/STATUS.md">frontier</a></p>',
            '<p><a href="packing/frontier/RESULTS.md">T-060</a> '
            '<a href="packing/frontier/n-011.md">case record</a></p>',
        )
    )
    progress = out.split(PROGRESS.opened, 1)[1].split(PROGRESS.closed, 1)[0]
    assert re.findall(r'<a href="([^"]+)">([^<]+)</a>', progress) == [
        ("all-results.html#t-060", "T-060"),
        ("cases.html#n-11", "case record"),
    ]
    intro = out.split(OVERVIEW_INTRO_OPEN, 1)[1].split(OVERVIEW_INTRO_CLOSE, 1)[0]
    assert intro == '<p><a href="frontier.html">frontier</a></p>'
    assert out.count('<a href="packing/frontier/RESULTS.md">outside the block</a>') == 3


def test_the_overview_fails_on_an_unresolved_introduction_link(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(site_documents, "repository_tree", lambda: INTRO_TREE)
    with pytest.raises(SystemExit, match="1 unresolved links in README's introduction"):
        rewrite_overview_blocks(_overview('<p><a href="docs/gone.md">gone</a></p>'))
    with pytest.raises(SystemExit, match="1 unresolved links in README's introduction"):
        rewrite_overview_blocks(
            _overview("<p>Fine.</p>", '<p><a href="docs/gone.md">gone</a></p>')
        )
    with pytest.raises(SystemExit, match="project-intro block is not marked in the page"):
        rewrite_overview_blocks('<p><a href="docs/review.md">no markers</a></p>')
    unmarked = f"{OVERVIEW_INTRO_OPEN}<p>Fine.</p>{OVERVIEW_INTRO_CLOSE}"
    with pytest.raises(SystemExit, match="recent-progress block is not marked in the page"):
        rewrite_overview_blocks(unmarked)
