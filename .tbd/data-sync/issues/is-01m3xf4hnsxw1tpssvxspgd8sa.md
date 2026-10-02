---
type: is
id: is-01m3xf4hnsxw1tpssvxspgd8sa
title: "Release procedure: a site version bump needs no tag or GitHub release; a release is cut only to host new generated assets"
kind: task
status: in_progress
priority: 3
version: 2
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-02T04:49:36.950Z
updated_at: 2026-10-02T04:50:27.722Z
---
Owner, 2026-10-01: 'The GitHub releases are not so important for the website. They are only important for the assets that are generated, like the PDFs or the videos.' Today development.md (Cutting an edition) and the text devtools.cut_release prints both end with 'tag the merge and create the GitHub release with the poster PDFs and PNGs attached' as steps left for the owner at every version bump. Bring both in line: the site's version is complete when the merge deploys and check_published_site passes; a release is made when there are assets that need a download address (the films, linked through render_overview.FILM_RELEASE, currently v0.4.2; the posters are served from the site itself). Update the printed steps, the paragraph in development.md and any test that pins the printed text (tests/test_cut_release.py).
