---
type: is
id: is-01m41cpfe7rfkas78e4mvx12aa
title: "PR 315: the push gate's failures (results-table widths, release pin)"
kind: task
status: open
priority: 2
version: 6
labels: []
dependencies: []
parent_id: is-01m41amwkn2j6r6jh6de7as7fb
created_at: 2026-10-03T17:23:56.487Z
updated_at: 2026-10-04T01:03:49.807Z
---
packing-validate --push at 6f6113111: test_site_result_columns (long case list wraps; table scrolls no further than its floors at 1024 and 768) fails, since the status cell's successor list widens the column; test_release pin needs re-pinning after the last data commit.

## Notes

State 2026-10-04 00:55 UTC: in jlevy/squares#315 at 6c5036895, merged with main at d303e9ef8 and re-pinned; hosted CI running on the head (green at 03833707a); local push gate passes but for the two sandbox-only tests. Reviewed by a strong-tier agent (think-rf21). Closes when #315 merges.
