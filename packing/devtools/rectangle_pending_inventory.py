"""Admit a complete exact pending-box census for diagnostic consumers only."""

from __future__ import annotations

from fractions import Fraction

from sqpack import rectangle_density as density


def _rational(value: object) -> Fraction:
    if type(value) is not str:
        raise density.CandidateError("pending box coordinate must be a rational string")
    try:
        return Fraction(value)
    except (ValueError, ZeroDivisionError) as error:
        raise density.CandidateError("pending box coordinate is not a rational") from error


def admit_pending_boxes(
    raw_boxes: object,
    *,
    unresolved_leaves: object,
    candidate: density.RectangleDensityCandidate,
    angle: int,
    max_depth: int,
) -> tuple[density.PendingBox, ...]:
    """Check exact serialization, geometry, and census without granting proof credit."""
    if (
        type(unresolved_leaves) is not int
        or unresolved_leaves <= 0
        or not isinstance(raw_boxes, (list, tuple))
        or len(raw_boxes) != unresolved_leaves
    ):
        raise density.CandidateError("frontier pending inventory is incomplete")
    cosine, sine = density._angle(angle)  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
    extent = candidate.core_side * (cosine + sine) / 2
    legal_low, legal_high = candidate.side / 2, candidate.side - extent
    boxes: list[density.PendingBox] = []
    seen: set[tuple[Fraction, Fraction, Fraction, Fraction]] = set()
    fields = {"angle", "left", "bottom", "right", "top", "depth", "stop_cause"}
    for raw in raw_boxes:
        item = raw.as_dict() if isinstance(raw, density.PendingBox) else raw
        if not isinstance(item, dict):
            raise density.CandidateError("pending box is not an object")
        if set(item) != fields:
            raise density.CandidateError("pending box fields differ")
        if (
            type(item["angle"]) is not int
            or item["angle"] != angle
            or type(item["depth"]) is not int
            or not 0 <= item["depth"] <= max_depth
            or type(item["stop_cause"]) is not str
            or item["stop_cause"] not in {"node_limit", "depth_limit", "point_box"}
        ):
            raise density.CandidateError("pending box metadata differs")
        box = density.PendingBox(
            angle,
            _rational(item["left"]),
            _rational(item["bottom"]),
            _rational(item["right"]),
            _rational(item["top"]),
            item["depth"],
            item["stop_cause"],
        )
        if not (
            legal_low <= box.left <= box.right <= legal_high
            and legal_low <= box.bottom <= box.top <= legal_high
        ):
            raise density.CandidateError("pending box lies outside the exact reduced root")
        identity = (box.left, box.bottom, box.right, box.top)
        if identity in seen:
            raise density.CandidateError("duplicate pending box")
        seen.add(identity)
        if box.as_dict() != item:
            raise density.CandidateError("pending box exact serialization differs")
        boxes.append(box)
    return tuple(boxes)
