---
type: is
id: is-01m3r1dp2anhxes2fesns7bhdf
title: "W5: avoid rebuilding every atlas witness for evidence-only edition changes"
kind: task
status: open
priority: 1
version: 3
spec_path: docs/project/reviews/review-2026-09-29-n11-optimality.md
labels: []
dependencies: []
parent_id: is-01m3qw8b5q2xgjp85cxx24134c
created_at: 2026-09-30T02:13:44.137Z
updated_at: 2026-10-01T10:08:05.344Z
---
Supporting integration efficiency only. Current evidence review annotation changes DATA_REVISION and requires refreshing stamped exports; existing atlas --update re-derives324 witness renderings even when geometry/composite data is unchanged. Measured245.08s wall/874.67s aggregate CPU with4 workers at8f5fff; proof lanes continued. Investigate a bounded restamp path using retained verified source, preserve identical SVG and PNG/PDF receipt contracts, retain mutation tests refusing stale or changed geometry. Do not weaken revision/data integrity or block proof checks on this optimization. Evidence packing/campaign/agent-sessions/session-164-validation/atlas-restamp-8f5fff.txt.

## Notes

2026-10-01 PR267 occurrence: October source date and reported-record edits required a DATA_REVISION restamp. The existing build_known_best_atlas --update regenerated 324 witnesses and house renderings with 10 default workers; observed wall time was about 13 minutes (last process census 11:31, no start/end timer). The two composite SVGs changed only in release-stamp text; exported PNG/PDF receipts were refreshed. This corroborates the metadata-only restamp cost; optimization remains follow-up work.
