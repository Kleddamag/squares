---
title: X-048 — Optimality Routes After n = 11
softschema:
  contract: packing.squares:Exploration/v1
  schema: ../schemas/exploration.schema.yaml
  envelope: exploration
  status: enforced
exploration:
  id: X-048
  title: Optimality Routes After n = 11
  date: '2026-10-01'
  author: Root coordinator with GPT-6 Astra max mathematical review and GPT-6 Sol research reviews
  campaign: packing.squares
  brief: >-
    Plan a fresh W3 block prioritizing n17 and other unresolved low cases after the
    imported n11 optimality proof and recent mixed-measure and parent-core results.
    Identify transferable mechanisms, endpoint obligations, structural obstacles,
    candidate falsifiers and the cheapest experiments to select next. No new bound,
    experiment verdict or proof certification is claimed.
  sources:
    - packing/frontier/results.yaml
    - packing/frontier/n-011.md
    - packing/frontier/n-012.md
    - packing/frontier/n-017.md
    - packing/frontier/n-018.md
    - packing/frontier/n-019.md
    - packing/frontier/n-020.md
    - packing/frontier/n-021.md
    - packing/frontier/n-026.md
    - packing/frontier/n-029.md
    - packing/resources/web/n11-optimality-2026-09-29/source/PROOF.md
    - docs/project/reviews/review-2026-09-30-n11-expository-simplification.md
    - docs/project/specs/active/plan-2026-09-25-after-r052-planning.md
    - packing/campaign/explorations/X-043-new-lower-bound-proof-directions.md
    - packing/campaign/explorations/X-044-low-n-certificate-transfer.md
    - packing/campaign/explorations/X-047-low-n-angles-after-the-parent-core-advance.md
    - packing/campaign/agendas/agenda-042-overnight-n11-settlement-and-low-n-angles.md
    - docs/project/reviews/review-2026-09-27-evand-s32-s12.md
    - packing/resources/web/evand-square-packing-2026-09-28/square-packing/s12/README.md
    - docs/project/reviews/review-2026-09-27-plan-4640020-lemma-check.md
    - docs/project/reviews/review-2026-09-28-n17-guzhou-r067-r068.md
    - docs/project/reviews/review-2026-09-28-evand-s21-s45-mixed-covers.md
    - docs/project/reviews/review-2026-10-01-evand-source-coverage.md
    - docs/project/reviews/review-2026-10-01-evand-mathematical-transfer.md
  proposes: [H-253, H-254, H-255, H-256, H-257, H-258, H-259]
---
# X-048: Optimality Routes After n = 11

The n = 11 proof supplies a useful architecture for another optimality proof: cover
every packing, exclude most possibilities, capture the survivors in a region where a
short exact argument forces the known side length.
For n = 17, the most promising adaptation couples global occupancy constraints with an
exact theorem about a family of Bidwell packings.
A faster version of the existing lower-bound certificate alone does not supply either
half of that argument.

This is a W3 exploration, with untested proposals below.
The
[next-session plan](../../../docs/project/specs/active/plan-2026-10-01-post-optimality-w3-session.md)
maps the proposed entry and checkpoints; W10 selects experiments after the opening W3
work. The source baseline is merged main at `f9a3409f0f03298fbeeb0a03788cd016087626b9`,
including the September 30 epistemics revision.
T-060 is machine-checked at **V3/C3** under that rubric; its historical V4/C5 label does
not imply that human proof review has occurred.
No rating or frontier field is changed here.

## What the New Results Change

| Result | Established in the retained record | Research consequence |
| --- | --- | --- |
| [T-060: n = 11](../../frontier/n-011.md) | Exact optimality at Trump’s algebraic side, using global exclusion, capture and a local endpoint theorem | A complete finite-to-continuous proof architecture is available for study and calibration |
| [T-043: n = 17](../../frontier/n-017.md) | R068 gives the strict lower bound 116511/25000 = 4.66044 | Start from the current certificate and identify structural losses; old R052 margins are historical |
| [T-052: n = 21](../../frontier/n-021.md) | Exact optimality at 5, using a mixed point-and-line measure | Retire n21 as an open target; inspect its endpoint accounting for integer-ceiling cases |
| T-061: Wang–Li n11 certificate | A strict rational improvement above 31/8, now superseded by T-060 | Certificate slack and rescaling are useful diagnostics, but do not replace an endpoint theorem |
| [Native arithmetic measurements](../../../docs/project/research/research-2026-09-30-exact-arithmetic-verifier-performance.md) | A bounded Rust verifier comparison preserves exact outputs and reduces measured CPU | Reuse measurement infrastructure when a selected proof lane is expensive; do not infer global replay speed from kernel timing |

