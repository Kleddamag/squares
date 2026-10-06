"""Measure a frozen producer slice without changing its arithmetic or certificate.

Run baseline and candidate in separate processes. `--profile` is a separate diagnostic
run, never a wall-time comparison. The callback observes the producer frame only at
completed steps; it does not mutate rows or memo entries.
"""

from __future__ import annotations

import argparse
import cProfile
import inspect
import json
import os
import pstats
import time
from pathlib import Path
from typing import Any

from devtools.check_hull_kernel_mask0 import n17_unique_frame
from devtools.check_n17_subpattern import PATTERNS, canonical_bytes, save_certificate
from devtools.process_memory import peak_memory_bytes
from sqpack.hull_kernel import Budget, producer


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--profile", action="store_true")
    parser.add_argument("--fixture", choices=("A", "W7"), default="A")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    frame = n17_unique_frame()
    mask = sorted(frame.cell_names.index(cell) for cell in PATTERNS[args.fixture])
    bins, rounds = (16, 12) if args.fixture == "A" else (8, 6)
    node_id = "n17-W5-partner-memo-A" if args.fixture == "A" else "n17-W7-audit-fixture"
    trace: list[dict[str, Any]] = []

    def observe(event: dict[str, Any]) -> None:
        current = inspect.currentframe()
        assert current is not None
        assert current.f_back is not None
        local = current.f_back.f_locals
        memo = local["memo"]
        current_ids = {id(row) for rows in local["rows"].values() for row in rows}
        obsolete = [
            (row, prepared) for key, (row, prepared) in memo.items() if key not in current_ids
        ]
        sample = {
            **event,
            "memo_entries": len(memo),
            "obsolete_entries": len(obsolete),
            "domain_entries": sum(len(prepared.domain_max) for _, prepared in memo.values()),
            "obsolete_domain_entries": sum(
                len(prepared.domain_max) for _, prepared in obsolete
            ),
            "process_peak_working_set_bytes": peak_memory_bytes(),
        }
        trace.append(sample)
        print(json.dumps(sample), flush=True)
        # Do not retain the producer frame through an inspection reference cycle.
        del local, current

    profiler = cProfile.Profile()
    wall, cpu = time.perf_counter(), time.process_time()
    if args.profile:
        profiler.enable()
    production = producer.produce(
        frame,
        mask,
        bins=bins,
        max_rounds=rounds,
        budget=Budget(time.monotonic() + 240, 5_000_000),
        node_id=node_id,
        progress=observe,
        collision=True,
        core="envelope",
        hull_limit=16,
        split=None,
    )
    if args.profile:
        profiler.disable()
    producer_wall = time.perf_counter() - wall
    producer_cpu = time.process_time() - cpu
    producer_peak = peak_memory_bytes()
    wall, cpu = time.perf_counter(), time.process_time()
    save_certificate(args.output, production.seed, production.node)
    save_wall = time.perf_counter() - wall
    save_cpu = time.process_time() - cpu
    summary = {
        "fixture": args.fixture,
        "bins": bins,
        "max_rounds": rounds,
        "profiled": args.profile,
        "actual_python_pid": os.getpid(),
        "producer_wall_seconds": producer_wall,
        "producer_cpu_seconds": producer_cpu,
        "producer_peak_working_set_bytes": producer_peak,
        "save_wall_seconds": save_wall,
        "save_cpu_seconds": save_cpu,
        "pipeline_peak_working_set_bytes": peak_memory_bytes(),
        "seed_canonical_bytes": len(canonical_bytes(production.seed)),
        "node_canonical_bytes": len(canonical_bytes(production.node)),
        "steps": len(production.node["steps"]),
        "rows": sum(len(step["rows"]) for step in production.node["steps"]),
        "closed": production.node["closed"],
        "outcome": production.outcome,
        "rounds": production.rounds,
        "memo_trace": trace,
        "files": sorted(path.name for path in args.output.glob("*.json.gz")),
        "limits": "No standalone checker memory claim; no mathematical exclusion admitted.",
    }
    (args.output / "summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    if args.profile:
        with (args.output / "profile.txt").open("w", encoding="utf-8") as stream:
            pstats.Stats(profiler, stream=stream).strip_dirs().sort_stats(
                "cumulative"
            ).print_stats(45)
    print(
        json.dumps(
            {
                key: value
                for key, value in summary.items()
                if key not in {"rounds", "memo_trace"}
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
