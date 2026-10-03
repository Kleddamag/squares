# Soundness Review: The Clean-Room Measure Verifier `sqverify-fast`

Reviewed 2026-10-03 by Claude (adversarial AI review, soundness), as review lane RA,
started unattended by the coordinating session and prompted separately from the crate’s
author lane. The subject is [`packing/sqverify_fast/`](../../../packing/sqverify_fast/)
at commit `717e4f8ca` (build `source_sha256` `775807fb…`), its proof obligation
[`SOUNDNESS.md`](../../../packing/sqverify_fast/SOUNDNESS.md), its
[`INDEPENDENCE.md`](../../../packing/sqverify_fast/INDEPENDENCE.md) and README, and the
specification `plan-2026-10-02-independent-measure-verifier.md`, which is not on this
branch: it was removed in `abf0a592b` and was read here from that commit’s parent.
The focus is mathematical soundness: every lemma, every arithmetic path that feeds an
accept decision, and admission.
Speed and independence were not assessed.
This is evidence for the coordinator, not a verdict of record: no rung moves by writing
it.

**In one line:** the mathematics is sound, but the build is not.
Its axis sweep at direction zero lets a non-finite intermediate drop vertices from the
minimum, and an admissible certificate whose direction-zero domain contains a centre of
exact capture zero is reported `verified`. **Reject until S1 is fixed.** (Superseded: S1
to S5 were fixed and the build is accepted on re-review; see §7.) Every lemma of
`SOUNDNESS.md` holds as stated for finite arithmetic.
One proof step (N2) is too weak for format M’s domain, though the code is right under
the spec’s fold. The rotated branch and bound survives the same overflow attack, because
its acceptance test rejects `NaN`.

## 1. What Was Reviewed

| Field | Value |
| --- | --- |
| Crate | `packing/sqverify_fast/`, `src/` 3,709 lines of Rust, toolchain 1.98.0 |
| Commit | `717e4f8ca` (branch head when the lane started) |
| Build identity | `source_sha256` `775807fbaa0845b131b71eec2939f591cf20b3c9cf7981026cab19fa51443eb1` |
| Proof obligation | `SOUNDNESS.md` (437 lines), every lemma |
| Specification | §1.2 to §1.6 of the plan at `abf0a592b~1` |
| Adversarial tests added | [`tests/adversarial.rs`](../../../packing/sqverify_fast/tests/adversarial.rs), seven tests, one `ignore`d as the S1 reproducer |

Read in full: `interval.rs`, `exact.rs`, `certificate.rs`, `axis.rs`, `oracle.rs`,
`rotated.rs`, `lib.rs`, `main.rs`, and the head of `rotated_tests.rs`. The authors’
checkers were not opened.

Commands, from `packing/sqverify_fast/` unless stated: `cargo build --release`,
`cargo fmt`, `cargo clippy --release --all-targets` (clean), `cargo test --release` (all
pass, one ignored), and `cargo test --release --test adversarial -- --ignored` (fails,
as S1 predicts). From `packing/`: the binary on retained certificates with
`--inject-fault-at-node`. Also `packing-validate --only "measure verifier Rust"` and
`packing-validate --edit`, both clean.

## 2. Verdict

**Reject.** One blocking defect:

- **S1.** A non-finite intermediate in the direction-zero vertex sweep removes vertices
  from the minimum silently.
  On an admitted certificate, direction zero is `verified` with a receipt minimum of
  $1.62$, while the exact capture at $(3.5, 3.5)$ in its domain is $0$.

S1 is an arithmetic defect, not a mathematical one: lemma I1 assumes every rounded
result is finite, and nothing in `axis.rs` checks that assumption.
Real certificates have densities near one and cannot trigger it.
A verifier’s soundness claim covers every admitted input, though, and the attacking
certificate passes every admission premise.
The fix is small (§5); with it and the S2 and S3 changes, this reviewer would expect to
accept.

Everything else is sound, or sound under a premise that is stated below and that the
code enforces.

## 3. Lemma by Lemma