The n17 gap to the **reported** Bidwell value is approximately 0.0150901. That is a
research target gap, not the repository’s fully verified bracket: the
[case record](../../frontier/n-017.md) still verifies only the upper bound 5. An exact
or interval-certified witness near Bidwell’s value is therefore an early deliverable,
even if a global exclusion route looks promising immediately.

## What Transfers from the Eleven-Square Proof

The [original proof](../../resources/web/n11-optimality-2026-09-29/source/PROOF.md) and
[simplification review](../../../docs/project/reviews/review-2026-09-30-n11-expository-simplification.md)
separate the following obligations.

| Component | General mechanism | What must be established again at n17 |
| --- | --- | --- |
| Closed centre cover | Every square has a centre in a covered region; cells with diameter below 1 hold at most one centre | A complete cover at the chosen cap, capacity proofs and closed boundary treatment |
| Occupancy masks | Reduce continuous placements to finite occupied-cell possibilities | Exhaustive occupancy enumeration; no observed contact graph or symmetry assumption may omit a packing |
| Ownership and common cores | Retain regions forced inside the square over every admitted pose | Sound cores for every angle interval and containment domain, preserving all possible owners |
| Charge and compatibility | Exclude occupancy patterns whose mandatory charges exceed available capacity | Per-atom validity, overlap accounting and global capacity; R068 features need their actual verifier semantics |
| Container symmetry | Transport configurations through exact square symmetries | Complete orbit coverage, including fixed points and seams; cells need not be permuted by the chosen symmetry |
| Capture | All survivors enter a specified terminal region | A complete certificate reaching a proved neighborhood, with no undecided leaves |
| Endpoint theorem | The terminal region cannot contain a smaller packing | A side-minimum theorem for the candidate n17 endpoint family, which may have feasible sliding motions |

For T-060, 16 closed cells give 4,368 eleven-cell masks, 2,184 half-turn classes and
2,180 exclusions; the four surviving cases reduce to a captured case through a separate
symmetry argument. Those sizes are consequences of the eleven-square geometry, not a
generic complexity bound for this method.

A crude n17 sizing calculation illustrates the obstacle.
In a container of side S, all unit-square centres lie in the square of side S − 1,
because every rotated unit square extends at least 1/2 in each coordinate direction.
At the reported S ≈ 4.67553, a 5-by-5 grid has cell diameter about 1.0396, too large for
the simple capacity-one guarantee.
A 6-by-6 grid has diameter about 0.8663, but already admits
`binomial(36,17) = 8,597,496,600` raw masks.
This rules out treating unpruned mask enumeration as a cheap first experiment.
It does not rule out better covers, occupancy constraints or implicit enumeration.

## Priority n17 Routes

### R1. Verify the Candidate and Describe Its Endpoint Family

The [Bidwell record](../../frontier/n-017.md) gives a degree-18 polynomial for the
reported side and two nonzero tilt angles.
It also reports feasible sliding squares.
A side polynomial alone is not a certified packing: coordinates, root selections,
containment and all pair separations must be checked.

First reconstruct the retained witness with a verified feasible upper enclosure.
An enclosure at a slightly larger side establishes an upper bound; equality at the
proposed algebraic endpoint requires a feasible witness at that endpoint itself.
Then separate a constrained backbone from the sliding coordinates and seek an exact
parameterization, or a certified tube containing the family.
For each contact chart, derive a side lower bound uniform over that tube.
The chart family must cover nearby changes of separating features; fixing a sliding
coordinate requires a proved side-preserving normalization.
An exact nonnegative combination of contact inequalities, an interval sign argument, or
a small reduced algebraic elimination may supply the terminal theorem.

