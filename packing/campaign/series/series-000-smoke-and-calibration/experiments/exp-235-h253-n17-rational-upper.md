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
  hypotheses:
  - H-253
  tier: confirmatory
  subject:
    label: Fixed Kleddamag rational n17 source certificate and lossless cyclic-corner conversion at its
      stated exact side.
    engine: import_half_angle_witness and existing stock and independent rational checkers
    assurance: verified
    method: exact-algebraic
    host_system: macOS ARM64, project Python3.14, one worker; load141 on10 cores and zero idle at 10:33
      preflight; actual launch load retained in provenance.log
    engine_commit: bacacdd15f4c7a410dfc9b8fff32c918e5851748
  instance:
    axis: n
    point: 17
    role: target
  method:
    control: Exact four-square grid accepted and overlapping two-square fixture rejected by both local
      checkers; synthetic rational rotation and metadata regressions passed before target conversion.
    candidate: The frozen upper-packing-certificate.json from the September21 Kleddamag packet, with exact
      side 4675530093604551/1000000000000000.
    runs_per_condition: 1
    interleaved: false
    operator: Codex Session165 coordinator
    entry_point: packing/campaign/series/series-000-smoke-and-calibration/results/exp-235-n17-rational-upper/replay.sh
    command: cd packing && gtimeout --signal=TERM --kill-after=5s 600s bash campaign/series/series-000-smoke-and-calibration/results/exp-235-n17-rational-upper/replay.sh
      campaign/series/series-000-smoke-and-calibration/results/exp-235-n17-rational-upper/run-001
    budget: 90 seconds per command, 600 seconds for the supervised whole run, one worker, requested 1GiB
      heap limit where supported and 10MiB file limit.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/exp-235-n17-rational-upper/run-001
    commit: bacacdd15f4c7a410dfc9b8fff32c918e5851748
    dirty: false
  results:
  - shape: determination
    role: outcome
    question: Does the fixed rational n17 certificate meet H253?
    outcome: criterion_met
    checked_by: Stock exact verifier and independent rational checker both accepted 17 squares/136pairs;
      source accepted 17/68/136. Astra max reviewed all outputs and separately checked exact source-to-output
      centroid, basis, half-angle recovery and side for all 17 squares.
  - shape: determination
    role: guard
    question: Did both local checkers accept the exact grid and refuse the overlapping negative control?
    outcome: criterion_met
    checked_by: All4 expected exits and complete outputs in run-001; negative pair gap is exactly -1/2.
  verdict:
    decision: accepted
    primary_criterion: Both exact local checkers accept all 17 unit squares, all68 vertices and136 pair
      separations at the exact frozen side, with source agreement, fixed control behavior and no blocking
      independent-review finding.
    reason: The frozen exact source, two local geometry implementations, independent mapping audit and
      all positive/negative controls agree. Acceptance is only of the rational upper witness.
    needs_review: false
    commit: bacacdd15f4c7a410dfc9b8fff32c918e5851748
  effort:
    timebox: 90 seconds per command;600 seconds total
    wall_seconds: 7.91
    pair_tests: 136
    stopped_by: criterion
---
# exp-235: Retained n17 Rational Upper Witness

[H-253](../../../hypotheses/H-253-n17-retained-rational-upper.md) fixes the claim,
source bytes, controls and refusal rules.
Run-001 used the shell entry point recorded above.
Its original source is available with
`git show bacacdd15f4c7a410dfc9b8fff32c918e5851748:packing/campaign/series/series-000-smoke-and-calibration/results/exp-235-n17-rational-upper/replay.sh`;
its component commands and outputs remain in the immutable raw receipts.
The current [Python replay launcher](../../../../devtools/replay_n17_rational_upper.py)
runs the same fixed checks into a fresh output directory:

```bash
cd packing
gtimeout --signal=TERM --kill-after=5s 600s .venv/bin/python3 -m devtools.replay_n17_rational_upper FRESH_OUTPUT_DIRECTORY
```

The launcher records commands, exit statuses, source integrity, Git provenance,
per-command wall/CPU time and memory.
The adapter’s preflight shares the independent checker’s geometry and is not counted as
an additional independent verification route.
The source verifier runs unoptimized, with `PYTHONOPTIMIZE` unset.

The requested per-process data/heap limit is unavailable on this platform;
`/usr/bin/time -l` measures actual peak resident memory.
The run uses no worker pool.
A timeout, crash or guard refusal retains its outputs and stops the sequence without a
scientific acceptance.

## Premeasurement Launch Refusal

The first launcher at `245fd2782` stopped before any control or target operation because
macOS refused the data-segment limit with `Invalid argument`. The
[raw launch refusal](../results/exp-235-n17-rational-upper/premeasurement-launch-001.log)
is retained. The revised launcher records this unsupported guard explicitly, consistent
with H-253’s preregistered memory cap where supported.
It keeps the frozen scientific criterion and mandatory wall, worker and file-size
ceilings. No target data motivated this portability correction.
Actual RSS will be measured; this platform does not provide the requested hard memory
guard through this shell API.

## Accepted Outcome

At 10:48:50–10:48:58 UTC, both local exact checkers and the source checker accepted all
17 unit squares at side 4675530093604551/1000000000000000. Both local outputs report 136
tested pairs, positive exact pair clearance and positive exact containment clearance.
Astra max reviewed every output and independently checked the converted centroid,
ordered basis, recovered half-angle and side for every square.
The criterion is met; no algebraic-endpoint or global-optimality statement follows.

Per-command wall times sum to7.91 seconds: conversion 1.74, stock target 1.74,
independent target0.36, source target 0.26, and four controls 3.81. Maximum measured
resident memory was73,400,320bytes across all commands.
These are single-run timings under contention, not a comparative benchmark.
Preparation, review and integration took minutes; exact target arithmetic was not the
bottleneck. The raw receipts and machine-readable summary preserve the breakdown.

The verified frontier upper field is not changed in this experiment.
`think-vdmf` owns source-specific evidence and registry admission; `think-j516` owns the
next endpoint-chart discriminator.
The rational witness is an existing Kleddamag reconstruction of Bidwell’s packing, not a
new packing discovered by this session.

## Publication Correction

D-511 affects the raw witness’s schema pointer, not its geometry.
The [portable copy](../results/exp-235-n17-rational-upper/portable-witness.yaml)
resolves its schema without fallback and preserves the original witness payload exactly.
The
[normalization receipt](../results/exp-235-n17-rational-upper/portable-witness-receipt.json)
records that equality.
The raw accepted output and every run log remain unchanged.
The [independent output review](../results/exp-235-n17-rational-upper/output-review.md)
retains the exact fidelity audit and its scope.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
