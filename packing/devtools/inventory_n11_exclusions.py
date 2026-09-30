"""Reconcile reviewed execution records into exact exclusion IDs.

This is bookkeeping, not geometric verification. Its premise is that the listed
executions occurred with the independently reviewed checker revisions. A stored
PASS is not an independent proof of execution or a global optimality proof.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from pathlib import Path
from typing import Any

from strif import atomic_write_text

from devtools.prepare_n11_nonfield_manifest import PACKET, REPO, REVISION, require
from devtools.run_n11_nonfield_batch import complete_case, retain_receipt

FIELD_SHA = "768b7110548ce9200d1a8887e417985d79109e5987ff8e0b2b7dd998976d260e"
MANIFEST_SHA = "a730804aef482e9f32d4b579608a52727b55fa2df8fa4327dfbeae82c0184520"
REVIEWED_CHECKERS = {
    "820f35f7dfeb5ec9dd0cd276305f3e86a230abfccb94ee2a70463682f69d6e15",
    "ac833d5d5e7aa24465697bec14095ac6e5245f35d8ba4993b6375f38370739ab",
    "6294b3eb43727c08635fde1407de6629946e2c2138f6c712150f0b9cf2a8114d",
    "19cf2e57a5647125f8760ad4bf69511beff14c049aee15b731ec0184f5f6245f",
    "da09d08d0e2d6c40755a15a9e9b4a47ae874513463acc9fb44e29f5a821afa2b",
    "722e654fbf426d9db3a799458c075378814da632b29a23c4b514e24a38a19a7c",
    "79473807be4564af6cb13f8c36ad6517b8f077383707513069bc8a5be933fb5c",
    "51c5fcfa802fe9e0ad644efd4bbaa14f132cb4f519e3b3c76ea4ba378686c814",
    "f430580c526c679d0b6a2551799bcec61a3973374fa7d6469064f11c459352cc",
}
PILOTS = {
    "generic-mask2095-intake/full-result.json": (
        2095,
        "2aa9c3819e4f39d9f4f489a25d1885b2a1c5a6f6c21099f42821d1165d608f88",
    ),
    "generic-case2135-pilot/final-result.json": (
        2135,
        "ecd3b2cd820ae92c0770641031a789b25ee9739cdba5f2064232f7b7ace234be",
    ),
    "generic-case2129-repeated/attempt-3.json": (
        2129,
        "69a65557ab5c8b15f90087ecd20c0faca4a983982adc7a509f983d33c8bcea31",
    ),
    "generic-case1687-partner/pilot-fast.json": (
        1687,
        "8566a62979920c37778638a9abbd36b90a4eed503601462bb84d6766a928d8f5",
    ),
    "generic-case1723-chain/pilot-fast-integer.json": (
        1723,
        "14b8676358dd4f9c4b71c6b0c329392ce3ee91895d092027f869d739c63b9eda",
    ),
    "generic-case2053-refined/pilot-fast-integer.json": (
        2053,
        "5296d5061231abc7dd6e13892990575b71e45e74ce35d529779dea1de59461f1",
    ),
}


def read_bound(path: Path, expected: str) -> dict[str, Any]:
    raw = path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == expected, f"binding differs: {path}")
    return json.loads(gzip.decompress(raw) if path.suffix == ".gz" else raw)


def admitted_batch(summary: dict[str, Any], repo: Path = REPO) -> set[int]:
    require(summary["source_revision"] == REVISION, "batch source revision")
    checker = summary["checker_sha256"]
    require(checker in REVIEWED_CHECKERS, "unreviewed checker revision")
    requested = summary["requested_case_ids"]
    require(len(requested) == len(set(requested)), "duplicate requested case")
    results = summary["results"]
    require(
        sorted(row["mask_index"] for row in results) == sorted(requested),
        "missing or duplicate case execution",
    )
    accepted: set[int] = set()
    for row in results:
        case = row["mask_index"]
        if row["status"] != "COMPLETE_CASE":
            require(row["excluded_case_ids"] == [], "incomplete case claims credit")
            continue
        path = (repo / row["receipt"]).resolve()
        require(path.is_relative_to(repo.resolve()), "receipt outside repository")
        record = read_bound(path, row["receipt_sha256"])
        require(complete_case(record, case, checker, row["exit_code"]), "incomplete receipt")
        require(not record.get("pending_row_indices"), "pending rows")
        require(row["excluded_case_ids"] == [case], "execution identity")
        accepted.add(case)
    require(sorted(accepted) == summary["excluded_case_ids"], "batch union differs")
    require(
        sorted(set(requested) - accepted) == summary["remaining_case_ids"],
        "batch remainder differs",
    )
    require(summary["global_optimality_proved"] is False, "batch scope")
    return accepted


def compact_batch(path: Path, repo: Path = REPO) -> None:
    """Rebind losslessly compressed ledgers without changing execution credit."""
    summary = json.loads(path.read_bytes())
    before = admitted_batch(summary, repo)
    originals: list[tuple[Path, str]] = []
    for row in summary["results"]:
        if "receipt" not in row:
            continue
        receipt = (repo / row["receipt"]).resolve()
        require(receipt.is_relative_to(repo.resolve()), "receipt outside repository")
        raw = receipt.read_bytes()
        require(hashlib.sha256(raw).hexdigest() == row["receipt_sha256"], "receipt changed")
        if receipt.suffix == ".gz":
            continue
        retained, fingerprint = retain_receipt(receipt, raw, remove_original=False)
        if retained != receipt:
            originals.append((receipt, hashlib.sha256(raw).hexdigest()))
        row["receipt"] = retained.relative_to(repo.resolve()).as_posix()
        row["receipt_sha256"] = fingerprint
        row["receipt_decoded_sha256"] = hashlib.sha256(raw).hexdigest()
    require(admitted_batch(summary, repo) == before, "compaction changed accepted IDs")
    atomic_write_text(path, json.dumps(summary, indent=2) + "\n")
    for original, fingerprint in originals:
        if hashlib.sha256(original.read_bytes()).hexdigest() == fingerprint:
            original.unlink()


def inventory(batches: list[Path]) -> dict[str, Any]:
    receipts = PACKET / "receipts"
    field = read_bound(receipts / "field-batch-a/field-coverage-inventory.json", FIELD_SHA)
    manifest = read_bound(receipts / "nonfield-manifest/manifest.json.gz", MANIFEST_SHA)
    fields = set(field["previously_accepted_field_case_ids"])
    required_nonfield = {case["mask_index"] for case in manifest["cases"]}
    require(len(fields) == 1904 and len(required_nonfield) == 276, "source partition sizes")
    require(not fields & required_nonfield, "source partition overlap")
    accepted = set(fields)
    bindings = []
    for relative, (case, sha) in PILOTS.items():
        record = read_bound(receipts / relative, sha)
        require(record["excluded_case_ids"] == [case], "pilot identity")
        accepted.add(case)
        bindings.append(
            {"path": (receipts / relative).relative_to(REPO).as_posix(), "sha256": sha}
        )
    for path in batches:
        raw = path.read_bytes()
        accepted |= admitted_batch(json.loads(raw))
        bindings.append(
            {
                "path": path.resolve().relative_to(REPO).as_posix(),
                "sha256": hashlib.sha256(raw).hexdigest(),
            }
        )
    required = fields | required_nonfield
    require(accepted <= required, "credit outside required census")
    remaining = required - accepted
    return {
        "status": "EXECUTION_RECORD_INVENTORY",
        "scope": "Exact union conditional on reviewed actual executions; no geometry rerun",
        "source_revision": REVISION,
        "global_optimality_proved": False,
        "geometry_rerun": False,
        "required_case_count": len(required),
        "accepted_case_count": len(accepted),
        "accepted_case_ids": sorted(accepted),
        "remaining_case_count": len(remaining),
        "remaining_case_ids": sorted(remaining),
        "remaining_by_family": {
            family: sorted(
                case["mask_index"]
                for case in manifest["cases"]
                if case["family"] == family and case["mask_index"] in remaining
            )
            for family in ("A1", "A2", "A3")
        },
        "field_inventory_sha256": FIELD_SHA,
        "nonfield_manifest_sha256": MANIFEST_SHA,
        "execution_record_bindings": bindings,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch", type=Path, action="append", default=[])
    parser.add_argument(
        "--compact-batches",
        action="store_true",
        help="losslessly compress large selected receipts",
    )
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.compact_batches:
        for path in args.batch:
            compact_batch(path)
    result = inventory(args.batch)
    atomic_write_text(args.out, json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {key: result[key] for key in ("accepted_case_count", "remaining_case_count")}
        )
    )


if __name__ == "__main__":
    main()
