"""Differential exact-area controls for the standalone Rust batch kernel.

This checks a geometry primitive against Python's reviewed exact oracle. It does
not promote any candidate, box frontier, or angle to a packing proof.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import resource
import subprocess
import time
from datetime import UTC, datetime
from fractions import Fraction
from pathlib import Path
from typing import Any

from sqpack import rectangle_density, rust_rectangle_geometry
from sqpack.rectangle_density import (
    ANGLE_STEP,
    DensityRectangle,
    RectangleDensityCandidate,
    exact_intersection_area,
    load_candidate,
    square_polygon,
    verify_candidate,
)
from sqpack.rust_rectangle_geometry import MAX_BINARY_BYTES

PROJECT = Path(__file__).resolve().parents[1]
ANALYTIC = PROJECT / "resources/web/wand125-tools-2026-09-29/native-analytic-control.json"
TOKOHARU = (
    PROJECT
    / "resources/web/external-square-certificates-2026-09-22/tokoharu-density"
    / "certificates/cert_n11_L381/certified_candidate.json"
)

type Polygon = tuple[tuple[Fraction, Fraction], ...]


def _batch(
    rectangles: tuple[DensityRectangle, ...], polygons: tuple[Polygon, ...]
) -> dict[str, object]:
    return {
        "version": 1,
        "rectangles": [
            {
                "left": str(rectangle.left),
                "bottom": str(rectangle.bottom),
                "right": str(rectangle.right),
                "top": str(rectangle.top),
                "density": str(rectangle.density),
            }
            for rectangle in rectangles
        ],
        "polygons": [[[str(x), str(y)] for x, y in polygon] for polygon in polygons],
    }


def _run(binary: Path, payload: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(binary)],
        input=payload,
        text=True,
        capture_output=True,
        timeout=20,
        check=False,
    )


def _compare(
    binary: Path,
    rectangles: tuple[DensityRectangle, ...],
    polygons: tuple[Polygon, ...],
) -> None:
    payload = json.dumps(_batch(rectangles, polygons), separators=(",", ":"))
    result = _run(binary, payload)
    if result.returncode != 0 or result.stderr:
        raise AssertionError(f"Rust exact batch failed: {result.stderr}")
    output: Any = json.loads(result.stdout)
    if not isinstance(output, dict) or set(output) != {"version", "coverages"}:
        raise AssertionError("Rust batch output schema changed")
    if output["version"] != 1 or not isinstance(output["coverages"], list):
        raise AssertionError("Rust batch output version or coverage type changed")
    if not all(isinstance(value, str) for value in output["coverages"]):
        raise AssertionError("Rust batch emitted a non-string rational")
    expected = [
        sum(
            (
                rectangle.density * exact_intersection_area(rectangle, polygon)
                for rectangle in rectangles
            ),
            Fraction(),
        )
        for polygon in polygons
    ]
    actual = [Fraction(value) for value in output["coverages"]]
    if len(actual) != len(expected):
        raise AssertionError("Rust batch omitted or added polygon results")
    if actual != expected:
        first = next(
            index for index, (a, b) in enumerate(zip(actual, expected, strict=True)) if a != b
        )
        raise AssertionError(
            f"exact coverage differs at polygon {first}: {actual[first]} != {expected[first]}"
        )


def _angle_polygon(
    candidate: RectangleDensityCandidate, index: int, x: Fraction, y: Fraction
) -> Polygon:
    tangent = index * ANGLE_STEP
    denominator = 1 + tangent * tangent
    cosine = (1 - tangent * tangent) / denominator
    sine = 2 * tangent / denominator
    return square_polygon(x, y, cosine, sine, candidate.core_side)


def _adversarial() -> tuple[tuple[DensityRectangle, ...], tuple[Polygon, ...]]:
    f = Fraction
    huge = f(10**160 + 1, 10**80 + 3)
    rectangles = (
        DensityRectangle(f(0), f(0), f(1), f(1), f(3, 7)),
        DensityRectangle(f(1, 2), f(0), f(3, 2), f(1), f(11, 13)),
        DensityRectangle(huge, huge, huge + f(1, 10**20), huge + f(1, 10**20), f(7, 5)),
    )
    square: Polygon = ((f(0), f(0)), (f(1), f(0)), (f(1), f(1)), (f(0), f(1)))
    return rectangles, (
        square,
        tuple(reversed(square)),
        ((f(1), f(0)), (f(2), f(0)), (f(2), f(1)), (f(1), f(1))),
        ((f(3, 2), f(0)), (f(5, 2), f(0)), (f(5, 2), f(1)), (f(3, 2), f(1))),
        ((f(1), f(1)),),
        ((f(0), f(0)), (f(1), f(0))),
        ((huge, huge), (huge + f(1, 10**20), huge), (huge, huge + f(1, 10**20))),
    )


def _refusals(binary: Path) -> None:
    valid = {
        "version": 1,
        "rectangles": [{"left": "0", "bottom": "0", "right": "1", "top": "1", "density": "1"}],
        "polygons": [[["0", "0"], ["1", "0"], ["0", "1"]]],
    }
    examples = {
        "parse": "{",
        "duplicate": '{"version":1,"version":1,"rectangles":[],"polygons":[]}',
        "zero denominator": json.dumps(valid).replace('"left": "0"', '"left": "1/0"'),
        "huge integer": json.dumps(valid).replace(
            '"left": "0"', '"left": "9' + "9" * 1300 + '"'
        ),
        "degenerate rectangle": json.dumps(valid).replace('"right": "1"', '"right": "0"'),
        "negative density": json.dumps(valid).replace('"density": "1"', '"density": "-1"'),
        "nonconvex": json.dumps(valid).replace(
            '[["0", "0"], ["1", "0"], ["0", "1"]]',
            '[["0", "0"], ["2", "0"], ["1", "1"], ["2", "2"], ["0", "2"]]',
        ),
        "self-crossing star": json.dumps(valid).replace(
            '[["0", "0"], ["1", "0"], ["0", "1"]]',
            '[["0", "3"], ["2", "-2"], ["-3", "1"], ["3", "1"], ["-2", "-2"]]',
        ),
        "wrong version": json.dumps(valid).replace('"version": 1', '"version": 2'),
        "numeric rational": json.dumps(valid).replace('"left": "0"', '"left": 0'),
    }
    for name, payload in examples.items():
        result = _run(binary, payload)
        if (
            result.returncode == 0
            or result.stdout
            or not result.stderr.startswith("sqverify-exact:")
        ):
            raise AssertionError(f"Rust batch accepted or misreported invalid {name}")


def _whole_verifier_controls(
    binary: Path, analytic: RectangleDensityCandidate, tokoharu: RectangleDensityCandidate
) -> None:
    """Compare complete and bounded verifier decisions, not just area primitives."""
    for candidate, indices, nodes, depth, retain in (
        (analytic, tuple(range(201)), 10_000, 20, False),
        (tokoharu, (1,), 100, 20, True),
    ):
        options = {
            "angle_indices": indices,
            "max_nodes_per_angle": nodes,
            "max_depth": depth,
            "max_seconds": 30,
            "retain_pending_boxes": retain,
        }
        python = verify_candidate(candidate, **options)
        rust = verify_candidate(candidate, **options, backend="rust", rust_binary=binary)
        rust_record = rust.as_dict()
        for key in ("backend", "rust_binary_sha256", "rust_table_sha256", "backend_timeout"):
            rust_record.pop(key)
        if rust_record != python.as_dict():
            raise AssertionError("resident Rust verifier changed the exact angle census")
        if candidate is analytic and rust.status != "VERIFIED":
            raise AssertionError("resident Rust verifier missed complete analytic admission")
        if candidate is tokoharu and rust.status != "INCONCLUSIVE":
            raise AssertionError("resident Rust verifier changed the bounded n11 status")


def _benchmark(
    binary: Path,
    analytic: RectangleDensityCandidate,
    tokoharu: RectangleDensityCandidate,
    output: Path,
) -> None:
    """Retain a matched-work observation; this never gates correctness on speed."""
    with binary.open("rb") as binary_file:
        binary_source = binary_file.read(MAX_BINARY_BYTES + 1)
    if not binary_source or len(binary_source) > MAX_BINARY_BYTES:
        raise AssertionError("benchmark binary exceeds the verifier's binary limit")
    source_paths = (
        Path(__file__),
        Path(rectangle_density.__file__),
        Path(rust_rectangle_geometry.__file__),
        PROJECT / "sqverify_exact/Cargo.toml",
        PROJECT / "sqverify_exact/rust-toolchain.toml",
        PROJECT / "sqverify_exact/src/lib.rs",
        PROJECT / "sqverify_exact/src/main.rs",
        PROJECT / "sqverify_exact/Cargo.lock",
    )
    source_bytes = {str(path.relative_to(PROJECT)): path.read_bytes() for path in source_paths}
    observations: list[dict[str, object]] = []
    for name, candidate, indices, nodes, depth, retain, input_path in (
        ("analytic-n3-all201", analytic, tuple(range(201)), 10_000, 20, False, ANALYTIC),
        ("tokoharu-n11-angle1-1000", tokoharu, (1,), 1_000, 20, True, TOKOHARU),
    ):
        reports: dict[str, dict[str, object]] = {}
        timing: dict[str, dict[str, float]] = {}
        for backend in ("python", "rust"):
            before_child = resource.getrusage(resource.RUSAGE_CHILDREN)
            start = time.perf_counter()
            report = verify_candidate(
                candidate,
                angle_indices=indices,
                max_nodes_per_angle=nodes,
                max_depth=depth,
                max_seconds=30,
                retain_pending_boxes=retain,
                backend=backend,
                rust_binary=binary if backend == "rust" else None,
            )
            wall = time.perf_counter() - start
            after_child = resource.getrusage(resource.RUSAGE_CHILDREN)
            record = report.as_dict()
            if backend == "rust":
                for key in (
                    "backend",
                    "rust_binary_sha256",
                    "rust_table_sha256",
                    "backend_timeout",
                ):
                    record.pop(key)
            reports[backend] = record
            timing[backend] = {
                "wall_seconds": wall,
                "child_cpu_seconds": (after_child.ru_utime + after_child.ru_stime)
                - (before_child.ru_utime + before_child.ru_stime),
            }
        if reports["python"] != reports["rust"]:
            raise AssertionError(f"matched verifier census changed for {name}")
        encoded = json.dumps(reports["python"], sort_keys=True, separators=(",", ":")).encode()
        observations.append(
            {
                "name": name,
                "input_sha256": hashlib.sha256(input_path.read_bytes()).hexdigest(),
                "status": reports["python"]["status"],
                "angles": len(indices),
                "nodes": sum(angle.nodes for angle in report.angles),
                "identical_exact_report": True,
                "normalized_report_sha256": hashlib.sha256(encoded).hexdigest(),
                "timing": timing,
            }
        )
    if binary.read_bytes() != binary_source or any(
        path.read_bytes() != source_bytes[str(path.relative_to(PROJECT))]
        for path in source_paths
    ):
        raise AssertionError("exact backend source changed during the matched benchmark")
    receipt = {
        "status": "MATCHED_EXACT_REPORTS_NO_SPEED_PROMOTION",
        "created_utc": datetime.now(UTC).isoformat(),
        "binary_sha256": hashlib.sha256(binary_source).hexdigest(),
        "source_sha256": {
            name: hashlib.sha256(source).hexdigest() for name, source in source_bytes.items()
        },
        "observations": observations,
        "timing_scope": (
            "wall includes admission, resident-child startup, IPC, work, and shutdown; "
            "child CPU excludes coordinator CPU"
        ),
        "replay": (
            ".venv/bin/python3 -m devtools.check_exact_rust_kernel "
            "--binary <release-binary> --benchmark-output <receipt.json>"
        ),
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", required=True, type=Path)
    parser.add_argument("--benchmark-output", type=Path)
    args = parser.parse_args()
    binary: Path = args.binary.resolve(strict=True)
    rectangles, polygons = _adversarial()
    golden = (
        Fraction(155, 182),
        Fraction(155, 182),
        Fraction(11, 26),
        Fraction(),
        Fraction(),
        Fraction(),
        Fraction(7, 10**41),
    )
    oracle = tuple(
        sum(
            (
                rectangle.density * exact_intersection_area(rectangle, polygon)
                for rectangle in rectangles
            ),
            Fraction(),
        )
        for polygon in polygons
    )
    if oracle != golden:
        raise AssertionError("Python exact oracle no longer matches analytic golden controls")
    _compare(binary, rectangles, polygons)

    analytic = load_candidate(ANALYTIC, n=3, expected_side=Fraction(3, 2))
    center = analytic.side / 2
    analytic_polygons = tuple(
        _angle_polygon(analytic, index, center, center) for index in range(201)
    )
    _compare(binary, analytic.rectangles, analytic_polygons)

    tokoharu = load_candidate(TOKOHARU, n=11, expected_side=Fraction(381, 100))
    center = tokoharu.side / 2
    tokoharu_polygons = (
        _angle_polygon(tokoharu, 1, center, center),
        _angle_polygon(tokoharu, 1, center + Fraction(1, 10), center),
    )
    _compare(binary, tokoharu.rectangles, tokoharu_polygons)
    _refusals(binary)
    _whole_verifier_controls(binary, analytic, tokoharu)
    if args.benchmark_output is not None:
        _benchmark(binary, analytic, tokoharu, args.benchmark_output)
    sources = {
        "analytic_sha256": hashlib.sha256(ANALYTIC.read_bytes()).hexdigest(),
        "tokoharu_sha256": hashlib.sha256(TOKOHARU.read_bytes()).hexdigest(),
        "polygons_checked": len(polygons) + len(analytic_polygons) + len(tokoharu_polygons),
        "refusals_checked": 10,
        "whole_verifier_controls": 2,
    }
    print("EXACT RUST GEOMETRY DIFFERENTIAL PASSED " + json.dumps(sources, sort_keys=True))


if __name__ == "__main__":
    main()