| Lemma | Verdict | Notes |
| --- | --- | --- |
| Theorem, N1 (net) | Sound | $\tan\frac{\theta_{r+1} - \theta_r}{2} = D/(1 + t_r t_{r+1})$; the endpoint polynomial is $t > \sqrt2 - 1$. |
| N2 (orientation) | Sound for formats T and L; **too weak for format M** (S3) | The fold at $\theta_{\max}$ suffices for Tokoharu’s domain. The per-bin domain needs the fold at $\pi/4$ (spec N5), which the code’s domains satisfy. |
| N3 (shrink) | Sound | $B\cos\delta(1 + \tan\delta) \le B(1 + D)$ for $\delta \le \arctan D$; for the per-bin bins, spec N2–N4 give the same with $z \le D/2$. |
| N4 (counting) | Sound | Cores are closed, pairwise disjoint, inside $K$; atoms on a core’s boundary are counted once per core. |
| Admission | Sound | §4.1. |
| C1 (quarter turn) | Sound | Both domains are squares centred at $(L/2, L/2)$. |
| D (domains) | Sound with the premise of S3 | `domain_upper` is exact; $\rho$ increases on $[0, \tan(\pi/8)]$, so $\rho(a_r)$ is the least half-width of every orientation folded into bin $r$. |
| A1 (vertices suffice) | Sound | Each term is affine in $x$ times affine in $y$ on a cell, and the events include both domain ends. |
| A2 (column sweep) | **Sound as mathematics; the implementation is defective (S1)** | The slope-step formula and the `Initial`, `At(0)`, `Never` bookkeeping are right. The minimum is taken with `value.lo < min_lower`, which skips `NaN`. |
| R1 (classification) | Sound | Triangle inequality along $u$, $v$ and both axes; slack per F2. |
| R2 (area at the centre) | Sound | §4.3. |
| R3 (mean value) | Sound | $F$ is Lipschitz; the L-shaped path stays in the convex box. |
| R4 (derivative) | Sound | Sign checked: translating the square by $+t$ moves $R$ by $-t$, so the left edge gains. |
| R5 (edge lengths) | Sound | All nine differences re-derived (§4.4). |
| R6 (inheritance) | Sound | A child’s straddling set is a subset of its parent’s; inside and outside rectangles have zero derivative on the child. |
| R7 | Not used by this build | Its proof is correct. |
| B1–B3 (atoms) | Sound | §4.5. |
| B5 (method at $r = 0$) | Sound |  |
| Z1, Z2 (direction zero, branch and bound) | Sound | The indicator is closed where the formula needs open, which differs only on a null set; the cross overlap is unimodal, so its least value over the outward-rounded ends bounds the box. |
| I1 (directed steps) | **Sound with the premise that every rounded result is finite** | `dn(+inf)` and `up(-inf)` are `NaN`; nothing enforces the premise. That is S1 in `axis.rs`, and S4 for the rest. |
| I2 (enclosing rationals) | Sound | `compare` was re-derived for subnormals and both signs. A poor `to_f64` start can only exhaust the 64-step loop, which refuses. |
| F2 (classification slack) | Sound with $L \le 1000$, which admission enforces | Operands are below about $4 \times 10^3$ and errors below $10^{-11}$, against `TAU` $= 10^{-9}$. |
| A3 (audit) | Sound as stated: bookkeeping only, sampled | The release binary can still emit `verified` under fault injection (S2). |

## 4. The Arithmetic Paths That Decide Acceptance

### 4.1 Admission

Decimal tokens are parsed from their text: `serde_json` runs with `arbitrary_precision`,
so a number is its own decimal string.
Fractions are normalised.
Numerators and denominators are capped at 4,096 bits.
Duplicate keys are refused by a separate visitor pass, before the `Value` read.
The D4 images are the eight symmetries of $[0, L]^2$, merged by exact key; a segment and
its reverse share one key.
The mass identity $\int g = M$ is exact.
For format T it is a tautology of the construction, but it is computed, not assumed.
$0 < M < n$, $0 < B < 1$, $B(1 + D) < 1$, $t_{\max}^2 + 2t_{\max} - 1 > 0$,
$t_{\max} < 1$, $L^2 \ge 2B^2$, $L \le 1000$ and containment are all exact.
`main.rs` refuses a threshold below 1, whether declared or given on the command line.

The tests `decimal_masses_are_exact_and_the_mass_premise_is_strict`,
`admission_refuses_each_broken_premise` and
`duplicate_keys_are_refused_before_any_reader_disagrees` attack this layer.
They try $0.1 + 0.2$ against `total_mass`, a mass equal to $n$ written as two decimals,
and $B(1 + D) = 1$ exactly.
They also try a hidden negative weight, a rectangle out by $10^{-30}$, a net one step
short of $\pi/4$, metadata disagreeing with the candidate, format L with a foreign net,
a zero-length segment, and a duplicate `weights` key.
Every one was refused or admitted exactly as the premises require.

