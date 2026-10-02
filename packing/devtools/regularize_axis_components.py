#!/usr/bin/env python3
"""Regularize the axis-aligned components of a witness into an exact derived view.

Usage:
    uv run --frozen --all-extras --group dev python -m devtools.regularize_axis_components \
        witnesses/known-best/n-102.yaml
    uv run --frozen --all-extras --group dev python -m devtools.regularize_axis_components \
        witnesses/known-best/n-102.yaml witnesses/known-best/n-103.yaml \
        --output-dir /some/scratch/dir --json

The atlas shades an axis-aligned square by how many of its four sides are shared with a
wall or a same-angle neighbour, at a gap tolerance of a hundredth of a side.  Many grid
squares in the best-known packings render lighter than their component suggests, because
the retained pose carries slack: a row sits 0.03 from the wall it visibly belongs to, or a
square is a hundredth off the row below it.  This tool builds a *regularized view* of one
witness and checks it exactly:

1. The decimal witness is promoted to the same exact rational pose its certificate was
   built from (`promote_rational` at the certification's digits, centre dilation 1, or
   the rational corners of an already exact witness).  Every square tilted beyond the
   angle snap tolerance keeps that exact pose, unchanged.
2. Every square within the angle snap tolerance of axis alignment is replaced by the
   exactly axis-aligned unit square at the same rational centre, when that is exactly
   feasible.  An exact lattice position needs an exactly axis-aligned square: a square
   tilted by `theta` sticks out past a wall-seated lattice slot by `theta / 2`.
3. Each exactly axis-aligned square slides, one axis at a time, toward the nearest
   lattice position (`1/2 + i` from one wall or `side - 1/2 - j` from the other) and
   stops at the first exact contact.  The slide is accepted when it is a snap (below the
   snap tolerance), when it ends on a wall or an axis-aligned square without lowering the
   square's atlas contact count, or when it raises that count.  Otherwise it is undone.
   Passes repeat until no square moves.
4. The result is verified over `Q` twice: by the repository's exact separating-axis
   verifier and by the independent rational checker that shares no code with it.

The view never replaces the source witness, never changes the certified side, never
promotes an evidence tier, and is written only to the output directory, never under
`witnesses/` or `atlas/`.  A drawing made from it must say it is regularized.
"""

from __future__ import annotations

import argparse
import json
import math
from collections.abc import Sequence
from dataclasses import dataclass, field
from fractions import Fraction
from pathlib import Path
from typing import Any

from strif import atomic_output_file

from devtools import check_rational_witness_independent as independent
from devtools.upper_bound_packets import MAX_SIDE_INCREASE, RATIONAL_DIGITS
from sqpack.verify import separated, verify_packing
from sqpack.witness import WitnessError, load_witness, promote_rational, witness_document

ROOT = Path(__file__).resolve().parent.parent
WITNESS_SCHEMA = ROOT / "witnesses/witness.schema.yaml"
FORBIDDEN_OUTPUT_ROOTS = (ROOT / "witnesses", ROOT / "atlas")
DEFAULT_OUTPUT_DIR = Path(
    "/tmp/claude-0/-home-user-squares/6179239e-fec5-52e8-aabb-a0e229f3f822/scratchpad/regularized"
)
"""The prototype's scratch default; pass `--output-dir` for anything that should last."""

ATLAS_GAP = 0.01
"""The workbench's `CONTACT.gap`: a hundredth of a side, under half a pixel at stage size."""
ATLAS_ANGLE_TOLERANCE_DEGREES = 0.5
"""The workbench's angle tolerance, the same the angle classes are seeded with."""
ATLAS_ANGLE_TOLERANCE_RADIANS = math.radians(ATLAS_ANGLE_TOLERANCE_DEGREES)
ANGLE_SNAP_TOLERANCE_RADIANS = 1e-4
"""Squares tilted less than this are straightened exactly; more is a real rotation."""
SNAP_TOLERANCE = Fraction("1e-9")
"""A move of at most this is a snap, accepted without a contact-count argument."""
PASS_CAP_MARGIN = 2
"""Passes beyond the square count before the fixpoint loop gives up."""

HALF = Fraction(1, 2)
QUARTER_TURN = math.pi / 2

Point = tuple[Fraction, Fraction]
Corners = list[Point]
Direction = tuple[int, int]

AXES: tuple[tuple[str, int], ...] = (("x", 0), ("y", 1))
FACES: tuple[tuple[str, Direction], ...] = (
    ("left", (-1, 0)),
    ("right", (1, 0)),
    ("bottom", (0, -1)),
    ("top", (0, 1)),
)


class RegularizeError(ValueError):
    """A typed refusal: the witness cannot be regularized exactly, and this says why."""

    def __init__(self, kind: str, detail: str):
        super().__init__(detail)
        self.kind = kind


# --------------------------------------------------------------------------------------
# Rational geometry
# --------------------------------------------------------------------------------------


