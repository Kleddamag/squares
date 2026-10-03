# Green’s DS7 Theorem 9: Review of the Report That Its Unavoidable Set Fails

Friedman’s survey DS7 states Trevor Green’s Theorem 9,
$s(k^2+1) \ge G_k = 2\sqrt2 - 1 + \bigl(k(k-1)^2 + (k-1)\sqrt{2k}\bigr)/(k^2+1)$, from a
private communication of 2000, with no proof; the only argument it publishes is Figure
34, sixteen points it calls unavoidable at side $G_4$ for $n = 17$. wand125 reports in
[jlevy/squares#308](https://github.com/jlevy/squares/issues/308) that those points are
not unavoidable, that the pattern reconstructed for every $k$ reproduces $G_k$ and fails
the same way for every $k \ge 4$, and that this is not a counterexample to the bound.

**In one line:** the report is right for every $k$ from 4 to 17, checked here in exact
arithmetic, and wrong in one aside: at $k = 2$ the pattern fails too, at the side walls.
The published material proves Theorem 9 for no $k \ge 4$. No verified bound in this
record rests on it, so no bound moves; the evidence entry is marked `defect-found`.

This is the review of stage 4 of the
[result import](../../../packing/campaign/result-import.md) for #308, written by the
import’s lane T on 2026-10-02 with a tool built for it,
[`devtools.check_green_ds7`](../../../packing/devtools/check_green_ds7.py).
It registers nothing.

## Scope and Evidence

| Field | Value |
| --- | --- |
| Source | wand125’s gist [`9e5f27e2`](https://gist.github.com/wand125/9e5f27e25607c0966c4f91bc1253ce8b) at `9d6de784`, 2026-10-02T12:35:13Z, retained whole in the [packet](../../../packing/resources/web/wand125-green-ds7-theorem9-2026-10-02/README.md) |
| Entries | `E-green-ds7-theorem9-reported-lower` (scope $n = 2…324$, $k = 1…17$) and its $k = 5$ twin `E-green26-reported-lower` |
| Not read | The illustrated claude.ai page the issue links, which cannot be fetched |
| Receipt | [`receipts/check_green_ds7.log`](../../../packing/resources/web/wand125-green-ds7-theorem9-2026-10-02/receipts/check_green_ds7.log) and its JSON, the run for $k = 2…17$ |

Read in full: the write-up and its three figures; DS7 Section 4 (Lemmas 1 to 4) and
Section 5 through Figure 34, from the retained HTML transcription; MacIver’s
[$s(17)$ manuscript](../../../packing/resources/web/maciver-square-packing-2026-09-07/README.md),
Sections 1 to 3; Evan Daniel’s lower-bound notes of 30 September in the
[2 October evand packet](../../../packing/resources/web/evand-square-packing-2026-10-02/README.md);
the two entries; every case record that cites them; `cases/green17`.

## The Argument and Where It Breaks

DS7 Section 5 fixes the convention: a set $P$ is unavoidable in a square $S$ when “any
unit square in $S$ contains an element of $P$ (possibly on its boundary)”, so closed
squares in a closed container; shrinking $P$ then puts a point in the interior of every
unit square at any smaller side, and $k^2$ points unavoidable at $G_k$ give
$s(k^2+1) \ge G_k$. To refute it, one closed unit square inside $[0, G_k]^2$ with every
point strictly outside is enough, and it refutes every open or shrunk variant too when
its clearances are positive.

**The pattern is Green’s.** $k$ rows at heights $m_y + jt$, even rows at offsets
$0, u, u+1, …, u+k-2$ and odd rows at $0, 1, …, k-2, u+k-2$ from $m_x$, with
$t = (k(k-1) + \sqrt{2k})/(k^2+1)$, $u = (k\sqrt{2k} - (k-1))/(k^2+1)$,
$m_x = \sqrt2 - t/2$ and $m_y = \sqrt2 - 1/2$. For every $k$ from 2 to 17 the tool
decides $t^2 + u^2 = 1$, $kt - u = k - 1$, and width $=$ height $= G_k$ as identities
over $\mathbb{Q}(\sqrt2, \sqrt k)$; DS7’s printed specializations at $k = 4, 5, 9$ are
the same numbers. The GIF inside the write-up’s copy of Figure 34 is byte for byte DS7’s
own `pic/L17.gif`, and its sixteen dots sit within 0.90 pixel of the reconstructed
$k = 4$ points at 38.2 pixels per unit; drawn the other way up the worst residual is
19.9 pixels. MacIver’s manuscript gives the same constants for $k = 4$ independently.
That identifies the figure’s set; it cannot show the figure is all of Green’s argument.

**Why it fails.** Between neighbouring rows the mesh has edges $(u, t)$ of length
exactly 1 and edges $(1-u, t)$ of length $d = \sqrt{2 - 2u}$. DS7’s Lemma 3 covers a
triangle only when every side is at most 1, so it needs $u \ge 1/2$; $u$ falls like
$\sqrt{2/k}$ and is below $1/2$ from $k = 4$. The write-up’s square $Q_k$, centred on
the long edge from $(u+1, 0)$ to $(2, t)$ and aligned with it, keeps that edge’s ends at
distance $d/2$ along its axis, outside its half side $1/2$ by $(d - 1)/2$, and the
nearest other points further out.

**$k = 2$ fails at the walls.** There $t = 4/5$ and the side margin
$m_x = \sqrt2 - 2/5 \approx 1.0142$ exceeds 1, so the strip of width one along either
side wall holds no point and an axis-parallel unit square inside it misses all four.
The write-up says the argument works for $k = 2$; it does not.
Theorem 9 at $k = 2$ is still true, since $s(5) = 2 + 1/\sqrt2 > G_2 = 2\sqrt2 - 1/5$.

**$k = 3$ works.** Every edge is at most 1 and $m_x < 1$. The pattern scaled to side
$3518321/10^6$, $4.1 \times 10^{-6}$ below $G_3$, and rounded to the grid of
`cases/green17/interval_audit.py`, is certified unavoidable by that module’s exhaustive
branch-and-bound (697,643 boxes, 306 s; the default run, a thousandth below $G_3$, takes
18,043 boxes).
At $G_3$ itself the walls are tight, Lemma 2 holding with equality, and no
rational branch-and-bound closes a family of width zero.

## What the Tool Decides

Slack is the exact check’s lower bound on how far the nearest point lies outside the
square; the ceiling bounds the largest side at which the pattern, scaled, could be
unavoidable, from a checked empty square grown about its centre.

| $k$ | $n$ | $G_k$ | $d$ | Slack of $Q_k$ | Ceiling below | Verdict |
| ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 2 | 5 | 2.628427 | 0.894 | 0.007107, a wall-strip square | 2.602790 | fails |
| 3 | 10 | 3.518325 | 0.965 | none found | — | unavoidable at $G_3 - 4.1 \cdot 10^{-6}$ |
| 4 | 17 | 4.445208 | 1.011 | 0.005449 | 4.397757 | fails |
| 5 | 26 | 5.391854 | 1.045 | 0.022358 | 5.163282 | fails |
| 6 | 37 | 6.350603 | 1.071 | 0.035439 | 5.934209 | fails |
| 7 | 50 | 7.317426 | 1.092 | 0.045971 | 6.706947 | fails |
| 8 | 65 | 8.289966 | 1.109 | 0.054700 | 7.479850 | fails |
| 9 | 82 | 9.266734 | 1.124 | 0.062097 | 8.252124 | fails |
| 10 | 101 | 10.246736 | 1.137 | 0.068473 | 9.023377 | fails |
| 11 | 122 | 11.229281 | 1.148 | 0.074047 | 9.793428 | fails |
| 12 | 145 | 12.213867 | 1.158 | 0.078977 | 10.562203 | fails |
| 13 | 170 | 13.200123 | 1.167 | 0.083379 | 11.329689 | fails |
| 14 | 197 | 14.187765 | 1.175 | 0.087343 | 12.095906 | fails |
| 15 | 226 | 15.176574 | 1.182 | 0.090937 | 12.860890 | fails |
| 16 | 257 | 16.166376 | 1.188 | 0.094217 | 13.624690 | fails |
| 17 | 290 | 17.157031 | 1.194 | 0.097226 | 14.387355 | fails |

Every slack is $(d - 1)/2$ to nine digits, as the write-up says, and the independent
search, which starts in every region Lemma 3 leaves open, finds no wider empty square at
any $k \ge 4$. The square the write-up publishes for $k = 4$ is empty and fits, slack
$0.0054494$. No rescaling of the pattern proves anything new: from $k = 6$ the ceiling
is below even the area bound $\sqrt{k^2+1}$, and at $k = 4$ and 5 it is below the
verified $116511/25000$ and $553/100$. At $k = 18$, the write-up’s rational case,
$t = 24/25$, $u = 7/25$ and the slack is $1/10$ within the rounding of the square’s
centre; a test holds it.

## The Tool’s Trust Boundary

- **Exact.** Every coordinate is a finite sum of rational multiples of square roots of
  distinct squarefree integers.
  Such roots are linearly independent over $\mathbb{Q}$ (Besicovitch, 1940), so a sum is
  zero exactly when its coefficients are, and a nonzero sign is decided by integer
  square-root enclosures refined until they exclude zero.
  A checked square has a rational rotation from a rational $\tan(\theta/2)$, so its
  frame is exactly unit.
  Fit is decided against $G_k$ itself, not an approximation.
- **Floating point** chooses the square to check: the write-up’s construction, rounded,
  and the search’s best pose.
  A bad choice can only fail to find an empty square.
- **The $k = 3$ certificate** is `cases/green17/interval_audit.py`’s, the instrument
  behind `E-green17-interval-audit`, applied to points rounded within $10^{-18}$; it
  certifies the rounded set, which proves $s(10) \ge 3518321/10^6$ and says the pattern
  works, not that the exact pattern is unavoidable at $G_3$.
- **Controls.** The tests refuse a grown square that catches two points, a square
  outside the container, and squares centred in a $k = 3$ mesh triangle whose sides are
  all at most 1, and refuse to certify the $k = 2$ pattern a thousandth below $G_2$.

## Findings

### G9-1 — Blocking for the entry: the published argument does not prove Theorem 9 for any $k \ge 4$

As above. It is a defect in the source’s argument, not a counterexample: no packing of
$k^2 + 1$ squares below $G_k$ is known, and Green’s unpublished argument may differ.
It blocks any reading of the reported value as resting on a proof, which the entry’s
`limitations` already disclaimed and now explain.

### G9-2 — Medium, in the report: the pattern fails at $k = 2$ as well

The write-up’s table says the argument works for $k = 2$ and 3. It works for $k = 3$
only. The reply should say so; nothing in the record depends on it.

### G9-3 — Low, in the record: the counter-evidence was already retained

MacIver’s manuscript, retained here since 7 September, says that at side $G_4$ Green’s
scaffold leaves “six one-parameter families of empty squares (defect tubes) threading
the six mesh edges longer than one”, and Daniel’s notes of 30 September, retained on 2
October, say the Figure 34 set is not unavoidable.
The entry stayed `not-reviewed` with neither noted.
A source that names a registered entry’s premise as false should reach that entry’s
review when it is retained.

### G9-4 — Note, in the report: the published $k = 4$ square is in container coordinates

“In the coordinates above” reads as offsets from $(m_x, m_y)$, where the square would
cross the right wall.
Its Figure 1 draws it in container coordinates, where it fits: a translate of $Q_4$
along the edge’s normal, inside MacIver’s defect tube.
The printed slack $0.00545$ is $0.0054494$ rounded.

### G9-5 — Note: the Table 2 typo agrees with the record

The write-up’s reading of DS7 Table 2 at $n = 82…85$ is the one
`E-green-ds7-theorem9-reported-lower` has recorded since 7 September.

## What Rests on the Entry

- **Verified lanes: none.** No case’s `verified_lower_bound` cites either entry.
  At $k = 2, 3$ the values are below the exact $s(5)$ and $s(10)$, and at $k = 4, 5$
  below the verified $116511/25000$ (`T-043`) and $553/100$ (`T-045`). At $k = 6…17$ the
  verified lanes rest on Nagamochi’s closed form, whose Lemma 1 is the separate question
  of [#295](https://github.com/jlevy/squares/issues/295).
- **Reported lanes holding Green’s value (31):** $n = 82$, $122…125$, $145…148$,
  $170…173$, $197…200$, $226…229$, $257…261$ and $290…294$. Their notes now say the
  Figure 34 argument does not prove it.
- **Evidence and history only (19):** $n = 26, 27$ through `E-green26-reported-lower`,
  and $n = 37…39$, $50…52$, $65…68$, $83…85$, $101…104$, where a wand125 report has
  replaced Green’s value in the reported lane.
- **Prose:** `n-017.md`, which compared `cases/green17` with Green’s value; the
  generator text in `devtools/audit_ds7_lower_bounds.py`; the generated
  `ds7-lower-bound-audit.json` and `INVENTORY.md` cite the entry and are unchanged.

## Certificates Above $G_k$

The issue’s second suggestion, against this record:

| $k$ | Certificate | Retained in | Register |
| ---: | --- | --- | --- |
| 4 | Guzhou0806 R068 | `n17-guzhou-r068-2026-09-28` | `T-043`, `V3`/`C3`, the verified lane |
| 5 | `rect_n26_L55325` | `wand125-rectangle-certificates-2026-10-01` | `T-068`, `V0`/`C1`; the verified lane is `T-045`’s $553/100$ |
| 6 | `mixed_n37_L644` | `wand125-point-and-mixed-2026-10-01` | `T-069`, `V0`/`C1` |
| 7 | `mixed_n50_L740` | `wand125-point-and-mixed-2026-09-28` | `T-048`, `V0`/`C0` |
| 8 | `mixed_n65_L835` | `wand125-point-and-mixed-2026-10-01` | `T-069`, `V0`/`C1` |
| 9 | `mixed_n82_L932` | not retained | none |
| 9 | `mixed_n83_L935` | `wand125-linear-certificates-2026-10-02` | `T-073`, `V0`/`C1` |
| 9 | `mixed_n84_L940` | `wand125-mixed-bounds-2026-10-02` | `T-071`, `V0`/`C1` |
| 9 | `mixed_n85_L946` | not retained; the packet holds `mixed_n85_L942` | `T-071` holds $471/50$ |
| 10 | `mixed_n101_L1028` | `wand125-linear-certificates-2026-10-02` | `T-073`, `V0`/`C1` |

The upstream head at review time, `b00fc70f` (2026-10-02T15:16:36Z), also holds
`mixed_n83_L937`, which the issue does not list.
The two unretained certificates and that one are for the import lane that triages the
upstream.

## Claims by Evidential Status

- **Proved here, exactly:** the pattern’s identities and $G_k$ for $k = 2…17$; an empty
  fitting closed unit square for $k = 2$ and $4…17$; the published $k = 4$ square; the
  ceilings.
- **Certified here by branch-and-bound:** the rounded $k = 3$ pattern at $3518321/10^6$.
- **Measured here:** the figure match, to 0.90 pixel.
- **Reported, unverified, unchanged:** Theorem 9 itself for $k \ge 4$.

## Disposition

`E-green-ds7-theorem9-reported-lower` and `E-green26-reported-lower` carry this review
as `external_review` with state `defect-found`; their `limitations` and blocker say the
Figure 34 argument cannot be the missing proof.
No verified or reported value changes.
The reply on #308 can confirm the report for $k \ge 4$, correct its $k = 2$ aside, and
point to the certificates table above.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
