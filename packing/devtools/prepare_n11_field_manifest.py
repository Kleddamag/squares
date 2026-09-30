"""Acquire a bounded batch of pinned field proposals; this never accepts a proof.

Greedy selection ranks the pinned A1 case lists against retained completed field
receipts. Selection and grammar admission are not geometric confirmation.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import subprocess
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict
from pathlib import Path
from typing import Any

from devtools import check_n11_optimality_field_mask0 as kernel
from devtools import check_n11_optimality_field_runner as runner

REPO = Path(__file__).resolve().parents[2]
RECEIPTS = kernel.PACKET / "receipts"


def git_bytes(checkout: Path, path: str) -> bytes:
    return subprocess.check_output(
        ["git", "-C", str(checkout), "show", f"{kernel.SOURCE_REVISION}:{path}"], timeout=10
    )


def acquire(checkout: Path, index: dict[str, Any], key: str, objects: Path) -> runner.ObjectPin:
    metadata = index["objects"][key]
    raw_sha = metadata["sha256"]
    object_path = metadata["object"]
    runner.require(
        object_path == f"data/objects/{raw_sha[:2]}/{raw_sha}.gz", "object path differs"
    )
    pointer = git_bytes(checkout, object_path).decode().splitlines()
    runner.require(
        len(pointer) == 3 and pointer[0] == "version https://git-lfs.github.com/spec/v1",
        "not an LFS pointer",
    )
    packed_sha = pointer[1].removeprefix("oid sha256:")
    packed_size = int(pointer[2].removeprefix("size "))
    runner.require(
        0 < packed_size <= 5_000_000 and 0 < metadata["bytes"] <= 20_000_000,
        "field object exceeds intake cap",
    )
    pin = runner.ObjectPin(raw_sha, metadata["bytes"], packed_sha, packed_size)
    target = objects / f"{raw_sha}.gz"
    if not target.exists():
        url = f"https://media.githubusercontent.com/media/Queuingtheorydotcom/11SquaresOptimal/{kernel.SOURCE_REVISION}/{object_path}"
        with urllib.request.urlopen(url, timeout=20) as response:
            packed = response.read(packed_size + 1)
        runner.require(
            len(packed) == packed_size and hashlib.sha256(packed).hexdigest() == packed_sha,
            "compressed source differs",
        )
        raw = gzip.decompress(packed)
        runner.require(
            len(raw) == pin.decoded_bytes and hashlib.sha256(raw).hexdigest() == raw_sha,
            "decoded source differs",
        )
        objects.mkdir(parents=True, exist_ok=True)
        target.open("xb").write(packed)
    kernel.pinned_gzip(
        target,
        packed_bytes=pin.compressed_bytes,
        packed_sha=pin.compressed_sha,
        raw_bytes=pin.decoded_bytes,
        raw_sha=pin.decoded_sha,
    )
    return pin


def prepare(
    entry: dict[str, Any], *, checkout: Path, index: dict[str, Any], output: Path
) -> dict[str, Any]:
    source_sha = entry["source_sha256"]
    root = output / source_sha
    objects = root / "objects"
    result: dict[str, Any] = {
        "source_sha256": source_sha,
        "proposed_case_ids": entry["cases"],
        "geometry_verified": False,
    }
    try:
        packet_pin = acquire(checkout, index, source_sha, objects)
        runner.require(
            packet_pin.decoded_sha == source_sha,
            "A1 packet identity differs from indexed bytes",
        )
        audit_path = Path(entry["fresh_audit"])
        runner.require(
            audit_path.parent.name == "phase3-fresh-fields", "unsupported audit path"
        )
        indexed_path = f"evidence/research/phase3-fresh-fields/{audit_path.name}"
        audit_key = index["files"][indexed_path]
        audit_pin = acquire(checkout, index, audit_key, objects)
        result.update(
            audit_archive_path=indexed_path,
            a1_audit_sha256=entry["fresh_audit_sha256"],
            audit_index_key=audit_key,
            audit_decoded_sha256=audit_pin.decoded_sha,
        )
        packet = kernel.strict_json(
            gzip.decompress((objects / f"{packet_pin.decoded_sha}.gz").read_bytes())
        )
        descriptor = {
            "version": 1,
            "mask_index": packet["mask_index"],
            "packet": asdict(packet_pin),
            "audit": asdict(audit_pin),
        }
        descriptor_path = root / "descriptor.json"
        encoded = json.dumps(descriptor, indent=2, sort_keys=True) + "\n"
        if descriptor_path.exists():
            runner.require(
                descriptor_path.read_text() == encoded, "existing descriptor differs"
            )
        else:
            descriptor_path.write_text(encoded)
        spec = runner.descriptor_spec(descriptor_path, objects, packet["mask_index"])
        cover_path = RECEIPTS / "d4-independent/objects" / f"{kernel.COVER_SHA}.gz"
        packet, audit, cover = runner.load_sources(spec, objects, cover_path)
        runner.admit(spec, packet, audit, cover)
        result.update(
            status="SUPPORTED_PROPOSAL_ONLY",
            mask_index=spec.mask_index,
            descriptor=str(descriptor_path.relative_to(REPO)),
            owners=sum(n for _, n in spec.owner_lengths),
            rows=sum(n for _, n in spec.row_counts),
        )
    except (ValueError, KeyError, TypeError, OSError, subprocess.SubprocessError) as error:
        result.update(status="REFUSED_PROPOSAL", reason=str(error))
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkout", type=Path, default=REPO / "attic/11SquaresOptimal")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--limit", type=int, default=6, choices=range(1, 61))
    args = parser.parse_args()
    output = args.output.resolve()
    runner.require(output.is_relative_to(REPO), "retain unique source evidence in repository")
    index = kernel.strict_json(git_bytes(args.checkout, "data/INDEX.json"))
    baseline = kernel.pinned_gzip(
        RECEIPTS / "case-census/objects" / f"{kernel.A1_SHA}.gz",
        packed_bytes=26100,
        packed_sha=kernel.A1_LFS_SHA,
        raw_bytes=122029,
        raw_sha=kernel.A1_SHA,
    )
    covered: set[int] = set()
    imported: set[str] = set()
    for path in RECEIPTS.glob("*/result.json.gz"):
        value = kernel.strict_json(gzip.decompress(path.read_bytes()))
        if (
            value.get("status") == "PASS_ONE_FIELD_GEOMETRY_AND_TRANSFER"
            and value.get("geometry_verified") is True
        ):
            covered.update(value["transfer"]["transferred_case_ids"])
            imported.add(value["packet_sha256"])
    candidates = [
        entry
        for entry in baseline["certificates"]
        if entry["family"] == "field" and entry["source_sha256"] not in imported
    ]
    selected = []
    proposed_union = set(covered)
    while candidates and len(selected) < args.limit:
        best = max(candidates, key=lambda entry: len(set(entry["cases"]) - proposed_union))
        if not set(best["cases"]) - proposed_union:
            break
        selected.append(best)
        proposed_union.update(best["cases"])
        candidates.remove(best)
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = [
            pool.submit(prepare, entry, checkout=args.checkout, index=index, output=output)
            for entry in selected
        ]
        results = [future.result() for future in futures]
    output.mkdir(parents=True, exist_ok=True)
    report = {
        "status": "INTAKE_ONLY",
        "global_optimality_proved": False,
        "source_revision": kernel.SOURCE_REVISION,
        "fields": results,
    }
    (output / "selection.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    for result in results:
        print(
            json.dumps(
                {key: result[key] for key in result if key != "proposed_case_ids"},
                sort_keys=True,
            )
        )


if __name__ == "__main__":
    main()
