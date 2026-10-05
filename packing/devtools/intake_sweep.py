#!/usr/bin/env python3
"""List every input the record has not taken in, across every standing intake source.

An intake pass (`campaign/result-import.md`, Running an Intake Pass) starts here. The
result import process used to start from "a GitHub issue, or a link", so an input that
arrived any other way waited on someone remembering it. On 2026-09-30 a Kingbird capture
found three September improvements and held them as `pending_catalogue_intake`, a plan
listed registering them, and no open bead owned the work. `check_requests --backlog`
reads issues and the register, `check_source_coverage` accepted the deferral with no end
date, and the record trailed the catalogue for five days until the owner noticed. This
command reads every source the process takes results from and every queue the record
keeps, and says for each item which open bead owns it, or that none does.

The sources, one section of the report each:

- **GitHub issues**: `check_requests --github`'s comparison through `gh`: issues the
  record lacks, replies missing from it, and comments after an entry's `read_through`.
- **Watched repositories**: every repository the source register, a packet's acquisition
  record or README, or the site's list of other projects names. `git ls-remote` reads each
  head. A head that no packet pins and that `campaign/intake-watch.yaml` has not read is
  new to the record, and a commit-only fetch counts and dates the commits past the pins.
- **The Kingbird catalogue**: the newest capture `devtools.capture_kingbird_catalogue`
  wrote, when it is newer than the record's, compared count by count through
  `devtools.diff_kingbird_catalogue`. A count it moves below its record is an intake.
- **Other catalogues**: the register's other catalogue and release sources, which no
  command reads, with the day each was last reviewed.
- **Record-side queues**: counts pending catalogue intake, deferred conflicts, the
  triage, results, asks and replies open issues are owed, and the validation backlog.
- **Manual reports**: they have no machine source. The runbook makes each a bead
  labelled `result-import` first, so the open ones are listed as the bead queue.

An item **needs an owner** when the record is behind a source and no open bead owns the
difference, or when the bead a deferral names is no longer open. The command then exits 1.
Items an open bead owns, the backlog and the bead queue are listed and do not fail it. A
source this run could not read is listed under **Not checked**, so a quiet report is not
mistaken for a clean one.

Usage, from `packing/`, or `make intake` at the root, which captures the catalogue first::

    uv run --frozen --all-extras --group dev python -m devtools.intake_sweep
    uv run --frozen --all-extras --group dev python -m devtools.intake_sweep --offline
    uv run --frozen --all-extras --group dev python -m devtools.intake_sweep --json

`--offline` skips GitHub and the remote heads, the two network steps; everything else
reads the tree, the bead store and the capture directory. The command writes nothing
outside a temporary directory, and no validation tier runs it: refreshing a public source
is a dated research survey, not a network operation inside ordinary validation
(`frontier/README.md`, Source Coverage and Freshness).
"""

from __future__ import annotations

import argparse
import gzip
import json
import os
import re
import subprocess
import sys
import tempfile
from collections.abc import Callable, Iterable, Mapping, Sequence
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass, field
from datetime import UTC, date, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

from devtools import check_bead_tree, check_requests
from devtools.audit_kingbird_catalogue import load_frontier_cases
from devtools.capture_kingbird_catalogue import CAPTURE_PREFIX, CAPTURES, STEM
from devtools.diff_kingbird_catalogue import compare, record_standings
from devtools.overview_sections import OTHER_PROJECTS
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
COVERAGE = ROOT / "frontier" / "source-coverage.yaml"
FRONTIER = ROOT / "frontier"
WATCH = ROOT / "campaign" / "intake-watch.yaml"
PACKETS = ROOT / "resources" / "web"

NEEDS_OWNER = "needs an owner"
OWNED = "owned"
LISTED = "listed"

