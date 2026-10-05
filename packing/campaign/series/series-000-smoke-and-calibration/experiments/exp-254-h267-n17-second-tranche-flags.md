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
  - shape: determination
    role: outcome
    question: Is target 2 (corner-SW, side-S0, side-S1, side-S2, interior-NW, interior-W, interior-S,
      interior-SE) infeasible at U, by a certificate the kernel's checker accepts and the standing verifier
      re-proves in full?
    outcome: criterion_met
    checked_by: The run (receipts/K/kernel-t2-bc425.json) returns PASS_CERTIFIED_CLOSED in 1,250 s of wall and
      886 s of process CPU (producer 771 s, checker 477 s) on 78 steps and 8,192 rows in 10 rounds, rows
      finest at 1/512, closure all_parent_poses_forbidden for interior-W at step 77. The standing verifier at
      cebb5d15a passes it in full mode in 758 s, checking all 7,579 live rows in full and 14,002 collision
      regions by 69,327,180 exact facet checks. Alone it excludes 80,404 states and 10,087 orbits.
  - shape: determination
    role: outcome
    question: Is target 4 (corner-SE, side-E0, side-S1, side-S2, interior-NW, interior-W, interior-S,
      interior-SE) infeasible at U, by a certificate the kernel's checker accepts and the standing verifier
      re-proves in full?
    outcome: criterion_met
    checked_by: The run (receipts/K/kernel-t4-bc425.json) returns PASS_CERTIFIED_CLOSED in 553 s of wall and
      379 s of process CPU (producer 310 s, checker 242 s) on 138 steps and 11,323 rows in 18 rounds, rows
      finest at 1/512, closure all_parent_poses_forbidden for side-E0 at step 137. The standing verifier at
      cebb5d15a passes it in full mode in 275 s, checking all 4,945 live rows in full and 11,028 collision
      regions by 34,265,064 exact facet checks. Alone it excludes 80,436 states and 10,090 orbits.
  - shape: determination
    role: outcome
    question: Is target 5 (side-N0, side-S1, side-N1, interior-NW, interior-W, interior-S, interior-N, interior-SE)
      infeasible at U, by a certificate the kernel's checker accepts and the standing verifier re-proves in
      full?
    outcome: criterion_met
    checked_by: The run (receipts/K/kernel-t5-bc425.json) returns PASS_CERTIFIED_CLOSED in 327 s of wall and 282 s of
      process CPU (producer 159 s, checker 166 s) on 22 steps and 1,408 rows in 3 rounds, rows finest at 1/64,
      closure all_parent_poses_forbidden for interior-S at step 21. The standing verifier at cebb5d15a passes
      it in full mode in 300 s, checking all 1,408 live rows in full and 4,158 collision regions by 27,723,164
      exact facet checks. Alone it excludes 66,232 states and 8,319 orbits.
  - shape: determination
    role: outcome
    question: Is target 3 (side-S0, side-E0, side-S1, side-S2, interior-NW, interior-W, interior-S,
      interior-SE) infeasible at U within the 7,000 s ceiling?
    outcome: criterion_missed
    checked_by: The run (receipts/K/kernel-t3-bc425.json) returns PASS_CERTIFIED_STALL in 1,139 s of wall and
      838 s of process CPU, the producer at its 24-round cap with producer time unused (192 steps, 16,810
      rows, finest 1/512); at the last round every owner still had live rows, interior-S 7, interior-SE 8,
      side-E0 5 and side-S1 6 the fewest. A non-closure; its node is kept for a stall diagnosis.
  - shape: determination
    role: outcome
    question: Is target 7 (corner-NW, side-S0, side-W0, side-W1, side-W2, interior-SW, interior-NW, interior-S)
      infeasible at U, by a certificate the kernel's checker accepts and the standing verifier re-proves in
      full?
    outcome: criterion_met
    checked_by: The run (receipts/K/kernel-t7-bc425.json) returns PASS_CERTIFIED_CLOSED in 482 s of wall and 355 s of
      process CPU (producer 217 s, checker 263 s) on 32 steps and 2,050 rows in 4 rounds, rows finest at
      1/128, closure all_parent_poses_forbidden for interior-S at step 31. The standing verifier at cebb5d15a
      passes it in full mode in 198 s, checking all 2,023 live rows in full and 5,096 collision regions by
      25,553,964 exact facet checks. Alone it excludes 81,848 states and 10,267 orbits.
  - shape: determination
    role: outcome
    question: Is target 6 (side-N0, side-S1, side-W2, interior-NW, interior-W, interior-S, interior-N,
      interior-SE) infeasible at U within the 7,000 s ceiling?
    outcome: criterion_missed
    checked_by: The run (receipts/K/kernel-t6-bc425.json) returns PASS_CERTIFIED_STALL in 1,374 s of wall and
      1,093 s of process CPU, the producer at its 24-round cap with producer time unused (192 steps, 17,378
      rows, finest 1/512); at the last round every owner still had live rows, interior-S 5 and interior-N 7
      the fewest. A non-closure; its node is kept for a stall diagnosis.
  - shape: determination
    role: outcome
    question: Is target 8 (corner-NW, side-W0, side-W1, side-W2, interior-SW, interior-NW, interior-S, interior-E)
      infeasible at U, by a certificate the kernel's checker accepts and the standing verifier re-proves in
      full?
    outcome: criterion_met
    checked_by: The run (receipts/K/kernel-t8-bc425.json) returns PASS_CERTIFIED_CLOSED in 738 s of wall and 696 s of
      process CPU (producer 390 s, checker 346 s) on 113 steps and 8,748 rows in 15 rounds, rows finest at
      1/512, closure all_parent_poses_forbidden for corner-NW at step 112. The standing verifier at cebb5d15a
      passes it in full mode in 439 s, checking all 6,299 live rows in full and 12,837 collision regions by
      48,076,168 exact facet checks. Alone it excludes 74,344 states and 9,328 orbits.
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
The second took 360 orbits and 2,872 states, against the 1,311 orbits
projected for it alone, because most of what it excludes the first had already excluded.

