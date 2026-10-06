"""Bounded compatibility diagnostic; never a certificate or an admission path.

Every atom covers possible poses of one owner in one angle row. A missing edge
means strict inner cores collide for every pair of centres in the two domains.
Present edges mean only that this test did not prove a collision. Arc and path
consistency preserve every complete compatible selection; survival is not feasibility.
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
    check_budget,
    read_json,
    write_json,
)
from devtools.check_hull_kernel_mask0 import n17_unique_frame
from devtools.check_n17_subpattern import content_sha256, saved_files
from devtools.pilot_n17_capture import endpoint_holds, load_endpoint
from devtools.process_memory import peak_memory_bytes
from sqpack.hull_kernel.collision import universal_collision
from sqpack.hull_kernel.frame import Frame
from sqpack.hull_kernel.geometry import Budget, IncompleteError, Polygon, RefusalError, require
from sqpack.hull_kernel.induction import hull, strict_core
from sqpack.hull_kernel.node import points
from sqpack.hull_kernel.rational import Q

MAX_INPUT_BYTES = 64 * 1024 * 1024


@dataclass
class Atom:
    owner: int
    row: int
    pieces: tuple[int, ...]
    domain: Polygon
    core: Polygon


remaining = partial(check_budget, wall_message="graph wall ceiling")


def atomize(frame: Frame, document: dict[str, Any], mode: str) -> dict[int, list[Atom]]:
    """All pieces are covered, including points and segments; no area filtering."""
    require(mode in {"row-hull", "pieces", "two-cover"}, "unknown abstraction")
    result: dict[int, list[Atom]] = {}
    for owner_text, rows in document["final_state"]["cells"].items():
        owner = int(owner_text)
        result[owner] = []
        for row_index, row in enumerate(rows):
            pieces = [
                (index, points(poly)) for index, poly in enumerate(row["residual_polygons"])
            ]
            require(all(poly for _, poly in pieces), "empty residual piece")
            if not pieces:
                continue
            reference = row["reference"]
            require(reference["kind"] == "phase3", "unprocessed seed row is unsupported")
            require(reference["node"] == document["node_id"], "foreign row reference")
            step = document["steps"][reference["step"]]
            source = step["rows"][reference["row"]]
            require(
                step["owner"] == owner and source["interval"] == row["interval"],
                "row source differs",
            )
            core = points(source["core_vertices"])
            lo, hi = (Q(value) for value in row["interval"])
            strict_core(frame, core, lo, hi)
            if mode == "pieces":
                groups = [[piece] for piece in pieces]
            elif mode == "row-hull" or len(pieces) == 1:
                groups = [pieces]
            else:
                # Exact, deterministic ordering is a heuristic only. Both hulls are
                # outer covers: every original polygon belongs to exactly one group.
                ordered = sorted(
                    pieces,
                    key=lambda item: (sum(x for x, _ in item[1]) / len(item[1]), item[0]),
                )
                middle = (len(ordered) + 1) // 2
                groups = [ordered[:middle], ordered[middle:]]
            result[owner].extend(
                Atom(
                    owner,
                    row_index,
                    tuple(index for index, _ in group),
                    hull([point for _, poly in group for point in poly]),
                    core,
                )
                for group in groups
            )
    return result


def incompatible(left: Atom, right: Atom, budget: Budget) -> bool:
    require(bool(left.domain) and bool(right.domain), "empty atom")
    try:
        universal_collision(
            left.core, left.domain, [(right.domain, right.core)], left.domain, budget=budget
        )
    except RefusalError as error:
        if str(error) != "region escapes universal collision set":
            raise
        return False
    return True


def propagate(
    domains: list[set[int]], edges: list[set[int]], budget: Budget, *, path: bool
) -> None:
    """Mutate symmetric relations to an AC or alternating AC/PC fixed point."""
    changed = True
    while changed:
        remaining(budget)
        changed = False
        for owner, domain in enumerate(domains):
            for atom in sorted(domain):
                if any(
                    not (edges[atom] & other)
                    for index, other in enumerate(domains)
                    if index != owner
                ):
                    domain.remove(atom)
                    for neighbor in tuple(edges[atom]):
                        edges[neighbor].discard(atom)
                    edges[atom].clear()
                    changed = True
        if not path:
            continue
        for left_owner, right_owner in combinations(range(len(domains)), 2):
            remaining(budget)
            for left in sorted(domains[left_owner]):
                for right in sorted(edges[left] & domains[right_owner]):
                    if any(
                        not (edges[left] & edges[right] & third)
                        for owner, third in enumerate(domains)
                        if owner not in {left_owner, right_owner}
                    ):
                        edges[left].remove(right)
                        edges[right].remove(left)
                        changed = True


def selection_survives(
    selection: list[int], domains: list[set[int]], edges: list[set[int]]
) -> bool:
    return all(atom in domain for atom, domain in zip(selection, domains, strict=True)) and all(
        right in edges[left] for left, right in combinations(selection, 2)
    )


def finite_supports(
    domains: list[set[int]], edges: list[set[int]], budget: Budget, *, max_nodes: int = 10_000
) -> dict[str, Any]:
    """Find one full selection per atom; distinguish exhaustive failure from a cap."""
    deadline = min(budget.deadline, time.monotonic() + 60)
    visits = 0
    witnesses: dict[str, list[int]] = {}
    unsupported: list[int] = []

    def search(assigned: dict[int, int]) -> list[int] | None:
        nonlocal visits
        visits += 1
        if visits > max_nodes or time.monotonic() >= deadline:
            raise IncompleteError("finite support search node/time ceiling")
        if len(assigned) == len(domains):
            return [assigned[owner] for owner in range(len(domains))]
        candidates: list[tuple[int, set[int]]] = []
        for owner, domain in enumerate(domains):
            if owner not in assigned:
                values = domain.copy()
                for atom in assigned.values():
                    values.intersection_update(edges[atom])
                candidates.append((owner, values))
        owner, values = min(candidates, key=lambda item: (len(item[1]), item[0]))
        for atom in sorted(values):
            result = search({**assigned, owner: atom})
            if result is not None:
                return result
        return None

    status = "completed"
    try:
        for owner, domain in enumerate(domains):
            remaining(budget)
            for atom in sorted(domain):
                witness = search({owner: atom})
                if witness is None:
                    unsupported.append(atom)
                else:
                    witnesses[str(atom)] = witness
    except IncompleteError:
        status = "guard-refused"
    return {
        "status": status,
        "search_nodes": visits,
        "node_ceiling": max_nodes,
        "all_atoms_supported": status == "completed" and all(domains) and not unsupported,
        "unsupported_atoms": unsupported,
        "witnesses": witnesses,
        "domains": [sorted(domain) for domain in domains],
        "edges": [
            [left, right]
            for left, neighbors in enumerate(edges)
            for right in sorted(neighbors)
            if left < right
        ],
    }


def verify_complete_support_packet(packet: dict[str, Any]) -> bool:
    """Check retained finite witnesses directly, without search or propagation."""
    domains = [set(domain) for domain in packet["domains"]]
    edges = {tuple(edge) for edge in packet["edges"]}
    witnesses = packet["witnesses"]
    if not domains or not all(domains) or set(map(int, witnesses)) != set().union(*domains):
        return False
    for forced, selection in witnesses.items():
        if len(selection) != len(domains) or int(forced) not in selection:
            return False
        if any(atom not in domains[owner] for owner, atom in enumerate(selection)):
            return False
        if any(tuple(sorted(pair)) not in edges for pair in combinations(selection, 2)):
            return False
    return True


def measure(
    frame: Frame,
    document: dict[str, Any],
    mode: str,
    budget: Budget,
    *,
    endpoint: bool = False,
    support_search: bool = False,
) -> dict[str, Any]:
    grouped = atomize(frame, document, mode)
    owners = sorted(grouped)
    counts = {str(owner): len(grouped[owner]) for owner in owners}
    pairs = sum(len(grouped[a]) * len(grouped[b]) for a, b in combinations(owners, 2))
    result: dict[str, Any] = {
        "mode": mode,
        "atoms_per_owner": counts,
        "possible_pair_tests": pairs,
    }
    if len(owners) > 6 or any(count > 32 for count in counts.values()) or pairs > 15_360:
        return {
            **result,
            "status": "guard-refused",
            "reason": "six owners / 32 atoms per owner / 15360 pair ceiling",
            "pair_tests": 0,
        }
    atoms: list[Atom] = []
    domains: list[set[int]] = []
    for owner in owners:
        domains.append(set(range(len(atoms), len(atoms) + len(grouped[owner]))))
        atoms.extend(grouped[owner])
    edges: list[set[int]] = [set() for _ in atoms]
    result["cover_inventory"] = [
        {"owner": atom.owner, "row": atom.row, "pieces": list(atom.pieces)} for atom in atoms
    ]
    if mode == "two-cover":
        result["grouping_axis"] = "x"
    for left_owner, right_owner in combinations(range(len(owners)), 2):
        remaining(budget)
        for left in sorted(domains[left_owner]):
            for right in sorted(domains[right_owner]):
                if not incompatible(atoms[left], atoms[right], budget):
                    edges[left].add(right)
                    edges[right].add(left)
    selection: list[int] = []
    if endpoint:
        targets = load_endpoint(frame).by_owner()
        for domain, owner in zip(domains, owners, strict=True):
            held = endpoint_holds(targets[owner], document["final_state"]["cells"][str(owner)])
            if held is None:
                raise RefusalError("endpoint absent from input")
            selection.append(
                next(
                    index
                    for index in sorted(domain)
                    if atoms[index].row == held["row"] and held["piece"] in atoms[index].pieces
                )
            )
        require(
            selection_survives(selection, domains, edges), "endpoint lost by collision graph"
        )
    original_rows = {(atom.owner, atom.row) for atom in atoms}

    def snapshot() -> dict[str, Any]:
        live = set().union(*domains)
        surviving_rows = {(atoms[index].owner, atoms[index].row) for index in live}
        return {
            "live_atoms": len(live),
            "edges": sum(map(len, edges)) // 2,
            "removed_rows": [list(row) for row in sorted(original_rows - surviving_rows)],
            "abstract_unsat": any(not domain for domain in domains),
        }

    result["initial"] = snapshot()
    propagate(domains, edges, budget, path=False)
    result["arc"] = snapshot()
    propagate(domains, edges, budget, path=True)
    result["path"] = snapshot()
    if endpoint:
        require(selection_survives(selection, domains, edges), "endpoint lost by propagation")
        result["endpoint_selection"] = selection
        result["endpoint_preserved"] = True
    if support_search:
        result["finite_support"] = finite_supports(domains, edges, budget)
        if result["finite_support"]["all_atoms_supported"]:
            require(
                verify_complete_support_packet(result["finite_support"]),
                "finite-support packet verification failed",
            )
            result["finite_support"]["witnesses_verified"] = True
    return {**result, "status": "completed", "pair_tests": pairs}


bounded_load = partial(read_json, limit=MAX_INPUT_BYTES, compressed=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--checked-receipt", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--mode", choices=("row-hull", "pieces", "two-cover"), required=True)
    parser.add_argument("--endpoint", action="store_true")
    parser.add_argument("--support-search", action="store_true")
    args = parser.parse_args()
    started, cpu = time.monotonic(), time.process_time()
    result: dict[str, Any] = {"diagnostic_only": True, "new_exclusions": 0, "mode": args.mode}
    try:
        seed_file, node_file = saved_files(args.directory)
        seed, document = bounded_load(seed_file), bounded_load(node_file)
        receipt = json.loads(args.checked_receipt.read_text(encoding="utf-8-sig"))
        require(
            receipt["status"] == "PASS_SAVED_STALL", "requires cold saved stalled-check receipt"
        )
        require(receipt["seed_sha256"] == content_sha256(seed), "seed receipt differs")
        require(receipt["node_sha256"] == content_sha256(document), "node receipt differs")
        result.update(seed_sha256=receipt["seed_sha256"], node_sha256=receipt["node_sha256"])
        budget = Budget(started + 300, 15_360)
        remaining(budget)
        result.update(
            measure(
                n17_unique_frame(),
                document,
                args.mode,
                budget,
                endpoint=args.endpoint,
                support_search=args.support_search,
            )
        )
    except IncompleteError as error:
        result.update(status="guard-refused", reason=str(error))
    except (RefusalError, KeyError, IndexError, TypeError, ValueError, OSError) as error:
        result.update(status="refused", reason=f"{type(error).__name__}: {error}")
    result.update(
        wall_seconds=time.monotonic() - started,
        cpu_seconds=time.process_time() - cpu,
        worker_peak_bytes=peak_memory_bytes(),
    )
    write_json(args.output, result)
    print(
        json.dumps(
            {
                key: value
                for key, value in result.items()
                if key not in {"cover_inventory", "finite_support"}
            }
        )
    )
    return 0 if result["status"] in {"completed", "guard-refused"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
