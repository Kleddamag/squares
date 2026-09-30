"""Measure two exact common-core subdivisions on a retained native frontier.

This diagnostic never resumes a proof or changes the verifier's acceptance decision.
"""

# This diagnostic checks the verifier's private split primitive against exact geometry.
# ruff: noqa: SLF001

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
import time
from fractions import Fraction
from pathlib import Path
from typing import Any

from devtools import compare_rectangle_density_bounds as comparison
from sqpack import rectangle_density as density

MAX_RECEIPT_BYTES = 4 * 1024 * 1024


class _DiagnosticDeadlineError(Exception):
    def __init__(self, partial: dict[str, Any] | None = None) -> None:
        self.partial = partial


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--frontier-receipt", type=Path, required=True)
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--side", type=Fraction)
    parser.add_argument("--angle", type=int, default=1)
    parser.add_argument("--max-nodes-per-angle", type=int, default=1000)
    parser.add_argument("--max-depth", type=int, default=20)
    parser.add_argument("--max-seconds", type=float, default=30.0)
    parser.add_argument("--expected-pending-boxes", type=int, default=78)
    parser.add_argument("--expected-depth-leaves", type=int, default=67)
    return parser


def _checked_split(box: density._CentreBox) -> tuple[density._CentreBox, density._CentreBox]:  # pyright: ignore[reportPrivateUsage]
    """Use the verifier's rule, then independently check its exact partition."""
    children = density._split(box)  # pyright: ignore[reportPrivateUsage]
    if len(children) != 2:
        raise density.CandidateError("subdivision did not produce both children")
    width, height = box.right - box.left, box.top - box.bottom
    if width <= 0 or height <= 0:
        raise density.CandidateError("cannot refine a degenerate parent box")
    if width >= height:
        middle = (box.left + box.right) / 2
        expected = (
            density._CentreBox(box.left, box.bottom, middle, box.top, box.depth + 1),  # pyright: ignore[reportPrivateUsage]
            density._CentreBox(middle, box.bottom, box.right, box.top, box.depth + 1),  # pyright: ignore[reportPrivateUsage]
        )
    else:
        middle = (box.bottom + box.top) / 2
        expected = (
            density._CentreBox(box.left, box.bottom, box.right, middle, box.depth + 1),  # pyright: ignore[reportPrivateUsage]
            density._CentreBox(box.left, middle, box.right, box.top, box.depth + 1),  # pyright: ignore[reportPrivateUsage]
        )
    if children != expected:
        raise density.CandidateError("subdivision is not the exact longest-side partition")
    return children


def _four_children(parent: density.PendingBox) -> tuple[density.PendingBox, ...]:
    box = density._CentreBox(  # pyright: ignore[reportPrivateUsage]
        parent.left, parent.bottom, parent.right, parent.top, parent.depth
    )
    first, second = _checked_split(box)
    children = (*_checked_split(first), *_checked_split(second))
    if len(children) != 4 or len(set(children)) != 4:
        raise density.CandidateError(
            "two-level subdivision did not produce four distinct children"
        )
    return tuple(
        density.PendingBox(
            parent.angle,
            child.left,
            child.bottom,
            child.right,
            child.top,
            child.depth,
            "diagnostic_child",
        )
        for child in children
    )


def _bound_before_deadline(
    candidate: density.RectangleDensityCandidate,
    box: density.PendingBox,
    deadline: float,
) -> Fraction:
    if time.monotonic() >= deadline:
        raise _DiagnosticDeadlineError
    value = density.pending_common_core_bound(candidate, box)
    if time.monotonic() >= deadline:
        raise _DiagnosticDeadlineError
    return value


def _refine_parent(
    candidate: density.RectangleDensityCandidate,
    parent: density.PendingBox,
    *,
    deadline: float,
) -> dict[str, Any]:
    children = _four_children(parent)
    row: dict[str, Any] = {
        "parent": parent.as_dict(),
        "parent_bound": None,
        "children": [],
        "complete": False,
    }
    try:
        parent_bound = _bound_before_deadline(candidate, parent, deadline)
        row["parent_bound"] = str(parent_bound)
        if parent_bound >= candidate.target:
            raise density.CandidateError("selected unresolved parent already reaches threshold")
        for child in children:
            child_bound = _bound_before_deadline(candidate, child, deadline)
            if child_bound < parent_bound:
                raise density.CandidateError("child bound fell below parent bound")
            row["children"].append({"box": child.as_dict(), "bound": str(child_bound)})
    except _DiagnosticDeadlineError as error:
        raise _DiagnosticDeadlineError(row) from error
    if len(row["children"]) != 4:
        raise density.CandidateError("two-level refinement is missing a child bound")
    row["complete"] = True
    row["all_children_closed"] = all(
        Fraction(child["bound"]) >= candidate.target for child in row["children"]
    )
    return row


