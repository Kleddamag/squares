---
type: is
id: is-01m42xfwp06kzm2b390dx1cw17
title: "Site: publish the shared design system once, cached across pages"
kind: epic
status: open
priority: 1
version: 7
labels: []
dependencies: []
child_order_hints:
  - is-01m42xhs1mmqpv12d1j74rrvey
  - is-01m42xhvh42fy1x77cd5j8c0dc
  - is-01m42xhxk4awqq1jmgzykwdct1
  - is-01m42xhzkhgcrhah1b41gpjxf4
  - is-01m42xj1dc4ez804wdvcv0t2yd
created_at: 2026-10-04T07:36:40.896Z
updated_at: 2026-10-04T07:37:51.276Z
---
Every page inlined ~1.8 MB (0.95 MB gzip) of faces, KaTeX, kpress CSS/JS; a reader re-downloaded it on every page (measured 2026-10-04 with measure_site_pages load --network fast-4g --after index.html: 1.0-1.3 MB per page, cold or warm). Move it to content-hashed files under assets/ (devtools/site_assets.py), in phases.
