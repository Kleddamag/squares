"""Exact arithmetic and refusal controls for the partial n=11 dual consumer."""

from __future__ import annotations

import copy
import json
from fractions import Fraction
from pathlib import Path

import pytest

from devtools import check_n11_optimality_local_dual as dual


def test_unique_trump_root_bracket() -> None:
    lo, hi, refinements = dual.root_interval()
    assert Fraction(9, 25) <= lo < hi <= Fraction(37, 100)
    assert dual.polynomial(lo) < 0 < dual.polynomial(hi)
    assert hi - lo <= Fraction(1, 10**80)
    assert refinements > 0


def toy_signed_duals() -> tuple[list[list[int]], list[dict[str, object]]]:
    scale = 100_000
    matrix = [[0] * 33 for _ in range(42)]
    for coordinate in range(33):
        matrix[coordinate][coordinate] = scale
    matrix[33] = [-scale] * 33
    certificates: list[dict[str, object]] = []
    for coordinate in range(33):
        positive = [0] * 42
        positive[coordinate] = 1
        certificates.append(
            {
                "coordinate": coordinate,
                "sign": 1,
                "coefficients": positive,
                "residual_upper": str(Fraction(33, scale)),
            }
        )
        negative = [0] * 42
        negative[33] = 1
        for other in range(33):
            if other != coordinate:
                negative[other] = 1
        certificates.append(
            {
                "coordinate": coordinate,
                "sign": -1,
                "coefficients": negative,
                "residual_upper": str(Fraction(33 * 33, scale)),
            }
        )
    return matrix, certificates


def test_complete_signed_dual_residuals_and_refusals() -> None:
    matrix, certificates = toy_signed_duals()
    assert dual.check_residuals(matrix, certificates, 1, 100_000) == (
        66,
        Fraction(1089, 100_000),
    )
    with pytest.raises(ValueError, match="incomplete"):
        dual.check_residuals(matrix, certificates[:-1], 1, 100_000)
    duplicate = copy.deepcopy(certificates)
    duplicate[1] = duplicate[0]
    with pytest.raises(ValueError, match="duplicate"):
        dual.check_residuals(matrix, duplicate, 1, 100_000)
    negative_weight = copy.deepcopy(certificates)
    negative_weight[0]["coefficients"] = [-1] + [0] * 41
    with pytest.raises(ValueError, match="nonnegative"):
        dual.check_residuals(matrix, negative_weight, 1, 100_000)
    wrong_residual = copy.deepcopy(certificates)
    wrong_residual[0]["residual_upper"] = "0"
    with pytest.raises(ValueError, match="does not equal"):
        dual.check_residuals(matrix, wrong_residual, 1, 100_000)


def test_branch_inventory_and_scales_refuse_missing_or_duplicate_data() -> None:
    branches = [{"branch": index} for index in range(128)]
    assert len(dual.validate_branch_inventory({"branches": branches})) == 128
    with pytest.raises(ValueError, match="incomplete"):
        dual.validate_branch_inventory({"branches": branches[:-1]})
    duplicated = copy.deepcopy(branches)
    duplicated[-1]["branch"] = 0
    with pytest.raises(ValueError, match="incomplete"):
        dual.validate_branch_inventory({"branches": duplicated})
    assert dual.validate_scales(
        {"coefficient_denominator": 10, "matrix_approximation_denominator": 100}
    ) == (10, 100)
    for bad in (0, -1, True):
        with pytest.raises(ValueError, match="coefficient scales"):
            dual.validate_scales(
                {"coefficient_denominator": bad, "matrix_approximation_denominator": 100}
            )


def test_retained_residual_result_does_not_claim_local_isolation() -> None:
    packing = Path(__file__).parents[1]
    result = json.loads(
        (
            packing
            / "resources/web/n11-optimality-2026-09-29/receipts/local-dual-residual/result.json"
        ).read_text()
    )
    assert result["status"] == "INCOMPLETE_LOCAL_DUAL_PROFILE"
    assert result["checked_branches"] == list(range(128))
    assert sum(row["signed_coordinates_checked"] for row in result["branch_results"]) == 8448
    assert "local_isolation_proved" not in result
    assert "global_optimality_proved" not in result