def rational_sign(value: Fraction) -> int:
    return (value > 0) - (value < 0)


def centre(corners: Corners) -> Point:
    return (
        sum((x for x, _ in corners), Fraction(0)) / 4,
        sum((y for _, y in corners), Fraction(0)) / 4,
    )


def bounding_box(corners: Corners) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    xs = [x for x, _ in corners]
    ys = [y for _, y in corners]
    return min(xs), max(xs), min(ys), max(ys)


def axis_square(center: Point) -> Corners:
    """The exactly axis-aligned unit square at `center`, counter-clockwise from lower-left."""
    cx, cy = center
    return [
        (cx - HALF, cy - HALF),
        (cx + HALF, cy - HALF),
        (cx + HALF, cy + HALF),
        (cx - HALF, cy + HALF),
    ]


def translate(corners: Corners, direction: Direction, distance: Fraction) -> Corners:
    dx, dy = direction
    return [(x + dx * distance, y + dy * distance) for x, y in corners]


def is_exact_axis(corners: Corners) -> bool:
    (ax, ay), (bx, by) = corners[0], corners[1]
    return (ax == bx) or (ay == by)


def _edge_normals(corners: Corners) -> list[Point]:
    normals: list[Point] = []
    for k in (0, 1):
        (px, py), (qx, qy) = corners[k], corners[k + 1]
        normals.append((-(qy - py), qx - px))
    return normals


def _projection(corners: Corners, axis: Point) -> tuple[Fraction, Fraction]:
    values = [axis[0] * x + axis[1] * y for x, y in corners]
    return min(values), max(values)


def interior_overlap_interval(
    moving: Corners, direction: Direction, fixed: Corners
) -> tuple[Fraction, Fraction] | None:
    """The open interval of slide distances at which the two interiors overlap.

    `moving + t * direction` and `fixed` have overlapping interiors exactly when every
    edge-normal axis of either square sees their projections overlap as open intervals.
    Each axis contributes one open interval of `t` (or everything, or nothing); the
    answer is their intersection, `None` when it is empty.  Exact over the rationals,
    which is what lets a slide stop at a zero gap without calling it an overlap.
    """
    low: Fraction | None = None
    high: Fraction | None = None
    for axis in _edge_normals(moving) + _edge_normals(fixed):
        a_lo, a_hi = _projection(moving, axis)
        b_lo, b_hi = _projection(fixed, axis)
        speed = direction[0] * axis[0] + direction[1] * axis[1]
        if speed == 0:
            if a_lo < b_hi and b_lo < a_hi:
                continue
            return None
        enter, leave = (b_lo - a_hi) / speed, (b_hi - a_lo) / speed
        if speed < 0:
            enter, leave = leave, enter
        low = enter if low is None else max(low, enter)
        high = leave if high is None else min(high, leave)
    if low is None or high is None or low >= high:
        return None
    return low, high


@dataclass(frozen=True)
class Blocker:
    kind: str
    """`wall`, `square`, or `target`."""
    name: str


def slide_limit(
    moving: Corners,
    direction: Direction,
    distance: Fraction,
    others: Sequence[tuple[str, Corners]],
    side: Fraction,
) -> tuple[Fraction, list[Blocker]]:
    """How far `moving` may slide along `direction`, and what it then touches.

    Returns the exact distance, at most `distance`, and every blocker in contact at
    that distance: the wall or squares that stop the slide, or `target` alone when
    nothing does.  A square already overlapping is reported as a zero slide.
    """
    limit = distance
    blockers: list[Blocker] = [Blocker("target", "")]
    min_x, max_x, min_y, max_y = bounding_box(moving)
    dx, dy = direction
    wall_room = {
        (-1, 0): min_x,
        (1, 0): side - max_x,
        (0, -1): min_y,
        (0, 1): side - max_y,
    }[direction]
    wall_name = {(-1, 0): "x=0", (1, 0): "x=s", (0, -1): "y=0", (0, 1): "y=s"}[direction]
    if wall_room < limit:
        limit, blockers = wall_room, [Blocker("wall", wall_name)]
    elif wall_room == limit:
        blockers.append(Blocker("wall", wall_name))
    swept = (
        min(min_x, min_x + dx * distance),
        max(max_x, max_x + dx * distance),
        min(min_y, min_y + dy * distance),
        max(max_y, max_y + dy * distance),
    )
    for name, fixed in others:
        o_min_x, o_max_x, o_min_y, o_max_y = bounding_box(fixed)
        # Boxes that only touch the swept box are kept: a slide that ends in exact
        # contact must report what it touches, which is how a move is judged.
        if o_max_x < swept[0] or o_min_x > swept[1] or o_max_y < swept[2] or o_min_y > swept[3]:
            continue
        window = interior_overlap_interval(moving, direction, fixed)
        if window is None:
            continue
        enter, leave = window
        if leave <= 0:
            continue
        room = max(enter, Fraction(0))
        if room < limit:
            limit, blockers = room, [Blocker("square", name)]
        elif room == limit:
            blockers.append(Blocker("square", name))
    if limit == distance and blockers and blockers[0].kind != "target":
        blockers.insert(0, Blocker("target", ""))
    return limit, blockers