def _require_receipt_header(
    receipt: object,
    *,
    candidate: density.RectangleDensityCandidate,
    candidate_sha256: str,
    checker_sha256: str,
    args: argparse.Namespace,
) -> None:
    if not isinstance(receipt, dict):
        raise density.CandidateError("frontier receipt is not a JSON object")
    expected = {
        "candidate_sha256": candidate_sha256,
        "checker_source_sha256": checker_sha256,
        "checker": "sqpack.rectangle_density:native-exact-v2",
        "bound_mode": "common-core",
        "retain_pending_boxes": True,
        "max_nodes_per_angle": args.max_nodes_per_angle,
        "max_depth": args.max_depth,
        "max_seconds": args.max_seconds,
        "requested_angle_count": 1,
        "angle_count": 1,
        "threshold": "1",
        "n": candidate.n,
        "L": str(candidate.side),
        "B": str(candidate.core_side),
        "mass": str(candidate.mass),
        "status": "INCONCLUSIVE",
    }
    if any(
        receipt.get(key) != value
        or (
            type(receipt.get(key)) not in (int, float)
            if key == "max_seconds"
            else type(receipt.get(key)) is not type(value)
        )
        for key, value in expected.items()
    ):
        raise density.CandidateError("frontier receipt input, source, or settings differ")


def _selected_leaves(
    angle: density.AngleVerification,
    args: argparse.Namespace,
    candidate: density.RectangleDensityCandidate,
) -> tuple[density.PendingBox, ...]:
    boxes = comparison._require_complete_frontier(  # pyright: ignore[reportPrivateUsage]
        angle, candidate, max_depth=args.max_depth
    )
    if angle.index != args.angle or angle.nodes != args.max_nodes_per_angle:
        raise density.CandidateError("frontier angle or node census differs")
    if len(boxes) != args.expected_pending_boxes:
        raise density.CandidateError("pending-box census differs")
    selected = tuple(
        box for box in boxes if box.depth == args.max_depth and box.stop_cause == "depth_limit"
    )
    if len(selected) != args.expected_depth_leaves:
        raise density.CandidateError("depth-capped leaf census differs")
    if any(box.stop_cause != "node_limit" for box in boxes if box not in selected):
        raise density.CandidateError("unexpected pending-box stop cause")
    return selected


def _unchanged(path: Path, original: bytes, *, label: str) -> None:
    if path.read_bytes() != original:
        raise density.CandidateError(f"{label} changed during diagnostic")


