---
title: "exp-252 — Session 182 lane A: the per-state price of excluding n17 residue states"
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-252
  series: series-000
  title: H-264's seed-182 draw of residue states run through the 17-owner kernel at 32 bins, each closure
    admitted on the standing verifier's full pass
  date: '2026-10-05'
  hypotheses:
  - H-264
  tier: confirmatory
  subject:
    label: The 12 residue orbits survey_n17_residue draws from its arity8 frame with --sample 12 --seed 182
      (2 at distance 2, 7 at 4, 3 at 6 from the endpoint's state; 10 counted), each run as a whole 17-cell
      pattern on the unique-state 24-cell cover at U = 1169/250.
    engine: devtools.check_n17_subpattern (producer and checker) and devtools.verify_n17_kernel_certificate in
      full mode under the kernel-streamed listing, both from the clean run worktree at the session-182
      registration commit; devtools.survey_n17_residue as the float pre-screen
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
    control: The float pre-screen placed the endpoint's own state (its positive control) and no other draw
      (receipts/A/survey-seed182.json). The kernel on the endpoint's own state, which is feasible at U, at a
      2,700 s ceiling must not close; it returned PASS_CERTIFIED_STALL in 333 s (receipts/A/kernel-control-endpoint.json).
    candidate: Each draw's seed and node, re-proved in full by the standing kernel verifier on a closure.
    runs_per_condition: 1
    interleaved: false
    operator: Claude Session 182; the run operator's lane A queue ran the survey, the control and the draws two
      at a time in the survey's own seeded random order, verified each closure and admitted it in the session
      checkout
    entry_point: packing/devtools/check_n17_subpattern.py
    command: 'From packing/ of the run worktree: nice -n 10 timeout -k 120 7600 .venv/bin/python3 -m
      devtools.check_n17_subpattern --cells CELLS17 --bins 32 --max-rounds 24 --hull-limit 16 --max-seconds
      7000 --save-objects DIR --output FILE; on a closure, nice -n 10 timeout -k 120 4000 .venv/bin/python3 -m
      devtools.verify_n17_kernel_certificate --progress --output CERT/verification.json CERT; then
      devtools.census_n17_certified in the session checkout.'
    budget: 7,000 s wall per state and 4,000 s per verification on one worker; lane A at most 26 CPU-hours
    record: packing/campaign/series/series-000-smoke-and-calibration/results/exp-252-n17-overnight-per-state-price
    dirty: false
    commit: cebb5d15aaa17d0cc13aa302ecbd750a54bfc57d
  results:
  - shape: determination
    role: outcome
    question: Is the draw at index 2 (mask 5683195, distance 4) infeasible at U, by a certificate the kernel's
      checker accepts and the standing verifier re-proves in full?
    outcome: criterion_met
    checked_by: The run (receipts/A/kernel-m5683195.json) returns PASS_CERTIFIED_CLOSED in 2,147 s of wall and
      869 s of process CPU (producer 1,366 s, checker 780 s, under contention from other agents' test runs)
      on 135 steps and 4,320 rows in 8 rounds, closure all_parent_poses_forbidden for interior-N at step 134.
      The standing verifier at cebb5d15a passes it in full mode in 676 s, checking all 4,247 live rows in full
      and 13,198 collision regions by 23,720,272 exact facet checks. It excludes its own 8 states, one orbit.
  - shape: determination
    role: outcome
    question: Is the draw at index 4 (mask 2817021, distance 4) excluded within the 7,000 s ceiling?
    outcome: criterion_missed
    checked_by: The run (receipts/A/kernel-m2817021.json) returns PASS_CERTIFIED_STALL in 2,072 s of wall and
      827 s of process CPU, the producer at a fixed point after 11 rounds (187 steps, 5,984 rows), well inside
      its ceiling, so the registered re-run does not apply. A non-closure.
  verdict:
    decision: in-progress
    primary_criterion: At least half of the counted draws excluded within two CPU-hours each, with N1's 7,000 s
      wall ceiling standing in for that limit; falsified by six non-closures of the ten counted.
    reason: Two of the ten counted draws have run, one closed and one did not; the verdict is fixed when five
      close or six do not, and the remaining runs continue for the cost estimate.
  lease:
    expires: '2026-10-06T08:14:04Z'
    host: Session 182 remote container
---
# exp-252: Session 182 Lane A, the Per-State Price

[H-264](../../../hypotheses/H-264-n17-geometric-exclusion-cost-per-leaf.md), as
rewritten in Session 182’s registration, asks what fraction of a seeded draw of residue
orbits the 17-owner kernel excludes by a certificate the standing verifier re-proves,
and at what cost per state.
This round is lane A of the
[n17 overnight plan](../../../../../docs/project/specs/active/plan-2026-10-05-n17-overnight.md)
(BC-419). It is in progress, and gains a row per draw until all twelve have run.

## Per-State Table So Far

| Index | Mask | Distance | Stratum | Outcome | Wall | Process CPU | Verifier |
| --- | --- | --- | --- | --- | ---: | ---: | --- |
| control | 1900015 (endpoint) | 0 | endpoint | stalled, as it must | 333 s | 321 s | — |
| 2 | 5683195 | 4 | c3/i4/d4 | closed, 8 rounds, admitted | 2,147 s | 869 s | full pass, 676 s |
| 4 | 2817021 | 4 | c3/i<=3/d4 | producer fixed point after 11 rounds | 2,072 s | 827 s | — |

With draw 5683195 admitted, the certified census counts 102,116 states in 12,928 orbits,
the endpoint surviving
([census](../results/exp-252-n17-overnight-per-state-price/census.json)).

The draws run in the survey’s own seeded random order (indices 2, 4, 1, 5, 8, 10, 3, 12,
11, 6, 7, 9). The receipt’s `index` field is the stratified draw position, not that
order. Wall exceeds process CPU by about 2.5 times here because other agents’ test runs
held the host at a load near 10; the per-state price is read from process CPU.

The receipts are under
[receipts/A](../../../explorations/X048-session-182-overnight/receipts/A/), the admitted
certificate’s small files under the X048 certificates folder, and its objects in the
[hosted-data manifest](../../../../hosted/n17-x048-session-168-certificates.yaml).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
