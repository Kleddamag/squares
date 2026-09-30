---
type: is
id: is-01m3r0r4v4kfdhcqxh22pt17dn
title: Independently verify n11 mask-202 field geometry
kind: task
status: open
priority: 1
version: 1
spec_path: docs/project/reviews/review-2026-09-29-n11-optimality-census-contract.md
delegate: codex-sol-geometry
labels:
  - n11
dependencies: []
parent_id: is-01m3qyb4p2myhwtvzke03640gd
created_at: 2026-09-30T02:01:58.371Z
updated_at: 2026-09-30T02:01:58.371Z
---
At pinned 11SquaresOptimal f9e0de7, inspect and independently verify the mask-202 field certificate and exact row proposals with a new generalized consumer, preserving frozen mask-0 checker/receipt. Mask202 lists 764 cases, 653 outside validated mask0, but IDs alone prove nothing. Profile one owner and row before a single <=30s full run; verify all required owner points, exact angle coverage/row geometry, canonical transfer equality, source bindings and negative controls. Retain result/provenance and never claim global optimality or other certificate families.
