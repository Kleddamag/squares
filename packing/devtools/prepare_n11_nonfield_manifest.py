"""Bind non-field replay proposals to individual pinned archive objects.

Published audits propose the node order. The geometric consumer must check
actual parent edges, accepted states, and every implication before excluding a
case. This tool neither executes upstream code nor downloads whole ZIP files.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import stat
import subprocess
import time
import urllib.request
from collections import Counter
from fractions import Fraction
from itertools import combinations
from pathlib import Path, PurePosixPath
from typing import Any

from strif import atomic_write_bytes, atomic_write_text

from devtools.check_n11_optimality_field_mask0 import strict_json

REPO = Path(__file__).resolve().parents[2]
REVISION = "f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c"
PACKET = REPO / "packing/resources/web/n11-optimality-2026-09-29"
COVER = "df7938d9ba27095a38fabe45f8b26b259a2cc896c2ae4aac6bae874f417adc4e"
INPUTS = {
    "A1": "04fa1ebb37f5dace29946224fe8c7c5d8a1bedb4fa860c65b359f4200415de57",
    "A2": "719efa40df07d5cb29874a44483737a4903c82498f18b348fc05b5ad08daa8e6",
    "A3": "ba2ba3eae20ffa7b88bbc8e97928a073d7c084d1976211fa16e5e6338860fcc1",
    "assignments": "03d6e82a9bde1bad6cf6683081cff2b583d7f60fddb2c810c91e071cb4575864",
    "A1_recipes": "53ef66cc8c1ee5e937fcd645a7bb831d96a65487b422d52cf67fb7d3c9b4ce61",
    "A2_inventory": "bec43e9ea5d9f3e3dbfdad6a07bf58190ba8edaac815732266a3201b1386b800",
}
U = Fraction(387708359002281417731, 10**20)
B = Fraction(191, 50) / U
DATA_ROLES = {"wall_seed", "producer_node", "producer_parent", "tree_node_source"}


def require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_masks() -> list[list[int]]:
    return [
        list(mask)
        for mask in sorted(
            {
                min(mask, tuple(sorted(15 - owner for owner in mask)))
                for mask in combinations(range(16), 11)
            }
        )
    ]


class Catalog:
    """Resolve immutable Git/LFS identities; fetch only bounded JSON metadata."""

    def __init__(self, checkout: Path, cache: Path, *, fetch: bool, deadline: float) -> None:
        self.checkout, self.cache = checkout, cache
        self.fetch, self.deadline = fetch, deadline
        self.index_raw = self.git_bytes("data/INDEX.json")
        self.index = strict_json(self.index_raw)
        self.by_sha: dict[str, list[str]] = {}
        self.objects: dict[str, dict[str, Any]] = {}
        self.loaded: dict[str, dict[str, Any]] = {}
        self.loaded_paths: dict[Path, str] = {}
        self.downloaded_bytes = 0
        for key, value in self.index["objects"].items():
            if value["kind"] == "blob":
                self.by_sha.setdefault(value["sha256"], []).append(key)

    def remaining(self) -> float:
        remaining = self.deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError("non-field manifest ceiling")
        return remaining

    def git_bytes(self, path: str) -> bytes:
        return subprocess.check_output(
            ["git", "-C", str(self.checkout), "show", f"{REVISION}:{path}"],
            timeout=min(10, self.remaining()),
        )

    def pin(self, fingerprint: str) -> dict[str, Any]:
        if fingerprint in self.objects:
            return self.objects[fingerprint]
        keys = sorted(self.by_sha.get(fingerprint, []))
        require(bool(keys), f"missing individual blob: {fingerprint}")
        entry = self.index["objects"][keys[0]]
        require(
            all(self.index["objects"][key] == entry for key in keys),
            "conflicting content-index aliases",
        )
        path = f"data/objects/{fingerprint[:2]}/{fingerprint}.gz"
        require(entry["object"] == path, "unexpected object path")
        lines = self.git_bytes(path).decode("ascii").splitlines()
        require(
            len(lines) == 3
            and lines[0] == "version https://git-lfs.github.com/spec/v1"
            and lines[1].startswith("oid sha256:")
            and lines[2].startswith("size "),
            "invalid pinned LFS pointer",
        )
        pin = {
            "index_keys": keys,
            "object_path": path,
            "decoded_sha256": fingerprint,
            "decoded_bytes": entry["bytes"],
            "compressed_sha256": lines[1].removeprefix("oid sha256:"),
            "compressed_bytes": int(lines[2].removeprefix("size ")),
        }
        require(
            type(pin["decoded_bytes"]) is int and pin["decoded_bytes"] > 0,
            "invalid indexed size",
        )
        self.objects[fingerprint] = pin
        return pin

    def metadata(self, fingerprint: str) -> dict[str, Any]:
        if fingerprint in self.loaded:
            return self.loaded[fingerprint]
        pin = self.pin(fingerprint)
        require(
            pin["decoded_bytes"] <= 2_000_000 and pin["compressed_bytes"] <= 300_000,
            "metadata object exceeds selected bound",
        )
        candidates = [
            self.cache / f"{fingerprint}.gz",
            PACKET / "receipts/case-census/objects" / f"{fingerprint}.gz",
        ]
        path = next((path for path in candidates if path.is_file()), candidates[0])
        if not path.is_file():
            require(self.fetch, f"missing metadata object {fingerprint}; use --fetch-metadata")
            url = (
                "https://media.githubusercontent.com/media/Queuingtheorydotcom/"
                f"11SquaresOptimal/{REVISION}/{pin['object_path']}"
            )
            with urllib.request.urlopen(url, timeout=min(20, self.remaining())) as response:
                packed = response.read(pin["compressed_bytes"] + 1)
            require(
                len(packed) == pin["compressed_bytes"]
                and digest(packed) == pin["compressed_sha256"],
                "downloaded metadata identity differs",
            )
            self.downloaded_bytes += len(packed)
            require(self.downloaded_bytes <= 3_000_000, "metadata download budget exceeded")
            self.cache.mkdir(parents=True, exist_ok=True)
            atomic_write_bytes(path, packed)
        packed = path.read_bytes()
        require(
            len(packed) == pin["compressed_bytes"]
            and digest(packed) == pin["compressed_sha256"],
            "cached compressed identity differs",
        )
        with gzip.GzipFile(fileobj=io.BytesIO(packed)) as stream:
            raw = stream.read(pin["decoded_bytes"] + 1)
        require(
            len(raw) == pin["decoded_bytes"] and digest(raw) == fingerprint,
            "decoded metadata identity differs",
        )
        result = strict_json(raw)
        self.loaded[fingerprint] = result
        self.loaded_paths[path] = pin["compressed_sha256"]
        self.remaining()
        return result


def ordered_nodes(audit: dict[str, Any], terminal: str, *, tree: bool) -> list[dict[str, Any]]:
    nodes = audit["nodes"]
    require(isinstance(nodes, list) and bool(nodes), "missing node inventory")
    hashes = [node["sha256"] for node in nodes]
    require(len(hashes) == len(set(hashes)), "duplicate ancestry node")
    if not tree:
        require(hashes[-1] == terminal, "terminal is not last in declared ancestry")
    result = []
    for position, node in enumerate(nodes):
        require(
            all(
                type(node[key]) is int and node[key] >= 0
                for key in ("complete_steps", "rows", "arrangement_slabs")
            ),
            "invalid reported work counts",
        )
        result.append(
            {
                "position": position,
                "source_sha256": node["sha256"],
                "node_id": node["node"],
                "historical_path": node["path"],
                "constraints_proposal": node["constraints"],
                "reported_rows": node["rows"],
                "reported_complete_steps": node["complete_steps"],
                "reported_arrangement_slabs": node["arrangement_slabs"],
            }
        )
    return result


def returned_transport(
    case: dict[str, Any], index: dict[str, Any], node_hashes: set[str], seed: str
) -> list[dict[str, Any]]:
    """Cross-bind the case plan to indexed ZIP members without obtaining the ZIP."""
    archive_key = index["files"]["evidence/" + case["archive"]]
    archive = index["objects"][archive_key]
    require(archive["kind"] == "zip", "returned container is not an indexed ZIP")
    members = archive["members"]
    by_name = {member["name"]: member for member in members}
    require(len(by_name) == len(members), "duplicate archive member")
    result = []
    destinations: set[str] = set()
    declared_nodes: set[str] = set()
    counts: Counter[str] = Counter()
    for item in case["stream_extract_members"]:
        name = PurePosixPath(item["member"])
        destination = item["destination_name"]
        require(
            not name.is_absolute()
            and ".." not in name.parts
            and destination == name.name
            and destination not in destinations,
            "unsafe or ambiguous member destination",
        )
        destinations.add(destination)
        member = by_name[str(name)]
        entry = index["objects"][member["source"]]
        require(
            type(member["mode"]) is int
            and member["mode"] >= 0
            and stat.S_IFMT(member["mode"]) in (0, stat.S_IFREG)
            and entry["kind"] == "blob"
            and entry["sha256"] == item["expected_sha256"]
            and entry["bytes"] == item["bytes"],
            "member identity or byte length differs",
        )
        role = item["role"]
        counts[role] += 1
        if role == "ancestry_node":
            require(entry["sha256"] not in declared_nodes, "duplicate declared ancestor")
            declared_nodes.add(entry["sha256"])
        else:
            expected = {
                "wall_seed": seed,
                "cover": COVER,
                "saved_audit": case["saved_audit_sha256"],
            }
            require(role in expected and entry["sha256"] == expected[role], "wrong member role")
        result.append(dict(item, index_key=member["source"]))
    require(
        counts["wall_seed"] == counts["cover"] == counts["saved_audit"] == 1
        and declared_nodes == node_hashes,
        "returned plan omits or adds a proof premise",
    )
    return result


def build(catalog: Catalog) -> dict[str, Any]:
    inputs = {name: catalog.metadata(value) for name, value in INPUTS.items()}
    a1, a2, a3 = (inputs[key] for key in ("A1", "A2", "A3"))
    masks = canonical_masks()
    fields = set().union(
        *(set(row["cases"]) for row in a1["certificates"] if row["family"] == "field")
    )
    require(len(fields) == 1904, "source field union differs")
    a1_recipes = {row["source_sha256"]: row for row in inputs["A1_recipes"]["generic_recipes"]}
    selected: list[tuple[str, dict[str, Any]]] = [
        ("A1", row)
        for row in a1["certificates"]
        if row["family"] == "generic" and set(row["cases"]) - fields
    ]
    selected += [("A2", row) for row in a2["extension_entries"]]
    selected += [("A3", row) for row in a3["cases"]]
    recipes: list[dict[str, Any]] = []
    for family, row in selected:
        catalog.remaining()
        audit_sha = row[
            {"A1": "fresh_audit_sha256", "A2": "audit_sha256", "A3": "saved_audit_sha256"}[
                family
            ]
        ]
        audit = catalog.metadata(audit_sha)
        source = row["source_sha256"]
        index = (
            row["cases"][0]
            if family == "A1"
            else row["mask"]
            if family == "A2"
            else row["mask_index"]
        )
        require(type(index) is int and 0 <= index < len(masks), "case index outside census")
        kind = row["kind"] if family == "A2" else "direct_v6" if family == "A1" else "direct_v9"
        require(
            kind
            in {
                "direct_v6",
                "direct_v9",
                "native_cached_v9",
                "native_cached_v4_center_partition",
                "necessary_D4_cuts_and_independent_geometry",
            },
            "unsupported source profile",
        )
        tree = kind == "native_cached_v4_center_partition"
        d4 = kind == "necessary_D4_cuts_and_independent_geometry"
        auxiliary: set[str] = set()
        geometry_audit = audit
        if d4:
            geometry_audit = catalog.metadata(audit["geometric_audit_sha256"])
            auxiliary.update(
                audit[key]
                for key in (
                    "geometric_audit_sha256",
                    "source_hulls_sha256",
                    "support_replay_sha256",
                    "geometry_replay_sha256",
                    "baseline_sha256",
                )
            )
        require(
            geometry_audit["mask_index"] == index
            and geometry_audit["mask"] == masks[index]
            and Fraction(geometry_audit["parent_Uplus"]) == U
            and Fraction(geometry_audit["parent_side"]) == B
            and geometry_audit["cover_sha256"] == COVER
            and geometry_audit["root_audit_sha256"] is None,
            "audit case, seed profile, or exact domain differs",
        )
        require(
            audit["tree_sha256" if tree else "source_sha256"] == source,
            "selected source binding differs",
        )
        if not tree:
            require(
                geometry_audit["bootstrap"]["kind"] == "independently_verified_wall_seed",
                "unsupported seed",
            )
            require(geometry_audit["source_sha256"] == source, "geometry source differs")
            if not d4:
                require(geometry_audit["constraints"] == [], "unexpected conditional source")
        seed = geometry_audit["root_sha256"]
        nodes = ordered_nodes(geometry_audit, source, tree=tree)
        node_hashes = {node["source_sha256"] for node in nodes}
        recipe: dict[str, Any] = {
            "mask_index": index,
            "mask": masks[index],
            "family": family,
            "source_profile": kind,
            "adapter": "closed_center_partition"
            if tree
            else "baseline_necessary_d4"
            if d4
            else "sequential_wall_seed",
            "source_sha256": source,
            "seed_sha256": seed,
            "audit_sha256": audit_sha,
            "ordered_ancestry_proposal": nodes,
            "actual_parent_edges_verified": False,
            "geometry_verified": False,
            "cached_receipts_authoritative": False,
        }
        if family == "A1":
            prior = a1_recipes[source]
            require(
                row["cases"] == [index]
                and prior["root_sha256"] == seed
                and [node["sha256"] for node in prior["nodes"]]
                == [node["source_sha256"] for node in nodes],
                "A1 recipe ancestry differs from fresh audit",
            )
        elif family == "A2":
            proposed = {
                file["expected_sha256"]
                for file in inputs["A2_inventory"]["files"]
                if index in file["used_by"] and DATA_ROLES.intersection(file["roles"])
            }
            require(
                proposed == node_hashes | {seed},
                "A2 source inventory differs from node/seed closure",
            )
            if tree:
                recipe["partition_proposal"] = catalog.metadata(source)
            if d4:
                recipe["required_baseline_cases"] = 1931
                recipe["necessity_premises_verified"] = False
        else:
            require(row["root_sha256"] == seed, "returned seed differs")
            jobs = [
                job for job in inputs["assignments"]["jobs"] if job["job_id"] == row["job_id"]
            ]
            require(
                len(jobs) == 1 and index in jobs[0]["mask_indices"],
                "case job assignment differs",
            )
            recipe["job_id"] = row["job_id"]
            recipe["archive"] = row["archive"]
            recipe["transport_members"] = returned_transport(
                row, catalog.index, node_hashes, seed
            )
        required = sorted(node_hashes | {seed, source, COVER, audit_sha} | auxiliary)
        for fingerprint in required:
            catalog.pin(fingerprint)
        recipe["required_object_sha256s"] = required
        recipe["reported_rows"] = sum(node["reported_rows"] for node in nodes)
        recipe["declared_compressed_bytes"] = sum(
            catalog.objects[key]["compressed_bytes"] for key in required
        )
        recipe["declared_decoded_bytes"] = sum(
            catalog.objects[key]["decoded_bytes"] for key in required
        )
        recipes.append(recipe)
    indices = [recipe["mask_index"] for recipe in recipes]
    require(
        len(indices) == len(set(indices)) == 276
        and set(indices) == set(range(2184)) - fields - {438, 999, 1462, 1659}
        and Counter(recipe["family"] for recipe in recipes) == {"A1": 27, "A2": 76, "A3": 173},
        "non-field recipes do not cover the exact remaining census",
    )
    return {
        "schema": "n11-nonfield-proposals-v1",
        "status": "COMPLETE_METADATA_RECIPES_ONLY",
        "source_revision": REVISION,
        "index_sha256": digest(catalog.index_raw),
        "input_sha256s": INPUTS,
        "geometry_verified": False,
        "actual_parent_edges_verified": False,
        "global_optimality_proved": False,
        "ancestry_basis": (
            "Pinned published audit replay order; actual source parent edges must be "
            "checked by the geometric consumer."
        ),
        "objects": dict(sorted(catalog.objects.items())),
        "cases": sorted(recipes, key=lambda recipe: recipe["mask_index"]),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkout", type=Path, default=REPO / "attic/11SquaresOptimal")
    parser.add_argument("--metadata-cache", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--fetch-metadata", action="store_true")
    parser.add_argument("--max-seconds", type=float, default=120)
    args = parser.parse_args()
    require(0 < args.max_seconds <= 300, "manifest ceiling must be in (0,300]")
    require(not args.output.exists(), "use a new output directory for frozen recipes")
    started = time.monotonic()
    source = Path(__file__).read_bytes()
    catalog = Catalog(
        args.checkout,
        args.metadata_cache,
        fetch=args.fetch_metadata,
        deadline=started + args.max_seconds,
    )
    result = build(catalog)
    require(Path(__file__).read_bytes() == source, "builder changed during intake")
    require(
        all(digest(path.read_bytes()) == sha for path, sha in catalog.loaded_paths.items()),
        "metadata changed during intake",
    )
    catalog.remaining()
    result["builder_sha256"] = digest(source)
    raw = json.dumps(result, sort_keys=True, separators=(",", ":")).encode() + b"\n"
    packed = gzip.compress(raw, mtime=0)
    cases = result["cases"]
    proof_objects = {sha for case in cases for sha in case["required_object_sha256s"]}
    summary = {
        "status": result["status"],
        "source_revision": REVISION,
        "index_sha256": result["index_sha256"],
        "cases": len(cases),
        "family_counts": dict(Counter(case["family"] for case in cases)),
        "adapter_counts": dict(Counter(case["adapter"] for case in cases)),
        "unique_required_objects": len(proof_objects),
        "declared_unique_compressed_bytes": sum(
            catalog.objects[sha]["compressed_bytes"] for sha in proof_objects
        ),
        "declared_unique_decoded_bytes": sum(
            catalog.objects[sha]["decoded_bytes"] for sha in proof_objects
        ),
        "metadata_objects_read": len(catalog.loaded),
        "metadata_downloaded_bytes_this_run": catalog.downloaded_bytes,
        "manifest_sha256": digest(raw),
        "manifest_gzip_sha256": digest(packed),
        "builder_sha256": digest(source),
        "geometry_verified": False,
        "actual_parent_edges_verified": False,
        "global_optimality_proved": False,
        "wall_seconds": time.monotonic() - started,
    }
    args.output.mkdir(parents=True)
    atomic_write_bytes(args.output / "manifest.json.gz", packed)
    atomic_write_text(
        args.output / "summary.json", json.dumps(summary, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
