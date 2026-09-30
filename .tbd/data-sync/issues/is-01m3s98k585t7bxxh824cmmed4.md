---
type: is
id: is-01m3s98k585t7bxxh824cmmed4
title: Repair solved n11 consumers before final PR publication
kind: bug
status: in_progress
priority: 1
version: 5
labels: []
dependencies: []
parent_id: is-01m3qcan8g6wnnpkvaemzt7rfm
created_at: 2026-09-30T13:50:00.359Z
updated_at: 2026-09-30T14:26:23.929Z
---
Incremental push at41af4f3c1 found11 test failures and30 setup errors: algebraic lower-bound rendering, DS7 restricted parser, solved-case assertions, and atlas data pin. Parallel Sol renderer/atlas and Astra-max comparison lanes. Keep proof receipts frozen; focused tests then incremental gate and hosted CI.

## Notes

Published6c8542175 passes local delta52checks/1639tests. Hosted Pages exposed solved-mode SVG rendering bug: omitted VERIFIED_MARK leaves raw-HTML break and SVG lines render as pre/code; print overflow1446px scalesPDF to13 instead of22pages. Sol owns minimal markup fix and rendered structural regression plus focused print/PDF verification. Do not relax geometry/pagecountguards. Mathematical receipts unchanged.
