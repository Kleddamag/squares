---
type: is
id: is-01m42xfwp06kzm2b390dx1cw17
title: "[epic] Site: publish the shared design system once, cached across pages"
kind: epic
status: open
priority: 1
version: 1
labels: []
dependencies: []
created_at: 2026-10-04T07:36:40.896Z
updated_at: 2026-10-04T07:36:40.896Z
---
Every page inlined ~1.8 MB (0.95 MB gzip) of faces, KaTeX, kpress CSS/JS; a reader re-downloaded it on every page (measured 2026-10-04 with measure_site_pages load --network fast-4g --after index.html: 1.0-1.3 MB per page, cold or warm). Move it to content-hashed files under assets/ (devtools/site_assets.py), in phases.
