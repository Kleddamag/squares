"""The intake sweep: every source read, every item owned by an open bead or reported.

The miss it exists for: on 2026-09-30 three Kingbird counts were held as pending intake
with no bead, nothing listed them, and the record trailed the catalogue for five days.
These pin each source's reading on fixtures small enough to read, with the two network
steps replaced, and pin that `--offline` makes no network call at all.
"""

from __future__ import annotations

import gzip
import json
from datetime import date
from pathlib import Path
from typing import Any

import pytest

from devtools import capture_kingbird_catalogue as capture_tool
from devtools import check_requests
from devtools import intake_sweep as sweep
from sqpack.yamlio import safe_load

TODAY = date(2026, 10, 5)
HEAD = "a" * 40
PIN = "b" * 40
LATER = "c" * 40


def _beads(**states: str) -> sweep.Beads:
    return sweep.Beads(dict(states), ())


def _coverage(**extra: Any) -> dict[str, Any]:
    return {
        "sources": [
            {
                "id": "repo-source",
                "role": "source-repository",
                "url": f"https://github.com/someone/packings/tree/{PIN}",
                "notes": "Retained at its head.",
            },
            {
                "id": "release",
                "role": "first-party-release",
                "title": "A Release",
                "url": "https://example.org/",
                "reviewed": "2026-08-25",
                "source_date": "2026-07-29",
            },
        ],
        **extra,
    }


def test_a_repository_is_named_without_its_revision_path_or_git_suffix() -> None:
    assert (
        sweep.repository(f"https://github.com/evand/square-packing/tree/{PIN}")
        == "https://github.com/evand/square-packing"
    )
    assert sweep.repository("https://github.com/a/b.git") == "https://github.com/a/b"
    assert (
        sweep.repository("https://gist.github.com/9e5f27e25607c0966c4f91bc1253ce8b.git")
        == "https://gist.github.com/9e5f27e25607c0966c4f91bc1253ce8b"
    )
    assert sweep.repository("https://doi.org/10.5281/zenodo.1") is None


def test_pins_come_from_the_register_acquisition_records_and_packet_readmes(
    tmp_path: Path,
) -> None:
    packet = tmp_path / "someone-packings-2026-10-01"
    (packet / "acquisition").mkdir(parents=True)
    record = {
        "sources": [
            {"source_url": "https://github.com/someone/packings", "source_commit": LATER}
        ]
    }
    (packet / "acquisition" / "sources.json.gz").write_bytes(
        gzip.compress(json.dumps(record).encode())
    )
    readme = tmp_path / "other-2026-09-01"
    readme.mkdir()
    (readme / "README.md").write_text(
        f"Retained from https://github.com/Other/Thing at {HEAD}.\n", encoding="utf-8"
    )
    found = sweep.watched_repositories(
        _coverage(), tmp_path, projects=["https://github.com/Other/Thing"]
    )
    assert found["https://github.com/someone/packings"].pins == {PIN, LATER}
    assert found["https://github.com/other/thing"].pins == {HEAD}
    assert found["https://github.com/other/thing"].url == "https://github.com/Other/Thing"


def _repositories(
    tmp_path: Path,
    head: str | Exception,
    watch: dict[str, Any] | None = None,
    beads: sweep.Beads | None = None,
    *,
    offline: bool = False,
) -> sweep.Section:
    def heads(_url: str) -> str:
        if isinstance(head, Exception):
            raise head
        return head

    def history(_url: str, _at: str, _known: Any) -> sweep.NewCommits:
        return sweep.NewCommits(3, "2026-10-03", "2026-10-04", ("new records",), 1)

    return sweep.repositories_section(
        _coverage(),
        watch or {"repositories": []},
        beads,
        offline=offline,
        heads=heads,
        history=history,
        packets=tmp_path,
        projects=[],
    )


def test_a_head_a_packet_pins_is_current_and_a_moved_head_needs_an_owner(
    tmp_path: Path,
) -> None:
    current = _repositories(tmp_path, PIN)
    assert current.items == []
    assert current.notes == ["1 of 1 heads are a commit a packet pins."]
    moved = _repositories(tmp_path, HEAD)
    (item,) = moved.items
    assert item.state == sweep.NEEDS_OWNER
    assert item.what == (
        "https://github.com/someone/packings: head aaaaaaaaaaaa, 3 commits past every "
        "retained pin, 2026-10-03 to 2026-10-04; newest: new records"
    )


