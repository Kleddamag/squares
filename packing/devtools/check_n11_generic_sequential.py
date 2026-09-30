"""Replay one pinned fresh-wall generic case with exact sequential geometry.

The manifest selects bytes and proposes ancestry. Only a complete independent
seed, every row of every accepted step, and a checked terminal contradiction
can exclude a canonical case. Unsupported ancestry or geometry is refused.
"""

# The frozen pilot intentionally exports no public geometry API yet.
# pyright: reportPrivateUsage=false
# ruff: noqa: SLF001

from __future__ import annotations

import argparse
import concurrent.futures
import gzip
import hashlib
import json
import multiprocessing
import resource
import sys
import time
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, cast

from strif import atomic_write_text

from devtools import check_n11_baseline_d4_cuts as d4_cuts
from devtools import check_n11_capture_transition_pilot as collision_kernel
from devtools import check_n11_closed_degenerate_cover as degenerate_cover
from devtools import check_n11_generic_fresh as frozen
from devtools import check_n11_optimality_field_mask0 as geometry
from devtools import n11_fast_exact_cover as fast_cover
from devtools import n11_integer_collision as integer_collision
from devtools import n11_nonfield_ancestry as ancestry
from devtools import n11_nonfield_assignment as a2_assignment
from devtools import n11_nonfield_d4_admission as d4_admission
from devtools import n11_nonfield_partner as partner
from devtools import n11_nonfield_refinement as refinement
from devtools import n11_nonfield_special_assignment as special_assignment

PACKET = geometry.PACKET
MANIFEST = PACKET / "receipts/nonfield-manifest/manifest.json.gz"
MANIFEST_GZIP_SHA = "a730804aef482e9f32d4b579608a52727b55fa2df8fa4327dfbeae82c0184520"
MANIFEST_SHA = "b2b80cb792e12a41860b4f82b51f93ca08e2e89b3c3718b632e982a2a8fb588b"
FROZEN_GENERIC_SHA = "e8fcfd02560d09e7a2a5b2622976ab021ef15a4456a2824b37abae926f6ab7d3"
FAST_COVER_SHA = "eb21b1acda671b9f858039d077b0c8a30d035ee5920e083887952bf44b156904"
DEGENERATE_COVER_SHA = "858c61c3ffa464a12be0fda9a14f802d7d9ea22f9b6aaa2b06c6974f0caa5385"
A2_HELPER_SHA = "f8135ba45073ad4bda7f66f543454b7484f46cc3fbcee63340afee1dbeac7265"
PARTNER_HELPER_SHA = "1722c6e3e93b53885342516f42a2e094991c34fa938f1befef3b947ff8daa0fa"
COLLISION_KERNEL_SHA = "22c5b4d1f23d48bcc4333bd279df41ba022c337109d063073771349b2854b309"
INTEGER_COLLISION_SHA = "4a1f71cdc96134af1083c84717912b73801b07933a8f7cd2eff8b998b31eab98"
ANCESTRY_HELPER_SHA = "f1d113d9d5c382933f3939d7481ecec6e486cc04890f417f7025af8e54264264"
REFINEMENT_HELPER_SHA = "937d36d64bf385d94d8dad9e6de5c1f8c487f07955cdbc826987dd63dea3464c"
D4_CHECKER_SHA = "338fb431d381502fa1a9721647f231f1a3e9db73a3c6337c3561e69d16bf5d32"
D4_ADMISSION_SHA = "621106a4855da5ca4bbc75985890561e80656cc7fb85dbcea95cf792b965ce28"
SPECIAL_ASSIGNMENT_SHA = "a01986779d54a80804b4ed9572c5448aa90e287c1dadae9b6b3f5377233aa4f7"
OBJECTS = PACKET / "receipts/nonfield-sources/objects"
METADATA_OBJECTS = PACKET / "receipts/case-census/objects"
Point = frozen.Point
Polygon = frozen.Polygon
Plane = tuple[Q, Q, Q]


def require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def remaining(budget: geometry.Budget) -> None:
    if time.monotonic() >= budget.deadline:
        raise geometry.IncompleteError("generic sequential wall ceiling expired")


def load_manifest(path: Path) -> dict[str, Any]:
    require(path.is_file() and path.stat().st_size == 186_249, "manifest compressed size")
    packed = path.read_bytes()
    require(hashlib.sha256(packed).hexdigest() == MANIFEST_GZIP_SHA, "manifest compressed SHA")
    raw = gzip.decompress(packed)
    require(
        len(raw) == 1_103_017 and hashlib.sha256(raw).hexdigest() == MANIFEST_SHA,
        "manifest decoded identity",
    )
    manifest = geometry.strict_json(raw)
    require(
        manifest["source_revision"] == geometry.SOURCE_REVISION
        and manifest["geometry_verified"] is False
        and manifest["actual_parent_edges_verified"] is False,
        "manifest scope or source changed",
    )
    return manifest


def load_object(sha: str, manifest: dict[str, Any], directory: Path) -> dict[str, Any]:
    pin = manifest["objects"][sha]
    require(pin["decoded_sha256"] == sha, "object manifest identity")
    return geometry.pinned_gzip(
        directory / f"{sha}.gz",
        packed_bytes=pin["compressed_bytes"],
        packed_sha=pin["compressed_sha256"],
        raw_bytes=pin["decoded_bytes"],
        raw_sha=sha,
    )


