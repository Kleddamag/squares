---
type: is
id: is-01m3xrx8b86kp8t1k6gj71p4ej
title: "Reply on #295 (T-007, Nagamochi Lemma 1 false): point to PR #305's review, register change awaits the owner"
kind: task
status: open
priority: 1
version: 5
labels:
  - result-import
  - packing
dependencies:
  - type: blocks
    target: is-01m3yrzmzcpq964zt2kr14w8jv
parent_id: is-01m41csdc2gp36ry5p6n7c2x2y
created_at: 2026-10-02T07:40:23.784Z
updated_at: 2026-10-03T17:27:10.276Z
---
J. PR jlevy/squares#305 (session-168) reviewed T-007: Lemma 1 false for every a > 3, b > 2 (Karakus family, exact), the gap reaches T-007 for every N >= 10, register unchanged pending the owner's decision. This bead only answers #295 and links the review; the register change belongs to that decision. Note for this stack: verified lower bounds raised here by replayed rectangle certificates remove T-007 from 17 more counts (46 operative left).

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
