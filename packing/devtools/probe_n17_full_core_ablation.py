"""Separate full-interval augmentation from halving on frozen E witness tuples.

This fixed-sample diagnostic does not search for replacement supports. Tuple losses
are not parent-row unsupportedness. The complete binary networks are not compared.
"""

from __future__ import annotations

import argparse
import json
import time
from collections.abc import Callable
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import Any

from devtools.check_hull_kernel_mask0 import n17_unique_frame
from devtools.check_n17_subpattern import content_sha256
from devtools.pilot_n17_capture import in_convex
from devtools.probe_n17_core_refinement import (
    MODEL as HALF_MODEL,
)
from devtools.probe_n17_core_refinement import (
    augmented_core,
    bound_source,
    child_reference,
    children,
)
from devtools.probe_n17_enhanced_row_support import safe_write
from devtools.probe_n17_raw_row_support import (
    PREDICATE,
    atom_reference,
    bounded_json,
    checked_inputs,
    raw_atoms,
)
from devtools.probe_n17_residual_graph import Atom, incompatible
from devtools.profile_n17_partner_memo import peak_memory_bytes
from sqpack.hull_kernel.frame import Frame
from sqpack.hull_kernel.geometry import (
    Budget,
    IncompleteError,
    Polygon,
    RefusalError,
    area2,
    require,
)
from sqpack.hull_kernel.induction import encode, strict_core
from sqpack.hull_kernel.rational import Q

SCHEMA = "n17.fixed-witness-full-core-ablation.v1"
MODEL = "full-chart-octagon-hull-old-core-frozen-domain-v1"
BASE_REVISION = "9a8b4ef75fbb880ec207d2a9769d2a518c10fb14"
MAX_PAIRS = 1185
MAX_PEAK_BYTES = 512 * 1024**2
WALL_SECONDS = 45
FROZEN = {
    False: (
        "39df9dca3cfa95544d8cc5297f70fc37b34221d5d3078b50b2f274502c978e6c",
        "e838cc4fb065c4894a577eaf35a7bd7bcec0bc89dd8776dd14f3375271d46d2a",
        "611c52644ed22fb9d704dbd56ec24e91e15002185a33e1b0866b17d9d1114395",
        "1313c67109a450f5fdfaa56d3285595b6e81e04f0708f756303db1ccb6145d35",
    ),
    True: (
        "9a38b7d6f18a57ee927196f711a03a7daf75b730288cfb3db47ed8d24a87eecb",
        "94ed69295b9665fe9346d4809976c67a59f8c37f9f3324e12ca589a9481d5be9",
        "9342f65ea06942cbbed51a150558ccfc8ee4b6c5a120d733502fe6567560bcaf",
        None,
    ),
}
type Parent = tuple[int, int]
type Predicate = Callable[[Atom, Atom, Budget], bool]


def remaining(budget: Budget) -> None:
    if time.monotonic() >= budget.deadline:
        raise IncompleteError("full-core ablation wall ceiling")
    if peak_memory_bytes() > MAX_PEAK_BYTES:
        raise IncompleteError("actual worker peak exceeds512MiB")


@dataclass
class Context:
    frame: Frame
    raw: list[Atom]
    document: dict[str, Any]
    selections: list[list[int]]
    h_survivors: set[int]
    h_lost: set[int]
    header: dict[str, Any]


