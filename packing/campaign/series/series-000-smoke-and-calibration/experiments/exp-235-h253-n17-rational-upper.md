---
title: exp-235 — independent replay of the retained n17 rational upper witness
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-235
  series: series-000
  title: Independent replay of the retained n17 rational upper witness
  date: '2026-10-01'
  hypotheses: [H-253]
  tier: confirmatory
  subject:
    label: Fixed Kleddamag rational n17 source certificate and lossless cyclic-corner conversion at its stated exact side.
    engine: import_half_angle_witness and existing stock and independent rational checkers
    assurance: verified
    method: exact-algebraic
    host_system: macOS ARM64, project Python3.14, one worker; load141 on10cores and zero idle at launch preflight
  instance: {axis: n, point: 17, role: target}
  method:
    control: Exact four-square grid accepted and overlapping two-square fixture rejected by both local checkers; synthetic rational rotation and metadata regressions passed before target conversion.
    candidate: The frozen upper-packing-certificate.json from the September21 Kleddamag packet, with exact side 4675530093604551/1000000000000000.
    runs_per_condition: 1
    interleaved: false
    operator: Codex Session165 coordinator
    entry_point: packing/campaign/series/series-000-smoke-and-calibration/results/exp-235-n17-rational-upper/replay.sh
    command: cd packing && gtimeout --signal=TERM --kill-after=5s 600s bash campaign/series/series-000-smoke-and-calibration/results/exp-235-n17-rational-upper/replay.sh campaign/series/series-000-smoke-and-calibration/results/exp-235-n17-rational-upper/run-001
    budget: 90 seconds per command, 600 seconds for the supervised whole run, one worker, 1GiB heap limit and 10MiB file limit.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/exp-235-n17-rational-upper/run-001
  lease:
    expires: '2026-10-01T11:00:00Z'
  results: []
  verdict:
    decision: in-progress
    primary_criterion: Both exact local checkers accept all17 unit squares, all68 vertices and136 pair separations at the exact frozen side, with source agreement, fixed control behavior and no blocking independent-review finding.
    reason: Preregistered round; target conversion and replay have not started.
---
# exp-235: Retained n17 Rational Upper Witness

[H-253](../../../hypotheses/H-253-n17-retained-rational-upper.md) fixes the claim,
source bytes, controls and refusal rules.
The [replay script](../results/exp-235-n17-rational-upper/replay.sh) records exact
commands, exit statuses, source integrity, Git provenance, per-command wall/CPU time and
memory. The adapter’s preflight shares the independent checker’s geometry and is not
counted as an additional independent verification route.
The source verifier runs unoptimized, with `PYTHONOPTIMIZE` unset.

The per-process memory guard limits data/heap on this platform rather than claiming a
portable total-RSS ceiling; `/usr/bin/time -l` measures actual peak resident memory.
The run uses no worker pool.
A timeout, crash or guard refusal retains its outputs and stops the sequence without a
scientific acceptance.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
