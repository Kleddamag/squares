"""Independently check the mask-438 root seed and one conditional owner update.

The source supplies proposed residual polygons and kernel points. Only exact
geometry and complete closed row coverage can promote an owner update; a row
sample, a deadline, or an unsupported degenerate domain remains incomplete.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import subprocess
import sys
import time
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from strif import atomic_write_bytes, atomic_write_text

from devtools import check_n11_optimality_field_mask0 as geometry

REPO = Path(__file__).resolve().parents[2]
COVER = (
    REPO
    / "packing/resources/web/n11-optimality-2026-09-29/receipts/d4-independent/objects"
    / f"{geometry.COVER_SHA}.gz"
)
SEED_SHA = "b93be3358f7dfbf063d4109c52fd3bbbbfff9b34cb468c3123598b54cea72a56"
ADAPTIVE_SHA = "5452ed7fe20266ec81749b79c1e00f4e9a2ba75242b25d90b7fb696ca317d40a"
GEOMETRY_SHA = "75fc0238f2ac91af9dc9cf57bd00792343dcf3321c395adddebf0f3465113ce5"
MASK = (0, 1, 2, 3, 4, 8, 9, 10, 11, 13, 15)
OWNER = 2
Point = tuple[Q, Q]
Polygon = list[Point]


def require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def remaining(budget: geometry.Budget) -> float:
    seconds = budget.deadline - time.monotonic()
    if seconds <= 0:
        raise geometry.IncompleteError("pilot wall ceiling expired")
    return seconds


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def points(value: Any) -> Polygon:
    require(isinstance(value, list), "points must be a list")
    return [geometry.point(point) for point in value]


def hull(values: Polygon) -> Polygon:
    """Build an exact convex hull without using the publisher's hull routine."""

    ordered = sorted(set(values))
    if len(ordered) <= 2:
        return ordered

    def turn(a: Point, b: Point, c: Point) -> Q:
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

    lower: Polygon = []
    upper: Polygon = []
    for point in ordered:
        while len(lower) >= 2 and turn(lower[-2], lower[-1], point) <= 0:
            lower.pop()
        lower.append(point)
    for point in reversed(ordered):
        while len(upper) >= 2 and turn(upper[-2], upper[-1], point) <= 0:
            upper.pop()
        upper.append(point)
    return lower[:-1] + upper[:-1]


def convex(value: Any) -> Polygon:
    poly = points(value)
    require(bool(poly), "empty polygon is not a region")
    if len(poly) <= 2:
        return hull(poly)
    signs = [
        (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0])
        for a, b, c in zip(poly, poly[1:] + poly[:1], poly[2:] + poly[:2], strict=True)
    ]
    require(
        all(value >= 0 for value in signs) or all(value <= 0 for value in signs),
        "nonconvex region",
    )
    result = hull(poly)
    require(geometry.area2(poly) == geometry.area2(result), "region differs from convex hull")
    return result


def quadratic_positive(a: Q, b: Q, c: Q, lo: Q, hi: Q) -> bool:
    probes = [lo, hi]
    if c > 0:
        minimum = -b / (2 * c)
        if lo < minimum < hi:
            probes.append(minimum)
    return all(a + b * t + c * t * t > 0 for t in probes)


def strict_core(side: Q, lo: Q, hi: Q, cosine: Q, sine: Q) -> bool:
    """Check every proposed core corner over the complete closed angle row."""

    if side <= 0:
        return False
    for xsign, ysign in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        qx = side * (xsign * cosine - ysign * sine) / 2
        qy = side * (xsign * sine + ysign * cosine) / 2
        for sign in (-1, 1):
            if not quadratic_positive(
                geometry.B / 2 - sign * qx,
                -2 * sign * qy,
                geometry.B / 2 + sign * qx,
                lo,
                hi,
            ) or not quadratic_positive(
                geometry.B / 2 - sign * qy,
                2 * sign * qx,
                geometry.B / 2 + sign * qy,
                lo,
                hi,
            ):
                return False
    return True


