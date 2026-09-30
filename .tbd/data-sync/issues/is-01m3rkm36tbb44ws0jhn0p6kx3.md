---
type: is
id: is-01m3rkm36tbb44ws0jhn0p6kx3
title: Acquire bounded source closures and schedule independent n11 replay
kind: task
status: in_progress
priority: 0
version: 4
spec_path: docs/project/specs/active/plan-2026-09-29-proof-verification-consolidation.md
labels: []
dependencies: []
parent_id: is-01m3rb05kzxrn6zcj60cs1c91f
created_at: 2026-09-30T07:31:48.569Z
updated_at: 2026-09-30T08:15:57.712Z
---
Consume the reviewed276-case proposal manifest, select small unsupported-yet-required batches, verify pinned INDEX/LFS/decoded identities and byte ceilings, reuse retained objects, and publish deterministic intake receipts without geometric acceptance. Run in parallel with shared-v9 implementation and capture induction.

## Notes

Pinned manifest and bounded acquisition committed2921d0cba/e5966d1fa. Thirteen intake controls pass. Twelve small case closures are now unified in ignored durable attic/n11-proof-inputs/<revision>/objects;16.41MB compressed/87.75MB decoded, finalreuse pass0.72s. All pins rederived from immutable INDEX/LFS; compressed and decoded hashes/lengths checked. New run_n11_nonfield_batch consumes the shared sequential adapter CLI, caps jobs×workers at4, case wall<=120s and batch wall<=300s; kills whole process groups on timeout. Ten controls require complete exact case identity, zero pending work, correct checker hash and successful exit before credit. Live batch awaits native_sol generalized checker. Source acquisition and orchestration are not themselves geometry proofs.
