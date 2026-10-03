# Valid7: an independent exact check

**Claim.**  Let `μ₇` be the mixed cover `cover/L4_k02_box7.txt` of the square `[0, 7]²` (from
[evand/square-packing](https://github.com/evand/square-packing), `s12/certificates/k2m3/`): 800 axis-parallel
segments carrying uniform mass on 60 lines of the 1/5 grid, and Lebesgue measure on `[9/5, 26/5]²`; total mass
`5701378693611/125000000000 ≈ 45.611 < 46`.  **Valid7**: every closed unit square `Q ⊆ [0, 7]²`, at every
position and every angle, has `μ₇(Q) ≥ 1`.

By the reduction proved in Lean in evand/square-packing (`bentz_of_valid7`), Valid7 implies
**s(k² − 3) = k for every k ≥ 6**.  That repository checks Valid7 with one program; this repository is a second,
independently written exact check of the same statement.

**Result (2026-10-02): Valid7 holds.**  Every pose was certified, with no symmetry reduction:
156,800 root boxes covering centres `[0, 7]²` × `u = tan(θ/2) ∈ [−1/2, 1/2]`, 0 uncertified, 0 counterexamples;
9,640,060 leaves; about 626 core-hours.  The records are in the release `records-v1` and are re-checked by
`verify.sh`.

## Independence

* Written from the cover format specification (`s21/FORMAT.md` of evand/square-packing) and the statement of
  the claim only.  The first certificate's checker and its lemma documents were **not read**; `READ_LOG.md`
  lists exactly what was read.
* Different by design: no D4 reduction (all centres and a full period of angles are checked); the angle 0 by
  a closure argument instead of an enumeration; different exact primitives (below).
* Exact rational arithmetic throughout (`fractions.Fraction`; polynomials in `u` with
  [python-flint](https://github.com/flintlib/python-flint), our own Sturm-sequence root isolation).  No
  floating-point number enters any decision.

## Method (details and proofs: `DESIGN.md`; lemmas in the module docstrings)

Poses `Q(c, θ) = c + R_θ [−½, ½]²` with `u = tan(θ/2) ∈ [−½, ½]` (more than the period `π/2` of the square;
`θ = 0` is interior).

* **Angle 0 by closure.**  For `θ ∉ (π/2)ℤ` the mass is continuous in the pose, and it is upper semicontinuous
  everywhere; so `μ ≥ 1` for all `θ ≠ 0` gives it at `θ = 0`.
* **Tier A, box core bound** (`src/tier_a.py`).  All squares of a pose box (centre box × `u`-interval) contain a
  rational polygon (inner bound of the angular core, eroded by the centre box), so `μ(Q) ≥ μ(core)`, computed
  exactly.  For the Lebesgue square `S` also `area(Q ∩ S) ≥ 1 − area(O \ S)` with `O` a rational outer hull, so
  that squares inside `S` (mass exactly 1) cost nothing.  Adaptive bisection.
* **Fixed angle** (`src/solver.py`).  At fixed `θ` the mass is piecewise quadratic in the centre on an
  arrangement of lines (Lemma F1).  By Brunn–Minkowski, `√area(Q ∩ S)` is concave, so no face has an interior
  minimum (Lemma F2): the minimum over a centre box is at a vertex of the arrangement or at the 1-D critical point
  of an edge.
* **Tier B, exact in `u`** (`src/tier_b2.py`, `src/rf.py`, `src/tier_b.py`).  Near the zero-margin families
  (squares touching a wall, squares with edges on the heavy integer lines; their mass grows like `1 + c|u|`,
  `c ≈ 0.40–0.48`).  Every vertex candidate is the intersection of two lines whose coefficients are rational
  functions of `u`; for each pair the set of `u` where it lies in the admissible centre box is cut out exactly
  (real roots isolated by Sturm sequences), and on each piece the mass at the vertex is obtained as a rational
  function of `u` by symbolic execution (every branch decided at a sample point and recorded as a guard
  polynomial that must not vanish on the piece), then proved `≥ 1` exactly.  Edge critical points are handled
  line by line in the same way.  Values equal to 1 (tight) are allowed.
* **Records** (`src/run_all.py`, `src/check_record.py`).  Every leaf is recorded.  `check_record.py` re-checks,
  independently of the driver's control flow, that the roots are exactly a product grid of
  `[0, 7]² × [−½, ½]` (each root once, across all record files), that the leaves of every root form a bisection
  partition of it, the EMPTY leaves exactly, and that no Tier B leaf contains `u = 0`; optionally it re-runs
  Tier A and Tier B on random leaves (`--recheck N`, `--recheck-b N`).

## Tests

`tests/run_mutants.sh` makes three mutant covers, each lowering one tight configuration by a relative `10⁻⁴`
(the wall family, the Lebesgue square, the corner family at `[1, 2]²`), and checks that each is refused; Tier B
reports a concrete pose with its exact mass below 1.

## Reproducing

```
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
./verify.sh            # downloads the records of release records-v1, checks their sha256, runs check_record.py
                       # (about 10 minutes and 6 GB of memory), and runs the mutant tests
```

The full certificate run (about 626 core-hours; 20 hours on 32 cores) is

```
.venv/bin/python src/run_all.py cover/L4_k02_box7.txt --nproc 32 --record runs/full.jsonl    # add --resume after an interruption
.venv/bin/python src/check_record.py cover/L4_k02_box7.txt runs/full.jsonl
```

It can be split by centre x over machines with `--centers x0 x1 0 7` (x0, x1 multiples of 1/10) and separate
records, all passed together to `check_record.py`.  Other useful entry points: `src/cover.py <cover>` (format,
exact total, D4 invariance, reported only), `src/tier_b2.py <cover> x0 x1 y0 y1 u0 u1` (Tier B on one box).

## History of the run

The code changed once during the run (hand-off rule and failure reporting only, no proof step), and a defect
found before the run was fixed with all earlier records discarded; the record header lines were edited before
publication (path names only).  All of this, with the file hashes and which roots ran under which version, is in
`versions/VERSIONS.md`.

## License

MIT (`LICENSE`).  `cover/L4_k02_box7.txt` is from evand/square-packing under its MIT license (`NOTICE`).
