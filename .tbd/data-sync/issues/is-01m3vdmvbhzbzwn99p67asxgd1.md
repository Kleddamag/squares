---
type: is
id: is-01m3vdmvbhzbzwn99p67asxgd1
title: "Standing: no 'current best' chip; 'superseded' marks every result that is no longer the best"
kind: task
status: in_progress
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T09:45:05.134Z
updated_at: 2026-10-01T09:45:09.404Z
---
Owner, 2026-10-01: let's drop 'current best' altogether since it is kind of implicit, and instead make sure 'superseded' reflects when something is no longer best. (1) The result tables and popovers draw no 'current best' chip; a result that still stands shows no standing chip. (2) 'Superseded' is shown on every result that is no longer the best known for its case and direction, derived from the register (a later result with a better bound on the same quantity, or the entry's superseded_by), not hand-set; audit all 61 results and list any that are no longer best but not marked, and any marked that still stand. (3) The standing filter and the 'Current best only' checkbox keep working: the checkbox hides superseded rows. (4) paper-design.md and the Results page prose say what the absence of a chip means.
