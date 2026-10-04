"""Compile a smaller mixed model preserving frozen E/B witness certificates.

Minimum cost is restricted to J58's retained edge library and six parent rows.
There is no support search, producer split rule or whole-network equivalence claim.
"""

from __future__ import annotations

import argparse
import json
import time
from collections.abc import Callable
from dataclasses import dataclass
from itertools import product
from pathlib import Path
from typing import Any

from devtools import probe_n17_full_core_ablation as full
from devtools.check_hull_kernel_mask0 import n17_unique_frame
from devtools.check_n17_subpattern import content_sha256
from devtools.probe_n17_core_refinement import Child, child_reference, children
from devtools.probe_n17_enhanced_row_support import safe_write
from devtools.probe_n17_raw_row_support import (
    atom_reference,
    bounded_json,
    checked_inputs,
    raw_atoms,
)
from devtools.probe_n17_residual_graph import Atom, incompatible
from devtools.profile_n17_partner_memo import peak_memory_bytes
from sqpack.hull_kernel.geometry import Budget, IncompleteError, RefusalError, require
from sqpack.hull_kernel.induction import encode, strict_core
from sqpack.hull_kernel.rational import Q

SCHEMA = "n17.fixed-certificate-selective-halving.v1"
MODEL = "selective-half-chart-octagon-hull-old-core-frozen-domain-v1"
BASE_REVISION = "aba2b3123841ecac937983df30119f9844e07363"
MAX_CALLS = 1024
WALL_SECONDS = 45
MAX_PEAK_BYTES = 512 * 1024**2
FULL = (1 << 64) - 1
D_SHA = "706b1fe0ccf1179abccb0966dc12a3b3ec018eaafacc6ae62dbb62b9040e7bc1"
D_REPLAY_SHA = "aefb7c1fc604a7b6b7fd3fec1e5eb8b03d4ee20800b7c314da4d2aa3d8b2b1a5"
B_SHA = "2bbbd642423037f4f03c4388937a981e09344cd51e5c163657383cfc82bfc116"
type Parent = tuple[int, int]
type Choice = int | None
type Predicate = Callable[[Atom, Atom, Budget], bool]


def remaining(budget: Budget) -> None:
    if time.monotonic() >= budget.deadline:
        raise IncompleteError("selective certificate wall ceiling")
    if peak_memory_bytes() > MAX_PEAK_BYTES:
        raise IncompleteError("actual worker peak exceeds512MiB")


def pattern(left: int, right: int, left_half: int, right_half: int) -> int:
    require(
        all(type(i) is int for i in (left, right, left_half, right_half)),
        "noninteger mask pattern",
    )
    require(
        0 <= left < right < 6 and left_half in (0, 1) and right_half in (0, 1),
        "invalid mask pattern",
    )
    return sum(
        1 << mask
        for mask in range(64)
        if ((mask >> left) & 1) == left_half and ((mask >> right) & 1) == right_half
    )


def coverage(left: int, right: int, left_half: Choice, right_half: Choice) -> int:
    require(
        type(left) is int and type(right) is int and 0 <= left < right < 6,
        "invalid coverage positions",
    )
    require(
        all(
            value is None or (type(value) is int and value in (0, 1))
            for value in (left_half, right_half)
        ),
        "invalid coverage choices",
    )
    return sum(
        1 << mask
        for mask in range(64)
        if (left_half is None or ((mask >> left) & 1) == left_half)
        and (right_half is None or ((mask >> right) & 1) == right_half)
    )


def hex64(value: int) -> str:
    return f"0x{value:016x}"


