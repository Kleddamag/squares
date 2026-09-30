"""Admission and refusal controls for the fresh derivative-frontier instrument."""

from __future__ import annotations

import copy
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from benchmarks import bench_rectangle_derivative_frontier as bench
from devtools import rectangle_derivative_bound as gradient
from sqpack import rectangle_density as density


def _candidate() -> density.RectangleDensityCandidate:
    return density.RectangleDensityCandidate(
        11, Fraction(381, 100), Fraction(1), bench.EFFECTIVE_CUTOFF, None, Fraction(1), ()
    )


def _report(candidate_sha: str, checker_sha: str) -> dict[str, Any]:
    candidate = _candidate()
    return {
        "status": "INCONCLUSIVE",
        "candidate_sha256": candidate_sha,
        "checker_source_sha256": checker_sha,
        "checker": "sqpack.rectangle_density:native-exact-v2",
        "n": 11,
        "L": str(candidate.side),
        "B": str(candidate.core_side),
        "mass": str(candidate.mass),
        "threshold": str(bench.EFFECTIVE_CUTOFF),
        "bound_mode": "common-core",
        "requested_angle_count": 1,
        "angle_count": 1,
        "max_nodes_per_angle": 1000,
        "max_depth": 48,
        "max_seconds": 30.0,
        "retain_pending_boxes": True,
        "angles": [
            {
                "index": 1,
                "status": "INCONCLUSIVE",
                "nodes": 1000,
                "accepted_leaves": 0,
                "unresolved_leaves": 1,
                "stop_cause": "node_limit",
                "pending_boxes": [
                    density.PendingBox(
                        1, Fraction(2), Fraction(2), Fraction(2), Fraction(2), 4, "node_limit"
                    ).as_dict()
                ],
            }
        ],
    }


def _admit(report: dict[str, Any]) -> tuple[density.PendingBox, ...]:
    return bench._admit_frontier(  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
        report, _candidate(), candidate_sha="candidate", checker_sha="checker"
    )


def test_fixed_frontier_admits_complete_exact_inventory() -> None:
    boxes = _admit(_report("candidate", "checker"))
    assert len(boxes) == 1
    assert (
        boxes[0].as_dict() == _report("candidate", "checker")["angles"][0]["pending_boxes"][0]
    )


@pytest.mark.parametrize(
    ("path", "value", "message"),
    [
        (("requested_angle_count",), True, "field type"),
        (("angles", 0, "index"), True, "frontier did not complete"),
        (("angles", 0, "nodes"), True, "frontier did not complete"),
        (("angles", 0, "unresolved_leaves"), True, "frontier did not complete"),
        (("angles", 0, "pending_boxes", 0, "angle"), True, "metadata differs"),
        (("angles", 0, "pending_boxes", 0, "left"), "1/0", "not a rational"),
        (("angles", 0, "pending_boxes", 0, "left"), {}, "rational string"),
        (("angles", 0, "pending_boxes", 0, "depth"), True, "metadata differs"),
    ],
)
def test_malformed_or_boolean_frontier_fields_refuse(
    path: tuple[str | int, ...], value: object, message: str
) -> None:
    report = _report("candidate", "checker")
    target: Any = report
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    with pytest.raises(ValueError, match=message):
        _admit(report)


def test_duplicate_geometry_refuses_even_when_depth_differs() -> None:
    report = _report("candidate", "checker")
    first = report["angles"][0]["pending_boxes"][0]
    duplicate = {**first, "depth": 5}
    report["angles"][0]["pending_boxes"] = [first, duplicate]
    report["angles"][0]["unresolved_leaves"] = 2
    with pytest.raises(ValueError, match="duplicate pending box"):
        _admit(report)


