---
type: is
id: is-01m3srwp77hjebx7ryvnsxa8fa
title: Keep terminal synopsis handoff and mutation anchor aligned after formatting
kind: bug
status: in_progress
priority: 2
version: 5
spec_path: docs/project/specs/active/plan-2026-09-29-proof-verification-consolidation.md
labels: []
dependencies: []
parent_id: is-01m3sk1aq5e7wm2hzghg3wf499
created_at: 2026-09-30T18:23:07.481Z
updated_at: 2026-09-30T19:16:28.668Z
closed_at: null
close_reason: null
resolution: null
duplicate_of: null
---
PR250 run36757489226 at7c8ed1116 failed synopsis and negative-control checks: Flowmark joined the handoff opening onto the previous paragraph, defeating the line-anchored parser, and controls.yaml still targets think-niqx instead of selected think-e2ot. Repair the paragraph boundary and registered mutation anchor, then run the two affected behavioral controls and source checkers after normal formatting. No mathematical checker change.

## Notes

Post-merge source-bound failure: run 36761793749, head 3687d9cba3033d6fdd5942150566b5fca4846c5c, deferred-controls-finer job 110045933934. In packing/devtools/controls.yaml:1330-1334, replacement target is think-e2ot→think-cyko but expect still says think-niqx. Actual check_synopsis refusal says Current Handoff must contain exactly one canonical Selected next entry marker for think-e2ot. Negative controls 171/172 fired; the 1440-step finer-net limit record agreed with its source certificate. No mathematical certificate failure is implied.
