#!/usr/bin/env python3
"""Check the site as GitHub Pages serves it, against the commit it should be built from.

`pages.yml` renders the overview and the pages beside it, the explainer with its Markdown
edition and PDF, and the workbench from `main`, and deploys them. Nothing is checked in,
so nothing in the repository says whether a deploy landed or what the pages it served
link to; this asks the live site. From `packing/`:

    uv run --frozen --group dev python -m devtools.check_published_site --commit <sha>

With no `--commit` the checkout's `origin/main` is the expectation, which is the commit
the last deploy built from once `git fetch` has run. One line per check, `ok` or
`FAIL`, and the exit status is 0 only when every check passes:

- every page `render_overview.PAGES` owns is served at its URL (the overview at the
  root), and the explainer at `explainer.html`; each carries the edition stamp
  `sqpack.release` names and the canonical URL its renderer wrote;
- no page and not the Markdown edition links a repository file at a commit hash: every
  repository link names `main` (`repo_links`), because a permalink to the commit a page
  was built from 404s once a squash merge leaves that commit on no branch. Every path a
  page links on `main` exists in the expected commit's tree, which is `main` when the
  deploy runs, and each link on the explainer, its Markdown edition, the overview and
  the frontier atlas is also asked of GitHub;
- every address a page used to have (`render_overview.MOVED_PAGES`) is still served, as
  a forwarder that names where a visit is sent now, so a link written before a page
  moved or was withdrawn does not 404;
- every result overview the results table's rows name (`data-row-pop-src`) is served
  beside the pages and is that result's, and the overviews' repository links pass the
  same two checks against the tree;
- the Markdown edition, the PDF and the composite assets are served beside the page,
  and the PDF is a PDF with the expected page count and a source receipt matching
  the exact HTML bytes the site serves;
- the optimality paper, which the Papers page's first card opens, is served where that
  card points, with its landing address, Markdown and PDF, and its bar marks Papers as
  the current section. Its own Pages job builds and checks its content. It is the one
  page whose repository links are held to a commit and not to `main`: a paper cites the
  evidence as it stood when the paper was typeset, so each citation on the page and in
  its Markdown names the expected commit, the one the deploy built from, which `main`
  keeps, and every path it cites is in that commit's tree. A citation that names `main`,
  or any other commit, fails;
- the workbench names the expected source commit, starts its public API in the pinned
  browser, and links back to this project's root rather than the account site's root.

This checks a live deployment, so it is not a step of the source gate;
`tests/test_check_published_site.py` covers its parsing and failure controls on fixtures.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from collections.abc import Callable, Sequence
from pathlib import Path
from urllib.parse import urljoin

from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import sync_playwright

from devtools import render_overview
from devtools.overview_sections import OPTIMALITY_PAPER, result_fragment
from devtools.render_explainer import (
    COMPOSITE_ASSETS,
    MARKDOWN_OUTPUT,
    PAGE_URL,
    REPO,
    SITE_URL,
)
from devtools.render_explainer_pdf import EXPECTED_PAGE_COUNT
from devtools.render_explainer_pdf import OUTPUT as PDF_OUTPUT
from devtools.repo_links import (
    REPO_URL,
    RepositoryTree,
    branch_paths,
    hash_pinned_links,
    repository_tree,
)
from sqpack.probes import probe
from sqpack.release import PUBLICATION_EDITION

#: The JavaScript this runs in the deployed workbench, as files (`sqpack.probes`).
PROBES = Path(__file__).resolve().parent / "probes"

#: A link into this repository as GitHub spells one: the ref, then the path, under
#: `blob/` for a file and `tree/` for a directory.
REPOSITORY_LINK = re.compile(re.escape(REPO_URL) + r"/(blob|tree)/([^/\s\"<>)]+)/([^\s\"<>)]*)")
CANONICAL = re.compile(r'<link\s+rel="canonical"\s+href="([^"]*)"')
#: The fuller body a row's popover fetches, as its address beside the page, and how a
#: result's overview opens: the one block it is, naming its result.
ROW_SOURCE = re.compile(r'data-row-pop-src="([^"]+)"')
RESULT_OVERVIEW = re.compile(r'\A<div class="site-result" data-result-overview="(t-\d{3})">')
#: Where a forwarder sends a visit, as its root element names it.
MOVED_TO = re.compile(r'<html\b[^>]*\sdata-moved-to="([^"]*)"')

#: Where the explainer is served. It is built as `index.html` and renamed when the site
#: is assembled, because the root is the overview's.
EXPLAINER = PAGE_URL.removeprefix(SITE_URL)

#: The site's own pages, by served name, read from the renderer that owns them so a page
#: added there is checked here without an edit. `index.html` is fetched as the root.
SITE_PAGES = tuple(render_overview.PAGES)

#: The pages whose repository links are each asked of GitHub as well. The rest are
#: checked against the commit's tree alone, which is offline, as the reader documents'
#: links already are when they are rendered; asking GitHub would cost a request per link
#: on every deploy. The results page is one, since its records are the register's links
#: and were asked of GitHub when the table was on the overview.
LINK_CHECKED_PAGES = frozenset({"index.html", "frontier.html", render_overview.RESULTS_PAGE})

#: The optimality paper's page, by path under the site's root, and what is served with
#: it: its directory's landing address, its Markdown and its PDF. The path is the one the
#: Papers card links (`overview_sections.OPTIMALITY_PAPER`).
OPTIMALITY_PAPER_FILES = (
    f"{OPTIMALITY_PAPER.rsplit('/', 1)[0]}/",
    f"{OPTIMALITY_PAPER.removesuffix('.html')}.md",
    f"{OPTIMALITY_PAPER.removesuffix('.html')}.pdf",
)
#: The paper's Markdown, whose citations are held to the same commit as the page's.
OPTIMALITY_PAPER_MARKDOWN = f"{OPTIMALITY_PAPER.removesuffix('.html')}.md"
#: The bar's current entry on that page, a level below the root.
PAPERS_CURRENT = '<a data-page="papers" aria-current="page" href="../papers.html">'

#: Every file the deploy serves beside the explainer, by name.
SERVED = (
    MARKDOWN_OUTPUT.name,
    PDF_OUTPUT.name,
    *(asset.name for asset in COMPOSITE_ASSETS),
)

USER_AGENT = "squares-check-published-site (+https://github.com/jlevy/squares)"
WORKBENCH_PATH = "workbench/"
WORKBENCH_REVISION = re.compile(
    r'<meta\s+name="squares-workbench-revision"\s+content="([0-9a-f]{40})">'
)
WORKBENCH_HOME = re.compile(r'<a\s+href="([^"]+)">the overview</a>')


def repository_links(text: str) -> set[tuple[str, str, str]]:
    """Every (kind, ref, path) the text links into the repository, scripts and styles aside."""
    markup = re.sub(r"<(script|style)\b.*?</\1>", "", text, flags=re.DOTALL | re.IGNORECASE)
    return {
        (kind, ref, path.rstrip("/")) for kind, ref, path in REPOSITORY_LINK.findall(markup)
    }


def paper_citations(text: str, commit: str) -> tuple[set[tuple[str, str]], list[str]]:
    """The optimality paper's repository links: each (kind, path) it cites at `commit`,
    without any query or anchor, and every link that names another ref, `main` among
    them, as `kind/ref/path`. The paper pins its citations to the commit it was built
    from (`render_n11_optimality_explainer.link_revision`), and the deploy builds it
    from the commit it deploys."""
    cited: set[tuple[str, str]] = set()
    strays: list[str] = []
    for kind, ref, path in sorted(repository_links(text)):
        if ref == commit:
            cited.add((kind, re.split(r"[?#]", path, maxsplit=1)[0].rstrip("/")))
        else:
            strays.append(f"{kind}/{ref}/{path}")
    return cited, strays


def pdf_pages(data: bytes) -> int:
    """The number of page objects a PDF declares; 0 when the bytes are not a PDF."""
    if not data.startswith(b"%PDF"):
        return 0
    return len(re.findall(rb"/Type\s*/Page(?![s])", data))


def pdf_source_matches(data: bytes, page: bytes) -> bool:
    """Whether the PDF's unique trailing source receipt names the exact fetched HTML."""
    receipt = re.search(rb"\n%sqpack-source-html-sha256: ([0-9a-f]{64})\n\Z", data)
    return (
        receipt is not None
        and data.count(b"%sqpack-source-html-sha256:") == 1
        and receipt[1] == hashlib.sha256(page).hexdigest().encode()
    )


