---
title: "Session 182 — n17 overnight lanes"
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-182
  title: n17 Overnight Lanes
  date: '2026-10-05'
  started_at: '2026-10-05T08:14:04Z'
  deadline_at: '2026-10-06T08:14:04Z'
  branch: claude/n17-session-182-overnight
  primary_bead: think-tmz6
  status: in_progress
  goal: >-
    Make as much measured progress on s(17) = S* as one night on this container allows:
    certified exclusions that lower the residue below 126,168 states in 15,953 orbits,
    each admitted by a standing verifier's full pass, and the decisive planning evidence
    of H-264's per-state price, lane R9's capture route and the mixed-flag stalls.
  workflow_phases:
  - workflow: review-planning-oversight
    focus: insight
    recording: contemporaneous
    clock_role: work
    commitment: BC-418
    objective: >-
      The run's declared OR-5 entry point. Codify H-264 by rewriting it in place,
      register BC-419 and BC-420, freeze lane K's target list from the census at the
      registration commit, read the OR-12 count, create the lane beads and publish the
      registration before the first target run.
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 60
    started_at: '2026-10-05T08:14:04Z'
    deadline_at: '2026-10-05T09:14:04Z'
    expected_output: >-
      The registration commit: H-264 rewritten, BC-419, BC-420 and BC-422, the frozen
      kernel target list, this record and the plan.
    validation_command: >-
      cd packing && uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: The records tier fails on something the registration cannot repair.
    fallback: Hold every target run and report the refusal to the coordinator.
    outcome: >-
      H-264 rewritten with instrument_ready true on the seed-182 draw (10 counted, 2 at
      distance 2). Nine kernel targets frozen: the plan's filter at this tree admits one
      class more than the review's eight, at best penetration 0.0050045 on the default
      receipts against 0.0049995 on the recheck list the review read. The OR-12 count
      is past eight (34 cells terminal since BC-369; nine sessions since session-180's
      efficiency-loop phase), so BC-422 adds the W5 block without dedicated compute.
    evidence:
    - packing/campaign/hypotheses/H-264-n17-geometric-exclusion-cost-per-leaf.md
    - packing/campaign/agendas/agenda-042-overnight-n11-settlement-and-low-n-angles.md
    - packing/campaign/explorations/X048-session-182-overnight/kernel-targets.txt
    stop_reason: The registration is committed and pushed before the first target run.
    next_action: W6 coordination of lanes A and K and the dispatched lanes.
  - workflow: research-loop
    focus: correctness
    recording: contemporaneous
    clock_role: work
    commitment: BC-418
    objective: >-
      Run lanes A (BC-419) and K (BC-420) from the clean run worktree on three compute
      slots, admit each closure a standing verifier passes in full, and coordinate the
      dispatched lanes R, D and H; re-plan only future slices at each check-in.
    status: in_progress
    entered_by: planned_checkpoint
    switch_reason: The registration is published, so measurement may begin.
    budget_minutes: 360
    started_at: '2026-10-05T08:30:00Z'
    deadline_at: '2026-10-05T14:30:00Z'
    expected_output: >-
      Per-target and per-state receipts for lanes A and K, admitted certificates with
      their verifier receipts, and the census before and after.
    validation_command: >-
      cd packing && uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: >-
      A soundness alarm: the kernel closes the endpoint's state or endpoint7, the branch
      and bound certifies an endpoint control, or a census reports the endpoint not
      surviving.
    fallback: >-
      Preserve every object, record a defect, admit nothing from that instrument, and
      escalate to the owner in the handoff.
    outcome: null
    evidence: []
    stop_reason: null
    next_action: >-
      The morning checkpoint at 14:30 UTC, which hands off without stopping the run
      (OR-8).
  budget:
    wall_minutes: 1440
    slice_minutes: 30
    checkpoint_minutes: 240
    finalization_minutes: 60
  stop_conditions:
  - Only the owner, an external blocker or exhausted work ends the run; a self-declared budget is not a stop condition (OR-8).
  - A soundness alarm stops that instrument at once; its objects are preserved, a defect is recorded and nothing from it is admitted.
  - A verifier FAIL on a producer closure stops admissions from that producer until a review.
  - Three consecutive crashes or refusals of one instrument stop that instrument.
  - Below 1.5 GB of available memory or 2.0 GB of free disk, no new job launches; a resource kill is recorded, never read as an outcome.
  - Frozen criteria and a running job's ceiling are never changed; only future slices are re-planned.
  progress:
    metric: >-
      The certified n17 census (states and orbits under admitted sub-pattern
      certificates, the endpoint surviving), and H-264's counted closures against its
      falsifier.
    before: >-
      126,168 states in 15,953 orbits certified (W7, A, SW9 and N1 admitted); H-264
      without a ready registration; the adaptive-row recipe that closed SW9 never run
      on the mixed arity-7 flags.
    after: null
  delegations:
  - task: >-
      W3 status review of X-048 on the stack top (the draft addition, a phase-1 report
      and notes), followed by an adversarial Opus review of the draft
    operator: Opus sub-agents
    status: completed
    recording: retrospective
    outcome: >-
      Written before this run's clock started; recorded as the history this W10 phase
      acts on. The review's findings F1 to F19 found H-264 unready and mis-scoped, the
      capture continuation unresumable, three instruments needing tool changes, and
      flag certification the cheapest direct census progress.
    evidence:
    - docs/project/specs/active/plan-2026-10-05-n17-overnight.md
    files: []
    checks:
    - The review re-ran the certified census at 451154f60 and the seed-182 draw (strata only).
    uncertainty: >-
      The draft and review live in the coordinator's scratchpad; the plan carries the
      consequences that the night acts on.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Lane H integrates the corrected addition into X-048 (H3).
    phase: 1
  - task: >-
      Run operator: preflight, the registration commit and draft PR, the clean run
      worktree, and the background queues for lanes A and K
    operator: Opus sub-agent at high effort
    status: in_progress
    recording: contemporaneous
    outcome: null
    evidence: null
    files:
    - packing/campaign/hypotheses/H-264-n17-geometric-exclusion-cost-per-leaf.md
    - packing/campaign/agendas/agenda-042-overnight-n11-settlement-and-low-n-angles.md
    - packing/campaign/explorations/X048-session-182-overnight/kernel-targets.txt
    - packing/campaign/agent-sessions/session-182-n17-overnight-lanes.md
    - docs/project/specs/active/plan-2026-10-05-n17-overnight.md
    checks: null
    uncertainty: null
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Keep the queues running and admit closures with a verifier pass at each check-in.
    phase: 2
    budget_minutes: 380
    started_at: '2026-10-05T08:14:04Z'
    deadline_at: '2026-10-05T14:30:00Z'
    expected_output: >-
      The pushed registration commit and draft PR, lane A and K receipts under the
      scratch output tree, and verifier receipts for every closure.
    validation_command: >-
      cd packing && uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: A soundness alarm, or the resource guards of the plan.
    fallback: Stop the affected queue, preserve its objects and report to the coordinator.
    write_scope:
    - The registration files above, admissions in the session checkout, and scratch outputs outside every worktree.
    excluded_commands:
    - Edits in the run worktree; changes to the wtn17stack or wt307fix worktrees.
  - task: Lane R, the capture route (lane R9, think-g2qn), from committed receipts
    operator: Fable sub-agent at max effort
    status: completed
    recording: contemporaneous
    outcome: >-
      Undecidable from the receipts with most of the question decided: none of the four
      named producer candidates is the limit, and an unnamed producer loss (the owned-hull
      compression toward the vertex mean, about 1.22e-4 at unit scale) is present and
      quantified; the review specifies the discriminating measurement for a later slice.
    evidence:
    - docs/project/reviews/review-2026-10-05-n17-capture-r9.md
    files:
    - docs/project/reviews/review-2026-10-05-n17-capture-r9.md
    - packing/campaign/explorations/X048-session-182-overnight/receipts/R9/score-pilot2-need-r9.json
    - packing/campaign/explorations/X048-session-182-overnight/receipts/R9/score-pilot2-need-r9.txt
    checks:
    - One run of devtools.score_n17_capture at 451154f60 reproduced the committed score table.
    uncertainty: >-
      The verdict rests on committed receipts; the measurement it specifies has not run.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: The coordinator codifies any candidate at the morning W10.
    phase: 2
  - task: Lane D, classification of lane K's and lane A's kernel stalls
    operator: Fable sub-agent at extra-high effort
    status: completed
    recording: contemporaneous
    outcome: >-
      K-k2 is loss-limited (knot owners interior-NW and interior-W at 0.5 and 4.5 per cent
      support, median cut margins near 0.010 against the 1/512 core loss), stopped at its
      round cap with producer time unused. The distance-4 and distance-6 per-state stalls
      share a wall knot whose margins (about 0.011 to 0.015) sit below the 1/32 losses of
      N1's recipe but above a 1/512 cut; the distance-2 draw 1964767 is
      consistency-limited at a true fixed point. C2 (aimed splits) is selected before C5.
    evidence:
    - docs/project/reviews/review-2026-10-05-n17-stall-classification.md
    files:
    - docs/project/reviews/review-2026-10-05-n17-stall-classification.md
    - packing/campaign/explorations/X048-session-182-overnight/receipts/stall-diagnosis/
    checks:
    - diagnose_n17_flag support and domains on each stall node, at nice 19 while the one-minute load was below 6.
    uncertainty: >-
      Deviation: the per-state nodes were diagnosed at 100 poses per owner, not 400, because
      400 did not finish inside the 1,200 s ceiling at the night's load (the receipts are
      suffixed -s100); the share estimates widen to about 5 percentage points.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: BC-423 and BC-424 test its two readings; the nodes were deleted once its receipts named them.
    phase: 2
  - task: Lane H, census reads the recheck, the survey distance filter, and the X-048 addition
    operator: Opus sub-agent at high effort
    status: completed
    recording: contemporaneous
    outcome: >-
      H1, the census projects the selector recheck's still-flagged classes by default; H2,
      survey_n17_residue --distance D with --sample 0; H3, the X-048 October 5 status
      addition. The coordinator committed and merged them on the session branch.
    evidence:
    - packing/devtools/census_n17_certified.py
    - packing/devtools/survey_n17_residue.py
    - packing/campaign/explorations/X-048-n17-optimality-after-n11.md
    files:
    - packing/devtools/census_n17_certified.py
    - packing/devtools/survey_n17_residue.py
    - packing/tests/test_census_n17_certified.py
    - packing/tests/test_survey_n17_residue.py
    - packing/campaign/explorations/X-048-n17-optimality-after-n11.md
    checks:
    - The census and survey test files pass on the session branch.
    uncertainty: >-
      The survey later gained --shard K/N in this session (504a84464) for lane E, outside
      lane H's own commits.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: None for the lane.
    phase: 2
  outputs:
  - packing/campaign/hypotheses/H-264-n17-geometric-exclusion-cost-per-leaf.md
  - packing/campaign/agendas/agenda-042-overnight-n11-settlement-and-low-n-angles.md
  - packing/campaign/explorations/X048-session-182-overnight/kernel-targets.txt
  - docs/project/specs/active/plan-2026-10-05-n17-overnight.md
  checks:
  - >-
    census_n17_certified at the session checkout (451154f60 plus the registration's
    record edits): 126,168 states in 15,953 orbits, 4 admitted, endpoint surviving; the
    plan's kernel-target filter selects nine classes.
  - >-
    survey_n17_residue --flag-set arity8 --sample 12 --seed 182 --strata-only: the
    endpoint control plus 12 draws, 2 at distance 2, 7 at 4 and 3 at 6 (draw only, no
    search).
  stop_reason: null
  next_action: >-
    Run lanes A and K's queues from the run worktree, admit verified closures, and write
    the morning handoff at 14:30 UTC without stopping the run.
