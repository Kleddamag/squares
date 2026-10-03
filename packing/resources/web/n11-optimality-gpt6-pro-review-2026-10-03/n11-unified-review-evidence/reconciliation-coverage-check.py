"""Small exact regression checks; no certificate or global proof replay.

Run from the workspace root:
  PYTHONPATH=squares/packing python reconciliation-coverage-check.py
"""

if not __debug__:
    raise RuntimeError("This mathematical checker refuses Python -O/-OO.")

from fractions import Fraction as Q
from itertools import combinations_with_replacement, pairwise
import hashlib
import json
from pathlib import Path
import time

from devtools import check_n11_optimality_field_mask0 as old
from devtools import n11_fast_exact_cover as fast
from devtools import n11_indexed_exact_cover as indexed
from devtools import check_n11_closed_degenerate_cover as degenerate
from devtools import check_n11_optimality_d4 as d4

EXPECTED_SOURCES = {
    "check_n11_optimality_field_mask0.py": "75fc0238f2ac91af9dc9cf57bd00792343dcf3321c395adddebf0f3465113ce5",
    "n11_fast_exact_cover.py": "eb21b1acda671b9f858039d077b0c8a30d035ee5920e083887952bf44b156904",
    "n11_indexed_exact_cover.py": "68580e324e56c555ea0587b6f396b208fb66563d1e10bd449b446c97b7667ccd",
    "check_n11_closed_degenerate_cover.py": "858c61c3ffa464a12be0fda9a14f802d7d9ea22f9b6aaa2b06c6974f0caa5385",
    "check_n11_optimality_d4.py": "19f4b0a47afd6acb327e85bd4a98ca2a43d2fdaa49aeb0edd30aa12d1b6aac1d",
}
MODULES = [old, fast, indexed, degenerate, d4]
for module in MODULES:
    module_path = Path(module.__file__)
    assert hashlib.sha256(module_path.read_bytes()).hexdigest() == EXPECTED_SOURCES[module_path.name]


def interval_poly(interval):
    lo, hi = interval
    return [(Q(0), lo)] if lo == hi else [(Q(0), lo), (Q(0), hi)]


def oracle(target, spans):
    """Closed membership at every endpoint and every open arrangement interval."""
    lo, hi = target
    points = sorted({lo, hi, *(x for span in spans for x in span if lo <= x <= hi)})
    probes = points + [(a + b) / 2 for a, b in pairwise(points)]
    return all(any(a <= p <= b for a, b in spans) for p in probes)


def old_slice(target, spans):
    return old.covers_vertical(interval_poly(target), [interval_poly(s) for s in spans], Q(0))


def fast_slice(target, spans):
    return fast._covers_vertical(
        fast._compile_polygon(interval_poly(target)),
        [fast._compile_polygon(interval_poly(s)) for s in spans],
        Q(0),
    )


def outcome(function, *args):
    try:
        result = function(*args, budget=old.Budget(time.monotonic() + 10, 100000))
    except ValueError as error:
        return {"accepted": False, "error": str(error)}
    return {"accepted": True, "result": result}


def rectangle(x0, x1, y0=Q(0), y1=Q(1)):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


intervals = [(Q(a), Q(b)) for a in range(-3, 4) for b in range(a, 4)]
region_lists = [(), *((s,) for s in intervals), *combinations_with_replacement(intervals, 2)]
stats = {
    "cases": 0,
    "old_false_accept_singleton": 0,
    "old_false_accept_nondegenerate": 0,
    "old_false_reject": 0,
    "corrected_errors": 0,
}
for target in intervals:
    for spans in region_lists:
        stats["cases"] += 1
        expected = oracle(target, spans)
        historical = old_slice(target, spans)
        corrected = fast_slice(target, spans)
        if historical and not expected:
            key = "old_false_accept_singleton" if target[0] == target[1] else "old_false_accept_nondegenerate"
            stats[key] += 1
        stats["old_false_reject"] += int(expected and not historical)
        stats["corrected_errors"] += int(corrected != expected)

