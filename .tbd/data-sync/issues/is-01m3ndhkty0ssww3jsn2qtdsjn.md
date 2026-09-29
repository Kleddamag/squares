---
type: is
id: is-01m3ndhkty0ssww3jsn2qtdsjn
title: "Evaluate wand125/square-packing-tools (325f32ff, MIT) against this repository's tools: adopt, replace or complement"
kind: task
status: open
priority: 1
version: 1
labels:
  - packing
  - wand125-update
  - tooling
  - research
dependencies: []
parent_id: is-01m3n5wh72rsqd2z97m8v1vv4q
created_at: 2026-09-29T01:47:52.542Z
updated_at: 2026-09-29T01:47:52.542Z
---
wand125 published the drivers behind its rectangle-density certificates at https://github.com/wand125/square-packing-tools, pinned here at 325f32ff9b8bd9a5e5b1f4d6e37699ea11f84a78 (tree 11d5a2110eb6ba3f22dcbe3c21c54642ce410db1, 2026-09-29T00:21Z, MIT, 472 KB; the owner-supplied announcement is packing/resources/web/wand125-x-update-2026-09-28/supplied-message-3-2026-09-29.txt). Contents: transfer/ and ladder/ (move a certified certificate to a larger n or L with re-optimised weights, budget-recovery edge rungs, the B*UB(n) ceiling l_cap.py, rescaling), performance/ (working-row LP with basis reuse, batch-16 and angle-parallel counterexample screening, a cached-axis verifier used only during search, and point_verifier_lazy, a faster zmx2 patch on Daniel's verifier), solver/ (Tokoharu's LP solver as they run it, with their modules; certificates are still accepted only by Tokoharu's unchanged verify.cpp). Task: retain a pinned copy as a packet; run its test suite and its end-to-end ladder here; compare each capability with this repository's generators (run_fractional_colgen, the BC-394/BC-395 ladder plan), the audit/replay tools (audit_tokoharu_density, audit_wand125_rectangles) and the capability matrix in docs/project/reviews/review-2026-09-28-density-solver-comparison.md, whose finding that these speed-ups were unpublished this release supersedes; decide per capability whether to adopt it as a pinned dependency, replace a tool here, complement one, or leave it; any verifier-side change (the cached-axis verifier, the lazy zmx2) is search-only or needs a Fable review before it can decide anything here. Output: a review document with the per-capability decision and, if adopted, the integration commitments. Related: think-v2lv (technique evaluation), think-0rrj (replay merge), BC-394/BC-395.
