---
type: is
id: is-01m4518aryrdsvpv95dqhqe3z3
title: "Independent check of ValidTilt9 for T-081: wand125's box-9 run, or sqverify_fast Milestone C (#316)"
kind: task
status: open
priority: 2
version: 1
labels:
  - result-import
  - packing
dependencies: []
parent_id: is-01m44qz0rxvkakmyqaj7qdgagv
created_at: 2026-10-05T03:20:56.349Z
updated_at: 2026-10-05T03:20:56.349Z
---
This bead owns the ask queued on jlevy/squares#316, which is evand's s(k^2 - 4) = k for every k >= 5, T-081. The ask is for an independent check of ValidTilt9, the tilted box-9 premise that qx2_zm.py certifies over 16,200 D4 roots, made by wand125's Valid7 checker on box 9 or another way. The ask in packing/campaign/result-requests.yaml names this bead as its `bead`. The answer bead for #316 is think-4uir, which owns the reply.

## State on 2026-10-05

- On evand/square-packing#1, at 2026-10-03T23:14:54Z, wand125 said that, following #316, they are running valid7-independent-check on the box-9 cover and will report the result on #316. Nothing has been reported on #316 yet.
- The other route is this repository's clean-room verifier, sqverify_fast. Its continuous-angle Milestone C (docs/project/specs/active/plan-2026-10-03-measure-verifier-milestone-c.md, under think-gpe0) is planned, not built.

## Claim map (stage 1, for when wand125 reports)

- The claim: a second exact decision of ValidTilt9 for evand's box-9 measure, written independently of qx2_zm.py.
- Register action: a new evidence entry on T-081 that gives an independent-implementation route beside the qx2 replay. Not a new register entry.
- Retain the repository at the revision that reports the run, and its release records by digest. Read its READ_LOG for independence.
- Price the replay from the source's recorded CPU time. Valid7's replay took about 206 worker-hours here, so this one needs a budget the owner sets.
