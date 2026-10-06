"""Lazy parent-row supports in the frozen H enhanced-core binary network.

Every original residual piece receives two strict half-interval cores and retains
its original center domain and parent row. Positive cliques only; misses are unknown.
"""

from __future__ import annotations

import argparse
import json
import time
from dataclasses import dataclass
from functools import partial
from itertools import combinations
from pathlib import Path
from typing import Any

from devtools.bounded_diagnostics import (
    MAX_MEMORY_BYTES,
    check_budget,
    retained_matches,
    same_header,
    same_inputs,
)
from devtools.bounded_diagnostics import write_json as safe_write
from devtools.check_hull_kernel_mask0 import n17_unique_frame
from devtools.check_n17_subpattern import content_sha256
from devtools.pilot_n17_capture import load_endpoint
from devtools.probe_n17_core_refinement import MODEL, augmented_core, bound_source, halves
from devtools.probe_n17_raw_row_support import (
    MAX_ATOMS,
    PREDICATE,
    LazySupports,
    atom_reference,
    bounded_json,
    checked_inputs,
    endpoint_selection,
    raw_atoms,
)
from devtools.probe_n17_residual_graph import Atom, incompatible
from devtools.process_memory import peak_memory_bytes
from sqpack.hull_kernel.frame import Frame
from sqpack.hull_kernel.geometry import Budget, IncompleteError, RefusalError, require
from sqpack.hull_kernel.induction import encode
from sqpack.hull_kernel.rational import Q

SCHEMA = "n17.enhanced-parent-row-support.v1"
MAX_CHILD_ATOMS = 8192
MAX_PARENT_ROWS = 128
MAX_PAIRS = 100_000
MAX_NODES = 100_000
WALL_SECONDS = 180
REPLAY_SECONDS = 120
BASE_REVISION = "14d131c8aaf2ac94239755f8438ab7d5e0192ef4"
H_PATH = {
    False: (
        "packing/campaign/explorations/X048-session-174-core-refinement/"
        "receipts/B-enhanced-packet.json"
    ),
    True: (
        "packing/campaign/explorations/X048-session-174-core-refinement/"
        "receipts/endpoint-enhanced-packet.json"
    ),
}
ARTIFACT_PROVENANCE = {
    "historical_revision": BASE_REVISION,
    "committed_paths": {"H_PATH": H_PATH},
}
type Parent = tuple[int, int]


remaining = partial(check_budget, wall_message="enhanced support wall ceiling")


def bounded_incompatible(left: Atom, right: Atom, budget: Budget) -> bool:
    remaining(budget)
    result = incompatible(left, right, budget)
    remaining(budget)  # LazySupports stores a result only after this returns.
    require(type(result) is bool, "pair result must be exact bool")
    return result


@dataclass
class Inventory:
    raw: list[Atom]
    atoms: list[Atom]
    references: list[dict[str, Any]]
    lookup: dict[tuple[int, int, int, int], int]
    digest: str

    def parents(self) -> set[Parent]:
        return {(atom.owner, atom.row) for atom in self.atoms}


def build_inventory(
    frame: Frame, raw: list[Atom], document: dict[str, Any], budget: Budget
) -> Inventory:
    require(0 < len(raw) <= MAX_ATOMS, "original raw4096 inventory ceiling")
    require(len(raw) * 2 <= MAX_CHILD_ATOMS, "derived child8192 ceiling")
    require(len({a.owner for a in raw}) <= 6, "owner ceiling")
    require(len({(a.owner, a.row) for a in raw}) <= MAX_PARENT_ROWS, "parent ceiling")
    cores: dict[Parent, Any] = {}
    atoms: list[Atom] = []
    references = []
    lookup = {}
    for raw_index, atom in enumerate(raw):
        remaining(budget)
        row = document["final_state"]["cells"][str(atom.owner)][atom.row]
        intervals = halves(*(Q(value) for value in row["interval"]))
        key = atom.owner, atom.row
        if key not in cores:
            cores[key] = (
                atom.core,
                intervals,
                [augmented_core(frame, atom.core, interval) for interval in intervals],
            )
        old, recorded, enhanced = cores[key]
        require(old == atom.core and recorded == intervals, "parent core identity differs")
        original = atom_reference(atom, document)
        for half, interval in enumerate(intervals):
            index = len(atoms)
            require(index == 2 * raw_index + half, "unstable derived index")
            atoms.append(Atom(atom.owner, atom.row, atom.pieces, atom.domain, enhanced[half]))
            references.append(
                {
                    **original,
                    "raw_atom_index": raw_index,
                    "half": half,
                    "child_interval": [str(value) for value in interval],
                    "child_core_sha256": content_sha256(encode(enhanced[half])),
                }
            )
            lookup[atom.owner, atom.row, atom.pieces[0], half] = index
    require(len(lookup) == len(atoms), "duplicate child identity")
    require(len(atoms) == 2 * len(raw), "undercoverage")
    remaining(budget)
    return Inventory(raw, atoms, references, lookup, content_sha256(references))


