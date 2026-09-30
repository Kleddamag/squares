"""Bind the accepted adaptive-root ownership state to capture root-self input.

This checks the exact phase-two owner hulls and row references consumed by the
first phase-three source node. Capture transition geometry remains separate.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import time
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from strif import atomic_write_text

from devtools import check_n11_capture_root_pilot as pilot
from devtools import check_n11_capture_root_round1 as first
from devtools import check_n11_optimality_field_mask0 as geometry

ROOT_SOURCE_SHA = "f9e67f28ea951fb5255c89e33b3ff0e1ee663c7011751761c9200441047b66d4"
ROOT_SOURCE_BYTES = 81_191_153
CHAIN_RESULT_SHA = "f10d50e6b34179a6b2fb066d6ade9553057c280f7538ae6e53fe06e639a56d11"
GRAPH_RESULT_SHA = "cb7ffccf1e3841d44a2dff88549fdee1911805e516f175ef484c5b6e9004b248"
ROOT_KEY = "research/candidate-capture/root-self-240.json"
DEPENDENCY_SHAS = {
    "pilot": "1abfc9244d19fcb38a131c3bee676c8973de991998c1e7ab224fae8196259737",
    "round1": "50eef26bff3aee127e9ad508b1587014514c8e5f1cf9a3214e8ace7a92d88afd",
    "geometry": "75fc0238f2ac91af9dc9cf57bd00792343dcf3321c395adddebf0f3465113ce5",
}


def dependencies_unchanged() -> bool:
    modules = {"pilot": pilot, "round1": first, "geometry": geometry}
    return all(
        module.__file__ is not None
        and pilot.digest(Path(module.__file__)) == DEPENDENCY_SHAS[name]
        for name, module in modules.items()
    )


def require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def extract(path: Path, expression: str) -> dict[str, Any]:
    raw = subprocess.run(
        ["jq", "-c", expression, str(path)],
        capture_output=True,
        check=True,
        timeout=20,
    ).stdout
    return geometry.strict_json(raw)


def check_hulls_and_refs(
    initial: dict[str, Any], owned: list[Any], row_counts: dict[int, int]
) -> list[dict[str, int]]:
    require(
        set(initial["groups"]) == set(initial["cell_references"]) == set(map(str, pilot.MASK)),
        "initial owner inventory differs",
    )
    census: list[dict[str, int]] = []
    for owner in pilot.MASK:
        accepted = pilot.points(owned[owner])
        proposed = pilot.points(initial["groups"][str(owner)])
        require(
            bool(accepted) and pilot.hull(accepted) == pilot.hull(proposed),
            f"owner {owner} initial hull differs from accepted root",
        )
        refs = initial["cell_references"][str(owner)]
        require(
            len(refs) == row_counts[owner]
            and refs
            == [
                {"kind": "phase2", "round": 14, "owner": owner, "row": index}
                for index in range(row_counts[owner])
            ],
            f"owner {owner} initial phase-two row references differ",
        )
        census.append(
            {
                "owner": owner,
                "accepted_points": len(accepted),
                "hull_vertices": len(pilot.hull(accepted)),
                "rows": len(refs),
            }
        )
    return census


def run(args: argparse.Namespace) -> dict[str, Any]:
    began = time.monotonic()
    result: dict[str, Any] = {
        "status": "REFUSED",
        "capture_root_initial_bridge_checked": False,
        "capture_transition_geometry_proved": False,
        "candidate_capture_proved": False,
        "global_optimality_proved": False,
        "checker_sha256": pilot.digest(Path(__file__)),
        "root_source_sha256": ROOT_SOURCE_SHA,
        "adaptive_sha256": pilot.ADAPTIVE_SHA,
        "chain_result_sha256": CHAIN_RESULT_SHA,
        "source_graph_result_sha256": GRAPH_RESULT_SHA,
        "dependency_sha256s": DEPENDENCY_SHAS,
    }
    try:
        require(dependencies_unchanged(), "imported proof dependency changed")
        require(
            pilot.digest(args.chain_result) == CHAIN_RESULT_SHA
            and pilot.digest(args.graph_result) == GRAPH_RESULT_SHA,
            "prior independent receipt changed",
        )
        accepted_chain = geometry.strict_json(args.chain_result.read_bytes())
        graph = geometry.strict_json(args.graph_result.read_bytes())
        require(
            accepted_chain["status"] == "PASS_ROOT_RECEIPT_CHAIN"
            and accepted_chain["root_receipt_chain_verified"] is True
            and accepted_chain["owner_updates"] == 154
            and accepted_chain["rows_checked"] == 16551
            and graph["actual_source_parent_graph_checked"] is True
            and graph["root_key"] == ROOT_KEY
            and graph["source_provenance"][ROOT_KEY]["decoded_sha256"] == ROOT_SOURCE_SHA,
            "root chain or source graph not admitted",
        )
        require(
            args.root_source.is_file()
            and args.root_source.stat().st_size == ROOT_SOURCE_BYTES
            and pilot.digest(args.root_source) == ROOT_SOURCE_SHA,
            "capture root source identity changed",
        )
        require(pilot.digest(args.adaptive) == pilot.ADAPTIVE_SHA, "adaptive source changed")
        root = extract(
            args.root_source,
            "{source,mask_index,mask,U,B,parent,constraints,initial,first_step:(.steps[0]|"
            "{index,owner,prior_owned_hulls,rows:(.rows|map(.prior_reference))})}",
        )
        adaptive = extract(
            args.adaptive,
            "{owned_points,round14_row_counts:(.rounds[13].cells|map({owner,rows:(.rows|length)}))}",
        )
        require(
            root["source"]["sha256"] == pilot.ADAPTIVE_SHA
            and root["mask_index"] == 438
            and tuple(root["mask"]) == pilot.MASK
            and Q(root["U"]) == geometry.U
            and Q(root["B"]) == geometry.B
            and root["parent"] is None
            and root["constraints"] == [],
            "capture root source premises differ",
        )
        row_counts = {item["owner"]: item["rows"] for item in adaptive["round14_row_counts"]}
        require(sorted(row_counts) == list(pilot.MASK), "adaptive final owner inventory")
        owned = adaptive["owned_points"]
        canonical = first.canonical_groups(
            {owner: pilot.points(owned[owner]) for owner in range(16)}
        )
        require(
            hashlib.sha256(json.dumps(canonical, separators=(",", ":")).encode()).hexdigest()
            == accepted_chain["final_state_sha256"],
            "adaptive final state differs from accepted chain",
        )
        census = check_hulls_and_refs(root["initial"], owned, row_counts)
        first_step = root["first_step"]
        owner = first_step["owner"]
        require(
            first_step["index"] == 0
            and owner in pilot.MASK
            and first_step["rows"] == root["initial"]["cell_references"][str(owner)],
            "first capture step does not consume accepted root rows",
        )
        prior = first_step["prior_owned_hulls"]
        require(set(prior) == set(map(str, pilot.MASK)), "first step hull inventory")
        for label in pilot.MASK:
            require(
                pilot.hull(pilot.points(prior[str(label)]))
                == pilot.hull(pilot.points(root["initial"]["groups"][str(label)])),
                f"first step owner {label} hull differs",
            )
        require(
            pilot.digest(args.root_source) == ROOT_SOURCE_SHA
            and pilot.digest(args.adaptive) == pilot.ADAPTIVE_SHA
            and pilot.digest(args.chain_result) == CHAIN_RESULT_SHA
            and pilot.digest(args.graph_result) == GRAPH_RESULT_SHA
            and pilot.digest(Path(__file__)) == result["checker_sha256"],
            "source changed during bridge check",
        )
        require(dependencies_unchanged(), "imported proof dependency changed during check")
        result.update(
            status="PASS_CAPTURE_ROOT_INITIAL_BRIDGE",
            capture_root_initial_bridge_checked=True,
            owner_census=census,
            owner_count=11,
            phase_two_rows=sum(row_counts.values()),
            first_step_owner=owner,
            first_step_rows=len(first_step["rows"]),
        )
    except (
        ValueError,
        KeyError,
        IndexError,
        TypeError,
        OSError,
        subprocess.CalledProcessError,
        subprocess.TimeoutExpired,
    ) as error:
        result["error"] = str(error)
    result["wall_seconds"] = time.monotonic() - began
    atomic_write_text(args.out, json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root-source", type=Path, required=True)
    parser.add_argument("--adaptive", type=Path, required=True)
    parser.add_argument("--chain-result", type=Path, required=True)
    parser.add_argument("--graph-result", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = run(args)
    print(
        json.dumps(
            {
                key: result.get(key)
                for key in (
                    "status",
                    "owner_count",
                    "phase_two_rows",
                    "first_step_rows",
                    "wall_seconds",
                    "error",
                )
            }
        )
    )
    return 0 if result["status"] == "PASS_CAPTURE_ROOT_INITIAL_BRIDGE" else 2


if __name__ == "__main__":
    raise SystemExit(main())