def subsets(
    rows: list[Parent], costs: dict[Parent, int], edges: list[dict[str, Any]]
) -> tuple[list[dict[str, Any]], dict[str, Any] | None]:
    require(
        len(rows) == 6 and len(set(rows)) == 6 and rows == sorted(rows),
        "six ordered distinct parent rows required",
    )
    require(
        all(type(costs[row]) is int and costs[row] > 0 for row in rows),
        "piece costs must be positive integers",
    )
    masks = []
    for edge in edges:
        bits = pattern(
            edge["left_position"], edge["right_position"], edge["left_half"], edge["right_half"]
        )
        require(
            type(edge["coverage_hex"]) is str and int(edge["coverage_hex"], 16) == bits,
            "J edge mask differs",
        )
        masks.append(bits)
    candidates = []
    for mask in range(64):
        selected = [row for i, row in enumerate(rows) if (mask >> i) & 1]
        eligible = [
            i
            for i, edge in enumerate(edges)
            if ((mask >> edge["left_position"]) & 1) and ((mask >> edge["right_position"]) & 1)
        ]
        bits = 0
        for i in eligible:
            bits |= masks[i]
        candidates.append(
            {
                "subset_mask": mask,
                "selected_rows": [list(row) for row in selected],
                "extra_atoms": sum(costs[row] for row in selected),
                "eligible_edge_indices": eligible,
                "coverage_hex": hex64(bits),
                "feasible": bits == FULL,
            }
        )
    feasible = [candidate for candidate in candidates if candidate["feasible"]]
    chosen = (
        min(feasible, key=lambda c: (c["extra_atoms"], c["selected_rows"]))
        if feasible
        else None
    )
    return candidates, chosen


@dataclass
class Inventory:
    atoms: list[Atom]
    refs: list[dict[str, Any]]
    lookup: dict[tuple[int, Choice], int]
    selected_rows: set[Parent]
    digest: str

    def variants(self, raw_index: int) -> list[int]:
        if (raw_index, None) in self.lookup:
            return [self.lookup[raw_index, None]]
        return [self.lookup[raw_index, half] for half in (0, 1)]


@dataclass
class Bound:
    context: full.Context
    inventory: Inventory
    d_packet: dict[str, Any]
    j_tuple: dict[str, Any]
    b_selections: list[list[int]]
    e_survivor_projection: list[dict[str, Any]]
    header: dict[str, Any]


def build_inventory(
    context: full.Context, full_atoms: list[Atom], selected: set[Parent], budget: Budget
) -> tuple[Inventory, dict[Parent, tuple[Child, Child]]]:
    refined, _ = children(
        context.frame, context.raw, context.selections, context.document, budget
    )
    representatives: dict[Parent, tuple[Child, Child]] = {}
    for raw_index, _ in sorted(refined):
        atom = context.raw[raw_index]
        representatives[atom.owner, atom.row] = refined[raw_index, 0], refined[raw_index, 1]
    require(selected <= set(representatives), "selected row outside inventory")
    atoms, refs, lookup = [], [], {}
    for raw_index, old in enumerate(context.raw):
        remaining(budget)
        choices: tuple[Choice, ...] = (0, 1) if (old.owner, old.row) in selected else (None,)
        for half in choices:
            if half is None:
                atom = full_atoms[raw_index]
                interval = tuple(
                    Q(value)
                    for value in context.document["final_state"]["cells"][str(old.owner)][
                        old.row
                    ]["interval"]
                )
            else:
                child = representatives[old.owner, old.row][half]
                atom = Atom(old.owner, old.row, old.pieces, old.domain, child.atom.core)
                interval = child.interval
            require(
                atom.domain == old.domain and atom.pieces == old.pieces,
                "mixed domain/piece changed",
            )
            strict_core(context.frame, atom.core, *interval)
            lookup[raw_index, half] = len(atoms)
            atoms.append(atom)
            refs.append(
                {
                    **atom_reference(old, context.document),
                    "raw_atom_index": raw_index,
                    "kind": "full" if half is None else "half",
                    "half": half,
                    "model_interval": [str(value) for value in interval],
                    "model_core_sha256": content_sha256(encode(atom.core)),
                }
            )
    extra = sum((a.owner, a.row) in selected for a in context.raw)
    require(
        len(atoms) == len(context.raw) + extra < 5044 and len(lookup) == len(atoms),
        "mixed inventory ceiling/identity differs",
    )
    remaining(budget)
    return Inventory(atoms, refs, lookup, selected, content_sha256(refs)), representatives


