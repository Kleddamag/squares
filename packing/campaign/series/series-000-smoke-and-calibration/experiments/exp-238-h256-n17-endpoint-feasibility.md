---
title: "exp-238 \u2014 exact n17 endpoint feasibility"
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-238
  series: series-000
  title: Exact n17 endpoint feasibility with centroid sliders
  date: '2026-10-01'
  hypotheses:
  - H-256
  tier: confirmatory
  subject:
    label: H255 exact root with the fixed H254 reconstruction and deterministic interior slider centroid.
    engine: devtools.check_n17_endpoint_feasibility
    assurance: verified
    method: exact-algebraic
    host_system: macOS ARM64, project Python3.14 and existing Sympy; one worker, host contention measured
      at launch.
    selftest_passed: true
    engine_commit: f77b3e0a7fdfec83ec7a4f6068404e23d91508b7
  instance:
    axis: n
    point: 17
    role: target
  method:
    control: Exact symbolic contact and unit-basis identities; unrelated-angle interval geometry, overlapping
      support, displaced contacts, missing/duplicate coverage, tampered root inputs and bounded large-rational
      serialization.
    candidate: Accepted exp237 root enclosure m plus/minus its exact inclusion bounds; fixed centroid
      sliders and complete H256 identity/strict obligation roster.
    runs_per_condition: 1
    interleaved: false
    operator: Codex Session165 coordinator
    entry_point: packing/devtools/check_n17_endpoint_feasibility.py
    command: cd packing && /usr/bin/time -l gtimeout --signal=TERM --kill-after=5s 180s .venv/bin/python3
      -m devtools.check_n17_endpoint_feasibility campaign/series/series-000-smoke-and-calibration/results/exp-237-n17-polynomial-root/run-001/certificate.json
    budget: One180second target run, one worker and10MiB output; optional1GiB data-segment limit where
      supported; independent output review.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/exp-238-n17-endpoint-feasibility/run-001
    commit: f77b3e0a7fdfec83ec7a4f6068404e23d91508b7
    dirty: false
  results:
  - shape: determination
    role: outcome
    question: Is the fixed centroid reconstruction feasible at the accepted exact chart root?
    outcome: criterion_met
    checked_by: All68 walls and136 pairs discharge with15/21 exact identities and53/115 strict intervals;
      independent complete roster/sign audit and recalculation of all187 exact intervals find no discrepancy.
  - shape: determination
    role: guard
    question: Are frozen root/source, controls, identities, provenance and mandatory resource limits valid?
    outcome: criterion_met
    checked_by: Nine controlled tests and independent code review; frozen Git blob, accepted root receipt
      and source match; tracked-clean run exits0 within180seconds/10MiB, unavailable optional memory cap
      recorded.
  verdict:
    decision: accepted
    primary_criterion: All68 wall and136 pair obligations discharge through the frozen exact identities
      or strict interval gaps, with controls and independent code/output review.
    reason: The exact root now has a certified17-square endpoint packing at fixed centroid sliders. All
      frozen obligations pass independent output review; global and split-orientation capture remain separate.
    needs_review: false
    commit: f77b3e0a7fdfec83ec7a4f6068404e23d91508b7
  effort:
    timebox: 180 seconds; one worker
    wall_seconds: 43.45
    pair_tests: 136
    stopped_by: criterion
---
# exp-238: Exact n17 Endpoint Feasibility

[H-256](../../../hypotheses/H-256-n17-exact-endpoint-feasibility.md) fixes the accepted
root enclosure, centroid sliders, complete geometric roster and strict acceptance rule.
The single target run follows a frozen instrument commit and independent controls.
The target ran once at12:23:08–12:23:54UTC, returned exit zero and passed independent
output review.

The symbolic stage proves exact contact and basis identities and the normalizations to
the accepted root polynomials.
The interval stage proves the remaining wall and pair inequalities over the entire root
enclosure.
Closing contacts vanish at the root; their zero values are not interval claims
about every point in that enclosure.

A failed enclosure is unresolved feasibility, not a refutation.
No root refinement, slider retuning, contact replacement or threshold adjustment is
permitted in this round.
An accepted endpoint plus the reviewed conditional minimum would settle the declared
orientation/branch/parameter class, while broader capture and global optimality remain
open.

## Accepted Outcome

All 15 wall identities, 21 pair identities, 53 strict wall inequalities and 115 strict
pair inequalities pass.
The [output review](../results/exp-238-n17-endpoint-feasibility/output-review.md)
records the independent full coverage/sign audit and recalculation of all187 intervals,
proof scope, guard evidence and complete timing breakdown.
The target took 43.45 seconds wall and produced a 4,717,067-byte exact certificate.
H-256 is confirmed. The conditional class minimum is now attained by an actual packing;
no global optimality or general contact capture is inferred.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
