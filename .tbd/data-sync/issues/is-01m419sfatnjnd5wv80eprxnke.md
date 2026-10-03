---
type: is
id: is-01m419sfatnjnd5wv80eprxnke
title: "n17 admission rule: five frictions found admitting SW9 and N1 (exp-250)"
kind: task
status: open
priority: 2
version: 2
spec_path: docs/project/reviews/review-2026-10-02-n17-bulk-exclusion-design.md
labels:
  - n17
dependencies: []
parent_id: is-01m3xkd6zmq1jqwtn628h2k7zy
created_at: 2026-10-03T16:33:08.953Z
updated_at: 2026-10-03T18:15:29.721Z
---
Lane A3, admitting SW9 (flag 3) and N1 in exp-250 (53fe57147), found five frictions in census_n17_certified's admission rule.
1. The receipt's directory must equal the entry's certificate path exactly, so a certificate directory cannot be renamed (both admitted ones are still *-pending) without another 6-8 min verification. Match on the seed and node content ids instead.
2. A verifier revision is admitted on a YAML comment ('only I/O changed'). Consider tying the listing to the verifier test file passing at that revision.
3. evidence is checked for existence only. It is a pointer, not a check; say so or drop it.
4. H-267 is scoped to arity <= 7, but the census counts every arity (SW9 is 9, N1 is 17). Re-scope H-267 or register a census hypothesis.
5. Producer costs (1,521 s, 3,723 s, the 3,767 s check-saved, the stall controls) appear in no round's wall_seconds; exp-250 counts only the verifications.
Constraint: OR-16 as amended. No new digest comparison; the integrity-ceremony ratchet must still pass.

## Notes

6. (2026-10-03, after lane V1, 318c28c42.) Every kernel verifier revision listed before 318c28c42 accepts an uncovered zero-area row, and those from e0b66f07b on also accept an uncovered one-point section. Neither branch ran on W7, SW9 or N1, so their admissions stand. New admissions should be verified at 318c28c42 or later. The census does not enforce that yet: it counts a receipt from any listed revision. Decide whether to restrict the older listings to the receipts that already use them. 7. The n11 receipts register (upstream 27660cf18) names three verification depths for a receipt; consider the same vocabulary for n17 admission.
