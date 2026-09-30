"""Exact, source-independent verification of rectangle-density certificates."""

from __future__ import annotations

import gzip
import io
import json
import math
import time
from collections.abc import Callable, Mapping, Sequence
from contextlib import ExitStack
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from sqpack.rust_rectangle_geometry import (
    RustGeometryError,
    RustGeometryTimeoutError,
    RustRectangleGeometry,
)

type Point = tuple[Fraction, Fraction]
type Polygon = tuple[Point, ...]

ANGLE_COUNT = 201
ANGLE_STEP = Fraction(83, 40000)
SMOOTHING_EPSILON = Fraction(1, 20000)
MAX_CANDIDATE_BYTES = 16 * 1024 * 1024
MAX_DECODED_BYTES = 64 * 1024 * 1024
MAX_RECTANGLES = 100_000
MAX_RATIONAL_BITS = 4096


class CandidateError(ValueError):
    """The candidate is malformed or fails an admission premise."""


class _BoundDeadlineError(TimeoutError):
    """A box bound was interrupted before its exact sum was complete."""


@dataclass(frozen=True, slots=True)
class DensityRectangle:
    """One axis-aligned rectangle with constant density."""

    left: Fraction
    bottom: Fraction
    right: Fraction
    top: Fraction
    density: Fraction

    @property
    def area(self) -> Fraction:
        return (self.right - self.left) * (self.top - self.bottom)


@dataclass(frozen=True, slots=True)
class RectangleDensityCandidate:
    """An admitted exact density and the packing claim it is meant to prove."""

    n: int
    side: Fraction
    core_side: Fraction
    target: Fraction
    declared_rhs: Fraction | None
    mass: Fraction
    rectangles: tuple[DensityRectangle, ...]


@dataclass(frozen=True, slots=True)
class Counterexample:
    """An exact legal core centre whose density integral misses the target."""

    x: Fraction
    y: Fraction
    value: Fraction

    def as_dict(self) -> dict[str, str]:
        return {"x": str(self.x), "y": str(self.y), "value": str(self.value)}


@dataclass(frozen=True, slots=True)
class PendingBox:
    """An unproved centre box retained only for diagnosis, never for replay."""

    angle: int
    left: Fraction
    bottom: Fraction
    right: Fraction
    top: Fraction
    depth: int
    stop_cause: str

    def as_dict(self) -> dict[str, object]:
        return {
            "angle": self.angle,
            "left": str(self.left),
            "bottom": str(self.bottom),
            "right": str(self.right),
            "top": str(self.top),
            "depth": self.depth,
            "stop_cause": self.stop_cause,
        }


@dataclass(frozen=True, slots=True)
class AngleVerification:
    """The exact subdivision result for one rational net direction."""

    index: int
    status: str
    nodes: int
    accepted_leaves: int
    unresolved_leaves: int
    lower_bound: Fraction
    counterexample: Counterexample | None = None
    stop_cause: str | None = None
    pending_boxes: tuple[PendingBox, ...] | None = None

    def as_dict(self) -> dict[str, object]:
        result: dict[str, object] = {
            "index": self.index,
            "status": self.status,
            "nodes": self.nodes,
            "accepted_leaves": self.accepted_leaves,
            "unresolved_leaves": self.unresolved_leaves,
            "lower_bound": str(self.lower_bound),
        }
        if self.counterexample is not None:
            result["counterexample"] = self.counterexample.as_dict()
        if self.stop_cause is not None:
            result["stop_cause"] = self.stop_cause
        if self.pending_boxes is not None:
            result["pending_boxes"] = [box.as_dict() for box in self.pending_boxes]
        return result


@dataclass(frozen=True, slots=True)
class VerificationReport:
    """A complete, partial, inconclusive, or counterexample coverage decision."""

    status: str
    candidate: RectangleDensityCandidate
    angles: tuple[AngleVerification, ...]
    max_nodes_per_angle: int
    max_depth: int
    max_seconds: float
    requested_angle_count: int
    bound_mode: str
    retain_pending_boxes: bool
    backend: str = "python"
    rust_binary_sha256: str | None = None
    rust_table_sha256: str | None = None
    backend_timeout: bool = False

    def as_dict(self) -> dict[str, object]:
        result: dict[str, object] = {
            "status": self.status,
            "n": self.candidate.n,
            "L": str(self.candidate.side),
            "B": str(self.candidate.core_side),
            "threshold": str(self.candidate.target),
            "declared_rhs": (
                str(self.candidate.declared_rhs)
                if self.candidate.declared_rhs is not None
                else None
            ),
            "mass": str(self.candidate.mass),
            "mass_below_n": str(self.candidate.n - self.candidate.mass),
            "angle_step": str(ANGLE_STEP),
            "angle_count": len(self.angles),
            "requested_angle_count": self.requested_angle_count,
            "bound_mode": self.bound_mode,
            "retain_pending_boxes": self.retain_pending_boxes,
            "max_nodes_per_angle": self.max_nodes_per_angle,
            "max_depth": self.max_depth,
            "max_seconds": self.max_seconds,
            "angles": [angle.as_dict() for angle in self.angles],
        }
        if self.backend == "rust":
            result.update(
                {
                    "backend": self.backend,
                    "rust_binary_sha256": self.rust_binary_sha256,
                    "rust_table_sha256": self.rust_table_sha256,
                    "backend_timeout": self.backend_timeout,
                }
            )
        return result


