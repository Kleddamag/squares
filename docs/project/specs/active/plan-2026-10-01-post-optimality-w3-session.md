# Plan: Transfer Recent Optimality Methods to n = 17 and Other Low Cases

**Date:** 2026-10-01

**Status:** Planned; execution has not started

**Workflow:** W3 insight iteration → W10 selection and codification → bounded W6
execution, with W7 only for a missing instrument and W2 for high-risk or promoted
claims.

**Tracking:** `think-7x1u` (program), `think-nb6b` (this planning deliverable).

## Objective

Find a credible route to another low-n optimality theorem, with n = 17 first.
Use the recent n = 11 global optimality proof and other imported results to identify
which structural lemmas, certificate mechanisms, and verification tools transfer.
The next session starts with mathematical exploration; tooling work serves a selected
proof obligation.

## Branch and Evidence Baseline

Branch `codex/w3-post-optimality-transfer` starts at `751ef78a4` on
`codex/n11-explainer-doc-review`, the head of
[PR #261](https://github.com/jlevy/squares/pull/261). The research baseline also
includes merged main at `f9a3409f0f03298fbeeb0a03788cd016087626b9`, read without
importing unrelated website changes into this stack.
Before execution, re-read current main and reconcile the result records and epistemic
ratings again. Integrate main after the parent merges, preserving the clean stacked diff
until then.

## Research Basis

[X-048](../../../../packing/campaign/explorations/X-048-n17-optimality-after-n11.md)
maps nine routes, their mathematical obligations and their first discriminators.
The initial selection is n17 first, n12 in parallel, and n20 as the first fallback.
n18 and n19 remain structural alternatives; n26 and n29 are reserve targets.
n11 and n21 supply accepted machine-checked controls and reusable arguments.

Three facts determine the opening work:

- n17 has a verified strict lower bound 4.66044 and a reported Bidwell packing at
  4.675530…, but the verified upper field is still 5. Exact candidate admission has its
  own proof obligations.
- The retained n17 witness has numerical evidence of sliding squares.
  Seek a side theorem for a family or backbone, not isolated coordinates.
- An elementary n17 centre grid already yields over eight billion raw occupancy masks.
  Price geometric pruning before building a complete enumeration.

The n12 additive obstruction reported by evand needs source recovery and an independent
check; its missing auxiliary files are recorded in X-048. Do not substitute an
unverified obstruction for a proved impossibility theorem.

## Goal Hierarchy

1. **Scientific goal:** obtain a new global optimality theorem, or a decisive
   obstruction to a proposed route, prioritizing n17.
2. **Immediate mathematical goal:** select a credible global exclusion/capture route and
   a compatible endpoint theorem; investigate a direct endpoint measure in parallel.
3. **Supporting verification goal:** exact upper witnesses, complete closed-domain
   coverage, clear certificate interfaces and independent acceptance.
4. **Supporting efficiency goal:** cheap discriminators and measured throughput on the
   selected proof work.
   Native-code optimization is selected only by a measured bottleneck, not made a
   prerequisite for mathematical exploration.

This planning block changes no theorem, bound, rating, verifier or production default.
The owner has requested a new W3 entry.
The older synopsis handoff remains historical context; this plan does not rewrite
another session’s completion record or close its remaining verification beads.

## Next Session: Parallel Lanes and Checkpoints

Create the actual session record when execution begins, using the next available session
ID and real start/deadline fields.
Do not reserve a fictional started session now.
Use the existing campaign and schemas; no new experiment framework is needed.

| Checkpoint | Work in parallel | Deliverable and exit |
| --- | --- | --- |
| Opening W3 | A: n17 endpoint/family; B: n17 occupancy/charge; C: low-n endpoint transfer | Each lane returns source-pinned assumptions, one strongest candidate, a falsifier, tool readiness and a cheapest useful test |
| W10 selection | Coordinator reconciles all lanes; Astra max checks the mathematical bridge; Sol checks executable contracts | Select one n17 discriminator and at most one secondary target, or retain explicit blockers if none is ready |
| W6 or narrow W7 | Run independent selected work concurrently; build only a named missing checker or producer seam | Fixed criterion and controls, frozen implementation before target measurement, durable output and all unresolved cases |
| W2 checkpoint | Independent mathematical review and implementation/evidence audit | Accept, refute, remain unresolved, or block; update claims only to the level the evidence supports |
| W5 checkpoint | Profile the measured bottleneck while other proof obligations proceed | A bounded improvement or rejection under unchanged correctness controls; return to the scientific lane |
| Integration | Coordinator updates the exploration, selected agenda entries, beads and PR | Every selected item has a disposition and next evidence; all completed evidence is committed and discoverable |

The opening W3 block is an actual research task, not a repeat of the intake survey.
Start from X-048 and challenge its strongest routes.
Do not restart broad literature ingestion unless a named missing source affects the next
decision.

### Lane A: Candidate Endpoint and Flexible Family

**Bead:** `think-s6ty`. **Owner roles:** Astra max mathematics; Sol implementation
assessment when needed.
**Write ownership:** a dedicated endpoint review or result directory selected at launch;
no shared frontier edits.

Inspect the Bidwell witness, coordinate precision, algebraic root and contacts.
Separate a relaxed feasible upper enclosure from an exact endpoint construction.
Identify free sliding parameters and test whether a backbone side inequality can be
proved uniformly over them.
Return the missing hypotheses and the smallest exact subsystem to check first.
Local side minimality alone does not establish global optimality.

### Lane B: Global Cover, Charge and Endpoint Alternatives

**Bead:** `think-70sf`. **Owner roles:** Sol tooling/geometry inventory, with Astra max
review of proposed lemmas.
**Write ownership:** a separate global-route note and prospective instrument contract.

Compare closed centre covers, R068 low-charge compatibility, direct endpoint measures
and subconfiguration cuts from settled cases.
Count or bound cases before expensive geometric exclusion.
Reuse H-248 / BC-387 for the capacity-one architecture fork; do not repeat its claim
under a new ID. Keep exact finite-program improvement separate from full continuous
verification.

### Lane C: Low-n Alternatives

**Bead:** `think-ayt3`. **Owner role:** Sol research and source comparison, with an
Astra max check for any selected new mathematical implication.
**Write ownership:** a low-n comparison note.

At n12, recover the reported fractional obstruction’s missing evidence and study
conditional occupancy rather than an unrestricted additive endpoint search.
At n20, identify the precise count or boundary condition lost from the n21 proof.
Use n18/19 only when a small endpoint subsystem or new global inequality makes them
competitive with those two routes.
No stronger reported lower bound enters the verified column without W2 acceptance.

### Coordinator: Select and Freeze

**Bead:** `think-eh7g`, blocked on the three opening lanes.
Reconcile the current active
[agenda-042](../../../../packing/campaign/agendas/agenda-042-overnight-n11-settlement-and-low-n-angles.md)
and its stale n11/n21 objectives.
At W10, either add current BC commitments there or explicitly disposition the old agenda
before creating a successor.
BCs, H-IDs and exp-IDs are allocated only when their artifacts are ready, not invented
as placeholders in this plan.

For each chosen experiment freeze:

- Target domain, rational cap or exact endpoint, source revisions and all assumptions
- One falsifiable criterion, including how failure differs from unresolved work
- Positive controls, adversarial refusals and the independent acceptance interface
- Input set, process/memory/node/output limits and timeout behavior
- Producer and checker commands, output location, resume policy and owner
- Mathematical payoff: a usable lemma, a complete case exclusion, a route obstruction,
  or a cost estimate that changes the next decision

The opening three agents can work concurrently within the available four slots,
including the coordinator.
After their reports arrive, reuse slots for implementation and adversarial review.
No two agents mutate the same registry, idea board, agenda or frontier record.
The coordinator owns those shared records and the PR.

## Validation and Efficiency

For this documentation-only plan, validate exploration schema, local links, document
map, generated synopsis and idea-board/ledger consistency.
Do not replay the n11 proof or run unrelated slow local tests to validate prose.
The normal hosted checks still apply to the PR.

For future proof work, first run a small known-valid case and a deliberately invalid
case through the exact acceptance path.
Record complete coverage, pending cases and skipped checks explicitly.
Use source checkers as comparison oracles while keeping a separately reviewed native
acceptance path for claims requiring independence.
Tools currently bound to n11 data require adaptation and review before n17 use.

Measure preparation, producer, checker and orchestration costs separately.
Record wall time, CPU, memory, case/node counts and output size for a fixed workload.
Parallelize independent cases and reviews; keep compilation caches and loaded input data
reusable when equivalence is preserved.
Run one representative end-to-end case before committing to a full census.

The first W5 checkpoint is after at most four execution blocks, and earlier if a
declared ceiling is missed or repeated setup dominates useful work.
Freeze the metric, workload, validity guards and stopping rule before timing a candidate
improvement. If compilation, orchestration or general CI is slow, improve that layer; do
not attribute it to rational arithmetic without a profile.
W5 runs beside independent mathematical work and cannot weaken the proof contract.

All temporary builds and caches use a verified writable external scratch directory with
explicit `TMPDIR`, `CARGO_TARGET_DIR` and `UV_CACHE_DIR`. Unique research evidence lives
in the repository, not disposable scratch.

## Completion and Publication

The planning deliverable is complete when X-048, this run sheet, the idea-board entry
and linked beads are reviewed and published on the stacked PR. The future session is
complete at a coherent evidence checkpoint, with each selected route explicitly
accepted, refuted, unresolved, blocked or deferred with its reason.
It need not claim a new theorem to leave a useful result.

Keep the PR based on `codex/n11-explainer-doc-review` while #261 is open.
Once the parent merges, reconcile current main and retarget the child to main, checking
that its diff contains only this research planning work.
Run focused checks again after conflict resolution and keep the PR’s evidence and
disposition tables current.
Do not merge this child ahead of the required parent integration.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
