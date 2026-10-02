---
type: is
id: is-01m3wx2dnc4m8yx4j5kbn9qxrd
title: "check_source_coverage: fail when a source key cited by a register entry or its evidence has no coverage entry; backfill the two missing"
kind: task
status: open
priority: 2
version: 1
labels:
  - packing
  - result-import
dependencies: []
parent_id: is-01m3nrt5zy2g6dpegq1fbczpzg
created_at: 2026-10-01T23:33:52.939Z
updated_at: 2026-10-01T23:33:52.939Z
---
W7. Found by the result import process review (docs/project/reviews/review-2026-10-01-result-import-process.md). check_source_coverage never reads the register or bibliography, so [wand125 rectangle bounds 2026-09-28] (T-046) and [wand125 tools 2026] (T-058, T-059) have no coverage entry and the gate passes. Add the check with a negative control, and add the two entries.
