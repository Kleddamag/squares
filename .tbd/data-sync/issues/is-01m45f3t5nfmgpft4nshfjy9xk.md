---
type: is
id: is-01m45f3t5nfmgpft4nshfjy9xk
title: "PR #360 B4 (Low): update the body's Validation after a full run"
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m45f3gxdbms4wekyer6s1j9e
created_at: 2026-10-05T07:23:08.340Z
updated_at: 2026-10-05T07:23:08.340Z
---
Review B finding B4 on jlevy/squares#360 (https://github.com/jlevy/squares/pull/360#pullrequestreview-5411026851), at head 451154f60. The body says 'Hosted: pending'; at 451154f60 the run was cancelled (validate, suite-b, frontend, macos-portability and the required roll-ups; latest run 37274530812 also cancelled). Fix: update it after a full run.
