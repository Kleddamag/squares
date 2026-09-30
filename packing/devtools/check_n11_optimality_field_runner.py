"""Source-bound shared exact runner for a narrowly supported n=11 field grammar.

This runner reuses the frozen local mask-0 rational geometry kernel. It is
independent of the upstream producer, but is not independent of that first-party
kernel. Published mask-0/mask-202 checkers and their receipts remain unchanged.
Only a complete ownership/row/transfer census can exclude canonical cases.
"""

from __future__ import annotations

import argparse
import json
import math
import resource
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from fractions import Fraction as Q
from functools import partial
from itertools import combinations, pairwise
from pathlib import Path
from typing import Any

from devtools import check_n11_optimality_field_mask0 as kernel

KERNEL_SHA = "75fc0238f2ac91af9dc9cf57bd00792343dcf3321c395adddebf0f3465113ce5"
PACKET_ROOT = kernel.PACKET
Point = kernel.Point
Polygon = kernel.Polygon


@dataclass(frozen=True, slots=True)
class ObjectPin:
    decoded_sha: str
    decoded_bytes: int
    compressed_sha: str
    compressed_bytes: int


@dataclass(frozen=True, slots=True)
class FieldSpec:
    mask_index: int
    packet: ObjectPin
    audit: ObjectPin
    site_count: int
    feature_source_id: int
    owner_lengths: tuple[tuple[int, int], ...]
    row_counts: tuple[tuple[int, int], ...]
    expected_direct: int
    expected_transferred: int
    max_regions: int | None
    weighted_features: tuple[tuple[tuple[int, ...], int, int], ...] = ()
    point_charges: tuple[tuple[int, int], ...] = ()
    cell_charge: int = 1

    @property
    def features(self) -> tuple[tuple[tuple[int, ...], int, int], ...]:
        return self.weighted_features or (
            (tuple(range(self.site_count)), 1, self.feature_source_id),
        )

    @property
    def charge_budget(self) -> int:
        return sum(weight for _, weight, _ in self.features) + sum(
            weight for _, weight in self.point_charges
        )

    @property
    def owners(self) -> tuple[int, ...]:
        return tuple(owner for owner, _ in self.owner_lengths)

    @property
    def positive_cells(self) -> tuple[int, ...]:
        return tuple(cell for cell, _ in self.row_counts)


SPECS = {
    0: FieldSpec(
        0,
        ObjectPin(
            "14164a3d91117055000ae78cd15a4e8ad5d6bb2c27ce24ff080605b873a93340",
            28065,
            "0759a9f56e0035713996287fa2bd540c29ad60820da5da40250136375442f832",
            3749,
        ),
        ObjectPin(
            "1a56056ad4d19786e41e248f0ef60866ad2021370e9ef809faa471fb679f8a54",
            201961,
            "156102cf720236023cf5ec86cc697a5d6d2615fcf0eaa82336574be49d8856a2",
            29707,
        ),
        5,
        931,
        ((0, 11), (1, 10), (2, 12), (3, 12), (6, 10)),
        ((1, 67), (2, 69)),
        453,
        459,
        None,
    ),
    202: FieldSpec(
        202,
        ObjectPin(
            "3492cd05d8c2fd1a2aadd84c93a09c4a509171e830b7b42c5a2f049f4f11e0d3",
            28181,
            "1f661949550dfcb5d9423e4b07f12bc6f0980f398321e5f07b08f2743822bf2b",
            3903,
        ),
        ObjectPin(
            "516bda8f938738c85c5b292f77aa9d9ffafe0c7fe4595807d659a5229fa04dbc",
            455851,
            "653a93ced3252910ab719e7b9d0ff5e7c4ef526966849d63f0b366bca0df11a3",
            66931,
        ),
        3,
        573,
        ((0, 11), (4, 13), (8, 14), (12, 12)),
        ((4, 85), (8, 354)),
        548,
        764,
        12,
    ),
    612: FieldSpec(
        612,
        ObjectPin(
            "9a777a1701cb23e63b5aec586f0650057888e18038bc037ba15f2747d9ea2f8d",
            28479,
            "8170748b74a6fb31258698050aa125866fbab8ab4beed43f98f43dcb01ff16f0",
            3801,
        ),
        ObjectPin(
            "85da259e513589756b1a112e41c98ef7dac2c7710a94f0378a1cf3488f9e780a",
            588766,
            "eb506136d85ae5251d6c28dbb7ef2bb15e54650b7805f36a39f3f786b979ed88",
            84782,
        ),
        8,
        0,
        ((0, 11), (1, 10), (2, 12), (3, 12), (7, 15)),
        ((0, 450), (1, 106), (2, 51)),
        453,
        459,
        None,
        (((0, 1, 3, 4, 5), 1, 456), ((2, 6, 7), 1, 654)),
    ),
    1155: FieldSpec(
        1155,
        ObjectPin(
            "8ac3b7c4093a06354850e4d804f250196ff0505bfc411ac05f4f78cbacec5734",
            46854,
            "e35e0e04e66f66f9aca0b92abd1b35085c561ffbf2f8689b89e6a24fae299fc0",
            5344,
        ),
        ObjectPin(
            "ad6ce694aa0a9449a6aabad34589d8a61a3fb812b616be4d779932aadae2e656",
            545641,
            "3f7acfd9e4e89a0422b9a15b073c6321d6cff7b088abf9388bd2bcfde3d48418",
            60617,
        ),
        13,
        0,
        ((8, 14), (9, 10), (10, 11), (11, 14), (12, 12), (14, 10)),
        ((8, 362), (9, 89), (10, 71)),
        85,
        252,
        None,
        (((0, 2, 5), 1, 333), ((3, 6, 8, 9, 10), 1, 369), ((1, 4, 11), 1, 573)),
        ((7, 1), (12, 1)),
        2,
    ),
}