#: The pauses, in seconds, before each retry of a transient answer. This runs straight after
#: a deploy reports success, when Pages can still answer 404 or 5xx for a short while, so a
#: single fetch failed a good deploy on timing alone (#160 R26). Thirty seconds in all.
RETRY_DELAYS = (2.0, 4.0, 8.0, 16.0)
#: Answers worth asking again: unreachable (0), not yet there, throttled, or a server error.
TRANSIENT_STATUSES = frozenset({0, 404, 408, 429, 500, 502, 503, 504})


def fetch_once(url: str, *, head: bool = False, timeout: float = 30.0) -> tuple[int, bytes]:
    """The status and body of a GET (or the status alone of a HEAD); 0 when unreachable."""
    if not url.startswith("https://"):
        raise ValueError(f"refusing to fetch a non-https URL: {url}")
    request = urllib.request.Request(
        url, method="HEAD" if head else "GET", headers={"User-Agent": USER_AGENT}
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.status, b"" if head else response.read()
    except urllib.error.HTTPError as error:
        return error.code, b""
    except urllib.error.URLError:
        return 0, b""


def fetch(
    url: str,
    *,
    head: bool = False,
    timeout: float = 30.0,
    delays: Sequence[float] = RETRY_DELAYS,
    sleep: Callable[[float], object] = time.sleep,
) -> tuple[int, bytes]:
    """`fetch_once`, asked again after each delay while the answer is transient.

    The last answer is returned whatever it is, so a page that stays missing still fails
    its check, only later.
    """
    answer = fetch_once(url, head=head, timeout=timeout)
    for delay in delays:
        if answer[0] not in TRANSIENT_STATUSES:
            break
        sleep(delay)
        answer = fetch_once(url, head=head, timeout=timeout)
    return answer


def expected_commit() -> str:
    """`origin/main` as the checkout knows it, which is what the last deploy built from."""
    found = subprocess.run(
        ("git", "rev-parse", "origin/main"),
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
    )
    if found.returncode != 0:
        raise SystemExit("no --commit given and origin/main cannot be resolved here")
    return found.stdout.strip()


def workbench_startup(url: str, project_root: str, *, timeout: float) -> tuple[bool, str]:
    """Start the deployed page and require its public API and project-root navigation."""
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            try:
                page = browser.new_page()
                page.goto(url, wait_until="load", timeout=timeout * 1000)
                page.wait_for_function(
                    probe(PROBES, "check_published_site/api-ready"),
                    timeout=timeout * 1000,
                )
                observed = page.evaluate(probe(PROBES, "check_published_site/startup"))
            finally:
                browser.close()
    except PlaywrightError as error:
        return False, f"workbench startup failed: {error}"
    pairs = observed.get("pairs") if isinstance(observed, dict) else None
    home = observed.get("home") if isinstance(observed, dict) else None
    passed = isinstance(pairs, int) and pairs > 0 and home == project_root
    return passed, f"workbench API started with {pairs!r} pairs; home resolved to {home!r}"


def check(
    site: str,
    commit: str,
    *,
    timeout: float,
    browser: bool = True,
) -> list[tuple[bool, str]]:
    """Every check as (passed, line), in the order they are printed."""
    results: list[tuple[bool, str]] = []
    site = site.rstrip("/") + "/"

    def served_page(name: str, url: str, canonical: str) -> tuple[bytes, str]:
        """Fetch one page and check it is served, stamped and canonical; its bytes and text."""
        status, body = fetch(url, timeout=timeout)
        text = body.decode("utf-8", errors="replace")
        results.append((status == 200, f"page {url}: HTTP {status}, {len(body)} bytes"))
        # The shared version (think-qsuu), pinned in release.py: a page names the data it
        # was drawn from, as the atlas and the videos do, whatever commit built it. The
        # commit is still what the workbench's source revision must name.
        stamped = PUBLICATION_EDITION in text
        where = f"{'' if stamped else 'not '}on {name}"
        results.append((stamped, f"edition stamp {PUBLICATION_EDITION!r} is {where}"))
        found = CANONICAL.search(text)
        declared = found.group(1) if found is not None else None
        results.append(
            (
                declared == canonical,
                f"{name} names canonical URL {declared!r} against expected {canonical!r}",
            )
        )
        return body, text

    try:
        tree: RepositoryTree | None = repository_tree(commit)
    except SystemExit as error:
        tree = None
        results.append((False, f"the tree of {commit} cannot be read here: {error}"))

    def links_main(name: str, text: str) -> None:
        """No link names a commit, and every path linked on `main` is in the tree."""
        pinned = hash_pinned_links(text)
        results.append(
            (
                not pinned,
                f"{name}: {len(pinned)} repository links pinned to a commit: {pinned[:5]}"
                if pinned
                else f"{name}: no repository link is pinned to a commit",
            )
        )
        if tree is None:
            return
        missing = tree.missing(branch_paths(text))
        results.append(
            (
                not missing,
                f"{name}: linked on main but not in {commit[:12]}: {missing[:5]}"
                if missing
                else f"{name}: every path linked on main is in {commit[:12]}",
            )
        )

    checked_links: set[tuple[str, str, str]] = set()
    overviews: list[str] = []
    for name in SITE_PAGES:
        url = site if name == "index.html" else site + name
        _, text = served_page(name, url, render_overview.canonical_url(name))
        links_main(name, text)
        if name in LINK_CHECKED_PAGES:
            checked_links |= repository_links(text)
        if name == render_overview.RESULTS_PAGE:
            overviews = sorted(set(ROW_SOURCE.findall(text)))

    # A page that moved or was withdrawn is still served at its old address, as a
    # forwarder: a deploy that dropped one would 404 every link written before the change.
    for forwarder in render_overview.forwarder_pages():
        status, body = fetch(site + forwarder.name, timeout=timeout)
        expected = MOVED_TO.search(forwarder.html)
        served = MOVED_TO.search(body.decode("utf-8", errors="replace"))
        target = None if served is None else served.group(1)
        results.append(
            (
                status == 200 and expected is not None and target == expected.group(1),
                f"forwarder {forwarder.name}: HTTP {status}, sends a visit to {target!r}",
            )
        )

    # The result overviews are files beside the pages, fetched when a row is opened: a
    # deploy that lost one would show only as a popover that keeps its short detail.
    results.append(
        (
            bool(overviews),
            f"{render_overview.RESULTS_PAGE} names {len(overviews)} result overviews",
        )
    )
    bodies = []
    for address in overviews:
        status, body = fetch(site + address, timeout=timeout)
        fragment = body.decode("utf-8", errors="replace")
        found = RESULT_OVERVIEW.match(fragment)
        holds = None if found is None else result_fragment(found.group(1))
        results.append(
            (
                status == 200 and holds == address,
                f"result overview {address}: HTTP {status}, {len(body)} bytes"
                + ("" if holds == address else f", but it is {holds!r}"),
            )
        )
        bodies.append(fragment)
    if bodies:
        links_main("the result overviews", "\n".join(bodies))

    # The explainer's bytes are what the PDF's source receipt names, so they are kept whole.
    page, text = served_page(EXPLAINER, site + EXPLAINER, PAGE_URL)

    status, markdown = fetch(site + MARKDOWN_OUTPUT.name, timeout=timeout)
    results.append(
        (
            status == 200,
            f"Markdown edition {MARKDOWN_OUTPUT.name}: HTTP {status}, {len(markdown)} bytes",
        )
    )

    markdown_text = markdown.decode("utf-8", errors="replace")
    links_main(EXPLAINER, text)
    links_main(MARKDOWN_OUTPUT.name, markdown_text)
    checked_links |= repository_links(text) | repository_links(markdown_text)
    for kind, ref, path in sorted(checked_links):
        url = f"{REPO_URL}/{kind}/{ref}/{path}"
        status, _ = fetch(url, head=True, timeout=timeout)
        results.append((status == 200, f"link HTTP {status}: {url}"))

    for name in SERVED:
        if name == MARKDOWN_OUTPUT.name:
            continue
        head_only = name != PDF_OUTPUT.name
        status, body = fetch(site + name, head=head_only, timeout=timeout)
        line = f"served {name}: HTTP {status}"
        ok = status == 200
        if name == PDF_OUTPUT.name:
            pages = pdf_pages(body)
            source_matches = pdf_source_matches(body, page)
            ok = ok and pages == EXPECTED_PAGE_COUNT and source_matches
            line += f", {len(body)} bytes, {pages} pages (expected {EXPECTED_PAGE_COUNT})"
            line += ", source HTML receipt " + (
                "matches fetched page"
                if source_matches
                else "missing, malformed, or mismatched"
            )
        results.append((ok, line))

    def cites_commit(name: str, text: str) -> None:
        """The paper's rule, where every other page's is `links_main`: each repository
        link names the expected commit, and every path cited there is in its tree."""
        cited, strays = paper_citations(text, commit)
        results.append(
            (
                bool(cited) and not strays,
                f"{name}: {len(strays)} repository links not pinned to {commit[:12]}: "
                f"{strays[:5]}"
                if strays
                else f"{name}: {len(cited)} citations, each pinned to {commit[:12]}",
            )
        )
        if tree is None:
            return
        missing = tree.missing(cited)
        results.append(
            (
                not missing,
                f"{name}: cited at {commit[:12]} but not in its tree: {missing[:5]}"
                if missing
                else f"{name}: every cited path is in {commit[:12]}",
            )
        )

    status, paper = fetch(site + OPTIMALITY_PAPER, timeout=timeout)
    paper_text = paper.decode("utf-8", errors="replace")
    current = PAPERS_CURRENT in paper_text
    marked = f"Papers is {'' if current else 'not '}the bar's current entry"
    line = f"optimality paper {OPTIMALITY_PAPER}: HTTP {status}, {len(paper)} bytes, {marked}"
    results.append((status == 200 and current, line))
    if status == 200:
        cites_commit(OPTIMALITY_PAPER, paper_text)
    for name in OPTIMALITY_PAPER_FILES:
        cited_here = name == OPTIMALITY_PAPER_MARKDOWN
        status, body = fetch(site + name, head=not cited_here, timeout=timeout)
        results.append((status == 200, f"served {name}: HTTP {status}"))
        if cited_here and status == 200:
            cites_commit(name, body.decode("utf-8", errors="replace"))

    workbench_url = site + WORKBENCH_PATH
    status, workbench = fetch(workbench_url, timeout=timeout)
    workbench_text = workbench.decode("utf-8", errors="replace")
    results.append(
        (
            status == 200,
            f"workbench {workbench_url}: HTTP {status}, {len(workbench)} bytes",
        )
    )
    stamped = WORKBENCH_REVISION.search(workbench_text)
    observed_revision = stamped.group(1) if stamped is not None else None
    results.append(
        (
            observed_revision == commit,
            f"workbench source revision {observed_revision!r} against expected {commit}",
        )
    )
    home = WORKBENCH_HOME.search(workbench_text)
    home_href = home.group(1) if home is not None else ""
    resolved_home = urljoin(workbench_url, home_href) if home_href else None
    results.append(
        (
            resolved_home == site,
            f"workbench home resolves to {resolved_home!r} against project root {site!r}",
        )
    )
    if browser:
        results.append(workbench_startup(workbench_url, site, timeout=timeout))
    return results


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    parser.add_argument(
        "--site", default=SITE_URL, help=f"the deployed site (default {SITE_URL})"
    )
    parser.add_argument("--commit", help="the full commit the deploy should have built from")
    parser.add_argument("--timeout", type=float, default=30.0, help="seconds per request")
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="skip the browser API startup check (HTTP identity checks still run)",
    )
    args = parser.parse_args(argv)
    commit = args.commit or expected_commit()
    results = check(args.site, commit, timeout=args.timeout, browser=not args.no_browser)
    failed = 0
    for passed, line in results:
        print(f"{'ok  ' if passed else 'FAIL'} {line}", flush=True)
        failed += not passed
    print(f"{len(results) - failed} of {len(results)} checks passed", flush=True)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
