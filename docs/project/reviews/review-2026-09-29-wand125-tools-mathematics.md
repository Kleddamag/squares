# wand125 Tools: Mathematical and Admission Review

The new repository publishes search machinery around Tokoharu’s rectangle-density
certificates, plus a separate exact point-and-threshold checker.
Its source supports reusing the existing rectangle proof contract.
Two claims need qualification before we adopt the tooling: the general $B\,UB(n)$
ceiling omits an orientation condition, and `scale_and_verify.py` can announce a packing
bound without checking the target count’s mass budget.

The disputed ceiling is tracked as **T-056**. The separately reported equality of the
n11 row scans is **T-057**.

This is a W2 factual review of
[wand125/square-packing-tools at `0d33ab61726c2ab03e3eb8f457dabaf22db8571f`](https://github.com/wand125/square-packing-tools/tree/0d33ab61726c2ab03e3eb8f457dabaf22db8571f),
retrieved on 2026-09-29. The admission defect was reproduced with the unchanged upstream
checker, and three n11 row scans were replayed.
The ceiling findings are source inspection and mathematical derivations.
The
[PR review comment](https://github.com/jlevy/squares/pull/246#issuecomment-5886292553)
records the intake findings and their initial dispositions.
No complete replay of the 12,028-row claim or reproduced speed measurement is claimed.
The [existing rectangle review](review-2026-09-22-tokoharu-density-mathematics.md)
supplies the detailed continuous coverage argument.

## What the New Claims Establish

| Component | Claim and proof obligation | Review disposition |
| --- | --- | --- |
| Transfer to another $n$ or $L$ | Reuse support and re-optimize weights, then prove coverage and the new exact budget | Valid architecture; transferring support alone proves nothing about the new target |
| Budget recovery | Add or move rectangle columns and repair screened violations before final verification | Search operation; requires a fresh proof at the final geometry and mass |
| Weight rescaling | Multiply nonnegative weights by an exact positive factor; coverage and mass scale linearly | Valid identity; final budget and coverage must both be checked |
| $B\,UB(n)$ ceiling | Pack $n$ disjoint checked cores into the container and sum their coverage | Valid for a packing whose orientations belong to the checked net; unrestricted statement has a missing premise |
| Working rows, cached bases, batched screens | Produce useful candidates faster | Outside the proof path when final full verification is mandatory |
| Cached-axis C++ checker and lazy zmx2 | Preserve verifier behavior while changing evaluation work | Separate implementation claims; source provenance and full-domain comparison required |
| General pose tree | Reproduce 12,028 n11 per-row minima with exact arithmetic | Reported upstream result; global counting argument and local replay remain separate obligations |

The source’s
[provenance table](https://github.com/wand125/square-packing-tools/blob/0d33ab61726c2ab03e3eb8f457dabaf22db8571f/solver/PROVENANCE.md)
identifies Tokoharu’s upstream commit `84bebef51856d46a19c145b035664324ba9572d3`. We
also compared Git blob identities of `solver/verify.cpp` and the previously retained
Tokoharu source: both are `9a64c606d9dd76843d06b4f120038df7d167606b`. This establishes
source identity for the checker, not a new replay result.

## Ceiling: Account for the Angular Net

[`l_cap.py:17–23`](https://github.com/wand125/square-packing-tools/blob/0d33ab61726c2ab03e3eb8f457dabaf22db8571f/transfer/l_cap.py#L17-L23)
argues that a packing of unit squares at side $U=UB(n)$, scaled by $B=9977/10000$,
provides $n$ disjoint cores each charged at least one.
The checker establishes that coverage for side-$B$ squares at the 201 angles
$\theta_r=2\arctan(83r/40000)$, modulo container symmetries.
Its extension to arbitrary orientations applies to *unit* squares, through containment
of a nearby net core.
It does not establish the same coverage for arbitrary orientations of side-$B$ squares.

Thus the stated argument proves a ceiling at $BU$ when the witness packing’s
orientations belong to that net, modulo $D_4$. Axis-aligned grid packings satisfy this
condition. A general freely rotated packing needs an additional containment allowance.
This is a gap in the stated ceiling argument; it is not a counterexample to a published
rectangle certificate.

A sufficient general ceiling follows from the existing nearest-angle calculation.
Put $D=83/40000$ and

$$
\alpha=B(1+D)=\frac{399908091}{400000000}=0.9997702275.
$$

For every orientation, a nearest checked angle has discrepancy $|\delta|\le\arctan D$. A
concentric side-$B$ core at that angle fits inside a square of the original orientation
and side $\alpha$, since $B(\cos|\delta|+\sin|\delta|)\le B(1+D)=\alpha$. Scale a
certified packing at side $U$ by $\alpha$, and place this net core inside each scaled
square. Their interiors remain disjoint, and each core is contained in the container.
For a nonnegative rectangle density, boundaries have zero mass, so checked coverage
implies

$$
M\ge \sum_{i=1}^{n}\int_{Q_i}g\ge n.
$$

Consequently a mass budget below $n$ is impossible at $L\ge\alpha U$. This bound is
sufficient, not necessarily sharp.
If the exact witness orientations are available, their individual net discrepancies can
give a smaller common scaling factor.
The checker’s stronger threshold $10001/10000$ only strengthens the mass contradiction.
Smoothing is unnecessary for this argument about the unsmoothed rectangle density.

The numerical table is another limitation.
The
[UB data](https://github.com/wand125/square-packing-tools/blob/0d33ab61726c2ab03e3eb8f457dabaf22db8571f/transfer/data/ub.json)
contains rounded display values, and `l_cap.py` uses only those floats.
For example, the n26 value `5.62132` is below $7/2+(3/2)\sqrt2$, and the n29 value
`5.933833` is below the rational witness side recorded in the same table.
These values are not certified outward bounds.
Some `ubExact` entries instead contain coarser integer bounds.
Treat the current three-decimal output as a search suggestion.
A proved ceiling needs a validated witness, its exact side or outward enclosure, and the
appropriate orientation allowance; rounding the answer down does not establish
impossibility above that rounded value.

## Rescaling: Coverage Acceptance Does Not Check the Budget

[`scale_and_verify.py:27–39`](https://github.com/wand125/square-packing-tools/blob/0d33ab61726c2ab03e3eb8f457dabaf22db8571f/transfer/scale_and_verify.py#L27-L39)
defaults to target mass `28.9`, verifies only that the old mass is smaller, and rescales
the weights exactly.
It calls `certify.py`, then
[prints a bound for the candidate’s `n`](https://github.com/wand125/square-packing-tools/blob/0d33ab61726c2ab03e3eb8f457dabaf22db8571f/transfer/scale_and_verify.py#L63-L79).
It never requires the new mass to be below that `n`.

The called
[`certify.py`](https://github.com/wand125/square-packing-tools/blob/0d33ab61726c2ab03e3eb8f457dabaf22db8571f/solver/certify.py)
checks the support, nonnegative weights, angular margin, interval input, and all 201
coverage cases. It records exact mass but does not compare it with a target count.
Therefore its successful coverage result cannot supply the missing budget premise.
For a candidate whose `n` is below the requested target mass, the wrapper can announce a
bound unsupported by its own checks.
An executed negative control confirms the defect.
We supplied `n=1`, `L=1.5`, `B=0.9977`, and a rectangle on $[0.001,1.499]^2$ with
initial mass $1/2$. The wrapper scaled its mass to the default $289/10$, the unchanged
C++ checker verified all 201 directions in 209 nodes, and the wrapper exited
successfully while announcing `certificate for s(1) >= 1.5`. This bound is false because
$s(1)=1$. The coverage result is valid; the missing mass-budget premise invalidates the
announced packing bound.

The
[receipt](../../../packing/resources/web/wand125-tools-2026-09-29/receipts/admission-control.json)
retains the exact mass, source revision, verifier identity, and complete direction
count. The
[run log](../../../packing/resources/web/wand125-tools-2026-09-29/receipts/admission-control.log)
retains the false announcement.
Reproduce it with the durable
[audit tool](../../../packing/devtools/audit_wand125_tools.py), from `packing/` with the
task’s external scratch environment configured:

```bash
uv run --frozen python -m devtools.audit_wand125_tools \
  /path/to/pinned/square-packing-tools \
  --scratch "$TMPDIR/wand125-admission-control" \
  --out resources/web/wand125-tools-2026-09-29/receipts \
  --timeout 60
```

The scratch directory must be new or empty.
The tool requires the pinned source revision with no tracked modifications and records
the upstream output as a negative control, never as a packing certificate.

The separate
[`rectangle_rescue.py`](https://github.com/wand125/square-packing-tools/blob/0d33ab61726c2ab03e3eb8f457dabaf22db8571f/solver/rectangle_rescue.py)
does check $0<M<n$, binds geometry and candidate bytes to the proof artifacts, checks
all 201 direction records, and compares the resulting verifier source with its selected
snapshot. `ladder/rung.py` calls that guarded path.
The finding is specific to the unprotected scaling wrapper; it does not establish that
the ladder admits the same mistake.

Required integration controls are an explicit integer target count, exact recomputation
of mass, a strict $M<n$ check, equality of admitted and proved $L$ and $B$, complete
direction coverage, and source-bound replay artifacts.
Test a wrong count, an over-budget rescaling, stale geometry, a missing angle, and a
substituted checker.
A successful process exit or a `VERIFIED_CONTINUOUS_DENSITY` label alone is
insufficient.

## Independent Verification and Follow-Up

For rectangle certificates, the existing independent rational preflight verifies the
data conversion, mass, support, symmetry multiplicities, angular containment margin, and
axis event set. The retained external-certificate replays still depend on Tokoharu’s C++
checker for complete nonzero-angle coverage.
Replaying identical C++ through another wrapper is independent of the search, but not
independent of that checker’s implementation.

An independent rectangle checker must enclose every translated overlap over the full
legal centre domain at every net angle, or check a complete subdivision certificate with
independently derived leaf bounds.
It also needs exact input binding, outward arithmetic, termination that refuses
unresolved cells, and the same final continuous-angle and mass argument.
Agreement on sampled centres cannot replace that coverage proof.
Retain the present C++ replay while developing this second route; do not label the
existing preflight a complete independent rectangle replay.
The new [native prototype](../../../packing/src/sqpack/rectangle_density.py) implements
that separate route using exact clipping and common-core bounds, under its
[reviewed contract](review-2026-09-29-native-rectangle-contract.md).
It has completed an analytic control, but its retained n11 probe is inconclusive.

The new
[`general_pose_tree` report](https://github.com/wand125/square-packing-tools/blob/0d33ab61726c2ab03e3eb8f457dabaf22db8571f/general_pose_tree/README.md)
concerns points and threshold charges.
It reports matching all 12,028 row minima of Kleddamag’s n11 certificate and explicitly
leaves the global counting argument with Kleddamag.
That is a useful separate cross-check claim.
Our retained
[three-row replay](../../../packing/resources/web/wand125-tools-2026-09-29/receipts/n11-sample.jsonl)
checked rows 0, 6014, and 12027. Each independently recomputed minimum matched its
recorded value, and each exact witness replayed.
These probes establish agreement on those three rows; **T-057’s full 12,028-row census
remains reported**. Its arithmetic, row enclosure, boundary semantics, $D_4$ folding,
threshold budget, exact $11\Gamma>M$ inequality, and complete row census each require
review or replay before we promote its result.
It does not verify rectangle densities or remove their current C++ dependency.

Source review found no defect in the threshold-charge boundary argument, exact four-axis
separation test, leaf enumeration, witness reconstruction, or endpoint wall enclosure
for well-formed pinned inputs.
The replay harness still needs admission controls:
[`run_n11.py`](https://github.com/wand125/square-packing-tools/blob/0d33ab61726c2ab03e3eb8f457dabaf22db8571f/general_pose_tree/run_n11.py)
resumes by row number without binding previous results to the certificate and checker,
while
[`summarize_n11.py`](https://github.com/wand125/square-packing-tools/blob/0d33ab61726c2ab03e3eb8f457dabaf22db8571f/general_pose_tree/summarize_n11.py)
counts duplicate rows and does not establish the exact `0..12027` census.
A complete local replay must reject duplicate, missing, stale or mixed-source rows
before it compares minima.
The generic
[`Measure` interface](https://github.com/wand125/square-packing-tools/blob/0d33ab61726c2ab03e3eb8f457dabaf22db8571f/general_pose_tree/measure.py)
also silently converts coordinates with `int()` after checking duplicates; strict
exact-integer validation is needed there.
The pinned Kleddamag loader asserts integer coordinates, so this conversion concern does
not invalidate the three ordinary row probes.

The
[cached-axis checker instructions](https://github.com/wand125/square-packing-tools/blob/0d33ab61726c2ab03e3eb8f457dabaf22db8571f/performance/verifiers/README.md)
require full replay with the unchanged verifier before publication.
The
[lazy zmx2 instructions](https://github.com/wand125/square-packing-tools/blob/0d33ab61726c2ab03e3eb8f457dabaf22db8571f/performance/point_verifier_lazy/README.md)
require a whole-domain census with zero uncertified or capped roots and describe their
timings as private reported measurements.
Maintain those distinctions in our synopsis: candidate search, source replay,
independent preflight, and a second complete verifier are separate evidence levels.

## Accelerated Verifiers: Static Review

The cached-axis variant preserves the canonical rectangle summation order and the
parenthesization of interval products; nonzero-direction code is unchanged.
Its adapter pins the source and runner identities and requires fresh logs.
The existing tests check activation, hashes and freshness, but do not establish compiled
output equality. Before integration, compare the canonical and cached axis checks at
tangencies and near the acceptance threshold, retain an equality receipt, and keep the
required canonical 201-angle publication replay.

The lazy point-verifier patch leaves the pair-bound endpoint calculation in place and
avoids computing endpoints only where zero line density makes the continuum term zero.
Static inspection found no mathematical change in that optimization.
Its
[`verify.py` wrapper](https://github.com/wand125/square-packing-tools/blob/0d33ab61726c2ab03e3eb8f457dabaf22db8571f/performance/point_verifier_lazy/verify.py)
needs stronger admission checks:

- The binary digest is compared with a supplied receipt, but the receipt’s source, patch
  and builder identities are not checked against the pinned build constants.
- Expected root count and reference census are optional.
  An empty root log passes the universal zero-uncertified/zero-capped check, so the
  wrapper does not independently establish a positive complete census.
- Final acceptance uses Python `assert`; an optimized interpreter removes the exit,
  unchanged-input, whole-cover verdict, root-count and reference-equality assertions.

These are static findings, not an executed counterexample to a retained lazy-verifier
run. Integration should enforce the pinned build identities, a positive expected census
and exact reference agreement with explicit refusal branches, and test counterfeit
receipts, empty or incomplete logs, input mutation and optimized-Python execution.
The reported private n32/n45 timings and full censuses remain unreplayed here.
The follow-up is tracked in `think-xgjo`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
