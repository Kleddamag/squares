---
type: is
id: is-01m3q3330ehfw8jkg6n2jjkz76
title: "W7: retain rectangle frontier and compare exact corner bounds"
kind: task
status: in_progress
priority: 1
version: 4
labels: []
dependencies:
  - type: blocks
    target: is-01m3q333efvqtrjzbncve0efps
parent_id: is-01m3p04ndehpya7g3mbmmad36g
created_at: 2026-09-29T17:23:39.650Z
updated_at: 2026-09-29T17:40:36.305Z
---
Implement bounded exact pending-box diagnostics without trusted resume, per-rectangle corner-minimum bound and independent analytic controls. Compare the same retained n11 frontier under a 30-second ceiling; acceptance requires at least one formerly unresolved box certified without weakening threshold or admission. Sol implementation and Astra-max mathematical review.

## Notes

Implementation and independent Astra-max review complete;21 native/golden tests pass. Same nine exact pending boxes compared in1.420s;corner>=common all9,strictgain3,newthresholdcrossings0. Frozen usefulness criterion NOT MET. Four queued boxes already old-bound sufficient; all gains among those. Parent complete-external gap remains. Integration/CI pending.
