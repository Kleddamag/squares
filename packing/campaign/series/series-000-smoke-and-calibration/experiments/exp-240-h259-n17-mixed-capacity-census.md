---
title: "exp-240 \u2014 n17 mixed-capacity occupancy census"
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-240
  series: series-000
  title: Exact n17 mixed-capacity occupancy census
  date: '2026-10-01'
  hypotheses:
  - H-259
  tier: confirmatory
  subject:
    label: Fixed25cell cover atcap1169/250 with16capacity1 and9capacity2 cells;36capacity1 baseline.
    engine: devtools.count_cell_occupancies and independent devtools.audit_cell_occupancies
    assurance: verified
    method: exact-algebraic
    host_system: macOS ARM64, projectPython3.14, standardlibrary integer arithmetic,oneworker
    selftest_passed: true
  instance:
    axis: n
    point: 17
    role: target
  method:
    control: '53 target-free producer and independent-auditor controls: small brute enumeration, empty/impossible
      states, malformed and mutated receipts, exact schema and capacity/size guards.'
    candidate: "Exact coefficientx17 of(1+x)^16(1+x+x\xB2)^9; unchangedcap/grid/closedseamcontract."
    runs_per_condition: 1
    interleaved: false
    operator: Codex Session165 coordinator
    entry_point: packing/devtools/count_cell_occupancies.py
    command: 'From packing: .venv/bin/python3 -m devtools.count_cell_occupancies --capacities [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2]
      --target 17; repeat baseline36ones,target17; separately audit eachJSON with devtools.audit_cell_occupancies.
      Exact shell commands retained in run-001/commands.txt.'
    budget: One30second combined command group,oneworker,1MiB eachoutput; no enumeration ofvectors or
      geometry.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/exp-240-n17-mixed-capacity-census/run-001
    dirty: false
  results: []
  verdict:
    decision: in-progress
    primary_criterion: Independent exact prefix/target/total count agreement and strict targetcount reduction
      versusbaseline, with reviewed complete geometric capacities and seamownership.
    reason: Registered before target evaluation; controlled instruments and reviewed geometry are ready.
    needs_review: true
  lease:
    expires: '2026-10-01T14:15:00Z'
---
# exp-240: n17 Mixed-Capacity Occupancy Census

[H259](../../../hypotheses/H-259-n17-mixed-capacity-cover.md) freezes the complete
closed centre cover, capacities, seam rule, exact count comparison, controls and limits.
The support/capacity proof has two Astra max reviews and coordinator review.
The producer uses coefficient dynamic programming; the auditor uses a separate closed
binomial sum, without importing producer code.
Their53 synthetic controls pass.

No coefficient of the target or baseline vector has been evaluated at registration.
The analytic total-state upper bound already predicts a reduction; this is a disclosed
prior expectation, not an unobserved discovery.
One frozen run will retain both full coefficient prefixes, audits, commands, exits and
timing. Exact ratio means target count divided by baseline count; neither quantity is a
count of geometric packings.

No symmetry reduction, contact pattern, orientation restriction or endpoint occupancy
cut is used. Acceptance requires independent output review.
Even success leaves a large necessary occupancy relaxation whose geometric cases have
not been excluded.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
