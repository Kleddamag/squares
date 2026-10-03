---
id: exp-008
title: H-008 skipping hopeless boxes' own enclosures multiplies nodes 880-fold
date: "2026-10-02"
hypotheses: [H-008]
decision: rejected
control: c2 (sqverify-fast-c2)
candidate: c2 plus the skip rule with ratio 1/4 (sqverify-fast-h008)
raw: ../results/exp-008-h008-callgrind.jsonl
regime: callgrind counts; the run was stopped after its first cell
---
# H-008: Skipping Hopeless Boxes’ Own Enclosures

| Cell | c2 nodes | H-008 nodes | c2 search instructions | H-008 search instructions |
| --- | ---: | ---: | ---: | ---: |
| `rect_n32_L595@r1` | 15,397 | 13,564,515 | 619,185,659 | 162,457,737,652 |

The verdict stayed `verified`, as it must (no box is accepted on the skipped work), but
the search did 262 times the instructions.
The remaining cells were not run.
Decision: **rejected** and reverted.

**What the prediction got wrong.** It assumed the inherited bound was a near miss.
At the top of the tree it is the root’s enclosure over the whole domain, which is loose
by orders of magnitude, so the rule fired at nearly every box below the root and each
subtree kept the root’s bound until its boxes were small enough for that loose bound to
certify. The inherited bound is a good *acceptance* test (exp-003) and a bad *predictor*
of whether a box’s own enclosure helps.
A variant that compares the margin with the parent’s own penalty, not the inherited one,
would avoid this; it is on the board as an idea, not registered.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
