# wand125 Rectangle Ceiling: Resolution of T-058

The 29 September review left `T-058` with two unresolved premises and an admission
defect. The source claims that a rectangle-density certificate with core side
$B=9977/10000$ cannot have mass below $n$ at any side $L\ge B\cdot UB(n)$, for its table
of upper bounds $UB(n)$, $n=1,\dots,100$.

All three findings are now settled.
The ceiling is proved in a corrected form, and exactly for every $n$ in the table.
The source’s own $B\cdot UB(n)$ is proved at the 64 table rows whose upper bound is an
integer grid. It is unproved, though not refuted, at the other 36. The corrected rule of
the source’s update `3eb08e6` is proved at all 100 rows: $B$ for an integer-grid row,
$\alpha=B(1+D)$ for every other row, applied to the table’s rounded value.
The false `s(1) >= 1.5` input is refused by this repository’s admission path, and tests
now pin exactly why.

This review was written on 2026-10-02 by Claude as lane DD of the result work
(`think-xgjo`). It registers nothing new and moves no bound.

## Scope and Evidence

Read in full: `T-058` and `E-wand125-tools-ceiling-report`; the
[tools review](review-2026-09-29-wand125-tools-mathematics.md); the packet
[README](../../../packing/resources/web/wand125-tools-2026-09-29/README.md); and, from
the retained archives, `transfer/l_cap.py` and `transfer/data/ub.json` at both pins
(`0d33ab6` and `3eb08e6`), plus the angle loop of `solver/verify.cpp`. Also read: the
[density mathematics review](review-2026-09-22-tokoharu-density-mathematics.md) and the
[native contract](review-2026-09-29-native-rectangle-contract.md), which define the
coverage predicate and its legal centre domain, and `parse_candidate` in
[`sqpack.rectangle_density`](../../../packing/src/sqpack/rectangle_density.py).

Built and run here, from `packing/`:

- [`sqpack.rectangle_ceiling`](../../../packing/src/sqpack/rectangle_ceiling.py), an
  exact verifier for ceiling certificates, and `premise_checks`, which decides each
  numeric premise of the general argument in rational arithmetic;
- [`devtools.certify_rectangle_ceiling`](../../../packing/devtools/certify_rectangle_ceiling.py),
  which builds and verifies one ceiling certificate per $n$ and compares it with the
  source table read from the retained archive;
- [`tests/test_rectangle_ceiling.py`](../../../packing/tests/test_rectangle_ceiling.py),
  16 tests, covering the verifier, the receipts and the admission refusals.

The
[receipt](../../../packing/resources/web/wand125-tools-2026-09-29/receipts/ceiling-certificates-2026-10-02.json)
holds one row per $n$. The
[certificates](../../../packing/resources/web/wand125-tools-2026-09-29/receipts/ceiling-certificates-2026-10-02.json.gz)
hold every core’s exact centre and net index.
`python -m devtools.certify_rectangle_ceiling --check` reverifies every retained
certificate. It then recomputes both files and requires byte equality.

## The Coverage Predicate

The net is the 201 directions $(\cos\theta_r,\sin\theta_r)=((1-t^2),2t)/(1+t^2)$, with
$t=rD$, $D=83/40000$ and $r=0,\dots,200$. Each direction is an exact rational unit
vector. A certificate is a nonnegative rectangle density $g$ on $[0,L]^2$ of mass $M$.
The input format makes it D4-invariant: each weight is spread over its eight images.
The certificate is checked so that every closed side-$B$ square at a net direction,
lying inside $[0,L]^2$, captures at least the threshold, which is at least one.

D4 invariance extends the predicate to the reflected directions $-\theta_r$ and to
quarter turns. Both reviews named above establish that the checked centre domain is the
whole legal domain, where $h=B(\cos\theta+\sin\theta)/2$:

$$
[h,\,L-h]^2.
$$

The lower-bound argument uses the predicate in exactly this form.
The ceiling below uses nothing else.

