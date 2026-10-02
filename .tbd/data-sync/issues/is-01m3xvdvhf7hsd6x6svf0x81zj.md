---
type: is
id: is-01m3xvdvhf7hsd6x6svf0x81zj
title: "Import wand125: rectangle certificate s(93) >= 973/100 at 06eeb40 (no request; found in triage of #294)"
kind: task
status: open
priority: 3
version: 2
labels:
  - result-import
  - packing
dependencies: []
parent_id: is-01m3yrdxte02c7bnygkke34ct4
created_at: 2026-10-02T08:24:24.879Z
updated_at: 2026-10-02T16:53:36.183Z
---
Unrequested claim (runbook stage 1, step 2): wand125/square-packing-bounds 06eeb40 adds rect_n93_L973, s(93) >= 973/100, raising the reported 9.7225 (T-068's rect_n93_L9725), checked by Tokoharu's verify.cpp a75140df (the 09-28 rectangle packet's checker). Same commit adds rect_n59_L79375 and rect_n77_L894, both below values the record already holds (no entry). Import: a packet at 06eeb40, a new entry (a later release raising a count), replay ~upstream per-angle CPU.
