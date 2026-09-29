"""Independent exact checks for rectangle-density certificates."""

from __future__ import annotations

import json
from dataclasses import replace
from fractions import Fraction
from pathlib import Path

import pytest

from devtools import verify_rectangle_density as cli
from sqpack.rectangle_density import (
    CandidateError,
    exact_intersection_area,
    load_candidate,
    parse_candidate,
    square_polygon,
    verify_candidate,
)


def _candidate(*, weight: str = "1683003/625000") -> dict[str, object]:
    return {
        "n": 3,
        "L": "3/2",
        "B": "9977/10000",
        "rhs": "1001/1000",
        "rectangles": [["1/1000", "1/1000", "1499/1000", "1499/1000"]],
        "weights": [weight],
    }


def test_exact_clipping_handles_containment_halving_and_tangency() -> None:
    polygon = square_polygon(
        Fraction(0), Fraction(0), Fraction(3, 5), Fraction(4, 5), Fraction(1)
    )
    assert exact_intersection_area((-1, -1, 1, 1), polygon) == 1
    assert exact_intersection_area((0, -1, 1, 1), polygon) == Fraction(1, 2)
    assert exact_intersection_area((Fraction(7, 10), -1, 1, 1), polygon) == 0


def test_small_analytic_density_proves_every_net_angle() -> None:
    candidate = parse_candidate(_candidate(), n=3, expected_side=Fraction(3, 2))
    assert candidate.mass == Fraction(1683003, 625000)
    assert len(candidate.rectangles) == 1

    report = verify_candidate(candidate, max_nodes_per_angle=10_000, max_depth=20)

    assert report.status == "VERIFIED"
    assert len(report.angles) == 201
    assert all(angle.status == "VERIFIED" for angle in report.angles)


def test_selected_angles_and_resource_limits_never_become_full_verification() -> None:
    candidate = parse_candidate(_candidate(), n=3)

    selected = verify_candidate(candidate, angle_indices=(0, 1, 200))
    capped = verify_candidate(candidate, angle_indices=(1,), max_nodes_per_angle=0)
    timed_out = verify_candidate(candidate, angle_indices=(0,), max_seconds=0)

    assert selected.status == "PARTIAL"
    assert capped.status == "INCONCLUSIVE"
    assert capped.angles[0].status == "INCONCLUSIVE"
    assert timed_out.status == "INCONCLUSIVE"
    assert timed_out.angles[0].lower_bound == 0


def test_exact_point_below_target_is_a_certificate_counterexample() -> None:
    candidate = parse_candidate(_candidate(weight="1683003/62500000"), n=3)

    report = verify_candidate(candidate, angle_indices=(0,))

    assert report.status == "COUNTEREXAMPLE"
    assert report.angles[0].counterexample is not None


def test_loader_preserves_decimal_rationals_and_rejects_malformed_candidates(
    tmp_path: Path,
) -> None:
    path = tmp_path / "candidate.json"
    path.write_text(
        '{"n":3,"L":1.5,"B":0.9977,"rectangles":'
        '[[0.001,0.001,1.499,1.499]],"weights":[2.6928048]}'
    )
    candidate = load_candidate(path, n=3)
    assert candidate.side == Fraction(3, 2)
    assert candidate.mass == Fraction(1683003, 625000)

    bad = {
        "duplicate": '{"n":3,"n":3,"L":1.5,"B":0.9977,"rectangles":[],"weights":[]}',
        "wrong n": json.dumps(_candidate() | {"n": 4}),
        "negative": json.dumps(_candidate(weight="-1")),
        "outside": json.dumps(
            _candidate() | {"rectangles": [["0", "1/1000", "1499/1000", "1499/1000"]]}
        ),
    }
    for name, text in bad.items():
        path = tmp_path / f"{name}.json"
        path.write_text(text)
        try:
            load_candidate(path, n=3)
        except CandidateError:
            pass
        else:
            raise AssertionError(f"malformed candidate accepted: {name}")


def test_direct_construction_and_noninteger_parameters_cannot_bypass_admission() -> None:
    candidate = parse_candidate(_candidate(), n=3)

    for changed in (replace(candidate, n=1), replace(candidate, mass=Fraction())):
        with pytest.raises(CandidateError):
            verify_candidate(changed, angle_indices=(0,))
    with pytest.raises(CandidateError):
        parse_candidate(_candidate() | {"n": None}, n=3.5)  # type: ignore[arg-type]
    with pytest.raises(CandidateError):
        verify_candidate(candidate, angle_indices=(1.5,))  # type: ignore[arg-type]
    with pytest.raises(CandidateError):
        verify_candidate(candidate, angle_indices=(0,), max_seconds=float("nan"))
    with pytest.raises(CandidateError):
        parse_candidate(_candidate() | {"angle_count": 200}, n=3)


def test_retained_tokoharu_candidate_loads_and_bounded_probe_refuses_to_promote() -> None:
    path = (
        Path(__file__).parents[1]
        / "resources/web/external-square-certificates-2026-09-22/tokoharu-density"
        / "certificates/cert_n11_L381/certified_candidate.json"
    )
    candidate = load_candidate(path, n=11, expected_side=Fraction(381, 100))

    report = verify_candidate(candidate, angle_indices=(1,), max_nodes_per_angle=0)

    assert candidate.mass < 11
    assert report.status == "INCONCLUSIVE"


def test_retained_scaled_admission_counterexample_is_rejected() -> None:
    path = (
        Path(__file__).parents[1]
        / "resources/web/wand125-tools-2026-09-29/receipts/admission-scaled.json"
    )

    with pytest.raises(CandidateError, match="mass"):
        load_candidate(path, n=1, expected_side=Fraction(3, 2))


def test_cli_reports_partial_selection_without_a_passing_exit(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "candidate.json"
    path.write_text(json.dumps(_candidate()))

    status = cli.main([str(path), "--n", "3", "--angles", "0,1"])

    output = json.loads(capsys.readouterr().out)
    assert status == 2
    assert output["status"] == "PARTIAL"
