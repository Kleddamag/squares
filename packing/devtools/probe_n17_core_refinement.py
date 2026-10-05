"""One fixed-witness half-interval/octagon augmentation; diagnostic support only.

Center domains never change. Surviving selections are solutions of this exact binary
abstraction, not common realizable poses. Loss of known support is always unknown.
"""

from __future__ import annotations

import argparse
import json
import time
from collections.abc import Callable
from dataclasses import dataclass
from functools import partial
from itertools import combinations, product
from pathlib import Path
from typing import Any

from devtools.bounded_diagnostics import (
    MAX_MEMORY_BYTES,
    check_budget,
    same_inputs,
)
from devtools.check_hull_kernel_mask0 import n17_unique_frame
from devtools.check_n17_subpattern import content_sha256
from devtools.pilot_n17_capture import in_convex, load_endpoint
from devtools.probe_n17_raw_row_support import (
    PREDICATE,
    atom_reference,
    bounded_json,
    checked_inputs,
    endpoint_selection,
    raw_atoms,
    seed_selections,
    write_json,
)
from devtools.probe_n17_residual_graph import Atom, incompatible
from devtools.process_memory import peak_memory_bytes
from sqpack.hull_kernel.frame import Frame
from sqpack.hull_kernel.geometry import (
    Budget,
    IncompleteError,
    Polygon,
    RefusalError,
    area2,
    require,
)
from sqpack.hull_kernel.induction import encode, hull, strict_core
from sqpack.hull_kernel.producer import octagon_core
from sqpack.hull_kernel.rational import Q

SCHEMA = "n17.fixed-witness-core-refinement.v1"
MODEL = "half-chart-octagon-hull-old-core-frozen-domain-v1"
MAX_SELECTIONS = 79
MAX_PAIRS = 4740
MAX_ASSIGNMENTS = 5056
WALL_SECONDS = 30
type RowKey = tuple[int, int]
type ChildKey = tuple[int, int]
type Predicate = Callable[[Atom, Atom, Budget], bool]


remaining = partial(check_budget, wall_message="core refinement wall ceiling")


def halves(lo: Q, hi: Q) -> tuple[tuple[Q, Q], tuple[Q, Q]]:
    require(lo < hi, "requires nondegenerate ordered chart interval")
    mid = (lo + hi) / 2
    return (lo, mid), (mid, hi)


def augmented_core(frame: Frame, old: Polygon, interval: tuple[Q, Q]) -> Polygon:
    core = hull(old + octagon_core(frame, *interval))
    strict_core(frame, core, *interval)
    require(all(in_convex(core, point) for point in old), "old core not contained")
    require(area2(core) >= area2(old), "core area decreased")
    return core


def bound_source(
    source: dict[str, Any],
    baseline: dict[str, Any],
    atoms: list[Atom],
    document: dict[str, Any],
    identity: dict[str, Any],
) -> list[list[int]]:
    require(source["status"] == "ALL_ROWS_SUPPORTED", "requires complete E source packet")
    selections = seed_selections(source, atoms, document, identity)
    require(0 < len(selections) <= MAX_SELECTIONS, "source selection ceiling")
    rows = {(atom.owner, atom.row) for atom in atoms}
    covered = {(atoms[i].owner, atoms[i].row) for selection in selections for i in selection}
    require(covered == rows, "source selections omit parent rows")
    owners = len({atom.owner for atom in atoms})
    require(
        baseline["status"] == "PASS_REPLAYED_ALL_ROWS"
        and baseline["diagnostic_only"] is True
        and baseline["new_exclusions"] == 0
        and baseline["all_rows_supported"] is True,
        "baseline replay status differs",
    )
    require(
        same_inputs(baseline["input_identity"], identity), "baseline input identity differs"
    )
    require(
        baseline["live_rows"] == baseline["supported_rows"] == len(rows)
        and baseline["selections_checked"] == len(selections)
        and baseline["fresh_pair_checks"] == len(selections) * owners * (owners - 1) // 2,
        "baseline inventory differs",
    )
    return selections


@dataclass
class Child:
    parent: int
    half: int
    interval: tuple[Q, Q]
    atom: Atom


