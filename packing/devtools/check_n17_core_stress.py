"""Unready draft of a deterministic common-core first-order stress for n17.

The CLI refuses before reading target inputs while exact proof and controls remain
incomplete. Its internal functions retain target-free preparation evidence.
"""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import time
from fractions import Fraction as Q
from functools import lru_cache
from pathlib import Path
from typing import Any

import sympy as sp

from devtools.check_n17_contact_chart import ANCHORS, CONTACTS, SOURCE
from devtools.check_n17_endpoint_feasibility import (
    FROZEN_ROOT_REF,
    Box,
    _dot,
    _encode_receipt,
    _fraction_string,
    _layout,
    _object_unique,
    _read_limited,
    symbolic_identities,
)
from devtools.check_n17_endpoint_features import (
    AXES,
    EXPECTED_COUNTS,
    FROZEN_ENDPOINT_REF,
    PARALLEL_PAIRS,
    _frozen_bytes,
    _require_endpoint_accepted,
    option_manifest,
    square_class,
)
from devtools.check_n17_root_certificate import CertificateError
from devtools.check_n17_root_certificate import check as check_root

DIMENSION = 52
FACE_PAIRS = tuple(sorted(PARALLEL_PAIRS))
CROSS_PAIRS = tuple(
    (left, right)
    for left, right, _, _ in CONTACTS
    if tuple(sorted((left, right))) not in PARALLEL_PAIRS
)
ZERO_FORCE_PAIRS = frozenset({(9, 11)})
ZERO_FORCE_WALLS = frozenset({(6, "bottom"), (5, "right")})
FROZEN_FEATURE_REF = (
    "feafdae49:packing/campaign/series/series-000-smoke-and-calibration/"
    "results/exp-239-n17-endpoint-features/run-001/certificate.json"
)
INSTRUMENT_READY = False


def _coordinate(label: int, component: str) -> int:
    return 3 * (label - 1) + {"x": 0, "y": 1, "angle": 2}[component]


def _add(row: list[Any], label: int, component: str, value: Any) -> None:
    index = _coordinate(label, component)
    row[index] = row[index] + value


