---
type: is
id: is-01m3w37j410apfmy2h5m0wqvc8
title: Papers live under papers/ with simple slugs, in URLs and in the source
kind: task
status: in_progress
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T16:02:18.368Z
updated_at: 2026-10-01T16:02:19.567Z
---
Owner, 2026-10-01: 'for papers we should update the URLs to match the site: explainer.html -> papers/n11-lower-bounds.html; n11-optimality/t-060-explainer.html -> papers/n11-optimality-review.html. Papers should have those simple slug names internally and externally. Or we could make it n11-lower-bounds-explainer.html for consistency.' Slugs taken: papers/n11-lower-bounds-explainer.html and papers/n11-optimality-review.html (each slug says the case, the subject and the kind of paper). Externally: the published paths, with the Markdown and PDF beside each under the same slug, and the old URLs (explainer.html, n11-optimality/t-060-explainer.html and its index, .md, .pdf) forwarding so no inbound link breaks. Internally: the renderers, templates, stylesheets, Pages jobs, tests, the Paper records (overview_sections.PAPERS), SITE_PAGES, repo_links, check_published_site and every link in reader documents use the slug names. The tutorial's place (papers/tutorial.html?) is proposed, not assumed.
