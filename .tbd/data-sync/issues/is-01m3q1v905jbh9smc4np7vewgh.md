---
type: is
id: is-01m3q1v905jbh9smc4np7vewgh
title: "Overview: drop the synopsis page; link GitHub documents as cards"
kind: feature
status: open
priority: 2
version: 6
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-09-29T17:01:55.076Z
updated_at: 2026-09-30T05:04:42.881Z
closed_at: null
close_reason: null
resolution: null
duplicate_of: null
---
RC 2026-09-29: drop the synopsis site page and link the GitHub docs as cards on the overview, including the Synopsis and the README. Done in 200b384a8: synopsis page, nav item and deploy input removed; SYNOPSIS.md links go to GitHub; 'On GitHub' section with eight document cards.

## Notes

Close reason correction: done on claude/overview-page-impl and shown in the private preview; RC's full review and the push are still pending.

Reopened: Done only on claude/overview-page-impl, which was never pushed; the owner asked on 2026-09-30 that it be treated as lost. The decision is carried in the revised spec (plan-2026-09-29-github-pages-overview.md) and the work is to be redone.

Reopened: Closed too early: the data and explainer parts landed (8c24872ae, 14cb1c051), but the overview page's own rendering of these sections is lane B's and has not landed yet.
