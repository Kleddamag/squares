---
title: "Session 161 — wand125’s Update and the 28 September Intake"
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-161
  title: wand125’s Update and the 28 September Intake
  date: '2026-09-28'
  started_at: '2026-09-28T23:26:00Z'
  deadline_at: '2026-09-29T11:26:00Z'
  branch: claude/magical-davinci-ueqmu1
  primary_bead: think-1an7
  status: stopped
  ended_at: '2026-09-29T07:12:33Z'
  certification_pending: think-l6la
  goal: >-
    Retain the update wand125 sent the owner, then take in what it and the collaborating
    repositories published on 27 and 28 September: evand’s s(21) = 5 and s(45) = 7,
    wand125’s point-only routes to both, its rectangle certificates to n = 95 and
    s(50) >= 37/5, and Guzhou0806’s s(17) > 116511/25000. Replay each here, have Fable
    max review every new argument before it is registered, register what epistemics.md
    derives, and publish it.
  workflow_phases:
  - workflow: research-survey
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: >-
      Retain wand125’s two X messages and the lower-bound table they link, map each
      claim to the register, and file the follow-up beads.
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 30
    started_at: '2026-09-28T23:26:00Z'
    deadline_at: '2026-09-28T23:56:00Z'
    expected_output: >-
      A retained packet with the messages and a byte capture of the table, and an epic
      with one bead per follow-up.
    validation_command: >-
      cd packing && uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: The messages cannot be tied to any retained source.
    fallback: Record the messages alone, with the owner as the source.
    outcome: >-
      The messages and the table (SHA-256 560ec3d6…) are retained in
      packing/resources/web/wand125-x-update-2026-09-28/ with a claims-to-record map, and
      epic think-1an7 carries eleven follow-up beads, the solver comparison the owner
      asked for among them.
    evidence:
    - packing/resources/web/wand125-x-update-2026-09-28/README.md
    stop_reason: The note is retained and every claim has an owning bead.
    next_action: Take the claims in, per the owner’s “research and add”.
  - workflow: factual-review
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: >-
      Retain and replay evand’s s(21) = 5 and s(45) = 7 bundles at 6aa82ba, wand125’s
      point-only s(21) and s(45) certificates, its rectangle certificates at 39d8ecc and
      its own-verifier s(50) certificates, and Guzhou0806’s R067 and R068; review each new
      argument with Fable max; register what epistemics.md derives.
    status: stopped
    entered_by: user_request
    switch_reason: >-
      The owner asked for the reported results to be researched and added. The upstream
      repositories had moved past the note: evand published both covers with two checkers
      each, wand125 added a point-only s(45) = 7 and s(50) >= 37/5, and Guzhou0806
      published s(17) > 4.66018 and > 4.66044.
    budget_minutes: 480
    started_at: '2026-09-28T23:47:00Z'
    deadline_at: '2026-09-29T07:47:00Z'
    expected_output: >-
      Retained packets with receipts, dated Fable max reviews, register entries, case
      records, regenerated views and atlas, and README and SYNOPSIS credits.
    validation_command: >-
      cd packing && uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: A replay fails or a review finds a gap the certificate does not close.
    fallback: Record the claim as reported but unverified, with the finding.
    outcome: >-
      Registered s(17) > 116511/25000 (T-043), s(21) = 5 (T-052), s(45) = 7 (T-053),
      wand125's point-only routes (T-054, T-055) and the reported s(50) >= 37/5 (T-048),
      each after its Fable max review, and published them in README, SYNOPSIS and the
      atlas through jlevy/squares#241 and jlevy/squares#243, both merged. The retained
      zmx2 run on the s(32) point cover was recorded as a second method in
      jlevy/squares#245, which a later session's review (2026-09-29) amended before
      merge. The complete zm_mixed.py re-sweeps for s(21) and s(45) did not finish.
    evidence:
    - packing/resources/web/wand125-rectangle-certificates-2026-09-28/README.md
    - packing/resources/web/evand-square-packing-2026-09-28/README.md
    - packing/resources/web/wand125-point-and-mixed-2026-09-28/README.md
    - packing/resources/web/n17-guzhou-r068-2026-09-28/README.md
    - docs/project/reviews/review-2026-09-28-wand125-n50-mixed-verifier.md
    - docs/project/reviews/review-2026-09-28-n17-guzhou-r067-r068.md
    - docs/project/reviews/review-2026-09-28-evand-s21-s45-mixed-covers.md
    - docs/project/reviews/review-2026-09-28-wand125-point-only-s21-s45.md
    - docs/project/reviews/review-2026-09-28-density-solver-comparison.md
    stop_reason: >-
      The session ended at 07:12Z with jlevy/squares#245 open and its phase deadline
      passed; the registrations it set out to make had landed, and the re-sweeps it
      started had not finished. Stopped, not completed: no qualifying gate pass covers
      the handover, so the debt is named under think-l6la.
    next_action: >-
      Under think-l6la: run the complete zm_mixed.py --d4 --cert-mode re-sweeps for
      s(21) and s(45), record them, and raise T-052 and T-053 to C4.
  budget:
    wall_minutes: 720
    slice_minutes: 480
    finalization_minutes: 90
  stop_conditions:
  - The owner ends the run; a self-declared budget is not a stop condition (OR-8).
  - No register entry without a Fable max review and an epistemics.md derivation.
  - Archived source material is retained byte-for-byte and never edited.
  progress:
    metric: New external bounds retained, replayed, reviewed and registered.
    before: >-
      s(21) >= 5000/1001 and s(17) > 466001/100000 verified; s(45) verified only at
      Nagamochi’s 1 + sqrt(34); wand125’s rectangle bounds registered at ad43d29 for 44
      counts from n = 18 to 78, three of them verified; s(50) reported at Green’s
      7.317426.
    after: >-
      s(17) > 116511/25000, s(21) = 5 and s(45) = 7 verified and registered (T-043,
      T-052, T-053); wand125's point-only s(45) = 7 replayed as a second certificate
      (T-054); s(21) point-only and s(50) >= 37/5 registered as reported (T-055, T-048);
      wand125's rectangle bounds at 39d8ecc registered for 50 counts, three verified.
  resource_rollups:
  - packing/campaign/resource-usage/b85b7ecf-955c-5223-9481-e5200885a948.yaml
  - packing/campaign/resource-usage/agent-a1599f925da991e56.yaml
  - packing/campaign/resource-usage/agent-a3a70f9027a6dfb47.yaml
  - packing/campaign/resource-usage/agent-a5b0a102d2ad6bfeb.yaml
  - packing/campaign/resource-usage/agent-a7497e51ab0c6ab3e.yaml
  - packing/campaign/resource-usage/agent-a925fccaaa104c764.yaml
  - packing/campaign/resource-usage/agent-ac9d1dadcb7d744d7.yaml
  - packing/campaign/resource-usage/agent-acb0d6d1650de489e.yaml
  - packing/campaign/resource-usage/agent-ad0d0d7f65651db68.yaml
  - packing/campaign/resource-usage/agent-af1471303a5fd7a0f.yaml
  delegations: []
  outputs:
  - packing/resources/web/wand125-x-update-2026-09-28/README.md
  - packing/resources/web/wand125-rectangle-certificates-2026-09-28/README.md
  - packing/resources/web/evand-square-packing-2026-09-28/README.md
  - packing/resources/web/wand125-point-and-mixed-2026-09-28/README.md
  - packing/resources/web/n17-guzhou-r068-2026-09-28/README.md
  - docs/project/reviews/review-2026-09-28-density-solver-comparison.md
  checks: []
  stop_reason: >-
    Stopped at 07:12Z, when the session opened jlevy/squares#245 and ended; its
    registrations are merged, and its unfinished replays and the uncertified handover
    are named under think-l6la rather than reported as passed.
  next_action: >-
    Under think-l6la: run the complete zm_mixed.py --d4 --cert-mode re-sweeps for s(21)
    and s(45), record them, and raise T-052 and T-053 to C4.
