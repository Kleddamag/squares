---
id: exp-015
title: Points, segments and the classification audit cost 1.4% on rectangle certificates
date: "2026-10-03"
hypotheses: []
decision: baseline
control: c3 (sqverify-fast-c3)
candidate: c5, c3 with points, segments, formats M and L, and the audit's fresh classification
raw: ../results/exp-015-atoms-callgrind.jsonl
regime: callgrind counts (load-independent)
---
# Milestone B’s Price on Rectangle Certificates

Not a performance hypothesis: Milestone B (`think-4vf7`) adds point and segment lists to
every box, which a rectangle certificate leaves empty, and the release audit now also
classifies every item against an audited box from scratch (lemma A3), which catches a
straddling item wrongly certified inside whose mass lies wholly in the centre’s own
square. This round prices both on the three standing cells.

| Cell | c3 search instructions | c5 search instructions | Change |
| --- | ---: | ---: | ---: |
| `rect_n32_L595@r1` | 630,700,000 | 638,600,000 | +1.3% |
| `rect_n32_L595@r100` | 1,049,000,000 | 1,062,000,000 | +1.2% |
| `rect_n61_L796@r100` | 3,231,000,000 | 3,281,000,000 | +1.5% |
| Total | 4.911 G | 4.981 G | **+1.4%** |

(Figures are the summary’s rounded values.)
Same verdicts and nodes.
CPU moved by the same small amount in the guard run beside the counts, at load average
5.3 to 7.0, which is too loaded to read it more finely.

c5 is the standing build from here, for every format.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
