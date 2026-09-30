---
type: is
id: is-01m3qyb4p2myhwtvzke03640gd
title: Check exact n11 exclusion census and conditional transfers
kind: task
status: in_progress
priority: 1
version: 6
spec_path: docs/project/reviews/review-2026-09-29-n11-optimality-census-contract.md
delegate: codex-sol-census
labels:
  - n11
dependencies:
  - type: blocks
    target: is-01m3qzjv5qsxp9kakp2f34dbqj
parent_id: is-01m3qw8b5q2xgjp85cxx24134c
child_order_hints:
  - is-01m3qzjv5qsxp9kakp2f34dbqj
  - is-01m3r0r4v4kfdhcqxh22pt17dn
created_at: 2026-09-30T01:19:55.061Z
updated_at: 2026-09-30T02:01:58.371Z
---
Implement the bounded case-census slice in the linked contract for pinned 11SquaresOptimal f9e0de7. Acquire only the five specified metadata objects (100,541 declared compressed bytes), independently enumerate the 2184 half-turn masks, and check exact 1931/76/173 family sets, job assignments, disjointness and four-case complement. Retain source/input identities, wall and CPU costs, complete ID census, and mutation refusals. PASS_CASE_CENSUS_ONLY must keep geometric exclusions and global optimality unchecked. Subsequent conditional-transfer acceptance must recompute support containment and strict checked-threshold sums for all 59 field packets, plus the 34 generic single-case transfers, rather than trust stored case lists. No broad repository tests or full proof-data acquisition.

## Notes

2026-09-30 independent A1-A5 census complete: checker b7b9fd05ff6cd9894bc272243a032039ebc2ddd79da2c754dd5c2c5b31300cdc, result 98dad8545582694ca6217fce113f49b33d29537ea128c3994c101e75f5b57efb in packing/resources/web/n11-optimality-2026-09-29/receipts/case-census/. PASS_CASE_CENSUS_ONLY; 1931 baseline +76 extensions +173 returned, exact four survivors; geometry/global false. 11 focused tests, Ruff/format and BasedPyright clean; wall 0.044s CPU 0.043s. Follow-on single field geometry child think-fi4w.
