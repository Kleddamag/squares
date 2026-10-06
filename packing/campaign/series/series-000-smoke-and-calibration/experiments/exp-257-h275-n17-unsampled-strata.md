---
title: "exp-257 — Session 182 BC-428: n17 residue states from the strata H-264's draw never reached"
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-257
  series: series-000
  title: A seeded draw of 31 residue states from the 21 unsampled strata of the arity8 frame, run as whole
    17-cell patterns under SW9's frozen adaptive-row kernel recipe, each closure admitted on the standing
    verifier's full pass
  date: '2026-10-05'
  hypotheses:
  - H-275
  tier: exploratory
  subject:
    label: The 31 states frozen in packing/campaign/explorations/X048-session-182-overnight/kernel-targets-bc428.txt,
      one from each of the 21 strata of survey_n17_residue's arity8 frame that H-264's seed-182 draw never
      reached and a second from each of the ten larger than the mean, each run as a whole 17-cell pattern on
      the unique-state 24-cell cover at U = 1169/250.
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
    control: BC-424's endpoint-state control under the same recipe, the endpoint's own state and feasible at U,
      returned PASS_CERTIFIED_STALL at its 24-round cap in 6,599 s (receipts/A/kernel-control-endpoint-sw9.json),
      and lane K's endpoint7 control returned PASS_CONTROL_STALLED (receipts/K/kernel-control-endpoint7.json).
      This round runs that recipe unchanged, so no new control runs. The endpoint's state must survive every
      admitted entry, which the census checks.
    candidate: Each frozen state's seed and node, re-proved in full by the standing kernel verifier on a closure.
    runs_per_condition: 1
    interleaved: false
    operator: Claude Session 182; the run operator's BC-428 queue runs the states in the frozen order on two
      workers, verifies each closure, and admits it in the session checkout
    entry_point: packing/devtools/check_n17_subpattern.py
    command: 'From packing/ of the run worktree: nice -n 10 timeout -k 120 7600 .venv/bin/python3 -m
      devtools.check_n17_subpattern --cells CELLS17 --bins 64 --max-rounds 24 --hull-limit 16 --producer-share
      0.6 --split-floor 512 --max-rows 1152 --split-patience 1 --max-seconds 7000 --save-objects DIR --output
      FILE; on a closure, nice -n 10 timeout -k 120 4000 .venv/bin/python3 -m devtools.verify_n17_kernel_certificate
      --progress --output CERT/verification.json CERT; then devtools.census_n17_certified in the session
      checkout.'
    budget: 7,000 s per state and 4,000 s per verification on one worker, two workers, until 2026-10-06T07:14:04Z
    record: packing/campaign/series/series-000-smoke-and-calibration/results/exp-257-n17-unsampled-strata
    dirty: false
    commit: cebb5d15aaa17d0cc13aa302ecbd750a54bfc57d
  results:
  - shape: determination
    role: outcome
    question: Is draw 2 (mask 4061102, stratum c3/i>=5/d4) infeasible at U, by a certificate the kernel's checker
      accepts and the standing verifier re-proves in full?
    outcome: criterion_met
    checked_by: The run (receipts/U/kernel-u2-bc428.json) returns PASS_CERTIFIED_CLOSED in 1,891 s of wall and 1,231 s
      of process CPU (producer 1,229 s, checker 660 s) on 56 steps and 3,712 rows in 4 rounds, rows finest at
      1/128, closure all_parent_poses_forbidden for side-E0 at step 55. The standing verifier at cebb5d15a
      passes it in full mode in 560 s, checking all 3,712 live rows in full and 13,050 collision regions by
      73,627,372 exact facet checks. It excludes its own 8 states, one orbit; the certified census after it is
      36,980 states in 4,710 orbits.
  - shape: determination
    role: outcome
    question: Is draw 3 (mask 4439807, stratum c4/i<=3/d>=8) infeasible at U, by a certificate the kernel's checker
      accepts and the standing verifier re-proves in full?
    outcome: criterion_met
    checked_by: The run (receipts/U/kernel-u3-bc428.json) returns PASS_CERTIFIED_CLOSED in 1,218 s of wall and 1,174 s
      of process CPU (producer 688 s, checker 529 s) on 95 steps and 6,336 rows in 6 rounds, rows finest at
      1/128, closure all_parent_poses_forbidden for side-W1 at step 94. The standing verifier at cebb5d15a
      passes it in full mode in 472 s, checking all 6,004 live rows in full and 16,200 collision regions by
      76,354,712 exact facet checks. It excludes its own 8 states, one orbit; the certified census after it is
      36,972 states in 4,709 orbits.
  - shape: determination
    role: outcome
    question: Is draw 4 (mask 6020797, stratum c3/i>=5/d6) infeasible at U, by a certificate the kernel's checker
      accepts and the standing verifier re-proves in full?
    outcome: criterion_met
    checked_by: The run (receipts/U/kernel-u4-bc428.json) returns PASS_CERTIFIED_CLOSED in 749 s of wall and 726 s of
      process CPU (producer 385 s, checker 362 s) on 49 steps and 3,200 rows in 3 rounds, rows finest at
      1/128, closure all_parent_poses_forbidden for interior-S at step 48. The standing verifier at cebb5d15a
      passes it in full mode in 312 s, checking all 3,200 live rows in full and 9,625 collision regions by
      50,455,248 exact facet checks. It excludes its own 8 states, one orbit; the certified census after it is
      36,964 states in 4,708 orbits.
  - shape: determination
    role: outcome
    question: Is draw 5 (mask 3931626, stratum c<=2/i>=5/d6) infeasible at U, by a certificate the kernel's checker
      accepts and the standing verifier re-proves in full?
    outcome: criterion_met
    checked_by: The run (receipts/U/kernel-u5-bc428.json) returns PASS_CERTIFIED_CLOSED in 1,221 s of wall and 1,135 s
      of process CPU (producer 581 s, checker 639 s) on 59 steps and 3,904 rows in 4 rounds, rows finest at
      1/128, closure all_parent_poses_forbidden for side-E1 at step 58. The standing verifier at cebb5d15a
      passes it in full mode in 563 s, checking all 3,897 live rows in full and 12,929 collision regions by
      74,192,232 exact facet checks. It excludes its own 8 states, one orbit; the certified census after it is
      36,956 states in 4,707 orbits.
  - shape: determination
    role: outcome
    question: Is draw 1 (mask 1900509, stratum c3/i<=3/d2) (distance 2, reported apart) excluded within the 7,000 s
      ceiling?
    outcome: criterion_missed
    checked_by: The run (receipts/U/kernel-u1-bc428.json) returns INCOMPLETE in 7,001 s of wall and 6,101 s of process
      CPU (capture row wall ceiling). Not a closure; nothing is concluded from it, and its saved node is kept.
  - shape: determination
    role: outcome
    question: Is draw 6 (mask 5491711, stratum c4/i4/d>=8) excluded within the 7,000 s ceiling?
    outcome: criterion_missed
    checked_by: The run (receipts/U/kernel-u6-bc428.json) returns PASS_CERTIFIED_STALL in 2,009 s of wall and 1,863 s of
      process CPU, the producer at a fixed point after 15 rounds (255 steps, 17,152 rows, finest 1/128),
      inside its ceiling. A non-closure; its node is kept.
  - shape: determination
    role: outcome
    question: Is draw 7 (mask 5959674, stratum c<=2/i4/d6) infeasible at U, by a certificate the kernel's checker
      accepts and the standing verifier re-proves in full?
    outcome: criterion_met
    checked_by: The run (receipts/U/kernel-u7-bc428.json) returns PASS_CERTIFIED_CLOSED in 1,606 s of wall and 1,475 s
      of process CPU (producer 790 s, checker 812 s) on 79 steps and 5,248 rows in 5 rounds, rows finest at
      1/128, closure all_parent_poses_forbidden for side-N2 at step 78. The standing verifier at cebb5d15a
      passes it in full mode in 714 s, checking all 5,160 live rows in full and 16,556 collision regions by
      93,568,844 exact facet checks. It excludes its own 8 states, one orbit; the certified census after it is
      36,948 states in 4,706 orbits.
  - shape: determination
    role: outcome
    question: Is draw 8 (mask 3078077, stratum c3/i4/d2) (distance 2, reported apart) infeasible at U, by a
      certificate the kernel's checker accepts and the standing verifier re-proves in full?
    outcome: criterion_met
    checked_by: The run (receipts/U/kernel-u8-bc428.json) returns PASS_CERTIFIED_CLOSED in 622 s of wall and 572 s of
      process CPU (producer 315 s, checker 306 s) on 44 steps and 2,880 rows in 3 rounds, rows finest at
      1/128, closure all_parent_poses_forbidden for side-S2 at step 43. The standing verifier at cebb5d15a
      passes it in full mode in 277 s, checking all 2,880 live rows in full and 9,094 collision regions by
      52,565,640 exact facet checks. It excludes its own 8 states, one orbit; the certified census after it is
      36,940 states in 4,705 orbits.
  verdict:
    decision: in-progress
    primary_criterion: The fraction of the frozen states the kernel excludes under SW9's recipe within the 7,000 s
      ceiling, each closure re-proved in full by the standing kernel verifier with the endpoint surviving, and
      the cost per state; the distance-2 draws reported apart.
    reason: Registered before its first run; each closure is admitted as its verifier passes, and the verdict is
      written when the list is exhausted or the deadline arrives.
  lease:
    expires: '2026-10-06T08:14:04Z'
    host: Session 182 remote container
