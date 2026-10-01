#!/usr/bin/env python3
"""Keep a migrated Markdown file's mathematics in LaTeX math: the migration's ratchet.

`devtools.migrate_math` moves mathematics written as code spans (`` `s(11) ≥ 31/8` ``)
into LaTeX math (`$s(11) \\ge 31/8$`), one file at a time, and
`packing/devtools/math-migrated.yaml` lists the files it has done. This check holds
those files where they are: in a listed file, a code span the migration tool classifies
as mathematics -- one `migrate_math --apply` would convert -- is a failure, and the
message is the conversion to make. A file not yet listed is never read, only counted,
so the backlog stays visible without failing anyone for it.

The ledger itself is checked too: a listed path must be a tracked Markdown file, and a
`keep` entry must still match a math-like span in its file, since an exception nothing
uses is one nobody will remember the reason for.

Usage, from `packing/`:

    uv run --frozen --group dev python -m devtools.check_math_markup

Exits 1 on a math code span in a migrated file or a ledger problem, 0 otherwise.
"""

from __future__ import annotations

import sys
from collections.abc import Sequence
from pathlib import Path

from devtools.migrate_math import LEDGER, REPO, Finding, Keep, analyze, load_ledger
from devtools.repo_scope import tracked_files

#: Markdown this migration never touches: archived source and vendored submodules.
NEVER_MIGRATED = ("packing/resources/", "vendor/")


def _unmigrated(ledger: dict[str, tuple[Keep, ...]]) -> int | None:
    """How many tracked Markdown files are not yet migrated, or None outside a checkout."""
    tracked = tracked_files(REPO, "*.md")
    if tracked is None:
        return None
    names = (path.relative_to(REPO).as_posix() for path in tracked)
    return sum(
        1 for name in names if name not in ledger and not name.startswith(NEVER_MIGRATED)
    )


def problems(ledger: dict[str, tuple[Keep, ...]], root: Path = REPO) -> list[str]:
    """Every math code span in a migrated file, and every ledger entry that is wrong."""
    found: list[str] = []
    for name, keep in sorted(ledger.items()):
        path = root / name
        if not name.endswith(".md") or not path.is_file():
            found.append(f"{name}: listed in {LEDGER.name} but not a Markdown file here")
            continue
        text = path.read_text(encoding="utf-8")
        findings: list[Finding] = analyze(text, keep)
        found.extend(
            f"{name}:{finding.span.line}: math written as code `{finding.span.content}`; "
            f"write ${finding.classification.latex}$"
            for finding in findings
            if finding.converts
        )
        stale = [
            entry
            for entry in keep
            if not any(
                entry.matches(text, finding.span)
                for finding in findings
                if finding.classification.kind == "math"
            )
        ]
        found.extend(
            f"{name}: keeps `{entry.span}`"
            + (f" where the line holds {entry.where!r}" if entry.where else "")
            + ", which no math-like span there matches any more"
            for entry in stale
        )
    return found


def main(argv: Sequence[str] | None = None) -> int:
    if argv:
        print("check_math_markup takes no arguments", file=sys.stderr)
        return 2
    ledger = load_ledger()
    found = problems(ledger)
    for problem in found:
        print(problem, file=sys.stderr)
    remaining = _unmigrated(ledger)
    backlog = "" if remaining is None else f"; {remaining} tracked Markdown files not yet"
    print(f"math markup: {len(ledger)} files migrated{backlog}")
    if found:
        print(
            f"{len(found)} problem(s): convert with `python -m devtools.migrate_math FILE "
            f"--apply`, or keep a span as code in {LEDGER.name} with the reason",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