## The Corrected Ceiling

**Lemma.** Suppose $[0,L]^2$ contains $n$ side-$B$ squares at net directions, or their
reflections, with pairwise disjoint interiors.
Then no certificate at any side $L'\ge L$ has $M<n$.

The squares lie in $[0,L']^2$, so each captures at least one.
Since $g$ is a bounded density, their boundaries carry no mass, so
$M\ge\int_{\cup Q_i}g\ge n$.

Call such a set of squares a *ceiling certificate*. It is a finite object with rational
data, so containment and disjointness are decidable exactly.
That is what `verify_ceiling` decides, by the separating-axis test on the four edge
normals, in `Fraction` arithmetic.

**Theorem.** Let a packing of $n$ unit squares in a square of side $U$ have orientations
$\varphi_i$. Let $\delta_i$ be the distance from $\varphi_i$ to the nearest direction of
the net’s D4 orbit. Then no certificate at side

$$
L\ \ge\ U\cdot B\cdot\max_i(\cos\delta_i+\sin\delta_i)
$$

has $M<n$. In particular, the bound is $L\ge B\cdot U$ when every orientation lies in
the orbit. For every packing it is $L\ge\alpha U$, where

$$
\alpha=B(1+D)=\frac{399908091}{400000000}.
$$

*Proof.* Scale the packing’s centres about the container centre by
$\lambda=B\max_i(\cos\delta_i+\sin\delta_i)$. The squares of side $\lambda$ are then
interior-disjoint and inside $[0,\lambda U]^2$. In each, place the concentric side-$B$
core at the nearest orbit direction.

A core turned by $|\delta|\le\pi/4$ fits in the concentric square of side
$B(\cos\delta+\sin\delta)\le\lambda$. Apply the lemma.

For the general bound, $\theta_0=0$, and consecutive half-angles differ by
$\arctan(D/(1+r(r+1)D^2))\le\arctan D$. Also $\tan(\theta_{200}/2)=0.415$ exceeds
$\tan(\pi/8)$, so every orientation is within $\arctan D$ of the orbit.
With $t=\tan|\delta|\le D$,

$$
\cos\delta+\sin\delta=\frac{1+t}{\sqrt{1+t^2}}\le\frac{1+D}{\sqrt{1+D^2}}<1+D.
$$

$\square$

The same scaling argument already caps the fractional point certificate, in
[X-014](../../../packing/campaign/explorations/X-014-closing-from-both-ends.md) and the
`cap` column of
[`CERTIFICATE-REACH.md`](../../../packing/frontier/CERTIFICATE-REACH.md).
What is new here is the rectangle form and an exact certificate for each case.

The sharp worst-case factor is $(1+D)/\sqrt{1+D^2}\approx1.0020728$, slightly below
$1+D=1.002075$. `premise_checks` decides each numeric premise exactly:

- the value of $\alpha$;
- that the net reaches $45^\circ$, which is $t_{200}^2+2t_{200}-1\ge0$;
- that every half-gap tangent is at most $D$;
- that the sharp factor is below $1+D$;
- that $\alpha<1$;
- that every net direction is a unit vector.

**The per-case certificates.** `place_cores` takes each repository known-best witness,
whatever its own assurance, and uses it only as a guide.

It gives each square its nearest orbit direction and scales the centres.
Then `verify_ceiling` must accept the exact result.
The ceiling of $n$ is the smaller of that side and the side $B\lceil\sqrt n\rceil$ of
the exactly verified grid certificate.

Every placement verified with zero added slack.
The witness numbers enter only as rational core centres, and nothing in the proof
depends on their accuracy.
Over the 36 rotated witnesses, the worst factor is $1.0019069$, at $n=68$. The single
$45^\circ$ squares of $n=5$, 10 and 26 cost $1.0013413$, because $45^\circ$ is not a net
direction.

## Findings and Verdicts

| Finding (29 September) | Verdict | What is now proved, and what is not |
| --- | --- | --- |
| **The ceiling lacks a net-orientation premise** | Confirmed and resolved | With the premise, $B\cdot U$ is proved. Without it, $U\cdot B\max(\cos\delta_i+\sin\delta_i)\le\alpha U$ is proved. The 64 grid rows meet the premise, and $B\cdot UB(n)$ holds there. The 36 non-grid rows have witnesses off the net, and $B\cdot UB(n)$ is not proved for them. Their proved ceilings exceed it by $3.6\times10^{-3}$ to $1.7\times10^{-2}$. No refutation exists either: one would need a certificate with $M<n$ between the two values. |
| **The table’s rounded floats are not certified upper bounds** | Confirmed and made moot | The proved ceilings never use the table: each is an exact rational from cores verified exactly. Read as exact decimals, the table still errs where the review said. For example, $5.62132$ is below $7/2+(3/2)\sqrt2$, which a test decides exactly. The ceilings still lie at or below the 3eb08e6 value $\mathrm{factor}\cdot UB(n)$ at all 100 rows, with a smallest margin of $1.08\times10^{-3}$, at $n=17$. |
| **The admission defect: coverage was accepted without the mass budget** | Confirmed for the 0d33ab6 wrapper. This repository refuses the input. | See below |

In operational terms, the source’s `L_cap` is the last thousandth a certificate is said
to reach, so the source claims impossibility from the next thousandth on.
That claim is proved at the 64 grid rows for `0d33ab6`, and at all 100 rows for
`3eb08e6`. At $n=5$, for example:

- `0d33ab6` gives `L_cap` $=2.700$, while the proved ceiling is $2.7045030\ldots$;
- `3eb08e6` gives $2.706$, and the proved ceiling lies below $2.707$.

## Admission: What Must Be Refused

The unchanged `0d33ab6` wrapper `scale_and_verify.py` rescaled a valid coverage density
to mass $289/10$. It then let `verify.cpp` pass all 201 directions, and printed
`certificate for s(1) >= 1.5`. Coverage was genuine, and the bound is false because
$s(1)=1$. Coverage proves nothing about a packing until it is paired with a budget for
the announced count.

Admission must refuse an input in each of the following cases:

1. The announced count $n$ is not a positive integer, or differs from a count the
   candidate declares.
2. The exact mass, recomputed from the admitted weight strings, does not lie strictly
   between $0$ and $n$. Any declared total is ignored.
3. The admitted side and core side are not the ones the announced bound states.
   The core side must also satisfy the angular margin.
4. Any weight is negative, or any positive rectangle lies outside the safe interior.
5. The net metadata differs from the checked net.

After admission, a bound is announced only on complete coverage of all 201 directions,
by a checker bound to its source.
A zero exit or a `VERIFIED` label is not enough on its own.

`parse_candidate` enforces items 1 to 5 before any coverage work.
`verify_candidate` re-enforces the mass and count checks on directly constructed
candidates.

The new tests show the following:

- The retained false input is refused on the budget, with the message
  `strictly between zero and n`.
- A declared total of $0.5$ does not rescue it.
- Masses $1$ and $289/10$ at $n=1$ are both refused.
- The same density at mass $1/2$ is admitted.
  The budget is therefore the input’s only admission defect.
- An announced $n=29$, or a different side, is refused for a mismatched count or side.

The 3eb08e6 wrapper refuses a target mass outside $(0,n)$. That fix is upstream’s, and
its retained control already shows it.

## What Remains

The proved ceiling is sufficient, not sharp.
The following remain open:

- whether any certificate with $M<n$ exists between $B\cdot UB(n)$ and the proved
  ceiling, at the 36 non-grid rows;
- smaller ceilings from better core placements;
- rows beyond the table.

None of these affects a lower bound.
The ceiling is a search limit, so `l_cap` may now cite this receipt in place of a
heuristic. Scaling another verified packing gives a ceiling for it, through the same
tool.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
