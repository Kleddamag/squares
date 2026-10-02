---
type: is
id: is-01m3xjxbdp7kkn4zemtj04cbwz
title: "W7: a derived regularized-view layer for the atlas, with a legend that says light can mean loose"
kind: feature
status: open
priority: 3
version: 3
labels:
  - research
dependencies: []
parent_id: is-01m3xgkna3m3w1w50ky6gqyxyk
created_at: 2026-10-02T05:55:35.478Z
updated_at: 2026-10-02T07:27:33.867Z
---
From X-049 (think-31v0, think-ea3f). The prototype devtools.regularize_axis_components produces exact derived views (verified twice over Q at the certificate's side) that cut the atlas's light green squares at the six named cases from 545 to 242 under the house rule, with no change of side. The census lists 2,453 regularizable squares in 54 records. Build it as a layer, never a witness change: a regularized pose per decimal record under its own directory, a manifest field naming it, a --check comparing digests (outside the fast gate: about 20-40 serial minutes), and a workbench/atlas toggle drawing it with a 'regularized' badge. Prerequisites named by the lane: a neighbour non-regression rule (at 206 two near-axis squares lost a contact when a neighbour moved), a separate colour class for squares tilted by hundredths of a degree instead of straightening them, and a decision for algebraic-field witnesses (same algorithm in Q(alpha), not prototyped) and interval-enclosure witnesses (no exact lattice statement). Also: the atlas legend says shade = full-side contacts but not that a light square can be loose optimizer output rather than short of neighbours; add one sentence.

## Notes

2026-10-02 session-168: layer built and pushed (PR 305, 22bfdb843). Done: non-regression rule (house and stage), --update-atlas/--check-atlas/--verify-atlas, 51 records regularized (all 50 packets + n=26), 89 Kingbird refused (promotion-overlap at dilation 1) and n=69 (decimal corners), atlas light green 7,725 -> 5,475 with none lighter; --check-atlas in the records tier; workbench stage legend row and homepage ATLAS_SHADE_KEY sentence. Remaining: (1) homepage House/Regularized toggle per the design note (renderings under atlas/known-best/regularized/rendering/, a third tile template with a badge, atlas-grid.js swap with ?layer=, tests in test_overview.py, test_site_atlas_views.py, measure_atlas_views) -- needs a host whose Playwright build matches the pin; (2) wire --verify-atlas (~313 s) into a deferred checkpoint and document it in development.md's validation table; (3) decide whether a view may use the smallest verifying dilation, which would open the 89 Kingbird records.
