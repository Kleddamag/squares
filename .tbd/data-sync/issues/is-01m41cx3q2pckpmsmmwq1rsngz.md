---
type: is
id: is-01m41cx3q2pckpmsmmwq1rsngz
title: Shrink PR 305's retained data and set one layout for retained JSON results
kind: feature
status: in_progress
priority: 1
version: 6
labels:
  - session-169
dependencies: []
parent_id: is-01m3xgkna3m3w1w50ky6gqyxyk
child_order_hints:
  - is-01m41cx4hamhczdr7c6fmkpy68
  - is-01m41cx57k479tywz7rqpgrceb
  - is-01m41cx5tj7pwgbrbb6dgk27da
  - is-01m41ephbrdagjrq2q882d007z
created_at: 2026-10-03T17:27:33.847Z
updated_at: 2026-10-03T17:58:55.608Z
---
Owner question, 2026-10-03: PR jlevy/squares#305 adds 275,273 lines across 574 files; should it be that big? Measured: 83% of the lines are generated data. The two X-049 censuses (138,135 lines), the T-007 consumer audit (44,882) and the regularized index (15,653) are json.dumps(indent=2), one scalar per line: 198,647 lines for about 2,700 records. Written one record per line they take 2,691 lines and half the bytes, with nothing lost; git stores about 280 KB either way, so gzip would only cost readable diffs. The 51 regularized SVGs are 11 MB, after the house atlas's committed 324 SVGs (52 MB). Owner decision, 2026-10-03: adopt the record-per-line layout in this PR or a PR stacked on it, all in this line of work, tracked by beads and followed up by sub-agents. Children: the four files in PR 305; the repository-wide writer in a stacked PR; and the SVG question.