**First discriminator:** a coordinate and contact audit identifying which variables
determine the side and which remain free, with a known valid packing as control.
Failure to certify the imported coordinates blocks promotion of that upper bound; it
does not refute Bidwell’s construction.
A feasible motion decreasing side would refute the proposed terminal theorem.
A same-side motion is expected and must be retained.

**Payoff:** a reusable endpoint target for every global route below.
The existing n11 local theorem is a design example, not an n17 checker.

### R2. Build a Small Occupancy Problem Before a Large Search

Try closed Voronoi covers adapted to the candidate geometry, mixed cell capacities, and
intersections of several covers.
Derive exclusions from centre distance, containment and cell capacity before branching
on square angles. Use exact graph or integer constraints to count surviving occupancy
patterns without listing all raw masks.

**First discriminator:** one rational cap above the candidate, a proved complete cover,
exact capacity bounds, and a census of survivors after each independently justified cut.
Report raw count, surviving count, memory and sample exclusion cost separately.
Keep known packings feasible; a cut that rejects one is invalid.
If the residual count remains too large under the declared resource cap, retain the
cover and the obstruction, then switch to a stronger constraint family.
An arbitrary threshold on mask count is not a mathematical failure criterion.

**Payoff:** a costed global capture route instead of an unrestricted 51-variable search.

### R3. Turn R068 Saturation into Constraints on Joint Placements

R068’s weighted-threshold rules and winning subsets already express more than a plain
point measure. Study which angle intervals and placements nearly attain the minimum
charge, and whether seventeen such near-minimizers can coexist.
The useful new statement would be a proved incompatibility between simultaneous
low-charge placements, not another unsupported extrapolation of row slack.
Flat row minima and a small surplus do not prove that reweighting is exhausted: that
needs an exact dual for the current dictionary and domain.

**First discriminator:** audit a fixed sample of the actual R068 binding rows, extract
their minimizing placements and identify a candidate pair or small-tuple obstruction.
Use R068 as a positive control; evaluate the proposed new cut at a declared stronger
side, such as 4.67, with rebuilt core and parent-centre envelopes.
Sampled minimizers only suggest cuts.
A global charge argument needs a complete cover of all low-charge poses, including
event-cell seams. The [X-043 interface](X-043-new-lower-bound-proof-directions.md) makes
the obligation precise: if every pose in class Cj has charge at least ℓj, and every
packing’s class-count vector belongs to a necessary relaxation R, prove
`min(z in R) sum(ℓj zj) > M`, where M is the total available charge.
Prove the selected obstruction over the full continuous domains represented by those
rows before adding it as a cut.
Retain feasible counterexamples and exact boundary contacts.
If all tested low-charge types coexist, that rejects the selected cut, not every
compatibility approach.

**Payoff:** couple a strong existing certificate to the occupancy problem and reduce the
number of expensive geometric cases.
The native reader’s missing R068 features are a separate implementation obligation;
successful replay of a simpler predecessor does not establish feature coverage.

### R4. Establish the Limit of the Present Certificate Architecture

Reuse the existing capacity-one ceiling question H-248 and BC-387 in
[agenda-042](../agendas/agenda-042-overnight-n11-settlement-and-low-n-angles.md).
The proposed route seeks weighted families of overlapping squares whose total dual
weight prevents every certificate in a specified atom class from proving the target.

The class must be stated exactly.
The general proposed witness assigns nonnegative weights of total at least 17 to
contained unit squares, with weight at most one on every clique of their
interior-overlap graph.
A triangle-free family of 34 squares, each of weight one half, is a special case.
H-248 targets 4.675 first and then 4.67; it must not be restarted below the lower bound
already certified by R068. Pointwise overlap depth alone does not establish the clique
constraint. The
[lemma review](../../../docs/project/reviews/review-2026-09-27-plan-4640020-lemma-check.md)
explains the passage to strict cores and capacity-one trigger sets.
Larger-capacity constraints and conditional geometry need separate analysis.

**First discriminator:** review the dual lemma against R068’s actual rule types before
searching for the proposed 34-square family.
An accepted dual witness limits a method, not the packing optimum.
A failed search is inconclusive.
Use the existing bead and hypothesis rather than register a duplicate.

