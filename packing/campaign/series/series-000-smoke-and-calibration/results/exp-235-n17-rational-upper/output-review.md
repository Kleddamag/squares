# Independent Output Review

**Reviewer:** GPT-6 Astra, max reasoning.
**Date:** 2026-10-01. **Instrument:** `bacacdd15f4c7a410dfc9b8fff32c918e5851748`.
**Decision:** H-253 met; rational upper feasibility only.

The reviewer inspected every stdout/stderr, `exits.tsv`, `commands.log`, provenance,
source integrity, preregistration and the launcher correction.
Both local checkers accept 17 squares and 136 pairs at the exact side; the source agrees
on 17 squares, 68 contained vertices and 136 pairs.
The four grid/overlap controls have the expected results.
The negative-control gap is exactly -1/2. Both local target outputs have identical,
positive exact minimum-gap strings; containment is also positive.

The independent read-only audit below checked conversion fidelity in 0.208 seconds of
tool-reported command wall time, including launch overhead.
It did not repeat pair or containment geometry.
Run from `packing/` with the normal project interpreter and `PYTHONOPTIMIZE` unset.
The first attempt used a login shell and failed in unrelated Java/fnm shell startup
before Python; the successful call used `login: false`. Neither audit attempt wrote
research files.

```python
from fractions import Fraction as F
from pathlib import Path
import json
import yaml

assert __debug__
p = Path(
    "campaign/series/series-000-smoke-and-calibration/results/exp-235-n17-rational-upper/run-001"
)
src = json.loads(
    Path(
        "resources/web/n17-kleddamag-certified-bound-2026-09-21/kleddamag-17-squares-certified-bound/upper-packing-certificate.json"
    ).read_text()
)
w = yaml.safe_load((p / "witness.yaml").read_text())["witness"]
assert w["n"] == len(w["squares"]) == len(src["squares"]) == 17
assert F(w["side"]) == F(src["side"]) == F("4675530093604551/1000000000000000")
assert w["square_size"] == "1"
for index, (a, b) in enumerate(zip(src["squares"], w["squares"], strict=True), 1):
    assert b["id"] == index
    pts = [tuple(map(F, v)) for v in b["corners"]]
    x, y, t = (F(a[k]) for k in ("x", "y", "t"))
    assert tuple(sum(v[j] for v in pts) / 4 for j in (0, 1)) == (x, y)
    u = tuple(pts[1][j] - pts[0][j] for j in (0, 1))
    v = tuple(pts[2][j] - pts[1][j] for j in (0, 1))
    assert u == ((1 - t * t) / (1 + t * t), 2 * t / (1 + t * t))
    assert v == (-u[1], u[0])
    assert t == u[1] / (1 + u[0])
    assert tuple(pts[3][j] + u[j] for j in (0, 1)) == pts[2]
r = json.loads((p / "target-main.stdout").read_text())
assert (
    r["verification_passed"] and r["n"] == 17 and r["pairs_tested"] == 136 and not r["failures"]
)
assert F(r["side"]) == F(w["side"])
text = (p / "target-independent.stdout").read_text()
assert "VERIFIED: 17 squares, 136 pairs" in text
assert "minimum pair gap: " + r["minimum_best_pair_gap"] in text
assert F(r["minimum_best_pair_gap"]) > 0 and F(r["minimum_containment_clearance"]) > 0
assert max(q.stat().st_size for q in p.iterdir() if q.is_file()) < 10 * 1024 * 1024
```

The audit passed all 17 rows; maximum retained output was `witness.yaml`, 32,223 bytes.
Tracked source was clean; the new run directory was untracked at provenance capture.
The unsupported macOS memory guard is declared, and no hard memory limit is claimed.
All commands were below 90 seconds, the run completed in eight seconds, one worker was
used and the file-size cap was active.

This is independent implementation checking within the same separating-axis method.
The exact algebraic endpoint, a uniform local side theorem for its flexible family, and
global exclusion below that endpoint remain unproved by this experiment.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
