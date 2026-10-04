---
id: exp-017
title: Making NaN fatal costs nothing once min and max carry it without a branch
date: "2026-10-03"
hypotheses: []
decision: baseline
control: c6 (sqverify-fast-c6)
candidate: c7b, c6 with the fixes for findings S1, S2 and S4 of the 3 October soundness review
raw: ../results/exp-017-nan-fatal-callgrind.jsonl
regime: callgrind counts (load-independent)
---
# The Price of a Fatal NaN

Not a performance hypothesis: the soundness review of 3 October rejected the crate
because the axis sweep let a `NaN` vertex drop out of its minimum (finding S1), and
asked that `NaN` be impossible or fatal everywhere (S4). The fix caps densities and the
net at admission (lemma F3), refuses a non-finite vertex or box, and replaces `f64::min`
and `f64::max`, which return the other operand when one is `NaN`, in every interval
primitive and in lemmas R2, Z1 and Z2. This round prices the replacement.

The first version, c7, tested both operands for `NaN` and cost **+17.1%** search
instructions over the three cells
([raw](../results/exp-017-nan-fatal-branchy-callgrind.jsonl)): the edge-length enclosure
takes eight minima per endpoint.
The standing version, c7b, selects with one comparison, which keeps a `NaN` in the
second operand, and adds `a * 0`, which is zero for finite `a` and `NaN` otherwise:

| Cell | c6 search instructions | c7b search instructions | Change |
| --- | ---: | ---: | ---: |
| `rect_n32_L595@r1` | 638,600,000 | 631,200,000 | −1.2% |
| `rect_n32_L595@r100` | 1,062,000,000 | 1,051,000,000 | −1.0% |
| `rect_n61_L796@r100` | 3,281,000,000 | 3,248,000,000 | −1.0% |
| Total | 4.981 G | 4.930 G | **−1.0%** |

(Figures are the summary’s rounded values.)
Same verdicts, nodes and least certified bounds, bit for bit: the fix touches no finite
path. The select compiles to one `minsd` or `maxsd`, cheaper than the library call’s
`NaN` handling it replaces.

c7b is the standing build from here.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
