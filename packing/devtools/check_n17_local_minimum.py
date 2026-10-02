"""Exact first-order parts of the n17 local-minimum checker (H-261, BC-407).

This instrument certifies the parts of H-261 that do not depend on the curvature
recipe: the kernel of the positively weighted H-258 rows, exact coordinate duals for
the 90 signed non-slider directions, and the margins of the 135 unavailable owner
alternatives. It does **not** implement curvature bounds, the ratio test, Taylor
checks over a box, uniformity over the slider domain, or the transfer from the rational
point to the algebraic root. Its receipt is therefore not an H-261 verdict.

Point. Everything is evaluated in `fractions.Fraction` arithmetic at the exact
rational point H-258 uses: the exp-237 root-box midpoint `(t, b)`, with the H-254
centres and the fixed H-256 centroid sliders built by `_layout`.

Model. The 58 common-core rows `A_i z >= 0` and their weights come unchanged from
`check_n17_core_stress.complete_stress`, in its frozen row order and its 52 columns
`z = (xi_1, eta_1, omega_1, ..., xi_17, eta_17, omega_17, sigma)`, with `sigma` the
side velocity. Exactly six weights vanish (5-right W-/W+, 6-bottom W-/W+, the 9/11 face
E-/E+); the other 52 rows form the positive set `P`.

Sliders and coordinates. With `u = (c, s)` and `v = (-s, c)` the frame of squares 9 to
14, the six slider generators are the unit vectors of `xi_5`, `xi_6`, `eta_6`, `omega_6`
and the vectors `v` placed on `(xi_11, eta_11)` and on `(xi_13, eta_13)`. The 45
non-slider coordinates are the remaining unit covectors, except that squares 11 and 13
contribute `u . V_11` and `u . V_13` (their component along `u`) instead of `xi` and
`eta`. The kernel claim is `rank A_P = 46` (exact elimination over Q, cross-checked mod
a prime) with every generator annihilated by every positive row, so the kernel is
exactly their span; all 58 rows have rank 50 with lineality `xi_6` and square 13 along
`v`.

Coordinate duals. For each non-slider covector `f_j` and sign `s` in {+1, -1}:

    minimise    a
    over        lambda_i >= 0 (i in P, the 52 positive rows only), a >= 0
    subject to  sum_{i in P} lambda_i A_i = a e_sigma - s f_j     (all 52 columns)

Any feasible pair gives `s f_j . z = a sigma - lambda^T A_P z <= a sigma` on the
first-order cone `A_P z >= 0`: this is the n11 focused-rectangle dual
`lambda^T A = (sign) e_j` with the side column carried by the multiple `a` and with
residual `epsilon_j = 0`. Requiring `a >= 0` loses nothing, since `z = 0` is feasible
in the primal below, so the optimum is nonnegative; and for a smaller packing
(`sigma <= 0`) the side term `a sigma` only helps. The curvature step this module does
not implement would add `M_j = sum_i lambda_i K_i` against the coordinate radius `r_j`,
reading the exact `lambda` from `solve_direction`. The six zero-weight rows are excluded
because the H-261
neighbourhood leaves the slider coordinates free, so those rows need not be active. The
kernel enters twice: `A_P k = 0`, `f_j . k = 0` and `e_sigma . k = 0` for every slider
generator `k`, so the six slider columns of the identity vanish identically and a
certificate is indifferent to the slider values; and the program is posed in the 46
quotient coordinates (45 non-slider plus `sigma`), where `A_P` has full column rank.
The Lagrangian dual is `maximise s f_j . z subject to A_P z >= 0, sigma <= 1`.

Solution and verification. HiGHS proposes an optimal vertex of that primal; the active
set seeds `sqpack.exact_lp.solve`, which re-derives the vertex in exact arithmetic and
pivots by Bland's rule to the exact optimum, restarting from the origin vertex if the
float hint is not an exact vertex. Each certificate is then verified independently of
the simplex: `lambda >= 0`, the 52-column identity exactly, and an exact primal point
`z` with `A_P z >= 0`, `sigma <= 1` and `s f_j . z = a`, so `a` is the exact optimum and
not only a bound. A direction with no nonnegative dual is reported with an exact ray
`z` (`A_P z >= 0`, `sigma <= 0`, `s f_j . z = 1`) and refuses the receipt.

Owner alternatives. Of the 168 raw separating-axis options of the 21 zero pairs (both
owners, both owner axes, both signs; `option_manifest`), 135 are unavailable. Each
margin `sign n . (r_j - r_i) - H_i(n) - H_j(n)`, with the support `H(n)` taken with exact
absolute values, must be strictly negative at the point.

Controls. `kernel-row` adds `xi_5` to the 5-bottom W- row, which must break the kernel
claim; `infeasible-dual` withholds the loaded 4-top W- row, which keeps the kernel claim
but removes every nonnegative dual of the leading direction `-omega_11`. A receipt is
accepted only if every target check passes and both controls are refused.
"""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import argparse
import hashlib
import json
import time
from collections.abc import Callable, Sequence
from dataclasses import dataclass, replace
from decimal import Decimal, localcontext
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import numpy as np
from scipy.optimize import linprog

