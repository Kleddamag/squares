---
id: exp-001
title: Baseline, the first sound build (v0) beside verify.cpp
date: "2026-10-02"
hypotheses: []
decision: baseline
control: verify.cpp through `devtools.audit_wand125_rectangles --control`
candidate: sqverify-fast v0, binary sha256 0cec8849cd988ecbb180f3923e874e104fceeb943d8e42ffea905a718d48b27d
raw: ../results/exp-001-baseline-v0-and-verify-cpp.jsonl
regime: shared 4-core container, load average 18 to 33, one repeat, interrupted by a container restart after 25 rows
---
# Baseline: v0 Beside verify.cpp

The first sound build, timed beside the authors’ checker on the fixed cells before any
optimization. CPU is the child process’s user plus system time from `wait4`; for
`verify.cpp` it is the checker process alone, as the replay tool measured it, so its
input generation and compilation are not charged to it.
v0’s process time includes exact admission (about 0.15 s for `n32` and 0.5 s for `n78`),
which `verify.cpp` does not perform.

| Cell | verify.cpp CPU s | verify.cpp boxes | v0 CPU s | v0 boxes | Ratio |
| --- | ---: | ---: | ---: | ---: | ---: |
| `rect_n32_L595@r1` | 1.697 | 15,387 | 0.300 | 15,397 | 5.7 |
| `rect_n32_L595@r100` | 4.628 | 25,041 | 0.373 | 24,525 | 12.4 |
| `rect_n32_L595@r150` | 5.850 | 28,541 | 0.438 | 27,725 | 13.4 |
| `rect_n32_L595@r200` | 6.712 | 32,183 | 0.492 | 31,061 | 13.6 |
| `rect_n78_L8955@r1` | 23.744 | 128,911 | 1.837 | 128,895 | 12.9 |
| `rect_n78_L8955@r50` | 36.025 | 132,139 | 2.097 | 131,641 | 17.2 |

Both programs verified every cell.
Node counts agree within 4%: the two bounds are of the same kind (first-order, centre
value minus derivative times half-width), arrived at independently.

**What the instrument got wrong.** The replay tool’s control mode runs `verify.cpp` only
when its mutation premise holds at the requested direction (the scaled certificate must
leave the witness below one); at `n32@r50` and at every `n61` cell it refused before
running the checker, so those cells have no reference reading.
The reference arm needs either directions where the premise holds or a direct
single-direction replay command.
The coordinator’s idle-runner comparison and lane W1’s
[`timings.json`](../../results/author-checker-profile-2026-10-02/timings.json) (297 to
533 µs per box for `verify.cpp` on `rect_n20_L48975`) are the other references.

**Axis direction.** Not in the cells: v0’s exact-event sweep evaluates `n32`’s 940,900
vertices in 0.09 s of CPU and `n78`’s 2,039,184 in about 0.55 s, where the upstream rows
record 316 s and 3,338 s for `verify.cpp`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
