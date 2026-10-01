#!/usr/bin/env python3
"""Check the site as GitHub Pages serves it, against the commit it should be built from.

`pages.yml` renders the overview and the pages beside it, the two papers under `papers/`
with their Markdown and PDF, and the workbench from `main`, and deploys them. Nothing is
checked in, so nothing in the repository says whether a deploy landed or what the pages
it served link to; this asks the live site. From `packing/`:

    uv run --frozen --group dev python -m devtools.check_published_site --commit <sha>

With no `--commit` the checkout's `origin/main` is the expectation, which is the commit
the last deploy built from once `git fetch` has run. `--site` may also name a site served
on this machine (`http://127.0.0.1:8765/`, as `devtools.preview_site --serve` serves
one), which is how the same checks are run on a build before it is deployed; give
`--commit` the commit that build was made from. One line per check, `ok` or `FAIL`, and
the exit status is 0 only when every check passes:

- every page `render_overview.PAGES` owns is served at its URL (the overview at the
  root), and the lower-bounds explainer at `papers/n11-lower-bounds-explainer.html`;
  each carries the edition stamp `sqpack.release` names and the canonical URL its
  renderer wrote;
- no page and not the Markdown edition links a repository file at a commit hash: every
  repository link names `main` (`repo_links`), because a permalink to the commit a page
  was built from 404s once a squash merge leaves that commit on no branch. Every path a
  page links on `main` exists in the expected commit's tree, which is `main` when the
  deploy runs, and each link on the explainer, its Markdown edition, the overview and
  the frontier atlas is also asked of GitHub;
- every result overview the results table's rows name (`data-row-pop-src`) is served
  beside the pages and is that result's, and the overviews' repository links pass the
  same two checks against the tree;
- the record links are all there. The checks above ask only whether a link that was
  written resolves, so a deploy that wrote fewer links passed them: on 2026-10-01 every
  link into `packing/resources` and `packing/campaign` was missing from the live site,
  with 783 of 783 checks green (D-512). So the renderer is asked what it writes from the
  register in this checkout, which the deploy job checks out at the deployed commit:
  each result row of the overview's and the results page's tables carries every record
  link the renderer gives that result, and the overviews of `RECORD_LINK_SAMPLE` carry
  every repository link the renderer writes for them. It fetches nothing more;
- the Markdown edition and the PDF are served beside the page under its slug and the
  composite assets at the site's root, and the PDF is a PDF with the expected page count
  and a source receipt matching the exact HTML bytes the site serves;
- the optimality paper, which the Papers page's first card opens, is served where that
  card points, `papers/n11-optimality-review.html`, with its Markdown and PDF beside it,
  and each paper's bar marks Papers as the current section, from a level below the
  root. Its own Pages job builds and checks its content. It is the one
  page whose repository links are held to a commit and not to `main`: a paper cites the
  evidence as it stood when the paper was typeset, so each citation on the page and in
  its Markdown names the expected commit, the one the deploy built from, which `main`
  keeps, and every path it cites is in that commit's tree. A citation that names `main`,
  or any other commit, fails;
- no link written before the papers moved breaks (`render_overview.MOVED_PAGES`,
  `MOVED_FILES`): each address a paper's page used to have serves a forwarder that names
  the page's address now as its canonical URL, in a link, in a refresh for a reader
  without scripts, and to the forwarding script, and in the pinned browser a visit to
  it with a query string and a fragment arrives at the new address with both; each
  address a paper's Markdown or PDF used to have serves the same bytes as the new one;
- the workbench names the expected source commit, starts its public API in the pinned
  browser, and links back to this project's root rather than the account site's root.

This checks a live deployment, so it is not a step of the source gate;
`tests/test_check_published_site.py` covers its parsing and failure controls on fixtures.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import posixpath
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path
from typing import NamedTuple
from urllib.parse import urljoin

from playwright.sync_api import Browser, sync_playwright
from playwright.sync_api import Error as PlaywrightError

from devtools import overview_data, render_overview, result_overview
from devtools.overview_sections import LOWER_BOUNDS_PAPER, OPTIMALITY_PAPER, result_fragment
from devtools.render_n11_lower_bounds_explainer import (
    COMPOSITE_ASSETS,
    PAGE_URL,
    REPO,
    SITE_URL,
)
from devtools.render_n11_lower_bounds_explainer_pdf import BROWSER_OVERRIDE, EXPECTED_PAGE_COUNT
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

#: The lower-bounds explainer's Markdown edition and its PDF, by path under the site's
#: root: beside the page, under the paper's slug.
LOWER_BOUNDS_MARKDOWN = f"{LOWER_BOUNDS_PAPER.removesuffix('.html')}.md"
LOWER_BOUNDS_PDF = f"{LOWER_BOUNDS_PAPER.removesuffix('.html')}.pdf"

#: The site's own pages, by served name, read from the renderer that owns them so a page
#: added there is checked here without an edit. `index.html` is fetched as the root.
SITE_PAGES = tuple(render_overview.PAGES)

#: The pages whose repository links are each asked of GitHub as well. The rest are
#: checked against the commit's tree alone, which is offline, as the reader documents'
#: links already are when they are rendered; asking GitHub would cost a request per link
#: on every deploy. The results page is one, since its records are the register's links
#: and were asked of GitHub when the table was on the overview.
LINK_CHECKED_PAGES = frozenset({"index.html", "frontier.html", render_overview.RESULTS_PAGE})

#: What is served with the optimality paper's page, by path under the site's root: its
#: Markdown and its PDF, beside it under its slug. The page's path is the one the Papers
#: card links (`overview_sections.OPTIMALITY_PAPER`).
OPTIMALITY_PAPER_MARKDOWN = f"{OPTIMALITY_PAPER.removesuffix('.html')}.md"
OPTIMALITY_PAPER_FILES = (
    OPTIMALITY_PAPER_MARKDOWN,
    f"{OPTIMALITY_PAPER.removesuffix('.html')}.pdf",
)
#: The bar's current entry on a paper's page, a level below the root.
PAPERS_CURRENT = '<a data-page="papers" aria-current="page" href="../papers.html">'

#: Every file the deploy serves with the lower-bounds explainer, by path under the site's
#: root: its Markdown and PDF beside it, and the atlas's files at the root.
SERVED = (
    LOWER_BOUNDS_MARKDOWN,
    LOWER_BOUNDS_PDF,
    *(asset.name for asset in COMPOSITE_ASSETS),
)

#: What a forwarder says about where its page is now: the address the script reads, the
#: refresh a reader without scripts follows, and the link.
MOVED_TO = re.compile(r'<html\b[^>]*\sdata-moved-to="([^"]*)"')
REFRESH = re.compile(r'<meta\s+http-equiv="refresh"\s+content="0;\s*url=([^"]*)"')
MOVED_LINK = re.compile(r'<p>[^<]*<a\s+href="([^"]*)"')
#: The query string and fragment a forwarder is visited with in the browser: the review
#: switch the explainer reads and a footnote, both of which a real old link carries.
FORWARDED_SUFFIX = "?review=fonts#fn-1"

USER_AGENT = "squares-check-published-site (+https://github.com/jlevy/squares)"
WORKBENCH_PATH = "workbench/"
WORKBENCH_REVISION = re.compile(
    r'<meta\s+name="squares-workbench-revision"\s+content="([0-9a-f]{40})">'
)
WORKBENCH_HOME = re.compile(r'<a\s+href="([^"]+)">the overview</a>')


#: The results whose published overviews are held, link for link, to what the renderer
#: writes for them. Between them their records cite files under directories of
#: `packing/resources` and of `packing/campaign`, the two trees the Pages jobs' partial
#: checkouts leave out (`rendered_record_links` refuses a sample that stops doing so):
#: T-060's source packet, certificate and proof; T-043's, for another case and source; and
#: T-023, a result of this project whose proofs and receipts are in the campaign.
RECORD_LINK_SAMPLE = ("T-060", "T-043", "T-023")
#: The trees a partial checkout omits the directories of, as `pages.yml` writes them.
OMITTED_TREES = ("packing/resources/", "packing/campaign/")
#: The pages with a table of results, whose rows each carry their result's record links.
RECORD_LINK_PAGES = ("index.html", render_overview.RESULTS_PAGE)
#: A table's result row from its opening tag on, which names the result as its own
#: address on the results page (`id`) and as `data-result` anywhere else, and the line of
#: record links in its result cell.
_RESULT_ROW = re.compile(r'(?:id|data-result)="(t-\d{3})"')
_ROW_RECORDS = re.compile(r'<div class="site-records">(.*?)</div>', re.DOTALL)


class RecordLinks(NamedTuple):
    """What the renderer writes from the register, for the deployed pages to be held to."""

    rows: dict[str, str]
    """Each result's record links as a table row carries them (`Result.records`), by the
    row's name (`t-060`): their addresses, one to a line."""
    overviews: dict[str, str]
    """The rendered overview of each result of `RECORD_LINK_SAMPLE`, by its address
    beside the pages (`result/t-060.html`)."""