def test_a_read_head_is_owned_by_its_bead_or_closed_with_nothing_to_import(
    tmp_path: Path,
) -> None:
    read = {"url": "https://github.com/someone/packings", "read_through": HEAD}
    owned_read = {
        **read,
        "read_on": "2026-10-05",
        "note": "s(58) >= 7.935",
        "bead": "think-aaaa",
    }
    section = _repositories(
        tmp_path, HEAD, {"repositories": [owned_read]}, _beads(**{"think-aaaa": "open"})
    )
    assert [(i.state, i.bead) for i in section.items] == [(sweep.OWNED, "think-aaaa")]
    closed = _repositories(
        tmp_path, HEAD, {"repositories": [owned_read]}, _beads(**{"think-aaaa": "closed"})
    )
    assert closed.items[0].state == sweep.NEEDS_OWNER
    nothing = {**read, "read_on": "2026-10-05", "note": "README edits"}
    quiet = _repositories(tmp_path, HEAD, {"repositories": [nothing]})
    assert quiet.items == []
    assert quiet.notes[-1].endswith("nothing to import.")
    later = _repositories(tmp_path, LATER, {"repositories": [nothing]})
    assert "past the last pass's read" in later.items[0].what


def test_an_unreadable_head_and_offline_are_reported_as_not_checked(tmp_path: Path) -> None:
    failed = _repositories(tmp_path, RuntimeError("repository not found"))
    assert failed.items == []
    assert failed.unchecked == [
        "https://github.com/someone/packings: `git ls-remote` failed: repository not found"
    ]
    offline = _repositories(tmp_path, HEAD, offline=True)
    assert offline.unchecked == ["1 repository heads: skipped by --offline"]
    stray = {"url": "https://github.com/nobody/cites-this", "read_through": HEAD}
    section = _repositories(tmp_path, PIN, {"repositories": [stray]})
    assert "which no record cites" in section.unchecked[0]


def test_github_differences_each_need_an_owner_and_a_failure_is_not_checked() -> None:
    record = {"repository": "jlevy/squares"}
    differences = ["#350 is not in the record: New result", "#282: unread comment URL (x, t)"]
    section = sweep.github_section(record, offline=False, compare_github=lambda _: differences)
    assert [i.state for i in section.items] == [sweep.NEEDS_OWNER] * 2
    assert "triage: pending" in section.items[0].step
    assert "read_through" in section.items[1].step

    def refused(_: object) -> list[str]:
        raise OSError("gh: not found")

    failed = sweep.github_section(record, offline=False, compare_github=refused)
    assert failed.unchecked == ["GitHub issues: `gh api` failed: gh: not found"]
    skipped = sweep.github_section(record, offline=True, compare_github=refused)
    assert skipped.unchecked == ["GitHub issues: skipped by --offline"]


#: A count the retained transcription prints once, and a later capture moves below it.
SIDE, LOWER = r"\Nn{5.93383346267692}", r"\Nn{5.93383000000000}"
CASES = {
    29: {"reported_upper_bound": {"value": "5.93383346267692", "source_key": "[Kingbird]"}}
}


def _kingbird(tmp_path: Path, text: str, **coverage: Any) -> sweep.Section:
    capture = tmp_path / "kingbird-2026-10-05"
    capture.mkdir()
    (capture / f"{capture_tool.STEM}.md").write_text(text, encoding="utf-8")
    live = safe_load(sweep.COVERAGE.read_text(encoding="utf-8"))
    live["pending_catalogue_intake"] = coverage.get("pending", [])
    return sweep.kingbird_section(
        live,
        coverage.get("beads"),
        TODAY,
        capture=sweep.newest_capture(tmp_path),
        cases=CASES,
    )


def _retained() -> str:
    live = safe_load(sweep.COVERAGE.read_text(encoding="utf-8"))
    source = next(s for s in live["sources"] if s["id"] == sweep.KINGBIRD)
    return (sweep.ROOT / source["local"]).with_suffix(".md").read_text(encoding="utf-8")


def test_a_count_a_newer_capture_moves_below_its_record_is_an_intake(tmp_path: Path) -> None:
    text = _retained()
    assert text.count(SIDE) == 1
    section = _kingbird(tmp_path, text.replace(SIDE, LOWER))
    (item,) = section.items
    assert item.state == sweep.NEEDS_OWNER
    assert item.what.startswith("n = 29: the capture of 2026-10-05 prints 5.93383000000000")


def test_a_count_declared_pending_with_its_bead_is_owned(tmp_path: Path) -> None:
    pending = [
        {"n": 29, "catalogue_value": "5.93383", "bead": "think-aaaa", "recorded": "2026-10-05"}
    ]
    section = _kingbird(
        tmp_path,
        _retained().replace(SIDE, LOWER),
        pending=pending,
        beads=_beads(**{"think-aaaa": "open"}),
    )
    assert [(i.state, i.bead) for i in section.items] == [(sweep.OWNED, "think-aaaa")]


def test_an_unchanged_capture_is_clean_and_no_newer_capture_is_not_checked(
    tmp_path: Path,
) -> None:
    same = _kingbird(tmp_path, _retained())
    assert same.items == []
    assert "0 counts read differently" in same.notes[0]
    live = safe_load(sweep.COVERAGE.read_text(encoding="utf-8"))
    none = sweep.kingbird_section(live, None, TODAY, capture=None, cases=CASES)
    assert none.unchecked[0].startswith(
        "Kingbird catalogue: no capture newer than the record's"
    )


