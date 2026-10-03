---
type: is
id: is-01m3ystck294q971jb9d2war1h
title: "Independent measure verifier, slice 3: two adversarial reviews"
kind: task
status: open
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-10-02-independent-measure-verifier.md
labels:
  - verifiers
dependencies:
  - type: blocks
    target: is-01m3ystff276btdyf2nxewyzyc
parent_id: is-01m3yrezbcgcr728c37fq49bvf
created_at: 2026-10-02T17:15:32.834Z
updated_at: 2026-10-03T05:12:14.738Z
---
Two reviewers, distinct from W2 and from each other, read the plan spec, W2's implementation and, as they choose, the authors' checkers; each writes a review in docs/project/reviews/ with a verdict on soundness (every lemma's obligation discharged in code), on the clean-room record, and on the acceptance receipts. Findings become beads. Starts when W2 declares a family complete. Exit: both accept, or findings fixed and re-reviewed.

## Notes

2026-10-03 05:12 Review RA (soundness; branch claude/review-ra-sqverify-fast @0e38246a9; review-2026-10-03-sqverify-fast-soundness.md): REJECT on S1 (blocking): axis.rs direction-0 minimum ignores NaN (value.lo < min_lower false for NaN); admissible format-T certificate with overflowing slope sums reports verified while exact capture is 0. S2: --inject-fault-at-node can exit 0 'verified' without recording the injection. S3: SOUNDNESS N2 wording. S4: other interval primitives drop NaN (not reached outside S1). Mathematics otherwise holds. Fix sent to W2 (NaN fatal everywhere, admission caps, re-run census and controls); RA to re-review after the fix. Review RB (testing/independence) still running.