from devtools.check_n17_core_stress import DIMENSION, complete_stress
from devtools.check_n17_endpoint_feasibility import (
    FROZEN_ROOT_REF,
    REPO,
    _check_frozen_root_bytes,
    _fraction_string,
    _layout,
    _object_unique,
    _read_limited,
)
from devtools.check_n17_endpoint_features import AXES, option_manifest, square_class
from sqpack.exact_lp import (
    ExactLP,
    ExactLPError,
    ExactSolution,
    LinearRow,
    independent_rows,
    rational_sign,
    solve,
)

SCHEMA = "n17-local-minimum-mechanical/v1"
ROOT_CERTIFICATE = (
    REPO
    / "packing/campaign/series/series-000-smoke-and-calibration/results"
    / "exp-237-n17-polynomial-root/run-001/certificate.json"
)
SOURCES = (
    "packing/devtools/check_n17_local_minimum.py",
    "packing/devtools/check_n17_core_stress.py",
    "packing/devtools/check_n17_endpoint_feasibility.py",
    "packing/devtools/check_n17_endpoint_features.py",
    "packing/devtools/check_n17_contact_chart.py",
    "packing/src/sqpack/exact_lp.py",
)
HALF = Q(1, 2)
SIDE = DIMENSION - 1
COMPONENTS = {"x": 0, "y": 1, "angle": 2}
ZERO_WEIGHT_KEYS = frozenset(
    {
        ("wall", 5, "right", 0),
        ("wall", 5, "right", 1),
        ("wall", 6, "bottom", 0),
        ("wall", 6, "bottom", 1),
        ("pair", 9, 11, 0),
        ("pair", 9, 11, 1),
    }
)
SLIDERS = ("xi5", "xi6", "eta6", "omega6", "v11", "v13")
LINEALITY = ("xi6", "v13")
EXPECTED_RANK_POSITIVE = 46
EXPECTED_RANK_ALL = 50
MODULUS = (1 << 61) - 1
CONTROLS = ("kernel-row", "infeasible-dual")
CONTROL_DIRECTION = ("omega11", -1)
DECIMAL_DIGITS = 30

RowKey = tuple[Any, ...]
Vector = dict[int, Q]


def column(label: int, component: str) -> int:
    """Column of a square's `x`, `y` or `angle` velocity in the H-258 order."""
    return 3 * (label - 1) + COMPONENTS[component]


def row_label(key: RowKey) -> str:
    return ":".join(str(part) for part in key)


def decimal(value: Q, digits: int = DECIMAL_DIGITS) -> str:
    """A rounded decimal for reading; the exact rational is always reported beside it."""
    with localcontext() as context:
        context.prec = digits
        return str(Decimal(value.numerator) / Decimal(value.denominator))


def _digits(value: Q) -> list[int]:
    """Decimal digit counts of numerator and denominator, without `str` on huge ints."""
    text = _fraction_string(abs(value))
    top, _, bottom = text.partition("/")
    return [len(top), len(bottom) if bottom else 1]


def _sha256_json(document: Any) -> str:
    return hashlib.sha256(json.dumps(document, sort_keys=True).encode()).hexdigest()


@dataclass(frozen=True)
class Model:
    """The 58 H-258 rows and weights at one exact rational point, as Fractions."""

    t: Q
    b: Q
    keys: tuple[RowKey, ...]
    rows: dict[RowKey, tuple[Q, ...]]
    weights: dict[RowKey, Q]
    stress_residuals: tuple[Q, ...]
    u: tuple[Q, Q]
    v: tuple[Q, Q]
    side: Q

    @property
    def positive_keys(self) -> tuple[RowKey, ...]:
        return tuple(key for key in self.keys if key not in ZERO_WEIGHT_KEYS)


