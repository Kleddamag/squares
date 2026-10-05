---
type: is
id: is-01m3xrx8b86kp8t1k6gj71p4ej
title: "Reply on #295 (T-007, Nagamochi Lemma 1 false): the follow-up after PR #305's register change"
kind: task
status: open
priority: 1
version: 7
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
updated_at: 2026-10-05T03:23:08.634Z
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

2026-10-05 (intake triage, think-nkzt): #305 merged on 2026-10-04 and think-yl2j closed on 2026-10-03, so the dependency is removed and the description is current. A reply is due. On origin/main d54cba554, check_requests --report finds that the 2026-10-04 follow-up gave T-007 as V3/C1, reviewed, and it is now V0/C1 with the defect recorded. Since that reply, T-085 and T-086 are confirmed and T-083 and T-084 are reviewed. The draft below is check_requests --draft 295 rendered on that commit. Re-render it on main before posting, post it on the owner's word, then record it under #295's replies in result-requests.yaml. #295 stays open after this reply while karakus-2026 is open: T-083 and T-084 at C1 need a replay of Proposition 5.1, and no bead names that replay yet.

## Draft reply on #295 (not posted)

Where this request stands in the record on `main`.

**Corrections to earlier replies.**

- The reply of 2026-10-04 gave T-007 as V3/C1, reviewed; it now reads V0/C1, incomplete.

**What is registered.**

- Nagamochi 2005, Lemma 1 is false, so the published proof of Theorem 2 is incomplete: the record holds this defect.
  - T-007, a defect is recorded against it: the read of 2026-10-02 found a defect in E-nagamochi-lower, and no replay here has passed.
  - T-085, confirmed at V3/C3: re-verified here by an independent implementation (devtools.check_nagamochi_lemma1_counterexample).
  - E-nagamochi-lower, a defect is recorded against it: the read of 2026-10-02 found a defect.
  - E-nagamochi-lemma1-counterexample, confirmed here: re-verified here by an independent implementation (devtools.check_nagamochi_lemma1_counterexample).
- Karakuş, arXiv:2609.37410: s(k^2 - 1) = k for every k >= 2, and s(N) >= 1/2 + sqrt(N - floor(sqrt N) + 1/4) for every nonsquare N >= 8:
  - T-083, reviewed: its argument has been read here and no blocking defect found, and no replay here has passed yet (V3/C1).
  - T-084, reviewed: its argument has been read here and no blocking defect found, and no replay here has passed yet (V3/C1).
- chelokot, s(n^2 - 2) = n for every n >= 2, kernel-checked in Lean:
  - T-086, confirmed at V3/C3: reproduced here with the author's own checker (The source's Lean development (formal/), built by lake at its pinned toolchain, devtools.replay_chelokot_lean).
  - T-085, confirmed at V3/C3: re-verified here by an independent implementation (devtools.check_nagamochi_lemma1_counterexample).
  - E-chelokot-square-minus-two-lean, confirmed here: reproduced here with the author's own checker (The source's Lean development (formal/), built by lake at its pinned toolchain, devtools.replay_chelokot_lean).

**What is still queued, and how it will be completed.**

- T-083: C2 and above need a replay: a machine check of Proposition 5.1, that every square of side in (1, 1.01] gets more than one from the strip measure, over its three-parameter pose space. A stronger floor at any n is a new result, not a rung change.
- T-084: C2 and above need a replay of the lower half: a machine check of Proposition 5.1, or a replay of chelokot's Lean proof of the same family by an augmented measure, which is reported and was not built here.

**On `main`.** [`packing/frontier/RESULTS.md`](https://github.com/jlevy/squares/blob/main/packing/frontier/RESULTS.md), [`packing/frontier/STATUS.md`](https://github.com/jlevy/squares/blob/main/packing/frontier/STATUS.md).

This issue stays open while anything above is queued, and a reply follows each change in the record.

---
_Generated by [Claude Code](https://claude.ai/code)_
