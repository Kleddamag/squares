---
title: "exp-241 \u2014 n17 closed-assignment D4 census"
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-241
  series: series-000
  title: Exact D4 quotient of closed n17 occupancy assignments
  date: '2026-10-01'
  hypotheses:
  - H-260
  tier: confirmatory
  subject:
    label: H259closedcover with existential closed-cell assignments;row-majorcapacities; completeD4action.
    engine: devtools.count_grid_symmetry and independent devtools.audit_grid_symmetry
    assurance: verified
    method: exact-algebraic
    host_system: macOS ARM64, projectPython3.14, standardlibrary integer arithmetic,oneworker
    selftest_passed: true
  instance:
    axis: n
    point: 17
    role: target
  method:
    control: 29target-free controls:17producer including tiny-grid brute-force andD4group closure/inverses,12independent
      binomial/mutation controls. Ruff andBasedPyrightclean; independentstaticmath/code review.
    candidate: Eight fixed-state counts for5by5cap1boundary/cap2interior cover atn17; no lex seam exclusion.
    runs_per_condition: 1
    interleaved: false
    operator: Codex Session165 coordinator
    entry_point: packing/devtools/count_grid_symmetry.py
    command: 'From packing: .venv/bin/python3 -m devtools.count_grid_symmetry --input frozen-grid-JSON;
      audit receipt using devtools.audit_grid_symmetry. Exact commands retained in run-001.'
    budget: Readiness14:15UTC,target/review14:25UTC;one30second combined group,oneworker,1MiB peroutput.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/exp-241-n17-closed-cell-symmetry/run-001
    dirty: false
  results: []
  verdict:
    decision: in-progress
    primary_criterion: Exact eight-term agreement, valid D4closedassignment action, sum divisible by8,
      identityH259match and strictly fewer orbits than161100756.
    reason: Controlled instruments ready14:14UTC before cutoff; target awaits frozencommit.
    needs_review: true
  lease:
    expires: '2026-10-01T14:25:00Z'
---
# exp-241: n17 Closed-Assignment Symmetry Census

[H260](../../../hypotheses/H-260-n17-closed-cell-symmetry.md) fixes the complete group,
geometric domain, polynomial audit and limits before target evaluation.
No target symmetry count has been observed.
The known H259identity count is an explicit control.

The independently reviewed closed-assignment domains cover all packings up to physical
symmetry. Lexicographic seam restrictions are absent.
The count measures necessary occupancy orbits only and excludes no geometric case.

Acceptance requires a frozen controlled implementation, separate polynomial auditor and
full output review.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
