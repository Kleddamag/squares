"""Bind the ten case-438 source-node headers and actual parent graph.

This checks source identities, ordered branch assumptions, and recorded closure
flags. It does not replay the geometric transitions or the external root induction.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import re
import time
from fractions import Fraction
from pathlib import Path
from typing import Any

from devtools import check_n11_optimality_capture_ancestry as capture

Q = Fraction
INDEX_SHA = "29d77766160f3f879d240eaf3fef0b488ec2f21e69f7bad1260b31063ecdf096"
CAPTURE_CHECKER_SHA = "0db9902b9686618bf58bebcaacffbba53e69443e2bf5cc823a7ae53e3b54ba9b"
GUARD_SHA = "0bc2edf59cbf620258719db7ba50cdf77af749d38dfbef76a131d32353443fb0"
ROOT_PATH = (
    "/workspace/eleven-square/research/phase3/work/phase2/conditional/mask438-adaptive.json"
)
SOURCE_PREFIX = "/workspace/eleven-square/"
ALIASES = {
    "root-self-240": "root",
    "far15y-self-300": "far15",
    "far13-collision-180": "far13",
    "near13-self-180": "near13",
    "near-refined1024-240": "near",
}
LEAF_NAMES = {
    "far15": "research/candidate-capture/far15y-self-300.json",
    "far13": "research/candidate-capture/far13-collision-180.json",
    "far2": "research/candidate-capture/tree438-facet/r110.json",
    "near": "research/candidate-capture/near-refined1024-240.json",
}


def require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def stream_sha(stream: Any) -> tuple[str, int]:
    digest = hashlib.sha256()
    size = 0
    for chunk in iter(lambda: stream.read(1024 * 1024), b""):
        size += len(chunk)
        digest.update(chunk)
    return digest.hexdigest(), size


def source_path_for(key: str, near_source: Path, source_dir: Path) -> tuple[Path, Path]:
    name = ALIASES.get(Path(key).stem, Path(key).stem)
    raw = near_source if name == "near" else source_dir / f"{name}.json"
    compressed = near_source.with_suffix(".gz") if name == "near" else source_dir / f"{name}.gz"
    return raw, compressed


def source_header(raw: Path, expected_sha: str) -> dict[str, Any]:
    with raw.open("rb") as stream:
        actual, _ = stream_sha(stream)
    require(actual == expected_sha, f"source decoded identity mismatch: {raw.name}")
    source = json.loads(raw.read_bytes())
    state = source["final_state"]
    require(
        source["mask_index"] == 438 and source["mask"] == state["mask"] == capture.MASK,
        "source case/mask drift",
    )
    require(Q(source["U"]) == Q(state["U"]) == capture.U, "source cap drift")
    require(Q(source["B"]) == Q(state["B"]) == capture.B, "source scale drift")
    require(
        source["constraints"] == state["constraints"], "source/final-state constraints drift"
    )
    require(source["source"] == state["source"], "source/final-state seed drift")
    require(
        source["source"]["path"] == ROOT_PATH
        and source["source"]["sha256"] == capture.ROOT_SOURCE_SHA,
        "source root seed differs",
    )
    require(state["guard_source"]["sha256"] == GUARD_SHA, "source guard identity differs")
    require(source["terminal"] is True, "source node is unfinished")
    contradiction = source["contradiction"]
    if contradiction is not None:
        require(
            contradiction["kind"] == "all_parent_poses_forbidden"
            and 0 <= contradiction["step"] < len(source["steps"]),
            "source contradiction is not a completed whole-branch marker",
        )
    return {
        "node_id": source["node_id"],
        "parent": source["parent"],
        "source": source["source"],
        "mask_index": source["mask_index"],
        "mask": source["mask"],
        "U": source["U"],
        "B": source["B"],
        "constraints": source["constraints"],
        "closed": source["closed"],
        "terminal": source["terminal"],
        "contradiction": contradiction,
        "steps": len(source["steps"]),
        "final_state_sha256": capture.canonical_sha(state),
        "source_guard_sha256": state["guard_source"]["sha256"],
    }


def check_source_graph(
    headers: dict[str, dict[str, Any]], node_hashes: dict[str, str]
) -> dict[str, Any]:
    require(set(headers) == set(node_hashes), "ten-source inventory incomplete")
    root = "research/candidate-capture/root-self-240.json"
    require(
        headers[root]["parent"] is None and headers[root]["constraints"] == [],
        "root has hidden parent or assumption",
    )
    children: dict[str, list[str]] = {key: [] for key in headers}
    for key, header in headers.items():
        if key == root:
            continue
        parent = header["parent"]
        require(isinstance(parent, dict), f"unparented nonroot source: {key}")
        path = parent["path"]
        require(
            isinstance(path, str) and path.startswith(SOURCE_PREFIX),
            "parent path outside source root",
        )
        parent_key = path[len(SOURCE_PREFIX) :]
        require(
            parent_key in headers and parent["sha256"] == node_hashes[parent_key],
            f"missing or changed parent: {key}",
        )
        require(parent_key != key, f"source self-parent: {key}")
        require(
            headers[parent_key]["contradiction"] is None,
            f"continuation after contradiction: {key}",
        )
        parent_cuts = headers[parent_key]["constraints"]
        child_cuts = header["constraints"]
        require(
            child_cuts[: len(parent_cuts)] == parent_cuts,
            f"inherited branch assumption lost or reordered: {key}",
        )
        require(
            0 <= len(child_cuts) - len(parent_cuts) <= 1, f"multiple new branch cuts: {key}"
        )
        children[parent_key].append(key)
    seen: set[str] = set()
    active: set[str] = set()

    def visit(key: str) -> None:
        require(key not in active, f"source parent cycle: {key}")
        if key in seen:
            return
        active.add(key)
        for child in children[key]:
            visit(child)
        active.remove(key)
        seen.add(key)

    visit(root)
    require(seen == set(headers), "source node disconnected from root")
    expected = capture.expected_leaves()
    for name, _predicates, cuts, closure in expected:
        key = LEAF_NAMES[name]
        header = headers[key]
        require(header["constraints"] == cuts, f"{name} actual source leaf cuts differ")
        if closure == "CONTRADICTION":
            require(
                header["closed"] is True and header["contradiction"] is not None,
                f"{name} lacks a reported whole-branch contradiction",
            )
        else:
            require(header["contradiction"] is None, "near source unexpectedly contradictory")
    return {
        "source_nodes_checked": len(headers),
        "actual_parent_edges_checked": len(headers) - 1,
        "root_key": root,
        "source_parent_edges": {
            key: header["parent"]["sha256"] for key, header in headers.items() if key != root
        },
        "far_leaf_contradiction_markers": [
            name
            for name in ("far15", "far13", "far2")
            if headers[LEAF_NAMES[name]]["contradiction"]
        ],
    }


def check_sources(
    packets: dict[str, dict[str, Any]],
    upstream: Path,
    source_dir: Path,
    *,
    near_source: Path,
    near_compressed: Path,
    deadline: float,
) -> dict[str, Any]:
    require(
        capture.digest_file(Path(capture.__file__)) == CAPTURE_CHECKER_SHA,
        "metadata checker semantics changed",
    )
    index_path = upstream / "data/INDEX.json"
    require(capture.digest_file(index_path) == INDEX_SHA, "upstream index identity mismatch")
    index = json.loads(index_path.read_text())
    node_hashes = packets["B1"]["geometry_nodes"]
    headers: dict[str, dict[str, Any]] = {}
    provenance: dict[str, dict[str, Any]] = {}
    for key, expected_sha in node_hashes.items():
        entry_key = index["files"]["evidence/" + key]
        entry = index["objects"][entry_key]
        require(entry["sha256"] == expected_sha, f"index/source digest mismatch: {key}")
        pointer = (upstream / entry["object"]).read_text()
        match = re.fullmatch(
            r"version https://git-lfs.github.com/spec/v1\n"
            r"oid sha256:([0-9a-f]{64})\nsize ([0-9]+)\n?",
            pointer,
        )
        if match is None:
            raise ValueError(f"LFS pointer malformed: {key}")
        compressed_sha, compressed_size = match.group(1), int(match.group(2))
        raw, compressed = source_path_for(key, near_source, source_dir)
        if key == LEAF_NAMES["near"]:
            compressed = near_compressed
        with compressed.open("rb") as stream:
            actual_compressed_sha, actual_compressed_size = stream_sha(stream)
        require(
            actual_compressed_sha == compressed_sha
            and actual_compressed_size == compressed_size,
            f"compressed source identity mismatch: {key}",
        )
        with gzip.open(compressed, "rb") as stream:
            decoded_sha, decoded_size = stream_sha(stream)
        require(
            decoded_sha == expected_sha and decoded_size == entry["bytes"],
            f"decoded LFS source mismatch: {key}",
        )
        require(raw.stat().st_size == decoded_size, f"decoded source size mismatch: {key}")
        headers[key] = source_header(raw, expected_sha)
        provenance[key] = {
            "index_key": entry_key,
            "compressed_object": entry["object"],
            "compressed_sha256": compressed_sha,
            "compressed_bytes": compressed_size,
            "decoded_sha256": expected_sha,
            "decoded_bytes": decoded_size,
        }
        require(time.monotonic() < deadline, f"runtime ceiling expired after {key}")
    graph = check_source_graph(headers, node_hashes)
    claimed_vs_actual = {
        name: {
            "claimed": packets[audit_id]["final_state_sha256"],
            "actual": headers[LEAF_NAMES[name]]["final_state_sha256"],
        }
        for name, audit_id in zip(capture.LEAF_NAMES, capture.LEAF_AUDITS, strict=True)
    }
    return {
        **graph,
        "source_provenance": provenance,
        "source_headers": headers,
        "leaf_final_state_digests": claimed_vs_actual,
        "all_leaf_audit_digests_match": all(
            pair["claimed"] == pair["actual"] for pair in claimed_vs_actual.values()
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packets", type=Path, required=True)
    parser.add_argument("--upstream", type=Path, required=True)
    parser.add_argument("--source-dir", type=Path, required=True)
    parser.add_argument("--near-source", type=Path, required=True)
    parser.add_argument("--near-compressed", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--max-seconds", type=float, default=30.0)
    args = parser.parse_args()
    require(0 < args.max_seconds <= 60, "bounded positive runtime ceiling required")
    start_wall, start_cpu = time.monotonic(), time.process_time()
    packets = capture.load_packets(args.packets)
    reported = capture.check_reported(packets)
    require(
        time.monotonic() - start_wall < args.max_seconds,
        "runtime ceiling expired after metadata",
    )
    metadata_wall, metadata_cpu = time.monotonic() - start_wall, time.process_time() - start_cpu
    source = check_sources(
        packets,
        args.upstream,
        args.source_dir,
        near_source=args.near_source,
        near_compressed=args.near_compressed,
        deadline=start_wall + args.max_seconds,
    )
    require(
        time.monotonic() - start_wall < args.max_seconds,
        "runtime ceiling expired after source graph",
    )
    result = {
        "status": "ACTUAL_SOURCE_PARENT_GRAPH_CHECKED_PUBLIC_AUDIT_BINDING_REFUSED"
        if not source["all_leaf_audit_digests_match"]
        else "ACTUAL_SOURCE_PARENT_GRAPH_CHECKED_GEOMETRY_UNCHECKED",
        "reported_metadata_consistent": True,
        "actual_source_parent_graph_checked": True,
        "root_induction_geometry_proved": False,
        "geometric_capture_proved": False,
        "candidate_mask_capture_proved": False,
        "global_optimality_proved": False,
        "scope": (
            "All ten hash-verified source nodes form the claimed rooted branch-assumption "
            "graph. This structural check does not replay source geometry or the external "
            "mask438-adaptive root induction. Published leaf audit final-state digests "
            "are checked independently and may refuse."
        ),
        "checker_sha256": capture.digest_file(Path(__file__)),
        "capture_checker_sha256": CAPTURE_CHECKER_SHA,
        "upstream_commit": "f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c",
        **reported,
        **source,
        "metadata_wall_seconds": metadata_wall,
        "metadata_process_cpu_seconds": metadata_cpu,
        "wall_seconds": time.monotonic() - start_wall,
        "process_cpu_seconds": time.process_time() - start_cpu,
        "max_seconds": args.max_seconds,
    }
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(
        json.dumps(
            {
                key: result[key]
                for key in (
                    "status",
                    "checker_sha256",
                    "source_nodes_checked",
                    "actual_parent_edges_checked",
                    "leaf_final_state_digests",
                    "wall_seconds",
                    "process_cpu_seconds",
                )
            }
        )
    )
    if not source["all_leaf_audit_digests_match"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
