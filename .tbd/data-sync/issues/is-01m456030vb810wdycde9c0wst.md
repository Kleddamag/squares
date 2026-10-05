---
type: is
id: is-01m456030vb810wdycde9c0wst
title: "Senior code review of PR 353's tooling: intake_sweep, capture_kingbird_catalogue, deferral guard, derive_kingbird_facts, upper_bound_packets chaining, audit_guzhou_r071, compare_site_floors"
kind: task
status: open
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m44qz0rxvkakmyqaj7qdgagv
created_at: 2026-10-05T04:43:49.146Z
updated_at: 2026-10-05T05:12:19.575Z
---

## Notes

Review of PR #353 Python/config (2026-10-05, reviewer sub-agent, scratch worktree /home/user/squares-lanes/rev-code at 24979c50b). Gates: ruff check + format --check and basedpyright clean on all 50 changed .py files; 105 new tests + 610 changed tests pass (19 skips = no Chromium, test_site_frontier_table); bead tree + soft-schema steps pass; apply_upper_bound_packets --check exit 0.
Findings (each reproduced):
A blocking: intake_sweep.py:413-416 treats every register /tree/<sha> URL as a whole-tree pin, which masks _unretained. At head 8aa6a10b with the record's pins the sweep reports no unretained commits; with acquisition-record pins alone it reports exactly 1ebd484 and c56b9b7, the docstring's own examples. Today wand125's register pin at 797bdf6e (the head) disables the check for that repo.
B should-fix: blocked_on fires on ANY resolved ref (intake_sweep.py:883); result-requests.schema.yaml:47 says once EVERY one has resolved.
C should-fix: _WAITING matches past-tense notes; online run flags think-e6ss from "was held for jlevy/squares#305, which merged 2026-10-04".
D should-fix: dead_deferral runs in --fast CI against origin/tbd-sync; closing think-uu60 turns every PR red with no tracked change (simulated).
E should-fix: gh_fetch paging rewrite has no test; per_page>100 truncates after page 1.
F should-fix: audit_guzhou_r071 ledgers exits 0 when theorem_agrees has a False check (reproduced).
G should-fix: --parse-revision is free text; no digest of the parse bytes is recorded.
nits: Decimal InvalidOperation uncaught in geometry_from_parse:551; LIVE excludes tbd 'deferred' but runbook:180 says 'closed'; deferrals() docstring overstates the schema; _comparable ignores curly single quotes; non-atomic writes in capture_kingbird_catalogue/compare_site_floors.
