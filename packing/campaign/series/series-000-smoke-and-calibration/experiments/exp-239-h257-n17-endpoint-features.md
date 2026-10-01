---
title: "exp-239 \u2014 exact n17 endpoint contact features"
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-239
  series: series-000
  title: Complete exact n17 endpoint contact-feature inventory
  date: '2026-10-01'
  hypotheses:
  - H-257
  tier: confirmatory
  subject:
    label: Accepted H255 root enclosure and H256 centroid packing with every owner-axis alternative retained.
    engine: devtools.check_n17_endpoint_features
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
    control: Synthetic parallel owner ties, two-axis corner, displaced contacts and walls, missing/duplicate
      coverage, strict negative and straddling intervals, malformed or altered frozen inputs.
    candidate: Fixed H255 m plus/minus eta and unchanged H256centroid;168pair options,60active-wall corners,9parallel-face
      offsets.
    runs_per_condition: 1
    interleaved: false
    operator: Codex Session165 coordinator
    entry_point: packing/devtools/check_n17_endpoint_features.py
    command: cd packing && /usr/bin/time -l gtimeout --signal=TERM --kill-after=5s 180s .venv/bin/python3
      -m devtools.check_n17_endpoint_features campaign/series/series-000-smoke-and-calibration/results/exp-237-n17-polynomial-root/run-001/certificate.json
      campaign/series/series-000-smoke-and-calibration/results/exp-238-n17-endpoint-feasibility/run-001/certificate.json
    budget: One180second target,oneworker,10MiB per output; optional1GiB data-segment cap where supported;
      independent output audit.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/exp-239-n17-endpoint-features/run-001
  results: []
  verdict:
    decision: in-progress
    primary_criterion: All33pair/29wall exact zero identities,135negative pair upper bounds,31positive
      corner lower bounds and9strict abs(tau)<1 intervals pass with complete labeled coverage and independent
      review.
    reason: Preregistered before feature target evaluation; instrument controls and independent review
      precede frozen execution.
    needs_review: false
  lease:
    expires: '2026-10-01T13:35:00Z'
    host: spud10.local
---
# exp-239: Exact n17 Endpoint Contact Features

[H-257](../../../hypotheses/H-257-n17-endpoint-contact-features.md) freezes the root,
centroid geometry, complete owner-axis and wall-corner roster, sign criterion and
limits. No feature target evaluation has occurred at preregistration.
The instrument and controls must pass independent review and be committed before use.

The single run certifies feature completeness for a later first-order model.
It does not solve a cone or establish stationarity, local minimality or global
optimality. Exact zero identities apply at the certified root; strict signs apply
throughout its accepted inclusion enclosure.
No undecided interval is rounded to zero.

A failed interval, count or identity remains unresolved feature classification.
Preserve the refusal and all raw files.
Do not refine the root, retune sliders, discard owner labels or change the criterion
after seeing target output.
Independent output audit is required before acceptance.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
