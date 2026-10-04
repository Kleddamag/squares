---
type: is
id: is-01m4219scr8whmzt1xxq4kb1pn
title: "Colour tokens: hold each page's own stylesheets to declaring every token it paints with"
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m41d7edgm9wc99zdrkaa5ehy
created_at: 2026-10-03T23:24:00.791Z
updated_at: 2026-10-03T23:24:00.791Z
---
check_colour_tokens.undeclared_paint_tokens pools the declarations of every served stylesheet and KPress's, so a site.css rule painting with a token only paper-publication.css declares would pass and paint nothing on the site. Check per page's actual stylesheet set (site pages: site.css, site-nav.css, site-result.css and KPress; papers: paper-publication.css and their own). Found by the review of the significance branch (think-uer5); nothing undeclared today when checked per set by hand.
