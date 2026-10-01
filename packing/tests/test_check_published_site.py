"""The live-site check's parsing, on fixtures: the network half is not a unit of the gate."""

from __future__ import annotations

import hashlib
from collections.abc import Callable, Sequence
from pathlib import Path

import pytest

from devtools import check_published_site, render_overview
from devtools import render_n11_lower_bounds_explainer_pdf as pdf
from devtools.check_published_site import (
    EXPLAINER,
    LINK_CHECKED_PAGES,
    OPTIMALITY_PAPER,
    OPTIMALITY_PAPER_FILES,
    OPTIMALITY_PAPER_MARKDOWN,
    PAPERS_CURRENT,
    SERVED,
    SITE_PAGES,
    WORKBENCH_HOME,
    WORKBENCH_REVISION,
    paper_citations,
    pdf_pages,
    repository_links,
)
from devtools.render_n11_lower_bounds_explainer import (
    COMPOSITE_ASSETS,
    MARKDOWN_OUTPUT,
    PAGE_URL,
)
from devtools.render_n11_lower_bounds_explainer_pdf import EXPECTED_PAGE_COUNT
from devtools.render_n11_lower_bounds_explainer_pdf import OUTPUT as PDF_OUTPUT
from devtools.repo_links import DEFAULT_BRANCH, REPO_URL, RepositoryTree
from sqpack.release import PUBLICATION_EDITION

#: A page's text linking into the repository four ways: from markup, from Markdown, from plain
#: text, and from inside a script, which the check must not read. `{{REPO_URL}}` and `{{SHA}}`
#: are filled in by the test; the script makes it a page, so it is a fixture and not a string.
REPOSITORY_LINKS = (
    Path(__file__).resolve().parent
    / "fixtures"
    / "check_published_site"
    / "repository-links.html"
)

COMMIT = "0123456789abcdef0123456789abcdef01234567"

#: The tree `main` holds at the deploy: every path a fixture page links on `main`.
TREE = RepositoryTree(
    files=frozenset({"README.md", *(f"packing/{name}.md" for name in SITE_PAGES)}),
    directories=frozenset({"", "packing"}),
)

Fetch = Callable[..., tuple[int, bytes]]


def workbench_page(commit: str, *, home: str = "../") -> bytes:
    return (
        f'<meta name="squares-workbench-revision" content="{commit}">'
        f'<div id="site-note"><a href="{home}">the overview</a></div>'
    ).encode()


def source_receipt(page: bytes) -> bytes:
    return f"\n%sqpack-source-html-sha256: {hashlib.sha256(page).hexdigest()}\n".encode()


def page(
    canonical: str,
    *,
    ref: str = DEFAULT_BRANCH,
    stamp: str = PUBLICATION_EDITION,
    link: str = "README.md",
) -> bytes:
    """A served page as the check reads one: a canonical link, the stamp, a repository link."""
    return (
        f'<link rel="canonical" href="{canonical}">'
        f'<p>({stamp})</p><a href="{REPO_URL}/blob/{ref}/{link}">Repository</a>'
    ).encode()


#: The result overviews the fixture's results table names, by address beside the pages.
OVERVIEWS = ("result/t-001.html", "result/t-002.html")


def result_overview(
    result_id: str, *, ref: str = DEFAULT_BRANCH, link: str = "README.md"
) -> bytes:
    """A result's overview as it is served: the one block, with a repository link."""
    return (
        f'<div class="site-result" data-result-overview="{result_id}">'
        f'<a href="{REPO_URL}/blob/{ref}/{link}">Register</a></div>\n'
    ).encode()


def optimality_paper(*, ref: str = COMMIT, link: str = "README.md") -> bytes:
    """The optimality paper's page as the check reads one: the bar with Papers current,
    and one citation, which the paper pins to the commit it was built from."""
    return (
        PAPERS_CURRENT + f'Papers</a><a href="{REPO_URL}/blob/{ref}/{link}#anchor">Receipt</a>'
    ).encode()


def optimality_markdown(*, ref: str = COMMIT, link: str = "README.md") -> bytes:
    """The paper's Markdown, with the same citation as a Markdown link."""
    return f"[Receipt]({REPO_URL}/blob/{ref}/{link}#anchor)\n".encode()


