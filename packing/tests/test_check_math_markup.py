"""Controls for the math-markup ratchet, `devtools.check_math_markup`.

The ratchet's contract has three halves, each pinned on a repository built in `tmp_path`:
a migrated file with a new math code span fails, with the LaTeX to write; a `keep` entry
lets one span stay code and fails once the span is gone; and a file that is not migrated
is never read, only counted, with generated views and excluded files counted apart. The
real register is checked last, against the real repository.
"""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from devtools.check_math_markup import (
    REGISTER,
    Keep,
    Register,
    RegisterError,
    check,
    load_register,
    main,
    scope,
)

DOCUMENT_MAP = textwrap.dedent(
    """\
    softschema: {contract: 'packing.squares:DocumentMap/v1', status: enforced}
    documents:
      - {path: STATUS.md, role: generated-view, authority: generated, lifecycle: generated}
      - {path: guide.md, role: tutorial, authority: current, lifecycle: maintained}
    exclusions:
      - pattern: archive/**/*.md
        reason: Source-faithful transcriptions.
    """
)


def _write(root: Path, relative: str, text: str) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """A small repository with every kind of Markdown file the ratchet sorts."""
    _write(tmp_path, "docs/project/document-map.yaml", DOCUMENT_MAP)
    _write(tmp_path, ".flowmarkignore", "# preserved\nreviews/quoted.md\n")
    _write(tmp_path, "guide.md", "# Guide\n\nThe bound $s(11) \\ge 31/8$ for `T-018`.\n")
    _write(tmp_path, "notes.md", "An unmigrated `s(11) ≥ 31/8`.\n")
    _write(tmp_path, "STATUS.md", "A generated `n = 11`.\n")
    _write(tmp_path, "archive/paper/source.md", "Archived `n = 11`.\n")
    _write(tmp_path, "reviews/quoted.md", "Quoted `n = 11`.\n")
    _write(tmp_path, ".agents/skills/x/SKILL.md", "A skill's `n = 11`.\n")
    return tmp_path


def test_scope_sorts_every_markdown_file(repo: Path) -> None:
    files = scope(repo)
    assert files.eligible == {"guide.md", "notes.md"}
    assert files.generated == {"STATUS.md"}
    assert files.excluded == {
        "archive/paper/source.md": "document-map exclusion",
        "reviews/quoted.md": "flowmark exclusion",
        ".agents/skills/x/SKILL.md": "tool-owned",
    }


def test_a_clean_migrated_file_passes(repo: Path) -> None:
    outcome = check(Register(("guide.md",), ()), repo)
    assert outcome.problems == []


def test_a_new_math_code_span_in_a_migrated_file_fails(repo: Path) -> None:
    _write(
        repo, "guide.md", "# Guide\n\nThe bound $s(11) \\ge 31/8$.\n\nAgain `n = 11` here.\n"
    )
    (problem,) = check(Register(("guide.md",), ()), repo).problems
    assert problem.startswith("guide.md:5: `n = 11` is mathematics written as code")
    assert "write $n = 11$" in problem


def test_math_github_shows_as_dollars_fails_with_the_code_to_write(repo: Path) -> None:
    _write(
        repo,
        "guide.md",
        "# Guide\n\nA side-$B$ square, the [case $n = 7$](n.md) and *the $n = 11$ one*.\n",
    )
    problems = check(Register(("guide.md",), ()), repo).problems
    assert [problem.split(" -- ")[0] for problem in problems] == [
        "guide.md:3: $B$ is shown as dollars on GitHub",
        "guide.md:3: $n = 7$ is shown as dollars on GitHub",
        "guide.md:3: $n = 11$ is shown as dollars on GitHub",
    ]
    assert "write `B`" in problems[0]
    assert "a link's text" in problems[1]
    assert "italics" in problems[2]