def require(condition: object, reason: str) -> None:
    if not condition:
        raise ValueError(reason)


def _pinned(path: Path, pin: ObjectPin) -> dict[str, Any]:
    return kernel.pinned_gzip(
        path,
        packed_bytes=pin.compressed_bytes,
        packed_sha=pin.compressed_sha,
        raw_bytes=pin.decoded_bytes,
        raw_sha=pin.decoded_sha,
    )


def load_sources(
    spec: FieldSpec, object_dir: Path, cover_path: Path
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    require(
        kernel.sha(Path(kernel.__file__).read_bytes()) == KERNEL_SHA,
        "frozen local geometry kernel changed",
    )
    packet = _pinned(object_dir / f"{spec.packet.decoded_sha}.gz", spec.packet)
    audit = _pinned(object_dir / f"{spec.audit.decoded_sha}.gz", spec.audit)
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
    canonical = sorted({min(mask, tuple(sorted(15 - i for i in mask))) for mask in raw})
    require(len(raw) == 4368 and len(canonical) == 2184, "canonical mask count changed")
    require(
        cover.get("all_eleven_cell_subsets") == [list(mask) for mask in raw],
        "raw mask ordering changed",
    )
    require(
        cover.get("canonical_eleven_cell_subsets") == [list(mask) for mask in canonical],
        "canonical mask ordering changed",
    )
    return canonical


def admit(
    spec: FieldSpec, packet: dict[str, Any], audit: dict[str, Any], cover: dict[str, Any]
) -> None:
    """Admit pinned nonnegative point and odd-site majority charges."""
    require(
        all(len(indices) in (3, 5) for indices, _, _ in spec.features),
        "unsupported majority-site arity",
    )
    require(
        audit.get("packet_sha256") == spec.packet.decoded_sha, "audit packet binding changed"
    )
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
        packet.get("mask_index") == audit.get("canonical_mask_index") == spec.mask_index,
        "canonical mask index changed",
    )
    require(
        packet.get("mask") == audit.get("mask") == list(canonical[spec.mask_index]),
        "canonical mask changed",
    )
    cert = packet["certificate"]
    require(
        Q(cert["L"]) == kernel.L
        and cert.get("coordinate_denominator") == 10**10
        and cert.get("weight_denominator") == 1,
        "field scale changed",
    )
    sites = cert.get("sites")
    require(
        isinstance(sites, list) and len(sites) == spec.site_count, "field site count changed"
    )
    require(
        all(
            isinstance(site, list)
            and len(site) == 2
            and all(type(value) is int and 0 <= value <= kernel.L * 10**10 for value in site)
            for site in sites
        ),
        "field sites outside rational container",
    )
    require(len({tuple(site) for site in sites}) == spec.site_count, "duplicate field site")
    require(
        cert.get("point_weights")
        == [dict(spec.point_charges).get(index, 0) for index in range(spec.site_count)],
        "point charges changed",
    )
    require(
        cert.get("features")
        == [
            {
                "kind": "majority_hull",
                "indices": list(indices),
                "threshold": len(indices) // 2 + 1,
                "weight": weight,
                "source_physical_feature": source_id,
            }
            for indices, weight, source_id in spec.features
        ],
        "unsupported field feature",
    )
    require(cert.get("budget_units") == spec.charge_budget, "field budget changed")
    require(
        packet.get("threshold_units")
        == [spec.cell_charge * int(i in spec.positive_cells) for i in range(16)],
        "positive cell charges changed",
    )
    require(
        packet.get("conditional_owner_support") == list(spec.owners)
        and packet.get("conditional_ownership") == "cell_owned_points",
        "conditional ownership changed",
    )
    groups = packet.get("ownership_points_field")
    if not isinstance(groups, list) or len(groups) != 16:
        raise ValueError("ownership group inventory changed")
    require(
        all(
            isinstance(groups[owner], list) and len(groups[owner]) == count
            for owner, count in spec.owner_lengths
        ),
        "scoped ownership point inventory changed",
    )