Two notes, neither a soundness issue.
Format L’s optional `certificate.D` and `certificate.angle_count` override the net after
the `net` block is checked.
The premises are then checked on the net actually used, so the result is sound, but a
receipt’s `D` can differ from the file’s declared `net`. `total_mass` is optional in
formats M and L, although the spec lists it as a field.

### 4.2 The direction-zero sweep (`axis.rs`)

Every operation is an `Iv` operation, rounded outward.
The overlap of $[x - h, x + h]$ with $[x_1, x_2]$ is enclosed through `min`, `max` and
`pos`, and the slope is updated after each cell’s increment, never before.
The minimum is the defect: see S1.

### 4.3 Lemma R2 (`area_dn`, `section_dn`)

The inner rectangle $[x_1^\uparrow, x_2^\downarrow] \times [y_1^\uparrow,
y_2^\downarrow]$ lies in $R$, and its offsets from $x_0, y_0$ are rounded inward.
Each of $f_1, f_2$ is rounded down and each of $g_1, g_2$ up from the exact enclosures
of $h/s$, $h/c$, $c/s$, $s/c$; $\pm k\xi$ is rounded by the sign of $\xi$. The nodes are
binary64 values used exactly, so their placement affects only tightness.
A piece contributes only when its rounded-down end sum is positive, and the halving is
followed by `dn`. The bound is valid for every choice of nodes.

### 4.4 Lemma R5 (`segment_length`)

The nine terms are $X - Y$ with $X \in \{e', f_1, f_2\}$, $Y \in \{b', g_1, g_2\}$;
$f_1 - g_2$ and $f_2 - g_1$ use $c/s + s/c = 1/(sc)$. All nine match the code.
The horizontal family exchanges $c$ and $s$ correctly: $(h - s\omega)/c$,
$(h + c\omega)/s$, $(-h - s\omega)/c$, $(c\omega - h)/s$. The enclosure over a box
remains valid even where a term depends on both coordinates; it is only less tight.

### 4.5 Atoms (B1–B3)

An atom is inside only by R1 with slack, and outside only by strict separation by more
than `TAU`, so a point or segment on a core’s boundary is never certified outside.
The straddling segment’s two parameter points are proved inside every square of the box,
convexity covers the piece between them, and the mass is taken by parameter.
`box_bounds_never_exceed_exact_capture_on_boundary_configurations` puts, at $L = 1000$,
where F2 is tightest, and at $r \in \{0, 1, 57, 133, 200\}$:

- a rectangle equal to the square’s bounding box;
- $10^{-12}$ slivers hugging its sides;
- every vertex as a point mass;
- every edge as a segment;
- a segment touching each vertex from outside.

It compares `centre_lower_bound` and `box_lower_bound` with the exact oracle at up to
1,440 poses in boxes from $0$ to $0.25$ wide.
No bound exceeded the exact capture.

### 4.6 The branch and bound’s acceptance

Every accept is `bound >= threshold_hi`, which is false for `NaN`, and a lower bound
built from `add_dn`, `sub_dn` or `mul_dn` that overflows becomes `NaN` (`dn(+inf)`),
never $+\infty$. The derivative magnitude `Iv::mag` drops a `NaN` endpoint (`f64::max`).
For each overflow pattern the other endpoint was traced: it is then $\pm\infty$ or the
inherited finite bound, which is valid, so the penalty is infinite or correct.
Boxes come from the rounded midpoint split with half-widths rounded up, so the leaves
cover the root, which encloses $[L/2, U_r]^2$ outward.

## 5. Findings

Severity is blocking, non-blocking, or note.
**One is blocking.**

### S1. The axis sweep drops vertices whose enclosure is `NaN` (blocking)

`axis::verify_axis` takes the minimum with `if value.lo < min_lower`, which is false
when `value.lo` is `NaN`, and decides with `min_lower >= threshold_hi` over the vertices
that remain. A `NaN` arises when the sum of a column’s slope steps overflows.
`add_dn` of two large lower ends is `dn(+inf) = NaN`, and from then on `NaN` sticks to
the slope.

