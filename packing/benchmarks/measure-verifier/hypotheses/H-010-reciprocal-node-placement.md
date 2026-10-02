---
id: H-010
title: Multiplying by reciprocals to place the area bound's nodes saves a tenth of the search
registered: "2026-10-02T21:05Z"
metric: search instructions over the three callgrind cells
direction: lower
criterion: accept rule of the campaign README
---
# Reciprocals for Node Placement

Lemma R2’s area bound places up to twelve candidate nodes per boundary rectangle, eight
of them by a division by the cosine or the sine.
Their positions only affect accuracy, so multiplying by approximate reciprocals computed
once per direction is equally sound.

Prediction: identical node counts and certified bounds to within the last digits, and
about 10% fewer search instructions (divisions are slow but few against the rest of the
area bound). Falsified below 10%.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