def majority_halfplanes(sites: list[Point], radius: Q) -> list[tuple[Q, Q, Q]]:
    """Exact finite median-strip normals for a supported odd-site feature."""
    require(len(sites) in (3, 5), "unsupported majority-site arity")
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


def proposed_rows(spec: FieldSpec, audit: dict[str, Any]) -> list[tuple[int, int, tuple[Q, Q]]]:
    raw = audit["independent_row_proofs"]
    require(
        isinstance(raw, list) and len(raw) == sum(n for _, n in spec.row_counts),
        "row proposal count changed",
    )
    by_cell: dict[int, list[tuple[Q, Q]]] = {cell: [] for cell in spec.positive_cells}
    for row in raw:
        cell = row["cell"]
        require(type(cell) is int and cell in by_cell, "row outside positive cells")
        interval = row["interval"]
        require(isinstance(interval, list) and len(interval) == 2, "malformed row interval")
        by_cell[cell].append((Q(interval[0]), Q(interval[1])))
    require(
        {cell: len(rows) for cell, rows in by_cell.items()} == dict(spec.row_counts),
        "positive-cell row counts changed",
    )
    ordered: list[tuple[int, int, tuple[Q, Q]]] = []
    for cell in spec.positive_cells:
        intervals = sorted(by_cell[cell])
        require(
            intervals[0][0] == 0 and intervals[-1][1] == 1,
            f"cell {cell}: angle endpoints missing",
        )
        require(len(set(intervals)) == len(intervals), f"cell {cell}: duplicate row")
        require(
            all(0 <= left < right <= 1 for left, right in intervals),
            f"cell {cell}: malformed row interval",
        )
        require(
            all(first[1] == second[0] for first, second in pairwise(intervals)),
            f"cell {cell}: row gap or overlap",
        )
        ordered.extend((cell, index, interval) for index, interval in enumerate(intervals))
    return ordered