**Reproducer** (`overflow_cert` in `tests/adversarial.rs`; also built by a script
outside the repository).
Format T: $L = 4$, $B = 9/10$, $n = 10^9$, threshold 1.

- A band $[0, 4] \times [3/2, 5/2]$, weight 16, density 2 after merging, captured in
  full by every centre on the domain’s lower edge $y = 2$.
- Twenty slivers $[k/1000, 4 - k/1000] \times [49/20 - 2^{-1000}, 49/20]$, $k = 0..19$,
  weight $2.2 \times 10^7$ each, density about $1.5 \times 10^{307}$.
- Total mass $440{,}000{,}016 < n$. Every premise holds, and the certificate is
  admitted.

Their `+1` slope steps sit just below the domain, so they all enter the initial slope.
Twenty of about $1.3 \times 10^{307}$ overflow, and every vertex above $y = 2$ in every
column becomes `NaN`. The receipt reads `"verdict":"verified"` with
`min_certified_lower_bound` $1.62$, at argmin $(3531/1000, 2)$. The exact capture at
$(7/2, 7/2)$, inside the domain $[2, 71/20]^2$, is $0$: the crate’s own oracle,
`--probe 0,3.5,3.5`, and `overflow_certificate_has_an_uncovered_centre` all agree.
Without the slivers, the same band is refused, as it should be.
`axis_sweep_refuses_the_overflow_certificate` is the regression test.
It fails on this build and is `ignore`d so that the gate stays green; un-ignore it with
the fix.

**Fix.** In `verify_axis`, record a vertex whenever `!(value.lo >= min_lower)`, so that
`NaN` lowers the minimum, or refuse when `!value.is_valid()`. Check that `min_lower` is
finite before accepting.
Defense in depth: refuse at admission any density or mass whose enclosure is not
comfortably finite, for example above $2^{512}$. Make `Iv::pos`, `Iv::min`, `Iv::max`,
`Iv::mag` and the `f64::min` chains in `segment_length` and `section_dn` propagate `NaN`
rather than drop it (S4).

### S2. A fault-injected run can exit 0 with `verified` receipts that do not say so (non-blocking)

`--inject-fault-at-node N` certifies a straddling item inside at box $N$, for the spec’s
§4.2 control. The audit is sampled every 1,024 boxes, so most injections are never
audited. On `rect_n32_L595` at $r = 100$, injection at boxes 9, 16, 23, … 72 (every one
tried past the first few) gave `verified`, `PARTIAL` and exit status 0. Neither the
receipts nor the summary record that a fault was injected.
No evidence pipeline passes the flag.
`check_sqverify_fast` uses it only in controls that require a refusal, so no recorded
verdict is affected.
But a receipt alone cannot show it came from a clean run.
**Fix:** record `inject_fault_at` in every receipt, and never report `verified` or exit
0 when it is set.
The retained controls already pair the flag with `--audit-every 1`; the
binary should require that pairing.

### S3. `SOUNDNESS.md` step N2 folds too late for format M’s per-bin domain (non-blocking, proof text)

N2 reflects only orientations above $\theta_{\max}$. Under that fold, a unit square at
half-angle tangent $t \in (\tan(\pi/8), t_{200} + D/2]$ is assigned to node 200, and its
half-width $\rho(t)$ is less than $\rho(a_{200})$, since $\rho$ falls past
$\tan(\pi/8)$. Its centre can then lie outside the per-bin domain that lemma D checks.
`per_bin_domain_needs_the_fold_at_pi_over_four` computes $\rho(t_{200} + D/2) <
\rho(a_{200})$ exactly.
The spec’s fold, N5, reflects every orientation above $\pi/4$. That makes lemma D
correct and the code sound, since the theorem’s conclusion is the same.
**Fix:** state N2 as the spec’s N5, a fold to $[0, \pi/4]$, and say that lemma D depends
on it.

### S4. Lemma I1’s finiteness premise is unchecked, and several primitives drop `NaN` (note)

`Iv::pos`, `Iv::min`, `Iv::max` and `Iv::mag` use `f64::max` and `f64::min`, which
return the non-`NaN` operand.
So does the `.min` chain in `segment_length` and `section_dn`. A `NaN` endpoint can
therefore become a finite and wrong one.
In the rotated path this cannot be reached from an admitted certificate:

