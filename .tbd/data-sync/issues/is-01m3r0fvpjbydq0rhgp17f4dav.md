---
type: is
id: is-01m3r0fvpjbydq0rhgp17f4dav
title: Repair public case-438 near-audit final-state digest binding
kind: bug
status: open
priority: 0
version: 1
spec_path: docs/project/reviews/review-2026-09-29-n11-optimality-census-contract.md
labels:
  - n11
dependencies: []
parent_id: is-01m3qyb542qv2xz4y2n7633g66
created_at: 2026-09-30T01:57:26.850Z
updated_at: 2026-09-30T01:57:26.850Z
---
At pinned f9e0de7, B7 near1024-independent-audit.json (decoded SHA4a93b7c8) reports source SHA491afdaa and final_state_sha256 81002706..., but canonical SHA-256 of final_state in that exact verified near-refined1024-240.json is a6d45c0c.... audit_capture_portable.py line408 claims to compute this digest from the raw source, and audit_complete_capture438.py line158 requires equality. Fixed RUN_ALL replay_candidate.py lines272-281 compares fresh geometry digest against historical B7; composition retains historical B7, so the public fresh-replay route would reject even if geometric replay succeeds. Investigate normalization/rebinding, regenerate and source-bind the audit/composition receipts, and separately validate actual source ancestry/geometry. This is a public certificate-binding defect, not a packing counterexample or theorem refutation.
