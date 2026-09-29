"""Compare exact bounds on one native verifier frontier; never certify it."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
import time
from fractions import Fraction
from pathlib import Path

from sqpack import rectangle_density as density


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--frontier-receipt", type=Path, required=True)
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--side", type=Fraction)
    parser.add_argument("--angle", type=int, default=1)
    parser.add_argument("--max-nodes-per-angle", type=int, default=100)
    parser.add_argument("--max-depth", type=int, default=20)
    parser.add_argument("--max-seconds", type=float, default=30.0)
    return parser


def _require_complete_frontier(
    frontier: density.AngleVerification,
) -> tuple[density.PendingBox, ...]:
    if (
        frontier.pending_boxes is None
        or len(frontier.pending_boxes) != frontier.unresolved_leaves
    ):
        raise density.CandidateError("frontier diagnostics are incomplete")
    return frontier.pending_boxes


def _require_unchanged(path: Path, original: bytes, *, label: str) -> None:
    if path.read_bytes() != original:
        raise density.CandidateError(f"{label} changed during comparison")


def _single_angle(report: density.VerificationReport) -> density.AngleVerification:
    if len(report.angles) != 1:
        raise density.CandidateError("exactly one frontier angle was required")
    return report.angles[0]


def _require_corner_dominance(common: Fraction, corner: Fraction) -> None:
    if corner < common:
        raise density.CandidateError("corner bound fell below common-core bound")


def _require_matching_frontier(
    receipt: object,
    *,
    candidate_sha256: str,
    checker_sha256: str,
    candidate: density.RectangleDensityCandidate,
    report: density.VerificationReport,
    angle: density.AngleVerification,
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
        "status": report.status,
    }
    if any(receipt.get(key) != value for key, value in expected.items()):
        raise density.CandidateError("frontier receipt input, source, or settings differ")
    if receipt.get("angles") != [angle.as_dict()]:
        raise density.CandidateError("frontier receipt boxes differ from this exact replay")
    if angle.status != "INCONCLUSIVE" or angle.unresolved_leaves == 0:
        raise density.CandidateError("frontier receipt has no inconclusive boxes to compare")


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if not math.isfinite(args.max_seconds) or args.max_seconds < 0:
        print(
            json.dumps(
                {"status": "REFUSED", "error": "max_seconds must be finite and nonnegative"}
            )
        )
        return 1
    if not 1 <= args.angle < density.ANGLE_COUNT:
        print(json.dumps({"status": "REFUSED", "error": "angle must be 1 through 200"}))
        return 1
    source_path = Path(density.__file__)
    tool_path = Path(__file__)
    started = time.monotonic()
    deadline = started + args.max_seconds
    try:
        source_bytes = source_path.read_bytes()
        tool_bytes = tool_path.read_bytes()
        candidate_bytes = args.candidate.read_bytes()
        receipt_bytes = args.frontier_receipt.read_bytes()
        receipt = json.loads(receipt_bytes)
        candidate = density.load_candidate_bytes(
            candidate_bytes,
            n=args.n,
            compressed=args.candidate.suffix == ".gz",
            expected_side=args.side,
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
        frontier = _single_angle(report)
        candidate_sha256 = hashlib.sha256(candidate_bytes).hexdigest()
        checker_sha256 = hashlib.sha256(source_bytes).hexdigest()
        _require_matching_frontier(
            receipt,
            candidate_sha256=candidate_sha256,
            checker_sha256=checker_sha256,
            candidate=candidate,
            report=report,
            angle=frontier,
            args=args,
        )
        pending_boxes = _require_complete_frontier(frontier)
        frontier_elapsed = time.monotonic() - started
        comparisons: list[dict[str, object]] = []
        timed_out = False
        for pending in pending_boxes:
            if time.monotonic() >= deadline:
                timed_out = True
                break
            common_started = time.monotonic()
            common = density.pending_common_core_bound(candidate, pending)
            common_elapsed = time.monotonic() - common_started
            corner_started = time.monotonic()
            try:
                corner = density.pending_corner_min_bound(candidate, pending, deadline=deadline)
            except TimeoutError:
                timed_out = True
                break
            corner_elapsed = time.monotonic() - corner_started
            _require_corner_dominance(common, corner)
            stronger = max(common, corner)
            comparisons.append(
                {
                    "box": pending.as_dict(),
                    "common_core_bound": str(common),
                    "corner_min_bound": str(corner),
                    "combined_bound": str(stronger),
                    "common_core_seconds": common_elapsed,
                    "corner_min_seconds": corner_elapsed,
                    "closes_old_gap": common < candidate.target <= stronger,
                }
            )
        _require_unchanged(source_path, source_bytes, label="checker source")
        _require_unchanged(tool_path, tool_bytes, label="comparison tool")
        _require_unchanged(args.candidate, candidate_bytes, label="candidate")
        _require_unchanged(args.frontier_receipt, receipt_bytes, label="frontier receipt")
    except (density.CandidateError, OSError, OverflowError, ValueError) as error:
        print(json.dumps({"status": "REFUSED", "error": str(error)}, sort_keys=True))
        return 1
    result = {
        "status": "DIAGNOSTIC_ONLY",
        "candidate": str(args.candidate),
        "candidate_sha256": candidate_sha256,
        "frontier_receipt": str(args.frontier_receipt),
        "frontier_receipt_sha256": hashlib.sha256(receipt_bytes).hexdigest(),
        "checker": "sqpack.rectangle_density:native-exact-v2",
        "checker_source_sha256": checker_sha256,
        "comparison_tool_sha256": hashlib.sha256(tool_bytes).hexdigest(),
        "n": candidate.n,
        "L": str(candidate.side),
        "B": str(candidate.core_side),
        "threshold": str(candidate.target),
        "max_nodes_per_angle": args.max_nodes_per_angle,
        "max_depth": args.max_depth,
        "max_seconds": args.max_seconds,
        "angle": args.angle,
        "frontier": frontier.as_dict(),
        "frontier_complete": True,
        "frontier_seconds": frontier_elapsed,
        "comparisons": comparisons,
        "compared_boxes": len(comparisons),
        "pending_boxes": len(pending_boxes),
        "comparison_complete": not timed_out and len(comparisons) == len(pending_boxes),
        "time_limit_reached": timed_out,
        "elapsed_seconds": time.monotonic() - started,
        "closed_boxes": sum(bool(row["closes_old_gap"]) for row in comparisons),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["comparison_complete"] else 2


if __name__ == "__main__":
    sys.exit(main())