def test_catalogues_no_command_reads_are_listed_with_their_age() -> None:
    (line,) = sweep.catalogues_section(_coverage(), TODAY).unchecked
    assert line == (
        "A Release (https://example.org/): read by hand; last reviewed 2026-08-25 "
        "(41 days ago), source dated 2026-07-29"
    )


def _issue(**extra: Any) -> dict[str, Any]:
    return {
        "number": 300,
        "state": "open",
        "triage": "done",
        "opened": "2026-10-01",
        "answer_bead": "think-bbbb",
        "results": [
            {"key": "later", "claim": "a bound", "not_registered": "not yet", "queued": True}
        ],
        "asks": [{"what": "a correction", "state": "queued"}],
        "replies": [],
        **extra,
    }


def test_a_pending_intake_and_an_open_issue_are_owned_while_their_beads_are_open() -> None:
    coverage = _coverage(
        pending_catalogue_intake=[
            {
                "n": 69,
                "catalogue_value": "8.82",
                "record_value": "8.83",
                "bead": "think-aaaa",
                "recorded": "2026-09-30",
            }
        ]
    )
    register = check_requests.Register(results={}, evidence={})
    beads = _beads(**{"think-aaaa": "in_progress", "think-bbbb": "closed"})
    section = sweep.queues_section(coverage, {"issues": [_issue()]}, register, beads, TODAY)
    intake, issue = section.items
    assert (intake.state, intake.since) == (sweep.OWNED, "2026-09-30 (5 days ago)")
    assert issue.state == sweep.NEEDS_OWNER
    assert issue.what == "#300 owes queued result later; queued ask: a correction; a reply"
    orphan = {**coverage["pending_catalogue_intake"][0]}
    del orphan["bead"]
    bare = sweep.queues_section(
        _coverage(pending_catalogue_intake=[orphan]), {"issues": []}, register, beads, TODAY
    )
    assert bare.items[0].state == sweep.NEEDS_OWNER


def test_offline_reads_no_network_and_reports_what_it_skipped() -> None:
    def network(*_: object) -> Any:
        pytest.fail("--offline made a network call")

    sections = sweep.sweep(
        today=TODAY,
        offline=True,
        capture=None,
        beads=None,
        compare_github=network,
        heads=network,
        history=network,
    )
    unchecked = [line for section in sections for line in section.unchecked]
    assert "GitHub issues: skipped by --offline" in unchecked
    assert any(line.endswith("repository heads: skipped by --offline") for line in unchecked)
    report = sweep.markdown(sections, TODAY)
    assert report.startswith("# Intake Sweep, 2026-10-05\n")
    assert "## Not Checked" in report


def test_the_report_leads_with_what_needs_an_owner() -> None:
    sections = [
        sweep.Section(
            "Source",
            items=[
                sweep.Item("orphan", sweep.NEEDS_OWNER, step="open a bead"),
                sweep.Item("held", sweep.OWNED, bead="think-aaaa", bead_state="open"),
            ],
            unchecked=["a source: skipped"],
        )
    ]
    report = sweep.markdown(sections, TODAY)
    assert (
        "1 item without an open bead to own it, 1 item owned by one, and 1 source not" in report
    )
    assert report.index("## Needs an Owner") < report.index("## Not Checked")
    assert report.index("## Not Checked") < report.index("## Source")
    assert "| Source | orphan |  | open a bead |" in report
    assert "| held | owned | think-aaaa (open) |  |" in report
    assert sweep.needing_owner(sections) == [sections[0].items[0]]


def test_a_capture_holds_the_page_its_transcription_under_the_archive_header_and_a_receipt(
    tmp_path: Path,
) -> None:
    out = tmp_path / "kingbird-2026-10-05"
    capture = capture_tool.write_capture(
        b"<html>page</html>",
        url="https://kingbird.myphotos.cc/packing/squares_in_squares.html",
        retrieved_utc="2026-10-05T06:00:00Z",
        last_modified="Thu, 01 Oct 2026 10:00:00 GMT",
        out=out,
        transcriber=lambda page: f"body of {page.name}\n",
    )
    text = (out / f"{capture_tool.STEM}.md").read_text(encoding="utf-8")
    assert text.startswith(f"# Archived: {capture_tool.STEM}\n\n**Source:** https://kingbird")
    assert "**Archived:** 2026-10-05, retrieved 06:00:00 UTC; the server reported" in text
    assert text.endswith("---\n\nbody of kingbird-squares-in-squares.html\n")
    receipt = json.loads((out / "capture.json").read_text(encoding="utf-8"))
    assert receipt["html_bytes"] == capture.html_bytes == len(b"<html>page</html>")
    assert sweep.newest_capture(tmp_path) == ("2026-10-05", out / f"{capture_tool.STEM}.md")
