---
title: Plan for Proof-Linked n11 Optimality Illustrations
date: 2026-09-30
status: draft
---
# Plan for Proof-Linked n11 Optimality Illustrations

**Bead:** `think-yc42` under `think-75cp`\
**Scope:** The published T-060 explainer and its HTML, Markdown, and PDF editions.

## Overview

The [earlier explainer](../../../../packing/devtools/templates/explainer-article.md)
lets a reader manipulate a square and see covered mass, then shows the finite-angle
reduction and its cost.
Its screen controls teach a specific mechanism; captions and static figures carry the
argument into print.
The [T-060 paper](../../../../packing/devtools/templates/n11-optimality-article.md)
currently has four source-bound SVGs: the exact-construction witness, sixteen Voronoi
cells, case-438 mask, and capture ancestry.
Those drawings establish the objects and the proof’s structure, but do not yet show
*why* a center cell has capacity one, how a pose row is eliminated or retained, how
charge excludes a mask, or why the local inequality rules out nonzero motion.

The next visuals should answer those questions at the point where the paper asks them.
They explain accepted computations; rendered pixels, user gestures, and rounded numbers
never become proof premises.

## Goals and Boundaries

- Tie each displayed datum to a retained exact input or accepted checker result, or
  label the figure as a schematic of a stated lemma.
- Give each screen interaction a legible static state and a caption that survives in
  Markdown and PDF. Keyboard, touch, and reduced-motion behavior belong in the same
  implementation slice as the interaction.
- Keep the existing witness and cover/mask figures.
  Add mechanism where those figures leave a reader to infer a proof step from a picture
  of its inputs.
- Keep the old point-certificate prover separate: its mass-atoms and direction-net
  controls do not verify T-060’s case-conditioned geometry.

No visualization will rerun the 2,180 exclusions, animate an arbitrary packing as if
every frame were certified, or suggest global uniqueness of optimal packings.
A projection of the 33-dimensional local rectangle will be identified as a projection,
not as the isolation theorem.

## Visual Map

| Priority and reader question | Figure or interaction; print state | Exact source and reusable part | Acceptance risk |
| --- | --- | --- | --- |
| **P0 — Why can a cell hold only one center?** | Extend Figure 2 with one selected cell, its physical diameter bound, and two hypothetical centers. An optional cell selector highlights a retained cell; print shows the cell with the narrowest checked margin. | Sixteen rational polygons bound by the [D4 receipt](../../../../packing/resources/web/n11-optimality-2026-09-29/receipts/d4-independent/result.json) and the independent [cell checker](../../../../packing/devtools/check_n11_optimality_d4.py). Reuse the current cell SVG coordinates and labels. | Compare the exact squared diameter with $1/(U-1)^2$; keep boundary ties closed. Displayed center points are hypothetical, not a packing or a measured minimum. |
| **P0 — How does an owner update preserve every possible pose?** | Four aligned panels for one accepted row: admitted center domain and whole angle interval; square-relative strict core and a partner’s owned hull; the reconstructed closed $K+(-Q)$ forbidden center region; residual cover and the row’s contribution to a complete ownership update. A step control may reveal panels in order. Print contains all four panels. | Use generic case 2095, step 1, owner 10, row 17 from its [accepted full result](../../../../packing/resources/web/n11-optimality-2026-09-29/receipts/generic-mask2095-intake/full-result.json), source-bound by the [generic fresh checker](../../../../packing/devtools/check_n11_generic_fresh.py). The row has one triangular residual; its checker reconstructs owned-hull obstacles rather than copying proposed collision polygons. Reuse exact polygon-to-SVG and accessible labels. | Bind the row, accepted predecessor, and complete successor. Keep center positions distinct from core offsets, and show the whole closed interval, not a sampled angle. Strict interiors justify rejecting the forbidden boundary. Cover the independently established legal domain, including residual segments and points. Ownership promotion waits for every row of the complete closed angular cover, common-core and compression checks; one row supplies only a contribution. This is a noncandidate case, not case-438 capture. |
| **P1 — Why can a field charge exclude many masks?** | A small two-core median-projection example, paired with a set diagram for required-owner membership and the strict sum $\sum q_i>b$. A selector can switch between a qualifying and a nonqualifying retained mask; print fixes one checked qualifying example and one counterexample to the transfer rule. | [Field checker](../../../../packing/devtools/check_n11_optimality_field_mask0.py), [field receipt](../../../../packing/resources/web/n11-optimality-2026-09-29/receipts/shared-field-mask0/summary.json), and [exclusion inventory](../../../../packing/resources/web/n11-optimality-2026-09-29/receipts/exclusion-inventory.json). Reuse the current mask cell IDs and highlight style, not the older article’s atom canvas. | Charge is median *projection* support, not “three sites inside a core.” Required owners and strict budget must be checked for every mask shown; equality is not an exclusion. A two-core drawing illustrates capacity one, not all 1,904 field cases. |
| **P1 — Why do four surviving masks reduce to case 438?** | A single point’s four reflected/rotated views over the current cell map, with label sets and one strict distance ban; print uses a four-view strip plus a short statement of exhaustive search. | [D4 checker](../../../../packing/devtools/check_n11_optimality_d4.py) and [accepted D4 result](../../../../packing/resources/web/n11-optimality-2026-09-29/receipts/d4-independent/result.json). Reuse the cover SVG; derive overlay regions from the retained rational object. | An irregular cell need not rotate into one cell. Retain shared boundaries, including eight singleton overlay regions, and distinguish an illustrative ban from the exhaustive 220-region/1,572-ban search. |
| **P1 — How do the four capture leaves cover every possibility?** | Annotate Figure 3’s edges with the exact closed $y_{15}$, $t_{13}$, and $t_2$ cuts. Selecting a leaf highlights its assumptions and accepted outcome; print shows all four leaf predicates and the ten-node ancestry together. | [Source graph](../../../../packing/resources/web/n11-optimality-2026-09-29/receipts/source-graph/result.json), [child-state checker](../../../../packing/devtools/check_n11_capture_child_node.py), and [pose-inclusion result](../../../../packing/resources/web/n11-optimality-2026-09-29/receipts/pose-inclusion/result.json). Reuse the current tree layout and node labels. | Both sides include equality; no endpoint is lost. Edges are proof dependencies, not square trajectories. The near leaf gives an enclosure; the separate local theorem discharges it. |
| **P2 — Why does a local linear obstruction cover a finite neighborhood?** | Diagram the normalized displacement $0<\tau\le1$ and the impossible inequality $\tau\le c_j\tau^2$ with $c_j<1$. An optional branch/coordinate selector reads only accepted margins; print fixes the worst certified ratio and states the full $128\times33\times2$ signed-coordinate census. | [Local-isolation result](../../../../packing/resources/web/n11-optimality-2026-09-29/receipts/local-isolation/result.json), [checker](../../../../packing/devtools/check_n11_optimality_local_isolation.py), and [pose-inclusion receipt](../../../../packing/resources/web/n11-optimality-2026-09-29/receipts/pose-inclusion/result.json). Reuse the old explainer’s exact-versus-preview readout convention. | Show that the inequality follows from the signed-coordinate duals and curvature bounds, not from a sampled motion. A line graph is an algebraic schematic, not a plot of 33-dimensional feasible poses. Do not use a rounded ratio to establish strictness or present fixed-$T$ isolation as global uniqueness. |
| **P2 — How can a cap at $U>T$ settle the exact value $T$?** | A two-frame commutative diagram follows a hypothetical side-$S<T$ packing into the centered $U$ cap, through the field coordinate conversion, then by a rigid alignment into the fixed-$T$ container. Print shows the complete arrows and the nested $S$ and $T$ containers. | [Pose-inclusion checker](../../../../packing/devtools/check_n11_optimality_pose_inclusion.py), [final composer](../../../../packing/devtools/check_n11_final_composition.py), and [accepted composition](../../../../packing/resources/web/n11-optimality-2026-09-29/receipts/final-composition.json). Reuse the paper’s frame formulas rather than a new geometric animation. | The field scale $B=L/U$ changes coordinates; it does not rescale a physical unit-square packing. The final map is a rigid rotation and translation. Trump’s exact span $T$ contradicts $S<T$; the drawing must not assert uniqueness at side $U$ or at every optimal pose. |

