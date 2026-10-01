"""Unready draft of an independent interval audit for the fixed H258 stress recipe.

This instrument is unfinished and has not been accepted or evaluated on H258 target
data. The receipt-binding entry point deliberately refuses every invocation. Its
arithmetic still uses unbounded exact fractions; the approved outward dyadic arithmetic
and synthetic controls remain unimplemented.

Only the independent tuple-interval reconstruction is reused. No producer arithmetic
or symbolic engine is imported. The 52 exact symbolic residual identities are an
explicit reviewed premise; residual intervals are never promoted to exact zero.
Equivalent interval expression orderings may yield different valid enclosures.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from devtools import audit_n17_endpoint_features as features
from devtools import audit_n17_endpoint_receipt as exact

Interval = exact.Interval
Vector = exact.Vector
Row = tuple[Any, ...]
add, sub, mul, div = exact.add, exact.subtract, exact.multiply, exact.divide
neg, point = exact.negate, exact.point
FEATURE_RUN = f"{exact.RESULTS}/exp-239-n17-endpoint-features/run-001"
FEATURE_REF = f"feafdae49:{FEATURE_RUN}/certificate.json"
HALF = point(Fraction(1, 2))
ZERO = point(0)
AXIS_FACES = {(1, 2), (1, 3), (5, 7)}
ZERO_ROWS = {
    ("wall", 5, "right", 0),
    ("wall", 5, "right", 1),
    ("wall", 6, "bottom", 0),
    ("wall", 6, "bottom", 1),
    ("pair", 9, 11, 0),
    ("pair", 9, 11, 1),
}
SMOOTH_OWNERS = {
    (3, 9): 3,
    (4, 10): 10,
    (3, 11): 11,
    (2, 13): 13,
    (10, 15): 10,
    (14, 17): 14,
    (15, 16): 16,
    (16, 8): 16,
    (14, 7): 14,
    (16, 17): 16,
    (12, 16): 12,
}
SUPPORT_SIGNS = {
    (3, 9): (1, 1),
    (4, 10): (1, -1),
    (3, 11): (1, 1),
    (2, 13): (1, 1),
    (10, 15): (1, 1),
    (14, 17): (1, 1),
    (15, 16): (1, -1),
    (16, 8): (1, 1),
    (14, 7): (1, -1),
    (16, 17): (1, -1),
    (12, 16): (1, 1),
}


def normal(layout: exact.Layout, name: str) -> Vector:
    return (
        (neg(layout.axes["v"][0]), neg(layout.axes["v"][1]))
        if name == "w"
        else layout.axes[name]
    )


def tangent(vector: Vector) -> Vector:
    return neg(vector[1]), vector[0]


def offset(layout: exact.Layout, left: int, right: int, name: str) -> Interval:
    return exact.dot(
        tangent(normal(layout, name)),
        exact.difference(layout.centres[right], layout.centres[left]),
    )


def smooth_spin_coefficients(
    layout: exact.Layout,
    pair: tuple[int, int],
    name: str,
) -> dict[int, Interval]:
    """Differentiate the rotating owner's normal and the nonowner's corner support."""
    owner = SMOOTH_OWNERS[pair]
    other = pair[1] if owner == pair[0] else pair[0]
    direction = normal(layout, name)
    vectors = [layout.axes[basis] for basis in features.basis_names(other)]
    signs = SUPPORT_SIGNS[pair]
    for vector, sign in zip(vectors, signs, strict=True):
        projection = exact.dot(direction, vector)
        exact.require(
            projection[0] > 0 if sign > 0 else projection[1] < 0,
            "nonparallel support-corner branch changed",
        )
    corner = (
        mul(
            HALF, add(mul(point(signs[0]), vectors[0][0]), mul(point(signs[1]), vectors[1][0]))
        ),
        mul(
            HALF, add(mul(point(signs[0]), vectors[0][1]), mul(point(signs[1]), vectors[1][1]))
        ),
    )
    hprime = exact.dot(tangent(direction), corner)
    return {owner: sub(offset(layout, *pair, name), hprime), other: hprime}


def load_scales(layout: exact.Layout) -> dict[str, Interval]:
    c, s, d, e, alpha, gamma = (
        layout.guards[name] for name in ("c", "s", "d", "e", "alpha", "gamma")
    )
    side = layout.side
    p = add(side, point(-2), neg(s), div(sub(mul(s, sub(side, point(3))), point(2)), c))
    q = add(side, point(-3), div(sub(mul(c, sub(side, point(3))), point(2)), s))
    ptheta = sub(div(add(side, point(-3), neg(mul(point(2), s))), mul(c, c)), c)
    qtheta = div(add(mul(point(2), c), neg(side), point(3)), mul(s, s))
    f1theta = add(neg(mul(s, sub(side, point(3)))), mul(c, sub(side, point(2))))
    f2theta = add(mul(d, ptheta), mul(e, qtheta))
    f2beta = add(neg(mul(e, p)), mul(d, q))
    g3theta = add(
        mul(c, sub(side, point(3))),
        neg(mul(s, sub(side, point(2)))),
        mul(mul(e, alpha), qtheta),
        neg(mul(mul(e, gamma), q)),
        gamma,
        neg(alpha),
    )
    g3beta = add(gamma, neg(alpha), mul(q, sub(mul(alpha, d), mul(gamma, e))))
    nu, rho = g3beta, neg(f2beta)
    mu = div(neg(add(mul(nu, f2theta), mul(rho, g3theta))), f1theta)
    z = add(nu, mul(alpha, rho))
    ell, r = div(mul(nu, d), c), div(mul(z, e), s)
    normalization = add(
        mul(add(c, s), mu),
        div(mul(gamma, nu), c),
        div(mul(gamma, z), s),
        mul(mul(gamma, rho), add(d, e)),
    )
    return {
        "P": p,
        "Q": q,
        "F1_theta": f1theta,
        "F2_theta": f2theta,
        "F2_beta": f2beta,
        "G3_theta": g3theta,
        "G3_beta": g3beta,
        "mu": mu,
        "nu": nu,
        "rho": rho,
        "Z": z,
        "L": ell,
        "R": r,
        "K": normalization,
    }


def force_roster(
    layout: exact.Layout,
    scales: dict[str, Interval],
) -> tuple[dict[tuple[int, int], Interval], dict[tuple[int, str], Interval]]:
    c, s, d, e, gamma = (layout.guards[name] for name in ("c", "s", "d", "e", "gamma"))
    mu, nu, rho, z, ell, r = (scales[name] for name in ("mu", "nu", "rho", "Z", "L", "R"))
    pair = {
        (1, 2): mul(c, r),
        (1, 3): mul(s, add(ell, rho)),
        (5, 7): mul(c, mu),
        (3, 9): mul(s, ell),
        (9, 10): ell,
        (4, 10): mu,
        (3, 11): rho,
        (11, 12): rho,
        (10, 12): mu,
        (2, 13): r,
        (13, 14): r,
        (12, 14): mu,
        (10, 15): ell,
        (14, 17): r,
        (15, 16): nu,
        (16, 8): mul(gamma, rho),
        (14, 7): mu,
        (16, 17): z,
        (12, 16): rho,
        (9, 11): ZERO,
    }
    wall = {
        (1, "left"): mul(c, r),
        (1, "bottom"): mul(s, add(ell, rho)),
        (2, "bottom"): mul(s, r),
        (3, "left"): mul(c, rho),
        (4, "left"): mul(s, mu),
        (4, "top"): mul(c, mu),
        (5, "bottom"): mul(c, mu),
        (5, "right"): ZERO,
        (6, "bottom"): ZERO,
        (7, "right"): mul(s, mu),
        (8, "right"): mul(mul(e, gamma), rho),
        (8, "top"): mul(mul(d, gamma), rho),
        (9, "left"): mul(c, ell),
        (15, "top"): div(mul(gamma, nu), c),
        (17, "right"): div(mul(gamma, z), s),
    }
    exact.require(
        set(pair) == {(a, b) for a, b, _ in exact.CONTACTS} and set(wall) == exact.ANCHORS,
        "incomplete independent force roster",
    )
    return pair, wall


def face_weights(force: Interval, moment: Interval, k: Interval) -> tuple[Interval, Interval]:
    return mul(HALF, add(force, div(moment, k))), mul(HALF, sub(force, div(moment, k)))


def wall_weights(force: Interval, moment: Interval) -> tuple[Interval, Interval]:
    return sub(mul(HALF, force), moment), add(mul(HALF, force), moment)


@dataclass(frozen=True)
class Stress:
    weights: dict[Row, Interval]
    guards: dict[str, Interval]
    offsets: dict[tuple[int, int], Interval]
    capacities: dict[tuple[int, int], tuple[Interval, Interval]]
    baseline: dict[int, Interval]
    moments: dict[tuple[int, int], Interval]
    scales: dict[str, Interval]


def construct(layout: exact.Layout) -> Stress:
    scales = load_scales(layout)
    pair_forces, wall_forces = force_roster(layout, scales)
    c, s, d, e, gamma = (layout.guards[name] for name in ("c", "s", "d", "e", "gamma"))
    mu, nu, rho, z, ell, r = (scales[name] for name in ("mu", "nu", "rho", "Z", "L", "R"))
    b2 = mul(HALF, mul(r, sub(c, s)))
    b3 = add(mul(mul(s, ell), sub(HALF, s)), mul(HALF, mul(rho, sub(c, s))))
    b7 = mul(HALF, mul(mu, sub(c, s)))
    wall_moments = dict.fromkeys(wall_forces, ZERO)
    wall_moments.update(
        {
            (1, "left"): neg(b2),
            (1, "bottom"): neg(b3),
            (4, "top"): neg(b7),
            (5, "bottom"): neg(b7),
            (8, "top"): mul(HALF, mul(mul(gamma, rho), sub(d, e))),
            (15, "top"): mul(HALF, mul(nu, sub(div(mul(d, s), c), e))),
            (17, "right"): mul(HALF, mul(z, sub(d, div(mul(e, c), s)))),
        }
    )
    moments = {(1, 2): b2, (1, 3): b3, (5, 7): b7, (9, 11): ZERO}
    baseline = dict.fromkeys(range(9, 15), ZERO)
    baseline[9] = mul(wall_forces[9, "left"], mul(HALF, neg(sub(c, s))))
    offsets: dict[tuple[int, int], Interval] = {}
    for left, right, direction in exact.CONTACTS:
        pair = left, right
        force = pair_forces[pair]
        if pair in features.PARALLEL_PAIRS:
            tau = offset(layout, left, right, direction)
            offsets[pair] = tau
            # Exact algebraic simplification of the equal split: f*tau/2 at each owner.
            contribution = mul(HALF, mul(force, tau))
            for label in pair:
                if label in baseline:
                    baseline[label] = add(baseline[label], contribution)
        else:
            for label, coefficient in smooth_spin_coefficients(layout, pair, direction).items():
                if label in baseline:
                    baseline[label] = add(baseline[label], mul(force, coefficient))
    moments.update(
        {
            (9, 10): neg(baseline[9]),
            (10, 12): neg(add(baseline[9], baseline[10])),
            (11, 12): neg(baseline[11]),
            (13, 14): neg(baseline[13]),
            (12, 14): add(baseline[13], baseline[14]),
        }
    )
    weights: dict[Row, Interval] = {}
    for (label, wall), force in wall_forces.items():
        values = (force,) if label == 9 else wall_weights(force, wall_moments[label, wall])
        for variant, value in enumerate(values):
            weights["wall", label, wall, variant] = div(value, scales["K"])
    capacities: dict[tuple[int, int], tuple[Interval, Interval]] = {}
    for pair, force in pair_forces.items():
        if pair in features.PARALLEL_PAIRS:
            k = HALF if pair in AXIS_FACES else mul(HALF, sub(point(1), offsets[pair]))
            moment = moments[pair]
            values = face_weights(force, moment, k)
            capacities[pair] = add(mul(k, force), moment), sub(mul(k, force), moment)
        else:
            values = (force,)
        for variant, value in enumerate(values):
            weights["pair", *pair, variant] = div(value, scales["K"])
    guards = {name: layout.guards[name] for name in ("c", "s", "d", "e", "alpha", "gamma", "T")}
    guards.update(
        {name: scales[name] for name in ("F1_theta", "mu", "nu", "rho", "Z", "L", "R", "K")}
    )
    exact.require(
        len(weights) == 58
        and set(offsets) == set(moments) == set(capacities) == features.PARALLEL_PAIRS,
        "independent stress coverage differs",
    )
    return Stress(weights, guards, offsets, capacities, baseline, moments, scales)


def sign(value: Fraction) -> int:
    return (value > 0) - (value < 0)


def compare_bound(own: Interval, reported: Any) -> dict[str, Any]:
    claimed = exact.read_interval(reported)
    exact.require(
        max(own[0], claimed[0]) <= min(own[1], claimed[1]),
        "independent and reported enclosures are disjoint",
    )
    return {
        "independent_lower_sign": sign(own[0]),
        "recorded_lower_sign": sign(claimed[0]),
        "exact_endpoints_equal": own == claimed,
    }


def audit_intervals(receipt: dict[str, Any], stress: Stress) -> dict[str, Any]:
    expected = {
        "weight_bounds": {str(key): value for key, value in stress.weights.items()},
        "guard_bounds": stress.guards,
        "parallel_offsets": {str(key): value for key, value in stress.offsets.items()},
    }
    comparisons: dict[str, dict[str, dict[str, Any]]] = {}
    failures: list[str] = []
    exact.require(
        type(receipt["weights"]) is int and receipt["weights"] == 58,
        "wrong stress weight count",
    )
    for section, quantities in expected.items():
        exact.require(set(receipt[section]) == set(quantities), f"incomplete {section}")
        comparisons[section] = {}
        for key, own in quantities.items():
            summary = compare_bound(own, receipt[section][key])
            claimed = exact.read_interval(receipt[section][key])
            comparisons[section][key] = summary
            if section == "weight_bounds" and (own[0] < 0 or claimed[0] < 0):
                failures.append(f"nonnegative.{key}")
            if section == "guard_bounds" and (own[0] <= 0 or claimed[0] <= 0):
                failures.append(f"strict_guard.{key}")
    for row in ZERO_ROWS:
        exact.require(
            stress.weights[row] == ZERO and receipt["weight_bounds"][str(row)] == ["0", "0"],
            "prescribed zero weight differs",
        )
    for pair, tau in stress.offsets.items():
        claimed = exact.read_interval(receipt["parallel_offsets"][str(pair)])
        if not (-1 < tau[0] <= tau[1] < 1 and -1 < claimed[0] <= claimed[1] < 1):
            failures.append(f"face_interior.{pair}")
        if pair not in AXIS_FACES and (tau[0] <= 0 or claimed[0] <= 0):
            failures.append(f"positive_offset.{pair}")
    exact.require(
        set(receipt["moment_capacities"]) == {str(pair) for pair in stress.capacities},
        "incomplete moment capacities",
    )
    capacities: dict[str, Any] = {}
    for pair, values in stress.capacities.items():
        reported = receipt["moment_capacities"][str(pair)]
        exact.require(type(reported) is list and len(reported) == 2, "wrong capacity pair")
        capacities[str(pair)] = [
            compare_bound(own, value) for own, value in zip(values, reported, strict=True)
        ]
        if any(
            own[0] < 0 or exact.read_interval(value)[0] < 0
            for own, value in zip(values, reported, strict=True)
        ):
            failures.append(f"capacity.{pair}")
    exact.require(
        type(receipt["nonnegative_weights"]) is int
        and receipt["nonnegative_weights"]
        == sum(
            exact.read_interval(value)[0] >= 0 for value in receipt["weight_bounds"].values()
        ),
        "reported nonnegative count differs",
    )
    return {
        "independent_nonnegative_weights": sum(
            value[0] >= 0 for value in stress.weights.values()
        ),
        "weight_count": 58,
        "positive_guard_count": 15,
        "parallel_offset_count": 9,
        "capacity_count": 18,
        "prescribed_zero_weights": 6,
        "comparisons": comparisons,
        "capacity_comparisons": capacities,
        "signs_certified": not failures,
        "failures": failures,
    }


def audit(_path: Path, _repo: Path = exact.REPO) -> dict[str, Any]:
    """Refuse until receipt binding, rigorous rounding and controls are implemented."""
    raise ValueError(
        "H258 auditor is unfinished and not accepted; receipt binding is unavailable"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()
    try:
        result = audit(args.certificate)
    except (
        ValueError,
        OSError,
        KeyError,
        TypeError,
        IndexError,
        RecursionError,
        subprocess.SubprocessError,
    ) as error:
        print(json.dumps({"audit_passed": False, "error": str(error)}))
        return 1
    print(json.dumps(result, indent=2))
    return 0 if result["audit_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
