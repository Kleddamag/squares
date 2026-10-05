---
title: "exp-251 — Session 182 lane K: the heaviest standing n17 flags under the adaptive-row kernel"
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-251
  series: series-000
  title: The arity-7 standing flags with the most census weight, run through the kernel under SW9's adaptive-row
    recipe at cap 1169/250, each closure admitted on the standing verifier's full pass
  date: '2026-10-05'
  hypotheses:
  - H-267
  tier: confirmatory
  subject:
    label: The nine arity-7 standing flags with at least three wall or corner cells and best penetration at
      least 5e-3, in projected-gain order (packing/campaign/explorations/X048-session-182-overnight/kernel-targets.txt),
      on the unique-state 24-cell cover at U = 1169/250.
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
    control: The endpoint7 pattern (the endpoint's own west-wall cells, feasible at U) under the same recipe at
      a 3,600 s ceiling must not close; it returned PASS_CONTROL_STALLED in 1,244 s (receipts/K/kernel-control-endpoint7.json).
      The endpoint's state must survive every admitted entry, which the census checks.
    candidate: Each frozen target's seed and node, re-proved in full by the standing kernel verifier.
    runs_per_condition: 1
    interleaved: false
    operator: Claude Session 182; the run operator's lane K queue produced and verified each certificate and
      admitted it in the session checkout
    entry_point: packing/devtools/check_n17_subpattern.py
    command: 'From packing/ of the run worktree: nice -n 10 timeout -k 120 7600 .venv/bin/python3 -m
      devtools.check_n17_subpattern --cells CELLS --bins 64 --max-rounds 24 --hull-limit 16 --producer-share
      0.6 --split-floor 512 --max-rows 1152 --split-patience 1 --max-seconds 7000 --save-objects DIR --output
      FILE; on a closure, nice -n 10 timeout -k 120 4000 .venv/bin/python3 -m devtools.verify_n17_kernel_certificate
      --progress --output CERT/verification.json CERT; then devtools.census_n17_certified in the session
      checkout.'
    budget: 7,000 s per kernel target and 4,000 s per verification on one worker; lane K's kernel budget at most
      17 CPU-hours
    record: packing/campaign/series/series-000-smoke-and-calibration/results/exp-251-n17-overnight-flag-certification
    dirty: false
    commit: cebb5d15aaa17d0cc13aa302ecbd750a54bfc57d
  results:
  - shape: determination
    role: outcome
    question: Is target 1 (side-S0, side-N0, side-S1, interior-SW, interior-NW, interior-W, interior-S) infeasible
      at U, by a certificate the kernel's checker accepts and the standing verifier re-proves in full?
    outcome: criterion_met
    checked_by: The run (receipts/K/kernel-k1.json) returns PASS_CERTIFIED_CLOSED in 305 s of wall (276 s
      of process CPU; producer 155 s, checker 149 s) on 27 steps and 1,728 rows in 4 rounds, finest row 1/64,
      closure all_parent_poses_forbidden for interior-W at step 26. The standing verifier at cebb5d15a passes
      it in full mode in 173 s, checking all 1,664 live rows in full and 4,132 collision regions by 23,294,320
      exact facet checks, the closure re-derived. Alone it excludes 116,160 states and 14,590 orbits.
  - shape: determination
    role: guard
    question: Do the certified exclusions leave at most 10^4 orbits, H-267's threshold?
    outcome: criterion_missed
    checked_by: With s182-k1 admitted, census_n17_certified counts 102,124 states and 12,929 orbits, the
      endpoint surviving, down from 126,168 and 15,953 at the registration (results/exp-251-n17-overnight-flag-certification/census.json).
      The same tool on a copy of the ledger restricted to the arity-at-most-7 entries (W7, A, s182-k1) counts
      14,477 orbits, down from exp-249's 17,690, against the threshold of 10^4. The census file was re-run
      at 27b787a1c, where the census reads the selector recheck; 86 flags still project, and certifying
      them all would leave 17,168 states in 2,197 orbits.
  verdict:
    decision: in-progress
    primary_criterion: The certified residue is at most 10^4 orbits with every certificate independently
      checked; rejected if it exceeds 10^4 at arity seven or a certificate excludes the endpoint state.
    reason: Lane K's round is running; each closure is admitted as its verifier passes, and the verdict is
      written when the target list is exhausted.
  lease:
    expires: '2026-10-06T08:14:04Z'
    host: Session 182 remote container
---
# exp-251: Session 182 Lane K, the Heaviest Standing Flags

[H-267](../../../hypotheses/H-267-n17-isolated-sub-pattern-residue.md) asks whether
certified sub-patterns of arity at most seven leave at most $10^4$ orbits on the
unique-state cover. This round is lane K of the
[n17 overnight plan](../../../../../docs/project/specs/active/plan-2026-10-05-n17-overnight.md)
(BC-420): the nine arity-7 standing flags with the most census weight, run through the
kernel with the adaptive-row recipe that closed SW9, which they had never had.

The round is in progress.
Each closure is admitted as soon as the standing verifier passes it in full from the
clean run worktree, and this record gains a result per target until the list is
exhausted.

## Admitted So Far

| Target | Cells | Producer | Verifier | Census after |
| --- | --- | --- | --- | --- |
| 1, `s182-k1` | side-S0, side-N0, side-S1, interior-SW, interior-NW, interior-W, interior-S | closed in 305 s, 27 steps, 1,728 rows | full pass, 173 s | 102,124 states, 12,929 orbits |

At the margin `s182-k1` removes 24,044 states and 3,024 orbits from the certified count,
exactly the census’s projected gain for that flag.
The receipts are under
[receipts/K](../../../explorations/X048-session-182-overnight/receipts/K/), the
certificate’s small files under the X048 certificates folder, and its objects in the
[hosted-data manifest](../../../../hosted/n17-x048-session-168-certificates.yaml).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
