"""Compare exact event construction on accepted and large proposed n=11 rows.

The 2095 rows have an accepted geometric receipt. The 1383 row is an untrusted
source proposal used only to measure event construction; it grants no case credit.
"""

# pyright: reportPrivateUsage=false
# ruff: noqa: SLF001

from __future__ import annotations

import argparse
import hashlib
import json
import time
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from strif import atomic_write_text

from devtools import check_n11_generic_fresh as generic
from devtools import check_n11_generic_sequential as sequential
from devtools import check_n11_optimality_field_mask0 as geometry
from devtools import n11_fast_exact_cover as fast
from devtools import n11_indexed_exact_cover as indexed

SOURCE_1383 = (
    Path(__file__).resolve().parents[2]
    / "attic/n11-proof-inputs/f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c/objects"
    / "34eca8dda7d8a97602b7eb0ee795b3674c52d10b9330fbd76d6f469be8f5cff1.gz"
)
SOURCE_1383_SHA = "34eca8dda7d8a97602b7eb0ee795b3674c52d10b9330fbd76d6f469be8f5cff1"
RECEIPT_2095 = generic.PACKET / "receipts/generic-mask2095-intake/full-result.json"


def _all_pair_events(
    polygons: list[fast.Polygon],
    lines: list[fast.Line],
    left: Q,
    right: Q,
    *,
    deadline: float,
) -> list[Q]:
    events = {
        point[0] for polygon in polygons for point in polygon if left <= point[0] <= right
    }
    pairs = 0
    for number, (a0, a1, m, b) in enumerate(lines):
        if time.monotonic() >= deadline:
            raise geometry.IncompleteError(f"all-pairs event deadline at edge {number}")
        for z0, z1, n, d in lines[number + 1 :]:
            pairs += 1
            if pairs % 1024 == 0 and time.monotonic() >= deadline:
                raise geometry.IncompleteError(f"all-pairs event deadline at pair {pairs}")
            if m == n:
                continue
            lo, hi = max(a0, z0, left), min(a1, z1, right)
            if lo <= hi:
                x = (d - b) / (m - n)
                if lo <= x <= hi:
                    events.add(x)
    return sorted(events)


def _row_geometry_2095(
    source: dict[str, Any], row_index: int
) -> tuple[fast.Polygon, list[fast.Polygon]]:
    step = source["steps"][0]
    row = step["rows"][row_index]
    domain = generic.convex(row["input_domain"])
    core = generic.convex(row["core_vertices"])
    prior = {
        int(owner): generic.hull(generic.points(group))
        for owner, group in step["prior_owned_hulls"].items()
    }
    forbidden = [
        generic.hull([(p[0] - q[0], p[1] - q[1]) for p in group for q in core])
        for owner, group in prior.items()
        if owner != step["owner"]
    ]
    return domain, forbidden + [generic.convex(value) for value in row["residual_polygons"]]


def _event_sample(polygons: list[fast.Polygon], *, deadline: float) -> dict[str, Any]:
    domain = polygons[0]
    left, right = min(point[0] for point in domain), max(point[0] for point in domain)
    lines = [line for poly in polygons for line in fast._compile_polygon(poly).edges]
    started = time.process_time()
    indexed_events = indexed.event_positions(
        polygons, lines, left, right, budget=geometry.Budget(deadline, 100_000)
    )
    indexed_cpu = time.process_time() - started
    started = time.process_time()
    try:
        reference_events = _all_pair_events(polygons, lines, left, right, deadline=deadline)
    except geometry.IncompleteError as error:
        return {
            "status": "REFERENCE_INCOMPLETE",
            "edge_segments": len(lines),
            "indexed_events": len(indexed_events),
            "indexed_process_cpu_seconds": indexed_cpu,
            "reference_error": str(error),
        }
    reference_cpu = time.process_time() - started
    if reference_events != indexed_events:
        raise ValueError("indexed event positions differ from all-pairs positions")
    return {
        "status": "MATCHED_EXACT_EVENTS",
        "edge_segments": len(lines),
        "events": len(indexed_events),
        "indexed_process_cpu_seconds": indexed_cpu,
        "reference_process_cpu_seconds": reference_cpu,
        "event_speedup": reference_cpu / indexed_cpu,
    }


