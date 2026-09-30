"""The live-site check's parsing, on fixtures: the network half is not a unit of the gate."""

from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from devtools import check_published_site
from devtools import render_explainer_pdf as pdf
from devtools.check_published_site import (
    SERVED,
    WORKBENCH_HOME,
    WORKBENCH_REVISION,
    pdf_pages,
    repository_links,
)
from devtools.render_explainer import COMPOSITE_ASSETS, MARKDOWN_OUTPUT, REPO_URL
from devtools.render_explainer_pdf import EXPECTED_PAGE_COUNT
from devtools.render_explainer_pdf import OUTPUT as PDF_OUTPUT
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


def workbench_page(commit: str, *, home: str = "../") -> bytes:
    return (
        f'<meta name="squares-workbench-revision" content="{commit}">'
        f'<div id="site-note"><a href="{home}">Square Packing</a></div>'
    ).encode()


def source_receipt(page: bytes) -> bytes:
    return f"\n%sqpack-source-html-sha256: {hashlib.sha256(page).hexdigest()}\n".encode()


EXPLAINER = check_published_site.EXPLAINER_PAGE


def as_served(page: bytes, url: str) -> bytes:
    """The fixture page as the site serves it at `url`, declaring its own canonical URL."""
    name = url.rstrip("/").rsplit("/", 1)[-1]
    name = name if name.endswith(".html") else "index.html"
    canonical = check_published_site.canonical_url(name)
    return f'<link rel="canonical" href="{canonical}">'.encode() + page


@pytest.fixture(autouse=True)
def served_media(monkeypatch: pytest.MonkeyPatch) -> list[list[str]]:
    """The media check asks the network, so each test sees the paths it would ask for."""
    asked: list[list[str]] = []

    def check_media(_site: str, paths: object) -> list[str]:
        asked.append(list(paths))  # pyright: ignore[reportArgumentType]
        return []

    monkeypatch.setattr(check_published_site.published_media, "check_media", check_media)
    return asked


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
    commit = "0123456789abcdef0123456789abcdef01234567"
    stamp = PUBLICATION_EDITION
    link = f'<a href="{REPO_URL}/blob/{commit}/README.md">Repository</a>'
    page = f"<p>({stamp})</p>{link}".encode()

    def fetch(url: str, *, head: bool = False, timeout: float = 30.0) -> tuple[int, bytes]:
        assert timeout == 1
        if url.endswith("/workbench/"):
            return 200, workbench_page(commit)
        if url.endswith(".pdf"):
            pages = b"1 0 obj << /Type /Page >> endobj\n" * EXPECTED_PAGE_COUNT
            return 200, b"%PDF-1.7\n" + pages + b"%%EOF" + source_receipt(
                as_served(page, EXPLAINER)
            )
        return 200, b"" if head else as_served(page, url)

    monkeypatch.setattr(check_published_site, "fetch", fetch)
    results = check_published_site.check(
        "https://example.org", commit, timeout=1, browser=False
    )
    assert all(passed for passed, _ in results), results

    page = f"<p>({stamp.replace(PUBLICATION_EDITION, 'v0.0.0-deadbe')})</p>{link}".encode()
    failures = [
        line
        for passed, line in check_published_site.check(
            "https://example.org", commit, timeout=1, browser=False
        )
        if not passed
    ]
    # The overview, the frontier atlas, the tutorial and the explainer each carry the stamp.
    assert len(failures) == 4
    assert all("edition stamp" in line for line in failures)


