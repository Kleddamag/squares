# Verification Tooling and Its Boundaries

This repository verifies several different mathematical objects: feasible packings,
weighted point covers, threshold charges, rectangle densities, and finite geometric
subproblems. A checker establishes only the theorem and input format it implements.
The existence of a checker is separate from a completed run on a particular claim.

**Current priority: T-060, the claimed global n = 11 optimum.**
[11SquaresOptimal](https://github.com/Queuingtheorydotcom/11SquaresOptimal) claims the
exact Trump endpoint through a global cell cover, 2,180 exclusions, a symmetry bridge
and complete capture into a local isolation region.
Its 23-stage source driver is a new trust boundary.
Neither the existing native T-037 lower-bound checker nor the rectangle-density checker
validates this global argument.
The [intake packet](../../packing/resources/web/n11-optimality-2026-09-29/README.md)
records the source pin and publication limits; **think-3i74** owns independent
mathematical audit and efficient reproduction.
Source replay, independent rule checks and complete global composition must be reported
separately.
General slow repository tests do not substitute for any of these obligations.
The [proof review and stage map](reviews/review-2026-09-29-n11-optimality.md) records
the reviewed implications, outstanding replay and next independent controls.

The [epistemic scale](../../epistemics.md#confirmation) distinguishes a complete replay
(`C3`) from confirmation by a distinct complete method (`C4`) and a mapped review
(`C5`). A source checker run here is a replay.
An independent parser, an exact premise audit, or a comparison of output logs can
strengthen that replay without becoming a second coverage decision.
Each claim’s retained receipts determine which work is complete.

## Verification Families

| Object | Main tools | What they establish and where they stop |
| --- | --- | --- |
| Feasible packing geometry | [`sqpack.verify`](../../packing/src/sqpack/verify.py), [`sqpack.assurance`](../../packing/src/sqpack/assurance.py), [independent rational witness checker](../../packing/devtools/check_rational_witness_independent.py) | Containment, unit-square geometry and pairwise interior disjointness. Exact rational or accepted algebraic-field data can prove an upper bound. The independent checker accepts rational corner witnesses only. Decimal checks remain numerical; feasibility alone does not prove optimality. |
| Interval enclosure of a packing | [`promote.interval_verify`](../../packing/src/sqpack/promote/interval_verify.py) | Outward-rounded enclosures can certify strict separation and containment. Unresolved contact is `undecided`; this route cannot certify an equality from a positive-width enclosure. |
| Weighted point certificate | [`decide_certificate`](../../packing/devtools/decide_certificate.py) | Exact event-cell sweep and directed-rounding interval branch and bound decide every required centre and direction. Full retention requires both methods to accept and agree on the minimum, with the input bytes unchanged. The shared certificate representation and theorem remain common premises. |
| Point and threshold certificate | [`decide_threshold_certificate`](../../packing/devtools/decide_threshold_certificate.py) | Exact sweep and interval branch and bound decide point charges plus threshold atoms: charge when at least `k` of a named set is covered, with its justified budget. The exact route also checks dense-grid and slab agreement. This is a separate schema from rectangle density. |
| Relational certificate | [`decide_relational_certificate`](../../packing/devtools/decide_relational_certificate.py) | Two exact routes decide supported point, threshold and floor atoms. Its two-route admission verdict does not claim the floating-point interval confirmation still required for a T-id in this class. Ordinary supported threshold records are delegated to the threshold gate. |
| Adaptive parent-core certificate | [`parent_core`](../../packing/src/sqpack/fractional/parent_core.py), [`parent_core_interval`](../../packing/src/sqpack/fractional/parent_core_interval.py) | Exact checks prove the angle-row cover, strict core containment, symmetry and budget; interval subdivision decides every centre in each row’s parent domain. Source-specific readers support Kleddamag n11, Evan Daniel’s angle-net format and Guzhou R052. A pilot, input refusal or sizing run cannot establish complete coverage. |
| Tokoharu rectangle density | [`audit_tokoharu_density`](../../packing/devtools/audit_tokoharu_density.py), [`audit_wand125_rectangles`](../../packing/devtools/audit_wand125_rectangles.py), [native exact prototype](../../packing/devtools/verify_rectangle_density.py) | Existing retained bound replays use the unchanged upstream C++ checker with independent exact prerequisites and input binding. The native prototype implements exact coverage without upstream code and passes a complete analytic control; a complete native run on a retained external certificate remains outstanding. |
| Mixed point and segment cover with zero margin | [`audit_evand_mixed_covers`](../../packing/devtools/audit_evand_mixed_covers.py) | Independent exact measure, symmetry and root-census audits surround source `zmx2` and `zm_mixed.py` runs. These audits do not re-prove individual boxes. The native parent-core engine needs strict interior cores and has no segment atom, so it cannot replace these source checkers. |
| wand125 point-only and modified rectangle bundles | [`audit_wand125_point_and_mixed`](../../packing/devtools/audit_wand125_point_and_mixed.py) | Independently checks exact arithmetic premises and input binding for the n21, n45 and n50 packets, then audits or reruns their source programs. Its `exact` command decides no coverage. The n50 research checker differs from the standard Tokoharu checker, including acceptance at coverage `>= 1`. |
| Finite family depth and closed polygon coverage | [exact face](../../packing/devtools/density_face_verifier.py), [independent slab](../../packing/devtools/density_slab_verifier.py), [graph certificate](../../packing/devtools/check_geometric_graph_certificate.py), [closed polygon cover](../../packing/devtools/check_closed_polygon_cover.py) readers | Scoped geometric lemmas about supplied square families or polygon inventories. The caller must bind the source geometry and prove the reduction to a packing claim. These tools do not supply global rectangle-density coverage over all square poses. |

The [native n11 review](reviews/review-2026-09-22-native-n11-parent-core.md) records a
complete parent-core run and its reconciliation.
Other adapters have different limits: the
[Guzhou R052 native reader](../../packing/devtools/verify_guzhou_r052_native.py) records
a refusal at the reviewed allocation ceilings; its optional sizing mode is explicitly
outside a coverage verdict.
The
[Evan Daniel angle-net reader](../../packing/devtools/verify_evand_angle_net_native.py)
requires every row certified before reporting `PASS_COMPLETE`. Successful parsing or the
existence of either adapter is insufficient to upgrade a source claim.

## Rectangle Density: Native Coverage and Remaining Replay Work

A rectangle certificate spreads nonnegative mass uniformly over each rectangle.
For a checking square, the captured mass is the sum of rectangle-intersection areas
multiplied by their densities.
This varies continuously with the square’s centre; point-certificate event cells, whose
captured atom sets are constant, do not decide it.

The counting proof requires total mass strictly below `n` and at least one unit of
captured mass for every required checking square.
A rational direction net and a strict shrink inequality place a checked inner square
inside every unit square, connecting the finite angle list to the continuum of
orientations. The retained standard Tokoharu format uses 201 directions and the stronger
coverage target `10001/10000`. All admissible centres at every direction must be
covered; scanning a finite set of centres only tests candidate placements.

The first-party exact preflight recomputes mass from the candidate decimals as rational
numbers, expands the eight symmetry images with multiplicity, and checks nonnegativity,
target side, the angle-net endpoint and containment and smoothing margins.
It also checks that every supplied binary64 interval encloses its exact datum and that
the axis-event list is complete.
The wand125 importer regenerates the interval input and checks its identity against the
published input. Source binding fixes which checker was reviewed and replayed.

The existing retained bound replays use Tokoharu’s unchanged `verify.cpp` for global
rotated coverage. Their independent rational clipping and slice probes test its
arithmetic at selected placements; they do not exhaust the centre domains.
That boundary is recorded in the
[Tokoharu mathematical review](reviews/review-2026-09-22-tokoharu-density-mathematics.md)
and
[wand125 rectangle replay packet](../../packing/resources/web/wand125-rectangle-certificates-2026-09-27/README.md#receipts).

The [native exact prototype](../../packing/src/sqpack/rectangle_density.py) implements a
different independent coverage procedure that can produce complete proofs.
Equality at the acceptance threshold may remain unresolved under subdivision.
At axis alignment it enumerates all rectangle events and evaluates their grid exactly.
At each oblique net direction it subdivides the admissible centre domain into rational
boxes. A polygon contained in every checking square over one box supplies a lower bound
on captured mass, computed by exact clipping against the density rectangles.
The optional `corner-min` mode sums each rectangle’s least exact overlap at the four box
corners. The [corner-bound review](reviews/review-2026-09-29-rectangle-corner-bound.md)
proves this bound and explains why taking the minimum after summing the rectangles would
be invalid. The default remains `common-core`. The engine accepts an angle only after
every box has a sufficient lower bound.

The [CLI](../../packing/devtools/verify_rectangle_density.py) rechecks exact admission
premises, rejects inconsistent net metadata, and binds its receipt to the candidate
bytes and checker source.
Its default threshold is `1`; the source’s `rhs` is recorded separately, and
`--threshold 10001/10000` requests the standard upstream target.
Only all 201 required angles can produce `VERIFIED`. A successful subset is `PARTIAL`;
an exhausted node, depth or cooperative search-time budget is `INCONCLUSIVE`; an exact
core placement below the requested threshold is `COUNTEREXAMPLE` to that certificate.
None of those other statuses establishes the packing bound.

`--retain-pending-boxes` retains exact unresolved boxes for oblique directions, with a
global 10,000-node request ceiling.
It refuses oversized requests rather than silently truncating diagnostics.
The [comparison command](../../packing/devtools/compare_rectangle_density_bounds.py)
replays and matches a retained frontier before evaluating both bounds on identical
boxes. Its output is always `DIAGNOSTIC_ONLY`; it supplies no trusted-resume or
proof-aggregation mechanism.

The [native controls](../../packing/tests/test_rectangle_density.py) include a complete
analytic positive density, an underweight cover, malformed inputs, direct-construction
admission bypasses, the retained over-budget negative control, and refusal to promote a
capped retained-certificate probe.
The executed receipts distinguish their outcomes:

| Input | Native result | Scope |
| --- | --- | --- |
| [Analytic density](../../packing/resources/web/wand125-tools-2026-09-29/native-analytic-control.json), `n=3`, `L=3/2`, mass `1683003/625000` | [`VERIFIED`](../../packing/resources/web/wand125-tools-2026-09-29/receipts/native-analytic.json) | All 201 angles at threshold `1`, with no unresolved leaves; a complete control for the new engine |
| Retained source negative control, `n=1`, mass `289/10` | [`REFUSED`](../../packing/resources/web/wand125-tools-2026-09-29/receipts/native-admission-refusal.json) | Rejected by the strict mass budget before coverage |
| Tokoharu n11 certificate at `381/100` | [`INCONCLUSIVE`](../../packing/resources/web/wand125-tools-2026-09-29/receipts/native-n11-bounded.json) | Angle 1 only, capped at 100 nodes: 46 accepted leaves and 9 unresolved leaves; no complete coverage claim |
| Same n11 input and exact pending frontier | [`DIAGNOSTIC_ONLY`](../../packing/resources/web/wand125-tools-2026-09-29/receipts/native-n11-bound-comparison.json) | All 9 pending boxes compared; corner bounds improved 3 but produced no new threshold crossing. The predeclared usefulness criterion was not met. |
| Same n11 input, angle 1 at 1,000 nodes and depth 20 | [`INCONCLUSIVE`](../../packing/resources/web/wand125-tools-2026-09-29/receipts/native-n11-angle1-1000-nodes.json) | 428 accepted leaves; 67 depth-capped leaves and 11 queued boxes remain. No larger replay selected. |
| Same n11 input, two further levels on all 67 depth-capped parents | [`DIAGNOSTIC_ONLY`](../../packing/resources/web/wand125-tools-2026-09-29/receipts/native-n11-depth22-refinement.json) | All 268 children evaluated; 15 parents close completely. The other 52 parents and 11 originally queued boxes prevent complete-angle coverage. |

A complete native coverage receipt for a retained external certificate remains
outstanding. The
[W7 implementation and replay plan](specs/active/plan-2026-09-29-native-rectangle-verification.md),
tracked by **think-bmf3**, requires that run before assigning method-distinct
confirmation to the external certificate.

wand125’s MIT-licensed
[`square-packing-tools`](https://github.com/wand125/square-packing-tools) adds
transformations and search accelerations while retaining the unchanged Tokoharu checker
for acceptance. The
[tools review](reviews/review-2026-09-29-wand125-tools-mathematics.md) tracks transfer,
budget recovery, the `B · UB(n)` ceiling, rescaling and the search changes as separate
claims.
A transformed certificate needs its resulting exact premises checked; if coverage
is inherited, the transformation theorem must justify that inheritance.
Otherwise it needs a new complete coverage run.
Cached search checks and batched counterexample screening supply neither obligation.

The
[executed admission negative control](../../packing/resources/web/wand125-tools-2026-09-29/receipts/admission-control.json)
shows why these obligations must stay separate: the source wrapper scaled a measure to
mass `289/10` for `n=1`, passed all 201 coverage checks, and
[announced `s(1) >= 1.5`](../../packing/resources/web/wand125-tools-2026-09-29/receipts/admission-control.log).
Since `s(1)=1`, the announcement is false.
Coverage succeeded, but the required `mass < n` check was absent.
The native checker rejects that retained scaled input at admission, before attempting
coverage.

## T-059 Row Replay and Its Separate Global Argument

The wand125 entries are T-058 (ceiling) and T-059 (row replay).
Their September 29 intake and archived receipts used provisional labels T-056/T-057; the
merge retained those published IDs for Couzo and de Winter and assigned these new IDs to
wand125. Historical receipts keep their original labels and bytes.

T-059 concerns all 12,028 row minima of the Kleddamag n11 point and threshold-charge
certificate. It is a different input and theorem from the Tokoharu rectangle example.
The [row-census wrapper](../../packing/devtools/check_general_pose_tree_census.py) has
three distinct operations: inspect legacy rows as unbound inventory, run the pinned
source checker with production-time input and source binding, and validate the resulting
row journal.
Complete row equality requires each index from 0 through 12027 exactly once.
Missing, repeated, stale or mixed rows cannot establish it.

The wrapper independently evaluates each returned witness with exact arithmetic.
This confirms the reported charge at that center; minimality over the entire row domain
still relies on the pinned source’s search.
A witness alone supplies an upper bound on the true minimum.
The wrapper uses isolated Python execution so an inherited optimization setting cannot
disable upstream assertions.

The
[fresh bound journal](../../packing/resources/web/wand125-tools-2026-09-29/receipts/n11-bound-sample-portable.jsonl)
and
[summary](../../packing/resources/web/wand125-tools-2026-09-29/receipts/n11-bound-sample-portable-summary.json)
cover rows 0, 6014 and 12027. All three source minima equal `1000047518`, and the
independent evaluator confirms all three attaining witnesses.
The result is `PARTIAL_ROW_EQUALITY`: 12,025 rows remain unreplayed by this wrapper, and
this sample does not include the recorded global minimum.
Its timing is a sample measurement, not a measured full-run cost.

The global packing argument is a separate obligation, already established for this
identical certificate by the
[complete native parent-core review](reviews/review-2026-09-22-native-n11-parent-core.md)
and its retained 12,028-row coverage decision.
That evidence proves the angle cover, strict enclosures, D4 reduction, threshold-charge
budget and positive counting gap, supporting the existing `V4/C4` bound `s(11) > 31/8`.
It is reusable evidence, not a missing proof or a new promotion.
Native threshold coverage need not reproduce each exact row minimum, so it does not
settle T-059’s claimed minimum equalities.
The
[bead map](specs/active/plan-2026-09-29-native-rectangle-verification.md#continuing-work-and-bead-dependencies)
tracks wrapper admission, complete replay and this prior-evidence reconciliation as
`think-pgrx`, `think-11z6` and `think-4t1e`.

## Mixed Covers and External Replay

“Mixed” names several formats here.
Threshold atoms, a point-and-segment measure, and the n50 rectangle bundle have
different geometric meanings and different acceptance conditions.
An importer must identify the measure and the theorem explicitly.

The
[September 28 Evan Daniel packet](../../packing/resources/web/evand-square-packing-2026-09-28/README.md#limitations)
retains complete fresh `zmx2` runs, independently audited root inventories, and samples
of the separate `zm_mixed.py` checker.
Re-summarising the shipped complete records or replaying a restricted region does not
constitute a complete fresh run of that second checker.
The native point and parent-core routes do not implement its zero-margin segment
measures. For the separate n32 point cover, [T-051](../../packing/frontier/RESULTS.md)
now retains two complete source-checker replays and is `V4/C4`. Its
[record](../../packing/frontier/n-032.md) distinguishes the arithmetic and box-closing
arguments while naming the shared point test, D4 fold, author and subdivision
architecture. This n32 confirmation does not discharge the pending complete mixed-cover
re-sweeps for n21 and n45.

The
[September 28 wand125 packet](../../packing/resources/web/wand125-point-and-mixed-2026-09-28/README.md#limitations)
distinguishes exact premise audits, source replay and pending work for each case.
In particular, its retained n50 sample covers four of 201 directions; that sample alone
does not establish the full rectangle claim.
The tool’s comparison modes can accept a matching partial run, so comparison success
must be read together with the covered scope.
A summary labelled `PASS` is meaningful only with the obligations it names.

Lean evidence needs the same separation.
Regenerating a data file or scanning for `sorry` does not run the kernel.
A theorem conditional on an unproved coverage premise also leaves that premise
outstanding after a successful build.
The external packets record which builds were attempted, which were blocked, and which
covering statements remain hypotheses; their status cannot be inferred from the presence
of `.lean` files.

## Admission and Regression Checks

Before promoting an imported lower bound, require:

1. **Identity and interpretation:** a pinned source, immutable certificate bytes,
   explicit count and side, measure format, and the exact checker or importer revision.
2. **The theorem’s premises:** nonnegative mass or charge, correct budget, symmetry
   where used, valid angle cover, containment and boundary conventions, and any
   transformation or rescaling argument.
3. **Complete decision scope:** every required angle, row or root, with no missing or
   duplicated work, no unresolved boxes, and no failed or capped branch treated as
   acceptance. Retain the full verdict and its input binding.
4. **Accurate confirmation:** distinguish source replay, first-party premise audit,
   first-party complete coverage and a second complete method.
   Record formal-kernel results and remaining hypotheses separately.

The fast regression tests cover several refusal boundaries:
[Tokoharu input and source mutations](../../packing/tests/test_tokoharu_density_audit.py),
[wand125 rectangle identity and frontier binding](../../packing/tests/test_wand125_rectangle_audit.py),
[native rectangle decisions and refusals](../../packing/tests/test_rectangle_density.py),
[point gate failures](../../packing/tests/test_decide_certificate.py),
[threshold decisions](../../packing/tests/test_decide_threshold_certificate.py),
[parent-core premises](../../packing/tests/test_fractional_parent_core.py),
[mixed-cover census and arithmetic](../../packing/tests/test_evand_mixed_covers.py), and
[wand125 point and mixed packet audits](../../packing/tests/test_wand125_point_and_mixed.py).
These tests check the tools’ contracts; their passing does not replay every large
certificate. The [validation tiers](../../development.md#validation-tiers) distinguish
routine checks from deliberately scheduled full computations.

The
[native verifier plan](specs/active/plan-2026-09-29-native-rectangle-verification.md#implementation-and-review-standards)
requires tbd’s language, testing and code-review guidelines, including the Rust rules
for Rust implementations and the golden-testing rules for CLI receipts.
Golden outputs preserve a reviewed decision trace; analytic controls and mathematical
review establish why the expected decision is justified.
The Rust `sqsearch` quality gate applies to the search crate.
It does not compile or test archived standalone `zmx2` sources, whose replay and
arithmetic obligations belong to their retained source packets.

For the new tools intake, transformation tests must include invalid target counts,
exhausted budgets, altered scales and nets, and stale metadata.
Search-acceleration tests need to exercise cached-axis invalidation, reused LP bases,
omitted working rows, and missing or duplicated parallel angle results.
Timing claims need matched inputs and measured runs; a speed-up is separate from a sound
certificate verdict.

The
[static accelerated-verifier review](reviews/review-2026-09-29-wand125-tools-mathematics.md#accelerated-verifiers-static-review)
found that the lazy-zmx2 wrapper does not enforce pinned build identities or a mandatory
positive reference census, and its final assertions disappear under optimized Python.
Those admission controls need repair before integration.
The cached-axis arithmetic appears unchanged, but compiled differential tests remain
outstanding. Neither static review constitutes a complete accelerated replay.

## Running the Tools

Run commands from `packing/` with the project CPython 3.14 environment.
On this Mac, first verify the external scratch volume and set `TMPDIR`,
`CARGO_TARGET_DIR` and `UV_CACHE_DIR` to the task’s external scratch directories,
following [AGENTS.md](../../AGENTS.md).
Keep unique receipts outside disposable scratch.
Use each packet’s replay instructions for its complete source invocation and resource
ceiling.

```bash
# Native retention decisions on certificates in the corresponding native format.
uv run --frozen python -m devtools.decide_certificate CERTIFICATE.json
uv run --frozen python -m devtools.decide_threshold_certificate CERTIFICATE.json

# Native exact rectangle prototype: full net, with an explicit cooperative search budget.
uv run --frozen python -m devtools.verify_rectangle_density CANDIDATE.json \
  --n COUNT --side SIDE --threshold 10001/10000 --angles all --max-seconds 300

# Exact premises and retained-record audits; these do not run global coverage.
uv run --frozen python -m devtools.audit_wand125_point_and_mixed exact --check
uv run --frozen python -m devtools.audit_evand_mixed_covers check

# Explicitly selected complete upstream replay of one retained rectangle certificate.
# RECEIPT_DIR must name a fresh durable output directory.
uv run --frozen python -m devtools.audit_tokoharu_density \
  --out "$RECEIPT_DIR" --n 11 --replay --workers 2 --timeout 900
```

The native gates’ `--quick` modes are useful for rejection but cannot retain a
certificate. The rectangle audit without `--replay` runs the exact prerequisites only.
Resume and comparison commands must retain the distinction between an incomplete
computation and a completed proof.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
