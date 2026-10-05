---
type: is
id: is-01m3ys167s43cwbqecd86pvw5k
title: "Answer #282: wand125's mixed certificates (T-069, T-071, T-072; later ones queued)"
kind: task
status: open
priority: 2
version: 7
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m41csdc2gp36ry5p6n7c2x2y
hold: null
hold_until: null
created_at: 2026-10-02T17:01:47.129Z
updated_at: 2026-10-05T05:35:49.996Z
started_at: 2026-10-05T03:21:48.835Z
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

## Notes

2026-10-03 22:55 T-069, T-071, T-072, T-075 at V3/C3 on main; T-082 (22 certificates of 3 Oct) on main at V0/C1 via #324 (4949d1439); reply with OC-1/OC-2 posted (issuecomment-5974294911). Stays open until T-082's replays are recorded (think-wpuu).

2026-10-05 (intake triage, think-nkzt): think-yl2j landed the stack and closed on 2026-10-03, so that dependency is removed. #282 is a rolling request, and it is not closeable while later certificates are unsettled. It also waits on think-wrdq, the replay of the 14 certificates of 4 October. Their import is think-07s1, on another lane, which also owns the 14 unread comments of 4 October. The next reply follows when T-082 or the 4 October import moves on main.

2026-10-05 after PR 353 merged (62f81e3a6): reply draft for #282 rendered by `check_requests --draft 282` on main. NOT POSTED; awaiting the owner.

Where this request stands in the record on `main`.

**What is registered.**

- s(37) >= 161/25, s(65) >= 167/20, s(66) >= 421/50, s(90) >= 48/5 and s(92) >= 969/100:
  - T-069, confirmed at V3/C3: reproduced here with the author's own checker (mixed_rotated_verify.cpp, with the source's per-angle replay functions, devtools.audit_wand125_point_and_mixed).
- s(84) >= 47/5 and s(85) >= 471/50 (52af997):
  - T-071, confirmed at V3/C3: reproduced here with the author's own checker (mixed_rotated_verify.cpp, with the source's per-angle replay functions, devtools.audit_wand125_point_and_mixed).
- s(76) >= 447/50 = 8.94 (mixed_n76_L894, 7975030):
  - T-072, confirmed at V3/C3: reproduced here with the author's own checker (mixed_rotated_verify.cpp, with the source's per-angle replay functions, devtools.audit_wand125_point_and_mixed).
- s(85) >= 473/50 = 9.46 (mixed_n85_L946, 028b915), so s(86), s(87) >= 9.46:
  - T-075, confirmed at V3/C3: reproduced here with the author's own checker (mixed_rotated_verify.cpp, with the source's per-angle replay functions, devtools.audit_wand125_point_and_mixed).
- s(87) >= 237/25, s(91) >= 97/10 and s(92) >= 39/4 (6e4e978):
  - T-075, confirmed at V3/C3: reproduced here with the author's own checker (mixed_rotated_verify.cpp, with the source's per-angle replay functions, devtools.audit_wand125_point_and_mixed).
- s(83) >= 937/100 (mixed_n83_L937, 25c421d):
  - T-075, confirmed at V3/C3: reproduced here with the author's own checker (mixed_rotated_verify.cpp, with the source's per-angle replay functions, devtools.audit_wand125_point_and_mixed).
- s(96) >= 249/25 = 9.96 (mixed_n96_L996, b00fc70):
  - T-075, confirmed at V3/C3: reproduced here with the author's own checker (mixed_rotated_verify.cpp, with the source's per-angle replay functions, devtools.audit_wand125_point_and_mixed).
- Twenty-two mixed rectangle-measure certificates posted in comments of 3 October 2026, from mixed_n95_L996 (s(95) >= 249/25) to mixed_n69_L8612 (s(69) >= 2153/250), at n = 51, 52, 55, 58, 69, 70, 71, 73, 74, 75, 76, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95 and 96, 21 above what the record reported at their counts; at n = 96, below T-081's reported s(96) = 10 and above the verified 249/25:
  - T-082, reviewed: its argument has been read here and no blocking defect found, and no replay here has passed yet (V0/C1).
- Fourteen mixed rectangle-measure certificates posted in comments from 3 October 19:33 UTC to 4 October 06:09 UTC: s(93) >= 247/25, s(44) >= 2789/400, s(56) >= 3121/400, s(84) >= 3763/400, s(67) >= 339/40, s(88) >= 769/80, s(94) >= 497/50, s(51) >= 747/100, s(75) >= 447/50, s(72) >= 219/25, s(57) >= 3149/400, s(43) >= 2763/400, s(42) >= 2739/400 and s(95) >= 1993/200 (b321ac9 to 3554616), each above what the record reported at its count:
  - T-090, reviewed: its argument has been read here and no blocking defect found, and no replay here has passed yet (V0/C1).
- Two more posted on 4 October at 07:04 and 07:17 UTC, s(86) >= 9503/1000 and s(69) >= 431/50 (683264c, 8aa6a10), pinned with the fourteen above at 8aa6a10:
  - T-090, reviewed: its argument has been read here and no blocking defect found, and no replay here has passed yet (V0/C1).
