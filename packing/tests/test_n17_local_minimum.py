"""Exact first-order parts of the n17 local-minimum checker (H-261, BC-407)."""

from __future__ import annotations

import hashlib
import json
from dataclasses import replace
from fractions import Fraction as Q
from functools import cache
from pathlib import Path

import pytest

from devtools import check_n17_local_minimum as local


@cache
def _target() -> local.Model:
    midpoint, _ = local.read_point(local.ROOT_CERTIFICATE.read_bytes())
    return local.build_model(*midpoint)


@cache
def _space() -> local.Quotient:
    return local.quotient(_target())


@cache
def _solved(name: str, sign: int) -> local.DirectionSolution:
    return local.solve_direction(_target(), _space(), name, sign)


def test_six_prescribed_zero_weights_and_52_positive_rows() -> None:
    audit = local.weight_audit(_target())
    assert audit["passed"]
    assert audit["zero_weight_rows"] == sorted(map(local.row_label, local.ZERO_WEIGHT_KEYS))
    assert audit["positive_weight_rows"] == 52
    # The midpoint is not the root: only the two prescribed F2 columns are off zero.
    omega12, omega16 = local.column(12, "angle"), local.column(16, "angle")
    assert set(audit["stress_residual_columns_at_point"]) == {str(omega12), str(omega16)}


def test_coordinates_annihilate_the_sliders_and_number_ninety_directions() -> None:
    model = _target()
    covectors = local.coordinates(model)
    assert len(covectors) == 45
    assert len(local.directions(model)) == 90
    assert model.u[0] ** 2 + model.u[1] ** 2 == 1
    for vector in local.slider_generators(model).values():
        for covector in covectors.values():
            assert sum((covector.get(i, Q(0)) * v for i, v in vector.items()), Q(0)) == 0


def test_kernel_is_exactly_the_slider_span_with_two_lineality_directions() -> None:
    audit = local.kernel_audit(_target())
    assert audit["passed"]
    assert (audit["rank_positive"], audit["kernel_dimension"], audit["rank_all"]) == (46, 6, 50)
    assert (audit["rank_positive_mod_p"], audit["rank_all_mod_p"]) == (46, 50)
    assert audit["lineality_generators"] == ["v13", "xi6"]
    zero_rows = audit["generator_values_on_zero_weight_rows"]
    assert zero_rows["xi5"] == {"wall:5:right:0": "-1", "wall:5:right:1": "-1"}
    assert zero_rows["v11"] == {"pair:9:11:0": "-1", "pair:9:11:1": "-1"}
    assert zero_rows["omega6"] == {"wall:6:bottom:0": "-1/2", "wall:6:bottom:1": "1/2"}


def test_rank_helpers_on_a_known_deficient_matrix() -> None:
    rows = [[Q(1), Q(2), Q(3)], [Q(2), Q(4), Q(6)], [Q(0), Q(1), Q(1, 2)]]
    assert local.exact_rank(rows) == 2
    assert local.modular_rank(rows) == 2


@pytest.mark.parametrize(
    ("name", "sign", "prefix"),
    [
        ("omega11", -1, "175.848328842"),
        ("omega16", -1, "74.1727814434"),
        ("eta16", 1, "12.0116678565"),
        ("xi17", 1, "1"),
        ("xi1", -1, "0"),
    ],
)
def test_selected_coordinate_duals_are_exact_optima(name: str, sign: int, prefix: str) -> None:
    solution = _solved(name, sign)
    assert solution.status == "certified_optimal"
    assert solution.a is not None
    assert local.decimal(solution.a).startswith(prefix)
    assert all(value > 0 for value in solution.lam.values())
    assert set(solution.lam) <= set(_target().positive_keys)
    assert local.verify_solution(_target(), _space(), solution)


def test_tampered_certificates_are_rejected() -> None:
    solution = _solved("omega11", -1)
    assert solution.a is not None
    key = next(iter(solution.lam))
    bumped = {**solution.lam, key: solution.lam[key] + Q(1, 10**9)}
    negated = {**solution.lam, key: -solution.lam[key]}
    for tampered in (
        replace(solution, lam=bumped),
        replace(solution, lam=negated),
        replace(solution, a=solution.a - Q(1, 10**9)),
        replace(solution, sign=1),
        replace(solution, status="undecided"),
    ):
        assert not local.verify_solution(_target(), _space(), tampered)


def test_unavailable_owner_alternatives_are_strictly_negative() -> None:
    audit = local.owner_alternative_audit(_target())
    assert audit["passed"]
    assert audit["unavailable"] == audit["strictly_negative"] == 135
    assert audit["identity_options"] == 33
    assert audit["identity_exact_zero"] == 31
    leading = [row["margin_decimal"][:7] for row in audit["least_negative"][:4]]
    assert leading == ["-0.0557", "-0.0557", "-0.0707", "-0.1474"]
    assert {tuple(row["pair"]) for row in audit["least_negative"][:2]} == {(7, 14), (14, 17)}


def test_kernel_row_control_is_refused() -> None:
    result = local.run_control(_target(), "kernel-row")
    assert result["refused"]
    assert "kernel.kernel_equals_slider_span" in result["failed_checks"]


def test_infeasible_dual_control_keeps_the_kernel_and_loses_the_dual() -> None:
    result = local.run_control(_target(), "infeasible-dual")
    assert result["refused"]
    assert all(result["kernel_checks"].values())
    assert result["direction"]["status"] == "no_nonnegative_dual"
    assert result["failed_checks"] == ["duals.-omega11"]


@pytest.mark.parametrize(
    ("control", "failed"), [("kernel-row", "kernel"), ("infeasible-dual", "duals")]
)
def test_cli_refuses_each_control(
    control: str,
    failed: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    seen: list[bytes] = []
    monkeypatch.setattr(local, "_check_frozen_root_bytes", seen.append)
    output = tmp_path / "receipt.json"
    assert local.main(["--control", control, "--output", str(output)]) == 1
    receipt = json.loads(output.read_text())
    raw = local.ROOT_CERTIFICATE.read_bytes()
    assert seen == [raw]
    assert receipt["passed"] is False
    assert receipt["checks"][failed] is False
    assert receipt["inputs"]["root_certificate_sha256"] == hashlib.sha256(raw).hexdigest()
    assert json.loads(capsys.readouterr().out)["passed"] is False


def test_cli_rejects_unbound_or_malformed_input(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    def reject(_raw: bytes) -> None:
        raise ValueError("root certificate differs from frozen exp-237 Git blob")

    monkeypatch.setattr(local, "_check_frozen_root_bytes", reject)
    assert local.main([]) == 2
    assert "frozen" in json.loads(capsys.readouterr().out)["error"]
    malformed = tmp_path / "root.json"
    malformed.write_text("{}")
    monkeypatch.setattr(local, "_check_frozen_root_bytes", lambda _raw: None)
    assert local.main([str(malformed)]) == 2
    assert json.loads(capsys.readouterr().out)["passed"] is False