---
# Session 182: n17 Overnight Lanes

This session executes the
[n17 overnight plan](../../../docs/project/specs/active/plan-2026-10-05-n17-overnight.md)
under BC-418 (`think-tmz6`). It opened with a W10 phase, the declared entry point, which
rewrote [H-264](../hypotheses/H-264-n17-geometric-exclusion-cost-per-leaf.md) in place
and registered the night’s cells in
[agenda-042](../agendas/agenda-042-overnight-n11-settlement-and-low-n-angles.md) before
any target ran.

## Lanes

| Lane | Cell and bead | Workflow | What it runs |
| --- | --- | --- | --- |
| K, flag certification | BC-420, `think-035m` | W6 under H-267 | The endpoint7 control, then the nine frozen targets in [kernel-targets.txt](../explorations/X048-session-182-overnight/kernel-targets.txt) under SW9’s adaptive-row recipe. |
| A, per-state price | BC-419, `think-z8an` | W6 under H-264 | The float pre-screen on the seed-182 draw, the kernel control on the endpoint’s state, then twelve draws two at a time. |
| R, capture route | `think-jcte` | W3 | Lane R9’s verdict from committed receipts. |
| D, stall diagnosis | `think-023x` | W3 | Lane K’s stall nodes, loss- or consistency-limited. |
| H, records and tools | `think-ahe4` | W9 | The census reading the recheck, the survey’s distance filter, and the X-048 addition. |
| W5 block | BC-422, `think-9ntw` | W5 | Gate walls from the registration’s validation runs and per-row costs from the lanes’ receipts. |

