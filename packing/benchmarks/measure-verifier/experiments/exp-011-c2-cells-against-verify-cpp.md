---
id: exp-011
title: The standing build c2 beside verify.cpp on six single-direction cells, 29 times less CPU
date: "2026-10-02"
hypotheses: []
decision: baseline
control: verify.cpp through `devtools.audit_wand125_rectangles --control`
candidate: c2 (sqverify-fast-c2)
raw: ../results/exp-011-c2-cells-vs-verify-cpp.jsonl
regime: shared 4-core container, load average 14.6 to 18.9 (the census on two cores beside it), one interleaved repeat
---
# c2 Beside verify.cpp, Single Directions

Each cell is one process per program and one direction.
c2’s CPU includes its exact admission (about 0.1 s for `n32`, 0.4 s for `n78`);
`verify.cpp`’s is its process alone.

| Cell | verify.cpp CPU s | c2 CPU s | Ratio | verify.cpp boxes | c2 boxes |
| --- | ---: | ---: | ---: | ---: | ---: |
| `rect_n32_L595@r1` | 2.154 | 0.194 | 11.1 | 15,387 | 15,397 |
| `rect_n32_L595@r100` | 6.243 | 0.252 | 24.8 | 25,041 | 24,525 |
| `rect_n32_L595@r150` | 7.587 | 0.268 | 28.3 | 28,541 | 27,725 |
| `rect_n32_L595@r200` | 8.531 | 0.304 | 28.0 | 32,183 | 31,061 |
| `rect_n78_L8955@r1` | 32.77 | 1.233 | 26.6 | 128,911 | 128,895 |
| `rect_n78_L8955@r50` | 46.78 | 1.367 | 34.2 | 132,139 | 131,641 |
| Total | 104.1 | 3.618 | **28.8** |  |  |

Every cell verified by both.
Against exp-001’s v0 on the same cells (about 13 times), the three accepted experiments
more than doubled the ratio.
The smallest ratio is the cell where admission is most of c2’s process; per direction,
without admission, every ratio is above 20. Whole certificates, where admission is paid
once and the axis direction counts, give more (exp-006: 43 on `rect_n32_L595`).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
