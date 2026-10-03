---
id: exp-003
title: H-006 inherited derivative bounds cut the search by 18.5%
date: "2026-10-02"
hypotheses: [H-006]
decision: accepted
control: c1 (v0 with H-002's admission and the refusal witnesses; sqverify-fast-c1)
candidate: c1 plus inherited derivative bounds (sqverify-fast-h006)
raw: [../results/exp-003-h006-callgrind.jsonl, ../results/exp-003-h006-cpu.jsonl]
regime: callgrind counts (load-independent); CPU interleaved, two repeats, load average 16.9 to 17.3
---
# H-006: Inherited Derivative Bounds

| Cell | c1 search instructions | H-006 search instructions | Change |
| --- | ---: | ---: | ---: |
| `rect_n32_L595@r1` | 1,552,591,200 | 1,279,098,950 | −17.6% |
| `rect_n32_L595@r100` | 2,645,030,601 | 2,144,474,031 | −18.9% |
| `rect_n61_L796@r100` | 7,949,641,252 | 6,474,787,019 | −18.6% |
| Total | 12.15 G | 9.90 G | **−18.5%** |

CPU guard, total of medians over `n32@r1`, `n32@r100`, `n61@r100`, `n78@r100`: c1 4.314
s, H-006 3.450 s (−20%); every cell faster, ranges disjoint.
Verdicts, node and leaf counts identical, as predicted: the minimum of two valid bounds
never loosened a box, and here never tightened one enough to save a split.

Decision: **accepted** by all three clauses.
Worth its complexity: a dozen lines and a one-sentence lemma (a bound on $|\partial F|$
proved over a box holds on its sub-boxes).

**What the prediction got wrong.** 25 to 40% was predicted from the gradient’s 70%
share; the saving was 18.5%. The share of leaves that certify on the inherited bound is
smaller than guessed, because a child halves only one side of its parent’s box, so its
penalty along the other axis is unchanged and the parent’s near miss usually stays a
near miss.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