def admit_assignment(case_id: int, recipe: dict[str, Any], manifest: dict[str, Any]) -> None:
    family = recipe["family"]
    require(family in ("A1", "A2", "A3"), "unsupported assignment family")
    metadata_sha = manifest["input_sha256s"][family]
    metadata = load_object(metadata_sha, manifest, METADATA_OBJECTS)
    if family == "A1":
        matches = [cert for cert in metadata["certificates"] if case_id in cert["cases"]]
        require(
            len(matches) == 1
            and matches[0]["family"] == "generic"
            and matches[0]["source_sha256"] == recipe["source_sha256"]
            and matches[0]["fresh_audit_sha256"] == recipe["audit_sha256"]
            and matches[0]["cases"] == [case_id],
            "A1 generic assignment differs from pinned source",
        )
    elif family == "A3":
        matches = [row for row in metadata["cases"] if row["mask_index"] == case_id]
        require(
            len(matches) == 1
            and matches[0]["source_sha256"] == recipe["source_sha256"]
            and matches[0]["saved_audit_sha256"] == recipe["audit_sha256"]
            and matches[0]["root_sha256"] == recipe["seed_sha256"]
            and matches[0]["job_id"] == recipe["job_id"],
            "A3 case/job assignment differs from pinned source",
        )
    else:
        baseline_sha = manifest["input_sha256s"]["A1"]
        baseline = load_object(baseline_sha, manifest, METADATA_OBJECTS)
        a2_assignment.admit_a2_extension(
            case_id,
            recipe,
            baseline,
            metadata,
            baseline_object_sha256=baseline_sha,
        )


def seed_state(
    seed: dict[str, Any],
    cover: dict[str, Any],
    case_id: int,
    mask: tuple[int, ...],
    *,
    budget: geometry.Budget,
) -> tuple[dict[int, Polygon], dict[int, list[dict[str, Any]]], list[Polygon], int]:
    require(seed.get("schema") == "generic_wall_seed_v1", "seed schema")
    require(type(seed.get("mask_index")) is int and seed["mask_index"] == case_id, "seed case")
    require(seed["mask"] == list(mask), "seed mask")
    require(Q(seed["U"]) == geometry.U and Q(seed["B"]) == geometry.B, "seed U/B")
    require(seed["cover_source"]["sha256"] == geometry.COVER_SHA, "seed cover")
    bins = seed["bins"]
    require(type(bins) is int and 1 <= bins <= 128, "unsupported seed bin count")
    require(set(seed["groups"]) == set(map(str, mask)), "seed owner inventory")
    require(set(seed["cells"]) == set(map(str, mask)), "seed cell inventory")
    world = [
        [(geometry.B * x, geometry.B * y) for x, y in geometry.cell_vertices(cover, owner)]
        for owner in range(16)
    ]
    require(
        len(seed["world"]) == 16
        and all(
            frozen._same(frozen.points(proposal), actual)
            for proposal, actual in zip(seed["world"], world, strict=True)
        ),
        "seed world differs from D4 cover",
    )
    groups: dict[int, Polygon] = {}
    rows: dict[int, list[dict[str, Any]]] = {}
    for owner in mask:
        group = frozen.points(seed["groups"][str(owner)])
        require(group and len(set(group)) == len(group), "seed point inventory")
        for point in group:
            remaining(budget)
            geometry.ownership(geometry.cell_vertices(cover, owner), point, budget=budget)
        groups[owner] = frozen.hull(group)
        owner_rows = seed["cells"][str(owner)]
        require(len(owner_rows) == bins, "seed angular row inventory")
        accepted: list[dict[str, Any]] = []
        for index, row in enumerate(owner_rows):
            remaining(budget)
            lo, hi = (Q(value) for value in row["interval"])
            require((lo, hi) == (Q(index, bins), Q(index + 1, bins)), "seed row gap/overlap")
            domain = geometry.intersect(world[owner], frozen._wall_lines(lo, hi))
            require(
                frozen._same(frozen.points(row["outer_domain"]), domain), "seed wall domain"
            )
            require(row["outer_bounds"] == [], "unsupported seed support restriction")
            given = [frozen.points(poly) for poly in row["residual_polygons"]]
            require(
                len(given) == int(bool(domain))
                and (not given or frozen._same(given[0], domain)),
                "seed residual differs from full legal wall domain",
            )
            reference = {"kind": "wall_seed", "owner": owner, "row": index}
            require(row["reference"] == reference, "seed row reference")
            accepted.append(
                {
                    "interval": [str(lo), str(hi)],
                    "reference": reference,
                    "outer_domain": frozen._encoded(domain),
                    "residual_polygons": [frozen._encoded(domain)] if domain else [],
                }
            )
        rows[owner] = accepted
    return groups, rows, world, bins


def necessary_self_cuts(
    row: dict[str, Any], group: Polygon, lo: Q, hi: Q
) -> list[tuple[Q, Q, Q]]:
    cuts: list[tuple[Q, Q, Q]] = []
    for item in row.get("self_hull_cuts", []):
        nx, ny = (Q(value) for value in item["normal"])
        upper = Q(item["upper"])
        require((nx, ny) != (0, 0), "zero self-cut normal")
        margin = upper - min(nx * x + ny * y for x, y in group)
        for sx in (-1, 1):
            for sy in (-1, 1):
                a = sx * nx + sy * ny
                d = sx * ny - sy * nx
                require(
                    geometry.quadratic_nonnegative(
                        margin - geometry.B * a / 2,
                        -geometry.B * d,
                        margin + geometry.B * a / 2,
                        lo,
                        hi,
                    ),
                    "self-hull cut is not necessary for every full square in row",
                )
        cuts.append((nx, ny, upper))
    return cuts