def bind(
    frame: Frame,
    atoms: list[Atom],
    document: dict[str, Any],
    identity: dict[str, Any],
    *,
    source: dict[str, Any],
    baseline: dict[str, Any],
    refinement: dict[str, Any],
    certificate: dict[str, Any] | None,
    budget: Budget,
    endpoint: bool,
) -> Context:
    remaining(budget)
    hashes = tuple(
        content_sha256(value) if value is not None else None
        for value in (source, baseline, refinement, certificate)
    )
    require(hashes == FROZEN[endpoint], "frozen E/baseline/H/J identity differs")
    selections = bound_source(source, baseline, atoms, document, identity)
    expected = (148, 24, 15, 15) if endpoint else (2522, 96, 79, 7)
    rows = {(a.owner, a.row) for a in atoms}
    require(
        (len(atoms), len(rows), len(selections), len(refinement["enhanced_selections"]))
        == expected,
        "frozen fixture inventory differs",
    )
    require(
        refinement["model"] == HALF_MODEL and refinement["predicate"] == PREDICATE,
        "H model differs",
    )
    require(refinement["input_identity"] == identity, "H input differs")
    require(
        refinement["source_packet_sha256"] == hashes[0]
        and refinement["baseline_replay_sha256"] == hashes[1],
        "H source/baseline differs",
    )
    refined, _ = children(frame, atoms, selections, document, budget)
    surviving = set()
    for item in refinement["enhanced_selections"]:
        i = item["source_selection_index"]
        require(
            type(i) is int and 0 <= i < len(selections) and i not in surviving,
            "invalid H source index",
        )
        refs = item["atoms"]
        require(type(refs) is list and len(refs) == len(selections[i]), "H tuple shape differs")
        for raw_index, ref in zip(selections[i], refs, strict=True):
            half = ref["half"]
            require(type(half) is int and half in (0, 1), "invalid H half")
            require(
                ref == child_reference(refined[raw_index, half], atoms, document),
                "H exact child reference differs",
            )
        surviving.add(i)
    lost = set(range(len(selections))) - surviving
    if certificate is not None:
        require(
            certificate["status"] == "PASS_ALL72_FIXED_TUPLE_LOSSES_CERTIFIED"
            and certificate["model"] == HALF_MODEL,
            "J status/model differs",
        )
        require(certificate["input_identity"] == identity, "J input differs")
        verified = set()
        for item in certificate["tuple_certificates"]:
            i = item["source_selection_index"]
            require(
                type(i) is int and i in lost and i not in verified, "invalid J source index"
            )
            require(
                [entry["original"] for entry in item["atoms"]]
                == [atom_reference(atoms[k], document) for k in selections[i]],
                "J original tuple differs",
            )
            verified.add(i)
        require(verified == lost and len(lost) == 72, "J/H loss partition differs")
    else:
        require(endpoint and not lost, "missing J certificate outside endpoint control")
    header = {
        "schema": SCHEMA,
        "model": MODEL,
        "predicate": PREDICATE,
        "baseline_revision": BASE_REVISION,
        "input_identity": identity,
        "E_packet_sha256": hashes[0],
        "baseline_replay_sha256": hashes[1],
        "H_packet_sha256": hashes[2],
        "J_certificate_sha256": hashes[3],
        "raw_atoms": len(atoms),
        "live_parent_rows": len(rows),
        "source_selections": len(selections),
        "H_lost_indices": sorted(lost),
        "H_survivor_indices": sorted(surviving),
        "diagnostic_only": True,
        "new_exclusions": 0,
        "unsupported_rows_verified": False,
        "whole_network_equivalence_verified": False,
        "limits": {
            "fresh_pair_calls": MAX_PAIRS,
            "wall_seconds": WALL_SECONDS,
            "worker_peak_bytes": MAX_PEAK_BYTES,
        },
    }
    remaining(budget)
    return Context(frame, atoms, document, selections, surviving, lost, header)


def nesting_failure(full: Polygon, half: Polygon) -> tuple[Q, Q] | None:
    return next((point for point in full if not in_convex(half, point)), None)


def geometry(
    context: Context, budget: Budget
) -> tuple[list[Atom], list[dict[str, Any]], dict[str, Any] | None]:
    cores: dict[Parent, tuple[Polygon, Polygon, tuple[Q, Q]]] = {}
    for atom in context.raw:
        remaining(budget)
        key = atom.owner, atom.row
        row = context.document["final_state"]["cells"][str(atom.owner)][atom.row]
        interval = tuple(Q(value) for value in row["interval"])
        require(len(interval) == 2, "full interval shape differs")
        lo, hi = interval
        if key not in cores:
            full = augmented_core(context.frame, atom.core, (lo, hi))
            strict_core(context.frame, full, lo, hi)
            require(
                all(in_convex(full, point) for point in atom.core), "old core not contained"
            )
            require(area2(full) >= area2(atom.core), "full core area decreased")
            cores[key] = atom.core, full, (lo, hi)
        require(
            cores[key][0] == atom.core and cores[key][2] == (lo, hi),
            "parent core/interval differs",
        )
    refined, _ = children(
        context.frame, context.raw, context.selections, context.document, budget
    )
    representatives = {
        (a.owner, a.row): i for i, a in enumerate(context.raw) if (i, 0) in refined
    }
    require(set(representatives) == set(cores), "E sample omits a parent core")
    rows = []
    failure = None
    for (owner, row), (old, full, interval) in sorted(cores.items()):
        remaining(budget)
        raw_index = representatives[owner, row]
        halves = [refined[raw_index, half].atom.core for half in (0, 1)]
        rows.append(
            {
                "owner": owner,
                "row": row,
                "full_interval": [str(value) for value in interval],
                "old_core_sha256": content_sha256(encode(old)),
                "full_core_sha256": content_sha256(encode(full)),
                "half_core_sha256": [content_sha256(encode(core)) for core in halves],
                "old_area2": str(area2(old)),
                "full_area2": str(area2(full)),
                "area_gain2": str(area2(full) - area2(old)),
            }
        )
        for half, core in enumerate(halves):
            point = nesting_failure(full, core)
            if point is not None and failure is None:
                failure = {
                    "owner": owner,
                    "row": row,
                    "half": half,
                    "vertex": [str(x) for x in point],
                }
    atoms = [
        Atom(a.owner, a.row, a.pieces, a.domain, cores[a.owner, a.row][1]) for a in context.raw
    ]
    require(
        all(
            a.domain == b.domain and a.pieces == b.pieces
            for a, b in zip(atoms, context.raw, strict=True)
        ),
        "domain/piece changed",
    )
    remaining(budget)
    return atoms, rows, failure


