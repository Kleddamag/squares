# Measure-Verifier Performance Campaign

**Question.** How much less CPU than the authors’ `verify.cpp` does the clean-room
verifier [`sqverify-fast`](../../sqverify_fast/) need to reach the same verdicts on the
wand125 rectangle-density certificates, and which changes to it earn their keep?

This is lane W2 of the independent fast measure verifier (`think-gpe0`, campaign bead
`think-tgra`). Soundness comes first: [SOUNDNESS.md](../../sqverify_fast/SOUNDNESS.md)
states the lemmas every change must keep, and an experiment whose verdicts differ from
the control’s on any benchmark cell is invalid, whatever its speed.

## Subject and Instance

The subject is one `sqverify-fast` build on this repository’s shared Linux container (4
cores, load average 18 to 33 during series 001, from other lanes), against the unchanged
`verify.cpp` compiled by the replay tool with `g++ -O2 -std=c++17
-fno-fast-math -ffp-contract=off`. The instance axis is the benchmark cell: one standing
certificate at one net direction, threshold $10001/10000$ (the authors’).

The fixed cells, declared in `benchmarks/bench_measure_verifier.py` before any
experiment, are `rect_n32_L595`, `rect_n61_L796` and `rect_n78_L8955` (1,080, 3,000 and
6,496 expanded rectangles) at $r = 1, 50, 100, 150, 200$, and `rect_n95_L98418` at $r =
1, 100, 200$. Direction $r = 0$ is reported separately: the two programs use unrelated
algorithms there and one ratio would swamp the rest.

## Metric Vector

| Metric | Role | Measured by |
| --- | --- | --- |
| Instructions in the direction search (`search_instructions`: inclusive cost of `rotated::verify_direction`), summed over the callgrind cells `n32@r1`, `n32@r100`, `n61@r100` | outcome | `--callgrind` (valgrind `Ir`), independent of load |
| Instructions per process, the same cells | outcome for admission changes; cost otherwise | the same run |
| CPU seconds per process (user plus system, `wait4`), total of per-cell medians | guard | interleaved runs, arm order rotated each repeat |
| Verdict of every cell | guard | must equal the control’s; any difference invalidates the round |
| Nodes per cell | mechanism | the verifier’s receipt |
| Load average before and after each run | regime | `/proc/loadavg` |

Wall time is recorded and never decides: the host’s load stayed above 6 throughout.

## Accept Rule

Declared 2026-10-02T18:01Z, after exp-002’s instruction counts for H-001 had been seen
and before any other candidate was measured; the outcome metric was narrowed to the
search’s own instructions at 19:55Z, after exp-002 showed that admission diluted process
totals, and before exp-003 was measured.
A candidate is **accepted** when, against its control (the standing best build):

1. every benchmark cell it ran has the control’s verdict;
2. its outcome metric (the search’s instructions, or the process’s for a change to
   admission) is at least 10% lower; and
3. its CPU total of medians, over at least two interleaved repeats of the cells both
   ran, is not higher than the control’s.

Otherwise it is **rejected** and reverted, and recorded either way.
Clause 3 is a guard against an instruction count that buys nothing on the hardware; it
does not let a CPU reading override the instruction count, since the load makes CPU time
noisy. The one judgment written beside the arithmetic is whether a change is worth its
complexity.

## Runbook

1. Build the candidate (`cargo build --release` in `packing/sqverify_fast`) and copy the
   binary aside under a label.
2. From `packing/`, run the callgrind cells for control and candidate:
   `python -m benchmarks.bench_measure_verifier --arm fast:control=PATH --arm
   fast:candidate=PATH --callgrind --repeats 1 --cells
   rect_n32_L595@r1,rect_n32_L595@r100,rect_n61_L796@r100 --out results/exp-NNN-cg.jsonl`.
3. Run the CPU cells, interleaved: the same with `--repeats 2` and no `--callgrind`.
4. Apply the accept rule; write `experiments/exp-NNN-*.md` with the numbers lifted from
   the JSONL, and commit the raw results with it.
5. For the headline comparison against `verify.cpp`, replay whole certificates:
   `python -m benchmarks.bench_measure_verifier --arm fast:candidate=PATH --arm
   verify-cpp --whole rect_n32_L595,rect_n31_L592 --out results/whole.jsonl`. Both arms
   then do all 201 directions on one worker, `verify.cpp` through the replay tool’s
   `--replay --workers 1` (its CPU includes the tool’s exact preflight and the compile,
   a few seconds). Per-direction cells against `verify.cpp` use `--arm
   verify-cpp` without `--whole`. The replay tool’s control mode refuses some directions
   before running the checker (its mutation premise does not hold there); those cells
   have no reference reading.

The coordinator runs the headline comparison on a dedicated idle runner with the same
script; this campaign’s CPU readings were taken under load and are the ratio’s local
estimate only.

## Records

- [ideas.md](ideas.md): the idea board.
- [hypotheses/](hypotheses/): one claim each.
- [experiments/](experiments/): one round each, failures included.
- [results/](results/): the raw JSONL of every round.
- [census/](census/): Milestone A, every replayed certificate at all 201 directions
  ([its generated table](census/README.md)), and `controls-c2.txt`, the full
  differential and mutation-control check of the build that ran it.

## Standing Results

The standing build is c2 (exp-003, exp-004 and exp-005 accepted on v0). On this loaded
host it used 43 times less CPU than `verify.cpp` on the whole of `rect_n32_L595`
(exp-006) and 29 times less on six single directions (exp-011). Six hypotheses were
rejected: H-001, H-005, H-008, H-004, H-009 and H-010. The two first-leg rounds found a
real 27 to 37% cut in boxes that costs as much again in enclosures; it is the most
promising open lead.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