**Payoff:** decide whether to invest in new atom types, compatibility, or capture.

### R5. Prove a Backbone Without Assuming the Catalogue Picture

Near the candidate side, area pressure and boundary occupancy may force a finite
collection of wall chains or connected blocks.
Enumerate those possibilities with disjunctive separation constraints and derive side
bounds for each. The witness suggests chains worth testing, but the global theorem must
account for chains absent from it, rotated interiors, degenerate contacts and
disconnected blocks.

**First discriminator:** select one proposed necessary wall-chain or occupancy lemma and
run an adversarial feasibility search for its negation.
Specify whether the lemma concerns all feasible packings, every minimizing packing, or
the existence of a normalized minimizing representative.
An arbitrary feasible counterexample can refute the first statement but need not refute
either of the others.
Certify any resulting packing before calling it a counterexample.
If the lemma survives, retain it as unproved until a complete exclusion certificate or
analytic derivation is available.
Do not make the witness’s three angle values a global restriction.

**Payoff:** reduce the dimension of capture, possibly bypassing a huge mask census.

### R6. A Hierarchy of Local Certificates with Global Coverage

Combine a cheap counting bound at the root with stronger pairwise or neighborhood
certificates only on unresolved cells.
Use exact Farkas witnesses for linear relaxations and interval or algebraic checks for
the nonlinear remainder.
Branch on the variable that removes the most unresolved geometry in a controlled pilot,
then freeze that choice for the measured experiment.

**First discriminator:** compare the old and strengthened relaxation on the same small
residual set, including a feasible terminal-family case.
Count eliminated cells and unresolved cells; separate producer time from independent
checker time and measure certificate size.
Any unproved strengthening invalidates the exclusion.

**Payoff:** spend exact arithmetic on a small residue while keeping the certificate
reader simple enough to audit independently.

### R7. Try a Direct Endpoint Measure

Daniel’s
[endpoint method for n21](../../../docs/project/reviews/review-2026-09-28-evand-s21-s45-mixed-covers.md)
suggests a second route to equality, separate from capture.
At a prospective exact endpoint T17, seek a nonnegative measure of total mass below 17
that assigns mass at least one to every closed unit square contained in the container.
Boundary contact can share mass in an actual endpoint packing.
For a hypothetical packing in a strictly smaller container, dilate it into the endpoint
container and take concentric unit-square cores.
These cores are disjoint closed sets, so their charges would sum to at least 17,
contradicting the total mass.
Precisely, let K = [0,T17]² and μ be the proposed finite nonnegative measure.
Dilation by T17/S makes the parent sides greater than one, so each closed unit core lies
strictly inside its parent, giving `17 ≤ sum(μ(Qi)) = μ(union(Qi)) ≤ μ(K) < 17`. Exact
feasibility at T17 separately supplies the upper bound needed for equality.

**First discriminator:** test a contact-supported measure against the endpoint packing
and its sliding family, then seek an exact finite dual obstruction or a candidate cover.
Algebraic sites, zero-margin contact seams and full continuous coverage remain
verification obligations.
This method is not a strict-parent-core certificate at T17, which would wrongly exclude
the endpoint packing itself.
An obstruction to the chosen site dictionary is not a universal obstruction.

### R8. Change the Certificate Features, Then Measure Their Value

Adaptive sites, richer threshold features and capacity-two resources could improve the
lower bound enough to simplify capture.
Compare them on identical frozen rows, preserving a rational primal/dual pair.
Then verify any candidate against the full parent domain at the proposed new side.
Changing side also changes legal parent-centre envelopes and core containment.

**First discriminator:** one proposed feature family with an exact improvement over the
fixed finite baseline, followed by a continuous counterexample check.
A finite LP gain is a search result until the universal constraints are verified.
Keep this route only if the gain changes the capture problem or yields a material bound;
do not spend the session polishing an immaterial decimal increment.

### R9. Use Settled Small Cases as Subconfiguration Cuts

T-060 gives a direct capacity fact: a square region of side strictly below T11 cannot
contain eleven complete unit squares.
Analogous facts follow from other settled small cases.
These could eliminate branches whose geometry forces too many whole squares into a
subcontainer, or yield capacity bounds for a cover of subregions.

