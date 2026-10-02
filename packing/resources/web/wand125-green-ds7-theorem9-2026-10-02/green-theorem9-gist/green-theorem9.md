# Green's bound for s(k² + 1): the unavoidable set in DS7 Figure 34 is not unavoidable

*wand125, 2026-10-02.* Here `s(N)` is the side of the smallest square holding `N` unit squares (rotations allowed, disjoint interiors).

## Summary

Friedman's survey DS7 states Green's lower bound for `N = k² + 1` (Theorem 9) and cites only a private communication; no proof has been published. For `n = 17` (k = 4), DS7's Figure 34 shows 16 points with a triangulation and presents them as an unavoidable set: every unit square in a container of side `G_4` would contain one of them. **That is false**: we give a unit square in that container which contains none of the 16 points, checked in exact rational arithmetic. We reconstruct the same configuration for every `k`. It reproduces Green's value exactly, and it fails in the same way for every `k ≥ 4`. So, as far as we know, Theorem 9 is not established for `k ≥ 4`.

This is not a counterexample to the theorem. Green may have had a different argument, and the bound may well be true.

**Interactive page** (English / Japanese): the argument and the gap with figures, and a view where you pick k = 2…60 to see the configuration and the empty square, with the clearance computed live: https://claude.ai/artifact/An5pCnG21oPi136aSUP3Rj

## 1. What is published

