# Proof Verification Consolidation and Independent n11 Completion

**Date:** 2026-09-29\
**Status:** Reviewed; implementation pending\
**Workflow:** W7 pipeline improvement supporting W2 proof confirmation, with measured W5
work\
**Owners:** coordinator; Sol implementation; Astra at max reasoning for mathematical
review\
**Beads:** consolidation epic **think-7nkq**; mathematical goal **think-3i74**

## Overview

Consolidate PR #246 into separable proof, evidence, and integration components so that
independent verification of T-060 can proceed concurrently and remain reviewable.
The primary deliverable is a justified verdict on the claimed n11 global optimum.
Reducing the diff and simplifying tools support that deliverable; neither substitutes
for mathematical confirmation.

The user requests full validation by tomorrow morning.
The working checkpoint is **2026-09-30 at 08:00 America/Los_Angeles** (15:00 UTC); 08:00
is the planning assumption for “morning,” not an additional user-specified constraint.
Finish earlier if possible.
The schedule is a target, not evidence that the remaining proof will pass or fit.
A failed certificate binding, an incomplete computation, and a mathematical refutation
must remain distinct outcomes.

## Goals

1. Independently accept every required global proof obligation, or isolate a precise
   flaw or unresolved obligation with reproducible evidence.
2. Replace per-certificate orchestration with a small shared field runner, retaining
   independent mathematics and explicit supported certificate shapes.
3. Preserve every unique source, accepted result, failed run, and implementation
   identity while reducing duplicate evidence and verbose review output.
4. Decouple exact proof decisions, diagnostic search, source acquisition, and CI.
5. Keep proof workers active while unrelated repository integration runs separately.

## Non-Goals

A blanket verifier rewrite, a new plugin framework, changing the theorem to make checks
pass, or claiming a full publisher replay are outside this consolidation.
The rectangle-density engine remains a different mathematical contract.
PR history restructuring, log compression, atlas optimization, and the explainer do not
block the morning proof target.
The explainer remains gated on validation and simplification under think-uz2x and
think-08pw.

## Background and Baseline

At `0dda2856e`, PR #246 adds 59,419 lines and removes 483 across 240 files.
Of the additions, 30,071 are retained source/evidence, 9,710 session records and
accounting, 9,283 implementation/configuration including CI, 6,648
tests/fixtures/goldens, 3,705 prose/registers, and two generated atlas text lines.
Binary payloads are separate.
The n11 checkers account for 4,395 lines and their tests for 991. At least 3,420
result/stdout lines are duplicated; three JSON receipts contain 15,240 lines, and
session logs contribute 7,212. These are storage/review targets, not reasons to discard
evidence. Compression reduces review noise; it does not simplify mathematics.

Current acceptance is **1,112 exact exclusions of the claimed 2,180**; 1,068 remain.
Fixed-T local isolation is accepted.
D4 reduction and near-pose inclusion retain their stated premises.
The ten-node capture parent graph is structurally checked, but root induction and
transition geometry remain unaccepted.
All four published leaf audits have stale final-state bindings.
T-060 remains **S5/V0/C1**, with no optimum promotion.
The [proof review](../../reviews/review-2026-09-29-n11-optimality.md) owns current
mathematical status; this spec owns the implementation decomposition.

## Design

### Components and Dependency Direction