def lattice_target(coordinate: Fraction, side: Fraction) -> Fraction:
    """The nearest lattice centre, seated from either wall; ties go to the origin side."""
    slots = math.floor(side - 1)
    if slots < 0:
        return coordinate
    low_index = min(max(round(coordinate - HALF), 0), slots)
    high_index = min(max(round(side - HALF - coordinate), 0), slots)
    low = HALF + low_index
    high = side - HALF - high_index
    return low if abs(coordinate - low) <= abs(coordinate - high) else high


# --------------------------------------------------------------------------------------
# The atlas rule, in the workbench's own arithmetic
# --------------------------------------------------------------------------------------


def angle_gap(angle: float) -> float:
    """Distance of an angle from the nearest quarter-turn multiple, as the atlas folds it."""
    distance = math.fmod(abs(angle), QUARTER_TURN)
    return min(distance, QUARTER_TURN - distance)


Pose = tuple[float, float, float]
"""A square's centre and angle in radians, in binary64, as the workbench holds them."""


def _shares_side(first: Pose, second: Pose, gap: float) -> bool:
    dx, dy = second[0] - first[0], second[1] - first[1]
    cosine, sine = math.cos(first[2]), math.sin(first[2])
    along = dx * cosine + dy * sine
    across = -dx * sine + dy * cosine
    return (abs(abs(along) - 1) <= gap and abs(across) <= gap) or (
        abs(abs(across) - 1) <= gap and abs(along) <= gap
    )


def atlas_contacts(
    poses: Sequence[Pose],
    side: float,
    *,
    gap: float = ATLAS_GAP,
    angle_tolerance: float = ATLAS_ANGLE_TOLERANCE_RADIANS,
) -> list[int]:
    """Full-side contact counts under the workbench rule (`core/geometry.ts`, `contactFacts`).

    Walls count only for a square within the angle tolerance of axis alignment; a pair
    counts when both fold to the same angle class and one centre offset is a side and
    the other nothing, each within `gap`; the count is capped at four.
    """
    counts = [0] * len(poses)
    for index, (x, y, angle) in enumerate(poses):
        if angle_gap(angle) > angle_tolerance:
            continue
        counts[index] = sum(
            (
                abs(x - 0.5) <= gap,
                abs(x - (side - 0.5)) <= gap,
                abs(y - 0.5) <= gap,
                abs(y - (side - 0.5)) <= gap,
            )
        )
    for left in range(len(poses)):
        for right in range(left + 1, len(poses)):
            if _atlas_pair(poses[left], poses[right], gap, angle_tolerance):
                counts[left] = min(4, counts[left] + 1)
                counts[right] = min(4, counts[right] + 1)
    return counts


def _atlas_pair(first: Pose, second: Pose, gap: float, angle_tolerance: float) -> bool:
    dx, dy = second[0] - first[0], second[1] - first[1]
    if dx * dx + dy * dy > 2.5:
        return False
    if angle_gap(first[2] - second[2]) > angle_tolerance:
        return False
    return _shares_side(first, second, gap)


def atlas_count_of(index: int, poses: Sequence[Pose], side: float) -> int:
    """One square's count under the same rule, for deciding a single move."""
    x, y, angle = poses[index]
    count = 0
    if angle_gap(angle) <= ATLAS_ANGLE_TOLERANCE_RADIANS:
        count = sum(
            (
                abs(x - 0.5) <= ATLAS_GAP,
                abs(x - (side - 0.5)) <= ATLAS_GAP,
                abs(y - 0.5) <= ATLAS_GAP,
                abs(y - (side - 0.5)) <= ATLAS_GAP,
            )
        )
    for other, pose in enumerate(poses):
        if other != index and _atlas_pair(
            poses[index], pose, ATLAS_GAP, ATLAS_ANGLE_TOLERANCE_RADIANS
        ):
            count = min(4, count + 1)
    return count


def pose_of(corners: Corners) -> Pose:
    cx, cy = centre(corners)
    (ax, ay), (bx, by) = corners[0], corners[1]
    angle = 0.0 if is_exact_axis(corners) else math.atan2(float(by - ay), float(bx - ax))
    return float(cx), float(cy), angle


# --------------------------------------------------------------------------------------
# Loading: the exact frame a witness can be regularized in
# --------------------------------------------------------------------------------------


@dataclass
class Piece:
    square_id: str
    corners: Corners
    source_angle: float
    """The retained angle in radians, folded to its distance from axis alignment."""
    status: str = "tilted"
    """`tilted`, `atlas-axis-untouched`, `exact-axis`, or `rotation-blocked`."""
    moves: list[dict[str, Any]] = field(default_factory=list)

    @property
    def atlas_axis(self) -> bool:
        return self.source_angle <= ATLAS_ANGLE_TOLERANCE_RADIANS

    @property
    def exact_axis(self) -> bool:
        return self.status == "exact-axis"


