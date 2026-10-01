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
    selftest_passed: true
    engine_commit: b3e5e1526e74421032dc2f5b79c243712fdd7b61
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
    commit: b3e5e1526e74421032dc2f5b79c243712fdd7b61
    dirty: false
  results:
  - shape: determination
    role: outcome
    question: Does the frozen box contain a unique exact root under the H255 contraction criterion?
    outcome: criterion_met
    checked_by: Separate exact checker accepts; independent Astra max audit verifies source, radius, inverse
      identities, all interval arithmetic, contraction/inclusion and every domain guard from retained
      outputs.
  - shape: determination
    role: guard
    question: Are controls, source/provenance and mandatory resource ceilings satisfied?
    outcome: criterion_met
    checked_by: 13 synthetic controls and independent code review; fixed source and tracked-clean commit;
      exit0 for producer/checker,90second and10MiB caps enforced; unsupported optional memory cap recorded.
  verdict:
    decision: accepted
    primary_criterion: H255 strict exact rational inclusion, contraction, inverse and whole-box domain
      guards pass both implementations and independent output review.
    reason: Exact root existence and uniqueness in the fixed box are established by both implementations
      and independent output review. Endpoint packing feasibility and global capture remain separate.
    needs_review: false
    commit: b3e5e1526e74421032dc2f5b79c243712fdd7b61
  effort:
    timebox: Producer90seconds and checker90seconds; one worker
    wall_seconds: 0.76
    stopped_by: criterion
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

## Accepted Result

The exact contraction norm is about $6.52534613777464\times10^{-11}<1$. The two
inclusion bounds are about $9.85923078412898\times10^{-24}$ and
$6.525346137774639\times10^{-23}$, both strictly below the fixed radius $10^{-12}$. The
retained certificate contains the exact fractions used for every comparison.
Producer and checker took 0.67 and 0.09 seconds wall respectively.
Independent retained-output arithmetic review took 0.0275 seconds; these are single-run
observations under host contention, not comparative benchmarks.

H-255 is confirmed. Positive normalizations map its root back to all three contact
equations. Together with the reviewed conditional theorem, this gives a minimum of the
declared necessary parameter system in its larger box.
It does not yet prove that a packing attains that minimum.
Every fixed point also lies coordinatewise within $m_i\pm\eta_i$, directly from the
accepted inclusion certificate; this narrower consequence needs no additional root solve
or changed experimental radius.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
