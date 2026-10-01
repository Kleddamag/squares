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
  results: []
  verdict:
    decision: in-progress
    primary_criterion: All68 wall and136 pair obligations discharge through the frozen exact identities
      or strict interval gaps, with controls and independent code/output review.
    reason: Preregistered before endpoint target evaluation; final instrument controls and independent
      review precede frozen execution.
    needs_review: false
  lease:
    expires: '2026-10-01T12:40:00Z'
    host: spud10.local
---
# exp-238: Exact n17 Endpoint Feasibility

[H-256](../../../hypotheses/H-256-n17-exact-endpoint-feasibility.md) fixes the accepted
root enclosure, centroid sliders, complete geometric roster and strict acceptance rule.
The single target run follows a frozen instrument commit and independent controls.
No endpoint target has run at preregistration.

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

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