def weighted_union_cover(
    domain: Polygon,
    atoms: list[tuple[int, str, Polygon]],
    threshold: int,
    *,
    budget: kernel.Budget,
) -> dict[str, int]:
    """Check closed vertical sections at every arrangement event and between them.

    Every physical atom has one convex region and is counted once. Collision
    regions carry the threshold as an infeasibility alternative, not global mass.
    """
    require(kernel.area2(domain) > 0, "degenerate row domain requires separate proof")
    require(threshold > 0 and all(weight > 0 for weight, _, _ in atoms), "invalid weights")
    require(len({name for _, name, _ in atoms}) == len(atoms), "duplicate weighted atom")
    polygons = [domain, *(polygon for _, _, polygon in atoms)]
    left, right = min(x for x, _ in domain), max(x for x, _ in domain)
    events = {x for polygon in polygons for x, _ in polygon if left <= x <= right}
    lines = kernel.edge_lines(polygons)
    for number, (a0, a1, m, b) in enumerate(lines):
        _budget(budget, len(events), "weighted arrangement edges")
        for z0, z1, n, d in lines[number + 1 :]:
            if m != n:
                start, stop = max(a0, z0, left), min(a1, z1, right)
                if start <= stop and start <= (crossing := (d - b) / (m - n)) <= stop:
                    events.add(crossing)
    positions = sorted(events)
    require(positions[0] == left and positions[-1] == right, "domain endpoints missing")
    probes = [positions[0]]
    for low, high in pairwise(positions):
        probes.extend(((low + high) / 2, high))
    work = len(events)
    for x in probes:
        _budget(budget, work, "weighted arrangement section")
        target = kernel.vertical_interval(domain, x)
        require(target is not None, "section outside domain")
        if target is None:
            raise ValueError("section outside domain")
        low, high = target
        spans = [
            (weight, span)
            for weight, _, polygon in atoms
            if (span := kernel.vertical_interval(polygon, x)) is not None
        ]
        ordinates = sorted(
            {low, high, *(y for _, span in spans for y in span if low <= y <= high)}
        )
        ys = [*ordinates, *((a + b) / 2 for a, b in pairwise(ordinates))]
        for y in ys:
            require(
                sum(weight for weight, (a, b) in spans if a <= y <= b) >= threshold,
                f"weighted row uncovered at exact (x,y)=({x},{y})",
            )
        work += len(ys)
    _budget(budget, work, "weighted coverage return")
    return {"events": len(events), "probes": work - len(events), "edge_segments": len(lines)}


def maximal_collision_regions(
    candidates: list[tuple[Q, str, Polygon]],
) -> list[tuple[Q, str, Polygon]]:
    """Remove contained alternatives, each a common domain intersected with a box.

    If A's bounding box lies in B's, A lies in B's capture box and the common
    domain, hence in B. This rule does not apply to distinct physical charge atoms.
    """
    extents = [
        (
            min(x for x, _ in poly),
            min(y for _, y in poly),
            max(x for x, _ in poly),
            max(y for _, y in poly),
        )
        for _, _, poly in candidates
    ]
    retained = []
    for index, (left, bottom, right, top) in enumerate(extents):
        if not any(
            other != index
            and a <= left
            and b <= bottom
            and c >= right
            and d >= top
            and (extents[other] != extents[index] or other < index)
            for other, (a, b, c, d) in enumerate(extents)
        ):
            retained.append(candidates[index])
    return retained