def covering_input_domain(required: Polygon, proposal: Any) -> Polygon:
    """Bind a pre-wall source hint, then return the proved legal-center domain."""
    require(bool(required), "empty legal domain needs a separate row proof")
    domain = frozen.convex(proposal)
    require(
        frozen.hull(required + domain) == domain,
        "row input domain excludes a required legal pose",
    )
    return required


def check_row(
    source: dict[str, Any],
    step: dict[str, Any],
    row_index: int,
    *,
    prior: dict[int, Polygon],
    predecessor: dict[str, Any],
    world: list[Polygon],
    budget: geometry.Budget,
    cover_backend: str = "reference",
    collision_backend: str = "reference",
    partner_live: dict[int, list[tuple[Polygon, Polygon]]] | None = None,
    center_planes: dict[int, list[Plane]] | None = None,
) -> tuple[dict[str, int], Polygon, list[tuple[Q, Q, Q]], dict[str, Any]]:
    row = step["rows"][row_index]
    owner = step["owner"]
    require(row["prior_reference"] == predecessor["reference"], "row predecessor reference")
    lo, hi = (Q(value) for value in row["interval"])
    old_lo, old_hi = (Q(value) for value in predecessor["interval"])
    require(old_lo <= lo < hi <= old_hi, "row interval escaped predecessor")
    cuts = necessary_self_cuts(row, prior[owner], lo, hi)
    cuts.extend((center_planes or {}).get(owner, []))
    required_domain = geometry.intersect(
        frozen.hull(frozen.points(predecessor["outer_domain"])),
        frozen._wall_lines(lo, hi) + cuts,
    )
    reference = {
        "kind": "phase3",
        "node": source["node_id"],
        "step": step["index"],
        "row": row_index,
    }
    require(row["reference"] == reference, "row reference")
    if not required_domain:
        require(
            row["input_domain"] == []
            and row["core_vertices"] == []
            and row["residual_polygons"] == []
            and row["collision_regions"] == []
            and row["common_core_halfplanes"] == []
            and row["outer_bounds"] == []
            and row["outer_domain"] == [],
            "empty legal row has an unsupported output",
        )
        remaining(budget)
        return (
            {"events": 0, "probes": 0, "edge_segments": 0, "collision_facet_checks": 0},
            [],
            [],
            {
                "interval": [str(lo), str(hi)],
                "reference": reference,
                "outer_domain": [],
                "residual_polygons": [],
            },
        )
    domain = covering_input_domain(required_domain, row["input_domain"])
    core = frozen.convex(row["core_vertices"])
    frozen._strict_core(core, lo, hi)
    collision_regions: list[Polygon] = []
    collision_checks = 0
    if row["collision_regions"]:
        pre_wall_domain = geometry.intersect(
            frozen.hull(frozen.points(predecessor["outer_domain"])), cuts
        )
        collision_regions, collision_checks = partner.admitted_collision_regions(
            row["collision_regions"],
            query_core=core,
            query_pre_wall_domain=pre_wall_domain,
            partners=partner_live or {},
            budget=budget,
            backend=collision_backend,
        )
    forbidden = [
        frozen.hull([(p[0] - q[0], p[1] - q[1]) for p in group for q in core])
        for other, group in prior.items()
        if other != owner
    ]
    residual = [frozen.convex(poly) for poly in row["residual_polygons"]]
    cover = (
        fast_cover.exact_union_cover if cover_backend == "fast" else geometry.exact_union_cover
    )
    coverage = (
        cover(domain, forbidden + residual + collision_regions, budget=budget)
        if geometry.area2(domain) > 0
        else degenerate_cover.exact_cover_closed_degenerate(
            domain, forbidden + residual + collision_regions, budget=budget
        )
    )
    coverage["collision_facet_checks"] = collision_checks
    vertices = [point for poly in residual for point in poly]
    expected: list[tuple[Q, Q, Q]] = []
    if vertices:
        for p, q in zip(core, core[1:] + core[:1], strict=True):
            nx, ny = q[1] - p[1], p[0] - q[0]
            expected.append(
                (nx, ny, nx * p[0] + ny * p[1] + min(nx * x + ny * y for x, y in vertices))
            )
    actual = [
        (Q(item["normal"][0]), Q(item["normal"][1]), Q(item["upper"]))
        for item in row["common_core_halfplanes"]
    ]
    require(set(actual) == set(expected), "common owned-core facets")
    support = [
        (Q(item["normal"][0]), Q(item["normal"][1]), Q(item["upper"]))
        for item in row["outer_bounds"]
    ]
    require(
        all(nx * x + ny * y <= upper for x, y in vertices for nx, ny, upper in support),
        "support bound excludes residual vertex",
    )
    if vertices:
        trusted_outer = frozen.hull(geometry.intersect(world[owner], support))
        require(frozen._same(trusted_outer, frozen.points(row["outer_domain"])), "row outer")
    else:
        require(not support and not row["outer_domain"], "empty residual has support")
        trusted_outer = []
    remaining(budget)
    accepted = {
        "interval": [str(lo), str(hi)],
        "reference": reference,
        "outer_domain": frozen._encoded(trusted_outer),
        "residual_polygons": [frozen._encoded(poly) for poly in residual],
    }
    return coverage, vertices, actual, accepted