def bind(
    document: dict[str, Any],
    identity: dict[str, Any],
    *,
    source: dict[str, Any],
    baseline: dict[str, Any],
    refinement: dict[str, Any],
    certificate: dict[str, Any],
    d_packet: dict[str, Any],
    d_replay: dict[str, Any],
    b_packet: dict[str, Any],
    budget: Budget,
) -> Bound:
    remaining(budget)
    require(
        content_sha256(d_packet) == D_SHA
        and content_sha256(d_replay) == D_REPLAY_SHA
        and content_sha256(b_packet) == B_SHA,
        "frozen D/replay/B identity differs",
    )
    frame = n17_unique_frame()
    raw = raw_atoms(frame, document)
    context = full.bind(
        frame,
        raw,
        document,
        identity,
        source=source,
        baseline=baseline,
        refinement=refinement,
        certificate=certificate,
        budget=budget,
        endpoint=False,
    )
    require(
        d_replay["status"] == "PASS_REPLAYED_FIXED_SAMPLE"
        and d_replay["packet_sha256"] == D_SHA,
        "D accepted replay differs",
    )
    require(
        d_packet["full_lost_indices"] == sorted(context.h_lost - {58})
        and d_packet["halving_additional_lost_indices"] == [58],
        "D/J partition differs",
    )
    full_atoms, full_rows, failure = full.geometry(context, budget)
    require(
        failure is None and full_rows == d_packet["full_core_rows"],
        "D geometry/nesting differs",
    )
    require(
        content_sha256([full.full_reference(i, a, context) for i, a in enumerate(full_atoms)])
        == d_packet["full_inventory_sha256"],
        "D inventory differs",
    )
    matches = [
        entry
        for entry in certificate["tuple_certificates"]
        if entry["source_selection_index"] == 58
    ]
    require(
        len(matches) == 1 and len(matches[0]["incompatible_pairs"]) == 7,
        "J58 edge inventory differs",
    )
    j_tuple = matches[0]
    rows = [(raw[i].owner, raw[i].row) for i in context.selections[58]]
    costs = {row: sum((a.owner, a.row) == row for a in raw) for row in rows}
    candidates, chosen = subsets(rows, costs, j_tuple["incompatible_pairs"])
    if chosen is None:
        raise RefusalError("no eligible fixed-library subset")
    selected = {(row[0], row[1]) for row in chosen["selected_rows"]}
    inventory, halves = build_inventory(context, full_atoms, selected, budget)
    require(
        chosen["extra_atoms"] == len(inventory.atoms) - len(raw),
        "chosen cost/model size differs",
    )
    require(
        b_packet["input_identity"] == identity and len(b_packet["selections"]) == 44,
        "B input/selection inventory differs",
    )
    original_lookup = {(a.owner, a.row, a.pieces[0]): i for i, a in enumerate(raw)}
    b_selections = []
    owners = sorted({a.owner for a in raw})
    projections = []
    for selection_number, selection in enumerate(b_packet["selections"]):
        remaining(budget)
        projected, originals = [], []
        require([ref["owner"] for ref in selection] == owners, "B tuple owner order differs")
        for ref in selection:
            key = ref["owner"], ref["row"], ref["piece"]
            require(
                all(type(value) is int for value in key) and key in original_lookup,
                "invalid B raw key",
            )
            raw_index = original_lookup[key]
            half = ref["half"]
            require(
                type(half) is int
                and half in (0, 1)
                and type(ref["raw_atom_index"]) is int
                and ref["raw_atom_index"] == raw_index,
                "B raw/half index differs",
            )
            old = raw[raw_index]
            representative = halves[old.owner, old.row][half]
            child = Child(
                raw_index,
                half,
                representative.interval,
                Atom(old.owner, old.row, old.pieces, old.domain, representative.atom.core),
            )
            expected = {**child_reference(child, raw, document), "raw_atom_index": raw_index}
            require(
                content_sha256(ref) == content_sha256(expected),
                "B exact child reference differs",
            )
            projected.append(
                inventory.lookup[raw_index, half if (old.owner, old.row) in selected else None]
            )
            originals.append(raw_index)
        b_selections.append(projected)
        if selection_number < 7:
            h = refinement["enhanced_selections"][selection_number]
            require(
                content_sha256(
                    [
                        {k: v for k, v in ref.items() if k != "raw_atom_index"}
                        for ref in selection
                    ]
                )
                == content_sha256(h["atoms"]),
                "B/H full retained prefix differs",
            )
            source_index = h["source_selection_index"]
            require(
                originals == context.selections[source_index],
                "E surviving tuple raw references differ",
            )
            projections.append(
                {
                    "source_E_index": source_index,
                    "B_selection_index": selection_number,
                    "original_atoms": [atom_reference(raw[i], document) for i in originals],
                    "projected_atoms": [inventory.refs[i] for i in projected],
                }
            )
    require(
        {entry["source_E_index"] for entry in projections} == context.h_survivors,
        "E7 survivor mapping differs",
    )
    header = {
        "schema": SCHEMA,
        "model": MODEL,
        "predicate": full.PREDICATE,
        "baseline_revision": BASE_REVISION,
        "input_identity": identity,
        "E_packet_sha256": content_sha256(source),
        "baseline_replay_sha256": content_sha256(baseline),
        "H_packet_sha256": content_sha256(refinement),
        "J_certificate_sha256": content_sha256(certificate),
        "D_packet_sha256": D_SHA,
        "D_replay_sha256": D_REPLAY_SHA,
        "B_packet_sha256": B_SHA,
        "raw_atoms": len(raw),
        "mixed_atoms": len(inventory.atoms),
        "H_atoms": 5044,
        "extra_atoms": chosen["extra_atoms"],
        "selected_parent_rows": chosen["selected_rows"],
        "row_costs": [
            {"owner": row[0], "row": row[1], "piece_count": costs[row]} for row in rows
        ],
        "candidate_subsets": candidates,
        "chosen_subset_mask": chosen["subset_mask"],
        "chosen_J58_edge_indices": chosen["eligible_edge_indices"],
        "restricted_library_minimum_verified": True,
        "mixed_inventory_sha256": inventory.digest,
        "E_surviving_projection": projections,
        "diagnostic_only": True,
        "new_exclusions": 0,
        "unsupported_rows_verified": False,
        "whole_network_equivalence_verified": False,
        "limits": {
            "uncached_pair_calls": MAX_CALLS,
            "wall_seconds": WALL_SECONDS,
            "worker_peak_bytes": MAX_PEAK_BYTES,
        },
        "mask_convention": (
            "bit i is half choice of ascending-owner position i; assignment index0..63; "
            "unrefined positions project to their sole full atom"
        ),
    }
    remaining(budget)
    return Bound(context, inventory, d_packet, j_tuple, b_selections, projections, header)


