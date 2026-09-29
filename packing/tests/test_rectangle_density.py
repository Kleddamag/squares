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
    _CentreBox,  # pyright: ignore[reportPrivateUsage]
    _common_core,  # pyright: ignore[reportPrivateUsage]
    coverage_at_point,
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


def test_asymmetric_orbit_and_common_core_have_analytic_oracles() -> None:
    candidate = parse_candidate(
        {
            "n": 2,
            "L": "4",
            "B": "1/2",
            "rectangles": [["9/20", "7/5", "11/20", "8/5"]],
            "weights": ["1"],
        },
        n=2,
    )
    assert len(candidate.rectangles) == 8
    assert candidate.mass == 1
    assert all(rectangle.area == Fraction(1, 50) for rectangle in candidate.rectangles)
    assert all(rectangle.density == Fraction(25, 4) for rectangle in candidate.rectangles)

    # At each centre the core contains exactly one complete orbit rectangle.
    # Its local half-projections are 11/100 and 1/10, both below B/2.
    # Every other image is separated by coordinate range, so the mass is 1/8.
    for x, y in ((1, 3), (5, 1), (7, 5), (3, 7)):
        assert coverage_at_point(
            candidate, Fraction(x, 2), Fraction(y, 2), Fraction(3, 5), Fraction(4, 5)
        ) == Fraction(1, 8)

    # Test the private proof primitive directly against independent containment
    # inequalities, including unequal box widths and unequal sine/cosine.
    box = _CentreBox(Fraction(9, 20), Fraction(7, 5), Fraction(11, 20), Fraction(8, 5), 0)
    cosine, sine = Fraction(3, 5), Fraction(4, 5)
    polygon = _common_core(candidate, box, cosine, sine)
    assert len(polygon) == 4
    assert exact_intersection_area((0, 0, 4, 4), polygon) == Fraction(21, 250)
    lower_bound = sum(
        (
            rectangle.density * exact_intersection_area(rectangle, polygon)
            for rectangle in candidate.rectangles
        ),
        Fraction(),
    )
    assert lower_bound == Fraction(1, 8)
    for x in (box.left, box.right):
        for y in (box.bottom, box.top):
            assert coverage_at_point(candidate, x, y, cosine, sine) == Fraction(1, 8)
            for px, py in polygon:
                assert abs(cosine * (px - x) + sine * (py - y)) <= Fraction(1, 4)
                assert abs(-sine * (px - x) + cosine * (py - y)) <= Fraction(1, 4)


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


@pytest.mark.parametrize(("index", "accepted", "unresolved"), [(0, 2, 6), (1, 0, 1)])
def test_counterexample_receipt_preserves_coverage_accounting(
    index: int, accepted: int, unresolved: int
) -> None:
    candidate = parse_candidate(
        {
            "n": 3,
            "L": "3/2",
            "B": "9977/10000",
            "rectangles": [["3/10", "3/10", "6/5", "6/5"]],
            "weights": ["6/5"],
        },
        n=3,
    )

    report = verify_candidate(
        candidate,
        angle_indices=(index,),
        max_depth=1,
        max_nodes_per_angle=10,
    )

    angle = report.angles[0]
    assert report.status == "COUNTEREXAMPLE"
    assert angle.nodes == 3
    assert angle.accepted_leaves == accepted
    assert angle.unresolved_leaves == unresolved


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
