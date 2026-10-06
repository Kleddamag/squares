---
type: is
id: is-01m3p04ndehpya7g3mbmmad36g
title: "W7: implement native exact rectangle-density coverage verifier"
kind: feature
status: in_progress
priority: 1
version: 17
spec_path: docs/project/reviews/review-2026-09-29-n11-optimality.md
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m3qw8b5q2xgjp85cxx24134c
child_order_hints:
  - is-01m3q3330ehfw8jkg6n2jjkz76
  - is-01m3q333efvqtrjzbncve0efps
  - is-01m3q3yck931awc12wrdfjtc8b
  - is-01m3q9nxx8t416wr59nsvcve5z
  - is-01m3qtxksrtmt2kc5qqnxf6t97
hold: null
hold_until: null
created_at: 2026-09-29T07:12:51.117Z
updated_at: 2026-10-06T08:28:17.276Z
started_at: 2026-09-29T07:14:10.458Z
---
W7 block in docs/project/specs/active/plan-2026-09-29-native-rectangle-verification.md. Exact rational common-core polygon subdivision and axis event sweep, source-distinct from verify.cpp; library, CLI, refusal controls, proof contract review. Analytic full-net control and bounded retained input probe required before first checkpoint. Full large-certificate independent confirmation remains separate.

## Notes

2026-10-06 (bead review): think-ck07 was closed as a duplicate of this bead. Carried over from it: any conversion of rectangle densities to point masses must bound the transport error and pay it from actual coverage slack (placing rectangle mass at cell centres is unsound without that proof), and input admission must include think-c0xc's guards. Evidence: docs/project/reviews/review-2026-09-22-tokoharu-density-mathematics.md.