The existing exact witness already answers “What attains $T$?” and needs no second
placement drawing. Figure 2’s cover and mask remain the location for capacity and D4
overlays. The current capture tree is a dependency picture; its missing split labels are
the first repair. The local proof presently has no figure, so its schematic should come
only after the row and branch visuals establish the meaning of a finite checked state.

## Implementation Slices

1. **Extend the retained SVGs.** Add the cell-capacity inset and closed cut labels to
   the existing figure module.
   Keep the four current figure slots and source checks; new data inputs must be added
   to the renderer’s tracked input set.
2. **Build one worked geometry row.** Extract display data from an accepted row and
   complete-step receipt, then render the four static panels.
   Add screen-only stepping only after static HTML/PDF is clear.
   This slice is the main test of whether an interaction improves understanding over
   captioned panels.
3. **Add the selective finite reductions.** Use the same cover labels for the field
   transfer and D4 views.
   Their controls switch among checked examples rather than calculating new certificate
   verdicts in the browser.
4. **Explain the endpoint.** Add the capture leaf selector, local inequality schematic,
   and cap-to-$T$ frame diagram, with the fixed-$T$/global distinction visible in their
   captions.

Each slice can be a separate implementation bead.
The paper text and figure placement should be reviewed with the user’s line edits before
changing figure numbering or captions.

## Verification and Publication

For every generated figure, compare its displayed case IDs, intervals, polygon vertices,
inequalities, and statuses with source-bound exact data before rounding to pixels.
Test malformed or missing source data as a render refusal.
A visual test must inspect HTML and the static PDF page at normal print scale; the
screen interaction must expose the same mathematical statement through keyboard controls
and text, with no hidden required step.
The publication check should reject absent figures, duplicate SVG IDs, remote or active
SVG content, stale render inputs, and an interaction that prints as an empty panel.
Keep diagrams explicitly explanatory: only the cited exact checkers and final
composition confer T-060 proof credit.

## Open Decision

The case-2095 row is the proposed first implementation because its exact reconstructed
owned-hull obstacles and one triangular residual make the lemma visible.
Review its source-bound polygons and complete-step successor before final layout.
The
[first capture row](../../../../packing/resources/web/n11-optimality-2026-09-29/receipts/capture-transition-row0/result.json)
is a separate, stronger example: its collision region is checked against all 149 partner
rows, 93 live, not merely against one fixed owned hull.
If shown later, label that universal obligation and keep its complete
[step receipt](../../../../packing/resources/web/n11-optimality-2026-09-29/receipts/capture-step0/result.json)
separate from the single-row receipt.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
