"""A page that moved or was withdrawn still arrives, in a browser.

`render_overview.forwarder_pages` writes a forwarder at each address a page used to
have. `tests/node/overview_forward` runs the script against a stand-in document; this
opens the forwarders themselves, as they are written, and reads where the browser ends
up: with scripts, at the target with the query string and the fragment the reader came
with; without scripts, at the target by the refresh. A target off the site, the defect
log on GitHub, is answered by a stand-in, so no test reaches the network.

Skipped where no Chromium can be launched; `SQPACK_CHROMIUM` names one the environment
supplies, as the other browser tools read it.
"""

from __future__ import annotations

import contextlib
import os
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest

from devtools import render_overview
from devtools.render_explainer_pdf import BROWSER_OVERRIDE
from devtools.repo_links import REPO_URL

#: What stands at each target: a page with nothing to run and nothing to fetch.
STAND_IN = "<!doctype html><title>target</title><p>target</p>"
DEFECTS = f"{REPO_URL}/blob/main/defects.md"


@pytest.fixture(scope="module")
def browser() -> Iterator[Any]:
    sync_api = pytest.importorskip("playwright.sync_api")
    with sync_api.sync_playwright() as driver:
        try:
            launched = driver.chromium.launch(executable_path=os.environ.get(BROWSER_OVERRIDE))
        except sync_api.Error as error:
            pytest.skip(f"no Chromium to launch: {error.message.splitlines()[0]}")
        yield launched
        launched.close()


@pytest.fixture(scope="module")
def site(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """The forwarders as the site writes them, beside a stand-in for each target page."""
    root = tmp_path_factory.mktemp("forwarders")
    render_overview.write_site(root, render_overview.forwarder_pages())
    for _, new in render_overview.MOVED_PAGES:
        if not new.startswith("https://"):
            (root / new).write_text(STAND_IN, encoding="utf-8")
    return root


def _arrives(browser: Any, address: str, expected: str, *, scripts: bool) -> str:
    """Where a reader who opens `address` ends up, with or without scripts, once the
    browser has had the chance to reach `expected`."""
    sync_api = pytest.importorskip("playwright.sync_api")
    context = browser.new_context(java_script_enabled=scripts)
    try:
        context.route(
            f"{REPO_URL}/**",
            lambda route: route.fulfill(status=200, content_type="text/html", body=STAND_IN),
        )
        page = context.new_page()
        page.goto(address, wait_until="load")
        # A page that never arrives is left where it is, and the caller compares.
        with contextlib.suppress(sync_api.TimeoutError):
            page.wait_for_url(expected, timeout=5000)
        return page.url
    finally:
        context.close()


def test_each_old_address_arrives_with_its_query_and_fragment(browser: Any, site: Path) -> None:
    moved = dict(render_overview.MOVED_PAGES)
    assert moved["results.html"] == "all-results.html"
    assert moved["status.html"] == "frontier.html"
    assert moved["defects.html"] == DEFECTS
    root = site.as_uri()
    arrivals = {
        "results.html": f"{root}/all-results.html",
        "status.html": f"{root}/frontier.html",
        "defects.html": DEFECTS,
    }
    for old, target in arrivals.items():
        assert _arrives(browser, f"{root}/{old}", target, scripts=True) == target, old
        kept = f"{target}?view=embed#n-17"
        came = f"{root}/{old}?view=embed#n-17"
        assert _arrives(browser, came, kept, scripts=True) == kept, old


def test_without_scripts_the_refresh_still_arrives(browser: Any, site: Path) -> None:
    """A reader without scripts is sent on by the refresh, which cannot keep a fragment."""
    root = site.as_uri()
    arrivals = {
        "results.html": f"{root}/all-results.html",
        "status.html": f"{root}/frontier.html",
        "defects.html": DEFECTS,
    }
    for old, target in arrivals.items():
        assert _arrives(browser, f"{root}/{old}", target, scripts=False) == target, old
