---
id: exp-004
title: H-002 cheaper admission cuts a single-direction process by a third
date: "2026-10-02"
hypotheses: [H-002]
decision: accepted
control: v0 (sha256 0cec8849…)
candidate: c1 (v0 plus H-002's admission and the refusal-witness changes, which do not run on a verified cell)
raw: [../results/exp-002-h001-callgrind.jsonl, ../results/exp-003-h006-callgrind.jsonl, ../results/exp-004-h002-cpu.jsonl]
regime: process callgrind counts from exp-002 (v0) and exp-003 (c1); CPU interleaved, two repeats, load average 15.8 to 16.1
---
# H-002: Cheaper Exact Admission

The change skips the coordinates of zero-weight rows, compares rationals with binary64
values by shifting integers instead of building normalized fractions, and reuses each
image’s exact mass. The exact premises checked are unchanged.

| Cell | v0 process instructions | c1 process instructions | Change |
| --- | ---: | ---: | ---: |
| `rect_n32_L595@r1` | 4,045,387,631 | 2,272,142,351 | −43.8% |
| `rect_n32_L595@r100` | 5,136,853,397 | 3,364,577,124 | −34.5% |
| `rect_n61_L796@r100` | 13,575,998,800 | 9,362,404,924 | −31.0% |
| Total | 22.76 G | 15.00 G | **−34.1%** |

CPU guard, total of medians: v0 2.375 s, c1 1.669 s (−30%), ranges disjoint on every
cell. Same verdicts and nodes.

Decision: **accepted**. The measurement was first started at 18:05 and killed by the
container restart; these counts come from the two later rounds that ran the same cells
on each binary, and the CPU guard was run afterwards for this decision.

**What the prediction got wrong.** It predicted at least 30% on the small certificates;
it gave 44% on `n32` and 31% on `n61`, where the search is a larger share.
Admission is still about 40% of `n61`’s single-direction process (the exact D4 merge’s
hashing and normalization of big rationals): a cost per certificate, paid once in a
whole-net run.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
