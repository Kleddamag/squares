#!/usr/bin/env python3
"""Render what a branch, or a stack of pull requests, does to the results register.

The top pull request of a stack is where the owner reads what the whole stack lands, and
`devtools.render_pr_rollup` cannot say it: its results section joins the register to one
agenda's wall by the date a result was scored, so a stack with no agenda renders nothing,
and a result whose rungs moved without a re-score is missed inside any window. A stack's
answer is a difference between two revisions, so this reads the register at both with
`git` and prints three Markdown blocks for the description's results section:

- **the results that changed**: every result new at the head, or whose verification,
  confirmation, significance, status, kind, credit or headline differs from the base, in
  the order `RESULTS.md` uses, with what changed (`new`, or `V0→V3, C1→C3`);
- **the frontier**: the case records' proved and open counts at both revisions, in the
  verified and the reported lane, the open cases bounded below only by Nagamochi (the
  three numbers `FRONTIER_COUNTS` pins in `sqpack.cli.validate`), and which cases moved;
- **the rungs**: the changed results counted by `V` and `C` at the head, with each rung's
  and each significance score's own wording from `epistemics.md`.

Nothing is re-derived here. Kind labels come from `devtools.check_results`, credit from
`devtools.result_credit.credit_line` with the bibliography at the same revision, status
from `devtools.result_status`, and the reading order, `n` and rubric wording from
`devtools.significance`. The rungs are the register's declared ones, which
`check_results` holds to their evidence at every revision that passed the gate.

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m devtools.render_stack_results \
        --base origin/main --head origin/claude/my-top-branch
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

import yaml

from devtools import significance
from devtools.check_case_prose import split_front_matter
from devtools.check_results import kind_label
from devtools.result_credit import credit_line
from devtools.result_status import status
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent
#: The records read at each revision, repository-relative as `git show` names them.
RESULTS_PATH = "packing/frontier/results.yaml"
EVIDENCE_PATH = "packing/frontier/evidence.yaml"
BIBLIOGRAPHY_PATH = "packing/resources/bibliography.yaml"
FRONTIER_PATH = "packing/frontier"
_CASE = re.compile(r"packing/frontier/n-\d+\.md")
#: The evidence that marks a verified lower bound as Nagamochi's closed form, as
#: `sqpack.cli.validate._frontier_corpus` counts it.
NAGAMOCHI = "E-nagamochi-lower"
#: The case fields whose movement the frontier block reports.
VERIFIED_FIELDS = ("verified_lower_bound", "verified_upper_bound")
ARROW = "→"


@dataclass(frozen=True)
class Snapshot:
    """The register, its evidence and sources, and the case records at one commit."""

    commit: str
    results: dict[str, dict[str, Any]]
    evidence: dict[str, dict[str, Any]]
    sources: dict[str, dict[str, Any]]
    cases: dict[int, dict[str, Any]]


@dataclass(frozen=True)
class Facts:
    """What the table shows of one result at one revision, and compares across two."""

    kind: str
    credit: str
    verification: str
    confirmation: str
    significance: int
    status: str
    headline: str


@dataclass(frozen=True)
class Frontier:
    """The case records' counts, as `sqpack.cli.validate._frontier_corpus` defines them."""

    first: int
    last: int
    cases: int
    proved: int
    open: int
    reported_proved: int
    reported_open: int
    nagamochi: int


def _git(repo: Path, *args: str, stdin: bytes | None = None) -> bytes:
    return subprocess.run(
        ("git", *args), cwd=repo, input=stdin, capture_output=True, check=True
    ).stdout


def resolve(ref: str, repo: Path = REPO) -> str:
    """The commit `ref` names, or a refusal naming the ref."""
    try:
        return (
            _git(repo, "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}").decode().strip()
        )
    except subprocess.CalledProcessError:
        raise ValueError(f"{ref} names no commit here; fetch it first") from None


def blobs(commit: str, paths: Sequence[str], repo: Path = REPO) -> dict[str, bytes | None]:
    """Each path's bytes at `commit`, or None where the path does not exist there.

    One `git cat-file --batch` for every path, since a revision's frontier is 300-odd
    files and a process each would cost more than the parse.
    """
    request = "".join(f"{commit}:{path}\n" for path in paths).encode()
    out = _git(repo, "cat-file", "--batch", stdin=request)
    found: dict[str, bytes | None] = {}
    position = 0
    for path in paths:
        end = out.index(b"\n", position)
        header = out[position:end].decode()
        position = end + 1
        if header.endswith(" missing"):
            found[path] = None
            continue
        size = int(header.rsplit(" ", 1)[1])
        found[path] = out[position : position + size]
        position += size + 1
    return found


def _document(path: str, data: bytes | None, commit: str) -> Any:
    if data is None:
        raise ValueError(f"{path} does not exist at {commit[:9]}")
    return safe_load(data.decode("utf-8"))