triangle = [(Q(0), Q(1)), (Q(1), Q(0)), (Q(1), Q(2))]
below = [(Q(0), Q(0))]
target_point = [(Q(0), Q(1))]
unit = rectangle(Q(0), Q(1))
left = rectangle(Q(0), Q(1, 2))
right = rectangle(Q(1, 2), Q(1))
gapped_right = rectangle(Q(1, 2) + Q(1, 10**50), Q(1))
controls = {
    "singleton_target_1_span_0": {
        "old": old_slice((Q(1), Q(1)), [(Q(0), Q(0))]),
        "corrected": fast_slice((Q(1), Q(1)), [(Q(0), Q(0))]),
        "oracle": False,
    },
    "positive_area_triangle_vertex_slice": {
        "area_twice": str(old.area2(triangle)),
        "target_slice": list(map(str, old.vertical_interval(triangle, Q(0)))),
        "region_slice": list(map(str, old.vertical_interval(below, Q(0)))),
        "historical_slice_accepts": old.covers_vertical(triangle, [below], Q(0)),
        "historical_full_cover": outcome(old.exact_union_cover, triangle, [below]),
        "corrected_full_cover": outcome(fast.exact_union_cover, triangle, [below]),
    },
    "degenerate_domain_guards": {
        "historical_point_cover": outcome(old.exact_union_cover, target_point, [target_point]),
        "compiled_point_cover": outcome(fast.exact_union_cover, target_point, [target_point]),
        "indexed_point_cover": outcome(indexed.exact_union_cover, target_point, [target_point]),
    },
    "separate_point_checker": {
        "point_below": outcome(degenerate.exact_cover_closed_degenerate, target_point, [below]),
        "point_equal": outcome(degenerate.exact_cover_closed_degenerate, target_point, [target_point]),
        "point_above": outcome(degenerate.exact_cover_closed_degenerate, target_point, [[(Q(0), Q(2))]]),
    },
    "closed_seam_and_gap": {},
}
for name, checker in (("historical", old), ("compiled", fast), ("indexed", indexed)):
    controls["closed_seam_and_gap"][name] = {
        "exact_seam": outcome(checker.exact_union_cover, unit, [left, right]),
        "gap_1e_minus_50": outcome(checker.exact_union_cover, unit, [left, gapped_right]),
    }
segment = [(Q(0), Q(0)), (Q(1), Q(0))]
controls["separate_segment_checker"] = {
    "exact_seam": outcome(degenerate.exact_cover_closed_degenerate, segment, [left, right]),
    "gap_1e_minus_50": outcome(degenerate.exact_cover_closed_degenerate, segment, [left, gapped_right]),
}

assert stats == {
    "cases": 12180,
    "old_false_accept_singleton": 616,
    "old_false_accept_nondegenerate": 0,
    "old_false_reject": 0,
    "corrected_errors": 0,
}, stats
assert controls["positive_area_triangle_vertex_slice"]["historical_slice_accepts"]
assert not controls["positive_area_triangle_vertex_slice"]["historical_full_cover"]["accepted"]
assert all(not v["accepted"] for v in controls["degenerate_domain_guards"].values())
assert controls["separate_point_checker"]["point_equal"]["accepted"]
assert not controls["separate_point_checker"]["point_below"]["accepted"]
assert not controls["separate_point_checker"]["point_above"]["accepted"]
for v in [*controls["closed_seam_and_gap"].values(), controls["separate_segment_checker"]]:
    assert v["exact_seam"]["accepted"] and not v["gap_1e_minus_50"]["accepted"]

cover_path = Path("geometry-audit") / (old.COVER_SHA + ".json")
cover_bytes = cover_path.read_bytes()
assert hashlib.sha256(cover_bytes).hexdigest() == old.COVER_SHA
cover_data = json.loads(cover_bytes)
reconstructed_cells, canonical_masks = d4.check_cover(cover_data)
for record in cover_data["cells"]:
    listed_polygon = [old.point(v) for v in record["vertices"]]
    # Field calls use listed polygon order, so check it independently of the
    # D4 reader's own hull normalization.
    checked_hull = degenerate.convex_hull(listed_polygon)
    assert old.area2(listed_polygon) == old.area2(checked_hull) > 0
controls["fixed_cover_convexity"] = {
    "sha256": old.COVER_SHA,
    "cells": len(reconstructed_cells),
    "all_raw_vertex_orders_convex_with_positive_area": True,
    "scope": "Reconstruct fixed Voronoi cells and validate their raw vertex orders; no D4 overlay/search replay.",
}

result = {
    "scope": "Exact small synthetic controls of unchanged pinned helper modules; no full global replay.",
    "source_revision": "jlevy/squares@ea0a3b19a70085683c3b65946cded03ffe4e2415",
    "source_sha256": {
        Path(m.__file__).name: hashlib.sha256(Path(m.__file__).read_bytes()).hexdigest() for m in MODULES
    },
    "required_source_files": [str(Path(m.__file__).resolve().relative_to(Path.cwd())) for m in MODULES],
    "required_data_files": [str(cover_path)],
    "finite_test_grid": "All closed targets on {-3,-2,-1,0,1,2,3}; zero, one, or two covering intervals, unordered with replacement.",
    "enumeration": stats,
    "controls": controls,
}
print(json.dumps(result, indent=2))
