---
id: H-002
title: Cheaper exact admission halves a short run's instructions
registered: "2026-10-02T17:55Z"
metric: callgrind instructions over the three callgrind cells
direction: lower
criterion: accept rule of the campaign README
---
# Cheaper Exact Admission Halves a Short Run’s Instructions

In the v0 profile of `n32@r100`, admission (exact parsing, D4 expansion, enclosures) was
2.5 billion of 5.1 billion instructions.
Three things it does are unnecessary: parsing the coordinates of zero-weight rows (3,184
of `n32`’s 3,319 rows), building a normalized rational from each binary64 candidate
during enclosure (two or three greatest-common-divisor reductions per value), and
recomputing each image’s mass, which the expansion check already multiplied out.

Prediction: the same verdicts and nodes, and at least 30% fewer instructions per
single-direction process on the small certificates, where admission weighs most.
The exact premises checked do not change.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
