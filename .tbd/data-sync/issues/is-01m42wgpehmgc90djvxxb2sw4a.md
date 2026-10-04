---
type: is
id: is-01m42wgpehmgc90djvxxb2sw4a
title: "Import wand125: 14+ mixed certificates (#282)"
kind: task
status: in_progress
priority: 1
version: 3
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m41csdc2gp36ry5p6n7c2x2y
hold: null
hold_until: null
created_at: 2026-10-04T07:19:38.704Z
updated_at: 2026-10-04T07:32:05.750Z
started_at: 2026-10-04T07:32:04.027Z
---
Mixed rectangle-measure certificates posted on jlevy/squares#282 from 2026-10-03 19:33Z (14 at upstream 3554616; two more at 6832.. and 8aa6.. after 07:00Z). Stages 1-2 on branch import-282-mixed14 (packet wand125-mixed-bounds-2026-10-04, W7 audit binding by pinned digest). Stage 3 (new T-NNN) waits for jlevy/squares#305. Replays (~124 CPU-h for 14) held with think-wpuu. Separate import needed: c56b9b7 (T-066 F1/F2, #280).

## Notes

2026-10-04 07:40Z stage 1 claim map (tbd-moderate, branch import-282-mixed14):

Pin: wand125/square-packing-bounds 8aa6a10b3b8f165d39c85b68982fed1de086516c (head, committed 2026-10-04T07:17:29Z; ls-remote: one branch, no tags). 16 certificates, one #282 comment each, all checked by the retained mixed_rotated_verify.cpp (code/ byte-identical to mixed_n50_L740). Each is above the record's reported lower bound at its count; none lifts a following count by monotonicity.

- n42 2739/400 (mixed_n42_L68475, aa26adf) supersedes T-077 reported 2731/400
- n43 2763/400 (eaed02b), n44 2789/400 (83010fa), n56 3121/400 (cf451aa) supersede T-068 reported (T-074 verified) 551/80, 2777/400, 3113/400
- n51 747/100 (0e0bdea), n69 431/50 (8aa6a10), n75 447/50 (35b83e7), n86 9503/1000 (683264c), n88 769/80 (92b1a7e), n93 247/25 (b321ac9), n94 497/50 (3c7c57a), n95 1993/200 (3554616) supersede T-082 reported 373/50, 2153/250, 223/25, 19/2, 48/5, 493/50, 248/25, 249/25
- n57 3149/400 (bc72720), n67 339/40 (2475d08), n72 219/25 (c44fd6f) supersede T-046 reported 1567/200, 1691/200, 437/50
- n84 3763/400 (c9c6be0) supersedes T-071 47/5

Register action (stage 3): one new entry, scope n = 42, 43, 44, 51, 56, 57, 67, 69, 72, 75, 84, 86, 88, 93, 94, 95; attribution.published 2026-10-04; key [wand125 mixed bounds 2026-10-04]; per-count reported evidence (T-082 pattern), coverage entry, reported lanes of the 16 case records. Waits for jlevy/squares#305.

Evidence updates, not new entries: 150939e (OC-1/OC-2 answer) removes completion-audit.json and its two README lines from T-082's 22 directories and T-075's mixed_n96_L996, nothing else (retained in the packet; test holds it). Separate imports needed: c56b9b7 (k2m5_n59_L8, T-066 F1/F2, #280) and 1ebd484 (point_n45_L7, s(45) = 7 verify.sh D4 fix + reference run, #279/#280).

Validation priced: 16 complete 201-direction replays, 130.8 CPU-h by mixed-price, 146.3 planned (x 1.119 observed ratio over 14 merged replays), 180.2 by the source's own oblique seconds; mixed-shard --runners 8 gives ~18.3 CPU-h / 4.6 wall-h per runner. Exact audit and mixed-fetch preflights pass for all 16. W7 done: audit binds bundles without completion-audit.json by the digest at the pin (WITHOUT_SOURCE_AUDIT). Replays held with think-wpuu.