def rendered_record_links() -> RecordLinks:
    """The record links as the renderer writes them from this checkout's register.

    These are the functions the pages are rendered with, `overview_data.load` for a row's
    records and `result_overview.result_popover_html` for an overview, so what is
    expected of the deploy is what a render of the same commit produces, and nothing is
    restated here. They resolve a cited path against the commit (`repo_links.path_kind`),
    so the answer does not depend on whether this checkout is partial. The sample has to
    cite something under a directory of each omitted tree, or it would pass a deploy
    that dropped those links again; a register that no longer does that fails here.
    """
    overview = overview_data.load()
    results = {result.id: result for result in overview.results}
    unknown = [result for result in RECORD_LINK_SAMPLE if result not in results]
    if unknown:
        raise SystemExit(f"the register has no {', '.join(unknown)} to sample")
    overviews = {
        result_fragment(result): result_overview.result_popover_html(results[result], overview)
        for result in RECORD_LINK_SAMPLE
    }
    cited = {path for body in overviews.values() for _, path in branch_paths(body)}
    for tree in OMITTED_TREES:
        # A file directly under the tree is in every checkout; one a directory down is not.
        if not any(path.startswith(tree) and "/" in path.removeprefix(tree) for path in cited):
            raise SystemExit(
                f"the overviews of {', '.join(RECORD_LINK_SAMPLE)} cite nothing under a "
                f"directory of {tree}: sample a result that does"
            )
    rows = {
        result.id.lower(): "\n".join(link.url for link in result.records)
        for result in overview.results
    }
    return RecordLinks(rows, overviews)


