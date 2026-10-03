"""Exact tiny geometry controls for the pinned publisher's distinct checker.

Run from the workspace root with Python 3:
  python reconciliation-original-coverage-check.py
No certificate, capture graph, or global theorem is replayed.
"""

if not __debug__:
    raise RuntimeError("This mathematical checker refuses Python -O/-OO.")

from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import sys

source_dir = Path("original/src/evidence/research/phase3/work/phase3/hull").resolve()
sys.path.insert(0, str(source_dir))
import arrangement_audit_v2 as arrangement
import audit_capture_v9 as capture

for module, expected in (
    (arrangement, "0dfc3d4ca546cf465d39bc75c534eeca133099a5283acae95810c4e957f3fc0b"),
    (capture, "95ae3362ee4992c332960e4af53697dd3d1b31e381682051b49fd47700ad9d0c"),
):
    assert hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest() == expected


def rect(x0, x1):
    return [(x0, F(0)), (x1, F(0)), (x1, F(1)), (x0, F(1))]


target = [(F(0), F(1))]
below = [(F(0), F(0))]
triangle = [(F(0), F(1)), (F(1), F(0)), (F(1), F(2))]
unit = rect(F(0), F(1))
left = rect(F(0), F(1, 2))
right = rect(F(1, 2), F(1))
gapped = rect(F(1, 2) + F(1, 10**50), F(1))
segment = [(F(0), F(0)), (F(1), F(0))]
controls = {
    "point_below": capture.lower_dimensional_cover(target, [below]),
    "point_equal": capture.lower_dimensional_cover(target, [target]),
    "segment_exact_seam": capture.lower_dimensional_cover(segment, [left, right]),
    "segment_gap_1e_minus_50": capture.lower_dimensional_cover(segment, [left, gapped]),
    "triangle_uncovered": arrangement.union_cover(triangle, [below]),
    "area_exact_seam": arrangement.union_cover(unit, [left, right]),
    "area_gap_1e_minus_50": arrangement.union_cover(unit, [left, gapped]),
}
expected = {
    "point_below": False,
    "point_equal": True,
    "segment_exact_seam": True,
    "segment_gap_1e_minus_50": False,
    "triangle_uncovered": False,
    "area_exact_seam": True,
    "area_gap_1e_minus_50": False,
}
assert all(controls[name]["passed"] is value for name, value in expected.items())
closure = sorted({
    Path(module.__file__).resolve()
    for module in list(sys.modules.values())
    if getattr(module, "__file__", None)
    and Path(module.__file__).resolve().is_relative_to(Path("original").resolve())
})
print(json.dumps({
    "scope": "Unchanged publisher helper modules; tiny synthetic inputs only, no global replay.",
    "source_revision": "Queuingtheorydotcom/11SquaresOptimal@f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c",
    "source_sha256": {
        Path(m.__file__).name: hashlib.sha256(Path(m.__file__).read_bytes()).hexdigest()
        for m in (arrangement, capture)
    },
    "required_source_files": {
        str(path.relative_to(Path.cwd())): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in closure
    },
    "controls": controls,
}, indent=2, default=str))
