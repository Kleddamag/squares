"""One A-seeded least-supported-owner schedule in the frozen enhanced network.

Positive parent supports only. Scheduling and a stronger seed prefix are combined;
new coverage is not a matched estimate of scheduling speedup.
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

from devtools import probe_n17_enhanced_row_support as enhanced
from devtools.bounded_diagnostics import (
    retained_matches,
    same_header,
    same_inputs,
)
from devtools.check_hull_kernel_mask0 import n17_unique_frame
from devtools.probe_n17_raw_row_support import (
    LazySupports,
    bounded_json,
    checked_inputs,
    raw_atoms,
)
from devtools.process_memory import peak_memory_bytes
from sqpack.hull_kernel.geometry import Budget, IncompleteError, RefusalError, require

SCHEMA = "n17.scheduled-enhanced-parent-row-support.v1"
BASE_REVISION = "0dcc3d6e8ec7f675fb12ad122fd9250a97b2f2f3"
A_PATH = {
    False: (
        "packing/campaign/explorations/X048-session-175-enhanced-support/"
        "receipts/B-support-packet.json"
    ),
    True: (
        "packing/campaign/explorations/X048-session-175-enhanced-support/"
        "receipts/endpoint-support-packet.json"
    ),
}
A_REPLAY_PATH = {
    False: (
        "packing/campaign/explorations/X048-session-175-enhanced-support/"
        "receipts/B-independent-replay.json"
    ),
    True: (
        "packing/campaign/explorations/X048-session-175-enhanced-support/"
        "receipts/endpoint-replay.json"
    ),
}
ARTIFACT_PROVENANCE = {
    "historical_revision": BASE_REVISION,
    "committed_paths": {"A_PATH": A_PATH, "A_REPLAY_PATH": A_REPLAY_PATH},
}
A_FIXTURES = {False: (26, 41), True: (15, 24)}


def accepted_seeds(
    value: dict[str, Any],
    replay: dict[str, Any],
    inv: enhanced.Inventory,
    original_header: dict[str, Any],
    h_initial: list[list[int]],
    *,
    endpoint: bool,
) -> list[list[int]]:
    """Bind accepted A artifacts and exact refs without uncharged pair queries."""
    require(retained_matches(value, BASE_REVISION, A_PATH[endpoint]), "frozen A packet differs")
    require(
        retained_matches(replay, BASE_REVISION, A_REPLAY_PATH[endpoint]),
        "frozen A replay differs",
    )
    require(
        same_header(value, original_header),
        "A input/model/inventory differs",
    )
    require(
        value["status"] in {"INCOMPLETE", "PARTIAL_SUPPORT", "ALL_ROWS_SUPPORTED"},
        "A status differs",
    )
    expected_count, expected_rows = A_FIXTURES[endpoint]
    refs = value["selections"]
    require(isinstance(refs, list) and len(refs) == expected_count, "A selection count differs")
    prefix = [[inv.references[index] for index in selection] for selection in h_initial]
    require(refs[: len(prefix)] == prefix, "A full H prefix differs")
    h_rows = set().union(*(enhanced.parent_coverage(s, inv) for s in h_initial))
    require(
        value["seeds_freshly_prevalidated"] is True
        and value["seed_selections"] == len(h_initial)
        and value["initial_selections_revalidated"] == len(h_initial)
        and value["initial_supported_rows"] == len(h_rows),
        "A seed metadata differs",
    )
    initial = [enhanced.selection_indices(selection, inv) for selection in refs]
    covered = set().union(*(enhanced.parent_coverage(s, inv) for s in initial))
    require(len(covered) == expected_rows, "A baseline coverage differs")
    require(
        value["supported_parent_rows"] == [list(row) for row in sorted(covered)]
        and value["new_parent_rows"] == [list(row) for row in sorted(covered - h_rows)]
        and value["unknown_parent_rows"]
        == [list(row) for row in sorted(inv.parents() - covered)],
        "A claimed coverage differs",
    )
    require(
        replay["status"] in {"PASS_REPLAYED_PARTIAL_SUPPORT", "PASS_REPLAYED_ALL_PARENT_ROWS"}
        and same_inputs(replay["input_identity"], original_header["input_identity"])
        and replay["live_parent_rows"] == len(inv.parents())
        and replay["supported_parent_rows"] == len(covered)
        and replay["selections_checked"] == len(initial)
        and replay["fresh_pair_checks"] == 15 * len(initial)
        and replay["unsupported_rows_verified"] is False,
        "A replay identity/coverage differs",
    )
    return initial


def schedule(
    inv: enhanced.Inventory, initial: list[list[int]]
) -> tuple[list[int], list[enhanced.Parent]]:
    """All parents, ordered by supported-parent count then numeric owner/row."""
    before = set().union(*(enhanced.parent_coverage(s, inv) for s in initial))
    owners = sorted({atom.owner for atom in inv.atoms})
    priority = sorted(owners, key=lambda owner: (sum(row[0] == owner for row in before), owner))
    rows = inv.parents()
    order = [row for owner in priority for row in sorted(rows) if row[0] == owner]
    require(len(order) == len(rows) and set(order) == rows, "schedule is not complete")
    return priority, order


def header(
    original: dict[str, Any],
    value: dict[str, Any],
    replay: dict[str, Any],
    inv: enhanced.Inventory,
    initial: list[list[int]],
) -> dict[str, Any]:
    del value, replay  # Preserve the public helper signature.
    priority, order = schedule(inv, initial)
    return {
        **original,
        "schema": SCHEMA,
        "artifact_provenance": ARTIFACT_PROVENANCE,
        "baseline_repository_revision": BASE_REVISION,
        "schedule": "least-supported-owner-then-numeric-row-v1",
        "owner_priority": priority,
        "row_order": [list(row) for row in order],
        "scheduling_effect_isolated": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    for name in (
        "checked-receipt",
        "source-packet",
        "baseline-replay",
        "refinement-packet",
        "accepted-packet",
        "accepted-replay",
        "output",
    ):
        parser.add_argument(f"--{name}", type=Path, required=True)
    parser.add_argument("--verify", type=Path)
    parser.add_argument("--endpoint", action="store_true")
    args = parser.parse_args()
    started, cpu = time.monotonic(), time.process_time()
    budget = Budget(
        started + (enhanced.REPLAY_SECONDS if args.verify else enhanced.WALL_SECONDS),
        enhanced.MAX_NODES,
    )
    result: dict[str, Any] = {
        "diagnostic_only": True,
        "new_exclusions": 0,
        "unsupported_rows_verified": False,
    }
    try:
        document, identity = checked_inputs(args.directory, args.checked_receipt)
        frame = n17_unique_frame()
        inv = enhanced.build_inventory(frame, raw_atoms(frame, document), document, budget)
        refinement = bounded_json(args.refinement_packet)
        enhanced.fixture_inventory(inv, refinement, endpoint=args.endpoint)
        source, baseline = bounded_json(args.source_packet), bounded_json(args.baseline_replay)
        h_initial = enhanced.seeds(
            refinement, source, baseline, inv, document, identity=identity
        )
        original = enhanced.header(inv, identity, refinement, source, baseline)
        if args.endpoint:
            enhanced.endpoint_children(frame, document, inv, h_initial)
            original["endpoint_angle_children_checked"] = True
        accepted, replay = (
            bounded_json(args.accepted_packet),
            bounded_json(args.accepted_replay),
        )
        initial = accepted_seeds(
            accepted, replay, inv, original, h_initial, endpoint=args.endpoint
        )
        common = header(original, accepted, replay, inv, initial)
        if args.verify:
            result.update(
                enhanced.verify_packet(bounded_json(args.verify), inv, common, initial, budget)
            )
        else:
            search = LazySupports(
                inv.atoms,
                budget,
                predicate=enhanced.bounded_incompatible,
                max_pairs=enhanced.MAX_PAIRS,
                max_nodes=enhanced.MAX_NODES,
            )
            enhanced.prevalidate(search, initial)

            def checkpoint(snapshot: dict[str, Any]) -> None:
                enhanced.safe_write(
                    args.output.with_suffix(".partial.json"),
                    enhanced.packet(snapshot, inv, common, initial, seeded=True),
                )

            _, order = schedule(inv, initial)
            snapshot = search.run(
                initial_selections=initial,
                strategy="forward-mrv",
                row_order=order,
                checkpoint=checkpoint,
            )
            result.update(enhanced.packet(snapshot, inv, common, initial, seeded=True))
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
    enhanced.safe_write(args.output, result)
    print(
        json.dumps(
            {key: result[key] for key in ("status", "wall_seconds", "worker_peak_bytes")}
        ),
        flush=True,
    )
    raise SystemExit(0 if result["status"] != "REFUSED" else 2)


if __name__ == "__main__":
    main()
