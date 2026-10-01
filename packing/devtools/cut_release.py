#!/usr/bin/env python3
"""Prepare a version bump: name the edition, redraw the release assets, and check them.

A version bump is when the large generated assets are rebuilt (the owner, 2026-10-01),
and it was a paragraph of manual steps in `development.md`. This is those steps as one
command. It edits `sqpack/release.py`, redraws the atlas posters, regenerates the claim
documents and runs the checks that hold them, in that order, and stops at the first
failure. It commits nothing, tags nothing and publishes nothing: those are the owner's,
and it ends by printing them.

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m devtools.cut_release v0.5.0 \
        --scope "One sentence on what the edition adds." --dry-run
    uv run --frozen --all-extras --group dev python -m devtools.cut_release v0.5.0 \
        --scope "One sentence on what the edition adds."

`--date` is the day the edition will first be published, written `October 2, 2026`; it
defaults to today in UTC, which is how `PUBLICATION_HISTORY` dates an edition, and is
corrected afterwards if the deployment lands on another day. `--dry-run` prints the plan
and changes nothing. On macOS the redraw needs Homebrew's Cairo:
`DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib` (development.md, Supported Environment).
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import textwrap
from collections.abc import Sequence
from datetime import UTC, datetime
from pathlib import Path

from strif import atomic_output_file

from devtools import release_pin
from sqpack import release

PACKING = Path(__file__).resolve().parents[1]
REPO = PACKING.parent
VERSION = re.compile(r"v(\d+)\.(\d+)\.(\d+)")
HISTORY_OPEN = "PUBLICATION_HISTORY = (\n"
REVISION_LINE = re.compile(r'^PUBLICATION_REVISION = "([0-9a-f]{7,40})"$', re.MULTILINE)
#: How wide a line of the edition's scope may be once it is indented and quoted.
SCOPE_WIDTH = 76
#: The pull-request tests that hold an edition: the stamp, the page that prints it, the
#: claim documents that link its revision, and the posters redrawn for it.
TESTS = (
    "tests/test_release.py",
    "tests/test_explainer.py",
    "tests/test_verify_claim.py",
    "tests/test_known_best_composites.py",
    "tests/test_artifact_dates.py",
)


def parsed(version: str) -> tuple[int, int, int]:
    found = VERSION.fullmatch(version)
    if found is None:
        raise ValueError(f"{version!r} is not a version: vMAJOR.MINOR.PATCH")
    major, minor, patch = (int(part) for part in found.groups())
    return major, minor, patch


def with_edition(
    source: str, *, version: str, first_published: str, scope: str, revision: str
) -> str:
    """`source`, the text of `release.py`, with a new edition at the front of its history.

    The entry is written the way the formatter leaves one, so the lint floor passes on
    the result. `PUBLICATION_REVISION` becomes `revision`, the commit the claim
    documents link to. `DATA_REVISION` is left alone: it follows the data, not the
    edition.
    """
    current = release.PUBLICATION_HISTORY[0].version
    if parsed(version) <= parsed(current):
        raise ValueError(f"{version} is not after the current edition, {current}")
    datetime.strptime(first_published, "%B %d, %Y")  # noqa: DTZ007
    if scope.strip() != scope or not scope.endswith(".") or "\n" in scope:
        raise ValueError("the scope is one trimmed sentence ending in a full stop")
    if re.fullmatch(r"[0-9a-f]{7,40}", revision) is None:
        raise ValueError(f"{revision!r} is not a commit")
    if source.count(HISTORY_OPEN) != 1 or len(REVISION_LINE.findall(source)) != 1:
        raise ValueError("release.py is not laid out as cut_release expects")
    pieces = textwrap.wrap(scope, SCOPE_WIDTH, break_long_words=False, break_on_hyphens=False)
    # Every piece but the last carries the space that joined it to the next.
    quoted = [
        json.dumps(piece + (" " if index < len(pieces) - 1 else ""), ensure_ascii=False)
        for index, piece in enumerate(pieces)
    ]
    literal = (
        f"result_scope={quoted[0]},"
        if len(quoted) == 1 and len(quoted[0]) <= SCOPE_WIDTH - 8
        else "result_scope=(\n"
        + "".join(f"            {piece}\n" for piece in quoted)
        + "        ),"
    )
    entry = (
        "    PublicationHistoryEntry(\n"
        f'        version="{version}",\n'
        f'        first_published="{first_published}",\n'
        f"        {literal}\n"
        "    ),\n"
    )
    bumped = source.replace(HISTORY_OPEN, HISTORY_OPEN + entry)
    return REVISION_LINE.sub(f'PUBLICATION_REVISION = "{revision}"', bumped)


def _git(*arguments: str) -> str:
    done = subprocess.run(
        ("git", "-C", str(REPO), *arguments), capture_output=True, text=True, check=True
    )
    return done.stdout.strip()


def steps(version: str) -> list[tuple[str, tuple[str, ...]]]:
    """What runs after `release.py` is edited, each as a module's own command."""
    return [
        (
            "redraw both atlas posters and their six exports",
            ("devtools.build_known_best_atlas", "--update-composites"),
        ),
        ("regenerate the claim documents", ("devtools.render_verifiable_claim",)),
        (
            f"hold the posters to {version}",
            ("devtools.build_known_best_atlas", "--check-composites"),
        ),
        ("run the tests that hold an edition", ("pytest", "-q", *TESTS)),
    ]