| Component | Responsibility and proposed boundary | Must not do |
| --- | --- | --- |
| Evidence reader | Bounded exact parsing, source pins, deterministic compression, decoded byte identity; share only after a second real consumer needs it | Interpret an upstream PASS, hash, or successful parse as a theorem |
| Field geometry | `packing/devtools/n11_field_geometry.py`: exact ownership, clipping, envelopes, odd-site median regions and closed-domain arrangement coverage | Read registries, invoke upstream verifiers, decide global completeness |
| Field runner | `packing/devtools/check_n11_optimality_field.py`: explicit immutable packet specification, capability admission, complete inventories, budget, exact case transfers and CLI | Silently broaden certificate grammar or accept a partial packet |
| Other proof components | Keep D4, local isolation, pose inclusion, root induction and capture transitions as separate consumers with explicit premises | Merge source-graph checks with geometric acceptance or reuse a conditional conclusion as its own premise |
| Proof composition | A small consumer joining accepted component identities, assumptions and exact ID sets | Promote from counts, progress logs, exit zero, or missing/unknown status |
| Rectangle diagnostics | Extract strict frontier admission from comparison/refinement; both call it, rather than importing each other’s CLI | Feed diagnostic search state directly into an accepted proof |
| Integration | Source/register publication, docs, release stamps and hosted checks | Make unrelated CI a prerequisite for the next proof job |

Reuse existing types and tools where they express these boundaries.
No general workflow engine, speculative backend interface, or repository-wide receipt
migration is required.
An independent checker may share our reviewed exact kernel; this is disclosed reuse, not
a distinct complete verification method.
Field exclusions reuse only the D4 checker’s unconditional cover, cell-capacity and
whole-half-turn facts; they do not depend on its conditional four-survivor reduction.
The local construction primitives also remain a disclosed shared dependency.

### Evidence and Historical Implementations

Keep published mask0/mask202 implementations and their receipts frozen as the baseline.
New extracted code writes new receipts bound to the full implementation dependency
closure, or a precise Git revision plus relevant paths.
Never rewrite a historical receipt to imply that it ran the replacement code.

Inventory path and hash consumers before repacking.
Preserve decoded bytes exactly; store deterministic gzip with decoded size/hash and a
concise readable summary.
Consolidate byte-identical stdout/results only after migrating all consumers and
provenance references atomically.
Unique failed and incomplete runs remain recoverable.
If a frozen executable requires the original path, retain it until a replay adapter is
proved; do not trade reproducibility for a smaller diff.

Raw source identity, compressed upstream LFS identity, and the publisher’s canonical
`final_state` digest are different checks.
Preserve each relevant contract, including duplicate-key rejection where required.
Do not normalize away the four binding defects.
Git remains the authority for ordinary repository integrity; extra cryptographic checks
are reserved for source and historical execution boundaries.

### Complete Versus Partial Results

A component result declares exact inputs, implementation, mathematical premises,
required/completed/pending obligations, and an explicit verdict.
Metadata-only, incomplete, refused, and accepted are different types of result.
A field packet contributes zero exclusions until ownership, all closed rows, transfer
arithmetic and final resource-limit checks complete.
A batch retains completed packets but computes its union from their exact accepted IDs,
never their reported counts.

Use the smallest sufficient certificate cover of the required case set.
It is not necessary to replay every redundant field certificate to prove the theorem.
Account for all remaining generic, extension and returned-case obligations; do not
extrapolate from the two supported field shapes.
Any further transfer beyond an existing proposal must be explicitly derived,
independently reviewed, and recorded as a new local deduction.

## Implementation Plan

### Phase 1: Minimal Shared Runner and Explicit Proof Contracts

- [ ] Inventory all remaining packet feature shapes and their marginal coverage, then
  identify the minimal supported adapters needed for a sufficient cover.
- [ ] Extract the first-party field kernel and common runner under **think-eewf**. Use
  explicit packet specifications for five-site mask0 and three-site mask202.
- [ ] Replay both controls once with new code and retain new receipts: exact 459 and 764
  case sets, union 1,112, plus complete ownership/row inventories.
- [ ] In parallel, specify and profile root/capture transition semantics on a bounded
  representative selection, including the large near trace.
  Measure complexity before choosing chunks or native-code optimization.
- [ ] Define composition against small accepted/incomplete/refused synthetic receipts
  now; bind real complete geometry later.
  Do not make capture wait for the field runner.

### Phase 2: Parallel Mathematical Completion

