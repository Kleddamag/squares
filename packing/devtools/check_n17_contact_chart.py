"""Exact, preregistered H-254 contact-chart fidelity screen.

The public CLI accepts only the retained H-253 source bytes. ``audit`` and
``reconstruct`` are pure functions so synthetic controls need not read those bytes.
This tests fidelity of one rational witness, never an endpoint or optimum.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, NamedTuple

from devtools.check_rational_witness_independent import pair_gap, square_failures
from devtools.import_half_angle_witness import MAX_SOURCE_BYTES

Point = tuple[Q, Q]
ZERO = Q(0)
ONE = Q(1)
HALF = Q(1, 2)
RESIDUAL_CAP = Q(1, 10**12)
AXIS_MARGIN = Q(1, 10**6)
SIDE = Q(4675530093604551, 10**15)
SOURCE_SHA256 = "24e296f5995abc9424e2d8d39ea0a8e44953b919430a04f006fa84c56fef45f7"
SOURCE_ROW_LABELS = (1, 5, 2, 6, 3, 7, 4, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17)
REPO = Path(__file__).resolve().parents[2]
SOURCE = (
    REPO / "packing/resources/web/n17-kleddamag-certified-bound-2026-09-21/"
    "kleddamag-17-squares-certified-bound/upper-packing-certificate.json"
)


class Pose(NamedTuple):
    x: Q
    y: Q
    t: Q


def dot(a: Point, b: Point) -> Q:
    return a[0] * b[0] + a[1] * b[1]


def sub(a: Point, b: Point) -> Point:
    return a[0] - b[0], a[1] - b[1]


def orientation(t: Q) -> tuple[Point, Point]:
    denominator = 1 + t * t
    u = ((1 - t * t) / denominator, 2 * t / denominator)
    return u, (-u[1], u[0])


def corners(pose: Pose) -> list[Point]:
    u, v = orientation(pose.t)
    return [
        (pose.x - u[0] / 2 - v[0] / 2, pose.y - u[1] / 2 - v[1] / 2),
        (pose.x + u[0] / 2 - v[0] / 2, pose.y + u[1] / 2 - v[1] / 2),
        (pose.x + u[0] / 2 + v[0] / 2, pose.y + u[1] / 2 + v[1] / 2),
        (pose.x - u[0] / 2 + v[0] / 2, pose.y - u[1] / 2 + v[1] / 2),
    ]


def support(t: Q, axis: Point) -> Q:
    u, v = orientation(t)
    return (abs(dot(axis, u)) + abs(dot(axis, v))) / 2


def canonical_axis(axis: Point) -> Point:
    if axis[0] < 0 or (axis[0] == 0 and axis[1] < 0):
        return -axis[0], -axis[1]
    return axis


def distinct_axes(left: Pose, right: Pose) -> tuple[Point, ...]:
    """The distinct unoriented unit SAT axes of two squares."""
    axes = (*orientation(left.t), *orientation(right.t))
    return tuple(dict.fromkeys(canonical_axis(axis) for axis in axes))


def undirected_gap(left: Pose, right: Pose, axis: Point) -> Q:
    displacement = (right.x - left.x, right.y - left.y)
    return abs(dot(axis, displacement)) - support(left.t, axis) - support(right.t, axis)


def directed_gap(left: Pose, right: Pose, axis: Point) -> Q:
    displacement = (right.x - left.x, right.y - left.y)
    return dot(axis, displacement) - support(left.t, axis) - support(right.t, axis)


def chart(side: Q, t: Q, b: Q) -> dict[str, Q | Point]:
    u, v = orientation(t)
    p, q = orientation(-b)
    c, s = u
    d, e = p[0], -p[1]
    h, k = (c + s) / 2, (d + e) / 2
    alpha, gamma = c * d - s * e, c * e + s * d
    if c == 0 or s == 0:
        raise ValueError("chart denominator c or s is zero")
    x = HALF + (2 + c * s + 3 * s - s * side) / c
    y = Q(3, 2) + (2 + 3 * c - c * side) / s
    a = d * (x + HALF) - e * (side - 1) + HALF
    bb = (d + e) * (side - 1) - HALF
    return {
        "u": u,
        "v": v,
        "w": (-v[0], -v[1]),
        "p": p,
        "q": q,
        "c": c,
        "s": s,
        "d": d,
        "e": e,
        "h": h,
        "k": k,
        "alpha": alpha,
        "gamma": gamma,
        "X": x,
        "Y": y,
        "A": a,
        "B": bb,
        "F1": c * (side - 3) + s * (side - 2) - 3,
        "F2": d * (side - x - Q(3, 2)) - e * (y - side + Q(3, 2)) - 1,
        "F3": alpha * (a - HALF) + gamma * (bb - HALF) - (c + 2 * s + 2),
    }


def _number(values: dict[str, Q | Point], key: str) -> Q:
    value = values[key]
    if not isinstance(value, Q):
        raise TypeError(f"{key} is not scalar")
    return value


def _point(values: dict[str, Q | Point], key: str) -> Point:
    value = values[key]
    if not isinstance(value, tuple):
        raise TypeError(f"{key} is not a point")
    return value


def reconstruct(side: Q, t: Q, b: Q, lambda6: Q, lambda13: Q) -> tuple[Point, ...]:
    """H-254's frozen 17-centre table, including its two source sliders."""
    z = chart(side, t, b)
    c, s = _number(z, "c"), _number(z, "s")
    d, e = _number(z, "d"), _number(z, "e")
    h, x, y = _number(z, "h"), _number(z, "X"), _number(z, "Y")
    a, bb = _number(z, "A"), _number(z, "B")
    u10, v10 = Q(3, 2) + c * s + 2 * s, c * (side - 1) - s - HALF
    u11, v11 = c + 2 * s + HALF, 2 * c + (c * c - s * s) / 2 - 1
    u12, v12 = u11 + 1, v10 - 1
    u13 = 2 * c + s + HALF
    u14, v14 = u13 + 1, v10 - 2

    def rotate(uu: Q, vv: Q) -> Point:
        return c * uu - s * vv, s * uu + c * vv

    return (
        (HALF, HALF),
        (Q(3, 2), HALF),
        (HALF, Q(3, 2)),
        (HALF, side - HALF),
        (side - HALF, HALF),
        (lambda6, HALF),
        (side - HALF, Q(3, 2)),
        (side - HALF, side - HALF),
        (h, 2 + h),
        rotate(u10, v10),
        rotate(u11, v11),
        rotate(u12, v12),
        rotate(u13, lambda13),
        rotate(u14, v14),
        (x, side - HALF),
        (d * a + e * bb, -e * a + d * bb),
        (side - HALF, y),
    )