@dataclass
class Guard:
    budget: Budget
    predicate: Predicate = incompatible
    calls: int = 0

    def check_pair(self, left: Atom, right: Atom) -> bool:
        remaining(self.budget)
        require(left.owner < right.owner, "noncanonical directed pair")
        if self.calls >= MAX_CALLS:
            raise IncompleteError("selective certificate pair ceiling")
        self.calls += 1
        value = self.predicate(left, right, self.budget)
        remaining(self.budget)
        require(type(value) is bool, "predicate did not return exactbool")
        return value


def prove(
    bound: Bound,
    budget: Budget,
    *,
    predicate: Predicate = incompatible,
    checkpoint: Callable[[dict[str, Any]], None] | None = None,
) -> dict[str, Any]:
    inv, context = bound.inventory, bound.context
    result = {
        **bound.header,
        "status": "INCOMPLETE",
        "reason": "progress checkpoint",
        "negative_certificates": [],
        "positive_selections": [],
        "fresh_pair_calls": 0,
    }
    guard = Guard(budget, predicate)

    def retain(i: int, edges: list[dict[str, Any]], kind: str) -> None:
        bits = 0
        for edge in edges:
            bits |= int(edge["coverage_hex"], 16)
        require(bits == FULL, "fixed loss certificate omits assignments")
        result["negative_certificates"].append(
            {"source_E_index": i, "library": kind, "edges": edges, "coverage_hex": hex64(bits)}
        )

    try:
        for i in bound.d_packet["full_lost_indices"]:
            remaining(budget)
            original = context.selections[i]
            witness = bound.d_packet["tuple_results"][i]["first_collision"]
            left, right = witness["left_position"], witness["right_position"]
            require(0 <= left < right < 6, "D witness position differs")
            edges = []
            for a, b in product(inv.variants(original[left]), inv.variants(original[right])):
                require(
                    guard.check_pair(inv.atoms[a], inv.atoms[b]) is True,
                    "D mixed witness not colliding",
                )
                edges.append(
                    {
                        "left_position": left,
                        "right_position": right,
                        "left_atom": inv.refs[a],
                        "right_atom": inv.refs[b],
                        "coverage_hex": hex64(
                            coverage(left, right, inv.refs[a]["half"], inv.refs[b]["half"])
                        ),
                    }
                )
            retain(i, edges, "D-full-collision-variants")
            result["fresh_pair_calls"] = guard.calls
            if checkpoint:
                checkpoint(result)
        original = context.selections[58]
        edges = []
        for edge_index in bound.header["chosen_J58_edge_indices"]:
            edge = bound.j_tuple["incompatible_pairs"][edge_index]
            left, right = edge["left_position"], edge["right_position"]
            a, b = (
                inv.lookup[original[left], edge["left_half"]],
                inv.lookup[original[right], edge["right_half"]],
            )
            require(
                guard.check_pair(inv.atoms[a], inv.atoms[b]) is True,
                "J58 selected witness not colliding",
            )
            edges.append(
                {
                    "J58_edge_index": edge_index,
                    "left_position": left,
                    "right_position": right,
                    "left_atom": inv.refs[a],
                    "right_atom": inv.refs[b],
                    "coverage_hex": hex64(
                        pattern(left, right, edge["left_half"], edge["right_half"])
                    ),
                }
            )
        retain(58, edges, "J58-eligible-half-collisions")
        for i, selection in enumerate(bound.b_selections):
            for left in range(6):
                for right in range(left + 1, 6):
                    require(
                        guard.check_pair(
                            inv.atoms[selection[left]], inv.atoms[selection[right]]
                        )
                        is False,
                        "B projected clique has a collision",
                    )
            result["positive_selections"].append(
                {"B_selection_index": i, "atoms": [inv.refs[j] for j in selection]}
            )
            result["fresh_pair_calls"] = guard.calls
            if checkpoint:
                checkpoint(result)
        lost = sorted(c["source_E_index"] for c in result["negative_certificates"])
        require(lost == sorted(context.h_lost), "E72 lost set differs")
        parents = sorted(
            {
                (inv.atoms[j].owner, inv.atoms[j].row)
                for selection in bound.b_selections
                for j in selection
            }
        )
        require(
            len(bound.b_selections) == 44 and len(parents) == 60,
            "B44/60 positive inventory differs",
        )
        remaining(budget)
        result.update(
            status="PASS_FIXED_CERTIFICATES_PRESERVED",
            reason=None,
            fixed_E_lost_indices=lost,
            fixed_E_survivor_indices=sorted(context.h_survivors),
            supported_parent_rows=[list(row) for row in parents],
            supported_parents=60,
            unknown_parents=36,
            fresh_pair_calls=guard.calls,
            fixed_E79_classification_preserved=True,
        )
    except (IncompleteError, RefusalError) as error:
        result.update(
            status="INCOMPLETE" if isinstance(error, IncompleteError) else "REFUSED",
            reason=str(error),
            fresh_pair_calls=guard.calls,
        )
    return result