def fixture_inventory(inv: Inventory, refinement: dict[str, Any], *, endpoint: bool) -> None:
    expected = (148, 296, 24, 48, 15) if endpoint else (2522, 5044, 96, 192, 7)
    require(
        (
            len(inv.raw),
            len(inv.atoms),
            len(inv.parents()),
            2 * len(inv.parents()),
            len(refinement["enhanced_selections"]),
        )
        == expected,
        "frozen fixture derived inventory differs",
    )
    require(
        retained_matches(refinement, BASE_REVISION, H_PATH[endpoint]),
        "frozen H packet identity differs",
    )


def selection_indices(refs: list[dict[str, Any]], inv: Inventory) -> list[int]:
    selected = []
    for ref in refs:
        key = ref["owner"], ref["row"], ref["piece"], ref["half"]
        require(all(type(value) is int and value >= 0 for value in key), "invalid child key")
        require(key[3] in (0, 1) and key in inv.lookup, "unknown child key")
        index = inv.lookup[key]
        require(ref == inv.references[index], "exact child provenance differs")
        selected.append(index)
    require(
        [inv.atoms[index].owner for index in selected] == sorted({a.owner for a in inv.atoms}),
        "selection owner inventory differs",
    )
    return selected


def seeds(
    refinement: dict[str, Any],
    source: dict[str, Any],
    baseline: dict[str, Any],
    inv: Inventory,
    document: dict[str, Any],
    *,
    identity: dict[str, Any],
) -> list[list[int]]:
    original_selections = bound_source(source, baseline, inv.raw, document, identity)
    require(refinement["schema"] == "n17.fixed-witness-core-refinement.v1", "H grammar differs")
    require(
        refinement["model"] == MODEL and refinement["predicate"] == PREDICATE, "H model differs"
    )
    require(
        refinement["diagnostic_only"] is True and refinement["new_exclusions"] == 0,
        "H exclusion claim",
    )
    require(same_inputs(refinement["input_identity"], identity), "H input identity differs")
    result, seen = [], set()
    for item in refinement["enhanced_selections"]:
        original_index = item["source_selection_index"]
        require(
            type(original_index) is int
            and 0 <= original_index < len(original_selections)
            and original_index not in seen,
            "H selection index differs",
        )
        seen.add(original_index)
        refs = []
        for raw_index, ref in zip(
            original_selections[original_index], item["atoms"], strict=True
        ):
            half = ref["half"]
            require(type(half) is int and half in (0, 1), "H half differs")
            expected = inv.references[2 * raw_index + half]
            require(
                ref
                == {key: value for key, value in expected.items() if key != "raw_atom_index"},
                "H exact child differs",
            )
            refs.append(expected)
        result.append(selection_indices(refs, inv))
    require(0 < len(result) <= 79, "H seed ceiling")
    covered = {parent for selection in result for parent in parent_coverage(selection, inv)}
    require(
        [list(row) for row in sorted(covered)] == refinement["supported_parent_rows"],
        "H parent coverage differs",
    )
    return result


def parent_coverage(selection: list[int], inv: Inventory) -> set[Parent]:
    return {(inv.atoms[index].owner, inv.atoms[index].row) for index in selection}


def prevalidate(search: LazySupports, initial: list[list[int]]) -> None:
    """Validate ALL seeds in a fresh charged cache before marking any coverage."""
    require(
        not search.cache and not search.selections and not search.supported,
        "seed cache not fresh",
    )
    for selection in initial:
        for left, right in combinations(selection, 2):
            require(search.compatible(left, right), "seed collision")
    remaining(search.budget)
    require(not search.supported, "seed coverage marked before full validation")