def build_model(t: Q, b: Q) -> Model:
    """Rebuild the frozen H-258 rows and weights with exact rational inputs."""
    if type(t) is not Q or type(b) is not Q:
        raise TypeError("the model point must be exact Fractions")
    rows, weights, _, residuals = complete_stress(t, b, HALF)
    side, aux, _ = _layout(t, b, HALF)
    exact_rows = {key: tuple(Q(value) for value in row) for key, row in rows.items()}
    if len(exact_rows) != 58 or any(len(row) != DIMENSION for row in exact_rows.values()):
        raise ValueError("H-258 builder no longer emits 58 rows of 52 columns")
    return Model(
        t=t,
        b=b,
        keys=tuple(rows),
        rows=exact_rows,
        weights={key: Q(value) for key, value in weights.items()},
        stress_residuals=tuple(Q(value) for value in residuals),
        u=(Q(aux["u"][0]), Q(aux["u"][1])),
        v=(Q(aux["v"][0]), Q(aux["v"][1])),
        side=Q(side),
    )


def mutate(model: Model, control: str) -> Model:
    """Apply one synthetic control mutation; the target model is never altered."""
    if control == "kernel-row":
        key = ("wall", 5, "bottom", 0)
        row = list(model.rows[key])
        row[column(5, "x")] += Q(1, 1000)
        return replace(model, rows={**model.rows, key: tuple(row)})
    if control == "infeasible-dual":
        withheld = ("wall", 4, "top", 0)
        return replace(model, keys=tuple(key for key in model.keys if key != withheld))
    raise ValueError(f"unknown control: {control}")


def slider_generators(model: Model) -> dict[str, Vector]:
    """The six named slider motions as exact sparse vectors over the 52 columns."""
    (vx, vy) = model.v
    return {
        "xi5": {column(5, "x"): Q(1)},
        "xi6": {column(6, "x"): Q(1)},
        "eta6": {column(6, "y"): Q(1)},
        "omega6": {column(6, "angle"): Q(1)},
        "v11": {column(11, "x"): vx, column(11, "y"): vy},
        "v13": {column(13, "x"): vx, column(13, "y"): vy},
    }


def coordinates(model: Model) -> dict[str, Vector]:
    """The 45 non-slider covectors, which are also their own lifts since `u` is unit."""
    (ux, uy) = model.u
    result: dict[str, Vector] = {}
    for label in range(1, 18):
        if label == 6:
            continue
        if label in {11, 13}:
            result[f"u{label}"] = {column(label, "x"): ux, column(label, "y"): uy}
        elif label != 5:
            result[f"xi{label}"] = {column(label, "x"): Q(1)}
        if label not in {11, 13}:
            result[f"eta{label}"] = {column(label, "y"): Q(1)}
        result[f"omega{label}"] = {column(label, "angle"): Q(1)}
    if len(result) != 45:
        raise ValueError("non-slider coordinate roster drifted")
    return result


def directions(model: Model) -> tuple[tuple[str, int], ...]:
    return tuple((name, sign) for name in coordinates(model) for sign in (1, -1))


def _apply(row: Sequence[Q], vector: Vector) -> Q:
    return sum((row[index] * value for index, value in vector.items()), Q(0))


def exact_rank(matrix: Sequence[Sequence[Q]]) -> int:
    """Rank over Q by Gaussian elimination, choosing the sparsest pivot row."""
    work = [list(row) for row in matrix if any(row)]
    rank = 0
    width = len(work[0]) if work else 0
    for index in range(width):
        candidates = [position for position in range(rank, len(work)) if work[position][index]]
        if not candidates:
            continue
        position = min(candidates, key=lambda row: sum(value != 0 for value in work[row]))
        work[rank], work[position] = work[position], work[rank]
        pivot = work[rank]
        inverse = 1 / pivot[index]
        for other in range(rank + 1, len(work)):
            factor = work[other][index]
            if factor != 0:
                scale = factor * inverse
                work[other] = [
                    left - scale * right if right != 0 else left
                    for left, right in zip(work[other], pivot, strict=True)
                ]
        rank += 1
    return rank


def modular_rank(matrix: Sequence[Sequence[Q]], modulus: int = MODULUS) -> int:
    """Rank modulo a prime, a lower bound for the rank over Q when entries are p-integral."""
    work: list[list[int]] = []
    for row in matrix:
        reduced: list[int] = []
        for value in row:
            if value.denominator % modulus == 0:
                raise ValueError("entry is not integral at the modular-rank prime")
            reduced.append(value.numerator * pow(value.denominator, -1, modulus) % modulus)
        work.append(reduced)
    rank = 0
    width = len(work[0]) if work else 0
    for index in range(width):
        position = next((r for r in range(rank, len(work)) if work[r][index]), None)
        if position is None:
            continue
        work[rank], work[position] = work[position], work[rank]
        inverse = pow(work[rank][index], -1, modulus)
        for other in range(rank + 1, len(work)):
            factor = work[other][index] * inverse % modulus
            if factor:
                work[other] = [
                    (left - factor * right) % modulus
                    for left, right in zip(work[other], work[rank], strict=True)
                ]
        rank += 1
    return rank


