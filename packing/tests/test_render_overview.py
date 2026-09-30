"""The site's own pages render deterministically, into their own directory, fetching nothing.

`devtools.render_overview` is the shared skeleton the overview, the frontier atlas and the
tutorial are rendered through; each part of the site has its own tests. What is held here
is what they share: a render of one commit is byte-identical twice over, every page sits
in the shared shell with no placeholder left and nothing it would fetch at view time, the
output never lands in the explainer's directory, and the navigation bar names every page
relative to the page it is on.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from devtools import render_overview, site_kit
from devtools.render_overview import OUTPUT, RENDER_INPUTS, check, render
from devtools.site_kit import Asset, Page, base_for, nav_html

COMMIT = "0" * 40


@pytest.fixture(scope="module")
def files() -> dict[str, bytes]:
    return render(COMMIT)


def test_a_render_of_one_commit_is_byte_identical(files: dict[str, bytes]) -> None:
    assert render(COMMIT) == files


def test_every_page_is_in_the_shell_with_nothing_left_to_fill(files: dict[str, bytes]) -> None:
    pages = {
        path: content.decode("utf-8")
        for path, content in files.items()
        if path.endswith(".html")
    }
    assert "index.html" in pages
    for path, html in pages.items():
        assert not re.search(r"\{\{[A-Z_]+\}\}", html), path
        assert 'class="site-nav"' in html, path
        assert 'class="site-footer"' in html, path
        assert f"/commit/{COMMIT}" in html, path


def test_the_output_is_not_the_explainers_directory() -> None:
    assert OUTPUT != render_overview.EXPLAINER_OUTPUT
    with pytest.raises(SystemExit, match="explainer's output"):
        render_overview.main(["--output", str(render_overview.EXPLAINER_OUTPUT), "--check"])


def test_check_names_stale_missing_and_extra_files(tmp_path: Path) -> None:
    files = {"index.html": b"new", "a/b.txt": b"b"}
    (tmp_path / "index.html").write_bytes(b"old")
    (tmp_path / "extra.txt").write_bytes(b"x")
    problems = check(tmp_path, files)
    assert any("index.html is stale" in p for p in problems)
    assert any("b.txt has not been rendered" in p for p in problems)
    assert any("extra.txt is not part of the render" in p for p in problems)


def test_every_declared_input_exists() -> None:
    missing = [path for path in RENDER_INPUTS if not path.exists()]
    assert not missing


def test_the_nav_marks_the_current_page_and_links_relative_to_it() -> None:
    root = nav_html("frontier")
    assert 'href="frontier.html" aria-current="page"' in root
    assert 'href="./"' in root
    nested = nav_html("tutorial", base="../")
    assert 'href="../explainer.html"' in nested
    assert 'href="../workbench/"' in nested
    assert f'href="{site_kit.REPO_URL}" rel="noopener"' in nested
    with pytest.raises(ValueError, match="unknown site page"):
        nav_html("synopsis")


def test_pages_and_assets_refuse_paths_outside_the_site() -> None:
    assert base_for("index.html") == ""
    assert base_for("thumbs/n-011.svg") == "../"
    with pytest.raises(ValueError, match="relative to the site root"):
        Asset("../escape.txt", b"")
    with pytest.raises(ValueError, match="exactly one of markdown and html"):
        Page(key="overview", path="index.html", title="t", description="d")
