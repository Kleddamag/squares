---
type: is
id: is-01m3ys14zf9kaxrjz44ksfrhmd
title: "Answer #294: wand125's linear certificates (T-073; n = 82 queued)"
kind: task
status: open
priority: 2
version: 2
labels:
  - result-import
dependencies: []
parent_id: is-01m41csdc2gp36ry5p6n7c2x2y
created_at: 2026-10-02T17:01:45.839Z
updated_at: 2026-10-03T17:26:53.084Z
---
Answer jlevy/squares#294 (wand125, opened 2026-10-02): Linear point/segment certificates: s(101) ≥ 257/25 = 10.28

Replies due, from `python -m devtools.check_requests --report` on 2026-10-02:
- an acknowledgement: nothing has been posted on this issue
- n101: T-073 at V0/C1: open, and no reply has said so
- n83: T-073 at V0/C1: open, and no reply has said so
- n82: an acknowledgement; not yet imported

Closeable now: no: n101 is open; n83 is open; n82 is queued.
Close condition: T-073 is confirmed or refuted, and the n = 82 certificate is imported and settled.

Sequence: once the pull request holding the ids above is on main, from packing/ on main run `uv run --frozen --all-extras --group dev python -m devtools.check_requests --draft 294`; the owner posts it (or an agent at the owner's request); record the comment's URL, date, kind and reported state under the issue's `replies` in packing/campaign/result-requests.yaml; rerun --report and close the issue with a final comment when it says closeable. Import beads: think-m7cm, think-r7yt.