- Twelve mixed rectangle-measure certificates posted in comments of 4 October 2026 from 07:51 to 19:04 UTC: s(91) >= 781/80, s(76) >= 1793/200, s(90) >= 973/100, s(71) >= 8721/1000, s(87) >= 479/50, s(54) >= 1537/200, s(73) >= 8813/1000, s(94) >= 199/20, s(53) >= 3051/400, s(88) >= 481/50, s(70) >= 3463/400 and s(58) >= 1587/200 (02f981a to 797bdf6), each above what the record reported at its count; at n = 88 and 94 above the fourteen's 769/80 and 497/50:
  - T-091, reviewed: its argument has been read here and no blocking defect found, and no replay here has passed yet (V0/C1).

**Not registered.**

- s(96) >= 248/25 = 9.92 (mixed_n96_L992, c5454ae): Raised within this thread by mixed_n96_L996 before any import, so an import at the later pin registers 9.96 alone and this one stays in the packet.

**What is still queued, and how it will be completed.**

- T-082: The complete replays, about 162 CPU-hours planned (179 by the source's own oblique seconds), with devtools.audit_wand125_point_and_mixed mixed-shard wand125-mixed-bounds-2026-10-03 --runners 8 for the ranges, mixed-replay on each and mixed-merge per certificate, before any verified lower bound is raised; a count's verified lower bound moves when its replay returns the certificate's own record at all 201 directions.
- T-090: The complete replays, about 146 CPU-hours planned (180 by the source's own oblique seconds), with devtools.audit_wand125_point_and_mixed mixed-shard wand125-mixed-bounds-2026-10-04 --runners 8 for the ranges, mixed-replay on each and mixed-merge per certificate, before any verified lower bound is raised; a count's verified lower bound moves when its replay returns the certificate's own record at all 201 directions.
- T-090: The complete replays, about 146 CPU-hours planned (180 by the source's own oblique seconds), with devtools.audit_wand125_point_and_mixed mixed-shard wand125-mixed-bounds-2026-10-04 --runners 8 for the ranges, mixed-replay on each and mixed-merge per certificate, before any verified lower bound is raised; a count's verified lower bound moves when its replay returns the certificate's own record at all 201 directions.
- T-091: The complete replays, about 131 CPU-hours planned (138 by the source's own oblique seconds), with devtools.audit_wand125_point_and_mixed mixed-shard wand125-mixed-bounds-evening-2026-10-04 --runners 6 for the ranges, mixed-replay on each and mixed-merge per certificate, before any verified lower bound is raised; a count's verified lower bound moves when its replay returns the certificate's own record at all 201 directions. Five of the bundles record their proof run on macOS arm64, and their replays must return those records exactly.

**On `main`.** [`packing/frontier/RESULTS.md`](https://github.com/jlevy/squares/blob/main/packing/frontier/RESULTS.md), [`docs/project/reviews/review-2026-10-02-wand125-mixed-rectangle-bounds.md`](https://github.com/jlevy/squares/blob/main/docs/project/reviews/review-2026-10-02-wand125-mixed-rectangle-bounds.md), [`packing/frontier/n-037.md`](https://github.com/jlevy/squares/blob/main/packing/frontier/n-037.md), [`packing/frontier/n-065.md`](https://github.com/jlevy/squares/blob/main/packing/frontier/n-065.md), [`packing/frontier/n-066.md`](https://github.com/jlevy/squares/blob/main/packing/frontier/n-066.md), [`packing/frontier/n-090.md`](https://github.com/jlevy/squares/blob/main/packing/frontier/n-090.md), [`packing/frontier/n-092.md`](https://github.com/jlevy/squares/blob/main/packing/frontier/n-092.md), [`packing/frontier/n-084.md`](https://github.com/jlevy/squares/blob/main/packing/frontier/n-084.md), [`packing/frontier/n-085.md`](https://github.com/jlevy/squares/blob/main/packing/frontier/n-085.md), [`packing/frontier/n-086.md`](https://github.com/jlevy/squares/blob/main/packing/frontier/n-086.md), [`packing/frontier/n-087.md`](https://github.com/jlevy/squares/blob/main/packing/frontier/n-087.md), [`docs/project/reviews/review-2026-10-02-wand125-linear-certificates-and-n76.md`](https://github.com/jlevy/squares/blob/main/docs/project/reviews/review-2026-10-02-wand125-linear-certificates-and-n76.md), [`packing/frontier/n-076.md`](https://github.com/jlevy/squares/blob/main/packing/frontier/n-076.md), [`docs/project/reviews/review-2026-10-02-wand125-afternoon-certificates.md`](https://github.com/jlevy/squares/blob/main/docs/project/reviews/review-2026-10-02-wand125-afternoon-certificates.md), [`packing/frontier/STATUS.md`](https://github.com/jlevy/squares/blob/main/packing/frontier/STATUS.md), [`docs/project/reviews/review-2026-10-03-wand125-october-3-certificates.md`](https://github.com/jlevy/squares/blob/main/docs/project/reviews/review-2026-10-03-wand125-october-3-certificates.md), [`docs/project/reviews/review-2026-10-05-wand125-october-4-certificates.md`](https://github.com/jlevy/squares/blob/main/docs/project/reviews/review-2026-10-05-wand125-october-4-certificates.md).

This issue stays open while anything above is queued, and a reply follows each change in the record.

---
_Generated by [Claude Code](https://claude.ai/code)_