---
# exp-257: Session 182 BC-428, H-264’s Unsampled Strata

[H-275](../../../hypotheses/H-275-n17-unsampled-strata-per-state-price.md) asks what
per-state exclusion costs in the 21 strata of the arity8 frame that
[exp-252](exp-252-h264-n17-overnight-per-state-price.md) reported as unsampled, 827
orbits that H-264 did not price.
This round is BC-428 of
[agenda-042](../../../agendas/agenda-042-overnight-n11-settlement-and-low-n-angles.md).
It runs the states under the adaptive-row recipe that closed all four of H-264’s counted
stalls in [exp-253](exp-253-h274-n17-stalls-under-adaptive-rows.md).

The draw is seeded and frozen before the first run: one state per stratum, and a second
from each of the ten strata larger than the mean of 827/21 orbits.
The run order puts every stratum’s first state before any second.
[draw-bc428.cmd.txt](../../../explorations/X048-session-182-overnight/receipts/U/draw-bc428.cmd.txt)
writes the draw from the frame listing and the seed-182 receipt.
Each closed state removes only its own orbit.
The two distance-2 states are reported apart, and any state not run by the deadline is
reported as not run.

## Runs

| Order | Stratum | Mask | Outcome | Process CPU | Verifier |
| --- | --- | --- | --- | --- | --- |
| 2 | c3/i>=5/d4 | 4061102 | closed, 4 rounds, admitted | 1,231 s | full pass, 560 s |
| 3 | c4/i<=3/d>=8 | 4439807 | closed, 6 rounds, admitted | 1,174 s | full pass, 472 s |
| 4 | c3/i>=5/d6 | 6020797 | closed, 3 rounds, admitted | 726 s | full pass, 312 s |
| 5 | c<=2/i>=5/d6 | 3931626 | closed, 4 rounds, admitted | 1,135 s | full pass, 563 s |
| 1 | c3/i<=3/d2 (d2) | 1900509 | incomplete at 7,001 s | 6,101 s | — |
| 6 | c4/i4/d>=8 | 5491711 | fixed point after 15 rounds, not closed | 1,863 s | — |
| 7 | c<=2/i4/d6 | 5959674 | closed, 5 rounds, admitted | 1,475 s | full pass, 714 s |
| 8 | c3/i4/d2 (d2) | 3078077 | closed, 3 rounds, admitted | 572 s | full pass, 277 s |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