#: The register's roles for a source that publishes many results and is read as a whole.
CATALOGUE_ROLES = frozenset({"current-catalogue", "first-party-release"})
KINGBIRD = "kingbird-current"
IMPORT_LABEL = "result-import"
SHA = re.compile(r"\b[0-9a-f]{40}\b")
_GITHUB = re.compile(r"https://github\.com/([\w.-]+)/([\w.-]+)")
_GIST = re.compile(r"https://gist\.github\.com/(?:[\w.-]+/)?([0-9a-f]+)(?:\.git)?")
_CAPTURE_DIR = re.compile(rf"{re.escape(CAPTURE_PREFIX)}(\d{{4}}-\d{{2}}-\d{{2}})")
NETWORK_TIMEOUT_SECONDS = 60
#: Read without a terminal, so a repository that has gone private fails instead of asking.
GIT_ENV = {**os.environ, "GIT_TERMINAL_PROMPT": "0"}

Mapped = Mapping[str, Any]


@dataclass(frozen=True)
class Item:
    """One thing the record has not taken in, or a queue entry, and who owns it."""

    what: str
    state: str
    bead: str = ""
    bead_state: str = ""
    since: str = ""
    step: str = ""


@dataclass
class Section:
    """One source's items, what the run noted about it, and what it could not read."""

    title: str
    items: list[Item] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    unchecked: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class Beads:
    """Bead states by `think-` alias, and the open beads labelled `result-import`."""

    states: dict[str, str]
    queue: tuple[tuple[str, str, str], ...]

    @classmethod
    def load(cls) -> Beads | None:
        found = check_bead_tree.load()
        if found is None:
            return None
        beads, _, aliases = found
        by_tail = {str(b["id"]).rpartition("-")[2]: b for b in beads}
        states: dict[str, str] = {}
        queue: list[tuple[str, str, str]] = []
        for short, tail in aliases.items():
            bead = by_tail.get(tail)
            if bead is None:
                continue
            alias, status = f"think-{short}", str(bead.get("status"))
            states[alias] = status
            if status in check_bead_tree.LIVE and IMPORT_LABEL in (bead.get("labels") or ()):
                queue.append((alias, status, str(bead.get("title", ""))))
        return cls(states, tuple(sorted(queue)))

    def state(self, alias: str) -> str:
        return self.states.get(alias, "no such bead")


def owned(
    what: str, alias: str, beads: Beads | None, *, since: str = "", step: str = ""
) -> Item:
    """An item a bead is named to own: owned while that bead is open, else orphaned."""
    if not alias:
        return Item(what, NEEDS_OWNER, since=since, step=step)
    if beads is None:
        return Item(what, OWNED, alias, "unconfirmed: no bead store", since, step)
    state = beads.state(alias)
    return Item(
        what, OWNED if state in check_bead_tree.LIVE else NEEDS_OWNER, alias, state, since, step
    )


def age(since: str, today: date) -> str:
    """`since` and how many days ago it was, for a reader deciding what is stale."""
    try:
        days = (today - date.fromisoformat(since[:10])).days
    except ValueError:
        return since
    return f"{since[:10]} ({days} day{'' if days == 1 else 's'} ago)"


# -- GitHub issues --------------------------------------------------------------------


def github_section(
    record: Mapped, *, offline: bool, compare_github: Callable[[Mapped], list[str]]
) -> Section:
    section = Section(f"GitHub issues on {record['repository']}")
    if offline:
        section.unchecked.append("GitHub issues: skipped by --offline")
        return section
    try:
        differences = compare_github(record)
    except (subprocess.CalledProcessError, OSError, ValueError) as error:
        detail = getattr(error, "stderr", "") or str(error)
        section.unchecked.append(f"GitHub issues: `gh api` failed: {str(detail).strip()[:200]}")
        return section
    section.items.extend(
        Item(difference, NEEDS_OWNER, step=_github_step(difference))
        for difference in differences
    )
    if not differences:
        section.notes.append("The record holds every issue, reply and comment.")
    return section


def _github_step(difference: str) -> str:
    """What `result-import.md`'s After the Merge does with one kind of difference."""
    if "is not in the record" in difference:
        return "enter it in result-requests.yaml with triage: pending, and an import bead"
    if "unread comment" in difference:
        return "read it: map any result it reports, then move the entry's read_through"
    if "reply missing" in difference:
        return "record the reply under the issue's replies"
    return "reconcile result-requests.yaml with the issue"


