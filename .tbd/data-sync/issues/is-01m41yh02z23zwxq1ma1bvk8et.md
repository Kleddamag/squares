---
type: is
id: is-01m41yh02z23zwxq1ma1bvk8et
title: Run linear-control n82 (and n83 if missing) so T-076/T-073 carry a refused mutated control, as T-080 does
kind: task
status: open
priority: 3
version: 1
labels:
  - records
dependencies: []
created_at: 2026-10-03T22:35:31.295Z
updated_at: 2026-10-03T22:35:31.295Z
---
The complete replays of the linear n82 and n83 certificates are recorded (#327), but main holds no control.json for n82 or n83 (T-080's n101 has one). Run devtools.audit_wand125_linear linear-control n82 and n83 and record them; corrected the #294 closing note in place on 2026-10-03 21:40 (it had claimed a refused control for n82).