def absent_links(rendered: str, published: str) -> list[str]:
    """Every repository path `rendered` links on `main` that `published` does not, as
    `kind/path`: what a deploy dropped."""
    return sorted(
        f"{kind}/{path}" for kind, path in branch_paths(rendered) - branch_paths(published)
    )


def row_records(page: str) -> dict[str, str]:
    """The line of record links in each result row of a page's table of results, by the
    row's name. A row is read from its own opening tag to the next row's, so a row that
    lost its line is not given its neighbour's."""
    found: dict[str, str] = {}
    for row in page.split("<tr ")[1:]:
        named = _RESULT_ROW.match(row)
        records = _ROW_RECORDS.search(row)
        if named is not None and records is not None:
            found[named.group(1)] = records.group(1)
    return found


def checkout_commit() -> str | None:
    """The commit this checkout is at, which is the register the expectation is read from."""
    found = subprocess.run(
        ("git", "rev-parse", "HEAD"), cwd=REPO, capture_output=True, text=True, check=False
    )
    return found.stdout.strip() if found.returncode == 0 else None


def record_link_checks(
    expected: RecordLinks,
    pages: Mapping[str, str],
    overviews: Mapping[str, str],
    *,
    rendered_at: str = "",
) -> list[tuple[bool, str]]:
    """The record-link checks as (passed, line): each page of `pages`, a served page with a
    table of results by name, and each sampled overview of `overviews`, the served
    overviews by address, against what the renderer writes. `rendered_at` ends a failing
    line where the expectation was not rendered at the deployed commit, since a failure
    may then be the checkout's and not the deploy's."""
    results: list[tuple[bool, str]] = []
    for name, text in pages.items():
        served = row_records(text)
        lacking = {
            row: absent
            for row, records in expected.rows.items()
            if (absent := absent_links(records, served.get(row, "")))
        }
        total = sum(len(branch_paths(records)) for records in expected.rows.values())
        if lacking:
            shown = "; ".join(
                f"{row} lacks {absent[:3]}" for row, absent in list(lacking.items())[:3]
            )
            line = (
                f"{name}: {len(lacking)} of {len(expected.rows)} result rows lack record "
                f"links the renderer writes: {shown}{rendered_at}"
            )
        else:
            line = (
                f"{name}: each of {len(expected.rows)} result rows carries its record "
                f"links, {total} in all"
            )
        results.append((not lacking, line))
    for address, rendered in expected.overviews.items():
        count = len(branch_paths(rendered))
        if address not in overviews:
            results.append(
                (
                    False,
                    f"result overview {address}: sampled for its record links and not served",
                )
            )
            continue
        absent = absent_links(rendered, overviews[address])
        line = (
            f"result overview {address}: lacks {len(absent)} of the {count} repository links "
            f"the renderer writes for it: {absent[:5]}{rendered_at}"
            if absent
            else f"result overview {address}: carries the {count} repository links the "
            "renderer writes for it"
        )
        results.append((not absent, line))
    return results


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
    from (`render_n11_optimality_review.link_revision`), and the deploy builds it
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


