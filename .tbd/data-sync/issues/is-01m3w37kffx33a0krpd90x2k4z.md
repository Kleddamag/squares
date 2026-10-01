---
type: is
id: is-01m3w37kffx33a0krpd90x2k4z
title: "Homepage: 'Reported, awaiting replay' is not a separate ad hoc block; those results sit with the main results, each with its current status"
kind: task
status: in_progress
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T16:02:19.756Z
updated_at: 2026-10-01T18:15:21.614Z
---
Owner, 2026-10-01: 'I have previously asked about the block "Reported, awaiting replay" on the main page. It doesn't make sense for this to be separated the way it is. Can you assign an agent specifically to this and be sure we understand where it's coming from and why it's not just integrated in a sensible way, systematically with our main results? Reflect the current status of each of these results. It should not appear in this ad hoc way on the main page.' Trace where the block comes from (which code, which data, which commit and bead introduced it, what the earlier request was), what each listed item is today (registered result or only a case-record report; its rungs, standing, evidence, whether a replay has since happened), and why it is outside the results table. Then integrate: every such item is a row of the one results table with its real status (V0/C0 or 'reported' standing, a filter value), or is dropped from the homepage if it is not a result; no separate block.

## Notes

See think-ai94; draft jlevy/squares#277.