E. Friedman, [*Packing Unit Squares in Squares: A Survey and New Results*](https://www.combinatorics.org/files/Surveys/ds7/ds7v5-2009/ds7-2009.html), Electron. J. Combin. Dynamic Survey DS7 (2009), contains three relevant items.

- **[Theorem 9](https://www.combinatorics.org/files/Surveys/ds7/ds7v5-2009/ds7-2009.html#lowerbounds)** (Section 5): `s(k² + 1) ≥ G_k = 2√2 − 1 + (k(k − 1)² + (k − 1)√(2k)) / (k² + 1)`. The attribution is "T. Green, 2000, private communication", and no proof is given.
- **[Figure 34](https://www.combinatorics.org/files/Surveys/ds7/ds7v5-2009/ds7-2009.html#figure34):** 16 points for `n = 17`, drawn with a triangulation, and the note `s(17) ≥ (40√2 + 19)/17`, which equals `G_4`. DS7 introduces it with the sentence "Unavoidable sets illustrating some of the lower bounds on s(n) are shown in Figure 34."
- **[Lemma 3](https://www.combinatorics.org/files/Surveys/ds7/ds7v5-2009/ds7-2009.html#technicallemmas)** (Section 4): if the centre of a unit square lies in a triangle whose sides all have length at most 1, the square contains a vertex of the triangle. DS7 uses this lemma for other lower bounds.

![DS7 Figure 34, left panel](https://gist.githubusercontent.com/wand125/9e5f27e25607c0966c4f91bc1253ce8b/raw/ds7-fig34-L17.svg)

*DS7, Figure 34 (left panel), reproduced for comment from Friedman (2009). The 16 points and their triangulation for `s(17) ≥ (40√2 + 19)/17`.*

| k | N = k² + 1 | G_k |
|---:|---:|---:|
| 4 | 17 | 4.445208 |
| 5 | 26 | 5.391854 |
| 6 | 37 | 6.350603 |
| 7 | 50 | 7.317426 |
| 8 | 65 | 8.289966 |
| 9 | 82 | 9.266734 |
| 10 | 101 | 10.246736 |

## 2. The reconstructed argument

**The counting step.** Place `k²` points in a container of side `L < G_k` so that every unit square in the container has a point in its interior. Packed squares have disjoint interiors, so each point lies in at most one of them. Hence at most `k²` squares fit, and `k² + 1` do not.

**The covering step.** Triangulate the points. If every edge has length at most 1, Lemma 3 shows that every unit square whose centre lies inside the triangulation contains a point. The margins at the walls handle the remaining squares.

**The point set.** Put `k` rows of points at heights `y = m_y + j·t` for `j = 0, …, k − 1`. Measured from `m_x`:
- even rows have points at `x = 0, u, u + 1, …, u + k − 2`;
- odd rows have points at `x = 0, 1, …, k − 2, u + k − 2`.

The parameters are

```
t² + u² = 1,   k·t − u = k − 1,   m_x = √2 − t/2,   m_y = √2 − 1/2,
t = (k(k − 1) + √(2k)) / (k² + 1),   u = (k√(2k) − (k − 1)) / (k² + 1).
```

With these choices the width `2m_x + u + k − 2` equals the height `2m_y + (k − 1)t`, and both equal `G_k` exactly. For `k = 4` the 16 points and the triangulation match Figure 34, up to the reflection `y ↦ G_4 − y` (Figure 34 draws the odd-row pattern at the bottom). The `√(2k)` in Green's formula is the `√(2k)` in `u`. This is how we infer that the configuration is the one behind Theorem 9.

MacIver's manuscript on `s(17)` (2026-09-07) uses the same configuration for `k = 4`. It also observes the empty squares described below, and it repairs that case with a defect-counting argument. To our knowledge, no repair for general `k` exists.

## 3. Why it fails for k ≥ 4

Between adjacent rows, the triangulation has edges of two kinds:

```
(u, t):       length √(u² + t²) = 1
(1 − u, t):   length d = √((1 − u)² + t²) = √(2 − 2u)
```

Lemma 3 needs `d ≤ 1`, that is `u ≥ 1/2`. But `u ≈ √(2/k)` decreases with `k`:

| k | u | t | d = √(2 − 2u) | slack (d − 1)/2 |
|---:|---:|---:|---:|---:|
| 2 | 0.60000 | 0.80000 | 0.89443 | − |
| 3 | 0.53485 | 0.84495 | 0.96452 | − |
| 4 | 0.48904 | 0.87226 | **1.01090** | 0.00545 |
| 5 | 0.45428 | 0.89086 | 1.04472 | 0.02236 |
| 6 | 0.42661 | 0.90444 | 1.07088 | 0.03544 |
| 7 | 0.40383 | 0.91483 | 1.09194 | 0.04597 |
| 8 | 0.38462 | 0.92308 | 1.10940 | 0.05470 |
| 9 | 0.36809 | 0.92979 | 1.12419 | 0.06210 |
| 10 | 0.35368 | 0.93537 | 1.13695 | 0.06847 |

For `k = 2, 3` every edge has length at most 1, and the argument works. From `k = 4` on, `(k − 1)(k − 2)` edges are longer than 1, and Lemma 3 does not apply to their triangles. The cause is a shortage of points. A triangulation with all edges at most 1 needs at least `2/√3 ≈ 1.155` points per unit area, while `k²` points in a square of side about `k` give about 1. With only `k` rows to fill a height of about `k`, the row spacing `t` must approach 1, which forces `u` below 1/2.

**An explicit empty square for every k ≥ 4.** Take the points `A = (u + 1, 0)` and `D = (2, t)` (relative to `(m_x, m_y)`). The edge `AD = (1 − u, t)` is a long edge, of length `d`. Let `z` be its midpoint, and let `Q_k` be the closed unit square centred at `z` with sides parallel to `e = (1 − u, t)/d` and `n = (−t, 1 − u)/d`.

Then `Q_k` lies inside `[0, G_k]²` and contains no point of the configuration. Every point `p` satisfies

```
max(|e·(p − z)|, |n·(p − z)|) − 1/2 ≥ (d − 1)/2 > 0.
```

*Proof sketch.*
- For `k ≥ 4`, `0 < u < 1/2` and `√3/2 < t < 1`.
- In the first two rows, the points nearest to `z` are `A`, `D`, `B = (u + 2, 0)` and `C = (1, t)`. We have `e·(A − z) = −d/2` and `e·(D − z) = d/2`, while `n·(B − z) = −t/d` and `n·(C − z) = t/d`, with `t/d = √((1 + u)/2) ≥ d/2`. Every other point of the first two rows lies further out along `e` or `n`.
- Points in rows `j ≥ 2` are at height at least `3t/2` from `z`, so their L∞ distance in the rotated frame is at least `3t/(2√2) > √2/2 ≥ d/2`.
- The half-width of `Q_k` along each axis is at most `√2/2`, and the distances from `z` to the four walls all exceed that, so `Q_k` lies inside the container.

**Exact checks.** We checked an empty square with exact rational interval arithmetic for `k = 4, 5, 6, 7, 8, 9, 10, 12, 15, 20`. For example, at `k = 4` (in the coordinates above) the square with centre `(29638179/10⁷, 302261/250000)` and `tan(θ/2) = 179111/312500` (θ ≈ 59.64°) lies in the container and is at L∞ distance at least `1/2 + 0.00545` from all 16 points. For `k = 18` everything is rational: `t = 24/25`, `u = 7/25`, `d = 6/5`, and the slack is exactly `1/10`.

| Figure 1 (k = 4) | Figure 2 (k = 10, close-up) |
|---|---|
| ![k = 4](https://gist.githubusercontent.com/wand125/9e5f27e25607c0966c4f91bc1253ce8b/raw/fig1-k4.svg) | ![k = 10](https://gist.githubusercontent.com/wand125/9e5f27e25607c0966c4f91bc1253ce8b/raw/fig2-k10-zoom.svg) |

*Figure 1:* the 16 points in `[0, G_4]²`. The red edges are the 6 edges of length `d ≈ 1.0109`, and the dashed square is an empty unit square.
*Figure 2:* `k = 10` near the edge `AD` (`d ≈ 1.1370`). The dashed square `Q_10` contains no point; its slack is `0.0685`.

## 4. What this does and does not show

- **Shown:** the 16 points of DS7's Figure 34 are not an unavoidable set for `n = 17`, contrary to what DS7 states. The same configuration fails for every `k ≥ 4`. So the argument that the published material suggests is not a proof for any `k ≥ 4`, because the counting step does not apply.
- **Not shown:** that Theorem 9 is false. We know no packing of `k² + 1` squares in a smaller square than `G_k`. Green may have had a different argument, but nothing of it has been published.
- **A points-only repair is limited.** If the rows are re-spaced so that every edge is at most 1, the same method only gives `s(k² + 1) ≥ L′_k` with `L′_k ≈ 0.894k`. That is below the area bound `√(k² + 1)` for `k ≥ 9`.

## 5. Published lower bounds above G_k (2026-10-02)

Only published certificates are listed.

| k | N | G_k | published lower bound above G_k |
|---:|---:|---:|---|
| 2, 3 | 5, 10 | — | `s(5)` and `s(10)` are known; the argument works |
| 4 | 17 | 4.4452 | 4.66044 (Guzhou0806, [R068](https://github.com/Guzhou0806/n17-square-packing/blob/main/R068_PUBLICATION.json)) |
| 5 | 26 | 5.3919 | 5.5325 ([`rect_n26_L55325`](https://github.com/wand125/square-packing-bounds/tree/main/certificates/rect_n26_L55325)) |
| 6 | 37 | 6.3506 | 6.44 ([`mixed_n37_L644`](https://github.com/wand125/square-packing-bounds/tree/main/certificates/mixed_n37_L644)) |
| 7 | 50 | 7.3174 | 7.40 ([`mixed_n50_L740`](https://github.com/wand125/square-packing-bounds/tree/main/certificates/mixed_n50_L740)) |
| 8 | 65 | 8.2900 | 8.35 ([`mixed_n65_L835`](https://github.com/wand125/square-packing-bounds/tree/main/certificates/mixed_n65_L835)) |
| 9 | 82 | 9.2667 | 9.32 ([`mixed_n82_L932`](https://github.com/wand125/square-packing-bounds/tree/main/certificates/mixed_n82_L932)) |
| 10 | 101 | 10.2467 | 10.28 ([`mixed_n101_L1028`](https://github.com/wand125/square-packing-bounds/tree/main/certificates/mixed_n101_L1028)) |
| 11–60 | | | none known; `G_k` is unproved |
| ≥ 61 | | | `√(k² + 1) > G_k`, so the area bound suffices |

## 6. A typo in DS7 Table 2

For `n = 82–85`, [Table 2](https://www.combinatorics.org/files/Surveys/ds7/ds7v5-2009/ds7-2009.html#appendix) (in the Appendix) gives `2√2 + (288 + 12√3)/41`. Substituting `k = 9` into Theorem 9 gives instead `2√2 + (247 + 12√2)/41 = 9.2667335…`. The printed form swaps `√2` for `√3` and drops a `−1`.

## References

- E. Friedman, *Packing Unit Squares in Squares: A Survey and New Results*, Electron. J. Combin. DS7 (2009), Theorem 9, Lemma 3, Figure 34 (image `pic/L17.gif`), Table 2. https://www.combinatorics.org/files/Surveys/ds7/ds7v5-2009/ds7-2009.html
- MacIver, manuscript on a lower bound for 17 unit squares (2026-09-07), Section 3.
- wand125/square-packing-bounds (certificates). https://github.com/wand125/square-packing-bounds
