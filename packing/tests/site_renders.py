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

from collections.abc import Callable
from functools import cache
from pathlib import Path

import pytest

from devtools import overview_data, render_overview, result_overview
from devtools.repo_links import REPO

#: What the Pages jobs' partial checkouts leave out, as `pages.yml` writes the patterns
#: (`!/packing/resources/*/`, `!/packing/campaign/*/`, which
#: `test_pages_workflow` holds): every directory directly under either, with all it
#: holds. The files directly under them, `bibliography.yaml` among them, are kept.
PARTIAL_CHECKOUT_OMITS = (REPO / "packing" / "resources", REPO / "packing" / "campaign")


def leave_out_the_archive_and_the_campaign(monkeypatch: pytest.MonkeyPatch) -> None:
    """Make the working tree answer as a Pages job's checkout does: nothing under a
    directory of `PARTIAL_CHECKOUT_OMITS` is a file, is a directory or exists. Git still
    has every path, as it does there. A renderer that reads the content of such a file
    is not caught here; the Pages job itself fails on that."""
    asked = {name: getattr(Path, name) for name in ("is_file", "is_dir", "exists")}

    def omitted(path: Path) -> bool:
        for root in PARTIAL_CHECKOUT_OMITS:
            if not path.is_absolute() or root not in path.parents:
                continue
            below = path.relative_to(root).parts
            if len(below) > 1 or asked["is_dir"](path):
                return True
        return False

    def patched(name: str) -> Callable[..., bool]:
        def answer(self: Path, *args: object, **kwargs: object) -> bool:
            return False if omitted(self) else asked[name](self, *args, **kwargs)

        return answer

    for name in asked:
        monkeypatch.setattr(Path, name, patched(name))


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
