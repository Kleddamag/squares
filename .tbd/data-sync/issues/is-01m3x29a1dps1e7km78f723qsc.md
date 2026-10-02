---
type: is
id: is-01m3x29a1dps1e7km78f723qsc
title: "Handoff: the website lane at the end of 1 October 2026 — what merged, what is in flight, what is the owner's"
kind: task
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-02T01:05:01.478Z
updated_at: 2026-10-02T01:05:01.478Z
---
Handoff of the website lane (epic think-xjq4) at 2026-10-02 01:35 UTC, 18:35 PT on 1 October. Read this first, then the beads it names.

**Merged on 1 October, all deployed:** #254 #255 #261 #262 #264 #265 #266 #267 #269 #270 #271 #274 #275 #276 #277 #278 #284 #285 #286 #287 #288 #289, and #291 (v0.5.0) as 8aaa411dc. The deployment of 07f014386 was verified (check_published_site 848 of 848; homepage, both papers and the atlas Triangle view read in a browser). The deployment of 8aaa411dc was running when this was written.

**In flight**

1. think-pt1k, v0.5.0: verify the deployment of 8aaa411dc, record it above PUBLICATION_HISTORY, then bring the tag and GitHub release to the owner. Steps and commands are in that bead's notes.
2. think-f1tu (children think-sv92, think-ekw5, think-dj7y), the Overview restructure: a subagent on branch claude/overview-structure in worktree overview-result-pop; a draft PR is to be opened by it. Review it, mark it ready and merge when clean.
3. think-sib7, P1 bug: main's post-merge validate job fails eleven table-layout tests on Linux at 07f014386, on both attempts of run 36943941580. They pass on macOS and the live site is unaffected. Main shows red until this is settled; the bead has the evidence and three steps to decide it.
4. think-t7k5: record suite_d's first measurement and rebuild the shard cost record from a green four-shard main run; the pending rule expires 2026-10-08.

**Owner decisions outstanding:** one list on think-cv22 (credits of T-025/026/031/033/009; status vocabulary and T-065's credit; result kinds; nav bar name; page titles and social card; tables below 1280; the review paper's version line, first-published day and repository line; whether PDFs and Videos sits right after the survey). Plus the v0.5.0 tag and release, and the wording of v0.5.0's scope sentence.

**Not this lane's:** #283 (research), #290 and #292 (the result import process) belong to other sessions and were not touched.

**How things work here** (also in the memory file project-site-pr-stack-2026-10-01): `gh pr merge N --merge` for a plain PR and `gh stack merge <top> --yes --merge` for a stack; `gh run rerun <id>` with no `--failed`; never change packing/pyproject.toml; data-path commits re-pin with `devtools.release_pin --update`; subagents on `model: fable` until the Opus limit resets on 4 October 23:00 PT; scratch on /Volumes/spud-ext1/agent-scratch (about 20 GB free). Housekeeping of worktrees and branches: think-d5l5.

**Follow-up beads still open from the day:** think-gv85, think-dda6, think-irsg, think-54rr, think-c4as, think-9y87, think-k8xp, think-3qn8, think-zb0i, think-b245, think-h896.
