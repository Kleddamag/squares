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
    engine_commit: 74480b0a0139aafaef4fa15c778cef9464569ca1
    selftest_passed: true
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
    commit: 74480b0a0139aafaef4fa15c778cef9464569ca1
    dirty: false
  results:
  - shape: determination
    role: outcome
    question: Does the retained rational witness satisfy every frozen H254 fidelity clause?
    outcome: criterion_met
    checked_by: 458 exact comparisons pass; independent Astra max review reconstructed the complete unique
      clause roster, all bounds and all chart scalars/vectors from the receipt.
  - shape: determination
    role: guard
    question: Did the instrument pass synthetic controls and retain the fixed source, side, label map
      and supervised limits?
    outcome: criterion_met
    checked_by: Seven synthetic controls passed independently; source SHA, side and map match; clean tracked
      commit, exit0, bounded output and wall; unsupported platform memory cap logged.
  verdict:
    decision: accepted
    primary_criterion: Every exact H254 residual, domain, orientation, feature and source-feasibility
      clause passes; controlled instrument and independent output review.
    reason: All458 frozen comparisons pass with complete independently audited coverage and controlled
      instrument. Acceptance establishes fidelity at the relaxed rational source only.
    needs_review: false
    commit: 74480b0a0139aafaef4fa15c778cef9464569ca1
  effort:
    timebox: 90 seconds; one worker
    wall_seconds: 1.13
    pair_tests: 136
    stopped_by: criterion
---
# exp-236: n17 Contact-Chart Fidelity

[H-254](../../../hypotheses/H-254-n17-contact-chart-fidelity.md) freezes the source,
complete contact table, domains, residual thresholds and refusal rules.
This round evaluated those clauses once at the independently reviewed frozen commit.
Exact rational comparisons assess fidelity at the relaxed witness; they do not establish
an endpoint root or an optimality theorem.

The instrument commit and actual launch state are captured in the raw receipt.
Raw outputs are immutable.
A criterion failure records its exact failed clauses without changing their thresholds;
a guard failure or timeout is unresolved.

## Accepted Outcome

The target ran at 11:24:26–11:24:27 UTC and returned exit zero.
All 458 exact comparisons passed.
The largest equation residual was approximately $1.346412991990249\times10^{-16}$; the
largest centre reconstruction residual was approximately
$8.507519164300177\times10^{-17}$, both below the frozen $10^{-12}$ cap.
The weakest alternative-axis separation was approximately $-0.05579984657519721$, well
below the required $-10^{-6}$. The receipt retains exact fractions; these decimal values
are summaries only.

Astra max independently parsed every comparison, reconstructed the complete unique
clause roster and its frozen bounds, and recomputed every chart scalar and vector from
recorded side and half-angles.
It found no missing, duplicate or extra clause, and verified the source identity, label
map, code revision and measured costs.
The [output review](../results/exp-236-n17-contact-chart/output-review.md) records scope
and counts. It did not rerun the target or count this audit as a new geometry method.

The command took 1.13 seconds wall, 0.52 user and 0.17 system CPU seconds, with
74,268,672 bytes maximum resident memory.
The JSON output is 208,788 bytes.
The launcher enforced a 90-second timeout and a 10 MiB file ceiling; macOS rejected the
optional data-segment memory cap, explicitly recorded in the raw guard log.
The host had load 88.74 on 10 cores at launch; this single run is not a comparative
benchmark. Preparation, mathematical derivation and review dominate elapsed work.

H-254 is confirmed. Exact root existence, endpoint packing and slider feasibility, local
capture and global optimality remain open.
The independent analytic conditional minimum derived alongside this run is in the
[W3 review](../../../../../docs/project/reviews/review-2026-10-01-post-optimality-w3-opening.md#conditional-minimum-in-the-frozen-parameter-box);
its proof does not depend on interpreting small residuals as zero.
`think-bj81` owns root isolation and endpoint feasibility next.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
