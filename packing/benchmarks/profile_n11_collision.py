"""Measure the frozen capture collision kernel on pinned first-step proposals.

This diagnostic grants no proof credit. It separates source loading, ordinary
kernel CPU and profiler overhead before selecting a native implementation.
"""

from __future__ import annotations

import argparse
import cProfile
import hashlib
import json
import pstats
import time
from pathlib import Path
from typing import Any

from strif import atomic_write_text

from devtools import check_n11_capture_transition_pilot as collision
from devtools import check_n11_optimality_field_mask0 as geometry


def run(source: Path, indices: list[int]) -> dict[str, Any]:
    started = time.monotonic()
    kernel = Path(collision.__file__)
    before = hashlib.sha256(kernel.read_bytes()).hexdigest()
    collision.require(
        before == "22c5b4d1f23d48bcc4333bd279df41ba022c337109d063073771349b2854b309"
        and collision.dependencies_unchanged(),
        "reviewed collision dependencies changed",
    )
    collision.require(
        collision.pilot.digest(source) == collision.bridge.ROOT_SOURCE_SHA,
        "root source changed",
    )
    step = collision.extract(source, ".steps[0]")
    loading = time.monotonic() - started
    results = []
    for index in indices:
        collision.require(0 <= index < len(step["rows"]), "row index outside step")
        row = step["rows"][index]
        query = collision.pilot.convex(row["core_vertices"])
        domain = collision.pilot.points(row["input_domain"])
        for proposed in row["collision_regions"]:
            owner = proposed["partner"]
            partner = [
                (collision.pilot.points(item["domain"]), collision.pilot.convex(item["core"]))
                for item in step["prior_partner_pose_covers"][str(owner)]
                if item["domain"]
            ]
            region = collision.pilot.convex(proposed["vertices"])

            def execute(
                query: collision.Polygon,
                domain: collision.Polygon,
                partner: list[tuple[collision.Polygon, collision.Polygon]],
                region: collision.Polygon,
            ) -> int:
                return collision.universal_collision(
                    query,
                    domain,
                    partner,
                    region,
                    budget=geometry.Budget(time.monotonic() + 60, 20_000),
                )

            wall = time.monotonic()
            cpu = time.process_time()
            count = execute(query, domain, partner, region)
            kernel_cpu = time.process_time() - cpu
            kernel_wall = time.monotonic() - wall
            profile = cProfile.Profile()
            cpu = time.process_time()
            profile.enable()
            repeated = execute(query, domain, partner, region)
            profile.disable()
            profiled_cpu = time.process_time() - cpu
            collision.require(repeated == count, "profiled operation count differs")
            statistics: dict[tuple[str, int, str], Any] = vars(pstats.Stats(profile))["stats"]
            hottest = sorted(statistics.items(), key=lambda pair: pair[1][2], reverse=True)[:15]
            results.append(
                {
                    "row": index,
                    "partner": owner,
                    "facet_vertex_checks": count,
                    "live_partner_rows": len(partner),
                    "kernel_cpu_seconds": kernel_cpu,
                    "kernel_wall_seconds": kernel_wall,
                    "profiled_cpu_seconds": profiled_cpu,
                    "hottest_self_cpu": [
                        {
                            "file": Path(key[0]).name,
                            "line": key[1],
                            "function": key[2],
                            "calls": value[1],
                            "self_cpu_seconds": value[2],
                            "cumulative_cpu_seconds": value[3],
                        }
                        for key, value in hottest
                    ],
                }
            )
    collision.require(results, "selection contains no collision regions")
    collision.require(
        hashlib.sha256(kernel.read_bytes()).hexdigest() == before,
        "kernel changed during profile",
    )
    collision.require(collision.dependencies_unchanged(), "dependencies changed during profile")
    return {
        "schema": "n11_capture_collision_profile_v1",
        "proof_credit": False,
        "kernel_sha256": before,
        "source_sha256": collision.bridge.ROOT_SOURCE_SHA,
        "input_loading_wall_seconds": loading,
        "wall_seconds": time.monotonic() - started,
        "profile_caveat": "Instrumentation inflates runtime; compare unprofiled kernel CPU.",
        "rows": results,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root-source", type=Path, required=True)
    parser.add_argument("--rows", type=int, nargs="+", default=[0, 100, 200])
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    report = run(args.root_source, args.rows)
    atomic_write_text(args.out, json.dumps(report, indent=2) + "\n")
    print(json.dumps({"rows": len(report["rows"]), "wall_seconds": report["wall_seconds"]}))


if __name__ == "__main__":
    main()
