#!/usr/bin/env python3
"""Check durable-document coverage, lifecycle, footers, links, summaries, and generated map.

A document the published overview lists as a card (`devtools.reader_documents`) needs a
one-sentence `summary` in the document map, and no summary may state a bound: the
overview's numbers are generated from the record, and a summary that carried one would
go stale the day the record moved past it. `states_a_bound` says precisely what counts.
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import unquote

from devtools.reader_documents import shown_paths
from devtools.render_document_map import MAP, REPO, SYNOPSIS, expected_synopsis, load_map
from devtools.repo_scope import is_vendored
from sqpack.yamlio import safe_load

FOOTER = "This document follows common-doc-guidelines.md."
# `site` is the explainer's render output, gitignored and rebuilt by every run. It is
# not durable, so it has nothing to be mapped to; the page and the Markdown document
# beside it are checked by the renderer's own `--check`, which compares them byte for
# byte against a fresh render.
#
# Vendored trees are not here. They are skipped by `devtools.repo_scope`, which reads
# `.gitmodules`, and they used to be a `vendor/**/*.md` exclusion in the document map
# instead. That failed on a plain clone: the map's loader requires every exclusion to
# match a file, and an unchecked-out submodule matches none, so `git clone` without
# `--recurse-submodules` failed the docs check while CI passed (think-5e7k). Upstream
# prose is not this repository's surface whether or not it is on disk, which is a
# statement about the declaration rather than about the working tree.
IGNORED_PARTS = {
    ".pytest_cache",
    ".venv",
    "__pycache__",
    "node_modules",
    "attic",
    "site",
}
REPOSITORY_ROOT = REPO
RETIRED_PHRASES = (
    "approximately verified",
    "numerical-arbitrary-precision",
    "numerically verified",
    "verified-construction",
)

#: The longest summary a card sets; the schema's `maxLength` is the same number.
SUMMARY_LIMIT = 160

# What stating a bound looks like. A summary says what a document covers, and names cases
# by integers (`n = 11`, `n = 1…324`, "twenty-six squares"); a bound is a value of `s`, or
# a side length, and it shows up in one of the shapes below. Each is named for the
# refusal, and `states_a_bound` returns the first that matches.
#
# Spacing inside TeX (`\;`, `\,`, `~`) and a `$` around the math count as space, and
# `\frac{` may open the number, so `$s(11) \;\ge\; \frac{31}{8}$` is the same statement
# as `s(11) >= 31/8`.
_SPACE = r"(?:\s|\\[,;:!]|~)*"
_INEQUALITY = r"(?:<=|>=|[<>≤≥≈]|\\(?:le|ge|leq|geq|lt|gt|approx)(?![A-Za-z]))"
_RELATION = rf"(?:{_INEQUALITY}|=|\b(?:is|at least|at most|equals?|exceeds?|below|above|to)\b)"
_NUMBER = rf"\$?{_SPACE}(?:\\[dt]?frac{_SPACE}\{{{_SPACE})?\d"
_S_OF = r"(?<![A-Za-z\\])s\s*\([^()]*\)"
BOUND_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    # `s(11) >= 3.8`, `s(32) = 6`, `$s(n) \ge 5$`, `s(11) is at least 3.8`.
    (
        "a relation of s(…) to a number",
        re.compile(rf"{_S_OF}{_SPACE}\$?{_SPACE}(?:{_RELATION}{_SPACE})+{_NUMBER}"),
    ),
    # `3.8 < s(11)`, `5 = s(21)`.
    (
        "a number in relation to s(…)",
        re.compile(rf"\d[\d.,/…]*{_SPACE}\$?{_SPACE}{_RELATION}{_SPACE}\$?{_SPACE}{_S_OF}"),
    ),
    # `side ≥ 4`, `n = 11 > 3`: an inequality or approximation beside a number, whatever
    # it compares. A range of cases is written with `=` and an ellipsis, or in words.
    (
        "an inequality with a number",
        re.compile(rf"{_INEQUALITY}{_SPACE}{_NUMBER}|\d{_SPACE}\$?{_SPACE}{_INEQUALITY}"),
    ),
    # The forms a side length takes and a count never does. A version (`v0.4`) and an
    # identifier (`T-026`, `BC303`, `H-161`) are not numbers here.
    ("a decimal", re.compile(r"(?<![\w.])\d+\.\d+")),
    ("a fraction", re.compile(r"(?<![\w/])\d+\s*/\s*\d+(?![\w/])|\\[dt]?frac\b")),
    ("a radical", re.compile(r"√|\\sqrt\b|\bsqrt\s*\(")),
)


def states_a_bound(text: str) -> tuple[str, str] | None:
    """The first bound-stating shape `text` contains, named, with what matched; else None."""
    for name, pattern in BOUND_PATTERNS:
        match = pattern.search(text)
        if match:
            return name, match.group(0)
    return None


def summary_faults(summary: str) -> list[str]:
    """What is wrong with one summary: its length, its shape, or a bound in it."""
    faults: list[str] = []
    if len(summary) > SUMMARY_LIMIT:
        faults.append(f"is {len(summary)} characters, over {SUMMARY_LIMIT}")
    if "\n" in summary or not summary.endswith(".") or re.search(r"[.!?]\s+\S", summary):
        faults.append("is not one sentence ending in a full stop")
    bound = states_a_bound(summary)
    if bound is not None:
        faults.append(
            f"states a bound ({bound[0]}: {bound[1]!r}); a summary says what the document "
            "covers, and the page's numbers come from the record"
        )
    return faults


def summary_problems(document_map: dict) -> list[str]:
    """Every card the overview shows has a summary, and every summary is well formed."""
    problems: list[str] = []
    entries = {document["path"]: document for document in document_map["documents"]}
    for path in shown_paths(document_map):
        entry = entries.get(path)
        if entry is None:
            problems.append(f"{path}: the overview lists it, but the document map does not")
        elif not str(entry.get("summary") or "").strip():
            problems.append(f"{path}: the overview lists it, so its map entry needs a summary")
    for document in document_map["documents"]:
        summary = document.get("summary")
        if summary is not None:
            problems.extend(
                f"{document['path']}: summary {fault}" for fault in summary_faults(str(summary))
            )
    return problems


def _matches(pattern: str) -> set[str]:
    return {path.relative_to(REPO).as_posix() for path in REPO.glob(pattern) if path.is_file()}


def _frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing YAML frontmatter")
    return safe_load(text.split("---\n", 2)[1])


def _slugs(text: str) -> set[str]:
    """Approximate GitHub heading ids, including duplicate-heading suffixes."""
    counts: Counter[str] = Counter()
    slugs: set[str] = set(re.findall(r'id="([^"]+)"', text))
    for heading in re.findall(r"^#{1,6}\s+(.+)$", text, re.MULTILINE):
        plain = re.sub(r"<[^>]+>", "", heading)
        plain = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", plain)
        base = re.sub(r"[^a-z0-9 _-]", "", plain.lower()).strip().replace(" ", "-")
        suffix = counts[base]
        counts[base] += 1
        slugs.add(base if suffix == 0 else f"{base}-{suffix}")
    return slugs


def _is_ephemeral_local_target(path: Path) -> bool:
    """Reject links whose apparent validity depends on untracked tbd working state."""
    try:
        relative = path.relative_to(REPOSITORY_ROOT)
    except ValueError:
        return False
    return relative.parts[:2] == (".tbd", "docs")


def _link_problems(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    problems: list[str] = []
    for raw_target in re.findall(r"!?\[[^]]*\]\(([^)]+)\)", text):
        target = raw_target.strip().strip("<>")
        if target.startswith(("http://", "https://", "mailto:")):
            continue
        relative, _, fragment = target.partition("#")
        label = path.relative_to(REPO).as_posix()
        if Path(unquote(relative)).is_absolute():
            problems.append(f"{label}: absolute local link -> {target}; use a relative path")
            continue
        resolved = path if not relative else (path.parent / unquote(relative)).resolve()
        if not resolved.exists():
            problems.append(f"{label}: dead link -> {target}")
        elif _is_ephemeral_local_target(resolved):
            problems.append(f"{label}: ephemeral local-state link -> {target}")
        elif (
            fragment
            and resolved.suffix == ".md"
            and unquote(fragment) not in _slugs(resolved.read_text(encoding="utf-8"))
        ):
            problems.append(f"{label}: dead anchor -> {target}")
    return problems


def check() -> list[str]:
    document_map = load_map()
    problems: list[str] = []
    documents = document_map["documents"]
    document_paths = [item["path"] for item in documents]
    if len(document_paths) != len(set(document_paths)):
        problems.append("document map contains duplicate standalone paths")

    covered = set(document_paths)
    for document in documents:
        path = REPO / document["path"]
        if not path.is_file():
            problems.append(f"mapped document does not exist: {document['path']}")
        replacement = document.get("superseded_by")
        if document["lifecycle"] == "superseded" and not replacement:
            problems.append(f"{document['path']}: superseded without superseded_by")
        if replacement and not (REPO / replacement).is_file():
            problems.append(f"{document['path']}: replacement does not exist: {replacement}")
    problems.extend(summary_problems(document_map))

    for collection in document_map["collections"]:
        matched = _matches(collection["pattern"])
        if not matched:
            problems.append(f"document collection is empty: {collection['pattern']}")
        overlap = covered & matched
        if overlap:
            problems.append(f"document map covers paths more than once: {sorted(overlap)[:3]}")
        covered |= matched
        schema = REPO / collection["schema"]
        if not schema.is_file():
            problems.append(f"collection schema does not exist: {collection['schema']}")
        for relative in sorted(matched):
            try:
                metadata = _frontmatter(REPO / relative)["softschema"]
            except (KeyError, TypeError, ValueError) as error:
                problems.append(f"{relative}: cannot read softschema metadata: {error}")
                continue
            if metadata.get("contract") != collection["contract"]:
                problems.append(
                    f"{relative}: contract {metadata.get('contract')!r} does not match "
                    f"{collection['contract']!r}"
                )

    excluded: set[str] = set()
    for exclusion in document_map["exclusions"]:
        matched = _matches(exclusion["pattern"])
        if not matched:
            problems.append(f"document exclusion is empty: {exclusion['pattern']}")
        excluded |= matched

    actual = {
        path.relative_to(REPO).as_posix()
        for path in REPO.rglob("*.md")
        if path.is_file()
        and not is_vendored(path)
        and not any(
            part in IGNORED_PARTS or part.startswith(".")
            for part in path.relative_to(REPO).parts
        )
    }
    unmapped = actual - covered - excluded
    problems.extend(f"unmapped durable document: {path}" for path in sorted(unmapped))
    problems.extend(
        f"mapped document is also excluded: {path}" for path in sorted(covered & excluded)
    )

    for relative in sorted(covered & actual):
        text = (REPO / relative).read_text(encoding="utf-8")
        if FOOTER not in text:
            problems.append(f"{relative}: common-doc footer is missing")
        problems.extend(_link_problems(REPO / relative))

    current_paths = {
        item["path"]
        for item in documents
        if item["authority"] in {"definitive", "current"} and item["role"] != "plan"
    }
    for relative in sorted(current_paths):
        lowered = (REPO / relative).read_text(encoding="utf-8").lower()
        problems.extend(
            f"{relative}: retired assurance phrase {phrase!r}"
            for phrase in RETIRED_PHRASES
            if phrase in lowered
        )
        if "role: exact_solution" in lowered:
            problems.append(f"{relative}: retired exact_solution resource role")

    current = SYNOPSIS.read_text(encoding="utf-8")
    try:
        if current != expected_synopsis(current, document_map):
            problems.append("SYNOPSIS.md document map is stale")
    except ValueError as error:
        problems.append(str(error))
    if MAP.relative_to(REPO).as_posix() != "docs/project/document-map.yaml":
        problems.append("document-map location drifted from its public contract")
    return problems


def main() -> int:
    problems = check()
    if problems:
        for problem in problems:
            print(f"FAIL {problem}", file=sys.stderr)
        return 1
    document_map = load_map()
    count = len(document_map["documents"]) + sum(
        len(_matches(collection["pattern"])) for collection in document_map["collections"]
    )
    print(f"  documentation map covers {count} durable documents; footers and links resolve")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
