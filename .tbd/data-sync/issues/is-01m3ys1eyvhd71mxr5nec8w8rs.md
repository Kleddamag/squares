---
type: is
id: is-01m3ys1eyvhd71mxr5nec8w8rs
title: "Answer #238: follow up the 29 September reply (V3/C3, no-fold run, Lean), then close"
kind: task
status: open
priority: 1
version: 1
labels:
  - result-import
dependencies: []
parent_id: is-01m3yrzmzcpq964zt2kr14w8jv
created_at: 2026-10-02T17:01:56.059Z
updated_at: 2026-10-02T17:01:56.059Z
---
Answer jlevy/squares#238 (evand, opened 2026-09-27): Exact values s(21) = 5 and s(32) = 6: registration request (external certificates)

Replies due, from `python -m devtools.check_requests --report` on 2026-10-02:
- a follow-up: the reply of 2026-09-29 said jlevy/squares#245 is under review; it has merged
- a follow-up: the reply of 2026-09-29 said the zm_mixed.py re-sweeps for s(21) and s(45) were started; their partial records were lost and they restart from nothing
- a follow-up: the reply of 2026-09-29 said the Lean theorems are recorded as reports; s13_eq_4 and the conditional s(21) and s(32) theorems were built here on 30 September
- s32: the reply of 2026-09-29 stated T-051 at V4/C3; it is now V3/C3
- s21: the reply of 2026-09-29 stated T-052 at V4/C3; it is now V3/C3
- s32-no-fold: T-051 at V3/C3, E-n032-evand-zmx2-full-sym-report (reported, external), E-n032-evand-zmx2-full-sym-replay (verified, replayed-here): confirmed, and no reply has said so
- s61-point-route: T-063 at V3/C3: confirmed, and no reply has said so

Closeable now: yes, with a final comment.
Close condition: A follow-up corrects the reply of 29 September (V3/C3 under the ladder of 30 September, #245 merged, the re-sweeps restarted, the Lean builds) and states the no-fold run's import. Nothing Daniel asked for is then queued.

Sequence: once the pull request holding the ids above is on main, from packing/ on main run `uv run --frozen --all-extras --group dev python -m devtools.check_requests --draft 238`; the owner posts it (or an agent at the owner's request); record the comment's URL, date, kind and reported state under the issue's `replies` in packing/campaign/result-requests.yaml; rerun --report and close the issue with a final comment when it says closeable. Import beads: think-48e1.
