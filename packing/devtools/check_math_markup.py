#!/usr/bin/env python3
"""The math-markup ratchet: a migrated Markdown file keeps its mathematics as LaTeX.

`devtools.migrate_math` moves a file's mathematics from code spans to `$…$`. Without a
check, the next edit writes `` `s(11) ≥ 3.82` `` again and the file drifts back one span
at a time. This is that check, for the pull-request surface: every file listed under
`migrated` in `devtools/math-markup.yaml` is planned exactly as `migrate_math` plans it,
and a code span it would convert fails the gate, with the LaTeX to write instead. A span
that must stay code despite reading as math is recorded under `keep` with its reason, and
a `keep` entry whose span has gone fails too, so the list only shrinks.

A file that is not listed is never read. The check counts them instead -- every tracked
hand-written Markdown file not yet migrated -- so the backlog stays visible without
being enforced, and `--backlog` lists it. Generated views are counted apart, since they
move at their renderers; the literature archive, vendored trees, tool-owned files under
dot directories, renderer templates and the preserved sources `.flowmarkignore` protects
are excluded, each with the reason the document map or `.flowmarkignore` records.

It is fast by construction, since it runs in the edit tier: a migrated file whose spans
contain no math by their text alone (`has_math_spans`) needs no block parse, and that is
every migrated file with nothing wrong in it. The run prints its own wall time.

Usage, from `packing/`:

    uv run --frozen --all-extras --group dev python -m devtools.check_math_markup
    uv run --frozen --all-extras --group dev python -m devtools.check_math_markup --backlog

Exits 1 on a finding, and 2 if the register cannot be read.
"""

from __future__ import annotations

import argparse
import sys
import time
from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath

from devtools.migrate_math import has_math_spans, plan
from devtools.repo_scope import tracked_files, vendored_directories
from sqpack.yamlio import load_yaml, safe_load

PACKING = Path(__file__).resolve().parents[1]
REPO = PACKING.parent
REGISTER = Path(__file__).resolve().parent / "math-markup.yaml"
DOCUMENT_MAP = PurePosixPath("docs/project/document-map.yaml")
FLOWMARKIGNORE = PurePosixPath(".flowmarkignore")
#: What a walk skips when there is no git index to ask: never this repository's prose.
UNTRACKED_PARTS = frozenset({".git", ".venv", "node_modules", "__pycache__", "site"})


class RegisterError(ValueError):
    """The register is not the shape this check reads."""


@dataclass(frozen=True)
class Keep:
    """One code span that reads as math but stays code, and why."""

    path: str
    span: str
    reason: str


@dataclass(frozen=True)
class Register:
    """The migrated files and the spans they keep as code."""

    migrated: tuple[str, ...]
    keep: tuple[Keep, ...]


