---
type: is
id: is-01m44rx09j4dapps52fx9bjjda
title: "Import Guzhou0806: s(17) R070 and R071 (4.6604427, 18641771/4000000), above the verified 116511/25000"
kind: task
status: in_progress
priority: 1
version: 2
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m44qz3phdnc1yfv76nxp6cak
hold: null
hold_until: null
created_at: 2026-10-05T00:54:56.562Z
updated_at: 2026-10-05T03:10:51.428Z
started_at: 2026-10-05T03:10:51.428Z
---
Found in stage 1 of the evand site import (think-plrl): evand's lower_bounds.json at evand/square-packing 7ff3b21 (retained in packing/resources/web/evand-square-packing-2026-10-04/) lists Guzhou0806 R070, s(17) > 46604427/10000000 (29 Sept, tree 8988d9333, certificates/R070-4.6604427) and R071, s(17) > 18641771/4000000 = 4.66044275 (30 Sept, tree 8c11f696, certificates/R071-C029; the repository's own CI replay 'R071 exact replay' passed; its README notes the old C027 partition records are missing), both above this record's verified s(17) > 116511/25000 (R068, T-043). Neither is in the register, an evidence entry or source coverage. By packing/campaign/result-import.md stage 1 a claim in scope that a request does not mention is an import of its own, from the author's own publication (github.com/Guzhou0806/n17-square-packing), not from evand's site. Kleddamag's 46601/10000 (29 Sept) is below R068 and stays a packet note. Pin the source, retain R070/R071 with their checkers, record as reported, price the paired replay (R068's took the C++ checker and Kleddamag's Node BigInt checker).
