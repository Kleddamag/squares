# Statement Audit: the Lean Formalization of Eleven-Square Optimality

**Date:** 2026-10-06. **Lane:** N11 of epic `think-wyf4`, bead `think-8spq`, stages 1 to
3 of the [result import runbook](../../../packing/campaign/result-import.md) for the
formalization of `T-060`. **Reviewer:** Claude Opus 5.5 (AI), the importing lane; this
is the lane’s own audit, not the separately prompted adversarial review, and **not the
human expert formalization review that `V5` needs** (§8).

**In one line:** `ElevenSquare.optimality` states exactly `T-060`’s claim, $s(11) = T$
with $T$ the register’s exact endpoint, over the register’s model of closed unit squares
with arbitrary independent rotations, boundary contact allowed and open interiors
disjoint. The only thing on its critical path besides Lean’s kernel and the three
standard axioms is `native_decide`: 10,464 numerical declarations, 13,308 auxiliary
axioms, trusted to Lean’s compiler, as the source itself says.
No defect blocks recording it.

## 1. What Was Audited

| Field | Value |
| --- | --- |
| Source | [Queuingtheorydotcom/11SquaresFormalized](https://github.com/Queuingtheorydotcom/11SquaresFormalized) at `cdc746ed907d258057c283aeb6d077cb2c27e349`, retained in the [6 October packet](../../../packing/resources/web/queuingtheorydotcom-n11-lean-2026-10-06/README.md) |
| Claim | `T-060`: $s(11) = T = (6u+4)/(1+2u-u^2)$, $u$ the unique root in $(9/25, 37/100)$ of $5u^8-10u^7-2u^6+14u^5+12u^4-6u^3+2u^2+2u-1$, independent rotations and boundary contact allowed |
| Read in full | `Geometry.lean`, `BasicGeometry.lean`, `Endpoint.lean`, `EndpointBounds.lean`, `Foundations.lean`, `Optimality.lean`, `Verification.lean`, `Pending/S09_GlobalLowerBound.lean`, `Cases.lean`; the declarations of `Construction.lean`; `lakefile.lean`, `lake-manifest.json`, `lean-toolchain`; `README.md`, `MISSING.md`, `ASSEMBLY.md`, `PROVENANCE.md`, `ACKNOWLEDGEMENTS.md`, `AGENTS.md`, `docs/VERIFICATION_20261006.md`; the run’s `summary.json`, `provenance.json`, `independent-review.json`; the final audit’s structure and axiom map |
| Run here | A streamed read of the commit’s archive, every Lean module hashed and scanned ([`receipts/tree-scan.json`](../../../packing/resources/web/queuingtheorydotcom-n11-lean-2026-10-06/receipts/tree-scan.json)); the axiom receipt extracted from the final audit ([`receipts/lean/axioms-public-theorems.json`](../../../packing/resources/web/queuingtheorydotcom-n11-lean-2026-10-06/receipts/lean/axioms-public-theorems.json)); a build of the statement closure from the retained bytes (§5) |
| Not done here | A build of the whole proof: 7,920 modules, which the source ran on a 64-worker runner and whose compiled objects alone are about 7.94 GB beyond Mathlib’s, on a host with 4 shared cores and under 12 GB of free disk |

## 2. The Claim Against the Theorem, Line by Line

The public theorems are in `Optimality.lean`, in `namespace ElevenSquare`:

```lean
theorem optimal_side_lower_bound {S : ℝ} (h : Packable 11 S) : T ≤ S
theorem optimality : Optimality
```

with `Optimality` from `Foundations.lean`:

```lean
def Optimality : Prop := Packable 11 T ∧ ∀ S : ℝ, Packable 11 S → T ≤ S
```

| `T-060` says | The formalization says | Where | Agrees |
| --- | --- | --- | --- |
| $s(11) = T$: the least side of a square holding eleven unit squares is $T$, attained | `Packable 11 T` and every `S` with `Packable 11 S` has `T ≤ S`; definitionally `IsLeast {S | Packable 11 S} T` (§5 checks this by `Iff.rfl`) | `Foundations.lean`, `Optimality.lean` | Yes |
| Eleven squares | `squares : Fin 11 → UnitSquare` | `Geometry.lean`, `Packing` | Yes |
| Unit squares, closed | `UnitSquare` is a `center : ℝ × ℝ` and an `axis : ℝ × ℝ` with `normSq axis = 1`; `ClosedSquare q p` is `|localX q p| ≤ 1/2 ∧ |localY q p| ≤ 1/2`, the coordinates of `p - center` along `axis` and its perpendicular | `Geometry.lean` | Yes: side 1, closed |
| Any orientation, independently | Each square has its own unconstrained real unit axis | `UnitSquare` | Yes |
| The container | `InContainer S p` is `0 ≤ p.1 ≤ S ∧ 0 ≤ p.2 ≤ S`; `contained`: every point of every closed square is in it | `Geometry.lean`, `Packing` | Yes: the closed $[0,S]^2$, axis-aligned without loss of generality |
| Boundary contact allowed | Containment is of closed squares in a closed container; only open interiors must be disjoint | `Packing` | Yes |
| Disjoint interiors | `OpenSquare` is the strict version of `ClosedSquare`; `interior_disjoint`: for `i ≠ j` no point is in both open squares | `Geometry.lean`, `Packing` | Yes |
| A packing exists at side $S$ | `Packable n S := Nonempty (Packing n S)`; `Packing` also carries `side_nonneg : 0 ≤ S`, which any packing of a unit square implies | `Geometry.lean` | Yes; the extra field is harmless |
| $T = (6u+4)/(1+2u-u^2)$ | `def T : ℝ := (6*u+4)/(1+2*u-u^2)` | `Endpoint.lean` | Yes, symbol for symbol |
| The polynomial | `endpointPolynomial x = 5 * x^8 - 10 * x^7 - 2 * x^6 + 14 * x^5 + 12 * x^4 - 6 * x^3 + 2 * x^2 + 2 * x - 1` | `Endpoint.lean` | Yes, term for term |
| $u$ the unique root in $(9/25, 37/100)$ | `u := Classical.choose endpoint_root_exists`, a root in `(rootLo, rootHi)`, two 30-digit rationals inside $(9/25, 37/100)$; `u_unique`: any root in the closed $[9/25, 37/100]$ equals `u`, from the derivative’s positivity there | `Endpoint.lean` | Yes: existence, location and uniqueness are proved, not assumed |
| $T = 3.8770835900228141773078970601…$ | Not stated; `EndpointBounds.lean` proves $191/50 < T < U$ with `U = 387708359002281417731/10^20`, and the register’s decimal is below `U` by about $2 \times 10^{-21}$ | `EndpointBounds.lean` | Consistent; the decimal is the register’s |
| No uniqueness of the packing | None stated | — | Yes |

**Name resolution.** `Optimality.lean` writes `Optimality`, `Packable` and `T` inside
`namespace ElevenSquare`, where they resolve to the definitions above: Lean refuses a
second declaration of the same name, no module defines a `Pending.T`, `Pending.Packing`
or `Pending.Packable` (`ElevenSquare/Pending/`, `Interop/` and `Simplified/` were
searched), and no module anywhere in the build declares a notation, macro, syntax or
elaborator that could reparse them (§4). The theorem’s own type was not printed from the
full environment, which needs the full build.

## 3. The Axiom Receipt

The source’s finalizer parses `#print axioms` from the run’s compiler logs into the
final audit, which is pinned in the packet by SHA-256 and whose decompressed digest
matches `summary.json`. For `ElevenSquare.optimality`,
`ElevenSquare.optimal_side_lower_bound` and `ElevenSquare.Pending.global_lower_bound`,
it records exactly:

- `propext`, `Classical.choice` and `Quot.sound`;
- 13,308 axioms named `<declaration>._native.native_decide.ax_<i>_<j>`, owned by 10,464
  declarations, the whole of the audit’s `native_certificate_axioms`.

No `sorryAx` and no other axiom appears for any of the audit’s 2,234 targets.
The three certificate targets depend on 3,346 (baseline), 1,832 (prior) and 3,920
(returned) of the native axioms.

**What the native axioms trust.** Each is the proposition a `native_decide` call
evaluated with compiled code, admitted as an axiom; the kernel never checks it.
The theorem therefore trusts Lean’s compiler, code generator and runtime, and any
`implemented_by` or `extern` in Lean core, Batteries or Mathlib that the evaluated code
reaches, such as the GMP-backed arithmetic of `Nat`. The project itself adds none (§4).
That is the trust model the source names, `lean_kernel_and_native_compiler`, and it is
weaker than a kernel-only check: the record must not describe this theorem as using “the
standard axioms only”.

**A difference from the 4 October report.** wand125 reported on jlevy/squares#317 that
the 76 prior-family and the 173 returned cases are kernel-checked with Lean’s standard
axioms only. That describes wand125’s proofs of those components.
In this integrated snapshot, `prior_certificate_exists` and
`returned_certificate_exists` depend on 1,832 and 3,920 `native_decide` axioms: the
integrated certificates are decided natively.

## 4. Kernel Escapes on the Critical Path

The scan read all 7,928 `.lean` files of the commit’s archive, 1,053,173,196 bytes,
without extracting it, and counted tokens in the text with comments and string literals
removed:

| Token | Files | Load-bearing |
| --- | --- | --- |
| `native_decide` | 1,839 files, 10,464 uses: the inventory’s counts exactly | Yes. All 13,308 generated axioms are in the public theorem’s axiom set |
| `sorry`, `admit` | 0 (4 files mention `sorry` in comments) | — |
| `axiom` declarations | 0 (1 file in a comment) | — |
| `implemented_by`, `extern`, `unsafe`, `opaque`, `csimp`, `ofReduceBool`, `trustCompiler` | 0 | — |
| `debug.skipKernelTC`, `#exit`, `#eval`, `run_cmd`, `run_elab`, `run_meta`, `run_tac`, environment modification, `initialize` | 0 | — |
| `notation`, `infix`, `prefix`, `postfix`, `macro`, `macro_rules`, `syntax`, `elab` | 0 | — |
| `import Lean…` | 9 files, each `import Lean.Elab.Tactic.Omega` (the `omega` tactic); 8 in the build | No escape |

**The scanned bytes are the run’s.** The SHA-256 of every one of the 7,920 modules in
the archive equals the final audit’s `source_sha256` entry for it; none is missing and
none differs. The eight other `.lean` files (the lakefile, two script fixtures, five
simplification benchmarks) are outside the build.
The three build pins hash to the digests in `provenance.json`, and the `ElevenSquare`
and `Sqpack` trees are the Git objects `summary.json` records for the verified commit
`1bf942a7`.

The scan is a token count, not a parse: a construct spelled differently would pass it.
It is a premise check beside the final audit’s axiom map, which is the decisive record
of what the theorem depends on.

## 5. The Statement Closure Built Here

`ElevenSquare.Foundations` imports no `Pending` module, so every definition the public
statements use, and the construction that attains $T$, build without the proof.
Its closure is 18 modules, about 410 KB, retained in the packet byte for byte.
On 6 October, from 18:49 to 18:57 UTC, they were built here one module at a time with
`nice -n 10` and `LEAN_NUM_THREADS=2`, on `leanprover/lean4:v4.34.1` (commit `5045d005`,
the compiler string the source’s run reports) and Mathlib `d13f23b7` from its official
cache, which was fetched whole and then pruned to the 1,836 Mathlib modules the closure
imports to fit the disk.
All 18 built with exit 0; no Mathlib module was rebuilt.
[`build-statement-closure.log`](../../../packing/resources/web/queuingtheorydotcom-n11-lean-2026-10-06/receipts/lean/build-statement-closure.log)
is the receipt.

Then
[`AuditN11Statement.lean`](../../../packing/resources/web/queuingtheorydotcom-n11-lean-2026-10-06/receipts/lean/AuditN11Statement.lean),
written for this audit, elaborated against those definitions with no error
([`audit-statement.log`](../../../packing/resources/web/queuingtheorydotcom-n11-lean-2026-10-06/receipts/lean/audit-statement.log)).
It checks the claim against the formal statement in Lean rather than by reading:

- `Optimality ↔ IsLeast {S : ℝ | Packable 11 S} T` by `Iff.rfl`: the statement is
  $s(11) = T$ with the minimum attained, by definition;
- `T = (6u+4)/(1+2u-u^2)` by `rfl`, and `endpointPolynomial x` equal by `rfl` to the
  register’s polynomial written out term by term here;
- `u ∈ (9/25, 37/100)`, `endpointPolynomial u = 0`, and every root in $[9/25, 37/100]$
  equal to `u`, from the source’s lemmas;
- `#print` of `Point`, `dot`, `normSq`, `perp`, `UnitSquare`, `localX`, `localY`,
  `ClosedSquare`, `OpenSquare`, `InContainer`, `Packing` and `Packable`, which are the
  definitions §2 quotes;
- two controls that the definitions are not vacuous: the axis-aligned square at centre
  $c$ is exactly $[c_1 - 1/2, c_1 + 1/2] \times [c_2 - 1/2, c_2 + 1/2]$, and two unit
  squares do not pack in a square of side 1 (`¬ Packable 2 1`).

`#print axioms` gives `[propext, Classical.choice, Quot.sound]` for
`construction_packable : Packable 11 T`, the upper half, and for `u_unique`, `T_lt_U`,
`optimality_of_lower_bound`, `improvement_within_cover` and
`packing_has_canonical_mask`. The upper half is therefore kernel-checked here with the
standard axioms only: Trump’s packing at side $T$, in the source’s exact construction.
The lower half, `optimal_side_lower_bound`, is the part that needs the 7,920 modules,
and this build says nothing about it.

## 6. Findings

None blocks recording the formalization as the source’s proof-assistant evidence.

- **F-1, the source’s comments are stale** (non-blocking).
  The doc-comment of `Optimality.lean` says its conclusions remain “UNPROVED until
  `global_lower_bound` and all of its dependencies have clean audits”; that of
  `global_lower_bound` calls it “conditional on the explicitly admitted exclusions and
  case438 capture”; and `verification/admissions.json` still reads
  `SOURCE_COMPLETE_REPLAY_PENDING`. The proof bodies are unconditional, and the final
  audit’s axiom map, with no `sorryAx`, is what says the bound is proved.
  Worth reporting upstream.
- **F-2, compiler trust** (non-blocking for statement fidelity; binding on wording).
  The theorem is not kernel-only (§3). Every view of `T-060` that mentions the
  formalization must say so, and the human formalization review has to accept that trust
  explicitly under its `axioms` check.
- **F-3, the run is not public** (non-blocking).
  EvolvingPrograms/11SquaresEvolving and run 37414883750 answered 404 here.
  The evidence of the passing run is what the source publishes: the summary, provenance,
  integration review and final audit.
  The integration commit itself was not run in Actions; its acceptance rests on the byte
  correspondence that §4 re-checked at module level.
- **F-4, a resumed run** (non-blocking).
  The run reused validated receipts; the finalizer checked each compiled object’s hash
  against its receipt and the axiom reports against the logs, and the integration review
  did not rehash the objects.
  No cold build of the whole proof is on record anywhere.
- **F-5, two libraries, two settings** (non-blocking).
  `Sqpack` compiles with `autoImplicit=true`, `ElevenSquare` with `false`. The public
  statements are in `ElevenSquare`, so an implicit variable cannot enter them silently.

## 7. Verdict

The formal statement says what `T-060` says, with the same exact $T$ and the same model.
The definitions of square, rotation, containment and disjoint interiors are the
register’s. The critical path holds no `sorry`, no declared axiom and no
`implemented_by`; it holds 10,464 `native_decide` declarations, which are load-bearing
and disclosed by the source.
Recorded as `E-n011-lean-formalization-run`, external proof-assistant evidence with a
passing source run and an axiom receipt.

## 8. What `V5` Still Needs

[epistemics.md → Review Records](../../../epistemics.md#review-records) asks for one
formalization review: `kind: formalization`, `reviewer_kind: human`,
`independent_of_author: true`, by a named person who states their competence in Lean and
in the mathematics and is not the formalization’s author, with `checked` including
`statement-fidelity`, `definitions`, `axioms` and `build`, an accepting verdict, and the
document mapped in [`document-map.yaml`](../document-map.yaml) as a non-superseded
review. This audit is none of that: its reviewer is an AI and the importing lane.

The owner may write that record if he can state that competence and has checked the four
items himself; the epistemics names no exception for him and none against him.
One fact bears on `independent_of_author`: the announcement thanks him, as @ojoshe, for
aiding in the process, and the acknowledgements credit this project’s exact packing
formulas. Whether that makes him an author of the formalization is his to say in the
record. No such record exists, and none is written here on his behalf.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