@dataclass(frozen=True, slots=True)
class _CentreBox:
    left: Fraction
    bottom: Fraction
    right: Fraction
    top: Fraction
    depth: int


def _box_coordinates(box: _CentreBox) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    return box.left, box.bottom, box.right, box.top


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise CandidateError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _reject_constant(token: str) -> None:
    raise CandidateError(f"nonfinite JSON number: {token}")


def _json_float(token: str) -> Fraction:
    _guard_rational_token(token)
    return _rational(token, field="JSON number")


def _guard_rational_token(token: str) -> None:
    if len(token) > 2048:
        raise CandidateError("JSON number token is too long")
    if "e" in token.lower():
        exponent = token.lower().split("e", 1)[1]
        try:
            if abs(int(exponent)) > MAX_RATIONAL_BITS:
                raise CandidateError("JSON number exponent exceeds the arithmetic limit")
        except ValueError as error:
            raise CandidateError("invalid JSON number exponent") from error


def _rational(value: object, *, field: str) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, int | str | Fraction):
        raise CandidateError(f"{field} is not an exact rational: {value!r}")
    if isinstance(value, str):
        _guard_rational_token(value)
    try:
        result = Fraction(value)
    except (ValueError, ZeroDivisionError) as error:
        raise CandidateError(f"{field} is not an exact rational: {value!r}") from error
    if max(result.numerator.bit_length(), result.denominator.bit_length()) > MAX_RATIONAL_BITS:
        raise CandidateError(f"{field} exceeds the exact-arithmetic bit limit")
    return result


def _source_images(
    side: Fraction,
    left: Fraction,
    bottom: Fraction,
    right: Fraction,
    top: Fraction,
) -> tuple[tuple[Fraction, Fraction, Fraction, Fraction], ...]:
    images: list[tuple[Fraction, Fraction, Fraction, Fraction]] = []
    for first_left, first_bottom, first_right, first_top in (
        (left, bottom, right, top),
        (bottom, left, top, right),
    ):
        for image_left, image_right in (
            (first_left, first_right),
            (side - first_right, side - first_left),
        ):
            for image_bottom, image_top in (
                (first_bottom, first_top),
                (side - first_top, side - first_bottom),
            ):
                images.append((image_left, image_bottom, image_right, image_top))
    return tuple(images)


