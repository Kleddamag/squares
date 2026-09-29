"""Exact controls for the bounded two-level rectangle frontier diagnostic."""

# The control directly exercises private exact primitives of the verifier and diagnostic.
# ruff: noqa: SLF001

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import replace
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import refine_rectangle_density_frontier as refinement
from sqpack import rectangle_density as density


def _candidate_data() -> dict[str, object]:
    return {
        "n": 65,
        "L": "4",
        "B": "1/2",
        "rectangles": [["1", "1", "3", "3"]],
        "weights": ["64"],
    }


def _local_bound(
    candidate: density.RectangleDensityCandidate,
    box: density.PendingBox,
) -> Fraction:
    centre = density._CentreBox(  # pyright: ignore[reportPrivateUsage]
        box.left, box.bottom, box.right, box.top, box.depth
    )
    polygon = density._common_core(  # pyright: ignore[reportPrivateUsage]
        candidate, centre, Fraction(4, 5), Fraction(3, 5)
    )
    return sum(
        (
            rectangle.density
            * density.exact_intersection_area(rectangle, polygon)
            for rectangle in candidate.rectangles
        ),
        Fraction(),
    )


def test_analytic_two_level_partition_and_bounds(monkeypatch: pytest.MonkeyPatch) -> None:
    candidate = density.parse_candidate(_candidate_data(), n=65)
    parent = density.PendingBox(
        1, Fraction(15, 8), Fraction(15, 8), Fraction(17, 8), Fraction(17, 8), 0,
        "depth_limit",
    )
    children = refinement._four_children(parent)  # pyright: ignore[reportPrivateUsage]

    assert candidate.mass == 64 < candidate.n
    assert len(candidate.rectangles) == 1
    assert candidate.rectangles[0].density == 16
    assert len(children) == 4
    assert all(child.depth == 2 for child in children)
    assert _local_bound(candidate, parent) == Fraction(9, 25)
    assert [_local_bound(candidate, child) for child in children] == [
        Fraction(169, 100)
    ] * 4

    # Drive the real parent/child aggregation with the exact local rotation.
    # Only the angle lookup is injected; clipping and all four bounds stay exact.
    monkeypatch.setattr(density, "_angle", lambda _index: (Fraction(4, 5), Fraction(3, 5)))
    row = refinement._refine_parent(  # pyright: ignore[reportPrivateUsage]
        candidate, parent, deadline=time.monotonic() + 10
    )
    assert row["complete"] is True
    assert row["parent_bound"] == "9/25"
    assert [child["bound"] for child in row["children"]] == ["169/100"] * 4
    assert row["all_children_closed"] is True


@pytest.fixture
def synthetic_frontier(tmp_path: Path) -> tuple[Path, Path]:
    candidate_path = tmp_path / "candidate.json"
    candidate_bytes = json.dumps(_candidate_data()).encode()
    candidate_path.write_bytes(candidate_bytes)
    candidate = density.load_candidate_bytes(candidate_bytes, n=65)
    report = density.verify_candidate(
        candidate,
        angle_indices=(1,),
        max_nodes_per_angle=1,
        max_depth=0,
        max_seconds=30,
        retain_pending_boxes=True,
    )
    assert report.status == "INCONCLUSIVE"
    assert report.angles[0].pending_boxes is not None
    assert len(report.angles[0].pending_boxes) == 1
    receipt = report.as_dict() | {
        "candidate": str(candidate_path),
        "candidate_sha256": hashlib.sha256(candidate_bytes).hexdigest(),
        "checker": "sqpack.rectangle_density:native-exact-v2",
        "checker_source_sha256": hashlib.sha256(
            Path(density.__file__).read_bytes()
        ).hexdigest(),
    }
    receipt_path = tmp_path / "frontier.json"
    receipt_path.write_text(json.dumps(receipt))
    return candidate_path, receipt_path


def _argv(candidate_path: Path, receipt_path: Path) -> list[str]:
    return [
        str(candidate_path),
        "--frontier-receipt", str(receipt_path),
        "--n", "65",
        "--max-nodes-per-angle", "1",
        "--max-depth", "0",
        "--expected-pending-boxes", "1",
        "--expected-depth-leaves", "1",
    ]


def test_public_diagnostic_retains_complete_parent_child_census(
    synthetic_frontier: tuple[Path, Path], capsys: pytest.CaptureFixture[str]
) -> None:
    status = refinement.main(_argv(*synthetic_frontier))
    output = json.loads(capsys.readouterr().out)

    assert status == 0
    assert output["status"] == "DIAGNOSTIC_ONLY"
    assert output["frontier_complete"] is True
    assert output["selected_parents"] == output["processed_parents"] == 1
    assert output["expected_children"] == output["evaluated_children"] == 4
    assert len(output["refinements"]) == 1
    assert len(output["refinements"][0]["children"]) == 4
    assert output["refinements"][0]["complete"] is True
    assert output["frontier"]["pending_boxes"][0] == output["refinements"][0]["parent"]
    assert all(
        Fraction(child["bound"]) >= Fraction(output["refinements"][0]["parent_bound"])
        for child in output["refinements"][0]["children"]
    )