- coordinates are at most $1000$;
- the line coefficients are at most about $250$;
- every overflow of a density product that was traced ends in an infinite penalty or a
  `NaN` bound, which the acceptance test rejects.

S1 is the same pattern where it does reach.
Bounding densities at admission (S1’s defense in depth) would close the class.

### S5. The specification `SOUNDNESS.md` cites is not on the branch (note)

Lemma D and the atom lemmas defer to “spec §1.4–§1.6”. The plan was deleted in
`abf0a592b`, so a reader of this branch cannot follow those references.
Restore the plan, or link the commit that holds it.

### S6. What the existing tests could not have caught (note)

The randomised property tests draw densities of order one at side 6, so neither overflow
nor F2’s extreme magnitudes are exercised.
`tests/adversarial.rs` adds both.
It also adds the boundary-pose configurations, where an off-by-slack classification
would show first.

## 6. What a Fix Must Show

- `axis_sweep_refuses_the_overflow_certificate`, un-ignored, passing.
- A second reproducer for S1 in which the `NaN` arises inside the domain (a `delta[j]`
  rather than the initial slope), also refused.
- The S2 receipt field, and a test that an injected run exits non-zero.
- The S3 edit to `SOUNDNESS.md`.
- `packing-validate --only "measure verifier Rust"` clean, and the census unchanged: the
  fix touches no finite path, so every recorded verdict should reproduce bit for bit.

## 7. Re-Review, 3 October Evening

Re-reviewed by the same lane, Claude (adversarial AI review, soundness), at the lane W2
head `4ddf37d9c`, which merges this branch.
The fixes are `cfb653a2f`, for S1 to S4, and `61acc9dcb`, for review RB’s TI-1 to TI-3
and the per-bin question.
Read in full: the diff of `src/` since `0e38246a9`, and the new or changed text of
`SOUNDNESS.md` (N2, N3, F3 and the tests list).
The coordinator asked four questions; each is answered below.

**Verdict: accept.** S1 to S5 are closed.
One note is new, R1, on the wording of N2, and it changes no conclusion.
A second, R2, is about the audit, which is not a lemma.

### 7.1 Each fix closes its defect

- **S1.** `verify_axis` now stops a column at the first vertex whose enclosure is not
  finite, records `non_finite`, and accepts only when `min_lower` is finite and at least
  the threshold. Both of W2’s reproducers end `non-finite`: the original, with the
  overflow in the initial slope, and a second whose slivers end at ordinate 3, so the
  overflow arises in a `delta[j]` inside the domain.
  Admission now refuses the original certificate outright, because its densities exceed
  $2^{96}$. The reproducers therefore raise the densities after admission, which tests
  the sweep itself. Variants added here:
  - `overflow_in_the_rotated_search_is_never_verified` raises the same densities in the
    branch and bound at $r \in \{1, 100, 200\}$, and in its direction-zero branch,
    forced with a point mass.
    None is verified.
  - `the_s1_shape_at_the_density_cap_is_refused_and_finite` builds the S1 shape just
    under the cap, with slivers $2^{-60}$ high: below a unit in the last place of their
    ordinate, so every event width straddles zero.
    Admission accepts it.
    Direction 0 is `refused` with a finite minimum of about $-10^{17}$, and $r = 1$ and
    $r = 200$ stop as counterexample candidates.
    None is `non-finite`. The exact capture at $(7/2, 7/2)$ is $0$.
- **S2.** `run_direction` turns any verified receipt from a fault-injected run into
  `fault-injected`, unverified, and records `fault_injected_at_box` in it and in the
  summary. `a_fault_injected_run_is_never_verified` holds it.
- **S3.** N2 now folds at $\pi/4$ and says that lemma D depends on the fold.
- **S4.** `fmin` and `fmax` replace `f64::min` and `f64::max` in every interval
  primitive and in R2, Z1 and Z2. Each selects with one comparison, which keeps a `NaN`
  second operand, then adds $0 \cdot a$, which is `NaN` when the first operand is `NaN`
  or infinite. On finite operands both return exactly `f64::min` and `f64::max`,
  including the signed zeros, which
  `fmin_and_fmax_are_exact_on_finite_operands_and_poison_on_failure` checks.
  An infinite second operand is selected correctly, so the primitives never turn a
  failure into a finite wrong value.
  `area_dn` now carries a `NaN` trapezoid sum into the total instead of skipping it.
  The search refuses a box whose centre bound, atom bound or own derivative enclosure is
  not finite. The inherited-bound path needs no check: its parent’s bounds were checked,
  and a `NaN` penalty fails `>=`.
