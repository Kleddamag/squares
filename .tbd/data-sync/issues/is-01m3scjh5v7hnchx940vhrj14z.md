---
type: is
id: is-01m3scjh5v7hnchx940vhrj14z
title: Measure live CI wall time despite missing step timestamps
kind: bug
status: in_progress
priority: 1
version: 5
labels: []
dependencies: []
parent_id: is-01m3qcan8g6wnnpkvaemzt7rfm
created_at: 2026-09-30T14:47:51.737Z
updated_at: 2026-09-30T15:05:15.365Z
---
At c32fd6f73, allindividualchecks andPages pass; Packing run36730867640 aggregate failed solely because jobsAPI omitted the live wall-step started_at for3reads. Add bounded specific eventual-consistency retry with refusal after exhaustion; preserve required-prerequisite and mixed-cohort safeguards and unchanged cost limits. Focus tests, publish and require full aggregate green.

## Notes

fa94d63b9 run36732391130 still failed after seven API reads: the live jobs list omitted the running wall step. Both behavioral shards and Pages passed; validate found open think-e2ot under closed composition parent, now reparented to think-7nkq and check_bead_tree passes. Sol is replacing unreliable self-observation with a conservative invocation-time endpoint bound to the live run/job/attempt; no budget or prerequisite checks may weaken.
