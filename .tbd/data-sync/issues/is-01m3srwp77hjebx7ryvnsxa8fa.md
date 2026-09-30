---
type: is
id: is-01m3srwp77hjebx7ryvnsxa8fa
title: Keep terminal synopsis handoff and mutation anchor aligned after formatting
kind: bug
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-09-29-proof-verification-consolidation.md
labels: []
dependencies: []
parent_id: is-01m3sk1aq5e7wm2hzghg3wf499
created_at: 2026-09-30T18:23:07.481Z
updated_at: 2026-09-30T18:54:13.721Z
closed_at: 2026-09-30T18:54:13.720Z
close_reason: The handoff paragraph boundary and current mutation anchor were repaired in 150f8b0dd; two affected focused controls, synopsis and 172 anchor checks passed locally. PR250 final head 461b0f5d5 passed its required hosted checks and merged as 3687d9cba3033d6fdd5942150566b5fca4846c5c. No mathematical source or receipt changed.
resolution: null
duplicate_of: null
---
PR250 run36757489226 at7c8ed1116 failed synopsis and negative-control checks: Flowmark joined the handoff opening onto the previous paragraph, defeating the line-anchored parser, and controls.yaml still targets think-niqx instead of selected think-e2ot. Repair the paragraph boundary and registered mutation anchor, then run the two affected behavioral controls and source checkers after normal formatting. No mathematical checker change.

## Notes

Focused repair committed150f8b0dd. After normal Flowmark hook, affected behavioral controls2passed44.02s (38.11s snapshot setup; maincall5.11s), check_synopsis and172anchorcheck pass. Earlier local mutation execution used isolated uv environment missing PyYAML; final run bound UV_PROJECT_ENVIRONMENT to synced rootvenv with UV_NO_SYNC1 and isolated/snapshot PYTHONPATH. Hosted rerun pending; no mathematical code or evidence changed.