def row_geometry(
    spec: FieldSpec,
    packet: dict[str, Any],
    cover: dict[str, Any],
    cell: int,
    interval: tuple[Q, Q],
    *,
    budget: kernel.Budget,
) -> dict[str, Any]:
    require(cell in spec.positive_cells, "row outside positive cells")
    core, halfwidth, cosine, sine = kernel.row_envelope(interval)
    world = [
        (kernel.B / 2 + (kernel.L - kernel.B) * x, kernel.B / 2 + (kernel.L - kernel.B) * y)
        for x, y in (kernel.point(vertex) for vertex in cover["cells"][cell]["vertices"])
    ]
    legal = kernel.intersect(
        world,
        [
            (Q(1), Q(0), kernel.L / 2 + halfwidth),
            (Q(-1), Q(0), -kernel.L / 2 + halfwidth),
            (Q(0), Q(1), kernel.L / 2 + halfwidth),
            (Q(0), Q(-1), -kernel.L / 2 + halfwidth),
        ],
    )
    require(kernel.area2(legal) > 0, "degenerate row domain requires separate proof")
    domain = [kernel.rotate(point, cosine, sine) for point in legal]
    cert = packet["certificate"]
    denominator = cert["coordinate_denominator"]
    sites = [
        kernel.rotate((Q(x, denominator), Q(y, denominator)), cosine, sine)
        for x, y in cert["sites"]
    ]
    radius = core / 2
    physical_atoms: list[tuple[int, str, Polygon]] = []
    for indices, weight, source_id in spec.features:
        region = kernel.intersect(
            domain, majority_halfplanes([sites[index] for index in indices], radius)
        )
        if kernel.area2(region) > 0:
            physical_atoms.append((weight, f"TRUE:{source_id}", region))
    for index, weight in spec.point_charges:
        region = kernel.intersect(domain, kernel.box_halfplanes(sites[index], radius))
        if kernel.area2(region) > 0:
            physical_atoms.append((weight, f"point:{index}", region))
    candidates: list[tuple[Q, str, Polygon]] = []
    if not spec.weighted_features:
        candidates.extend(
            (kernel.area2(region), "TRUE", region) for _, _, region in physical_atoms
        )
    for owner in spec.owners:
        if owner == cell:
            continue
        for index, value in enumerate(packet["ownership_points_field"][owner]):
            captured = kernel.intersect(
                domain,
                kernel.box_halfplanes(kernel.rotate(kernel.point(value), cosine, sine), radius),
            )
            if kernel.area2(captured) > 0:
                candidates.append(
                    (kernel.area2(captured), f"owner:{owner}:point:{index}", captured)
                )
    eligible = len(candidates)
    if spec.weighted_features:
        candidates = maximal_collision_regions(candidates)
    if spec.max_regions is not None:
        candidates.sort(key=lambda row: row[0], reverse=True)
        candidates = candidates[: spec.max_regions]
    try:
        if spec.weighted_features:
            atoms = physical_atoms + [
                (spec.cell_charge, name, region) for _, name, region in candidates
            ]
            proof = weighted_union_cover(domain, atoms, spec.cell_charge, budget=budget)
        else:
            proof = kernel.exact_union_cover(
                domain, [row[2] for row in candidates], budget=budget
            )
    except ValueError as error:
        if spec.max_regions is not None and str(error).startswith(
            ("row uncovered at exact x=", "weighted row uncovered")
        ):
            reason = (
                f"selected {spec.max_regions}-region subset did not cover "
                f"cell {cell} interval {interval}"
            )
            raise kernel.IncompleteError(reason) from error
        raise
    return {
        "cell": cell,
        "interval": [str(interval[0]), str(interval[1])],
        "core_side": str(core),
        "parent_center_halfwidth": str(halfwidth),
        "domain_area_twice": str(kernel.area2(domain)),
        "eligible_regions": eligible,
        "selected_regions": len(candidates),
        "selected_region_ids": [row[1] for row in candidates],
        "physical_atom_ids": [name for _, name, _ in physical_atoms],
        "required_charge": spec.cell_charge,
        **proof,
    }


def transfer_cases(
    spec: FieldSpec,
    packet: dict[str, Any],
    cover: dict[str, Any],
    baseline: dict[str, Any],
) -> dict[str, list[int]]:
    canonical = canonical_masks(cover)
    support = set(spec.owners)
    thresholds = packet["threshold_units"]

    def applicable(mask: tuple[int, ...]) -> bool:
        return (
            support.issubset(mask)
            and sum(thresholds[cell] for cell in mask) > spec.charge_budget
        )

    direct = [index for index, mask in enumerate(canonical) if applicable(mask)]
    transferred = [
        index
        for index, mask in enumerate(canonical)
        if applicable(mask) or applicable(tuple(sorted(15 - cell for cell in mask)))
    ]
    if spec.expected_direct:
        require(len(direct) == spec.expected_direct, "direct transfer count changed")
    require(
        len(transferred) == spec.expected_transferred, "whole-half-turn transfer count changed"
    )
    entries = [
        row
        for row in baseline["certificates"]
        if row.get("family") == "field" and row.get("source_sha256") == spec.packet.decoded_sha
    ]
    require(len(entries) == 1, "A1 field certificate identity changed")
    listed = entries[0]["cases"]
    require(
        isinstance(listed, list)
        and len(listed) == len(transferred)
        and all(type(value) is int for value in listed)
        and len(set(listed)) == len(listed)
        and set(listed) == set(transferred),
        "A1 transferred case IDs differ",
    )
    return {"direct_case_ids": direct, "transferred_case_ids": transferred}