def verify_packet(value: dict[str, Any], bound: Bound, budget: Budget) -> dict[str, Any]:
    for key, expected in bound.header.items():
        require(
            content_sha256(value.get(key)) == content_sha256(expected), f"packet {key} differs"
        )
    require(
        value["status"] == "PASS_FIXED_CERTIFICATES_PRESERVED",
        "partial packet cannot certify preservation",
    )
    fresh = prove(bound, budget)
    scientific = {
        k: v for k, v in value.items() if k not in {"wall_seconds", "worker_peak_bytes"}
    }
    require(
        content_sha256(fresh) == content_sha256(scientific),
        "fresh mixed certificate replay differs",
    )
    remaining(budget)
    return {
        "status": "PASS_REPLAYED_FIXED_CERTIFICATES",
        "packet_sha256": content_sha256(value),
        "fresh_pair_calls": fresh["fresh_pair_calls"],
        "mixed_atoms": len(bound.inventory.atoms),
        "selected_parent_rows": bound.header["selected_parent_rows"],
        "extra_atoms": bound.header["extra_atoms"],
        "fixed_E_lost_indices": fresh["fixed_E_lost_indices"],
        "fixed_E_survivor_indices": fresh["fixed_E_survivor_indices"],
        "supported_parents": fresh["supported_parents"],
        "input_identity": bound.header["input_identity"],
        "diagnostic_only": True,
        "new_exclusions": 0,
        "unsupported_rows_verified": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    for name in (
        "checked-receipt",
        "source-packet",
        "baseline-replay",
        "refinement-packet",
        "conflict-certificate",
        "full-packet",
        "full-replay",
        "support-packet",
        "output",
    ):
        parser.add_argument("--" + name, type=Path, required=True)
    parser.add_argument("--verify", type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    budget = Budget(started + WALL_SECONDS, MAX_CALLS)
    result: dict[str, Any] = {
        "diagnostic_only": True,
        "new_exclusions": 0,
        "unsupported_rows_verified": False,
    }
    try:
        document, identity = checked_inputs(args.directory, args.checked_receipt)
        bound = bind(
            document,
            identity,
            source=bounded_json(args.source_packet),
            baseline=bounded_json(args.baseline_replay),
            refinement=bounded_json(args.refinement_packet),
            certificate=bounded_json(args.conflict_certificate),
            d_packet=bounded_json(args.full_packet),
            d_replay=bounded_json(args.full_replay),
            b_packet=bounded_json(args.support_packet),
            budget=budget,
        )
        if args.verify:
            result = verify_packet(bounded_json(args.verify), bound, budget)
        else:
            result = prove(
                bound,
                budget,
                checkpoint=lambda value: safe_write(
                    args.output.with_suffix(".partial.json"), value
                ),
            )
    except (
        IncompleteError,
        RefusalError,
        KeyError,
        IndexError,
        TypeError,
        ValueError,
        OSError,
    ) as error:
        result.update(
            status="INCOMPLETE" if isinstance(error, IncompleteError) else "REFUSED",
            reason=f"{type(error).__name__}: {error}",
        )
    result.update(
        wall_seconds=time.monotonic() - started, worker_peak_bytes=peak_memory_bytes()
    )
    safe_write(args.output, result)
    print(
        json.dumps(
            {
                k: v
                for k, v in result.items()
                if k
                not in {
                    "candidate_subsets",
                    "negative_certificates",
                    "positive_selections",
                    "E_surviving_projection",
                    "input_identity",
                }
            }
        )
    )
    return 0 if str(result["status"]).startswith("PASS_") else 2


if __name__ == "__main__":
    raise SystemExit(main())
