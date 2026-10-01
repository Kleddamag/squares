---
type: is
id: is-01m3wbd2vc3yzjczyhg3kqt775
title: "Social cards: clean Open Graph and Twitter metadata on every page, with the hero graphic (n = 53) as the image"
kind: task
status: in_progress
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T18:25:07.941Z
updated_at: 2026-10-01T18:25:10.455Z
---
Owner, 2026-10-01: 'we should fix the opengraph and other social media card info to be clean on all the pages on the site. we should use the hero graphic (n=53) as the social graph image'. Every page (KPress pages, both papers, the workbench, document pages, forwarders): og:title, og:description, og:type, og:url (the page's canonical URL), og:site_name 'The Square Packing Project', og:image with width, height and alt, twitter:card summary_large_image with title, description and image, a canonical link, and a meta description; one definition feeds all page kinds. The image is the homepage hero (the n = 53 packing) rendered to a 1200x630 PNG at build time from the committed drawing, served from the site at an absolute URL; checked by check_published_site.
