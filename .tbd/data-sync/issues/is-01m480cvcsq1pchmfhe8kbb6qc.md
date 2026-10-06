---
type: is
id: is-01m480cvcsq1pchmfhe8kbb6qc
title: "Replay wand125's ValidTilt9 run (records-tilt9-v1, c561dbb) in full: the independent route to T-081's finite premise"
kind: task
status: open
priority: 2
version: 2
labels:
  - result-import
  - packing
dependencies: []
created_at: 2026-10-06T07:03:39.160Z
updated_at: 2026-10-06T07:56:07.631Z
---
Held from think-dsz4 (lane R3, 6 October intake round), which retained wand125/valid7-independent-check at c561dbb3 in packing/resources/web/wand125-valid7-independent-check-2026-10-06/ and recorded the run as reported evidence E-k2m4-wand125-validtilt9-report on T-081. The full replay costs far more than the 6 CPU-hour ceiling of that lane, so it waits for a budget the owner sets. The price, from a stratified sample of roots re-run here, is in the packet's receipts/validtilt9_sample_compare.json and README (Price section). Two designs, per review-2026-10-06-wand125-validtilt9-independent-check.md section 5: (A) re-certify every CORE and TIERB2 leaf of the published records with check_record.py --partial --recheck/--recheck-b, sharded, against the retained release/records.sha256 (option-free, tests the published certificate; leaf re-certification cost about as much as the search for Valid7); or (B) re-run run_all.py over the 28,350 roots with each root's phase options from devtools.audit_validtilt9_independent PHASES (the sample's stage/run/compare subcommands), comparing leaf lists root for root. Controls: devtools.audit_validtilt9_independent control (two box-9 mutants refused). Then a replayed-here evidence entry, independent-implementation, and T-081's ValidTilt9 part can move; the Lean reduction needs its own replayed entry as well.

## Notes

2026-10-06 lane R3 (think-dsz4), branch claude/ecstatic-pascal-pothtx-r3:
- Packet: packing/resources/web/wand125-valid7-independent-check-2026-10-06/ (c561dbb3; records-tilt9-v1 pinned by digest in release/records.sha256).
- Tool: devtools.audit_validtilt9_independent (audit, stage, sample, run, compare, control). The full replay can reuse stage/run/compare per root; PHASES gives each root's published options.
- Price from a stratified sample (receipts/validtilt9_sample_compare.json): ~435 CPU-hours here as published (root for root, leaves compared; 2/3 of it the 266 heavy roots that ran at --amin 1/1280), ~118 CPU-hours with every root under the last options (--amin 1/1280 --bmid-u 7/16 --bmid-w 1/20), the softer figure (nine heavy probes, ratio 0.0002-0.57, weighted 0.012). Host CPU per recorded second 0.52-0.59 by phase. Design (A) of the review (re-certify every published leaf) not priced.
- Already done here: verify_tilt9.sh RECORD OK (fresh seed), records audit OK, 30 roots re-decided (21 with published leaves), two box-9 mutant controls refused.
- Waits for a budget the owner sets; nothing else blocks it.
