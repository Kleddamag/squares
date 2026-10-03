"""Check the conditional fixed-T local-isolation inequalities for eleven squares.

The exact witness/derivative source is shared with the published checker. This
consumer independently replays proposal arithmetic, feature coverage, and the
strict anisotropic Taylor margins. It does not check source-pose inclusion.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import time
from fractions import Fraction
from math import isqrt
from pathlib import Path
from typing import Any, cast

from cases.trump11 import isolation_radius
from devtools import check_n11_optimality_local_dual as dual

Q = Fraction
DUAL_CHECKER_SHA = "2078773593607d3da54f4d6fe7088c5fed224309837d712b030c75d9be04e1f1"
U = Q(387708359002281417731, 10**20)


def require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def signature(values: Any) -> tuple[tuple[tuple[int, int], ...], ...]:
    return tuple(
        tuple((coefficient.numerator, coefficient.denominator) for coefficient in value.coeffs)
        for value in values
    )


def radical_upper(value: Q, denominator: int = 10**15) -> Q:
    require(value >= 0 and denominator > 0, "invalid radicand or rounding scale")
    scaled = (value.numerator * denominator**2 + value.denominator - 1) // value.denominator
    root = isqrt(scaled)
    if root * root < scaled:
        root += 1
    upper = Q(root, denominator)
    require(upper * upper >= value, "radical upper bound is unsound")
    return upper


def strict_feature_margin(upper_value: Q, linear: Q, curvature: Q) -> Q:
    margin = -(upper_value + linear + curvature / 2)
    require(margin > 0, "unavailable feature may activate in rectangle")
    return margin


def strict_dual_margin(radius: Q, residual: Q, maximum_radius: Q, mass: Q) -> Q:
    right = 2 * (radius - residual * maximum_radius)
    require(right > 0 and 0 < mass < right, "anisotropic signed-coordinate dual margin failed")
    return mass / right


def bridge_features(
    witness: isolation_radius.Witness, functions: list[isolation_radius.Elementary]
) -> tuple[dict[tuple[Any, ...], list[isolation_radius.Elementary]], dict[str, int]]:
    contacts = {contact.pair: contact for contact in witness.contacts}
    require(len(contacts) == 14, "contact pair inventory incomplete")
    features: dict[tuple[Any, ...], list[isolation_radius.Elementary]] = {}
    for function in functions:
        if function.kind == "pair" and function.subject[:2] in contacts:
            features.setdefault(function.subject[:5], []).append(function)
    require(len(features) == 112, "contact feature inventory incomplete")
    choices: dict[tuple[int, int], list[tuple[Any, ...]]] = {pair: [] for pair in contacts}
    unavailable: dict[tuple[Any, ...], list[isolation_radius.Elementary]] = {}
    active = 0
    for key, members in sorted(features.items()):
        require(
            len(members) == 4 and {item.subject[-1] for item in members} == set(range(4)),
            "feature corner inventory incomplete",
        )
        signs = [item.value.sign() for item in members]
        if min(signs) < 0:
            unavailable[key] = members
            continue
        require(min(signs) == 0, "available contact feature lacks a tied corner")
        active += 1
        tied = tuple(
            sorted({signature(item.gradient) for item in members if item.value.is_zero()})
        )
        first, second, owner, axis, order = key
        alias = f"{first}-{second}/{owner}.{axis}/{order}"
        options = [
            option for option in contacts[first, second].options if alias in option.aliases
        ]
        require(len(options) == 1, "nonlinear feature alias is not uniquely assigned")
        require(
            tied == tuple(sorted(signature(row.coefficients) for row in options[0].rows)),
            "feature gradients differ from tangent option",
        )
        choices[first, second].append(tied)
    require(
        active == 24 and len(unavailable) == 88, "available/unavailable feature census differs"
    )
    require(
        sum(len(option.aliases) for contact in contacts.values() for option in contact.options)
        == active,
        "raw feature alias census differs",
    )
    walls = tuple(
        sorted(
            signature(function.gradient)
            for function in functions
            if function.kind == "wall" and function.value.is_zero()
        )
    )
    require(
        walls == tuple(sorted(signature(row.coefficients) for row in witness.walls)),
        "wall derivative bridge differs",
    )
    matrices: set[tuple[Any, ...]] = set()
    raw_count = 0
    for selection in itertools.product(*(choices[pair] for pair in sorted(choices))):
        raw_count += 1
        matrices.add(
            tuple(sorted(walls + tuple(row for feature in selection for row in feature)))
        )
    expected = {
        tuple(sorted(signature(row.coefficients) for row in branch["rows"]))
        for branch in witness.branches
    }
    require(
        raw_count == 512 and len(matrices) == 128 and matrices == expected,
        "raw-to-derivative branch bridge incomplete",
    )
    return unavailable, {
        "contact_pairs": len(contacts),
        "features": len(features),
        "available_features": active,
        "unavailable_features": len(unavailable),
        "raw_selections": raw_count,
        "derivative_matrices": len(matrices),
    }


def audit(
    weighted_path: Path, focused_path: Path, *, branch_limit: int, max_seconds: float
) -> dict[str, object]:
    require(
        math.isfinite(max_seconds) and max_seconds > 0 and 1 <= branch_limit <= 128,
        "invalid wall ceiling or branch limit",
    )
    started, cpu_started = time.monotonic(), time.process_time()
    deadline = started + max_seconds
    require(
        dual.digest(Path(dual.__file__)) == DUAL_CHECKER_SHA,
        "dual residual checker source changed",
    )
    sources = dual.bound_sources()
    require(
        dual.digest(weighted_path) == dual.WEIGHTED_SHA
        and dual.digest(focused_path) == dual.FOCUSED_SHA,
        "proposal source hash mismatch",
    )
    proposal = json.loads(weighted_path.read_text())
    focused = json.loads(focused_path.read_text())
    radii = [Q(value) for value in focused["radii"]]
    require(
        len(radii) == 33 and all(0 < radius <= Q(1, 64) for radius in radii),
        "anisotropic radii outside analytic box",
    )
    denominator, scale = dual.validate_scales(proposal)
    receipts = dual.validate_branch_inventory(proposal)
    phases: dict[str, dict[str, float]] = {}

    def phase(name: str, wall: float, cpu: float) -> None:
        phases[name] = {
            "wall_seconds": time.monotonic() - wall,
            "process_cpu_seconds": time.process_time() - cpu,
        }
        if time.monotonic() > deadline:
            raise TimeoutError(f"local isolation exceeded wall ceiling in {name}")

    wall, cpu = time.monotonic(), time.process_time()
    lo, hi, refinements = dual.root_interval()
    witness = isolation_radius.load_witness()
    require(
        len(witness.squares) == 11
        and len(witness.contacts) == 14
        and len(witness.branches) == 128,
        "exact witness inventory differs",
    )
    side_lower, side_upper = dual.field_interval(witness.side, lo, hi)
    require(0 < side_lower <= side_upper < U, "attaining side does not lie below cap")
    for axis in (0, 1):
        require(
            any(point[axis].is_zero() for square in witness.squares for point in square),
            "lower opposite wall contact missing",
        )
        require(
            any(
                (witness.side - point[axis]).is_zero()
                for square in witness.squares
                for point in square
            ),
            "upper opposite wall contact missing",
        )
    phase("root_witness_endpoint", wall, cpu)
    wall, cpu = time.monotonic(), time.process_time()
    functions = isolation_radius.elementary_functions(witness, Q(1, 64))
    require(len(functions) == 1936, "elementary value-gradient inventory incomplete")
    unavailable, bridge = bridge_features(witness, functions)
    phase("nonlinear_feature_branch_bridge", wall, cpu)
    cache: dict[tuple[Any, ...], tuple[Q, Q]] = {}

    def interval(value: Any) -> tuple[Q, Q]:
        key = tuple(value.coeffs)
        if key not in cache:
            cache[key] = dual.field_interval(value, lo, hi)
        return cache[key]

    root2, inverse_root2 = Q(proposal["sqrt2_upper"]), Q(proposal["inverse_sqrt2_upper"])
    require(
        root2 > 0
        and root2 * root2 > 2
        and inverse_root2 > 0
        and 2 * inverse_root2 * inverse_root2 > 1,
        "uncertified radical bound",
    )
    distances: dict[tuple[int, int], Q] = {}
    velocities: dict[tuple[int, int], Q] = {}

    def curvature(function: isolation_radius.Elementary) -> Q:
        if function.kind == "wall":
            return inverse_root2 * radii[3 * function.subject[0] + 2] ** 2
        first, second, owner = function.subject[:3]
        other = second if owner == first else first
        pair = (first, second)
        if pair not in distances:
            dx = witness.centres[first][0] - witness.centres[second][0]
            dy = witness.centres[first][1] - witness.centres[second][1]
            squared_upper = interval(dx * dx + dy * dy)[1]
            distances[pair] = radical_upper(squared_upper) + 2 * root2 * Q(1, 64)
            vx = radii[3 * first] + radii[3 * second]
            vy = radii[3 * first + 1] + radii[3 * second + 1]
            velocities[pair] = radical_upper(vx * vx + vy * vy)
        owner_angle = radii[3 * owner + 2]
        other_angle = radii[3 * other + 2]
        return (
            distances[pair] * owner_angle**2
            + 2 * velocities[pair] * owner_angle
            + inverse_root2 * (owner_angle + other_angle) ** 2
        )

    wall, cpu = time.monotonic(), time.process_time()
    row_curvature: dict[tuple[Any, ...], Q] = {}
    for function in functions:
        if function.value.is_zero():
            key = signature(function.gradient)
            row_curvature[key] = max(row_curvature.get(key, Q(0)), curvature(function))
    require(
        {contact.pair for contact in witness.contacts} <= set(distances),
        "contact center-distance bounds incomplete",
    )
    phase("exact_anisotropic_curvature", wall, cpu)
    wall, cpu = time.monotonic(), time.process_time()
    gap_records = proposal["unavailable_feature_proofs"]
    require(len(gap_records) == 88, "unavailable feature proposal incomplete")
    seen_features: set[tuple[Any, ...]] = set()
    smallest_gap: Q | None = None
    for item in gap_records:
        key = tuple(item["feature"])
        require(
            key in unavailable and key not in seen_features,
            "duplicate or invalid unavailable feature",
        )
        seen_features.add(key)
        corner = item["negative_corner"]
        require(type(corner) is int and 0 <= corner < 4, "invalid proposed negative corner")
        member = next(
            function for function in unavailable[key] if function.subject[-1] == corner
        )
        upper_value = interval(member.value)[1]
        require(upper_value < 0, "proposed corner is not strictly negative at witness")
        linear = sum(
            (
                max(abs(lower), abs(upper)) * radius
                for (lower, upper), radius in zip(
                    map(interval, member.gradient), radii, strict=True
                )
            ),
            Q(0),
        )
        margin = strict_feature_margin(upper_value, linear, curvature(member))
        smallest_gap = margin if smallest_gap is None else min(smallest_gap, margin)
    require(seen_features == set(unavailable), "unavailable feature inventory incomplete")
    phase("all_88_feature_margins", wall, cpu)
    outcomes: list[dict[str, object]] = []
    worst_ratio = Q(0)
    worst_coordinate: dict[str, int] | None = None
    maximum_radius = max(radii)
    for branch in witness.branches[:branch_limit]:
        index = branch["branch"]
        wall, cpu = time.monotonic(), time.process_time()
        matrix = dual.integer_matrix(branch["rows"], lo, hi, scale)
        coordinates, maximum_error = dual.check_residuals(
            matrix, receipts[index]["certificates"], denominator, scale
        )
        row_bounds = [row_curvature[signature(row.coefficients)] for row in branch["rows"]]
        require(
            len(row_bounds) == 42 and all(bound > 0 for bound in row_bounds),
            "missing positive row curvature",
        )
        for item in receipts[index]["certificates"]:
            coordinate, sign = item["coordinate"], item["sign"]
            error = Q(item["residual_upper"])
            mass = sum(
                (
                    Q(weight, denominator) * bound
                    for weight, bound in zip(item["coefficients"], row_bounds, strict=True)
                ),
                Q(0),
            )
            ratio = strict_dual_margin(radii[coordinate], error, maximum_radius, mass)
            if ratio > worst_ratio:
                worst_ratio = ratio
                worst_coordinate = {"branch": index, "coordinate": coordinate, "sign": sign}
        outcomes.append(
            {
                "branch": index,
                "signed_coordinates_checked": coordinates,
                "maximum_residual": str(maximum_error),
            }
        )
        phase(f"branch_{index}_residual_curvature", wall, cpu)
    require(
        dual.digest(weighted_path) == dual.WEIGHTED_SHA
        and dual.digest(focused_path) == dual.FOCUSED_SHA,
        "proposal source changed during audit",
    )
    require(
        dual.bound_sources() == sources
        and dual.digest(Path(dual.__file__)) == DUAL_CHECKER_SHA,
        "shared exact source changed during audit",
    )
    complete = (
        branch_limit == 128
        and len(outcomes) == 128
        and all(item["signed_coordinates_checked"] == 66 for item in outcomes)
    )
    return {
        "status": "PASS_INDEPENDENT_FIXED_T_LOCAL_ISOLATION"
        if complete
        else "INCOMPLETE_FIXED_T_LOCAL_ISOLATION",
        "fixed_T_local_isolation_proved": complete,
        "pose_inclusion_proved": False,
        "case_438_capture_proved": False,
        "global_optimality_proved": False,
        "scope": (
            "Exact fixed-T labelled Trump pose isolated within the supplied "
            "anisotropic rectangle; source-pose inclusion, case-438 capture, "
            "and global exclusion remain separate premises."
            if complete
            else "Partial exact local audit only; unprocessed branches remain obligations."
        ),
        "source_shared_with_published_checker": True,
        "source_hashes": sources,
        "residual_checker_sha256": DUAL_CHECKER_SHA,
        "checker_sha256": dual.digest(Path(__file__)),
        "input_sha256": {"weighted": dual.WEIGHTED_SHA, "focused": dual.FOCUSED_SHA},
        "root_refinements": refinements,
        "root_interval": [str(lo), str(hi)],
        "features": bridge,
        "center_distance_upper_bounds": len(distances),
        "unavailable_feature_margins_checked": len(seen_features),
        "smallest_unavailable_margin": str(smallest_gap),
        "required_branches": 128,
        "checked_branches": [item["branch"] for item in outcomes],
        "signed_coordinate_margins_checked": sum(
            cast(int, item["signed_coordinates_checked"]) for item in outcomes
        ),
        "worst_dual_ratio": str(worst_ratio),
        "worst_coordinate": worst_coordinate,
        "branch_results": outcomes,
        "phases": phases,
        "wall_seconds": time.monotonic() - started,
        "process_cpu_seconds": time.process_time() - cpu_started,
        "max_seconds": max_seconds,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument("--weighted", type=Path, required=True)
    _ = parser.add_argument("--focused", type=Path, required=True)
    _ = parser.add_argument("--branch-limit", type=int, default=128)
    _ = parser.add_argument("--max-seconds", type=float, default=45.0)
    _ = parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit(
        args.weighted,
        args.focused,
        branch_limit=args.branch_limit,
        max_seconds=args.max_seconds,
    )
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
