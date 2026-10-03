---
id: exp-014
title: The sampled release audit costs 3.4% of the search
date: "2026-10-02"
hypotheses: []
decision: baseline
control: c2 (sqverify-fast-c2)
candidate: c3, c2 plus the audit of every 1,024th box (sqverify-fast-audit)
raw: ../results/exp-014-audit-callgrind.jsonl
regime: callgrind counts (load-independent)
---
# The Release Audit’s Price

Not a performance hypothesis: spec §4.2 asks the verifier to refuse a box-level fault
that flips one inside classification, and release builds had no redundancy that could.
The audit recomputes an audited box’s centre bound from every rectangle, with no
classification and nothing inherited (lemma A3), and stops the direction as
`audit-failed` on a disagreement.
It runs at the root and every 1,024th box by default.

| Cell | c2 search instructions | c3 search instructions | Change |
| --- | ---: | ---: | ---: |
| `rect_n32_L595@r1` | 619,185,659 | 630,700,000 | +1.9% |
| `rect_n32_L595@r100` | 1,030,652,595 | 1,049,000,000 | +1.8% |
| `rect_n61_L796@r100` | 3,101,143,181 | 3,231,000,000 | +4.2% |
| Total | 4.751 G | 4.911 G | **+3.4%** |

(c3’s figures are the summary’s rounded values.)
Same verdicts and nodes.
The fault-injection controls in `devtools/check_sqverify_fast.py` refuse a fault at box
2 with the default sampling and with an audit of every box, and a fault at box 1,000
with an audit of every box.
A fault deep in the tree whose subtree holds no audited box can escape the default
sampling; `--audit-every 1` closes that gap at about ten times the cost, and is the
setting for a run whose evidence must survive a bookkeeping fault.

c3 is the standing build from here: the audit stays on by default.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
