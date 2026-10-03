"""Profile exact n=11 local-dual residuals from source-bound proposals.

This is a partial arithmetic control. It never emits a local-isolation PASS:
curvature, feature stability, and complete branch coverage need separate checks.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import time
from fractions import Fraction
from pathlib import Path
from typing import Any

from cases.trump11 import isolation_radius, packing, tangent_cones
from sqpack import exact_lp, field, verify

Q = Fraction
PACKING = Path(__file__).resolve().parents[1]
WEIGHTED_SHA = "ffe9f89d40a9538ec9a10d8700999f05483d0ccfad17b84d430590da7dd65889"
FOCUSED_SHA = "9a9cf4e0fdcb1b1d226b9c07ec08d08cbbc572749cec9bc09cf3cd92bd4d88f3"
SHARED_SOURCE_PINS = {
    "cases/trump11/packing.py": (
        "3b4eae938c37c13af6252ac5d83fa99aa95f6b1627b99920c5df8be94c56bea9"
    ),
    "cases/trump11/tangent_cones.py": (
        "17302de574d9f7bc377cbc1dc4c537dc60976d6a1e4e63432adb5fa184058765"
    ),
    "cases/trump11/isolation_radius.py": (
        "3b4f754b8a77c0a6edb12a8f669e705594817992f9983956d308aa7b343031b4"
    ),
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bound_sources() -> dict[str, str]:
    modules = {
        "cases/trump11/packing.py": packing,
        "cases/trump11/tangent_cones.py": tangent_cones,
        "cases/trump11/isolation_radius.py": isolation_radius,
        "src/sqpack/field.py": field,
        "src/sqpack/verify.py": verify,
        "src/sqpack/exact_lp.py": exact_lp,
    }
    hashes: dict[str, str] = {}
    for name, module in modules.items():
        path = PACKING / name
        if module.__file__ is None or Path(module.__file__).resolve() != path.resolve():
            raise ValueError("imported exact-geometry module differs from expected source")
        hashes[name] = digest(path)
    if any(hashes[name] != expected for name, expected in SHARED_SOURCE_PINS.items()):
        raise ValueError("shared exact-geometry source differs from published pin")
    return hashes


def polynomial(x: Q) -> Q:
    value = Q(0)
    for coefficient in packing.U_MIN_POLY:
        value = value * x + coefficient
    return value


def root_interval() -> tuple[Q, Q, int]:
    left, right = Q(9, 25), Q(37, 100)
    if not polynomial(left) < 0 < polynomial(right):
        raise ValueError("Trump polynomial does not bracket the claimed root")
    derivative_lower = (
        40 * left**7
        + 70 * left**4
        + 48 * left**3
        + 4 * left
        + 2
        - 70 * right**6
        - 12 * right**5
        - 18 * right**2
    )
    if derivative_lower <= 0:
        raise ValueError("root uniqueness lower derivative bound failed")
    count = 0
    while right - left > Q(1, 10**80):
        middle = (left + right) / 2
        sign = polynomial(middle)
        if sign == 0:
            raise ValueError("unexpected rational Trump root")
        if sign < 0:
            left = middle
        else:
            right = middle
        count += 1
    return left, right, count


def field_interval(value: Any, lo: Q, hi: Q) -> tuple[Q, Q]:
    lower = upper = Q(0)
    for degree, coefficient in enumerate(value.coeffs):
        first = coefficient * lo**degree
        second = coefficient * hi**degree
        lower += min(first, second)
        upper += max(first, second)
    return lower, upper


def integer_matrix(rows: Any, lo: Q, hi: Q, scale: int) -> list[list[int]]:
    result: list[list[int]] = []
    if len(rows) != 42:
        raise ValueError("branch must have 42 rows")
    for row in rows:
        if len(row.coefficients) != 33:
            raise ValueError("branch row must have 33 coordinates")
        integers: list[int] = []
        for coefficient in row.coefficients:
            lower, upper = field_interval(coefficient, lo, hi)
            rounded = round((lower + upper) * scale / 2)
            if not Q(rounded - 1, scale) <= lower <= upper <= Q(rounded + 1, scale):
                raise ValueError("matrix entry approximation error exceeds 1/scale")
            integers.append(rounded)
        result.append(integers)
    return result


def check_residuals(
    matrix: list[list[int]], certificates: list[dict[str, Any]], denominator: int, scale: int
) -> tuple[int, Q]:
    coordinates: set[tuple[int, int]] = set()
    maximum = Q(0)
    for certificate in certificates:
        coordinate, sign = certificate["coordinate"], certificate["sign"]
        if (
            type(coordinate) is not int
            or type(sign) is not int
            or not 0 <= coordinate < 33
            or sign not in (-1, 1)
        ):
            raise ValueError("invalid signed coordinate")
        if (coordinate, sign) in coordinates:
            raise ValueError("duplicate signed coordinate")
        coordinates.add((coordinate, sign))
        weights = certificate["coefficients"]
        if len(weights) != 42 or any(
            type(weight) is not int or weight < 0 for weight in weights
        ):
            raise ValueError("invalid nonnegative dual weights")
        mass = Q(sum(weights), denominator)
        if mass <= 0:
            raise ValueError("zero dual mass")
        residual = 0
        for column in range(33):
            actual = sum(weights[row] * matrix[row][column] for row in range(42))
            target = sign * denominator * scale if column == coordinate else 0
            residual += abs(actual - target)
        error = Q(residual, denominator * scale) + mass * Q(33, scale)
        if not 0 <= error < 1:
            raise ValueError("dual residual does not isolate its coordinate")
        if error != Q(certificate["residual_upper"]):
            raise ValueError("proposed residual does not equal independent integer replay")
        maximum = max(maximum, error)
    required = {(coordinate, sign) for coordinate in range(33) for sign in (-1, 1)}
    if coordinates != required or len(certificates) != 66:
        raise ValueError("signed-coordinate inventory incomplete")
    return len(coordinates), maximum


def validate_scales(proposal: dict[str, Any]) -> tuple[int, int]:
    denominator = proposal["coefficient_denominator"]
    scale = proposal["matrix_approximation_denominator"]
    if type(denominator) is not int or type(scale) is not int or denominator <= 0 or scale <= 0:
        raise ValueError("invalid dual coefficient scales")
    return denominator, scale


def validate_branch_inventory(proposal: dict[str, Any]) -> dict[int, dict[str, Any]]:
    branches = proposal["branches"]
    if not isinstance(branches, list):
        raise TypeError("proposal branch inventory malformed")
    receipts = {item["branch"]: item for item in branches}
    if len(receipts) != len(branches) or set(receipts) != set(range(128)):
        raise ValueError("proposal branch inventory incomplete")
    return receipts


def profile(
    weighted_path: Path, focused_path: Path, *, branch_limit: int, max_seconds: float
) -> dict[str, object]:
    if not math.isfinite(max_seconds) or max_seconds <= 0 or not 1 <= branch_limit <= 128:
        raise ValueError("invalid profile ceiling or branch limit")
    started = time.monotonic()
    cpu_started = time.process_time()
    deadline = started + max_seconds
    source_hashes = bound_sources()
    if digest(weighted_path) != WEIGHTED_SHA or digest(focused_path) != FOCUSED_SHA:
        raise ValueError("proposal input hash mismatch")
    proposal = json.loads(weighted_path.read_text())
    focused = json.loads(focused_path.read_text())
    radii = [Q(value) for value in focused["radii"]]
    if len(radii) != 33 or any(not 0 < radius <= Q(1, 64) for radius in radii):
        raise ValueError("proposed anisotropic radii invalid")
    denominator, scale = validate_scales(proposal)
    phases: dict[str, dict[str, float]] = {}

    def mark(name: str, wall_start: float, cpu_start: float) -> None:
        phases[name] = {
            "wall_seconds": time.monotonic() - wall_start,
            "process_cpu_seconds": time.process_time() - cpu_start,
        }
        if time.monotonic() > deadline:
            raise TimeoutError(f"local dual profile exceeded wall ceiling in {name}")

    wall, cpu = time.monotonic(), time.process_time()
    lo, hi, refinements = root_interval()
    mark("exact_root_isolation", wall, cpu)
    wall, cpu = time.monotonic(), time.process_time()
    witness = isolation_radius.load_witness()
    if len(witness.branches) != 128:
        raise ValueError("exact branch count mismatch")
    mark("shared_source_witness_and_branches", wall, cpu)
    receipts = validate_branch_inventory(proposal)
    outcomes: list[dict[str, object]] = []
    for branch in witness.branches[:branch_limit]:
        index = branch["branch"]
        wall, cpu = time.monotonic(), time.process_time()
        matrix = integer_matrix(branch["rows"], lo, hi, scale)
        mark(f"branch_{index}_matrix", wall, cpu)
        wall, cpu = time.monotonic(), time.process_time()
        checked, maximum = check_residuals(
            matrix, receipts[index]["certificates"], denominator, scale
        )
        mark(f"branch_{index}_residuals", wall, cpu)
        outcomes.append(
            {
                "branch": index,
                "signed_coordinates_checked": checked,
                "maximum_residual": str(maximum),
            }
        )
    if digest(weighted_path) != WEIGHTED_SHA or digest(focused_path) != FOCUSED_SHA:
        raise ValueError("proposal input changed during profile")
    if bound_sources() != source_hashes:
        raise ValueError("exact-geometry source changed during profile")
    return {
        "status": "INCOMPLETE_LOCAL_DUAL_PROFILE",
        "scope": (
            "Selected exact dual residuals only; row curvature, 88 feature margins, "
            "full branch census, local isolation, pose inclusion, and global theorem "
            "are unchecked."
        ),
        "source_shared_with_published_checker": True,
        "source_hashes": source_hashes,
        "input_sha256": {"weighted": WEIGHTED_SHA, "focused": FOCUSED_SHA},
        "checker_sha256": digest(Path(__file__)),
        "root_refinements": refinements,
        "root_interval": [str(lo), str(hi)],
        "required_branches": 128,
        "checked_branches": [item["branch"] for item in outcomes],
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
    _ = parser.add_argument("--branch-limit", type=int, default=1)
    _ = parser.add_argument("--max-seconds", type=float, default=25.0)
    _ = parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = profile(
        args.weighted,
        args.focused,
        branch_limit=args.branch_limit,
        max_seconds=args.max_seconds,
    )
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
