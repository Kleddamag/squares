---
id: H-004
title: Bounding the first leg's derivative on its segment cuts nodes
registered: "2026-10-02T18:05Z"
metric: search instructions over the three callgrind cells
direction: lower
criterion: accept rule of the campaign README
---
# Bounding the First Leg’s Derivative on Its Segment Cuts Nodes

Lemma R3 walks from the centre along $x$ at fixed $y_0$, then along $y$. The first leg
only needs $|\partial_x F|$ on the segment $[x_0 \pm d_x] \times \{y_0\}$, a degenerate
box whose enclosure is tighter than the whole box’s; the second leg needs the whole box.
Taking the better of the two path orders gives a bound at least as good as the box bound
(lemma R7).

Prediction: 5 to 20% fewer nodes, partly paid back by a second enclosure per boundary
rectangle. Falsified if search instructions do not fall by 10%.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