def children(
    frame: Frame,
    atoms: list[Atom],
    selections: list[list[int]],
    document: dict[str, Any],
    budget: Budget,
) -> tuple[dict[ChildKey, Child], list[dict[str, Any]]]:
    cores: dict[RowKey, tuple[Polygon, tuple[tuple[Q, Q], tuple[Q, Q]], list[Polygon]]] = {}
    result = {}
    growth = []
    for index in sorted({i for selection in selections for i in selection}):
        remaining(budget)
        atom = atoms[index]
        row_key = atom.owner, atom.row
        row = document["final_state"]["cells"][str(atom.owner)][atom.row]
        intervals = halves(*(Q(value) for value in row["interval"]))
        if row_key not in cores:
            enhanced = []
            for half, interval in enumerate(intervals):
                remaining(budget)
                core = augmented_core(frame, atom.core, interval)
                enhanced.append(core)
                growth.append(
                    {
                        "owner": atom.owner,
                        "row": atom.row,
                        "half": half,
                        "area_gain2": str(area2(core) - area2(atom.core)),
                    }
                )
            cores[row_key] = atom.core, intervals, enhanced
        old, recorded_intervals, enhanced = cores[row_key]
        require(old == atom.core and recorded_intervals == intervals, "row core differs")
        for half, interval in enumerate(intervals):
            result[index, half] = Child(
                index,
                half,
                interval,
                Atom(atom.owner, atom.row, atom.pieces, atom.domain, enhanced[half]),
            )
    return result, growth


def child_reference(
    child: Child, atoms: list[Atom], document: dict[str, Any]
) -> dict[str, Any]:
    return {
        **atom_reference(atoms[child.parent], document),
        "half": child.half,
        "child_interval": [str(value) for value in child.interval],
        "child_core_sha256": content_sha256(encode(child.atom.core)),
    }


def endpoint_choices(
    frame: Frame,
    atoms: list[Atom],
    selections: list[list[int]],
    document: dict[str, Any],
    refined: dict[ChildKey, Child],
) -> tuple[int, ...]:
    require(
        selections[0] == endpoint_selection(frame, document, atoms), "endpoint source differs"
    )
    targets = load_endpoint(frame).by_owner()
    choices = []
    for index in selections[0]:
        target = targets[atoms[index].owner]
        matching = [
            half
            for half in (0, 1)
            if any(
                refined[index, half].interval[0] <= low
                and high <= refined[index, half].interval[1]
                for low, high in target.charts
            )
        ]
        require(bool(matching), "endpoint enclosure crosses child split")
        choices.append(matching[0])
    return tuple(choices)


class Refiner:
    def __init__(
        self,
        selections: list[list[int]],
        refined: dict[ChildKey, Child],
        budget: Budget,
        *,
        predicate: Predicate = incompatible,
        max_pairs: int = MAX_PAIRS,
        max_assignments: int = MAX_ASSIGNMENTS,
    ):
        self.source = selections
        self.refined = refined
        self.budget = budget
        self.predicate = predicate
        self.max_pairs = max_pairs
        self.max_assignments = max_assignments
        self.cache: dict[tuple[ChildKey, ChildKey], bool] = {}
        self.pair_tests = 0
        self.assignments = 0
        self.completed = 0
        self.kept: list[tuple[int, tuple[int, ...]]] = []
        self.lost: list[int] = []

    def compatible(self, a: ChildKey, b: ChildKey) -> bool:
        remaining(self.budget)
        if self.refined[a].atom.owner > self.refined[b].atom.owner:
            a, b = b, a
        require(self.refined[a].atom.owner < self.refined[b].atom.owner, "same owner pair")
        key = a, b
        if key not in self.cache:
            if self.pair_tests >= self.max_pairs:
                raise IncompleteError("refined unique pair ceiling")
            self.pair_tests += 1
            compatible = not self.predicate(
                self.refined[a].atom, self.refined[b].atom, self.budget
            )
            remaining(self.budget)
            self.cache[key] = compatible
        return self.cache[key]

    def holds(self, selection: list[int], choices: tuple[int, ...]) -> bool:
        remaining(self.budget)
        if self.assignments >= self.max_assignments:
            raise IncompleteError("child assignment ceiling")
        self.assignments += 1
        keys = list(zip(selection, choices, strict=True))
        return all(self.compatible(a, b) for a, b in combinations(keys, 2))

    def run(
        self,
        *,
        endpoint: tuple[int, ...] | None = None,
        checkpoint: Callable[[], None] | None = None,
    ) -> tuple[str, str | None]:
        try:
            for source_index, selection in enumerate(self.source):
                if source_index == 0 and endpoint is not None:
                    require(
                        self.holds(selection, endpoint), "endpoint child selection collides"
                    )
                    found = endpoint
                else:
                    found = next(
                        (
                            choice
                            for choice in product((0, 1), repeat=len(selection))
                            if self.holds(selection, choice)
                        ),
                        None,
                    )
                if found is None:
                    self.lost.append(source_index)
                else:
                    self.kept.append((source_index, found))
                self.completed += 1
                if checkpoint:
                    checkpoint()
        except IncompleteError as error:
            return "INCOMPLETE", str(error)
        return "COMPLETE", None


