"""Boundary and complete-feature controls for the fixed-T local consumer."""

from __future__ import annotations

import json
from dataclasses import replace
from fractions import Fraction
from pathlib import Path

import pytest

from cases.trump11 import isolation_radius
from devtools import check_n11_optimality_local_isolation as local


def test_strict_taylor_margins_reject_equality() -> None:
    assert local.strict_feature_margin(Fraction(-3), Fraction(1), Fraction(2)) == 1
    with pytest.raises(ValueError, match="may activate"):
        local.strict_feature_margin(Fraction(-2), Fraction(1), Fraction(2))
    assert local.strict_dual_margin(
        Fraction(2), Fraction(1, 4), Fraction(2), Fraction(1)
    ) == Fraction(1, 3)
    with pytest.raises(ValueError, match="dual margin"):
        local.strict_dual_margin(Fraction(2), Fraction(1, 4), Fraction(2), Fraction(3))


def test_exact_radical_upper_control() -> None:
    assert local.radical_upper(Fraction(1)) == 1
    assert local.radical_upper(Fraction(2)) ** 2 > 2
    with pytest.raises(ValueError, match="radicand"):
        local.radical_upper(Fraction(-1))


def test_feature_to_branch_bridge_rejects_omission() -> None:
    witness = isolation_radius.load_witness()
    functions = isolation_radius.elementary_functions(witness, Fraction(1, 64))
    _, census = local.bridge_features(witness, functions)
    assert census == {
        "contact_pairs": 14,
        "features": 112,
        "available_features": 24,
        "unavailable_features": 88,
        "raw_selections": 512,
        "derivative_matrices": 128,
    }
    contacts = {contact.pair for contact in witness.contacts}
    omitted = next(
        index
        for index, function in enumerate(functions)
        if function.kind == "pair" and function.subject[:2] in contacts
    )
    with pytest.raises(ValueError, match="corner inventory"):
        local.bridge_features(witness, functions[:omitted] + functions[omitted + 1 :])
    with pytest.raises(ValueError, match="branch bridge"):
        local.bridge_features(replace(witness, branches=witness.branches[:-1]), functions)


def test_retained_full_and_partial_scope_boundary() -> None:
    receipt = (
        Path(__file__).parents[1]
        / "resources/web/n11-optimality-2026-09-29/receipts/local-isolation"
    )
    full = json.loads((receipt / "result.json").read_text())
    partial = json.loads((receipt / "partial-result.json").read_text())
    assert full["checker_sha256"] == partial["checker_sha256"]
    assert full["input_sha256"] == partial["input_sha256"]
    assert full["status"] == "PASS_INDEPENDENT_FIXED_T_LOCAL_ISOLATION"
    assert full["fixed_T_local_isolation_proved"] is True
    assert full["signed_coordinate_margins_checked"] == 8448
    assert full["unavailable_feature_margins_checked"] == 88
    assert partial["status"] == "INCOMPLETE_FIXED_T_LOCAL_ISOLATION"
    assert partial["fixed_T_local_isolation_proved"] is False
    assert partial["checked_branches"] == [0]
    assert partial["signed_coordinate_margins_checked"] == 66
    assert full["pose_inclusion_proved"] is False
    assert full["case_438_capture_proved"] is False
    assert full["global_optimality_proved"] is False