def _budget(budget: kernel.Budget, work: int, phase: str) -> None:
    if time.monotonic() >= budget.deadline or work >= budget.max_nodes:
        raise kernel.IncompleteError(f"global ceiling before {phase}")


def _check_row(
    row: tuple[int, int, tuple[Q, Q]],
    *,
    spec: FieldSpec,
    packet: dict[str, Any],
    cover: dict[str, Any],
    budget: kernel.Budget,
) -> dict[str, Any]:
    _budget(budget, 0, "start row")
    cell, index, interval = row
    return {
        "row_index": index,
        **row_geometry(spec, packet, cover, cell, interval, budget=budget),
    }


def all_geometry(
    spec: FieldSpec,
    packet: dict[str, Any],
    audit: dict[str, Any],
    cover: dict[str, Any],
    baseline: dict[str, Any],
    *,
    budget: kernel.Budget,
    workers: int = 1,
) -> dict[str, Any]:
    require(1 <= workers <= 4, "workers must be between 1 and 4")
    rows = proposed_rows(spec, audit)
    owner_keys = [
        (owner, index) for owner, count in spec.owner_lengths for index in range(count)
    ]
    done_points: list[dict[str, Any]] = []
    done_rows: list[dict[str, Any]] = []
    work = 0
    try:
        for owner, index in owner_keys:
            _budget(budget, work, "next owner point")
            proof = kernel.ownership(
                kernel.cell_vertices(cover, owner),
                kernel.point(packet["ownership_points_field"][owner][index]),
                budget=kernel.Budget(budget.deadline, budget.max_nodes - work),
            )
            work += proof["nodes"]
            done_points.append({"owner": owner, "point_index": index, **proof})
        check = partial(_check_row, spec=spec, packet=packet, cover=cover, budget=budget)
        if workers == 1:
            for row in rows:
                _budget(budget, work, "next row")
                proof = check(row)
                work += proof["events"] + proof["probes"]
                done_rows.append(proof)
        else:
            # Ordered delivery preserves the exact obligation inventory. Each child
            # shares the wall deadline; the parent enforces aggregate work before PASS.
            with ProcessPoolExecutor(max_workers=workers) as pool:
                for proof in pool.map(check, rows, chunksize=1, buffersize=workers):
                    _budget(budget, work, "next parallel row")
                    work += proof["events"] + proof["probes"]
                    done_rows.append(proof)
        _budget(budget, work, "transfer")
        transfer = transfer_cases(spec, packet, cover, baseline)
        _budget(budget, work, "PASS return")
    except kernel.IncompleteError as error:
        return {
            "status": "INCOMPLETE",
            "reason": str(error),
            "ownership_checked": done_points,
            "ownership_pending": [
                {"owner": owner, "point_index": index}
                for owner, index in owner_keys[len(done_points) :]
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
        "status": "PASS_ONE_FIELD_GEOMETRY_AND_TRANSFER",
        "mask_index": spec.mask_index,
        "ownership_checked": done_points,
        "ownership_pending": [],
        "rows_checked": done_rows,
        "rows_pending": [],
        "work_units": work,
        "ownership_points": len(done_points),
        "positive_cell_rows": len(done_rows),
        "canonical_cases_excluded": len(transfer["transferred_case_ids"]),
        "geometry_verified": True,
        "validated_field_certificates": 1,
        "transfer": transfer,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mask-index", type=int, choices=tuple(SPECS), required=True)
    parser.add_argument("--objects", type=Path, required=True)
    parser.add_argument("--cover", type=Path, required=True)
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--workers", type=int, choices=range(1, 5), default=1)
    parser.add_argument("--owner", type=int)
    parser.add_argument("--point", type=int, default=0)
    parser.add_argument("--row-cell", type=int)
    parser.add_argument("--row-index", type=int, default=0)
    parser.add_argument("--max-seconds", type=float, default=30.0)
    parser.add_argument("--max-work", type=int, default=100000)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    if not math.isfinite(args.max_seconds) or args.max_seconds <= 0 or args.max_work <= 0:
        parser.error("ceilings must be positive and finite")
    spec = SPECS[args.mask_index]
    checker_source = Path(__file__).read_bytes()
    child_start = resource.getrusage(resource.RUSAGE_CHILDREN)
    start, cpu = time.monotonic(), time.process_time()
    result: dict[str, Any]
    try:
        packet, audit, cover = load_sources(spec, args.objects, args.cover)
        admit(spec, packet, audit, cover)
        kernel.admit_d4_receipt()
        budget = kernel.Budget(start + args.max_seconds, args.max_work)
        if args.all:
            require(
                args.owner is None and args.row_cell is None,
                "--all cannot select one obligation",
            )
            baseline = kernel.pinned_gzip(
                PACKET_ROOT / "receipts/case-census/objects" / f"{kernel.A1_SHA}.gz",
                packed_bytes=26100,
                packed_sha=kernel.A1_LFS_SHA,
                raw_bytes=122029,
                raw_sha=kernel.A1_SHA,
            )
            result = all_geometry(
                spec, packet, audit, cover, baseline, budget=budget, workers=args.workers
            )
        elif args.row_cell is None:
            require(args.owner in spec.owners, "owner outside supported scope")
            points = packet["ownership_points_field"][args.owner]
            require(0 <= args.point < len(points), "point index outside owner group")
            proof = kernel.ownership(
                kernel.cell_vertices(cover, args.owner),
                kernel.point(points[args.point]),
                budget=budget,
            )
            result = {
                "status": "PASS_ONE_OWNERSHIP_POINT_ONLY",
                "owner": args.owner,
                "point": args.point,
                "proof": proof,
            }
        else:
            require(args.row_cell in spec.positive_cells, "row outside positive cells")
            rows = [
                row for row in audit["independent_row_proofs"] if row["cell"] == args.row_cell
            ]
            require(0 <= args.row_index < len(rows), "row index outside proposal inventory")
            source = rows[args.row_index]
            interval = Q(source["interval"][0]), Q(source["interval"][1])
            proof = row_geometry(spec, packet, cover, args.row_cell, interval, budget=budget)
            result = {
                "status": "PASS_ONE_ROW_ONLY",
                "row_index": args.row_index,
                "proof": proof,
            }
    except kernel.IncompleteError as error:
        result = {"status": "INCOMPLETE", "reason": str(error)}
    except (ValueError, KeyError, IndexError, TypeError, OSError) as error:
        result = {"status": "REFUSED", "reason": str(error)}
    if Path(__file__).read_bytes() != checker_source:
        result = {"status": "REFUSED", "reason": "checker source changed during execution"}
    child_end = resource.getrusage(resource.RUSAGE_CHILDREN)
    result.setdefault("geometry_verified", False)
    result.setdefault("canonical_cases_excluded", 0)
    result.update(
        mask_index=spec.mask_index,
        upstream_source_revision=kernel.SOURCE_REVISION,
        packet_sha256=spec.packet.decoded_sha,
        audit_proposal_sha256=spec.audit.decoded_sha,
        cover_sha256=kernel.COVER_SHA,
        d4_receipt_sha256=kernel.D4_RESULT_SHA,
        frozen_geometry_kernel_sha256=KERNEL_SHA,
        checker_sha256=kernel.sha(checker_source),
        global_optimality_proved=False,
        wall_seconds=time.monotonic() - start,
        process_cpu_seconds=time.process_time() - cpu,
        child_cpu_seconds=(
            child_end.ru_utime
            + child_end.ru_stime
            - child_start.ru_utime
            - child_start.ru_stime
        ),
        wall_ceiling_seconds=args.max_seconds,
        work_ceiling=args.max_work,
        workers=args.workers,
        cpu_scope="coordinator_only" if args.workers > 1 else "whole_process",
    )
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.open("x", encoding="utf-8").write(encoded)
    print(encoded, end="")
    return 0 if result["status"].startswith("PASS_") else 2


if __name__ == "__main__":
    sys.exit(main())
