---
type: is
id: is-01m3w3hhw6kkk8wfk66wvrbm33
title: "Review 'Standing' on the results table: a workflow status (recorded, reviewed, confirmed, incomplete) in place of the present values"
kind: feature
status: in_progress
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T16:07:45.798Z
updated_at: 2026-10-01T16:08:42.005Z
---
Owner, 2026-10-01: 'another bigger issue, let's also review the "Standing" setting on the results chart. it seems like it isn't very well thought through or useful in its current form with the data. perhaps it could be simplified to reflect the actual workflows, e.g. "recorded" to mean we've recorded the result, "reviewed", "confirmed" if this project has confirmed it, and "incomplete" if it's still a placeholder or has some other notable omissions or issues'. Scope: (1) what Standing is today: its values (current best; current best, reported; superseded; second certificate; reported; the nine non-bounds), how each is derived, how many results carry each, and what a reader can and cannot do with it; (2) a proposal: a status that follows the project's workflow, with the owner's four values as the starting vocabulary, each defined by a predicate over the record (registered; review record present; confirmed by this project per the C ladder; placeholder or with recorded omissions), derived and checked, not hand-set; how it relates to the V and C rungs (no duplication), to 'superseded' (the owner asked on the same day that superseded mark every result no longer the best: keep it as its own mark), to kind (think-69j0) and to the 'not fully assessed' tag (think-d04u, the same field); (3) implement on the branch with the schema, checker, register views, site chip and filter; (4) the classification table for the owner. Same agent as think-d04u.

## Notes

Owner added 2026-10-01: 'That concern should be tracked as a bead and given to the agent that's dealing with the reported awaiting replay issue. We might want a status that indicates results that we are actively analyzing versus waiting on others to respond or clarify.' So the workflow status must be able to tell 'in analysis here' from 'waiting on the source' (a question or request for clarification is open with the author). Assigned to the agent on claude/awaiting-replay together with think-d04u.
