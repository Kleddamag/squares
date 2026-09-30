"""Independently replay both closed center branches of pinned exclusion 1383.

The common ancestry is checked once. Each branch starts from its own copy of
that accepted state, and both contradictions must pass before singleton credit.
Publisher audit success flags and cached geometry never authorize acceptance.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import math
import resource
import sys
import time
from pathlib import Path
from types import ModuleType
from typing import Any

from strif import atomic_write_text

from devtools import check_n11_generic_sequential as generic
from devtools import n11_nonfield_center_orchestrator as orchestrator
from devtools import n11_nonfield_center_partition as partition

GENERIC_SHA = "280becc5393d9528ea36dca739fad1074e3c18e13e0722466e30c2fd16514ce1"
PARTITION_SHA = "43d2b8ec9c18911bbc26858f31db8429b2453b21a3a5a07c81daf7c5aa489e9b"
ORCHESTRATOR_SHA = "cfa62c5c4d3947bf6c9483b5cde9d194305d833d944e6ef467c52876d25fdf9a"
CASE = 1383


def require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def dependencies() -> dict[str, tuple[ModuleType, str]]:
    return {
        "generic": (generic, GENERIC_SHA),
        "orchestrator": (orchestrator, ORCHESTRATOR_SHA),
        "partition": (partition, PARTITION_SHA),
        "geometry": (generic.geometry, generic.frozen.GEOMETRY_SHA),
        "frozen_generic": (generic.frozen, generic.FROZEN_GENERIC_SHA),
        "fast_cover": (generic.fast_cover, generic.FAST_COVER_SHA),
        "indexed_cover": (generic.indexed_cover, generic.INDEXED_COVER_SHA),
        "degenerate_cover": (generic.degenerate_cover, generic.DEGENERATE_COVER_SHA),
        "a2_assignment": (generic.a2_assignment, generic.A2_HELPER_SHA),
        "partner": (generic.partner, generic.PARTNER_HELPER_SHA),
        "collision": (generic.collision_kernel, generic.COLLISION_KERNEL_SHA),
        "integer_collision": (generic.integer_collision, generic.INTEGER_COLLISION_SHA),
        "ancestry": (generic.ancestry, generic.ANCESTRY_HELPER_SHA),
        "refinement": (generic.refinement, generic.REFINEMENT_HELPER_SHA),
        "special_assignment": (generic.special_assignment, generic.SPECIAL_ASSIGNMENT_SHA),
    }


def admit_complete(result: dict[str, Any]) -> None:
    require(
        result.get("nodes_completed") == 8
        and result.get("branches_completed") == ["le", "ge"]
        and all(
            result.get(key) is None
            for key in ("current_node", "current_branch", "current_step", "current_row")
        )
        and result.get("pending_row_indices") == [],
        "center partition is incomplete",
    )


def run(args: argparse.Namespace) -> dict[str, Any]:
    require(not args.out.exists(), "use a new receipt path")
    started, cpu = time.monotonic(), time.process_time()
    children = resource.getrusage(resource.RUSAGE_CHILDREN)
    budget = generic.geometry.Budget(started + args.max_seconds, args.max_events)
    result: dict[str, Any] = {
        "status": "INCOMPLETE",
        "mask_index": CASE,
        "geometry_verified": False,
        "global_optimality_proved": False,
        "excluded_case_ids": [],
        "nodes_completed": 0,
        "branches_completed": [],
        "current_node": None,
        "current_branch": None,
        "current_step": None,
        "current_row": None,
        "pending_row_indices": [],
        "checked_row_indices_current_step": [],
        "source_sha256": {},
        "max_seconds": args.max_seconds,
        "max_events": args.max_events,
        "workers": args.workers,
        "cover_backend": "indexed",
        "collision_backend": "integer",
    }
    paths = {"checker": Path(__file__), "manifest": args.manifest}
    fingerprints: dict[str, str] = {}

    def bind(name: str, path: Path) -> None:
        require(args.out.resolve() != path.resolve(), "receipt overlaps input")
        paths[name] = path
        fingerprints[name] = generic.digest(path)
        result["source_sha256"][name] = fingerprints[name]

    try:
        require(
            math.isfinite(args.max_seconds)
            and 0 < args.max_seconds <= 7200
            and type(args.workers) is int
            and 1 <= args.workers <= 3
            and type(args.max_events) is int
            and args.max_events > 0,
            "invalid bounded replay parameters",
        )
        for name, path in list(paths.items()):
            bind(name, path)
        for name, (module, sha) in dependencies().items():
            require(module.__file__ is not None, "missing dependency source")
            bind(name, Path(module.__file__ or ""))
            require(fingerprints[name] == sha, f"changed reviewed dependency: {name}")
        require(generic.collision_kernel.dependencies_unchanged(), "collision dependencies")
        generic.geometry.admit_d4_receipt()
        manifest = generic.load_manifest(args.manifest)
        matches = [case for case in manifest["cases"] if case["mask_index"] == CASE]
        require(len(matches) == 1, "missing or duplicate partition recipe")
        recipe = matches[0]
        require(
            recipe["adapter"] == "closed_center_partition"
            and recipe["source_profile"] == "native_cached_v4_center_partition"
            and recipe["family"] == "A2"
            and len(recipe["ordered_ancestry_proposal"]) == 8,
            "unsupported center-partition recipe",
        )
        mask = tuple(recipe["mask"])

        def load(name: str, sha: str, directory: Path) -> dict[str, Any]:
            bind(name, directory / f"{sha}.gz")
            return generic.load_object(sha, manifest, directory)

        cover = load(
            "cover",
            generic.geometry.COVER_SHA,
            generic.PACKET / "receipts/d4-independent/objects",
        )
        require(cover["canonical_eleven_cell_subsets"][CASE] == list(mask), "canonical mask")
        baseline = load("baseline", manifest["input_sha256s"]["A1"], generic.METADATA_OBJECTS)
        load("assignment", manifest["input_sha256s"]["A2"], generic.METADATA_OBJECTS)
        generic.admit_assignment(CASE, recipe, manifest)
        tree = load("tree", recipe["source_sha256"], args.objects)
        require(
            tree == recipe["partition_proposal"]
            and tree["global_optimality_proved"] is False
            and tree["mask_exclusion_proved"] is False,
            "partition proposal or source scope differs",
        )
        seed = load("seed", recipe["seed_sha256"], args.objects)
        audit = load("audit", recipe["audit_sha256"], args.objects)
        generic.special_assignment.admit_special_audit(recipe, audit, baseline)
        nodes = recipe["ordered_ancestry_proposal"]
        require(len({node["source_sha256"] for node in nodes}) == 8, "duplicate source node")
        sources = {
            node["source_sha256"]: load(
                f"source_node_{index}", node["source_sha256"], args.objects
            )
            for index, node in enumerate(nodes)
        }
        # Refuse malformed branch plans before spending time on seed geometry.
        partition.admit_center_partition(recipe, tree, sources)
        result["admission_wall_seconds"] = time.monotonic() - started
        seed_started, seed_cpu = time.monotonic(), time.process_time()
        groups, rows, world, bins = generic.seed_state(seed, cover, CASE, mask, budget=budget)
        result.update(
            seed_wall_seconds=time.monotonic() - seed_started,
            seed_process_cpu_seconds=time.process_time() - seed_cpu,
            owned_seed_points_checked=sum(len(seed["groups"][str(owner)]) for owner in mask),
            seed_rows_checked=len(mask) * bins,
        )
        orchestrator.replay_center_partition(
            recipe,
            tree,
            sources,
            groups,
            rows,
            world=world,
            mask=mask,
            result=result,
            budget=budget,
            workers=args.workers,
            cover_backend="indexed",
            collision_backend="integer",
        )
        admit_complete(result)
        require(
            all(generic.digest(path) == fingerprints[name] for name, path in paths.items()),
            "source changed during center-partition replay",
        )
        require(generic.collision_kernel.dependencies_unchanged(), "collision source changed")
        generic.remaining(budget)
        result.update(
            status="PASS_CENTER_PARTITION_EXCLUSION",
            geometry_verified=True,
            excluded_case_ids=[CASE],
        )
    except (generic.geometry.IncompleteError, concurrent.futures.TimeoutError) as error:
        result["error"] = str(error)
    except (ValueError, KeyError, IndexError, TypeError, OSError, RuntimeError) as error:
        result.update(status="REFUSED", error=str(error))
    after = resource.getrusage(resource.RUSAGE_CHILDREN)
    result.update(
        wall_seconds=time.monotonic() - started,
        coordinator_process_cpu_seconds=time.process_time() - cpu,
        child_process_cpu_seconds=(
            after.ru_utime + after.ru_stime - children.ru_utime - children.ru_stime
        ),
    )
    atomic_write_text(args.out, json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=generic.MANIFEST)
    parser.add_argument("--objects", type=Path, required=True)
    parser.add_argument("--workers", type=int, choices=(1, 2, 3), default=1)
    parser.add_argument("--max-seconds", type=float, default=3600)
    parser.add_argument("--max-events", type=int, default=50_000)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    result = run(args)
    print(json.dumps({key: result.get(key) for key in ("status", "wall_seconds", "error")}))
    return 0 if result["status"] == "PASS_CENTER_PARTITION_EXCLUSION" else 2


if __name__ == "__main__":
    sys.exit(main())
