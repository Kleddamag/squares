"""Independently verify the pinned n=11 mask-202 field certificate.

The upstream audit supplies candidate intervals, never accepted geometry. Exact
rational ownership and polygon-arrangement primitives come from the frozen local
mask-0 checker, whose source bytes are bound below. Every required point and row
must complete before this one certificate excludes any canonical case.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from fractions import Fraction as Q
from itertools import combinations, pairwise
from pathlib import Path
from typing import Any

from devtools import check_n11_optimality_field_mask0 as kernel

REPO = Path(__file__).resolve().parents[2]
PACKET = kernel.PACKET
KERNEL_SHA = "75fc0238f2ac91af9dc9cf57bd00792343dcf3321c395adddebf0f3465113ce5"
SOURCE_REVISION = kernel.SOURCE_REVISION
FIELD_SHA = "3492cd05d8c2fd1a2aadd84c93a09c4a509171e830b7b42c5a2f049f4f11e0d3"
FIELD_LFS_SHA = "1f661949550dfcb5d9423e4b07f12bc6f0980f398321e5f07b08f2743822bf2b"
AUDIT_SHA = "516bda8f938738c85c5b292f77aa9d9ffafe0c7fe4595807d659a5229fa04dbc"
AUDIT_LFS_SHA = "653a93ced3252910ab719e7b9d0ff5e7c4ef526966849d63f0b366bca0df11a3"
MASK0_RESULT_SHA = "821274111e6eb50d47e20882da083e3e23d25ee37e6725a18b18d133ab798663"
OWNER_SUPPORT = (0, 4, 8, 12)
POSITIVE_CELLS = (4, 8)
SOURCE_ROWS = {4: 85, 8: 354}


def require(condition: object, reason: str) -> None:
    if not condition:
        raise ValueError(reason)


def load_sources(
    object_dir: Path, cover_path: Path
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    require(
        kernel.sha(Path(kernel.__file__).read_bytes()) == KERNEL_SHA,
        "local geometry kernel changed",
    )
    packet = kernel.pinned_gzip(
        object_dir / f"{FIELD_SHA}.gz",
        packed_bytes=3903,
        packed_sha=FIELD_LFS_SHA,
        raw_bytes=28181,
        raw_sha=FIELD_SHA,
    )
    audit = kernel.pinned_gzip(
        object_dir / f"{AUDIT_SHA}.gz",
        packed_bytes=66931,
        packed_sha=AUDIT_LFS_SHA,
        raw_bytes=455851,
        raw_sha=AUDIT_SHA,
    )
    cover = kernel.pinned_gzip(
        cover_path,
        packed_bytes=25016,
        packed_sha=kernel.COVER_LFS_SHA,
        raw_bytes=773471,
        raw_sha=kernel.COVER_SHA,
    )
    return packet, audit, cover


def canonical_masks(cover: dict[str, Any]) -> list[tuple[int, ...]]:
    raw = list(combinations(range(16), 11))
    canonical = sorted({min(mask, tuple(sorted(15 - cell for cell in mask))) for mask in raw})
    require(len(raw) == 4368 and len(canonical) == 2184, "mask counts changed")
    require(
        cover.get("all_eleven_cell_subsets") == [list(mask) for mask in raw],
        "raw mask ordering changed",
    )
    require(
        cover.get("canonical_eleven_cell_subsets") == [list(mask) for mask in canonical],
        "canonical mask ordering changed",
    )
    return canonical


def admit(packet: dict[str, Any], audit: dict[str, Any], cover: dict[str, Any]) -> None:
    require(audit.get("packet_sha256") == FIELD_SHA, "audit packet binding changed")
    require(
        packet.get("cover_sha256") == audit.get("cover_sha256") == kernel.COVER_SHA,
        "cover binding changed",
    )
    require(
        Q(packet["parent_Uplus"]) == Q(audit["parent_Uplus"]) == kernel.U, "U premise changed"
    )
    require(Q(audit["parent_side"]) == kernel.B, "B=L/U premise changed")
    canonical = canonical_masks(cover)
    require(
        packet.get("mask_index") == audit.get("canonical_mask_index") == 202,
        "mask index changed",
    )
    require(packet.get("mask") == audit.get("mask") == list(canonical[202]), "mask changed")
    certificate = packet["certificate"]
    require(Q(certificate["L"]) == kernel.L, "field side changed")
    require(certificate.get("coordinate_denominator") == 10**10, "field scale changed")
    require(certificate.get("weight_denominator") == 1, "weight scale changed")
    sites = certificate["sites"]
    require(isinstance(sites, list) and len(sites) == 3, "field site count changed")
    require(
        all(
            isinstance(site, list)
            and len(site) == 2
            and all(type(v) is int and 0 <= v <= kernel.L * 10**10 for v in site)
            for site in sites
        ),
        "field sites outside rational container",
    )
    require(len({tuple(site) for site in sites}) == 3, "duplicate field site")
    require(certificate.get("point_weights") == [0, 0, 0], "point charges changed")
    require(
        certificate.get("features")
        == [
            {
                "kind": "majority_hull",
                "indices": [0, 1, 2],
                "threshold": 2,
                "weight": 1,
                "source_physical_feature": 573,
            }
        ],
        "majority feature changed",
    )
    require(certificate.get("budget_units") == 1, "field budget changed")
    require(
        packet.get("threshold_units") == [int(i in POSITIVE_CELLS) for i in range(16)],
        "cell thresholds changed",
    )
    require(
        packet.get("conditional_owner_support") == list(OWNER_SUPPORT),
        "conditional owners changed",
    )
    require(
        packet.get("conditional_ownership") == "cell_owned_points",
        "ownership semantics changed",
    )
    require(len(packet["ownership_points_field"]) == 16, "ownership group count changed")


def majority_halfplanes(sites: list[kernel.Point], radius: Q) -> list[tuple[Q, Q, Q]]:
    """Exact odd-majority median strips for any supported odd site count."""
    require(len(sites) in (3, 5) and len(sites) % 2 == 1, "unsupported majority site count")
    normals = {(Q(1), Q(0)), (Q(0), Q(1))}
    for number, p in enumerate(sites):
        for q in sites[number + 1 :]:
            a, b = q[1] - p[1], p[0] - q[0]
            if a or b:
                normals.add(kernel.primitive_normal(a, b))
    halfplanes: list[tuple[Q, Q, Q]] = []
    for a, b in sorted(normals):
        median = sorted(a * x + b * y for x, y in sites)[len(sites) // 2]
        margin = radius * (abs(a) + abs(b))
        halfplanes.extend(((a, b, median + margin), (-a, -b, -median + margin)))
    return halfplanes


def row_geometry(
    packet: dict[str, Any],
    cover: dict[str, Any],
    cell: int,
    interval: tuple[Q, Q],
    *,
    budget: kernel.Budget,
) -> dict[str, Any]:
    require(cell in POSITIVE_CELLS, "row outside positive cells")
    core, h, c, s = kernel.row_envelope(interval)
    world = [
        (kernel.B / 2 + (kernel.L - kernel.B) * x, kernel.B / 2 + (kernel.L - kernel.B) * y)
        for x, y in (kernel.point(vertex) for vertex in cover["cells"][cell]["vertices"])
    ]
    legal = kernel.intersect(
        world,
        [
            (Q(1), Q(0), kernel.L / 2 + h),
            (Q(-1), Q(0), -kernel.L / 2 + h),
            (Q(0), Q(1), kernel.L / 2 + h),
            (Q(0), Q(-1), -kernel.L / 2 + h),
        ],
    )
    require(kernel.area2(legal) > 0, "degenerate row domain requires a separate proof")
    domain = [kernel.rotate(p, c, s) for p in legal]
    denominator = packet["certificate"]["coordinate_denominator"]
    sites = [
        kernel.rotate((Q(x, denominator), Q(y, denominator)), c, s)
        for x, y in packet["certificate"]["sites"]
    ]
    radius = core / 2
    true_region = kernel.intersect(domain, majority_halfplanes(sites, radius))
    candidates: list[tuple[Q, str, kernel.Polygon]] = []
    if kernel.area2(true_region) > 0:
        candidates.append((kernel.area2(true_region), "TRUE", true_region))
    for owner in OWNER_SUPPORT:
        if owner == cell:
            continue
        for index, value in enumerate(packet["ownership_points_field"][owner]):
            captured = kernel.intersect(
                domain,
                kernel.box_halfplanes(kernel.rotate(kernel.point(value), c, s), radius),
            )
            if kernel.area2(captured) > 0:
                candidates.append(
                    (kernel.area2(captured), f"owner:{owner}:point:{index}", captured)
                )
    eligible_count = len(candidates)
    # A strict subset is enough for a sound union proof. Exact area only sets
    # proof-search order; coverage of the entire domain is still checked afresh.
    candidates.sort(key=lambda row: row[0], reverse=True)
    selected = candidates[:12]
    try:
        proof = kernel.exact_union_cover(domain, [row[2] for row in selected], budget=budget)
    except ValueError as error:
        if str(error).startswith("row uncovered at exact x="):
            raise kernel.IncompleteError(
                f"selected 12-region subset did not cover cell {cell} interval {interval}"
            ) from error
        raise
    return {
        "cell": cell,
        "interval": [str(interval[0]), str(interval[1])],
        "core_side": str(core),
        "parent_center_halfwidth": str(h),
        "domain_area_twice": str(kernel.area2(domain)),
        "eligible_regions": eligible_count,
        "selected_regions": len(selected),
        "selection_rule": (
            "12 largest eligible intersections by exact rational area; "
            "ties preserve construction order"
        ),
        "selected_region_ids": [row[1] for row in selected],
        **proof,
    }


def proposed_rows(audit: dict[str, Any]) -> list[tuple[int, int, tuple[Q, Q]]]:
    raw = audit["independent_row_proofs"]
    require(isinstance(raw, list) and len(raw) == 439, "row proposal count changed")
    groups: dict[int, list[tuple[Q, Q]]] = {4: [], 8: []}
    for row in raw:
        cell = row["cell"]
        require(type(cell) is int and cell in POSITIVE_CELLS, "row outside positive cells")
        interval = row["interval"]
        require(isinstance(interval, list) and len(interval) == 2, "malformed row interval")
        groups[cell].append((Q(interval[0]), Q(interval[1])))
    require(
        {cell: len(rows) for cell, rows in groups.items()} == SOURCE_ROWS,
        "positive-cell row counts changed",
    )
    ordered: list[tuple[int, int, tuple[Q, Q]]] = []
    for cell in POSITIVE_CELLS:
        intervals = sorted(groups[cell])
        require(
            intervals[0][0] == 0 and intervals[-1][1] == 1,
            f"cell {cell}: angle endpoints missing",
        )
        require(len(set(intervals)) == len(intervals), f"cell {cell}: duplicate row")
        require(all(0 <= a < b <= 1 for a, b in intervals), f"cell {cell}: malformed interval")
        require(
            all(left[1] == right[0] for left, right in pairwise(intervals)),
            f"cell {cell}: row gap or overlap",
        )
        ordered.extend((cell, index, interval) for index, interval in enumerate(intervals))
    return ordered


def transfer_cases(
    packet: dict[str, Any], cover: dict[str, Any], baseline: dict[str, Any]
) -> dict[str, Any]:
    canonical = canonical_masks(cover)
    support = set(OWNER_SUPPORT)
    threshold = packet["threshold_units"]

    def applicable(mask: tuple[int, ...]) -> bool:
        return support.issubset(mask) and sum(threshold[i] for i in mask) > 1

    direct = [i for i, mask in enumerate(canonical) if applicable(mask)]
    transferred = [
        i
        for i, mask in enumerate(canonical)
        if applicable(mask) or applicable(tuple(sorted(15 - cell for cell in mask)))
    ]
    require(len(transferred) == 764, "mask-202 transfer count changed")
    entries = [
        row
        for row in baseline["certificates"]
        if row.get("family") == "field" and row.get("source_sha256") == FIELD_SHA
    ]
    require(len(entries) == 1, "A1 mask-202 certificate identity changed")
    listed = entries[0]["cases"]
    require(
        isinstance(listed, list)
        and len(listed) == 764
        and all(type(case) is int for case in listed)
        and len(set(listed)) == 764
        and set(listed) == set(transferred),
        "A1 mask-202 transfer list differs",
    )
    mask0_path = PACKET / "receipts/field-mask0/result.json"
    mask0_raw = mask0_path.read_bytes()
    require(kernel.sha(mask0_raw) == MASK0_RESULT_SHA, "validated mask-0 result changed")
    mask0 = kernel.strict_json(mask0_raw)
    require(
        mask0.get("status") == "PASS_ONE_FIELD_MASK0_GEOMETRY_AND_TRANSFER",
        "mask-0 status changed",
    )
    prior = mask0["transfer"]["transferred_case_ids"]
    require(len(prior) == 459 and len(set(prior)) == 459, "validated mask-0 cases changed")
    new = sorted(set(transferred) - set(prior))
    require(len(new) == 653, "mask-202 marginal case count changed")
    return {
        "direct_case_ids": direct,
        "transferred_case_ids": transferred,
        "new_beyond_mask0_case_ids": new,
    }


def check_budget(budget: kernel.Budget, work: int, phase: str) -> None:
    if time.monotonic() >= budget.deadline or work >= budget.max_nodes:
        raise kernel.IncompleteError(f"global ceiling before {phase}")


def all_geometry(
    packet: dict[str, Any],
    audit: dict[str, Any],
    cover: dict[str, Any],
    baseline: dict[str, Any],
    *,
    budget: kernel.Budget,
) -> dict[str, Any]:
    rows = proposed_rows(audit)
    owner_keys = [
        (owner, index)
        for owner in OWNER_SUPPORT
        for index in range(len(packet["ownership_points_field"][owner]))
    ]
    require(len(owner_keys) == 50, "scoped ownership point count changed")
    done_points: list[dict[str, Any]] = []
    done_rows: list[dict[str, Any]] = []
    work = 0
    try:
        for owner, index in owner_keys:
            check_budget(budget, work, "next owner point")
            proof = kernel.ownership(
                kernel.cell_vertices(cover, owner),
                kernel.point(packet["ownership_points_field"][owner][index]),
                budget=kernel.Budget(budget.deadline, budget.max_nodes - work),
            )
            work += proof["nodes"]
            done_points.append({"owner": owner, "point_index": index, **proof})
        for cell, index, interval in rows:
            check_budget(budget, work, "next row")
            proof = row_geometry(
                packet,
                cover,
                cell,
                interval,
                budget=kernel.Budget(budget.deadline, budget.max_nodes - work),
            )
            work += proof["events"] + proof["probes"]
            done_rows.append({"row_index": index, **proof})
        check_budget(budget, work, "transfer")
        transfer = transfer_cases(packet, cover, baseline)
        check_budget(budget, work, "PASS return")
    except kernel.IncompleteError as error:
        return {
            "status": "INCOMPLETE",
            "reason": str(error),
            "ownership_checked": done_points,
            "ownership_pending": [
                {"owner": o, "point_index": i} for o, i in owner_keys[len(done_points) :]
            ],
            "rows_checked": done_rows,
            "rows_pending": [
                {
                    "cell": cell,
                    "row_index": index,
                    "interval": [str(interval[0]), str(interval[1])],
                }
                for cell, index, interval in rows[len(done_rows) :]
            ],
            "work_units": work,
            "canonical_cases_excluded": 0,
            "geometry_verified": False,
        }
    return {
        "status": "PASS_ONE_FIELD_MASK202_GEOMETRY_AND_TRANSFER",
        "ownership_checked": done_points,
        "ownership_pending": [],
        "rows_checked": done_rows,
        "rows_pending": [],
        "work_units": work,
        "ownership_points": len(done_points),
        "positive_cell_rows": len(done_rows),
        "canonical_cases_excluded": len(transfer["transferred_case_ids"]),
        "new_cases_beyond_mask0": len(transfer["new_beyond_mask0_case_ids"]),
        "geometry_verified": True,
        "validated_field_certificates": 1,
        "transfer": transfer,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--objects", type=Path, required=True)
    parser.add_argument("--cover", type=Path, required=True)
    parser.add_argument("--owner", type=int, default=0)
    parser.add_argument("--point", type=int, default=0)
    parser.add_argument("--row-cell", type=int, choices=POSITIVE_CELLS)
    parser.add_argument("--row-index", type=int, default=0)
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--max-seconds", type=float, default=30.0)
    parser.add_argument("--max-nodes", type=int, default=100000)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    if not math.isfinite(args.max_seconds) or args.max_seconds <= 0 or args.max_nodes <= 0:
        parser.error("ceilings must be positive and finite")
    start, cpu = time.monotonic(), time.process_time()
    result: dict[str, Any]
    try:
        packet, audit, cover = load_sources(args.objects, args.cover)
        admit(packet, audit, cover)
        kernel.admit_d4_receipt()
        budget = kernel.Budget(start + args.max_seconds, args.max_nodes)
        if args.all:
            require(args.row_cell is None, "--all cannot select one row")
            baseline = kernel.pinned_gzip(
                PACKET / "receipts/case-census/objects" / f"{kernel.A1_SHA}.gz",
                packed_bytes=26100,
                packed_sha=kernel.A1_LFS_SHA,
                raw_bytes=122029,
                raw_sha=kernel.A1_SHA,
            )
            result = all_geometry(packet, audit, cover, baseline, budget=budget)
        elif args.row_cell is None:
            require(args.owner in OWNER_SUPPORT, "owner outside scoped support")
            group = packet["ownership_points_field"][args.owner]
            require(0 <= args.point < len(group), "point index outside owner group")
            proof = kernel.ownership(
                kernel.cell_vertices(cover, args.owner),
                kernel.point(group[args.point]),
                budget=budget,
            )
            result = {
                "status": "PASS_ONE_OWNERSHIP_POINT_ONLY",
                "owner": args.owner,
                "point": args.point,
                "proof": proof,
            }
        else:
            rows = [
                row for row in audit["independent_row_proofs"] if row["cell"] == args.row_cell
            ]
            require(0 <= args.row_index < len(rows), "row index outside proposal inventory")
            source = rows[args.row_index]
            interval = Q(source["interval"][0]), Q(source["interval"][1])
            proof = row_geometry(packet, cover, args.row_cell, interval, budget=budget)
            result = {
                "status": "PASS_ONE_ROW_ONLY",
                "row_index": args.row_index,
                "proof": proof,
            }
    except kernel.IncompleteError as error:
        result = {"status": "INCOMPLETE", "reason": str(error)}
    except (ValueError, KeyError, IndexError, TypeError, OSError) as error:
        result = {"status": "REFUSED", "reason": str(error)}
    result.setdefault("geometry_verified", False)
    result.setdefault("canonical_cases_excluded", 0)
    result.update(
        source_revision=SOURCE_REVISION,
        packet_sha256=FIELD_SHA,
        audit_proposal_sha256=AUDIT_SHA,
        cover_sha256=kernel.COVER_SHA,
        d4_receipt_sha256=kernel.D4_RESULT_SHA,
        kernel_checker_sha256=KERNEL_SHA,
        checker_sha256=kernel.sha(Path(__file__).read_bytes()),
        global_optimality_proved=False,
        wall_seconds=time.monotonic() - start,
        process_cpu_seconds=time.process_time() - cpu,
        wall_ceiling_seconds=args.max_seconds,
        node_ceiling=args.max_nodes,
    )
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.open("x", encoding="utf-8").write(encoded)
    print(encoded, end="")
    return (
        0
        if result["status"]
        in (
            "PASS_ONE_OWNERSHIP_POINT_ONLY",
            "PASS_ONE_ROW_ONLY",
            "PASS_ONE_FIELD_MASK202_GEOMETRY_AND_TRANSFER",
        )
        else 2
    )


if __name__ == "__main__":
    sys.exit(main())
