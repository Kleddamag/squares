"""Verify a rectangle-density certificate with the native exact checker."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path

from sqpack import rectangle_density
from sqpack.rectangle_density import (
    ANGLE_COUNT,
    CandidateError,
    load_candidate_bytes,
    verify_candidate,
)


def _angles(value: str) -> tuple[int, ...]:
    if value == "all":
        return tuple(range(ANGLE_COUNT))
    result: list[int] = []
    for part in value.split(","):
        if "-" in part:
            first_text, last_text = part.split("-", 1)
            try:
                first, last = int(first_text), int(last_text)
            except ValueError as error:
                raise argparse.ArgumentTypeError(
                    "angle range endpoints must be integers"
                ) from error
            if not 0 <= first <= last < ANGLE_COUNT:
                raise argparse.ArgumentTypeError("angle range must lie from 0 through 200")
            result.extend(range(first, last + 1))
        else:
            try:
                index = int(part)
            except ValueError as error:
                raise argparse.ArgumentTypeError("angle indices must be integers") from error
            if not 0 <= index < ANGLE_COUNT:
                raise argparse.ArgumentTypeError("angle index must lie from 0 through 200")
            result.append(index)
    if not result:
        raise argparse.ArgumentTypeError("at least one angle is required")
    return tuple(result)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--side", type=Fraction)
    parser.add_argument("--threshold", type=Fraction, default=Fraction(1))
    parser.add_argument("--angles", type=_angles, default=tuple(range(ANGLE_COUNT)))
    parser.add_argument("--max-nodes-per-angle", type=int, default=1_000_000)
    parser.add_argument("--max-depth", type=int, default=48)
    parser.add_argument("--max-seconds", type=float, default=300.0)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    checker_path = Path(rectangle_density.__file__)
    try:
        checker_source = checker_path.read_bytes()
        candidate_bytes = args.candidate.read_bytes()
        candidate = load_candidate_bytes(
            candidate_bytes,
            n=args.n,
            compressed=args.candidate.suffix == ".gz",
            expected_side=args.side,
            target=args.threshold,
        )
        report = verify_candidate(
            candidate,
            angle_indices=args.angles,
            max_nodes_per_angle=args.max_nodes_per_angle,
            max_depth=args.max_depth,
            max_seconds=args.max_seconds,
        )
    except (CandidateError, OSError) as error:
        print(json.dumps({"status": "REFUSED", "error": str(error)}, sort_keys=True))
        return 1
    try:
        checker_changed = checker_path.read_bytes() != checker_source
    except OSError as error:
        print(json.dumps({"status": "REFUSED", "error": str(error)}, sort_keys=True))
        return 1
    if checker_changed:
        print(
            json.dumps(
                {"status": "REFUSED", "error": "checker source changed during verification"},
                sort_keys=True,
            )
        )
        return 1
    result = report.as_dict()
    result["candidate"] = str(args.candidate)
    result["candidate_sha256"] = hashlib.sha256(candidate_bytes).hexdigest()
    result["checker"] = "sqpack.rectangle_density:native-exact-v1"
    result["checker_source_sha256"] = hashlib.sha256(checker_source).hexdigest()
    print(json.dumps(result, indent=2, sort_keys=True))
    if report.status == "VERIFIED":
        return 0
    return 1 if report.status == "COUNTEREXAMPLE" else 2


if __name__ == "__main__":
    sys.exit(main())
