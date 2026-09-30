---
type: is
id: is-01m3qw1d6z2hnprytp2r49qe4f
title: Build a dedicated n11 proof explainer paper with demonstrations and visualizations
kind: feature
status: open
priority: 2
version: 4
spec_path: docs/project/reviews/review-2026-09-29-n11-optimality.md
labels:
  - n11
  - explainer
dependencies: []
parent_id: is-01m3qw8b5q2xgjp85cxx24134c
created_at: 2026-09-30T00:39:38.973Z
updated_at: 2026-09-30T01:10:22.812Z
---
Create a separate explainer paper specifically for n=11, using the existing explainer paper as the reference for visual style, typography, exposition, mathematical layout and figure quality. Review the existing explainer infrastructure (including packing/devtools/templates/explainer-article.md) and the earlier docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md for reusable work without inheriting an unsupported claim or starting a duplicate implementation. User explicitly requires no drafting, design or figure implementation until think-uz2x closes after completed proof validation and a recorded simplification/streamlining effort. Explain the precise validated theorem from first principles; demonstrate its geometric certificate, local coverage argument and global counting contradiction; visualize the essential geometry and explain the role and limits of computational verification. Bind demonstrations and figures to validated inputs and reproducible tools. Clearly separate intuition from proof, exact facts from illustrative pictures, and the global bound from any independent row-equality or rectangle-verification claims. Include a readable chain of lemmas, assumptions, proof dependencies, source credit, verification commands and limitations. Acceptance: a coherent standalone n11 paper in the established style, reproducible figures/demonstrations checked against the frozen simplified proof, independent Astra-max mathematical review and editorial/visual review. Preserve the existing general explainer as a separate paper. No work begins merely because software CI is green; the explicit proof-and-simplification prerequisite must be satisfied.

## Notes

User clarification: intended paper is for the global n=11 optimality proof T-060, after independent validation and simplification. Existing lower-bound confirmation does not unlock this task. Keep blocked on think-uz2x; no exposition or figure drafting yet.
