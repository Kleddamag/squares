---
id: exp-016
title: H-012 fused first-leg enclosures keep the node savings and break even
date: "2026-10-03"
hypotheses: [H-012]
decision: rejected
control: c5 (sqverify-fast-c5)
candidate: c5 with both lemma R7 enclosures of every edge in one pass (sqverify-fast-h012)
raw: ../results/exp-016-h012-callgrind.jsonl
regime: callgrind counts (load-independent)
---
# H-012: Fused First-Leg Enclosures

| Cell | c5 nodes | H-012 nodes | c5 search instructions | H-012 search instructions | Change |
| --- | ---: | ---: | ---: | ---: | ---: |
| `rect_n32_L595@r1` | 15,397 | 9,721 | 638,600,000 | 601,200,000 | −5.9% |
| `rect_n32_L595@r100` | 24,525 | 17,893 | 1,062,000,000 | 1,102,000,000 | +3.8% |
| `rect_n61_L796@r100` | 85,773 | 58,459 | 3,281,000,000 | 3,275,000,000 | −0.2% |
| Total |  |  | 4.981 G | 4.977 G | **−0.1%** |

(Figures are the summary’s rounded values.)
Same verdicts, and exp-009’s node counts, as predicted.
On the mixed certificate `mixed_n76_L894` the candidate verified directions 1 and 100
with 42% and 24% fewer boxes, at no lower CPU on this loaded host.
Decision: **rejected** and reverted; c5 stays standing.

**What the prediction got wrong.** Sharing the offset products and the end-free terms
did not make the second enclosure cheap: a box cost about 50% more, not 20 to 35%, so
the third of the boxes it removed paid for it and no more.
The edge-length enclosures are nearly the whole of a box’s cost, and the four end-offset
terms with their minima are most of an enclosure.
Lemma R7 stays proved in `SOUNDNESS.md` and unused; after three rounds (exp-009,
exp-010, exp-016) it pays only with a predictor that picks the boxes that need it at
less than the cost of an enclosure, which none of the three found.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
