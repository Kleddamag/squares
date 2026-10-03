---
id: H-005
title: One a-priori error budget beats per-operation directed rounding
registered: "2026-10-02T18:05Z"
metric: callgrind instructions over the three callgrind cells
direction: lower
criterion: accept rule of the campaign README
---
# One A-Priori Error Budget Beats Per-Operation Directed Rounding

Each interval operation rounds to nearest and then steps outward with `next_up` and
`next_down`, which in the v0 profile were a large share of the edge-enclosure code.
Every quantity there has bounded magnitude, so evaluating the affine terms in plain
binary64 and widening the final minimum once by a proved absolute error bound is also
sound, and needs a fraction of the operations.

Prediction: node counts within 1% of the control, instructions at least 10% lower.
It needs a new lemma in `SOUNDNESS.md`, with the bound’s constant derived for the
admitted side limit.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
