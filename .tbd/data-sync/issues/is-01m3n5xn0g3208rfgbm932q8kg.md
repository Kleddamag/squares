---
type: is
id: is-01m3n5xn0g3208rfgbm932q8kg
title: Finish the verified-lane replays of wand125's rectangle certificates so the atlas draws them
kind: task
status: in_progress
priority: 1
version: 4
labels:
  - packing
  - wand125-update
  - review
dependencies:
  - type: blocks
    target: is-01m3n5y05cdnsnkspf7e4vg5jp
parent_id: is-01m3n5wh72rsqd2z97m8v1vv4q
created_at: 2026-09-28T23:34:38.352Z
updated_at: 2026-09-29T01:43:28.355Z
---
Root cause of wand125's 'not reflected yet': the atlas and PDF draw the verified lower bound, and only n = 27 and 31 (28 by monotonicity) have complete replays; the rest of the 44 retained certificates, about 102 CPU-h by upstream per-angle times, plus every new certificate from the re-pin, remain reported. Plan and run the batches (tools: devtools.audit_wand125_rectangles --replay, Tokoharu's unmodified verify.cpp), record receipts, and promote each passing count's verified bound. Budget the CPU honestly; this is the gating item for the atlas refresh.

## Notes

Ten cloud replay batches (full SHA 65526c34, retried 00:57Z after the short-SHA start failure): b01 session_016RkVAZbyeMUwdTDHtSbCbU (sep28 72,56,91,31); b02 session_015e73Kqu8BbGTeFxdX7E4bX (sep28 67,38,29; sep27 30); b03 session_01C3c4tAbqdvDZFWroYDc155 (55,51,42,88); b04 session_011JESrmwLSZhrzBYgqXv5x8 (69,53,41,86); b05 session_01NoBKKKHAeR4sZPqZu1JBg5 (73,54,37,43,44); b06 session_01GV4wkGt3VEh7mSyFEpDTBW (74,66,58,94,57); b07 session_012PMwcf2QSiPtfzB9GGMDRw (sep27 75,40,20,61,26); b08 session_01J9kJSFGBnG6MjUWo5MhszW (sep27 78,18,19; sep28 95); b09 session_01RZQWcNf8a1SKUpzyjcH4DV (52,59,71,39); b10 session_01TzpU5w9Sp969rCi6FpAgG4 (68,28,76,60,70,89). Receipts push to claude/replay-wand125-rect-bNN under transfer/wand125-rect-bNN/. Skipped: n45 (Daniel's s(45)=7 supersedes), n77 (carried from n76 by mass). Merge needs think-0rrj.
