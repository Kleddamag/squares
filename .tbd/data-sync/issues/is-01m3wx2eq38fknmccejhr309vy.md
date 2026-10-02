---
type: is
id: is-01m3wx2eq38fknmccejhr309vy
title: "Import ledger: a typed link from a register entry to the issue that asked for it, an answered date, and a generated view of every import and its stage"
kind: feature
status: open
priority: 1
version: 1
labels:
  - packing
  - result-import
dependencies: []
parent_id: is-01m3nrt5zy2g6dpegq1fbczpzg
created_at: 2026-10-01T23:33:54.018Z
updated_at: 2026-10-01T23:33:54.018Z
---
W7. No field links a result to its request and nothing records that an author was answered: issue 170 has no reference anywhere in the repository and was never answered; issue 256 was registered as T-062/T-063 without a reply. Add an optional request block to a register entry (issue, answered), and devtools.import_ledger to render one row per result by others: status, next move, issue, answered. Offline and deterministic; reading GitHub is a separate dated step.