def weight_audit(model: Model) -> dict[str, Any]:
    """Confirm the six prescribed zero weights and the positivity of the other 52."""
    zero = sorted(row_label(key) for key in model.keys if model.weights[key] == 0)
    negative = sorted(row_label(key) for key in model.keys if model.weights[key] < 0)
    positive = [model.weights[key] for key in model.keys if model.weights[key] > 0]
    expected_zero = sorted(row_label(key) for key in ZERO_WEIGHT_KEYS)
    smallest = min(
        (key for key in model.keys if model.weights[key] > 0), key=model.weights.__getitem__
    )
    nonzero_residuals = {
        str(index): decimal(value, 12)
        for index, value in enumerate(model.stress_residuals)
        if value != 0
    }
    return {
        "rows": len(model.keys),
        "zero_weight_rows": zero,
        "negative_weight_rows": negative,
        "positive_weight_rows": len(positive),
        "smallest_positive_weight": {
            "row": row_label(smallest),
            "value": decimal(model.weights[smallest], 12),
        },
        "stress_residual_columns_at_point": nonzero_residuals,
        "passed": zero == expected_zero and not negative and len(positive) == 52,
    }


def kernel_audit(model: Model) -> dict[str, Any]:
    """Exact rank, kernel basis and lineality of the positive rows and of all rows."""
    positive = [model.rows[key] for key in model.positive_keys]
    every = [model.rows[key] for key in model.keys]
    generators = slider_generators(model)
    rank_positive = exact_rank(positive)
    rank_all = exact_rank(every)
    modular_positive = modular_rank(positive)
    modular_all = modular_rank(every)
    dense = [
        [vector.get(index, Q(0)) for index in range(DIMENSION)]
        for vector in generators.values()
    ]
    generator_rank = exact_rank(dense)
    annihilated: dict[str, bool] = {}
    zero_row_values: dict[str, dict[str, str]] = {}
    for name, vector in generators.items():
        annihilated[name] = all(
            _apply(model.rows[key], vector) == 0 for key in model.positive_keys
        )
        zero_row_values[name] = {
            row_label(key): _fraction_string(_apply(model.rows[key], vector))
            for key in model.keys
            if key not in model.positive_keys and _apply(model.rows[key], vector) != 0
        }
    lineality = sorted(name for name, values in zero_row_values.items() if not values)
    kernel_dimension = DIMENSION - rank_positive
    equals_span = kernel_dimension == 6 and generator_rank == 6 and all(annihilated.values())
    checks = {
        "rank_positive": rank_positive == EXPECTED_RANK_POSITIVE,
        "rank_positive_mod_p": modular_positive == EXPECTED_RANK_POSITIVE,
        "kernel_equals_slider_span": equals_span,
        "rank_all": rank_all == EXPECTED_RANK_ALL,
        "rank_all_mod_p": modular_all == EXPECTED_RANK_ALL,
        "lineality": DIMENSION - rank_all == 2
        and annihilated["xi6"]
        and annihilated["v13"]
        and lineality == sorted(LINEALITY),
    }
    return {
        "positive_rows": len(positive),
        "rank_positive": rank_positive,
        "rank_positive_mod_p": modular_positive,
        "kernel_dimension": kernel_dimension,
        "generator_rank": generator_rank,
        "generators": {
            name: {str(index): _fraction_string(value) for index, value in vector.items()}
            for name, vector in generators.items()
        },
        "generators_annihilated_by_positive_rows": annihilated,
        "generator_values_on_zero_weight_rows": zero_row_values,
        "rank_all": rank_all,
        "rank_all_mod_p": modular_all,
        "lineality_dimension": DIMENSION - rank_all,
        "lineality_generators": lineality,
        "modulus": str(MODULUS),
        "checks": checks,
        "passed": all(checks.values()),
    }


@dataclass(frozen=True)
class Quotient:
    """Positive rows written in the 46 quotient coordinates (45 non-slider and sigma)."""

    names: tuple[str, ...]
    lifts: tuple[Vector, ...]
    keys: tuple[RowKey, ...]
    rows: tuple[tuple[Q, ...], ...]