**First discriminator:** derive one exact containment-and-assignment lemma from an n17
occupancy case and apply the known small-case bound to it.
Containment of centres alone is insufficient; whole squares and the strict side
inequality must be proved.
Overlapping subcontainers also require sound assignment or counting rules.
This is a structural use of the n11 theorem, not a numerical implication from s(11) to
s(17).

## Other Low Cases

Values below are the verified bounds in the main snapshot, except where explicitly
marked as reported. Ranking is a research judgment, not a probability of success.

| Priority | Case and verified bracket | Most useful route | First decision |
| --- | --- | --- | --- |
| Primary | [17](../../frontier/n-017.md): 4.66044 < s ≤ 5; reported upper 4.675530… | Family endpoint plus global occupancy/compatibility | Can the candidate endpoint be certified, and can the global cases be compressed? |
| Parallel secondary | [12](../../frontier/n-012.md): 3.968615 ≤ s ≤ 4 | Integer-endpoint occupancy and conditional charge/capacity | Audit the reported additive dual obstruction, then test a route outside its scope |
| First fallback | [20](../../frontier/n-020.md): 4.85 ≤ s ≤ 5 | Transfer the n21 mixed-measure mechanism with stronger occupancy or boundary constraints | Where does losing the twenty-first square break the count? |
| Structural fallback | [18](../../frontier/n-018.md): 4.679 ≤ s ≤ (7 + √7)/2 | Exact backbone/terminal-family analysis paired with stronger lower constraints | Is the construction’s side controlled by a small certifiable subsystem? |
| Structural fallback | [19](../../frontier/n-019.md): 4.8 ≤ s ≤ 3 + 4√2/3 | Same decomposition, with its own contact and boundary classification | Does a local subsystem yield a uniform side obstruction? |
| Reserve | [26](../../frontier/n-026.md): 5.508 ≤ s ≤ (7 + 3√2)/2; [29](../../frontier/n-029.md): 5.71 ≤ s ≤ 5.933834, rounded outward | Defect blocks near grid plateaus and improved exact construction analysis | Is there a substantially smaller proof problem than at n17? |

The reported lower bounds 4.695, 4.815 and 4.895 for n18–20 are intake leads; they are
not substituted for verified fields here.
For n12, the
[retained evand source](../../resources/web/evand-square-packing-2026-09-28/square-packing/s12/README.md)
reports exact fractional obstructions at 3.99 and 4, discussed in the
[mathematical review](../../../docs/project/reviews/review-2026-09-27-evand-s32-s12.md).
The
[October source audit](../../../docs/project/reviews/review-2026-10-01-evand-source-coverage.md)
recovers public support files for the side-4 and side-5 obstructions at revision
`08e8a5faa54c0a7b0bb1cb0134c77d3565ce40c5`. They have mathematical review but no fresh
local replay. The newer side-3.99 mass is $48112643084/3999999987$, approximately
12.02816; its support file remains absent from the public tree.
Check the recovered evidence before declaring the entire additive route closed.
An accepted closed-depth dual would obstruct every finite nonnegative spatial measure,
including segments and area, rather than just a fixed point dictionary.
Conditional occupancy is therefore a better initial bet than blindly transferring n21’s
endpoint measure. At side 5, the source’s exact fractional mass is
$10323890641/499999999$, approximately 20.64778, which would obstruct a plain additive
proof of n20 if its exact premises are verified.
T-052’s existing cover has exact mass 20.89474919732: a conditional adaptation must
obtain more than 0.89474919732 of valid budget saving to get strictly below 20, or prove
a correspondingly stronger minimum charge.
An exact dual obstruction could force a change of method rather than merely a better
choice of sites.
Closed cases n13–16 and n21–25 are useful positive controls for capacity
and endpoint arguments.
Additional upper-bound constructions and catalogue changes merit intake under W1/W2, but
do not displace the mathematical priority without a concrete new route.

