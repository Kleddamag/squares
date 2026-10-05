---
title: "exp-253 — Session 182 BC-424: lane A's counted n17 stalls under the adaptive-row kernel"
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-253
  series: series-000
  title: H-274's four frozen lane A stalls run as whole 17-cell patterns under SW9's adaptive-row kernel
    recipe at cap 1169/250, each closure admitted on the standing verifier's full pass
  date: '2026-10-05'
  hypotheses:
  - H-274
  tier: confirmatory
  subject:
    label: The four counted draws of H-264's seed-182 draw that had stalled under N1's recipe by H-274's
      registration (masks 2784767, 2817021, 2878207 and 3063677, at distances 4, 4, 6 and 4 from the
      endpoint's state), each run as a whole 17-cell pattern on the unique-state 24-cell cover at U = 1169/250.
    engine: devtools.check_n17_subpattern (producer and checker) and devtools.verify_n17_kernel_certificate in
      full mode under the kernel-streamed listing, both from the clean run worktree at the session-182
      registration commit
    assurance: verified
    method: exact-algebraic
    host_system: Linux x86_64 remote session container, project Python 3.14.7, one worker per job at nice 10
    selftest_passed: true
    engine_commit: cebb5d15aaa17d0cc13aa302ecbd750a54bfc57d
  instance:
    axis: n
    point: 17
    role: target
  method:
    control: The kernel on the endpoint's own state, which is feasible at U, under the same recipe at the
      7,000 s ceiling must not close. It ran beside the first state, and no closure was admitted before it
      finished. It returned PASS_CERTIFIED_STALL in 6,599 s of wall and 6,299 s of process CPU, the producer
      at its 24-round cap on 408 steps and 27,520 rows, finest 1/128, excluding nothing
      (receipts/A/kernel-control-endpoint-sw9.json).
    candidate: Each frozen state's seed and node, re-proved in full by the standing kernel verifier on a closure.
    runs_per_condition: 1
    interleaved: false
    operator: Claude Session 182; the run operator's BC-424 queue ran the control beside the first state and the
      states two at a time in mask order, verified each closure, and admitted it in the session checkout once
      the control had finished without closing
    entry_point: packing/devtools/check_n17_subpattern.py
    command: 'From packing/ of the run worktree: nice -n 10 timeout -k 120 7600 .venv/bin/python3 -m
      devtools.check_n17_subpattern --cells CELLS17 --bins 64 --max-rounds 24 --hull-limit 16 --producer-share
      0.6 --split-floor 512 --max-rows 1152 --split-patience 1 --max-seconds 7000 --save-objects DIR --output
      FILE; on a closure, nice -n 10 timeout -k 120 4000 .venv/bin/python3 -m devtools.verify_n17_kernel_certificate
      --progress --output CERT/verification.json CERT; then devtools.census_n17_certified in the session
      checkout.'
    budget: 7,000 s per state and for the control and 4,000 s per verification, one worker each; about 10
      CPU-hours at most
    record: packing/campaign/series/series-000-smoke-and-calibration/results/exp-253-n17-stalls-under-adaptive-rows
    dirty: false
    commit: cebb5d15aaa17d0cc13aa302ecbd750a54bfc57d
  results:
  - shape: determination
    role: outcome
    question: Is the state with mask 2784767 (lane A's draw at index 10, distance 4, stalled under N1's recipe)
      infeasible at U, by a certificate the kernel's checker accepts and the standing verifier re-proves in
      full?
    outcome: criterion_met
    checked_by: The run (receipts/A/kernel-m2784767-sw9.json) returns PASS_CERTIFIED_CLOSED in 1,761 s of wall
      and 1,675 s of process CPU (producer 939 s, checker 820 s) on 114 steps and 7,610 rows in 7 rounds,
      rows finest at 1/128, closure all_parent_poses_forbidden for side-S2 at step 113. The standing verifier
      at cebb5d15a passes it in full mode in 782 s, checking all 7,420 live rows in full and 20,918 collision
      regions by 113,168,864 exact facet checks. It excludes its own 8 states, one orbit. Under N1's recipe
      the same state reached a producer fixed point after 828 s of process CPU (exp-252).
  - shape: determination
    role: outcome
    question: Is the state with mask 2817021 (lane A's draw at index 4, distance 4, stalled under N1's recipe)
      infeasible at U, by a certificate the kernel's checker accepts and the standing verifier re-proves in
      full?
    outcome: criterion_met
    checked_by: The run (receipts/A/kernel-m2817021-sw9.json) returns PASS_CERTIFIED_CLOSED in 2,154 s of wall
      and 2,100 s of process CPU (producer 1,133 s, checker 1,020 s) on 134 steps and 8,960 rows in 8 rounds,
      rows finest at 1/128, closure all_parent_poses_forbidden for interior-NW at step 133. The standing
      verifier at cebb5d15a passes it in full mode in 911 s, checking all 8,707 live rows in full and 25,457
      collision regions by 136,159,832 exact facet checks. It excludes its own 8 states, one orbit. Under N1's
      recipe the same state reached a producer fixed point after 828 s of process CPU (exp-252).
  - shape: determination
    role: outcome
    question: Is the state with mask 2878207 (lane A's draw at index 8, distance 6, stalled under N1's recipe)
      infeasible at U, by a certificate the kernel's checker accepts and the standing verifier re-proves in
      full?
    outcome: criterion_met
    checked_by: The run (receipts/A/kernel-m2878207-sw9.json) returns PASS_CERTIFIED_CLOSED in 901 s of wall
      and 875 s of process CPU (producer 464 s, checker 436 s) on 61 steps and 4,022 rows in 4 rounds, rows
      finest at 1/128, closure all_parent_poses_forbidden for side-E1 at step 60. The standing verifier at
      cebb5d15a passes it in full mode in 421 s, checking all 4,022 live rows in full and 11,385 collision
      regions by 63,401,908 exact facet checks. It excludes its own 8 states, one orbit. Under N1's recipe the
      same state reached a producer fixed point after 925 s of process CPU (exp-252).
  verdict:
    decision: accepted
    primary_criterion: At least two of the four frozen states close within the 7,000 s ceiling, each re-proved
      in full by the standing kernel verifier; rejected if fewer than two do, and void if the endpoint-state
      control closes.
    reason: >-
      The first two frozen states, 2784767 and 2817021, closed within the ceiling under
      SW9's recipe, each re-proved in full by the standing kernel verifier and admitted
      after the endpoint-state control finished without closing, which meets the
      criterion of two. Both had reached producer fixed points under N1's recipe. The
      third, 2878207, closed after the verdict too; the fourth, 3063677, runs on for the
      cost. Held for the W2 review the plan requires before X-048 or the frontier states
      the verdict.
    needs_review: true
    commit: 3396efda0
  effort:
    timebox: 7,000 s per state and for the control, 4,000 s per verification, one worker each
    wall_seconds: 6601
    stopped_by: criterion
---
# exp-253: Session 182 BC-424, Lane A’s Stalls Under Adaptive Rows

[H-274](../../../hypotheses/H-274-n17-per-state-closure-under-adaptive-rows.md) asks
whether the residue states that stalled under N1’s recipe in
[exp-252](exp-252-h264-n17-overnight-per-state-price.md) close under the adaptive-row
recipe that closed SW9 and eight of lane K’s nine arity-7 flags.
This round is BC-424 of
[agenda-042](../../../agendas/agenda-042-overnight-n11-settlement-and-low-n-angles.md),
registered at a check-in with the four counted stalls that existed then.
[Lane D’s stall classification](../../../../../docs/project/reviews/review-2026-10-05-n17-stall-classification.md)
gives the mechanism.
The distance-4 stalls share a north-wall knot whose cut margins, about 0.011 to 0.015,
sit below the first-order losses of 32 uniform bins but above a cut at the 1/512 split
floor.

The control and the first state ran side by side, and admission, not launch, waited for
the control. Session 182 changed to that procedure after its second container restart;
its record gives the reason.
Each closed state removes only its own orbit.

H-274 is accepted on its first two states and held for a W2 review.
Both closed with their finest rows at 1/128, so neither needed rows as fine as the 1/512
split floor. The round’s wall, 6,601 s, runs from the launch at 14:19:55 UTC to the
control’s end, which released both closures.
Two earlier launches of the control and the first state were killed by container
restarts without receipts and are not counted.
The third state, 2878207, closed after the verdict in 875 s of CPU; the fourth runs on
for the cost.

## Runs

| Mask | Distance | Under N1’s recipe (exp-252) | Under SW9’s recipe | Process CPU | Verifier |
| --- | --- | --- | --- | --- | --- |
| control | 0 | stalled in 333 s | 24-round cap, not closed | 6,299 s | — |
| 2784767 | 4 | fixed point, 828 s | closed, 7 rounds, admitted | 1,675 s | full pass, 782 s |
| 2817021 | 4 | fixed point, 828 s | closed, 8 rounds, admitted | 2,100 s | full pass, 911 s |
| 2878207 | 6 | fixed point, 925 s | closed, 4 rounds, admitted after the verdict | 875 s | full pass, 421 s |

The receipts are under
[receipts/A](../../../explorations/X048-session-182-overnight/receipts/A/), each
certificate’s small files under the X048 certificates folder, and its objects in the
[hosted-data manifest](../../../../hosted/n17-x048-session-168-certificates.yaml).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
