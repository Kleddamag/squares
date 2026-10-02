# Idea Board: Measure-Verifier Performance

Every idea about making `sqverify-fast` faster or tighter, one line each.
A registered row names its hypothesis and stops carrying the outcome, which the
experiments own.

## Registered

| Status | Id | Idea | Crux |
| --- | --- | --- | --- |
| registered | [H-001](hypotheses/H-001-edge-classification.md) | Classify each boundary rectangle’s four edges before enclosing their lengths | A rectangle crossed by one side of the square has two or three edges wholly inside or outside, whose lengths are exact for free |
| registered | [H-002](hypotheses/H-002-cheap-admission.md) | Admit the certificate without exact work it does not need | Zero-weight rows, normalized rational enclosures and recomputed masses dominate a short run |
| registered | [H-003](hypotheses/H-003-merged-jump-segments.md) | Enclose the derivative from merged density jumps, not per-rectangle edges | Coincident edges of adjacent rectangles cancel before the interval sum widens |
| registered | [H-004](hypotheses/H-004-path-specific-gradient.md) | Bound the first leg’s derivative on the segment, not the box | The first leg of the mean-value path stays on the line through the centre |
| registered | [H-006](hypotheses/H-006-inherited-derivative-bound.md) | Try acceptance with the parent’s derivative bound before computing the child’s | A bound proved on a box holds on its sub-boxes, and most leaves are one split from a near miss |
| registered | [H-007](hypotheses/H-007-branch-free-directed-steps.md) | Step outward by adding a scaled magnitude instead of calling `next_up` | The library step’s branches were three quarters of the edge enclosure |
| registered | [H-008](hypotheses/H-008-skip-hopeless-own-gradient.md) | Split a box at once when its margin is far below its inherited penalty | Internal boxes compute an enclosure only to fail |
| registered | [H-009](hypotheses/H-009-lazy-first-leg-enclosures.md) | Compute a first-leg enclosure only when the other leg fits in the margin | Exp-009’s node savings without paying at every box |
| registered | [H-005](hypotheses/H-005-error-budget-arithmetic.md) | Replace per-operation directed rounding in the edge enclosures by one a-priori error budget | Rounding steps are a large share of the hot loop |

## Raw

- Reuse the box partition of direction $r - 1$ to seed direction $r$: neighbouring
  directions’ certified boxes may mostly still certify.
- Best-first or breadth-first order to share classification across siblings.
- Structure-of-arrays rectangle data and batched classification for vectorization.
- A cheap acceptance test before the gradient (inside mass alone, or the parent’s
  gradient scaled to the child).
- Second-order bound with a Hessian enclosure: halves the curvature penalty, but the
  gradient jumps at near-parallel edges make the Hessian large at small angles.
- Continuous-angle boxes in place of the 201-direction net.
- Skip a box’s own enclosure only when its margin is far below its parent’s *own*
  penalty (exp-008 showed the inherited bound is a bad predictor).
- Multiply by precomputed reciprocals of the cosine and sine when placing the area
  bound’s nodes, instead of dividing (node placement needs no accuracy).

## Parked

- Threads across directions: cuts wall time, not CPU; already available as `--threads`.

## Dead

Nothing yet.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
