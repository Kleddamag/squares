# wand125’s Note on Green’s DS7 Theorem 9, Pinned 2026-10-02

This packet retains a write-up by wand125, published as a GitHub gist on 2 October
2026, which argues that the unavoidable set behind Trevor Green’s lower bound in
Friedman’s survey DS7, Theorem 9,

$$
s(k^2+1) \ge G_k = 2\sqrt2 - 1 + \frac{k(k-1)^2 + (k-1)\sqrt{2k}}{k^2+1},
$$

is not unavoidable for $k \ge 4$, starting from the sixteen points of DS7’s Figure 34
for $n = 17$. The request is
[jlevy/squares#308](https://github.com/jlevy/squares/issues/308), which names this
record’s evidence entry `E-green-ds7-theorem9-reported-lower`. The source says plainly
that it is not a counterexample to the bound itself.

## Source and Pin

| Field | Value |
| --- | --- |
| Source | <https://gist.github.com/wand125/9e5f27e25607c0966c4f91bc1253ce8b>, cloned as `https://gist.github.com/9e5f27e25607c0966c4f91bc1253ce8b.git` |
| Revision | `9d6de784d98169b90a1af8d5e57c0499cfb12874`, tree `51a98c06`, the head of `master` and the third of three commits, all of 2 October 2026 |
| Committed | 2026-10-02T12:35:13Z; the first commit, `94c30fdd`, is of 05:45:38Z and the second, `86a341ba`, of 05:45:47Z. The commit author’s name is Hiroaki Hosono, the name the [valid7 packet](../wand125-valid7-independent-check-2026-10-02/README.md) reads from wand125’s commits |
| Retrieved | 2026-10-02T16:41:34Z, a full clone |
| Licence | None stated: the gist has no licence file or notice. Retained, as the [MacIver manuscripts](../maciver-square-packing-2026-09-07/README.md) are, as the source a record entry’s review reads |
| Request | [jlevy/squares#308](https://github.com/jlevy/squares/issues/308), opened 2026-10-02T14:06:26Z by wand125, after the pinned commit |

The two later commits change one line each of `green-theorem9.md`; the packet pins the
head, which the issue links.

## Credit and AI Assistance, as the Source States Them

The write-up’s byline is “wand125, 2026-10-02”. It has no attribution file and no
statement about how it was written.
It credits Friedman’s survey for the statement, Lemma 3 and Figure 34, and says that
MacIver’s manuscript on $s(17)$ “uses the same configuration for $k = 4$”, observes the
empty squares, and repairs that case with a defect-counting argument.
That manuscript has been retained here since 7 September as **[MacIver 2026 n17]**.

## What Is Retained

All four files of the gist, 47,975 bytes, byte-identical under
[`green-theorem9-gist/`](green-theorem9-gist/), listed with their digests in
[`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256):

| File | What it is |
| --- | --- |
| `green-theorem9.md` | The write-up: the published statement, the reconstructed pattern, why it fails for $k \ge 4$, an explicit empty square for every $k \ge 4$, published bounds above $G_k$, and a DS7 Table 2 typo |
| `ds7-fig34-L17.svg` | A 171 by 171 SVG wrapper around one embedded GIF, which is byte for byte DS7’s `pic/L17.gif` as combinatorics.org served it on 2026-10-02, SHA-256 `2b6b3af60fe9b629e00824d80c937c8f7de9f9fa354b4b96af03d9ca5a6e8c54` |
| `fig1-k4.svg` | The source’s figure of the $k = 4$ pattern, its six long edges and its published empty square |
| `fig2-k10-zoom.svg` | The source’s close-up of the empty square at $k = 10$ |

[`devtools.acquire_source`](../../../devtools/acquire_source.py) `--check` re-derives
the packet from its manifest.

**Not retained:** the illustrated page the issue links,
<https://claude.ai/artifact/An5pCnG21oPi136aSUP3Rj>, with figures and a $k = 2$ to $60$
explorer. It needs a signed-in session to fetch, so nothing of it is held here and
nothing below depends on it.
The source publishes no code for its exact checks.

## The Claims, as the Source States Them

1. DS7’s Figure 34 points for $n = 17$ are not unavoidable at side
   $G_4 = (40\sqrt2 + 19)/17$: a unit square inside the container contains none of
   them, “checked in exact rational arithmetic”.
2. The pattern reconstructed for every $k$ — $k$ rows at heights $m_y + jt$, even rows
   at offsets $0, u, u+1, \ldots, u+k-2$ and odd rows at $0, 1, \ldots, k-2, u+k-2$ from
   $m_x$, with $t^2 + u^2 = 1$, $kt - u = k - 1$, $m_x = \sqrt2 - t/2$ and
   $m_y = \sqrt2 - 1/2$ — has width and height exactly $G_k$, and matches Figure 34 up
   to the reflection $y \mapsto G_4 - y$.
3. For $k \ge 4$ the mesh edges $(1-u, t)$ have length $d = \sqrt{2-2u} > 1$, so DS7’s
   Lemma 3 does not apply to their triangles, and the unit square $Q_k$ centred at the
   midpoint of such an edge and aligned with it misses every point with slack $(d-1)/2$.
   At $k = 4$ it publishes the square with centre $(29638179/10^7, 302261/250000)$ and
   $\tan(\theta/2) = 179111/312500$; at $k = 18$, $t = 24/25$, $u = 7/25$ and the slack
   is $1/10$.
4. For $k = 2$ and $3$ every edge is at most 1 “and the argument works”.
5. DS7’s Table 2 prints $2\sqrt2 + (288 + 12\sqrt3)/41$ for $n = 82$ to $85$ where Theorem
   9 at $k = 9$ gives $2\sqrt2 + (247 + 12\sqrt2)/41$.

## Checked Here

[`devtools.check_green_ds7`](../../../devtools/check_green_ds7.py) reconstructs the
pattern in exact arithmetic over $\mathbb{Q}(\sqrt2, \sqrt k)$ and decides every
comparison exactly; the
[review of 2 October](../../../../docs/project/reviews/review-2026-10-02-green-ds7-theorem9.md)
gives its findings in full. In short:

- Claims 2 and 3 hold for every $k$ from 4 to 17, the range this record’s entry
  covers: the identities are exact, $Q_k$ fits in the closed container and misses every
  point, with slack $(d-1)/2$, and the square the source publishes for $k = 4$ does
  too, its centre read in container coordinates as its Figure 1 draws it. An
  independent search finds no wider empty square at any of these $k$. Claim 1 follows.
- The GIF in `ds7-fig34-L17.svg` is DS7’s own, and its sixteen dots sit within 0.9 pixel
  of the reconstructed $k = 4$ points at 38.2 pixels per unit, row $j = 0$ at the top of
  the image as claim 2 says.
- Claim 4 holds for $k = 3$ and fails for $k = 2$. At $k = 3$ the scaled pattern is
  certified unavoidable a thousandth below $G_3$ in the receipt’s run, and
  $4.1 \times 10^{-6}$ below it in a longer run the review reports. At $k = 2$,
  $t = 4/5$ and the side margin $m_x = \sqrt2 - 2/5$ exceeds 1, so a unit square in the
  strip along either side wall contains no point. Theorem 9 at $k = 2$ is still true,
  because $s(5) = 2 + 1/\sqrt2$ exceeds $G_2 = 2\sqrt2 - 1/5$, but this pattern does
  not prove it.
- Claim 5 agrees with this record’s `E-green-ds7-theorem9-reported-lower`, which has
  excluded the printed Table 2 cell since 7 September.

The tool’s run of 2 October for $k = 2$ to $17$ is in [`receipts/`](receipts/):
[`check_green_ds7.log`](receipts/check_green_ds7.log), written by
`devtools.replay_receipt`, and [`check_green_ds7.json`](receipts/check_green_ds7.json),
one record per $k$ with every checked square’s exact centre and rotation.

## Limitations

The write-up reconstructs one argument from DS7’s figure and statement.
Green’s own proof is unpublished, so the source shows, and this packet’s check confirms,
only that the argument the published material suggests does not prove Theorem 9 for
$k \ge 4$; neither says the bound is false. The ceiling the check reports is an upper bound
on what this one pattern, scaled, can prove, not on $s(k^2+1)$.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
