---
id: exp-007
title: H-005 one error budget per edge costs 2% more than branch-free steps
date: "2026-10-02"
hypotheses: [H-005]
decision: rejected
control: c2 (H-006 and H-007 accepted; sqverify-fast-c2)
candidate: c2 with the edge-length enclosure evaluated in round-to-nearest and widened once by `2^-49 m`
raw: ../results/exp-007-h005-callgrind.jsonl
regime: callgrind counts (load-independent)
---
# H-005: One Error Budget per Edge

| Cell | c2 search instructions | H-005 search instructions | Change |
| --- | ---: | ---: | ---: |
| `rect_n32_L595@r1` | 619,185,659 | 630,931,663 | +1.9% |
| `rect_n32_L595@r100` | 1,030,652,595 | 1,051,389,308 | +2.0% |
| `rect_n61_L796@r100` | 3,101,143,181 | 3,166,637,132 | +2.1% |
| Total | 4.75 G | 4.85 G | **+2.1%** |

Verdicts unchanged; nodes unchanged except `n32@r1`, where the wider budget cost ten
fewer nodes (15,387 against 15,397), within noise of the bound.
Decision: **rejected** and reverted; the CPU guard was not run because clause 2 already
failed.

**What the prediction got wrong.** It was registered when every interval operation still
called `next_up` and `next_down`. Once exp-005 made the directed step three branch-free
floating-point operations, the budget’s own cost (the magnitude sum `m` and its product)
plus evaluating each of the nine terms at both ends was no cheaper than directed
rounding. The hypothesis was overtaken by the change before it.
The edge-length differential test written for it,
`rotated_tests::edge_length_enclosures_contain_exact_lengths_over_the_box`, stays: it
checks the enclosure in use against exact rational lengths at box corners and interior
points, and fails on a seeded wrong endpoint.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