def quotient(model: Model) -> Quotient:
    named = coordinates(model)
    names = (*named, "sigma")
    lifts = (*named.values(), {SIDE: Q(1)})
    keys = model.positive_keys
    rows = tuple(tuple(_apply(model.rows[key], lift) for lift in lifts) for key in keys)
    return Quotient(names=names, lifts=lifts, keys=keys, rows=rows)


def _lift(space: Quotient, point: Sequence[Q]) -> list[Q]:
    full = [Q(0)] * DIMENSION
    for value, lift in zip(point, space.lifts, strict=True):
        for index, coefficient in lift.items():
            full[index] += value * coefficient
    return full


def _exact_program(space: Quotient, objective_index: int, sign: int, *, ray: bool) -> ExactLP:
    """`min -s z_j` over `-A_P z <= 0`, `sigma <= 1`; or the bounded ray program."""
    width = len(space.names)
    unit = [Q(0)] * width
    unit[-1] = Q(1)
    rows = [
        LinearRow(row_label(key), tuple(-value for value in row))
        for key, row in zip(space.keys, space.rows, strict=True)
    ]
    rows.append(LinearRow("sigma", tuple(unit)))
    rhs = [Q(0)] * len(space.keys) + [Q(0) if ray else Q(1)]
    if ray:
        bound = [Q(0)] * width
        bound[objective_index] = Q(sign)
        rows.append(LinearRow("bound", tuple(bound)))
        rhs.append(Q(1))
    objective = [Q(0)] * width
    objective[objective_index] = Q(-sign)
    return ExactLP(tuple(objective), tuple(rows), tuple(rhs), Q(0), Q(1))


def _float_order(lp: ExactLP, space: Quotient, objective_index: int, sign: int) -> list[int]:
    """Rows ordered by their slack at a HiGHS optimum, tightest first."""
    width = len(space.names)
    matrix = np.array([[float(value) for value in row.coefficients] for row in lp.rows])
    rhs = np.array([float(value) for value in lp.rhs])
    cost = np.zeros(width)
    cost[objective_index] = -sign
    result = linprog(cost, A_ub=matrix, b_ub=rhs, bounds=[(None, None)] * width, method="highs")
    if result.status != 0:
        return list(range(len(lp.rows)))
    slack = rhs - matrix @ result.x
    return sorted(range(len(lp.rows)), key=lambda index: (abs(float(slack[index])), index))


def _exact_solve(lp: ExactLP, order: list[int], width: int) -> tuple[ExactSolution, str]:
    """Bland's rule from the float-suggested vertex, else from the origin vertex."""
    try:
        start = independent_rows(lp, order, size=width)
        return solve(lp, start, rational_sign), "float_hint"
    except ExactLPError as error:
        if error.kind == "unbounded":
            raise
    origin = independent_rows(lp, range(len(lp.rows) - 1), size=width)
    return solve(lp, origin, rational_sign), "origin"


def _verify_dual(
    model: Model, space: Quotient, name: str, sign: int, *, lam: dict[RowKey, Q], a: Q
) -> bool:
    """Replay `sum lambda_i A_i = a e_sigma - s f_j` in all 52 columns, independently."""
    if a < 0 or any(value < 0 for value in lam.values()) or not set(lam) <= set(space.keys):
        return False
    total = [Q(0)] * DIMENSION
    for key, value in lam.items():
        for index, coefficient in enumerate(model.rows[key]):
            if coefficient != 0:
                total[index] += value * coefficient
    expected = [Q(0)] * DIMENSION
    expected[SIDE] = a
    for index, coefficient in coordinates(model)[name].items():
        expected[index] -= sign * coefficient
    return total == expected


def _verify_primal(
    model: Model,
    space: Quotient,
    name: str,
    sign: int,
    *,
    point: Sequence[Q],
    value: Q,
    ray: bool,
) -> bool:
    """Replay the primal witness on the original rows: feasibility and attained value."""
    full = _lift(space, point)
    feasible = all(_apply(model.rows[key], dict(enumerate(full))) >= 0 for key in space.keys)
    side_ok = full[SIDE] <= 0 if ray else full[SIDE] <= 1
    attained = sign * _apply(full, coordinates(model)[name]) == value
    return feasible and side_ok and attained


@dataclass(frozen=True)
class DirectionSolution:
    """The exact outcome for one signed direction.

    For `certified_optimal`, `lam` and `a` are the exact dual and `point` the exact primal
    optimum in the quotient coordinates; for `no_nonnegative_dual`, `point` is the exact
    ray. A downstream curvature step reads `lam` from here rather than from a receipt.
    """

    name: str
    sign: int
    status: str
    lam: dict[RowKey, Q]
    a: Q | None
    point: tuple[Q, ...]
    active: tuple[str, ...] = ()
    pivots: int = 0
    start: str = ""
    error: str = ""

    @property
    def label(self) -> str:
        return f"{'+' if self.sign > 0 else '-'}{self.name}"


