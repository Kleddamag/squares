---
type: is
id: is-01m3ys167s43cwbqecd86pvw5k
title: "Answer #282: wand125's mixed certificates (T-069, T-071, T-072; later ones queued)"
kind: task
status: open
priority: 2
version: 1
labels:
  - result-import
dependencies: []
parent_id: is-01m3yrzmzcpq964zt2kr14w8jv
created_at: 2026-10-02T17:01:47.129Z
updated_at: 2026-10-02T17:01:47.129Z
---
Answer jlevy/squares#282 (wand125, opened 2026-10-01): Mixed rectangle-measure certificates for n = 37, 65, 66, 90, 92 (after T-048): registration request

Replies due, from `python -m devtools.check_requests --report` on 2026-10-02:
- an acknowledgement: nothing has been posted on this issue
- mixed-five: T-069 at V0/C1: open, and no reply has said so
- n84-n85: T-071 at V0/C1: open, and no reply has said so
- n76: T-072 at V3/C3: confirmed, and no reply has said so
- n96-992: say why it is not registered (Raised within this thread by mixed_n96_L996 before any import, so an import at the later pin registers 9.96 alone and this one stays in the packet.)
- n85-946: an acknowledgement; not yet imported
- n87-n91-n92: an acknowledgement; not yet imported
- n83-937: an acknowledgement; not yet imported
- n96-996: an acknowledgement; not yet imported

Closeable now: no: mixed-five is open; n84-n85 is open; n85-946 is queued; n87-n91-n92 is queued; n83-937 is queued; n96-996 is queued.
Close condition: T-069, T-071 and T-072 are confirmed or refuted, and every later certificate posted here is imported and settled. The thread is a rolling request: each release is imported and answered on its own.

Sequence: once the pull request holding the ids above is on main, from packing/ on main run `uv run --frozen --all-extras --group dev python -m devtools.check_requests --draft 282`; the owner posts it (or an agent at the owner's request); record the comment's URL, date, kind and reported state under the issue's `replies` in packing/campaign/result-requests.yaml; rerun --report and close the issue with a final comment when it says closeable. Import beads: think-ye2x, think-fb6h, think-09ag, think-r7yt.
