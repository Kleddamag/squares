---
title: Independent Review of the n17 Endpoint Feature Inventory
date: 2026-10-01
status: complete
---
# Independent Review of the n17 Endpoint Feature Inventory

[H-257](../../../../hypotheses/H-257-n17-endpoint-contact-features.md) is accepted.
The exact endpoint has the complete predicted separating-axis and active-wall corner
inventory. This establishes the geometric premises of the reviewed first-order model; it
does not itself prove stationarity or optimality.

## Complete Coverage and Review

The single [raw run](run-001/certificate.json) covers every owner, local basis axis and
sign at all 21 zero-contact pairs, retaining duplicate owner labels when the base axes
coincide. It also covers all four vertices at each of the 15 active wall incidences.

| Obligation | Exact Identities at the Root | Strict Interval Bounds | Total |
| --- | --- | --- | --- |
| Owner-axis pair options | 33 | 135 negative upper bounds | 168 |
| Active-wall corner gaps | 29 | 31 positive lower bounds | 60 |
| Parallel-face tangent offsets | Nine formula identities | Nine intervals strictly inside $(-1,1)$ | 9 |

Twenty-two distinct symbolic pair identities underlie the 33 owner-labeled zero options.
The other 53 wall incidences and 115 noncontact pairs retain their accepted H256 strict
clearances. This is the 60 active-wall corner scope, not an unreported replay of all 272
wall-corner combinations.

Two Astra max reviewers checked the producer, symbolic normalizations, complete owner
roster and branch derivation.
Sol’s seven target-free controls passed, with Ruff and BasedPyright clean.
The complete symbolic control took 28.33 seconds and is declared in the measured
slow-test registry; six fast controls remain on the pull-request surface.

The separately implemented
[receipt auditor](../../../../../../packing/devtools/audit_n17_endpoint_features.py)
uses independent tuple-interval arithmetic and reconstruction.
It imports or executes neither the feature producer nor its arithmetic.
Its nine synthetic controls passed in 0.17 seconds in the coordinator’s replay, and the
coordinator reviewed the full auditor.
The [retained output audit](audit/independent-receipt.json) reproduces both exact
endpoints of all 175 interval records: 135 negative owner alternatives, 31 positive
corners and nine tangent offsets.
Caching 106 distinct negative geometry intervals preserves all 135 owner-labeled
comparisons. Every coverage, identity manifest, scope and prerequisite binding agrees.
The full audit took 11.274893291 seconds.

This independent arithmetic audit trusts the accepted H255 root and H256 packing proofs,
and the separately reviewed symbolic zero, normalization and tangent-offset identities.
It does not independently reprove those symbolic identities or claim proof-assistant
verification. The [audit command](audit/independent-command.txt) preserves the actual
invocation and its unused UV cache-path typo; direct Python did not invoke uv or use
that cache. The corrected replay command is also recorded.

## Provenance and Cost

The target ran once at commit `b34801483af0ac244b936c8e16b9993a172f62f6`, starting
13:07:40 UTC and finishing 13:08:24 UTC. Root and endpoint bytes were bound to their
accepted Git blobs. The tracked checkout was clean and assertions were enabled.
The complete packet exited zero with no failed feature clauses.

It took 41.80 seconds wall, 33.25 user and 0.92 system, with 136,216,576 bytes maximum
resident memory. The certificate is 6,198,237 bytes.
Internal symbolic work took 24.50648 seconds and interval work including fraction
serialization took 16.09253; the internal total of 40.72891 precedes final output and
process exit. The 180-second timeout and 10 MiB file ceiling held.
The optional data-segment cap was unsupported and is explicitly recorded.
Host load was 80.52 on ten cores, with zero CPU idle; this is a contended observation,
not a comparative benchmark.
No source data, root box, sliders, classification or acceptance criterion was adjusted.
The raw run remains immutable.

## Mathematical Consequence and Next Step

The
[first-order derivation](../../../../../../docs/project/reviews/review-2026-10-01-n17-first-order-branches.md)
now has its exact-root feature premises.
Nine parallel-face owner disjunctions reduce to two simultaneous inequalities each,
while the 2/3 corner retains two alternative spatial directions.
Together with the wall and nonparallel-contact rows, the complete first-order model
consists of two 59-row cones in 52 variables.
Two Astra reviewers and the coordinator independently checked that reduction.

[H-258](../../../../hypotheses/H-258-n17-common-core-stress.md) selects one explicit
common-core dual for the next round.
It must prove exact stationarity identities and nonnegative weights before ruling out
first-order descent.
Zero-side motions require higher-order or exact continuation analysis; global coverage
remains separate.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
