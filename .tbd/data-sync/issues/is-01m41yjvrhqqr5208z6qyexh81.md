---
type: is
id: is-01m41yjvrhqqr5208z6qyexh81
title: Review the streamed kernel verifier (601bbf110) and list it in the n17 ledger
kind: task
status: open
priority: 1
version: 1
spec_path: docs/project/reviews/review-2026-10-02-n17-bulk-exclusion-design.md
labels:
  - n17
dependencies: []
parent_id: is-01m3xkd6zmq1jqwtn628h2k7zy
created_at: 2026-10-03T22:36:32.401Z
updated_at: 2026-10-03T22:36:32.401Z
---
Lane M1 changed the standing kernel verifier, packing/devtools/verify_n17_kernel_certificate.py, at 601bbf110. It now reads a node a step at a time with its own NodeStream (imports unchanged). Its facet memo is capped at 2^15 pairs, and the forbidden regions of a replaced owned hull are dropped. A node out of canonical member order, or with a repeated member, is refused. The measured peaks fell from 598 to 258 MB (W7-split) and from 792 to 208 MB (SW8). Receipts are identical in all 16 fields, collision_facet_checks 34,562,332 included. The revision is not in certified-sub-patterns.yaml, so verifications at it do not count; new admissions verify at 318c28c42's file until it is listed. Needed: an independent review of the reader's soundness (it must read exactly what json.loads reads, and refuse anything else) and of the memo bounds (pure functions of exact inputs). Then a ledger listing at 601bbf110 citing the review. Flag 2's verifier profile (scratchpad) gives its peak on a 931 MB node.
