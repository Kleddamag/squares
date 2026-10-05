---
type: is
id: is-01m471p5snjnhtjya7ah05n4g8
title: "Import evand #375: exact rational optima of 48 known-best packings (upper bounds 3e-13..5e-11 below the register) and exact certificates for 321 records at 13ee36e; n = 17's certificate held"
kind: task
status: in_progress
priority: 1
version: 3
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m46g4yac7ewc22drc7twjhy5
hold: null
hold_until: null
created_at: 2026-10-05T22:06:58.868Z
updated_at: 2026-10-05T22:34:50.518Z
started_at: 2026-10-05T22:08:15.283Z
---

## Notes

Stage 1 (triage), 2026-10-05, lane F of think-fg6g, worktree squares-lanes/exact,
branch claude/ecstatic-pascal-pothtx-exact (base 4fa04caf2).

Source pinned: evand/square-packing 13ee36e5807727d12a5da36b9b90a96bdba272bf
(committed 2026-10-05T20:54:59Z; head at 22:08Z and 22:22Z), s12/search/exact/.
The head is 2 commits past the 7ff3b211 pin: ab2bf47 (WISHLIST section G and a literature
note on the degree of s(n); nothing to import) and 13ee36e (this import).

Claim map (issue #375, body only, no comments):
- exact-optima-48: s(n) <= S'_n at n = 68, 102, 103, 106, 110, 123, 126, 131, 132, 152,
  154, 155, 156, 172, 177, 180, 181, 182, 199, 206-211, 228, 236-241, 259, 263,
  268-273, 297, 301-307; S' rational, 3.5e-13 to 5.0e-11 below the record's reported
  side. Register action: one new upper-bound entry (provisional T-099) whose scope covers
  the 48, with a reported entry and replay entries; the case records' reported and
  verified upper lanes move to S' (the T-088 and T-092 precedents: an optimization or a
  later release that lowers a side is a new entry, the earlier ones keep their claims and
  the case records decide which is current). Who else holds each value: Couzo's printed
  sides (T-056 at 40 counts, T-092 at 208, 209, 228, 263, 272, 303, 306), de Winter's
  n = 211 (T-057), and n = 126, de Winter's packing via the Kingbird catalogue, whose
  verified ceiling is the 12 x 12 grid today.
- certificates-273: exact certificates at the 272 other certified counts (n = 17 held),
  1e-20 to 1e-14 above the printed sides; the author asks for nothing. Register action:
  none ("below the standing bound and asking for no work"); retained by digest, replayed
  with the rest, and noted as a possible later use where the verified ceiling trails.
- kkt-local-minima: 315 of 321 (44 of the 48) numerically KKT local minima; numerical
  evidence, recorded as reported in T-099 and its evidence, not verified.
- n105-descent: n = 105's witness may not be a local minimum (first-order descent with
  corner-corner slips); numerical observation, no register action.
- n17-certificate: held by the owner (think-x4v4); not retained, replayed or recorded.

Validation plan, priced:
- The source's checkers verify_cert.py and verify_cert2.py (stdlib Fraction): measured
  54.6 CPU s for the 48 retained; about 4 CPU min for all 320.
- First-party: devtools.evand_exact_certificates converts each certificate exactly
  (t -> (c, s)) to a rational center-basis Witness/v2 for sqpack.witness.exact_verify and
  to rational corners for devtools.check_rational_witness_independent; measured 2.1 s at
  n = 68 and 33 s at n = 307; about 70 CPU min for all 320.
- Controls: per improving certificate, the tightest pair overlapped by its gap plus one
  unit of the side's denominator, the box shrunk past its least clearance by one unit
  (both must be refused by all four checkers), and the box shrunk by one unit alone.
- Comparison: S' against the earlier holders' printed and verified sides, and each pose
  against the known-best witness, square for square.
- Optional reproduction sample with reproduce.sh (about 1-2 CPU h for all; sample only,
  2 threads, nice).
- One separately prompted adversarial review.
