---
type: is
id: is-01m3v4n7pnw3btcp0q6cpqcq8k
title: Classify every result by kind (lower bound, upper bound, optimality, simplification, …) and retire the 'not a bound' tag
kind: feature
status: in_progress
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T07:08:00.595Z
updated_at: 2026-10-01T08:58:14.178Z
---
Owner, 2026-10-01: 'I also had asked for a bead around classifying all the results as lower bound or upper bound or optimality or simplification or possibly others. It shouldn't block this work but it's an important refinement. We should not have a tag "not a bound" as that is too vague.' The original bead was never synced from the cloud sandbox. Scope: (1) a required kind on every entry of packing/frontier/results.yaml, with a closed vocabulary in the schema: lower bound, upper bound, optimality (an exact value settled), simplification (a shorter or cleaner proof or certificate of a known result), and whatever else the 61 entries actually need, each named for what it is (for example rigidity or local isolation, case exclusion, erratum or correction, second certificate, audit); propose the vocabulary from the register and have the owner confirm it. (2) check_results enforces it, and derives or cross-checks it against the claim where it can. (3) The standing 'not a bound' (render_recent_results, overview_sections.NOT_A_BOUND_LABEL, the all-results prose, paper-design.md) is retired: a result that is not a bound shows its kind instead. (4) The site shows the kind as a chip or column and filters by it in the shared filter bar; RESULTS.md groups or labels by it. A separate PR after the website, ladder and prose-cleanup PRs, since all of them edit results.yaml; not blocking.
