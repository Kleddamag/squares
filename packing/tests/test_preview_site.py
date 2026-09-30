"""The local site preview's own decisions, without a browser.

`devtools.preview_site` opens every page in Chromium, which is the owner's review and the
`overview` job's smoke check rather than something a unit test repeats. What can be pinned
here is what it decides before and after the browser: which relative references name a
file the assembled site lacks, which pages the math-face walk covers, and that the films
it copies only on `main` are noted rather than failed.
"""

from __future__ import annotations

from pathlib import Path

from devtools import preview_site
from devtools.preview_site import Findings, missing_references, resolve, site_math


def test_references_resolve_against_the_page_that_names_them() -> None:
    assert resolve("index.html", "frontier.html") == "frontier.html"
    assert resolve("index.html", "./") == "index.html"
    assert resolve("workbench/index.html", "../explainer.html#s-3") == "explainer.html"
    assert resolve("index.html", "workbench/") == "workbench/index.html"
    assert resolve("index.html", "films/n-324.mp4") == "films/n-324.mp4"


def test_absolute_and_fragment_references_are_not_the_sites_to_check() -> None:
    assert resolve("index.html", "https://github.com/jlevy/squares") is None
    assert resolve("index.html", "#results") is None
    assert resolve("index.html", "data:image/svg+xml,%3Csvg%3E") is None


def test_a_missing_file_fails_and_a_film_off_main_is_noted(tmp_path: Path) -> None:
    (tmp_path / "frontier.html").write_text("", encoding="utf-8")
    findings = Findings()
    missing_references(
        tmp_path,
        "index.html",
        ["frontier.html", "tutorial.html", "films/n-100.mp4", "../outside.html"],
        findings,
        films=False,
    )
    assert findings.problems == [
        "index.html: tutorial.html names tutorial.html, which the site lacks",
        "index.html: ../outside.html leaves the site",
    ]
    assert findings.notes == [
        "index.html: films/n-100.mp4 is copied into the site on main only"
    ]


def test_a_film_is_required_once_the_films_are_supplied(tmp_path: Path) -> None:
    findings = Findings()
    missing_references(tmp_path, "index.html", ["films/n-100.mp4"], findings, films=True)
    assert findings.problems == [
        "index.html: films/n-100.mp4 names films/n-100.mp4, which the site lacks"
    ]


def test_the_face_walk_covers_the_sites_own_pages_only() -> None:
    assert site_math("index.html")
    assert site_math("frontier.html")
    assert site_math("tutorial.html")
    assert not site_math(preview_site.EXPLAINER_PAGE)
    assert not site_math("workbench/index.html")


def test_the_walk_and_the_typesetting_are_probes_on_disk() -> None:
    for name in ("math_face", "typeset_all", "ready", "overflow", "links"):
        assert (preview_site.PROBES / "preview_site" / f"{name}.js").is_file(), name
