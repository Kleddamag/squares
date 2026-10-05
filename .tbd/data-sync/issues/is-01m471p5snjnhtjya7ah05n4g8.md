---
type: is
id: is-01m471p5snjnhtjya7ah05n4g8
title: "Import evand #375: exact rational optima of 48 known-best packings (upper bounds 3e-13..5e-11 below the register) and exact certificates for 321 records at 13ee36e; n = 17's certificate held"
kind: task
status: in_progress
priority: 1
version: 4
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m46g4yac7ewc22drc7twjhy5
hold: null
hold_until: null
created_at: 2026-10-05T22:06:58.868Z
updated_at: 2026-10-05T23:23:37.497Z
started_at: 2026-10-05T22:08:15.283Z
---

## Notes

Stage 1 (triage), 2026-10-05: see the claim map below; acknowledgement posted
https://github.com/jlevy/squares/issues/375#issuecomment-6004562871 (22:35:10Z), recorded in
result-requests.yaml (#375, answer bead think-ybmt).

Provisional register id renumbered by the coordinator from T-099 to T-098 (T-095 to T-097 are
s(12), s(18), s(66)); the branch uses T-098 throughout.

Stage 2 (retain): packet packing/resources/web/evand-square-packing-2026-10-05 written by
devtools.acquire_source from a blobless clone at 13ee36e; 58 files retained (48 improving
certificates, verify_cert.py, verify_cert2.py, exactsolve.py, geom.py, verify_all.sh,
reproduce.sh, results.md, results.json(.gz), both READMEs), 632 pinned by digest; n = 17's
certificate, input and test-set outputs left out of the scope (think-x4v4).
Key [evand exact optima 2026-10-05]; credit Daniel after Couzo, de Winter, Ellsworth, Levy;
lineage builds-on-project.

Stage 3 (record): T-098 upper-bound, 48 counts; evidence E-evand-exact-optima-2026-10-05-report,
-exact-replay, -source-replay; verifiers V-evand-verify-cert-py, V-evand-verify-cert2-py,
V-evand-exact-certificates. Case records written by devtools.apply_exact_optima, a layer
composed into apply_upper_bound_packets and generate_frontier_case; source-coverage selects
the packet (claims record: the retained certificate directory). Atlas pictures the finder's
pose (pictured_source_key).

Stage 4 (replay), 320 certificates (all but n = 17):
- first-party: sqpack exact_verify + check_rational_witness_independent, all VALID, 2,820 CPU s
  on 2 workers (802 for the 48); least wall clearance 5e-21, least pair gap 1e-20.
- source checkers verify_cert.py + verify_cert2.py: all accept, 202 CPU s (55 for the 48).
- comparison: all 48 below the earlier printed side by 3.53e-13 to 4.97e-11, matched one to
  one; largest displacement 1.44e-3 (free squares), non-free 4.14e-5 (n = 263).
- finding: verify_all.sh's first leg (grep -q VALID) also matches INVALID.
Follow-up opened: think-70bh (the 78 trailing ceilings the other certificates could lift).