---
# wand125’s Update and the 28 September Intake

On 28 September wand125 wrote to the owner that the known-best PDF lagged the field:
evand had proved `s(21) = 5` and `s(45) = 7`, and wand125’s rectangle certificates now
improved most counts from `n = 18` to `95`. The owner asked for the note to be kept, for
follow-up beads, and then for the results to be researched and added.

The sources had moved again by then.
evand’s repository carries both covers with two independently written checkers each and
reports kernel-checked Lean proofs of `s(13) = 4` and `s(32) = 6`; wand125’s adds
point-only certificates for `s(21) = 5` and `s(45) = 7` and `s(50) >= 37/5` on its own
verifier; Guzhou0806’s publishes `s(17) > 116511/25000` without having run it locally.
This session retains each, replays it here, has Fable max review it, and registers what
the evidence supports.

## Recovery State

Work still running on 2026-09-29 at 01:50 UTC, and how to collect it.
A successor collects each item in the same way; nothing below is registered until its
receipt is committed.

| Work | Where it runs | Where the receipt lands | Bead |
| --- | --- | --- | --- |
| Full `zm_mixed.py` re-sweep of Daniel’s `s(21)` cover (second method, for `C4`) | Cloud session `session_011CfRigVmuCke9r31UzDPhM` | Branch `claude/replay-evand-s21-zm-mixed`, `transfer/evand-s21-zm-mixed-full/` | `think-l6la` |
| The same for `s(45)` | Cloud session `session_01Xt9EM5JEiNoK5aSsWz6E6x` | Branch `claude/replay-evand-s45-zm-mixed`, `transfer/evand-s45-zm-mixed-full/` | `think-l6la` |
| Coverage replays of 45 wand125 rectangle certificates, in ten batches of about 13 CPU-h | Cloud sessions listed on `think-20mv` | Branches `claude/replay-wand125-rect-b01` to `b10`, `transfer/wand125-rect-bNN/` | `think-20mv` |
| Complete replay of wand125’s `s(50) >= 37/5` (L740), about 10.5 CPU-h | This host, three workers | The command and its check are in the point-and-mixed packet README, “Pending: the complete L740 replay” | `think-nnlg` |
| wand125’s point-only `s(21)` portable replay, frontier stage | This host, two workers | `n21-compare` in the same packet README | `think-ifsv` |

A cloud replay of the `s(50)` certificate refused to run the external checker under its
session’s permission classifier and pushed only that refusal, on
`claude/replay-wand125-n50-l740`; the replay runs here instead.
Each batch writes its own `audit.json` beside its `rect_n*/` directories.
`audit_wand125_rectangles --resume` keeps only cases already in the output’s
`audit.json`, so merging the batches into one packet receipt needs a merge step in that
tool, which does not exist yet (`think-0rrj`); re-running `--resume --replay` on copied
directories would replay them again.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
