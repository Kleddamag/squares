"""Check reported case-438 capture metadata and its pinned near-state binding.

The small audit packet can establish reported graph consistency. The actual source
parent graph and geometric replay require their separate source objects. A mismatch
in a source-bound audit field is a certificate refusal, not a packing counterexample.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import time
from fractions import Fraction
from pathlib import Path
from typing import Any

Q = Fraction
MASK = [0, 1, 2, 3, 4, 8, 9, 10, 11, 13, 15]
U = Q(387708359002281417731, 10**20)
B = Q(191, 50) / U
NEAR_SHA = "491afdaaf411e7fdb4968bdcda7232ea517ead34739d0ae8c7d5570333a981cc"
NEAR_BYTES = 185901535
POSE_RESULT_SHA = "c5b970458135847f5790f2311e4861faf720924ad7e62f5bafb6d1978743144c"
ROOT_SOURCE_SHA = "5452ed7fe20266ec81749b79c1e00f4e9a2ba75242b25d90b7fb696ca317d40a"
PACKETS = {
    "B1": (
        "f5c66ab125f7a4695039197ae52b5ce5ee2dd2365142e4cf8488a220f250f5d5",
        5892,
        "57b1991c0c537a767a1d12a17f643485339c1533114f6e41ae58189adb6439e4",
        1991,
    ),
    "B2": (
        "dd192f1a95fe23d0ae63112ef8f6f78ee31ba2f81241c47abf2b48299e430f45",
        20536,
        "77fcd8a1cbd1934e16c7ca39c9328b9b8dd3c8049a3088c04c78a2a0c961b491",
        5232,
    ),
    "B3": (
        "8e369168774ba97721ba49efcff2d35cbe5f0d86f3e01a37b419a800e047d7e4",
        30071,
        "9197e68e4a55d5157823f1446a5a469c3cc521e37501a44f32ac988d718f8ef0",
        2948,
    ),
    "B4": (
        "c68188a3ecd68ae865c139347cf5d4234f3e99e69c16709c806f4d307e732689",
        4160,
        "c9263e1f0b6596472372d64fe759f68a89ac4459cfbff55e19f21c8ff20c85d8",
        1713,
    ),
    "B5": (
        "6088857994ed2fae2e5de5f27c0fccbeb7aac668736506fa81b6afdfefeed7e3",
        7513,
        "81710beb5b04f42bdd68e3070f5cc8efa6a4578ab64598096d9f1d12d93c7768",
        2335,
    ),
    "B6": (
        "cc9b3d39e30bcf76a27956a7c453476d9364f6c3d2cc9864d66506ec65306832",
        10638,
        "41d9f18517d61cb9414ac3697f72833eed0483dc2e4869613471766785770b17",
        2596,
    ),
    "B7": (
        "4a93b7c841b4380fb0bd481b6d57e595d9f4ae84fe3ce86fc57bad7374c765a3",
        12950,
        "958b3b39f5216309291a52214f0a79cf08e203eb174d9897ebcb7db76240d0b8",
        2775,
    ),
}
LEAF_NAMES = ("far15", "far13", "far2", "near")
LEAF_AUDITS = ("B4", "B5", "B6", "B7")
NODE_PREFIX = "/workspace/eleven-square/"


def require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_sha(value: Any) -> str:
    return sha(json.dumps(value, default=str, sort_keys=True, separators=(",", ":")).encode())


def digest_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_packets(packet_dir: Path) -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    for name, (decoded_sha, decoded_size, compressed_sha, compressed_size) in PACKETS.items():
        compressed = (packet_dir / f"{name}.gz").read_bytes()
        require(
            len(compressed) == compressed_size and sha(compressed) == compressed_sha,
            f"{name} compressed identity mismatch",
        )
        decoded = gzip.decompress(compressed)
        require(
            len(decoded) == decoded_size and sha(decoded) == decoded_sha,
            f"{name} decoded identity mismatch",
        )
        records[name] = json.loads(decoded)
    return records


def center_cut(keep: str) -> dict[str, Any]:
    sign = 1 if keep == "le" else -1
    return {
        "owner": 15,
        "normal": [0, sign],
        "upper_field": str(sign * B * (U / 2 + Q(5, 4))),
        "axis": 1,
        "bound_centered_unit": "5/4",
        "keep": keep,
    }


def angle_cut(owner: int, bound: Q, keep: str) -> dict[str, Any]:
    require(0 < bound < 1, "angular partition cut lies outside closed domain")
    return {"kind": "half_angle", "owner": owner, "bound_half_angle": str(bound), "keep": keep}


def expected_leaves() -> list[tuple[str, list[list[Any]], list[dict[str, Any]], str]]:
    first = [center_cut("le")]
    second = [center_cut("ge"), angle_cut(13, Q(147, 512), "le")]
    third = [
        center_cut("ge"),
        angle_cut(13, Q(147, 512), "ge"),
        angle_cut(2, Q(183, 512), "le"),
    ]
    fourth = [
        center_cut("ge"),
        angle_cut(13, Q(147, 512), "ge"),
        angle_cut(2, Q(183, 512), "ge"),
    ]
    return [
        ("far15", [[15, "center", "5/4", "le"]], first, "CONTRADICTION"),
        (
            "far13",
            [[15, "center", "5/4", "ge"], [13, "angle", "147/512", "le"]],
            second,
            "CONTRADICTION",
        ),
        (
            "far2",
            [
                [15, "center", "5/4", "ge"],
                [13, "angle", "147/512", "ge"],
                [2, "angle", "183/512", "le"],
            ],
            third,
            "CONTRADICTION",
        ),
        (
            "near",
            [
                [15, "center", "5/4", "ge"],
                [13, "angle", "147/512", "ge"],
                [2, "angle", "183/512", "ge"],
            ],
            fourth,
            "FOCUSED_LOCAL_RECTANGLE",
        ),
    ]


def node_key(record: dict[str, Any]) -> str:
    path = record["path"]
    require(
        isinstance(path, str) and path.startswith(NODE_PREFIX),
        "node path outside pinned source root",
    )
    return path[len(NODE_PREFIX) :]


def mathematical_node_fields(record: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in record.items() if key != "cached_from_audit_sha256"}


def check_reported(packets: dict[str, dict[str, Any]]) -> dict[str, Any]:
    pins, composition, root = (packets[name] for name in ("B1", "B2", "B3"))
    nodes = pins["geometry_nodes"]
    premises = pins["bound_premises"]
    require(
        len(nodes) == 10 and len(premises) == 24, "ten-node or 24-premise inventory mismatch"
    )
    require(
        nodes == composition["geometry_nodes"] and premises == composition["bound_premises"],
        "composition inventories disagree",
    )
    require(composition["mask_index"] == root["mask_index"] == 438, "wrong case index")
    require(composition["required_antecedent_mask"] == MASK, "wrong composition mask")
    require(
        Q(composition["parent_Uplus"]) == U and Q(composition["parent_side"]) == B,
        "wrong composition frame",
    )
    require(
        root["source_sha256"] == ROOT_SOURCE_SHA and ROOT_SOURCE_SHA in premises.values(),
        "root source premise mismatch",
    )
    require(
        root["branch_exclusion_proved"] is False and root["global_optimality_proved"] is False,
        "root audit scope mismatch",
    )
    owner_rounds: dict[int, list[int]] = {owner: [] for owner in MASK}
    for row in root["cells"]:
        owner = row["owner"]
        require(
            owner in owner_rounds and row["complete"] is True, "root owner induction incomplete"
        )
        owner_rounds[owner].append(row["round"])
    require(
        all(sorted(rounds) == list(range(1, 15)) for rounds in owner_rounds.values()),
        "root owner-round inventory incomplete",
    )
    require(len(root["cells"]) == 154, "root owner-round duplicate")

    leaves = composition["closed_leaves"]
    require(len(leaves) == 4, "closed leaf count mismatch")
    all_nodes: dict[str, dict[str, Any]] = {}
    audited: dict[str, dict[str, dict[str, Any]]] = {}
    previous_keys: set[str] = set()
    for (name, predicates, cuts, closure), audit_name, leaf in zip(
        expected_leaves(), LEAF_AUDITS, leaves, strict=True
    ):
        audit = packets[audit_name]
        require(
            leaf["name"] == name
            and leaf["predicates"] == predicates
            and leaf["closure"] == closure,
            f"{name} closed partition differs",
        )
        require(
            leaf["audit_sha256"] == PACKETS[audit_name][0]
            and leaf["source_sha256"] == audit["source_sha256"],
            f"{name} audit/source binding mismatch",
        )
        require(audit["constraints"] == cuts, f"{name} field or angle cut differs")
        require(
            audit["root_sha256"] == ROOT_SOURCE_SHA
            and audit["root_audit_sha256"] == PACKETS["B3"][0],
            f"{name} root binding mismatch",
        )
        require(audit["mask_index"] == 438 and audit["mask"] == MASK, f"{name} mask mismatch")
        require(
            Q(audit["parent_Uplus"]) == U and Q(audit["parent_side"]) == B,
            f"{name} frame mismatch",
        )
        require(
            audit["global_optimality_proved"] is False and audit["inside_local_guard"] is False,
            f"{name} status scope mismatch",
        )
        require(
            audit["branch_exclusion_proved"] is (name != "near"),
            f"{name} branch status mismatch",
        )
        raw_nodes = audit["nodes"]
        require(
            len(raw_nodes) == {"far15": 2, "far13": 5, "far2": 8, "near": 10}[name],
            f"{name} node count differs",
        )
        require(
            len({node_key(record) for record in raw_nodes}) == len(raw_nodes),
            f"{name} repeats a geometry node",
        )
        current: dict[str, dict[str, Any]] = {}
        for record in raw_nodes:
            key = node_key(record)
            require(
                key in nodes and nodes[key] == record["sha256"],
                f"{name} node identity mismatch",
            )
            current[key] = mathematical_node_fields(record)
            if key in all_nodes:
                require(
                    current[key] == all_nodes[key], f"{name} cached node math fields changed"
                )
            else:
                all_nodes[key] = current[key]
            if "cached_from_audit_sha256" in record:
                earlier_sha = record["cached_from_audit_sha256"]
                require(earlier_sha in audited, f"{name} cached audit is not earlier")
                require(
                    audited[earlier_sha].get(key) == current[key],
                    f"{name} cached node is not in earlier audit",
                )
        require(
            current[node_key(raw_nodes[-1])]["sha256"] == audit["source_sha256"],
            f"{name} final node differs from source",
        )
        require(previous_keys <= set(current), f"{name} dropped earlier geometry node")
        previous_keys = set(current)
        expected_prior = (
            None if name == "far15" else PACKETS[LEAF_AUDITS[LEAF_NAMES.index(name) - 1]][0]
        )
        cited = audit.get("premise_audits") or []
        require(
            (not cited)
            if expected_prior is None
            else (len(cited) == 1 and cited[0]["sha256"] == expected_prior),
            f"{name} cached premise chain differs",
        )
        audited[PACKETS[audit_name][0]] = current
    require(set(all_nodes) == set(nodes), "reported geometry node union incomplete")
    require(
        composition["pose_rows_covered"] == 136 and composition["vertices_covered"] == 1542,
        "reported pose inventory mismatch",
    )
    require(
        composition["local_rectangle_audit_sha256"]
        == "9a9cf4e0fdcb1b1d226b9c07ec08d08cbbc572749cec9bc09cf3cd92bd4d88f3",
        "reported local input differs",
    )
    return {
        "reported_geometry_nodes": len(all_nodes),
        "reported_bound_premises": len(premises),
        "reported_root_owner_rounds": len(root["cells"]),
        "closed_leaves": list(LEAF_NAMES),
        "reported_cached_audit_chain": [PACKETS[name][0] for name in LEAF_AUDITS],
        "near_parent_sha256": nodes["research/candidate-capture/tree438-facet/r111.json"],
    }


def check_near_binding(
    packets: dict[str, dict[str, Any]],
    near_path: Path,
    pose_result_path: Path,
) -> dict[str, Any]:
    require(
        near_path.stat().st_size == NEAR_BYTES and digest_file(near_path) == NEAR_SHA,
        "pinned near source identity mismatch",
    )
    near = json.loads(near_path.read_bytes())
    near_audit = packets["B7"]
    require(near["node_id"] == "near-refined1024-240", "near node identity mismatch")
    require(near["mask_index"] == 438 and near["mask"] == MASK, "near source mask mismatch")
    require(Q(near["U"]) == U and Q(near["B"]) == B, "near source frame mismatch")
    require(
        near["parent"]["sha256"]
        == packets["B1"]["geometry_nodes"][
            "research/candidate-capture/tree438-facet/r111.json"
        ],
        "near actual parent differs",
    )
    require(
        near["constraints"] == near["final_state"]["constraints"] == near_audit["constraints"],
        "near final constraints differ",
    )
    require(near["final_state"]["mask"] == MASK, "near final-state mask differs")
    require(
        near["terminal"] is True and near["contradiction"] is None,
        "near source terminal scope differs",
    )
    pose_bytes = pose_result_path.read_bytes()
    require(sha(pose_bytes) == POSE_RESULT_SHA, "accepted pose inclusion result changed")
    pose = json.loads(pose_bytes)
    require(
        pose["status"] == "PASS_POSE_INCLUSION" and pose["source_sha256"] == NEAR_SHA,
        "pose result is for another source",
    )
    require(
        pose["live_rows_checked"] == 136 and pose["vertices_checked"] == 1542,
        "pose census differs",
    )
    actual = canonical_sha(near["final_state"])
    claimed = near_audit["final_state_sha256"]
    return {
        "near_source_sha256": NEAR_SHA,
        "near_actual_parent_sha256": near["parent"]["sha256"],
        "near_final_state_actual_sha256": actual,
        "near_final_state_reported_sha256": claimed,
        "near_final_state_digest_matches": actual == claimed,
        "pose_inclusion_result_sha256": POSE_RESULT_SHA,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--packets", type=Path, required=True, help="Directory of pinned B1.gz through B7.gz"
    )
    parser.add_argument(
        "--near-source", type=Path, required=True, help="Decoded pinned near source"
    )
    parser.add_argument("--pose-result", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--max-seconds", type=float, default=15.0)
    args = parser.parse_args()
    require(0 < args.max_seconds <= 60, "bounded positive runtime ceiling required")
    start_wall, start_cpu = time.monotonic(), time.process_time()
    packets = load_packets(args.packets)
    reported = check_reported(packets)
    reported_wall, reported_cpu = time.monotonic() - start_wall, time.process_time() - start_cpu
    require(reported_wall < args.max_seconds, "runtime ceiling expired after reported metadata")
    binding = check_near_binding(packets, args.near_source, args.pose_result)
    require(
        time.monotonic() - start_wall < args.max_seconds,
        "runtime ceiling expired after source binding",
    )
    status = (
        "REPORTED_CAPTURE_METADATA_CONSISTENT_SOURCE_BINDING_REFUSED"
        if not binding["near_final_state_digest_matches"]
        else "NEAR_SOURCE_BOUND_OTHER_ANCESTRY_UNCHECKED"
    )
    result = {
        "status": status,
        "reported_capture_metadata_consistent": True,
        "near_source_binding_accepted": binding["near_final_state_digest_matches"],
        "complete_source_ancestry_proved": False,
        "geometric_capture_proved": False,
        "candidate_mask_capture_proved": False,
        "global_optimality_proved": False,
        "scope": (
            "Small packet inventory and closed branch predicates checked; actual "
            "source graph and geometry remain separate. A stale final-state digest "
            "blocks this published certificate binding, not the packing theorem."
        ),
        "checker_sha256": digest_file(Path(__file__)),
        "upstream_commit": "f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c",
        "packet_decoded_sha256": {name: record[0] for name, record in PACKETS.items()},
        **reported,
        **binding,
        "reported_metadata_wall_seconds": reported_wall,
        "reported_metadata_process_cpu_seconds": reported_cpu,
        "wall_seconds": time.monotonic() - start_wall,
        "process_cpu_seconds": time.process_time() - start_cpu,
        "max_seconds": args.max_seconds,
    }
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result))
    if not binding["near_final_state_digest_matches"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
