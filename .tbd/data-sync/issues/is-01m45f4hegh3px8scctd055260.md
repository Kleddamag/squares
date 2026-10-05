---
type: is
id: is-01m45f4hegh3px8scctd055260
title: "PR #350 B2 (Medium): replace the retracted 'ten times more of the tree per node' sentence with wand125's correction"
kind: task
status: open
priority: 2
version: 1
spec_path: docs/project/reviews/review-2026-10-02-n17-bulk-exclusion-design.md
labels: []
dependencies: []
parent_id: is-01m45f4dj0p0t4bsxjnxcz5whv
created_at: 2026-10-05T07:23:32.176Z
updated_at: 2026-10-05T07:23:32.176Z
---
Review B finding B2 on jlevy/squares#350 (https://github.com/jlevy/squares/pull/350#pullrequestreview-5411026984), at head 9179aab7d. Limits says the specification-only prover 'closes about ten times more of the tree per node than the existing relaxation'. wand125's comment of 2026-10-05 02:41 UTC on #350 retracts it as a search-order artefact: single-threaded at 1 M nodes the two close 2.17% and 2.05% of W7; Knuth's estimate puts the existing tree on A at about 40,000 nodes against 138,000 for the other prover. Fix: replace the sentence with the correction.
