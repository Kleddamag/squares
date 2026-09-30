#!/usr/bin/env python3
"""Backfill `registered`, the day each register entry entered `results.yaml`, from git.

The register had no registration date. `significance.scored` dates the last assessment,
`established` the day a result of this project first passed here, and
`attribution.published` the day a result by others entered its source; none of them says
when the entry was taken into this register, which the overview's results table sorts
by. The Pages build cannot read history, so the date has to be a field, and the entries
that predate the field take it once from the commit that added them.

**What "added" means.** An entry is added by the earliest commit, in the history of
`HEAD`, whose `results.yaml` holds an entry with the same `id` that is the same result: its
`n` overlap the current entry's and it has the same attribution, none for this project's
results and an overlapping set of source keys for others'. Matching the content as well
as the id matters twice in this history. On 2026-09-21 two branches each registered a
`T-031`, and the merge renumbered one of them `T-032`, so an id alone can name a
different result in an older revision. Scopes grow as a source's later releases join an
entry, so the match asks for an overlap rather than an equal scope. The date is the
committing day in UTC, the day the entry landed.

This is a one-time tool, kept so the backfill can be re-read and re-run: with no option
it prints each entry's date, its commit and any disagreement with a date already
recorded; `--write` inserts the missing dates into `results.yaml` without touching any
other line. `registered` goes right after `established` on this project's results and
right after `headline` on others', and is written in the file's own quoting. Entries
registered after this backfill carry the field from the day they are written, so nothing
runs this in the gate.

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m devtools.backfill_registered
    uv run --frozen --all-extras --group dev python -m devtools.backfill_registered --write
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from strif import atomic_output_file

from devtools.check_results import scope_values
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent
RESULTS = ROOT / "frontier" / "results.yaml"
#: The register as git names it, from the repository root.
RESULTS_PATH = RESULTS.relative_to(REPO).as_posix()

#: The line that opens an entry, and the two a date is written after.
_ENTRY = re.compile(r"^  - id: (T-\d{3})$")
_ESTABLISHED = re.compile(r"^    established: ")
_HEADLINE = re.compile(r"^    headline: ")
_KEY = re.compile(r"^    [a-z_]+:")


@dataclass(frozen=True, slots=True)
class Registration:
    """The commit that added one entry, and its day in UTC."""

    id: str
    commit: str
    day: str


def _git(*arguments: str) -> str:
    found = subprocess.run(
        ("git", *arguments),
        cwd=REPO,
        capture_output=True,
        text=True,
        check=True,
        env={**os.environ, "TZ": "UTC"},
    )
    return found.stdout


def history() -> list[tuple[str, str]]:
    """Every commit that changed the register, oldest first, with its UTC day.

    `--full-history` keeps the merges, where a renumbering can happen; the shallow clones
    a remote session starts from cannot answer, so the tool refuses one.
    """
    if _git("rev-parse", "--is-shallow-repository").strip() == "true":
        raise SystemExit("a shallow clone cannot date the register; run git fetch --unshallow")
    lines = _git(
        "log",
        "--full-history",
        "--format=%H %ct %cd",
        "--date=format-local:%Y-%m-%d",
        "--",
        RESULTS_PATH,
    ).splitlines()
    commits = [line.split(" ") for line in lines if line]
    commits.sort(key=lambda parts: (int(parts[1]), parts[0]))
    return [(commit, day) for commit, _, day in commits]


def _keys(record: Mapping[str, Any]) -> frozenset[str]:
    attribution = record.get("attribution") or {}
    return frozenset(str(key) for key in attribution.get("source_keys") or [])


def same_result(old: Mapping[str, Any], new: Mapping[str, Any]) -> bool:
    """Whether an older revision's entry is this entry: same id, `n` and attribution.

    The `attribution` field itself arrived on 2026-09-29, so an older revision of a
    result by others carries none; the sources are compared only where both name them.
    """
    if old.get("id") != new["id"]:
        return False
    try:
        overlap = scope_values(dict(old["scope"])) & scope_values(dict(new["scope"]))
    except KeyError, TypeError:
        return False
    if not overlap:
        return False
    return not (old.get("attribution") and new.get("attribution")) or bool(
        _keys(old) & _keys(new)
    )


def registrations(results: Sequence[Mapping[str, Any]]) -> dict[str, Registration]:
    """The commit that added each current entry, by id."""
    wanted = {str(record["id"]): record for record in results}
    found: dict[str, Registration] = {}
    for commit, day in history():
        if len(found) == len(wanted):
            break
        try:
            text = _git("show", f"{commit}:{RESULTS_PATH}")
        except subprocess.CalledProcessError:
            continue
        for old in (safe_load(text) or {}).get("results") or []:
            rid = str(old.get("id"))
            if rid in wanted and rid not in found and same_result(old, wanted[rid]):
                found[rid] = Registration(rid, commit, day)
    missing = sorted(set(wanted) - set(found))
    if missing:
        raise SystemExit(f"no commit in this history adds {', '.join(missing)}")
    return found


def with_registered(text: str, days: Mapping[str, str]) -> str:
    """The register with `registered` written into every entry that lacks it.

    Line by line, so every other byte stays as the file has it: after `established` where
    the entry has one, else after `headline`, each of which is one line.
    """
    lines = text.split("\n")
    output: list[str] = []
    entry = ""
    after: re.Pattern[str] | None = None
    for index, line in enumerate(lines):
        match = _ENTRY.match(line)
        if match:
            entry = match.group(1)
            block: list[str] = []
            for later in lines[index + 1 :]:
                if _ENTRY.match(later) or not later.startswith("    "):
                    break
                block.append(later)
            if any(item.startswith("    registered: ") for item in block):
                after = None
            elif any(_ESTABLISHED.match(item) for item in block):
                after = _ESTABLISHED
            else:
                after = _HEADLINE
        output.append(line)
        if after is not None and after.match(line):
            following = lines[index + 1] if index + 1 < len(lines) else ""
            if not _KEY.match(following):
                raise SystemExit(f"{entry}: the line after {line.strip()!r} is not a key")
            output.append(f"    registered: '{days[entry]}'")
            after = None
    return "\n".join(output)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="insert the missing dates")
    arguments = parser.parse_args(argv)
    text = RESULTS.read_text(encoding="utf-8")
    results = safe_load(text)["results"]
    found = registrations(results)
    disagreements = 0
    for record in results:
        rid = str(record["id"])
        registration = found[rid]
        recorded = record.get("registered")
        note = ""
        if recorded is not None and str(recorded) != registration.day:
            note = f"  DISAGREES with the recorded {recorded}"
            disagreements += 1
        print(f"{rid}  {registration.day}  {registration.commit[:9]}{note}")
    if arguments.write:
        updated = with_registered(text, {rid: item.day for rid, item in found.items()})
        before = safe_load(text)["results"]
        after = safe_load(updated)["results"]
        for old, new in zip(before, after, strict=True):
            added = {key: value for key, value in new.items() if key not in old}
            if {**old, **added} != new or set(added) - {"registered"}:
                raise SystemExit(f"{old['id']}: the write changed more than registered")
        if updated != text:
            with atomic_output_file(RESULTS) as temporary:
                temporary.write_text(updated, encoding="utf-8")
            print(f"wrote registered into {RESULTS.relative_to(REPO)}")
        else:
            print("every entry already carries registered")
    if disagreements:
        print(f"{disagreements} recorded dates disagree with the history", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
