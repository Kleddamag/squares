---
type: is
id: is-01m45f3gxdbms4wekyer6s1j9e
title: "Address PR #360 Review B (round 1) and the stack-level review of stack 357"
kind: chore
status: in_progress
priority: 1
version: 5
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m456snzxb4mjvrjh0amapqg3
child_order_hints:
  - is-01m45f3m155h382vqmatedev88
  - is-01m45f3q24s4j810mkkrpmtdfq
  - is-01m45f3t5nfmgpft4nshfjy9xk
hold: null
hold_until: null
created_at: 2026-10-05T07:22:58.861Z
updated_at: 2026-10-06T08:09:49.874Z
started_at: 2026-10-06T08:09:49.874Z
---
Review B (senior, round 1, with the stack-level review) on jlevy/squares#360 (fixed-witness certificates layer, top of stack 357, rebuild of #352), pinned to head 451154f60: https://github.com/jlevy/squares/pull/360#pullrequestreview-5411026851. Layer verdict: approve after B1 and B2, once CI is green. Stack verdict: well organized, not yet ready; what remains is #347 B1 (think-jhgi), green CI on every layer (think-umlx) and the per-layer Medium findings. Findings: B1 BASE_REVISION provenance (child); B2 Sessions 177-179 merge uncertified (think-q0z7); B3 wording overstates the evidence (child); B4 body Validation (child). Stack-level merge order: #347 green + B1; green CI on #354-#360 and the session certifications; gh stack merge 360 --yes --merge (owner runs it); then #350 retargeted to main. #352 stays open until #360 is green. Draft PR; mark ready before the stack merges. Closes when every finding is closed and the dispositions reply is posted.
