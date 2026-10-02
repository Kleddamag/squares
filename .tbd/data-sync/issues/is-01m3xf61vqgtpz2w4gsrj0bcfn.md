---
type: is
id: is-01m3xf61vqgtpz2w4gsrj0bcfn
title: "Papers are individually versioned: the repository's version no longer appears on a paper"
kind: feature
status: in_progress
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-02T04:50:26.294Z
updated_at: 2026-10-02T04:51:49.125Z
---
Owner, 2026-10-01: 'And the repository version should not go on the papers anymore. Papers should be individually versioned in the future.' Today the first paper's credits print the publication's edition and data hash ('v0.5.0-971e5f (version history)'), its Version History lists every publication edition including site-only ones (v0.5.0, 'The website edition'), and the site's colophon with the repository version closes each paper and its PDF; the review already carries its own 'Draft v0.1.0'. Wanted: each paper has its own version and its own history in sqpack.release, written by devtools.paper_front; no repository version or data hash anywhere on a paper page, its Markdown edition or its PDF; the site's pages keep the repository version in their footer. This settles the first of #289's four questions on think-cv22 (the review keeps its own version). Done together with think-be7y in one PR, since both change devtools.cut_release and development.md's Cutting an edition.

## Notes

State at 2026-10-02 03:15 UTC (20:15 PT, 1 October). A Fable subagent started at 03:05 UTC in worktree /Volumes/spud-ext1/agent-scratch/worktrees/overview-papers on branch claude/paper-versions (from origin/main at 0848631a8), covering this bead and think-be7y in one PR. It is told to push after each step and open a draft PR early; find it with `gh pr list --head claude/paper-versions`.

The owner's further words, same evening:
- "at least for the new papers. for the original explainer it has its own versinos but they can be detached from the repo now, and probably we should droip the one "0.4.x" version on that paper if it didn't actually reflect a change in that paper"
- "The version history on any paper and the versions on the paper should reflect versions of the paper, not of the website or anything else."
- "But we don't want to retroactively change any version number that we have published where there's a change of the paper."

So: a published edition under which the paper changed keeps its number and date; an edition under which it did not change (v0.5.0 for certain, and whichever 0.4.x the git history shows) leaves the paper's history; the paper's current version is its last kept number. The repository's version stays the site's (footers, posters, claim documents).
