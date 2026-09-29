---
type: is
id: is-01m3nqe3s65axz2b553w4awa2t
title: "README top summary: 'first lower bounds' for 12/20/21 is incorrect, 'only then registers' misstates reported registration, 'Twenty-six' recent count and the star caption's date rule"
kind: bug
status: closed
priority: 1
version: 2
labels:
  - packing
  - documentation
  - wand125-update
dependencies: []
parent_id: is-01m3neehm7hq4apdvzg9925738
created_at: 2026-09-29T04:40:43.558Z
updated_at: 2026-09-29T05:11:43.351Z
closed_at: 2026-09-29T05:11:43.351Z
close_reason: Fixed in 3002ae25c on claude/magical-davinci-ueqmu1-docs-refresh
resolution: null
duplicate_of: null
---
README.md:15-17 claims the first public lower bounds for n = 12, 20, 21; Evan Daniel's 15680/3951 was in his repository from 2026-08-25 (n-012.md:121), before T-017, and DS7 reports size-specific bounds at 19-21 (n-020.md:139, results.yaml:983). README.md:20-24 and :348-352 say every bound is registered only after replay; 28 of the 55 recent bounds are registered as reported first. README.md:46-48 'Twenty-six ... three of them this project's' is now 27 verified-lane stars (55 cases in either lane, 3 new exact values). README.md:64 caption says 'since August 2026'; the rule is RECENT_SINCE = 22 August on the verified lane. Inventory §3.1 items 1-3, 7, 9, 17.