def coverage(selections: list[dict[str, Any]]) -> tuple[list[list[int]], list[list[int]]]:
    parent = {(ref["owner"], ref["row"]) for item in selections for ref in item["atoms"]}
    child = {
        (ref["owner"], ref["row"], ref["half"]) for item in selections for ref in item["atoms"]
    }
    return [list(row) for row in sorted(parent)], [list(row) for row in sorted(child)]


def packet(
    search: Refiner,
    atoms: list[Atom],
    document: dict[str, Any],
    identity: dict[str, Any],
    source: dict[str, Any],
    *,
    baseline: dict[str, Any],
    growth: list[dict[str, Any]],
    status: str,
    reason: str | None,
    endpoint: tuple[int, ...] | None,
) -> dict[str, Any]:
    del source, baseline  # Retain the established public helper signature.
    selections = [
        {
            "source_selection_index": i,
            "atoms": [
                child_reference(search.refined[index, half], atoms, document)
                for index, half in zip(search.source[i], choices, strict=True)
            ],
        }
        for i, choices in search.kept
    ]
    parents, child_rows = coverage(selections)
    rows = {(atom.owner, atom.row) for atom in atoms}
    if status == "COMPLETE":
        status = (
            "ALL_PARENT_ROWS_SUPPORTED" if len(parents) == len(rows) else "LOST_KNOWN_SUPPORT"
        )
    return {
        "schema": SCHEMA,
        "model": MODEL,
        "predicate": PREDICATE,
        "diagnostic_only": True,
        "new_exclusions": 0,
        "status": status,
        "reason": reason,
        "input_identity": identity,
        "raw_atoms": len(atoms),
        "live_parent_rows": len(rows),
        "source_selections": len(search.source),
        "source_selections_completed": search.completed,
        "unique_pair_tests": search.pair_tests,
        "cache_entries": len(search.cache),
        "assignments": search.assignments,
        "limits": {
            "unique_pairs": MAX_PAIRS,
            "assignments": MAX_ASSIGNMENTS,
            "wall_seconds": WALL_SECONDS,
            "peak_bytes": MAX_MEMORY_BYTES,
        },
        "enhanced_selections": selections,
        "supported_parent_rows": parents,
        "observed_supported_child_rows": child_rows,
        "child_coverage_is_lower_bound": True,
        "unknown_parent_rows": [
            list(row) for row in sorted(rows - {tuple(row) for row in parents})
        ],
        "lost_source_selection_indices": search.lost,
        "core_growth": growth,
        "endpoint_choices": list(endpoint) if endpoint is not None else None,
    }


