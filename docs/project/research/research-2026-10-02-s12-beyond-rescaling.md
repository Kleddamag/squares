# Research: s(12) Beyond Rescaling

**Date:** 2026-10-02

**Author:** Lane BB of the 2 October result work, for the squares project

**Status:** Complete.
One candidate result, $s(12) \ge 15680000/3949423 = 3.9702002\ldots$, verified over the
whole angle range by the producer’s verifier; this project’s own checker decided a
sample of its rows. The register entry is the records lane’s to make.

## Overview

Evan Daniel’s weighted certificate proves $s(12) \ge 15680/3951 = 3.9686155\ldots$
(T-049). In jlevy/squares#309 squarepacker scaled the same certificate, weights
unchanged, by $7902/7901$, to $31360/7901 = 3.9691178\ldots$, and found that it verifies
at the angle net $N = 24000$ but not at $6000$ or $12000$.

This lane took both steps further.

- **Route A, the same certificate scaled further:** $s(12) \ge 1568000/395039 =
  3.9692284\ldots$, verified at $N = 96000$. This is #309’s method with a finer net and
  a search for the largest scale, and it is credited to squarepacker’s rescaling and
  Daniel’s certificate.
- **Route B, the same points re-weighted:** $s(12) \ge 15680000/3949423 =
  3.9702002\ldots$, verified at $N = 96000$. Daniel’s 1,736 points, scaled by
  $3951000/3949423$, carry new weights solved here by linear programming, of total
  $14970347/1250000 = 11.9762776 < 12$. It exceeds #309’s bound by about $0.00108$ and
  Daniel’s by about $0.00158$.

Route B is the candidate result.
The re-weighting is this project’s own step; the geometry is Daniel’s.

## How the Verifier Decides a Certificate

A certificate is points $p_i$ with weights $w_i \ge 0$, and it asserts that every closed
unit square in $[0, s]^2$, at every angle, captures weight at least 1. With
$\sum w_i < 12$ that rules out twelve unit squares in any smaller container, by the
scaling argument of Daniel’s `certificates/FORMAT.md`.

Daniel’s verifier (`s12/verify/` in the
[retained packet](../../../packing/resources/web/evand-square-packing-2026-09-26/README.md))
splits the angles $[0°, 45°]$ into bins $[\theta_k, \theta_{k+1}]$ with
$\theta_k = 2\arctan(k/N)$, so every rotation is rational.
A unit square at any angle in a bin contains the concentric square of side
$\sigma_k = 1/(\cos\delta + \sin\delta)$ at angle $\theta_k$, where $\delta$ is the
bin’s width; $\sigma_k$ is rounded down to a multiple of $10^{-6}$. For each bin an
exact `i128` arrangement sweep then finds the least captured weight of that smaller
square over every centre at which some square of the bin fits.
So between net angles the verifier proves coverage for a slightly smaller square, and
the cost is $1 - \sigma_k \approx \delta \approx 2/N$ of the square’s side:
$3.3 \times 10^{-4}$ at $N = 6000$ and $2.1 \times 10^{-5}$ at $N = 96000$.

That is why #309’s scale fails at coarse nets and passes at $24000$: the scale shrinks
every square relative to the points by $1.3 \times 10^{-4}$, and only a net finer than
about $15000$ leaves that much of the shrink unspent.

## Route A: Scaling Further

[`devtools.s12_angle_net_rescale`](../../../packing/devtools/s12_angle_net_rescale.py)
copies the retained `verify/` crate, builds it as shipped and with `overflow-checks` on,
writes Daniel’s file with coordinates multiplied by $m$ over a new denominator $D'$, and
runs the verifier over every bin or, as a screen that can only refuse, over every $k$-th
bin.

With $m = 1000$, screens at $N = 96000$ refused $D' = 3950378$ and passed $3950381$. The
scale therefore stops near $s = 3.96923$. Finer nets buy little beyond that, because the
failures there are steps, not erosion: at $D' = 3950350$ a square near $19.8°$ loses a
point outright at $N = 192000$ as well, capturing $0.990$.

The complete sweep at $D' = 3950390$, $N = 96000$, took 812 seconds on four threads and
returned `VERIFIED` with least captured weight $10000056/10^7$ at bin 0
([receipt](../../../packing/cases/n12_beyond_rescaling/receipts/route-a-source-verifier.json)).

**Why the least weight does not change with the scale.** The same $10000056/10^7$ is the
least weight of Daniel’s original file at $N = 6000$ and of #309’s at $N = 24000$. In
all three it is attained in bin 0, by an axis-parallel unit square in the corner,
centred near $(0.54, 0.60)$, that captures the same 58 points.
They lie on the two inner edges of the corner square, between $x$ or $y = 0.53$ and $1$.
The verifier’s dump of bin 0 lists 52 cells at this value, in four distinct member sets,
for each of the three files.
The captured weight is a sum over a fixed set of points, so it does not move as the
scale grows; it changes only when a point crosses a square’s edge, and then by that
point’s whole weight.
The margin a scale consumes is geometric slack, which the weight margin does not show.

## Route B: Re-Weighting

[`devtools.s12_reweight`](../../../packing/devtools/s12_reweight.py) keeps the scaled
points and solves for new weights.
There is one variable per D4 orbit of points, and one row per placement the source
verifier reports as near-tight.
The objective is the least total weight with every row capturing at least
$1 + 2 \times 10^{-6}$.

