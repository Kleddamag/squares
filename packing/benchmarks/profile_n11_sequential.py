"""Inventory nonfield row costs and profile the pinned generic pilot.

The manifest supplies proposals, not verified work. The profile repeats selected
first-step rows of the accepted mask-2095 pilot without promoting another case.
"""

# Profiling deliberately calls the frozen checker's row internals without modifying them.
# ruff: noqa: SLF001
# pyright: reportPrivateUsage=false

from __future__ import annotations

import argparse
import cProfile
import gzip
import hashlib
import json
import pstats
import statistics
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, cast

from strif import atomic_write_text

from devtools import check_n11_generic_fresh as generic
from devtools import check_n11_optimality_field_mask0 as geometry

PACKET = geometry.PACKET
MANIFEST = PACKET / "receipts/nonfield-manifest/manifest.json.gz"
BASELINE = PACKET / "receipts/generic-mask2095-intake/full-result.json"
MANIFEST_SHA = "a730804aef482e9f32d4b579608a52727b55fa2df8fa4327dfbeae82c0184520"
GENERIC_SHA = "e8fcfd02560d09e7a2a5b2622976ab021ef15a4456a2824b37abae926f6ab7d3"


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _percentile(values: list[int], numerator: int, denominator: int) -> int:
    ordered = sorted(values)
    return ordered[(len(ordered) - 1) * numerator // denominator]


def inventory(manifest_path: Path, baseline_path: Path) -> dict[str, Any]:
    raw = manifest_path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != MANIFEST_SHA:
        raise ValueError("nonfield manifest bytes changed")
    manifest = json.loads(gzip.decompress(raw))
    receipt = json.loads(baseline_path.read_text())
    if receipt["status"] != "PASS_ONE_GENERIC_EXCLUSION" or receipt["rows_checked"] != 160:
        raise ValueError("generic pilot receipt is incomplete")
    if (
        receipt["source_sha256"]["checker"] != GENERIC_SHA
        or _digest(Path(generic.__file__)) != GENERIC_SHA
    ):
        raise ValueError("generic pilot checker differs from receipt")
    if receipt["source_sha256"]["geometry"] != _digest(Path(geometry.__file__)):
        raise ValueError("generic pilot geometry differs from receipt")
    cases = manifest["cases"]
    if len(cases) != 276 or len({row["mask_index"] for row in cases}) != 276:
        raise ValueError("nonfield case inventory changed")
    rows = []
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for case in cases:
        entry = {
            "mask_index": case["mask_index"],
            "family": case["family"],
            "adapter": case["adapter"],
            "source_profile": case["source_profile"],
            "reported_rows": case["reported_rows"],
            "ancestry_depth": len(case["ordered_ancestry_proposal"]),
            "declared_compressed_bytes": case["declared_compressed_bytes"],
            "declared_decoded_bytes": case["declared_decoded_bytes"],
            "reported_arrangement_slabs": sum(
                item["reported_arrangement_slabs"] for item in case["ordered_ancestry_proposal"]
            ),
        }
        rows.append(entry)
        groups[case["adapter"]].append(entry)
    pilot_rows = [row for step in receipt["step_timings"] for row in step["row_timings"]]
    if len(pilot_rows) != 160:
        raise ValueError("generic pilot row timings are incomplete")
    pilot_cpu = sum(float(row["process_cpu_seconds"]) for row in pilot_rows)
    sequential_rows = sum(row["reported_rows"] for row in groups["sequential_wall_seed"])
    pilot_rate = pilot_cpu / len(pilot_rows)
    return {
        "schema": "n11_nonfield_row_cost_inventory_v1",
        "status": "METADATA_AND_SCENARIOS_ONLY",
        "geometry_verified_for_manifest_cases": False,
        "input_sha256": {"manifest": MANIFEST_SHA, "baseline_receipt": _digest(baseline_path)},
        "case_count": len(rows),
        "reported_rows_total": sum(row["reported_rows"] for row in rows),
        "sequential_reported_rows": sequential_rows,
        "adapters": {
            name: {"cases": len(group), "reported_rows": sum(r["reported_rows"] for r in group)}
            for name, group in sorted(groups.items())
        },
        "families": dict(sorted(Counter(row["family"] for row in rows).items())),
        "ancestry_depths": dict(sorted(Counter(row["ancestry_depth"] for row in rows).items())),
        "sequential_row_quantiles": {
            "min": min(row["reported_rows"] for row in groups["sequential_wall_seed"]),
            "p50": _percentile(
                [row["reported_rows"] for row in groups["sequential_wall_seed"]], 1, 2
            ),
            "p90": _percentile(
                [row["reported_rows"] for row in groups["sequential_wall_seed"]], 9, 10
            ),
            "max": max(row["reported_rows"] for row in groups["sequential_wall_seed"]),
        },
        "pilot": {
            "mask_index": 2095,
            "rows": len(pilot_rows),
            "row_cpu_seconds_total": pilot_cpu,
            "row_cpu_seconds_median": statistics.median(
                float(row["process_cpu_seconds"]) for row in pilot_rows
            ),
            "row_cpu_seconds_mean": pilot_rate,
            "row_events_median": statistics.median(row["events"] for row in pilot_rows),
            "row_events_max": max(row["events"] for row in pilot_rows),
            "seed_process_cpu_seconds": receipt["seed_process_cpu_seconds"],
            "child_process_cpu_seconds": receipt["child_process_cpu_seconds"],
        },
        "illustrative_sequential_cpu_hours": {
            str(multiplier): sequential_rows * pilot_rate * multiplier / 3600
            for multiplier in (0.5, 1, 2)
        },
        "scenario_caveat": (
            "Pilot mask 2095 is a different source with 160 independently checked rows. "
            "The multipliers apply its mean row CPU cost to reported, unverified "
            "sequential rows; they exclude seed, ancestry, loading, and adapter costs "
            "and are not a runtime estimate or proof credit."
        ),
        "cases": sorted(rows, key=lambda row: row["mask_index"]),
    }


def profile_first_step_rows(indices: list[int]) -> dict[str, Any]:
    if not indices or any(index < 0 or index >= 32 for index in indices):
        raise ValueError("select first-step row indices in 0..31")
    if _digest(Path(generic.__file__)) != GENERIC_SHA:
        raise ValueError("generic checker source changed")
    if _digest(Path(geometry.__file__)) != generic.GEOMETRY_SHA:
        raise ValueError("shared geometry source changed")
    started = time.monotonic()
    budget = geometry.Budget(started + 55, 50_000)
    geometry.admit_d4_receipt()
    cover = generic._load_pin(
        generic.COVER,
        (geometry.COVER_SHA, 773_471, geometry.COVER_LFS_SHA, 25_016),
    )
    source = generic._load_pin(
        generic.OBJECTS / f"{generic.SOURCE_PIN[0]}.gz", generic.SOURCE_PIN
    )
    seed = generic._load_pin(generic.OBJECTS / f"{generic.SEED_PIN[0]}.gz", generic.SEED_PIN)
    groups, rows, world = generic._seed(seed, cover, budget=budget)
    generic._source_header(source, groups, rows)
    step = source["steps"][0]
    if step["index"] != 0 or step["owner"] != 6:
        raise ValueError("pilot first step changed")
    findings = []
    for index in indices:
        profiler = cProfile.Profile()
        row_started = time.monotonic()
        profiler.enable()
        coverage, _, _, _ = generic._check_row(
            source,
            step,
            step["rows"][index],
            index,
            6,
            prior=groups,
            predecessor=rows[6][index],
            world=world,
            budget=budget,
        )
        profiler.disable()
        statistics_by_function = cast(
            dict[tuple[str, int, str], tuple[int, int, float, float, object]],
            vars(pstats.Stats(profiler))["stats"],
        )
        hotspots = sorted(
            statistics_by_function.items(), key=lambda item: item[1][3], reverse=True
        )
        findings.append(
            {
                "row": index,
                "coverage": coverage,
                "profiled_wall_seconds": time.monotonic() - row_started,
                "profiled_calls": sum(item[1][1] for item in statistics_by_function.items()),
                "top_cumulative": [
                    {
                        "file": str(Path(key[0]).name),
                        "line": key[1],
                        "function": key[2],
                        "calls": value[1],
                        "own_seconds": value[2],
                        "cumulative_seconds": value[3],
                    }
                    for key, value in hotspots[:25]
                ],
            }
        )
    return {
        "schema": "n11_generic2095_row_profile_v1",
        "status": "DIAGNOSTIC_ONLY",
        "source_sha256": {
            "checker": _digest(Path(generic.__file__)),
            "geometry": _digest(Path(geometry.__file__)),
            "source": generic.SOURCE_PIN[0],
            "seed": generic.SEED_PIN[0],
        },
        "wall_seconds": time.monotonic() - started,
        "rows": findings,
        "profile_caveat": (
            "cProfile instrumentation inflates runtime; use receipts for unprofiled cost."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    inventory_command = sub.add_parser("inventory")
    inventory_command.add_argument("--manifest", type=Path, default=MANIFEST)
    inventory_command.add_argument("--baseline", type=Path, default=BASELINE)
    inventory_command.add_argument("--out", type=Path, required=True)
    profile_command = sub.add_parser("profile2095")
    profile_command.add_argument("--rows", type=int, nargs="+", default=[0, 22, 31])
    profile_command.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = (
        inventory(args.manifest, args.baseline)
        if args.command == "inventory"
        else profile_first_step_rows(args.rows)
    )
    atomic_write_text(args.out, json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: result[key] for key in ("status", "wall_seconds") if key in result}))


if __name__ == "__main__":
    main()
