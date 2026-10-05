---
type: is
id: is-01m45f3q24s4j810mkkrpmtdfq
title: "PR #360 B3 (Low): J72 called 'independently certified'; it is a fixed-sample, freshly replayed result"
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m45f3gxdbms4wekyer6s1j9e
created_at: 2026-10-05T07:23:05.156Z
updated_at: 2026-10-05T07:23:05.156Z
---
Review B finding B3 on jlevy/squares#360 (https://github.com/jlevy/squares/pull/360#pullrequestreview-5411026851), at head 451154f60. X048-session-178-full-core-ablation/README.md:16 calls J72 'independently certified'. J72 is a fixed-sample result; its 'independent replay' re-runs the same predicate code in a fresh process. Fix: 'freshly replayed' and 'fixed-sample result', not 'certified'. See #355 B4.