At integer endpoints, distinguish certificates at S < 4 or S < 5 from equality.
A theorem may exclude every smaller side while allowing multiple optimal families at the
endpoint.
Do not infer n20 optimality from s(21) = 5: deleting a square provides an upper
bound, while monotonicity points the wrong way for the required lower bound.

## New Leads from the October Evand Review

The
[source audit](../../../docs/project/reviews/review-2026-10-01-evand-source-coverage.md)
and
[Astra mathematical review](../../../docs/project/reviews/review-2026-10-01-evand-mathematical-transfer.md)
separate newly reported theorems from research mechanisms.
The source reports $s(60) = s(61) = 8$ and $s(k^2 - 3) = k$ for every integer $k \ge 6$.
The latter reduces all sizes to a finite covering premise in a 7 × 7 box; the Lean
reduction assumes that premise, and the source currently supplies only one exact
implementation for checking it.
These reports neither settle n17 nor replace the obligations in R1–R9.

| Lead | Why investigate it | First discriminator and stopping condition |
| --- | --- | --- |
| Exact limiting configurations for R1/R7 | A continuum cover can fail arbitrarily close to a tight contact even when sampled angles pass. The source uses exact limiting constraints before searching for endpoint weights. | Derive necessary constraints on the proposed n17 sliding/contact family. Test exact feasibility before a global sweep; an infeasible subsystem rejects that certificate template, not optimality. |
| Continuum clique resources for n12 | The source already explores cliques defined by a point and a region, beyond ordinary spatial measures. Its finite box-clique gains nearly disappear at grazing contacts. | Start with an exact finite primal/dual comparison, then seek a uniform bound over the full continuum. Use the mathematical review’s corrected threshold argument if needed; a sampled gain without coverage of grazing contacts is inconclusive. |
| Higher-order local obstructions | The n12 source reports exact witnesses for proper subsets of a proposed obstruction; its claim that the whole leaf has no positive separation remains numerical. First-order certificates can miss a zero-margin plateau. | Identify the first nonzero exact order on a specific candidate family; retain a feasible adversary or unresolved term instead of inferring a global theorem from local derivatives. |
| A periodic family with deficit four | The reported deficit-three proof separates fixed corners, periodic walls and an area interior. A wider boundary pattern might have enough mass saving for $k^2 - 4$. | Price the source’s width-three LP first and require the exact saving condition $D > 1$ before any global checker run. The source estimates 5–10 CPU-hours for that LP and 50–80 for a subsequent check, so this is a reserve campaign, not an automatic overnight job. |

W10 may select a small discriminator from these leads without waiting for every large
external replay. It must state which unverified source premise it assumes.
The finite family premise, s60 replay, and recovered dual checks have separate beads
`think-4k80`, `think-e7xa`, and `think-q5tt`. The
[session plan](../../../docs/project/specs/active/plan-2026-10-01-post-optimality-w3-session.md)
keeps n17 first and limits secondary work to what changes the next decision.

## Approaches to Retire or Restrict

- Retire n11 and n21 as open optimality targets in the new session.
  Preserve their earlier experiments as historical evidence and use their accepted
  artifacts as controls.
- Do not rerun frozen-support weight optimization merely because Rust is faster.
  Require a new structural constraint or measured remaining headroom first.
- Do not copy the n11 exact field, terminal neighborhood, charge partition or D4 case
  numbering into n17. Reuse interfaces and proof obligations, not those constants.
- A local optimum, a rigid contact graph, or a large sample of failed searches does not
  cover all packings. Rattlers also prevent an isolated-point endpoint argument.
- An empty relaxed cell can exclude a case; a nonempty relaxed cell may be spurious.
  Preserve unresolved cases until a stronger argument decides them.
- A partial native replay or a matched bounded benchmark does not independently confirm
  the entire external certificate.

## Selection for the Next Session

Open with three parallel deliverables: n17 endpoint/family analysis, n17 global
cover-and-charge analysis, and low-n endpoint transfer.
The coordinator reconciles them into one n17 experiment and at most one secondary
experiment, each with a frozen falsifier and independent validity checks.
Keep R4 as the existing architecture-ceiling task; use it when it discriminates between
the selected alternatives.