def verify_solution(model: Model, space: Quotient, solution: DirectionSolution) -> bool:
    """Replay a certificate on the original 52 columns, independently of the simplex."""
    if solution.status == "certified_optimal" and solution.a is not None:
        return _verify_dual(
            model, space, solution.name, solution.sign, lam=solution.lam, a=solution.a
        ) and _verify_primal(
            model,
            space,
            solution.name,
            solution.sign,
            point=solution.point,
            value=solution.a,
            ray=False,
        )
    if solution.status == "no_nonnegative_dual":
        return _verify_primal(
            model,
            space,
            solution.name,
            solution.sign,
            point=solution.point,
            value=Q(1),
            ray=True,
        )
    return False


def solve_direction(model: Model, space: Quotient, name: str, sign: int) -> DirectionSolution:
    """Exact optimal dual and primal certificate for one signed non-slider direction."""
    index = space.names.index(name)
    width = len(space.names)
    lp = _exact_program(space, index, sign, ray=False)
    try:
        solution, start = _exact_solve(lp, _float_order(lp, space, index, sign), width)
    except ExactLPError as error:
        if error.kind != "unbounded":
            return DirectionSolution(name, sign, "undecided", {}, None, (), error=str(error))
        return _no_dual(model, space, name, sign)
    vertex = solution.vertex
    lam: dict[RowKey, Q] = {}
    a = Q(0)
    for row_index, multiplier in zip(vertex.active, vertex.multipliers, strict=True):
        if row_index == len(space.keys):
            a = multiplier
        elif multiplier != 0:
            lam[space.keys[row_index]] = multiplier
    result = DirectionSolution(
        name,
        sign,
        "certified_optimal",
        lam,
        a,
        tuple(vertex.point),
        active=tuple(lp.rows[row].label for row in vertex.active),
        pivots=solution.pivots,
        start=start,
    )
    if a != -vertex.objective_value or not verify_solution(model, space, result):
        return replace(result, status="undecided", error="exact replay failed")
    return result


def _no_dual(model: Model, space: Quotient, name: str, sign: int) -> DirectionSolution:
    """Certify, by an exact ray, that a direction has no nonnegative dual."""
    index = space.names.index(name)
    lp = _exact_program(space, index, sign, ray=True)
    try:
        solution, start = _exact_solve(
            lp, _float_order(lp, space, index, sign), len(space.names)
        )
    except ExactLPError as error:
        return DirectionSolution(name, sign, "undecided", {}, None, (), error=str(error))
    result = DirectionSolution(
        name,
        sign,
        "no_nonnegative_dual",
        {},
        None,
        tuple(solution.vertex.point),
        pivots=solution.pivots,
        start=start,
    )
    if solution.vertex.objective_value != -1 or not verify_solution(model, space, result):
        return replace(result, status="undecided", error="ray replay failed")
    return result


def direction_record(solution: DirectionSolution) -> dict[str, Any]:
    """The receipt entry: exact optimum, readable multipliers, digests of exact vectors."""
    record: dict[str, Any] = {
        "direction": solution.label,
        "coordinate": solution.name,
        "sign": solution.sign,
        "status": solution.status,
        "pivots": solution.pivots,
        "start": solution.start,
    }
    point_digest = _sha256_json([_fraction_string(value) for value in solution.point])
    if solution.status == "certified_optimal" and solution.a is not None:
        exact = {row_label(key): _fraction_string(value) for key, value in solution.lam.items()}
        record.update(
            {
                "a": _fraction_string(solution.a),
                "a_decimal": decimal(solution.a),
                "a_digits": _digits(solution.a),
                "support": len(solution.lam),
                "lambda_sum_decimal": decimal(sum(solution.lam.values(), Q(0)), 12),
                "lambda_decimal": {
                    row_label(key): decimal(value, 10) for key, value in solution.lam.items()
                },
                "lambda_sha256": _sha256_json(exact),
                "primal_sha256": point_digest,
                "active_rows": list(solution.active),
            }
        )
    elif solution.status == "no_nonnegative_dual":
        record.update(
            {
                "ray_sha256": point_digest,
                "ray_side_velocity": _fraction_string(solution.point[-1]),
            }
        )
    else:
        record["error"] = solution.error
    return record


