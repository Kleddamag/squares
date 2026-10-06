"""Exact cached collision adapter and one frozen mixed-query cost profile.

The corpus contains known B-compatible and J-incompatible directed child pairs.
First-use means one initially empty cache over the whole corpus, including setup.
No search, geometry change, producer mutation or search-speedup claim is made.
"""

from __future__ import annotations

import argparse
import json
import time
from collections.abc import Callable
from dataclasses import dataclass
from functools import partial
from itertools import combinations
from pathlib import Path
from typing import Any

from devtools import probe_n17_enhanced_row_support as enhanced
from devtools.bounded_diagnostics import (
    MAX_MEMORY_BYTES,
    check_budget,
    retained_matches,
    same_header,
    same_inputs,
)
from devtools.check_hull_kernel_mask0 import n17_unique_frame
from devtools.probe_n17_raw_row_support import (
    atom_reference,
    bounded_json,
    checked_inputs,
    raw_atoms,
    seed_selections,
)
from devtools.probe_n17_residual_graph import Atom, incompatible
from devtools.process_memory import peak_memory_bytes
from sqpack.hull_kernel import collision
from sqpack.hull_kernel.geometry import Budget, IncompleteError, RefusalError, require

SCHEMA = "n17.cached-collision-profile.v1"
BASE_REVISION = "1b53404772cb2bc3aae27888d154cfb86500ca12"
B_PATH = (
    "packing/campaign/explorations/X048-session-176-owner-priority/"
    "receipts/B-support-packet.json"
)
J_PATH = (
    "packing/campaign/explorations/X048-session-177-cached-collision/"
    "receipts/J-fixed-tuple-certificate.json"
)
ARTIFACT_PROVENANCE = {
    "historical_revision": BASE_REVISION,
    "committed_paths": {"B_PATH": B_PATH, "J_PATH": J_PATH},
}
MAX_QUERIES = 958
MAX_CALLS = 4096
WALL_SECONDS = 30
PASSES = ("rational", "integer", "cached_first", "cached_warm")
EXPECTED_B_SELECTIONS = 44
EXPECTED_J_TUPLES = 72
EXPECTED_J_WITNESSES = 298
type Predicate = Callable[[Atom, Atom, Budget], bool]


remaining = partial(check_budget, wall_message="cached collision profile wall ceiling")


@dataclass
class Guard:
    budget: Budget
    max_calls: int = MAX_CALLS
    calls: int = 0

    def check_pair(self, predicate: Predicate, left: Atom, right: Atom) -> bool:
        remaining(self.budget)
        require(left.owner < right.owner, "noncanonical directed pair")
        if self.calls >= self.max_calls:
            raise IncompleteError("collision primitive call ceiling")
        self.calls += 1
        answer = predicate(left, right, self.budget)
        remaining(self.budget)
        require(type(answer) is bool, "predicate result must be exact bool")
        return answer


def integer_incompatible(left: Atom, right: Atom, budget: Budget) -> bool:
    require(bool(left.domain) and bool(right.domain), "empty atom")
    try:
        collision.integer_universal_collision(
            left.core, left.domain, [(right.domain, right.core)], left.domain, budget=budget
        )
    except RefusalError as error:
        if str(error) != "region escapes universal collision set":
            raise
        return False
    return True


class CachedPredicate:
    """One inventory's exact facet/domain-minimum caches; mutation refuses."""

    def __init__(self, atoms: list[Atom], budget: Budget) -> None:
        remaining(budget)
        self.originals = tuple(atoms)
        self.indices = {id(atom): index for index, atom in enumerate(atoms)}
        require(len(self.indices) == len(atoms), "duplicate atom object")
        self.snapshots = [
            Atom(a.owner, a.row, a.pieces, list(a.domain), list(a.core)) for a in atoms
        ]
        self.prepared: list[list[collision.PreparedRow]] = []
        self.facets: collision.FacetCache = {}
        for atom in self.snapshots:
            remaining(budget)
            self.prepared.append(collision.prepare_rows([(atom.domain, atom.core)]))
        remaining(budget)

    def bound(self, atom: Atom) -> int:
        index = self.indices.get(id(atom))
        require(index is not None, "atom does not belong to cache inventory")
        assert index is not None
        old = self.snapshots[index]
        require(
            self.originals[index] is atom
            and (atom.owner, atom.row, atom.pieces) == (old.owner, old.row, old.pieces)
            and atom.domain == old.domain
            and atom.core == old.core,
            "cache inventory atom was mutated",
        )
        return index

    def __call__(self, left: Atom, right: Atom, budget: Budget) -> bool:
        remaining(budget)
        require(left.owner < right.owner, "noncanonical directed pair")
        li, ri = self.bound(left), self.bound(right)
        query = self.snapshots[li]
        try:
            collision.cached_universal_collision(
                query.core,
                query.domain,
                self.prepared[ri],
                query.domain,
                budget=budget,
                facets=self.facets,
            )
        except RefusalError as error:
            if str(error) != "region escapes universal collision set":
                raise
            answer = False
        else:
            answer = True
        remaining(budget)
        return answer

    def sizes(self) -> dict[str, int]:
        return {
            "prepared_atoms": len(self.prepared),
            "facet_entries": len(self.facets),
            "minimum_entries": sum(
                len(row.minima) for family in self.prepared for row in family
            ),
        }


