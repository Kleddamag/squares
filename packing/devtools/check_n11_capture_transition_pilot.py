"""Independently replay one root-self capture row's collision and cover geometry.

This is a bounded pilot. A passed row does not promote its step, source node,
candidate capture, or global optimality.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import time
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from strif import atomic_write_text

from devtools import check_n11_capture_root_bridge as bridge
from devtools import check_n11_capture_root_pilot as pilot
from devtools import check_n11_closed_degenerate_cover as degenerate
from devtools import check_n11_optimality_field_mask0 as geometry

BRIDGE_RESULT_SHA = "ba65b7416678f701feee8c027e2b4f9359e9d3324ceee0958fbc8ca30afe309d"
BRIDGE_SHA = "2bbddc8f27575eb6a61e0a4f97e0cb71194357fbd6a341ec1d710a6a2c1ae9a5"
DEGENERATE_SHA = "858c61c3ffa464a12be0fda9a14f802d7d9ea22f9b6aaa2b06c6974f0caa5385"
DEPENDENCY_SHAS = {
    "bridge": BRIDGE_SHA,
    "pilot": bridge.DEPENDENCY_SHAS["pilot"],
    "geometry": bridge.DEPENDENCY_SHAS["geometry"],
    "degenerate": DEGENERATE_SHA,
}
SUPPORT_NORMALS = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1))
Point = pilot.Point
Polygon = pilot.Polygon


def require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def remaining(budget: geometry.Budget) -> None:
    if time.monotonic() >= budget.deadline:
        raise geometry.IncompleteError("capture row wall ceiling")


def dependencies_unchanged() -> bool:
    modules = {
        "bridge": bridge,
        "pilot": pilot,
        "geometry": geometry,
        "degenerate": degenerate,
    }
    return all(
        module.__file__ is not None
        and pilot.digest(Path(module.__file__)) == DEPENDENCY_SHAS[name]
        for name, module in modules.items()
    )


def extract(path: Path, query: str) -> dict[str, Any]:
    raw = subprocess.run(
        ["jq", "-c", query, str(path)], capture_output=True, check=True, timeout=20
    )
    return geometry.strict_json(raw.stdout)


def same(left: Polygon, right: Polygon) -> bool:
    return pilot.hull(left) == pilot.hull(right)


def outward_round(value: Q) -> Q:
    scale = 10**8
    return Q(-((-value.numerator * scale) // value.denominator), scale)


def phase2_outer(row: dict[str, Any], world: Polygon) -> Polygon:
    vertices = [point for region in row["residual_polygons"] for point in pilot.convex(region)]
    if not vertices:
        return []
    lines = [
        (Q(nx), Q(ny), outward_round(max(nx * x + ny * y for x, y in vertices)))
        for nx, ny in SUPPORT_NORMALS
    ]
    return pilot.hull(geometry.intersect(world, lines))


def necessary_self_cuts(
    supplied: list[dict[str, Any]], owned: Polygon, lo: Q, hi: Q
) -> list[tuple[Q, Q, Q]]:
    require(bool(owned), "empty accepted owned hull")
    result: list[tuple[Q, Q, Q]] = []
    for item in supplied:
        nx, ny = pilot.points([item["normal"]])[0]
        upper = Q(item["upper"])
        require((nx, ny) != (0, 0), "zero self-cut normal")
        allowance = upper - min(nx * x + ny * y for x, y in owned)
        for sx in (-1, 1):
            for sy in (-1, 1):
                a = sx * nx + sy * ny
                d = sx * ny - sy * nx
                require(
                    geometry.quadratic_nonnegative(
                        allowance - geometry.B * a / 2,
                        -geometry.B * d,
                        allowance + geometry.B * a / 2,
                        lo,
                        hi,
                    ),
                    "self-cut excludes a possible square center",
                )
        result.append((nx, ny, upper))
    return result


def strict_core(core: Polygon, lo: Q, hi: Q) -> None:
    require(len(core) >= 3 and geometry.area2(core) > 0, "degenerate strict core")
    for x, y in core:
        for sign in (-1, 1):
            require(
                pilot.quadratic_positive(
                    geometry.B / 2 - sign * x,
                    -2 * sign * y,
                    geometry.B / 2 + sign * x,
                    lo,
                    hi,
                )
                and pilot.quadratic_positive(
                    geometry.B / 2 - sign * y,
                    2 * sign * x,
                    geometry.B / 2 + sign * y,
                    lo,
                    hi,
                ),
                "core not strictly inside every full-angle square",
            )


def row_domain(
    row: dict[str, Any], prior: dict[str, Any], owned: Polygon, world: Polygon
) -> tuple[Q, Q, Polygon]:
    lo, hi = (Q(value) for value in row["interval"])
    old_lo, old_hi = (Q(value) for value in prior["interval"])
    require(0 <= old_lo <= lo < hi <= old_hi <= 1, "prior angle interval escaped")
    outer = phase2_outer(prior, world)
    cuts = necessary_self_cuts(row["self_hull_cuts"], owned, lo, hi)
    return lo, hi, pilot.hull(geometry.intersect(outer, cuts)) if outer else []


def partner_cover(
    rows: list[dict[str, Any]],
    prior_rows: list[dict[str, Any]],
    owner: int,
    owned: Polygon,
    world: Polygon,
    *,
    budget: geometry.Budget,
) -> tuple[list[tuple[Polygon, Polygon]], int]:
    require(bool(rows), "missing partner pose cover")
    cursor = Q()
    live: list[tuple[Polygon, Polygon]] = []
    for row in rows:
        remaining(budget)
        reference = row["reference"]
        old_index = reference["row"]
        require(
            reference == {"kind": "phase2", "round": 14, "owner": owner, "row": old_index}
            and type(old_index) is int
            and 0 <= old_index < len(prior_rows),
            "partner predecessor reference differs",
        )
        lo, hi, domain = row_domain(row, prior_rows[old_index], owned, world)
        require(lo == cursor, "partner angle cover gap or overlap")
        cursor = hi
        require(same(pilot.points(row["domain"]), domain), "partner center domain differs")
        if domain:
            core = pilot.convex(row["core"])
            strict_core(core, lo, hi)
            live.append((domain, core))
        else:
            require(row["core"] == [], "empty partner pose has nonempty core")
    require(cursor == 1, "partner angle cover incomplete")
    return live, len(rows)


def facets(poly: Polygon) -> list[tuple[Q, Q, Q]]:
    hull = pilot.hull(poly)
    require(len(hull) >= 3 and geometry.area2(hull) > 0, "degenerate collision hull")
    return [
        (b[1] - a[1], a[0] - b[0], (b[1] - a[1]) * a[0] + (a[0] - b[0]) * a[1])
        for a, b in zip(hull, hull[1:] + hull[:1], strict=True)
    ]


def universal_collision(
    query_core: Polygon,
    query_domain: Polygon,
    partner_rows: list[tuple[Polygon, Polygon]],
    region: Polygon,
    *,
    budget: geometry.Budget,
) -> int:
    """Check a closed inner region of every possible partner-core collision set."""
    require(bool(partner_rows), "empty partner family requires separate contradiction")
    require(all(geometry.area2(core) > 0 for _, core in partner_rows), "partner core")
    require(geometry.area2(query_core) > 0, "query core")
    query_lines = degenerate.convex_halfplanes(query_domain)
    for x, y in region:
        require(
            all(nx * x + ny * y <= upper for nx, ny, upper in query_lines),
            "collision region escapes query domain",
        )
    checks = 0
    for domain, core in partner_rows:
        remaining(budget)
        difference = pilot.hull([(x - qx, y - qy) for x, y in core for qx, qy in query_core])
        for nx, ny, upper in facets(difference):
            bound = upper + min(nx * x + ny * y for x, y in domain)
            for x, y in region:
                checks += 1
                require(nx * x + ny * y <= bound, "region escapes universal collision set")
    return checks


def wall_lines(lo: Q, hi: Q) -> list[tuple[Q, Q, Q]]:
    width = min(sum(geometry.trig(t), Q()) for t in (lo, hi))
    require(
        geometry.quadratic_nonnegative(1 - width, Q(2), -1 - width, lo, hi),
        "whole-angle wall envelope",
    )
    h = geometry.B * width / 2
    return [
        (Q(1), Q(), geometry.L - h),
        (Q(-1), Q(), -h),
        (Q(), Q(1), geometry.L - h),
        (Q(), Q(-1), -h),
    ]


def normalized_line(nx: Q, ny: Q, upper: Q) -> tuple[Q, Q, Q]:
    require((nx, ny) != (0, 0), "zero common-core normal")
    scale = abs(nx) if nx else abs(ny)
    return nx / scale, ny / scale, upper / scale


def verify_row_output(
    row: dict[str, Any], core: Polygon, residual: list[Polygon], world: Polygon
) -> int:
    vertices = [point for polygon in residual for point in polygon]
    planes = row["common_core_halfplanes"]
    bounds = row["outer_bounds"]
    if not vertices:
        require(
            planes == [] and bounds == [] and row["outer_domain"] == [],
            "empty residual retained output",
        )
        return 0
    expected = {
        normalized_line(nx, ny, upper + min(nx * x + ny * y for x, y in vertices))
        for nx, ny, upper in facets(core)
    }
    actual = {
        normalized_line(Q(item["normal"][0]), Q(item["normal"][1]), Q(item["upper"]))
        for item in planes
    }
    require(len(planes) == len(expected) and actual == expected, "common-core output planes")
    require(len(bounds) == len(SUPPORT_NORMALS), "outer-support inventory")
    lines = []
    for item, (nx, ny) in zip(bounds, SUPPORT_NORMALS, strict=True):
        require(tuple(item["normal"]) == (nx, ny), "outer-support normal differs")
        upper = Q(item["upper"])
        require(
            all(nx * x + ny * y <= upper for x, y in vertices), "outer support cuts residual"
        )
        lines.append((Q(nx), Q(ny), upper))
    outer = geometry.intersect(world, lines)
    require(same(pilot.points(row["outer_domain"]), outer), "row outer domain differs")
    return len(planes)


def check_first_row(
    root: dict[str, Any],
    adaptive: dict[str, Any],
    cover: dict[str, Any],
    *,
    scope: str,
    budget: geometry.Budget,
) -> dict[str, Any]:
    step = root["step"]
    row = step["row"]
    require(step["index"] == 0 and step["owner"] == 15, "first capture step changed")
    require(
        row["reference"] == {"kind": "phase3", "node": "root-self-240", "step": 0, "row": 0},
        "row identity",
    )
    cells = {cell["owner"]: cell["rows"] for cell in adaptive["cells"]}
    require(set(cells) == {10, 15}, "selected phase-two cell inventory")
    groups = {
        int(key): pilot.hull(pilot.points(value))
        for key, value in root["initial"]["groups"].items()
    }
    require(set(groups) == set(pilot.MASK), "initial owner inventory")
    worlds = {
        owner: [
            (geometry.B * x, geometry.B * y) for x, y in geometry.cell_vertices(cover, owner)
        ]
        for owner in (10, 15)
    }
    row_index = row["prior_reference"]["row"]
    require(
        row["prior_reference"]
        == {"kind": "phase2", "round": 14, "owner": 15, "row": row_index},
        "query predecessor reference",
    )
    require(
        type(row_index) is int and 0 <= row_index < len(cells[15]), "query predecessor index"
    )
    lo, hi, domain = row_domain(row, cells[15][row_index], groups[15], worlds[15])
    require((lo, hi) == (Q(), Q(1, 7936)), "first row interval changed")
    require(same(pilot.points(row["input_domain"]), domain), "query center domain differs")
    core = pilot.convex(row["core_vertices"])
    strict_core(core, lo, hi)
    partner = partner_cover(
        step["partner10"], cells[10], 10, groups[10], worlds[10], budget=budget
    )
    live, cover_count = partner
    regions = row["collision_regions"]
    require(len(regions) == 1 and regions[0]["partner"] == 10, "first row collision inventory")
    region = pilot.convex(regions[0]["vertices"])
    facet_checks = universal_collision(core, domain, live, region, budget=budget)
    result: dict[str, Any] = {
        "partner_cover_rows": cover_count,
        "live_partner_rows": len(live),
        "collision_vertices": len(region),
        "universal_facet_vertex_checks": facet_checks,
        "first_row_collision_checked": True,
        "first_row_full_geometry_checked": False,
    }
    if scope == "collision":
        return result
    legal = geometry.intersect(domain, wall_lines(lo, hi))
    forbidden = [
        pilot.hull([(x - qx, y - qy) for x, y in group for qx, qy in core])
        for owner, group in groups.items()
        if owner != 15
    ]
    residual = [pilot.convex(polygon) for polygon in row["residual_polygons"]]
    if legal:
        cover_result = (
            geometry.exact_union_cover(legal, [*forbidden, region, *residual], budget=budget)
            if geometry.area2(legal) > 0
            else degenerate.exact_cover_closed_degenerate(
                legal, [*forbidden, region, *residual], budget=budget
            )
        )
    else:
        require(not residual, "empty legal row has residual")
        cover_result = {"events": 0, "probes": 0}
    planes = verify_row_output(row, core, residual, worlds[15])
    result.update(
        first_row_full_geometry_checked=True,
        coverage_events=cover_result["events"],
        coverage_probes=cover_result["probes"],
        common_core_planes_checked=planes,
    )
    return result


def run(args: argparse.Namespace) -> dict[str, Any]:
    began = time.monotonic()
    budget = geometry.Budget(began + args.max_seconds, args.max_events)
    result: dict[str, Any] = {
        "status": "REFUSED",
        "first_row_collision_checked": False,
        "first_row_full_geometry_checked": False,
        "capture_step_proved": False,
        "candidate_capture_proved": False,
        "global_optimality_proved": False,
        "checker_sha256": pilot.digest(Path(__file__)),
        "root_source_sha256": bridge.ROOT_SOURCE_SHA,
        "adaptive_sha256": pilot.ADAPTIVE_SHA,
        "bridge_result_sha256": BRIDGE_RESULT_SHA,
        "dependency_sha256s": DEPENDENCY_SHAS,
        "scope_requested": args.scope,
        "max_seconds": args.max_seconds,
        "max_events_per_cover": args.max_events,
    }
    try:
        require(args.max_seconds > 0 and args.max_events > 0, "positive budgets required")
        require(dependencies_unchanged(), "imported proof dependency changed")
        require(pilot.digest(args.bridge_result) == BRIDGE_RESULT_SHA, "bridge result changed")
        admitted = geometry.strict_json(args.bridge_result.read_bytes())
        require(
            admitted["capture_root_initial_bridge_checked"] is True, "root bridge not admitted"
        )
        require(pilot.digest(args.root_source) == bridge.ROOT_SOURCE_SHA, "root source changed")
        require(pilot.digest(args.adaptive) == pilot.ADAPTIVE_SHA, "adaptive source changed")
        geometry.admit_d4_receipt()
        cover = geometry.pinned_gzip(
            pilot.COVER,
            packed_bytes=25016,
            packed_sha=geometry.COVER_LFS_SHA,
            raw_bytes=773471,
            raw_sha=geometry.COVER_SHA,
        )
        remaining(budget)
        root = extract(
            args.root_source,
            '{initial,step:(.steps[0]|{index,owner,row:.rows[0],partner10:.prior_partner_pose_covers["10"]})}',
        )
        adaptive = extract(
            args.adaptive,
            "{cells:[.rounds[13].cells[]|select(.owner==10 or .owner==15)|{owner,rows}]}",
        )
        remaining(budget)
        result.update(check_first_row(root, adaptive, cover, scope=args.scope, budget=budget))
        require(
            pilot.digest(args.root_source) == bridge.ROOT_SOURCE_SHA
            and pilot.digest(args.adaptive) == pilot.ADAPTIVE_SHA
            and pilot.digest(args.bridge_result) == BRIDGE_RESULT_SHA
            and pilot.digest(Path(__file__)) == result["checker_sha256"]
            and dependencies_unchanged(),
            "input or checker changed during replay",
        )
        remaining(budget)
        result["status"] = (
            "PASS_FIRST_CAPTURE_ROW_GEOMETRY"
            if args.scope == "row"
            else "PASS_FIRST_CAPTURE_ROW_COLLISION"
        )
    except geometry.IncompleteError as error:
        result.update(status="INCOMPLETE", error=str(error))
    except (
        ValueError,
        KeyError,
        IndexError,
        TypeError,
        OSError,
        subprocess.CalledProcessError,
        subprocess.TimeoutExpired,
    ) as error:
        result["error"] = str(error)
    result["wall_seconds"] = time.monotonic() - began
    atomic_write_text(args.out, json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root-source", type=Path, required=True)
    parser.add_argument("--adaptive", type=Path, required=True)
    parser.add_argument("--bridge-result", type=Path, required=True)
    parser.add_argument("--scope", choices=("collision", "row"), default="collision")
    parser.add_argument("--max-seconds", type=float, default=25)
    parser.add_argument("--max-events", type=int, default=20000)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = run(args)
    print(
        json.dumps(
            {
                key: result.get(key)
                for key in (
                    "status",
                    "first_row_collision_checked",
                    "first_row_full_geometry_checked",
                    "partner_cover_rows",
                    "live_partner_rows",
                    "universal_facet_vertex_checks",
                    "wall_seconds",
                    "error",
                )
            }
        )
    )
    return 0 if result["status"].startswith("PASS_") else 2


if __name__ == "__main__":
    raise SystemExit(main())