class _WorkerState:
    source: dict[str, Any] | None = None
    world: list[Polygon] | None = None
    cover_backend: str = "reference"
    collision_backend: str = "reference"
    partner_live: dict[int, list[tuple[Polygon, Polygon]]] | None = None
    center_planes: dict[int, list[Plane]] | None = None


def capability_preflight(
    source: dict[str, Any],
    mask: tuple[int, ...],
    max_rows: int,
    parent_sha: str | None = None,
    *,
    admitted_constraints: bool = False,
) -> None:
    """Reject known unsupported source grammar before expensive seed ownership."""
    require(
        source["schema"] == "exact_generic_owned_hull_v1"
        and (
            source["parent"] is None
            if parent_sha is None
            else isinstance(source["parent"], dict)
            and source["parent"].get("sha256") == parent_sha
        )
        and (admitted_constraints or source["constraints"] == [])
        and source["guard_source"] is None,
        "unsupported parent/guard grammar",
    )
    require(type(max_rows) is int and max_rows > 0, "row ceiling")
    require(source["steps"], "empty source step inventory")
    for index, step in enumerate(source["steps"]):
        require(
            type(step["index"]) is int and step["index"] == index and step["owner"] in mask,
            "step owner/order",
        )
        require(step["allowed_half_angle"] == ["0", "1"], "unsupported angle scope")
        require(isinstance(step["prior_partner_pose_covers"], dict), "partner cover map")
        require(
            isinstance(step["rows"], list)
            and len(step["rows"]) <= max_rows
            and (step["complete"] is False or bool(step["rows"])),
            "step angular inventory",
        )
        require(
            all(isinstance(row["collision_regions"], list) for row in step["rows"]),
            "collision-region inventory",
        )


def _worker_init(
    source: dict[str, Any],
    world: list[Polygon],
    backends: tuple[str, str],
    partner_live: dict[int, list[tuple[Polygon, Polygon]]],
    center_planes: dict[int, list[Plane]],
) -> None:
    _WorkerState.source, _WorkerState.world = source, world
    _WorkerState.cover_backend, _WorkerState.collision_backend = backends
    _WorkerState.partner_live = partner_live
    _WorkerState.center_planes = center_planes


def _worker_row(
    step_index: int,
    row_index: int,
    prior: dict[int, Polygon],
    predecessor: dict[str, Any],
    budget: geometry.Budget,
) -> tuple[int, dict[str, int], Polygon, list[tuple[Q, Q, Q]], dict[str, Any], float, float]:
    source, world = _WorkerState.source, _WorkerState.world
    if source is None or world is None:
        raise ValueError("worker source unavailable")
    started, cpu_started = time.monotonic(), time.process_time()
    coverage, vertices, planes, accepted = check_row(
        source,
        source["steps"][step_index],
        row_index,
        prior=prior,
        predecessor=predecessor,
        world=world,
        budget=budget,
        cover_backend=_WorkerState.cover_backend,
        collision_backend=_WorkerState.collision_backend,
        partner_live=_WorkerState.partner_live,
        center_planes=_WorkerState.center_planes,
    )
    return (
        row_index,
        coverage,
        vertices,
        planes,
        accepted,
        time.monotonic() - started,
        time.process_time() - cpu_started,
    )


def admit_terminal_contradiction(
    source: dict[str, Any], state_rows: dict[int, list[dict[str, Any]]]
) -> None:
    """The accepted empty pose cover proves closure regardless of producer flag."""
    contradiction = source["contradiction"]
    require(
        isinstance(contradiction, dict)
        and contradiction["kind"] == "all_parent_poses_forbidden"
        and contradiction["step"] == len(source["steps"]) - 1
        and contradiction["owner"] == source["steps"][-1]["owner"]
        and all(not row["residual_polygons"] for row in state_rows[contradiction["owner"]]),
        "terminal contradiction not independently shown",
    )
    require(
        type(source["terminal"]) is bool and source["closed"] is True,
        "source nonterminal",
    )


