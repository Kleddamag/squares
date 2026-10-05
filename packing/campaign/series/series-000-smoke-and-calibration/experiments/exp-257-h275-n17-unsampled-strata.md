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
  results: []
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

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