def load_register(path: Path = REGISTER) -> Register:
    """Read and shape-check the register; a malformed one raises `RegisterError`."""
    data = load_yaml(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or set(data) != {"migrated", "keep"}:
        raise RegisterError(f"{path.name}: expected exactly the keys `migrated` and `keep`")
    migrated, keep = data["migrated"], data["keep"]
    if not isinstance(migrated, list) or not all(isinstance(item, str) for item in migrated):
        raise RegisterError(f"{path.name}: `migrated` must be a list of paths")
    if not isinstance(keep, list):
        raise RegisterError(f"{path.name}: `keep` must be a list")
    entries: list[Keep] = []
    for item in keep:
        if (
            not isinstance(item, dict)
            or set(item) != {"path", "span", "reason"}
            or not all(isinstance(value, str) and value.strip() for value in item.values())
        ):
            raise RegisterError(
                f"{path.name}: a `keep` entry is {{path, span, reason}}, none empty: {item!r}"
            )
        entries.append(Keep(item["path"], item["span"], item["reason"]))
    return Register(tuple(migrated), tuple(entries))


@dataclass(frozen=True)
class Scope:
    """Every tracked Markdown file, sorted by what the ratchet may do with it."""

    eligible: frozenset[str]
    generated: frozenset[str]
    excluded: dict[str, str] = field(default_factory=dict)


def _markdown(repo: Path) -> list[str]:
    """Every tracked Markdown file, repository-relative; a walk where there is no index."""
    tracked = tracked_files(repo, "*.md")
    if tracked is None:
        tracked = [
            path
            for path in repo.rglob("*.md")
            if path.is_file() and not UNTRACKED_PARTS & set(path.relative_to(repo).parts)
        ]
    return sorted(path.relative_to(repo).as_posix() for path in tracked)


def _document_map(repo: Path) -> tuple[frozenset[str], list[str]]:
    """The document map's generated views and its exclusion patterns, if it has one."""
    source = repo / DOCUMENT_MAP
    if not source.is_file():
        return frozenset(), []
    document = safe_load(source.read_text(encoding="utf-8"))
    generated = frozenset(
        entry["path"]
        for entry in document.get("documents", [])
        if entry.get("role") == "generated-view" or entry.get("authority") == "generated"
    )
    return generated, [entry["pattern"] for entry in document.get("exclusions", [])]


def _flowmark_exclusions(repo: Path) -> list[str]:
    source = repo / FLOWMARKIGNORE
    if not source.is_file():
        return []
    lines = (line.strip() for line in source.read_text(encoding="utf-8").splitlines())
    return [line for line in lines if line and not line.startswith("#")]


def _excluded_by(path: str, patterns: Sequence[str]) -> bool:
    """Whether a pattern names `path`: a directory prefix, a file, or a glob."""
    posix = PurePosixPath(path)
    return any(
        path.startswith(pattern) if pattern.endswith("/") else posix.full_match(pattern)
        for pattern in patterns
    )


def _why_excluded(
    path: str, repo: Path, map_patterns: Sequence[str], ignored: Sequence[str]
) -> str | None:
    """Why the ratchet may never list `path`, or `None` if it may."""
    parts = PurePosixPath(path).parts
    prefixes = {"/".join(parts[:length]) for length in range(1, len(parts))}
    if prefixes & vendored_directories(repo):
        return "vendored"
    if any(part.startswith(".") for part in parts[:-1]):
        return "tool-owned"
    if _excluded_by(path, map_patterns):
        return "document-map exclusion"
    if _excluded_by(path, ignored):
        return "flowmark exclusion"
    return None


def scope(repo: Path = REPO) -> Scope:
    """Sort the tracked Markdown into eligible, generated and excluded files."""
    generated_views, map_patterns = _document_map(repo)
    ignored = _flowmark_exclusions(repo)
    eligible: set[str] = set()
    generated: set[str] = set()
    excluded: dict[str, str] = {}
    for path in _markdown(repo):
        if path in generated_views:
            generated.add(path)
        elif (reason := _why_excluded(path, repo, map_patterns, ignored)) is not None:
            excluded[path] = reason
        else:
            eligible.add(path)
    return Scope(frozenset(eligible), frozenset(generated), excluded)


@dataclass
class Outcome:
    """What one run found: the problems, and the counts it reports."""

    problems: list[str] = field(default_factory=list)
    kept: int = 0


def _normalized(content: str) -> str:
    return " ".join(content.split())


def _check_file(path: str, text: str, keeps: set[str], outcome: Outcome) -> None:
    """Fail every math code span in one migrated file that `keep` does not name."""
    found: set[str] = set()
    if has_math_spans(text):
        for decision in plan(text).decisions:
            if decision.verdict.kind != "math":
                continue
            span = _normalized(decision.span.content)
            found.add(span)
            if span in keeps:
                outcome.kept += 1
                continue
            outcome.problems.append(
                f"{path}:{decision.span.line}: `{span}` is mathematics written as code "
                f"({decision.verdict.rule}); write ${decision.verdict.latex}$, or run "
                f"`python -m devtools.migrate_math --apply {path}`"
            )
    outcome.problems.extend(
        f"{path}: `keep` names `{span}`, which is no longer a math code span here; remove it"
        for span in sorted(keeps - found)
    )


def check(register: Register, repo: Path = REPO, files: Scope | None = None) -> Outcome:
    """Check every migrated file and the register's own consistency."""
    files = files if files is not None else scope(repo)
    outcome = Outcome()
    if list(register.migrated) != sorted(set(register.migrated)):
        outcome.problems.append("math-markup.yaml: `migrated` must be sorted and unique")
    for keep in register.keep:
        if keep.path not in register.migrated:
            outcome.problems.append(f"math-markup.yaml: `keep` names {keep.path}, not migrated")
    for path in register.migrated:
        if path not in files.eligible:
            why = (
                "a generated view, migrated at its renderer"
                if path in files.generated
                else files.excluded.get(path, "not a tracked Markdown file")
            )
            outcome.problems.append(f"math-markup.yaml: {path} cannot be listed: {why}")
            continue
        keeps = {keep.span for keep in register.keep if keep.path == path}
        _check_file(path, (repo / path).read_text(encoding="utf-8"), keeps, outcome)
    return outcome


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="check_math_markup",
        description="Fail a math code span in a migrated file; report the unmigrated backlog.",
    )
    parser.add_argument("--register", type=Path, default=REGISTER, help=argparse.SUPPRESS)
    parser.add_argument("--repo", type=Path, default=REPO, help=argparse.SUPPRESS)
    parser.add_argument("--backlog", action="store_true", help="list the unmigrated files")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    started = time.perf_counter()
    try:
        register = load_register(arguments.register)
    except (OSError, RegisterError) as error:
        print(f"  cannot read the math-markup register: {error}", file=sys.stderr)
        return 2
    files = scope(arguments.repo)
    outcome = check(register, arguments.repo, files)
    backlog = sorted(files.eligible - set(register.migrated))
    for problem in outcome.problems:
        print(f"  {problem}", file=sys.stderr)
    excluded = Counter(files.excluded.values())
    kept = f", {outcome.kept} spans kept as code" if outcome.kept else ""
    print(f"  math markup: {len(register.migrated)} migrated files checked{kept}")
    reasons = ", ".join(f"{reason} {count}" for reason, count in sorted(excluded.items()))
    print(
        f"  backlog: {len(backlog)} of {len(files.eligible)} hand-written Markdown files "
        f"not yet migrated; {len(files.generated)} generated views move at their renderers; "
        f"{excluded.total()} excluded" + (f" ({reasons})" if reasons else "")
    )
    if arguments.backlog:
        for path in backlog:
            print(f"    {path}")
    print(f"  ({time.perf_counter() - started:.2f}s)")
    return 1 if outcome.problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