- **Rows** come from the verifier’s `TIGHT_DUMP` diagnostic, which lists each
  arrangement cell whose captured weight is at most a threshold, as an interval of
  centres in the bin’s frame.
  The set of points a cell’s squares contain is constant on the open cell, so the tool
  decides membership exactly, in integers, at the cell’s midpoint.
  Each round dumps every 96th bin, with the offset rotating between rounds.
- **Weights** come from HiGHS in floating point and are rounded *up* to numerators over
  $10^7$, which can only raise a captured weight.
  The total is computed exactly.

The runs
([round log](../../../packing/cases/n12_beyond_rescaling/receipts/reweight-rounds.jsonl)):

| Container | Rounds | Rows | LP total |
| --- | ---: | ---: | ---: |
| $3.9696$ ($D' = 3950020$) | 17 | 6,391 | 11.97143 |
| $3.9702$ ($D' = 3949423$) | 16 | 8,660 | 11.97618 |
| $3.9702$, focus on six failing bins | 3 | 8,745 | 11.97628 |

The first complete sweep of the $3.9702$ weights refused them at six bins (14704 and
20574 to 20578, least $0.99787$;
[receipt](../../../packing/cases/n12_beyond_rescaling/receipts/route-b-first-pass-refused.json)).
Three rounds that swept those bins every time fixed them.
The second complete sweep, with the overflow-checked build, returned `VERIFIED`: least
captured weight $10000045/10^7$ at bin 0, 39,765 bins, 802 seconds on four threads
([receipt](../../../packing/cases/n12_beyond_rescaling/receipts/route-b-source-verifier.json)).

The LP total rises by about $0.008$ per $0.001$ of container side over this range, and
it is $0.024$ below 12 at $3.9702$. This point set may carry the bound further.
Daniel reports that column generation stops getting below 12 near $3.9696$ at
$N = 6000$, whose net costs about $3.3 \times 10^{-4}$ of side, an effective $3.9709$.
The cap of this lane ended the search; how far the 1,736 points carry is open.

## Verification Receipts

The certificate is
[`certificate.txt.gz`](../../../packing/cases/n12_beyond_rescaling/certificate.txt.gz)
(SHA-256 `6823e8e8…`, decompressed), with its claim in
[`claim.json`](../../../packing/cases/n12_beyond_rescaling/claim.json).

| Check | Whose code | Scope | Outcome |
| --- | --- | --- | --- |
| Arrangement sweep, `s12/verify` at `167d842c`, built with overflow checks | the producer’s (Daniel’s) | all 39,765 bins, $N = 96000$ | `VERIFIED`, least $10000045/10^7$ |
| Parent-core interval branch and bound, `devtools.verify_evand_angle_net_native` | first-party | 1,034 of 39,765 rows: every 40th, the six formerly failing bins with neighbours, the last row | `PASS_PARTIAL`: every selected row certified, none refuted ([receipt](../../../packing/cases/n12_beyond_rescaling/receipts/native-sample.json)) |
| Well-formedness, D4 orbits, total, geometry equal to Daniel’s points scaled | first-party, `tests/test_s12_angle_net_rescale.py` | whole file | pass |

The first-party checker decides the same row structure as the producer’s sweep but
shares none of its code: an exact premise check and a directed-rounding branch and bound
over centre boxes. The sample took 365 row-CPU-seconds, about 0.35 a row, so a complete
run at $N = 96000$ would take about four CPU-hours, which was beyond this lane’s cap.
It is the next step that would make the confirmation method-distinct.

## Controls

Both mutations must be refused, and both were
([receipt](../../../packing/cases/n12_beyond_rescaling/receipts/controls.json)).

1. **Lowered orbit.** One point of the binding corner square, with its D4 images, loses
   $100/10^7$ of weight.
   The set stays symmetric and its total falls, so only coverage can refuse it.
   The source verifier gives bin 0 a least weight of $9999845/10^7$, and the native
   checker refutes row 0 with an exact witness.
2. **One step larger.** The same integers and weights over $D' = 3949000$, container
   $15680/3949 = 3.9706255$. A stride-64 screen finds 128 of 622 bins below 1, least
   $0.9764$ at bin 7808, and the native checker refutes row 7808 with an exact witness,
   charge $1958699/2000000$.

## Cost

About 6.5 CPU-hours on a four-core container, against a cap of 8. Screens took about
0.6, the two Route A sweeps about 1.1, the re-weighting rounds about 2.3, the two
complete Route B sweeps 1.8, and the native sample and controls about 0.7.

## Attribution

The result is Levy’s, by this project’s re-weighting.
It builds on Evan Daniel’s certificate `s12_lower_3.9686.txt` (T-049), whose 1,736
points it uses unchanged up to scale, and on squarepacker’s rescaling in
jlevy/squares#309, whose method Route A continues.
Daniel’s verifier, built unmodified from the retained source, is the check that decides
it.

## References

- [T-049 source packet](../../../packing/resources/web/evand-square-packing-2026-09-26/README.md)
  and its [review](../reviews/review-2026-09-27-evand-s32-s12.md)
- [The case directory](../../../packing/cases/n12_beyond_rescaling/__init__.py), with
  the two certificates, claim and receipts
- [`devtools.s12_angle_net_rescale`](../../../packing/devtools/s12_angle_net_rescale.py),
  [`devtools.s12_reweight`](../../../packing/devtools/s12_reweight.py) and
  [`devtools.verify_evand_angle_net_native`](../../../packing/devtools/verify_evand_angle_net_native.py)

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