def full_reference(index: int, atom: Atom, context: Context) -> dict[str, Any]:
    return {
        **atom_reference(context.raw[index], context.document),
        "raw_atom_index": index,
        "full_core_sha256": content_sha256(encode(atom.core)),
    }


def classify(
    context: Context,
    atoms: list[Atom],
    budget: Budget,
    result: dict[str, Any],
    *,
    predicate: Predicate = incompatible,
    checkpoint: Callable[[], None] | None = None,
) -> None:
    result.update(tuple_results=[], fresh_pair_checks=0)
    owners = sorted({a.owner for a in context.raw})
    for i, selection in enumerate(context.selections):
        remaining(budget)
        require([atoms[k].owner for k in selection] == owners, "noncanonical tuple owners")
        first_collision = None
        checks = 0
        for left, right in combinations(range(len(selection)), 2):
            remaining(budget)
            if result["fresh_pair_checks"] >= MAX_PAIRS:
                raise IncompleteError("full-core pair ceiling")
            result["fresh_pair_checks"] += 1
            answer = predicate(atoms[selection[left]], atoms[selection[right]], budget)
            remaining(budget)
            require(type(answer) is bool, "predicate did not return exactbool")
            checks += 1
            if answer:
                first_collision = {"left_position": left, "right_position": right}
                break
        result["tuple_results"].append(
            {
                "source_selection_index": i,
                "atoms": [full_reference(k, atoms[k], context) for k in selection],
                "verdict": "lost" if first_collision else "survives",
                "first_collision": first_collision,
                "pair_checks": checks,
            }
        )
        if checkpoint is not None:
            checkpoint()
    lost = {
        item["source_selection_index"]
        for item in result["tuple_results"]
        if item["verdict"] == "lost"
    }
    if not lost <= context.h_lost or lost & context.h_survivors:
        result.update(
            status="STOP_SOUNDNESS_INVESTIGATION",
            reason="full/H monotonic classification contradiction",
        )
        remaining(budget)
        return
    coverage = sorted(
        {
            (atoms[k].owner, atoms[k].row)
            for i, selection in enumerate(context.selections)
            if i not in lost
            for k in selection
        }
    )
    result.update(
        status="PASS_FIXED_SAMPLE_COMPARISON",
        full_lost_indices=sorted(lost),
        full_survivor_indices=sorted(set(range(len(context.selections))) - lost),
        halving_additional_lost_indices=sorted(context.h_lost - lost),
        supported_parent_rows=[list(row) for row in coverage],
        observed_supported_parents=len(coverage),
        unknown_parent_rows=context.header["live_parent_rows"] - len(coverage),
        fixed_classification_equal=lost == context.h_lost,
    )
    remaining(budget)


def analyze(
    context: Context,
    budget: Budget,
    *,
    checkpoint: Callable[[dict[str, Any]], None] | None = None,
) -> dict[str, Any]:
    result = {
        **context.header,
        "status": "INCOMPLETE",
        "reason": "progress checkpoint",
        "tuple_results": [],
        "fresh_pair_checks": 0,
    }
    try:
        atoms, rows, failure = geometry(context, budget)
        result.update(
            full_core_rows=rows,
            full_inventory_sha256=content_sha256(
                [full_reference(i, a, context) for i, a in enumerate(atoms)]
            ),
            nesting_failure=failure,
        )
        if failure is not None:
            result.update(
                status="NESTING_FAILED",
                reason="full core escapes an H half core; comparison stopped",
            )
        elif not any(Q(row["area_gain2"]) > 0 for row in rows):
            result.update(
                status="NO_CORE_GROWTH", reason="no positive exact full-core area gain"
            )
        else:
            classify(
                context,
                atoms,
                budget,
                result,
                checkpoint=(lambda: checkpoint(result)) if checkpoint else None,
            )
            if result["status"] == "PASS_FIXED_SAMPLE_COMPARISON":
                result["reason"] = None
        remaining(budget)
    except IncompleteError as error:
        result.update(status="INCOMPLETE", reason=str(error))
    return result


