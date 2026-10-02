"""The Chromium the site's tests measure in, launched one way.

The site's layout tests pin pixels: a 24ch measure at 224.8 px, a credit column at its
184 px floor, a frontier table that fills its 1200 px track exactly. They were measured
in Playwright's pinned Chromium headless shell on macOS, and the same shell on Linux read
every one of them wider, by whole pixels of text: the shell hints text at `HINTING_FULL`
unless told otherwise, which on Linux rounds each glyph's advance to a whole pixel, so
the 24ch measure read 232 px, 9 px a digit, where macOS reads 8.7, and eleven tests
failed on main's first full run with the pins (run 36943941580, D-513). The faces are the
page's own, inlined; what differed was how the shell metered them.

So `devtools.preview_site.launch_chromium` launches with `--font-render-hinting=none`,
and the site's tests launch through `launch` here, which skips where no Chromium can be
launched -- unless `REQUIRED` is set, when the gate step that owns them has installed one
and a skip would be a hole in the surface. It was one: the behavioural shards install no
browser, so these tests skipped on every pull request, and main's runs reused the pull
requests' trees, so nothing read them on Linux until that run.
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any, NoReturn

import pytest

from devtools import preview_site

if TYPE_CHECKING:
    from playwright.sync_api import Browser, Playwright

#: Set by the gate step that owns the site's browser tests: a Chromium that cannot be
#: launched fails the test instead of skipping it. `sqpack.cli.validate.REQUIRE_CHROMIUM`
#: is the same name, where the step sets it.
REQUIRED = "SQPACK_REQUIRE_CHROMIUM"


def required() -> bool:
    """Whether this run has said it must have a Chromium."""
    return bool(os.environ.get(REQUIRED))


def unavailable(reason: str) -> NoReturn:
    """Skip the test for `reason`, or fail it where the run requires a Chromium."""
    if required():
        pytest.fail(f"{reason}; {REQUIRED} is set, so this run must have a Chromium to launch")
    pytest.skip(reason)


def api() -> Any:
    """`playwright.sync_api`, or a skip where it is not installed (a failure where
    the run requires a Chromium)."""
    try:
        from playwright import sync_api  # noqa: PLC0415
    except ImportError as error:
        unavailable(f"playwright is not installed: {error}")
    return sync_api


def launch(driver: Playwright) -> Browser:
    """The site's Chromium, launched through `driver` as `launch_chromium` launches it;
    a skip where none can be launched (a failure where the run requires one)."""
    sync_api = api()
    try:
        return preview_site.launch_chromium(driver)
    except sync_api.Error as error:
        unavailable(f"no Chromium to launch: {error.message.splitlines()[0]}")
