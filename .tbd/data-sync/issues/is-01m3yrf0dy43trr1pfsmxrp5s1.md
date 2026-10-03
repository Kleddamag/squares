---
type: is
id: is-01m3yrf0dy43trr1pfsmxrp5s1
title: "Stacked PR on #298: verifier provenance and the independent verifier"
kind: task
status: in_progress
priority: 1
version: 3
labels:
  - verifiers
dependencies: []
parent_id: is-01m3yrdxte02c7bnygkke34ct4
created_at: 2026-10-02T16:51:51.358Z
updated_at: 2026-10-03T05:00:25.693Z
---
Branch stacked on claude/zealous-gauss-jem7l9; carries the verifier-provenance epic and the independent-verifier slices. Draft until its lanes land; green and mergeable after #298. Merge order #290 -> #292 -> #298 -> this.

## Notes

Branches to stack (all pushed): claude/lane-x-verifier-provenance, claude/lane-w1-verifier-spec, claude/lane-w2-fast-verifier-wip. Base: claude/zealous-gauss-jem7l9 after the records lane's pushes. After merging, re-run packing/devtools/backfill_verifier_relation.py (lane X) on the merged evidence.yaml rather than hand-resolving conflicts; render views; open as draft PR with base claude/zealous-gauss-jem7l9. Full state: think-20pp notes.