def run(*, max_seconds: float) -> dict[str, Any]:
    if not 0 < max_seconds <= 60:
        raise ValueError("benchmark ceiling must be in (0, 60]")
    if not indexed.dependencies_unchanged():
        raise ValueError("indexed dependencies changed")
    started = time.monotonic()
    deadline = started + max_seconds
    accepted_source = generic._load_pin(
        generic.OBJECTS / f"{generic.SOURCE_PIN[0]}.gz", generic.SOURCE_PIN
    )
    accepted_receipt = json.loads(RECEIPT_2095.read_text())
    if accepted_receipt["status"] != "PASS_ONE_GENERIC_EXCLUSION":
        raise ValueError("accepted 2095 receipt is incomplete")
    accepted: list[dict[str, Any]] = []
    for row_index in (0, 22, 31):
        domain, regions = _row_geometry_2095(accepted_source, row_index)
        event_result = _event_sample([domain, *regions], deadline=deadline)
        if event_result["status"] != "MATCHED_EXACT_EVENTS":
            raise geometry.IncompleteError("accepted control did not finish both event methods")
        fast_result = fast.exact_union_cover(
            domain, regions, budget=geometry.Budget(deadline, 100_000)
        )
        indexed_result = indexed.exact_union_cover(
            domain, regions, budget=geometry.Budget(deadline, 100_000)
        )
        expected = accepted_receipt["step_timings"][0]["row_timings"][row_index]
        if fast_result != indexed_result or (
            indexed_result["events"],
            indexed_result["probes"],
        ) != (expected["events"], expected["probes"]):
            raise ValueError(f"accepted row {row_index} cover result differs")
        accepted.append({"row": row_index, **event_result, "cover": indexed_result})

    proposed: list[dict[str, Any]] = []
    manifest = sequential.load_manifest(sequential.MANIFEST)
    source_1383 = sequential.load_object(SOURCE_1383_SHA, manifest, SOURCE_1383.parent)
    step = source_1383["steps"][1]
    row = step["rows"][2]
    domain = generic.convex(row["input_domain"])
    residuals = [generic.convex(value) for value in row["residual_polygons"]]
    for count in (32, 64, 128, 256, len(residuals)):
        if time.monotonic() >= deadline:
            proposed.append({"residual_regions": count, "status": "BUDGET_EXHAUSTED"})
            break
        proposed.append(
            {
                "residual_regions": count,
                **_event_sample([domain, *residuals[:count]], deadline=deadline),
            }
        )
    core = generic.convex(row["core_vertices"])
    prior = {
        int(owner): generic.hull(generic.points(group))
        for owner, group in step["prior_owned_hulls"].items()
    }
    forbidden = [
        generic.hull([(p[0] - q[0], p[1] - q[1]) for p in group for q in core])
        for owner, group in prior.items()
        if owner != step["owner"]
    ]
    collisions = [generic.convex(value["vertices"]) for value in row["collision_regions"]]
    if time.monotonic() < deadline:
        full_proposal = _event_sample(
            [domain, *forbidden, *collisions, *residuals], deadline=deadline
        )
    else:
        full_proposal = {"status": "BUDGET_EXHAUSTED"}
    return {
        "schema": "n11_indexed_cover_benchmark_v1",
        "status": "DIAGNOSTIC_ONLY",
        "max_seconds": max_seconds,
        "wall_seconds": time.monotonic() - started,
        "source_sha256": {
            "benchmark": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "indexed": hashlib.sha256(Path(indexed.__file__).read_bytes()).hexdigest(),
            "fast": hashlib.sha256(Path(fast.__file__).read_bytes()).hexdigest(),
            "accepted_source": generic.SOURCE_PIN[0],
            "accepted_receipt": hashlib.sha256(RECEIPT_2095.read_bytes()).hexdigest(),
            "proposed_source": SOURCE_1383_SHA,
            "proposed_manifest": hashlib.sha256(sequential.MANIFEST.read_bytes()).hexdigest(),
        },
        "accepted_rows": accepted,
        "proposed_row": {
            "case": 1383,
            "node": 0,
            "step": 1,
            "row": 2,
            "residual_samples": proposed,
            "full_proposal": full_proposal,
            "full_proposal_region_counts": {
                "forbidden": len(forbidden),
                "collision": len(collisions),
                "residual": len(residuals),
            },
        },
        "scope": "The 1383 row is source-proposal geometry, not an accepted proof row.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--max-seconds", type=float, default=30.0)
    args = parser.parse_args()
    result = run(max_seconds=args.max_seconds)
    atomic_write_text(args.out, json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "status": result["status"],
                "full_proposal": result["proposed_row"]["full_proposal"],
            }
        )
    )


if __name__ == "__main__":
    main()