def parse_candidate(
    data: Mapping[str, object],
    *,
    n: int,
    expected_side: Fraction | None = None,
    target: Fraction = Fraction(1),
) -> RectangleDensityCandidate:
    """Validate a Tokoharu-format candidate and construct its exact D4 density."""

    if isinstance(n, bool) or not isinstance(n, int) or n <= 0:
        raise CandidateError("n must be a positive integer")
    declared_n = data.get("n")
    if declared_n is not None and (
        isinstance(declared_n, bool) or not isinstance(declared_n, int) or declared_n != n
    ):
        raise CandidateError(f"candidate count does not match requested n = {n}")
    side = _rational(data.get("L"), field="L")
    core_side = _rational(data.get("B"), field="B")
    target = _rational(target, field="threshold")
    if expected_side is not None and side != expected_side:
        raise CandidateError(
            f"candidate side {side} does not match requested side {expected_side}"
        )
    if target < 1:
        raise CandidateError("coverage threshold must be at least one")
    if not (side > 0 and 0 < core_side < 1 and side * side > 2 * core_side * core_side):
        raise CandidateError("invalid container or core side")
    if core_side * (1 + ANGLE_STEP) + 3 * SMOOTHING_EPSILON >= 1:
        raise CandidateError("core side fails the angular and smoothing margin")
    endpoint = (ANGLE_COUNT - 1) * ANGLE_STEP
    if endpoint * endpoint + 2 * endpoint - 1 < 0:
        raise CandidateError("angle net does not reach the symmetry endpoint")
    declared_rhs = _rational(data["rhs"], field="rhs") if "rhs" in data else None
    certificate = data.get("certificate")
    if certificate is not None:
        if not isinstance(certificate, Mapping):
            raise CandidateError("certificate metadata must be an object")
        declared_fields: tuple[tuple[str, Fraction | int], ...] = (
            ("L", side),
            ("B", core_side),
            ("epsilon", SMOOTHING_EPSILON),
            ("D", ANGLE_STEP),
            ("angle_count", ANGLE_COUNT),
        )
        for key, expected in declared_fields:
            if key not in certificate:
                continue
            if key == "angle_count":
                actual = certificate[key]
                if (
                    isinstance(actual, bool)
                    or not isinstance(actual, int)
                    or actual != expected
                ):
                    raise CandidateError(
                        f"certificate metadata {key} does not match native net"
                    )
            elif _rational(certificate[key], field=f"certificate.{key}") != expected:
                raise CandidateError(f"certificate metadata {key} does not match native net")
    for key, expected in (
        ("angle_step", ANGLE_STEP),
        ("epsilon", SMOOTHING_EPSILON),
    ):
        if key in data and _rational(data[key], field=key) != expected:
            raise CandidateError(f"declared {key} does not match native net")
    if "angle_count" in data:
        count = data["angle_count"]
        if isinstance(count, bool) or not isinstance(count, int) or count != ANGLE_COUNT:
            raise CandidateError("declared angle_count does not match native net")

    rows = data.get("rectangles")
    weights = data.get("weights")
    if not isinstance(rows, list) or not isinstance(weights, list) or len(rows) != len(weights):
        raise CandidateError("rectangle and weight arrays must have equal lengths")
    if len(rows) > MAX_RECTANGLES:
        raise CandidateError("candidate has too many source rectangles")

    rectangle_densities: dict[tuple[Fraction, Fraction, Fraction, Fraction], Fraction] = {}
    mass = Fraction()
    for index, (row, raw_weight) in enumerate(zip(rows, weights, strict=True)):
        if not isinstance(row, list) or len(row) != 4:
            raise CandidateError(f"rectangle {index} needs four coordinates")
        coordinates = tuple(_rational(value, field=f"rectangle {index}") for value in row)
        left, bottom, right, top = coordinates
        weight = _rational(raw_weight, field=f"weight {index}")
        if weight < 0:
            raise CandidateError(f"weight {index} is negative")
        if weight == 0:
            continue
        if not (
            SMOOTHING_EPSILON < left < right < side - SMOOTHING_EPSILON
            and SMOOTHING_EPSILON < bottom < top < side - SMOOTHING_EPSILON
        ):
            raise CandidateError(f"positive rectangle {index} is outside the safe interior")
        area = (right - left) * (top - bottom)
        density = weight / (8 * area)
        mass += weight
        for image in _source_images(side, left, bottom, right, top):
            rectangle_densities[image] = rectangle_densities.get(image, Fraction()) + density
    if not 0 < mass < n:
        raise CandidateError("exact total mass must lie strictly between zero and n")
    rectangles = tuple(
        DensityRectangle(*coordinates, density)
        for coordinates, density in rectangle_densities.items()
    )
    integrated = sum(
        (rectangle.density * rectangle.area for rectangle in rectangles), Fraction()
    )
    if integrated != mass:
        raise CandidateError("D4 expansion changed the exact total mass")
    return RectangleDensityCandidate(n, side, core_side, target, declared_rhs, mass, rectangles)