def site_pages(**overrides: bytes) -> dict[str, bytes]:
    """Every page a good deploy serves, by served name, each named as its renderer names it,
    and the result overviews its results table names, by their address."""
    return site_naming(OVERVIEWS, **overrides)


def site_naming(named: Sequence[str], /, **overrides: bytes) -> dict[str, bytes]:
    """`site_pages`, with the results table, whichever page stands for it, naming the
    overviews in `named`."""
    pages = {
        name: page(render_overview.canonical_url(name), link=f"packing/{name}.md")
        for name in SITE_PAGES
    }
    pages[EXPLAINER] = page(PAGE_URL)
    for address in OVERVIEWS:
        pages[address] = result_overview(address.rsplit("/", 1)[1].removesuffix(".html"))
    pages[OPTIMALITY_PAPER] = optimality_paper()
    pages[OPTIMALITY_PAPER_MARKDOWN] = optimality_markdown()
    pages.update(overrides)
    pages[render_overview.RESULTS_PAGE] += "".join(
        f'<div class="site-row-pop-body" data-row-pop-src="{address}"></div>'
        for address in named
    ).encode()
    return pages


def fake_site(
    pages: dict[str, bytes],
    *,
    workbench: bytes | None = None,
    pdf_page_count: int = EXPECTED_PAGE_COUNT,
    receipt: bytes | None = None,
    requested: list[str] | None = None,
    lost: Sequence[str] = (),
) -> Fetch:
    """A deployed site at any root: its pages, the workbench, the PDF, and every link.
    An address ending in one of `lost` is a 404."""

    def fetch(url: str, *, head: bool = False, timeout: float = 30.0) -> tuple[int, bytes]:
        assert timeout == 1
        if requested is not None:
            requested.append(url)
        if any(url.endswith(name) for name in lost):
            return 404, b"Not found"
        if url.startswith(REPO_URL):
            return 200, b""
        if url.endswith("/workbench/"):
            return 200, workbench if workbench is not None else workbench_page(COMMIT)
        if url.endswith(".pdf"):
            pages_ = b"1 0 obj << /Type /Page >> endobj\n" * pdf_page_count
            tail = receipt if receipt is not None else source_receipt(pages[EXPLAINER])
            return 200, b"%PDF-1.7\n" + pages_ + b"%%EOF" + tail
        name = "index.html" if url.endswith("/") else url.rsplit("/", 1)[1]
        nested = "/".join(url.rsplit("/", 2)[1:])
        if nested.startswith("result/") and nested not in pages:
            return 404, b"Not found"
        body = pages.get(nested, pages.get(name, b"served"))
        return 200, b"" if head else body

    return fetch


def failures(
    monkeypatch: pytest.MonkeyPatch,
    fetch: Fetch,
    *,
    site: str = "https://example.org",
    browser: bool = False,
) -> list[str]:
    monkeypatch.setattr(check_published_site, "fetch", fetch)
    monkeypatch.setattr(
        check_published_site,
        "repository_tree",
        lambda commit: TREE if commit == COMMIT else None,
    )
    return [
        line
        for passed, line in check_published_site.check(site, COMMIT, timeout=1, browser=browser)
        if not passed
    ]


def test_repository_links_are_read_from_markup_and_markdown_but_not_from_scripts() -> None:
    sha = "0123456789abcdef0123456789abcdef01234567"
    text = (
        REPOSITORY_LINKS.read_text(encoding="utf-8")
        .replace("{{REPO_URL}}", REPO_URL)
        .replace("{{SHA}}", sha)
    )
    assert repository_links(text) == {
        ("blob", sha, "packing/a.py"),
        ("tree", sha, "packing/atlas/known-best"),
        ("blob", "main", "README.md"),
    }


def test_pdf_pages_counts_page_objects_and_refuses_what_is_not_a_pdf() -> None:
    pdf = b"%PDF-1.7\n1 0 obj << /Type /Pages /Kids [2 0 R 3 0 R] >> endobj\n"
    pdf += b"2 0 obj << /Type /Page >> endobj\n3 0 obj << /Type/Page >> endobj\n%%EOF"
    assert pdf_pages(pdf) == 2
    assert pdf_pages(b"<html>not a pdf</html>") == 0


