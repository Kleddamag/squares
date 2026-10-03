"""Check review S2's two-radius local rectangle with the unchanged fixed-T isolation audit.

The review (S2 and Appendix A.2) replaces the 33 fitted local radii by r = 1/256 for
every center coordinate and every angle, except the angular radii of local labels 9 and
10 (coordinates 29 and 32), which become 2r = 1/128. This module rebuilds that rectangle
deterministically from the accepted focused object, checks in exact arithmetic that
every accepted radius is at most its replacement, and runs the accepted isolation audit
(`devtools.check_n11_optimality_local_isolation`, unedited) on it. The audit pins the
accepted focused digest, so the pin is pointed at the rebuilt object's own pinned digest
for the duration of the call and restored afterwards.

The result is a checked replacement retained beside the accepted local-isolation
component, not in place of it: the proof's rectangle remains the fitted one.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import sys
import tempfile
import time
from collections.abc import Sequence
from fractions import Fraction
from pathlib import Path
from typing import Any

from devtools import check_n11_optimality_local_dual as dual
from devtools import check_n11_optimality_local_isolation as local

Q = Fraction
REPO = Path(__file__).resolve().parents[2]
PACKET = REPO / "packing/resources/web/n11-optimality-2026-09-29"
OBJECTS = PACKET / "receipts/local-dual-residual/objects"
ACCEPTED_FOCUSED_SHA = "9a9cf4e0fdcb1b1d226b9c07ec08d08cbbc572749cec9bc09cf3cd92bd4d88f3"
VARIANT_SHA = "c3395ec46641117e66bea741b2f6348b0a1568fced73ae8a87064a62d8be947d"
BASE_RADIUS = Q(1, 256)
WIDE_COORDINATES = (29, 32)
COMPONENTS = ("x", "y", "theta")
PASS = "PASS_TWO_RADIUS_FIXED_T_LOCAL_ISOLATION"
INCOMPLETE = "INCOMPLETE_TWO_RADIUS_FIXED_T_LOCAL_ISOLATION"
REFUSED = "REFUSED_TWO_RADIUS_FIXED_T_LOCAL_ISOLATION"
PAIR_CONSTANTS = {(1, 1): Q(21, 2), (1, 2): Q(57, 4), (2, 1): Q(99, 4), (2, 2): Q(30)}
WALL_CONSTANTS = {1: Q(3, 4), 2: Q(3)}
SCOPE = (
    "Review S2's two-radius rectangle (every center coordinate 1/256; every angle 1/256 "
    "except local labels 9 and 10 at 1/128), checked by this repository's unchanged "
    "fixed-T isolation audit with its own per-pair curvature bounds. A checked "
    "replacement retained beside the accepted local-isolation component, which it does "
    "not replace: the proof's rectangle remains the fitted one. Pose inclusion in this "
    "larger box follows from the accepted pose-inclusion receipt plus the radius "
    "comparison recorded here. Case-438 capture, the global exclusions, and global "
    "optimality are not checked."
)
POSE_INCLUSION = {
    "proved_here": False,
    "follows_from": [
        "packing/resources/web/n11-optimality-2026-09-29/receipts/pose-inclusion/result.json",
        "radius_comparison",
    ],
    "argument": (
        "Every accepted radius is at most its replacement, so the accepted rectangle lies "
        "inside the two-radius rectangle. The accepted receipt places every live closed "
        "source pose domain in the accepted rectangle, hence in this one."
    ),
}


def require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def decode(path: Path, expected: str) -> bytes:
    raw = gzip.decompress(path.read_bytes())
    require(digest(raw) == expected, f"decoded object digest differs: {path.name}")
    return raw


def replacement_radii() -> list[Q]:
    return [
        2 * BASE_RADIUS if coordinate in WIDE_COORDINATES else BASE_RADIUS
        for coordinate in range(33)
    ]


def radius_comparison(accepted: Sequence[Q], replacement: Sequence[Q]) -> list[dict[str, Any]]:
    """Tabulate each accepted radius against its replacement, refusing any that exceeds it."""
    require(len(accepted) == len(replacement) == 33, "radius vectors must have 33 entries")
    rows = []
    for coordinate, (old, new) in enumerate(zip(accepted, replacement, strict=True)):
        require(
            0 < old <= new <= Q(1, 64),
            f"accepted radius exceeds its replacement at coordinate {coordinate}",
        )
        rows.append(
            {
                "coordinate": coordinate,
                "label": coordinate // 3,
                "component": COMPONENTS[coordinate % 3],
                "accepted": str(old),
                "replacement": str(new),
                "ratio": str(old / new),
            }
        )
    return rows


def serialize(focused: dict[str, Any]) -> bytes:
    return (json.dumps(focused, indent=2) + "\n").encode()


def build_variant(focused_raw: bytes, replacement: Sequence[Q]) -> bytes:
    """Replace the radii list and the per-label inclusion copies; keep every other field."""
    focused = json.loads(focused_raw)
    require(serialize(focused) == focused_raw, "focused object does not reserialize exactly")
    radii = [Q(value) for value in focused["radii"]]
    require(len(radii) == len(replacement) == 33, "radius vectors must have 33 entries")
    inclusion = focused["inclusion"]
    require(
        [record["label"] for record in inclusion] == list(range(11))
        and all(
            [Q(value) for value in record["radii"]]
            == radii[3 * record["label"] : 3 * record["label"] + 3]
            for record in inclusion
        ),
        "per-label inclusion radii differ from the radii list",
    )
    text = [str(value) for value in replacement]
    variant = {
        **focused,
        "radii": text,
        "inclusion": [
            {**record, "radii": text[3 * record["label"] : 3 * record["label"] + 3]}
            for record in inclusion
        ],
    }
    return serialize(variant)


def curvature_constants() -> dict[str, Any]:
    """The review's six closed-form constants and their premises, as exact arithmetic."""
    for (owner, partner), expected in PAIR_CONSTANTS.items():
        value = Q(3, 2) * owner**2 + 6 * owner + Q(3, 4) * (owner + partner) ** 2
        require(value == expected, "review pair curvature constant differs")
    for owner, expected in WALL_CONSTANTS.items():
        require(Q(3, 4) * owner**2 == expected, "review wall curvature constant differs")
    gap = Q(9, 4) - 2 * Q(33, 32) ** 2
    require(gap == Q(63, 512), "center-distance premise differs")
    require(Q(8) < Q(9) and Q(1, 2) < Q(9, 16), "velocity or inverse-root premise fails")
    return {
        "formula_pair": "K_pair <= r^2 (3/2 a^2 + 6 a + 3/4 (a + b)^2), a, b in {1, 2}",
        "formula_wall": "K_wall <= 3/4 a^2 r^2",
        "pair": [
            {"multipliers": [owner, partner], "K_over_r_squared": str(value)}
            for (owner, partner), value in PAIR_CONSTANTS.items()
        ],
        "wall": [
            {"multiplier": owner, "K_over_r_squared": str(value)}
            for owner, value in WALL_CONSTANTS.items()
        ],
        "premises": [
            {
                "claim": "contact-pair center distance (33/32) sqrt(2) < 3/2",
                "exact_check": "2 (33/32)^2 < 9/4",
                "gap": str(gap),
            },
            {"claim": "relative center velocity 2 sqrt(2) r < 3 r", "exact_check": "8 < 9"},
            {"claim": "1/sqrt(2) < 3/4", "exact_check": "1/2 < 9/16"},
        ],
        "used_by_audit": False,
        "note": (
            "The review's coarse constants, checked here as exact arithmetic only. The "
            "audit applies the repository's finer per-pair bounds: the witness center "
            "distance plus 2 sqrt(2)/64 and the exact relative velocity."
        ),
    }


