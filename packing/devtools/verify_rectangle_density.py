"""Verify a rectangle-density certificate with the native exact checker."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from collections.abc import Iterator
from contextlib import contextmanager
from fractions import Fraction
from pathlib import Path

from sqpack import rectangle_density, rust_rectangle_geometry
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
    parser.add_argument(
        "--bound-mode", choices=("common-core", "corner-min"), default="common-core"
    )
    parser.add_argument("--backend", choices=("python", "rust"), default="python")
    parser.add_argument("--rust-binary", type=Path)
    parser.add_argument("--retain-pending-boxes", action="store_true")
    parser.add_argument(
        "--timing",
        action="store_true",
        help=(
            "report read/hash, admission, verification, and source-recheck wall and "
            "process CPU time; excludes startup, argument parsing, and output serialization"
        ),
    )
    return parser


class _PhaseTiming:
    def __init__(self, *, enabled: bool, backend: str) -> None:
        self.enabled = enabled
        self.backend = backend
        self.phases: dict[str, dict[str, float]] = {}

    @contextmanager
    def phase(self, name: str) -> Iterator[None]:
        if not self.enabled:
            yield
            return
        wall_start = time.perf_counter()
        cpu_start = time.process_time()
        try:
            yield
        finally:
            self.phases[name] = {
                "wall_seconds": time.perf_counter() - wall_start,
                "process_cpu_seconds": time.process_time() - cpu_start,
            }

    def attach(self, result: dict[str, object]) -> None:
        if self.enabled:
            rust_backend = self.backend == "rust"
            result["timing"] = {
                "wall_clock": "perf_counter",
                "cpu_clock": "process_time",
                "process_cpu_scope": (
                    "Python coordinator only; Rust child CPU excluded"
                    if rust_backend
                    else "Python coordinator including native exact geometry"
                ),
                "excluded": [
                    "module_startup_and_argument_parsing",
                    "receipt_build_serialization_and_output",
                ],
                "phases": self.phases,
            }


def _refused(error: Exception | str, timing: _PhaseTiming) -> int:
    result: dict[str, object] = {"status": "REFUSED", "error": str(error)}
    timing.attach(result)
    print(json.dumps(result, sort_keys=True))
    return 1


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    checker_path = Path(rectangle_density.__file__)
    adapter_path = Path(rust_rectangle_geometry.__file__)
    timing = _PhaseTiming(enabled=args.timing, backend=args.backend)
    try:
        with timing.phase("input_read_hash"):
            checker_source = checker_path.read_bytes()
            candidate_bytes = args.candidate.read_bytes()
            candidate_sha256 = hashlib.sha256(candidate_bytes).hexdigest()
            checker_sha256 = hashlib.sha256(checker_source).hexdigest()
            adapter_source = adapter_path.read_bytes() if args.backend == "rust" else None
        with timing.phase("admission"):
            candidate = load_candidate_bytes(
                candidate_bytes,
                n=args.n,
                compressed=args.candidate.suffix == ".gz",
                expected_side=args.side,
                target=args.threshold,
            )
        with timing.phase("verification"):
            report = verify_candidate(
                candidate,
                angle_indices=args.angles,
                max_nodes_per_angle=args.max_nodes_per_angle,
                max_depth=args.max_depth,
                max_seconds=args.max_seconds,
                bound_mode=args.bound_mode,
                retain_pending_boxes=args.retain_pending_boxes,
                backend=args.backend,
                rust_binary=args.rust_binary,
            )
    except (CandidateError, OSError) as error:
        return _refused(error, timing)
    try:
        with timing.phase("source_recheck"):
            checker_changed = checker_path.read_bytes() != checker_source
            adapter_changed = (
                adapter_source is not None and adapter_path.read_bytes() != adapter_source
            )
    except OSError as error:
        return _refused(error, timing)
    if checker_changed or adapter_changed:
        return _refused("checker source changed during verification", timing)
    result = report.as_dict()
    result["candidate"] = str(args.candidate)
    result["candidate_sha256"] = candidate_sha256
    result["checker"] = (
        "sqpack.rectangle_density:rust-common-core-v1"
        if args.backend == "rust"
        else "sqpack.rectangle_density:native-exact-v2"
    )
    result["checker_source_sha256"] = checker_sha256
    if adapter_source is not None:
        result["rust_adapter_source_sha256"] = hashlib.sha256(adapter_source).hexdigest()
    timing.attach(result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if report.status == "VERIFIED":
        return 0
    return 1 if report.status == "COUNTEREXAMPLE" else 2


if __name__ == "__main__":
    sys.exit(main())
