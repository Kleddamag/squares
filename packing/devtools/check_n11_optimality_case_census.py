"""Independently audit the published n=11 case census, not its geometry.

Five pinned public objects describe baseline, prior-extension, and returned-case
coverage. This checker reconstructs the 16-cell mask universe and checks membership,
certificate inventories, source bindings, and job assignments. A passing census does
not verify any exclusion certificate or prove global optimality.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import math
import re
import sys
import time
from collections import Counter
from fractions import Fraction
from itertools import combinations
from pathlib import Path
from typing import Any, NamedTuple

REPO = Path(__file__).resolve().parents[2]
PACKET = REPO / "packing/resources/web/n11-optimality-2026-09-29"
SOURCE_REVISION = "f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c"
INDEX_SHA256 = "29d77766160f3f879d240eaf3fef0b488ec2f21e69f7bad1260b31063ecdf096"
SURVIVORS = (438, 999, 1462, 1659)
EXPECTED_MASKS = {
    438: (0, 1, 2, 3, 4, 8, 9, 10, 11, 13, 15),
    999: (0, 1, 2, 4, 6, 7, 9, 10, 12, 14, 15),
    1462: (0, 1, 3, 5, 6, 8, 9, 11, 12, 13, 14),
    1659: (0, 2, 3, 4, 5, 6, 7, 11, 12, 13, 14),
}
U = Fraction(387708359002281417731, 10**20)
L = Fraction(191, 50)
B = L / U


class ObjectPin(NamedTuple):
    decoded_path: str
    index_key: str
    decoded_sha256: str
    decoded_bytes: int
    object_path: str
    lfs_sha256: str
    compressed_bytes: int


PINS = {
    "A1": ObjectPin(
        "evidence/research/PHASE3_FRESH_REPLAY_RESULT.json",
        "60add61f5efc56652a350944ad34cafd19d9c590f058ebaad2d98d8854be9538",
        "04fa1ebb37f5dace29946224fe8c7c5d8a1bedb4fa860c65b359f4200415de57",
        122029,
        "data/objects/04/04fa1ebb37f5dace29946224fe8c7c5d8a1bedb4fa860c65b359f4200415de57.gz",
        "adbb5f181a18d157fe12a5a62055b01bf7eff7a91ce08b8aeca6f01408953d21",
        26100,
    ),
    "A2": ObjectPin(
        "evidence/results/prior-union/PRIOR_UNION_RESULT.json",
        "d3c8a8f207c986462c6c85d399b739fce7841e0adaff6b75801ac171bc319db4",
        "719efa40df07d5cb29874a44483737a4903c82498f18b348fc05b5ad08daa8e6",
        270956,
        "data/objects/71/719efa40df07d5cb29874a44483737a4903c82498f18b348fc05b5ad08daa8e6.gz",
        "e42dc34909640e073110f2a9cf1526a3258c371f8dc5ab3776162e0ad3d16740",
        25401,
    ),
    "A3": ObjectPin(
        "evidence/inputs/returned-replay-plan.json",
        "ba2ba3eae20ffa7b88bbc8e97928a073d7c084d1976211fa16e5e6338860fcc1",
        "ba2ba3eae20ffa7b88bbc8e97928a073d7c084d1976211fa16e5e6338860fcc1",
        401045,
        "data/objects/ba/ba2ba3eae20ffa7b88bbc8e97928a073d7c084d1976211fa16e5e6338860fcc1.gz",
        "965718825788759fa51c033382fa569fae7e055b991316a1646f18532c36976e",
        45515,
    ),
    "A4": ObjectPin(
        "evidence/inputs/CASE_ASSIGNMENTS.json",
        "3f5ce8ccd45268a34f567f87897640255ea946dec3e43f1bca161a951806f0d1",
        "03d6e82a9bde1bad6cf6683081cff2b583d7f60fddb2c810c91e071cb4575864",
        37021,
        "data/objects/03/03d6e82a9bde1bad6cf6683081cff2b583d7f60fddb2c810c91e071cb4575864.gz",
        "dba5a74b7652c38e990163e857013b457ccc6cee0b71d3930a228c4cb2029159",
        2762,
    ),
    "A5": ObjectPin(
        "evidence/results/returned/SUMMARY.json",
        "8147c29389e597227ddee71ebacafe7358b0fd6b8e07885fb0e0ff0ab860a3cb",
        "7920ae9fede574c58ea36893724a55911a02f2875dd808f799a99fd3ea0ee18e",
        2257,
        "data/objects/79/7920ae9fede574c58ea36893724a55911a02f2875dd808f799a99fd3ea0ee18e.gz",
        "405c171283f9b68afc43e2c2a7b029d7dcb7acafe05552c8cb81def04921506f",
        763,
    ),
}
COVER_SHA256 = "df7938d9ba27095a38fabe45f8b26b259a2cc896c2ae4aac6bae874f417adc4e"
COVER_LFS_SHA256 = "7c6d14012f06eb892912a50c93cc7408ce1f90524d46693c6178a01ceae71a99"
COVER_BYTES = 773471
COVER_COMPRESSED_BYTES = 25016


def require(condition: object, reason: str) -> None:
    if not condition:
        raise ValueError(reason)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def strict_json(data: bytes) -> dict[str, Any]:
    def no_duplicate(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in result, f"duplicate JSON key {key!r}")
            result[key] = value
        return result

    value: Any = json.loads(data, object_pairs_hook=no_duplicate)
    require(isinstance(value, dict), "JSON root is not an object")
    return value


def bounded_gzip(data: bytes, *, decoded_size: int, label: str) -> bytes:
    with gzip.GzipFile(fileobj=io.BytesIO(data)) as source:
        decoded = source.read(decoded_size + 1)
        require(len(decoded) == decoded_size, f"{label}: decoded size mismatch")
        require(not source.read(1), f"{label}: decoded size exceeded")
    return decoded


def check_deadline(deadline: float, phase: str) -> None:
    if time.monotonic() >= deadline:
        raise TimeoutError(f"wall ceiling reached before {phase}")


def packed_json(
    path: Path,
    *,
    compressed_sha: str,
    compressed_size: int,
    decoded_sha: str,
    decoded_size: int,
) -> dict[str, Any]:
    require(path.is_file(), f"missing pinned object: {path}")
    require(path.stat().st_size == compressed_size, f"compressed size mismatch: {path}")
    packed = path.read_bytes()
    require(digest(packed) == compressed_sha, f"compressed SHA-256 mismatch: {path}")
    data = bounded_gzip(packed, decoded_size=decoded_size, label=str(path))
    require(digest(data) == decoded_sha, f"decoded SHA-256 mismatch: {path}")
    return strict_json(data)


def load_inputs(
    packet: Path, object_dir: Path, cover_path: Path
) -> tuple[dict[str, Any], dict[str, Any]]:
    index_path = packet / "source/data/INDEX.json.gz"
    require(
        index_path.is_file() and index_path.stat().st_size < 500_000,
        "index missing or oversized",
    )
    index_data = bounded_gzip(
        index_path.read_bytes(), decoded_size=1_316_778, label="source index"
    )
    require(digest(index_data) == INDEX_SHA256, "pinned content index changed")
    index = strict_json(index_data)
    pointer_path = packet / "lfs-pointer-inventory.json.gz"
    require(
        pointer_path.is_file() and pointer_path.stat().st_size < 500_000,
        "pointer inventory missing or oversized",
    )
    pointer_data = bounded_gzip(
        pointer_path.read_bytes(), decoded_size=624_725, label="pointer inventory"
    )
    pointers = strict_json(pointer_data)
    require(
        pointers.get("source_revision") == SOURCE_REVISION, "pointer source revision changed"
    )
    pointer_by_path = {row["path"]: row for row in pointers["objects"]}
    require(len(pointer_by_path) == len(pointers["objects"]), "duplicate pointer path")
    records: dict[str, Any] = {}
    for name, pin in PINS.items():
        require(
            index["files"].get(pin.decoded_path) == pin.index_key, f"{name}: index key changed"
        )
        entry = index["objects"][pin.index_key]
        require(
            entry
            == {
                "bytes": pin.decoded_bytes,
                "kind": "blob",
                "object": pin.object_path,
                "sha256": pin.decoded_sha256,
            },
            f"{name}: indexed object identity changed",
        )
        pointer = pointer_by_path[pin.object_path]
        require(
            pointer["oid_sha256"] == pin.lfs_sha256
            and pointer["declared_size_bytes"] == pin.compressed_bytes,
            f"{name}: LFS pointer identity changed",
        )
        records[name] = packed_json(
            object_dir / f"{pin.decoded_sha256}.gz",
            compressed_sha=pin.lfs_sha256,
            compressed_size=pin.compressed_bytes,
            decoded_sha=pin.decoded_sha256,
            decoded_size=pin.decoded_bytes,
        )
    cover = packed_json(
        cover_path,
        compressed_sha=COVER_LFS_SHA256,
        compressed_size=COVER_COMPRESSED_BYTES,
        decoded_sha=COVER_SHA256,
        decoded_size=COVER_BYTES,
    )
    return records, cover


def checked_ids(value: Any, label: str, *, count: int | None = None) -> list[int]:
    require(isinstance(value, list), f"{label}: case IDs must be a list")
    require(
        all(type(item) is int and 0 <= item < 2184 for item in value),
        f"{label}: noninteger or out-of-range case ID",
    )
    duplicates = sorted(item for item, amount in Counter(value).items() if amount > 1)
    require(not duplicates, f"{label}: duplicate case IDs {duplicates}")
    if count is not None:
        require(len(value) == count, f"{label}: expected {count} IDs, got {len(value)}")
    return value


def same_ids(actual: set[int], expected: set[int], label: str) -> None:
    missing, unexpected = sorted(expected - actual), sorted(actual - expected)
    require(
        not missing and not unexpected, f"{label}: missing={missing}, unexpected={unexpected}"
    )


def hash_field(row: dict[str, Any], key: str, label: str) -> str:
    value = row.get(key)
    if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
        raise ValueError(f"{label}: invalid {key}")
    return value


def text_field(row: dict[str, Any], key: str, label: str) -> str:
    value = row.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"{label}: missing {key}")
    return value


def mask_universe(cover: dict[str, Any]) -> list[tuple[int, ...]]:
    raw = list(combinations(range(16), 11))
    canonical = sorted({min(mask, tuple(sorted(15 - cell for cell in mask))) for mask in raw})
    require(len(raw) == 4368 and len(canonical) == 2184, "mask universe count changed")
    require(cover.get("number_of_cells") == 16, "cover cell count changed")
    require(cover.get("eleven_cell_selections") == 4368, "cover raw count changed")
    require(
        cover.get("canonical_eleven_cell_selections") == 2184, "cover canonical count changed"
    )
    require(
        cover.get("symmetry_cell_involution") == list(reversed(range(16))),
        "cover half-turn involution changed",
    )
    require(
        cover.get("all_eleven_cell_subsets") == [list(mask) for mask in raw],
        "cover raw mask array changed",
    )
    require(
        cover.get("canonical_eleven_cell_subsets") == [list(mask) for mask in canonical],
        "cover canonical mask array changed",
    )
    require(Fraction(cover["side_upper"]) >= U, "cover side upper is below U")
    require(
        {index: canonical[index] for index in SURVIVORS} == EXPECTED_MASKS,
        "four survivor masks changed",
    )
    return canonical


def audit_records(
    records: dict[str, Any], cover: dict[str, Any], deadline: float
) -> dict[str, Any]:
    canonical = mask_universe(cover)
    all_ids = set(range(len(canonical)))
    a1, a2, a3, a4, a5 = (records[name] for name in PINS)
    check_deadline(deadline, "baseline audit")
    require(
        a1.get("status") == "PASS_FRESH_INDEPENDENT_1931_CASE_UNION", "A1 format/status changed"
    )
    require(a1.get("cover_sha256") == COVER_SHA256, "A1 cover binding changed")
    require(Fraction(a1["parent_Uplus"]) == U, "A1 U premise changed")
    require(Fraction(a1["parent_side"]) == B, "A1 B=L/U premise changed")
    baseline = set(
        checked_ids(a1["excluded_canonical_mask_indices"], "A1 baseline", count=1931)
    )
    remaining = set(
        checked_ids(a1["remaining_canonical_mask_indices"], "A1 remaining", count=253)
    )
    same_ids(remaining, all_ids - baseline, "A1 baseline complement")
    require(
        a1.get("excluded") == 1931 and a1.get("remaining") == 253, "A1 declared counts changed"
    )
    certificates = a1["certificates"]
    require(
        isinstance(certificates, list) and len(certificates) == 93,
        "A1 certificate inventory changed",
    )
    field_union: set[int] = set()
    generic_union: set[int] = set()
    counts: Counter[str] = Counter()
    identities: set[tuple[str, str, str]] = set()
    for number, certificate in enumerate(certificates):
        label = f"A1 certificate {number}"
        family = certificate.get("family")
        require(family in ("field", "generic"), f"{label}: unknown family")
        counts[family] += 1
        source = text_field(certificate, "source", label)
        source_hash = hash_field(certificate, "source_sha256", label)
        text_field(certificate, "fresh_audit", label)
        hash_field(certificate, "fresh_audit_sha256", label)
        identity = family, source, source_hash
        require(identity not in identities, f"{label}: duplicate certificate identity")
        identities.add(identity)
        supported = set(checked_ids(certificate["cases"], f"{label} cases"))
        require(bool(supported), f"{label}: no supported case")
        if family == "field":
            field_union.update(supported)
        else:
            require(len(supported) == 1, f"{label}: generic certificate is not single-case")
            generic_union.update(supported)
    require(counts == {"field": 59, "generic": 34}, f"A1 family counts changed: {dict(counts)}")
    require(len(field_union) == a1.get("field_cases") == 1904, "A1 field union changed")
    require(len(generic_union) == a1.get("generic_cases") == 34, "A1 generic support changed")
    require(len(generic_union - field_union) == 27, "A1 new generic cases changed")
    same_ids(field_union | generic_union, baseline, "A1 certificate union")
    check_deadline(deadline, "prior-extension audit")
    require(
        a2.get("status") == "PASS_STRICT_PRIOR_76_EXTENSION_INTEGRATION",
        "A2 format/status changed",
    )
    snapshot_hash = hash_field(a1, "authoritative_snapshot_sha256", "A1")
    require(a2.get("baseline_sha256") == snapshot_hash, "A2 baseline source binding changed")
    require(a2.get("baseline_excluded") == 1931, "A2 baseline count changed")
    require(
        a2.get("fresh_baseline_replay", {}).get("sha256") == PINS["A1"].decoded_sha256,
        "A2 fresh baseline replay binding changed",
    )
    extensions = a2["extension_entries"]
    require(
        isinstance(extensions, list) and len(extensions) == 76, "A2 extension inventory changed"
    )
    extension_ids: set[int] = set()
    extension_audits: dict[int, str] = {}
    for number, entry in enumerate(extensions):
        label = f"A2 extension {number}"
        case = entry.get("mask")
        checked_ids([case], label, count=1)
        require(
            entry.get("cases") == [case] and entry.get("new_cases") == [case],
            f"{label}: not one new case",
        )
        require(case not in extension_ids, f"A2 duplicate extension case ID {case}")
        require(case not in baseline, f"A2 extension overlaps baseline: {case}")
        extension_ids.add(case)
        text_field(entry, "source", label)
        hash_field(entry, "source_sha256", label)
        text_field(entry, "audit", label)
        extension_audits[case] = hash_field(entry, "audit_sha256", label)
    require(
        a2.get("extension_receipts") == 76 and a2.get("distinct_extension_cases") == 76,
        "A2 declared extension counts changed",
    )
    prior = set(
        checked_ids(a2["excluded_canonical_mask_indices"], "A2 prior union", count=2007)
    )
    same_ids(prior, baseline | extension_ids, "A2 baseline-plus-extension union")
    prior_remaining = set(
        checked_ids(a2["remaining_canonical_mask_indices"], "A2 remaining", count=177)
    )
    same_ids(prior_remaining, all_ids - prior, "A2 prior complement")
    require(
        a2.get("excluded_canonical_cases") == 2007
        and a2.get("remaining_canonical_cases") == 177,
        "A2 declared prior counts changed",
    )
    evidence = a2["per_case_evidence"]
    require(isinstance(evidence, dict), "A2 per-case evidence missing")
    evidence_ids = {int(key) for key in evidence if re.fullmatch(r"0|[1-9][0-9]*", key)}
    require(len(evidence_ids) == len(evidence), "A2 malformed per-case evidence key")
    same_ids(evidence_ids, prior, "A2 per-case evidence inventory")
    for case in prior:
        claimed = evidence[str(case)]
        require(isinstance(claimed, list) and bool(claimed), f"A2 case {case}: no evidence")
        expected = f"baseline:{snapshot_hash}" if case in baseline else extension_audits[case]
        require(expected in claimed, f"A2 case {case}: source audit binding missing")
    check_deadline(deadline, "returned-case audit")
    require(a3.get("format") == "streaming-returned-replay-plan-v1", "A3 plan format changed")
    require(
        a4.get("status") == "FROZEN_RELAY_ASSIGNMENTS_NOT_AN_OPTIMALITY_PROOF",
        "A4 assignment format changed",
    )
    require(
        a4.get("source_snapshot_sha256") == a2.get("snapshot_sha256"),
        "A4 prior snapshot binding changed",
    )
    require(a4.get("baseline_excluded") == 1931, "A4 baseline count changed")
    require(
        a4.get("latest_receipt_count_excluded") == 2007
        and a4.get("latest_receipt_count_remaining") == 177,
        "A4 prior counts changed",
    )
    require(
        checked_ids(a4["candidate_masks"], "A4 survivors", count=4) == list(SURVIVORS),
        "A4 survivor IDs changed",
    )
    jobs = a4["jobs"]
    require(
        isinstance(jobs, list) and len(jobs) == a4.get("case_job_count") == 12,
        "A4 job inventory changed",
    )
    assigned: dict[int, str] = {}
    job_ids: set[str] = set()
    for number, job in enumerate(jobs):
        label = f"A4 job {number}"
        job_id = text_field(job, "job_id", label)
        require(job_id not in job_ids, f"A4 duplicate job {job_id}")
        job_ids.add(job_id)
        ids = checked_ids(job["mask_indices"], f"{label} mask indices")
        require(bool(ids), f"{label}: empty assignment")
        masks = job["masks"]
        require(
            isinstance(masks, dict) and set(masks) == {str(case) for case in ids},
            f"{label}: mask map differs",
        )
        for case in ids:
            require(case not in assigned, f"A4 duplicate assignment for case {case}")
            require(masks[str(case)] == list(canonical[case]), f"A4 case {case}: mask differs")
            assigned[case] = job_id
    require(
        len(assigned) == a4.get("noncandidate_cases") == 173, "A4 assigned case count changed"
    )
    plans = a3["cases"]
    require(isinstance(plans, list) and len(plans) == 173, "A3 plan inventory changed")
    returned = set(
        checked_ids([case.get("mask_index") for case in plans], "A3 returned cases", count=173)
    )
    same_ids(returned, set(assigned), "A3/A4 job assignment inventory")
    job_sources: dict[str, tuple[str, str]] = {}
    for number, case in enumerate(plans):
        label = f"A3 case {number}"
        case_id = case["mask_index"]
        require(case.get("job_id") == assigned[case_id], f"A3 case {case_id}: job differs")
        for mask_field in ("assigned_mask", "mask"):
            if mask_field in case:
                require(
                    case[mask_field] == list(canonical[case_id]),
                    f"A3 case {case_id}: {mask_field} differs",
                )
        archive = text_field(case, "archive", label)
        require(
            archive.startswith("inputs/returned/")
            and ".." not in Path(archive).parts
            and archive.endswith(".zip"),
            f"{label}: unsafe archive path",
        )
        root_prefix = case.get("root_prefix")
        expected_root = (
            f"eleven-square-middle-four/{case['job_id']}-result"
            if root_prefix is None
            else f"{case['job_id']}-result"
        )
        require(
            root_prefix is None or root_prefix == expected_root,
            f"{label}: root prefix differs from job",
        )
        root_prefix = expected_root
        job_source = (archive, root_prefix)
        if case["job_id"] in job_sources:
            require(
                job_sources[case["job_id"]] == job_source,
                f"{label}: job source identity differs",
            )
        else:
            job_sources[case["job_id"]] = job_source
        source_member = text_field(case, "source_member", label)
        audit_member = text_field(case, "saved_audit_member", label)
        require(
            source_member.startswith(root_prefix + "/")
            and audit_member.startswith(root_prefix + "/")
            and ".." not in Path(source_member).parts
            and ".." not in Path(audit_member).parts,
            f"{label}: unsafe source/audit member",
        )
        source_hash = hash_field(case, "source_sha256", label)
        audit_hash = hash_field(case, "saved_audit_sha256", label)
        root_hash = hash_field(case, "root_sha256", label)
        members = case.get("stream_extract_members")
        require(isinstance(members, list), f"{label}: extraction inventory missing")
        by_member = {member["member"]: member for member in members}
        require(len(by_member) == len(members), f"{label}: duplicate extracted member")
        for member, expected_hash in ((source_member, source_hash), (audit_member, audit_hash)):
            require(
                member in by_member
                and by_member[member].get("expected_sha256") == expected_hash,
                f"{label}: source/audit member binding differs",
            )
        require(
            any(member.get("expected_sha256") == root_hash for member in members),
            f"{label}: root seed binding missing",
        )
        require(
            any(member.get("expected_sha256") == COVER_SHA256 for member in members),
            f"{label}: cover binding missing",
        )
    require(a5.get("status") == "PASS_ALL_173_RETURNED_CASES", "A5 completion status changed")
    require(a5.get("plan_sha256") == PINS["A3"].decoded_sha256, "A5 plan digest changed")
    require(
        a5.get("assignment_sha256") == PINS["A4"].decoded_sha256, "A5 assignment digest changed"
    )
    require(
        a5.get("completed") == a5.get("required") == 173, "A5 completed/required count changed"
    )
    completed = set(checked_ids(a5["completed_cases"], "A5 completed cases", count=173))
    unresolved = checked_ids(a5["unresolved_cases"], "A5 unresolved cases", count=0)
    require(not unresolved, "A5 completion flag has unresolved cases")
    same_ids(completed, returned, "A5 completed/returned equality")
    require(not (returned & prior), f"returned/prior overlap: {sorted(returned & prior)}")
    required = all_ids - set(SURVIVORS)
    same_ids(prior | returned, required, "complete reported exclusion census")
    require(
        all(
            records[name].get("global_optimality_proved") is False
            for name in ("A1", "A2", "A4", "A5")
        ),
        "published global-status metadata changed",
    )
    check_deadline(deadline, "census completion")
    return {
        "status": "PASS_CASE_CENSUS_ONLY",
        "geometry_verified": False,
        "global_optimality_proved": False,
        "source_revision": SOURCE_REVISION,
        "premises": {"U": str(U), "L": str(L), "B": str(B), "cover_sha256": COVER_SHA256},
        "mask_universe": {"raw": 4368, "canonical": 2184},
        "baseline": {
            "case_ids": sorted(baseline),
            "count": len(baseline),
            "field_certificates": 59,
            "generic_certificates": 34,
            "field_union": len(field_union),
            "generic_new": len(generic_union - field_union),
        },
        "extensions": {"case_ids": sorted(extension_ids), "count": len(extension_ids)},
        "returned": {
            "case_ids": sorted(returned),
            "count": len(returned),
            "jobs": len(job_ids),
        },
        "census_checked_case_ids": sorted(all_ids),
        "census_unresolved_case_ids": [],
        "reported_excluded_case_ids": sorted(prior | returned),
        "surviving_canonical_case_ids": list(SURVIVORS),
        "geometrically_unverified_case_count": len(all_ids),
        "survivor_masks": {str(case): list(canonical[case]) for case in SURVIVORS},
        "limitations": (
            "Certificate geometry, field transfer, returned audits, and case-438 "
            "capture are not verified by this census."
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet", type=Path, default=PACKET)
    parser.add_argument("--objects", type=Path, required=True)
    parser.add_argument("--cover", type=Path, required=True)
    parser.add_argument("--max-seconds", type=float, default=30.0)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    if not math.isfinite(args.max_seconds) or args.max_seconds <= 0:
        parser.error("--max-seconds must be positive and finite")
    start_wall, start_cpu = time.monotonic(), time.process_time()
    checker_sha = digest(Path(__file__).read_bytes())
    try:
        records, cover = load_inputs(args.packet, args.objects, args.cover)
        result = audit_records(records, cover, start_wall + args.max_seconds)
    except TimeoutError as error:
        result = {
            "status": "INCOMPLETE_TIMEOUT",
            "reason": str(error),
            "geometry_verified": False,
            "global_optimality_proved": False,
            "source_revision": SOURCE_REVISION,
            "census_checked_case_ids": [],
            "census_unresolved_case_ids": list(range(2184)),
        }
    except (OSError, ValueError, KeyError, TypeError, OverflowError) as error:
        result = {
            "status": "REFUSED",
            "reason": str(error),
            "geometry_verified": False,
            "global_optimality_proved": False,
            "source_revision": SOURCE_REVISION,
            "census_checked_case_ids": [],
            "census_unresolved_case_ids": list(range(2184)),
        }
    result["checker_sha256"] = checker_sha
    result["source_object_sha256"] = {name: pin.decoded_sha256 for name, pin in PINS.items()}
    result["wall_seconds"] = time.monotonic() - start_wall
    result["process_cpu_seconds"] = time.process_time() - start_cpu
    result["wall_ceiling_seconds"] = args.max_seconds
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8") as receipt:
            receipt.write(encoded)
    print(encoded, end="")
    return 0 if result["status"] == "PASS_CASE_CENSUS_ONLY" else 2


if __name__ == "__main__":
    sys.exit(main())
