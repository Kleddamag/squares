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
import gzip
import hashlib
import importlib
import json
import math
import sys
import time
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from devtools import check_hull_kernel_mask0 as mask0_tool
from devtools.provenance import provenance
from sqpack.hull_kernel import node, sequential
from sqpack.hull_kernel.frame import Frame
from sqpack.hull_kernel.geometry import Budget, IncompleteError, RefusalError

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
    # Second in the arity-7 certification priority (best penetration 6.3e-5).
    "NW7": (
        "side-N0",
        "side-N1",
        "side-W2",
        "interior-SW",
        "interior-NW",
        "interior-W",
        "interior-S",
    ),
    # The endpoint's own west-wall cells (its squares 1, 2, 3, 4, 9, 10 and 11): W7's
    # falsifier, which shares five of W7's seven cells.
    "endpoint7": (
        "corner-SW",
        "side-S0",
        "side-W0",
        "side-W2",
        "side-N0",
        "corner-NW",
        "interior-W",
    ),
}
CONTROLS = frozenset({"endpoint6", "endpoint7"})
PRODUCER = "sqpack.hull_kernel.producer"
MAX_EVENTS = 200_000


def canonical_bytes(value: Any) -> bytes:
    """The bytes an object is digested and saved as: sorted keys, no spaces, UTF-8."""
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def content_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def save_certificate(
    directory: Path, seed: dict[str, Any], node_object: dict[str, Any]
) -> None:
    """Write `seed-<sha256>.json.gz` and `node-<sha256>.json.gz` of the canonical bytes."""
    directory.mkdir(parents=True, exist_ok=True)
    for kind, value in (("seed", seed), ("node", node_object)):
        raw = canonical_bytes(value)
        target = directory / f"{kind}-{hashlib.sha256(raw).hexdigest()}.json.gz"
        target.write_bytes(gzip.compress(raw, mtime=0))


def load_certificate(directory: Path) -> tuple[dict[str, Any], dict[str, Any], str, str]:
    """The saved seed and node, and their content ids (`content_sha256`).

    `save_certificate` names each file by its content id; the name is a name, and a file
    is read whatever it is called and however its JSON is spaced. The node names its seed
    by the seed's content id, which the replay's header admission checks.
    """
    loaded: list[dict[str, Any]] = []
    for kind in ("seed", "node"):
        found = sorted(directory.glob(f"{kind}-*.json.gz"))
        if len(found) != 1:
            raise RefusalError(f"expected exactly one saved {kind} in {directory}")
        loaded.append(json.loads(gzip.decompress(found[0].read_bytes())))
    seed, node_object = loaded
    return seed, node_object, content_sha256(seed), content_sha256(node_object)


def checker_modules() -> dict[str, str]:
    """SHA-256 of every `sqpack.hull_kernel` module this process has imported."""
    digests: dict[str, str] = {}
    for name, module in sorted(sys.modules.items()):
        location = getattr(module, "__file__", None)
        if name.startswith("sqpack.hull_kernel") and location:
            digests[name] = hashlib.sha256(Path(location).read_bytes()).hexdigest()
    return digests


