---
title: Independent Review of the n17 Endpoint Feasibility Certificate
date: 2026-10-01
status: complete
---
# Independent Review of the n17 Endpoint Feasibility Certificate

[H-256](../../../../hypotheses/H-256-n17-exact-endpoint-feasibility.md) is accepted.
The exact H255 root, H254 reconstruction and fixed slider centroid give 17 unit squares
contained at the chart side with pairwise disjoint interiors.
This certifies the endpoint packing; it does not establish global optimality.

## Instrument and Output Review

Two Astra max reviews checked the centroid algebra, complete contact roster and symbolic
normalizations before target use.
A Sol implementation separates exact symbolic identities from strict rational interval
inequalities. Nine synthetic controls passed, including malformed or altered input,
missing coverage, overlapping geometry, displaced contacts and long exact fraction
serialization. Independent control replay took 25.61 seconds; Ruff and BasedPyright were
clean.
H256 records the pretarget synthetic-control scope and all instrument corrections.

The single target ran at frozen commit `f77b3e0a7fdfec83ec7a4f6068404e23d91508b7`. All
68 walls and all 136 unordered pairs occur exactly once:

| Obligation | Exact Identities | Strict Interval Inequalities | Total |
| --- | --- | --- | --- |
| Walls | 15 | 53 | 68 |
| Pairs | 21 | 115 | 136 |

Astra independently audited the complete packet.
Every strict lower bound is positive; all identity records carry zero values scoped to
the certified root. Strict bounds apply to the entire root enclosure.
The 21 pair manifests match the independently specified H254 roster plus the 2/3 corner
contact.
Symbolic completion includes all wall and pair identities, three normalizations,
basis identities and the slider relation.
The root bytes equal the published exp237 Git blob; its embedded checker receipt, source
digest, midpoint and coordinatewise inclusion bounds match the accepted record.
The raw packet is complete, with exit zero and no failed geometric clause.

The initial complete structural/sign audit took 0.919706917 seconds; selected
independent interval recalculation took 0.796323583 seconds.
The retained
[independent receipt auditor](../../../../../../packing/devtools/audit_n17_endpoint_receipt.py)
then reproduced both endpoints of all 187 intervals: 53 strict walls, 115 strict pairs,
and 19 guard, side and slider records.
Its [retained full audit](audit/independent-receipt.json) took 5.005088875 seconds;
[the exact command](audit/independent-command.txt) is retained beside it.
Eight synthetic controls cover arithmetic, malformed rational and JSON input, missing or
duplicated obligations, altered bounds, identity directions, scope and exact side
comparisons. Ruff and BasedPyright reported no findings.

The auditor imports or executes neither the endpoint producer nor the root checker.
It checks the identity manifest while relying on the accepted H255 root proof and the
separately reviewed analytic contact identities; it does not independently reprove those
identities. This is an independent full interval audit with explicit premises.

An exact Fraction comparison also places the entire endpoint side enclosure strictly
below the retained rational upper bound $4675530093604551/10^{15}$. Directed decimal
rounding gives $S_\ast\in[4.6755300936045509516340076871127879,
4.6755300936045509516342148538535054]$. This removes the rational witness’s relaxation;
it does not claim a new packing discovery or establish an identity with the catalogue’s
degree-18 polynomial.

The minimum reported strict wall clearance is 10/top, about 0.5832845047. The minimum
strict pair clearance is 11/13, about 0.0237377432. The 14/16 separator uses the forward
$q$ direction, with lower bound about 0.0394691039. These rounded values explain the
margins; acceptance uses the exact fractions in the immutable receipt.

## Cost and Limits

The raw command took 43.45 seconds wall, 33.16 user and 0.90 system, with 116,228,096
bytes maximum resident memory.
The receipt is 4,717,067 bytes.
A 180-second timeout and 10 MiB file ceiling were enforced.
The optional data-segment cap was unavailable and is explicitly recorded.
Host load was 77.88 on 10 cores with zero CPU idle; other tasks were left running.
This single contended run is not a language or library benchmark.

| Internal Phase | Seconds | What It Includes |
| --- | --- | --- |
| Root checker | 0.02135 | Rechecking the accepted fixed root certificate |
| Symbolic identities | 25.79694 | Exact rational-function cancellation and normalization |
| Interval geometry | 16.41939 | Rational arithmetic and conversion of exact bounds to decimal strings |
| Other measured orchestration | 0.04173 | Work inside the instrument outside those phases |
| Instrument total | 42.27940 | Measured before final JSON output and process exit |

The internal timing does not separately measure interval arithmetic and integer-to-text
conversion. Wall/pair bound strings account for 94.8% of the receipt; all bound literals
account for 99.1%. The longest pair record, 14/16, has 81,106 characters of bounds.
W5 bead `think-4krl` records this measured cost.
Caching repeated support values would preserve the exact intervals; a future fixed
dyadic outward-rounding contract could control denominator and receipt growth.
Neither optimization was applied to this run, and neither has a measured speedup.
The original evidence remains unchanged.

## Mathematical Consequence

The root is now an attained minimum of the declared necessary orientation,
contact-branch and parameter class, by the separately reviewed conditional minimum
theorem. The
[analytic slider proof](../../../../../../docs/project/reviews/review-2026-10-01-post-optimality-w3-opening.md#endpoint-slider-geometry)
extends the centroid construction to its entire nondegenerate closed triangle, with area
$T^2/(2s)>0$. This is a two-parameter family; it is not a claim that these are all its
degrees of freedom. H256 itself tested the fixed centroid.

The
[projection-branch review](../../../../../../docs/project/reviews/review-2026-10-01-n17-projection-branches.md)
relaxes several orientation premises using universal support inequalities.
Capture of all split orientations and separating branches, configurations outside the
parameter box, and global coverage remain open.
The same interval/support mathematics underlies the implementations and reviews; no
proof-assistant or method-distinct confirmation is claimed.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
