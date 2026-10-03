---
id: exp-013
title: H-011 sign-definite side starts save under 2% of boxes and nothing overall
date: "2026-10-02"
hypotheses: [H-011]
decision: rejected
control: c2 (sqverify-fast-c2)
candidate: c2 plus a side-start bound at failing boxes with a sign-definite axis (sqverify-fast-h011)
raw: ../results/exp-013-h011-callgrind.jsonl
regime: callgrind counts (load-independent); load average 2.7
---
# H-011: Sign-Definite Side Starts

| Cell | c2 nodes | H-011 nodes | c2 search instructions | H-011 search instructions | Change |
| --- | ---: | ---: | ---: | ---: | ---: |
| `rect_n32_L595@r1` | 15,397 | 15,121 | 619,185,659 | 617,296,764 | −0.3% |
| `rect_n32_L595@r100` | 24,525 | 24,467 | 1,030,652,595 | 1,032,346,697 | +0.2% |
| `rect_n61_L796@r100` | 85,773 | 85,441 | 3,101,143,181 | 3,105,680,772 | +0.1% |
| Total |  |  | 4.751 G | 4.755 G | **+0.1%** |

Same verdicts. Decision: **rejected** and reverted.

**What the prediction got wrong.** The boxes that fail are, almost all, boxes where the
derivative enclosure changes sign on both axes: they sit near the capture’s minimum
ridge, which is where the threshold is close, and that is exactly where no axis is
sign-definite. Boxes with a definite slope already certify on the centre bound.
The lemma (R8) is sound and cheap to state but has nowhere to act on these certificates.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