@dataclass
class ExactFrame:
    pieces: list[Piece]
    side: Fraction
    reported_side: Fraction
    before: list[Pose]
    """The retained witness as the atlas draws it: binary64 centres and angles, lower-left."""
    provenance: dict[str, Any]


def _witness_poses(witness: dict[str, Any]) -> list[Pose]:
    """The retained pose in the workbench's arithmetic, shifted to a lower-left origin."""
    side = float(Fraction(str(witness["side"])))
    shift = side / 2 if witness["coordinates"]["origin"] == "container-center" else 0.0
    unit = witness["coordinates"]["angle_unit"]
    poses: list[Pose] = []
    for square in witness["squares"]:
        if witness["representation"] == "corners":
            corners = [(Fraction(str(x)), Fraction(str(y))) for x, y in square["corners"]]
            x, y, angle = pose_of(corners)
            poses.append((x + shift, y + shift, angle))
            continue
        x, y = (float(Fraction(str(value))) for value in square["center"])
        if witness["representation"] == "center-angle":
            angle = float(Fraction(str(square["angle"])))
            angle = math.radians(angle) if unit == "degrees" else angle
        else:
            angle = math.atan2(
                float(Fraction(str(square["basis"][1]))),
                float(Fraction(str(square["basis"][0]))),
            )
        poses.append((x + shift, y + shift, angle))
    return poses


def exact_frame(witness: dict[str, Any], source_path: str) -> ExactFrame:
    """The exact rational pose this witness is regularized from, and where it came from."""
    kind = witness["scalar"]["kind"]
    reported_side = Fraction(str(witness["side"]))
    before = _witness_poses(witness)
    if kind == "rational":
        if witness["representation"] != "corners":
            raise RegularizeError(
                "unsupported-representation",
                "a rational witness is regularized from its corners; this one has "
                f"{witness['representation']!r}",
            )
        shift = (
            reported_side / 2 if witness["coordinates"]["origin"] == "container-center" else 0
        )
        pieces = [
            Piece(
                str(square["id"]),
                [(Fraction(x) + shift, Fraction(y) + shift) for x, y in square["corners"]],
                angle_gap(pose[2]),
            )
            for square, pose in zip(witness["squares"], before, strict=True)
        ]
        provenance = {
            "kind": "rational",
            "derivation": "the witness's own rational corners",
            "certified_side": str(reported_side),
            "center_dilation": "1",
        }
        return ExactFrame(pieces, reported_side, reported_side, before, provenance)
    if kind != "decimal":
        raise RegularizeError(
            "unsupported-scalar-kind",
            f"{kind!r} geometry has no exact rational frame here: an enclosure proves no "
            "equality and an algebraic field needs field arithmetic this prototype lacks",
        )
    try:
        result, promoted = promote_rational(
            witness,
            rational_digits=RATIONAL_DIGITS,
            max_side_increase=MAX_SIDE_INCREASE,
            source_path=source_path,
            replay_path=source_path,
        )
    except WitnessError as error:
        raise RegularizeError(
            "promotion-failed",
            f"no exact rational pose at dilation 1 within {MAX_SIDE_INCREASE}: {error}",
        ) from error
    if result["center_dilation"] != "1":
        raise RegularizeError(
            "promotion-dilated",
            f"the exact pose needed centre dilation {result['center_dilation']}, so it is "
            "not the author's packing and is not regularized",
        )
    side = Fraction(promoted["side"])
    pieces = [
        Piece(
            str(square["id"]),
            [(Fraction(x), Fraction(y)) for x, y in square["corners"]],
            angle_gap(pose[2]),
        )
        for square, pose in zip(promoted["squares"], before, strict=True)
    ]
    provenance = {
        "kind": "rational",
        "derivation": (
            "promote_rational in process, the procedure upper_bound_packets certify uses"
        ),
        "rational_digits": RATIONAL_DIGITS,
        "max_side_increase": MAX_SIDE_INCREASE,
        "center_dilation": result["center_dilation"],
        "certified_side": str(side),
        "certified_side_decimal": result["side_decimal"],
    }
    return ExactFrame(pieces, side, reported_side, before, provenance)


# --------------------------------------------------------------------------------------
# Regularization
# --------------------------------------------------------------------------------------


def _feasible(index: int, corners: Corners, pieces: Sequence[Piece], side: Fraction) -> bool:
    """Whether `corners` in place of piece `index` is exactly inside and interior-disjoint."""
    min_x, max_x, min_y, max_y = bounding_box(corners)
    if min_x < 0 or min_y < 0 or max_x > side or max_y > side:
        return False
    for other, piece in enumerate(pieces):
        if other == index:
            continue
        o_min_x, o_max_x, o_min_y, o_max_y = bounding_box(piece.corners)
        if o_max_x <= min_x or o_min_x >= max_x or o_max_y <= min_y or o_min_y >= max_y:
            continue
        if separated(corners, piece.corners, rational_sign) is None:
            return False
    return True