def verify_packet(
    value: dict[str, Any],
    atoms: list[Atom],
    document: dict[str, Any],
    identity: dict[str, Any],
    source: dict[str, Any],
    *,
    baseline: dict[str, Any],
    selections: list[list[int]],
    refined: dict[ChildKey, Child],
    growth: list[dict[str, Any]],
    budget: Budget,
    frame: Frame,
) -> dict[str, Any]:
    del source, baseline  # Retain the established public helper signature.
    require(
        value["schema"] == SCHEMA
        and value["model"] == MODEL
        and value["predicate"] == PREDICATE,
        "packet grammar differs",
    )
    require(
        value["status"]
        in {"ALL_PARENT_ROWS_SUPPORTED", "LOST_KNOWN_SUPPORT", "INCOMPLETE", "NO_CORE_GROWTH"},
        "packet status differs",
    )
    require(
        value["diagnostic_only"] is True and value["new_exclusions"] == 0,
        "packet claims exclusion",
    )
    require(same_inputs(value["input_identity"], identity), "input identity differs")
    rows = {(a.owner, a.row) for a in atoms}
    require(
        value["raw_atoms"] == len(atoms)
        and value["live_parent_rows"] == len(rows)
        and value["source_selections"] == len(selections),
        "inventory differs",
    )
    require(value["core_growth"] == growth, "core growth differs")
    held = value["enhanced_selections"]
    require(
        isinstance(held, list) and len(held) <= MAX_SELECTIONS, "retained selection ceiling"
    )
    seen = set()
    checks = 0
    for item in held:
        i = item["source_selection_index"]
        require(
            type(i) is int and 0 <= i < len(selections) and i not in seen,
            "source index differs",
        )
        seen.add(i)
        references = item["atoms"]
        require(len(references) == len(selections[i]), "owner inventory differs")
        chosen = []
        for index, reference in zip(selections[i], references, strict=True):
            half = reference["half"]
            require(type(half) is int and half in (0, 1), "invalid child half")
            child = refined[index, half]
            require(
                reference == child_reference(child, atoms, document), "child provenance differs"
            )
            chosen.append(child)
        for left, right in combinations(chosen, 2):
            remaining(budget)
            require(left.atom.owner < right.atom.owner, "owner direction differs")
            require(checks < MAX_PAIRS, "replay pair ceiling")
            require(
                not incompatible(left.atom, right.atom, budget),
                "refined selection contains collision",
            )
            remaining(budget)
            checks += 1
    parents, child_rows = coverage(held)
    require(
        value["supported_parent_rows"] == parents
        and value["observed_supported_child_rows"] == child_rows,
        "coverage differs",
    )
    require(
        value["unknown_parent_rows"]
        == [list(row) for row in sorted(rows - {tuple(row) for row in parents})],
        "unknown rows differ",
    )
    require(value["child_coverage_is_lower_bound"] is True, "child coverage claim differs")
    if value["status"] == "ALL_PARENT_ROWS_SUPPORTED":
        require(len(parents) == len(rows), "all-parent-row claim omits rows")
    endpoint = value["endpoint_choices"]
    if endpoint is not None:
        expected = endpoint_choices(frame, atoms, selections, document, refined)
        require(endpoint == list(expected), "endpoint choices differ")
        require(
            bool(held) and held[0]["source_selection_index"] == 0, "endpoint selection absent"
        )
        require([ref["half"] for ref in held[0]["atoms"]] == endpoint, "endpoint halves differ")
    return {
        "status": "PASS_REPLAYED_ALL_PARENT_ROWS"
        if len(parents) == len(rows)
        else "PASS_REPLAYED_PARTIAL_SUPPORT",
        "supported_parent_rows": len(parents),
        "live_parent_rows": len(rows),
        "observed_supported_child_rows": len(child_rows),
        "selections_checked": len(held),
        "fresh_pair_checks": checks,
        "packet_content_verified": True,
        "input_identity": identity,
        "endpoint_angle_children_replayed": endpoint is not None,
        "unsupported_rows_verified": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--checked-receipt", type=Path, required=True)
    parser.add_argument("--source-packet", type=Path, required=True)
    parser.add_argument("--baseline-replay", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--verify", type=Path)
    parser.add_argument("--endpoint", action="store_true")
    args = parser.parse_args()
    started, cpu = time.monotonic(), time.process_time()
    budget = Budget(started + WALL_SECONDS, MAX_ASSIGNMENTS)
    result: dict[str, Any] = {"diagnostic_only": True, "new_exclusions": 0}
    try:
        document, identity = checked_inputs(args.directory, args.checked_receipt)
        frame = n17_unique_frame()
        atoms = raw_atoms(frame, document)
        source, baseline = bounded_json(args.source_packet), bounded_json(args.baseline_replay)
        selections = bound_source(source, baseline, atoms, document, identity)
        refined, growth = children(frame, atoms, selections, document, budget)
        remaining(budget)
        if args.verify:
            result.update(
                verify_packet(
                    bounded_json(args.verify),
                    atoms,
                    document,
                    identity,
                    source,
                    baseline=baseline,
                    selections=selections,
                    refined=refined,
                    growth=growth,
                    budget=budget,
                    frame=frame,
                )
            )
        else:
            search = Refiner(selections, refined, budget)
            endpoint = (
                endpoint_choices(frame, atoms, selections, document, refined)
                if args.endpoint
                else None
            )

            def checkpoint() -> None:
                write_json(
                    args.output.with_suffix(".partial.json"),
                    packet(
                        search,
                        atoms,
                        document,
                        identity,
                        source,
                        baseline=baseline,
                        growth=growth,
                        status="INCOMPLETE",
                        reason="progress checkpoint",
                        endpoint=endpoint,
                    ),
                )

            if not any(Q(item["area_gain2"]) > 0 for item in growth):
                status, reason = "NO_CORE_GROWTH", "no exact positive area gain"
            else:
                status, reason = search.run(endpoint=endpoint, checkpoint=checkpoint)
            result.update(
                packet(
                    search,
                    atoms,
                    document,
                    identity,
                    source,
                    baseline=baseline,
                    growth=growth,
                    status=status,
                    reason=reason,
                    endpoint=endpoint,
                )
            )
    except IncompleteError as error:
        result.update(status="INCOMPLETE", reason=str(error))
    except (RefusalError, KeyError, IndexError, TypeError, ValueError, OSError) as error:
        result.update(status="REFUSED", reason=f"{type(error).__name__}: {error}")
    result.update(
        wall_seconds=time.monotonic() - started,
        cpu_seconds=time.process_time() - cpu,
        worker_peak_bytes=peak_memory_bytes(),
    )
    write_json(args.output, result)
    print(
        json.dumps(
            {
                key: item
                for key, item in result.items()
                if key
                not in {
                    "enhanced_selections",
                    "core_growth",
                    "supported_parent_rows",
                    "observed_supported_child_rows",
                    "unknown_parent_rows",
                }
            }
        )
    )
    return 2 if result["status"] == "REFUSED" else 0


if __name__ == "__main__":
    raise SystemExit(main())