def load_snapshot(ref: str, repo: Path = REPO) -> Snapshot:
    """Read the register, evidence, bibliography and every case record at `ref`."""
    commit = resolve(ref, repo)
    listed = _git(repo, "ls-tree", "--name-only", commit, f"{FRONTIER_PATH}/").decode()
    case_paths = [path for path in listed.splitlines() if _CASE.fullmatch(path)]
    found = blobs(commit, (RESULTS_PATH, EVIDENCE_PATH, BIBLIOGRAPHY_PATH, *case_paths), repo)
    results = _document(RESULTS_PATH, found[RESULTS_PATH], commit)["results"]
    evidence = _document(EVIDENCE_PATH, found[EVIDENCE_PATH], commit)["evidence"]
    sources = _document(BIBLIOGRAPHY_PATH, found[BIBLIOGRAPHY_PATH], commit)["sources"]
    cases: dict[int, dict[str, Any]] = {}
    for path in case_paths:
        text = (found[path] or b"").decode("utf-8")
        packing = safe_load(split_front_matter(text)[0])["packing"]
        cases[int(packing["n"])] = packing
    return Snapshot(
        commit=commit,
        results={record["id"]: record for record in results},
        evidence={entry["id"]: entry for entry in evidence},
        sources={source["key"]: source for source in sources},
        cases=cases,
    )


def facts(record: Mapping[str, Any], snapshot: Snapshot) -> Facts:
    """One result's compared fields at the revision `snapshot` was read from."""
    return Facts(
        kind=kind_label(str(record.get("kind", ""))),
        credit=credit_line(record, snapshot.sources),
        verification=str(record["verification"]),
        confirmation=str(record["confirmation"]),
        significance=int(record["significance"]["score"]),
        status=status(record, snapshot.evidence),
        headline=" ".join(
            str(record.get("headline") or significance.headline(dict(record))).split()
        ),
    )


def change(before: Facts | None, after: Facts) -> str:
    """What moved between two revisions of one result, or "" for nothing.

    Rungs and status print as `old→new`; kind and credit name themselves because their
    values do not; a changed headline is named and the new one is in its own column.
    """
    if before is None:
        return "new"
    moved = [
        f"{old}{ARROW}{new}"
        for old, new in (
            (before.verification, after.verification),
            (before.confirmation, after.confirmation),
            (f"S{before.significance}", f"S{after.significance}"),
            (before.status, after.status),
        )
        if old != new
    ]
    if before.kind != after.kind:
        moved.append(f"kind {before.kind}{ARROW}{after.kind}")
    if before.credit != after.credit:
        moved.append(f"credit {before.credit}{ARROW}{after.credit}")
    if before.headline != after.headline:
        moved.append("headline")
    return ", ".join(moved)


def changed(base: Snapshot, head: Snapshot) -> list[tuple[dict[str, Any], Facts, str]]:
    """Every result new at the head or moved since the base, in `RESULTS.md`'s order."""
    rows: dict[str, tuple[Facts, str]] = {}
    for rid, record in head.results.items():
        after = facts(record, head)
        before = base.results.get(rid)
        moved = change(None if before is None else facts(before, base), after)
        if moved:
            rows[rid] = (after, moved)
    ordered = significance.by_significance([head.results[rid] for rid in rows])
    return [(record, *rows[record["id"]]) for record in ordered]


def _cell(value: object) -> str:
    """One Markdown table cell from prose-shaped YAML."""
    return " ".join(str(value).split()).replace("|", "\\|")


def _short(commit: str) -> str:
    return commit[:9]


def render_results(rows: Sequence[tuple[dict[str, Any], Facts, str]]) -> list[str]:
    lines = [
        "| Result | `n` | Kind | Credit | `V` | `C` | `S` | Status | Headline | Change |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    lines.extend(
        f"| `{record['id']}` | {significance.scope_label(record)} | {row.kind} "
        f"| {row.credit} | `{row.verification}` | `{row.confirmation}` "
        f"| `S{row.significance}` | {row.status} | {_cell(row.headline)} | {_cell(moved)} |"
        for record, row, moved in rows
    )
    return lines


def frontier(snapshot: Snapshot) -> Frontier:
    cases = snapshot.cases.values()
    return Frontier(
        first=min(snapshot.cases, default=0),
        last=max(snapshot.cases, default=0),
        cases=len(snapshot.cases),
        proved=sum(case["status"] == "proved" for case in cases),
        open=sum(case["status"] == "open" for case in cases),
        reported_proved=sum(case["reported_status"] == "proved" for case in cases),
        reported_open=sum(case["reported_status"] == "open" for case in cases),
        nagamochi=sum(
            case["status"] == "open"
            and NAGAMOCHI in (case.get("verified_lower_bound") or {}).get("evidence", ())
            for case in cases
        ),
    )


def _value(bound: Mapping[str, Any] | None) -> Decimal | str | None:
    """A bound's value, compared as a number so `8` and `8.0` are one value."""
    value = (bound or {}).get("value")
    if value is None:
        return None
    try:
        return Decimal(str(value))
    except InvalidOperation:
        return str(value)