@dataclass(frozen=True)
class Query:
    left: int
    right: int
    expected: bool


def corpus(
    support: dict[str, Any],
    certificate: dict[str, Any],
    source: dict[str, Any],
    refinement: dict[str, Any],
    baseline: dict[str, Any],
    *,
    inv: enhanced.Inventory,
    document: dict[str, Any],
    identity: dict[str, Any],
) -> list[Query]:
    del refinement, baseline  # Provenance is informational; exact refs bind the corpus.
    require(
        retained_matches(support, BASE_REVISION, B_PATH)
        and retained_matches(certificate, BASE_REVISION, J_PATH),
        "frozen B/J differs",
    )
    for value in (support, certificate):
        require(
            value["model"] == enhanced.MODEL and value["predicate"] == enhanced.PREDICATE,
            "corpus model differs",
        )
        require(
            value["diagnostic_only"] is True and value["new_exclusions"] == 0,
            "corpus exclusion claim",
        )
        require(
            same_inputs(value["input_identity"], identity),
            "corpus input/H differs",
        )
    require(
        support["schema"] == "n17.scheduled-enhanced-parent-row-support.v1",
        "B grammar/inventory differs",
    )
    require(
        certificate["row_unsupportedness_verified"] is False
        and certificate["certified_fixed_tuples"] == EXPECTED_J_TUPLES,
        "J scope/count differs",
    )
    require(
        len(support["selections"]) == EXPECTED_B_SELECTIONS
        and len(certificate["tuple_certificates"]) == EXPECTED_J_TUPLES,
        "corpus inventory differs",
    )
    expected: dict[tuple[int, int], bool] = {}

    def add(left: int, right: int, *, result: bool) -> None:
        require(
            inv.atoms[left].owner < inv.atoms[right].owner, "corpus owner direction differs"
        )
        key = left, right
        require(
            key not in expected or expected[key] is result, "corpus expected classes conflict"
        )
        expected[key] = result

    for selection in support["selections"]:
        for left, right in combinations(enhanced.selection_indices(selection, inv), 2):
            add(left, right, result=False)
    originals = seed_selections(source, inv.raw, document, identity)
    witness_count, seen = 0, set()
    for item in certificate["tuple_certificates"]:
        index = item["source_selection_index"]
        require(
            type(index) is int and 0 <= index < len(originals) and index not in seen,
            "J source selection differs",
        )
        seen.add(index)
        selection = originals[index]
        require(len(item["atoms"]) == len(selection) == 6, "J owner inventory differs")
        for raw_index, ref in zip(selection, item["atoms"], strict=True):
            require(
                ref["original"] == atom_reference(inv.raw[raw_index], document),
                "J original ref differs",
            )
            children = [
                {
                    "half": half,
                    "interval": inv.references[2 * raw_index + half]["child_interval"],
                    "core_sha256": inv.references[2 * raw_index + half]["child_core_sha256"],
                }
                for half in (0, 1)
            ]
            require(ref["children"] == children, "J child ref differs")
        for edge in item["incompatible_pairs"]:
            i, j, lh, rh = (
                edge[key]
                for key in ("left_position", "right_position", "left_half", "right_half")
            )
            require(
                all(type(v) is int for v in (i, j, lh, rh))
                and 0 <= i < j < 6
                and lh in (0, 1)
                and rh in (0, 1),
                "J pair pattern differs",
            )
            add(2 * selection[i] + lh, 2 * selection[j] + rh, result=True)
            witness_count += 1
    require(
        witness_count == EXPECTED_J_WITNESSES and 0 < len(expected) <= MAX_QUERIES,
        "mixed corpus ceiling/count differs",
    )
    require(set(expected.values()) == {False, True}, "both expected classes required")
    return [Query(left, right, expected[left, right]) for left, right in sorted(expected)]