def straighten(pieces: list[Piece], side: Fraction, *, angle_snap: float) -> None:
    """Replace every nearly axis-aligned square by the exact one at its centre, when feasible.

    All candidates are straightened together first, because two squares in exact contact
    in the certificate may each block the other's straightening alone and not together.
    If the joint replacement fails, each candidate is tried on its own in id order and
    the ones that fail are kept as the certificate has them.
    """
    candidates = [
        index for index, piece in enumerate(pieces) if piece.source_angle <= angle_snap
    ]
    proposed = {index: axis_square(centre(pieces[index].corners)) for index in candidates}
    trial = [
        Piece(p.square_id, proposed.get(i, p.corners), p.source_angle)
        for i, p in enumerate(pieces)
    ]
    if all(_feasible(index, trial[index].corners, trial, side) for index in candidates):
        for index in candidates:
            pieces[index].corners = proposed[index]
            pieces[index].status = "exact-axis"
    else:
        for index in candidates:
            if _feasible(index, proposed[index], pieces, side):
                pieces[index].corners = proposed[index]
                pieces[index].status = "exact-axis"
            else:
                pieces[index].status = "rotation-blocked"
    for piece in pieces:
        if piece.status == "tilted" and piece.atlas_axis:
            piece.status = "atlas-axis-untouched"


def _attempt_slide(
    index: int,
    axis: int,
    pieces: list[Piece],
    side: Fraction,
    *,
    snap_tolerance: Fraction,
) -> dict[str, Any] | None:
    """Slide one square along one axis toward its lattice target; return the move or None."""
    piece = pieces[index]
    position = centre(piece.corners)[axis]
    target = lattice_target(position, side)
    if target == position:
        return None
    sign = 1 if target > position else -1
    direction: Direction = (sign, 0) if axis == 0 else (0, sign)
    distance = abs(target - position)
    others = [(p.square_id, p.corners) for i, p in enumerate(pieces) if i != index]
    limit, blockers = slide_limit(piece.corners, direction, distance, others, side)
    if limit == 0:
        return None
    moved = translate(piece.corners, direction, limit)
    poses = [pose_of(p.corners) for p in pieces]
    before = atlas_count_of(index, poses, float(side))
    poses[index] = pose_of(moved)
    after = atlas_count_of(index, poses, float(side))
    by_id = {p.square_id: p for p in pieces}
    ends_on_face = any(
        b.kind == "wall" or (b.kind == "square" and by_id[b.name].exact_axis) for b in blockers
    )
    kind = "snap" if limit <= snap_tolerance else "compaction"
    accepted = kind == "snap" or after > before or (after >= before and ends_on_face)
    move = {
        "axis": "xy"[axis],
        "direction": sign,
        "distance": str(limit),
        "distance_decimal": f"{float(limit):.3e}",
        "reached_target": limit == distance,
        "blockers": [f"{b.kind}:{b.name}" if b.name else b.kind for b in blockers],
        "kind": kind,
        "contacts_before": before,
        "contacts_after": after,
        "accepted": accepted,
    }
    if accepted:
        piece.corners = moved
    return move


def compact(
    pieces: list[Piece], side: Fraction, *, snap_tolerance: Fraction, max_passes: int
) -> dict[str, Any]:
    """Slide exact axis-aligned squares toward lattice positions until nothing moves."""
    order = sorted(
        (i for i, p in enumerate(pieces) if p.exact_axis),
        key=lambda i: (_wall_distance(pieces[i].corners, side), pieces[i].square_id),
    )
    passes = 0
    converged = False
    accepted = rejected = snaps = compactions = 0
    largest = Fraction(0)
    while passes < max_passes:
        passes += 1
        moved_any = False
        for index in order:
            for _name, axis in AXES:
                move = _attempt_slide(index, axis, pieces, side, snap_tolerance=snap_tolerance)
                if move is None:
                    continue
                if move["accepted"] or move not in pieces[index].moves:
                    pieces[index].moves.append(move)
                if move["accepted"]:
                    moved_any = True
                    accepted += 1
                    if move["kind"] == "snap":
                        snaps += 1
                    else:
                        compactions += 1
                    largest = max(largest, Fraction(move["distance"]))
                else:
                    rejected += 1
        if not moved_any:
            converged = True
            break
    return {
        "passes": passes,
        "converged": converged,
        "accepted": accepted,
        "snaps": snaps,
        "compactions": compactions,
        "rejected": rejected,
        "largest_move": str(largest),
        "largest_move_decimal": f"{float(largest):.3e}",
    }


def _wall_distance(corners: Corners, side: Fraction) -> Fraction:
    min_x, max_x, min_y, max_y = bounding_box(corners)
    return min(min_x, min_y, side - max_x, side - max_y)


