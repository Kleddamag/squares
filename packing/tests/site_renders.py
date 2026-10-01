"""One render of each site page, and of each result's overview, per test process.

Rendering a page of the site costs seconds: the overview and the frontier atlas about
two each, the case records about five (the page is 9 MB), every page together about ten,
and the sixty-one result overviews about eight. Rendering is deterministic
(`test_overview.test_the_render_is_deterministic` renders afresh to say so), and the
site's test modules only read what is rendered, so they share one render of each, kept
here for the life of the process. Before this, `test_overview`, `test_repo_links`,
`test_case_pages`, `test_frontier_page`, `test_site_documents`, `test_result_overview`,
`test_site_math_faces` and `test_site_text_tokens` each rendered their own, and the
overview was rendered five times in one run of the suite (think-lfnl).

A test module takes these in a module-scoped fixture, never in a test's body, for two
reasons. A fixture's time is setup time, so no check carries a 9 MB render in its own
call time. And a module-scoped fixture is built before a test's own `monkeypatch`
applies, so a test that patches a renderer cannot leave a patched page in the cache; a
test that needs a page rendered under a patch calls the renderer itself.

A worker of a parallel run is a process of its own and renders its own.
"""

from __future__ import annotations

from functools import cache

from devtools import overview_data, render_overview, result_overview


@cache
def page(name: str) -> render_overview.Page:
    """The page `render_overview.PAGES` builds as `name`, rendered once."""
    return render_overview.PAGES[name]()


def html(name: str) -> str:
    """That page's text."""
    return page(name).html


def pages() -> dict[str, str]:
    """Every page `render_overview.PAGES` builds, by name."""
    return {name: html(name) for name in render_overview.PAGES}


@cache
def overview() -> overview_data.Overview:
    """The record as the site reads it, loaded once."""
    return overview_data.load()


@cache
def result_bodies() -> dict[str, str]:
    """Every registered result's overview, by id, in the register's order."""
    loaded = overview()
    return {
        result.id: result_overview.result_popover_html(result, loaded)
        for result in loaded.results
    }
