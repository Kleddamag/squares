---
title: "exp-236 \u2014 exact n17 contact-chart fidelity"
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-236
  series: series-000
  title: Exact n17 contact-chart fidelity
  date: '2026-10-01'
  hypotheses:
  - H-254
  tier: confirmatory
  subject:
    label: Frozen Kleddamag rational witness under the preregistered n17 equality-chart fidelity criterion.
    engine: devtools.check_n17_contact_chart
    assurance: verified
    method: exact-algebraic
    host_system: macOS ARM64, project Python3.14, one worker; load66.14 and zero idle CPU at11:17UTC preflight.
  instance:
    axis: n
    point: 17
    role: target
  method:
    control: Synthetic rational bases verify all15 anchors,17 defining contacts,20 support sums and3 closing
      identities; tangential displacement, sign/domain failure, ambiguous axis, source tamper and slider
      overlap are refused.
    candidate: Unchanged H253 source bytes, fixed side, label map, domain and all H254 thresholds; no
      fitting.
    runs_per_condition: 1
    interleaved: false
    operator: Codex Session165 coordinator
    entry_point: packing/devtools/check_n17_contact_chart.py
    command: cd packing && /usr/bin/time -l gtimeout --signal=TERM --kill-after=5s 90s .venv/bin/python3
      -m devtools.check_n17_contact_chart
    budget: 90seconds wall, one worker,10MiB file output;1GiB data memory limit where supported, unsupported
      guards explicitly recorded.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/exp-236-n17-contact-chart/run-001
  results: []
  verdict:
    decision: in-progress
    primary_criterion: Every exact H254 residual, domain, orientation, feature and source-feasibility
      clause passes; controlled instrument and independent output review.
    reason: Claim reserved before target execution; instrument approval and committed clean-tree launch
      are mandatory.
    needs_review: true
  lease:
    expires: '2026-10-01T11:45:00Z'
---
# exp-236: n17 Contact-Chart Fidelity

[H-254](../../../hypotheses/H-254-n17-contact-chart-fidelity.md) freezes the source,
complete contact table, domains, residual thresholds and refusal rules.
This round evaluates those clauses once after the controlled instrument is committed.
Exact rational comparisons assess fidelity at the relaxed witness; they do not establish
an endpoint root or an optimality theorem.

The instrument commit and actual launch state are captured at execution, then added to
this record. Raw outputs are immutable.
A criterion failure records its exact failed clauses without changing their thresholds;
a guard failure or timeout is unresolved.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