ANCHORS = (
    (1, "left"),
    (1, "bottom"),
    (2, "bottom"),
    (3, "left"),
    (4, "left"),
    (4, "top"),
    (5, "right"),
    (5, "bottom"),
    (6, "bottom"),
    (7, "right"),
    (8, "right"),
    (8, "top"),
    (9, "left"),
    (15, "top"),
    (17, "right"),
)
CONTACTS = (
    (1, 2, "ex", "one"),
    (1, 3, "ey", "one"),
    (5, 7, "ey", "one"),
    (3, 9, "ey", "hhalf"),
    (9, 10, "u", "one"),
    (4, 10, "w", "hhalf"),
    (3, 11, "u", "hhalf"),
    (9, 11, "w", "one"),
    (11, 12, "u", "one"),
    (10, 12, "w", "one"),
    (2, 13, "u", "hhalf"),
    (13, 14, "u", "one"),
    (12, 14, "w", "one"),
    (10, 15, "u", "hhalf"),
    (14, 17, "u", "hhalf"),
    (15, 16, "p", "khalf"),
    (16, 8, "q", "khalf"),
    (14, 7, "w", "hhalf"),
    (16, 17, "p", "khalf"),
    (12, 16, "u", "mixed"),
)


def anchor_gap(pose: Pose, side: Q, wall: str) -> Q:
    ex, ey = (ONE, ZERO), (ZERO, ONE)
    if wall == "left":
        return pose.x - support(pose.t, ex)
    if wall == "right":
        return side - pose.x - support(pose.t, ex)
    if wall == "bottom":
        return pose.y - support(pose.t, ey)
    if wall == "top":
        return side - pose.y - support(pose.t, ey)
    raise ValueError(f"unknown wall {wall}")