def test_identifier_uncertain_and_heading_spans_never_fail(repo: Path) -> None:
    _write(
        repo,
        "guide.md",
        "# The `n = 11` case\n\nSee `T-018`, `V4/C3`, `s(11) >= 381/100` and `1.28 ms`.\n",
    )
    assert check(Register(("guide.md",), ()), repo).problems == []


def test_keep_lets_one_span_stay_code_and_a_stale_keep_fails(repo: Path) -> None:
    _write(repo, "guide.md", "Kept `n = 11` as code.\n")
    kept = Keep("guide.md", "n = 11", "quoted from a command's output")
    outcome = check(Register(("guide.md",), (kept,)), repo)
    assert outcome.problems == []
    assert outcome.kept == 1
    _write(repo, "guide.md", "Now $n = 11$ is math.\n")
    (problem,) = check(Register(("guide.md",), (kept,)), repo).problems
    assert "no longer a math code span" in problem


def test_an_unmigrated_file_is_never_read(repo: Path) -> None:
    """Bytes that are not UTF-8 would raise if the ratchet opened the file."""
    (repo / "notes.md").write_bytes(b"\xff\xfe not text `n = 11`\n")
    assert check(Register(("guide.md",), ()), repo).problems == []


def test_only_hand_written_tracked_markdown_can_be_listed(repo: Path) -> None:
    outcome = check(Register(("STATUS.md", "archive/paper/source.md", "missing.md"), ()), repo)
    generated = "a generated view, migrated at its renderer"
    assert outcome.problems == [
        f"math-markup.yaml: STATUS.md cannot be listed: {generated}",
        "math-markup.yaml: archive/paper/source.md cannot be listed: document-map exclusion",
        "math-markup.yaml: missing.md cannot be listed: not a tracked Markdown file",
    ]


def test_the_register_must_be_sorted_and_keep_only_migrated_files(repo: Path) -> None:
    outcome = check(Register(("notes.md", "guide.md"), (Keep("other.md", "n", "why"),)), repo)
    assert "math-markup.yaml: `migrated` must be sorted and unique" in outcome.problems
    assert "math-markup.yaml: `keep` names other.md, not migrated" in outcome.problems


@pytest.mark.parametrize(
    "text",
    [
        "migrated: []\n",
        "migrated: [a.md]\nkeep: [{path: a.md, span: n}]\n",
        "migrated: [a.md]\nkeep: [{path: a.md, span: n, reason: ''}]\n",
        "migrated: a.md\nkeep: []\n",
    ],
)
def test_a_malformed_register_is_refused(tmp_path: Path, text: str) -> None:
    register = tmp_path / "math-markup.yaml"
    register.write_text(text, encoding="utf-8")
    with pytest.raises(RegisterError):
        load_register(register)
    assert main(["--register", str(register), "--repo", str(tmp_path)]) == 2


def test_the_command_reports_the_backlog(
    repo: Path, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    register = tmp_path / "register.yaml"
    register.write_text("migrated: [guide.md]\nkeep: []\n", encoding="utf-8")
    assert main(["--register", str(register), "--repo", str(repo), "--backlog"]) == 0
    output = capsys.readouterr().out
    assert "1 of 2 hand-written Markdown files not yet migrated" in output
    assert "1 generated views move at their renderers" in output
    assert "3 excluded (document-map exclusion 1, flowmark exclusion 1, tool-owned 1)" in output
    assert "    notes.md" in output


def test_the_command_fails_on_a_finding(
    repo: Path, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    register = tmp_path / "register.yaml"
    register.write_text("migrated: [guide.md, notes.md]\nkeep: []\n", encoding="utf-8")
    assert main(["--register", str(register), "--repo", str(repo)]) == 1
    assert (
        "notes.md:1: `s(11) ≥ 31/8` is mathematics written as code" in capsys.readouterr().err
    )


def test_the_real_register_holds_and_every_migrated_file_passes() -> None:
    register = load_register(REGISTER)
    assert check(register).problems == []
