---
type: is
id: is-01m3n5xn0g3208rfgbm932q8kg
title: Finish the verified-lane replays of wand125's rectangle certificates so the atlas draws them
kind: task
status: in_progress
priority: 1
version: 3
labels:
  - packing
  - wand125-update
  - review
dependencies:
  - type: blocks
    target: is-01m3n5y05cdnsnkspf7e4vg5jp
parent_id: is-01m3n5wh72rsqd2z97m8v1vv4q
created_at: 2026-09-28T23:34:38.352Z
updated_at: 2026-09-29T00:29:14.676Z
---
Root cause of wand125's 'not reflected yet': the atlas and PDF draw the verified lower bound, and only n = 27 and 31 (28 by monotonicity) have complete replays; the rest of the 44 retained certificates, about 102 CPU-h by upstream per-angle times, plus every new certificate from the re-pin, remain reported. Plan and run the batches (tools: devtools.audit_wand125_rectangles --replay, Tokoharu's unmodified verify.cpp), record receipts, and promote each passing count's verified bound. Budget the CPU honestly; this is the gating item for the atlas refresh.
