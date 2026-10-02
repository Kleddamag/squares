"""Run the simple mode-A producer on one n17 sub-pattern, then certify it (H-267, BC-418).

The frame is the H-266 unique-state cover at cap 1169/250 with D4 and no capture cap
(`check_hull_kernel_mask0.n17_unique_frame`). A pattern is a set of cells named by the
cover; its claim, if it closes, is that no packing at that cap has distinct squares with
centres in those closed cells, one per cell, whatever the other squares do.

`sqpack.hull_kernel.producer` proposes a seed and a node; nothing it says counts. The
certificate is `node.admit_seed` (every owned point proved, every wall row the full
legal domain) followed by `sequential.replay_sequential` on exactly the produced
objects, which derives closure itself. A certified closure excludes, by containment and
D4, every orbit representative that `Frame.states_containing` lists; a stall excludes
nothing and is reported with every owner's residual extents per round.

The selector lane's flagged arity-6 classes are `A`, `B` and `C`, in its priority order;
`W7` heads its arity-7 certification priority (corner-SW, the west wall, side-N0 and the
two west interior cells).
`endpoint6` is the positive control: six cells of the H256 endpoint's own state, which
the endpoint realises at a side below the cap, so a closure there is a soundness failure
and the run refuses.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
import time
from pathlib import Path
from typing import Any

from devtools import check_hull_kernel_mask0 as mask0_tool
from sqpack.hull_kernel import node, producer, sequential
from sqpack.hull_kernel.frame import Frame
from sqpack.hull_kernel.geometry import Budget, IncompleteError

PATTERNS = {
    "A": (
        "interior-SW",
        "interior-NW",
        "interior-W",
        "interior-S",
        "interior-N",
        "interior-SE",
    ),
    "B": ("side-S1", "side-W1", "interior-NW", "interior-W", "interior-S", "interior-SE"),
    "C": ("interior-NW", "interior-W", "interior-S", "interior-N", "interior-E", "interior-SE"),
    "W7": (
        "corner-SW",
        "side-N0",
        "side-W0",
        "side-W1",
        "side-W2",
        "interior-SW",
        "interior-W",
    ),
    "endpoint6": ("corner-SW", "side-S0", "side-W0", "side-W2", "corner-NW", "interior-W"),
}
CONTROLS = frozenset({"endpoint6"})
MAX_EVENTS = 200_000


def orbit_size(frame: Frame, state: tuple[int, ...]) -> int:
    return len({frame.image(action, state) for action in frame.actions})


def run(
    frame: Frame,
    cells: tuple[str, ...],
    *,
    name: str,
    bins: int,
    max_rounds: int,
    max_seconds: float,
    cover: str,
) -> dict[str, Any]:
    started = time.monotonic()
    mask = sorted(frame.cell_names.index(cell) for cell in cells)
    budget = Budget(started + max_seconds, MAX_EVENTS)
    production = producer.produce(
        frame,
        mask,
        bins=bins,
        max_rounds=max_rounds,
        budget=budget,
        node_id=f"n17-{name}",
        progress=lambda event: print(
            json.dumps({**event, "seconds": round(time.monotonic() - started, 1)}),
            file=sys.stderr,
            flush=True,
        ),
    )
    produced = time.monotonic()
    seed = node.admit_seed(
        frame, production.seed, mask=mask, bins=bins, budget=budget, allow_empty_groups=True
    )
    trace = sequential.replay_sequential(
        frame,
        production.node,
        seed,
        mask=mask,
        seed_sha256=producer.content_sha256(production.seed),
        budget=budget,
        cover=cover,
    )
    checked = time.monotonic()
    closed = trace.closure is not None
    result: dict[str, Any] = {
        "pattern": name,
        "cells": list(cells),
        "mask": mask,
        "bins": bins,
        "max_rounds": max_rounds,
        "cover_backend": cover,
        "producer_outcome": production.outcome,
        "certified": "closed" if closed else "stalled",
        "closure": trace.closure,
        "seed_points": {
            frame.cell_names[owner]: len(production.seed["groups"][str(owner)])
            for owner in mask
        },
        "steps_checked": len(trace.steps),
        "rows_checked": sum(step["rows"] for step in trace.steps),
        "events": sum(step["events"] for step in trace.steps),
        "probes": sum(step["probes"] for step in trace.steps),
        "steps": trace.steps,
        "rounds": [
            {
                "round": entry["round"],
                "steps": entry["steps"],
                "live_rows": {e["cell"]: e["live_rows"] for e in entry["extents"]},
                "residual_box_extent": {
                    e["cell"]: e["residual_box_extent"] for e in entry["extents"]
                },
                "owned_hull_vertices": {
                    e["cell"]: e["owned_hull_vertices"] for e in entry["extents"]
                },
            }
            for entry in production.rounds
        ],
        "final_extents": trace.extents,
        "node_sha256": producer.content_sha256(production.node),
        "seed_sha256": producer.content_sha256(production.seed),
        "producer_seconds": produced - started,
        "checker_seconds": checked - produced,
    }
    if closed:
        excluded = frame.states_containing(mask)
        result["excluded_orbits"] = len(excluded)
        result["excluded_states"] = sum(
            orbit_size(frame, frame.representatives[index]) for index in excluded
        )
    else:
        result["excluded_orbits"] = 0
        result["excluded_states"] = 0
    if name in CONTROLS:
        result["control"] = "endpoint sub-pattern must stall"
        result["status"] = "REFUSED_CONTROL_CLOSED" if closed else "PASS_CONTROL_STALLED"
    else:
        result["status"] = "PASS_CERTIFIED_CLOSED" if closed else "PASS_CERTIFIED_STALL"
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pattern", choices=sorted(PATTERNS), default="A")
    parser.add_argument("--cells", nargs="+", help="cell names, in place of --pattern")
    parser.add_argument("--bins", type=int, default=64)
    parser.add_argument("--max-rounds", type=int, default=6)
    parser.add_argument("--cover", choices=sorted(sequential.COVERS), default="indexed")
    parser.add_argument("--max-seconds", type=float, default=1800.0)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    if not math.isfinite(args.max_seconds) or args.max_seconds <= 0:
        parser.error("the wall ceiling must be positive and finite")
    if args.bins <= 0 or args.max_rounds <= 0:
        parser.error("bins and rounds must be positive")
    name = "custom" if args.cells else args.pattern
    cells = tuple(args.cells) if args.cells else PATTERNS[args.pattern]
    start, cpu = time.monotonic(), time.process_time()
    try:
        frame = mask0_tool.n17_unique_frame()
        result = run(
            frame,
            cells,
            name=name,
            bins=args.bins,
            max_rounds=args.max_rounds,
            max_seconds=args.max_seconds,
            cover=args.cover,
        )
    except IncompleteError as error:
        result = {"status": "INCOMPLETE", "reason": str(error), "excluded_orbits": 0}
    except (ValueError, KeyError, IndexError, TypeError, OSError) as error:
        result = {"status": "REFUSED", "reason": str(error), "excluded_orbits": 0}
    result.update(
        kernel_sha256=mask0_tool.kernel_digests(),
        tool_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        wall_seconds=time.monotonic() - start,
        process_cpu_seconds=time.process_time() - cpu,
        wall_ceiling_seconds=args.max_seconds,
    )
    encoded = json.dumps(result, indent=2, sort_keys=True, default=str) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    summary = {
        key: result.get(key)
        for key in (
            "status",
            "pattern",
            "certified",
            "producer_outcome",
            "closure",
            "excluded_orbits",
            "excluded_states",
            "steps_checked",
            "rows_checked",
            "rounds",
            "reason",
            "wall_seconds",
        )
    }
    print(json.dumps(summary, indent=1, sort_keys=True, default=str))
    return 0 if str(result["status"]).startswith("PASS") else 2


if __name__ == "__main__":
    sys.exit(main())