def audited(weighted: Path, focused: Path, *, max_seconds: float) -> dict[str, Any]:
    """Run the unchanged audit with the focused pin pointed at the variant, then restore."""
    require(dual.FOCUSED_SHA == ACCEPTED_FOCUSED_SHA, "focused pin is not the accepted one")
    try:
        dual.FOCUSED_SHA = VARIANT_SHA
        return local.audit(weighted, focused, branch_limit=128, max_seconds=max_seconds)
    finally:
        dual.FOCUSED_SHA = ACCEPTED_FOCUSED_SHA


def check(*, objects: Path = OBJECTS, max_seconds: float) -> dict[str, Any]:
    started = time.monotonic()
    weighted_raw = decode(objects / f"{dual.WEIGHTED_SHA}.gz", dual.WEIGHTED_SHA)
    focused_raw = decode(objects / f"{ACCEPTED_FOCUSED_SHA}.gz", ACCEPTED_FOCUSED_SHA)
    accepted = [Q(value) for value in json.loads(focused_raw)["radii"]]
    replacement = replacement_radii()
    comparison = radius_comparison(accepted, replacement)
    variant = build_variant(focused_raw, replacement)
    require(digest(variant) == VARIANT_SHA, "two-radius variant digest differs from its pin")
    constants = curvature_constants()
    remaining = max_seconds - (time.monotonic() - started)
    require(remaining > 0, "wall ceiling spent before the audit")
    with tempfile.TemporaryDirectory() as scratch:
        weighted_path = Path(scratch) / "weighted.json"
        focused_path = Path(scratch) / "focused-two-radius.json"
        weighted_path.write_bytes(weighted_raw)
        focused_path.write_bytes(variant)
        audit = audited(weighted_path, focused_path, max_seconds=remaining)
    require(
        audit["input_sha256"] == {"weighted": dual.WEIGHTED_SHA, "focused": VARIANT_SHA},
        "audit did not read the two-radius rectangle",
    )
    complete = audit["fixed_T_local_isolation_proved"] is True
    ratio = Q(audit["worst_dual_ratio"])
    return {
        "status": PASS if complete else INCOMPLETE,
        "fixed_T_two_radius_isolation_proved": complete,
        "replaces_accepted_component": False,
        "pose_inclusion_proved": False,
        "case_438_capture_proved": False,
        "global_optimality_proved": False,
        "scope": SCOPE,
        "two_radius_checker_sha256": digest(Path(__file__).read_bytes()),
        "accepted_focused_sha256": ACCEPTED_FOCUSED_SHA,
        "variant_focused_sha256": VARIANT_SHA,
        "weighted_sha256": dual.WEIGHTED_SHA,
        "replacement_rule": {
            "base_radius": str(BASE_RADIUS),
            "wide_radius": str(2 * BASE_RADIUS),
            "wide_coordinates": list(WIDE_COORDINATES),
            "wide_meaning": "angular radii of local labels 9 and 10",
            "changed_fields": ["radii", "inclusion[*].radii"],
        },
        "radius_comparison": comparison,
        "largest_accepted_to_replacement_ratio": str(
            max(Q(row["ratio"]) for row in comparison)
        ),
        "pose_inclusion_in_larger_box": POSE_INCLUSION,
        "review_curvature_constants": constants,
        "worst_dual_ratio": str(ratio),
        "worst_dual_ratio_approx": f"{float(ratio):.12f}",
        "worst_coordinate": audit["worst_coordinate"],
        "signed_coordinate_margins_checked": audit["signed_coordinate_margins_checked"],
        "unavailable_feature_margins_checked": audit["unavailable_feature_margins_checked"],
        "smallest_unavailable_margin_approx": (
            f"{float(Q(audit['smallest_unavailable_margin'])):.12f}"
        ),
        "isolation_audit": audit,
        "wall_seconds": time.monotonic() - started,
        "max_seconds": max_seconds,
    }


def refusal(error: Exception) -> dict[str, Any]:
    return {
        "status": REFUSED,
        "reason": f"{type(error).__name__}: {error}",
        "global_optimality_proved": False,
        "two_radius_checker_sha256": digest(Path(__file__).read_bytes()),
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--objects", type=Path, default=OBJECTS)
    parser.add_argument("--max-seconds", type=float, default=90.0)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        result = check(objects=args.objects, max_seconds=args.max_seconds)
    except (ValueError, KeyError, TypeError, OSError, TimeoutError) as error:
        result = refusal(error)
    rendered = json.dumps(result, indent=2) + "\n"
    if args.output is not None:
        args.output.write_text(rendered)
    print(rendered, end="")
    return 0 if result["status"] == PASS else 1


if __name__ == "__main__":
    sys.exit(main())