def replay_one_node(
    source: dict[str, Any],
    groups: dict[int, Polygon],
    rows: dict[int, list[dict[str, Any]]],
    *,
    world: list[Polygon],
    mask: tuple[int, ...],
    result: dict[str, Any],
    budget: geometry.Budget,
    workers: int,
    cover_backend: str = "reference",
    collision_backend: str = "reference",
    parent_sha: str | None = None,
    final_node: bool = True,
    center_planes: dict[int, list[Plane]] | None = None,
) -> tuple[dict[int, Polygon], dict[int, list[dict[str, Any]]]]:
    require(source["schema"] == "exact_generic_owned_hull_v1", "source schema")
    require(
        (
            source["parent"] is None
            if parent_sha is None
            else isinstance(source["parent"], dict)
            and source["parent"].get("sha256") == parent_sha
        )
        and (center_planes is not None or source["constraints"] == [])
        and source["guard_source"] is None,
        "unsupported parent/guard",
    )
    require(set(source["initial"]["groups"]) == set(map(str, mask)), "source initial groups")
    require(
        set(source["initial"]["cell_references"]) == set(map(str, mask)), "source initial rows"
    )
    for owner in mask:
        require(
            frozen._same(frozen.points(source["initial"]["groups"][str(owner)]), groups[owner])
            and source["initial"]["cell_references"][str(owner)]
            == [row["reference"] for row in rows[owner]],
            "source initial state differs from proved seed",
        )
    state_groups, state_rows = dict(groups), dict(rows)
    result.setdefault("steps_completed", 0)
    result.setdefault("rows_checked", 0)
    result.setdefault("step_timings", [])
    for step_index, step in enumerate(source["steps"]):
        step_started = time.monotonic()
        result["current_step"] = step_index
        owner = step["owner"]
        require(
            type(step["index"]) is int and step["index"] == step_index and owner in mask,
            "step owner/order",
        )
        require(
            step["allowed_half_angle"] == ["0", "1"]
            and set(step["prior_owned_hulls"]) == set(map(str, mask))
            and all(
                frozen._same(frozen.points(step["prior_owned_hulls"][str(i)]), state_groups[i])
                for i in mask
            ),
            "step previous accepted state",
        )
        require(type(step["complete"]) is bool, "step completeness flag")
        if not step["complete"]:
            require(
                step_index == len(source["steps"]) - 1 and not final_node,
                "incomplete step cannot promote or close a case",
            )
            result["skipped_incomplete_source_rows"] = result.get(
                "skipped_incomplete_source_rows", 0
            ) + len(step["rows"])
            break
        predecessors = refinement.complete_refinement(
            step["rows"], state_rows[owner], max_rows=budget.max_nodes
        )
        row_count = len(predecessors)
        if step["prior_partner_pose_covers"]:
            partner_live, partner_counts = partner.admitted_partner_covers(
                step["prior_partner_pose_covers"],
                query_owner=owner,
                mask=mask,
                accepted_groups=state_groups,
                accepted_rows=state_rows,
                budget=budget,
                center_planes=center_planes,
            )
        else:
            partner_live = {}
            partner_counts = {"rows": 0, "empty_rows": 0, "live_rows": 0}
        result["pending_row_indices"] = list(range(row_count))
        result["checked_row_indices_current_step"] = []
        if workers == 1:
            completed = []
            for row_index in range(row_count):
                remaining(budget)
                result["current_row"] = row_index
                started, cpu_started = time.monotonic(), time.process_time()
                values = check_row(
                    source,
                    step,
                    row_index,
                    prior=state_groups,
                    predecessor=predecessors[row_index],
                    world=world,
                    budget=budget,
                    cover_backend=cover_backend,
                    collision_backend=collision_backend,
                    partner_live=partner_live,
                    center_planes=center_planes,
                )
                completed.append(
                    (
                        row_index,
                        *values,
                        time.monotonic() - started,
                        time.process_time() - cpu_started,
                    )
                )
                result["checked_row_indices_current_step"].append(row_index)
                result["pending_row_indices"].remove(row_index)
        else:
            with concurrent.futures.ProcessPoolExecutor(
                max_workers=workers,
                mp_context=multiprocessing.get_context("spawn"),
                initializer=_worker_init,
                initargs=(
                    source,
                    world,
                    (cover_backend, collision_backend),
                    partner_live,
                    center_planes or {},
                ),
            ) as pool:
                futures = {
                    pool.submit(
                        _worker_row,
                        step_index,
                        row_index,
                        state_groups,
                        predecessors[row_index],
                        budget,
                    ): row_index
                    for row_index in range(row_count)
                }
                completed = []
                for future in concurrent.futures.as_completed(
                    futures, timeout=max(0, budget.deadline - time.monotonic())
                ):
                    checked = future.result()
                    row_index = checked[0]
                    completed.append(checked)
                    result["checked_row_indices_current_step"].append(row_index)
                    result["pending_row_indices"].remove(row_index)
        require(len(completed) == row_count, "incomplete step join")
        accepted_rows: list[dict[str, Any]] = []
        all_vertices: Polygon = []
        all_planes: list[tuple[Q, Q, Q]] = []
        row_timings = []
        for row_index, coverage, vertices, planes, accepted, wall, cpu in sorted(completed):
            accepted_rows.append(accepted)
            all_vertices.extend(vertices)
            all_planes.extend(planes)
            row_timings.append(
                {
                    "row": row_index,
                    "events": coverage["events"],
                    "probes": coverage["probes"],
                    "wall_seconds": wall,
                    "process_cpu_seconds": cpu,
                    "collision_facet_checks": coverage["collision_facet_checks"],
                }
            )
            result["rows_checked"] += 1
        kernel = frozen.points(step["common_owned_kernel"])
        for point in kernel:
            require(
                all(0 <= coordinate <= geometry.L for coordinate in point)
                and all(nx * point[0] + ny * point[1] <= upper for nx, ny, upper in all_planes),
                "promoted point lacks full-row ownership proof",
            )
        if all_vertices:
            state_groups[owner] = frozen._compressed(step, state_groups[owner], kernel)
        else:
            require("inner_grid_compression" not in step, "empty terminal has compression")
        state_rows[owner] = accepted_rows
        result["steps_completed"] += 1
        result["step_timings"].append(
            {
                "step": step_index,
                "node": result["current_node"],
                "owner": owner,
                "rows": row_count,
                "row_timings": row_timings,
                "wall_seconds": time.monotonic() - step_started,
                "row_process_cpu_seconds": sum(
                    item["process_cpu_seconds"] for item in row_timings
                ),
                "partner_cover": partner_counts,
            }
        )
        result["current_row"] = None
        result["checked_row_indices_current_step"] = []
        result["pending_row_indices"] = []
    final = source["final_state"]
    require(
        final["mask_index"] == source["mask_index"]
        and final["mask"] == source["mask"]
        and Q(final["U"]) == geometry.U
        and Q(final["B"]) == geometry.B
        and final["constraints"] == source["constraints"]
        and final["guard"] == {}
        and final["guard_source"] is None
        and final["source"] == source["source"],
        "final state premise",
    )
    require(
        len(final["world"]) == 16
        and all(
            frozen._same(frozen.points(given), accepted)
            for given, accepted in zip(final["world"], world, strict=True)
        ),
        "final world differs from D4",
    )
    require(
        set(final["groups"]) == set(map(str, mask))
        and set(final["cells"]) == set(map(str, mask)),
        "final owner inventory",
    )
    for owner in mask:
        require(
            frozen._same(frozen.points(final["groups"][str(owner)]), state_groups[owner]),
            "final group differs from accepted state",
        )
        given_rows = final["cells"][str(owner)]
        require(len(given_rows) == len(state_rows[owner]), "final angular inventory")
        for given, accepted in zip(given_rows, state_rows[owner], strict=True):
            require(
                given["reference"] == accepted["reference"]
                and [Q(value) for value in given["interval"]]
                == [Q(value) for value in accepted["interval"]]
                and frozen._same(
                    frozen.points(given["outer_domain"]),
                    frozen.points(accepted["outer_domain"]),
                )
                and len(given["residual_polygons"]) == len(accepted["residual_polygons"])
                and all(
                    frozen._same(frozen.points(a), frozen.points(b))
                    for a, b in zip(
                        given["residual_polygons"], accepted["residual_polygons"], strict=True
                    )
                ),
                "final row differs from accepted state",
            )
    if final_node:
        admit_terminal_contradiction(source, state_rows)
    else:
        require(
            source["terminal"] is True
            and source["closed"] is False
            and source["contradiction"] is None,
            "open ancestry checkpoint asserted a contradiction",
        )
    require(source["global_optimality_proved"] is False, "source scope changed")
    result["current_step"] = result["current_row"] = None
    remaining(budget)
    return state_groups, state_rows