def _run_mocked(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    *,
    report_change: dict[str, Any] | None = None,
    timed_out: bool = False,
) -> tuple[int, Path, list[str]]:
    source = (
        bench.PACKING / "resources/web/wand125-tools-2026-09-29/native-analytic-control.json"
    )
    candidate_sha = hashlib.sha256(source.read_bytes()).hexdigest()
    checker_sha = hashlib.sha256(Path(density.__file__).read_bytes()).hexdigest()
    report = _report(candidate_sha, checker_sha)
    if report_change is not None:
        if report_change == {"internal_timeout": True}:
            report["angles"][0]["stop_cause"] = "time_limit"
        else:
            report.update(report_change)
    out = tmp_path / "frontier"
    monkeypatch.setattr(
        bench,
        "_parse",
        lambda: SimpleNamespace(
            candidate=source,
            candidate_sha256=candidate_sha,
            out=out,
            frontier_outer_seconds=40.0,
            diagnostic_seconds=120.0,
        ),
    )
    monkeypatch.setattr(density, "load_candidate_bytes", lambda *_args, **_kwargs: _candidate())
    commands: list[str] = []

    def command(
        argv: list[str], *, cwd: Path, timeout: float
    ) -> tuple[dict[str, object], str, str]:
        assert cwd == bench.PACKING
        assert timeout == 40.0
        commands.extend(argv)
        return (
            {"timed_out": timed_out, "exit_code": 2, "wall_seconds": 0.01},
            json.dumps(report),
            "",
        )

    monkeypatch.setattr(bench.supervisor, "run_command", command)
    monkeypatch.setattr(
        gradient,
        "build_signed_edges",
        lambda *_args, **_kwargs: gradient.DerivativeEdges((), ()),
    )
    monkeypatch.setattr(
        gradient,
        "bound_pending",
        lambda *_args, **_kwargs: gradient.BoxBound(
            Fraction(),
            Fraction(2),
            gradient.Interval(Fraction(), Fraction()),
            gradient.Interval(Fraction(), Fraction()),
            Fraction(2),
            Fraction(2),
        ),
    )
    return bench.main(), out, commands


def test_cli_runs_fixed_frontier_and_binds_helper_source(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    status, out, command = _run_mocked(tmp_path, monkeypatch)
    assert status == 0
    assert command[1:3] == ["-m", "devtools.verify_rectangle_density"]
    for flag in ("--angles", "--max-nodes-per-angle", "--retain-pending-boxes", "--timing"):
        assert flag in command
    result = json.loads((out / "result.json").read_text())
    assert result["status"] == "DIAGNOSTIC_ONLY"
    assert result["proof_credit"] is False
    assert result["pending_boxes"] == result["evaluated_boxes"] == 1
    assert result["newly_closed_boxes"] == 1
    assert result["comparisons"][0]["closed_by_combined_bound"] is True
    assert "closed_by_new_bound" not in result["comparisons"][0]
    assert (
        result["sources_sha256"]["pending_inventory"]
        == hashlib.sha256(Path(bench.inventory.__file__).read_bytes()).hexdigest()
    )
    assert (
        result["sources_sha256"]["supervisor"]
        == hashlib.sha256(Path(bench.supervisor.__file__).read_bytes()).hexdigest()
    )
    assert len(result["git_head"]) == 40
    assert type(result["git_dirty_at_start"]) is bool
    assert result["total_wall_seconds"] >= result["diagnostic_wall_seconds"]
    assert result["diagnostic_wall_seconds"] >= 0


@pytest.mark.parametrize(
    ("report_change", "timed_out", "expected"),
    [
        ({"candidate_sha256": "wrong"}, False, "REFUSED"),
        (None, True, "INCOMPLETE"),
        ({"internal_timeout": True}, False, "INCOMPLETE"),
    ],
)
def test_cli_separates_refusal_from_incomplete_deadline(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    report_change: dict[str, Any] | None,
    expected: str,
    *,
    timed_out: bool,
) -> None:
    status, out, _ = _run_mocked(
        tmp_path, monkeypatch, report_change=copy.deepcopy(report_change), timed_out=timed_out
    )
    assert status == 2
    result = json.loads((out / "result.json").read_text())
    assert result["status"] == expected
    assert result["proof_credit"] is False
    assert result["total_wall_seconds"] >= 0
