"""Synthetic exact controls for the H-255 producer; no target source is loaded."""

from __future__ import annotations

import json
from fractions import Fraction as Q

import pytest

from devtools.check_n17_root_certificate import (
    check_quantities,
    domain_intervals,
    n17_polynomials,
)
from devtools.make_n17_root_certificate import (
    Interval,
    Polynomial,
    certify,
    fixed_domain,
    fixed_polynomials,
)


def test_interval_product_powers_and_input_refusals() -> None:
    assert (Interval(Q(-2), Q(3)) * Interval(Q(-5), Q(-1))).as_json() == ["-15", "10"]
    assert (Interval(Q(-2), Q(3)) ** 2).as_json() == ["0", "9"]
    invalid_boolean = True
    for lower, upper in ((Q(2), Q(1)), (invalid_boolean, Q(1)), (0.0, Q(1))):
        with pytest.raises(ValueError, match="ordered exact Fractions"):
            Interval(lower, upper)  # type: ignore[arg-type]


def test_fixed_polynomials_match_source_formulas_and_independent_coefficients() -> None:
    t, b = Q(1, 3), Q(1, 5)
    d, e, ell = 1 + t * t, 1 + b * b, (1 + t) * (1 + t * t)
    n_alpha = (1 - t * t) * (1 - b * b) - 4 * t * b
    expected = (
        2 * t * (1 - t) * (1 - b * b) + (1 - t) ** 2 * ell * b - t * ell * e,
        (1 - t * t) * d * e * e
        - (1 + t) * d * e * (b * (1 - t * t) + t * (1 - b * b))
        - (1 - t) * (1 - b * b) * n_alpha,
    )
    polynomials = fixed_polynomials()
    assert tuple(poly.evaluate(t, b) for poly in polynomials) == expected
    assert all(value.denominator == 1 for poly in polynomials for value in poly.terms.values())
    assert [poly.as_json() for poly in polynomials] == [
        [[i, j, str(coefficient)] for (i, j), coefficient in sorted(poly.items())]
        for poly in n17_polynomials()
    ]


def test_nontrivial_exact_krawczyk_control_crosses_json_boundary() -> None:
    x, y = Polynomial.variable(0), Polynomial.variable(1)
    result = certify((x * x + 2 * y - 3, 3 * x + y * y - 4), (Q(101, 100), Q(1)), Q(1, 50))
    assert result["criterion_passed"] is True
    assert result["C"] == [["-50/49", "50/49"], ["75/49", "-101/98"]]
    assert result["correction"] == ["99/9800", "-3/19600"]
    assert result["row_norms"] == ["4/49", "251/2450"]
    assert result["inclusion_bounds"] == ["23/1960", "1079/490000"]
    assert result["q"] == "251/2450"
    independent = check_quantities(
        json.loads(json.dumps(result)),
        (
            {(2, 0): 1, (0, 1): 2, (0, 0): -3},
            {(1, 0): 3, (0, 2): 1, (0, 0): -4},
        ),
        (Q(101, 100), Q(1)),
        Q(1, 50),
    )
    assert independent["q"] == result["q"]


def test_outside_boundary_singular_and_two_root_controls() -> None:
    x, y = Polynomial.variable(0), Polynomial.variable(1)
    origin, radius = (Q(0), Q(0)), Q(1)
    outside = certify((x - 2, y), origin, radius)
    assert outside["criterion_passed"] is False
    assert "inclusion.0" in outside["failures"]
    boundary = certify((x - 1, y), origin, radius)
    assert boundary["criterion_passed"] is False
    assert boundary["inclusion_bounds"][0] == "1"
    with pytest.raises(ValueError, match="singular"):
        certify((x * x, y), origin, radius)
    wide = certify((x * x - 1, y), (Q(1, 2), Q(0)), Q(2))
    assert wide["criterion_passed"] is False
    assert "contraction" in wide["failures"]


def test_malformed_dimensions_midpoint_radius_and_domain() -> None:
    x, y = Polynomial.variable(0), Polynomial.variable(1)
    invalid_boolean = True
    for midpoint, radius in (
        ((Q(0), Q(0)), Q(0)),
        ((Q(0), Q(0)), invalid_boolean),
        ((Q(0),), Q(1)),
    ):
        with pytest.raises(ValueError, match="rho>0"):
            certify((x, y), midpoint, radius)  # type: ignore[arg-type]
    for malformed in (0.5, invalid_boolean):
        with pytest.raises(ValueError, match="exact integers or Fractions"):
            Polynomial.constant(malformed)  # type: ignore[arg-type]
    _, failures = fixed_domain((Q(0), Q(0)), Q(1, 10**12))
    assert {"domain.t", "domain.b", "denominator.t"} <= set(failures)
    synthetic_midpoint = (Q(365, 1000), Q(335, 1000))
    domain, _ = fixed_domain(synthetic_midpoint, Q(1, 10**12))
    assert domain == domain_intervals(synthetic_midpoint, Q(1, 10**12))
