"""Map reviewed n11 executions to the final composition obligations.

This is an evidence inventory, not a geometry verifier. Only explicitly reviewed
receipt identities enter the registry. Matching metadata cannot establish that an
execution occurred, and this command never promotes the global theorem.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from strif import atomic_write_text

from devtools.inventory_n11_exclusions import (
    PACKET,
    PILOTS,
    REPO,
    REVISION,
    inventory,
    read_bound,
    require,
)
from devtools.n11_composition_joins import (
    local_joins,
    reviewed_capture_states,
    root_scope,
    symmetry_join,
)

RECEIPTS = PACKET / "receipts"
FIXED = {
    "case-census": "98dad8545582694ca6217fce113f49b33d29537ea128c3994c101e75f5b57efb",
    "d4-independent": "c4aa4df460593abcb51cd4ebaaf916c78a6a718659bb6b7bf4245e3e67e6c00e",
    "source-graph": "cb7ffccf1e3841d44a2dff88549fdee1911805e516f175ef484c5b6e9004b248",
    "capture-root-chain": "f10d50e6b34179a6b2fb066d6ade9553057c280f7538ae6e53fe06e639a56d11",
    "capture-root-bridge-final2": (
        "ba65b7416678f701feee8c027e2b4f9359e9d3324ceee0958fbc8ca30afe309d"
    ),
    "capture-step0": "8ca86cc3f119c1dc42e14b142d04cf6863934b799b8e8b6818e54830b1d22b78",
    "capture-root-node-full-integer": (
        "0d55007a6c5092c0e276ec4e6a2f8524a32ddc4d527ffa3a930f088ff11bccc4"
    ),
    "capture-branch-r1-full": (
        "677719a04426aa53a9ebe3bf8d597e78079313eec2e387bc6f4e4655fd5610f4"
    ),
    "capture-child-far15": ("cda898189d5026234bb6dfd1239dec356a1ea7c1e22504034b02d0c6b692641e"),
    "capture-child-r10": "d75b95da3f286f794aa091a4abbddfea22eb264c29530200d19fa6bb8aab517f",
    "capture-child-near13": "c6e6f7bca7d19f759445fada136ee9632eb7ed69fa792ee486514bdcd781c1d2",
    "capture-child-far13": "1204bb9ca399d96b2b47e2980defa1e4194f1ea089e9bc8ff72568fe90c90feb",
    "pose-inclusion": "c5b970458135847f5790f2311e4861faf720924ad7e62f5bafb6d1978743144c",
    "local-isolation": "a98623f57017b4f04c8d3a72083caa7d4a6fb5096a79ab1e4dbbf2cd9b35a29d",
}
# Source identities come from the reviewed graph, not from a supplied PASS string.
CAPTURE = {
    "c86ed9d005dc5b2c347aa89964d7a9305bfe67f3ab3451a6e663a2185dac5fd5": (
        "capture-child-far13",
        "child_source_sha256",
        "child_node_state_checked",
    ),
    "a2f30c9246b770a2da91e45489f7b9343c345c105e00333f7ca67ab66b53db09": (
        "capture-child-near13",
        "child_source_sha256",
        "child_node_state_checked",
    ),
    "f9e67f28ea951fb5255c89e33b3ff0e1ee663c7011751761c9200441047b66d4": (
        "capture-root-node-full-integer",
        "root_source_sha256",
        "root_node_state_checked",
    ),
    "63c6e29d75491d51aa9abc404e35eb99bc862456f07bf7aa3c20f7b1c9ea5e52": (
        "capture-branch-r1-full",
        "r1_source_sha256",
        "r1_node_state_checked",
    ),
    "e25a5de42cb45d9057660bb6d5942f980672e5d6e6b97e361c10931359c2f486": (
        "capture-child-far15",
        "child_source_sha256",
        "child_node_state_checked",
    ),
    "58da537ee50dee6f21848f166a4d685961ebae6de4077835e40eef1fc1f89f48": (
        "capture-child-r10",
        "child_source_sha256",
        "child_node_state_checked",
    ),
}


def bound(path: Path, fingerprint: str) -> dict[str, Any]:
    raw = path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == fingerprint, f"changed receipt: {path}")
    return json.loads(raw)


def acyclic(parents: dict[str, str | None]) -> None:
    for node in parents:
        seen: set[str] = set()
        cursor: str | None = node
        while cursor is not None:
            require(cursor in parents, "missing dependency node")
            require(cursor not in seen, "cyclic proof dependency")
            seen.add(cursor)
            cursor = parents[cursor]


def conditional_d4(census: dict[str, Any]) -> list[int]:
    """Bind the earlier baseline without deriving it from later conditional cases."""
    baseline_sha = "e581a614d4d3210375059e4fd98bfdae0ebb1ca8ba3078050454b0da208f3c6f"
    baseline = bound(
        RECEIPTS / "baseline-d4-cuts/baseline-execution-inventory.json", baseline_sha
    )
    required = set(census["baseline"]["case_ids"])
    accepted = set(baseline["accepted_case_ids"])
    require(len(required) == 1931 and required <= accepted, "baseline exclusions missing")
    require(not {1383, 2175, 2176} & accepted, "conditional exclusion in its own premise")
    for binding in baseline["execution_record_bindings"]:
        path = (REPO / binding["path"]).resolve()
        require(path.is_relative_to(RECEIPTS.resolve()), "baseline execution outside packet")
        read_bound(path, binding["sha256"])
    for case in (2175, 2176):
        relative = f"generic-case{case}-complete/replay.json.gz"
        require(PILOTS[relative][0] == case, "special case registry identity")
        execution = read_bound(RECEIPTS / relative, PILOTS[relative][1])
        require(execution["excluded_case_ids"] == [case], "conditional exclusion identity")
        require(
            execution["source_sha256"]["baseline_execution_inventory"] == baseline_sha,
            "conditional exclusion baseline differs",
        )
        report = bound(
            RECEIPTS / f"generic-case{case}-complete/replay-d4-cuts.json",
            execution["source_sha256"]["d4_report"],
        )
        require(
            report["baseline_execution_premise_admitted"] is True
            and report["finite_obligations_complete"] is True
            and report["necessary_cuts_verified"] is True
            and set(report["baseline_case_ids"]) == required
            and report["baseline_pending_case_ids"] == []
            and [row["mask_index"] for row in report["cases"]] == [case],
            "conditional cut scope differs",
        )
    return [2175, 2176]


def completion() -> dict[str, Any]:
    records = {name: bound(RECEIPTS / name / "result.json", sha) for name, sha in FIXED.items()}
    path = RECEIPTS / "exclusion-inventory.json"
    previous = json.loads(path.read_bytes())
    batches = [
        REPO / row["path"]
        for row in previous["execution_record_bindings"]
        if row["path"].endswith("/summary.json")
    ]
    exclusions = inventory(batches)
    require(
        exclusions == previous, "retained exclusion inventory differs from reviewed records"
    )
    required = set(range(2184)) - {438, 999, 1462, 1659}
    accepted = set(exclusions["accepted_case_ids"])
    require(accepted <= required, "excluded survivor or foreign case")
    require(set(exclusions["remaining_case_ids"]) == required - accepted, "wrong remainder")
    d4_cases = conditional_d4(records["case-census"])

    graph = records["source-graph"]
    require(graph["upstream_commit"] == REVISION, "capture revision differs")
    provenance = graph["source_provenance"]
    parents = {
        pin["decoded_sha256"]: graph["source_parent_edges"].get(name)
        for name, pin in provenance.items()
    }
    require(
        len(parents) == 10 and sum(p is None for p in parents.values()) == 1, "capture census"
    )
    acyclic(parents)
    require(set(CAPTURE) <= set(parents), "reviewed capture outside required graph")
    nodes = []
    for name, pin in provenance.items():
        source = pin["decoded_sha256"]
        registry = CAPTURE.get(source)
        if registry is not None:
            receipt, source_key, state_key = registry
            record = records[receipt]
            require(record[source_key] == source and record[state_key] is True, "capture scope")
            require(record["global_optimality_proved"] is False, "unexpected global promotion")
            if parents[source] is not None:
                require(parents[source] in CAPTURE, "accepted child without accepted parent")
            if source_key == "child_source_sha256":
                parent_receipt = CAPTURE[parents[source]][0]
                require(
                    record["parent_source_sha256"] == parents[source]
                    and record["parent_result_sha256"] == FIXED[parent_receipt],
                    "child execution premise differs",
                )
        nodes.append(
            {
                "source_path": name,
                "source_sha256": source,
                "parent_source_sha256": parents[source],
                "reviewed_execution_bound": registry is not None,
            }
        )

    # These exact receipt joins were independently reviewed before registry admission.
    joins = (
        ("capture-root-bridge-final2", "chain_result_sha256", "capture-root-chain"),
        ("capture-step0", "bridge_result_sha256", "capture-root-bridge-final2"),
        ("capture-root-node-full-integer", "step0_result_sha256", "capture-step0"),
        ("capture-branch-r1-full", "root_result_sha256", "capture-root-node-full-integer"),
        ("pose-inclusion", "accepted_local_result_sha256", "local-isolation"),
    )
    for child, field, parent in joins:
        require(records[child][field] == FIXED[parent], f"receipt join differs: {child}")
    far15 = records["capture-child-far15"]
    require(
        far15["terminal_empty_pose_checked"] is True
        and far15["final_state_canonical_sha256"]
        == graph["leaf_final_state_digests"]["far15"]["actual"],
        "far15 contradiction or actual leaf state differs",
    )
    for relative, sha in records["capture-root-chain"]["receipt_file_sha256"].items():
        target = (RECEIPTS / relative).resolve()
        require(target.is_relative_to(RECEIPTS.resolve()), "root-chain path escaped packet")
        bound(target, sha)
    missing_nodes = [node for node in nodes if not node["reviewed_execution_bound"]]
    missing_leaves = reviewed_capture_states(graph, records, CAPTURE)
    local_joins(records, RECEIPTS)
    symmetry_join(records, RECEIPTS)
    root_scope(records)
    return {
        "status": "INCOMPLETE_PROOF_OBLIGATION_INVENTORY",
        "source_revision": REVISION,
        "geometry_rerun": False,
        "global_optimality_proved": False,
        "premise": (
            "Listed reviewed component executions occurred; "
            "this inventory does not prove their occurrence."
        ),
        "final_composition_review_required": True,
        "accepted_exclusions": len(accepted),
        "required_exclusions": len(required),
        "missing_exclusion_ids": sorted(required - accepted),
        "conditional_d4_premises_bound": d4_cases,
        "center_partition_execution_pending": 1383 not in accepted,
        "capture_nodes": nodes,
        "missing_capture_source_sha256s": [node["source_sha256"] for node in missing_nodes],
        "missing_capture_leaf_executions": missing_leaves,
        "closed_capture_split_algebra_checked": True,
        "retained_pose_local_join_checked": True,
        "pending_joins": [
            "Both center-partition branches for case 1383",
            "All three far-leaf contradictions and closed branch coverage",
            "Accepted near final state to pose inclusion and local isolation",
            "Final consumer join to the reviewed endpoint/witness argument",
        ],
        "reviewed_fixed_receipt_sha256s": FIXED,
        "exclusion_inventory_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = completion()
    atomic_write_text(args.out, json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "accepted_exclusions": result["accepted_exclusions"],
                "missing_exclusions": len(result["missing_exclusion_ids"]),
                "missing_capture_nodes": len(result["missing_capture_source_sha256s"]),
            }
        )
    )


if __name__ == "__main__":
    main()