def _bounded_receipt_read(path: Path) -> bytes:
    with path.open("rb") as stream:
        content = stream.read(MAX_RECEIPT_BYTES + 1)
    if len(content) > MAX_RECEIPT_BYTES:
        raise density.CandidateError("frontier receipt exceeds diagnostic size limit")
    return content


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if (
        not 1 <= args.angle < density.ANGLE_COUNT
        or args.max_nodes_per_angle <= 0
        or args.max_depth < 0
        or args.expected_pending_boxes <= 0
        or args.expected_depth_leaves <= 0
        or args.expected_depth_leaves > args.expected_pending_boxes
        or not math.isfinite(args.max_seconds)
        or not 0 <= args.max_seconds <= 30
    ):
        print(json.dumps({"status": "REFUSED", "error": "invalid diagnostic settings"}))
        return 1
    source_path = Path(density.__file__)
    tool_path = Path(__file__)
    comparison_path = Path(comparison.__file__)
    inventory_path = Path(comparison.inventory.__file__)
    started = time.monotonic()
    deadline = started + args.max_seconds
    try:
        source_bytes = source_path.read_bytes()
        tool_bytes = tool_path.read_bytes()
        comparison_bytes = comparison_path.read_bytes()
        inventory_bytes = inventory_path.read_bytes()
        candidate_bytes = args.candidate.read_bytes()
        receipt_bytes = _bounded_receipt_read(args.frontier_receipt)
        receipt = json.loads(receipt_bytes)
        candidate = density.load_candidate_bytes(
            candidate_bytes,
            n=args.n,
            compressed=args.candidate.suffix == ".gz",
            expected_side=args.side,
        )
        candidate_sha256 = hashlib.sha256(candidate_bytes).hexdigest()
        checker_sha256 = hashlib.sha256(source_bytes).hexdigest()
        _require_receipt_header(
            receipt,
            candidate=candidate,
            candidate_sha256=candidate_sha256,
            checker_sha256=checker_sha256,
            args=args,
        )
        report = density.verify_candidate(
            candidate,
            angle_indices=(args.angle,),
            max_nodes_per_angle=args.max_nodes_per_angle,
            max_depth=args.max_depth,
            max_seconds=max(0.0, deadline - time.monotonic()),
            bound_mode="common-core",
            retain_pending_boxes=True,
        )
        angle = comparison._single_angle(report)  # pyright: ignore[reportPrivateUsage]
        rows: list[dict[str, Any]] = []
        partial_row: dict[str, Any] | None = None
        selected: tuple[density.PendingBox, ...] = ()
        frontier_complete = angle.stop_cause != "time_limit"
        if frontier_complete:
            comparison._require_matching_frontier(  # pyright: ignore[reportPrivateUsage]
                receipt,
                candidate_sha256=candidate_sha256,
                checker_sha256=checker_sha256,
                candidate=candidate,
                report=report,
                angle=angle,
                args=args,
            )
            selected = _selected_leaves(angle, args, candidate)
            for parent in selected:
                try:
                    rows.append(_refine_parent(candidate, parent, deadline=deadline))
                except _DiagnosticDeadlineError as error:
                    partial_row = error.partial
                    break
        _unchanged(source_path, source_bytes, label="checker source")
        _unchanged(tool_path, tool_bytes, label="refinement tool")
        _unchanged(comparison_path, comparison_bytes, label="comparison tool")
        _unchanged(inventory_path, inventory_bytes, label="pending inventory helper")
        _unchanged(args.candidate, candidate_bytes, label="candidate")
        _unchanged(args.frontier_receipt, receipt_bytes, label="frontier receipt")
    except (
        density.CandidateError,
        OSError,
        OverflowError,
        ValueError,
        RecursionError,
    ) as error:
        print(json.dumps({"status": "REFUSED", "error": str(error)}, sort_keys=True))
        return 1
    complete = frontier_complete and partial_row is None and len(rows) == len(selected)
    result = {
        "status": "DIAGNOSTIC_ONLY" if complete else "PARTIAL_DIAGNOSTIC",
        "outcome": (
            "LOCAL_CLOSURE_OBSERVED"
            if any(row["all_children_closed"] for row in rows)
            else "NO_LOCAL_CLOSURES"
        )
        if complete
        else "INCOMPLETE",
        "candidate_sha256": candidate_sha256,
        "frontier_receipt_sha256": hashlib.sha256(receipt_bytes).hexdigest(),
        "checker_source_sha256": checker_sha256,
        "refinement_tool_sha256": hashlib.sha256(tool_bytes).hexdigest(),
        "comparison_tool_sha256": hashlib.sha256(comparison_bytes).hexdigest(),
        "pending_inventory_source_sha256": hashlib.sha256(inventory_bytes).hexdigest(),
        "angle": args.angle,
        "threshold": "1",
        "max_nodes_per_angle": args.max_nodes_per_angle,
        "max_depth": args.max_depth,
        "max_seconds": args.max_seconds,
        "frontier_complete": frontier_complete,
        "frontier": angle.as_dict() if frontier_complete else None,
        "expected_parents": args.expected_depth_leaves,
        "selected_parents": len(selected),
        "processed_parents": len(rows),
        "expected_children": 4 * args.expected_depth_leaves,
        "evaluated_children": sum(len(row["children"]) for row in rows)
        + (len(partial_row["children"]) if partial_row else 0),
        "closed_parents": sum(bool(row["all_children_closed"]) for row in rows),
        "refinements": rows,
        "incomplete_parent": partial_row,
        "time_limit_reached": not complete,
        "elapsed_seconds": time.monotonic() - started,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if complete else 2


if __name__ == "__main__":
    sys.exit(main())