def test_the_served_files_are_the_markdown_edition_the_pdf_and_the_composite_assets() -> None:
    assert SERVED[0] == MARKDOWN_OUTPUT.name
    assert SERVED[1] == PDF_OUTPUT.name
    assert set(SERVED[2:]) == {asset.name for asset in COMPOSITE_ASSETS}


def test_the_checked_pages_are_every_page_the_site_serves_but_the_workbench() -> None:
    """The overview's renderer is the list: a page added there is checked without an edit.

    The explainer moved to `explainer.html` when the overview took the root, and the
    checker names it from the explainer's own canonical URL, so the two cannot disagree.
    """
    assert tuple(render_overview.PAGES) == SITE_PAGES
    assert SITE_PAGES.index("index.html") == 0
    assert PAGE_URL.endswith(f"/{EXPLAINER}")
    assert EXPLAINER.endswith(".html")
    assert {*SITE_PAGES, EXPLAINER, "workbench/index.html"} <= set(render_overview.SITE_PAGES)
    assert {"index.html", "frontier.html", "all-results.html"} == LINK_CHECKED_PAGES
    assert render_overview.canonical_url("index.html") == check_published_site.SITE_URL
    assert render_overview.canonical_url("tutorial.html").endswith("/squares/tutorial.html")
    # The papers page was added to the renderer alone, and is checked here for it.
    assert "papers.html" in SITE_PAGES
    assert render_overview.canonical_url("papers.html").endswith("/squares/papers.html")


