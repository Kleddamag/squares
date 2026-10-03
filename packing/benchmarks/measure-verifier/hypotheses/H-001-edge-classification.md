---
id: H-001
title: Edge classification removes most edge-length enclosures
registered: "2026-10-02T17:52Z"
metric: callgrind instructions over the three callgrind cells
direction: lower
criterion: accept rule of the campaign README
---
# Edge Classification Removes Most Edge-Length Enclosures

The derivative bound encloses the length of each boundary rectangle’s four edges inside
the square over the whole box, with nine interval affine terms per edge.
At depth a boundary rectangle is usually crossed by one side of the square, so two or
three of its edges lie wholly inside every square of the box or wholly outside all of
them.
Applying lemma R1 to the edge as a degenerate rectangle gives those lengths exactly
(the edge’s length, or zero) for a few plain comparisons.

Prediction: node counts unchanged (the enclosure was already tight for such edges), and
the direction’s instruction count falls by about a third of the gradient’s share.
The gradient was 69% of a direction’s instructions in the v0 profile of `n32@r100`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