def header(
    inv: enhanced.Inventory,
    queries: list[Query],
    support: dict[str, Any],
    certificate: dict[str, Any],
    identity: dict[str, Any],
    *,
    refinement: dict[str, Any],
    source: dict[str, Any],
    baseline: dict[str, Any],
) -> dict[str, Any]:
    del (
        support,
        certificate,
        refinement,
        source,
        baseline,
    )  # Preserve the public helper signature.
    return {
        "schema": SCHEMA,
        "artifact_provenance": ARTIFACT_PROVENANCE,
        "diagnostic_only": True,
        "new_exclusions": 0,
        "unsupported_rows_verified": False,
        "baseline_repository_revision": BASE_REVISION,
        "model": enhanced.MODEL,
        "predicate": enhanced.PREDICATE,
        "input_identity": identity,
        "raw_atoms": len(inv.raw),
        "child_atoms": len(inv.atoms),
        "query_count": len(queries),
        "expected_compatible_pairs": sum(not q.expected for q in queries),
        "expected_collision_pairs": sum(q.expected for q in queries),
        "queries": [
            {
                "left": inv.references[q.left],
                "right": inv.references[q.right],
                "expected_incompatible": q.expected,
            }
            for q in queries
        ],
        "query_order": "ascending-derived-atom-index-pair; sorted-owner direction",
        "limits": {
            "unique_queries": MAX_QUERIES,
            "primitive_calls": MAX_CALLS,
            "wall_seconds": WALL_SECONDS,
            "peak_bytes": MAX_MEMORY_BYTES,
        },
        "cold_scope": "initially-empty cache over whole corpus; not per-query",
        "search_speedup_measured": False,
    }


def profile(
    inv: enhanced.Inventory,
    queries: list[Query],
    guard: Guard,
    result: dict[str, Any],
    checkpoint: Callable[[dict[str, Any]], None] | None = None,
) -> None:
    require(
        0 < len(queries) <= MAX_QUERIES and 4 * len(queries) <= guard.max_calls,
        "profile corpus/call ceiling",
    )
    result["answers"], result["timings"] = {}, {}
    expected = [q.expected for q in queries]

    def run(name: str, predicate: Predicate) -> None:
        started = time.monotonic()
        answers: list[bool] = []
        result["answers"][name] = answers
        for q in queries:
            answer = guard.check_pair(predicate, inv.atoms[q.left], inv.atoms[q.right])
            require(answer is q.expected, f"{name} differs from expected class")
            answers.append(answer)
        result["timings"][name + "_seconds"] = time.monotonic() - started
        result["primitive_calls"] = guard.calls
        if checkpoint:
            checkpoint(result)

    run("rational", incompatible)
    run("integer", integer_incompatible)
    started = time.monotonic()
    cached = CachedPredicate(inv.atoms, guard.budget)
    result["timings"]["cached_setup_seconds"] = time.monotonic() - started
    run("cached_first", cached)
    result["cache_after_first"] = cached.sizes()
    run("cached_warm", cached)
    result["cache_after_warm"] = cached.sizes()
    require(all(result["answers"][name] == expected for name in PASSES), "four arrays disagree")
    timings = result["timings"]
    total = timings["cached_setup_seconds"] + timings["cached_first_seconds"]
    saving = timings["rational_seconds"] - total
    timings.update(
        cached_first_use_seconds=total,
        first_use_saving_seconds=saving,
        first_use_ratio=total / timings["rational_seconds"]
        if timings["rational_seconds"]
        else None,
    )
    remaining(guard.budget)
    result.update(
        status="PASS_EQUIVALENT_MIXED_CORPUS",
        next_matched_search_prerequisite=total <= 0.8 * timings["rational_seconds"]
        and saving >= 0.1,
        next_matched_search_threshold={
            "max_first_use_ratio": 0.8,
            "minimum_saving_seconds": 0.1,
        },
        interpretation=(
            "Single fixed-corpus descriptive result; no search speedup "
            "or automatic search authorization"
        ),
    )