| Target | Cells | Producer | Verifier | Census after |
| --- | --- | --- | --- | --- |
| 1, `s182-bc425-t1` | corner-SW, side-N0, side-W0, side-W1, side-W2, interior-NW, interior-W, interior-S | closed in 817 s, 47 steps, 4,043 rows | full pass, 555 s | 60,368 states, 7,668 orbits |
| 2, `s182-bc425-t2` | corner-SW, side-S0, side-S1, side-S2, interior-NW, interior-W, interior-S, interior-SE | closed in 1,250 s, 78 steps, 8,192 rows | full pass, 758 s | 57,496 states, 7,308 orbits |
| 4, `s182-bc425-t4` | corner-SE, side-E0, side-S1, side-S2, interior-NW, interior-W, interior-S, interior-SE | closed in 553 s, 138 steps, 11,323 rows | full pass, 275 s | 53,016 states, 6,742 orbits (after lane A’s state 3063677 too) |
| 3 | side-S0, side-E0, side-S1, side-S2, interior-NW, interior-W, interior-S, interior-SE | 24-round cap at 1,139 s, not closed | — | — |
| 6 | side-N0, side-S1, side-W2, interior-NW, interior-W, interior-S, interior-N, interior-SE | 24-round cap at 1,374 s, not closed | — | — |
| 5, `s182-bc425-t5` | side-N0, side-S1, side-N1, interior-NW, interior-W, interior-S, interior-N, interior-SE | closed in 327 s, 22 steps, 1,408 rows | full pass, 300 s | 50,728 states, 6,453 orbits |
| 7, `s182-bc425-t7` | corner-NW, side-S0, side-W0, side-W1, side-W2, interior-SW, interior-NW, interior-S | closed in 482 s, 32 steps, 2,050 rows | full pass, 198 s | 44,316 states, 5,649 orbits |
| 8, `s182-bc425-t8` | corner-NW, side-W0, side-W1, side-W2, interior-SW, interior-NW, interior-S, interior-E | closed in 738 s, 113 steps, 8,748 rows | full pass, 439 s | 41,456 states, 5,287 orbits |

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
