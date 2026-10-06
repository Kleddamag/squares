---
type: is
id: is-01m421pnn9vr4pfhrmc9dwcs8t
title: "n = 12: the reported lower bound sits below the verified one, so T-078 still holds it"
kind: bug
status: open
priority: 2
version: 3
labels: []
dependencies: []
parent_id: null
created_at: 2026-10-03T23:31:02.952Z
updated_at: 2026-10-06T08:27:18.114Z
---
Found in the review of jlevy/squares#315 (think-rf21). packing/frontier/n-012.md records reported_lower_bound 3.969117 (T-078) and verified_lower_bound 3.970200 (T-079). A reported bound below the verified one leaves T-078 holding the reported lower bound, though T-079's notes say it supersedes T-078; the derived successor lists read 'superseded by T-078 and T-079' for T-049 and T-017. Decide whether the reported lower bound should be raised to the verified value when the verified one passes it (a data fix on main), or whether standing should ignore a reported bound below the verified one.