def test_check_rejects_a_deployed_pdf_that_crossed_a_page_boundary(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    commit = "0123456789abcdef0123456789abcdef01234567"
    stamp = PUBLICATION_EDITION
    page = (
        f'<p>({stamp})</p><a href="{REPO_URL}/blob/{commit}/README.md">Repository</a>'
    ).encode()

    def fetch(url: str, *, head: bool = False, timeout: float = 30.0) -> tuple[int, bytes]:
        assert timeout == 1
        if url.endswith("/workbench/"):
            return 200, workbench_page(commit)
        if url.endswith(".pdf"):
            pages = b"1 0 obj << /Type /Page >> endobj\n" * (EXPECTED_PAGE_COUNT + 1)
            return 200, b"%PDF-1.7\n" + pages + b"%%EOF" + source_receipt(
                as_served(page, EXPLAINER)
            )
        return 200, b"" if head else as_served(page, url)

    monkeypatch.setattr(check_published_site, "fetch", fetch)
    failures = [
        line
        for passed, line in check_published_site.check(
            "https://example.org", commit, timeout=1, browser=False
        )
        if not passed
    ]
    assert len(failures) == 1
    assert f"{EXPECTED_PAGE_COUNT + 1} pages (expected {EXPECTED_PAGE_COUNT})" in failures[0]


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
    commit = "0123456789abcdef0123456789abcdef01234567"
    stamp = PUBLICATION_EDITION
    page = (
        f'<p>({stamp})</p><a href="{REPO_URL}/blob/{commit}/README.md">Repository</a>'
    ).encode()

    def fetch(url: str, *, head: bool = False, timeout: float = 30.0) -> tuple[int, bytes]:
        assert timeout == 1
        if url.endswith("/workbench/"):
            return 200, workbench_page("f" * 40, home="/")
        if url.endswith(".pdf"):
            pages = b"1 0 obj << /Type /Page >> endobj\n" * EXPECTED_PAGE_COUNT
            return 200, b"%PDF-1.7\n" + pages + b"%%EOF" + source_receipt(
                as_served(page, EXPLAINER)
            )
        return 200, b"" if head else as_served(page, url)

    monkeypatch.setattr(check_published_site, "fetch", fetch)
    failures = [
        line
        for passed, line in check_published_site.check(
            "https://example.org/squares", commit, timeout=1, browser=False
        )
        if not passed
    ]
    assert len(failures) == 2
    assert "workbench source revision" in failures[0]
    assert "workbench home resolves" in failures[1]


def test_check_requires_the_workbench_browser_api_to_start(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    commit = "0123456789abcdef0123456789abcdef01234567"
    stamp = PUBLICATION_EDITION
    page = (
        f'<p>({stamp})</p><a href="{REPO_URL}/blob/{commit}/README.md">Repository</a>'
    ).encode()

    def fetch(url: str, *, head: bool = False, timeout: float = 30.0) -> tuple[int, bytes]:
        assert timeout == 1
        if url.endswith("/workbench/"):
            return 200, workbench_page(commit)
        if url.endswith(".pdf"):
            pages = b"1 0 obj << /Type /Page >> endobj\n" * EXPECTED_PAGE_COUNT
            return 200, b"%PDF-1.7\n" + pages + b"%%EOF" + source_receipt(
                as_served(page, EXPLAINER)
            )
        return 200, b"" if head else as_served(page, url)

    monkeypatch.setattr(check_published_site, "fetch", fetch)
    monkeypatch.setattr(
        check_published_site,
        "workbench_startup",
        lambda _url, _root, *, timeout: (False, f"API missing after {timeout}s"),
    )
    failures = [
        line
        for passed, line in check_published_site.check("https://example.org", commit, timeout=1)
        if not passed
    ]
    assert failures == ["API missing after 1s"]


@pytest.mark.parametrize(
    "receipt_kind",
    ["missing", "malformed", "wrong-source", "duplicate", "uppercase", "trailing-data"],
)
def test_check_rejects_a_pdf_without_the_deployed_html_source_receipt(
    monkeypatch: pytest.MonkeyPatch, receipt_kind: str
) -> None:
    commit = "0123456789abcdef0123456789abcdef01234567"
    stamp = PUBLICATION_EDITION
    page = (
        f'<p>({stamp})</p><a href="{REPO_URL}/blob/{commit}/README.md">Repository</a>'
    ).encode()
    valid = source_receipt(as_served(page, EXPLAINER))
    receipt = {
        "missing": b"",
        "malformed": b"\n%sqpack-source-html-sha256: not-a-digest\n",
        "wrong-source": source_receipt(as_served(page, EXPLAINER) + b"<!-- old source -->"),
        "duplicate": valid + valid,
        "uppercase": valid[: valid.index(b":") + 1] + valid[valid.index(b":") + 1 :].upper(),
        "trailing-data": valid + b"unbound suffix",
    }[receipt_kind]

    def fetch(url: str, *, head: bool = False, timeout: float = 30.0) -> tuple[int, bytes]:
        assert timeout == 1
        if url.endswith("/workbench/"):
            return 200, workbench_page(commit)
        if url.endswith(".pdf"):
            pages = b"1 0 obj << /Type /Page >> endobj\n" * EXPECTED_PAGE_COUNT
            return 200, b"%PDF-1.7\n" + pages + b"%%EOF" + receipt
        return 200, b"" if head else as_served(page, url)

    monkeypatch.setattr(check_published_site, "fetch", fetch)
    failures = [
        line
        for passed, line in check_published_site.check(
            "https://example.org", commit, timeout=1, browser=False
        )
        if not passed
    ]
    assert len(failures) == 1
    assert "source HTML receipt" in failures[0]


def test_check_compares_the_exact_fetched_html_bytes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    commit = "0123456789abcdef0123456789abcdef01234567"
    stamp = PUBLICATION_EDITION
    page = (
        f'<p>({stamp})</p><a href="{REPO_URL}/blob/{commit}/README.md">Repository</a>'
    ).encode() + b"<!-- byte-exact source: \xff -->"

    def fetch(url: str, *, head: bool = False, timeout: float = 30.0) -> tuple[int, bytes]:
        assert timeout == 1
        if url.endswith("/workbench/"):
            return 200, workbench_page(commit)
        if url.endswith(".pdf"):
            pages = b"1 0 obj << /Type /Page >> endobj\n" * EXPECTED_PAGE_COUNT
            return 200, b"%PDF-1.7\n" + pages + b"%%EOF" + source_receipt(
                as_served(page, EXPLAINER)
            )
        return 200, b"" if head else as_served(page, url)

    monkeypatch.setattr(check_published_site, "fetch", fetch)
    results = check_published_site.check(
        "https://example.org", commit, timeout=1, browser=False
    )
    assert all(passed for passed, _ in results), results


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


def test_site_pages_accept_main_only_for_the_links_they_declare(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A document card on the default branch passes; an undeclared `main` link fails."""
    commit = "0123456789abcdef0123456789abcdef01234567"
    card = f"{REPO_URL}/blob/main/SYNOPSIS.md"
    island = (
        f'<script type="application/json" id="site-default-branch-links">["{card}"]</script>'
    )
    page = (
        f"<p>({PUBLICATION_EDITION})</p>"
        f'<a href="{REPO_URL}/blob/{commit}/README.md">record</a>'
        f'<a href="{card}">card</a>{island}'
    ).encode()
    explainer = (
        f'<p>({PUBLICATION_EDITION})</p><a href="{REPO_URL}/blob/{commit}/README.md">record</a>'
    ).encode()

    def fetch(url: str, *, head: bool = False, timeout: float = 30.0) -> tuple[int, bytes]:
        del timeout
        if url.endswith("/workbench/"):
            return 200, workbench_page(commit)
        if url.endswith(".pdf"):
            pages = b"1 0 obj << /Type /Page >> endobj\n" * EXPECTED_PAGE_COUNT
            return 200, b"%PDF-1.7\n" + pages + b"%%EOF" + source_receipt(
                as_served(explainer, EXPLAINER)
            )
        if url.endswith((EXPLAINER, ".md")):
            return 200, b"" if head else as_served(explainer, url)
        return 200, b"" if head else as_served(page, url)

    monkeypatch.setattr(check_published_site, "fetch", fetch)
    results = check_published_site.check(
        "https://example.org", commit, timeout=1, browser=False
    )
    assert all(passed for passed, _ in results), [line for ok, line in results if not ok]

    undeclared = page.replace(island.encode(), b"")
    assert check_published_site.ref_problems(undeclared.decode(), commit) == [card]


def test_the_media_check_reports_what_published_media_finds(
    monkeypatch: pytest.MonkeyPatch, served_media: list[list[str]]
) -> None:
    commit = "0123456789abcdef0123456789abcdef01234567"
    page = (
        f"<p>({PUBLICATION_EDITION})</p>"
        f'<a href="{REPO_URL}/blob/{commit}/README.md">record</a>'
        '<a href="known-best-1-100.pdf"><img src="known-best-1-100-preview.png"></a>'
        '<video><source src="films/ascent-n1-324-1080p60-citations.mp4"></video>'
    ).encode()

    def fetch(url: str, *, head: bool = False, timeout: float = 30.0) -> tuple[int, bytes]:
        del timeout
        if url.endswith("/workbench/"):
            return 200, workbench_page(commit)
        if url.endswith(".pdf"):
            pages = b"1 0 obj << /Type /Page >> endobj\n" * EXPECTED_PAGE_COUNT
            return 200, b"%PDF-1.7\n" + pages + b"%%EOF" + source_receipt(
                as_served(page, EXPLAINER)
            )
        return 200, b"" if head else as_served(page, url)

    monkeypatch.setattr(check_published_site, "fetch", fetch)
    results = check_published_site.check(
        "https://example.org", commit, timeout=1, browser=False
    )
    assert all(passed for passed, _ in results), [line for ok, line in results if not ok]
    (asked,) = served_media
    assert "films/ascent-n1-324-1080p60-citations.mp4" in asked
    assert "known-best-1-100.pdf" in asked

    monkeypatch.setattr(
        check_published_site.published_media,
        "check_media",
        lambda _site, _paths: ["films/x.mp4: application/octet-stream, not video/mp4"],
    )
    failures = [
        line
        for passed, line in check_published_site.check(
            "https://example.org", commit, timeout=1, browser=False
        )
        if not passed
    ]
    assert failures == ["media: films/x.mp4: application/octet-stream, not video/mp4"]