def seed_points(
    seed: dict[str, Any], cover: dict[str, Any], *, budget: geometry.Budget
) -> dict[int, Polygon]:
    require(seed.get("mask_index") == 438 and tuple(seed.get("mask", [])) == MASK, "seed mask")
    require(seed.get("cover_sha256") == geometry.COVER_SHA, "seed cover binding")
    require(Q(seed["parent_Uplus"]) == geometry.U, "seed cap")
    require(cover["canonical_eleven_cell_subsets"][438] == list(MASK), "cover mask")
    source_groups = seed["owned_points"]
    require(
        isinstance(source_groups, list) and len(source_groups) == 16, "seed group inventory"
    )
    groups = {owner: points(source_groups[owner]) for owner in range(16)}
    require(sum(len(groups[owner]) for owner in MASK) == 130, "occupied seed census")
    for owner in MASK:
        cell = geometry.cell_vertices(cover, owner)
        for point in groups[owner]:
            geometry.ownership(cell, point, budget=budget)
    return groups


def selected_round(adaptive: Path, *, timeout: float) -> tuple[dict[str, Any], bytes]:
    query = (
        "{mask_index,mask,parent_Uplus,parent_side,cover_sha256,seed_sha256,branch,"
        "round:(.rounds[0]|{index,prior_owned_points,prior_snapshot_sha256,"
        "owner_inventory:(.cells|map(.owner)),cell:(.cells[]|select(.owner==2))})}"
    )
    process = subprocess.run(
        ["jq", "-c", query, str(adaptive)],
        capture_output=True,
        check=True,
        timeout=timeout,
    )
    value = geometry.strict_json(process.stdout)
    return value, process.stdout


def admit_prior(selected: dict[str, Any], groups: dict[int, Polygon]) -> dict[str, Any]:
    require(
        selected.get("mask_index") == 438 and tuple(selected.get("mask", [])) == MASK,
        "adaptive mask",
    )
    require(selected.get("cover_sha256") == geometry.COVER_SHA, "adaptive cover")
    require(selected.get("seed_sha256") == SEED_SHA, "adaptive seed")
    require(Q(selected["parent_Uplus"]) == geometry.U, "adaptive cap")
    require(Q(selected["parent_side"]) == geometry.B, "adaptive side")
    require(selected.get("branch") is None, "conditional branch in unguarded root")
    rnd = selected["round"]
    require(rnd["index"] == 1, "wrong root round")
    require(sorted(rnd["owner_inventory"]) == list(MASK), "round-one owner inventory")
    prior = rnd["prior_owned_points"]
    require(isinstance(prior, list) and len(prior) == 16, "prior group inventory")
    require(
        all(points(prior[i]) == groups[i] for i in range(16)), "prior differs from checked seed"
    )
    canonical = json.dumps(
        [[[str(x), str(y)] for x, y in points(group)] for group in prior],
        separators=(",", ":"),
        sort_keys=True,
    ).encode()
    require(
        hashlib.sha256(canonical).hexdigest() == rnd["prior_snapshot_sha256"], "prior digest"
    )
    cell = rnd["cell"]
    require(cell["owner"] == OWNER and cell["complete"] is True, "owner update incomplete")
    require(len(cell["rows"]) == 69, "owner row inventory changed")
    require(len(cell["common_core_kernel"]) == 28, "kernel inventory changed")
    return cell


def row_check(
    row: dict[str, Any],
    world: Polygon,
    other_hulls: dict[int, Polygon],
    *,
    budget: geometry.Budget,
) -> tuple[dict[str, int], list[tuple[Point, Q, Q]], Polygon]:
    lo, hi = (Q(value) for value in row["interval"])
    require(
        row.get("domain_restriction") == {"kind": "original_cell"},
        "unexpected prior restriction",
    )
    _, h, cosine, sine = geometry.row_envelope((lo, hi))
    core = Q(row["core_side"])
    require(
        strict_core(core, lo, hi, cosine, sine), "proposed core fails whole-angle strictness"
    )
    require(Q(row["reference_half_angle"]) == (lo + hi) / 2, "reference angle")
    legal = geometry.intersect(
        world,
        [
            (Q(1), Q(0), geometry.L / 2 + h),
            (Q(-1), Q(0), -geometry.L / 2 + h),
            (Q(0), Q(1), geometry.L / 2 + h),
            (Q(0), Q(-1), -geometry.L / 2 + h),
        ],
    )
    require(bool(legal) and geometry.area2(legal) > 0, "degenerate legal domain unsupported")
    require(hull(points(row["input_domain"])) == hull(world), "source input domain differs")
    corners = [
        (core * (a * cosine - b * sine) / 2, core * (a * sine + b * cosine) / 2)
        for a, b in ((-1, -1), (1, -1), (1, 1), (-1, 1))
    ]
    forbidden = [
        hull([(p[0] + q[0], p[1] + q[1]) for p in group for q in corners])
        for group in other_hulls.values()
    ]
    residual = [convex(region) for region in row["residual_polygons"]]
    coverage = geometry.exact_union_cover(legal, forbidden + residual, budget=budget)
    vertices = [point for poly in residual for point in poly]
    strips: list[tuple[Point, Q, Q]] = []
    if vertices:
        for normal in ((cosine, sine), (-sine, cosine)):
            projections = [normal[0] * x + normal[1] * y for x, y in vertices]
            strips.append((normal, max(projections) - core / 2, min(projections) + core / 2))
    proposed = row["common_core_strips"]
    require(len(proposed) == len(strips), "common-core strip count differs")
    for item, (normal, lower, upper) in zip(proposed, strips, strict=True):
        require(
            points([item["normal"]])[0] == normal
            and Q(item["lower"]) == lower
            and Q(item["upper"]) == upper,
            "common-core strip differs",
        )
    return coverage, strips, vertices


