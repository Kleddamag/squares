"""The bead staleness report: two shapes the tree checker prints and never fails on.

The bead tree and the agenda layer are edited by different hands at different times.
Cells name beads through a `think-` alias the store's table resolves; an in-progress
bead named only by terminal cells is work the agenda finished with, and one named by
no cell is work tracked outside the agenda layer. These pin the join and the two
counts on a fixture small enough to read.
"""

from __future__ import annotations

from pathlib import Path

from devtools.check_bead_tree import (
    check,
    deferral_problems,
    deferrals,
    parse_aliases,
    staleness,
)


def _bead(bead_id: str, status: str, title: str) -> dict[str, object]:
    return {"id": bead_id, "status": status, "title": title}


def _cell(cell_id: str, state: str, bead: str) -> dict[str, str]:
    return {"id": cell_id, "agenda": "agenda-001", "state": state, "bead": bead}


FINISHED = _bead("is-01aaaa", "in_progress", "finished on the agenda, live on the tree")
OUTSIDE = _bead("is-01bbbb", "in_progress", "tracked outside the agenda layer")
ALIASES = {"aaaa": "01aaaa", "bbbb": "01bbbb"}


def test_an_in_progress_bead_named_only_by_terminal_cells_is_stale() -> None:
    cells = [
        _cell("BC-001", "complete", "think-aaaa"),
        _cell("BC-002", "stopped", "think-aaaa"),
    ]
    report = staleness([FINISHED, OUTSIDE], ALIASES, cells)
    assert [entry["bead"] for entry in report["stale"]] == ["think-aaaa"]
    assert report["stale"][0]["cells"] == ["BC-001 complete", "BC-002 stopped"]
    assert report["stale"][0]["title"] == "finished on the agenda, live on the tree"


def test_an_in_progress_bead_named_by_no_cell_is_untracked() -> None:
    cells = [_cell("BC-001", "complete", "think-aaaa"), _cell("BC-002", "ready", "think-zzzz")]
    report = staleness([FINISHED, OUTSIDE], ALIASES, cells)
    assert [entry["bead"] for entry in report["untracked"]] == ["think-bbbb"]
    assert report["untracked"][0]["cells"] == []


def test_one_live_naming_cell_keeps_a_bead_out_of_both_lists() -> None:
    cells = [
        _cell("BC-001", "complete", "think-aaaa"),
        _cell("BC-002", "blocked", "think-aaaa"),
    ]
    report = staleness([FINISHED], ALIASES, cells)
    assert report == {"stale": [], "untracked": []}


def test_only_in_progress_beads_are_reported() -> None:
    closed = _bead("is-01cccc", "closed", "done and closed")
    open_bead = _bead("is-01dddd", "open", "queued, not started")
    report = staleness([closed, open_bead], {"cccc": "01cccc"}, [])
    assert report == {"stale": [], "untracked": []}


def test_the_alias_table_is_read_without_yaml_retyping() -> None:
    table = (
        "schema_version: 1\n---\n1e10: 01aaaa\nnull: 01bbbb\n# note\nrh18: 01cccc\n"
        '"48e1": 01dddd\n'
    )
    assert parse_aliases(table) == {
        "schema_version": "1",
        "1e10": "01aaaa",
        "null": "01bbbb",
        "rh18": "01cccc",
        "48e1": "01dddd",
    }


def test_a_bead_without_an_alias_is_reported_by_its_id() -> None:
    report = staleness([OUTSIDE], {}, [_cell("BC-001", "ready", "think-bbbb")])
    assert [entry["bead"] for entry in report["untracked"]] == ["is-01bbbb"]


def test_the_report_does_not_change_the_gate_verdict() -> None:
    """Both shapes are reports; the tree's two invariants still decide pass or fail."""
    assert check([FINISHED, OUTSIDE]) == []


def _write(path: Path, text: str) -> Path:
    path.write_text(text, encoding="utf-8")
    return path


def test_every_deferral_a_record_declares_is_collected_with_its_bead(tmp_path: Path) -> None:
    """Pending intakes, deferred conflicts, open issues and watched-repository reads."""
    coverage = _write(
        tmp_path / "coverage.yaml",
        "pending_catalogue_intake:\n"
        "  - {n: 69, bead: think-aaaa, recorded: '2026-09-30'}\n"
        "beyond_horizon_claims:\n"
        "  - {n: 400, disposition: deferred-conflict, bead: think-bbbb}\n"
        "  - {n: 401, disposition: superseded}\n",
    )
    requests = _write(
        tmp_path / "requests.yaml",
        "issues:\n"
        "  - {number: 282, state: open, answer_bead: think-cccc}\n"
        "  - {number: 170, state: closed, answer_bead: think-dddd}\n",
    )
    watch = _write(
        tmp_path / "watch.yaml",
        "repositories:\n"
        "  - {url: 'https://github.com/a/b', read_through: 7ff3b2113532, bead: think-eeee}\n"
        "  - {url: 'https://github.com/a/c', read_through: 0123456789ab}\n",
    )
    named = deferrals(coverage, requests, watch)
    assert [alias for _, alias in named] == [
        "think-aaaa",
        "think-bbbb",
        "think-cccc",
        "think-eeee",
    ]
    assert named[0][0] == "source-coverage.yaml pending_catalogue_intake n=69"
    assert deferrals(tmp_path / "absent", tmp_path / "absent", tmp_path / "absent") == []


def test_a_deferral_whose_bead_is_closed_or_missing_fails_and_a_live_one_passes() -> None:
    """The orphan the 2026-09-30 intakes became, by a closed bead instead of none."""
    beads = [
        _bead("is-01aaaa", "open", "the intake"),
        _bead("is-01bbbb", "closed", "an intake closed under its deferral"),
        _bead("is-01cccc", "blocked", "waiting on a source"),
    ]
    aliases = {"aaaa": "01aaaa", "bbbb": "01bbbb", "cccc": "01cccc"}
    named = [
        ("pending n=69", "think-aaaa"),
        ("pending n=83", "think-bbbb"),
        ("issue #1", "think-cccc"),
        ("pending n=87", "think-zzzz"),
    ]
    problems = deferral_problems(beads, aliases, named)
    assert [(p["parent"], p["status"]) for p in problems] == [
        ("pending n=83", "closed"),
        ("pending n=87", "no such bead"),
    ]
    assert {p["kind"] for p in problems} == {"dead_deferral"}


def test_the_live_records_deferrals_are_all_well_formed_aliases() -> None:
    """What the gate resolves against the store is at least a bead alias."""
    for where, alias in deferrals():
        assert alias.startswith("think-"), where
        assert len(alias) == len("think-aaaa"), where