| Lane | Bead | Independent work and acceptance | Actual blockers |
| --- | --- | --- | --- |
| Exclusions, Sol | think-35ui under think-ncw8 | Verify a sufficient exact union covering all 2,180 required cases, with no missing IDs or unsupported grammar | Reviewed shared field runner think-eewf; separate adapters for uncovered certificate families |
| Root induction, Sol | think-mnd1 under think-pgie | Prove all eleven owners through root round 14, complete angular/center cover and cached-premise validity | Pinned root input closure and reviewed induction semantics |
| Capture transitions, Sol in the capture lane | think-5jp8 under think-pgie | Verify actual node transitions, three far contradictions and valid near domains, including all closed branch boundaries | Transition semantics; jobs may run conditionally before root acceptance |
| Mathematical audit, Astra max | think-3i74 | Review new rule families, strict inequalities, exact frames, no circular premises, and each completed receipt | Implementation/source evidence as it becomes available |
| Global composition, coordinator with Astra | think-36tg | Join exclusions, four-survivor reduction, root and branches, pose/local result, U-to-T argument and exact upper witness | Complete accepted mathematical dependencies, not CI or evidence compression |

The current runtime permits three subagents plus the coordinator: one Sol on exclusions,
one Sol on root/capture, and Astra max reviewing both.
Root and branch tasks are separate beads even when one Sol owns that lane.
Execute independent packet/node jobs in bounded worker processes; use additional agent
slots only if actually available.

The capture dependency graph is explicit:

```text
seed + cover → root14 → root-self → far15
                           └────→ r1 → r10 → far13
                                   └─→ near13 → r11 → r110 (far2)
                                                  └→ r111 → near
```

All three far closures and the near/local route are required.
The three far states need recomputed empty residuals over complete owner domains, not
recorded contradiction flags.
Near needs valid transitions through r111 and all near rows before its final state can
supply the accepted pose inclusion.
Composition also checks the owner-role bijection, exact field-to-centered frame, chart
endpoints, and construction wall span.

The capture lane is not a four-branch serial publisher replay.
Each node checks its transition conditional on exact parent state; parent validity is
joined through the acyclic dependency graph at composition.
Shared ancestors are verified once.
Owner, round and row chunks must form a complete inventory; a chunk boundary is never a
gap in the mathematical domain.

Known scale: root induction has 16,551 angular rows; its adaptive input is about 21.3 MB
compressed/136.8 MB decoded.
The ten cached capture sources total about 112.7 MB compressed/565.3 MB decoded.
The near trace alone has 119,372 rows.
These are inventory sizes, not runtime forecasts or accepted geometric work.
Source acquisition and decode are shared immutable preparation, not repeated per worker.

### Phase 3: Evidence and Review Consolidation

This phase runs only on spare capacity until the mathematical target is closed.

- [ ] **think-xmia:** lossless evidence packaging, duplicate elimination, readable
  summaries and migrated consumers; archive unique logs with a compact command/result
  index.
- [ ] **think-bhjn:** decouple rectangle diagnostic admission and map PR ownership into
  proof logic, evidence intake, rectangle tooling, and CI/efficiency changes.
- [ ] **think-zypq:** avoid re-deriving every witness solely to refresh edition stamps,
  preserving release and artifact-source checks.
  This remains optional supporting work.
- [ ] **think-69b5:** finish semantic regressions, before/after size and cost
  measurements, reviewer navigation and coherent integration.
  Remove obsolete live code only after the replacement passes; historical accepted
  implementations remain distinguishable.

Preserve PR #246 and its review comments.
Plan small follow-up commits by concern first.
Decide an actual PR split from the dependency map; do not force a linear stack onto
independent components or rewrite published history as a side effect of this plan.
If split, each PR must be independently reviewable/testable and retain source pinning,
status disclosures and links to the historical review.

## Morning Checkpoints and Efficiency Rules