- **S5.** `SOUNDNESS.md` now names commit `abf0a592b`, where the plan can still be read.

### 7.2 Lemma F3 and the caps

The caps are a side of at most 1,000, at most $2^{16}$ directions, a last tangent of at
most $1/2$, at most $10^6$ rows, an expanded density of at most $2^{96}$ (checked after
merging, per key), and a total mass below $n < 2^{64}$. Every step of F3 was rechecked
against them:

- **Line coefficients.** $D > 	an(\pi/8)/2^{16} > 2^{-18}$, so $s_1 > 2^{-18}$; with
  $c \ge 3/5$, each line coefficient is below $2^{19}$, and each R5 term is below
  $2^{12} \cdot 2^{19}$.
- **Sweep events.** There are at most $4 \cdot 8 \cdot 10^6 + 2 < 2^{25}$ of them, so
  column weights, slopes and vertex values sit far below $2^{1024}$.
- **Outward rounding.** The growth factor over $2^{40}$ steps is about $e^{2^{-11}}$.
- **Atoms.** Points and segments carry no density, only mass below $2^{64}$.
- **Division.** The divisor in `lambda_range` is bounded below and its quotient is
  clamped, as F3 says.

`lemma_f3_holds_at_its_extremes` admits the extreme corner: $L = 1000$, $2^{16}$
directions at the smallest step the endpoint polynomial allows, and rectangles at
exactly $2^{96}$. It searches $r \in \{0, 1, 2, 2^{16} - 1\}$. No direction ends
`non-finite`.

F3 is sound. The caps cost the retained certificates nothing: W2’s census at `4ddf37d9c`
reproduces the earlier nodes and least bounds wherever both runs exist.

### 7.3 Format M’s shrink step

Bin $r$ takes half-angle tangents $t$ with $|t - t_r| \le D/2$. Then
$z = 	an(\delta/2) = |t - t_r|/(1 + t t_r) \le D/2$, and
$\cos\delta + \sin\delta = (1 + 2z - z^2)/(1 + z^2) \le 1 + 2z \le 1 + D$, because the
difference $2z^2 + 2z^3$ is nonnegative.
So $B(1 + D) < 1$ suffices, and the half-angle form of N3 is sound for both domains.
The extra admission check $B(1 + D/(1 - D^2/4)) < 1$ for format M is stronger than
needed. It is harmless at $B = 9977/10000$, where the two limits are $0.997929\ldots$,
and it can only refuse.
Admission now also pins format M’s and format L’s net to step $83/40000$ with 201
directions, so metadata cannot move the bins lemma D assumes.

### 7.4 No new path to a false `verified`

Every changed decision only adds refusals: the non-finite stops, the fault-injection
override, the gzip checks, the net pin, and the per-bin premise.
`fmin` and `fmax` agree with the old selections on every finite input, so no finite
verdict can change; the census confirms this.
The only change that loosens anything is the audit’s new `representation_slack` (R2
below), and the audit decides refusals only.

### R1. N2 still ends “so $\delta \le rctan D$” (note, proof text)

Under the half-angle assignment, $\delta$ can reach $2rctan(D/2)$, which is larger than
$rctan D$, as N3 itself now says.
The sentence in N2 is therefore false, and N3’s first chain,
$B\cos\delta(1 + 	an\delta) \le B(1 + D)$, rests on it.
The half-angle form in N3 makes both domains sound without it.
Edit N2 to conclude $	an(\delta/2) \le D/2$, and let N3 use only the half-angle form.

### R2. The audit’s tolerance can become vacuous for extreme slivers (note)

To end false `audit-failed` refusals (RB’s TI-1), `representation_slack` widens the
tolerance by each rectangle’s density times the gap between its outer and inner
representable rectangles.
Near the $2^{96}$ cap that gap times the density can exceed the bound itself, and then
the audit cannot detect a bookkeeping error at that box.
This is not a soundness gap: the audit (A3) is defense in depth, and no acceptance rests
on it. `SOUNDNESS.md` should still say that the audit is weakest where densities are
extreme.

Commands: `cargo fmt`, `cargo clippy --release --all-targets` (clean),
`cargo test --release` (all pass, none ignored), and `packing-validate --edit` (clean).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