def run(args: argparse.Namespace) -> dict[str, Any]:
    require(type(args.case_id) is int and 0 <= args.case_id < 2184, "case ID")
    require(0 < args.max_seconds <= 3600, "case wall ceiling")
    require(type(args.workers) is int and 1 <= args.workers <= 3, "row workers 1..3")
    require(type(args.max_events) is int and args.max_events > 0, "event ceiling")
    cover_backend = getattr(args, "cover_backend", "reference")
    require(cover_backend in ("reference", "fast"), "unsupported cover backend")
    collision_backend = getattr(args, "collision_backend", "reference")
    require(collision_backend in ("reference", "integer"), "unsupported collision backend")
    started, cpu_started = time.monotonic(), time.process_time()
    children_before = resource.getrusage(resource.RUSAGE_CHILDREN)
    budget = geometry.Budget(started + args.max_seconds, args.max_events)
    paths = {
        "checker": Path(__file__),
        "frozen_generic": Path(frozen.__file__),
        "degenerate_cover": Path(degenerate_cover.__file__),
        "refinement_helper": Path(refinement.__file__),
        "geometry": Path(geometry.__file__),
        "manifest": args.manifest,
    }
    if cover_backend == "fast":
        paths["fast_cover"] = Path(fast_cover.__file__)
    before: dict[str, str] = {}
    result: dict[str, Any] = {
        "status": "INCOMPLETE",
        "mask_index": args.case_id,
        "geometry_verified": False,
        "excluded_case_ids": [],
        "global_optimality_proved": False,
        "source_sha256": {},
        "max_seconds": args.max_seconds,
        "max_events": args.max_events,
        "workers": args.workers,
        "cover_backend": cover_backend,
        "collision_backend": collision_backend,
        "current_node": None,
        "current_step": None,
        "current_row": None,
        "pending_row_indices": [],
        "checked_row_indices_current_step": [],
    }
    try:
        before = {name: digest(path) for name, path in paths.items()}
        result["source_sha256"].update(before)
        require(before["geometry"] == frozen.GEOMETRY_SHA, "frozen geometry changed")
        require(before["frozen_generic"] == FROZEN_GENERIC_SHA, "frozen generic kernel changed")
        require(
            before["degenerate_cover"] == DEGENERATE_COVER_SHA,
            "closed degenerate cover kernel changed",
        )
        require(
            before["refinement_helper"] == REFINEMENT_HELPER_SHA,
            "refinement helper changed",
        )
        if cover_backend == "fast":
            require(before["fast_cover"] == FAST_COVER_SHA, "fast cover kernel changed")
        geometry.admit_d4_receipt()
        manifest = load_manifest(args.manifest)
        recipes = [case for case in manifest["cases"] if case["mask_index"] == args.case_id]
        require(len(recipes) == 1, "missing/duplicate case recipe")
        recipe = recipes[0]
        special_d4 = recipe["adapter"] == "baseline_necessary_d4"
        require(
            special_d4 or recipe["adapter"] == "sequential_wall_seed",
            "unsupported adapter",
        )
        require(
            1 <= len(recipe["ordered_ancestry_proposal"]) <= 8,
            "unsupported ancestry length",
        )
        require(
            recipe["source_profile"] == "necessary_D4_cuts_and_independent_geometry"
            if special_d4
            else recipe["source_profile"] in ("direct_v6", "direct_v9", "native_cached_v9"),
            "unsupported source profile",
        )
        nodes = recipe["ordered_ancestry_proposal"]
        require(
            all(node["position"] == index for index, node in enumerate(nodes))
            and nodes[-1]["source_sha256"] == recipe["source_sha256"]
            and len({node["source_sha256"] for node in nodes}) == len(nodes),
            "ancestry source order or identity",
        )
        mask = tuple(recipe["mask"])
        metadata_sha = manifest["input_sha256s"][recipe["family"]]
        paths["assignment"] = METADATA_OBJECTS / f"{metadata_sha}.gz"
        paths["cover"] = PACKET / "receipts/d4-independent/objects" / f"{geometry.COVER_SHA}.gz"
        bound_inputs = ["assignment", "cover"]
        if recipe["family"] == "A2":
            paths["a2_baseline"] = METADATA_OBJECTS / f"{manifest['input_sha256s']['A1']}.gz"
            paths["a2_helper"] = Path(a2_assignment.__file__)
            bound_inputs.extend(("a2_baseline", "a2_helper"))
        if len(nodes) > 1:
            paths["ancestry_helper"] = Path(ancestry.__file__)
            bound_inputs.append("ancestry_helper")
        if special_d4:
            paths["special_assignment"] = Path(special_assignment.__file__)
            paths["d4_admission"] = Path(d4_admission.__file__)
            paths["d4_cut_checker"] = Path(d4_cuts.__file__)
            bound_inputs.extend(("special_assignment", "d4_admission", "d4_cut_checker"))
        for name in bound_inputs:
            before[name] = digest(paths[name])
            result["source_sha256"][name] = before[name]
        if recipe["family"] == "A2":
            require(before["a2_helper"] == A2_HELPER_SHA, "A2 assignment helper changed")
        if len(nodes) > 1:
            require(
                before["ancestry_helper"] == ANCESTRY_HELPER_SHA,
                "ancestry helper changed",
            )
        if special_d4:
            require(
                before["special_assignment"] == SPECIAL_ASSIGNMENT_SHA
                and before["d4_admission"] == D4_ADMISSION_SHA
                and before["d4_cut_checker"] == D4_CHECKER_SHA
                and d4_cuts.dependencies_unchanged(),
                "special D4 source dependency changed",
            )
        cover = load_object(
            geometry.COVER_SHA, manifest, geometry.PACKET / "receipts/d4-independent/objects"
        )
        require(
            cover["canonical_eleven_cell_subsets"][args.case_id] == list(mask), "canonical mask"
        )
        admit_assignment(args.case_id, recipe, manifest)
        for role in ("source", "seed", "audit"):
            sha = recipe[f"{role}_sha256"]
            paths[role] = args.objects / f"{sha}.gz"
            before[role] = digest(paths[role])
            result["source_sha256"][role] = before[role]
        sources = []
        for index, node in enumerate(nodes):
            name = f"source_node_{index}"
            paths[name] = args.objects / f"{node['source_sha256']}.gz"
            before[name] = digest(paths[name])
            result["source_sha256"][name] = before[name]
            sources.append(load_object(node["source_sha256"], manifest, args.objects))
        seed = load_object(recipe["seed_sha256"], manifest, args.objects)
        audit = load_object(recipe["audit_sha256"], manifest, args.objects)
        has_collision = any(
            row["collision_regions"]
            for source in sources
            for step in source["steps"]
            for row in step["rows"]
        )
        if collision_backend == "integer":
            require(has_collision, "integer collision backend has no collision work")
        if any(
            step["prior_partner_pose_covers"]
            or any(row["collision_regions"] for row in step["rows"])
            for source in sources
            for step in source["steps"]
        ):
            paths["partner_helper"] = Path(partner.__file__)
            paths["collision_kernel"] = Path(collision_kernel.__file__)
            if collision_backend == "integer":
                paths["integer_collision"] = Path(integer_collision.__file__)
            bound_collision_sources = ["partner_helper", "collision_kernel"]
            if collision_backend == "integer":
                bound_collision_sources.append("integer_collision")
            for name in bound_collision_sources:
                before[name] = digest(paths[name])
                result["source_sha256"][name] = before[name]
            require(before["partner_helper"] == PARTNER_HELPER_SHA, "partner helper changed")
            require(
                before["collision_kernel"] == COLLISION_KERNEL_SHA,
                "collision kernel changed",
            )
            if collision_backend == "integer":
                require(
                    before["integer_collision"] == INTEGER_COLLISION_SHA,
                    "integer collision kernel changed",
                )
            require(
                collision_kernel.dependencies_unchanged(),
                "collision kernel dependency changed",
            )
        center_planes: dict[int, list[Plane]] | None = None
        if special_d4:
            baseline = load_object(manifest["input_sha256s"]["A1"], manifest, METADATA_OBJECTS)
            special_assignment.admit_special_audit(recipe, audit, baseline)
            supplied_inventory = getattr(args, "baseline_inventory", None)
            inventory_sha = getattr(args, "baseline_inventory_sha256", None)
            require(
                isinstance(supplied_inventory, Path) and isinstance(inventory_sha, str),
                "D4 baseline inventory arguments",
            )
            inventory = cast(Path, supplied_inventory)
            paths["baseline_execution_inventory"] = inventory
            before["baseline_execution_inventory"] = digest(inventory)
            result["source_sha256"]["baseline_execution_inventory"] = before[
                "baseline_execution_inventory"
            ]
            require(
                before["baseline_execution_inventory"] == inventory_sha,
                "D4 baseline inventory SHA",
            )
            provided_report = getattr(args, "d4_report_out", None)
            require(
                provided_report is None or isinstance(provided_report, Path), "D4 report path"
            )
            report_out = (
                cast(Path, provided_report)
                if provided_report is not None
                else args.out.with_name(f"{args.out.stem}-d4-cuts.json")
            )
            require(not report_out.exists(), "D4 report output already exists")
            remaining(budget)
            cut_report = d4_cuts.run(
                argparse.Namespace(
                    case=[args.case_id],
                    baseline_inventory=inventory,
                    baseline_inventory_sha256=inventory_sha,
                    max_seconds=min(60.0, budget.deadline - time.monotonic()),
                    max_nodes=5_000_000,
                    out=report_out,
                )
            )
            paths["d4_report"] = report_out
            before["d4_report"] = digest(report_out)
            result["source_sha256"]["d4_report"] = before["d4_report"]
            result["d4_report_path"] = str(report_out)
            center_planes = d4_admission.admitted_constraint_planes(
                sources[0], recipe, cut_report
            )
        for index, (node, source) in enumerate(zip(nodes, sources, strict=True)):
            require(
                source["node_id"] == node["node_id"]
                and source["mask_index"] == args.case_id
                and source["mask"] == list(mask),
                "node/case identity",
            )
            require(
                Q(source["U"]) == geometry.U
                and Q(source["B"]) == geometry.B
                and source["source"]["sha256"] == recipe["seed_sha256"],
                "source premise",
            )
            capability_preflight(
                source,
                mask,
                budget.max_nodes,
                nodes[index - 1]["source_sha256"] if index else None,
                admitted_constraints=special_d4,
            )
        if not special_d4:
            require(
                audit["source_sha256"] == recipe["source_sha256"]
                and audit["root_sha256"] == recipe["seed_sha256"]
                and audit["cover_sha256"] == geometry.COVER_SHA
                and audit["mask_index"] == args.case_id
                and audit["mask"] == list(mask)
                and audit["transferred_canonical_mask_indices"] == [args.case_id],
                "audit source/case binding",
            )
        seed_started, seed_cpu = time.monotonic(), time.process_time()
        groups, rows, world, bins = seed_state(seed, cover, args.case_id, mask, budget=budget)
        result["seed_wall_seconds"] = time.monotonic() - seed_started
        result["seed_process_cpu_seconds"] = time.process_time() - seed_cpu
        result["owned_seed_points_checked"] = sum(len(seed["groups"][str(i)]) for i in mask)
        result["seed_rows_checked"] = len(mask) * bins
        result["nodes_completed"] = 0
        for index, (_node, source) in enumerate(zip(nodes, sources, strict=True)):
            result["current_node"] = index
            if index:
                groups, rows = ancestry.admit_child_state(
                    source,
                    parent_source_sha256=nodes[index - 1]["source_sha256"],
                    seed_sha256=recipe["seed_sha256"],
                    case_id=args.case_id,
                    mask=mask,
                    accepted_groups=groups,
                    accepted_rows=rows,
                )
            groups, rows = replay_one_node(
                source,
                groups,
                rows,
                world=world,
                mask=mask,
                result=result,
                budget=budget,
                workers=args.workers,
                cover_backend=cover_backend,
                collision_backend=collision_backend,
                parent_sha=nodes[index - 1]["source_sha256"] if index else None,
                final_node=index == len(nodes) - 1,
                center_planes=center_planes,
            )
            result["nodes_completed"] = index + 1
        remaining(budget)
        require(
            all(digest(path) == before[name] for name, path in paths.items()),
            "source changed during replay",
        )
        if "collision_kernel" in paths:
            require(
                collision_kernel.dependencies_unchanged(),
                "collision kernel dependency changed during replay",
            )
        if special_d4:
            require(d4_cuts.dependencies_unchanged(), "D4 cut dependency changed during replay")
        result["status"] = "PASS_ONE_GENERIC_EXCLUSION"
        result["geometry_verified"] = True
        result["excluded_case_ids"] = [args.case_id]
        result["current_node"] = None
    except (geometry.IncompleteError, concurrent.futures.TimeoutError) as error:
        result["error"] = str(error)
    except (ValueError, KeyError, IndexError, TypeError, OSError, RuntimeError) as error:
        result["status"] = "REFUSED"
        result["error"] = str(error)
    result["wall_seconds"] = time.monotonic() - started
    result["coordinator_process_cpu_seconds"] = time.process_time() - cpu_started
    children_after = resource.getrusage(resource.RUSAGE_CHILDREN)
    result["child_process_cpu_seconds"] = (
        children_after.ru_utime
        + children_after.ru_stime
        - children_before.ru_utime
        - children_before.ru_stime
    )
    result["cpu_scope"] = "coordinator and completed child processes in this run"
    atomic_write_text(args.out, json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case-id", type=int, required=True)
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--objects", type=Path, default=OBJECTS)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--max-seconds", type=float, default=30)
    parser.add_argument("--max-events", type=int, default=50_000)
    parser.add_argument("--cover-backend", choices=("reference", "fast"), default="reference")
    parser.add_argument(
        "--collision-backend", choices=("reference", "integer"), default="reference"
    )
    parser.add_argument("--baseline-inventory", type=Path)
    parser.add_argument("--baseline-inventory-sha256")
    parser.add_argument("--d4-report-out", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    result = run(parser.parse_args())
    print(
        json.dumps(
            {key: result.get(key) for key in ("status", "mask_index", "wall_seconds", "error")}
        )
    )
    return 0 if result["status"] == "PASS_ONE_GENERIC_EXCLUSION" else 2


if __name__ == "__main__":
    sys.exit(main())
