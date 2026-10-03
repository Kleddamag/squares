---
type: is
id: is-01m4055fqdnsc95js0egq5sc1t
title: Repo-wide integrity-ceremony audit and removal plan (lane R7)
kind: task
status: open
priority: 0
version: 1
spec_path: docs/project/reviews/review-2026-10-02-n17-bulk-exclusion-design.md
labels: []
dependencies: []
parent_id: is-01m3xkd6zmq1jqwtn628h2k7zy
created_at: 2026-10-03T05:53:05.260Z
updated_at: 2026-10-03T05:53:05.260Z
---
Owner direction 2026-10-03: 'needless ceremony around things like this is a constant tax on all development and progress'; 'we are not validating across a trust boundary... worrying about correctness'; 'determinism should not cost rerunning code'. R7 inventories every hash/digest comparison of repository-owned files, frozen-blob/frozen-copy comparison, digest-gated refusal (checkpoints, receipts, caches), forced re-run and internal signing; verdict KEEP (named trust boundary) / REPLACE (Git revision, small determinism test, semantic comparison) / REMOVE; ranked implementable slices; proposed OR-16 amendment. Known n17 instances: MODULE_SHA256, digest-named certificates with name checks, ledger verifier digests and receipt_sha256, tool/kernel_sha256, capture load_checkpoint refusing after a byte-identical kernel speedup (forced a 256-row restart). Deliverable: docs/project/reviews/review-2026-10-03-integrity-ceremony-audit.md.
