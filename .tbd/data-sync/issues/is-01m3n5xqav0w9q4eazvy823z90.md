---
type: is
id: is-01m3n5xqav0w9q4eazvy823z90
title: Compare the rectangle-density solver used by wand125 and Tokoharu with this repository's certificate tools and choose the path forward
kind: task
status: open
priority: 1
version: 1
labels:
  - packing
  - wand125-update
  - research
  - tooling
dependencies: []
parent_id: is-01m3n5wh72rsqd2z97m8v1vv4q
created_at: 2026-09-28T23:34:40.731Z
updated_at: 2026-09-28T23:34:40.731Z
---
Owner request, 2026-09-28. Subjects: tokoharu/square-packing-density-bounds (solver, push.py driver, verify.cpp, reviewed 2026-09-22 in review-2026-09-22-tokoharu-density-mathematics.md), wand125/square-packing-density-bounds (the fork, with the drivers and speed-ups in packing/resources/web/wand125-x-update-2026-09-28/supplied-messages.txt) and the mixed Green-style search behind mixed_n50_L740, against this repository's weighted-certificate generators, exact and interval verifiers, native parent-core interval route and sqsearch engine. Produce a capability matrix: certificate languages (points, thresholds, winning subsets, rectangle densities, mixed), trust boundary and margins, cost per certified rung, reach across n <= 100 and beyond, automation, licence. Decide: adopt or vendor the external solver, wrap it behind this repository's preflight and replay, port its densities into the native route (which would also give C4 on rectangle certificates), or leave generation to the community and specialise in verification. Output: a review document and one selected next entry; Fable at max for the mathematical comparison per OR-2.