#: A site this machine serves, as `devtools.preview_site --serve` does: the one kind of
#: address that is not https and is still asked, so a build can be checked before it is
#: deployed. GitHub is always asked over https.
LOCAL_SITE = re.compile(r"http://(?:127\.0\.0\.1|localhost)(?::\d+)?/")


def fetch_once(url: str, *, head: bool = False, timeout: float = 30.0) -> tuple[int, bytes]:
    """The status and body of a GET (or the status alone of a HEAD); 0 when unreachable."""
    if not (url.startswith("https://") or LOCAL_SITE.match(url)):
        raise ValueError(f"refusing to fetch a URL that is neither https nor local: {url}")
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


def forwarder_says(text: str) -> dict[str, str | None]:
    """Where a forwarder says its page is now, in each of the four places it says it:
    its canonical URL, the address its script reads, its refresh, and its link."""
    places = (
        ("canonical", CANONICAL),
        ("script", MOVED_TO),
        ("refresh", REFRESH),
        ("link", MOVED_LINK),
    )
    found = {name: pattern.search(text) for name, pattern in places}
    return {
        name: match.group(1) if match is not None else None for name, match in found.items()
    }


def forwarder_expected(old: str, new: str) -> dict[str, str | None]:
    """What `forwarder_says` has to answer for the page that moved from `old` to `new`:
    the new address in full as the canonical URL, and relative to the old one elsewhere."""
    target = posixpath.relpath(new, posixpath.dirname(old))
    return {
        "canonical": render_overview.canonical_url(new),
        "script": target,
        "refresh": target,
        "link": target,
    }


def visited_address(old: str) -> str:
    """The address a reader has for a page that moved: a directory's `index.html` is
    linked as its directory."""
    return old.removesuffix("index.html")


def forwarder_arrivals(
    browser: Browser, site: str, *, timeout: float
) -> list[tuple[bool, str]]:
    """Visit each address a page used to have in `browser`, with a query string and a
    fragment, and require it to arrive at the page's address now with both."""
    results: list[tuple[bool, str]] = []
    for old, new in render_overview.MOVED_PAGES:
        start = site + visited_address(old) + FORWARDED_SUFFIX
        arrival = site + new + FORWARDED_SUFFIX
        page = browser.new_page()
        try:
            page.goto(start, wait_until="load", timeout=timeout * 1000)
            page.wait_for_url(arrival, timeout=timeout * 1000)
        except PlaywrightError:
            pass  # Where the visit is now says what went wrong.
        landed = page.url
        page.close()
        results.append(
            (landed == arrival, f"visiting {start} arrives at {landed!r}, expected {arrival!r}")
        )
    return results


