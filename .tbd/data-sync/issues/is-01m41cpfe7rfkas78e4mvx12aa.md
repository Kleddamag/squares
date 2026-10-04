---
type: is
id: is-01m41cpfe7rfkas78e4mvx12aa
title: "PR 315: the push gate's failures (results-table widths, release pin)"
kind: task
status: open
priority: 2
version: 7
labels: []
dependencies: []
parent_id: is-01m41amwkn2j6r6jh6de7as7fb
created_at: 2026-10-03T17:23:56.487Z
updated_at: 2026-10-04T02:18:42.167Z
---
packing-validate --push at 6f6113111: test_site_result_columns (long case list wraps; table scrolls no further than its floors at 1024 and 768) fails, since the status cell's successor list widens the column; test_release pin needs re-pinning after the last data commit.

## Notes

State 2026-10-04 02:20 UTC: jlevy/squares#315 at 833a5117f is ready to merge: 29 checks pass, 28 skipped by design; mergeable and clean, and merges cleanly into main at fa5133b49. Reviewed (think-rf21) and its fixes checked (think-wizo). Waiting on the owner's merge.
