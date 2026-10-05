---
type: is
id: is-01m3xkb16rqvby3jstb2cse70j
title: Update the n17 frontier record now that H-265 identifies S* with the catalogue polynomial
kind: task
status: open
priority: 2
version: 2
spec_path: packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-245-h265-n17-catalogue-polynomial.md
labels: []
dependencies: []
parent_id: is-01m3v9vq36ykk2jdzce75req44
created_at: 2026-10-02T06:03:03.768Z
updated_at: 2026-10-05T05:45:42.470Z
---
exp-245 accepted H-265. packing/frontier/n-017.md still says the identity with the degree-18 polynomial is not established (blocker detail near line 136; prose near lines 253, 612 and 642). Add an evidence entry for exp-245, narrow the blocker to global optimality, update the prose, and regenerate the frontier views; no bound or status change.

## Notes

2026-10-05. Delivered on PR 347 in 4c060f233: n-017.md (the blocker, the lead paragraph, the certified-endpoint section with a pointer to the explainer, the orientation sentence narrowed rather than reversed, and the degree-18 section), T-065's notes and next_rung, an annotation on E-n017-certified-endpoint, the new E-n017-catalogue-polynomial-identity (same-implementation, audited-here) and V-n17-catalogue-polynomial, with RESULTS.md, INVENTORY.md and VERIFIERS.md regenerated. The description's lines near 136, 253, 612 and 642 were 136-137, 253-254, 621-623 and 653-654, plus 634-635. Close when PR 347 merges.