def histogram(counts: Sequence[int]) -> list[int]:
    """How many squares carry each contact count from zero to four."""
    return [sum(1 for count in counts if count == k) for k in range(5)]


# --------------------------------------------------------------------------------------
# Classifying what stays light
# --------------------------------------------------------------------------------------


def _face_contact(index: int, face: Direction, poses: Sequence[Pose], side: float) -> bool:
    x, y, _angle = poses[index]
    fx, fy = face
    if fx and abs(x - (0.5 if fx < 0 else side - 0.5)) <= ATLAS_GAP:
        return True
    if fy and abs(y - (0.5 if fy < 0 else side - 0.5)) <= ATLAS_GAP:
        return True
    for other, pose in enumerate(poses):
        if other == index or angle_gap(pose[2]) > ATLAS_ANGLE_TOLERANCE_RADIANS:
            continue
        dx, dy = pose[0] - x, pose[1] - y
        along, across = (dx, dy) if fx else (dy, dx)
        if abs(along - (fx or fy)) <= ATLAS_GAP and abs(across) <= ATLAS_GAP:
            return True
    return False


def at_lattice(piece: Piece, side: Fraction, axis: int) -> bool:
    """Whether the square's centre sits exactly on its nearest lattice position on `axis`."""
    position = centre(piece.corners)[axis]
    return lattice_target(position, side) == position


def classify_face(
    index: int, face: Direction, pieces: Sequence[Piece], poses: Sequence[Pose], side: Fraction
) -> str:
    """Why a face of an exact axis-aligned square has no counted contact.

    The face is pushed outward by up to one side with the same exact slide the
    compaction uses, and what stops it decides the label.  `hole`: nothing within a side,
    or a wall or an aligned axis-aligned square further than the gap while every square
    involved already sits on its lattice, so the gap is the mismatch between the two
    wall-seated lattices and no slide closes it.  `tilted-neighbour`: the first thing in
    front is a square outside the atlas angle tolerance.  `offset`: an axis-aligned
    square is in front but shifted across by more than the gap.  `slack`: an aligned
    axis-aligned square is in front, further than the gap, and one of the two is off its
    lattice, so a compaction was blocked or refused.  `wall-slack`: the same for a wall.
    `untouched-neighbour`: the square in front is one the atlas calls axis-aligned but the
    source tilts beyond the snap tolerance, so it was left as certified.  A gap wider
    than half a side is a hole whatever is behind it: no lattice slot fits in it.
    """
    piece = pieces[index]
    others = [(p.square_id, p.corners) for i, p in enumerate(pieces) if i != index]
    limit, blockers = slide_limit(piece.corners, face, Fraction(1), others, side)
    stops = [b for b in blockers if b.kind != "target"]
    if limit >= 1 or not stops:
        return "hole"
    axis = 0 if face[0] else 1
    seated = at_lattice(piece, side, axis)
    if any(b.kind == "wall" for b in stops):
        return "hole" if seated or limit > HALF else "wall-slack"
    by_id = {p.square_id: (i, p) for i, p in enumerate(pieces)}
    other, neighbour = by_id[stops[0].name]
    if not neighbour.atlas_axis:
        return "tilted-neighbour"
    if not neighbour.exact_axis:
        return "untouched-neighbour"
    across = abs(poses[other][1 - axis] - poses[index][1 - axis])
    if across > ATLAS_GAP:
        return "offset"
    both_seated = seated and at_lattice(neighbour, side, axis)
    return "hole" if both_seated or limit > HALF else "slack"


# --------------------------------------------------------------------------------------
# The whole operation
# --------------------------------------------------------------------------------------


def regularized_witness(
    witness: dict[str, Any], frame: ExactFrame, *, summary: dict[str, Any]
) -> dict[str, Any]:
    """The regularized view as a Witness/v2 record: rational corners, verified, derived."""

    def literal(value: Fraction) -> str:
        return (
            str(value.numerator)
            if value.denominator == 1
            else f"{value.numerator}/{value.denominator}"
        )

    retained = witness.get("source") or {}
    source = {"path": str(retained.get("path") or "unrecorded")}
    for key in ("key", "url", "retrieved"):
        value = retained.get(key)
        if isinstance(value, str) and value:
            source[key] = value
    return {
        "id": f"{witness['id']}-regularized",
        "n": witness["n"],
        "side": literal(frame.side),
        "square_size": "1",
        "representation": "corners",
        "scalar": {"kind": "rational"},
        "coordinates": {
            "origin": "lower-left",
            "axes": "x-right-y-up",
            "angle_unit": "not-applicable",
        },
        "squares": [
            {
                "id": witness["squares"][i]["id"],
                "corners": [[literal(x), literal(y)] for x, y in p.corners],
            }
            for i, p in enumerate(frame.pieces)
        ],
        "claim": {
            "coordinate_provenance": "verified",
            "method": "exact-algebraic",
            "limitations": (
                "A regularized derived view for drawing, not the source witness: tilted "
                "squares keep their certified exact pose, nearly axis-aligned squares are "
                "straightened and slid into exact lattice or face contact, and the container "
                "side is the exact certificate's. It changes no frontier value, promotes no "
                "evidence tier, and any drawing made from it must say it is regularized."
            ),
        },
        "source": source,
        "certificate": {
            "kind": "regularized-view",
            "derived_from": witness["id"],
            "exact_frame": frame.provenance,
            "regularization": summary,
            "replay": "uv run --frozen packing-witness verify <this file>",
        },
    }