def header(
    inv: Inventory,
    identity: dict[str, Any],
    refinement: dict[str, Any],
    source: dict[str, Any],
    baseline: dict[str, Any],
) -> dict[str, Any]:
    del refinement, source, baseline  # Preserve the public helper signature.
    return {
        "schema": SCHEMA,
        "artifact_provenance": ARTIFACT_PROVENANCE,
        "model": MODEL,
        "predicate": PREDICATE,
        "diagnostic_only": True,
        "new_exclusions": 0,
        "unsupported_rows_verified": False,
        "baseline_repository_revision": BASE_REVISION,
        "input_identity": identity,
        "raw_atoms": len(inv.raw),
        "child_atoms": len(inv.atoms),
        "live_parent_rows": len(inv.parents()),
        "half_rows": 2 * len(inv.parents()),
        "limits": {
            "unique_pairs": MAX_PAIRS,
            "nodes": MAX_NODES,
            "wall_seconds": WALL_SECONDS,
            "peak_bytes": MAX_MEMORY_BYTES,
        },
    }


def packet(
    snapshot: dict[str, Any],
    inv: Inventory,
    common: dict[str, Any],
    initial: list[list[int]],
    *,
    seeded: bool,
) -> dict[str, Any]:
    selections = snapshot["selections"]
    covered = set().union(*(parent_coverage(selection, inv) for selection in selections))
    before = set().union(*(parent_coverage(selection, inv) for selection in initial))
    status = snapshot["status"]
    if status == "EXHAUSTIVE_UNSUPPORTED_ROWS":
        status = "PARTIAL_SUPPORT"
    return {
        **common,
        "status": status,
        "reason": snapshot.get("reason"),
        "seeds_freshly_prevalidated": seeded,
        "seed_selections": len(initial),
        "initial_selections_revalidated": snapshot["initial_selections_revalidated"],
        "initial_supported_rows": snapshot["initial_supported_rows"],
        "initial_unique_pairs": snapshot["initial_unique_pairs"],
        "search_nodes": snapshot["search_nodes"],
        "unique_pair_tests": snapshot["unique_pair_tests"],
        "cache_entries": snapshot["cache_entries"],
        "selections": [
            [inv.references[index] for index in selection] for selection in selections
        ],
        "supported_parent_rows": [list(row) for row in sorted(covered)],
        "new_parent_rows": [list(row) for row in sorted(covered - before)],
        "unknown_parent_rows": [list(row) for row in sorted(inv.parents() - covered)],
        "exhaustive_unverified_candidates": snapshot["exhaustive_unsupported_rows"],
    }


def verify_packet(
    value: dict[str, Any],
    inv: Inventory,
    common: dict[str, Any],
    initial: list[list[int]],
    budget: Budget,
) -> dict[str, Any]:
    require(
        same_header(value, common),
        "packet model/input/inventory differs",
    )
    require(
        value["status"] in {"ALL_ROWS_SUPPORTED", "PARTIAL_SUPPORT", "INCOMPLETE", "RUNNING"},
        "packet status differs",
    )
    held = value["selections"]
    require(isinstance(held, list) and len(held) <= MAX_PARENT_ROWS + 79, "selection ceiling")
    prefix = [[inv.references[index] for index in selection] for selection in initial]
    require(held[: len(prefix)] == prefix, "full seed prefix differs")
    before = set().union(*(parent_coverage(selection, inv) for selection in initial))
    require(
        value["seeds_freshly_prevalidated"] is True
        and value["seed_selections"] == len(initial)
        and value["initial_selections_revalidated"] == len(initial)
        and value["initial_supported_rows"] == len(before),
        "seed metadata differs",
    )
    covered, checks = set(), 0
    for refs in held:
        remaining(budget)
        selection = selection_indices(refs, inv)
        for left, right in combinations(selection, 2):
            require(
                not bounded_incompatible(inv.atoms[left], inv.atoms[right], budget),
                "retained selection collision",
            )
            checks += 1
        covered.update(parent_coverage(selection, inv))
    require(
        value["supported_parent_rows"] == [list(row) for row in sorted(covered)],
        "claimed parent coverage differs",
    )
    require(
        value["new_parent_rows"] == [list(row) for row in sorted(covered - before)],
        "claimed new parents differ",
    )
    require(
        value["unknown_parent_rows"] == [list(row) for row in sorted(inv.parents() - covered)],
        "claimed unknown parents differ",
    )
    if value["status"] == "ALL_ROWS_SUPPORTED":
        require(covered == inv.parents(), "all-parent claim differs")
    remaining(budget)
    return {
        "status": "PASS_REPLAYED_ALL_PARENT_ROWS"
        if covered == inv.parents()
        else "PASS_REPLAYED_PARTIAL_SUPPORT",
        "supported_parent_rows": len(covered),
        "live_parent_rows": len(inv.parents()),
        "new_parent_rows": [list(row) for row in sorted(covered - before)],
        "selections_checked": len(held),
        "fresh_pair_checks": checks,
        "packet_content_verified": True,
        "input_identity": common["input_identity"],
        "unsupported_rows_verified": False,
    }