def _ns(values: Iterable[int]) -> str:
    found = sorted(values)
    return ", ".join(str(n) for n in found) if found else "none"


def render_frontier(base: Snapshot, head: Snapshot) -> list[str]:
    before, after = frontier(base), frontier(head)
    label = f"n = {after.first}..{after.last}"
    rows = (
        ("Cases", before.cases, after.cases),
        ("Proved, verified lane", before.proved, after.proved),
        ("Open, verified lane", before.open, after.open),
        ("Proved, reported lane", before.reported_proved, after.reported_proved),
        ("Open, reported lane", before.reported_open, after.reported_open),
        ("Open with only Nagamochi's lower bound", before.nagamochi, after.nagamochi),
    )
    lines = [
        f"| Frontier, {label} | Base `{_short(base.commit)}` | Head `{_short(head.commit)}` |",
        "| --- | --- | --- |",
        *(f"| {name} | {old} | {new} |" for name, old, new in rows),
        "",
    ]
    shared = head.cases.keys() & base.cases.keys()
    for lane, field, word in (
        ("verified", "status", "Proved"),
        ("reported", "reported_status", "Reported proved"),
    ):
        moved = [
            n
            for n in shared
            if base.cases[n][field] == "open" and head.cases[n][field] == "proved"
        ]
        reopened = [
            n
            for n in shared
            if base.cases[n][field] == "proved" and head.cases[n][field] == "open"
        ]
        lines.append(f"- {word} at the head and open at the base ({lane} lane): {_ns(moved)}.")
        if reopened:
            lines.append(
                f"- Open at the head and proved at the base ({lane} lane): {_ns(reopened)}."
            )
    for field in VERIFIED_FIELDS:
        moved = [
            n
            for n in shared
            if _value(base.cases[n].get(field)) != _value(head.cases[n].get(field))
        ]
        lines.append(f"- `{field}` value changed at {_cases(len(moved))}: {_ns(moved)}.")
    return lines


def _cases(count: int) -> str:
    return f"{count} case" if count == 1 else f"{count} cases"


def render_rungs(rows: Sequence[tuple[dict[str, Any], Facts, str]]) -> list[str]:
    """The changed results by `V` and `C` at the head, and the rubric's wording."""
    counts = Counter((row.verification, row.confirmation) for _, row, _ in rows)
    vs = sorted({v for v, _ in counts})
    cs = sorted({c for _, c in counts})
    new = sum(moved == "new" for _, _, moved in rows)
    lines = [
        f"{len(rows)} results changed: {new} new, {len(rows) - new} moved.",
        "",
        "| `V` \\ `C` | " + " | ".join(f"`{c}`" for c in cs) + " | Total |",
        "| --- | " + " | ".join("---" for _ in cs) + " | --- |",
    ]
    for v in vs:
        cells = [str(counts[v, c]) if counts[v, c] else "" for c in cs]
        lines.append(
            f"| `{v}` | " + " | ".join(cells) + f" | {sum(counts[v, c] for c in cs)} |"
        )
    words = {axis: significance.anchors(axis) for axis in ("V", "C", "S")}
    scores = sorted({row.significance for _, row, _ in rows}, reverse=True)
    lines.append("")
    lines.extend(f"- `{v}`: {words['V'][int(v[1:])]}." for v in vs)
    lines.extend(f"- `{c}`: {words['C'][int(c[1:])]}." for c in cs)
    lines.extend(f"- `S{score}`: {words['S'][score]}." for score in scores)
    return lines


def render(base: Snapshot, head: Snapshot, base_ref: str, head_ref: str) -> str:
    rows = changed(base, head)
    removed = sorted(base.results.keys() - head.results.keys())
    lines = [
        (
            f"The results register at `{_short(head.commit)}` (`{head_ref}`) against "
            f"`{_short(base.commit)}` (`{base_ref}`), generated by "
            "`devtools.render_stack_results`. `V`, `C` and status are the register's at the "
            "head; the order is `RESULTS.md`'s, significance first."
        ),
        "",
    ]
    if rows:
        lines += render_results(rows)
    else:
        lines.append("No result is new or moved.")
    if removed:
        lines += ["", f"In the register at the base and not at the head: {', '.join(removed)}."]
    lines += ["", *render_frontier(base, head)]
    if rows:
        lines += ["", *render_rungs(rows)]
    return "\n".join(lines) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", default="origin/main", help="revision compared against")
    parser.add_argument("--head", default="HEAD", help="revision whose changes are shown")
    args = parser.parse_args(argv)
    try:
        rendered = render(
            load_snapshot(args.base), load_snapshot(args.head), args.base, args.head
        )
    except ValueError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    except (KeyError, TypeError, yaml.YAMLError, subprocess.CalledProcessError) as error:
        print(f"error: unable to render the stack's results: {error!r}", file=sys.stderr)
        return 1
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
