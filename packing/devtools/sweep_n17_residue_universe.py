"""Sweep of the n17 residue's arity-8-to-10 universe in float search (H-267). Not a certificate.

Lane F1's ranked plan, step 2 (cost-reduction review, sections 2.4, 2.6 and 3.1). The
residue is the states of the unique-state cover that survive every confirmed selector flag
(the selector's re-check receipt). Its *universe* at arity `k` is every connected class of
`k` cells that occurs in some residue state and lies in no D4 image of the endpoint's
state: a class in no residue state removes nothing whatever its verdict, and a class in an
endpoint image is placed by the endpoint's own pose, so both restrictions are exact for
the consumer. Every class is searched with the selector's `recheck_flag`, sub-pattern
witnesses first and then the class warm started from them, under a screen budget (12
starts, 24 hops, 48 and 48 deep attempts, the finish); a class the screen cannot place is
searched again under the selector's full budget, and is flagged only if that fails too.
Each verdict is the selector's, seeded by the run seed and the class's mask, so it does
not depend on the order or on the chunking.

Order. F1's locality-filtered queues come first: arity 8 at three to five missing pairs,
then arity 9 at most two, then arity 10 at most two; then the rest by arity and missing
pairs. Within a queue, classes go by residue coverage (the residue orbits holding an image
of the class), most first. Arity-8 classes with at most two missing pairs are not queued:
the arity-8 priority sweep searched them all and the residue holds only those it placed.

Resumable. `plan` writes the queue once (`plan.json`, with its digest in every chunk).
`sweep` searches it in chunks of a fixed size and writes each chunk's receipt atomically
when it completes; rerun with the same arguments after a restart and it skips every chunk
already written. `summary` reads the plan and the chunks: per queue, the classes searched,
placed and flagged and the hit rate; and the greedy cover of the residue's orbits by the
flags found so far, with the falsifier of F1's plan (a cover of less than half).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
from numpy.typing import NDArray

from devtools import select_n17_sub_patterns as selector

PLAN_SCHEMA = "n17-residue-universe-plan/v1"
CHUNK_SCHEMA = "n17-residue-universe-chunk/v1"
SUMMARY_SCHEMA = "n17-residue-universe-summary/v1"
STATUS = (
    "float search, not a certificate: a flag is a class the selector's search with the "
    "finish could not place; the prover must certify it before it excludes anything"
)
MODULE_SHA256 = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
SCREEN = selector.Budget(starts=12, hops=24, deep_starts=48, deep_hops=48)
FULL = selector.Budget()
ARITIES = (8, 9, 10)
PRIORITY_TESTED = (8, 2)  # the arity-8 priority sweep searched every class up to 2 missing
QUEUES: tuple[tuple[str, int, int, int | None], ...] = (
    ("arity 8, three to five missing pairs", 8, 3, 5),
    ("arity 9, at most two missing pairs", 9, 0, 2),
    ("arity 10, at most two missing pairs", 10, 0, 2),
    ("arity 8, six or more missing pairs", 8, 6, None),
    ("arity 9, three to five missing pairs", 9, 3, 5),
    ("arity 10, three to five missing pairs", 10, 3, 5),
    ("arity 9, six or more missing pairs", 9, 6, None),
    ("arity 10, six or more missing pairs", 10, 6, None),
)

States = NDArray[np.int64]


@dataclass(frozen=True)
class Residue:
    """The surviving states, their orbit index, and the endpoint's images."""

    alive: States
    orbit_of: NDArray[np.int64]
    orbits: int
    endpoint_images: tuple[int, ...]


def orbit_index(
    alive: States, group: tuple[tuple[int, ...], ...]
) -> tuple[NDArray[np.int64], int]:
    """Each state's orbit, numbered by its least image."""
    if not alive.size:
        return np.zeros(0, dtype=np.int64), 0
    least = np.min(np.stack([selector.apply_permutation(alive, p) for p in group]), axis=0)
    _, inverse = np.unique(least, return_inverse=True)
    return inverse.astype(np.int64), int(inverse.max()) + 1


def make_residue(
    geometry: selector.Geometry,
    flags: list[int],
    endpoint_state: int,
    *,
    size: int = selector.TARGET,
) -> Residue:
    states = selector.all_states(len(geometry.names), size)
    images = sorted({image for mask in flags for image in selector.orbit(mask, geometry.group)})
    alive = selector.survivors(states, images)
    orbit_of, orbits = orbit_index(alive, geometry.group)
    return Residue(
        alive, orbit_of, orbits, tuple(sorted(selector.orbit(endpoint_state, geometry.group)))
    )