def endpoint_children(
    frame: Frame, document: dict[str, Any], inv: Inventory, initial: list[list[int]]
) -> None:
    original = endpoint_selection(frame, document, inv.raw)
    require([index // 2 for index in initial[0]] == original, "endpoint raw seed differs")
    targets = load_endpoint(frame).by_owner()
    for index in initial[0]:
        lo, hi = (Q(value) for value in inv.references[index]["child_interval"])
        require(
            any(
                lo <= low and high <= hi for low, high in targets[inv.atoms[index].owner].charts
            ),
            "endpoint enclosure crosses child split",
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--checked-receipt", type=Path, required=True)
    parser.add_argument("--source-packet", type=Path, required=True)
    parser.add_argument("--baseline-replay", type=Path, required=True)
    parser.add_argument("--refinement-packet", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--verify", type=Path)
    parser.add_argument("--endpoint", action="store_true")
    args = parser.parse_args()
    started, cpu = time.monotonic(), time.process_time()
    budget = Budget(started + (REPLAY_SECONDS if args.verify else WALL_SECONDS), MAX_NODES)
    result: dict[str, Any] = {
        "diagnostic_only": True,
        "new_exclusions": 0,
        "unsupported_rows_verified": False,
    }
    try:
        document, identity = checked_inputs(args.directory, args.checked_receipt)
        frame = n17_unique_frame()
        raw = raw_atoms(frame, document)
        inv = build_inventory(frame, raw, document, budget)
        refinement = bounded_json(args.refinement_packet)
        fixture_inventory(inv, refinement, endpoint=args.endpoint)
        source, baseline = bounded_json(args.source_packet), bounded_json(args.baseline_replay)
        initial = seeds(refinement, source, baseline, inv, document, identity=identity)
        common = header(inv, identity, refinement, source, baseline)
        if args.endpoint:
            endpoint_children(frame, document, inv, initial)
            common["endpoint_angle_children_checked"] = True
        if args.verify:
            result.update(
                verify_packet(bounded_json(args.verify), inv, common, initial, budget)
            )
        else:
            search = LazySupports(
                inv.atoms,
                budget,
                predicate=bounded_incompatible,
                max_pairs=MAX_PAIRS,
                max_nodes=MAX_NODES,
            )
            prevalidate(search, initial)

            def checkpoint(snapshot: dict[str, Any]) -> None:
                safe_write(
                    args.output.with_suffix(".partial.json"),
                    packet(snapshot, inv, common, initial, seeded=True),
                )

            snapshot = search.run(
                initial_selections=initial, strategy="forward-mrv", checkpoint=checkpoint
            )
            result.update(packet(snapshot, inv, common, initial, seeded=True))
    except (IncompleteError, RefusalError) as error:
        result.update(
            status="INCOMPLETE" if isinstance(error, IncompleteError) else "REFUSED",
            reason=str(error),
        )
    result.update(
        wall_seconds=time.monotonic() - started,
        cpu_seconds=time.process_time() - cpu,
        worker_peak_bytes=peak_memory_bytes(),
    )
    safe_write(args.output, result)
    print(
        json.dumps(
            {key: result[key] for key in ("status", "wall_seconds", "worker_peak_bytes")}
        ),
        flush=True,
    )
    raise SystemExit(0 if result["status"] != "REFUSED" else 2)


if __name__ == "__main__":
    main()
