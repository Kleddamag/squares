---
id: exp-002
title: H-001 edge classification saves 5% of process instructions
date: "2026-10-02"
hypotheses: [H-001]
decision: rejected
control: v0 (sha256 0cec8849…)
candidate: v0 plus edge classification (sqverify-fast-h001)
raw: ../results/exp-002-h001-callgrind.jsonl
regime: callgrind instruction counts, one run per cell; load does not affect the count
---
# H-001: Edge Classification

| Cell | v0 instructions | H-001 instructions | Change |
| --- | ---: | ---: | ---: |
| `rect_n32_L595@r1` | 4,045,387,631 | 3,891,490,029 | −3.8% |
| `rect_n32_L595@r100` | 5,136,853,397 | 4,836,391,064 | −5.8% |
| `rect_n61_L796@r100` | 13,575,998,800 | 12,830,000,000 (rounded in the summary) | −5.5% |
| Total | 22.76 G | 21.56 G | −5.3% |

Same verdicts and node counts.
The accept rule asks for 10% fewer instructions, so the change is **rejected** and
reverted.

**What the prediction got wrong.** It was right about the component and wrong about the
whole. Admission (exact parsing, expansion and enclosure) was half of each
single-direction process, so even a large saving inside the gradient moved the total
little; and classifying an edge costs most of what enclosing its length does.
The measurement also showed that process totals dilute every change to the search, which
led to the harness reporting the search’s own instructions (`search_instructions`,
inclusive cost of `rotated::verify_direction`) from exp-003 on.
Edge classification may be worth revisiting with that metric if the edge enclosure gets
more expensive than the classification again.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
