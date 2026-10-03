---
id: H-008
title: Skipping the own derivative enclosure on hopeless boxes saves search work
registered: "2026-10-02T20:24Z"
metric: search instructions over the three callgrind cells
direction: lower
criterion: accept rule of the campaign README
---
# Skipping the Own Derivative Enclosure on Hopeless Boxes

About half the boxes are internal: they compute their own derivative enclosure only to
fail and split. When a box’s centre margin is below a quarter of the penalty its
inherited bounds charge, its own enclosure would have to be four times tighter to
certify, which a box half its parent’s size rarely achieves.
Splitting such a box at once, with its children keeping the inherited bounds, saves the
enclosure; it is sound because no box is accepted on the skipped computation.

Prediction: node counts rise by under 5% (children inherit looser bounds), and search
instructions fall by 10 to 25%. Falsified if node growth eats the saving.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
