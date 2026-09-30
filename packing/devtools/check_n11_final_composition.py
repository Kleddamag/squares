"""Compose explicitly reviewed n11 executions, refusing every missing premise.

This command does not rerun geometry. Its conclusion is conditional on the
observed executions identified in the reviewed registry actually occurring.
The complete exclusion inventory must receive its own final review and fixed
identity before this command can report a complete composition.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from strif import atomic_write_text

from devtools import (
    inventory_n11_completion,
    inventory_n11_exclusions,
    n11_composition_joins,
    prepare_n11_nonfield_manifest,
    run_n11_nonfield_batch,
)
from devtools.inventory_n11_completion import FIXED, RECEIPTS, bound, completion
from devtools.inventory_n11_exclusions import PILOTS, read_bound, require

# Fill only after all 2,180 executions and their exact union receive final review.
REVIEWED_COMPLETE_EXCLUSION_INVENTORY: str | None = (
    "498801611757f8ce4557dd105697c4e6c4ab8aa3d460e0306b90bda4657ffe48"
)


def source_closure() -> dict[str, str]:
    paths = [Path(__file__)]
    for module in (
        inventory_n11_completion,
        inventory_n11_exclusions,
        n11_composition_joins,
        prepare_n11_nonfield_manifest,
        run_n11_nonfield_batch,
    ):
        if module.__file__ is None:
            raise ValueError(f"composition dependency has no source: {module.__name__}")
        paths.append(Path(module.__file__))
    return {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in paths}


def compose() -> dict[str, Any]:
    sources = source_closure()
    inventory = completion()
    pending = []
    if inventory["missing_exclusion_ids"]:
        pending.append("required exclusion executions remain")
    if inventory["missing_capture_source_sha256s"]:
        pending.append("required capture node executions remain")
    if inventory["missing_capture_leaf_executions"]:
        pending.append("required far contradictions or near final-state execution remain")
    if REVIEWED_COMPLETE_EXCLUSION_INVENTORY is None:
        pending.append("complete exclusion inventory awaits final review and fixed identity")
    else:
        require(
            inventory["exclusion_inventory_sha256"] == REVIEWED_COMPLETE_EXCLUSION_INVENTORY,
            "reviewed complete exclusion inventory changed",
        )

    center = [
        (relative, fingerprint)
        for relative, (case, fingerprint) in PILOTS.items()
        if case == 1383
    ]
    if not center:
        pending.append("reviewed complete center-partition execution remains")
    else:
        require(len(center) == 1, "ambiguous center-partition execution registry")
        record = read_bound(RECEIPTS / center[0][0], center[0][1])
        require(
            record["status"] == "PASS_CENTER_PARTITION_EXCLUSION"
            and record["geometry_verified"] is True
            and record["excluded_case_ids"] == [1383]
            and record["nodes_completed"] == 8
            and record["branches_completed"] == ["le", "ge"],
            "center partition lacks both complete branches",
        )

    near = FIXED.get("capture-child-near")
    if near is None:
        pending.append(
            "accepted near state has not discharged the conditional inclusion premise"
        )
    else:
        record = bound(RECEIPTS / "capture-child-near/result.json", near)
        graph = bound(RECEIPTS / "source-graph/result.json", FIXED["source-graph"])
        pose = bound(RECEIPTS / "pose-inclusion/result.json", FIXED["pose-inclusion"])
        require(
            record["child_source_sha256"] == pose["source_sha256"]
            and record["final_state_canonical_sha256"]
            == graph["leaf_final_state_digests"]["near"]["actual"],
            "near-to-inclusion final state differs",
        )

    complete = not pending
    require(source_closure() == sources, "composition source changed during execution")
    return {
        "status": "PASS_REVIEWED_COMPONENT_COMPOSITION"
        if complete
        else "INCOMPLETE_COMPOSITION",
        "geometry_rerun": False,
        "observed_execution_premise": inventory["premise"],
        "global_optimality_proved": complete,
        "accepted_exclusions": inventory["accepted_exclusions"],
        "required_exclusions": inventory["required_exclusions"],
        "pending_obligations": pending,
        "missing_exclusion_ids": inventory["missing_exclusion_ids"],
        "missing_capture_source_sha256s": inventory["missing_capture_source_sha256s"],
        "endpoint_argument": (
            "Concentric embedding of any S<T into U, the complete exclusion/D4 reduction, "
            "closed capture and pose inclusion place it in the fixed-T local neighborhood. "
            "Local isolation forces the verified witness of span T, contradicting S<T. "
            "The same independently checked witness supplies the upper bound at T."
        ),
        "reviewed_receipt_sha256s": FIXED,
        "exclusion_inventory_sha256": inventory["exclusion_inventory_sha256"],
        "source_sha256": sources,
        "checker_sha256": sources[Path(__file__).name],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    require(not args.out.exists(), "use a new composition receipt path")
    result = compose()
    atomic_write_text(args.out, json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "pending": result["pending_obligations"]}))
    return 0 if result["global_optimality_proved"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
