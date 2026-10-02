---
id: H-006
title: Inheriting the parent's derivative bound skips most leaves' gradient work
registered: "2026-10-02T19:52Z"
metric: search instructions over the three callgrind cells
direction: lower
criterion: accept rule of the campaign README
---
# Inheriting the Parent’s Derivative Bound

A bound on $|\partial_x F|$ and $|\partial_y F|$ proved over a box holds on every
sub-box, so a child can first try lemma R3 with its parent’s bounds and its own centre
value, which it computes anyway.
Only if that fails does it enclose its own derivative, and it keeps the smaller of the
two bounds per axis for its own children.

Prediction: the same verdicts; node counts equal or slightly lower (the minimum of two
valid bounds is never looser); a large share of leaves certify on the inherited bound,
skipping the gradient, which was about 70% of the search in v0’s profile.
Expect 25 to 40% fewer search instructions.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
