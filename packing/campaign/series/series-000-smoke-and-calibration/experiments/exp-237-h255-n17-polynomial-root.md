---
title: "exp-237 \u2014 exact existence of the n17 contact-chart root"
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-237
  series: series-000
  title: Exact n17 polynomial-root existence
  date: '2026-10-01'
  hypotheses:
  - H-255
  tier: confirmatory
  subject:
    label: Fixed H255 rational box for the independently derived two-polynomial n17 contact chart.
    engine: devtools.make_n17_root_certificate and devtools.check_n17_root_certificate
    assurance: verified
    method: exact-algebraic
    host_system: macOS ARM64, project Python3.14, one worker; host contention measured at launch.
    selftest_passed: false
  instance:
    axis: n
    point: 17
    role: target
  method:
    control: Independent hand-derived nonlinear positive certificate; interval signs and powers; singular,
      boundary, outside and two-root refusals; altered certificate quantities, source and domain guards.
    candidate: Unchanged H253 source midpoint (t9,-t16), radius1/10^12 and both fixed integer polynomials;
      no fitting, adaptation or radius refinement.
    runs_per_condition: 1
    interleaved: false
    operator: Codex Session165 coordinator
    entry_point: packing/devtools/make_n17_root_certificate.py
    command: cd packing && .venv/bin/python3 -m devtools.make_n17_root_certificate; independently check
      its retained JSON using devtools.check_n17_root_certificate. Exact supervised invocations are retained
      in run-001/command.txt.
    budget: Producer90seconds and checker90seconds; one worker,10MiB per output; optional1GiB data-segment
      cap where supported.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/exp-237-n17-polynomial-root/run-001
  results: []
  verdict:
    decision: in-progress
    primary_criterion: H255 strict exact rational inclusion, contraction, inverse and whole-box domain
      guards pass both implementations and independent output review.
    reason: Preregistered before target evaluation; controlled code must be independently reviewed and
      frozen first.
    needs_review: false
  lease:
    expires: '2026-10-01T12:10:00Z'
    host: spud10.local
---
# exp-237: Exact n17 Polynomial Root

[H-255](../../../hypotheses/H-255-n17-exact-polynomial-root.md) fixes the polynomial
system, source midpoint, radius, all domain guards and strict contraction criterion.
The producer and checker use independently implemented exact rational arithmetic.
The second implementation uses the same mathematical argument; it is not a distinct
verification method.

No target evaluation has occurred at preregistration.
After independent code review, commit the instruments and controls, record that commit
and the tracked-clean launch state, then run the producer once and check its retained
JSON once. Retain all raw outputs and resource receipts.
A failed certificate is unresolved root existence; it is not permission to adjust the
box or refute the root.

Acceptance establishes one root in the fixed box.
The reviewed conditional minimum then applies to the declared necessary system.
Endpoint packing feasibility, joint slider domains, capture and global optimality remain
separate proof obligations.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
