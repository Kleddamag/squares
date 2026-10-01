"""An address a paper used to have still arrives at the paper, in a browser.

The papers moved to `papers/<slug>.html` on 2026-10-01 (think-cmz6), and links to their
old addresses are in dated records, in other people's pages and in readers' bookmarks,
most of them with a fragment: a section, a footnote, the explainer's certificate picker.
`render_overview.forwarder_pages` writes a forwarder at each old address
(`MOVED_PAGES`), and the overview sends an old fragment of its own on.

Whether a forwarder forwards is the browser's to say: a script that replaces the
location, a refresh inside `<noscript>`, and a relative address resolved from a
directory. So this serves the real forwarders, and the real overview, beside stand-in
papers on a local address and visits each old address in Chromium, with scripts and
without, and then asks `check_published_site` the same of the same site, which is the
check a deploy is held to.

Skipped where no Chromium can be launched; `SQPACK_CHROMIUM` names one the environment
supplies, as the other browser tools read it.
"""

from __future__ import annotations

import os
import socket
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest

from devtools import check_published_site, render_overview
from devtools.overview_sections import LOWER_BOUNDS_PAPER, OPTIMALITY_PAPER
from devtools.preview_site import serve
from devtools.render_n11_lower_bounds_explainer_pdf import BROWSER_OVERRIDE
from tests import site_renders

#: Real fragments and a real query string an old link carries: a section of each paper,
#: a footnote, the explainer's certificate picker and its review switch.
EXPLAINER_LINKS = ("#proof-of-the-new-lower-bound", "#fn-3", "?review=fonts#381-100")
REVIEW_LINKS = ("#the-result", "#fn-1", "?view=embed#fn-3")
#: How long a forward may take.
ARRIVAL_MS = 10_000


def _free_port() -> int:
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        return int(probe.getsockname()[1])


@pytest.fixture(scope="module")
def site(tmp_path_factory: pytest.TempPathFactory) -> Iterator[str]:
    """The forwarders and the overview as they are rendered, beside stand-ins for the
    pages they lead to, served on a local address; the address, with its closing slash."""
    root = Path(tmp_path_factory.mktemp("site"))
    files = [*render_overview.forwarder_pages(), site_renders.page("index.html")]
    render_overview.write_site(root, files)
    for name in (LOWER_BOUNDS_PAPER, OPTIMALITY_PAPER, render_overview.RESULTS_PAGE):
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(f"<!doctype html><title>{name}</title><p>{name}</p>", "utf-8")
    port = _free_port()
    server = serve(root, port)
    try:
        yield f"http://127.0.0.1:{port}/"
    finally:
        server.shutdown()
        server.server_close()


@pytest.fixture(scope="module")
def chromium() -> Iterator[Any]:
    sync_api = pytest.importorskip("playwright.sync_api")
    with sync_api.sync_playwright() as driver:
        try:
            browser = driver.chromium.launch(executable_path=os.environ.get(BROWSER_OVERRIDE))
        except sync_api.Error as error:
            pytest.skip(f"no Chromium to launch: {error.message.splitlines()[0]}")
        yield browser
        browser.close()


def _arrival(browser: Any, start: str, arrival: str, *, scripts: bool = True) -> str:
    """Where a visit to `start` is once it has had time to arrive at `arrival`."""
    from playwright.sync_api import Error  # noqa: PLC0415

    context = browser.new_context(java_script_enabled=scripts)
    page = context.new_page()
    try:
        page.goto(start, wait_until="load")
        page.wait_for_url(arrival, timeout=ARRIVAL_MS)
    except Error:
        pass
    landed: str = page.url
    context.close()
    return landed


@pytest.mark.parametrize("suffix", EXPLAINER_LINKS)
def test_the_explainers_old_address_arrives_at_the_paper(
    site: str, chromium: Any, suffix: str
) -> None:
    """`explainer.html`, with the fragment and the query string an old link carried."""
    arrival = site + LOWER_BOUNDS_PAPER + suffix
    assert _arrival(chromium, f"{site}explainer.html{suffix}", arrival) == arrival


@pytest.mark.parametrize("old", ["n11-optimality/t-060-explainer.html", "n11-optimality/"])
@pytest.mark.parametrize("suffix", REVIEW_LINKS)
def test_the_optimality_papers_old_addresses_arrive_at_the_paper(
    site: str, chromium: Any, old: str, suffix: str
) -> None:
    """Its page and the directory it was linked by, which the forwarder a level down
    has to climb out of."""
    arrival = site + OPTIMALITY_PAPER + suffix
    assert _arrival(chromium, f"{site}{old}{suffix}", arrival) == arrival


@pytest.mark.parametrize(
    ("old", "new"),
    [
        ("explainer.html", LOWER_BOUNDS_PAPER),
        ("n11-optimality/t-060-explainer.html", OPTIMALITY_PAPER),
        ("n11-optimality/", OPTIMALITY_PAPER),
    ],
)
def test_a_reader_without_scripts_still_arrives(
    site: str, chromium: Any, old: str, new: str
) -> None:
    """The refresh sends a reader without scripts to the paper. A refresh cannot keep a
    fragment, so the reader arrives at the top of the right page."""
    arrival = site + new
    assert _arrival(chromium, f"{site}{old}#fn-3", arrival, scripts=False) == arrival
    assert _arrival(chromium, f"{site}{old}", arrival, scripts=False) == arrival


def test_the_overview_sends_an_old_explainer_fragment_to_the_paper(
    site: str, chromium: Any
) -> None:
    """The explainer was once the site's root, so a fragment the overview lacks goes to
    the paper where it is served now, in one step and not through `explainer.html`; a
    result's row goes to the results table; and a fragment the overview has stays."""
    arrival = f"{site}{LOWER_BOUNDS_PAPER}?review=fonts#fn-3"
    assert _arrival(chromium, f"{site}?review=fonts#fn-3", arrival) == arrival
    arrival = f"{site}{render_overview.RESULTS_PAGE}#t-018"
    assert _arrival(chromium, f"{site}index.html#t-018", arrival) == arrival
    stays = f"{site}#verification-ladders"
    assert _arrival(chromium, stays, stays) == stays


def test_the_deployed_site_check_follows_the_same_forwarders(
    site: str, chromium: Any, monkeypatch: pytest.MonkeyPatch
) -> None:
    """`check_published_site` visits each old address the way a deploy is checked, and
    accepts a site this machine serves; it fails when a forwarder leads nowhere."""
    followed = check_published_site.forwarder_arrivals(chromium, site, timeout=10)
    assert [passed for passed, _ in followed] == [True] * len(render_overview.MOVED_PAGES)
    assert followed[0][1] == (
        f"visiting {site}explainer.html?review=fonts#fn-1 arrives at "
        f"'{site}papers/n11-lower-bounds-explainer.html?review=fonts#fn-1', expected "
        f"'{site}papers/n11-lower-bounds-explainer.html?review=fonts#fn-1'"
    )
    assert f"visiting {site}n11-optimality/?review=fonts#fn-1 " in followed[2][1]
    assert check_published_site.fetch_once(f"{site}explainer.html")[0] == 200

    monkeypatch.setattr(
        render_overview,
        "MOVED_PAGES",
        (("explainer.html", "papers/not-a-paper.html"),),
    )
    ((passed, line),) = check_published_site.forwarder_arrivals(chromium, site, timeout=2)
    assert not passed
    assert "papers/not-a-paper.html" in line
