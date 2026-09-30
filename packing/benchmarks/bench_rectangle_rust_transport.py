"""Measure exact resident Rust singleton versus batch transport on fixed work.

This is a geometry transport diagnostic, not a verifier or packing proof.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import resource
import time
from datetime import UTC, datetime
from fractions import Fraction
from pathlib import Path

from sqpack import rectangle_density, rust_rectangle_geometry
from sqpack.rectangle_density import ANGLE_STEP, load_candidate, square_polygon
from sqpack.rust_rectangle_geometry import RustRectangleGeometry

PROJECT = Path(__file__).resolve().parents[1]
CANDIDATE = (
    PROJECT
    / "resources/web/external-square-certificates-2026-09-22/tokoharu-density"
    / "certificates/cert_n11_L381/certified_candidate.json"
)
COUNT = 128
PAIRS = 3
MAX_SECONDS = 30


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _run(
    binary: Path,
    rectangles: tuple[rectangle_density.DensityRectangle, ...],
    polygons: tuple[rectangle_density.Polygon, ...],
    mode: str,
    deadline: float,
) -> tuple[tuple[Fraction, ...], dict[str, float]]:
    child_before = resource.getrusage(resource.RUSAGE_CHILDREN)
    cpu_before = time.process_time()
    wall_before = time.perf_counter()
    with RustRectangleGeometry(rectangles, binary, deadline=deadline) as engine:
        query_before = time.perf_counter()
        if mode == "singleton":
            values = tuple(engine.coverage(polygon) for polygon in polygons)
        else:
            values = engine.coverages(polygons)
        query_wall = time.perf_counter() - query_before
    child_after = resource.getrusage(resource.RUSAGE_CHILDREN)
    return values, {
        "session_wall_seconds": time.perf_counter() - wall_before,
        "query_wall_seconds": query_wall,
        "coordinator_cpu_seconds": time.process_time() - cpu_before,
        "child_cpu_seconds": (
            child_after.ru_utime
            + child_after.ru_stime
            - child_before.ru_utime
            - child_before.ru_stime
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    binary = args.binary.resolve(strict=True)
    candidate = load_candidate(CANDIDATE, n=11)
    cosine = (1 - ANGLE_STEP * ANGLE_STEP) / (1 + ANGLE_STEP * ANGLE_STEP)
    sine = 2 * ANGLE_STEP / (1 + ANGLE_STEP * ANGLE_STEP)
    lower = candidate.side / 2
    span = candidate.side - candidate.core_side * (cosine + sine) / 2 - lower
    polygons = tuple(
        square_polygon(
            lower + span * Fraction(index % 16, 15),
            lower + span * Fraction(index // 16, 7),
            cosine,
            sine,
            candidate.core_side,
        )
        for index in range(COUNT)
    )
    source_paths = (
        Path(__file__),
        Path(rectangle_density.__file__),
        Path(rust_rectangle_geometry.__file__),
        CANDIDATE,
        PROJECT / "sqverify_exact/src/lib.rs",
        PROJECT / "sqverify_exact/src/main.rs",
        binary,
    )
    before = {str(path): _sha(path) for path in source_paths}
    deadline = time.monotonic() + MAX_SECONDS
    records: list[dict[str, object]] = []
    paired_ratios: list[float] = []
    for pair in range(PAIRS):
        order = ("singleton", "batch") if pair % 2 == 0 else ("batch", "singleton")
        pair_values: dict[str, tuple[Fraction, ...]] = {}
        pair_timings: dict[str, dict[str, float]] = {}
        for mode in order:
            values, timing = _run(binary, candidate.rectangles, polygons, mode, deadline)
            pair_values[mode] = values
            pair_timings[mode] = timing
        if pair_values["singleton"] != pair_values["batch"]:
            raise AssertionError("singleton and batch exact coverages differ")
        if len(pair_values["batch"]) != COUNT:
            raise AssertionError("batch coverage count changed")
        paired_ratios.append(
            pair_timings["batch"]["query_wall_seconds"]
            / pair_timings["singleton"]["query_wall_seconds"]
        )
        values_digest = hashlib.sha256(
            json.dumps([str(value) for value in pair_values["batch"]]).encode()
        ).hexdigest()
        records.append(
            {
                "pair": pair,
                "order": order,
                "timing": pair_timings,
                "exact_values_sha256": values_digest,
                "exact_values_equal": True,
            }
        )
    if before != {str(path): _sha(path) for path in source_paths}:
        raise AssertionError("source or binary changed during transport diagnostic")
    if time.monotonic() >= deadline:
        raise TimeoutError("transport diagnostic exceeded its 30-second ceiling")
    receipt = {
        "status": "FIXED_WORK_TRANSPORT_DIAGNOSTIC_ONLY",
        "created_utc": datetime.now(UTC).isoformat(),
        "source_sha256": before,
        "work": {"polygons": COUNT, "pairs": PAIRS, "angle_index": 1},
        "criterion": "batch query wall <= 0.75 * singleton query wall in all three pairs",
        "criterion_met": all(ratio <= 0.75 for ratio in paired_ratios),
        "paired_batch_over_singleton_query_wall": paired_ratios,
        "observations": records,
        "scope": (
            "Exact area queries only. Session wall includes child startup/shutdown; "
            "query wall includes JSON encode/write/read/decode and Rust arithmetic. "
            "Child CPU excludes coordinator; no verifier proof or speed claim."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
