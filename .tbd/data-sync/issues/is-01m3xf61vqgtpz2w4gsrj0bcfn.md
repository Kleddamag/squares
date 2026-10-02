---
type: is
id: is-01m3xf61vqgtpz2w4gsrj0bcfn
title: "Papers are individually versioned: the repository's version no longer appears on a paper"
kind: feature
status: in_progress
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-02T04:50:26.294Z
updated_at: 2026-10-02T04:50:27.291Z
---
Owner, 2026-10-01: 'And the repository version should not go on the papers anymore. Papers should be individually versioned in the future.' Today the first paper's credits print the publication's edition and data hash ('v0.5.0-971e5f (version history)'), its Version History lists every publication edition including site-only ones (v0.5.0, 'The website edition'), and the site's colophon with the repository version closes each paper and its PDF; the review already carries its own 'Draft v0.1.0'. Wanted: each paper has its own version and its own history in sqpack.release, written by devtools.paper_front; no repository version or data hash anywhere on a paper page, its Markdown edition or its PDF; the site's pages keep the repository version in their footer. This settles the first of #289's four questions on think-cv22 (the review keeps its own version). Done together with think-be7y in one PR, since both change devtools.cut_release and development.md's Cutting an edition.
