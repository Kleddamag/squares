---
type: is
id: is-01m41cx57k479tywz7rqpgrceb
title: Adopt the record-per-line writer for every large retained JSON result (stacked PR)
kind: task
status: in_progress
priority: 2
version: 2
labels:
  - session-169
dependencies: []
parent_id: is-01m41cx3q2pckpmsmmwq1rsngz
created_at: 2026-10-03T17:27:35.411Z
updated_at: 2026-10-03T17:29:56.716Z
---
In a PR stacked on jlevy/squares#305: inventory every tracked JSON result over about 5,000 lines (chunk-components.json at 365,916, the agenda-033/040/031 results near 180,000, session-153-native-full.json, exp-042's paths, chunk-partitions.json, translation-escape-screen.json and the rest), find the writer of each, move each writer onto the shared record-per-line writer from think-1uwx, regenerate, and keep every --check, digest and release pin consistent. Document the layout in development.md as the convention for retained JSON, and add a check that a retained JSON result over a line threshold uses it. Files whose bytes are bound by a digest, a pinned release or an external source are listed and left alone with the reason.
