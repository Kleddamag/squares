---
type: is
id: is-01m44rx09j4dapps52fx9bjjda
title: "Import Guzhou0806: s(17) R070 and R071 (4.6604427, 18641771/4000000), above the verified 116511/25000"
kind: task
status: in_progress
priority: 1
version: 3
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m44qz3phdnc1yfv76nxp6cak
hold: null
hold_until: null
created_at: 2026-10-05T00:54:56.562Z
updated_at: 2026-10-05T03:38:33.521Z
started_at: 2026-10-05T03:10:51.428Z
---
Found in stage 1 of the evand site import (think-plrl): evand's lower_bounds.json at evand/square-packing 7ff3b21 (retained in packing/resources/web/evand-square-packing-2026-10-04/) lists Guzhou0806 R070, s(17) > 46604427/10000000 (29 Sept, tree 8988d9333, certificates/R070-4.6604427) and R071, s(17) > 18641771/4000000 = 4.66044275 (30 Sept, tree 8c11f696, certificates/R071-C029; the repository's own CI replay 'R071 exact replay' passed; its README notes the old C027 partition records are missing), both above this record's verified s(17) > 116511/25000 (R068, T-043). Neither is in the register, an evidence entry or source coverage. By packing/campaign/result-import.md stage 1 a claim in scope that a request does not mention is an import of its own, from the author's own publication (github.com/Guzhou0806/n17-square-packing), not from evand's site. Kleddamag's 46601/10000 (29 Sept) is below R068 and stays a packet note. Pin the source, retain R070/R071 with their checkers, record as reported, price the paired replay (R068's took the C++ checker and Kleddamag's Node BigInt checker).

## Notes

Workflow: W1 import, stages 1-3 of packing/campaign/result-import.md, plus the R068-style pre-replay audit. Branch claude/ecstatic-pascal-pothtx-guzhou, commit 7ae4194dd (not pushed).

Pin: Guzhou0806/n17-square-packing 8c11f6962506940c5de67a9fa73b3d1e2e151196 (2026-09-30T22:53:43Z, main at retrieval 2026-10-05T03:11Z); R070 at 8988d933 (2026-09-29T07:56:05Z). Packet packing/resources/web/n17-guzhou-r071-2026-09-30 (acquire_source declaration; 153 retained, 33 pinned-only: 32 byte-identical to the R068 packet's upstream/ checker and notices, 1 research output; --check PACKET_MATCHES_ITS_CONTRACT). Keys [Guzhou0806 n17 R071] (dated 2026-09-30), [Guzhou0806 n17 R070] (context). Coverage guzhou-n17-r071-2026.

Claim map (claim -> action -> id):
- R071 s(17) > 18641771/4000000 = 4.66044275, C027 cert 15b6bf6a, R068's charge unchanged, 5,114 intervals -> new entry (later release raising T-043's value), reported -> T-093 (provisional; V0/C0, S2 draft), E-n017-guzhou-r071-report, n-017 reported lane
- R070 s(17) > 46604427/10000000 = 4.6604427, cert 8438cae4, 5,107 intervals -> none: superseded by R071 (built on it) the next day, never replayed; stays in packet and n-017 prose
- R070 319-orbit same-budget overlay; parent-separation obstruction at 186417711/40000000 in a fixed-weight class -> none (no bound, source says so)
- R071 C028/C029 conditional joint geometry at 9321/2000 in one first-anchor box (17 conflicts, 2 forced holes, 9<=Vmax<=11, 8 unknown pairs) -> none (source: does not prove s(17)>4.6605)
- T-043 (R068) keeps the verified field; coverage note added.

Pre-replay audit (devtools.audit_guzhou_r071, receipts in packet): both certificates' point orbits, rules, budget and requested minimum equal R068's; chains refine R068's (R070 +116, R071 +7 bisections over R070); all cores rebuilt (same angle, new side). R070 published 4+4 ledgers agree row by row: min 1000026844 on all 5,107 rows, cells 2,260,759,562,719, surplus 7404. R071 C027 summary consistent with its cert; names R068's verify_global_variable.js and replay.js digests and R068/R070's executable. R071 row records missing (source says so). Source CI: R070 run 36539632653 and R071 run 36788162356 both success (bound job 16m43s); artifacts unreachable (Azure blob 403).

Price (stage 4, not run): R071 complete paired replay (run_public.js bound or replay.js at 2 partitions, then audit_guzhou_r071 compare R071 FRESH --published FRESH) ~ 4,200 CPU-s (~70 CPU-min), ~80 min wall on 2 contended cores, scaled from R068's measured 4,093 CPU-s by R070's published cells (x1.023). Source: C027 1,694 s at 3 partitions; R070 869 s at 4. Needs Boost headers (libboost1.83-dev; absent here). R070 needs no replay of its own. Cheaper diagnostic first: the r071-bound CI artifact (expires 2026-12-29) holds fresh partitions, from a host that can reach the blob store.

Kleddamag/17-squares-certified-bound 17d18245 (4.6601, below T-043): read recorded in intake-watch.yaml; overlaps think-nkzt's list.
