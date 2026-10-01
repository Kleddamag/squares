---
type: is
id: is-01m3r1dp2anhxes2fesns7bhdf
title: "W5: avoid rebuilding every atlas witness for evidence-only edition changes"
kind: task
status: open
priority: 1
version: 4
spec_path: docs/project/reviews/review-2026-09-29-n11-optimality.md
labels: []
dependencies: []
parent_id: is-01m3qw8b5q2xgjp85cxx24134c
created_at: 2026-09-30T02:13:44.137Z
updated_at: 2026-10-01T10:16:40.835Z
---
Supporting integration efficiency only. Current evidence review annotation changes DATA_REVISION and requires refreshing stamped exports; existing atlas --update re-derives324 witness renderings even when geometry/composite data is unchanged. Measured245.08s wall/874.67s aggregate CPU with4 workers at8f5fff; proof lanes continued. Investigate a bounded restamp path using retained verified source, preserve identical SVG and PNG/PDF receipt contracts, retain mutation tests refusing stale or changed geometry. Do not weaken revision/data integrity or block proof checks on this optimization. Evidence packing/campaign/agent-sessions/session-164-validation/atlas-restamp-8f5fff.txt.

## Notes

2026-10-01 PR267 first restamp: October source-date and reported-record edits required DATA_REVISION update. Existing build_known_best_atlas --update regenerated 324 witnesses/house renderings with 10 default workers; observed wall about 13 minutes (last census 11:31, no start/end timer). Two composite SVGs changed only in release-stamp text; PNG/PDF receipts refreshed. 2026-10-01 PR267 origin/main merge restamp: timed existing --update --jobs 4 after data merge e05a4312: real 851.72s, user 1084.19s, sys 22.84s; again 324 witnesses/renderings rebuilt and only two SVG release-stamp lines changed, plus PNG/PDF receipts. This was host-contended, not a controlled worker-count comparison: at 03:03:19-20 PDT host had load averages 66.39/85.81/110.03, 0% CPU idle, 108 running processes on 10 cores, 31 GiB of 32 GiB RAM used, about 9.6 GiB compressed and 5.72 GiB swap. Do not attribute the delay solely to renderer design or compare 10 versus 4 workers as a benchmark. The supported restamp optimization remains follow-up work.
