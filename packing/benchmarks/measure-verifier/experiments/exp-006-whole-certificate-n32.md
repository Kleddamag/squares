---
id: exp-006
title: Whole rect_n32_L595, c2 against verify.cpp, 43 times less CPU
date: "2026-10-02"
hypotheses: []
decision: baseline
control: verify.cpp through `devtools.audit_wand125_rectangles --replay --workers 1`
candidate: c2 (sqverify-fast-c2), `--directions all --threads 1`
raw: ../results/exp-006-whole-n32.jsonl
regime: shared 4-core container, load average 10.1 to 11.4 (two other runs of this lane beside it), one run each
---
# Whole `rect_n32_L595`: c2 Against verify.cpp

The headline comparison, local estimate: both programs check all 201 directions of the
same certificate on one worker each.

| Arm | CPU s | Wall s | Verdict | Nodes |
| --- | ---: | ---: | --- | ---: |
| `verify.cpp`, replay tool, one worker | 1,456.9 | 2,012.8 | PASS | 5,808,912 (940,900 of them axis vertices) |
| `sqverify-fast` c2, one thread | 33.7 | 44.6 | VERIFIED | 4,753,696 boxes plus 940,900 axis vertices |

**Ratio 43.2 in CPU.** The `verify.cpp` figure includes the replay tool’s exact
preflight and compile, a few seconds; c2’s includes its exact admission, under a second.
The axis direction took `verify.cpp` 395.7 s of wall time and c2 0.07 s of CPU; without
it the ratio on the 200 rotated directions is still above 30.

This is a baseline, not an experiment: no hypothesis was tested.
The figure was taken under load and is the campaign’s local estimate; the coordinator’s
idle-runner run of `bench_measure_verifier.py --headline` is the one to quote.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
