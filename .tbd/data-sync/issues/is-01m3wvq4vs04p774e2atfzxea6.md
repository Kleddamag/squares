---
type: is
id: is-01m3wvq4vs04p774e2atfzxea6
title: "Housekeeping after 1 October: worktrees, merged branches, scratch builds, orphaned processes"
kind: task
status: open
priority: 3
version: 1
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T23:10:14.903Z
updated_at: 2026-10-01T23:10:14.903Z
---
The external drive is 96% full. After the open PRs land: remove merged agent worktrees under /Volumes/spud-ext1/agent-scratch/worktrees (keep those with open branches), delete merged remote branches (claude/site-polish-*, claude/prose-*, claude/result-kinds, claude/site-coherence, claude/paper-*, claude/awaiting-replay, claude/register-rung-residue, claude/release-assets-on-demand, and the per-lane branches), remove the squares-site-* preview builds except the one being served on localhost:8000, and check for orphaned playwright and multiprocessing processes from stopped agents (several were found idle or spinning for four to five hours on 1 October). Nothing is deleted without looking at it first.
