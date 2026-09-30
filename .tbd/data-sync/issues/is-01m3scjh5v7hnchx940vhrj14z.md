---
type: is
id: is-01m3scjh5v7hnchx940vhrj14z
title: Tolerate bounded jobs-API lag in the live CI wall audit
kind: bug
status: in_progress
priority: 1
version: 3
labels: []
dependencies: []
parent_id: is-01m3qcan8g6wnnpkvaemzt7rfm
created_at: 2026-09-30T14:47:51.737Z
updated_at: 2026-09-30T14:53:05.203Z
---
At c32fd6f73, allindividualchecks andPages pass; Packing run36730867640 aggregate failed solely because jobsAPI omitted the live wall-step started_at for3reads. Add bounded specific eventual-consistency retry with refusal after exhaustion; preserve required-prerequisite and mixed-cohort safeguards and unchanged cost limits. Focus tests, publish and require full aggregate green.

## Notes

Published fa94d63b9: original3readsettlement plus bounded2/4/8/12s fallback onlyforcoherent live aggregator missingits wall-step timestamp.77 focusedtests/staticpass; exhausted/completed/inconsistent guardsretained. FinalheadCIpending.