@pytest.mark.parametrize("tamper", ["source", "census"])
def test_stale_source_and_malformed_census_refuse(
    synthetic_frontier: tuple[Path, Path],
    capsys: pytest.CaptureFixture[str],
    tamper: str,
) -> None:
    candidate_path, receipt_path = synthetic_frontier
    receipt: dict[str, Any] = json.loads(receipt_path.read_text())
    if tamper == "source":
        receipt["checker_source_sha256"] = "0" * 64
    else:
        receipt["angles"][0]["pending_boxes"] = []
    receipt_path.write_text(json.dumps(receipt))

    assert refinement.main(_argv(candidate_path, receipt_path)) == 1
    assert json.loads(capsys.readouterr().out)["status"] == "REFUSED"


def test_timeout_keeps_current_parent_incomplete(
    synthetic_frontier: tuple[Path, Path],
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    real_bound = refinement._bound_before_deadline  # pyright: ignore[reportPrivateUsage]
    calls = 0

    def expire_after_first_child(
        candidate: density.RectangleDensityCandidate,
        box: density.PendingBox,
        deadline: float,
    ) -> Fraction:
        nonlocal calls
        calls += 1
        if calls == 3:
            raise refinement._DiagnosticDeadlineError  # pyright: ignore[reportPrivateUsage]
        return real_bound(candidate, box, deadline)

    monkeypatch.setattr(refinement, "_bound_before_deadline", expire_after_first_child)
    assert refinement.main(_argv(*synthetic_frontier)) == 2
    output = json.loads(capsys.readouterr().out)
    assert output["status"] == "PARTIAL_DIAGNOSTIC"
    assert output["frontier_complete"] is True
    assert output["expected_parents"] == 1
    assert output["expected_children"] == 4
    assert output["processed_parents"] == 0
    assert output["evaluated_children"] == 1
    assert len(output["incomplete_parent"]["children"]) == 1
    assert output["incomplete_parent"]["complete"] is False


def test_missing_child_partition_refuses(
    synthetic_frontier: tuple[Path, Path],
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original = refinement._four_children  # pyright: ignore[reportPrivateUsage]
    monkeypatch.setattr(refinement, "_four_children", lambda parent: original(parent)[:3])

    assert refinement.main(_argv(*synthetic_frontier)) == 1
    output = json.loads(capsys.readouterr().out)
    assert output["status"] == "REFUSED"
    assert "missing a child bound" in output["error"]


def test_vacuous_zero_census_refuses(
    synthetic_frontier: tuple[Path, Path], capsys: pytest.CaptureFixture[str]
) -> None:
    assert refinement.main([*_argv(*synthetic_frontier), "--expected-depth-leaves", "0"]) == 1
    assert json.loads(capsys.readouterr().out)["status"] == "REFUSED"


def test_receipt_size_limit_refuses_before_json_decode(
    synthetic_frontier: tuple[Path, Path], capsys: pytest.CaptureFixture[str]
) -> None:
    candidate_path, receipt_path = synthetic_frontier
    receipt_path.write_bytes(b"x" * (refinement.MAX_RECEIPT_BYTES + 1))

    assert refinement.main(_argv(candidate_path, receipt_path)) == 1
    output = json.loads(capsys.readouterr().out)
    assert output["status"] == "REFUSED"
    assert "size limit" in output["error"]


def test_comparison_helper_change_during_refinement_refuses(
    synthetic_frontier: tuple[Path, Path],
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    helper = tmp_path / "comparison-helper.py"
    helper.write_bytes(Path(refinement.comparison.__file__).read_bytes())
    monkeypatch.setattr(refinement.comparison, "__file__", str(helper))
    original = refinement.comparison._single_angle  # pyright: ignore[reportPrivateUsage]

    def change_helper(report: density.VerificationReport) -> density.AngleVerification:
        angle = original(report)
        helper.write_text("changed during refinement")
        return angle

    monkeypatch.setattr(refinement.comparison, "_single_angle", change_helper)
    assert refinement.main(_argv(*synthetic_frontier)) == 1
    output = json.loads(capsys.readouterr().out)
    assert output["status"] == "REFUSED"
    assert "comparison tool changed" in output["error"]


def test_replay_timeout_keeps_configured_expected_census(
    synthetic_frontier: tuple[Path, Path],
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original = density.verify_candidate

    def timed_replay(*args: Any, **kwargs: Any) -> density.VerificationReport:
        report = original(*args, **kwargs)
        return replace(
            report,
            angles=(replace(report.angles[0], stop_cause="time_limit"),),
        )

    monkeypatch.setattr(density, "verify_candidate", timed_replay)
    assert refinement.main(_argv(*synthetic_frontier)) == 2
    output = json.loads(capsys.readouterr().out)
    assert output["status"] == "PARTIAL_DIAGNOSTIC"
    assert output["frontier_complete"] is False
    assert output["expected_parents"] == 1
    assert output["expected_children"] == 4
    assert output["selected_parents"] == output["processed_parents"] == 0
    assert output["evaluated_children"] == 0
