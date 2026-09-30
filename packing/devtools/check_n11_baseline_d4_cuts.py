"""Check the finite D4 support obligations for cases 2175 and 2176.

The exact 1931-case baseline is an explicit execution premise. Without a
complete bound execution inventory this runs diagnostically and grants no
necessary-cut credit. It never replays a source node or excludes a case.
Geometric consumers must compare their actual source constraints with the
explicit manifest-bound cuts returned here before using this conditional lemma.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
import time
from dataclasses import dataclass
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from strif import atomic_write_text

from devtools import check_n11_optimality_d4 as d4
from devtools import check_n11_optimality_field_mask0 as geometry

PACKET = geometry.PACKET
REPO = Path(__file__).resolve().parents[2]
B = Q(191, 50) / d4.U
MANIFEST_GZIP_SHA = "a730804aef482e9f32d4b579608a52727b55fa2df8fa4327dfbeae82c0184520"
MANIFEST_SHA = "b2b80cb792e12a41860b4f82b51f93ca08e2e89b3c3718b632e982a2a8fb588b"
BASELINE_METADATA_SHA = "04fa1ebb37f5dace29946224fe8c7c5d8a1bedb4fa860c65b359f4200415de57"
BASELINE_SNAPSHOT_SHA = "bc3563a0c9955a561f99cbefe7278e027feff085ff6d97bc338e347f97514545"
FIELD_INVENTORY_SHA = "768b7110548ce9200d1a8887e417985d79109e5987ff8e0b2b7dd998976d260e"
DEPENDENCIES = {
    "d4": (d4, "19f4b0a47afd6acb327e85bd4a98ca2a43d2fdaa49aeb0edd30aa12d1b6aac1d"),
    "geometry": (geometry, "75fc0238f2ac91af9dc9cf57bd00792343dcf3321c395adddebf0f3465113ce5"),
}


@dataclass(frozen=True)
class Cut:
    owner: int
    normal: tuple[Q, Q]
    upper: Q


@dataclass
class SearchBudget:
    deadline: float
    max_nodes: int
    nodes: int = 0

    def check(self) -> None:
        if time.monotonic() >= self.deadline:
            raise geometry.IncompleteError("D4 support wall ceiling")

    def tick(self) -> None:
        self.check()
        if self.nodes >= self.max_nodes:
            raise geometry.IncompleteError("D4 support search node ceiling")
        self.nodes += 1


def checked_ids(values: Any, count: int, label: str) -> set[int]:
    d4.require(
        isinstance(values, list)
        and len(values) == count
        and all(type(value) is int and 0 <= value < 2184 for value in values)
        and len(set(values)) == count,
        label,
    )
    return set(values)


def baseline_context(
    metadata: dict[str, Any],
) -> tuple[set[int], list[tuple[int, ...]], list[tuple[int, ...]]]:
    """Bind the exact baseline complement, preserving both raw orientations."""
    excluded = checked_ids(metadata["excluded_canonical_mask_indices"], 1931, "baseline IDs")
    remaining = checked_ids(
        metadata["remaining_canonical_mask_indices"], 253, "baseline complement"
    )
    d4.require(
        remaining == set(range(2184)) - excluded
        and not {2175, 2176} & excluded
        and metadata["authoritative_snapshot_sha256"] == BASELINE_SNAPSHOT_SHA
        and metadata["cover_sha256"] == d4.INPUT_HASHES["cover"]
        and Q(metadata["parent_Uplus"]) == d4.U
        and Q(metadata["parent_side"]) == B,
        "baseline complement or geometry identity",
    )
    _, canonical = d4.canonical_masks()
    allowed = sorted(
        {canonical[index] for index in remaining}
        | {d4.half_turn(canonical[index]) for index in remaining}
    )
    d4.require(len(allowed) == 506, "baseline raw-mask inventory")
    return excluded, canonical, allowed


def execution_missing(record: dict[str, Any], baseline: set[int]) -> list[int]:
    """Check an execution-inventory premise, without claiming to rerun its geometry."""
    d4.require(
        record["status"] == "EXECUTION_RECORD_INVENTORY"
        and record["source_revision"] == geometry.SOURCE_REVISION
        and record["global_optimality_proved"] is False
        and record["geometry_rerun"] is False
        and record["nonfield_manifest_sha256"] == MANIFEST_GZIP_SHA
        and record["field_inventory_sha256"] == FIELD_INVENTORY_SHA
        and record["required_case_count"] == 2180,
        "execution inventory scope",
    )
    accepted = checked_ids(
        record["accepted_case_ids"], record["accepted_case_count"], "accepted IDs"
    )
    pending = checked_ids(
        record["remaining_case_ids"], record["remaining_case_count"], "pending IDs"
    )
    d4.require(
        not accepted & pending and accepted | pending == set(range(2184)) - set(d4.SURVIVORS),
        "execution inventory partition",
    )
    return sorted(baseline - accepted)


class ForcedRegionSearch:
    """Exhaust the finite overapproximation with one source-owner region fixed."""

    def __init__(
        self,
        labels: list[tuple[int, ...]],
        banned: set[tuple[int, int]],
        allowed: list[tuple[int, ...]],
        budget: SearchBudget,
    ) -> None:
        d4.require(bool(allowed) and len(set(allowed)) == len(allowed), "allowed masks")
        width = len(allowed[0])
        d4.require(
            width > 0
            and all(len(mask) == width and tuple(sorted(set(mask))) == mask for mask in allowed)
            and all(0 <= cell < 16 for mask in allowed for cell in mask)
            and all(len(row) == 4 and all(0 <= cell < 16 for cell in row) for row in labels),
            "finite search mask or label grammar",
        )
        self.labels, self.budget, self.width = labels, budget, width
        self.allowed = set(allowed)
        self.all_targets = (1 << len(allowed)) - 1
        self.contains = [
            sum(1 << index for index, mask in enumerate(allowed) if cell in mask)
            for cell in range(16)
        ]
        self.initial = [
            sum(1 << index for index, row in enumerate(labels) if row[0] == owner)
            for owner in range(16)
        ]
        self.compatible = [
            sum(
                1 << other
                for other, candidate in enumerate(labels)
                if all(a != b for a, b in zip(row, candidate, strict=True))
                and tuple(sorted((index, other))) not in banned
            )
            for index, row in enumerate(labels)
        ]

    def solve(self, mask: tuple[int, ...], forced: int) -> tuple[list[int] | None, int]:
        d4.require(
            mask in self.allowed
            and len(mask) == self.width
            and 0 <= forced < len(self.labels)
            and self.labels[forced][0] in mask,
            "forced source assignment",
        )
        before = self.budget.nodes
        domains = {
            owner: (1 << forced if owner == self.labels[forced][0] else self.initial[owner])
            for owner in mask
        }

        def search(domains: dict[int, int], targets: tuple[int, ...]) -> list[int] | None:
            self.budget.tick()
            if not domains:
                return []
            possible = {}
            for owner, options in domains.items():
                possible[owner] = sum(
                    1 << region
                    for region in d4.members(options)
                    if all(
                        targets[view] & self.contains[self.labels[region][view]]
                        for view in range(4)
                    )
                )
                if not possible[owner]:
                    return None
            owner = min(possible, key=lambda item: (possible[item].bit_count(), item))
            for region in d4.members(possible[owner]):
                next_domains = {
                    other: options & self.compatible[region]
                    for other, options in possible.items()
                    if other != owner
                }
                if any(not options for options in next_domains.values()):
                    continue
                next_targets = tuple(
                    targets[view] & self.contains[self.labels[region][view]]
                    for view in range(4)
                )
                found = search(next_domains, next_targets)
                if found is not None:
                    return [region, *found]
            return None

        witness = search(domains, (self.all_targets,) * 4)
        return witness, self.budget.nodes - before


def offending_regions(
    labels: list[tuple[int, ...]],
    vertices: list[d4.Polygon],
    mask: tuple[int, ...],
    cuts: list[Cut],
) -> list[int]:
    """Only strict violation triggers rejection; closed equality remains allowed."""
    planes: dict[int, list[tuple[Q, Q, Q]]] = {owner: [] for owner in mask}
    for cut in cuts:
        nx, ny = cut.normal
        d4.require(cut.owner in planes and (nx, ny) != (0, 0), "cut owner or normal")
        normalized_upper = (cut.upper / B - (nx + ny) / 2) / (d4.U - 1)
        planes[cut.owner].append((nx, ny, normalized_upper))
    return [
        index
        for index, (row, poly) in enumerate(zip(labels, vertices, strict=True))
        if any(
            nx * x + ny * y > upper for nx, ny, upper in planes.get(row[0], []) for x, y in poly
        )
    ]


def read_bound(path: Path, expected: str, bindings: dict[Path, str]) -> dict[str, Any]:
    packed = path.read_bytes()
    raw = gzip.decompress(packed) if path.suffix == ".gz" else packed
    d4.require(hashlib.sha256(raw).hexdigest() == expected, f"source identity: {path}")
    bindings[path] = hashlib.sha256(packed).hexdigest()
    return geometry.strict_json(raw)


def dependencies_unchanged() -> bool:
    return all(
        module.__file__ is not None and d4.sha256(Path(module.__file__)) == expected
        for module, expected in DEPENDENCIES.values()
    )


def run(args: argparse.Namespace) -> dict[str, Any]:
    started, cpu_started = time.monotonic(), time.process_time()
    budget = SearchBudget(started + args.max_seconds, args.max_nodes)
    bindings: dict[Path, str] = {}
    result: dict[str, Any] = {
        "schema": "n11_baseline_d4_cut_obligations_v1",
        "status": "INCOMPLETE",
        "checker_sha256": d4.sha256(Path(__file__)),
        "source_revision": geometry.SOURCE_REVISION,
        "finite_obligations_complete": False,
        "baseline_execution_premise_admitted": False,
        "necessary_cuts_verified": False,
        "source_constraints_match_verified": False,
        "proof_credit": False,
        "excluded_case_ids": [],
        "global_optimality_proved": False,
        "baseline_geometry_rerun": False,
        "cases": [],
        "max_seconds": args.max_seconds,
        "max_nodes": args.max_nodes,
        "scope": (
            "Manifest-listed cuts only; consumers must bind actual source constraints. "
            "Baseline admission remains conditional on reviewed observed executions."
        ),
    }
    try:
        d4.require(
            math.isfinite(args.max_seconds) and args.max_seconds > 0 and args.max_nodes > 0,
            "positive finite budgets",
        )
        d4.require(dependencies_unchanged(), "frozen dependency changed")
        requested = args.case or [2175, 2176]
        d4.require(
            len(set(requested)) == len(requested) and set(requested) <= {2175, 2176},
            "requested case inventory",
        )
        manifest_path = PACKET / "receipts/nonfield-manifest/manifest.json.gz"
        manifest = read_bound(manifest_path, MANIFEST_SHA, bindings)
        d4.require(
            bindings[manifest_path] == MANIFEST_GZIP_SHA
            and manifest["source_revision"] == geometry.SOURCE_REVISION,
            "manifest binding",
        )
        d4.require(
            manifest["input_sha256s"]["A1"] == BASELINE_METADATA_SHA,
            "baseline metadata binding",
        )
        metadata = read_bound(
            PACKET / "receipts/case-census/objects" / f"{BASELINE_METADATA_SHA}.gz",
            BASELINE_METADATA_SHA,
            bindings,
        )
        excluded, canonical, allowed = baseline_context(metadata)
        missing = sorted(excluded)
        d4.require(
            bool(args.baseline_inventory) == bool(args.baseline_inventory_sha256),
            "execution inventory requires explicit SHA",
        )
        if args.baseline_inventory is not None:
            d4.require(
                args.baseline_inventory.resolve().is_relative_to(REPO),
                "execution inventory must be retained in the repository",
            )
            record = read_bound(
                args.baseline_inventory, args.baseline_inventory_sha256, bindings
            )
            missing = execution_missing(record, excluded)
        result.update(
            baseline_case_ids=sorted(excluded),
            baseline_pending_case_ids=missing,
            baseline_snapshot_sha256=BASELINE_SNAPSHOT_SHA,
            allowed_raw_masks=[list(mask) for mask in allowed],
        )
        inputs = {
            role: read_bound(
                PACKET / "receipts/d4-independent/objects" / f"{sha}.gz", sha, bindings
            )
            for role, sha in d4.INPUT_HASHES.items()
        }
        d4.require(
            inputs["overlay"]["cover_sha256"] == d4.INPUT_HASHES["cover"]
            and inputs["distance"]["overlay_sha256"] == d4.INPUT_HASHES["overlay"],
            "geometry parent identity",
        )
        cells, reconstructed = d4.check_cover(inputs["cover"])
        d4.require(reconstructed == canonical, "canonical case identity")
        budget.check()
        labels, vertices, prefixes, dimensions = d4.check_overlay(cells, inputs["overlay"])
        budget.check()
        banned = d4.check_bans(vertices, inputs["distance"])
        budget.check()
        result.update(
            overlay_prefix_counts=prefixes,
            overlay_dimensions=dimensions,
            strict_distance_bans=len(banned),
        )
        search = ForcedRegionSearch(labels, banned, allowed, budget)
        for case_id in requested:
            recipe = next(case for case in manifest["cases"] if case["mask_index"] == case_id)
            nodes = recipe["ordered_ancestry_proposal"]
            d4.require(
                recipe["adapter"] == "baseline_necessary_d4"
                and recipe["required_baseline_cases"] == 1931
                and tuple(recipe["mask"]) == canonical[case_id]
                and len(nodes) == 1
                and nodes[0]["source_sha256"] == recipe["source_sha256"],
                "cut recipe identity",
            )
            proposed = nodes[0]["constraints_proposal"]
            cuts = [
                Cut(
                    item["owner"],
                    (Q(item["normal"][0]), Q(item["normal"][1])),
                    Q(item["upper_field"]),
                )
                for item in proposed
            ]
            d4.require(
                len(cuts) == {2175: 72, 2176: 73}[case_id]
                and all(type(cut.owner) is int for cut in cuts),
                "constraint inventory",
            )
            queries = offending_regions(labels, vertices, canonical[case_id], cuts)
            checked: dict[str, Any] = {
                "mask_index": case_id,
                "source_sha256": recipe["source_sha256"],
                "node_id": nodes[0]["node_id"],
                "constraints": proposed,
                "offending_regions": queries,
                "finite_search": [],
            }
            result["cases"].append(checked)
            for region in queries:
                result.update(current_case=case_id, current_region=region)
                witness, count = search.solve(canonical[case_id], region)
                checked["finite_search"].append(
                    {
                        "region": region,
                        "owner": labels[region][0],
                        "status": "UNSAT" if witness is None else "SURVIVES",
                        "nodes": count,
                        "witness": witness,
                    }
                )
                d4.require(
                    witness is None,
                    f"offending region survives: case {case_id}, region {region}",
                )
        d4.require(
            all(d4.sha256(path) == sha for path, sha in bindings.items())
            and dependencies_unchanged()
            and d4.sha256(Path(__file__)) == result["checker_sha256"],
            "source changed during support check",
        )
        budget.check()
        admitted = not missing
        result.update(
            status="PASS_CONDITIONAL_BASELINE_D4_CUTS"
            if admitted
            else "PASS_DIAGNOSTIC_FINITE_CUT_OBLIGATIONS",
            finite_obligations_complete=True,
            baseline_execution_premise_admitted=admitted,
            necessary_cuts_verified=admitted,
            proof_credit=admitted,
            current_case=None,
            current_region=None,
        )
    except geometry.IncompleteError as error:
        result["error"] = str(error)
    except (
        ValueError,
        KeyError,
        IndexError,
        TypeError,
        OSError,
        EOFError,
        ZeroDivisionError,
        StopIteration,
    ) as error:
        result.update(status="REFUSED", error=str(error))
    result.update(
        search_nodes=budget.nodes,
        wall_seconds=time.monotonic() - started,
        process_cpu_seconds=time.process_time() - cpu_started,
        input_file_sha256={
            path.resolve().relative_to(REPO).as_posix(): sha for path, sha in bindings.items()
        },
        dependency_sha256={name: value[1] for name, value in DEPENDENCIES.items()},
    )
    atomic_write_text(args.out, json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", action="append", type=int, choices=(2175, 2176))
    parser.add_argument("--baseline-inventory", type=Path)
    parser.add_argument("--baseline-inventory-sha256")
    parser.add_argument("--max-seconds", type=float, default=120)
    parser.add_argument("--max-nodes", type=int, default=5_000_000)
    parser.add_argument("--out", type=Path, required=True)
    result = run(parser.parse_args())
    print(
        json.dumps(
            {
                key: result[key]
                for key in (
                    "status",
                    "finite_obligations_complete",
                    "necessary_cuts_verified",
                    "search_nodes",
                    "wall_seconds",
                )
            }
        )
    )
    return 0 if result["finite_obligations_complete"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
