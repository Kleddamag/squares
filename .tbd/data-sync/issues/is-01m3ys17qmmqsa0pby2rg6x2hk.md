---
type: is
id: is-01m3ys17qmmqsa0pby2rg6x2hk
title: "Answer #281: wand125's 34 raised rectangle bounds (T-068)"
kind: task
status: open
priority: 2
version: 1
labels:
  - result-import
dependencies: []
parent_id: is-01m3yrzmzcpq964zt2kr14w8jv
created_at: 2026-10-02T17:01:48.659Z
updated_at: 2026-10-02T17:01:48.659Z
---
Answer jlevy/squares#281 (wand125, opened 2026-10-01): Rectangle-density lower bounds raised since T-046 (34 counts in n = 19…95): registration request

Replies due, from `python -m devtools.check_requests --report` on 2026-10-02:
- an acknowledgement: nothing has been posted on this issue
- rect-34: T-068 at V0/C1: open, and no reply has said so

Closeable now: no: rect-34 is open.
Close condition: T-068 is confirmed or refuted at all 34 counts. Counts that pass move to replayed entries, as T-045 and T-070 did for T-046; add each such entry to this result.

Sequence: once the pull request holding the ids above is on main, from packing/ on main run `uv run --frozen --all-extras --group dev python -m devtools.check_requests --draft 281`; the owner posts it (or an agent at the owner's request); record the comment's URL, date, kind and reported state under the issue's `replies` in packing/campaign/result-requests.yaml; rerun --report and close the issue with a final comment when it says closeable. Import beads: think-6ei5.
