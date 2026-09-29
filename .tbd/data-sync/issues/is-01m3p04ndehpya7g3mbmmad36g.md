---
type: is
id: is-01m3p04ndehpya7g3mbmmad36g
title: "W7: implement native exact rectangle-density coverage verifier"
kind: feature
status: in_progress
priority: 1
version: 4
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m3nzy6gqfv60whzzvww0ffa0
hold: null
hold_until: null
created_at: 2026-09-29T07:12:51.117Z
updated_at: 2026-09-29T07:39:19.333Z
started_at: 2026-09-29T07:14:10.458Z
---
W7 block in docs/project/specs/active/plan-2026-09-29-native-rectangle-verification.md. Exact rational common-core polygon subdivision and axis event sweep, source-distinct from verify.cpp; library, CLI, refusal controls, proof contract review. Analytic full-net control and bounded retained input probe required before first checkpoint. Full large-certificate independent confirmation remains separate.

## Notes

Initial native checker and admission controls implemented, independently reviewed,9focused tests pass. All201 directions verified on analytic n3 control; retained n11 angle1 at100nodes is inconclusive (46accepted leaves,9pending boxes). Next falsifiable comparison: replace/supplement common-core term for each expanded rectangle R by rho_R times minimum exact overlap area at FOUR center-box corners, then sum. Quasiconcavity follows from convexity of R and core plus planar Brunn-Minkowski; termwise bound dominates common-core. Never use minimum of total density over corners. Cache per-rectangle corner areas; compare same100-node n11 probe and analytic/refusal controls. Current receipt has no box coordinates, so9pending DFS boxes are not9proven difficult cells. Full retained-certificate completion remains open.
