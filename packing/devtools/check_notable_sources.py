#!/usr/bin/env python3
"""Hold the notable-sources registry to the frontier's sources and the archive.

`resources/notable-sources.yaml` is the list behind the overview's Other Square Packing
Projects section: one entry per project or site. It joins two records that already exist,
and this check keeps it joined to both.

- **Every reviewed frontier source is on the page, once.** Each id in
  `frontier/source-coverage.yaml` belongs to exactly one entry's `coverage`, and an entry
  names no coverage id that record lacks. So a source the frontier reviews can never drop
  off the page, and no release is shown under two projects.
- **Every credit resolves.** An entry's keys resolve in `resources/bibliography.yaml`, or,
  for a source the bibliography does not carry, among the keys the archive index
  (`resources/README.md`) defines in bold. Every coverage source's own `source_key` is
  among its entry's keys. Where a key is in the bibliography, that key's credit is what
  the card prints, so the entry may not state a `credit` of its own; where none is, it
  must, since there is nothing else to print.
- **Every retained copy exists**, as a file, or as a directory where the path ends in a
  slash, so the card's archive link is never dead and its `tree`/`blob` kind is decided
  without the filesystem, which the Pages checkout leaves out.
- **Every summary is one sentence that states no bound**: no `s(`, no relation sign and no
  decimal or fraction, so the numbers on the page stay generated from the record.

The registry's shape is its schema, `NotableSources/v1`, validated here too, since a
registry that declares `status: enforced` must be loaded by something.

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m devtools.check_notable_sources
"""

from __future__ import annotations

import re
import sys
from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path
from typing import Any

from devtools import validate_schemas
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent
NOTABLE_SOURCES = ROOT / "resources" / "notable-sources.yaml"
COVERAGE = ROOT / "frontier" / "source-coverage.yaml"
BIBLIOGRAPHY = ROOT / "resources" / "bibliography.yaml"
ARCHIVE_INDEX = ROOT / "resources" / "README.md"

#: How the archive index defines a key: in bold, at the head of a table row or a bullet.
DEFINED_KEY = re.compile(r"\*\*(\[.+?\])\*\*")
#: What a summary may not state, since each is a bound or part of one.
BOUND_SIGNS = (
    ("s(", "names s(n)"),
    ("≥", "states a relation"),
    ("≤", "states a relation"),
    (">", "states a relation"),
    ("<", "states a relation"),
    ("=", "states a relation"),
    ("√", "states a value"),
)
FRACTIONAL = re.compile(r"\d+[./]\d+")
#: A sentence ending inside the summary: a stop, then space and a capital.
SENTENCE_BREAK = re.compile(r"[.!?]\s+[A-Z]")


def archive_keys(text: str) -> frozenset[str]:
    """The keys the archive index defines in bold."""
    return frozenset(DEFINED_KEY.findall(text))


def summary_problems(summary: str) -> list[str]:
    """What a summary states that it may not: a second sentence, or a bound."""
    text = " ".join(summary.split())
    problems: list[str] = []
    if not text.endswith("."):
        problems.append("does not end as a sentence")
    if SENTENCE_BREAK.search(text):
        problems.append("is more than one sentence")
    problems.extend(f"{reason} ({sign!r})" for sign, reason in BOUND_SIGNS if sign in text)
    problems.extend(f"states a value ({value!r})" for value in FRACTIONAL.findall(text))
    return problems


def retained_problem(path: str, repo: Path = REPO) -> str | None:
    """Why a retained copy is not there, or None where it is."""
    target = repo / path
    if path.endswith("/"):
        return None if target.is_dir() else f"{path} is not a retained directory"
    if target.is_dir():
        return f"{path} is a directory, written without its trailing slash"
    return None if target.is_file() else f"{path} is not a retained file"


def problems(
    registry: Sequence[Mapping[str, Any]],
    coverage: Sequence[Mapping[str, Any]],
    bibliography: Iterable[str],
    archive: Iterable[str],
    repo: Path = REPO,
) -> list[str]:
    """Everything wrong with the registry, given the records it joins."""
    found: list[str] = []
    cited = frozenset(bibliography)
    defined = frozenset(archive) | cited
    coverage_by_id = {str(source["id"]): source for source in coverage}
    owners: dict[str, list[str]] = {}
    seen: set[str] = set()
    for entry in registry:
        name = str(entry["id"])
        if name in seen:
            found.append(f"{name}: the id is used twice")
        seen.add(name)
        keys = [str(key) for key in entry["keys"]]
        found.extend(f"{name}: {key} resolves nowhere" for key in keys if key not in defined)
        in_bibliography = [key for key in keys if key in cited]
        if in_bibliography and entry.get("credit"):
            found.append(
                f"{name}: states a credit although {in_bibliography[0]} is in the "
                "bibliography, whose credit the card prints"
            )
        if not in_bibliography and not entry.get("credit"):
            found.append(f"{name}: no key is in the bibliography, so it states its credit")
        for item in entry.get("coverage") or []:
            owners.setdefault(str(item), []).append(name)
            source = coverage_by_id.get(str(item))
            if source is None:
                found.append(f"{name}: covers {item}, which source-coverage.yaml lacks")
            elif str(source["source_key"]) not in keys:
                found.append(f"{name}: covers {item} but not its key {source['source_key']}")
        problem = retained_problem(str(entry["retained"]), repo)
        if problem:
            found.append(f"{name}: {problem}")
        found.extend(
            f"{name}: its summary {issue}" for issue in summary_problems(str(entry["summary"]))
        )
    for item in coverage_by_id:
        holders = owners.get(item, [])
        if not holders:
            found.append(f"{item}: a reviewed frontier source that no entry covers")
        elif len(holders) > 1:
            found.append(f"{item}: covered by {len(holders)} entries: {', '.join(holders)}")
    return found


def main() -> int:
    failures = [f"schema: {error}" for error in validate_schemas.check(NOTABLE_SOURCES)]
    registry = safe_load(NOTABLE_SOURCES.read_text(encoding="utf-8"))["sources"]
    coverage = safe_load(COVERAGE.read_text(encoding="utf-8"))["sources"]
    bibliography = [
        str(source["key"])
        for source in safe_load(BIBLIOGRAPHY.read_text(encoding="utf-8"))["sources"]
    ]
    archive = archive_keys(ARCHIVE_INDEX.read_text(encoding="utf-8"))
    if not failures:
        failures = problems(registry, coverage, bibliography, archive)
    if failures:
        print(f"{len(failures)} notable-sources problems:")
        for line in failures:
            print(f"  {line}")
        return 1
    covered = sum(len(entry.get("coverage") or []) for entry in registry)
    print(
        f"{len(registry)} notable sources: all {covered} reviewed frontier sources on the "
        "page once, every credit key resolved, every retained copy present, every summary "
        "one sentence with no bound"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