Record source revisions, assumptions, expected information, unresolved proof obligations
and the exact next artifact for every selected route.
The
[session plan](../../../docs/project/specs/active/plan-2026-10-01-post-optimality-w3-session.md)
sets execution dependencies, review boundaries and efficiency triggers.
H-253 through H-257 now discharge rational feasibility, chart fidelity, root existence,
endpoint feasibility and the complete active-feature inventory.
The following execution checkpoint supersedes the initial readiness assessment while
preserving its selection rationale.

## October 1 Execution Checkpoint

[Session 165](../agent-sessions/session-165-post-optimality-overnight.md) has five
accepted rounds, with immutable inputs and independent review:

| Obligation | Result | Exact Scope |
| --- | --- | --- |
| [H-253](../hypotheses/H-253-n17-retained-rational-upper.md) | Accepted | Replay of the existing rational upper witness through two local exact implementations and the source checker |
| [H-254](../hypotheses/H-254-n17-contact-chart-fidelity.md) | Accepted | All 458 chart-fidelity comparisons at the relaxed rational witness |
| [H-255](../hypotheses/H-255-n17-exact-polynomial-root.md) | Accepted | Exact existence and uniqueness in the fixed root box, with an independently implemented checker |
| [H-256](../hypotheses/H-256-n17-exact-endpoint-feasibility.md) | Accepted | Exact physical endpoint at fixed centroid sliders; all 68 walls and 136 pairs certified, all 187 interval bounds independently recalculated |
| [H-257](../hypotheses/H-257-n17-endpoint-contact-features.md) | Accepted | Complete168owner-axis/60wall-corner/9offset inventory; all175interval records independently recalculated |

The
[mathematical review](../../../docs/project/reviews/review-2026-10-01-post-optimality-w3-opening.md)
and
[projection-branch theorem](../../../docs/project/reviews/review-2026-10-01-n17-projection-branches.md)
therefore establish an attained minimum within a declared parameter and
separating-branch family.
The latter removes several orientation assumptions and proves angle rigidity at
equality, while keeping the branch premises explicit.
A rotational freedom at square 6 shows why an isolated-coordinate theorem is
inappropriate.

[H-258](../hypotheses/H-258-n17-common-core-stress.md) selected a fixed common-core
stress for both first-order branches.
Its mathematical recipe passed static review, but three bounded symbolic preparation
attempts did not finish.
The instrument is stopped, and no target stress was evaluated.
Neither stationarity nor its negation has been established.
Exact residual completion, adversarial controls and bounded interval arithmetic remain
prerequisites for a separately admitted future run.
Even a complete stationarity certificate would require further higher-order and global
arguments. H-027’s class-angle derivative threshold is not silently replaced by this
weaker question.

The separately registered
[n12 weighted-cycle review](../../../docs/project/reviews/review-2026-10-01-n12-weighted-cycle-capture.md)
proves a finite-row inequality for arbitrary nonnegative edge weights.
At side 4, canonical componentwise wall repair loses no certificate with a nonpositive
margin bound on a fixed pair support.
This removes wall variables from that conditional certificate problem.
Exact hand controls and independent algebra review passed; no source solver run or
geometric target was replayed.
Global coverage of valid row supports remains the missing premise, so this is not a new
n12 lower bound.

The two main scientific gaps remain local capture of unrestricted orientations and
separating branches, and global exclusion outside a captured neighbourhood.
The [n17 case](../../frontier/n-017.md) now admits the accepted endpoint’s rational
outward ceiling under `think-vdmf`, replacing the grid ceiling5 while leaving the case
open. The rational H253 witness remains separate fallback evidence.
Low-n and global-cover routes retain their recorded readiness limits rather than
launching a broad search during endpoint work.

## Planning Review

Astra at max reasoning reviewed the transfer mechanisms and draft mathematics.
Sol separately audited current low-n bounds and reported obstruction sources, and
another Sol review checked workflow, document structure and execution boundaries.
The integrated corrections distinguish a flexible endpoint from isolation, exact
feasibility from an outward upper enclosure, whole-clique constraints from pointwise
depth, and sampled weak poses from complete coverage.
Upper bounds in the comparison table are exact or rounded outward.
These are reviews of proposed research, not fresh proof replays or endorsements of the
untested hypotheses.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