# -- Watched repositories -------------------------------------------------------------


def repository(url: str) -> str | None:
    """A source's address as its repository's, with no revision, path or `.git`."""
    if match := _GITHUB.match(url):
        name = match[2].rstrip(".").removesuffix(".git")
        return f"https://github.com/{match[1]}/{name}"
    if match := _GIST.match(url):
        return f"https://gist.github.com/{match[1]}"
    return None


@dataclass
class Watched:
    """A repository the record cites, and every commit of it the record retains."""

    url: str
    pins: set[str] = field(default_factory=set)
    cited_by: set[str] = field(default_factory=set)


def _acquisition_sources(packets: Path) -> Iterable[tuple[str, Mapped]]:
    for path in sorted(packets.glob("*/acquisition/sources.json*")):
        raw = gzip.decompress(path.read_bytes()) if path.suffix == ".gz" else path.read_bytes()
        for source in json.loads(raw).get("sources") or ():
            yield path.parent.parent.name, source


def watched_repositories(
    coverage: Mapped, packets: Path = PACKETS, projects: Iterable[str] | None = None
) -> dict[str, Watched]:
    """Every repository the record names, keyed in lower case, with the commits it pins.

    A pin is a full commit id the record gives for the repository: a packet's acquisition
    record, a commit in a register source's address or notes, or one in the README of a
    packet that names the repository. A commit of another repository counted here by a
    README that names two is harmless, since it never equals this one's head.
    """
    found: dict[str, Watched] = {}

    def watch(url: str | None, cited_by: str, pins: Iterable[str] = ()) -> None:
        if url is None:
            return
        entry = found.setdefault(url.lower(), Watched(url))
        entry.cited_by.add(cited_by)
        entry.pins.update(pins)

    for source in coverage["sources"]:
        text = f"{source['url']} {source.get('notes', '')}"
        watch(repository(source["url"]), source["id"], SHA.findall(text))
    for packet, source in _acquisition_sources(packets):
        commit = source.get("source_commit") or source.get("source_ref") or ""
        watch(repository(str(source.get("source_url", ""))), packet, SHA.findall(commit))
    for url in projects if projects is not None else (u for u, _, _ in OTHER_PROJECTS):
        watch(repository(url), "the site's other projects")
    for readme in sorted(packets.glob("*/README.md")):
        text = readme.read_text(encoding="utf-8", errors="replace")
        named = {repository(m.group(0)) for m in _GITHUB.finditer(text)}
        for url in named:
            if url is not None and url.lower() in found:
                found[url.lower()].pins.update(SHA.findall(text))
    return found


def remote_head(url: str) -> str:
    """The commit a repository's default branch points at now; network."""
    shown = subprocess.run(
        ("git", "ls-remote", url, "HEAD"),
        capture_output=True,
        text=True,
        timeout=NETWORK_TIMEOUT_SECONDS,
        env=GIT_ENV,
        check=False,
    )
    head = shown.stdout.split()[:1]
    if shown.returncode or not head:
        raise RuntimeError((shown.stderr.strip().splitlines() or ["no HEAD"])[-1])
    return head[0]


@dataclass(frozen=True)
class NewCommits:
    """The commits a head holds past every retained pin present in its history."""

    count: int
    first: str
    last: str
    subjects: tuple[str, ...]
    pins_in_history: int