def audit(poses: tuple[Pose, ...], side: Q) -> dict[str, Any]:
    """Evaluate every frozen clause and return exact, inspectable residuals."""
    if len(poses) != 17:
        raise ValueError("expected exactly 17 labelled poses")
    t, b = poses[8].t, -poses[15].t
    z = chart(side, t, b)
    axes = {"ex": (ONE, ZERO), "ey": (ZERO, ONE)}
    axes.update({key: _point(z, key) for key in ("u", "w", "p", "q")})
    checks: list[dict[str, Any]] = []

    def record(
        name: str,
        value: Q,
        lower: Q | None,
        upper: Q | None,
        *,
        strict_lower: bool = False,
    ) -> None:
        passed = (lower is None or (value > lower if strict_lower else value >= lower)) and (
            upper is None or value <= upper
        )
        checks.append(
            {
                "name": name,
                "value": str(value),
                "lower": str(lower) if lower is not None else None,
                "strict_lower": strict_lower,
                "upper": str(upper) if upper is not None else None,
                "passed": passed,
            }
        )

    for name, value, low, high in (
        ("S", side, Q(4675, 1000), Q(4676, 1000)),
        ("t", t, Q(36, 100), Q(37, 100)),
        ("b", b, Q(33, 100), Q(34, 100)),
    ):
        record(f"domain.{name}", value, low, high)
    for key in ("c", "s", "d", "e", "alpha", "gamma"):
        record(f"sign.{key}", _number(z, key), Q(0), None, strict_lower=True)
    for label in (*range(1, 9), 15, 17):
        record(f"orientation.{label}", poses[label - 1].t, ZERO, ZERO)
    for label in range(9, 15):
        record(f"orientation.{label}", poses[label - 1].t - t, ZERO, ZERO)

    for label, wall in ANCHORS:
        record(
            f"anchor.{label}.{wall}",
            anchor_gap(poses[label - 1], side, wall),
            ZERO,
            RESIDUAL_CAP,
        )

    support_values = {
        "one": ONE,
        "hhalf": _number(z, "h") + HALF,
        "khalf": _number(z, "k") + HALF,
        "mixed": (ONE + _number(z, "alpha") + _number(z, "gamma")) / 2,
    }
    for left, right, axis_name, support_name in CONTACTS:
        a = axes[axis_name]
        first, second = poses[left - 1], poses[right - 1]
        tag = f"contact.{left}.{right}.{axis_name}"
        support_sum = support(first.t, a) + support(second.t, a)
        record(f"{tag}.support", support_sum - support_values[support_name], ZERO, ZERO)
        record(f"{tag}.gap", directed_gap(first, second, a), ZERO, RESIDUAL_CAP)
        chosen = canonical_axis(a)
        pair_axes = distinct_axes(first, second)
        record(f"{tag}.selected_axis", Q(chosen in pair_axes), ONE, ONE)
        for alternative in pair_axes:
            if alternative != chosen:
                record(
                    f"{tag}.alternative.{alternative[0]}.{alternative[1]}",
                    undirected_gap(first, second, alternative),
                    None,
                    -AXIS_MARGIN,
                )

    x, y, aa, bb = (_number(z, key) for key in ("X", "Y", "A", "B"))
    p, q = _point(z, "p"), _point(z, "q")
    for key in ("F1", "F2", "F3"):
        record(f"equation.{key}", abs(_number(z, key)), ZERO, RESIDUAL_CAP)
    for name, value in (
        ("X", x - poses[14].x),
        ("Y", y - poses[16].y),
        ("A", aa - dot(p, poses[15][:2])),
        ("B", bb - dot(q, poses[15][:2])),
    ):
        record(f"auxiliary.{name}", abs(value), ZERO, RESIDUAL_CAP)

    centres = reconstruct(side, t, b, poses[5].x, dot(_point(z, "v"), poses[12][:2]))
    for label, (source, reconstructed) in enumerate(zip(poses, centres, strict=True), start=1):
        record(f"centre.{label}.x", abs(source.x - reconstructed[0]), ZERO, RESIDUAL_CAP)
        record(f"centre.{label}.y", abs(source.y - reconstructed[1]), ZERO, RESIDUAL_CAP)

    # The three closing-gap identities are exact algebraic controls on the table.
    reconstructed_poses = tuple(
        Pose(*centre, pose.t) for centre, pose in zip(centres, poses, strict=True)
    )
    for (left, right, axis_name, _), key in zip(CONTACTS[-3:], ("F1", "F2", "F3"), strict=True):
        value = directed_gap(
            reconstructed_poses[left - 1], reconstructed_poses[right - 1], axes[axis_name]
        )
        record(f"identity.{key}", value - _number(z, key), ZERO, ZERO)

    squares = [corners(pose) for pose in poses]
    for label, square in enumerate(squares, start=1):
        checks.extend(
            {"name": f"shape.{label}", "value": failure, "passed": False}
            for failure in square_failures(square, label)
        )
        for corner, point in enumerate(square, start=1):
            for axis, coordinate in zip(("x", "y"), point, strict=True):
                record(f"containment.{label}.{corner}.{axis}", coordinate, ZERO, side)
    pairs_tested = 0
    for left, right in itertools.combinations(range(17), 2):
        pairs_tested += 1
        record(
            f"separation.{left + 1}.{right + 1}",
            pair_gap(squares[left], squares[right]),
            ZERO,
            None,
        )

    failed = [check["name"] for check in checks if not check["passed"]]
    return {
        "criterion_passed": not failed,
        "side": str(side),
        "t": str(t),
        "b": str(b),
        "chart": {
            key: str(value) if isinstance(value, Q) else [str(part) for part in value]
            for key, value in z.items()
        },
        "counts": {
            "anchors": len(ANCHORS),
            "selected_contacts": len(CONTACTS),
            "centres": len(centres) * 2,
            "pairs": pairs_tested,
            "checks": len(checks),
            "failed": len(failed),
        },
        "checks": checks,
        "failures": failed,
        "limitations": (
            "Fidelity at one fixed rational witness only; no endpoint or optimality claim."
        ),
    }