def remaining(version: str) -> str:
    """What the command leaves to the owner, as text to print."""
    family = "packing/atlas/known-best/known-best-1-*"
    return textwrap.dedent(
        f"""\
        Left to do, none of it done here:
          1. Review the diff, then commit release.py, the eight atlas files and the
             regenerated claim documents together, and merge.
          2. Wait for the "Certificate page" workflow on main, then from packing/:
               python -m devtools.check_published_site --commit <merge commit>
          3. If the deployment's UTC date is not the one in PUBLICATION_HISTORY, correct
             it, and record the deployment in the comment above the history.
          4. Tag the merge and create the release, with the posters attached:
               git tag {version} <merge commit> && git push origin {version}
               gh release create {version} --title {version} --notes-file <notes> \\
                   {family}.pdf {family}.png
          5. The films stay on the release that carries them
             (render_overview.FILM_RELEASE) until they are cut again:
             packages/workbench/README.md has that runbook."""
    )


def prepared(version: str, first_published: str, scope: str) -> tuple[str, str]:
    """The revision the claim documents will link and `release.py` as bumped, or a refusal.

    Refused before anything is written: a bump that is not one, a tree with uncommitted
    changes, and a stale pin. A poster drawn over either of the last two would be stamped
    with data it does not show.
    """
    revision = _git("rev-parse", "--short=8", "HEAD")
    bumped = with_edition(
        release_pin.RELEASE.read_text(encoding="utf-8"),
        version=version,
        first_published=first_published,
        scope=scope,
        revision=revision,
    )
    dirty = _git("status", "--porcelain")
    if dirty:
        raise ValueError(f"the working tree is not clean:\n{dirty}")
    if release_pin.check(REPO, release_pin.RELEASE) != 0:
        raise ValueError("the pinned data revision is stale; re-pin and commit first")
    return revision, bumped


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("version", help="the new edition, as vMAJOR.MINOR.PATCH")
    parser.add_argument("--scope", required=True, help="one sentence: what the edition adds")
    parser.add_argument("--date", help="the day it is first published: October 2, 2026")
    parser.add_argument("--dry-run", action="store_true", help="print the plan; change nothing")
    arguments = parser.parse_args(argv)
    today = datetime.now(UTC)
    first_published = arguments.date or f"{today:%B} {today.day}, {today.year}"
    try:
        revision, bumped = prepared(arguments.version, first_published, arguments.scope)
    except (RuntimeError, ValueError, subprocess.CalledProcessError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    plan = steps(arguments.version)
    print(
        f"{release.PUBLICATION_VERSION} -> {arguments.version}, first published "
        f"{first_published}, claim documents linked at {revision}"
    )
    print("  1. add the edition to release.PUBLICATION_HISTORY and set PUBLICATION_REVISION")
    for number, (what, command) in enumerate(plan, start=2):
        print(f"  {number}. {what}: python -m {' '.join(command)}")
    if arguments.dry_run:
        print("dry run: nothing was changed")
        print(remaining(arguments.version))
        return 0
    with atomic_output_file(release_pin.RELEASE) as temporary:
        temporary.write_text(bumped, encoding="utf-8")
    for what, command in plan:
        print(f"+ {what}", flush=True)
        done = subprocess.run((sys.executable, "-m", *command), cwd=PACKING, check=False)
        if done.returncode != 0:
            print(
                f"FAIL: could not {what}. release.py is edited and anything already "
                "redrawn is in the tree; fix the cause and rerun the remaining commands "
                "above by hand",
                file=sys.stderr,
            )
            return done.returncode
    print(remaining(arguments.version))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
