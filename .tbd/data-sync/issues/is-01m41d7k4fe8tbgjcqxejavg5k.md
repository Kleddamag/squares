---
type: is
id: is-01m41d7k4fe8tbgjcqxejavg5k
title: "Site colours: every colour a named token, enforced by a test"
kind: task
status: open
priority: 2
version: 8
labels: []
dependencies: []
parent_id: is-01m41d7edgm9wc99zdrkaa5ehy
created_at: 2026-10-03T17:33:17.327Z
updated_at: 2026-10-04T02:18:42.984Z
---
Owner, 2026-10-03: all colours like the significance teal are logical CSS variables, so they can be changed in one place, and the design system enforces it. Tokenize the literal colours in the site stylesheets (shadows, the popover scrim, color-mix tints, the star's red) and add a check that no rule outside a custom property declaration names a colour of its own.

## Notes

State 2026-10-04 02:20 UTC: jlevy/squares#330 at 457937b95 is ready to merge after #315: 29 checks pass, 28 skipped by design; mergeable and clean against #315's branch. Reviewed (think-uer5) and its fixes checked (think-wizo).
