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

from devtools.inventory_n11_exclusions import PACKET, REPO, REVISION, inventory, require

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
    "pose-inclusion": "c5b970458135847f5790f2311e4861faf720924ad7e62f5bafb6d1978743144c",
    "local-isolation": "a98623f57017b4f04c8d3a72083caa7d4a6fb5096a79ab1e4dbbf2cd9b35a29d",
}
# Source identities come from the reviewed graph, not from a supplied PASS string.
CAPTURE = {
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
    for relative, sha in records["capture-root-chain"]["receipt_file_sha256"].items():
        target = (RECEIPTS / relative).resolve()
        require(target.is_relative_to(RECEIPTS.resolve()), "root-chain path escaped packet")
        bound(target, sha)
    missing_nodes = [node for node in nodes if not node["reviewed_execution_bound"]]
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
        "capture_nodes": nodes,
        "missing_capture_source_sha256s": [node["source_sha256"] for node in missing_nodes],
        "pending_joins": [
            "All conditional exclusion premises and center branches",
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