These checkpoints implement the user’s deadline; they are not predicted proof runtimes.

| Local checkpoint, 2026-09-30 | Required decision |
| --- | --- |
| 00:00 | Shared controls accepted or exact blocker recorded; root/near representative profiles and missing-source inventory available. Select job sizes and estimate completion from measurements. |
| 03:00 | All required certificate families have a supported path or explicit blocker. Report accepted exact union and root/capture obligations. Reassign implementation capacity to the limiting lane. |
| 06:30 | Reserve remaining effort for unfinished proof jobs, composition, adversarial review and publication. Stop optional cleanup. |
| 08:00 | Publish complete independent confirmation if earned, otherwise a precise flaw/incompleteness report with the remaining conditions and retained evidence. |

Do not wait for checkpoint times when the next step is ready.
Record real starts and finishes in the session; reassess the remaining critical path at
each bounded work slice.
Do not change a failed run’s original budget after seeing its outcome.

Use a short pilot before a new large kernel.
The two completed field runs were 16.58 and 17.61 seconds outer wall under 30-second
ceilings; no aggregate estimate for all remaining families follows from those two
measurements. Large capture jobs require measured chunk ceilings and cancellation/resume
at completed obligation boundaries.
Keep input/decode, kernel CPU/wall, worker contention, queueing, review and
orchestration costs separate.
Exact arithmetic optimization precedes native rewrites; native code is justified by a
measured bottleneck and must preserve the same mathematical controls.

Every W5 task names the proof obligation it accelerates.
Use mounted writable external scratch with explicit TMPDIR, CARGO_TARGET_DIR and
UV_CACHE_DIR; source and unique receipts stay durable.
If scratch is unavailable, pause disk-heavy jobs and continue read-only mathematical
review rather than spill to the internal disk.

## Testing Strategy

| Change | Minimal necessary verification |
| --- | --- |
| Storage/reader only | Decoded-byte round trips, tamper/truncation/duplicate-key refusals, affected links and consumers; no unchanged geometry replay |
| Shared field kernel/runner | Focused boundary and refusal tests; one full bounded run each of mask0 and mask202; exact case-ID sets, not counts alone |
| Capture reader/canonical hashing | Reproduce all four published digest mismatches and ten-node/nine-edge structure; geometry/capture/global flags remain false |
| New capture semantics | Exact analytic transition controls, mutation refusals, complete owner/row inventories, reviewed full source-node runs and conditional-premise accounting |
| Global composition | Missing/duplicate case, wrong frame/source, undischarged conditional premise, partial dependency, missing boundary and unsupported claim all refuse; full acceptance requires every live dependency |

Field controls preserve 55 ownership points/136 rows and 50 points/439 rows, correct
three-site versus five-site median indices, strict core/ownership inequalities, closed
endpoints and degenerate segments, and every arrangement event and open slab.
Subset coverage may succeed; subset failure is incomplete, not a counterexample.

Retain focused semantic assertions alongside compact production-CLI goldens with
arguments, stdout/stderr, exit status and resulting artifacts.
Normalize only declared unstable timing fields; never normalize exact numbers, verdicts,
IDs or evidence pins.
A golden update cannot authorize changed mathematics.
Bind the new dependency closure and disclose shared geometry; agreement between two
wrappers around one kernel is not independent confirmation.

Unchanged local/D4/pose consumers retain their accepted receipts.
Changing their mathematical dependencies requires the corresponding focused controls and
bounded full component check, including 512-to-128 branches, 8,448 local inequalities,
88 strict feature gaps, and 136 pose rows/1,542 vertices where applicable.
Apply tbd engineering, code-review, general-testing and golden-testing guidelines; for
actual Rust changes also apply Rust arithmetic, lint, review and testing guidelines.

Run scoped lint/types/tests and affected record checks.
Fast controls belong in ordinary CI. Full certificate executions retain separate
measured receipts.
Batch repository CI alongside research; no general slow local suite is
a prerequisite for this plan.

