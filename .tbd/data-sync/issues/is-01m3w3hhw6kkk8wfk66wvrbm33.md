---
type: is
id: is-01m3w3hhw6kkk8wfk66wvrbm33
title: "Review 'Standing' on the results table: a workflow status (recorded, reviewed, confirmed, incomplete) in place of the present values"
kind: feature
status: in_progress
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T16:07:45.798Z
updated_at: 2026-10-01T18:15:19.387Z
---
Owner, 2026-10-01: 'another bigger issue, let's also review the "Standing" setting on the results chart. it seems like it isn't very well thought through or useful in its current form with the data. perhaps it could be simplified to reflect the actual workflows, e.g. "recorded" to mean we've recorded the result, "reviewed", "confirmed" if this project has confirmed it, and "incomplete" if it's still a placeholder or has some other notable omissions or issues'. Scope: (1) what Standing is today: its values (current best; current best, reported; superseded; second certificate; reported; the nine non-bounds), how each is derived, how many results carry each, and what a reader can and cannot do with it; (2) a proposal: a status that follows the project's workflow, with the owner's four values as the starting vocabulary, each defined by a predicate over the record (registered; review record present; confirmed by this project per the C ladder; placeholder or with recorded omissions), derived and checked, not hand-set; how it relates to the V and C rungs (no duplication), to 'superseded' (the owner asked on the same day that superseded mark every result no longer the best: keep it as its own mark), to kind (think-69j0) and to the 'not fully assessed' tag (think-d04u, the same field); (3) implement on the branch with the schema, checker, register views, site chip and filter; (4) the classification table for the owner. Same agent as think-d04u.

## Notes

Draft jlevy/squares#277 (claude/awaiting-replay). Plan: docs/project/specs/active/plan-2026-10-01-result-status.md. Finding: the block's 48 rows were two register entries (T-046, T-048) written out case by case, a port of a README table; removed. Also found: complete replays of T-048, T-055 and 21 of T-046's certificates passed on 29 September and sit on unmerged transfer branches; the three entries now say 'in analysis here'. Owner to confirm: the vocabulary, the rung at which a result is confirmed, the activity mark (in analysis here / waiting on others).