def new_commits(url: str, head: str, known: Iterable[str]) -> NewCommits:
    """Count and date the commits past the pins, from a commit-only fetch; network.

    `--filter=tree:0` fetches commits and no trees or blobs, about a second and half a
    megabyte for a repository of 560 commits, into a directory removed on return. Which
    pins are in the head's history is read from the fetched commit list, never by asking
    for an object: in a partial clone a missing object is fetched from the remote, one
    round trip per pin, which made the first version of this sweep take minutes.
    """
    with tempfile.TemporaryDirectory(prefix="intake-sweep-") as scratch:

        def git(*arguments: str) -> subprocess.CompletedProcess[str]:
            return subprocess.run(
                ("git", "-C", scratch, *arguments),
                capture_output=True,
                text=True,
                timeout=NETWORK_TIMEOUT_SECONDS,
                env=GIT_ENV,
                check=False,
            )

        git("init", "--quiet", "--bare")
        fetched = git("fetch", "--quiet", "--no-tags", "--filter=tree:0", url, head)
        if fetched.returncode:
            raise RuntimeError((fetched.stderr.strip().splitlines() or ["fetch failed"])[-1])
        history = set(git("rev-list", head).stdout.split())
        present = sorted(pin for pin in set(known) if pin in history)
        listed = git("log", "--format=%cI%x09%s", head, "--not", *present, "--")
        lines = [line.split("\t", 1) for line in listed.stdout.splitlines() if "\t" in line]
        return NewCommits(
            count=len(lines),
            first=lines[-1][0][:10] if lines else "",
            last=lines[0][0][:10] if lines else "",
            subjects=tuple(subject for _, subject in lines[:3]),
            pins_in_history=len(present),
        )


Heads = Callable[[str], str]
History = Callable[[str, str, Iterable[str]], NewCommits]


def repositories_section(
    coverage: Mapped,
    watch: Mapped,
    beads: Beads | None,
    *,
    offline: bool,
    heads: Heads = remote_head,
    history: History = new_commits,
    packets: Path = PACKETS,
    projects: Iterable[str] | None = None,
) -> Section:
    repos = watched_repositories(coverage, packets, projects)
    section = Section(f"Watched repositories ({len(repos)})")
    reads = {str(entry["url"]).lower(): entry for entry in watch.get("repositories") or ()}
    section.unchecked.extend(
        f"intake-watch.yaml reads {url}, which no record cites; remove the entry"
        for url in sorted(set(reads) - set(repos))
    )
    if offline:
        section.unchecked.append(f"{len(repos)} repository heads: skipped by --offline")
        return section
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = dict(
            zip(repos, pool.map(_try(heads), (r.url for r in repos.values())), strict=True)
        )
    current = 0
    behind: list[tuple[Watched, str, set[str], Mapped | None]] = []
    for key, entry in sorted(repos.items()):
        head = results[key]
        if isinstance(head, Exception):
            section.unchecked.append(f"{entry.url}: `git ls-remote` failed: {head}")
            continue
        read = reads.get(key)
        if head in entry.pins:
            current += 1
            if read is not None:
                section.notes.append(
                    f"{entry.url}: a packet now pins the head, so intake-watch.yaml's read of "
                    f"{str(read['read_through'])[:12]} can be removed."
                )
            continue
        if read is not None and str(read["read_through"]) == head:
            if read.get("bead"):
                section.items.append(
                    owned(
                        f"{entry.url} at {head[:12]}: {read['note']}",
                        str(read["bead"]),
                        beads,
                        since=str(read["read_on"]),
                        step="import it: a packet at the head, then stages 2 and 3",
                    )
                )
            else:
                section.notes.append(
                    f"{entry.url}: read through {head[:12]} on {read['read_on']}, "
                    "nothing to import."
                )
            continue
        known = entry.pins | ({str(read["read_through"])} if read is not None else set())
        behind.append((entry, head, known, read))
    with ThreadPoolExecutor(max_workers=8) as pool:
        section.items.extend(
            pool.map(lambda job: _new_head(job[0], job[1], job[2], job[3], history), behind)
        )
    section.notes.insert(0, f"{current} of {len(repos)} heads are a commit a packet pins.")
    return section


def _try(function: Callable[[str], str]) -> Callable[[str], str | Exception]:
    def attempt(argument: str) -> str | Exception:
        try:
            return function(argument)
        except (RuntimeError, OSError, subprocess.SubprocessError) as error:
            return error

    return attempt