## Upstream Validation and Performance Equivalence

The user additionally requires reproduction and audit of wand125’s verification process,
then independent verification at least as fast and effective.
**think-om8z** owns this work; **think-0jps** owns the reusable comparison tool.
The
[process map](../../verification-tooling.md#wand125-verification-process-and-independent-equivalence)
separates source acquisition, proposals, exact admission, continuous coverage, complete
angle census, packing deduction and receipt publication.

Pin the new upstream `3eb08e6c` separately from `0d33ab6`; reproduce the corrected
mass-budget controls and review the revised ceiling guidance.
Preserve historical findings rather than relabeling them as current defects.
Existing `verify.cpp` is unchanged; its reuse is upstream reproduction, not an
independent implementation.

Acceptance has two independent requirements: equivalent mathematical scope and adequate
measured performance.
First-party default threshold 1 is not equivalent to the source’s 10001/10000 coverage
target.
Record nominal and effective C++ thresholds explicitly, using the exact effective
binary64 cutoff for strict timing comparisons.
Require full 201-direction and center-domain decisions, exact candidate/parameter
binding and all packing-budget premises.
Incomplete runs cannot establish timing parity.

Start with one complete analytic control and a bounded representative feasibility probe.
Then freeze a representative certificate corpus before optimizing, run alternating
matched pairs on the same host/worker allocation, and compare complete-result wall and
aggregate CPU, separating compile/setup and kernel costs.
The parity target is no slower complete verification at the matched resource budget,
with no reduction in accepted coverage or refusal checks; noisy measurements remain
unresolved. Analytic-control parity alone does not establish parity on external proof
certificates.

Measure before choosing native code or a stronger geometric bound.
A source-distinct interval implementation may be more economical than optimizing
rational clipping, but requires its own rounding, boundary and full-domain proof review.
Avoid a literal C++ translation presented as independent mathematics.
This certificate family is separate from T-060: performance here does not discharge
remaining field/capture obligations.
Keep the morning proof lanes available and report any resource tradeoff explicitly.

## Rollout and Completion

New runner receipts coexist with frozen controls until exact equivalence and review
pass. Migrations are reversible through Git and preserve recoverable source evidence.
A compact reviewer index points to one current mathematical status, component code,
source identity, replay, expected verdict, limits and accepted exact IDs.
Report text additions, binary bytes, duplicate bytes and live implementation size
separately; a smaller diff alone does not demonstrate simpler verification.

The consolidation epic closes only when its components are simplified, evidence remains
reproducible, and targeted regression checks pass.
The mathematical goal closes only with a justified theorem verdict, independent of
cleanup completion. The morning report must say explicitly if full confirmation was not
achieved. The known public binding failure remains documented even if a corrected
first-party proof later succeeds.

## Open Risks and Decisions

- Remaining certificate feature shapes and capture kernel runtime are not yet measured.
  Inventory/profile these first; do not promise completion from file size or case
  counts.
- A sufficient certificate subset may be much smaller than all published packets; prove
  exact coverage before omitting redundant computations.
- Source geometry may contain a real flaw beyond stale bindings.
  Preserve failing input and distinguish a verifier limitation from an invalid proof
  step.
- Determine actual PR boundaries after the dependency inventory.
  Planning does not authorize force-push, deletion of unique evidence, or contacting
  upstream authors.

## References

- [PR #246 and size audit](https://github.com/jlevy/squares/pull/246#issuecomment-5904217093)
- [Proof review](../../reviews/review-2026-09-29-n11-optimality.md)
- [Census/capture contract](../../reviews/review-2026-09-29-n11-optimality-census-contract.md)
- [Tooling overview](../../verification-tooling.md)
- [Session 164](../../../../packing/campaign/agent-sessions/session-164-upstream-merge-and-certification.md)
- [Validation tiers](../../../../development.md#validation-tiers)

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