def hit_orbits(
    residue: Residue, group: tuple[tuple[int, ...], ...], mask: int
) -> NDArray[np.int64]:
    """The residue orbits holding some image of the class."""
    hit = np.zeros(residue.alive.size, dtype=np.bool_)
    for image in selector.orbit(mask, group):
        hit |= (residue.alive & image) == image
    return np.unique(residue.orbit_of[hit])


def universe(
    geometry: selector.Geometry, residue: Residue, arities: Sequence[int]
) -> list[dict[str, Any]]:
    """Every connected class of the arities in some residue state and no endpoint image."""
    rows: list[dict[str, Any]] = []
    for arity in arities:
        classes = selector.pattern_classes(geometry, arity, None)
        free = [m for m in classes if not any(m & e == m for e in residue.endpoint_images)]
        rows.extend(
            {
                "mask": mask,
                "arity": arity,
                "missing": selector.missing_pairs(geometry, mask),
                "coverage": int(hit_orbits(residue, geometry.group, mask).size),
            }
            for mask in sorted(selector.occurring_classes(free, residue.alive))
        )
    return rows


def queue_of(row: dict[str, Any]) -> int | None:
    for index, (_, arity, low, high) in enumerate(QUEUES):
        if (
            row["arity"] == arity
            and low <= row["missing"]
            and (high is None or row["missing"] <= high)
        ):
            return index
    return None


