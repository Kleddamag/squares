---
type: is
id: is-01m3qzjv5qsxp9kakp2f34dbqj
title: Independently check smallest n11 field-certificate geometry
kind: task
status: open
priority: 1
version: 3
spec_path: docs/project/reviews/review-2026-09-29-n11-optimality-census-contract.md
delegate: codex-sol-geometry
labels:
  - n11
dependencies:
  - type: blocks
    target: is-01m3r0r4v4kfdhcqxh22pt17dn
parent_id: is-01m3qyb4p2myhwtvzke03640gd
created_at: 2026-09-30T01:41:36.054Z
updated_at: 2026-09-30T02:01:58.371Z
---
Use pinned 11SquaresOptimal f9e0de7 source to audit one smallest field-certificate packet (mask 0, 459 reported transfers) under a bounded profile and exact acceptance contract. Acquire only minimal pinned source objects, independently recompute rational feature/owner/support/threshold checks, retain source hashes, complete row and transfer census, limits and mutation refusals. One packet is a conditional geometric sample, not verification of all 59 field certificates or global optimality. No full proof replay or unrelated broad tests.

## Notes

2026-09-30 one-packet mask0 independent geometry complete: checker 75fc0238f2ac91af9dc9cf57bd00792343dcf3321c395adddebf0f3465113ce5, result 821274111e6eb50d47e20882da083e3e23d25ee37e6725a18b18d133ab798663 in packing/resources/web/n11-optimality-2026-09-29/receipts/field-mask0/. Strict 55 owner points (34 disk/21 wall), exact arrangement cover of 136 rows (67+69), 453 direct and 459 whole-half-turn transfers match A1. 16.515s wall/16.458s CPU, 27,544 work units under 30s/100k. Astra mathematical review approved this single field packet; 58 other field,34 generic,76 prior extension,173 returned geometries and global optimality unverified. 7 focused tests, Ruff/format and BasedPyright clean.
