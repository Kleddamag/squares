---
type: is
id: is-01m3xrx8b86kp8t1k6gj71p4ej
title: "Reply on #295 (T-007, Nagamochi Lemma 1 false): the follow-up after PR #305's register change"
kind: task
status: open
priority: 1
version: 9
delegate: claude-code@vm
labels:
  - result-import
  - packing
dependencies:
  - type: blocks
    target: is-01m3yrzmzcpq964zt2kr14w8jv
parent_id: is-01m41csdc2gp36ry5p6n7c2x2y
hold: null
hold_until: null
created_at: 2026-10-02T07:40:23.784Z
updated_at: 2026-10-06T09:05:26.934Z
started_at: 2026-10-05T03:21:49.383Z
---
J. PR jlevy/squares#305 (session-168) reviewed T-007 and changed the register; it merged on 2026-10-04. Lemma 1 is false for every a > 3, b > 2 (Karakus family, exact). T-007 is at V0/C1 with the defect recorded, the 287 verified floors that rested on it are re-derived (D-516), and T-083 to T-086 are registered. This bead answers #295. Note for the 2 October stack: verified lower bounds raised by replayed rectangle certificates removed T-007 from 17 more counts (46 operative left then).

## Replies due on #295 (2026-10-02)

Answer jlevy/squares#295 (wand125, opened 2026-10-02): T-007 (Nagamochi 2005): Lemma 1 is false; published counterexamples and replacement results

Replies due, from `python -m devtools.check_requests --report` on 2026-10-02:
- an acknowledgement: nothing has been posted on this issue
- lemma1-false: T-007 at V3/C1, E-nagamochi-lower (verified, external): open, and no reply has said so
- karakus-2026: an acknowledgement; not yet imported
- chelokot-2026: an acknowledgement; not yet imported

Closeable now: no: lemma1-false is open; karakus-2026 is queued; chelokot-2026 is queued; asked: Re-derive the 63 operative values T-007 supplies from the replacements or stronger results.
Close condition: The record holds the Lemma 1 defect against T-007, the values it supplies are re-derived, and the two replacement sources are registered or declined.

Sequence: once the pull request holding the ids above is on main, from packing/ on main run `uv run --frozen --all-extras --group dev python -m devtools.check_requests --draft 295`; the owner posts it (or an agent at the owner's request); record the comment's URL, date, kind and reported state under the issue's `replies` in packing/campaign/result-requests.yaml; rerun --report and close the issue with a final comment when it says closeable. Import beads: think-bmze.

## Notes

2026-10-06 (lane R6): a reply is due once R6's staged exit (think-lpul) merges. On the exit branch, check_requests --report says #295 is "Closeable: yes, with a final comment". The reply corrects the 5 October follow-up on T-083 and T-084. Render it with check_requests --draft 295 from main after the merge, link the review think-lpul stores, then close the issue. The lane's draft, not posted:

@wand125, the last open item here is done, so this closes the issue.

**Corrections to earlier replies.** The reply of 5 October gave T-083 and T-084, Karakuş's results, at V3/C1, reviewed. They now read V3/C3, confirmed.

- **Karakuş, arXiv:2609.37410.** T-083 (Corollary 6.2, every nonsquare 8 ≤ N ≤ 324) and T-084 (Corollary 1.2, s(k² − 1) = k, held here for k = 3 to 18) are confirmed, re-verified here by an independent implementation. Proposition 5.1 is the step the rectangle bound rests on: the strip measure gives the interior of every square of side in (1, 1.01] more than one. [`check_karakus_strip_measure`](https://github.com/jlevy/squares/blob/main/packing/devtools/check_karakus_strip_measure.py) decides it by an exact branch and bound over the square's orientation, side and the height at which the strip's line cuts it. The cover is 5,939 boxes in exact rational arithmetic, retained and replayed box by box. It is tight at one pose: the axis-parallel square on the container's floor, where the measure is 1 + (λ − 1)(λ + ½). The four boxes there close by an exact expansion in λ − 1. Three mutated measures are refused, each with a counterexample. Two steps stay read and are not machine-checked: the reduction of a square's measure to its vertical profile, and Theorem 1.1's scale-and-sum. Both are elementary. [Review of 6 October: link once stored.]
- **Nagamochi's Lemma 1** is unchanged since the last reply. T-007 records the defect at V0/C1, and T-085, the finding, is confirmed at V3/C3.
- **chelokot** is unchanged. T-086, s(k² − 2) = k, is confirmed at V3/C3, reproduced here with the author's own checker.

The close condition holds: the record holds the Lemma 1 defect against T-007, every value it supplied is re-derived, and both replacement sources are registered and confirmed. Thank you for the report.

On `main`: [`RESULTS.md`](https://github.com/jlevy/squares/blob/main/packing/frontier/RESULTS.md).
