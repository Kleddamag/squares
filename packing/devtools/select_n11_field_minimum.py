"""Select a minimum sufficient family of accepted n=11 field certificates.

Each accepted field receipt records the canonical cases its certificate excludes
(`transfer.transferred_case_ids`). This tool reads the field coverage inventory, admits
every receipt it lists against its decoded digest and completion status, and computes:
the exact case union, how many packets cover each case, the mandatory packets (those
covering some case that no other packet covers), and an exact minimum sufficient
selection (the mandatory packets plus a minimum cover of whatever they leave, found by
exhaustive branch and bound).

Minimality is relative to this fixed family of recorded transfer sets. It is
bookkeeping over retained receipts: no field geometry is rerun, and the selected
receipts keep every dependency they had (packets, audit proposals, cover, D4 receipt).
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from strif import atomic_write_text

from devtools.inventory_n11_exclusions import FIELD_SHA
from devtools.prepare_n11_nonfield_manifest import PACKET, REPO, require

INVENTORY = PACKET / "receipts/field-batch-a/field-coverage-inventory.json"
PASS = "PASS_ONE_FIELD_GEOMETRY_AND_TRANSFER"
SCHEMA = "sqpack.n11-field-minimum-selection.v1"
DEFAULT_MAX_NODES = 1_000_000


@dataclass(frozen=True)
class Packet:
    """One accepted field certificate and the exact cases its receipt transfers."""

    packet_sha256: str
    mask_index: int
    path: str
    decoded_sha256: str
    checker_sha256: str
    audit_proposal_sha256: str
    cases: frozenset[int]
    rows: int
    ownership_points: int


@dataclass(frozen=True)
class Cover:
    """Every minimum-cardinality cover of a universe, with the search effort it took."""

    size: int
    selections: tuple[frozenset[str], ...]
    nodes: int


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def admit(record: dict[str, Any], repo: Path) -> Packet:
    """Read one inventory record's receipt and refuse anything short of a complete PASS."""
    raw = gzip.decompress((repo / record["path"]).read_bytes())
    require(digest(raw) == record["decoded_sha256"], f"receipt bytes differ: {record['path']}")
    result = json.loads(raw)
    require(
        result["status"] == PASS
        and result["geometry_verified"] is True
        and result["global_optimality_proved"] is False
        and result["rows_pending"] == []
        and result["ownership_pending"] == [],
        f"receipt is not a complete field PASS: {record['path']}",
    )
    require(
        result["packet_sha256"] == record["packet_sha256"]
        and result["checker_sha256"] == record["checker_sha256"],
        f"receipt identity differs from inventory: {record['path']}",
    )
    transferred = result["transfer"]["transferred_case_ids"]
    require(
        all(type(case) is int and 0 <= case < 2184 for case in transferred)
        and len(set(transferred)) == len(transferred) == result["canonical_cases_excluded"],
        f"transferred case list malformed: {record['path']}",
    )
    require(
        len(result["rows_checked"]) == result["positive_cell_rows"]
        and len(result["ownership_checked"]) == result["ownership_points"],
        f"row or ownership census differs: {record['path']}",
    )
    return Packet(
        packet_sha256=record["packet_sha256"],
        mask_index=result["mask_index"],
        path=record["path"],
        decoded_sha256=record["decoded_sha256"],
        checker_sha256=result["checker_sha256"],
        audit_proposal_sha256=result["audit_proposal_sha256"],
        cases=frozenset(transferred),
        rows=result["positive_cell_rows"],
        ownership_points=result["ownership_points"],
    )


def load_packets(inventory: dict[str, Any], repo: Path) -> dict[str, Packet]:
    packets: dict[str, Packet] = {}
    for record in inventory["accepted_receipts"]:
        packet = admit(record, repo)
        earlier = packets.setdefault(packet.packet_sha256, packet)
        require(
            earlier.cases == packet.cases,
            f"one packet transfers two different case sets: {packet.packet_sha256}",
        )
    return packets