def compressed_points(cell: dict[str, Any], prior: Polygon, kernel: Polygon) -> Polygon:
    original = hull(prior + kernel)
    require(hull(points(cell["compression_source_hull"])) == original, "compression hull")
    receipt = cell["inner_grid_compression"]
    result = points(receipt["vertices"])
    denominator = int(receipt["denominator"])
    require(
        denominator > 0 and len(result) == len(receipt["witnesses"]) == 7, "compression census"
    )
    for point, witness in zip(result, receipt["witnesses"], strict=True):
        indices = witness["indices"]
        weights = [Q(value) for value in witness["weights"]]
        require(
            1 <= len(indices) == len(weights) <= 3
            and all(type(index) is int and 0 <= index < len(original) for index in indices)
            and all(weight >= 0 for weight in weights)
            and sum(weights) == 1,
            "invalid convex combination",
        )
        require(
            all((coordinate * denominator).denominator == 1 for coordinate in point)
            and points([witness["point"]])[0] == point
            and point
            == tuple(
                sum(
                    (
                        weight * original[index][axis]
                        for index, weight in zip(indices, weights, strict=True)
                    ),
                    Q(),
                )
                for axis in (0, 1)
            ),
            "compressed point not in accepted hull",
        )
    return result


def run(args: argparse.Namespace) -> dict[str, Any]:
    require(0 < args.max_seconds <= 30, "pilot ceiling must be <=30 seconds")
    started = time.monotonic()
    budget = geometry.Budget(started + args.max_seconds, args.max_events)
    checker_sha = digest(Path(__file__))
    geometry_sha = digest(Path(geometry.__file__))
    result: dict[str, Any] = {
        "status": "INCOMPLETE",
        "scope": args.scope,
        "root_induction_proved": False,
        "candidate_capture_proved": False,
        "global_optimality_proved": False,
        "checker_sha256": checker_sha,
        "shared_geometry_sha256": geometry_sha,
        "max_nodes_per_geometry_call": args.max_events,
    }
    try:
        require(geometry_sha == GEOMETRY_SHA, "shared exact geometry source changed")
        geometry.admit_d4_receipt()
        cover = geometry.pinned_gzip(
            COVER,
            packed_bytes=25016,
            packed_sha=geometry.COVER_LFS_SHA,
            raw_bytes=773471,
            raw_sha=geometry.COVER_SHA,
        )
        require(digest(args.seed) == SEED_SHA, "seed source identity")
        seed = geometry.strict_json(args.seed.read_bytes())
        groups = seed_points(seed, cover, budget=budget)
        result["seed_points_checked"] = 130
        result["seed_sha256"] = SEED_SHA
        result["cover_sha256"] = geometry.COVER_SHA
        if args.scope == "seed":
            remaining(budget)
            require(
                digest(args.seed) == SEED_SHA
                and digest(COVER) == geometry.COVER_LFS_SHA
                and digest(Path(__file__)) == checker_sha
                and digest(Path(geometry.__file__)) == GEOMETRY_SHA,
                "seed or checker source changed",
            )
            remaining(budget)
            result["status"] = "PASS_STRICT_ROOT_SEED"
        else:
            require(digest(args.adaptive) == ADAPTIVE_SHA, "adaptive source identity")
            selected, raw_selected = selected_round(args.adaptive, timeout=remaining(budget))
            require(digest(args.adaptive) == ADAPTIVE_SHA, "adaptive changed during extraction")
            atomic_write_bytes(
                args.out.parent / "selected-round1-owner2.json.gz",
                gzip.compress(raw_selected, mtime=0),
            )
            result["selected_sha256"] = hashlib.sha256(raw_selected).hexdigest()
            result["adaptive_sha256"] = ADAPTIVE_SHA
            cell = admit_prior(selected, groups)
            world = [
                (geometry.B * x, geometry.B * y)
                for x, y in geometry.cell_vertices(cover, OWNER)
            ]
            other_hulls = {owner: hull(groups[owner]) for owner in MASK if owner != OWNER}
            cursor = Q()
            all_strips: list[tuple[Point, Q, Q]] = []
            all_vertices: Polygon = []
            retained: list[list[str]] = []
            rows_to_check = 1 if args.scope == "row" else len(cell["rows"])
            for index, row in enumerate(cell["rows"][:rows_to_check]):
                lo, hi = (Q(value) for value in row["interval"])
                require(lo == cursor and lo < hi <= 1, "angle partition gap or overlap")
                coverage, strips, vertices = row_check(row, world, other_hulls, budget=budget)
                result["rows_checked"] = index + 1
                result["last_row_cover"] = coverage
                if vertices:
                    all_strips.extend(strips)
                    all_vertices.extend(vertices)
                    retained.append([str(lo), str(hi)])
                cursor = hi
            if args.scope == "row":
                remaining(budget)
                require(
                    digest(args.seed) == SEED_SHA
                    and digest(args.adaptive) == ADAPTIVE_SHA
                    and digest(COVER) == geometry.COVER_LFS_SHA
                    and digest(Path(__file__)) == checker_sha
                    and digest(Path(geometry.__file__)) == GEOMETRY_SHA,
                    "row source changed",
                )
                remaining(budget)
                result["status"] = "PASS_ONE_ROW_DIAGNOSTIC"
            else:
                remaining(budget)
                require(cursor == 1 and len(cell["rows"]) == 69, "incomplete angle partition")
                require(retained == cell["retained_angle_intervals"], "retained angles differ")
                kernel = points(cell["common_core_kernel"])
                for point in kernel:
                    require(
                        all(0 <= value <= geometry.L for value in point),
                        "kernel outside container",
                    )
                    require(
                        all(
                            lower <= normal[0] * point[0] + normal[1] * point[1] <= upper
                            for normal, lower, upper in all_strips
                        ),
                        "kernel point outside accepted common core",
                    )
                require(
                    [
                        [
                            str(min(point[axis] for point in all_vertices)),
                            str(max(point[axis] for point in all_vertices)),
                        ]
                        for axis in (0, 1)
                    ]
                    == cell["center_bounds_field"],
                    "center bounds differ",
                )
                new = compressed_points(cell, groups[OWNER], kernel)
                result["compressed_owned_points"] = len(new)
                remaining(budget)
                require(
                    digest(args.seed) == SEED_SHA
                    and digest(args.adaptive) == ADAPTIVE_SHA
                    and digest(COVER) == geometry.COVER_LFS_SHA
                    and digest(Path(__file__)) == checker_sha
                    and digest(Path(geometry.__file__)) == GEOMETRY_SHA,
                    "owner source changed",
                )
                remaining(budget)
                result["status"] = "PASS_CONDITIONAL_OWNER_UPDATE"
    except (geometry.IncompleteError, subprocess.TimeoutExpired) as error:
        result["error"] = str(error)
    except (
        ValueError,
        KeyError,
        IndexError,
        TypeError,
        subprocess.CalledProcessError,
    ) as error:
        result["status"] = "REFUSED"
        result["error"] = str(error)
    result["wall_seconds"] = time.monotonic() - started
    atomic_write_text(args.out, json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=Path, required=True)
    parser.add_argument("--adaptive", type=Path, required=True)
    parser.add_argument("--scope", choices=("seed", "row", "owner"), required=True)
    parser.add_argument("--max-seconds", type=float, default=30)
    parser.add_argument("--max-events", type=int, default=100_000)
    parser.add_argument("--out", type=Path, required=True)
    result = run(parser.parse_args())
    print(
        json.dumps(
            {
                key: result.get(key)
                for key in ("status", "scope", "rows_checked", "wall_seconds", "error")
            }
        )
    )
    return 0 if result["status"].startswith("PASS_") else 2


if __name__ == "__main__":
    sys.exit(main())
