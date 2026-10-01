"""Controls for updating only the atlas footer and its export receipts."""

from __future__ import annotations

import subprocess

import pytest

from devtools import build_known_best_atlas as atlas


def test_restamp_preserves_every_nonfooter_svg_byte() -> None:
    original = (
        '<svg xmlns="http://www.w3.org/2000/svg"><g data-feature="packing-card">'
        '<polygon points="0,0 1,0 1,1"/></g>'
        '<text data-feature="release-stamp" x="4">v0.4.2-old123</text></svg>'
    )
    updated = atlas.restamped_svg(original, "v0.4.2-new456")
    assert updated == original.replace("v0.4.2-old123", "v0.4.2-new456")
    assert atlas.restamped_svg(updated, "v0.4.2-new456") == updated
    crlf = original.replace("><", ">\r\n<")
    assert atlas.restamped_svg(crlf, "v0.4.2-new456") == crlf.replace(
        "v0.4.2-old123", "v0.4.2-new456"
    )


@pytest.mark.parametrize(
    "source",
    [
        '<svg xmlns="http://www.w3.org/2000/svg"/>',
        (
            '<svg xmlns="http://www.w3.org/2000/svg">'
            '<text data-feature="release-stamp">a</text>'
            '<text data-feature="release-stamp">b</text></svg>'
        ),
        (
            '<svg xmlns="http://www.w3.org/2000/svg"><text data-feature="release-stamp">'
            "<tspan>nested</tspan></text></svg>"
        ),
    ],
)
def test_restamp_refuses_missing_duplicate_or_nested_footer(source: str) -> None:
    with pytest.raises(ValueError, match="exactly one plain"):
        _ = atlas.restamped_svg(source, "new")


def test_source_guard_refuses_changed_geometry_inputs(monkeypatch: pytest.MonkeyPatch) -> None:
    def git_result(*arguments: str) -> subprocess.CompletedProcess[str]:
        if arguments[0] == "log":
            return subprocess.CompletedProcess(arguments, 0, "a" * 40 + "\n", "")
        if arguments[0] == "show":
            relative = arguments[1].split(":", 1)[1]
            return subprocess.CompletedProcess(
                arguments, 0, (atlas.REPOSITORY_ROOT / relative).read_text("utf-8"), ""
            )
        return subprocess.CompletedProcess(arguments, 1, "", "")

    monkeypatch.setattr(atlas, "_git_result", git_result)
    monkeypatch.setattr(atlas, "source_plans", dict)
    with pytest.raises(ValueError, match="geometry inputs changed"):
        atlas.restamp_source_guard()


def test_source_guard_refuses_edited_svg_or_other_frontier_case(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def git_result(*arguments: str) -> subprocess.CompletedProcess[str]:
        if arguments[0] == "log":
            return subprocess.CompletedProcess(arguments, 0, "a" * 40 + "\n", "")
        if arguments[0] == "show":
            relative = arguments[1].split(":", 1)[1]
            content = (atlas.REPOSITORY_ROOT / relative).read_text("utf-8")
            return subprocess.CompletedProcess(arguments, 0, content, "")
        if "--name-only" in arguments:
            assert "HEAD" not in arguments
            return subprocess.CompletedProcess(arguments, 0, "packing/frontier/n-018.md\n", "")
        return subprocess.CompletedProcess(arguments, 0, "", "")

    monkeypatch.setattr(atlas, "_git_result", git_result)
    monkeypatch.setattr(atlas, "source_plans", dict)
    with pytest.raises(ValueError, match="other than n-017"):
        atlas.restamp_source_guard()

    def edited_svg(*arguments: str) -> subprocess.CompletedProcess[str]:
        if arguments[0] == "show":
            return subprocess.CompletedProcess(arguments, 0, "edited svg", "")
        return git_result(*arguments)

    monkeypatch.setattr(atlas, "_git_result", edited_svg)
    with pytest.raises(ValueError, match="differs from its retained composite build"):
        atlas.restamp_source_guard()