def check_saved(
    directory: Path,
    frame: Frame | None = None,
    *,
    max_seconds: float = 3600.0,
    require_no_producer: bool = True,
    cover: str = "indexed",
) -> dict[str, Any]:
    """Certify saved objects with the checker alone: seed admission, the sequential
    replay and the transfer. The producer is never imported; with `require_no_producer`
    its absence from `sys.modules` is asserted before and after the check. `cover` names
    the row-cover sweep (`sequential.COVERS`); the indexed and reference forms prove the
    same cover and report the same events and probes."""
    if require_no_producer and PRODUCER in sys.modules:
        raise RefusalError("the producer is loaded; a saved check must run without it")
    started = time.monotonic()
    seed, node_object, seed_sha, node_sha = load_certificate(directory)
    frame = frame if frame is not None else mask0_tool.n17_unique_frame()
    mask = node_object["mask"]
    bins = seed["bins"]
    budget = Budget(started + max_seconds, MAX_EVENTS)
    seed_state = node.admit_seed(
        frame, seed, mask=mask, bins=bins, budget=budget, allow_empty_groups=True
    )
    trace = sequential.replay_sequential(
        frame,
        node_object,
        seed_state,
        mask=mask,
        seed_sha256=seed_sha,
        budget=budget,
        cover=cover,
    )
    if require_no_producer and PRODUCER in sys.modules:
        raise RefusalError("the producer was imported during a saved check")
    closed = trace.closure is not None
    result: dict[str, Any] = {
        "status": "PASS_SAVED_CLOSED" if closed else "PASS_SAVED_STALL",
        "frame": frame.name,
        "cells": [frame.cell_names[owner] for owner in mask],
        "mask": mask,
        "bins": bins,
        "cover_backend": cover,
        "seed_sha256": seed_sha,
        "node_sha256": node_sha,
        "closure": trace.closure,
        "steps_checked": len(trace.steps),
        "rows_checked": sum(step["rows"] for step in trace.steps),
        "events": sum(step["events"] for step in trace.steps),
        "collision_regions": sum(step.get("collision_regions", 0) for step in trace.steps),
        "producer_imported": PRODUCER in sys.modules,
        "checker_modules_sha256": checker_modules(),
        "check_seconds": time.monotonic() - started,
    }
    excluded = frame.states_containing(mask) if closed else []
    result["excluded_orbits"] = len(excluded)
    result["excluded_states"] = sum(
        orbit_size(frame, frame.representatives[index]) for index in excluded
    )
    return result


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
    collision: bool = True,
    hull_limit: int | None = 16,
    producer_share: float = 0.5,
    save_objects: Path | None = None,
    core: str = "envelope",
    split: dict[str, int] | None = None,
) -> dict[str, Any]:
    """Produce, save if asked, then certify with the checker. `split` (keys `floor`,
    `max_rows`, `patience`) turns on the producer's adaptive rows; without it the rows
    stay the seed's uniform bins and nothing in the output changes."""
    producer = importlib.import_module(PRODUCER)
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
        collision=collision,
        hull_limit=hull_limit,
        stop_at=started + max_seconds * producer_share,
        core=core,
        split=None if split is None else producer.SplitPolicy(**split),
        progress=lambda event: print(
            json.dumps({**event, "seconds": round(time.monotonic() - started, 1)}),
            file=sys.stderr,
            flush=True,
        ),
    )
    produced = time.monotonic()
    if save_objects is not None:
        # Saved before checking, so a check the ceiling cuts short can be finished later
        # with --check-saved; saved objects claim nothing until a check passes on them.
        save_certificate(save_objects, production.seed, production.node)
    seed = node.admit_seed(
        frame, production.seed, mask=mask, bins=bins, budget=budget, allow_empty_groups=True
    )
    trace = sequential.replay_sequential(
        frame,
        production.node,
        seed,
        mask=mask,
        seed_sha256=content_sha256(production.seed),
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
        "collision_regions": collision,
        "hull_limit": hull_limit,
        "producer_share": producer_share,
        "core": core,
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
            | (
                {}
                if split is None
                else {
                    "rows": {e["cell"]: e["rows"] for e in entry["extents"]},
                    "splits": entry.get("splits"),
                    "planned_rows": entry.get("planned_rows"),
                }
            )
            for entry in production.rounds
        ],
        "final_extents": trace.extents,
        "node_sha256": content_sha256(production.node),
        "seed_sha256": content_sha256(production.seed),
        "producer_seconds": produced - started,
        "checker_seconds": checked - produced,
    }
    if split is not None:
        result["split"] = dict(split)
        result["finest_row"] = str(
            min(
                Q(row["interval"][1]) - Q(row["interval"][0])
                for step in production.node["steps"]
                for row in step["rows"]
            )
        )
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
        result["control"] = "an endpoint sub-pattern must stall"
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
    parser.add_argument("--no-collision", action="store_true", help="no partner collisions")
    parser.add_argument("--hull-limit", type=int, default=16, help="0 keeps every vertex")
    parser.add_argument(
        "--save-objects", type=Path, help="write the certified seed and node here, gzipped"
    )
    parser.add_argument(
        "--producer-share",
        type=float,
        default=0.5,
        help="the share of the wall ceiling after which the producer starts no new step",
    )
    parser.add_argument(
        "--core",
        choices=("envelope", "octagon"),
        default="envelope",
        help="the producer's strict core: the midpoint envelope square or the end octagon",
    )
    parser.add_argument(
        "--split-floor",
        type=int,
        default=0,
        help="adaptive rows: bisect stuck rows down to 1/N in t (0, the default, is off)",
    )
    parser.add_argument(
        "--max-rows", type=int, default=0, help="with --split-floor: rows over all owners"
    )
    parser.add_argument(
        "--split-patience",
        type=int,
        default=1,
        help="with --split-floor: rounds a row must stay unshrunk before it is split",
    )
    parser.add_argument(
        "--check-saved",
        type=Path,
        help="certify a saved seed and node with the checker alone; nothing is produced",
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    if not math.isfinite(args.max_seconds) or args.max_seconds <= 0:
        parser.error("the wall ceiling must be positive and finite")
    if args.bins <= 0 or args.max_rounds <= 0:
        parser.error("bins and rounds must be positive")
    if not 0 < args.producer_share < 1:
        parser.error("the producer share must lie in (0, 1)")
    if args.split_floor < 0 or (
        args.split_floor and (args.max_rows <= 0 or args.split_patience <= 0)
    ):
        parser.error("--split-floor needs a positive --max-rows and --split-patience")
    name = "custom" if args.cells else args.pattern
    cells = tuple(args.cells) if args.cells else PATTERNS[args.pattern]
    start, cpu = time.monotonic(), time.process_time()
    if args.check_saved is not None:
        try:
            result = check_saved(
                args.check_saved, max_seconds=args.max_seconds, cover=args.cover
            )
        except IncompleteError as error:
            result = {"status": "INCOMPLETE", "reason": str(error), "excluded_orbits": 0}
        except (ValueError, KeyError, IndexError, TypeError, OSError) as error:
            result = {"status": "REFUSED", "reason": str(error), "excluded_orbits": 0}
        result.update(
            provenance=provenance(Path(__file__)),
            wall_seconds=time.monotonic() - start,
            process_cpu_seconds=time.process_time() - cpu,
        )
        encoded = json.dumps(result, indent=2, sort_keys=True, default=str) + "\n"
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(encoded, encoding="utf-8")
        print(encoded, end="")
        return 0 if str(result["status"]).startswith("PASS") else 2
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
            collision=not args.no_collision,
            hull_limit=args.hull_limit or None,
            producer_share=args.producer_share,
            save_objects=args.save_objects,
            core=args.core,
            split=(
                {
                    "floor": args.split_floor,
                    "max_rows": args.max_rows,
                    "patience": args.split_patience,
                }
                if args.split_floor
                else None
            ),
        )
    except IncompleteError as error:
        result = {"status": "INCOMPLETE", "reason": str(error), "excluded_orbits": 0}
    except (ValueError, KeyError, IndexError, TypeError, OSError) as error:
        result = {"status": "REFUSED", "reason": str(error), "excluded_orbits": 0}
    result.update(
        provenance=provenance(Path(__file__), *sorted(Path(node.__file__).parent.glob("*.py"))),
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
