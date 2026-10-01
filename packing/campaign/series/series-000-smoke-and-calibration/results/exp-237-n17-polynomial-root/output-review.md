---
title: Independent Review of the n17 Exact Root Certificate
date: 2026-10-01
status: complete
---
# Independent Review of the n17 Exact Root Certificate

The [H-255 criterion](../../../../hypotheses/H-255-n17-exact-polynomial-root.md) fixes
two integer polynomials, the retained rational source midpoint and radius $10^{-12}$.
The [experiment](../../experiments/exp-237-h255-n17-polynomial-root.md) asks only for
root existence and uniqueness in that box.
It does not ask a numerical root finder to choose a promising box after seeing the
target.

## Instrument Review

Sol implemented the producer.
Astra max independently implemented the checker, without reading or importing the
producer’s arithmetic.
A second Astra max reviewed both against the polynomial reduction, the contraction
theorem and the fixed domain.
The two implementations share a mathematical method, not arithmetic implementation.
This is not method-distinct confirmation or proof-assistant verification.

The independent reviewer checked the exact midpoint inverse in both multiplication
orders, signed interval products and powers, polynomial derivatives, the interval
Jacobian, the contraction matrix, row norms, absolute correction and strict inclusion.
The fixed coefficient maps have 12 and 19 terms.
Independent literal expansions agree.
Both side guards and the positive normalizations back to the contact equations were
reviewed.
Thirteen synthetic controls passed, including a certificate passed through JSON
serialization to the separate checker, and malformed or altered inputs that must be
refused. Ruff and BasedPyright found no issues.

The hand-derived control initially contained a transcription error in one inverse entry.
Sol identified it through the inverse identity; both Astra reviewers confirmed the
correction before target use.
H-255 retains the erratum and the incorrect matrix as a negative control.
The review also corrected two schema/provenance mismatches and added malformed-JSON
refusals before the target.
No target criterion changed.

## Retained Run

The run used frozen commit `b3e5e1526e74421032dc2f5b79c243712fdd7b61` at
11:55:01–11:55:03 UTC. Tracked files matched that commit; the newly created evidence
directory was the only untracked path.
Both commands returned zero.
The producer took 0.67 seconds wall, 0.41 user and 0.19 system, with 74,727,424 bytes
maximum resident memory.
The checker took 0.09 seconds wall, 0.07 user and 0.01 system, with 26,329,088 bytes
maximum resident memory.
Certificate and checker output sizes are 45,159 and 4,809 bytes.

The exact fractions in [certificate.json](run-001/certificate.json) and
[checker.json](run-001/checker.json) summarize to a contraction norm of about
$6.52534613777464\times10^{-11}$ and inclusion bounds of about
$9.85923078412898\times10^{-24}$ and $6.525346137774639\times10^{-23}$. These are below
the frozen strict bounds of 1 and $10^{-12}$ respectively.
Decimals here are explanatory; all acceptance comparisons use exact fractions.

Timeouts of 90 seconds per command and a 10 MiB output ceiling were enforced.
The optional data-segment memory cap was unavailable on this host and is explicitly
recorded. Host load was 23.66 on 10 cores with 0.39% CPU idle.
These single-run costs include contention and are not a controlled language or library
benchmark.

## Output Review and Scope

Astra max independently reviewed all ten raw files, fixed source bytes and label map,
source midpoint, radius and tracked-clean provenance.
It reconstructed both inverse identities, every contraction-matrix endpoint, row norm,
signed correction, inclusion bound and all eight domain intervals from the retained
exact values, and checked the separate receipt for equality.
The instruments still matched the frozen commit.
This retained-output arithmetic audit took 0.027525583 seconds; it did not rerun either
target command. No blocking discrepancy was found.
The coordinator accepts H-255 at its stated root-existence scope.

The accepted root discharges the existence premise of the
[conditional box-minimum theorem](../../../../../../docs/project/reviews/review-2026-10-01-post-optimality-w3-opening.md#conditional-minimum-in-the-frozen-parameter-box).
That theorem concerns the declared necessary inequalities and orientation/branch
premises. Endpoint packing feasibility, joint slider domains and capture of arbitrary
nearby or global packings remain separate obligations.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
