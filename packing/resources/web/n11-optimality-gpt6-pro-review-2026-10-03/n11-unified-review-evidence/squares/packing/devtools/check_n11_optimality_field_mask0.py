"""Independent rational geometry checks for the one n=11 mask-0 field packet.

The packet and upstream audit provide points and candidate angle intervals only.
This checker never accepts their PASS flags or geometrical conclusions. A result for
one point or row is explicitly partial and proves no canonical case exclusion.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
import sys
import time
from fractions import Fraction as Q
from itertools import combinations, pairwise
from pathlib import Path
from typing import Any, NamedTuple

REPO = Path(__file__).resolve().parents[2]
PACKET = REPO / "packing/resources/web/n11-optimality-2026-09-29"
SOURCE_REVISION = "f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c"
FIELD_SHA = "14164a3d91117055000ae78cd15a4e8ad5d6bb2c27ce24ff080605b873a93340"
FIELD_LFS_SHA = "0759a9f56e0035713996287fa2bd540c29ad60820da5da40250136375442f832"
AUDIT_SHA = "1a56056ad4d19786e41e248f0ef60866ad2021370e9ef809faa471fb679f8a54"
AUDIT_LFS_SHA = "156102cf720236023cf5ec86cc697a5d6d2615fcf0eaa82336574be49d8856a2"
COVER_SHA = "df7938d9ba27095a38fabe45f8b26b259a2cc896c2ae4aac6bae874f417adc4e"
COVER_LFS_SHA = "7c6d14012f06eb892912a50c93cc7408ce1f90524d46693c6178a01ceae71a99"
A1_SHA = "04fa1ebb37f5dace29946224fe8c7c5d8a1bedb4fa860c65b359f4200415de57"
A1_LFS_SHA = "adbb5f181a18d157fe12a5a62055b01bf7eff7a91ce08b8aeca6f01408953d21"
D4_RESULT_SHA = "c4aa4df460593abcb51cd4ebaaf916c78a6a718659bb6b7bf4245e3e67e6c00e"
D4_CHECKER_SHA = "19f4b0a47afd6acb327e85bd4a98ca2a43d2fdaa49aeb0edd30aa12d1b6aac1d"
U = Q(387708359002281417731, 10**20)
L = Q(191, 50)
B = L / U
OWNER_SUPPORT = (0, 1, 2, 3, 6)
POSITIVE_CELLS = (1, 2)
Point = tuple[Q, Q]
Polygon = list[Point]


class IncompleteError(Exception):
    """A bounded check could not finish without making a proof claim."""


class Budget(NamedTuple):
    deadline: float
    max_nodes: int


def require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def strict_json(data: bytes) -> dict[str, Any]:
    def pairs(rows: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in rows:
            require(key not in result, f"duplicate JSON key: {key}")
            result[key] = value
        return result

    result: Any = json.loads(data, object_pairs_hook=pairs)
    require(isinstance(result, dict), "JSON root is not an object")
    return result


def pinned_gzip(
    path: Path, *, packed_bytes: int, packed_sha: str, raw_bytes: int, raw_sha: str
) -> dict[str, Any]:
    require(path.is_file() and path.stat().st_size == packed_bytes, f"size mismatch: {path}")
    packed = path.read_bytes()
    require(sha(packed) == packed_sha, f"compressed SHA mismatch: {path}")
    data = gzip.decompress(packed)
    require(
        len(data) == raw_bytes and sha(data) == raw_sha, f"decoded identity mismatch: {path}"
    )
    return strict_json(data)


def point(value: Any) -> Point:
    require(isinstance(value, list) and len(value) == 2, "expected a two-coordinate point")
    return Q(value[0]), Q(value[1])


def qpoint(value: Any) -> Point:
    return Q(value[0]), Q(value[1])


def area2(poly: Polygon) -> Q:
    if len(poly) < 3:
        return Q(0)
    return abs(
        sum(
            (p[0] * q[1] - p[1] * q[0] for p, q in zip(poly, poly[1:] + poly[:1], strict=True)),
            Q(0),
        )
    )


def clip(poly: Polygon, line: tuple[Q, Q, Q]) -> Polygon:
    """Intersect even a point or segment polygon with the closed half-plane ax+by<=c."""
    if not poly:
        return []
    a, b, c = line
    out: Polygon = []
    for p, q in zip(poly, poly[1:] + poly[:1], strict=True):
        dp = a * p[0] + b * p[1] - c
        dq = a * q[0] + b * q[1] - c
        if dp <= 0 and (not out or out[-1] != p):
            out.append(p)
        if (dp < 0 < dq) or (dq < 0 < dp):
            z = dp / (dp - dq)
            cross = (p[0] + z * (q[0] - p[0]), p[1] + z * (q[1] - p[1]))
            if not out or out[-1] != cross:
                out.append(cross)
        elif dp == 0 and dq > 0 and (not out or out[-1] != p):
            out.append(p)
        elif dq == 0 and dp > 0 and (not out or out[-1] != q):
            out.append(q)
    if len(out) > 1 and out[-1] == out[0]:
        out.pop()
    return out


def cell_vertices(cover: dict[str, Any], owner: int) -> Polygon:
    cells = cover["cells"]
    require(len(cells) == 16, "cover cell count changed")
    vertices = [point(v) for v in cells[owner]["vertices"]]
    require(len(vertices) >= 3 and area2(vertices) > 0, f"cell {owner}: degenerate cover")
    return [(Q(1, 2) + (U - 1) * x, Q(1, 2) + (U - 1) * y) for x, y in vertices]


def trig(t: Q) -> tuple[Q, Q]:
    return (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)


def projection_range(
    vector: Point, c_interval: tuple[Q, Q], s_interval: tuple[Q, Q]
) -> tuple[Q, Q]:
    a, d = vector
    clo, chi = c_interval
    slo, shi = s_interval
    values = (a * clo + d * slo, a * clo + d * shi, a * chi + d * slo, a * chi + d * shi)
    return min(values), max(values)


def ownership(
    polygon: Polygon, field_point: Point, *, budget: Budget, max_depth: int = 20
) -> dict[str, Any]:
    """Prove strict capture over all legal centers and the full angle interval."""
    unit = field_point[0] / B, field_point[1] / B
    require(all(0 <= x <= L for x in field_point), "field point outside container")
    max_distance2 = max((unit[0] - v[0]) ** 2 + (unit[1] - v[1]) ** 2 for v in polygon)
    if max_distance2 < Q(1, 4):
        return {
            "method": "strict_disk_vertex_bound",
            "maximum_vertex_distance_squared": str(max_distance2),
            "nodes": 0,
            "leaves": 1,
            "empty_leaves": 0,
            "strict_squared_distance_slack": str(Q(1, 4) - max_distance2),
        }
    stack = [(Q(0), Q(1), 0)]
    nodes = leaves = empty = 0
    margin = Q(1, 2)
    deepest = 0
    while stack:
        if time.monotonic() >= budget.deadline or nodes >= budget.max_nodes:
            raise IncompleteError(f"ownership ceiling: nodes={nodes}, pending={len(stack)}")
        lo, hi, depth = stack.pop()
        nodes += 1
        clo, slo = trig(lo)
        chi, shi = trig(hi)
        h = min(clo + slo, chi + shi) / 2
        legal = polygon
        for axis in (0, 1):
            normal = (Q(1), Q(0)) if axis == 0 else (Q(0), Q(1))
            legal = clip(legal, (-normal[0], -normal[1], -h))
            legal = clip(legal, (normal[0], normal[1], U - h))
        deepest = max(deepest, depth)
        if not legal:
            leaves += 1
            empty += 1
            continue
        local = Q(1, 2)
        for x, y in legal:
            dx, dy = unit[0] - x, unit[1] - y
            for a, d in ((dx, dy), (dy, -dx)):
                lower, upper = projection_range((a, d), (chi, clo), (slo, shi))
                local = min(local, Q(1, 2) - max(-lower, upper))
        if local > 0:
            margin = min(margin, local)
            leaves += 1
        elif depth < max_depth:
            mid = (lo + hi) / 2
            stack.append((mid, hi, depth + 1))
            stack.append((lo, mid, depth + 1))
        else:
            raise IncompleteError(
                f"ownership depth ceiling: interval=({lo},{hi}), nodes={nodes}"
            )
    return {
        "method": "strict_wall_interval_bound",
        "maximum_vertex_distance_squared": str(max_distance2),
        "nodes": nodes,
        "leaves": leaves,
        "empty_leaves": empty,
        "minimum_margin": str(margin),
        "deepest": deepest,
    }


def load_sources(
    object_dir: Path, cover_path: Path
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    packet = pinned_gzip(
        object_dir / f"{FIELD_SHA}.gz",
        packed_bytes=3749,
        packed_sha=FIELD_LFS_SHA,
        raw_bytes=28065,
        raw_sha=FIELD_SHA,
    )
    audit = pinned_gzip(
        object_dir / f"{AUDIT_SHA}.gz",
        packed_bytes=29707,
        packed_sha=AUDIT_LFS_SHA,
        raw_bytes=201961,
        raw_sha=AUDIT_SHA,
    )
    cover = pinned_gzip(
        cover_path,
        packed_bytes=25016,
        packed_sha=COVER_LFS_SHA,
        raw_bytes=773471,
        raw_sha=COVER_SHA,
    )
    return packet, audit, cover


def admit_d4_receipt() -> None:
    receipt = PACKET / "receipts/d4-independent/result.json"
    raw = receipt.read_bytes()
    require(sha(raw) == D4_RESULT_SHA, "accepted D4 receipt changed")
    result = strict_json(raw)
    require(
        result.get("status") == "PASS_INDEPENDENT_CONDITIONAL_D4_BRIDGE",
        "D4 receipt status changed",
    )
    require(
        result.get("input_sha256", {}).get("cover") == COVER_SHA, "D4 cover binding changed"
    )
    require(result.get("checker_sha256") == D4_CHECKER_SHA, "D4 checker identity changed")
    checker = REPO / "packing/devtools/check_n11_optimality_d4.py"
    require(sha(checker.read_bytes()) == D4_CHECKER_SHA, "D4 checker source changed")


def admit(packet: dict[str, Any], audit: dict[str, Any], cover: dict[str, Any]) -> None:
    require(audit.get("packet_sha256") == FIELD_SHA, "audit packet binding changed")
    require(
        packet.get("cover_sha256") == audit.get("cover_sha256") == COVER_SHA,
        "cover binding changed",
    )
    require(Q(packet["parent_Uplus"]) == Q(audit["parent_Uplus"]) == U, "U premise changed")
    require(Q(audit["parent_side"]) == B, "B=L/U premise changed")
    require(
        packet.get("mask_index") == audit.get("canonical_mask_index") == 0, "mask index changed"
    )
    require(
        packet.get("mask") == audit.get("mask") == cover["canonical_eleven_cell_subsets"][0],
        "mask changed",
    )
    cert = packet["certificate"]
    require(
        Q(cert["L"]) == L and cert["coordinate_denominator"] == 10**10, "field scale changed"
    )
    require(len(cert["sites"]) == len(cert["point_weights"]) == 5, "field site count changed")
    denominator = cert["coordinate_denominator"]
    require(
        all(
            isinstance(site, list)
            and len(site) == 2
            and all(type(value) is int and 0 <= value <= L * denominator for value in site)
            for site in cert["sites"]
        ),
        "field sites outside rational container",
    )
    require(len({tuple(site) for site in cert["sites"]}) == 5, "duplicate field site")
    require(cert["point_weights"] == [0] * 5, "field point weights changed")
    require(
        cert["features"]
        == [
            {
                "kind": "majority_hull",
                "indices": [0, 1, 2, 3, 4],
                "threshold": 3,
                "weight": 1,
                "source_physical_feature": 931,
            }
        ],
        "majority feature changed",
    )
    require(cert["budget_units"] == 1, "physical budget changed")
    require(
        packet.get("threshold_units") == [int(i in POSITIVE_CELLS) for i in range(16)],
        "cell thresholds changed",
    )
    require(
        packet.get("conditional_owner_support") == list(OWNER_SUPPORT), "owner support changed"
    )
    require(
        packet.get("conditional_ownership") == "cell_owned_points",
        "ownership semantics changed",
    )
    require(len(packet["ownership_points_field"]) == 16, "ownership field inventory changed")
    raw = list(combinations(range(16), 11))

    def turn(mask: tuple[int, ...]) -> tuple[int, ...]:
        return tuple(sorted(15 - i for i in mask))

    canonical = sorted({min(mask, turn(mask)) for mask in raw})
    require(len(canonical) == 2184, "canonical mask count changed")
    require(
        cover.get("all_eleven_cell_subsets") == [list(mask) for mask in raw],
        "raw mask ordering changed",
    )
    require(
        cover.get("canonical_eleven_cell_subsets") == [list(mask) for mask in canonical],
        "canonical mask ordering changed",
    )


def quadratic_nonnegative(a: Q, b: Q, c: Q, left: Q, right: Q) -> bool:
    probes = [left, right]
    if c > 0:
        critical = -b / (2 * c)
        if left < critical < right:
            probes.append(critical)
    return all(a + b * t + c * t * t >= 0 for t in probes)


def row_envelope(interval: tuple[Q, Q]) -> tuple[Q, Q, Q, Q]:
    left, right = interval
    require(0 <= left < right <= 1, "row interval outside closed angle domain")
    mid = (left + right) / 2
    c, s = trig(mid)
    endpoint = [trig(t) for t in interval]
    factors = [c * cz + s * sz + abs(c * sz - s * cz) for cz, sz in endpoint]
    factor = max(factors)
    min_width = min(cz + sz for cz, sz in endpoint)
    core = (B - Q(1, 10**12)) / factor
    halfwidth = L / 2 - B * min_width / 2
    require(0 < core < B and core * factor < B, "strict inner core fails")
    require(
        quadratic_nonnegative(factor - c - s, 2 * (c - s), factor + c + s, left, mid)
        and quadratic_nonnegative(factor - c + s, -2 * (c + s), factor + c - s, mid, right),
        "full-angle core envelope fails",
    )
    require(
        quadratic_nonnegative(1 - min_width, Q(2), -1 - min_width, left, right),
        "full-angle legal-wall envelope fails",
    )
    return core, halfwidth, c, s


def rotate(p: Point, c: Q, s: Q) -> Point:
    x, y = p[0] - L / 2, p[1] - L / 2
    return c * x + s * y, -s * x + c * y


def intersect(poly: Polygon, lines: list[tuple[Q, Q, Q]]) -> Polygon:
    for line in lines:
        poly = clip(poly, line)
        if not poly:
            break
    return poly


def primitive_normal(dx: Q, dy: Q) -> Point:
    denominator = math.lcm(dx.denominator, dy.denominator)
    a, b = int(dx * denominator), int(dy * denominator)
    scale = math.gcd(abs(a), abs(b))
    require(scale > 0, "zero normal")
    a, b = a // scale, b // scale
    if a < 0 or (a == 0 and b < 0):
        a, b = -a, -b
    return Q(a), Q(b)


def true_halfplanes(sites: list[Point], radius: Q) -> list[tuple[Q, Q, Q]]:
    """Median-strip TRUE region; between these normal events its supports are affine."""
    normals = {(Q(1), Q(0)), (Q(0), Q(1))}
    for number, p in enumerate(sites):
        for q in sites[number + 1 :]:
            dx, dy = q[1] - p[1], p[0] - q[0]
            if dx or dy:
                normals.add(primitive_normal(dx, dy))
    rows: list[tuple[Q, Q, Q]] = []
    for a, b in sorted(normals):
        median = sorted(a * x + b * y for x, y in sites)[2]
        margin = radius * (abs(a) + abs(b))
        rows.extend(((a, b, median + margin), (-a, -b, -median + margin)))
    return rows


def box_halfplanes(center: Point, radius: Q) -> list[tuple[Q, Q, Q]]:
    x, y = center
    return [
        (Q(1), Q(0), x + radius),
        (Q(-1), Q(0), -x + radius),
        (Q(0), Q(1), y + radius),
        (Q(0), Q(-1), -y + radius),
    ]


def vertical_interval(poly: Polygon, x: Q) -> tuple[Q, Q] | None:
    ordinates: list[Q] = []
    for p, q in zip(poly, poly[1:] + poly[:1], strict=True):
        if min(p[0], q[0]) <= x <= max(p[0], q[0]):
            if p[0] == q[0]:
                ordinates.extend((p[1], q[1]))
            else:
                ordinates.append(p[1] + (x - p[0]) * (q[1] - p[1]) / (q[0] - p[0]))
    return (min(ordinates), max(ordinates)) if ordinates else None


def edge_lines(polygons: list[Polygon]) -> list[tuple[Q, Q, Q, Q]]:
    """Nonvertical edge as y=m*x+b over its closed x range."""
    lines: list[tuple[Q, Q, Q, Q]] = []
    for poly in polygons:
        for p, q in zip(poly, poly[1:] + poly[:1], strict=True):
            if p[0] == q[0]:
                continue
            slope = (q[1] - p[1]) / (q[0] - p[0])
            lines.append((min(p[0], q[0]), max(p[0], q[0]), slope, p[1] - slope * p[0]))
    return lines


def covers_vertical(domain: Polygon, regions: list[Polygon], x: Q) -> bool:
    target = vertical_interval(domain, x)
    if target is None:
        raise ValueError("coverage probe outside domain")
    spans = [span for poly in regions if (span := vertical_interval(poly, x)) is not None]
    spans.sort()
    cursor = target[0]
    for low, high in spans:
        if low > cursor:
            return False
        cursor = max(cursor, high)
        if cursor >= target[1]:
            return True
    return False


def exact_union_cover(
    domain: Polygon, regions: list[Polygon], *, budget: Budget
) -> dict[str, int]:
    """Exact vertical sweep at every edge event and between consecutive events."""
    require(area2(domain) > 0, "degenerate row domain needs a separate proof")
    require(bool(regions), "no eligible charge regions")
    polygons = [domain, *regions]
    left, right = min(p[0] for p in domain), max(p[0] for p in domain)
    events = {p[0] for poly in polygons for p in poly if left <= p[0] <= right}
    lines = edge_lines(polygons)
    for number, (a0, a1, m, b) in enumerate(lines):
        if time.monotonic() >= budget.deadline:
            raise IncompleteError(f"row event construction timed out after {number} edges")
        for z0, z1, n, d in lines[number + 1 :]:
            if m == n:
                continue
            start, stop = max(a0, z0, left), min(a1, z1, right)
            if start <= stop:
                crossing = (d - b) / (m - n)
                if start <= crossing <= stop:
                    events.add(crossing)
        if len(events) > budget.max_nodes:
            raise IncompleteError(f"row event ceiling: events={len(events)}")
    positions = sorted(events)
    require(positions[0] == left and positions[-1] == right, "row domain endpoint missing")
    probes = [positions[0]]
    for a, b in pairwise(positions):
        probes.extend(((a + b) / 2, b))
    if len(probes) > budget.max_nodes:
        raise IncompleteError(f"row probe ceiling: probes={len(probes)}")
    for number, x in enumerate(probes):
        if time.monotonic() >= budget.deadline:
            raise IncompleteError(f"row sweep timeout: checked={number}, total={len(probes)}")
        require(covers_vertical(domain, regions, x), f"row uncovered at exact x={x}")
    return {"events": len(positions), "probes": len(probes), "edge_segments": len(lines)}


def row_geometry(
    packet: dict[str, Any],
    cover: dict[str, Any],
    cell: int,
    interval: tuple[Q, Q],
    *,
    budget: Budget,
) -> dict[str, Any]:
    require(cell in POSITIVE_CELLS, "row outside positive cells")
    core, h, c, s = row_envelope(interval)
    world = [
        (B / 2 + (L - B) * x, B / 2 + (L - B) * y)
        for x, y in (point(v) for v in cover["cells"][cell]["vertices"])
    ]
    legal = intersect(
        world,
        [
            (Q(1), Q(0), L / 2 + h),
            (Q(-1), Q(0), -L / 2 + h),
            (Q(0), Q(1), L / 2 + h),
            (Q(0), Q(-1), -L / 2 + h),
        ],
    )
    require(area2(legal) > 0, "degenerate row domain needs a separate proof")
    domain = [rotate(p, c, s) for p in legal]
    cert = packet["certificate"]
    denominator = cert["coordinate_denominator"]
    sites = [rotate((Q(x, denominator), Q(y, denominator)), c, s) for x, y in cert["sites"]]
    radius = core / 2
    true_region = intersect(domain, true_halfplanes(sites, radius))
    regions = [true_region] if area2(true_region) > 0 else []
    for owner in OWNER_SUPPORT:
        if owner == cell:
            continue
        for value in packet["ownership_points_field"][owner]:
            captured = intersect(domain, box_halfplanes(rotate(point(value), c, s), radius))
            if area2(captured) > 0:
                regions.append(captured)
    proof = exact_union_cover(domain, regions, budget=budget)
    return {
        "cell": cell,
        "interval": [str(interval[0]), str(interval[1])],
        "core_side": str(core),
        "parent_center_halfwidth": str(h),
        "domain_area_twice": str(area2(domain)),
        "eligible_regions": len(regions),
        **proof,
    }


def proposed_rows(audit: dict[str, Any]) -> list[tuple[int, int, tuple[Q, Q]]]:
    raw = audit["independent_row_proofs"]
    require(isinstance(raw, list) and len(raw) == 136, "row proposal count changed")
    by_cell: dict[int, list[tuple[Q, Q]]] = {1: [], 2: []}
    for row in raw:
        cell = row["cell"]
        require(
            type(cell) is int and cell in POSITIVE_CELLS, "row proposal outside positive cells"
        )
        interval = row["interval"]
        require(isinstance(interval, list) and len(interval) == 2, "malformed row interval")
        by_cell[cell].append((Q(interval[0]), Q(interval[1])))
    require(len(by_cell[1]) == 67 and len(by_cell[2]) == 69, "positive-cell row counts changed")
    ordered: list[tuple[int, int, tuple[Q, Q]]] = []
    for cell in POSITIVE_CELLS:
        intervals = sorted(by_cell[cell])
        require(
            intervals[0][0] == 0 and intervals[-1][1] == 1,
            f"cell {cell}: angle endpoints missing",
        )
        require(len(set(intervals)) == len(intervals), f"cell {cell}: duplicate row interval")
        for left, right in intervals:
            require(0 <= left < right <= 1, f"cell {cell}: malformed row interval")
        for (_, end), (start, _) in pairwise(intervals):
            require(end == start, f"cell {cell}: row gap or overlap")
        ordered.extend((cell, index, interval) for index, interval in enumerate(intervals))
    return ordered


def transferred_cases(
    packet: dict[str, Any], cover: dict[str, Any], baseline: dict[str, Any]
) -> dict[str, Any]:
    canonical = [tuple(mask) for mask in cover["canonical_eleven_cell_subsets"]]
    support = set(OWNER_SUPPORT)
    thresholds = packet["threshold_units"]

    def applicable(mask: tuple[int, ...]) -> bool:
        return support.issubset(mask) and sum(thresholds[cell] for cell in mask) > 1

    direct = [index for index, mask in enumerate(canonical) if applicable(mask)]
    transferred = [
        index
        for index, mask in enumerate(canonical)
        if applicable(mask) or applicable(tuple(sorted(15 - cell for cell in mask)))
    ]
    require(len(direct) == 453 and len(transferred) == 459, "mask-0 transfer counts changed")
    entries = [
        row
        for row in baseline["certificates"]
        if row.get("family") == "field" and row.get("source_sha256") == FIELD_SHA
    ]
    require(len(entries) == 1, "A1 mask-0 certificate identity changed")
    listed = entries[0]["cases"]
    require(
        isinstance(listed, list)
        and len(listed) == 459
        and all(type(value) is int for value in listed)
        and len(set(listed)) == len(listed),
        "A1 mask-0 case list malformed",
    )
    require(set(listed) == set(transferred), "A1 mask-0 transfer list differs")
    return {"direct_case_ids": direct, "transferred_case_ids": transferred}


def check_global_budget(budget: Budget, work: int, phase: str) -> None:
    if time.monotonic() >= budget.deadline or work >= budget.max_nodes:
        raise IncompleteError(f"global ceiling before next {phase}")


def all_geometry(
    packet: dict[str, Any],
    audit: dict[str, Any],
    cover: dict[str, Any],
    baseline: dict[str, Any],
    *,
    budget: Budget,
) -> dict[str, Any]:
    rows = proposed_rows(audit)
    owner_keys = [
        (owner, index)
        for owner in OWNER_SUPPORT
        for index in range(len(packet["ownership_points_field"][owner]))
    ]
    require(len(owner_keys) == 55, "scoped ownership point count changed")
    checked_points: list[dict[str, Any]] = []
    checked_rows: list[dict[str, Any]] = []
    work = 0
    try:
        for owner, index in owner_keys:
            check_global_budget(budget, work, "owned point")
            proof = ownership(
                cell_vertices(cover, owner),
                point(packet["ownership_points_field"][owner][index]),
                budget=Budget(budget.deadline, budget.max_nodes - work),
            )
            work += proof["nodes"]
            checked_points.append({"owner": owner, "point_index": index, **proof})
        for cell, index, interval in rows:
            check_global_budget(budget, work, "row")
            proof = row_geometry(
                packet,
                cover,
                cell,
                interval,
                budget=Budget(budget.deadline, budget.max_nodes - work),
            )
            work += proof["events"] + proof["probes"]
            checked_rows.append({"row_index": index, **proof})
        check_global_budget(budget, work, "transfer audit")
        transfer = transferred_cases(packet, cover, baseline)
        check_global_budget(budget, work, "PASS return")
    except IncompleteError as error:
        return {
            "status": "INCOMPLETE",
            "reason": str(error),
            "ownership_checked": checked_points,
            "ownership_pending": [
                {"owner": owner, "point_index": index}
                for owner, index in owner_keys[len(checked_points) :]
            ],
            "rows_checked": checked_rows,
            "rows_pending": [
                {
                    "cell": cell,
                    "row_index": index,
                    "interval": [str(interval[0]), str(interval[1])],
                }
                for cell, index, interval in rows[len(checked_rows) :]
            ],
            "work_units": work,
            "canonical_cases_excluded": 0,
            "geometry_verified": False,
        }
    return {
        "status": "PASS_ONE_FIELD_MASK0_GEOMETRY_AND_TRANSFER",
        "ownership_checked": checked_points,
        "ownership_pending": [],
        "rows_checked": checked_rows,
        "rows_pending": [],
        "work_units": work,
        "ownership_points": len(checked_points),
        "positive_cell_rows": len(checked_rows),
        "canonical_cases_excluded": len(transfer["transferred_case_ids"]),
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
    parser.add_argument(
        "--all", action="store_true", help="check all 55 owners and all 136 rows"
    )
    parser.add_argument("--max-seconds", type=float, default=30.0)
    parser.add_argument("--max-nodes", type=int, default=10000)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    if not math.isfinite(args.max_seconds) or args.max_seconds <= 0 or args.max_nodes <= 0:
        parser.error("ceilings must be positive and finite")
    start, cpu = time.monotonic(), time.process_time()
    try:
        packet, audit, cover = load_sources(args.objects, args.cover)
        admit(packet, audit, cover)
        admit_d4_receipt()
        if args.all:
            require(args.row_cell is None, "--all cannot select one row")
            baseline = pinned_gzip(
                PACKET / "receipts/case-census/objects" / f"{A1_SHA}.gz",
                packed_bytes=26100,
                packed_sha=A1_LFS_SHA,
                raw_bytes=122029,
                raw_sha=A1_SHA,
            )
            result = all_geometry(
                packet,
                audit,
                cover,
                baseline,
                budget=Budget(start + args.max_seconds, args.max_nodes),
            )
        elif args.row_cell is None:
            require(args.owner in OWNER_SUPPORT, "owner outside scoped support")
            group = packet["ownership_points_field"][args.owner]
            require(0 <= args.point < len(group), "point index outside owner group")
            checked = ownership(
                cell_vertices(cover, args.owner),
                point(group[args.point]),
                budget=Budget(start + args.max_seconds, args.max_nodes),
            )
            result: dict[str, Any] = {
                "status": "PASS_ONE_OWNERSHIP_POINT_ONLY",
                "owner": args.owner,
                "point": args.point,
                "proof": checked,
            }
        else:
            rows = [r for r in audit["independent_row_proofs"] if r["cell"] == args.row_cell]
            require(0 <= args.row_index < len(rows), "row index outside proposal inventory")
            row = rows[args.row_index]
            interval = Q(row["interval"][0]), Q(row["interval"][1])
            checked = row_geometry(
                packet,
                cover,
                args.row_cell,
                interval,
                budget=Budget(start + args.max_seconds, args.max_nodes),
            )
            result = {
                "status": "PASS_ONE_ROW_ONLY",
                "row_index": args.row_index,
                "proof": checked,
            }
    except IncompleteError as error:
        result = {"status": "INCOMPLETE", "reason": str(error)}
    except (ValueError, KeyError, IndexError, TypeError, OSError) as error:
        result = {"status": "REFUSED", "reason": str(error)}
    result.setdefault("geometry_verified", False)
    result.setdefault("canonical_cases_excluded", 0)
    result.update(
        source_revision=SOURCE_REVISION,
        packet_sha256=FIELD_SHA,
        audit_proposal_sha256=AUDIT_SHA,
        cover_sha256=COVER_SHA,
        d4_receipt_sha256=D4_RESULT_SHA,
        checker_sha256=sha(Path(__file__).read_bytes()),
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
            "PASS_ONE_FIELD_MASK0_GEOMETRY_AND_TRANSFER",
        )
        else 2
    )


if __name__ == "__main__":
    sys.exit(main())
