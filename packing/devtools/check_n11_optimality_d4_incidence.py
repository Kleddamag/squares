"""Check the final n=11 D4 bridge by incidence propagation and one distance bound.

This is the replacement that finding S3 of
`docs/project/reviews/review-2026-10-03-n11-optimality-adversarial-gpt6-pro.md` proposes
for the three finite searches of `check_n11_optimality_d4`. The sixteen closed cells and
the 220 closed four-view regions are rebuilt with that module's exact builders. Then, for
each source case 999, 1462 and 1659 in view g0 and each of the 216 ordered triples of
allowed raw masks in views g1, g2 and g3, the bijection between the eleven owners and each
view's eleven labels is propagated to a fixpoint. The one 999 survivor is closed by an
exact distance bound; the one 1462 survivor is the 999 case seen through the reflection g1.

Only the cover and overlay objects are read. The 1,572 strict distance bans, the 2,180
mask exclusions, and the case-438 capture are neither read nor replayed: they remain
premises, and this checker proves no global optimality.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
import sys
import time
from collections.abc import Sequence
from fractions import Fraction
from itertools import product
from pathlib import Path
from typing import Any, NamedTuple

from devtools import check_n11_optimality_d4 as d4

F = Fraction
Labels = tuple[int, ...]
Mask = tuple[int, ...]
Interval = tuple[F, F]
Box = tuple[Interval, Interval]

REPO = Path(__file__).resolve().parents[2]
PACKET = REPO / "packing/resources/web/n11-optimality-2026-09-29"
OBJECTS = PACKET / "receipts/d4-independent/objects"
RECONSTRUCTION = Path(d4.__file__).resolve()
PASS = "PASS_D4_INCIDENCE_BRIDGE"
REFUSED = "REFUSED_D4_INCIDENCE_BRIDGE"


class ObjectPin(NamedTuple):
    decoded_sha256: str
    stored_sha256: str


PINS = {
    "cover": ObjectPin(
        "df7938d9ba27095a38fabe45f8b26b259a2cc896c2ae4aac6bae874f417adc4e",
        "7c6d14012f06eb892912a50c93cc7408ce1f90524d46693c6178a01ceae71a99",
    ),
    "overlay": ObjectPin(
        "845b5f748843dd60fa7e290a5ea1a304da4e439ae229bd73a841aec816f4e700",
        "4b36026f5f16998929032abf5e730b56a2166a0880d5b6464b3abf9d9ed62bda",
    ),
}
TARGET = 438
SOURCES = (999, 1462, 1659)
OTHER_VIEWS = (1, 2, 3)
# Review S3's table: immediate contradictions, further propagation contradictions, and
# surviving triples per source. The operation counts depend on how a propagator counts
# and orders its steps, so they are recorded beside this checker's own, not required.
REVIEW_COUNTS = {999: (168, 47, 1), 1462: (198, 17, 1), 1659: (196, 20, 0)}
REVIEW_MAX_OPERATIONS = {999: 19, 1462: 15, 1659: 7}
REVIEW_SURVIVORS: dict[int, tuple[tuple[str, str, str], ...]] = {
    999: (("J1462", "J1462", "J999"),),
    1462: (("J999", "HJ999", "HJ1462"),),
    1659: (),
}
FORCED_BOXES: dict[Labels, Box] = {
    (1, 1, 11, 4): ((F(23, 50), F(27, 50)), (F(0), F(11, 100))),
    (2, 5, 6, 9): ((F(11, 25), F(14, 25)), (F(23, 100), F(7, 25))),
}
REVIEW_DELTA = (F(1, 10), F(7, 25))
SCALE_CAP = F(3)
DISTANCE_BOUND = F(1989, 2500)
# The construction's own view masks in the review's frame, where g0 carries case 438;
# `tests/test_n11_optimality_d4_incidence.py` derives them from `cases.trump11`.
CONSTRUCTION_PATTERN = ("J438", ("J1659", "HJ1462", "J999"))
# Review appendix A.3: sites 0..7 over 2,000,000; site 15-i is (1,1) minus site i.
COMPACT_DENOMINATOR = 2_000_000
COMPACT_SITES = (
    (209982, 265837),
    (746404, 91006),
    (1267243, 277512),
    (1731123, 205608),
    (206181, 800758),
    (742311, 625866),
    (1270514, 832045),
    (1781756, 671052),
)
SCOPE = (
    "Review S3's replacement for the final D4 bridge only. From the cover and overlay "
    "objects alone, every one of the 648 source/triple combinations for sources 999, "
    "1462 and 1659 under the hypothesis that no D4 view admits case 438 is contradicted "
    "by incidence propagation, by one exact distance bound (the 999 survivor), or by "
    "the reflection g1 onto the closed 999 source (the 1462 survivor). The 1,572-ban "
    "distance inventory is not read here; it remains the premise of the earlier "
    "conditional cuts for cases 2175 and 2176 and is not deleted by this bridge. All "
    "prior exclusions (the 2,180 mask exclusions that leave cases 438, 999, 1462 and "
    "1659) and the case-438 capture remain premises; no global optimality is proved."
)
REDUCTION = (
    "Let P be a packing whose four views carry the 1462 survivor's masks (J1462, J999, "
    "HJ999, HJ1462) in g0..g3. Since g2*g1 = H*g3 and g3*g1 = H*g2 and the half-turn H "
    "sends cell j to cell 15-j, a center of P in region R(a0,a1,a2,a3) maps under g1 to "
    "a center of g1(P) in region R(a1,a0,15-a3,15-a2). So g1(P) carries masks (J999, "
    "J1462, H(HJ1462), H(HJ999)) = (J999, J1462, J1462, J999): its g0 view is the raw "
    "canonical mask J999, with no half-turn needed, and its other views are the 999 "
    "survivor's. g1(P) is a packing in the same container satisfying the same premises, "
    "since the set of D4 views is unchanged and so no view of g1(P) admits case 438, "
    "and every one of the 216 triples of source 999 has been contradicted. Hence P does "
    "not exist either; no symmetry-equivariant boundary tie-break is needed."
)

RULES = (
    (
        "An owner's initial domain is every closed region whose g0 label is the owner "
        "and whose g1, g2, g3 labels lie in those views' masks."
    ),
    (
        "Immediate contradiction: before any rule fires, some owner has no region or "
        "some label of a g1, g2 or g3 mask lies in no owner's domain."
    ),
    (
        "Reserve (one operation): an owner with exactly one region removes from every "
        "other owner each region sharing any of its g1, g2, g3 labels."
    ),
    (
        "Force (one operation when it removes a region): a label carried by one owner's "
        "domain alone restricts that owner to regions carrying it."
    ),
    (
        "Propagation contradiction: an owner's domain or a label's owner set empties "
        "after a rule has fired."
    ),
)


class Outcome(NamedTuple):
    status: str
    operations: int
    domains: dict[int, frozenset[int]]
    reason: str


class SourceCensus(NamedTuple):
    source: int
    counts: dict[str, int]
    max_operations: int
    survivors: list[tuple[tuple[Mask, ...], Outcome]]


def require(condition: object, message: str) -> None:
    d4.require(condition, message)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_object(directory: Path, role: str) -> dict[str, Any]:
    pin = PINS[role]
    stored = (directory / f"{pin.decoded_sha256}.gz").read_bytes()
    require(sha256_bytes(stored) == pin.stored_sha256, f"{role} stored object hash mismatch")
    decoded = gzip.decompress(stored)
    require(sha256_bytes(decoded) == pin.decoded_sha256, f"{role} source hash mismatch")
    return json.loads(decoded)


def check_compact_cover(cover: dict[str, Any]) -> int:
    sites = [(F(x, COMPACT_DENOMINATOR), F(y, COMPACT_DENOMINATOR)) for x, y in COMPACT_SITES]
    sites += [(1 - x, 1 - y) for x, y in reversed(sites)]
    reported = [tuple(F(value) for value in row["center"]) for row in cover["cells"]]
    require(reported == sites, "cover sites differ from the review's compact specification")
    return len(sites)


def mask_names(canonical: Sequence[Mask], cases: Sequence[int]) -> dict[Mask, str]:
    names: dict[Mask, str] = {}
    for case in cases:
        names[canonical[case]] = f"J{case}"
        names[d4.half_turn(canonical[case])] = f"HJ{case}"
    require(len(names) == 2 * len(cases), "allowed raw masks are not distinct")
    return names


def initial_domains(labels: Sequence[Labels], masks: Sequence[Mask]) -> dict[int, set[int]]:
    allowed = [frozenset(mask) for mask in masks]
    return {
        owner: {
            region
            for region, row in enumerate(labels)
            if row[0] == owner and all(row[view] in allowed[view] for view in OTHER_VIEWS)
        }
        for owner in masks[0]
    }


def supporters(
    labels: Sequence[Labels], domains: dict[int, set[int]], view: int, label: int
) -> list[int]:
    return [
        owner
        for owner, domain in domains.items()
        if any(labels[region][view] == label for region in domain)
    ]


def outcome(status: str, operations: int, domains: dict[int, set[int]], reason: str) -> Outcome:
    frozen = {owner: frozenset(domain) for owner, domain in domains.items()}
    return Outcome(status, operations, frozen, reason)


def unsupported_label(
    labels: Sequence[Labels], masks: Sequence[Mask], domains: dict[int, set[int]]
) -> tuple[int, int] | None:
    for view in OTHER_VIEWS:
        for label in masks[view]:
            if not supporters(labels, domains, view, label):
                return view, label
    return None


def reserve(
    labels: Sequence[Labels], domains: dict[int, set[int]], owner: int
) -> tuple[bool, int | None]:
    """Remove the labels of `owner`'s only region from every other owner's domain."""
    (region,) = domains[owner]
    changed = False
    for other, domain in domains.items():
        if other == owner:
            continue
        clashing = {
            candidate
            for candidate in domain
            if any(labels[candidate][view] == labels[region][view] for view in OTHER_VIEWS)
        }
        if clashing:
            domain.difference_update(clashing)
            changed = True
            if not domain:
                return changed, other
    return changed, None


def propagate(labels: Sequence[Labels], masks: Sequence[Mask]) -> Outcome:
    """Propagate the owner/label bijection of one four-view mask assignment.

    Owners are the eleven g0 labels of `masks[0]`. An owner's domain is every closed
    region with its g0 label whose label in each other view lies in that view's mask.
    Two sound rules run to a fixpoint: an owner with one region reserves that region's
    label in every view, and a view's label carried by one owner's domain alone forces
    that owner onto it. An empty domain or an uncarried label is a contradiction:
    "immediate" before any rule fires, "propagation" after.
    """
    domains = initial_domains(labels, masks)
    empty = [owner for owner in sorted(domains) if not domains[owner]]
    if empty:
        return outcome("immediate", 0, domains, f"owner {empty[0]} has no region")
    missing = unsupported_label(labels, masks, domains)
    if missing is not None:
        view, label = missing
        return outcome("immediate", 0, domains, f"label {label} of g{view} has no owner")
    operations = 0
    reserved: set[int] = set()
    changed = True
    while changed:
        changed = False
        for owner in sorted(domains):
            if owner in reserved or len(domains[owner]) != 1:
                continue
            reserved.add(owner)
            operations += 1
            removed, emptied = reserve(labels, domains, owner)
            changed |= removed
            if emptied is not None:
                reason = f"owner {owner} reserves every region of owner {emptied}"
                return outcome("propagation", operations, domains, reason)
        for view in OTHER_VIEWS:
            for label in masks[view]:
                owners = supporters(labels, domains, view, label)
                if not owners:
                    reason = f"label {label} of g{view} lost every owner"
                    return outcome("propagation", operations, domains, reason)
                if len(owners) > 1:
                    continue
                domain = domains[owners[0]]
                off_label = {region for region in domain if labels[region][view] != label}
                if off_label:
                    domain.difference_update(off_label)
                    operations += 1
                    changed = True
    return outcome("survivor", operations, domains, "fixpoint")


def run_census(
    labels: Sequence[Labels],
    canonical: Sequence[Mask],
    sources: Sequence[int],
    allowed: Sequence[Mask],
    deadline: float,
) -> dict[int, SourceCensus]:
    result: dict[int, SourceCensus] = {}
    for source in sources:
        counts = {"triples": 0, "immediate": 0, "propagation": 0, "survivor": 0}
        survivors: list[tuple[tuple[Mask, ...], Outcome]] = []
        most = 0
        for triple in product(allowed, repeat=3):
            d4.check_deadline(deadline)
            found = propagate(labels, (canonical[source], *triple))
            counts["triples"] += 1
            counts[found.status] += 1
            most = max(most, found.operations)
            if found.status == "survivor":
                survivors.append((triple, found))
        result[source] = SourceCensus(source, counts, most, survivors)
    return result


def text(value: F) -> str:
    return str(value)


def polygon_json(polygon: d4.Polygon) -> list[list[str]]:
    return [[text(x), text(y)] for x, y in polygon]


def box_json(box: Box) -> dict[str, list[str]]:
    return {"x": [text(box[0][0]), text(box[0][1])], "y": [text(box[1][0]), text(box[1][1])]}


def bounding_box(polygon: d4.Polygon) -> Box:
    xs = [x for x, _ in polygon]
    ys = [y for _, y in polygon]
    return (min(xs), max(xs)), (min(ys), max(ys))


def box_inside(inner: Box, outer: Box) -> bool:
    return all(
        outer[axis][0] <= inner[axis][0] <= inner[axis][1] <= outer[axis][1] for axis in (0, 1)
    )


def reflect_box(box: Box) -> Box:
    return (1 - box[0][1], 1 - box[0][0]), box[1]


def max_delta(first: Box, second: Box) -> tuple[F, F]:
    dx, dy = (
        max(second[axis][1] - first[axis][0], first[axis][1] - second[axis][0])
        for axis in (0, 1)
    )
    return dx, dy


def forced_owner(labels: Sequence[Labels], found: Outcome, region: Labels) -> int:
    index = labels.index(region)
    owners = [owner for owner, domain in found.domains.items() if domain == {index}]
    require(len(owners) == 1, f"region {region} is not forced on exactly one owner")
    return owners[0]


def close_forced_pair(
    labels: Sequence[Labels],
    vertices: Sequence[d4.Polygon],
    found: Outcome,
    boxes: dict[Labels, Box],
) -> dict[str, Any]:
    """Contradict a fixpoint that forces two distinct owners into two near regions."""
    regions = list(boxes)
    require(len(regions) == 2, "a distance closure takes exactly two regions")
    owners = [forced_owner(labels, found, region) for region in regions]
    require(len(set(owners)) == 2, "the forced regions do not hold two distinct owners")
    forced: list[dict[str, Any]] = []
    for owner, region in zip(owners, regions, strict=True):
        polygon = vertices[labels.index(region)]
        box = bounding_box(polygon)
        require(box_inside(box, boxes[region]), f"region {region} leaves its stated box")
        forced.append(
            {
                "owner": owner,
                "region_labels": list(region),
                "vertices": polygon_json(polygon),
                "vertex_bounding_box": box_json(box),
                "stated_box": box_json(boxes[region]),
                "inside_stated_box": True,
            }
        )
    dx, dy = max_delta(boxes[regions[0]], boxes[regions[1]])
    require(dx <= REVIEW_DELTA[0] and dy <= REVIEW_DELTA[1], "box differences exceed review")
    scale = d4.U - 1
    require(0 < scale < SCALE_CAP, "physical scale is not below three")
    review_sum = REVIEW_DELTA[0] ** 2 + REVIEW_DELTA[1] ** 2
    require(SCALE_CAP**2 * review_sum == DISTANCE_BOUND, "review bound arithmetic changed")
    box_bound = scale**2 * review_sum
    require(box_bound < DISTANCE_BOUND < 1, "box distance bound is not below 1989/2500")
    first, second = (vertices[labels.index(region)] for region in regions)
    exact = scale**2 * max(d4.squared_distance(p, q) for p in first for q in second)
    require(exact <= scale**2 * (dx**2 + dy**2) <= box_bound, "vertex bound exceeds box bound")
    require(exact < 1, "forced centers may be a unit apart")
    return {
        "forced_regions": forced,
        "max_abs_dx_from_boxes": text(dx),
        "max_abs_dy_from_boxes": text(dy),
        "physical_scale": text(scale),
        "physical_scale_below_3": True,
        "box_bound_squared_distance": text(box_bound),
        "box_bound_squared_distance_float": float(box_bound),
        "review_bound": text(DISTANCE_BOUND),
        "box_bound_below_review_bound_below_one": True,
        "exact_vertex_max_squared_physical_distance": text(exact),
        "exact_vertex_max_squared_physical_distance_float": float(exact),
        "exact_vertex_bound_below_one": True,
    }


def reflect_labels(row: Labels) -> Labels:
    """Labels under g1 of a region: g1g1 = 1, g2g1 = H g3, g3g1 = H g2."""
    return row[1], row[0], 15 - row[3], 15 - row[2]


def reflect_masks(masks: Sequence[Mask]) -> tuple[Mask, ...]:
    return masks[1], masks[0], d4.half_turn(masks[3]), d4.half_turn(masks[2])


def check_reflection(labels: Sequence[Labels], vertices: Sequence[d4.Polygon]) -> int:
    """Check that g1 carries every closed region R(a) onto R(reflect_labels(a))."""
    index = {row: position for position, row in enumerate(labels)}
    for position, row in enumerate(labels):
        image = reflect_labels(row)
        require(reflect_labels(image) == row, "label reflection is not an involution")
        require(image in index, f"reflected region {image} is missing")
        moved = d4.hull((1 - x, y) for x, y in vertices[position])
        require(moved == vertices[index[image]], f"g1 does not carry region {row}")
    return len(labels)


def named(masks: Sequence[Mask], names: dict[Mask, str]) -> list[str]:
    return [names[mask] for mask in masks]


def survivor_json(
    labels: Sequence[Labels], masks: Sequence[Mask], found: Outcome, names: dict[Mask, str]
) -> dict[str, Any]:
    return {
        "view_mask_names": named(masks, names),
        "view_masks": [list(mask) for mask in masks],
        "operations": found.operations,
        "fixpoint_domains": {
            str(owner): sorted(list(labels[region]) for region in domain)
            for owner, domain in sorted(found.domains.items())
        },
    }


def census_json(
    found: SourceCensus, canonical: Sequence[Mask], names: dict[Mask, str]
) -> dict[str, Any]:
    review = REVIEW_COUNTS.get(found.source)
    survivors = [named(triple, names) for triple, _ in found.survivors]
    entry: dict[str, Any] = {
        "source_canonical_index": found.source,
        "source_mask": list(canonical[found.source]),
        "triples": found.counts["triples"],
        "immediate_contradictions": found.counts["immediate"],
        "propagation_contradictions": found.counts["propagation"],
        "surviving_triples": found.counts["survivor"],
        "max_propagation_operations": found.max_operations,
        "survivor_other_view_masks": survivors,
    }
    if review is not None:
        entry["review_counts"] = {
            "immediate_contradictions": review[0],
            "propagation_contradictions": review[1],
            "surviving_triples": review[2],
            "max_recorded_propagation_operations": REVIEW_MAX_OPERATIONS[found.source],
        }
    return entry


def check_review_census(censuses: dict[int, SourceCensus], names: dict[Mask, str]) -> None:
    for source, found in censuses.items():
        counts = found.counts
        observed = (counts["immediate"], counts["propagation"], counts["survivor"])
        require(counts["triples"] == 216, f"source {source} did not see 216 triples")
        require(observed == REVIEW_COUNTS[source], f"source {source} counts differ from review")
        survivors = tuple(tuple(named(triple, names)) for triple, _ in found.survivors)
        require(survivors == REVIEW_SURVIVORS[source], f"source {source} survivors differ")


def reduce_by_reflection(
    labels: Sequence[Labels],
    vertices: Sequence[d4.Polygon],
    canonical: Sequence[Mask],
    censuses: dict[int, SourceCensus],
    names: dict[Mask, str],
) -> dict[str, Any]:
    (triple, found), *rest = censuses[1462].survivors
    require(not rest, "source 1462 has more than one survivor")
    masks = (canonical[1462], *triple)
    require(masks[1] == canonical[999], "the 1462 survivor's g1 view is not raw J999")
    transported = reflect_masks(masks)
    require(transported[0] == canonical[999], "reflected source is not raw J999")
    require(all(mask in names for mask in transported[1:]), "reflected view mask not allowed")
    closed = [other for other, _ in censuses[999].survivors]
    require(transported[1:] in closed, "reflected triple is not the 999 survivor")
    regions = check_reflection(labels, vertices)
    boxes = {reflect_labels(region): reflect_box(box) for region, box in FORCED_BOXES.items()}
    direct = close_forced_pair(labels, vertices, found, boxes)
    return {
        "survivor": survivor_json(labels, masks, found, names),
        "g1_view_raw_mask": list(masks[1]),
        "g1_view_is_raw_canonical_j999": True,
        "reflected_view_mask_names": named(transported, names),
        "reflected_masks_equal_999_survivor": True,
        "regions_carried_by_g1": regions,
        "argument": REDUCTION,
        "direct_corroboration": direct,
    }


def control_census(
    labels: Sequence[Labels], canonical: Sequence[Mask], deadline: float
) -> dict[str, Any]:
    """Allow case 438 again: propagation alone must leave the construction's pattern."""
    cases = (TARGET, *SOURCES)
    names = mask_names(canonical, cases)
    censuses = run_census(labels, canonical, cases, sorted(names), deadline)
    source, triple = CONSTRUCTION_PATTERN
    require(source == f"J{TARGET}", "construction pattern is not anchored at case 438")
    pattern = list(triple)
    found = [named(masks, names) for masks, _ in censuses[TARGET].survivors]
    require(pattern in found, "the construction's own pattern did not survive propagation")
    return {
        "allowed_raw_masks": sorted(names.values()),
        "construction_pattern": {"g0": source, "other_views": pattern, "survives": True},
        "sources": {
            str(case): {
                "triples": entry.counts["triples"],
                "immediate_contradictions": entry.counts["immediate"],
                "propagation_contradictions": entry.counts["propagation"],
                "surviving_triples": entry.counts["survivor"],
            }
            for case, entry in censuses.items()
        },
    }