def dual_audit(
    model: Model,
    *,
    only: Sequence[tuple[str, int]] | None = None,
    fail_fast: bool = False,
    progress: Callable[[str], None] | None = None,
) -> dict[str, Any]:
    """Exact coordinate duals for every requested signed non-slider direction."""
    space = quotient(model)
    wanted = tuple(only) if only is not None else directions(model)
    solutions: list[DirectionSolution] = []
    for name, sign in wanted:
        solution = solve_direction(model, space, name, sign)
        solutions.append(solution)
        if progress is not None:
            value = "" if solution.a is None else decimal(solution.a, 12)
            progress(f"{solution.label}: {solution.status} {value}")
        if fail_fast and solution.status != "certified_optimal":
            break
    optima = {
        solution.label: solution.a
        for solution in solutions
        if solution.status == "certified_optimal" and solution.a is not None
    }
    ranked = sorted(optima, key=lambda label: (-optima[label], label))
    return {
        "directions_requested": len(wanted),
        "directions_attempted": len(solutions),
        "certified_optimal": len(optima),
        "no_nonnegative_dual": [
            solution.label for solution in solutions if solution.status == "no_nonnegative_dual"
        ],
        "undecided": [
            solution.label for solution in solutions if solution.status == "undecided"
        ],
        "largest": [
            {"direction": label, "a_decimal": decimal(optima[label], 12)}
            for label in ranked[:12]
        ],
        "zero_multiple": sorted(label for label, value in optima.items() if value == 0),
        "results": [direction_record(solution) for solution in solutions],
        "passed": len(optima) == len(wanted),
    }


def _support(label: int, normal: tuple[Q, Q], aux: dict[str, Any]) -> Q:
    first, second = (aux[name] for name in AXES[square_class(label)])
    return (
        abs(normal[0] * first[0] + normal[1] * first[1])
        + abs(normal[0] * second[0] + normal[1] * second[1])
    ) / 2


def owner_alternative_audit(model: Model) -> dict[str, Any]:
    """Exact margins of the 168 raw owner-axis options; the 135 unavailable must be < 0."""
    _, aux, centres = _layout(model.t, model.b, HALF)
    strict: list[tuple[Q, dict[str, Any]]] = []
    identity: list[tuple[Q, dict[str, Any]]] = []
    for option in option_manifest():
        left, right, owner = int(option["left"]), int(option["right"]), int(option["owner"])
        normal = aux[option["axis"]]
        displacement = (
            centres[right - 1][0] - centres[left - 1][0],
            centres[right - 1][1] - centres[left - 1][1],
        )
        margin = Q(
            option["sign"] * (normal[0] * displacement[0] + normal[1] * displacement[1])
            - _support(left, normal, aux)
            - _support(right, normal, aux)
        )
        entry = {
            "pair": [left, right],
            "owner": owner,
            "axis": option["axis"],
            "sign": option["sign"],
            "margin": _fraction_string(margin),
            "margin_decimal": decimal(margin, 12),
        }
        (identity if option["kind"] == "identity" else strict).append((margin, entry))
    ranked = [entry for _, entry in sorted(strict, key=lambda item: -item[0])]
    negative = sum(margin < 0 for margin, _ in strict)
    largest_identity = max(abs(margin) for margin, _ in identity)
    return {
        "options": len(strict) + len(identity),
        "unavailable": len(strict),
        "strictly_negative": negative,
        "least_negative": [
            {key: row[key] for key in ("pair", "owner", "axis", "sign", "margin_decimal")}
            for row in ranked[:8]
        ],
        "identity_options": len(identity),
        "identity_exact_zero": sum(margin == 0 for margin, _ in identity),
        "identity_largest_abs_decimal": decimal(largest_identity, 6),
        "margins": [entry for _, entry in strict],
        "identity_margins": [entry for _, entry in identity],
        "passed": len(strict) == 135 and negative == 135 and len(identity) == 33,
    }


def run_control(model: Model, control: str) -> dict[str, Any]:
    """Run one synthetic control through the checks it targets; it must be refused."""
    mutated = mutate(model, control)
    kernel = kernel_audit(mutated)
    failed = [f"kernel.{name}" for name, ok in kernel["checks"].items() if not ok]
    detail: dict[str, Any] = {"kernel_checks": kernel["checks"]}
    if control == "infeasible-dual":
        duals = dual_audit(mutated, only=(CONTROL_DIRECTION,), fail_fast=True)
        detail["direction"] = duals["results"][0]
        if not duals["passed"]:
            failed.append(f"duals.{duals['results'][0]['direction']}")
    return {"control": control, "refused": bool(failed), "failed_checks": failed, **detail}


def source_digests() -> dict[str, str]:
    return {path: hashlib.sha256((REPO / path).read_bytes()).hexdigest() for path in SOURCES}