def load_frozen_source(path: Path = SOURCE) -> tuple[tuple[Pose, ...], str]:
    """Read only the fixed H-253 source identity and lossless label permutation."""
    with path.open("rb") as stream:
        raw = stream.read(MAX_SOURCE_BYTES + 1)
    if len(raw) > MAX_SOURCE_BYTES:
        raise ValueError("source exceeds fixed input ceiling")
    digest = hashlib.sha256(raw).hexdigest()
    if digest != SOURCE_SHA256:
        raise ValueError(f"source SHA-256 mismatch: {digest}")
    document = json.loads(raw)
    if type(document) is not dict or type(document.get("side")) is not str:
        raise ValueError("source must declare an exact rational side")
    if Q(document["side"]) != SIDE:
        raise ValueError("source side is not the fixed H-253 side")
    entries = document.get("squares")
    if type(entries) is not list or len(entries) != 17:
        raise ValueError("source does not have exactly 17 squares")
    labelled: list[Pose | None] = [None] * 17
    for row, label in zip(entries, SOURCE_ROW_LABELS, strict=True):
        if type(row) is not dict or set(row) != {"x", "y", "t"}:
            raise ValueError("source pose must contain exactly x, y, t")
        if any(type(row[key]) is not str for key in ("x", "y", "t")):
            raise ValueError("source pose coordinates must be exact rational strings")
        labelled[label - 1] = Pose(*(Q(row[key]) for key in ("x", "y", "t")))
    if any(pose is None for pose in labelled):
        raise ValueError("source label map is incomplete")
    return tuple(pose for pose in labelled if pose is not None), digest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--source", type=Path, default=SOURCE)
    options = parser.parse_args(argv)
    try:
        poses, digest = load_frozen_source(options.source)
        result = audit(poses, SIDE)
        result["source"] = {
            "path": str(options.source),
            "sha256": digest,
            "row_to_label": list(SOURCE_ROW_LABELS),
        }
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as error:
        result = {"criterion_passed": False, "refused": str(error)}
        print(json.dumps(result, indent=2, sort_keys=True))
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["criterion_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
