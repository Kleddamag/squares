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
  verdict:
    decision: in-progress
    primary_criterion: The certified residue at arity at most seven is at most 10^4 orbits with every certificate
      independently checked; a closure is admitted only on the standing verifier's full pass with the endpoint
      surviving.
    reason: Registered before its first run; each closure is admitted as its verifier passes, and the verdict is
      written when the list is exhausted or a stop rule fires.
  lease:
    expires: '2026-10-06T08:14:04Z'
    host: Session 182 remote container
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
174\. Target 2 alone would take 1,372, so with it admitted no more is needed.
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

## Runs

| Target | Cells | Producer | Verifier | Census after |
| --- | --- | --- | --- | --- |
| 2 | corner-SW, side-S0, side-W0, side-W2, interior-SW, interior-NW, interior-W | 24-round cap at 1,044 s, not closed | — | — |
| 1 | side-N1, side-E1, interior-SW, interior-W, interior-S, interior-N, interior-E | producer fixed point after 16 rounds at 3,773 s, not closed | — | — |
| 4, `s182-bc427-t4` | side-E1, interior-SW, interior-NW, interior-W, interior-S, interior-N, interior-E | closed in 171 s, 15 steps, 960 rows | full pass, 84 s | 4,874 orbits; 9,990 at arity at most seven |

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
