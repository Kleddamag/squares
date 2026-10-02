---
type: is
id: is-01m3yrdxte02c7bnygkke34ct4
title: Import, confirm and answer every reported result (2 October 2026 effort)
kind: epic
status: open
priority: 1
version: 21
labels:
  - result-import
dependencies: []
parent_id: is-01m3wvgebtkjqb3km59h7768zx
child_order_hints:
  - is-01m3yreyarxjm3sv4f4m5g4gyn
  - is-01m3yrezbcgcr728c37fq49bvf
  - is-01m3yrf0dy43trr1pfsmxrp5s1
  - is-01m3yrf1pvmgmydcqjn2qssw1z
  - is-01m3yrf30j3g4mng5fjgars13w
  - is-01m3yrf43whatj7rsvfbkqnaca
  - is-01m3yrf5bp4ngk5a0a4tprhz2r
  - is-01m3wyad4yp229ckemcctd6zkr
  - is-01m3xrx5xc165z1jkhccsrasc9
  - is-01m3xrx6p081zyj7efn8tjkqw0
  - is-01m3wyah4pvzsny49hfj5y9zst
  - is-01m3wyaf139nw81xjkwm1ggk3b
  - is-01m3wyajwc1tbyq4f2rbhjhqdh
  - is-01m3xrx8b86kp8t1k6gj71p4ej
  - is-01m3xvdvhf7hsd6x6svf0x81zj
  - is-01m3yrzkz80qd1wv5sjr0kkkv0
  - is-01m3yrzmzcpq964zt2kr14w8jv
  - is-01m3ytdhr6h2xnsvj4f2nc2nk2
created_at: 2026-10-02T16:51:15.917Z
updated_at: 2026-10-02T20:47:25.896Z
---
Umbrella for the 2 October 2026 effort: PRs #290 -> #292 -> #298 (imports and records), plus a stacked PR for verifier provenance and the independent verifier. Children track each lane; done when every reported result is confirmed or refuted (or has a bead naming exactly what remains), every issue has a current status reply, closeable issues are closed, and all PRs are merged.

## Notes

## Handoff state, 2026-10-02 20:20 UTC (coordinator session_01HbQD6XX8UwXyhUcQ7fCG46)

Stack: #290 -> #292 -> #298 (branch claude/zealous-gauss-jem7l9, draft) -> stacked verifier PR (think-tatg, not yet opened). Umbrella bead: think-20pp. Validation epic think-or93; issue-reply epic think-jl4z; verifier provenance think-mvkp; independent verifier think-gpe0.

### On #298's branch (pushed, 41ae96c22)
s(77)=9 and s(78)=9 at V3/C3 (T-067); s(76)>=447/50 at V3/C3 (T-072); earlier: s(59), s(60), s(61) V3/C3, T-070, T-045, s(32) replay.

### Finished lane branches waiting to merge into #298 (records lane is merging them; all pushed)
- claude/lane-q-issue-tracking: packing/campaign/result-requests.yaml + devtools/check_requests.py (--report/--backlog/--draft/--github), gate step, stage-7 docs.
- claude/lane-z-s21-s50-receipts-controls: T-048 (s(50) L740) and T-055 (point s(21)) replay receipts + n21 mutation controls.
- claude/lane-t-green-ds7: #308 — check_green_ds7 (exact): Green's DS7 Thm 9 pattern fails k=2 and k=4..17, holds k=3; E-green-* defect-found; no verified bound affected.
- claude/replay-wand125-afternoon-inputs: ten new wand125 certificates at b00fc70 retained + preflight + blind review (register at V0; mixed entry before rectangles, finding AF-6).
- claude/lane-cc-t036-replay: T-036 replay mode; stays C2 (composition note).
- claude/lane-dd-t058-ceiling: T-058 ceiling proved/corrected, V3/C3; review its check_certificate_citations change.

### Records lane (local agent; resumable only in this container) — next batches
Push A: merge the six branches above; record T-048, T-055 (controls: receipts/controls/n21_control_*.log). Push B: T-071 (n84 m2, n85 m3 receipts), T-069 (n65,n90 m1; n92 m2; n66,n37 m3), T-068 (merge 30 rect transfer dirs from claude/replay-wand125-rect-oct1-r1..r4 with audit_wand125_rectangles --packet 2026-10-01 --merge, then apply_wand125_rectangles), register the ten afternoon certificates at V0. If the lane is gone, a new lane redoes this from these instructions.