def certify(
    t: Q,
    b: Q,
    *,
    control: str | None = None,
    progress: Callable[[str], None] | None = None,
) -> dict[str, Any]:
    """All mechanical checks at one point; with `control`, on the mutated model."""
    timings: dict[str, float] = {}
    started = time.monotonic()
    target = build_model(t, b)
    model = target if control is None else mutate(target, control)
    timings["build"] = time.monotonic() - started
    stage = time.monotonic()
    weights = weight_audit(target)
    kernel = kernel_audit(model)
    timings["kernel"] = time.monotonic() - stage
    stage = time.monotonic()
    duals = (
        dual_audit(model, fail_fast=control is not None, progress=progress)
        if kernel["passed"]
        else {"passed": False, "skipped": "kernel claim failed; duals not attempted"}
    )
    timings["duals"] = time.monotonic() - stage
    stage = time.monotonic()
    owners = owner_alternative_audit(target)
    timings["owner_alternatives"] = time.monotonic() - stage
    stage = time.monotonic()
    controls = [run_control(target, name) for name in CONTROLS] if control is None else []
    timings["controls"] = time.monotonic() - stage
    checks = {
        "weights": weights["passed"],
        "kernel": kernel["passed"],
        "duals": duals["passed"],
        "owner_alternatives": owners["passed"],
        "controls_refused": all(row["refused"] for row in controls) and control is None,
    }
    timings["total"] = time.monotonic() - started
    return {
        "point": {
            "t": _fraction_string(t),
            "b": _fraction_string(b),
            "t_decimal": decimal(t),
            "b_decimal": decimal(b),
            "side_decimal": decimal(target.side),
        },
        "control": control,
        "weights": weights,
        "kernel": kernel,
        "duals": duals,
        "owner_alternatives": owners,
        "controls": controls,
        "checks": checks,
        "passed": all(checks.values()),
        "timing_seconds": timings,
    }


def read_point(raw: bytes) -> tuple[tuple[Q, Q], tuple[Q, Q]]:
    """The exp-237 midpoint and inclusion radii from root-certificate bytes."""
    document = json.loads(raw, object_pairs_hook=_object_unique)
    midpoint = tuple(Q(value) for value in document["box"]["midpoint"])
    radii = tuple(Q(value) for value in document["inclusion_bounds"])
    if len(midpoint) != 2 or len(radii) != 2:
        raise ValueError("root box must have two dimensions")
    return (midpoint[0], midpoint[1]), (radii[0], radii[1])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Exact first-order parts of the n17 local-minimum checker (H-261)."
    )
    parser.add_argument("root_certificate", type=Path, nargs="?", default=ROOT_CERTIFICATE)
    parser.add_argument("--output", type=Path, help="write the JSON receipt here")
    parser.add_argument("--control", choices=CONTROLS, help="run one refusal control")
    parser.add_argument("--progress", action="store_true", help="report each direction")
    args = parser.parse_args(argv)
    try:
        raw = _read_limited(args.root_certificate)
        _check_frozen_root_bytes(raw)
        midpoint, radii = read_point(raw)
        result = certify(
            *midpoint,
            control=args.control,
            progress=(lambda line: print(line, flush=True)) if args.progress else None,
        )
    except (ValueError, OSError, KeyError, IndexError, TypeError, ExactLPError) as error:
        print(json.dumps({"schema": SCHEMA, "passed": False, "error": str(error)}))
        return 2
    receipt = {
        "schema": SCHEMA,
        "scope": (
            "mechanical parts of H-261 only: kernel, exact coordinate duals, owner "
            "alternative margins at the rational point; no curvature bound, ratio test, "
            "Taylor box check, slider-domain uniformity, or root transfer"
        ),
        "inputs": {
            "root_certificate": str(args.root_certificate),
            "root_certificate_sha256": hashlib.sha256(raw).hexdigest(),
            "root_certificate_git_ref": FROZEN_ROOT_REF,
            "root_box_radii": [_fraction_string(value) for value in radii],
            "sources_sha256": source_digests(),
        },
        **result,
    }
    encoded = json.dumps(receipt, sort_keys=True, indent=1)
    if args.output is not None:
        args.output.write_text(encoded + "\n")
    summary = {
        "schema": SCHEMA,
        "passed": receipt["passed"],
        "checks": receipt["checks"],
        "control": receipt["control"],
        "largest_dual": receipt["duals"].get("largest", [])[:1],
        "timing_seconds": receipt["timing_seconds"],
    }
    print(json.dumps(summary, sort_keys=True))
    return 0 if receipt["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
