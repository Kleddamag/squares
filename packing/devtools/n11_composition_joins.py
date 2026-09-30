"""Exact joins for the reviewed n11 component executions.

These checks consume only the caller's fixed, reviewed receipt registry. They
check composition, not execution occurrence or a fresh geometric replay.
"""

from __future__ import annotations

import gzip
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


def require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def retained_object(path: Path, fingerprint: str) -> dict[str, Any]:
    raw = gzip.decompress(path.read_bytes())
    require(hashlib.sha256(raw).hexdigest() == fingerprint, f"changed retained input: {path}")
    return json.loads(raw)


def capture_conditions(graph: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Check three complementary closed splits and their inherited conditions."""
    headers = {Path(path).stem: row for path, row in graph["source_headers"].items()}
    require(len(headers) == 10, "capture node names are not unique")
    cap = Q("387708359002281417731/100000000000000000000")
    scale = Q("382000000000000000000/387708359002281417731")
    mask = [0, 1, 2, 3, 4, 8, 9, 10, 11, 13, 15]
    height = scale * (cap / 2 + Q(5, 4))

    def center(sign: int, keep: str) -> dict[str, Any]:
        return {
            "owner": 15,
            "normal": [0, sign],
            "upper_field": str(sign * height),
            "axis": 1,
            "bound_centered_unit": "5/4",
            "keep": keep,
        }

    def angle(owner: int, bound: str, keep: str) -> dict[str, Any]:
        return {"kind": "half_angle", "owner": owner, "bound_half_angle": bound, "keep": keep}

    upper = [center(-1, "ge")]
    near13 = [*upper, angle(13, "147/512", "ge")]
    expected = {
        "root-self-240": [],
        "far15y-self-300": [center(1, "le")],
        "r1": upper,
        "r10": [*upper, angle(13, "147/512", "le")],
        "far13-collision-180": [*upper, angle(13, "147/512", "le")],
        "near13-self-180": near13,
        "r11": near13,
        "r110": [*near13, angle(2, "183/512", "le")],
        "r111": [*near13, angle(2, "183/512", "ge")],
        "near-refined1024-240": [*near13, angle(2, "183/512", "ge")],
    }
    require(headers.keys() == expected.keys(), "capture node inventory differs")
    for name, constraints in expected.items():
        row = headers[name]
        require(row["constraints"] == constraints, f"closed capture conditions differ: {name}")
        require(Q(row["U"]) == cap and Q(row["B"]) == scale, "capture frame differs")
        require(row["mask_index"] == 438 and row["mask"] == mask, "capture mask differs")
    return headers


def reviewed_capture_states(
    graph: dict[str, Any],
    records: dict[str, dict[str, Any]],
    registry: dict[str, tuple[str, str, str]],
) -> list[str]:
    """Join available accepted states; return missing leaf executions explicitly."""
    headers = capture_conditions(graph)
    leaves = {"far15y-self-300": (8, 7), "far13-collision-180": (10, 23), "r110": (8, 10)}
    missing = []
    for path, pin in graph["source_provenance"].items():
        name = Path(path).stem
        accepted = registry.get(pin["decoded_sha256"])
        if accepted is None:
            if name in leaves or name == "near-refined1024-240":
                missing.append(name)
            continue
        receipt = records[accepted[0]]
        header = headers[name]
        # The older root/r1 replay establishes final-state equality internally;
        # later child receipts additionally expose that exact state digest.
        if accepted[1] == "child_source_sha256":
            require(receipt["constraints"] == header["constraints"], "execution branch differs")
            require(
                receipt["final_state_canonical_sha256"] == header["final_state_sha256"],
                "accepted capture final state differs",
            )
        if name in leaves:
            owner, step = leaves[name]
            terminal = receipt["steps"][-1]
            require(
                receipt["terminal_empty_pose_checked"] is True
                and receipt["status"] == "PASS_CHILD_TERMINAL_CONTRADICTION"
                and terminal["owner"] == owner
                and terminal["index"] == step
                and terminal["terminal"] is True
                and terminal["complete"] is True
                and terminal["compressed_additions"] == 0,
                "far leaf lacks accepted empty-pose contradiction",
            )
        if name == "near-refined1024-240":
            require(
                receipt["terminal_empty_pose_checked"] is False
                and header["closed"] is False
                and header["contradiction"] is None
                and receipt["status"] == "PASS_CHILD_NODE_STATE"
                and receipt["steps_checked"] == 121
                and len(receipt["steps"]) == 121
                and [step["index"] for step in receipt["steps"]] == list(range(121))
                and all(step["complete"] is True for step in receipt["steps"]),
                "near conclusion must preserve its feasible residual state",
            )
    return missing


def local_joins(records: dict[str, dict[str, Any]], receipts: Path) -> None:
    """Bind the retained pose extraction to the reviewed local endpoint computation."""
    pose = records["pose-inclusion"]
    local = records["local-isolation"]
    graph = records["source-graph"]
    packing = Path(__file__).resolve().parents[1]
    for relative, fingerprint in local["source_hashes"].items():
        path = (packing / relative).resolve()
        require(path.is_relative_to(packing), "local arithmetic source escaped packing")
        require(
            hashlib.sha256(path.read_bytes()).hexdigest() == fingerprint,
            f"changed local arithmetic source: {relative}",
        )
    require(len(local["source_hashes"]) == 6, "local arithmetic source inventory differs")
    inputs = {
        role: retained_object(
            receipts / "local-dual-residual/objects" / f"{fingerprint}.gz", fingerprint
        )
        for role, fingerprint in local["input_sha256"].items()
    }
    require(set(inputs) == {"weighted", "focused"}, "local input inventory differs")
    radii = inputs["focused"]["radii"]
    require(len(radii) == 33, "local radius count differs")
    near_path = "research/candidate-capture/near-refined1024-240.json"
    require(
        pose["source_sha256"] == graph["source_provenance"][near_path]["decoded_sha256"],
        "pose inclusion uses another near source",
    )
    packed = (receipts / "pose-inclusion/derived-state.json.gz").read_bytes()
    require(
        hashlib.sha256(packed).hexdigest() == pose["derived_state_gzip_sha256"],
        "changed pose extraction archive",
    )
    raw = gzip.decompress(packed)
    require(
        hashlib.sha256(raw).hexdigest() == pose["derived_state_sha256"],
        "changed pose extraction",
    )
    derived = json.loads(raw)
    require(
        derived["final_state"]["guard_source"]["sha256"] == pose["guard_sha256"],
        "pose guard differs",
    )
    require(
        hashlib.sha256((receipts / "pose-inclusion/guard.json").read_bytes()).hexdigest()
        == pose["guard_sha256"],
        "changed role guard",
    )
    require(
        pose["focused_sha256"] == local["input_sha256"]["focused"]
        and pose["root_interval"] == local["root_interval"],
        "local neighborhood differs",
    )
    require(
        pose["source_frame"]
        == {
            "U": "387708359002281417731/100000000000000000000",
            "B": "382000000000000000000/387708359002281417731",
            "inverse": "(yf/B-U/2,U/2-xf/B)",
        },
        "inverse frame differs",
    )
    require(
        [(row["label"], row["owner"]) for row in pose["owners"]]
        == list(enumerate([3, 15, 8, 0, 4, 1, 2, 11, 9, 10, 13])),
        "role bijection differs",
    )
    require(
        [Q(radius) for row in pose["owners"] for radius in row["accepted_radii"]]
        == [Q(radius) for radius in radii],
        "accepted pose radii differ",
    )
    require(
        pose["live_rows_checked"] == 136
        and pose["vertices_checked"] == 1542
        and pose["zero_endpoint_observed"] is True
        and pose["one_endpoint_observed"] is True,
        "closed pose inclusion scope differs",
    )
    require(
        local["fixed_T_local_isolation_proved"] is True
        and local["unavailable_feature_margins_checked"] == 88
        and local["signed_coordinate_margins_checked"] == 8448
        and [row["branch"] for row in local["branch_results"]] == list(range(128))
        and all(row["signed_coordinates_checked"] == 66 for row in local["branch_results"])
        and "root_witness_endpoint" in local["phases"],
        "local endpoint computation scope differs",
    )


def symmetry_join(records: dict[str, dict[str, Any]], receipts: Path) -> None:
    d4 = records["d4-independent"]
    require(
        set(d4["input_sha256"]) == {"cover", "overlay", "distance"},
        "D4 input inventory differs",
    )
    for fingerprint in d4["input_sha256"].values():
        retained_object(receipts / "d4-independent/objects" / f"{fingerprint}.gz", fingerprint)
    require(
        d4["canonical_masks"] == 2184 and d4["raw_masks"] == 4368, "symmetry census differs"
    )
    require(
        [(row["source_canonical_index"], row["status"]) for row in d4["finite_search"]]
        == [(999, "UNSAT"), (1462, "UNSAT"), (1659, "UNSAT")],
        "symmetry search incomplete",
    )


def root_scope(records: dict[str, dict[str, Any]]) -> None:
    chain = records["capture-root-chain"]
    bridge = records["capture-root-bridge-final2"]
    require(
        [row["round"] for row in chain["rounds"]] == list(range(1, 15))
        and chain["rounds"][0]["result_sha256"]
        == "488f26c0effe528f29d2cc06f60766e2c1f845f2aac93f65b18c0c4d3b5e76a4"
        and len(chain["receipt_file_sha256"]) == 168
        and chain["owner_updates"] == 154
        and chain["rows_checked"] == 16551
        and chain["additions"] == 1060,
        "adaptive root execution scope differs",
    )
    require(
        bridge["owner_count"] == 11
        and bridge["phase_two_rows"] == 2036
        and [row["owner"] for row in bridge["owner_census"]]
        == [0, 1, 2, 3, 4, 8, 9, 10, 11, 13, 15],
        "root bridge ownership scope differs",
    )
