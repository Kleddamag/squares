---
type: is
id: is-01m3wffybkqpgcsbqk3ej8aebs
title: PDFs and generated files carry the right date
kind: task
status: in_progress
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T19:36:35.954Z
updated_at: 2026-10-01T19:36:36.836Z
---
Owner, 2026-10-01: 'can you confirm the pdf and generated files are using the appropriate date? I saw recent PRs with sept 29 on the pdf.' For every generated artifact that prints or embeds a date (the atlas posters known-best-1-100 and 1-324 in PDF, SVG and PNG; the two papers' PDFs and their 'revised' lines; the films' captions; document metadata such as PDF CreationDate and ModDate; generated Markdown views with 'as of' or 'reviewed' dates): find where the date comes from (a release constant, the data revision's commit date, the build clock, a hand-typed string), what it says today against what it should say (the date of the data it shows), and why a PR on 1 October showed 29 September. Fix each to one documented rule; test it.
