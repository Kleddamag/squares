---
type: is
id: is-01m3n5xnf99f0aptwqfc250hkh
title: "n = 50: review and replay wand125's own-verifier certificates, s(50) >= 7.35 and mixed_n50_L740 at 37/5"
kind: task
status: in_progress
priority: 1
version: 3
labels:
  - packing
  - wand125-update
  - review
  - soundness
dependencies:
  - type: blocks
    target: is-01m3n5y05cdnsnkspf7e4vg5jp
parent_id: is-01m3n5wh72rsqd2z97m8v1vv4q
created_at: 2026-09-28T23:34:38.825Z
updated_at: 2026-09-28T23:47:44.251Z
---
Two claims beyond Tokoharu's verifier format (packing/resources/web/wand125-x-update-2026-09-28/supplied-messages.txt): 7.35, whose coverage reaches 1.0000000005 below verify.cpp's required 1.0001 margin, so it ships with its own verifier and a full replay bundle; and 7.40 (certificates/mixed_n50_L740), from bringing Green's N = k^2 + 1 approach into the search, about 0.083 above Green's 7.317426 (the register's reported bound, [Friedman DS7]). New trust boundary: review the custom verifier's soundness (outward rounding, what the margin is for, whether coverage >= 1 is decided rigorously) and the mixed certificate language before any replay counts; then replay in full. Overlaps think-pr2b (BC-394's own n = 50 and n = 82 ladders); wand125 names n = 65 (Green 8.2900) and n = 82 (Green 9.2667) as its next targets.
