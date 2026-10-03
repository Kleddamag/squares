---
id: exp-005
title: H-007 branch-free directed steps cut the search by 52%
date: "2026-10-02"
hypotheses: [H-007]
decision: accepted
control: H-006 build (sqverify-fast-h006)
candidate: H-006 plus branch-free `up` and `dn` (sqverify-fast-h007)
raw: [../results/exp-005-h007-callgrind.jsonl, ../results/exp-005-h007-cpu.jsonl]
regime: callgrind counts (load-independent); CPU interleaved, two repeats, load average 18.0 to 18.5
---
# H-007: Branch-Free Directed Steps

| Cell | H-006 search instructions | H-007 search instructions | Change |
| --- | ---: | ---: | ---: |
| `rect_n32_L595@r1` | 1,279,098,950 | 621,989,352 | −51.4% |
| `rect_n32_L595@r100` | 2,144,474,031 | 1,035,568,491 | −51.7% |
| `rect_n61_L796@r100` | 6,474,787,019 | 3,116,264,565 | −51.9% |
| Total | 9.90 G | 4.77 G | **−51.8%** |

CPU guard, total of medians over `n32@r1`, `n32@r100`, `n61@r100`, `n78@r100`: H-006
3.610 s, H-007 2.607 s (−28%); every cell faster, ranges disjoint.
Node and leaf counts identical; the least certified bounds move in the fourteenth
decimal (`n32@r100`: 1.0001011771194057 to 1.0001011771194015), the price of stepping up
to two values out.

Decision: **accepted**. Worth its complexity: two three-operation functions and a
half-page lemma replace the library calls, and every interval operation benefits.

**What the prediction got wrong.** Instructions fell by the predicted half, but CPU by
only 28%: the removed instructions were cheap, well-predicted branches and integer
moves, while the floating-point dependency chains that remain set the pace.
Instruction counts overstate gains of this kind; the CPU guard is what keeps that
honest.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
