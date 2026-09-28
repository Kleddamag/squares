---
type: is
id: is-01m3n5xpvba2f3jnn09bgcq9dk
title: Evaluate wand125's certificate-transfer and speed-up techniques for this repository's ladders
kind: task
status: open
priority: 2
version: 1
labels:
  - packing
  - wand125-update
  - research
dependencies: []
parent_id: is-01m3n5wh72rsqd2z97m8v1vv4q
created_at: 2026-09-28T23:34:40.235Z
updated_at: 2026-09-28T23:34:40.235Z
---
From packing/resources/web/wand125-x-update-2026-09-28/supplied-messages.txt: expanding n from a certified parent with re-optimized weights; climbing L with edge-rectangle budget recovery; exact rescaling to a nearby L; inheritance by mass; the ceiling that no certificate with core side B reaches L >= B*UB(n) (a known packing shrunk by B holds n disjoint cores), used to cap targets; parallel counterexample screening over the angle net; batched counterexample feedback; LP warm start (40-50% less solve time reported); a low-memory working LP; the lazy-intersection zmx2 variant; the Lean certificate-to-data overlay; spot-instance ladders with a 30-minute monitor. W3: state which apply to BC-394 and BC-395's ladders and the n11 and n17 generators, add idea rows or hypotheses for those worth measuring, and adopt the ceiling as a pre-run guard if it holds as stated (it bounds the certificate side, not s(n)).