def verify(objects: Path, *, max_seconds: float) -> dict[str, Any]:
    start = time.monotonic()
    cpu_start = time.process_time()
    require(math.isfinite(max_seconds) and max_seconds > 0, "wall ceiling must be positive")
    deadline = start + max_seconds
    require(
        {role: pin.decoded_sha256 for role, pin in PINS.items()}
        == {role: d4.INPUT_HASHES[role] for role in PINS},
        "input pins disagree with the reconstruction module",
    )
    cover = load_object(objects, "cover")
    overlay = load_object(objects, "overlay")
    require(overlay["cover_sha256"] == PINS["cover"].decoded_sha256, "overlay parent mismatch")
    compact_sites = check_compact_cover(cover)
    cells, canonical = d4.check_cover(cover)
    d4.check_deadline(deadline)
    labels, vertices, prefixes, dimensions = d4.check_overlay(cells, overlay)
    d4.check_deadline(deadline)
    names = mask_names(canonical, SOURCES)
    allowed = sorted(names)
    censuses = run_census(labels, canonical, SOURCES, allowed, deadline)
    check_review_census(censuses, names)
    (triple, found), *_ = censuses[999].survivors
    masks = (canonical[999], *triple)
    distance = close_forced_pair(labels, vertices, found, FORCED_BOXES)
    reduction = reduce_by_reflection(labels, vertices, canonical, censuses, names)
    control = control_census(labels, canonical, deadline)
    d4.check_deadline(deadline)
    return {
        "status": PASS,
        "scope": SCOPE,
        "global_optimality_proved": False,
        "input_sha256": {role: pin.decoded_sha256 for role, pin in PINS.items()},
        "input_stored_object_sha256": {role: pin.stored_sha256 for role, pin in PINS.items()},
        "checker_path": "packing/devtools/check_n11_optimality_d4_incidence.py",
        "checker_sha256": sha256_bytes(Path(__file__).read_bytes()),
        "reconstruction_module_path": "packing/devtools/check_n11_optimality_d4.py",
        "reconstruction_module_sha256": sha256_bytes(RECONSTRUCTION.read_bytes()),
        "compact_cover_sites_checked": compact_sites,
        "overlay_prefix_counts": prefixes,
        "overlay_dimensions": {str(key): value for key, value in sorted(dimensions.items())},
        "allowed_non_target_raw_masks": {names[mask]: list(mask) for mask in allowed},
        "views": ["g0(x,y)=(x,y)", "g1(x,y)=(1-x,y)", "g2(x,y)=(1-y,x)", "g3(x,y)=(y,x)"],
        "propagation_rules": list(RULES),
        "sources": [census_json(censuses[source], canonical, names) for source in SOURCES],
        "survivor_999": survivor_json(labels, masks, found, names),
        "distance_closure_999": distance,
        "reflection_reduction_1462": reduction,
        "control_with_case_438_allowed": control,
        "wall_seconds": time.monotonic() - start,
        "process_cpu_seconds": time.process_time() - cpu_start,
    }


def refusal(error: Exception) -> dict[str, Any]:
    return {
        "status": REFUSED,
        "reason": f"{type(error).__name__}: {error}",
        "global_optimality_proved": False,
        "checker_sha256": sha256_bytes(Path(__file__).read_bytes()),
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--objects", type=Path, default=OBJECTS)
    parser.add_argument("--max-seconds", type=float, default=45.0)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        result = verify(args.objects, max_seconds=args.max_seconds)
    except (ValueError, KeyError, TypeError, OSError, TimeoutError) as error:
        result = refusal(error)
    rendered = json.dumps(result, indent=2) + "\n"
    if args.output is not None:
        args.output.write_text(rendered)
    print(rendered, end="")
    return 0 if result["status"] == PASS else 1


if __name__ == "__main__":
    sys.exit(main())
