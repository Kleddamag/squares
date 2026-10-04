---
type: is
id: is-01m41d7k4fe8tbgjcqxejavg5k
title: "Site colours: every colour a named token, enforced by a test"
kind: task
status: open
priority: 2
version: 7
labels: []
dependencies: []
parent_id: is-01m41d7edgm9wc99zdrkaa5ehy
created_at: 2026-10-03T17:33:17.327Z
updated_at: 2026-10-04T01:03:50.623Z
---
Owner, 2026-10-03: all colours like the significance teal are logical CSS variables, so they can be changed in one place, and the design system enforces it. Tokenize the literal colours in the site stylesheets (shadows, the popover scrim, color-mix tints, the star's red) and add a check that no rule outside a custom property declaration names a colour of its own.

## Notes

State 2026-10-04 00:55 UTC: in jlevy/squares#330 at 2368107da (with #315's 6c5036895), stacked on #315; hosted CI running (green at c8b03f91d); local push gate passes but for the two sandbox-only tests. Reviewed by a strong-tier agent (think-uer5). Closes when #330 merges, after #315.