def _new_head(
    entry: Watched, head: str, known: set[str], read: Mapped | None, history: History
) -> Item:
    past = "the last pass's read" if read is not None else "every retained pin"
    try:
        commits = history(entry.url, head, known)
    except (RuntimeError, OSError, subprocess.SubprocessError) as error:
        what = (
            f"{entry.url}: head {head[:12]} is past {past}; the commits could not be read "
            f"({error})"
        )
        return Item(what, NEEDS_OWNER, step=_REPOSITORY_NEXT)
    if not known:
        where = "no packet pins it"
    elif commits.pins_in_history:
        where = f"{commits.count} commit{'' if commits.count == 1 else 's'} past {past}"
    else:
        where = "no retained pin is in its history"
    span = f", {commits.first}" if commits.first else ""
    if commits.last != commits.first:
        span += f" to {commits.last}"
    newest = (
        f"; newest: {commits.subjects[0]}" if commits.subjects and commits.subjects[0] else ""
    )
    return Item(
        f"{entry.url}: head {head[:12]}, {where}{span}{newest}",
        NEEDS_OWNER,
        since=commits.first,
        step=_REPOSITORY_NEXT,
    )


_REPOSITORY_NEXT = (
    "read it: an import bead and a packet for a new result, else a read in intake-watch.yaml"
)


# -- The Kingbird catalogue and the other catalogues ----------------------------------


def newest_capture(captures: Path = CAPTURES) -> tuple[str, Path] | None:
    """The newest dated capture `capture_kingbird_catalogue` wrote, as (date, transcription)."""
    dated = [
        (match[1], path / f"{STEM}.md")
        for path in captures.glob(f"{CAPTURE_PREFIX}*")
        if (match := _CAPTURE_DIR.fullmatch(path.name)) and (path / f"{STEM}.md").is_file()
    ]
    return max(dated) if dated else None


def kingbird_section(
    coverage: Mapped,
    beads: Beads | None,
    today: date,
    *,
    capture: tuple[str, Path] | None,
    cases: Mapping[int, Mapping[str, object]] | None = None,
) -> Section:
    source = next(s for s in coverage["sources"] if s["id"] == KINGBIRD)
    reviewed = str(source["reviewed"])
    section = Section("The Kingbird catalogue")
    command = "`make intake`, or `python -m devtools.capture_kingbird_catalogue` from packing/"
    if capture is None or capture[0] <= reviewed:
        section.unchecked.append(
            f"Kingbird catalogue: no capture newer than the record's, {age(reviewed, today)}; "
            f"capture one with {command}"
        )
        return section
    captured, path = capture
    retained = (ROOT / str(source["local"])).with_suffix(".md")
    changes = compare(retained.read_text(encoding="utf-8"), path.read_text(encoding="utf-8"))
    standings = record_standings(
        changes, load_frontier_cases(FRONTIER) if cases is None else cases
    )
    pending = {int(e["n"]): e for e in coverage.get("pending_catalogue_intake") or ()}
    other: list[int] = []
    for change in changes:
        standing = standings.get(change.n)
        if standing is None or standing.relation != "below" or change.after is None:
            other.append(change.n)
            continue
        what = (
            f"n = {change.n}: the capture of {captured} prints {change.after.side}, below the "
            f"record's {standing.value} ({standing.source_key})"
        )
        declared = pending.get(change.n)
        if declared is not None and Decimal(declared["catalogue_value"]) == Decimal(
            change.after.side
        ):
            section.items.append(
                owned(what, str(declared["bead"]), beads, since=str(declared["recorded"]))
            )
        else:
            section.items.append(
                Item(
                    what,
                    NEEDS_OWNER,
                    since=captured,
                    step="an intake: a bead, then register it or declare it pending intake",
                )
            )
    section.notes.append(
        f"Compared the capture of {captured} with the record's of {reviewed}: "
        f"{len(changes)} count{'' if len(changes) == 1 else 's'} read differently, "
        f"{len(changes) - len(other)} below the record."
    )
    if other:
        section.notes.append(
            "Changed and not below the record, for the refresh to classify with "
            f"`diff_kingbird_catalogue`: n = {', '.join(map(str, other))}."
        )
    return section


