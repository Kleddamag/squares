---
type: is
id: is-01m3w2epwv3nyche0sm30s17y6
title: "Release: name the site's version v0.5.0 once the stack has landed and the deployment is verified"
kind: task
status: open
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T15:48:44.044Z
updated_at: 2026-10-01T15:48:46.712Z
---
Owner, 2026-10-01: 'after all land let's make sure we update the name of the version of the site to v0.5.0', and 'Make sure everything is deployed correctly first.' Order: (1) the remaining PRs land (#266, #271, #270, the coherence fixes); (2) the live site is verified from that main (check_published_site, every page 200, the paper, films, PDFs); (3) the version becomes v0.5.0. Today the version is the git tag and GitHub release v0.4.2: render_overview.FILM_RELEASE, the explainer template's film URLs, README's release link, the atlas stamp (v0.4.2-<data revision>, from release.py), and about 20 files in all name it. Work out what the release procedure is from development.md and release.py (tag, GitHub release with the film and poster assets or the films kept at v0.4.2 and referenced there, DATA_REVISION re-pin, atlas re-stamp, changelog or release notes), propose it to the owner, and carry it out; creating the tag and the GitHub release is outward-facing and needs the owner's go at that point.