def verify_packet(value: dict[str, Any], context: Context, budget: Budget) -> dict[str, Any]:
    scientific = {
        key: item
        for key, item in value.items()
        if key not in {"wall_seconds", "worker_peak_bytes"}
    }
    for key, item in context.header.items():
        require(content_sha256(value.get(key)) == content_sha256(item), f"packet {key} differs")
    require(
        value["status"] in {"PASS_FIXED_SAMPLE_COMPARISON", "NESTING_FAILED", "NO_CORE_GROWTH"},
        "incomplete packet cannot certify comparison",
    )
    fresh = analyze(context, budget)
    require(
        content_sha256(fresh) == content_sha256(scientific),
        "fresh fixed-sample/geometry replay differs",
    )
    remaining(budget)
    return {
        "status": "PASS_REPLAYED_FIXED_SAMPLE"
        if value["status"] == "PASS_FIXED_SAMPLE_COMPARISON"
        else "PASS_REPLAYED_GEOMETRY_OBSTRUCTION",
        "packet_sha256": content_sha256(value),
        "fresh_pair_checks": fresh["fresh_pair_checks"],
        "source_selections": context.header["source_selections"],
        "input_identity": context.header["input_identity"],
        "full_lost_indices": fresh.get("full_lost_indices"),
        "halving_additional_lost_indices": fresh.get("halving_additional_lost_indices"),
        "observed_supported_parents": fresh.get("observed_supported_parents"),
        "nesting_failure": fresh["nesting_failure"],
        "diagnostic_only": True,
        "new_exclusions": 0,
        "unsupported_rows_verified": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--checked-receipt", type=Path, required=True)
    parser.add_argument("--source-packet", type=Path, required=True)
    parser.add_argument("--baseline-replay", type=Path, required=True)
    parser.add_argument("--refinement-packet", type=Path, required=True)
    parser.add_argument("--conflict-certificate", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--verify", type=Path)
    parser.add_argument("--endpoint", action="store_true")
    args = parser.parse_args()
    started = time.monotonic()
    budget = Budget(started + WALL_SECONDS, MAX_PAIRS)
    result: dict[str, Any] = {
        "diagnostic_only": True,
        "new_exclusions": 0,
        "unsupported_rows_verified": False,
    }
    try:
        document, identity = checked_inputs(args.directory, args.checked_receipt)
        frame = n17_unique_frame()
        atoms = raw_atoms(frame, document)
        context = bind(
            frame,
            atoms,
            document,
            identity,
            source=bounded_json(args.source_packet),
            baseline=bounded_json(args.baseline_replay),
            refinement=bounded_json(args.refinement_packet),
            certificate=bounded_json(args.conflict_certificate)
            if args.conflict_certificate
            else None,
            budget=budget,
            endpoint=args.endpoint,
        )
        if args.verify:
            value = bounded_json(args.verify)
            result = verify_packet(value, context, budget)
        else:
            result = analyze(
                context,
                budget,
                checkpoint=lambda value: safe_write(
                    args.output.with_suffix(".partial.json"), value
                ),
            )
    except IncompleteError as error:
        result.update(status="INCOMPLETE", reason=str(error))
    except (RefusalError, KeyError, IndexError, TypeError, ValueError, OSError) as error:
        result.update(status="REFUSED", reason=f"{type(error).__name__}: {error}")
    result.update(
        wall_seconds=time.monotonic() - started, worker_peak_bytes=peak_memory_bytes()
    )
    safe_write(args.output, result)
    print(
        json.dumps(
            {
                k: v
                for k, v in result.items()
                if k not in {"tuple_results", "full_core_rows", "input_identity"}
            }
        )
    )
    return (
        0
        if str(result["status"]).startswith("PASS_")
        or result["status"] in {"NESTING_FAILED", "NO_CORE_GROWTH"}
        else 2
    )


if __name__ == "__main__":
    raise SystemExit(main())