### Stacked verifier PR (think-tatg), branches pushed
- claude/lane-x-verifier-provenance: verifiers.yaml (70 programs, 29 external / 41 first-party), `verifiers` field, `shared-components`, independence_record rule, backfill tool (re-run after merging #298's records), VERIFIERS.md, prose rule for "confirmed". Owner decisions open: E-basic-* relation; E-n061 evand replay relation; six reports with checkers not held.
- claude/lane-w1-verifier-spec: plan spec docs/project/specs/active/plan-2026-10-02-independent-measure-verifier.md, author-checker profile (dirty side: research-2026-10-02-author-checker-profile.md, attribution/, profile script — clean-room implementers must not read).
- claude/lane-w2-fast-verifier-wip: clean-room sqverify_fast crate + experiment-loop campaign (WIP; INDEPENDENCE.md is the independence record).

### Replays running on cloud runners (each pushes receipts to its branch)
- Afternoon certs: m3 session_01CzNNdoXQjbXmAfv6zs13w5 (mixed n83 0-135, n87, n91; claude/replay-wand125-mixed-m3), m4 session_01BGKgRZydsHzUGUiZGqNwCm (n83 136-200, n92-L975, n96; claude/replay-wand125-afternoon-m4), m5 session_01HVkqH8HS4iRSVcQERYzDd6 (n85-L946; -m5), r5 session_01Pg9MGThVFSWTpaHTS4ZjcF (rect n42,n70,n20; -r5), linear n82 on r4 session_01TN1ZrwkmHSieu6FsR3FW6R (0-123; claude/replay-wand125-rect-oct1-r4) and session_01XNF82uVWu1g5o9eCCX2zYL (124-200; claude/replay-n77-full). n82 and n83 need linear-merge / mixed-merge after combining both halves.
- T-046 leftovers (09-28 rect n51,57,58,72,73,91): r1 session_01AyjYboxCsdF1iBKigq2iPR, r2 session_01UBNRoxHxsLTNBCfrXqLMyw (transfer/wand125-rect-sept28-*); n37 skipped (dominated by T-069's mixed n37 L644).
- T-073 linear n83 + control: m1 session_01BHPzddeVuWdjN525XZEut4 (claude/replay-wand125-mixed-m1).
- T-064: inputs claude/replay-valid7-inputs (lane Y: plan_valid7_replay, stage_evand_bentz_lean, review-2026-10-02-valid7-independent-checker.md). qx2 shards q1 session_017mu9dcHKeA7ES8RuGqzT8R / q2 session_01PJ7txntsBi6jjiryzRAYsi (~23 CPU-h, producer code -> C3); wand125 independent checker with --guard-d1 w1..w5 sessions session_01R22nsoV18AzemS5GCHGYXT, session_014UhQfsYQoPybryiN3iZVLY, session_0185351vkZWnES4rr5vzafud, session_0186W3uHkAvNKWFP4C9C5DxV, session_018vBSk8uQXXFfXCzD6nW4HT (~216 CPU-h, independent implementation); Lean build lane LL session_01FXttkLyRcYcz2og7DwgWmM (claude/lane-ll-t064-lean). Then `plan_valid7_replay compare` and records per review §8.5/§11.

### Cloud lanes
- BB session_018harhuQFyWjFkbWsNbvPSX (claude/lane-bb-s12-improvement): our own s(12) attempt; Route A verified s(12) >= 1568000/395039 at N=96000 (credit: Levy after squarepacker #309 and Daniel); Route B (LP re-weighting) in progress.
- EE session_01QrRJs7S9BsvVvR9ftP2Jec (claude/lane-ee-t059-census): T-059 12,028-row census running (~9,300 s).
- FF session_01JYBTrMXDhanrMSMeoyHPXj (claude/lane-ff-s61-point): s(61) point-only cover, verified D4 roots; finishing review + handoff.
- AA (local, claude/lane-aa-s12-309-wip): #309 squarepacker s(12) >= 31360/7901 — import, replays, review; attribution squarepacker after Daniel.

### Open decisions for the owner
- T-007 (#295, think-bkqm): decide on PR #305's review before record edits.
- The three provenance questions above.
- Posting issue replies: after merge, `python -m devtools.check_requests --draft N` renders each reply (needs HEAD on main); posting needs the owner's permission (earlier attempt was blocked). Corrections owed on #247, #238, #227.

### How to resume
Fetch the branches above; `tbd show think-20pp` (and children) for per-item next steps; `python -m devtools.check_requests --backlog` lists every entry below V3/C3 with its next_rung. Check runners with get_session / list_events on the session ids above; resend a short "resume" message if one stopped (usage limits stop them).