def make_queue(rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """The queue in F1's order, and the classes left out of it."""
    queued: list[dict[str, Any]] = []
    left: list[dict[str, Any]] = []
    for row in rows:
        index = queue_of(row)
        if index is None:
            left.append(row)
        else:
            queued.append({**row, "queue": index})
    queued.sort(key=lambda r: (r["queue"], -r["coverage"], r["mask"]))
    return queued, left


def load_flags(path: Path, geometry: selector.Geometry) -> list[int]:
    """The flags still standing: a re-check receipt's `flagged`, or any selector receipt's."""
    document = json.loads(path.read_text(encoding="utf-8"))
    return sorted(
        {
            selector.canonical(selector.mask_of(flag["indices"]), geometry.group)
            for flag in document["flagged"]
        }
    )


def digest_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_atomic(path: Path, document: Any) -> None:
    temporary = path.with_suffix(path.suffix + ".partial")
    _ = temporary.write_text(
        json.dumps(document, indent=1, sort_keys=True) + "\n", encoding="utf-8"
    )
    _ = temporary.replace(path)


def plan(
    flags_path: Path, directory: Path, *, arities: Sequence[int] = ARITIES
) -> dict[str, Any]:
    """Compute and write the queue once; reuse it if it is already written."""
    target = directory / "plan.json"
    if target.exists():
        written = json.loads(target.read_text(encoding="utf-8"))
        if written["flags_source"]["sha256"] != digest_of(flags_path):
            raise ValueError(f"{target} was planned under other flags; use a new directory")
        return written
    clock = time.perf_counter()
    geometry = selector.cover_geometry()
    endpoint = selector.mask_of(selector.endpoint_pose()["cells"])
    flags = load_flags(flags_path, geometry)
    residue = make_residue(geometry, flags, endpoint)
    rows = universe(geometry, residue, arities)
    queued, left = make_queue(rows)
    by_arity: dict[str, Any] = {}
    for arity in arities:
        mine = [r for r in rows if r["arity"] == arity]
        counts = [r["missing"] for r in mine]
        coverages = sorted(r["coverage"] for r in mine)
        by_arity[str(arity)] = {
            "classes": len(mine),
            "by_missing_pairs": [counts.count(d) for d in range(max(counts, default=-1) + 1)],
            "coverage_max": coverages[-1] if coverages else 0,
            "coverage_median": coverages[len(coverages) // 2] if coverages else 0,
            "left_out": sum(1 for r in left if r["arity"] == arity),
        }
    document = {
        "schema": PLAN_SCHEMA,
        "status": STATUS,
        "design": selector.DEFAULT_DESIGN,
        "flags_source": {"path": str(flags_path), "sha256": digest_of(flags_path)},
        "flags": len(flags),
        "residue": {
            "states": int(residue.alive.size),
            "orbits": residue.orbits,
            "endpoint_survives": endpoint in set(residue.alive.tolist()),
        },
        "universe": by_arity,
        "left_out_rule": "arity 8 at most two missing pairs: the priority sweep searched them",
        "queues": [
            {"name": name, "classes": sum(1 for r in queued if r["queue"] == index)}
            for index, (name, _, _, _) in enumerate(QUEUES)
        ],
        "queue": [
            [r["mask"], r["arity"], r["missing"], r["coverage"], r["queue"]] for r in queued
        ],
        "module_sha256": MODULE_SHA256,
        "seconds": round(time.perf_counter() - clock, 3),
    }
    directory.mkdir(parents=True, exist_ok=True)
    write_atomic(target, document)
    return document


def search_class(
    geometry: selector.Geometry,
    mask: int,
    *,
    seed: int,
    screen: selector.Budget,
    full: selector.Budget,
) -> dict[str, Any]:
    """The screen, then the full budget for a class the screen cannot place."""
    clock = time.perf_counter()
    screened = selector.recheck_flag(geometry, mask, seed=seed, budget=screen)
    row: dict[str, Any] = {
        "screen": screened["status"],
        "screen_attempts": screened["attempts"],
    }
    final = screened
    if screened["status"] != "placed":
        final = selector.recheck_flag(geometry, mask, seed=seed, budget=full)
    row.update(
        status="placed" if final["status"] == "placed" else "flagged",
        best_penetration=final["best_penetration"],
        attempts=final["attempts"],
        found_by=final["found_by"],
        seconds=round(time.perf_counter() - clock, 3),
    )
    if row["status"] == "flagged":
        row.update(cells=final["cells"], pose=final["pose"], components=final["components"])
    return row


def sweep(
    directory: Path,
    *,
    chunk: int,
    seed: int = 1,
    limit_chunks: int | None = None,
    geometry: selector.Geometry | None = None,
    screen: selector.Budget = SCREEN,
    full: selector.Budget = FULL,
) -> list[int]:
    """Search the planned queue chunk by chunk, skipping chunks already written."""
    plan_path = directory / "plan.json"
    planned = json.loads(plan_path.read_text(encoding="utf-8"))
    plan_digest = digest_of(plan_path)
    geometry = geometry or selector.cover_geometry()
    queue = planned["queue"]
    written: list[int] = []
    chunks = (len(queue) + chunk - 1) // chunk
    for index in range(chunks):
        target = directory / f"chunk-{index:05d}.json"
        if target.exists():
            continue
        if limit_chunks is not None and len(written) >= limit_chunks:
            break
        clock = time.perf_counter()
        rows = []
        for mask, arity, missing, coverage, queue_index in queue[
            index * chunk : (index + 1) * chunk
        ]:
            found = search_class(geometry, mask, seed=seed, screen=screen, full=full)
            rows.append(
                {
                    "mask": mask,
                    "arity": arity,
                    "missing": missing,
                    "coverage": coverage,
                    "queue": queue_index,
                    **found,
                }
            )
        write_atomic(
            target,
            {
                "schema": CHUNK_SCHEMA,
                "status": STATUS,
                "plan_sha256": plan_digest,
                "chunk": index,
                "chunk_size": chunk,
                "seed": seed,
                "screen": budget_record(screen),
                "full": budget_record(full),
                "classes": rows,
                "module_sha256": MODULE_SHA256,
                "selector_sha256": selector.MODULE_SHA256,
                "seconds": round(time.perf_counter() - clock, 3),
            },
        )
        written.append(index)
        print(
            json.dumps(
                {
                    "chunk": index,
                    "of": chunks,
                    "flagged": sum(1 for r in rows if r["status"] == "flagged"),
                    "seconds": round(time.perf_counter() - clock, 1),
                }
            ),
            flush=True,
        )
    return written


def budget_record(budget: selector.Budget) -> dict[str, Any]:
    return {
        "starts": budget.starts,
        "hops": budget.hops,
        "deep_starts": budget.deep_starts,
        "deep_hops": budget.deep_hops,
        "margin": budget.margin,
        "finish": selector.FINISH if budget.finish else None,
    }


def greedy_cover(sets: dict[int, NDArray[np.int64]], orbits: int) -> list[dict[str, Any]]:
    """Flags in the order that removes the most residue orbits not yet removed."""
    left = np.ones(orbits, dtype=np.bool_)
    remaining = dict(sets)
    order: list[dict[str, Any]] = []
    while remaining:
        gains = {mask: int(np.count_nonzero(left[hit])) for mask, hit in remaining.items()}
        best = max(sorted(gains), key=lambda mask: gains[mask])
        if gains[best] == 0:
            break
        left[remaining.pop(best)] = False
        order.append({"mask": best, "removes": gains[best], "orbits_left": int(left.sum())})
    return order


def summary(directory: Path, flags_path: Path) -> dict[str, Any]:
    """Hit rates per queue and the greedy cover of the residue by the flags found so far."""
    planned = json.loads((directory / "plan.json").read_text(encoding="utf-8"))
    plan_digest = digest_of(directory / "plan.json")
    rows: list[dict[str, Any]] = []
    for path in sorted(directory.glob("chunk-*.json")):
        document = json.loads(path.read_text(encoding="utf-8"))
        if document["plan_sha256"] != plan_digest:
            raise ValueError(f"{path} was written for another plan")
        rows.extend(document["classes"])
    queues = []
    for index, (name, _, _, _) in enumerate(QUEUES):
        mine = [r for r in rows if r["queue"] == index]
        flagged = [r for r in mine if r["status"] == "flagged"]
        queues.append(
            {
                "name": name,
                "planned": planned["queues"][index]["classes"],
                "searched": len(mine),
                "flagged": len(flagged),
                "hit_rate": len(flagged) / len(mine) if mine else None,
                "screen_unplaced": sum(1 for r in mine if r["screen"] != "placed"),
                "search_seconds": round(sum(r["seconds"] for r in mine), 1),
                "coverage_range": [
                    min(r["coverage"] for r in mine),
                    max(r["coverage"] for r in mine),
                ]
                if mine
                else None,
            }
        )
    geometry = selector.cover_geometry()
    endpoint = selector.mask_of(selector.endpoint_pose()["cells"])
    residue = make_residue(geometry, load_flags(flags_path, geometry), endpoint)
    flags = [r for r in rows if r["status"] == "flagged"]
    sets = {r["mask"]: hit_orbits(residue, geometry.group, r["mask"]) for r in flags}
    order = greedy_cover(sets, residue.orbits)
    removed = residue.orbits - (order[-1]["orbits_left"] if order else residue.orbits)
    named = {r["mask"]: r for r in flags}
    return {
        "schema": SUMMARY_SCHEMA,
        "status": STATUS,
        "plan_sha256": plan_digest,
        "residue_orbits": residue.orbits,
        "searched": len(rows),
        "planned": len(planned["queue"]),
        "flagged": len(flags),
        "queues": queues,
        "greedy_cover": [
            {
                **step,
                "cells": named[step["mask"]]["cells"],
                "best_penetration": named[step["mask"]]["best_penetration"],
            }
            for step in order
        ],
        "cover_removes": removed,
        "cover_share": removed / residue.orbits if residue.orbits else None,
        "falsifier": "the flags' greedy cover removes less than half of the residue",
        "falsified_so_far": removed < residue.orbits / 2,
        "module_sha256": MODULE_SHA256,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument("command", choices=("plan", "sweep", "summary"))
    _ = parser.add_argument("--flags", type=Path, required=True, help="the re-check receipt")
    _ = parser.add_argument("--directory", type=Path, required=True, help="plan and chunks")
    _ = parser.add_argument("--chunk", type=int, default=500)
    _ = parser.add_argument("--seed", type=int, default=1)
    _ = parser.add_argument("--limit-chunks", type=int, default=None)
    _ = parser.add_argument("--output", type=Path, help="the summary's receipt")
    arguments = parser.parse_args(argv)
    planned = plan(arguments.flags, arguments.directory)
    if arguments.command == "plan":
        print(json.dumps({k: planned[k] for k in ("residue", "universe", "queues", "seconds")}))
        return 0
    if arguments.command == "sweep":
        _ = sweep(
            arguments.directory,
            chunk=arguments.chunk,
            seed=arguments.seed,
            limit_chunks=arguments.limit_chunks,
        )
        return 0
    record = summary(arguments.directory, arguments.flags)
    text = json.dumps(record, indent=1, sort_keys=True)
    if arguments.output is not None:
        write_atomic(arguments.output, record)
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
