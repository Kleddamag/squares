"""The stack renderer says what moved in the register between two revisions.

`devtools.render_stack_results` reads the register, its evidence, the bibliography and
the case records at two commits and renders the changed results, the frontier counts
and the rungs. These hold each comparison to a synthetic register, the reading of a
revision to a scratch repository, and the live register to an empty difference with
itself.
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

import pytest
import yaml

from devtools import render_stack_results, significance
from devtools.render_stack_results import (
    Facts,
    Snapshot,
    change,
    changed,
    load_snapshot,
    render,
)

Record = dict[str, Any]
SCRATCH_GIT = (
    "-c",
    "user.name=Stack Renderer Test",
    "-c",
    "user.email=stack-test@example.invalid",
    "-c",
    "commit.gpgsign=false",
    "-c",
    "core.hooksPath=/dev/null",
)
SOURCES = {"[Daniel]": {"key": "[Daniel]", "authors": ["Evan Daniel"], "credit": "Daniel"}}
EVIDENCE = {
    "E-replay": {"id": "E-replay", "replay_status": "passed"},
    "E-report": {"id": "E-report"},
}


def result(rid: str, rungs: str = "V3/C3", score: int = 3, **more: Any) -> Record:
    verification, confirmation = rungs.split("/")
    return {
        "id": rid,
        "kind": "lower-bound",
        "headline": "`s(10) ≥ 3`",
        "claim": "s(10) >= 3.",
        "scope": {"n_values": [10]},
        "verification": verification,
        "confirmation": confirmation,
        "significance": {"score": score},
        "evidence": ["E-replay"] if confirmation == "C3" else ["E-report"],
        **more,
    }


def case(n: int, status: str = "open", lower: str = "3", evidence: str = "E-replay") -> Record:
    return {
        "n": n,
        "status": status,
        "reported_status": status,
        "verified_lower_bound": {"value": lower, "evidence": [evidence]},
        "verified_upper_bound": {"value": "4"},
    }


def snapshot(commit: str, results: list[Record], cases: list[Record]) -> Snapshot:
    return Snapshot(
        commit=commit * 40,
        results={record["id"]: record for record in results},
        evidence=EVIDENCE,
        sources=SOURCES,
        cases={record["n"]: record for record in cases},
    )


def facts(**more: Any) -> Facts:
    fields: dict[str, Any] = {
        "kind": "lower bound",
        "credit": "Levy",
        "verification": "V0",
        "confirmation": "C1",
        "significance": 2,
        "status": "reviewed",
        "headline": "`s(10) ≥ 3`",
    }
    return Facts(**{**fields, **more})


def test_change_names_every_moved_field_and_nothing_else() -> None:
    before = facts()
    assert change(None, before) == "new"
    assert change(before, before) == ""
    after = facts(
        kind="optimality",
        credit="Levy after Daniel",
        verification="V3",
        confirmation="C3",
        significance=3,
        status="confirmed",
        headline="`s(10) = 3`",
    )
    assert change(before, after) == (
        "V0→V3, C1→C3, S2→S3, reviewed→confirmed, kind lower bound→optimality, "
        "credit Levy→Levy after Daniel, headline"
    )


def test_changed_keeps_new_and_moved_results_in_results_md_order() -> None:
    base = snapshot(
        "a",
        [result("T-001"), result("T-002", "V0/C1"), result("T-005", builds_on={"credit": []})],
        [],
    )
    head = snapshot(
        "b",
        [
            result("T-001"),
            result("T-002"),
            result("T-003", score=4),
            result("T-004", "V0/C1", score=2),
            result("T-005", builds_on={"credit": ["Daniel"]}),
        ],
        [],
    )
    rows = changed(base, head)
    assert [(record["id"], moved) for record, _, moved in rows] == [
        ("T-003", "new"),
        ("T-002", "V0→V3, C1→C3, reviewed→confirmed"),
        ("T-005", "credit Levy→Levy after Daniel"),
        ("T-004", "new"),
    ]
    attributed = result("T-006", attribution={"source_keys": ["[Daniel]"]})
    assert render_stack_results.facts(attributed, head).credit == "Daniel"


def test_render_counts_the_frontier_and_the_rungs_in_the_rubric_s_words() -> None:
    base = snapshot(
        "a",
        [result("T-001", "V0/C1")],
        [case(10), case(11, evidence="E-nagamochi-lower"), case(12, lower="8")],
    )
    head = snapshot(
        "b",
        [result("T-001"), result("T-002", "V0/C1", score=4)],
        [case(10, "proved", lower="4"), case(11), case(12, lower="8.0")],
    )
    text = render(base, head, "origin/main", "top")
    assert "`bbbbbbbbb` (`top`) against `aaaaaaaaa` (`origin/main`)" in text
    assert "| `T-002` | 10 | lower bound | Levy | `V0` | `C1` | `S4` | reviewed |" in text
    assert "| Proved, verified lane | 0 | 1 |" in text
    assert "| Open with only Nagamochi's lower bound | 1 | 0 |" in text
    assert "- Proved at the head and open at the base (verified lane): 10." in text
    # `8` and `8.0` are one value, so n = 12 has not moved.
    assert "- `verified_lower_bound` value changed at 1 case: 10." in text
    assert "- `verified_upper_bound` value changed at 0 cases: none." in text
    assert "2 results changed: 1 new, 1 moved." in text
    assert "| `V0` | 1 |  | 1 |" in text
    assert f"- `S4`: {significance.anchor_for(4)}." in text
    assert f"- `C3`: {significance.anchors('C')[3]}." in text


def test_render_says_so_when_nothing_moved_or_a_result_left() -> None:
    base = snapshot("a", [result("T-001"), result("T-002")], [case(10)])
    head = snapshot("b", [result("T-001")], [case(10)])
    text = render(base, head, "base", "head")
    assert "No result is new or moved." in text
    assert "In the register at the base and not at the head: T-002." in text
    assert "results changed" not in text


def _git(repository: Path, *arguments: str) -> None:
    subprocess.run(("git", "-C", str(repository), *SCRATCH_GIT, *arguments), check=True)


def _write(repository: Path, path: str, document: object) -> None:
    target = repository / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(yaml.safe_dump(document, allow_unicode=True), encoding="utf-8")


def test_load_snapshot_reads_each_revision_from_git(tmp_path: Path) -> None:
    _git(tmp_path, "init", "-q")
    _write(tmp_path, "packing/frontier/results.yaml", {"results": [result("T-001", "V0/C1")]})
    _write(tmp_path, "packing/frontier/evidence.yaml", {"evidence": list(EVIDENCE.values())})
    _write(tmp_path, "packing/resources/bibliography.yaml", {"sources": list(SOURCES.values())})
    front = yaml.safe_dump({"packing": case(10)})
    (tmp_path / "packing/frontier/n-010.md").write_text(f"---\n{front}---\n# s(10)\n")
    _git(tmp_path, "add", "--all")
    _git(tmp_path, "commit", "-q", "-m", "base")
    _write(tmp_path, "packing/frontier/results.yaml", {"results": [result("T-001")]})
    _git(tmp_path, "commit", "-q", "-am", "head")

    base = load_snapshot("HEAD~1", tmp_path)
    head = load_snapshot("HEAD", tmp_path)
    assert base.cases[10]["status"] == "open"
    assert base.results["T-001"]["verification"] == "V0"
    assert [moved for _, _, moved in changed(base, head)] == [
        "V0→V3, C1→C3, reviewed→confirmed"
    ]

    with pytest.raises(ValueError, match="names no commit"):
        load_snapshot("no-such-ref", tmp_path)
    _git(tmp_path, "rm", "-q", "packing/resources/bibliography.yaml")
    _git(tmp_path, "commit", "-q", "-m", "drop the bibliography")
    with pytest.raises(ValueError, match=r"bibliography\.yaml does not exist"):
        load_snapshot("HEAD", tmp_path)


def test_the_live_register_renders_against_itself(capsys: pytest.CaptureFixture[str]) -> None:
    assert render_stack_results.main(["--base", "HEAD", "--head", "HEAD"]) == 0
    out = capsys.readouterr().out
    assert "No result is new or moved." in out
    assert "| Cases |" in out
