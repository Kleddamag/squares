---
type: is
id: is-01m3xjzm0199pssnrkahhwqb6t
title: "Overview: drop The Frontier Survey section; one Frontier Survey card joins the page cards under The Squares Project, and those cards sit in two rows"
kind: task
status: in_progress
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-02T05:56:49.792Z
updated_at: 2026-10-02T07:38:44.700Z
---
Owner, 2026-10-02: 'and drop the whole section: The Frontier Survey — The frontier survey is the record the atlas is drawn from: … when a bound by others counts as verified. — and then move one Frontier Survey card to the top below The Squares Project headers, and put the cards into two rows instead of one'. The Overview loses The Frontier Survey heading, its paragraph and its two cards (added in #299). One Frontier Survey card (the one to the Frontier page, every case from n = 1 to 324) joins the page cards under The Squares Project (today four: the optimality paper, the explainer, the tutorial, the workbench), and that group is laid out in two rows instead of one. Every inbound link to the Overview's #the-frontier-survey (README, other pages) is repointed to the Frontier page.

## Notes

2026-10-02 07:40 UTC, branch claude/amazing-bohr-ytjim9 off origin/main 81cb5716 (jlevy/squares#304 merged hqb3, wz9d, l38m; the old branch had no ec5k work). PR jlevy/squares#306: 322ef34cd (this bead) and 7b1142497 (tests: the Frontier math-face test no longer asks for the subtitle wz9d removed, red on main; the card-lines refusal through page_cards). Done: The Frontier Survey section, its paragraph and two cards gone; the card to every case (frontier.html) is the fifth page card; the recent-cases card went. Page cards stand two over three (SECTION_CARD_LINES = {pages: (2, 3)}: one frame, a grid per line, each capped at three medium columns by data-cards-most), chosen over three over two from shots at 1280. forward.js sends #the-frontier-survey and #the-survey to frontier.html. README and epistemics.md repointed; paper-design.md updated. Push tier at 322ef34cd: 3761 passed, 3 failed (math-face fixed in 7b1142497; two fixed_core_packet reaping tests fail in this sandbox on code identical to main); rerun at 7b1142497 in progress. Close when #306 merges.
