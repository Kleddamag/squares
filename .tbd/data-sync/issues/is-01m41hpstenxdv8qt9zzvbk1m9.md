---
type: is
id: is-01m41hpstenxdv8qt9zzvbk1m9
title: Fetch only main and the PR head in the six full-history CI jobs
kind: task
status: open
priority: 3
version: 1
labels:
  - session-169
  - owner-decision
dependencies: []
parent_id: is-01m41cx3q2pckpmsmmwq1rsngz
created_at: 2026-10-03T18:51:29.997Z
updated_at: 2026-10-03T18:51:29.997Z
---
Six jobs on every PR push (validate, suite-a to suite-d, frontend) use actions/checkout fetch-depth 0, which fetches refs/heads/* and tags: about 950 MB each, 5.7 GB a push. Fetching main and the PR head only would save about 217 MB a job (about 1.3 GB a push), for cycle time (OR-14), not storage; the jobs need main's history for ancestry and provenance checks, which a two-ref fetch keeps. Owner decision on CI configuration.
