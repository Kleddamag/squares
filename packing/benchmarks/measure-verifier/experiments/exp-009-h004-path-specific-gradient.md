---
id: exp-009
title: H-004 first-leg enclosures on every box cut nodes by a third and cost 40% more
date: "2026-10-02"
hypotheses: [H-004]
decision: rejected
control: c2 (sqverify-fast-c2)
candidate: c2 plus first-leg enclosures computed eagerly at every box (sqverify-fast-h004)
raw: ../results/exp-009-h004-callgrind.jsonl
regime: callgrind counts (load-independent)
---
# H-004: First-Leg Enclosures on Every Box

| Cell | c2 nodes | H-004 nodes | c2 search instructions | H-004 search instructions | Change |
| --- | ---: | ---: | ---: | ---: | ---: |
| `rect_n32_L595@r1` | 15,397 | 9,721 | 619,185,659 | 802,800,000 | +29.7% |
| `rect_n32_L595@r100` | 24,525 | 17,893 | 1,030,652,595 | 1,482,000,000 | +43.8% |
| `rect_n61_L796@r100` | 85,773 | not recorded | 3,101,143,181 | 4,354,000,000 | +40.4% |
| Total |  |  | 4.75 G | 6.64 G | **+39.7%** |

(H-004’s search instructions are the summary’s rounded values; the raw file holds the
process totals.) Same verdicts.
Decision: **rejected**.

**What the prediction got wrong.** It was right about the bound: lemma R7 removed 27 to
37% of the boxes, more than the 5 to 20% predicted.
It was wrong about where to compute it.
Every box paid for two more edge-length enclosures per boundary rectangle, while only
boxes near certification can use them.
That observation became H-009: compute a first-leg enclosure only when the other leg’s
penalty already fits in the margin, a necessary condition for the path to certify.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