def replay(
    value: dict[str, Any],
    inv: enhanced.Inventory,
    queries: list[Query],
    common: dict[str, Any],
    guard: Guard,
) -> dict[str, Any]:
    require(
        same_header(value, common),
        "profile input/query binding differs",
    )
    require(value["status"] == "PASS_EQUIVALENT_MIXED_CORPUS", "profile not complete")
    if "queries" in common:
        require(
            all(type(item["expected_incompatible"]) is bool for item in value["queries"]),
            "query expected class must be exact bool",
        )
    expected = [q.expected for q in queries]
    require(
        set(value["answers"]) == set(PASSES)
        and all(
            isinstance(value["answers"][name], list)
            and len(value["answers"][name]) == len(queries)
            and all(type(answer) is bool for answer in value["answers"][name])
            and value["answers"][name] == expected
            for name in PASSES
        ),
        "profile answer arrays differ",
    )
    actual = [
        guard.check_pair(incompatible, inv.atoms[q.left], inv.atoms[q.right]) for q in queries
    ]
    require(actual == expected, "fresh rational replay disagrees")
    return {
        "status": "PASS_FRESH_MIXED_CORPUS",
        "packet_content_verified": True,
        "fresh_pair_checks": guard.calls,
        "query_count": len(queries),
        "performance_statistics_verified": False,
        "cached_profile_implementation_executed": False,
        "input_identity": common["input_identity"],
        "diagnostic_only": True,
        "new_exclusions": 0,
        "unsupported_rows_verified": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    for name in (
        "checked-receipt",
        "source-packet",
        "baseline-replay",
        "refinement-packet",
        "support-packet",
        "conflict-certificate",
        "output",
    ):
        parser.add_argument(f"--{name}", type=Path, required=True)
    parser.add_argument("--verify", type=Path)
    args = parser.parse_args()
    started, cpu = time.monotonic(), time.process_time()
    guard = Guard(Budget(started + WALL_SECONDS, 100000))
    result: dict[str, Any] = {
        "diagnostic_only": True,
        "new_exclusions": 0,
        "unsupported_rows_verified": False,
        "status": "RUNNING",
    }
    try:
        document, identity = checked_inputs(args.directory, args.checked_receipt)
        frame = n17_unique_frame()
        inv = enhanced.build_inventory(
            frame, raw_atoms(frame, document), document, guard.budget
        )
        refinement = bounded_json(args.refinement_packet)
        enhanced.fixture_inventory(inv, refinement, endpoint=False)
        source, baseline = bounded_json(args.source_packet), bounded_json(args.baseline_replay)
        support, certificate = (
            bounded_json(args.support_packet),
            bounded_json(args.conflict_certificate),
        )
        queries = corpus(
            support,
            certificate,
            source,
            refinement,
            baseline,
            inv=inv,
            document=document,
            identity=identity,
        )
        common = header(
            inv,
            queries,
            support,
            certificate,
            identity,
            refinement=refinement,
            source=source,
            baseline=baseline,
        )
        remaining(guard.budget)
        geometry_seconds = time.monotonic() - started
        if args.verify:
            result.update(replay(bounded_json(args.verify), inv, queries, common, guard))
        else:
            result.update(common, geometry_build_seconds=geometry_seconds)
            profile(
                inv,
                queries,
                guard,
                result,
                lambda value: enhanced.safe_write(
                    args.output.with_suffix(".partial.json"), value
                ),
            )
    except (IncompleteError, RefusalError) as error:
        result.update(
            status="INCOMPLETE" if isinstance(error, IncompleteError) else "REFUSED",
            reason=str(error),
        )
    result.update(
        wall_seconds=time.monotonic() - started,
        cpu_seconds=time.process_time() - cpu,
        primitive_calls=guard.calls,
        worker_peak_bytes=peak_memory_bytes(),
    )
    enhanced.safe_write(args.output, result)
    print(
        json.dumps(
            {key: result[key] for key in ("status", "wall_seconds", "worker_peak_bytes")}
        ),
        flush=True,
    )
    raise SystemExit(0 if result["status"] not in {"REFUSED", "INCOMPLETE"} else 2)


if __name__ == "__main__":
    main()
