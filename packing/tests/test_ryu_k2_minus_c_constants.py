"""The numerical chain of Ryu's k^2 - M(k) >= 0.033 log k, and controls that it refuses."""

from __future__ import annotations

from fractions import Fraction

from cases.asymptotic.ryu_k2_minus_c_constants import check_constants


def _failed(checks: tuple) -> set[str]:
    return {check.name for check in checks if not check.holds}


def test_every_inequality_holds_with_the_computer_assisted_overlap_bound() -> None:
    checks = check_constants(9)
    assert len(checks) == 31
    assert _failed(checks) == set()


def test_every_inequality_holds_with_the_analytic_overlap_bound() -> None:
    checks = check_constants(13)
    assert len(checks) == 28
    assert _failed(checks) == set()


def test_the_stated_limits_and_thresholds() -> None:
    values = {check.name: check.value for check in check_constants(9)}
    limit = values["for k >= 10^13: F(k)/log k > 0.99977/30.147 > 0.033"]
    assert limit.startswith("0.0331631671")
    threshold = Fraction(4 * Fraction("30.147") - Fraction("0.3819"), Fraction("0.99977"))
    assert Fraction("120.2337") < threshold < Fraction("120.2338")
    assert values[next(name for name in values if name.startswith("c = 4:"))].startswith(
        "120.233753"
    )


def test_a_tenth_overlapping_rectangle_breaks_the_stated_constants() -> None:
    failed = _failed(
        check_constants(10, a_bound="10.6067", bracket_bound="30.147", kappa="0.033")
    )
    assert "A = 4 sqrt(10/Q*)/(2 - 3e-6) < 10.6067" in failed


def test_a_larger_bracket_or_kappa_is_refused() -> None:
    assert "bracket with A < 10.6067 is < 30.14" in _failed(
        check_constants(9, bracket_bound="30.14")
    )
    assert "for k >= 10^13: F(k)/log k > 0.99977/30.147 > 0.0332" in _failed(
        check_constants(9, kappa="0.0332")
    )


def test_a_smaller_q_star_is_refused() -> None:
    assert "A = 4 sqrt(9/Q*)/(2 - 3e-6) < 10.6067" in _failed(check_constants(9, q_star="0.31"))
