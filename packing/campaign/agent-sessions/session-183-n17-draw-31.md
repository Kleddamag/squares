---
title: "Session 183 — n17 draw 31"
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-183
  title: n17 Draw 31
  date: '2026-10-06'
  started_at: '2026-10-06T15:52:43Z'
  deadline_at: '2026-10-06T17:07:43Z'
  branch: claude/n17-session-183-u31
  primary_bead: think-2pjf
  status: in_progress
  goal: >-
    Run the one state of BC-428's frozen draw that exp-257 never reached, draw 31 (mask
    6015871, stratum c4/i>=5/d>=8), under exp-257's recipe and command unchanged and
    under a round registered before it starts, and land its verdict, and its admission
    if the standing verifier passes it in full, as a merge-ready pull request.
  workflow_phases:
  - workflow: review-planning-oversight
    focus: correctness
    recording: contemporaneous
    clock_role: work
    commitment: BC-429
    objective: >-
      The session's declared OR-5 entry point. Register BC-429, exp-258 and this record,
      pass the records tier, and commit and push the registration before the run starts.
    status: in_progress
    entered_by: session_start
    switch_reason: null
    budget_minutes: 15
    started_at: '2026-10-06T15:52:43Z'
    deadline_at: '2026-10-06T16:07:43Z'
    expected_output: >-
      The registration commit: BC-429 in agenda-042, exp-258 and this record, pushed to
      claude/n17-session-183-u31.
    validation_command: >-
      cd packing && uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: The records tier fails on something the registration cannot repair.
    fallback: Hold the run and report the refusal.
    outcome: null
    evidence:
    - packing/campaign/agendas/agenda-042-overnight-n11-settlement-and-low-n-angles.md
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-258-h275-n17-draw-31.md
    stop_reason: null
    next_action: Start draw 31 from the clean run worktree once the registration is pushed.
  budget:
    wall_minutes: 75
    slice_minutes: 50
    finalization_minutes: 10
  stop_conditions:
  - The session deadline at 17:07:43 UTC; nothing runs past it.
  - A producer that has not closed by 16:57:43 UTC is stopped unless its 7,000 s ceiling ends before the deadline, and the round is recorded as stopped by its timebox with resume_from.
  - A soundness alarm stops the instrument at once; its objects are preserved and nothing from it is admitted.
  - A verifier FAIL on the closure stops admission.
  - Below 1.5 GB of available memory or 2.0 GB of free disk, the run does not start; a resource kill is recorded, never read as an outcome.
  - The frozen recipe and the running job's ceiling are never changed.
  progress:
    metric: >-
      The certified n17 census (states and orbits under admitted sub-pattern
      certificates, the endpoint surviving), and BC-428's draws decided.
    before: >-
      36,792 states in 4,686 orbits certified under 57 admitted entries, the endpoint
      surviving (census_n17_certified at 00f320296); 29 of BC-428's 31 draws run to a
      verdict and draw 31 not run.
    after: >-
      Recorded at the close.
  delegations: []
  outputs:
  - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-258-h275-n17-draw-31.md
  - packing/campaign/agendas/agenda-042-overnight-n11-settlement-and-low-n-angles.md
  checks:
  - >-
    census_n17_certified at 00f320296: 36,792 states in 4,686 orbits, 57 admitted, the
    endpoint surviving.
  stop_reason: null
  next_action: >-
    Start draw 31 from the clean run worktree once the registration is pushed.
---
# Session 183: n17 Draw 31

BC-428’s seeded draw from H-264’s unsampled strata
([exp-257](../series/series-000-smoke-and-calibration/experiments/exp-257-h275-n17-unsampled-strata.md))
stopped on its clock with one state not run.
This session runs that state, draw 31, under BC-429 and
[exp-258](../series/series-000-smoke-and-calibration/experiments/exp-258-h275-n17-draw-31.md),
with exp-257’s recipe and command unchanged, from the clean run worktree at `cebb5d15a`.
The registration is committed and pushed before the run starts.

## Log

- **Registration.** BC-429, exp-258 and this record, before the run.
  The census at `00f320296` is 36,792 states in 4,686 orbits under 57 admitted entries,
  the endpoint surviving.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
