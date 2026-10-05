---
type: is
id: is-01m46g50d30wjshv5mzscc8bej
title: Verify the wand125 mixed backlog (T-090, T-091, T-094; n != 17) with sqverify_fast on the 201-angle net, and move verified lanes the policy allows
kind: task
status: in_progress
priority: 1
version: 3
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m46g4yac7ewc22drc7twjhy5
hold: null
hold_until: null
created_at: 2026-10-05T17:00:30.498Z
updated_at: 2026-10-05T17:19:52.518Z
started_at: 2026-10-05T17:06:26.474Z
---

## Notes

## Policy (step 1), 2026-10-05 17:20 UTC

What a full sqverify_fast pass at all 201 directions counts for:
- With admission passing (exact premises: mass < n, B(1+D/(1-D^2/4)) < 1, net pinned at step 83/40000 to index 200, per-bin domain for format M), every direction `verified`, summary `VERIFIED`, exit 0, at the declared threshold 1, it proves s(n) >= L by SOUNDNESS.md's theorem. sqverify_fast src/ at 04a0a2217 is byte-identical to 4ddf37d9c, the build RA (soundness) and RB (testing, independence) accepted on 3 October; only Cargo.toml's gate-test profile was added since.
- In the register it is one evidence entry per certificate: assurance verified, method interval-certified, performed_by repository, origin replayed-here, relationship_to_generator independent-implementation, verifiers [V-sqverify-fast] (not yet in verifiers.yaml: added by this lane, first-party, decides, independence_record packing/sqverify_fast/independence-record.yaml), certificate = the retained candidate whose decompressed SHA-256 the packet pins, replay command, replay_status passed. Structurally that is V3 and C3 (epistemics.md, Verification and Confirmation), given a control path. It is a complete replay here and an independent decision of coverage, which the source-checker replays of T-069..T-075 were not.
- It is not a second method (same net-and-shrink, interval-certified), so it never raises a result already at C3 (T-069, T-071, T-072, T-075: an attribute beside the rung, think-gpe0/think-3ok2). Not V4/C4: two adversarial reviews by distinct reviewers plus a human oversight record are needed.
- result-import.md stage 4 says the replay "runs the source's own verification"; the same section admits independent-implementation replays in relationship_to_generator. The register next_rung texts of T-082/T-090/T-091/T-094 plan source-checker replays (146+131+26.5+162 CPU-h). Recorded as a tension for the coordinator, not resolved by this lane.

What a verified-lane move needs (frontier/README.md, epistemics.md "Integrated", think-mt6e which no checker enforces yet):
- a complete replay here (above), passing, on the pinned bytes;
- a mapped review of the mathematics under docs/project/reviews/, cited as proof.audit_record on the replay entry and in the register entry's reviews;
- controls: at least one control path on a C3 entry; result-import stage 4 asks two mutated certificates refused and a test holding them. Here: per-certificate --control receipts (99/100 scaling; near-threshold scaling to 1 - 1e-6 at the least-bound leaf centre) and a test that re-checks them;
- every derived consumer of a moved verified bound follows (case records, carries by mass to higher counts, views, citations, atlas, tests, overview, SYNOPSIS, piercing survey).

Is a review required:
- T-090, T-091: the 5 October review (separately prompted, accepted) is the review of their mathematics. T-082: the 3 October review. T-094: none, so required (think-flv5's review lane).
- Neither review saw a sqverify_fast replay (both were written for source-checker replays). One separately prompted adversarial review covering T-094's mathematics and the sqverify_fast replays of the whole batch is run by this lane.