def minimum_covers(
    universe: frozenset[int], sets: dict[str, frozenset[int]], *, max_nodes: int
) -> Cover:
    """Find every minimum-cardinality cover of `universe` by exhaustive branch and bound.

    Each node branches on the uncovered case with the fewest candidate sets: every cover
    contains one of them. A branch is cut only when even the largest remaining set,
    repeated, could not finish within the best size found, so ties are all collected.
    """
    useful = {key: members & universe for key, members in sets.items() if members & universe}
    require(universe <= frozenset().union(*useful.values()), "universe has an uncoverable case")
    containing: dict[int, list[str]] = {case: [] for case in universe}
    for key in sorted(useful):
        for case in useful[key]:
            containing[case].append(key)
    largest = max((len(members) for members in useful.values()), default=1)
    best = len(useful)
    found: set[frozenset[str]] = set()
    nodes = 0

    def search(uncovered: frozenset[int], chosen: frozenset[str]) -> None:
        nonlocal best, nodes
        nodes += 1
        require(nodes <= max_nodes, "minimum-cover search exceeded its node ceiling")
        if not uncovered:
            if len(chosen) < best:
                best = len(chosen)
                found.clear()
            found.add(chosen)
            return
        if len(chosen) + -(-len(uncovered) // largest) > best:
            return
        pivot = min(uncovered, key=lambda case: (len(containing[case]), case))
        for key in containing[pivot]:
            search(uncovered - useful[key], chosen | {key})

    search(universe, frozenset())
    return Cover(size=best, selections=tuple(sorted(found, key=sorted)), nodes=nodes)


def receipt_row(packet: Packet, *, mandatory: bool) -> dict[str, Any]:
    return {
        "packet_sha256": packet.packet_sha256,
        "mask_index": packet.mask_index,
        "path": packet.path,
        "decoded_sha256": packet.decoded_sha256,
        "checker_sha256": packet.checker_sha256,
        "audit_proposal_sha256": packet.audit_proposal_sha256,
        "transferred_case_count": len(packet.cases),
        "complete_angle_rows": packet.rows,
        "ownership_points": packet.ownership_points,
        "mandatory": mandatory,
    }


def select(
    inventory_path: Path,
    *,
    repo: Path = REPO,
    expected_sha: str | None = FIELD_SHA,
    max_nodes: int = DEFAULT_MAX_NODES,
) -> dict[str, Any]:
    require(
        inventory_path.resolve().is_relative_to(repo.resolve()),
        "inventory must lie inside the repository so its declared path is relative",
    )
    raw = inventory_path.read_bytes()
    require(expected_sha is None or digest(raw) == expected_sha, "inventory bytes differ")
    inventory = json.loads(raw)
    packets = load_packets(inventory, repo)
    union = frozenset().union(*(packet.cases for packet in packets.values()))
    declared = frozenset(inventory["previously_accepted_field_case_ids"])
    require(union == declared, "accepted receipts do not reproduce the declared field union")
    holders: dict[int, list[str]] = {case: [] for case in union}
    for key in sorted(packets):
        for case in packets[key].cases:
            holders[case].append(key)
    private: dict[str, list[int]] = {}
    for case in sorted(union):
        if len(holders[case]) == 1:
            private.setdefault(holders[case][0], []).append(case)
    mandatory = frozenset(private)
    covered = frozenset().union(*(packets[key].cases for key in mandatory))
    remainder = union - covered
    optional = {key: packets[key].cases for key in packets if key not in mandatory}
    cover = minimum_covers(remainder, optional, max_nodes=max_nodes)
    require(bool(cover.selections), "no cover of the remainder was found")
    additional = min(
        cover.selections,
        key=lambda keys: (sum(packets[key].rows for key in keys), sorted(keys)),
    )
    chosen = mandatory | additional
    chosen_union = frozenset().union(*(packets[key].cases for key in chosen))
    require(chosen_union == union, "selected packets do not reproduce the union")
    size = len(mandatory) + cover.size
    require(len(chosen) == size, "selection size differs from its lower bound")
    order = sorted(packets, key=lambda key: (packets[key].mask_index, key))
    multiplicity = Counter(len(keys) for keys in holders.values())
    if remainder:
        remainder_reason = (
            f"the {len(remainder)} cases they leave need at least {cover.size} more "
            f"packets, by exhaustive branch and bound over the {len(optional)} other "
            f"packets ({cover.nodes} nodes)"
        )
    else:
        remainder_reason = "they already cover the union, so nothing else is needed"
    return {
        "schema": SCHEMA,
        "status": "MINIMUM_FIELD_SELECTION",
        "scope": (
            "Exact minimum within this fixed family of accepted field transfer sets; "
            "bookkeeping over retained receipts, with no field geometry rerun. Not a "
            "minimum over every possible field construction or mixed proof. Selected "
            "receipts keep their packets, audit proposals, cover, and D4 dependencies."
        ),
        "global_optimality_proved": False,
        "geometry_rerun": False,
        "inventory_path": inventory_path.resolve().relative_to(repo.resolve()).as_posix(),
        "inventory_sha256": digest(raw),
        "accepted_receipt_records": len(inventory["accepted_receipts"]),
        "distinct_accepted_packets": len(packets),
        "union_check": {
            "case_count": len(union),
            "equals_inventory_field_case_ids": union == declared,
            "selected_union_equals_full_union": chosen_union == union,
        },
        "union_case_ids": sorted(union),
        "coverage_counts": [len(holders[case]) for case in sorted(union)],
        "coverage_histogram": {
            str(count): multiplicity[count] for count in sorted(multiplicity)
        },
        "mandatory_count": len(mandatory),
        "mandatory_witnesses": [
            {
                "packet_sha256": key,
                "mask_index": packets[key].mask_index,
                "witness_case_id": private[key][0],
                "private_case_ids": private[key],
            }
            for key in order
            if key in mandatory
        ],
        "mandatory_union_case_count": len(covered),
        "remainder_case_ids": sorted(remainder),
        "remainder_minimum_size": cover.size,
        "remainder_minimum_selections": [sorted(keys) for keys in cover.selections],
        "remainder_search_nodes": cover.nodes,
        "minimum_size": size,
        "minimum_selection_count": len(cover.selections),
        "selection_tie_break": "fewest complete angle rows, then packet hash order",
        "selected_receipts": [
            receipt_row(packets[key], mandatory=key in mandatory)
            for key in order
            if key in chosen
        ],
        "omitted_receipts": [
            {
                **receipt_row(packets[key], mandatory=False),
                "case_ids": sorted(packets[key].cases),
            }
            for key in order
            if key not in chosen
        ],
        "totals": {
            "all": {
                "packets": len(packets),
                "complete_angle_rows": sum(packet.rows for packet in packets.values()),
                "ownership_points": sum(packet.ownership_points for packet in packets.values()),
            },
            "selected": {
                "packets": len(chosen),
                "complete_angle_rows": sum(packets[key].rows for key in chosen),
                "ownership_points": sum(packets[key].ownership_points for key in chosen),
            },
        },
        "minimality": (
            f"No selection of fewer than {size} of these {len(packets)} accepted packets "
            f"covers the {len(union)}-case union. Each of the {len(mandatory)} mandatory "
            "packets transfers a witness case that no other accepted packet transfers, "
            f"so every covering selection contains all of them; {remainder_reason}. "
            + (
                "The minimum selection is unique."
                if len(cover.selections) == 1
                else f"There are {len(cover.selections)} minimum selections; the "
                "tie-break above picks one."
            )
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--inventory",
        type=Path,
        default=None,
        help="field coverage inventory; the pinned retained inventory when omitted",
    )
    parser.add_argument("--max-nodes", type=int, default=DEFAULT_MAX_NODES)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    manifest = select(
        args.inventory or INVENTORY,
        expected_sha=None if args.inventory else FIELD_SHA,
        max_nodes=args.max_nodes,
    )
    atomic_write_text(args.out, json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                key: manifest[key]
                for key in (
                    "distinct_accepted_packets",
                    "union_check",
                    "mandatory_count",
                    "remainder_case_ids",
                    "minimum_size",
                    "minimum_selection_count",
                    "totals",
                )
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