def load_candidate_bytes(
    raw: bytes,
    *,
    n: int,
    compressed: bool = False,
    expected_side: Fraction | None = None,
    target: Fraction = Fraction(1),
) -> RectangleDensityCandidate:
    """Parse candidate bytes already captured for a content-bound receipt."""

    if len(raw) > MAX_CANDIDATE_BYTES:
        raise CandidateError("candidate exceeds the compressed/input byte limit")
    try:
        if compressed:
            with gzip.GzipFile(fileobj=io.BytesIO(raw)) as stream:
                decoded = stream.read(MAX_DECODED_BYTES + 1)
        else:
            decoded = raw
        value = json.loads(
            decoded,
            parse_float=_json_float,
            object_pairs_hook=_pairs,
            parse_constant=_reject_constant,
        )
    except CandidateError:
        raise
    except (OSError, EOFError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise CandidateError(f"cannot read exact candidate JSON: {error}") from error
    if len(decoded) > MAX_DECODED_BYTES:
        raise CandidateError("candidate exceeds the decoded byte limit")
    if not isinstance(value, dict):
        raise CandidateError("candidate JSON must be an object")
    return parse_candidate(value, n=n, expected_side=expected_side, target=target)


def load_candidate(
    path: Path,
    *,
    n: int,
    expected_side: Fraction | None = None,
    target: Fraction = Fraction(1),
) -> RectangleDensityCandidate:
    """Load exact JSON, accepting a plain file or deterministic gzip."""

    try:
        raw = path.read_bytes()
    except OSError as error:
        raise CandidateError(f"cannot read exact candidate JSON: {error}") from error
    return load_candidate_bytes(
        raw,
        n=n,
        compressed=path.suffix == ".gz",
        expected_side=expected_side,
        target=target,
    )


def square_polygon(
    x: Fraction,
    y: Fraction,
    cosine: Fraction,
    sine: Fraction,
    side: Fraction,
) -> Polygon:
    """Return exact rotated-square corners in counterclockwise order."""

    return tuple(
        (
            x + side * (cosine * u - sine * v) / 2,
            y + side * (sine * u + cosine * v) / 2,
        )
        for u, v in ((-1, -1), (1, -1), (1, 1), (-1, 1))
    )


def _clip_axis(polygon: Polygon, *, axis: int, edge: Fraction, sign: int) -> Polygon:
    if not polygon:
        return ()
    inside = tuple(
        point[axis] >= edge if sign == 1 else point[axis] <= edge for point in polygon
    )
    if all(inside):
        return polygon
    if not any(inside):
        return ()
    output: list[Point] = []
    previous = polygon[-1]
    previous_inside = inside[-1]
    for current, current_inside in zip(polygon, inside, strict=True):
        if current_inside != previous_inside:
            factor = (previous[axis] - edge) / (previous[axis] - current[axis])
            output.append(
                (
                    previous[0] + factor * (current[0] - previous[0]),
                    previous[1] + factor * (current[1] - previous[1]),
                )
            )
        if current_inside:
            output.append(current)
        previous = current
        previous_inside = current_inside
    return tuple(output)


def exact_intersection_area(
    rectangle: DensityRectangle | tuple[object, object, object, object],
    polygon: Sequence[Point],
) -> Fraction:
    """Return the exact area where a convex polygon meets an axis-aligned rectangle."""

    if isinstance(rectangle, DensityRectangle):
        left, bottom, right, top = (
            rectangle.left,
            rectangle.bottom,
            rectangle.right,
            rectangle.top,
        )
    else:
        left, bottom, right, top = (
            _rational(rectangle[0], field="rectangle edge"),
            _rational(rectangle[1], field="rectangle edge"),
            _rational(rectangle[2], field="rectangle edge"),
            _rational(rectangle[3], field="rectangle edge"),
        )
    clipped = tuple(polygon)
    for axis, edge, sign in (
        (0, left, 1),
        (0, right, -1),
        (1, bottom, 1),
        (1, top, -1),
    ):
        clipped = _clip_axis(clipped, axis=axis, edge=edge, sign=sign)
        if len(clipped) < 3:
            return Fraction()
    twice_area = sum(
        (
            point[0] * clipped[(index + 1) % len(clipped)][1]
            - point[1] * clipped[(index + 1) % len(clipped)][0]
            for index, point in enumerate(clipped)
        ),
        Fraction(),
    )
    return abs(twice_area) / 2


def _angle(index: int) -> tuple[Fraction, Fraction]:
    tangent = index * ANGLE_STEP
    denominator = 1 + tangent * tangent
    return (1 - tangent * tangent) / denominator, 2 * tangent / denominator


def _validate_candidate(candidate: RectangleDensityCandidate) -> None:
    """Recheck invariants so direct library construction cannot bypass admission."""

    if isinstance(candidate.n, bool) or not isinstance(candidate.n, int) or candidate.n <= 0:
        raise CandidateError("candidate n must be a positive integer")
    scalars = (
        candidate.side,
        candidate.core_side,
        candidate.target,
        candidate.declared_rhs,
        candidate.mass,
    )
    if any(value is not None and type(value) is not Fraction for value in scalars):
        raise CandidateError("candidate scalar fields must be exact fractions")
    if (
        candidate.side <= 0
        or not 0 < candidate.core_side < 1
        or candidate.side * candidate.side <= 2 * candidate.core_side * candidate.core_side
        or candidate.target < 1
    ):
        raise CandidateError("candidate geometry or threshold fails admission")
    if candidate.core_side * (1 + ANGLE_STEP) + 3 * SMOOTHING_EPSILON >= 1:
        raise CandidateError("candidate core side fails the angular and smoothing margin")
    densities = {
        (rectangle.left, rectangle.bottom, rectangle.right, rectangle.top): rectangle.density
        for rectangle in candidate.rectangles
    }
    if len(densities) != len(candidate.rectangles):
        raise CandidateError("candidate contains duplicate expanded rectangles")
    integrated = Fraction()
    for rectangle in candidate.rectangles:
        rectangle_values = (
            rectangle.left,
            rectangle.bottom,
            rectangle.right,
            rectangle.top,
            rectangle.density,
        )
        if any(type(value) is not Fraction for value in rectangle_values):
            raise CandidateError("density rectangle fields must be exact fractions")
        if (
            rectangle.density <= 0
            or not SMOOTHING_EPSILON
            < rectangle.left
            < rectangle.right
            < candidate.side - SMOOTHING_EPSILON
            or not SMOOTHING_EPSILON
            < rectangle.bottom
            < rectangle.top
            < candidate.side - SMOOTHING_EPSILON
        ):
            raise CandidateError("candidate contains an invalid density rectangle")
        integrated += rectangle.density * rectangle.area
        for image in _source_images(
            candidate.side,
            rectangle.left,
            rectangle.bottom,
            rectangle.right,
            rectangle.top,
        ):
            if densities.get(image) != rectangle.density:
                raise CandidateError("expanded density is not D4 invariant")
    if integrated != candidate.mass or not 0 < candidate.mass < candidate.n:
        raise CandidateError("candidate exact mass fails admission")


def _coverage_polygon(candidate: RectangleDensityCandidate, polygon: Polygon) -> Fraction:
    if not polygon:
        return Fraction()
    left = min(point[0] for point in polygon)
    right = max(point[0] for point in polygon)
    bottom = min(point[1] for point in polygon)
    top = max(point[1] for point in polygon)
    total = Fraction()
    for rectangle in candidate.rectangles:
        if (
            rectangle.right <= left
            or rectangle.left >= right
            or rectangle.top <= bottom
            or rectangle.bottom >= top
        ):
            continue
        total += rectangle.density * exact_intersection_area(rectangle, polygon)
    return total


def coverage_at_point(
    candidate: RectangleDensityCandidate,
    x: Fraction,
    y: Fraction,
    cosine: Fraction,
    sine: Fraction,
) -> Fraction:
    """Integrate the exact density over one legal side-`B` core."""

    return _coverage_polygon(
        candidate,
        square_polygon(x, y, cosine, sine, candidate.core_side),
    )


def _common_core(
    candidate: RectangleDensityCandidate,
    box: _CentreBox,
    cosine: Fraction,
    sine: Fraction,
) -> Polygon:
    midpoint_x = (box.left + box.right) / 2
    midpoint_y = (box.bottom + box.top) / 2
    half_width_x = (box.right - box.left) / 2
    half_width_y = (box.top - box.bottom) / 2
    local_x = candidate.core_side / 2 - cosine * half_width_x - sine * half_width_y
    local_y = candidate.core_side / 2 - sine * half_width_x - cosine * half_width_y
    if local_x <= 0 or local_y <= 0:
        return ()
    return tuple(
        (
            midpoint_x + cosine * u - sine * v,
            midpoint_y + sine * u + cosine * v,
        )
        for u, v in (
            (-local_x, -local_y),
            (local_x, -local_y),
            (local_x, local_y),
            (-local_x, local_y),
        )
    )


def _corner_minimum(
    candidate: RectangleDensityCandidate,
    box: _CentreBox,
    cosine: Fraction,
    sine: Fraction,
    deadline: float | None = None,
) -> Fraction:
    """Sum each rectangle's least corner overlap over a centre box.

    For a fixed convex rectangle, the square-intersection area's square root is
    concave on its positive-overlap support under translation (planar
    Brunn--Minkowski). Every centre is a convex combination of the four corners;
    if all corner overlaps are positive, concavity gives their minimum as a
    lower bound. If a corner overlap is zero, nonnegativity gives the same
    (zero) lower bound. Minima precede the sum of nonnegative densities.
    """

    polygons = tuple(
        square_polygon(x, y, cosine, sine, candidate.core_side)
        for x in (box.left, box.right)
        for y in (box.bottom, box.top)
    )
    total = Fraction()
    for rectangle in candidate.rectangles:
        if deadline is not None and _expired(deadline):
            raise _BoundDeadlineError
        overlaps = (exact_intersection_area(rectangle, polygon) for polygon in polygons)
        total += rectangle.density * min(overlaps)
    return total


def _box_lower_bound(
    candidate: RectangleDensityCandidate,
    box: _CentreBox,
    cosine: Fraction,
    sine: Fraction,
    *,
    bound_mode: str,
    deadline: float,
    coverage: Callable[[Polygon], Fraction],
) -> Fraction:
    common = coverage(_common_core(candidate, box, cosine, sine))
    if bound_mode == "common-core" or common >= candidate.target:
        return common
    return max(common, _corner_minimum(candidate, box, cosine, sine, deadline))


def pending_common_core_bound(
    candidate: RectangleDensityCandidate, pending: PendingBox
) -> Fraction:
    """Re-evaluate the old bound on a diagnostic box without proof authority."""

    box = _CentreBox(pending.left, pending.bottom, pending.right, pending.top, pending.depth)
    cosine, sine = _angle(pending.angle)
    return _coverage_polygon(candidate, _common_core(candidate, box, cosine, sine))


def pending_corner_min_bound(
    candidate: RectangleDensityCandidate, pending: PendingBox, *, deadline: float
) -> Fraction:
    """Re-evaluate the stronger bound; a timeout has no usable partial sum."""

    box = _CentreBox(pending.left, pending.bottom, pending.right, pending.top, pending.depth)
    cosine, sine = _angle(pending.angle)
    return _corner_minimum(candidate, box, cosine, sine, deadline)


def _axis_events(
    candidate: RectangleDensityCandidate, lower: Fraction, upper: Fraction
) -> tuple[tuple[Fraction, ...], tuple[Fraction, ...]]:
    x_events = {lower, upper}
    y_events = {lower, upper}
    half = candidate.core_side / 2
    for rectangle in candidate.rectangles:
        for edge in (rectangle.left, rectangle.right):
            for event in (edge - half, edge + half):
                if lower <= event <= upper:
                    x_events.add(event)
        for edge in (rectangle.bottom, rectangle.top):
            for event in (edge - half, edge + half):
                if lower <= event <= upper:
                    y_events.add(event)
    return tuple(sorted(x_events)), tuple(sorted(y_events))


def _expired(deadline: float) -> bool:
    return time.monotonic() >= deadline


def _verify_axis(
    candidate: RectangleDensityCandidate,
    *,
    max_nodes: int,
    deadline: float,
    coverage: Callable[[Polygon], Fraction],
) -> AngleVerification:
    lower = candidate.side / 2
    upper = candidate.side - candidate.core_side / 2
    x_events, y_events = _axis_events(candidate, lower, upper)
    minimum: Fraction | None = None
    nodes = 0
    event_count = len(x_events) * len(y_events)
    for x in x_events:
        for y in y_events:
            if nodes >= max_nodes or _expired(deadline):
                cause = "node_limit" if nodes >= max_nodes else "time_limit"
                return AngleVerification(
                    0,
                    "INCONCLUSIVE",
                    nodes,
                    nodes,
                    event_count - nodes,
                    Fraction(),
                    stop_cause=cause,
                )
            try:
                value = coverage(
                    square_polygon(x, y, Fraction(1), Fraction(), candidate.core_side)
                )
            except _BoundDeadlineError:
                return AngleVerification(
                    0,
                    "INCONCLUSIVE",
                    nodes,
                    nodes,
                    event_count - nodes,
                    Fraction(),
                    stop_cause="time_limit",
                )
            nodes += 1
            minimum = value if minimum is None else min(minimum, value)
            if value < candidate.target:
                return AngleVerification(
                    0,
                    "COUNTEREXAMPLE",
                    nodes,
                    nodes - 1,
                    event_count - nodes,
                    Fraction(),
                    Counterexample(x, y, value),
                    stop_cause="counterexample_found",
                )
    if minimum is None:
        raise CandidateError("axis event grid is empty")
    return AngleVerification(0, "VERIFIED", nodes, nodes, 0, minimum)


def _split(box: _CentreBox) -> tuple[_CentreBox, _CentreBox]:
    width = box.right - box.left
    height = box.top - box.bottom
    if width >= height:
        midpoint = (box.left + box.right) / 2
        return (
            _CentreBox(box.left, box.bottom, midpoint, box.top, box.depth + 1),
            _CentreBox(midpoint, box.bottom, box.right, box.top, box.depth + 1),
        )
    midpoint = (box.bottom + box.top) / 2
    return (
        _CentreBox(box.left, box.bottom, box.right, midpoint, box.depth + 1),
        _CentreBox(box.left, midpoint, box.right, box.top, box.depth + 1),
    )


def _verify_rotated(
    candidate: RectangleDensityCandidate,
    index: int,
    *,
    max_nodes: int,
    max_depth: int,
    deadline: float,
    bound_mode: str,
    retain_pending_boxes: bool,
    coverage: Callable[[Polygon], Fraction],
) -> AngleVerification:
    cosine, sine = _angle(index)
    extent = candidate.core_side * (cosine + sine) / 2
    lower = candidate.side / 2
    upper = candidate.side - extent
    if upper < lower:
        raise CandidateError(f"empty reduced centre domain at angle {index}")
    stack = [_CentreBox(lower, lower, upper, upper, 0)]
    nodes = 0
    accepted = 0
    unresolved = 0
    pending: list[PendingBox] | None = [] if retain_pending_boxes else None
    stop_cause: str | None = None
    certified_minimum: Fraction | None = None
    while stack:
        if nodes >= max_nodes or _expired(deadline):
            stop_cause = "node_limit" if nodes >= max_nodes else "time_limit"
            unresolved += len(stack)
            if pending is not None:
                pending.extend(
                    PendingBox(index, *_box_coordinates(queued), queued.depth, stop_cause)
                    for queued in stack
                )
            break
        box = stack.pop()
        nodes += 1
        try:
            lower_bound = _box_lower_bound(
                candidate,
                box,
                cosine,
                sine,
                bound_mode=bound_mode,
                deadline=deadline,
                coverage=coverage,
            )
        except _BoundDeadlineError:
            stop_cause = "time_limit"
            unresolved += 1 + len(stack)
            if pending is not None:
                pending.append(PendingBox(index, *_box_coordinates(box), box.depth, stop_cause))
                pending.extend(
                    PendingBox(index, *_box_coordinates(queued), queued.depth, stop_cause)
                    for queued in stack
                )
            break
        if lower_bound >= candidate.target:
            accepted += 1
            certified_minimum = (
                lower_bound
                if certified_minimum is None
                else min(certified_minimum, lower_bound)
            )
            continue
        midpoint_x = (box.left + box.right) / 2
        midpoint_y = (box.bottom + box.top) / 2
        try:
            point_value = coverage(
                square_polygon(midpoint_x, midpoint_y, cosine, sine, candidate.core_side)
            )
        except _BoundDeadlineError:
            stop_cause = "time_limit"
            unresolved += 1 + len(stack)
            if pending is not None:
                pending.append(PendingBox(index, *_box_coordinates(box), box.depth, stop_cause))
                pending.extend(
                    PendingBox(index, *_box_coordinates(queued), queued.depth, stop_cause)
                    for queued in stack
                )
            break
        if point_value < candidate.target:
            if pending is not None:
                pending.extend(
                    PendingBox(
                        index,
                        *_box_coordinates(queued),
                        queued.depth,
                        "counterexample_found",
                    )
                    for queued in stack
                )
            return AngleVerification(
                index,
                "COUNTEREXAMPLE",
                nodes,
                accepted,
                unresolved + len(stack),
                Fraction(),
                Counterexample(midpoint_x, midpoint_y, point_value),
                "counterexample_found",
                tuple(pending) if pending is not None else None,
            )
        if box.depth >= max_depth or (box.left == box.right and box.bottom == box.top):
            unresolved += 1
            cause = "depth_limit" if box.depth >= max_depth else "point_box"
            stop_cause = cause if stop_cause is None else stop_cause
            if pending is not None:
                pending.append(PendingBox(index, *_box_coordinates(box), box.depth, cause))
            continue
        first, second = _split(box)
        stack.extend((second, first))
    status = "VERIFIED" if unresolved == 0 else "INCONCLUSIVE"
    return AngleVerification(
        index,
        status,
        nodes,
        accepted,
        unresolved,
        (
            certified_minimum
            if status == "VERIFIED" and certified_minimum is not None
            else Fraction()
        ),
        stop_cause=stop_cause,
        pending_boxes=tuple(pending) if pending is not None else None,
    )


def verify_candidate(
    candidate: RectangleDensityCandidate,
    *,
    angle_indices: Sequence[int] = tuple(range(ANGLE_COUNT)),
    max_nodes_per_angle: int = 1_000_000,
    max_depth: int = 48,
    max_seconds: float = 300.0,
    bound_mode: str = "common-core",
    retain_pending_boxes: bool = False,
    backend: str = "python",
    rust_binary: Path | None = None,
) -> VerificationReport:
    """Verify selected net directions; only the complete 201-angle census can pass."""

    _validate_candidate(candidate)
    indices = tuple(angle_indices)
    if (
        not indices
        or len(set(indices)) != len(indices)
        or any(
            isinstance(index, bool)
            or not isinstance(index, int)
            or not 0 <= index < ANGLE_COUNT
            for index in indices
        )
    ):
        raise CandidateError("angle indices must be distinct integers from 0 through 200")
    if (
        isinstance(max_nodes_per_angle, bool)
        or not isinstance(max_nodes_per_angle, int)
        or isinstance(max_depth, bool)
        or not isinstance(max_depth, int)
        or max_nodes_per_angle < 0
        or max_depth < 0
    ):
        raise CandidateError("work limits must be nonnegative")
    if isinstance(max_seconds, bool) or not isinstance(max_seconds, int | float):
        raise CandidateError("max_seconds must be a nonnegative finite number")
    max_seconds = float(max_seconds)
    if max_seconds < 0 or not math.isfinite(max_seconds):
        raise CandidateError("max_seconds must be a nonnegative finite number")
    if bound_mode not in ("common-core", "corner-min"):
        raise CandidateError("bound mode must be common-core or corner-min")
    if backend not in ("python", "rust"):
        raise CandidateError("backend must be python or rust")
    if backend == "rust" and bound_mode != "common-core":
        raise CandidateError("Rust backend currently supports common-core only")
    if backend == "rust" and not isinstance(rust_binary, Path):
        raise CandidateError("Rust backend requires an explicit binary path")
    if backend == "python" and rust_binary is not None:
        raise CandidateError("Rust binary path requires the Rust backend")
    if type(retain_pending_boxes) is not bool:
        raise CandidateError("retain_pending_boxes must be Boolean")
    if retain_pending_boxes and max(1, max_nodes_per_angle) * len(indices) > 10_000:
        raise CandidateError("pending-box retention requires at most 10000 total nodes")
    deadline = time.monotonic() + max_seconds
    results: list[AngleVerification] = []
    rust_binary_sha256: str | None = None
    rust_table_sha256: str | None = None
    backend_timed_out = False
    try:
        with ExitStack() as resources:
            if backend == "rust":
                assert rust_binary is not None
                engine = resources.enter_context(
                    RustRectangleGeometry(candidate.rectangles, rust_binary, deadline=deadline)
                )
                rust_binary_sha256 = engine.binary_sha256
                rust_table_sha256 = engine.table_sha256

                def coverage(polygon: Polygon) -> Fraction:
                    try:
                        return engine.coverage(polygon)
                    except RustGeometryTimeoutError as error:
                        raise _BoundDeadlineError from error

            else:

                def coverage(polygon: Polygon) -> Fraction:
                    return _coverage_polygon(candidate, polygon)

            for index in indices:
                result = (
                    _verify_axis(
                        candidate,
                        max_nodes=max_nodes_per_angle,
                        deadline=deadline,
                        coverage=coverage,
                    )
                    if index == 0
                    else _verify_rotated(
                        candidate,
                        index,
                        max_nodes=max_nodes_per_angle,
                        max_depth=max_depth,
                        deadline=deadline,
                        bound_mode=bound_mode,
                        retain_pending_boxes=retain_pending_boxes,
                        coverage=coverage,
                    )
                )
                results.append(result)
                if _expired(deadline):
                    break
    except RustGeometryTimeoutError:
        backend_timed_out = True
    except (RustGeometryError, OSError) as error:
        raise CandidateError(f"Rust exact geometry refused: {error}") from error
    angles = tuple(results)
    if any(angle.status == "COUNTEREXAMPLE" for angle in angles):
        status = "COUNTEREXAMPLE"
    elif (
        backend_timed_out
        or len(angles) != len(indices)
        or any(angle.status == "INCONCLUSIVE" for angle in angles)
    ):
        status = "INCONCLUSIVE"
    elif indices == tuple(range(ANGLE_COUNT)):
        status = "VERIFIED"
    else:
        status = "PARTIAL"
    return VerificationReport(
        status,
        candidate,
        angles,
        max_nodes_per_angle,
        max_depth,
        max_seconds,
        len(indices),
        bound_mode,
        retain_pending_boxes,
        backend,
        rust_binary_sha256,
        rust_table_sha256,
        backend_timed_out,
    )