CORNER_SIGNS: dict[tuple[int, int], tuple[int, int]] = {
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


def _corner_offset(
    pair: tuple[int, int], normal: tuple[Any, Any], aux: dict[str, Any], half: Any
) -> tuple[Any, Any]:
    left, right = pair
    sorted_pair = tuple(sorted(pair))
    owner = next(
        row["owner"]
        for row in option_manifest()
        if (row["left"], row["right"]) == sorted_pair and row["kind"] == "identity"
    )
    other = right if owner == left else left
    first, second = (aux[name] for name in AXES[square_class(other)])
    a, b = CORNER_SIGNS[pair]
    for vector, expected in ((first, a), (second, b)):
        projection = _dot(normal, vector)
        if isinstance(projection, Box) and not (
            projection.lo > 0 if expected > 0 else projection.hi < 0
        ):
            raise ValueError(f"unsupported cross-contact support branch: {pair}")
    return (
        half * (a * first[0] + b * second[0]),
        half * (a * first[1] + b * second[1]),
    )


def _wall_rows(label: int, wall: str, aux: dict[str, Any], half: Any) -> tuple[list[Any], ...]:
    if (label, wall) not in ANCHORS:
        raise ValueError("wall is not active")
    if label == 9:
        if wall != "left":
            raise ValueError("unexpected oblique wall")
        row = [0] * DIMENSION
        _add(row, label, "x", 1)
        _add(row, label, "angle", -(aux["c"] - aux["s"]) / 2)
        return (row,)
    result: list[list[Any]] = []
    for angle_sign in (-1, 1):
        row = [0] * DIMENSION
        component = "x" if wall in ("left", "right") else "y"
        _add(row, label, component, 1 if wall in ("left", "bottom") else -1)
        _add(row, label, "angle", angle_sign * half)
        if wall in ("right", "top"):
            row[-1] = 1
        result.append(row)
    return tuple(result)


def _pair_rows(
    pair: tuple[int, int],
    axis: str,
    aux: dict[str, Any],
    centres: tuple[tuple[Any, Any], ...],
    half: Any,
) -> tuple[list[Any], ...]:
    left, right = pair
    normal = aux[axis]
    tangent = (-normal[1], normal[0])
    displacement = (
        centres[right - 1][0] - centres[left - 1][0],
        centres[right - 1][1] - centres[left - 1][1],
    )
    translation = [0] * DIMENSION
    for component, value in zip(("x", "y"), normal, strict=True):
        _add(translation, right, component, value)
        _add(translation, left, component, -value)
    if pair in PARALLEL_PAIRS:
        tau = _dot(tangent, displacement)
        # All nonzero declared offsets have a strictly positive root branch.
        k = (1 - tau) / 2
        if pair in {(1, 2), (1, 3), (5, 7)}:
            k = half
        minus, plus = translation.copy(), translation.copy()
        _add(minus, left, "angle", tau / 2 + k)
        _add(minus, right, "angle", tau / 2 - k)
        _add(plus, left, "angle", tau / 2 - k)
        _add(plus, right, "angle", tau / 2 + k)
        return minus, plus
    sorted_pair = tuple(sorted(pair))
    owner = next(
        row["owner"]
        for row in option_manifest()
        if (row["left"], row["right"]) == sorted_pair and row["kind"] == "identity"
    )
    other = right if owner == left else left
    corner = _corner_offset(pair, normal, aux, half)
    hprime = _dot(tangent, corner)
    _add(translation, owner, "angle", _dot(tangent, displacement) - hprime)
    _add(translation, other, "angle", hprime)
    return (translation,)


def common_rows(
    t: Any, b: Any, half: Any
) -> tuple[dict[tuple[Any, ...], list[Any]], Any, dict[str, Any]]:
    side, aux, centres = _layout(t, b, half)
    rows: dict[tuple[Any, ...], list[Any]] = {}
    for label, wall in ANCHORS:
        for variant, row in enumerate(_wall_rows(label, wall, aux, half)):
            rows["wall", label, wall, variant] = row
    for left, right, axis, _ in CONTACTS:
        for variant, row in enumerate(_pair_rows((left, right), axis, aux, centres, half)):
            rows["pair", left, right, variant] = row
    if len(rows) != 58:
        raise ValueError(f"common core requires 58 rows, got {len(rows)}")
    return rows, side, aux


def load_scales(
    side: Any, aux: dict[str, Any], formal: tuple[Any, Any, Any] | None = None
) -> dict[str, Any]:
    """Frozen partial-angle derivatives, evaluated only after fixing the side."""
    c, s, d, e = (aux[name] for name in ("c", "s", "d", "e"))
    alpha, gamma = aux["alpha"], aux["gamma"]
    p = side - 2 - s + (s * (side - 3) - 2) / c
    q = side - 3 + (c * (side - 3) - 2) / s
    p_theta = (side - 3 - 2 * s) / (c * c) - c
    q_theta = (2 * c - side + 3) / (s * s)
    f1_theta = -s * (side - 3) + c * (side - 2)
    f2_theta = d * p_theta + e * q_theta
    f2_beta = -e * p + d * q
    g3_theta = (
        c * (side - 3) - s * (side - 2) + e * alpha * q_theta - e * gamma * q + gamma - alpha
    )
    g3_beta = gamma - alpha + q * (alpha * d - gamma * e)
    nu, rho = g3_beta, -f2_beta
    mu = -(nu * f2_theta + rho * g3_theta) / f1_theta
    if formal is not None:
        mu, nu, rho = formal
    z = nu + alpha * rho
    ell = nu * d / c
    r = z * e / s
    k = (c + s) * mu + gamma * nu / c + gamma * z / s + gamma * rho * (d + e)
    return {
        "P": p,
        "Q": q,
        "F1_theta": f1_theta,
        "F2_theta": f2_theta,
        "F2_beta": f2_beta,
        "G3_theta": g3_theta,
        "G3_beta": g3_beta,
        "mu": mu,
        "nu": nu,
        "rho": rho,
        "Z": z,
        "L": ell,
        "R": r,
        "K": k,
    }


def force_roster(
    aux: dict[str, Any], scales: dict[str, Any]
) -> tuple[dict[tuple[int, int], Any], dict[tuple[int, str], Any]]:
    c, s, d, e = (aux[name] for name in ("c", "s", "d", "e"))
    gamma = aux["gamma"]
    mu, nu, rho = (scales[name] for name in ("mu", "nu", "rho"))
    z, ell, r = (scales[name] for name in ("Z", "L", "R"))
    pair = {
        (1, 2): c * r,
        (1, 3): s * (ell + rho),
        (5, 7): c * mu,
        (3, 9): s * ell,
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
        (16, 8): gamma * rho,
        (14, 7): mu,
        (16, 17): z,
        (12, 16): rho,
        (9, 11): 0,
    }
    wall = {
        (1, "left"): c * r,
        (1, "bottom"): s * (ell + rho),
        (2, "bottom"): s * r,
        (3, "left"): c * rho,
        (4, "left"): s * mu,
        (4, "top"): c * mu,
        (5, "bottom"): c * mu,
        (5, "right"): 0,
        (6, "bottom"): 0,
        (7, "right"): s * mu,
        (8, "right"): e * gamma * rho,
        (8, "top"): d * gamma * rho,
        (9, "left"): c * ell,
        (15, "top"): gamma * nu / c,
        (17, "right"): gamma * z / s,
    }
    if set(pair) != {(left, right) for left, right, _, _ in CONTACTS} or len(wall) != 15:
        raise ValueError("incomplete normal-force roster")
    return pair, wall


def deterministic_weights(
    rows: dict[tuple[Any, ...], list[Any]],
    side: Any,
    aux: dict[str, Any],
    centres: tuple[tuple[Any, Any], ...],
    half: Any,
    *,
    formal: tuple[Any, Any, Any] | None = None,
    normalize: bool = True,
) -> tuple[
    dict[tuple[Any, ...], Any],
    dict[str, Any],
    dict[tuple[int, int], Any],
    dict[tuple[int, str], Any],
]:
    """Assemble the immutable force/moment recipe, including six zero rows."""
    scales = load_scales(side, aux, formal)
    pair_forces, wall_forces = force_roster(aux, scales)
    c, s, d, e, gamma = (aux[name] for name in ("c", "s", "d", "e", "gamma"))
    mu, nu, rho = (scales[name] for name in ("mu", "nu", "rho"))
    z, ell, r = (scales[name] for name in ("Z", "L", "R"))
    b2 = r * (c - s) / 2
    b3 = s * ell * (half - s) + rho * (c - s) / 2
    b7 = mu * (c - s) / 2
    wall_moments = {
        (1, "left"): -b2,
        (1, "bottom"): -b3,
        (2, "bottom"): 0,
        (3, "left"): 0,
        (4, "left"): 0,
        (4, "top"): -b7,
        (5, "bottom"): -b7,
        (5, "right"): 0,
        (6, "bottom"): 0,
        (7, "right"): 0,
        (8, "right"): 0,
        (8, "top"): gamma * rho * (d - e) / 2,
        (15, "top"): nu * (d * s / c - e) / 2,
        (17, "right"): z * (d - e * c / s) / 2,
    }
    moments: dict[tuple[int, int], Any] = {
        (1, 2): b2,
        (1, 3): b3,
        (5, 7): b7,
        (9, 11): 0,
    }

    def assembled(moment_map: dict[tuple[int, int], Any]) -> dict[tuple[Any, ...], Any]:
        weights: dict[tuple[Any, ...], Any] = {}
        for (label, wall), force in wall_forces.items():
            if label == 9:
                weights["wall", label, wall, 0] = force
            else:
                moment = wall_moments[label, wall]
                weights["wall", label, wall, 0] = force * half - moment
                weights["wall", label, wall, 1] = force * half + moment
        for pair, force in pair_forces.items():
            if pair in PARALLEL_PAIRS:
                axis = next(axis for left, right, axis, _ in CONTACTS if (left, right) == pair)
                n = aux[axis]
                tangent = (-n[1], n[0])
                tau = _dot(
                    tangent,
                    (
                        centres[pair[1] - 1][0] - centres[pair[0] - 1][0],
                        centres[pair[1] - 1][1] - centres[pair[0] - 1][1],
                    ),
                )
                k = half if pair in {(1, 2), (1, 3), (5, 7)} else (1 - tau) / 2
                moment = moment_map.get(pair, 0)
                weights["pair", *pair, 0] = (force + moment / k) * half
                weights["pair", *pair, 1] = (force - moment / k) * half
            else:
                weights["pair", *pair, 0] = force
        if set(weights) != set(rows):
            raise ValueError("weight roster does not cover every common row")
        return weights

    baseline = assembled(moments)
    angular_residual = {
        label: sum(
            (
                weight * rows[key][_coordinate(label, "angle")]
                for key, weight in baseline.items()
            ),
            0,
        )
        for label in range(9, 15)
    }
    moments.update(
        {
            (9, 10): -angular_residual[9],
            (10, 12): -angular_residual[9] - angular_residual[10],
            (11, 12): -angular_residual[11],
            (13, 14): -angular_residual[13],
            (12, 14): angular_residual[13] + angular_residual[14],
        }
    )
    if set(moments) != set(PARALLEL_PAIRS):
        raise ValueError("incomplete parallel-face moment roster")
    weights = assembled(moments)
    final_weights = (
        {key: weight / scales["K"] for key, weight in weights.items()} if normalize else weights
    )
    return final_weights, scales, moments, wall_moments


def complete_stress(
    t: Any,
    b: Any,
    half: Any,
    *,
    formal: tuple[Any, Any, Any] | None = None,
    normalize: bool = True,
) -> tuple[
    dict[tuple[Any, ...], list[Any]], dict[tuple[Any, ...], Any], dict[str, Any], list[Any]
]:
    side, aux, centres = _layout(t, b, half)
    rows, _, _ = common_rows(t, b, half)
    weights, scales, _, _ = deterministic_weights(
        rows, side, aux, centres, half, formal=formal, normalize=normalize
    )
    residuals = [
        sum((weights[key] * row[column] for key, row in rows.items()), 0)
        - ((1 if normalize else scales["K"]) if column == DIMENSION - 1 else 0)
        for column in range(DIMENSION)
    ]
    return rows, weights, scales, residuals


def _block_residuals(
    rows: dict[tuple[Any, ...], list[Any]],
    aux: dict[str, Any],
    centres: tuple[tuple[Any, Any], ...],
    scales: dict[str, Any],
    *,
    face_moments: dict[tuple[int, int], Any],
    wall_moments: dict[tuple[int, str], Any],
) -> list[Any]:
    """Cancel each tied two-row block algebraically before column summation."""
    pair_forces, wall_forces = force_roster(aux, scales)
    residuals = [0] * DIMENSION
    for (label, wall), force in wall_forces.items():
        if label == 9:
            row = rows["wall", label, wall, 0]
            for column, coefficient in enumerate(row):
                residuals[column] += force * coefficient
            continue
        component = "x" if wall in ("left", "right") else "y"
        position = _coordinate(label, component)
        residuals[position] += force if wall in ("left", "bottom") else -force
        if wall in ("right", "top"):
            residuals[-1] += force
        residuals[_coordinate(label, "angle")] += wall_moments[label, wall]
    for left, right, axis, _ in CONTACTS:
        pair = (left, right)
        force = pair_forces[pair]
        if pair not in PARALLEL_PAIRS:
            row = rows["pair", left, right, 0]
            for column, coefficient in enumerate(row):
                residuals[column] += force * coefficient
            continue
        normal = aux[axis]
        for component, value in zip(("x", "y"), normal, strict=True):
            residuals[_coordinate(left, component)] -= force * value
            residuals[_coordinate(right, component)] += force * value
        tangent = (-normal[1], normal[0])
        tau = _dot(
            tangent,
            (
                centres[right - 1][0] - centres[left - 1][0],
                centres[right - 1][1] - centres[left - 1][1],
            ),
        )
        moment = face_moments[pair]
        residuals[_coordinate(left, "angle")] += force * tau / 2 + moment
        residuals[_coordinate(right, "angle")] += force * tau / 2 - moment
    residuals[-1] -= scales["K"]
    return residuals


def _verify_tied_row_shapes(
    rows: dict[tuple[Any, ...], list[Any]],
    aux: dict[str, Any],
    centres: tuple[tuple[Any, Any], ...],
) -> int:
    """Bind the block cancellation to each retained physical row."""
    checked = 0
    for label, wall in ANCHORS:
        if label == 9:
            continue
        minus, plus = rows["wall", label, wall, 0], rows["wall", label, wall, 1]
        component = "x" if wall in ("left", "right") else "y"
        expected = [0] * DIMENSION
        expected[_coordinate(label, component)] = 2 if wall in ("left", "bottom") else -2
        expected[-1] = 2 if wall in ("right", "top") else 0
        for column in range(DIMENSION):
            if sp.cancel(minus[column] + plus[column] - expected[column]) != 0:
                raise ValueError(f"wall row sum changed: {(label, wall, column)}")
            difference = -1 if column == _coordinate(label, "angle") else 0
            if sp.cancel(minus[column] - plus[column] - difference) != 0:
                raise ValueError(f"wall row difference changed: {(label, wall, column)}")
        checked += 1
    for left, right, axis, _ in CONTACTS:
        if (left, right) not in PARALLEL_PAIRS:
            continue
        minus, plus = rows["pair", left, right, 0], rows["pair", left, right, 1]
        normal = aux[axis]
        tangent = (-normal[1], normal[0])
        tau = _dot(
            tangent,
            (
                centres[right - 1][0] - centres[left - 1][0],
                centres[right - 1][1] - centres[left - 1][1],
            ),
        )
        k = sp.Rational(1, 2) if (left, right) in {(1, 2), (1, 3), (5, 7)} else (1 - tau) / 2
        expected_sum: list[Any] = [0] * DIMENSION
        expected_diff: list[Any] = [0] * DIMENSION
        for component, value in zip(("x", "y"), normal, strict=True):
            expected_sum[_coordinate(left, component)] = -2 * value
            expected_sum[_coordinate(right, component)] = 2 * value
        expected_sum[_coordinate(left, "angle")] = tau
        expected_sum[_coordinate(right, "angle")] = tau
        expected_diff[_coordinate(left, "angle")] = 2 * k
        expected_diff[_coordinate(right, "angle")] = -2 * k
        for column in range(DIMENSION):
            if sp.cancel(minus[column] + plus[column] - expected_sum[column]) != 0:
                raise ValueError(f"face row sum changed: {(left, right, column)}")
            if sp.cancel(minus[column] - plus[column] - expected_diff[column]) != 0:
                raise ValueError(f"face row difference changed: {(left, right, column)}")
        checked += 1
    if checked != 23:
        raise ValueError("tied-row shape coverage incomplete")
    return checked


@lru_cache(maxsize=1)
def symbolic_residual_proofs() -> dict[str, Any]:
    """Prove the full coefficient identity as rational functions before root use."""
    foundation = symbolic_identities()
    t, b = sp.symbols("t b", real=True)
    mu, nu, rho = sp.symbols("mu nu rho", real=True)
    half = sp.Rational(1, 2)
    side, aux, centres = _layout(t, b, half)
    rows, _, _ = common_rows(t, b, half)
    tied_row_shapes = _verify_tied_row_shapes(rows, aux, centres)
    weights, scales, face_moments, wall_moments = deterministic_weights(
        rows, side, aux, centres, half, formal=(mu, nu, rho), normalize=False
    )
    residuals = _block_residuals(
        rows,
        aux,
        centres,
        scales,
        face_moments=face_moments,
        wall_moments=wall_moments,
    )
    f, q, k, ell, dw, m, a, omega = sp.symbols("f q k ell dw m a omega")
    if (
        sp.cancel(
            (f + q / k) * (ell - k * dw) / 2
            + (f - q / k) * (ell + k * dw) / 2
            - (f * ell - q * dw)
        )
        != 0
        or sp.cancel(
            (f / 2 - m) * (a - omega / 2) + (f / 2 + m) * (a + omega / 2) - (f * a + m * omega)
        )
        != 0
    ):
        raise ValueError("generic two-row block cancellation failed")
    f2 = (
        aux["d"] * (side - aux["X"] - sp.Rational(3, 2))
        - aux["e"] * (aux["Y"] - side + sp.Rational(3, 2))
        - 1
    )
    expected_twelve = (
        mu * scales["F1_theta"]
        + nu * scales["F2_theta"]
        + rho * scales["G3_theta"]
        + aux["gamma"] * rho * f2
    )
    expected_sixteen = -(
        nu * scales["F2_beta"] + rho * scales["G3_beta"] + aux["gamma"] * rho * f2
    )
    for index, residual in enumerate(residuals):
        expected = (
            expected_twelve
            if index == _coordinate(12, "angle")
            else (expected_sixteen if index == _coordinate(16, "angle") else 0)
        )
        if sp.cancel(residual - expected) != 0:
            raise ValueError(f"common-core stationarity identity failed at column {index}")
    fixed = load_scales(side, aux)
    if (
        sp.cancel(fixed["nu"] * fixed["F2_beta"] + fixed["rho"] * fixed["G3_beta"]) != 0
        or sp.cancel(
            fixed["mu"] * fixed["F1_theta"]
            + fixed["nu"] * fixed["F2_theta"]
            + fixed["rho"] * fixed["G3_theta"]
        )
        != 0
    ):
        raise ValueError("fixed load cancellation failed")
    zero_keys = {
        ("wall", 5, "right", 0),
        ("wall", 5, "right", 1),
        ("wall", 6, "bottom", 0),
        ("wall", 6, "bottom", 1),
        ("pair", 9, 11, 0),
        ("pair", 9, 11, 1),
    }
    for key in zero_keys:
        if sp.cancel(weights[key]) != 0:
            raise ValueError(f"prescribed zero-weight identity failed: {key}")
    return {
        "foundation": foundation,
        "rows": 58,
        "columns": DIMENSION,
        "zero_residual_identities": 50,
        "exceptional_F2_identities": 2,
        "prescribed_zero_weights": len(zero_keys),
        "tied_row_shapes": tied_row_shapes,
    }


def interval_sign_audit(midpoint: tuple[Q, Q], radii: tuple[Q, Q]) -> dict[str, Any]:
    """Check the fixed stress on the entire accepted exact root enclosure."""
    if len(midpoint) != 2 or len(radii) != 2:
        raise ValueError("root enclosure must have two dimensions")
    if any(type(value) is not Q for value in (*midpoint, *radii)) or any(
        radius <= 0 for radius in radii
    ):
        raise ValueError("invalid exact root enclosure")
    t, b = (
        Box(value - radius, value + radius)
        for value, radius in zip(midpoint, radii, strict=True)
    )
    half = Box.point(Q(1, 2))
    side, aux, centres = _layout(t, b, half)
    rows, _, _ = common_rows(t, b, half)
    weights, scales, moments, _ = deterministic_weights(rows, side, aux, centres, half)
    guards = {key: aux[key] for key in ("c", "s", "d", "e", "alpha", "gamma", "T")}
    guards.update(
        {key: scales[key] for key in ("F1_theta", "mu", "nu", "rho", "Z", "L", "R", "K")}
    )
    for key, bound in guards.items():
        if bound.lo <= 0:
            raise ValueError(f"strict stress denominator/force guard failed: {key}")
    tau_bounds: dict[tuple[int, int], Box] = {}
    capacities: dict[tuple[int, int], tuple[Box, Box]] = {}
    pair_forces, _ = force_roster(aux, scales)
    for left, right, axis, _ in CONTACTS:
        pair = (left, right)
        if pair not in PARALLEL_PAIRS:
            continue
        n = aux[axis]
        tau = _dot(
            (-n[1], n[0]),
            (
                centres[right - 1][0] - centres[left - 1][0],
                centres[right - 1][1] - centres[left - 1][1],
            ),
        )
        if pair not in {(1, 2), (1, 3), (5, 7)} and tau.lo <= 0:
            raise ValueError(f"positive parallel offset branch failed: {pair}")
        if tau.lo <= -1 or tau.hi >= 1:
            raise ValueError(f"parallel face offset escaped interior: {pair}")
        tau_bounds[pair] = tau
        k = half if pair in {(1, 2), (1, 3), (5, 7)} else (1 - tau) / 2
        force, moment = pair_forces[pair], moments[pair]
        capacities[pair] = (k * force + moment, k * force - moment)
    if len(tau_bounds) != 9:
        raise ValueError("parallel offset coverage incomplete")
    failures = [f"weight.{key}" for key, bound in weights.items() if bound.lo < 0]
    failures.extend(
        f"capacity.{pair}.{sign}"
        for pair, bounds in capacities.items()
        for sign, bound in zip(("plus", "minus"), bounds, strict=True)
        if bound.lo < 0
    )
    negatives = [bound for bound in weights.values() if bound.hi < 0]
    negatives.extend(
        bound for bounds in capacities.values() for bound in bounds if bound.hi < 0
    )
    disposition = (
        "confirmed_fixed_stress"
        if not failures
        else "rejected_fixed_candidate" if negatives else "unresolved_interval_sign"
    )
    return {
        "row_order": [list(key) for key in rows],
        "weight_bounds": {str(key): weights[key].as_json() for key in rows},
        "guard_bounds": {key: bound.as_json() for key, bound in guards.items()},
        "parallel_offsets": {str(key): bound.as_json() for key, bound in tau_bounds.items()},
        "moment_capacities": {
            str(key): [bound.as_json() for bound in bounds]
            for key, bounds in capacities.items()
        },
        "weights": len(weights),
        "nonnegative_weights": sum(bound.lo >= 0 for bound in weights.values()),
        "passed": not failures,
        "disposition": disposition,
        "failures": failures,
    }


def _require_features_accepted(
    document: dict[str, Any], root: dict[str, Any], source: bytes
) -> None:
    if (
        document.get("schema") != "n17-endpoint-feature-certificate/v1"
        or document.get("criterion_passed") is not True
        or document.get("root_git_ref") != FROZEN_ROOT_REF
        or document.get("endpoint_git_ref") != FROZEN_ENDPOINT_REF
        or document.get("source_sha256") != hashlib.sha256(source).hexdigest()
        or document.get("inventory", {}).get("counts") != EXPECTED_COUNTS
        or document.get("inventory", {}).get("box")
        != {
            "midpoint": root["box"]["midpoint"],
            "inclusion_bounds": root["inclusion_bounds"],
        }
    ):
        raise ValueError("frozen H-257 feature inventory is not accepted")


def _root_box(root: dict[str, Any]) -> tuple[tuple[Q, Q], tuple[Q, Q]]:
    midpoint = tuple(Q(value) for value in root["box"]["midpoint"])
    radii = tuple(Q(value) for value in root["inclusion_bounds"])
    if len(midpoint) != 2 or len(radii) != 2:
        raise ValueError("root box must have two dimensions")
    return (midpoint[0], midpoint[1]), (radii[0], radii[1])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root_certificate", type=Path)
    parser.add_argument("endpoint_certificate", type=Path)
    parser.add_argument("feature_certificate", type=Path)
    parser.add_argument("--source", type=Path, default=SOURCE)
    args = parser.parse_args(argv)
    if not INSTRUMENT_READY:
        print(
            json.dumps(
                {
                    "schema": "n17-core-stress-certificate/v1",
                    "criterion_passed": False,
                    "error": "instrument_unready",
                },
                sort_keys=True,
            )
        )
        return 2
    started = time.monotonic()
    try:
        source = _read_limited(args.source)
        root_raw = _read_limited(args.root_certificate)
        endpoint_raw = _read_limited(args.endpoint_certificate)
        feature_raw = _read_limited(args.feature_certificate)
        _frozen_bytes(FROZEN_ROOT_REF, root_raw)
        _frozen_bytes(FROZEN_ENDPOINT_REF, endpoint_raw)
        _frozen_bytes(FROZEN_FEATURE_REF, feature_raw)
        root = json.loads(root_raw, object_pairs_hook=_object_unique)
        endpoint = json.loads(endpoint_raw, object_pairs_hook=_object_unique)
        feature = json.loads(feature_raw, object_pairs_hook=_object_unique)
        root_verification = check_root(root, source)
        _require_endpoint_accepted(endpoint, root, source)
        _require_features_accepted(feature, root, source)
        midpoint, radii = _root_box(root)
        symbolic_started = time.monotonic()
        identities = symbolic_residual_proofs()
        symbolic_seconds = time.monotonic() - symbolic_started
        interval_started = time.monotonic()
        interval = interval_sign_audit(midpoint, radii)
        interval_seconds = time.monotonic() - interval_started
        result = {
            "schema": "n17-core-stress-certificate/v1",
            "root_git_ref": FROZEN_ROOT_REF,
            "endpoint_git_ref": FROZEN_ENDPOINT_REF,
            "feature_git_ref": FROZEN_FEATURE_REF,
            "source_sha256": hashlib.sha256(source).hexdigest(),
            "root_verification": root_verification,
            "box": {
                "midpoint": [_fraction_string(value) for value in midpoint],
                "inclusion_bounds": [_fraction_string(value) for value in radii],
            },
            "identities": identities,
            "interval": interval,
            "criterion_passed": interval["passed"],
            "timing_seconds": {
                "total": time.monotonic() - started,
                "symbolic": symbolic_seconds,
                "interval": interval_seconds,
            },
        }
        print(_encode_receipt(result))
        return 0 if result["criterion_passed"] else 1
    except (
        CertificateError,
        ValueError,
        OSError,
        KeyError,
        IndexError,
        TypeError,
        ZeroDivisionError,
        RecursionError,
        subprocess.TimeoutExpired,
    ) as error:
        print(
            json.dumps(
                {
                    "schema": "n17-core-stress-certificate/v1",
                    "criterion_passed": False,
                    "error": str(error),
                },
                sort_keys=True,
            )
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