def test_live_source_check_accepts_the_receipt_written_by_the_pdf_exporter(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    page = tmp_path / "index.html"
    page.write_bytes(b"<html>the exact publication source</html>\n")
    output = tmp_path / "explainer.pdf"
    monkeypatch.setattr(pdf, "PAGE", page)
    monkeypatch.setattr(pdf, "OUTPUT", output)
    monkeypatch.setattr(pdf, "render_pdf_bytes", lambda: b"%PDF-1.7\n%%EOF\n")
    pdf.update()
    assert check_published_site.pdf_source_matches(output.read_bytes(), page.read_bytes())


def test_check_accepts_the_requested_build_and_rejects_a_stale_stamp(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    requested: list[str] = []
    assert failures(monkeypatch, fake_site(site_pages(), requested=requested)) == []
    assert "https://example.org/" in requested
    assert f"https://example.org/{EXPLAINER}" in requested
    assert "https://example.org/index.html" not in requested, "the overview is the root"

    stale = site_pages(**{EXPLAINER: page(PAGE_URL, stamp="v0.0.0-deadbe")})
    (failure,) = failures(monkeypatch, fake_site(stale))
    assert "edition stamp" in failure
    assert EXPLAINER in failure

    stale = site_pages(**{"index.html": page(render_overview.SITE_URL, stamp="v0.0.0-deadbe")})
    (failure,) = failures(monkeypatch, fake_site(stale))
    assert "edition stamp" in failure
    assert "index.html" in failure


def test_check_requires_each_page_to_name_its_own_canonical_url(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A page served under another's name, or the explainer still claiming the root.

    The explainer's canonical URL is how a search engine and a share card find it; one
    left at `/` after the move would point both at the overview.
    """
    swapped = site_pages(**{EXPLAINER: page(render_overview.SITE_URL)})
    (failure,) = failures(monkeypatch, fake_site(swapped))
    assert f"{EXPLAINER} names canonical URL" in failure

    for name in SITE_PAGES:
        wrong = site_pages(**{name: page(PAGE_URL)})
        (failure,) = failures(monkeypatch, fake_site(wrong))
        assert f"{name} names canonical URL" in failure, name

    missing = site_pages(**{"index.html": b"<p>(" + PUBLICATION_EDITION.encode() + b")</p>"})
    found = failures(monkeypatch, fake_site(missing))
    assert any("index.html names canonical URL None" in line for line in found), found


def test_check_refuses_a_repository_link_pinned_to_a_commit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A link to the commit a page was built from 404s once a squash merge leaves that
    commit on no branch, so every page, full hash or short, is held to `main`.

    Only the overview, the frontier atlas and the explainer have each link asked of
    GitHub as well.
    """
    for name in SITE_PAGES:
        for ref in (COMMIT, COMMIT[:8]):
            pinned = page(render_overview.canonical_url(name), ref=ref)
            found = failures(monkeypatch, fake_site(site_pages(**{name: pinned})))
            url = f"{REPO_URL}/blob/{ref}/README.md"
            assert found == [f"{name}: 1 repository links pinned to a commit: [{url!r}]"], (
                name,
                found,
            )

    requested: list[str] = []
    assert failures(monkeypatch, fake_site(site_pages(), requested=requested)) == []
    asked = {url.removeprefix(f"{REPO_URL}/blob/{DEFAULT_BRANCH}/") for url in requested}
    for name in SITE_PAGES:
        assert (f"packing/{name}.md" in asked) == (name in LINK_CHECKED_PAGES), name
    assert "README.md" in asked, "the explainer's links are still asked"


def test_check_requires_every_path_linked_on_main_to_be_in_the_commit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A path on `main` that the deployed commit's tree lacks is a 404 from the start."""
    for name in SITE_PAGES:
        gone = page(render_overview.canonical_url(name), link="packing/gone.md")
        found = failures(monkeypatch, fake_site(site_pages(**{name: gone})))
        assert found == [
            f"{name}: linked on main but not in {COMMIT[:12]}: ['blob/packing/gone.md']"
        ], name


def test_check_requires_every_result_overview_the_results_table_names(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A row's popover fetches its result's overview from beside the page, so a deploy
    without one, or with another result's under its name, shows only as a popover that
    keeps its short detail. Each named overview is asked for, and its repository links
    are held to `main` and to the commit's tree as a page's are."""
    requested: list[str] = []
    assert failures(monkeypatch, fake_site(site_pages(), requested=requested)) == []
    for address in OVERVIEWS:
        assert f"https://example.org/{address}" in requested

    lost = site_naming((*OVERVIEWS, "result/t-003.html"))
    assert failures(monkeypatch, fake_site(lost)) == [
        "result overview result/t-003.html: HTTP 404, 9 bytes, but it is None"
    ]

    swapped = site_pages(**{"result/t-002.html": result_overview("t-001")})
    (failure,) = failures(monkeypatch, fake_site(swapped))
    assert failure.startswith("result overview result/t-002.html: HTTP 200, ")
    assert failure.endswith("but it is 'result/t-001.html'")

    assert failures(monkeypatch, fake_site(site_naming(()))) == [
        "all-results.html names 0 result overviews"
    ]

    pinned = site_pages(**{"result/t-001.html": result_overview("t-001", ref=COMMIT[:8])})
    url = f"{REPO_URL}/blob/{COMMIT[:8]}/README.md"
    assert failures(monkeypatch, fake_site(pinned)) == [
        f"the result overviews: 1 repository links pinned to a commit: [{url!r}]"
    ]

    gone = site_pages(**{"result/t-001.html": result_overview("t-001", link="packing/gone.md")})
    missing = f"linked on main but not in {COMMIT[:12]}: ['blob/packing/gone.md']"
    assert failures(monkeypatch, fake_site(gone)) == [f"the result overviews: {missing}"]


def test_check_requires_the_optimality_paper_where_the_papers_card_points(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The Papers page's first card opens the optimality paper, which another build
    writes into a directory of its own: a deploy without it, or with a page there whose
    bar does not mark Papers, fails, and so does one without its landing address, its
    Markdown or its PDF."""
    assert OPTIMALITY_PAPER == "n11-optimality/t-060-explainer.html"
    assert OPTIMALITY_PAPER in render_overview.SITE_PAGES
    assert OPTIMALITY_PAPER_FILES == (
        "n11-optimality/",
        "n11-optimality/t-060-explainer.md",
        "n11-optimality/t-060-explainer.pdf",
    )
    requested: list[str] = []
    assert failures(monkeypatch, fake_site(site_pages(), requested=requested)) == []
    for name in (OPTIMALITY_PAPER, *OPTIMALITY_PAPER_FILES):
        assert f"https://example.org/{name}" in requested, name

    (failure,) = failures(monkeypatch, fake_site(site_pages(), lost=(OPTIMALITY_PAPER,)))
    assert failure.startswith(f"optimality paper {OPTIMALITY_PAPER}: HTTP 404, ")
    assert failure.endswith("Papers is not the bar's current entry")

    bare = site_pages(
        **{OPTIMALITY_PAPER: optimality_paper().replace(b' aria-current="page"', b"")}
    )
    (failure,) = failures(monkeypatch, fake_site(bare))
    assert failure.startswith(f"optimality paper {OPTIMALITY_PAPER}: HTTP 200, ")
    assert failure.endswith("Papers is not the bar's current entry")

    for name in OPTIMALITY_PAPER_FILES[1:]:
        assert failures(monkeypatch, fake_site(site_pages(), lost=(name,))) == [
            f"served {name}: HTTP 404"
        ]


def test_the_optimality_papers_citations_name_the_deployed_commit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The paper is the one page whose repository links are held to a commit and not to
    `main`: it cites the evidence as it stood when it was typeset, and the deploy builds
    it from the commit it deploys, which `main` keeps. So each citation, on the page and
    in its Markdown, names the expected commit, and every cited path is in that commit's
    tree. A citation on `main` or at another commit fails, as does a page with none and
    a cited path the tree lacks."""
    assert OPTIMALITY_PAPER_MARKDOWN == "n11-optimality/t-060-explainer.md"
    assert OPTIMALITY_PAPER_MARKDOWN in OPTIMALITY_PAPER_FILES
    other = "f" * 40
    text = (
        f'<a href="{REPO_URL}/blob/{COMMIT}/packing/a.md#part">a</a>'
        f'<a href="{REPO_URL}/blob/{COMMIT}/packing/b.json?plain=1">b</a>'
        f'<a href="{REPO_URL}/blob/main/README.md">c</a>'
        f'<a href="{REPO_URL}/tree/{other}/packing">d</a>'
        f'<a href="{REPO_URL}">the repository itself is not a citation</a>'
    )
    assert paper_citations(text, COMMIT) == (
        {("blob", "packing/a.md"), ("blob", "packing/b.json")},
        ["blob/main/README.md", f"tree/{other}/packing"],
    )

    requested: list[str] = []
    assert failures(monkeypatch, fake_site(site_pages(), requested=requested)) == []
    assert f"https://example.org/{OPTIMALITY_PAPER_MARKDOWN}" in requested

    for name, made in (
        (OPTIMALITY_PAPER, optimality_paper),
        (OPTIMALITY_PAPER_MARKDOWN, optimality_markdown),
    ):
        stray = f"{name}: 1 repository links not pinned to {COMMIT[:12]}: "
        on_main = site_pages(**{name: made(ref=DEFAULT_BRANCH)})
        assert failures(monkeypatch, fake_site(on_main)) == [
            stray + "['blob/main/README.md#anchor']"
        ]
        elsewhere = site_pages(**{name: made(ref=other)})
        assert failures(monkeypatch, fake_site(elsewhere)) == [
            stray + f"['blob/{other}/README.md#anchor']"
        ]
        gone = site_pages(**{name: made(link="packing/gone.md")})
        assert failures(monkeypatch, fake_site(gone)) == [
            f"{name}: cited at {COMMIT[:12]} but not in its tree: ['blob/packing/gone.md']"
        ]
    uncited = site_pages(**{OPTIMALITY_PAPER_MARKDOWN: b"# A paper citing nothing\n"})
    assert failures(monkeypatch, fake_site(uncited)) == [
        f"{OPTIMALITY_PAPER_MARKDOWN}: 0 citations, each pinned to {COMMIT[:12]}"
    ]


def test_check_fails_when_the_commit_tree_cannot_be_read(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def unreadable(commit: str) -> RepositoryTree:
        raise SystemExit(f"git ls-tree {commit} failed")

    monkeypatch.setattr(check_published_site, "fetch", fake_site(site_pages()))
    monkeypatch.setattr(check_published_site, "repository_tree", unreadable)
    found = [
        line
        for passed, line in check_published_site.check(
            "https://example.org", COMMIT, timeout=1, browser=False
        )
        if not passed
    ]
    assert found == [f"the tree of {COMMIT} cannot be read here: git ls-tree {COMMIT} failed"]


def test_check_rejects_a_deployed_pdf_that_crossed_a_page_boundary(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    found = failures(
        monkeypatch, fake_site(site_pages(), pdf_page_count=EXPECTED_PAGE_COUNT + 1)
    )
    assert len(found) == 1
    assert f"{EXPECTED_PAGE_COUNT + 1} pages (expected {EXPECTED_PAGE_COUNT})" in found[0]


def test_workbench_receipt_parses_exact_revision_and_project_relative_home() -> None:
    commit = "0123456789abcdef0123456789abcdef01234567"
    text = workbench_page(commit).decode()
    revision = WORKBENCH_REVISION.search(text)
    home = WORKBENCH_HOME.search(text)
    assert revision is not None
    assert revision.group(1) == commit
    assert home is not None
    assert home.group(1) == "../"


def test_check_rejects_a_stale_workbench_or_account_root_navigation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    found = failures(
        monkeypatch,
        fake_site(site_pages(), workbench=workbench_page("f" * 40, home="/")),
        site="https://example.org/squares",
    )
    assert len(found) == 2
    assert "workbench source revision" in found[0]
    assert "workbench home resolves" in found[1]


def test_check_requires_the_workbench_browser_api_to_start(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        check_published_site,
        "workbench_startup",
        lambda _url, _root, *, timeout: (False, f"API missing after {timeout}s"),
    )
    assert failures(monkeypatch, fake_site(site_pages()), browser=True) == [
        "API missing after 1s"
    ]


@pytest.mark.parametrize(
    "receipt_kind",
    ["missing", "malformed", "wrong-source", "duplicate", "uppercase", "trailing-data"],
)
def test_check_rejects_a_pdf_without_the_deployed_html_source_receipt(
    monkeypatch: pytest.MonkeyPatch, receipt_kind: str
) -> None:
    pages = site_pages()
    explainer = pages[EXPLAINER]
    valid = source_receipt(explainer)
    receipt = {
        "missing": b"",
        "malformed": b"\n%sqpack-source-html-sha256: not-a-digest\n",
        "wrong-source": source_receipt(explainer + b"<!-- old source -->"),
        "duplicate": valid + valid,
        "uppercase": valid[: valid.index(b":") + 1] + valid[valid.index(b":") + 1 :].upper(),
        "trailing-data": valid + b"unbound suffix",
    }[receipt_kind]
    found = failures(monkeypatch, fake_site(pages, receipt=receipt))
    assert len(found) == 1
    assert "source HTML receipt" in found[0]


def test_check_compares_the_exact_fetched_html_bytes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    pages = site_pages(**{EXPLAINER: page(PAGE_URL) + b"<!-- byte-exact source: \xff -->"})
    assert failures(monkeypatch, fake_site(pages)) == []

    overview_receipt = source_receipt(pages["index.html"])
    (found,) = failures(monkeypatch, fake_site(pages, receipt=overview_receipt))
    assert "source HTML receipt" in found, "the receipt names the explainer, not the root"


def test_fetch_retries_a_transient_answer_before_reporting_it(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Pages can answer 404 or 5xx for a short while after a deploy reports success, and
    the check runs straight after it (#160 R26). A lasting answer is still reported."""
    answers = [(404, b""), (503, b""), (200, b"page")]
    pauses: list[float] = []
    monkeypatch.setattr(
        check_published_site, "fetch_once", lambda _url, **_kwargs: answers.pop(0)
    )
    status = check_published_site.fetch(
        "https://example.org/", timeout=1, delays=(1.0, 2.0, 4.0), sleep=pauses.append
    )
    assert status == (200, b"page")
    assert pauses == [1.0, 2.0]

    pauses.clear()
    monkeypatch.setattr(check_published_site, "fetch_once", lambda _url, **_kwargs: (0, b""))
    status = check_published_site.fetch(
        "https://example.org/", timeout=1, delays=(1.0, 2.0), sleep=pauses.append
    )
    assert status == (0, b"")
    assert pauses == [1.0, 2.0]

    pauses.clear()
    monkeypatch.setattr(check_published_site, "fetch_once", lambda _url, **_kwargs: (403, b""))
    status = check_published_site.fetch(
        "https://example.org/", timeout=1, delays=(1.0, 2.0), sleep=pauses.append
    )
    assert status == (403, b"")
    assert pauses == [], "a refusal is an answer, not a deploy still settling"
