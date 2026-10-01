"""Re-pinning the data revision is one line, written by one command, and rebuilds nothing.

Until 2026-10-01 a re-pin also ran `build_known_best_atlas --update`, which took seven
to eighteen minutes and rewrote eight binaries. `devtools.release_pin` is what is left
of that step: it reads git and writes the one line `tests/test_release.py` holds to it.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from devtools import release_pin
from sqpack import release

#: The identity and settings a scratch repository commits under, so the user's global
#: signing and hooks cannot reach it.
SCRATCH_GIT = (
    "-c",
    "user.name=release pin test",
    "-c",
    "user.email=release-pin-test@example.invalid",
    "-c",
    "commit.gpgsign=false",
    "-c",
    "core.hooksPath=/dev/null",
)
SOURCE = (
    '"""A scratch release module."""\n\n'
    "#: Not the pin: an example in prose, DATA_REVISION = "
    '"0000000000000000000000000000000000000000"\n'
    'DATA_REVISION = "{revision}"\n'
    "DATA_REVISION_LENGTH = 6\n"
)


def _git(repo: Path, *arguments: str) -> str:
    done = subprocess.run(
        ("git", "-C", str(repo), *SCRATCH_GIT, *arguments),
        capture_output=True,
        text=True,
        check=True,
    )
    return done.stdout.strip()


def _commit(repo: Path, path: str, text: str) -> str:
    target = repo / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text)
    _git(repo, "add", path)
    _git(repo, "commit", "--quiet", "-m", f"touch {path}")
    return _git(repo, "rev-parse", "HEAD")


@pytest.fixture
def scratch(tmp_path: Path) -> tuple[Path, Path, str, str]:
    """A repository whose release module pins its first data commit, with a second made.

    Returns the repository, the release module, the pinned commit and the last data
    commit, which the pin now trails.
    """
    repo = tmp_path / "origin"
    repo.mkdir()
    _git(repo, "init", "--quiet")
    first = _commit(repo, "packing/frontier/n-017.md", "first\n")
    source = repo / "packing/src/sqpack/release.py"
    _commit(repo, "packing/src/sqpack/release.py", SOURCE.format(revision=first))
    last = _commit(repo, "packing/frontier/n-017.md", "second\n")
    return repo, source, first, last


def test_the_pin_is_read_and_written_as_one_line() -> None:
    """Every other byte of the module is left as it was, the look-alike in prose included."""
    first, second = "1" * 40, "2" * 40
    text = SOURCE.format(revision=first)
    assert release_pin.pinned(text) == first
    assert release_pin.repinned(text, second) == SOURCE.format(revision=second)
    assert release_pin.repinned(text, first) == text
    with pytest.raises(ValueError, match="not a full commit"):
        release_pin.repinned(text, "afd831")
    with pytest.raises(ValueError, match="exactly once; found 0"):
        release_pin.pinned("DATA_REVISION = compute()\n")
    with pytest.raises(ValueError, match="exactly once; found 2"):
        release_pin.pinned(text + f'DATA_REVISION = "{second}"\n')


def test_the_real_release_module_has_exactly_one_pin_and_it_is_the_one_imported() -> None:
    assert release_pin.pinned(release_pin.RELEASE.read_text()) == release.DATA_REVISION


def test_a_stale_pin_is_reported_then_repinned_and_only_the_pin_changes(
    scratch: tuple[Path, Path, str, str], capsys: pytest.CaptureFixture[str]
) -> None:
    """The whole of what a contributor does after a data commit.

    `--check` fails and names the command; `--update` writes the line; `--check` passes;
    and the working tree's only change is that line of that file, with no artifact
    beside it.
    """
    repo, source, first, last = scratch
    assert release_pin.check(repo, source) == 1
    assert f"the data changed at {last[:12]} and release.py pins {first[:12]}" in (
        capsys.readouterr().err
    )

    assert release_pin.update(repo, source) == 0
    assert (
        f"re-pinned DATA_REVISION from {first[:12]} to {last[:12]}" in capsys.readouterr().out
    )
    assert source.read_text() == SOURCE.format(revision=last)
    assert _git(repo, "status", "--porcelain") == "M packing/src/sqpack/release.py"
    assert _git(repo, "diff", "--numstat") == "1\t1\tpacking/src/sqpack/release.py"

    assert release_pin.check(repo, source) == 0
    assert release_pin.update(repo, source) == 0
    assert "already the last data commit" in capsys.readouterr().out

    # The re-pin is not a data commit, so committing it leaves the pin right.
    _git(repo, "commit", "--quiet", "-am", "release: re-pin")
    assert release_pin.check(repo, source) == 0


def test_a_repin_is_refused_while_the_data_has_uncommitted_changes(
    scratch: tuple[Path, Path, str, str], capsys: pytest.CaptureFixture[str]
) -> None:
    """The pin names a commit, so the commit has to exist before it can be pinned."""
    repo, source, first, _last = scratch
    (repo / "packing/frontier/n-018.md").write_text("not committed\n")
    assert release_pin.update(repo, source) == 1
    assert "uncommitted changes" in capsys.readouterr().err
    assert source.read_text() == SOURCE.format(revision=first)

    # A redrawn poster is not data, and does not hold a re-pin up.
    (repo / "packing/frontier/n-018.md").unlink()
    poster = repo / "packing/atlas/known-best/known-best-1-100.svg"
    poster.parent.mkdir(parents=True)
    poster.write_text("<svg/>\n")
    assert release_pin.update(repo, source) == 0


def test_where_git_cannot_name_a_data_commit_the_command_says_so(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(release_pin, "REPO", tmp_path)
    assert release_pin.main(["--check"]) == 1
    assert "FAIL: git cannot name the last data commit" in capsys.readouterr().err
