---
title: "exp-254 — Session 182 BC-425: lane K's second tranche of n17 flags under the adaptive-row kernel"
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-254
  series: series-000
  title: The next ten standing flags by projected gain, arity at most 8, run through the kernel under lane K's
    frozen SW9 recipe at cap 1169/250, each closure admitted on the standing verifier's full pass
  date: '2026-10-05'
  hypotheses:
  - H-267
  tier: exploratory
  subject:
    label: The ten standing flags frozen in packing/campaign/explorations/X048-session-182-overnight/kernel-targets-bc425.txt,
      lane K's filter widened only in arity (at most 8 cells, at least three wall or corner cells, best
      penetration at least 5e-3) on the census at 18b7c5ae1, in projected-gain order; all ten are arity 8,
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
    control: Lane K's endpoint7 control under the same recipe, the endpoint's own west-wall cells and feasible
      at U, returned PASS_CONTROL_STALLED in 1,244 s (receipts/K/kernel-control-endpoint7.json) and covers this
      tranche, which runs that recipe unchanged; no new control runs. The endpoint's state must survive every
      admitted entry, which the census checks.
    candidate: Each frozen target's seed and node, re-proved in full by the standing kernel verifier.
    runs_per_condition: 1
    interleaved: false
    operator: Claude Session 182; the run operator's BC-425 queue produced and verified each certificate on one
      slot and then two, and admitted each closure in the session checkout
    entry_point: packing/devtools/check_n17_subpattern.py
    command: 'From packing/ of the run worktree: nice -n 10 timeout -k 120 7600 .venv/bin/python3 -m
      devtools.check_n17_subpattern --cells CELLS --bins 64 --max-rounds 24 --hull-limit 16 --producer-share
      0.6 --split-floor 512 --max-rows 1152 --split-patience 1 --max-seconds 7000 --save-objects DIR --output
      FILE; on a closure, nice -n 10 timeout -k 120 4000 .venv/bin/python3 -m devtools.verify_n17_kernel_certificate
      --progress --output CERT/verification.json CERT; then devtools.census_n17_certified in the session
      checkout.'
    budget: 7,000 s per target and 4,000 s per verification on one worker
    record: packing/campaign/series/series-000-smoke-and-calibration/results/exp-254-n17-second-tranche-flags
    dirty: false
    commit: cebb5d15aaa17d0cc13aa302ecbd750a54bfc57d
  results:
  - shape: determination
    role: outcome
    question: Is target 1 (corner-SW, side-N0, side-W0, side-W1, side-W2, interior-NW, interior-W, interior-S)
      infeasible at U, by a certificate the kernel's checker accepts and the standing verifier re-proves in
      full?
    outcome: criterion_met
    checked_by: The run (receipts/K/kernel-t1-bc425.json) returns PASS_CERTIFIED_CLOSED in 817 s of wall and
      653 s of process CPU (producer 436 s, checker 379 s) on 47 steps and 4,043 rows in 6 rounds, rows
      finest at 1/512, closure all_parent_poses_forbidden for interior-W at step 46. The standing verifier at
      cebb5d15a passes it in full mode in 555 s, checking all 3,979 live rows in full and 9,069 collision
      regions by 55,752,668 exact facet checks. Alone it excludes 84,704 states and 10,619 orbits.
  verdict:
    decision: in-progress
    primary_criterion: Each frozen target run once, a closure admitted only on the standing verifier's full pass
      with the endpoint surviving; descriptive for the census, and an arity-8 closure does not count toward
      H-267's criterion, which is read at arity at most seven.
    reason: The tranche is running; each closure is admitted as its verifier passes, and the verdict is written
      when the list is exhausted or a stop rule fires.
  lease:
    expires: '2026-10-06T08:14:04Z'
    host: Session 182 remote container
---
# exp-254: Session 182 BC-425, Lane K’s Second Tranche

This round is BC-425 of
[agenda-042](../../../agendas/agenda-042-overnight-n11-settlement-and-low-n-angles.md),
lane K’s second tranche under
[H-267](../../../hypotheses/H-267-n17-isolated-sub-pattern-residue.md), added at a
check-in and registered before its first run.
It takes the ten standing flags with the most projected gain against the certified line
at `18b7c5ae1`, using lane K’s filter widened only in arity, and runs them under the
frozen SW9 recipe that closed eight of lane K’s nine arity-7 targets.
All ten are arity 8. A closure removes its orbits from the certified census but does not
count toward H-267’s criterion, which is read at arity at most seven.

## Runs

The first closure took 1,494 orbits and 11,880 states off the certified line, exactly
its projected gain.

| Target | Cells | Producer | Verifier | Census after |
| --- | --- | --- | --- | --- |
| 1, `s182-bc425-t1` | corner-SW, side-N0, side-W0, side-W1, side-W2, interior-NW, interior-W, interior-S | closed in 817 s, 47 steps, 4,043 rows | full pass, 555 s | 60,368 states, 7,668 orbits |

The targets and the census they came from are
[kernel-targets-bc425.txt](../../../explorations/X048-session-182-overnight/kernel-targets-bc425.txt)
and
[census-bc425-targets.json](../../../explorations/X048-session-182-overnight/receipts/K/census-bc425-targets.json).
The receipts are under
[receipts/K](../../../explorations/X048-session-182-overnight/receipts/K/), each
certificate’s small files under the X048 certificates folder, and its objects in the
[hosted-data manifest](../../../../hosted/n17-x048-session-168-certificates.yaml).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