def regularize(
    witness: dict[str, Any],
    *,
    source_path: str,
    angle_snap: float = ANGLE_SNAP_TOLERANCE_RADIANS,
    snap_tolerance: Fraction = SNAP_TOLERANCE,
    max_passes: int | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Regularize one witness; return the report and the regularized Witness/v2 record."""
    frame = exact_frame(witness, source_path)
    pieces = frame.pieces
    side = frame.side
    straighten(pieces, side, angle_snap=angle_snap)
    passes = max_passes if max_passes is not None else len(pieces) + PASS_CAP_MARGIN
    moves = compact(pieces, side, snap_tolerance=snap_tolerance, max_passes=passes)

    after_poses = [pose_of(p.corners) for p in pieces]
    counts_before = atlas_contacts(frame.before, float(frame.reported_side))
    counts_after = atlas_contacts(after_poses, float(side))
    report = verify_packing([p.corners for p in pieces], side, sign=rational_sign, bucket=True)

    per_square: list[dict[str, Any]] = []
    structural: dict[str, int] = {}
    became_dark = became_lighter = 0
    light_before = light_after = 0
    for index, piece in enumerate(pieces):
        entry: dict[str, Any] = {
            "id": piece.square_id,
            "status": piece.status,
            "source_angle_from_axis": f"{piece.source_angle:.3e}",
            "contacts_before": counts_before[index],
            "contacts_after": counts_after[index],
            "moves": [m for m in piece.moves if m["accepted"]],
            "rejected_moves": [m for m in piece.moves if not m["accepted"]],
        }
        if piece.atlas_axis:
            light_before += counts_before[index] < 4
            light_after += counts_after[index] < 4
            if counts_before[index] < 4 and counts_after[index] == 4:
                became_dark += 1
            if counts_after[index] < counts_before[index]:
                became_lighter += 1
            if piece.exact_axis and counts_after[index] < 4:
                faces = {
                    name: classify_face(index, face, pieces, after_poses, side)
                    for name, face in FACES
                    if not _face_contact(index, face, after_poses, float(side))
                }
                entry["light_faces"] = faces
                for reason in faces.values():
                    structural[reason] = structural.get(reason, 0) + 1
        per_square.append(entry)

    statuses: dict[str, int] = {}
    for piece in pieces:
        statuses[piece.status] = statuses.get(piece.status, 0) + 1
    summary = {
        "angle_snap_tolerance_radians": angle_snap,
        "snap_tolerance": str(snap_tolerance),
        "statuses": statuses,
        "moves": moves,
        "exact_contacts_after": report.touching_pairs,
    }
    result = {
        "operation": "regularize",
        "source": {
            "id": witness["id"],
            "path": source_path,
            "n": witness["n"],
            "reported_side": str(frame.reported_side),
            "scalar_kind": witness["scalar"]["kind"],
            "representation": witness["representation"],
            "coordinate_provenance": witness["claim"]["coordinate_provenance"],
            "method": witness["claim"]["method"],
        },
        "exact_frame": {
            **frame.provenance,
            "side_minus_reported": str(side - frame.reported_side),
            "side_minus_reported_decimal": f"{float(side - frame.reported_side):.3e}",
            "fits_reported_side": side <= frame.reported_side,
        },
        "atlas_rule": {
            "gap": ATLAS_GAP,
            "angle_tolerance_degrees": ATLAS_ANGLE_TOLERANCE_DEGREES,
            "walls": "axis-aligned squares only",
            "cap": 4,
        },
        "regularization": summary,
        "atlas_contacts": {
            "axis_aligned_squares": sum(1 for p in pieces if p.atlas_axis),
            "light_before": light_before,
            "light_after": light_after,
            "became_dark": became_dark,
            "became_lighter": became_lighter,
            "histogram_before": histogram(counts_before),
            "histogram_after": histogram(counts_after),
            "total_before": sum(counts_before),
            "total_after": sum(counts_after),
        },
        "structural_light_faces": dict(sorted(structural.items())),
        "exact_verification": {
            "arithmetic": "rational (fractions.Fraction), exact separating-axis predicates",
            "repository_verifier": {
                "valid": report.valid,
                "pairs_tested": report.pairs_tested,
                "touching_pairs": report.touching_pairs,
                "container_contacts": report.container_contacts,
                "failures": report.failures[:10],
            },
        },
        "squares": per_square,
        "claim_boundary": (
            "Derived view only. Same n, the certificate's exact side (never larger than "
            "the verified upper bound), tilted squares unchanged from the certificate. Not "
            "the source witness, not a frontier change, not an evidence-tier promotion; a "
            "drawing of it must say it is regularized."
        ),
    }
    return result, regularized_witness(witness, frame, summary=summary)


# --------------------------------------------------------------------------------------
# Command line
# --------------------------------------------------------------------------------------


def _guard_output_dir(output_dir: Path) -> Path:
    resolved = output_dir.resolve()
    for forbidden in FORBIDDEN_OUTPUT_ROOTS:
        if resolved == forbidden.resolve() or forbidden.resolve() in resolved.parents:
            raise RegularizeError(
                "forbidden-output",
                "a regularized view is a derived artifact and may not be written under "
                f"{forbidden}",
            )
    return resolved


def run_one(
    path: Path,
    output_dir: Path,
    *,
    angle_snap: float,
    snap_tolerance: Fraction,
    max_passes: int | None,
) -> dict[str, Any]:
    witness = load_witness(path, fallback_schema=WITNESS_SCHEMA)
    try:
        source_path = path.resolve().relative_to(ROOT.parent).as_posix()
    except ValueError:
        source_path = path.as_posix()
    report, view = regularize(
        witness,
        source_path=source_path,
        angle_snap=angle_snap,
        snap_tolerance=snap_tolerance,
        max_passes=max_passes,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{path.stem}-regularized"
    witness_path = output_dir / f"{stem}.yaml"
    with atomic_output_file(witness_path) as temporary:
        temporary.write_text(
            witness_document(view, schema=str(WITNESS_SCHEMA)), encoding="utf-8"
        )
    independent_verdict = independent.check(witness_path)
    report["exact_verification"]["independent_checker"] = independent_verdict
    report["exact_verification"]["passed"] = bool(
        report["exact_verification"]["repository_verifier"]["valid"]
        and independent_verdict["verification_passed"]
    )
    report_path = output_dir / f"{stem}.json"
    report["outputs"] = {"witness": str(witness_path), "report": str(report_path)}
    with atomic_output_file(report_path) as temporary:
        temporary.write_text(json.dumps(report, indent=2, sort_keys=True, default=str) + "\n")
    return report


def summarize(report: dict[str, Any]) -> str:
    contacts = report["atlas_contacts"]
    moves = report["regularization"]["moves"]
    exact = report["exact_verification"]
    return (
        f"n={report['source']['n']}: axis-aligned {contacts['axis_aligned_squares']}, "
        f"light {contacts['light_before']} -> {contacts['light_after']} "
        f"(dark gained {contacts['became_dark']}, lost {contacts['became_lighter']}); "
        f"moves {moves['accepted']} accepted ({moves['snaps']} snaps, "
        f"{moves['compactions']} compactions), {moves['rejected']} refused, "
        f"largest {moves['largest_move_decimal']}, passes {moves['passes']}"
        f"{'' if moves['converged'] else ' (NOT converged)'}; "
        f"structural {report['structural_light_faces']}; "
        f"exact {'passed' if exact.get('passed') else 'FAILED'} "
        f"(side - reported = {report['exact_frame']['side_minus_reported_decimal']})"
    )


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    command.add_argument(
        "witnesses", nargs="+", type=Path, help="Witness/v2 YAML files to regularize"
    )
    command.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="where the regularized witness and report go (never under witnesses/ or atlas/)",
    )
    command.add_argument(
        "--angle-snap",
        type=float,
        default=ANGLE_SNAP_TOLERANCE_RADIANS,
        help="radians from axis alignment within which a square is straightened exactly",
    )
    command.add_argument(
        "--snap-tolerance",
        type=Fraction,
        default=SNAP_TOLERANCE,
        help="moves up to this are snaps and need no contact-count argument",
    )
    command.add_argument(
        "--max-passes", type=int, default=None, help="cap on compaction passes"
    )
    command.add_argument("--json", action="store_true", help="print each report as JSON")
    return command


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        output_dir = _guard_output_dir(args.output_dir)
    except RegularizeError as error:
        print(f"refused [{error.kind}]: {error}")
        return 2
    status = 0
    for path in args.witnesses:
        try:
            report = run_one(
                path,
                output_dir,
                angle_snap=args.angle_snap,
                snap_tolerance=args.snap_tolerance,
                max_passes=args.max_passes,
            )
        except (RegularizeError, WitnessError) as error:
            print(f"{path}: refused [{error.kind}]: {error}")
            status = 1
            continue
        print(
            json.dumps(report, indent=2, sort_keys=True, default=str)
            if args.json
            else summarize(report)
        )
        if not report["exact_verification"]["passed"]:
            status = 1
    return status


if __name__ == "__main__":
    raise SystemExit(main())
