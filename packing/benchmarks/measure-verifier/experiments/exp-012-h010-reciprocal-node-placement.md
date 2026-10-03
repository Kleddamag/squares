---
id: exp-012
title: H-010 reciprocal node placement changes nothing measurable
date: "2026-10-02"
hypotheses: [H-010]
decision: rejected
control: c2 (sqverify-fast-c2)
candidate: c2 with node placement by multiplication with per-direction reciprocals (sqverify-fast-h010)
raw: [../results/exp-012-h010-callgrind.jsonl, ../results/exp-012-h010-cpu.jsonl]
regime: callgrind counts; CPU interleaved, three repeats, load average 3.2 to 3.3 (the quietest window of the day)
---
# H-010: Reciprocal Node Placement

Search instructions were identical on every cell (4.751 G in both arms): a division is
one instruction, as is the multiplication replacing it.
CPU, total of medians over `n32@r1`, `n32@r100`, `n61@r100`, `n78@r100`: c2 2.863 s,
H-010 2.946 s, with overlapping ranges on every cell.
Same verdicts and nodes.

Decision: **rejected** and reverted; no detectable effect.

**What the prediction got wrong.** The divisions’ latency is hidden behind the
independent work around them; the area bound is bound by its dependent chains of
outward-rounded operations, not by its divides.
This also shows a blind spot of the instruction-count metric, which cannot see latency
effects in either direction, so a change aimed at latency needs the CPU guard as its
outcome, not as a guard.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
