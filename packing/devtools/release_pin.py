#!/usr/bin/env python3
"""Re-pin the data revision: the one line a data commit leaves to be written.

Every page prints `sqpack.release.PUBLICATION_EDITION`, whose hash is the pinned
`DATA_REVISION`, and `tests/test_release.py` holds that pin to the last commit that
changed the data. No commit can contain its own hash, so a commit that changes the data
is followed by one that re-pins. This writes that commit's one line, and nothing else
has to be done for it: no artifact is rebuilt (`sqpack.release`, rule 3).

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m devtools.release_pin --check
    uv run --frozen --all-extras --group dev python -m devtools.release_pin --update

`--check` says whether the pin is what git says and exits 1 when it is not. `--update`
rewrites the line, and refuses while the data has uncommitted changes, since the pin
names a commit and the commit has to exist first.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path

from strif import atomic_output_file

from sqpack import release

PACKING = Path(__file__).resolve().parents[1]
REPO = PACKING.parent
RELEASE = PACKING / "src/sqpack/release.py"
#: The pin as `release.py` writes it: one assignment, at the start of a line.
PIN_LINE = re.compile(r'^DATA_REVISION = "([0-9a-f]{40})"$', re.MULTILINE)


def pinned(source: str) -> str:
    """The revision `source`, the text of `release.py`, pins."""
    found = PIN_LINE.findall(source)
    if len(found) != 1:
        raise ValueError(
            "release.py must assign DATA_REVISION a full commit exactly once; "
            f"found {len(found)}"
        )
    return found[0]


def repinned(source: str, revision: str) -> str:
    """`source` with its pin set to `revision`, and every other byte as it was."""
    if re.fullmatch(r"[0-9a-f]{40}", revision) is None:
        raise ValueError(f"{revision!r} is not a full commit")
    pinned(source)
    return PIN_LINE.sub(f'DATA_REVISION = "{revision}"', source)


def uncommitted_data(repo: Path) -> str:
    """The data paths git reports as changed and not committed, one per line."""
    found = subprocess.run(
        ("git", "-C", str(repo), "status", "--porcelain", "--", *release.data_pathspec()),
        capture_output=True,
        text=True,
        check=False,
    )
    if found.returncode != 0:
        raise RuntimeError(
            f"git cannot list the data's changes in {repo}: {found.stderr.strip()}"
        )
    return found.stdout.rstrip()


def check(repo: Path, source: Path) -> int:
    """0 when the pin is the last data commit; 1, with the remedy, when it is not."""
    now = pinned(source.read_text(encoding="utf-8"))
    live = release.data_revision(repo)
    if live == now:
        print(f"the pin is the last data commit, {live[:12]}")
        return 0
    print(
        f"the data changed at {live[:12]} and release.py pins {now[:12]}: "
        "run `python -m devtools.release_pin --update` and commit the one line",
        file=sys.stderr,
    )
    return 1


def update(repo: Path, source: Path) -> int:
    """Set the pin to the last data commit. Rewrites one line, or nothing."""
    dirty = uncommitted_data(repo)
    if dirty:
        print(
            "the data has uncommitted changes; commit them, then re-pin to that commit:\n"
            + dirty,
            file=sys.stderr,
        )
        return 1
    text = source.read_text(encoding="utf-8")
    now = pinned(text)
    live = release.data_revision(repo)
    if live == now:
        print(f"the pin is already the last data commit, {live[:12]}")
        return 0
    with atomic_output_file(source) as temporary:
        temporary.write_text(repinned(text, live), encoding="utf-8")
    print(
        f"re-pinned DATA_REVISION from {now[:12]} to {live[:12]}; commit "
        f"{source.relative_to(repo).as_posix()} alone, for example as\n"
        f"  release: re-pin DATA_REVISION to {live[:8]}"
    )
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="compare the pin with git")
    mode.add_argument("--update", action="store_true", help="set the pin to what git says")
    arguments = parser.parse_args(argv)
    try:
        return update(REPO, RELEASE) if arguments.update else check(REPO, RELEASE)
    except (RuntimeError, ValueError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
