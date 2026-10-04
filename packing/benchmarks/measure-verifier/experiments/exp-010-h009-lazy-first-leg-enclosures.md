---
id: exp-010
title: H-009 lazy first-leg enclosures keep the node savings and still cost 1% more
date: "2026-10-02"
hypotheses: [H-009]
decision: rejected
control: c2 (sqverify-fast-c2)
candidate: c2 plus first-leg enclosures only where the other leg fits in the margin (sqverify-fast-h004b)
raw: ../results/exp-010-h004b-callgrind.jsonl
regime: callgrind counts (load-independent)
---
# H-009: Lazy First-Leg Enclosures

| Cell | c2 nodes | H-009 nodes | c2 search instructions | H-009 search instructions | Change |
| --- | ---: | ---: | ---: | ---: | ---: |
| `rect_n32_L595@r1` | 15,397 | 9,721 | 619,185,659 | 589,438,039 | −4.8% |
| `rect_n32_L595@r100` | 24,525 | 17,893 | 1,030,652,595 | 1,082,366,076 | +5.0% |
| `rect_n61_L796@r100` | 85,773 | 58,459 | 3,101,143,181 | 3,141,682,491 | +1.3% |
| Total |  |  | 4.75 G | 4.81 G | **+1.3%** |

Same verdicts, and exactly H-004’s node counts, as predicted (the lazy rule computes the
first-leg bound wherever it could certify).
Decision: **rejected** and reverted.

**What the prediction got wrong.** The necessary condition is weak: at most boxes that
fail the box bound the margin still covers one leg’s penalty, so the extra enclosures
ran at nearly every failing box, and a box’s cost rose by about half while the box count
fell by a third. The lemma stays proved in `SOUNDNESS.md` (R7) and unused.
It would pay if an edge-length enclosure became much cheaper than a box, or if a cheaper
predictor than the margin test chose the boxes that need it.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