Lanes A and K run only from a detached run worktree at the registration commit, which is
never edited. Every closure is re-proved there by a standing verifier in full before the
coordinator admits it in the session checkout.
Certificate objects stay out of Git (OR-18).

## Notes for the Morning Record

- For exp-251’s reviewer: lane K’s first target, K-k1, started at 09:07:12 UTC, after
  the registration commit `cebb5d15a` but about four minutes before its push; the commit
  hash, which every receipt names, still fixes the order.
- A container restart at about 10:32 UTC killed every process.
  Three jobs without receipts (A-m1964767, A-m2878207, K-k6) re-ran from scratch; every
  closure already had its verification receipt, and the queues resumed by skipping
  completed receipts.
- A second container restart killed every process: they stopped writing at about 12:45
  UTC and the container rebooted at 13:24:55. BC-423’s endpoint7 control (started 11:29,
  its producer done and its checker mid-run), BC-424’s endpoint-state control (started
  12:07) and lane E’s shard 3 left no receipts and re-ran from scratch at 13:29.
- Procedure changed at the coordinator’s direction after that restart: BC-423’s and
  BC-424’s controls now run beside their first target instead of before it, and
  admission, not launch, is gated on the control.
  A closure verified while its lane’s control is still running waits until the control
  finishes without closing; a control closure is still a soundness alarm that stops the
  instrument and voids the lane’s closures.
  Every soundness gate is kept.
  The reason: two container restarts in a day, and controls under the 48-round settings
  run to near their 7,000 s ceiling, so running controls serially doubled each lane’s
  exposure to a restart.
- K-k2 stopped at its 24-round cap with producer time unused, so `--max-rounds` is a
  free lever for lane K’s stalls; BC-423 tests it with lane D’s settings.
- Lane D diagnosed the per-state stall nodes at 100 poses per owner instead of 400,
  because 400 did not finish inside its 1,200 s ceiling at the night’s load.
- exp-252 (H-264) is accepted, confirmed with corrections by its W2 factual review; the
  review’s F1 corrects the attribution in the message of `6717b0b11`: state 5500414’s
  orbit was already excluded by SW9 (exp-250), not by lane K’s flags.
- Slices added at check-ins, each registered before its first run: BC-423 (K-k2 with
  lane D’s settings), H-273 and BC-421 (lane E, on slot 4, with the survey’s new
  `--shard`), and H-274 and BC-424 (lane A’s counted stalls under SW9’s recipe).
- The branch-and-bound queue’s Knuth list is frozen in `s182/K/bb/knuth-targets.txt`:
  the 34 flags with at most two wall cells (the recheck’s placed flag excluded) and
  kernel target 2. It waits for the slot after BC-423.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
