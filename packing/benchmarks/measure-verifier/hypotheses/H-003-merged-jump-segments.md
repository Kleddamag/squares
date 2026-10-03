---
id: H-003
title: Merged density jumps tighten the derivative enclosure and cut nodes
registered: "2026-10-02T18:05Z"
metric: callgrind instructions over the three callgrind cells
direction: lower
criterion: accept rule of the campaign README
---
# Merged Density Jumps Tighten the Derivative Enclosure

The derivative of the captured mass is a sum over vertical density jumps of jump times
length inside the square (lemma R4 summed).
Where two rectangles share an edge, the per-rectangle enclosure adds two intervals of
opposite sign whose widths add; merged into one segment of jump $\rho_2 - \rho_1$ the
width is $|\rho_2 - \rho_1|$ times one length enclosure.

Prediction: fewer nodes wherever adjacent rectangles have similar densities, and fewer
edge enclosures per box.
Falsified if the certificates’ rectangles rarely share edges (then node counts move by
under 2%).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
