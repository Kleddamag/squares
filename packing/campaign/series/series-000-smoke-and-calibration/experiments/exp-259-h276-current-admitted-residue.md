---
title: exp-259 — current admitted n17 residue partition control
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-259
  series: series-000
  title: Complete D4 and composition/distance partition of the current admitted n17 residue
  date: '2026-10-07'
  hypotheses: [H-276]
  tier: confirmatory
  subject:
    label: Current unique-state n17 cover at U=1169/250 under58 admitted entries.
    engine: devtools.stratify_n17_certified_residue; source frozen by the registration commit before measurement.
    assurance: verified
    method: exact-algebraic
    host_system: macOS arm64, project Python3.14.7, one process; external scratch.
    selftest_passed: true
  instance: {axis: n, point: 17, role: calibration}
  method:
    control: Standing certified census from Session183 plus independent synthetic orbit enumeration; six focused controls pass.
    candidate: Full canonical orbit roster with composition/distance strata; no optional producer receipts.
    runs_per_condition: 1
    interleaved: false
    operator: GPT-6.1 Sol coordinator, Session184
    entry_point: packing/devtools/stratify_n17_certified_residue.py
    command: >-
      From packing/ with TMPDIR, UV_CACHE_DIR and CARGO_TARGET_DIR under verified
      external scratch: /Volumes/spud-ext1/agent-scratch/n17-w3-01a114fb/venv/bin/python3
      -m devtools.stratify_n17_certified_residue --output
      campaign/series/series-000-smoke-and-calibration/results/exp-259-current-admitted-residue/partition.json
    budget: Two-minute measurement ceiling; no exclusion search or admission mutation.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/exp-259-current-admitted-residue
  lease:
    expires: '2026-10-07T07:38:33Z'
    host: macOS arm64
  results: []
  verdict:
    decision: in-progress
    primary_criterion: Exact census36784states/4685orbits/58admissions, complete disjoint orbit and stratum sums, endpoint survives.
    reason: Source, criteria and retained output path declared before the real-ledger control; no target measurement yet.
---
# exp-259: Actual Admitted Residue Control

This is the first population control for BC-432 in Session184. Its source and H-276
criterion are committed before the real-ledger command.
The accepted ledger remains unchanged from `f3a13e3a2`. The instrument must preserve
every surviving assignment state, endpoint included; no new exclusion is admitted by
this round.

The complete roster is retained for Astra’s subsequent workload selection.
All diagnostic labels initially mean only that no optional receipts were supplied.
They do not mean these states have never been attempted.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
