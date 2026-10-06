---
title: "exp-256 — Session 182 BC-427: lane K's third tranche, the remaining n17 flags of arity at most seven"
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-256
  series: series-000
  title: The sixteen remaining standing flags of arity at most seven with the most projected gain, run through
    the kernel under lane K's frozen SW9 recipe at cap 1169/250, each closure admitted on the standing
    verifier's full pass
  date: '2026-10-05'
  hypotheses:
  - H-267
  tier: confirmatory
  subject:
    label: The sixteen standing flags frozen in packing/campaign/explorations/X048-session-182-overnight/kernel-targets-bc427.txt,
      the classes of arity at most seven with the most projected gain against the certified line at
      71b1d0363 (fourteen of arity 7, two of arity 6; lane K's target 2 excluded), in projected-gain order, on
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
    control: Lane K's endpoint7 control under the same recipe, the endpoint's own west-wall cells and feasible
      at U, returned PASS_CONTROL_STALLED in 1,244 s (receipts/K/kernel-control-endpoint7.json) and covers this
      tranche, which runs that recipe unchanged; no new control runs. The endpoint's state must survive every
      admitted entry, which the census checks.
    candidate: Each frozen target's seed and node, re-proved in full by the standing kernel verifier.
    runs_per_condition: 1
    interleaved: false
    operator: Claude Session 182; the run operator's BC-427 queue produces and verifies each certificate on two
      workers and admits each closure in the session checkout
    entry_point: packing/devtools/check_n17_subpattern.py
    command: 'From packing/ of the run worktree: nice -n 10 timeout -k 120 7600 .venv/bin/python3 -m
      devtools.check_n17_subpattern --cells CELLS --bins 64 --max-rounds 24 --hull-limit 16 --producer-share
      0.6 --split-floor 512 --max-rows 1152 --split-patience 1 --max-seconds 7000 --save-objects DIR --output
      FILE; on a closure, nice -n 10 timeout -k 120 4000 .venv/bin/python3 -m devtools.verify_n17_kernel_certificate
      --progress --output CERT/verification.json CERT; then devtools.census_n17_certified in the session
      checkout.'
    budget: 7,000 s per target and 4,000 s per verification on one worker, two workers
    record: packing/campaign/series/series-000-smoke-and-calibration/results/exp-256-n17-third-tranche-flags
    dirty: false
    commit: cebb5d15aaa17d0cc13aa302ecbd750a54bfc57d
  results:
  - shape: determination
    role: outcome
    question: Is target 2 (corner-SW, side-S0, side-W0, side-W2, interior-SW, interior-NW, interior-W) infeasible at U
      within the 7,000 s ceiling?
    outcome: criterion_missed
    checked_by: The run (receipts/K/kernel-t2-bc427.json) returns PASS_CERTIFIED_STALL in 1,044 s of wall and 984 s of
      process CPU, the producer at its 24-round cap (168 steps, 18,402 rows, finest 1/512); at the last round
      every owner still had live rows, side-W0 9 and side-S0 15 the fewest. A non-closure; its node is kept.
  - shape: determination
    role: outcome
    question: Is target 1 (side-N1, side-E1, interior-SW, interior-W, interior-S, interior-N, interior-E) infeasible
      at U within the 7,000 s ceiling?
    outcome: criterion_missed
    checked_by: The run (receipts/K/kernel-t1-bc427.json) returns PASS_CERTIFIED_STALL in 3,773 s of wall and 3,636 s of
      process CPU, the producer with producer outcome stalled (112 steps, 13,468 rows, finest 1/512); at the
      last round every owner still had live rows, side-N1 100 and interior-SW 134 the fewest. A non-closure;
      its node is kept.
  - shape: determination
    role: outcome
    question: Is target 4 (side-E1, interior-SW, interior-NW, interior-W, interior-S, interior-N, interior-E)
      infeasible at U, by a certificate the kernel's checker accepts and the standing verifier re-proves in
      full?
    outcome: criterion_met
    checked_by: The run (receipts/K/kernel-t4-bc427.json) returns PASS_CERTIFIED_CLOSED in 171 s of wall and 146 s of
      process CPU (producer 96 s, checker 73 s) on 15 steps and 960 rows in 3 rounds, rows finest at 1/64,
      closure all_parent_poses_forbidden for side-E1 at step 14. The standing verifier at cebb5d15a passes it
      in full mode in 84 s, checking all 957 live rows in full and 2,682 collision regions by 17,169,132 exact
      facet checks. Alone it excludes 51,260 states and 6,468 orbits. The arity-at-most-7 entries then leave
      78,824 states and 9,990 orbits (receipts/K/census-arity7-after-bc427-t4.json).
  - shape: determination
    role: outcome
    question: Is target 3 (side-N0, side-W0, side-N1, interior-SW, interior-NW, interior-W, interior-S) infeasible at
      U within the 7,000 s ceiling?
    outcome: criterion_missed
    checked_by: The run (receipts/K/kernel-t3-bc427.json) returns PASS_CERTIFIED_STALL in 3,458 s of wall and 3,323 s of
      process CPU, the producer at its 24-round cap (168 steps, 18,675 rows, finest 1/512); at the last round
      every owner still had live rows, interior-NW 55 and side-N0 68 the fewest. A non-closure; its node is
      kept.
  - shape: determination
    role: outcome
    question: Is target 6 (side-S1, side-W1, interior-NW, interior-W, interior-S, interior-SE) infeasible at U, by a
      certificate the kernel's checker accepts and the standing verifier re-proves in full?
    outcome: criterion_met
    checked_by: The run (receipts/K/kernel-t6-bc427.json) returns PASS_CERTIFIED_CLOSED in 197 s of wall and 179 s of
      process CPU (producer 105 s, checker 91 s) on 40 steps and 2,816 rows in 7 rounds, rows finest at 1/256,
      closure all_parent_poses_forbidden for interior-W at step 39. The standing verifier at cebb5d15a passes
      it in full mode in 120 s, checking all 2,382 live rows in full and 4,632 collision regions by 22,785,964
      exact facet checks. Alone it excludes 109,080 states and 13,752 orbits. The arity-at-most-7 entries then
      leave 64,632 states and 8,191 orbits (receipts/K/census-arity7-after-bc427-t6.json).
  - shape: determination
    role: outcome
    question: Is target 7 (side-W0, side-W1, interior-SW, interior-NW, interior-W, interior-S, interior-N) infeasible
      at U within the 7,000 s ceiling?
    outcome: criterion_missed
    checked_by: The run (receipts/K/kernel-t7-bc427.json) returns PASS_CERTIFIED_STALL in 842 s of wall and 763 s of
      process CPU, the producer at its 24-round cap (168 steps, 17,907 rows, finest 1/512); at the last round
      every owner still had live rows, side-W0 20 and interior-W 34 the fewest. A non-closure; its node is
      kept.
  - shape: determination
    role: outcome
    question: Is target 5 (side-E0, side-S1, interior-NW, interior-W, interior-S, interior-N, interior-SE) infeasible
      at U within the 7,000 s ceiling?
    outcome: criterion_missed
    checked_by: The run (receipts/K/kernel-t5-bc427.json) returns PASS_CERTIFIED_STALL in 4,554 s of wall and 4,292 s of
      process CPU, the producer at its 24-round cap (168 steps, 19,241 rows, finest 1/512); at the last round
      every owner still had live rows, side-E0 64 and side-S1 85 the fewest. A non-closure; its node is kept.
  - shape: determination
    role: outcome
    question: Is target 9 (side-E1, interior-SW, interior-NW, interior-W, interior-N, interior-E, interior-SE)
      infeasible at U within the 7,000 s ceiling?
    outcome: criterion_missed
    checked_by: The run (receipts/K/kernel-t9-bc427.json) returns PASS_CERTIFIED_STALL in 726 s of wall and 446 s of
      process CPU, the producer at its 24-round cap (168 steps, 12,670 rows, finest 1/512); at the last round
      every owner still had live rows, interior-E 11 and interior-NW 11 the fewest. A non-closure; its node is
      kept.
  - shape: determination
    role: outcome
    question: Is target 10 (interior-NW, interior-W, interior-S, interior-N, interior-E, interior-SE) infeasible at U
      within the 7,000 s ceiling?
    outcome: criterion_missed
    checked_by: The run (receipts/K/kernel-t10-bc427.json) returns PASS_CERTIFIED_STALL in 712 s of wall and 400 s of
      process CPU, the producer at its 24-round cap (144 steps, 10,944 rows, finest 1/512); at the last round
      every owner still had live rows, interior-N 18 and interior-NW 22 the fewest. A non-closure; its node is
      kept.
  - shape: determination
    role: outcome
    question: Is target 8 (side-S0, side-S1, interior-SW, interior-NW, interior-W, interior-N, interior-SE) infeasible
      at U within the 7,000 s ceiling?
    outcome: criterion_missed
    checked_by: The run (receipts/K/kernel-t8-bc427.json) returns PASS_CERTIFIED_STALL in 5,424 s of wall and 4,572 s of
      process CPU, the producer at a fixed point after 21 rounds (147 steps, 16,289 rows, finest 1/512); at
      the last round every owner still had live rows, interior-W 23 and interior-SW 37 the fewest. A
      non-closure; its node is kept.
  - shape: determination
    role: cost
    question: Were targets 11 to 16 run before the tranche closed?
    outcome: criterion_missed
    checked_by: >-
      No. At the coordinator's re-plan at 21:43 UTC the queue stopped launching after
      target 10, and targets 11 to 16 were not run. The reasons were three. SW9's recipe
      had stopped five of the eight runs finished by then at the 24-round cap, and six of
      the ten it ran in the end.
      The six project 15 to 54 orbits each against the certified line at f749123fd, and
      15 to 439 against the arity-7 line
      (receipts/K/census-bc427-close.json; receipts/K/census-arity7-after-bc427-t6.json).
      And H-267 was already confirmed (exp-251). Those six, and every kept cap-stall node
      of this tranche, are the natural input to BC-423's recipe once the user rules on its
      control.
  verdict:
    decision: accepted
    primary_criterion: The certified residue at arity at most seven is at most 10^4 orbits with every certificate
      independently checked; a closure is admitted only on the standing verifier's full pass with the endpoint
      surviving.
    reason: >-
      Two of the ten targets run closed and were admitted on the standing verifier's full
      pass, target 4 (488c72d77) and target 6 (340e92b84), and they took the arity-7 line
      from 10,173 to 9,990 and then 8,191 orbits, the endpoint surviving
      (receipts/K/census-arity7-after-bc427-t6.json), which meets the criterion. The other
      eight stalled, six at the 24-round cap and two at producer fixed points, and targets
      11 to 16 were not run. The W2 review of exp-251
      (docs/project/reviews/review-2026-10-05-exp-251-h267.md) replayed target 4's
      verification and recounted both the 9,990 and the 8,191 lines; H-267's verdict is
      exp-251's.
    needs_review: false
  effort:
    timebox: 7,000 s per target and 4,000 s per verification, one worker per job, two workers
    wall_seconds: 11095
    stopped_by: criterion
---
# exp-256: Session 182 BC-427, Lane K’s Third Tranche

This round is BC-427 of
[agenda-042](../../../agendas/agenda-042-overnight-n11-settlement-and-low-n-angles.md),
lane K’s third tranche under
[H-267](../../../hypotheses/H-267-n17-isolated-sub-pattern-residue.md).
It is aimed at H-267’s threshold independently of lane K’s target 2, which BC-423 holds
for the user’s ruling.

H-267’s count at arity at most seven is 10,173 orbits, from
[census-arity7-after-k9.json](../../../explorations/X048-session-182-overnight/receipts/K/census-arity7-after-k9.json),
which is unchanged since `s182-k9` because every later admission is arity 8 or larger.
The threshold of at most $10^4$ needs 173 orbits off that line, and going below it needs
174\. Target 2 alone would take 1,372 from that line, so with it admitted no more is
needed; after target 4 it would take 1,344 from the 9,990 line
([census-arity7-after-bc427-t4.json](../../../explorations/X048-session-182-overnight/receipts/K/census-arity7-after-bc427-t4.json)).
Without it, any one of the ten frozen targets that project at least 174 orbits against
the arity-7 line (183 to 1,799) would suffice alone.
Target 4, which projects 183, closed and was admitted, and the line now stands at 9,990
orbits
([census-arity7-after-bc427-t4.json](../../../explorations/X048-session-182-overnight/receipts/K/census-arity7-after-bc427-t4.json)),
ten under $10^4$. H-267 is claimed only after a W2 review, so exp-251’s verdict stays
open. The census flags 33 classes of arity at most seven besides target 2. The frozen
list is the sixteen with the most projected gain against the certified line at
`71b1d0363`, which is the tranche’s cap.
No arity-8 flag fills it.

The tranche closed after target 10 at the coordinator’s re-plan.
Two of the ten targets run closed, eight stalled (six at the 24-round cap, two at
producer fixed points), and targets 11 to 16 were not run.
The round’s wall, 11,095 s, runs from the launch at 18:57:42 UTC to target 8’s end at
22:02:37. The six not run, and every cap-stall node kept here, are the natural input to
BC-423’s recipe once the user rules on its control.

## Runs

| Target | Cells | Producer | Verifier | Census after |
| --- | --- | --- | --- | --- |
| 2 | corner-SW, side-S0, side-W0, side-W2, interior-SW, interior-NW, interior-W | 24-round cap at 1,044 s, not closed | — | — |
| 1 | side-N1, side-E1, interior-SW, interior-W, interior-S, interior-N, interior-E | producer fixed point after 16 rounds at 3,773 s, not closed | — | — |
| 4, `s182-bc427-t4` | side-E1, interior-SW, interior-NW, interior-W, interior-S, interior-N, interior-E | closed in 171 s, 15 steps, 960 rows | full pass, 84 s | 4,874 orbits; 9,990 at arity at most seven |
| 3 | side-N0, side-W0, side-N1, interior-SW, interior-NW, interior-W, interior-S | 24-round cap at 3,458 s, not closed | — | — |
| 6, `s182-bc427-t6` | side-S1, side-W1, interior-NW, interior-W, interior-S, interior-SE | closed in 197 s, 40 steps, 2,816 rows | full pass, 120 s | 4,711 orbits; 8,191 at arity at most seven |
| 7 | side-W0, side-W1, interior-SW, interior-NW, interior-W, interior-S, interior-N | 24-round cap at 842 s, not closed | — | — |
| 5 | side-E0, side-S1, interior-NW, interior-W, interior-S, interior-N, interior-SE | 24-round cap at 4,554 s, not closed | — | — |
| 9 | side-E1, interior-SW, interior-NW, interior-W, interior-N, interior-E, interior-SE | 24-round cap at 726 s, not closed | — | — |
| 10 | interior-NW, interior-W, interior-S, interior-N, interior-E, interior-SE | 24-round cap at 712 s, not closed | — | — |
| 8 | side-S0, side-S1, interior-SW, interior-NW, interior-W, interior-N, interior-SE | producer fixed point after 21 rounds at 5,424 s, not closed | — | — |

The targets and the census they came from are
[kernel-targets-bc427.txt](../../../explorations/X048-session-182-overnight/kernel-targets-bc427.txt)
and
[census-bc427-targets.json](../../../explorations/X048-session-182-overnight/receipts/K/census-bc427-targets.json).
The receipts are under
[receipts/K](../../../explorations/X048-session-182-overnight/receipts/K/), each
certificate’s small files under the X048 certificates folder, and its objects in the
[hosted-data manifest](../../../../hosted/n17-x048-session-168-certificates.yaml).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
