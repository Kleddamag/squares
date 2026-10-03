---
type: is
id: is-01m3zq1e2jrzc7w09gkzt9qx4c
title: "Adaptive (non-uniform) kernel rows: producer split rule (K2) and verifier partition/predecessor check (P2, reviewed by R6)"
kind: task
status: open
priority: 0
version: 1
spec_path: docs/project/reviews/review-2026-10-02-n17-cost-reduction-pruning.md
labels: []
dependencies: []
parent_id: is-01m3xkd6zmq1jqwtn628h2k7zy
created_at: 2026-10-03T01:46:12.434Z
updated_at: 2026-10-03T01:46:12.434Z
---
K2's closure rule: a class closes only when per-row losses (wall legal-box loss ~dtheta/2 near axis angles, core loss) are below ~1-1.5x its float margin. Residue margins are 4e-3 to 1e-2, so uniform rows would need 128-256 bins (4-8x cost). Adaptive rows bisect only live wall rows near axis angles: effective 256-512 bins there at ~1.5-2x the 64-bin cost. The checker already accepts refinement (complete_refinement); producer split rule opt-in (K2); verifier must check partition and predecessor containment (P2); R6 reviews before the new digest is listed. First target: the 539-orbit south-wall class, which stalls at 64 bins (e1ee78eb9).
