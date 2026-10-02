"""`tests.site_browser` launches the site's Chromium with its text unhinted, and fails
rather than skips where a run requires a Chromium it cannot launch (D-513)."""

from __future__ import annotations

from typing import Any

import pytest

from devtools import preview_site
from devtools.render_n11_lower_bounds_explainer_pdf import BROWSER_OVERRIDE
from tests import site_browser


class _Chromium:
    def __init__(self, error: Exception | None = None) -> None:
        self.error = error
        self.launched: list[dict[str, Any]] = []

    def launch(self, **options: Any) -> str:
        if self.error is not None:
            raise self.error
        self.launched.append(options)
        return "browser"


class _Driver:
    def __init__(self, chromium: _Chromium) -> None:
        self.chromium = chromium


def test_the_site_is_measured_with_hinting_off(monkeypatch: pytest.MonkeyPatch) -> None:
    """The launch carries `--font-render-hinting=none` ahead of any other argument, and
    the Chromium `SQPACK_CHROMIUM` names when it names one."""
    monkeypatch.setenv(BROWSER_OVERRIDE, "/opt/chromium")
    chromium = _Chromium()
    driver: Any = _Driver(chromium)
    assert preview_site.launch_chromium(driver, args=["--x"], headless=True) == "browser"
    assert chromium.launched == [
        {
            "executable_path": "/opt/chromium",
            "args": ["--font-render-hinting=none", "--x"],
            "headless": True,
        }
    ]
    monkeypatch.delenv(BROWSER_OVERRIDE)
    preview_site.launch_chromium(driver)
    assert chromium.launched[-1] == {
        "executable_path": None,
        "args": ["--font-render-hinting=none"],
    }


def test_no_chromium_skips_locally_and_fails_where_required(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sync_api = pytest.importorskip("playwright.sync_api")
    error = sync_api.Error("Executable doesn't exist at /nowhere\nmore")
    driver: Any = _Driver(_Chromium(error))
    monkeypatch.delenv(site_browser.REQUIRED, raising=False)
    assert not site_browser.required()
    with pytest.raises(pytest.skip.Exception) as skipped:
        site_browser.launch(driver)
    assert "no Chromium to launch: Executable doesn't exist at /nowhere" in str(skipped.value)
    monkeypatch.setenv(site_browser.REQUIRED, "1")
    assert site_browser.required()
    with pytest.raises(pytest.fail.Exception) as failed:
        site_browser.launch(driver)
    assert site_browser.REQUIRED in str(failed.value)
    assert "Executable doesn't exist at /nowhere" in str(failed.value)
