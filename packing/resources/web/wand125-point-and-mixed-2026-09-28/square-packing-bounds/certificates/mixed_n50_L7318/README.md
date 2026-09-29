# s(50) >= 3659/500 = 7.318

A density certificate proving that 50 unit squares do not fit in a square of side
`L = 3659/500 = 7.318`. This exceeds Green's bound for `n = 50`,
`2√2 + 101/25 + 3√14/25 = 7.3174260…`, by more than `0.000573`.

The measure is 355 rectangles with uniform density (no point masses), total mass
`4999999/100000 = 49.99999 < 50`, in the same geometric setting as the rectangle
certificates in this repository (core side `B = 9977/10000`, 201 half-angle net nodes
with step `83/40000`). It is **not** in tokoharu's certificate format: every net angle
was proved with coverage lower bound `>= 1` (minimum `1.0000019…`), below the
`1.0001` that tokoharu's `verify.cpp` requires. It was therefore checked with a
separate verifier, `code/mixed_rotated_verify.cpp`, a research copy of that verifier
which proves coverage `>= 1` directly over every centre domain.

## Argument

D4 symmetry reduces orientations to `[0, π/4]`. The net has 201 nodes, and
`B(1 + 83/40000) < 1`, so every unit square at any orientation contains, strictly in its
interior, a closed square of side `B` at a net angle. For every net angle and every
admissible centre, that core has measure `>= 1`. Cores chosen inside the 50 squares of a
packing are pairwise disjoint, including their boundaries, so the total mass would be
`>= 50`, contradicting `49.99999 < 50`.

## Files

- `candidate.json`: the rational measure (`L`, `B`, the 355 rectangles and their weights).
- `certificate.json`: the result of the full replay: axis table and all 200 oblique angles.
- `manifest.json`: the angle net and the verifier's SHA-256.
- `code/`: the checker (Python 3 with NumPy, and a C++17 compiler).
- `n50-L7.318-proof-bundle.tar.gz`: the complete bundle, 621 files including every
  angle's input and result
  (SHA-256 `239e4ac5c4b756811708ca78140394d1c4d99d56b066b9fd2eafb90f239b06bd`).

## Reproduce

```sh
tar xzf n50-L7.318-proof-bundle.tar.gz
cd n50-L7.318-proof-bundle
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 code/verify_mixed_full_proof.py proof --workers 3
```

The checker regenerates every input from the rational candidate. It then checks the
symmetry, the angle-net containment and the budget. It rechecks the axis case with
integer tables (3,204,100 cells, an implementation independent of the one that produced
the tables) and re-executes the 200 oblique centre-domain proofs.

The oblique replay uses the same outward-rounded algorithm; it is not an independent
second implementation, and nothing here is a proof-assistant formalization. The full
replay was run twice, once where the certificate was produced and once from this
tarball before publication, and both ended with `ALL_ANGLES_VERIFIED_AND_REPLAYED`.

## Provenance

This certificate comes from our L = 7.33 rectangle candidate for `n = 50` (built with the
solver in `tokoharu/square-packing-density-bounds`), shrunk exactly and rescaled to the
budget.
