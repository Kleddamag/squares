---
id: H-012
title: First-leg enclosures fused with the box's, sharing the offset terms, make lemma R7 pay
registered: "2026-10-03T00:20Z"
metric: search instructions over the three callgrind cells
direction: lower
criterion: accept rule of the campaign README
---
# Fused First-Leg Enclosures

Registered after exp-009 and exp-010, which found lemma R7 removing 27 to 37% of the
boxes while the extra enclosures cost as much again.
An edge’s length over the box (lemma R5) is the least of nine terms; on R7’s first-leg
segment only the four terms that hold the edge’s end offsets change, since the centre’s
other coordinate is fixed there, and the offset products, the two constants and the two
offset-only terms are shared.
So compute both enclosures of every edge in one pass: the shared part once, the four
end-offset terms twice.
Accept a box when the larger of R7’s two path bounds, or R3’s, clears the threshold.
At direction zero the segment enclosures are the box’s, which are valid on the segment.

Prediction: exp-009’s node counts, a box costing 20 to 35% more rather than about 110%
more, and at least 10% fewer search instructions than c5 in all.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