def catalogues_section(coverage: Mapped, today: date) -> Section:
    """The register's other catalogue and release sources: no command reads them."""
    section = Section("Other catalogues and releases")
    for source in coverage["sources"]:
        if source["role"] not in CATALOGUE_ROLES or source["id"] == KINGBIRD:
            continue
        section.unchecked.append(
            f"{source['title']} ({source['url']}): read by hand; last reviewed "
            f"{age(str(source['reviewed']), today)}, source dated {source['source_date']}"
        )
    return section


# -- Record-side queues ---------------------------------------------------------------


def queues_section(
    coverage: Mapped,
    record: Mapped,
    register: check_requests.Register,
    beads: Beads | None,
    today: date,
) -> Section:
    section = Section("Record-side queues")
    for entry in coverage.get("pending_catalogue_intake") or ():
        section.items.append(
            owned(
                f"n = {entry['n']} pending catalogue intake: the catalogue prints "
                f"{entry['catalogue_value']}, the record reports {entry['record_value']}",
                str(entry.get("bead") or ""),
                beads,
                since=age(str(entry.get("recorded") or ""), today),
                step="register the result and take the side into the record",
            )
        )
    for claim in coverage.get("beyond_horizon_claims") or ():
        if claim.get("disposition") == "deferred-conflict":
            section.items.append(
                owned(
                    f"n = {claim['n']} deferred conflict with {claim['source_id']}",
                    str(claim.get("bead") or ""),
                    beads,
                )
            )
    for issue in record["issues"]:
        if issue["state"] != "open":
            continue
        state = check_requests.issue_state(issue, register)
        owed = [
            *(["triage"] if issue["triage"] == "pending" else []),
            *(
                f"queued result {r.key}"
                for r in state.results
                if r.state == check_requests.QUEUED
            ),
            *(
                f"queued ask: {a['what']}"
                for a in issue.get("asks", ())
                if a["state"] == "queued"
            ),
            *(["a reply"] if state.replies_due else []),
        ]
        if owed:
            section.items.append(
                owned(
                    f"#{issue['number']} owes {'; '.join(owed)}",
                    str(issue["answer_bead"]),
                    beads,
                    since=str(issue["opened"]),
                    step="the stage it waits on; draft a reply with check_requests --draft",
                )
            )
    return section


def backlog_section(
    record: Mapped, register: check_requests.Register, beads: Beads | None
) -> Section:
    section = Section("Validation backlog: register entries below V3 or C3")
    for row in check_requests.backlog_rows(record, register):
        named = [f"{b} ({beads.state(b) if beads else '?'})" for b in row.beads]
        section.items.append(
            Item(
                f"{row.id} at {row.rungs}, {row.status}"
                + (f", {row.activity}" if row.activity else "")
                + (f"; issues {', '.join(f'#{n}' for n in row.issues)}" if row.issues else ""),
                LISTED,
                bead=", ".join(named) or "none named",
                step=row.next_rung[:160],
            )
        )
    return section


def bead_queue_section(beads: Beads | None) -> Section:
    section = Section(f"Open `{IMPORT_LABEL}` beads, manual reports included")
    if beads is None:
        section.unchecked.append(
            "bead queue: no bead store (no tbd sync worktree, no tbd-sync branch)"
        )
        return section
    section.items.extend(
        Item(title, LISTED, bead=alias, bead_state=status)
        for alias, status, title in beads.queue
    )
    return section


# -- The report -----------------------------------------------------------------------