def forwarders_followed(site: str, *, timeout: float) -> list[tuple[bool, str]]:
    """`forwarder_arrivals` in the pinned browser. `SQPACK_CHROMIUM` names a browser the
    environment supplies, as the other browser tools read it."""
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(
                executable_path=os.environ.get(BROWSER_OVERRIDE)
            )
            try:
                return forwarder_arrivals(browser, site, timeout=timeout)
            finally:
                browser.close()
    except PlaywrightError as error:
        return [(False, f"the forwarders could not be visited: {error}")]


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
    tables: dict[str, str] = {}
    for name in SITE_PAGES:
        url = site if name == "index.html" else site + name
        _, text = served_page(name, url, render_overview.canonical_url(name))
        links_main(name, text)
        if name in LINK_CHECKED_PAGES:
            checked_links |= repository_links(text)
        if name in RECORD_LINK_PAGES:
            tables[name] = text
        if name == render_overview.RESULTS_PAGE:
            overviews = sorted(set(ROW_SOURCE.findall(text)))

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

    # Every link above resolves; whether every link is there is asked of the renderer.
    try:
        expected = rendered_record_links()
    except SystemExit as error:
        results.append(
            (False, f"the record links cannot be rendered in this checkout: {error}")
        )
    else:
        head = checkout_commit()
        rendered_at = (
            ""
            if head == commit
            else f" (expected as rendered at {(head or 'no commit')[:12]}, not {commit[:12]})"
        )
        results.extend(
            record_link_checks(
                expected,
                tables,
                dict(zip(overviews, bodies, strict=True)),
                rendered_at=rendered_at,
            )
        )

    # The explainer's bytes are what the PDF's source receipt names, so they are kept whole.
    page, text = served_page(LOWER_BOUNDS_PAPER, site + LOWER_BOUNDS_PAPER, PAGE_URL)
    current = PAPERS_CURRENT in text
    marked = f"Papers is {'' if current else 'not '}the bar's current entry"
    results.append((current, f"{LOWER_BOUNDS_PAPER}: {marked}, linked from a level below"))

    status, markdown = fetch(site + LOWER_BOUNDS_MARKDOWN, timeout=timeout)
    results.append(
        (
            status == 200,
            f"Markdown edition {LOWER_BOUNDS_MARKDOWN}: HTTP {status}, {len(markdown)} bytes",
        )
    )

    markdown_text = markdown.decode("utf-8", errors="replace")
    links_main(LOWER_BOUNDS_PAPER, text)
    links_main(LOWER_BOUNDS_MARKDOWN, markdown_text)
    checked_links |= repository_links(text) | repository_links(markdown_text)
    # This loop is where the check's time goes: one request to github.com for each distinct
    # link, in turn. On 2026-10-01 it was 614 of 783 checks and nearly all of a 14 m 47 s
    # run from a laptop, at 1.3 to 3.8 s a request (the deploy job's whole run took
    # 4 m 35 s). 558 of the 614 name `packing/frontier`, among them the 324 case files
    # and 170 line anchors into `results.yaml` and `evidence.yaml`, each anchor asked as an
    # address of its own though the files are two. The record-link checks above add no
    # request.
    for kind, ref, path in sorted(checked_links):
        url = f"{REPO_URL}/{kind}/{ref}/{path}"
        status, _ = fetch(url, head=True, timeout=timeout)
        results.append((status == 200, f"link HTTP {status}: {url}"))

    for name in SERVED:
        if name == LOWER_BOUNDS_MARKDOWN:
            continue
        head_only = name != LOWER_BOUNDS_PDF
        status, body = fetch(site + name, head=head_only, timeout=timeout)
        line = f"served {name}: HTTP {status}"
        ok = status == 200
        if name == LOWER_BOUNDS_PDF:
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

    # No link written before the papers moved breaks: a page's old address forwards, and
    # a file's old address serves the same bytes.
    for old, new in render_overview.MOVED_PAGES:
        status, body = fetch(site + old, timeout=timeout)
        says = forwarder_says(body.decode("utf-8", errors="replace"))
        expected = forwarder_expected(old, new)
        results.append(
            (
                status == 200 and says == expected,
                f"forwarder {old}: HTTP {status}, leads to {new}"
                if says == expected
                else f"forwarder {old}: HTTP {status}, says {says} against expected {expected}",
            )
        )
    for old, new in render_overview.MOVED_FILES:
        old_status, old_body = fetch(site + old, timeout=timeout)
        new_status, new_body = fetch(site + new, timeout=timeout)
        same = old_status == 200 and new_status == 200 and old_body == new_body
        verdict = "the same bytes as" if same else "not the bytes of"
        line = (
            f"moved file {old}: HTTP {old_status}, {len(old_body)} bytes, {verdict} {new} "
            f"(HTTP {new_status}, {len(new_body)} bytes)"
        )
        results.append((same, line))
    if browser:
        results.extend(forwarders_followed(site, timeout=timeout))

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
        help="skip the checks that open a browser, the workbench's API startup and the "
        "forwarders' arrival (HTTP identity checks still run)",
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