def sweep(
    *,
    today: date,
    offline: bool,
    capture: tuple[str, Path] | None,
    beads: Beads | None,
    compare_github: Callable[[Mapped], list[str]] = check_requests.compare_github,
    heads: Heads = remote_head,
    history: History = new_commits,
) -> list[Section]:
    coverage = safe_load(COVERAGE.read_text(encoding="utf-8"))
    watch = safe_load(WATCH.read_text(encoding="utf-8"))
    record = check_requests.load_record()
    register = check_requests.load_register()
    return [
        github_section(record, offline=offline, compare_github=compare_github),
        repositories_section(
            coverage, watch, beads, offline=offline, heads=heads, history=history
        ),
        kingbird_section(coverage, beads, today, capture=capture),
        catalogues_section(coverage, today),
        queues_section(coverage, record, register, beads, today),
        backlog_section(record, register, beads),
        bead_queue_section(beads),
    ]


def needing_owner(sections: Sequence[Section]) -> list[Item]:
    return [item for section in sections for item in section.items if item.state == NEEDS_OWNER]


def _count(number: int, noun: str) -> str:
    return f"{number} {noun}{'' if number == 1 else 's'}"


def _cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def markdown(sections: Sequence[Section], today: date) -> str:
    """The report: what needs an owner and what was not checked first, then each source."""
    orphans = [(s.title, i) for s in sections for i in s.items if i.state == NEEDS_OWNER]
    owned_count = sum(item.state == OWNED for s in sections for item in s.items)
    unchecked = [line for section in sections for line in section.unchecked]
    summary = (
        f"{_count(len(orphans), 'item')} without an open bead to own it, "
        f"{_count(owned_count, 'item')} owned by one, and "
        f"{_count(len(unchecked), 'source')} not checked."
    )
    lines = [f"# Intake Sweep, {today.isoformat()}", "", summary, ""]
    if orphans:
        lines += [
            "## Needs an Owner",
            "",
            "| source | item | since | next |",
            "| --- | --- | --- | --- |",
        ]
        lines += [
            f"| {title} | {_cell(i.what)} | {i.since} | {_cell(i.step)} |"
            for title, i in orphans
        ]
        lines.append("")
    if unchecked:
        lines += ["## Not Checked", "", *(f"- {line}" for line in unchecked), ""]
    for section in sections:
        lines += [f"## {section.title}", ""]
        lines += [*section.notes, ""] if section.notes else []
        shown = [item for item in section.items if item.state != NEEDS_OWNER]
        if len(shown) < len(section.items):
            lines += [
                f"{_count(len(section.items) - len(shown), 'item')} above need an owner.",
                "",
            ]
        if shown:
            lines += ["| item | state | bead | since |", "| --- | --- | --- | --- |"]
            for item in shown:
                bead = f"{item.bead} ({item.bead_state})" if item.bead_state else item.bead
                lines.append(
                    f"| {_cell(item.what)} | {item.state} | {_cell(bead)} | {item.since} |"
                )
            lines.append("")
        if section.unchecked:
            lines += ["Not checked: see above.", ""]
        elif not section.items and not section.notes:
            lines += ["Nothing.", ""]
    return "\n".join(lines).rstrip() + "\n"


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    command.add_argument("--offline", action="store_true", help="skip GitHub and remote heads")
    command.add_argument("--json", action="store_true", help="print the sweep as JSON")
    command.add_argument("--capture", type=Path, help="a Kingbird capture directory to compare")
    command.add_argument("--today", type=date.fromisoformat, help=argparse.SUPPRESS)
    return command


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    today = args.today or datetime.now(UTC).date()
    capture = None
    if args.capture is not None:
        match = _CAPTURE_DIR.search(args.capture.name)
        capture = (match[1] if match else today.isoformat(), args.capture / f"{STEM}.md")
    else:
        capture = newest_capture()
    sections = sweep(today=today, offline=args.offline, capture=capture, beads=Beads.load())
    if args.json:
        document = {
            "date": today.isoformat(),
            "needs_owner": len(needing_owner(sections)),
            "sections": [asdict(section) for section in sections],
        }
        json.dump(document, sys.stdout, indent=2, ensure_ascii=False)
        sys.stdout.write("\n")
    else:
        sys.stdout.write(markdown(sections, today))
    return 1 if needing_owner(sections) else 0


if __name__ == "__main__":
    raise SystemExit(main())
