---
type: is
id: is-01m3ystck294q971jb9d2war1h
title: "Independent measure verifier, slice 3: two adversarial reviews"
kind: task
status: open
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-10-02-independent-measure-verifier.md
labels:
  - verifiers
dependencies:
  - type: blocks
    target: is-01m3ystff276btdyf2nxewyzyc
parent_id: is-01m3yrezbcgcr728c37fq49bvf
created_at: 2026-10-02T17:15:32.834Z
updated_at: 2026-10-03T05:55:17.133Z
---
Two reviewers, distinct from W2 and from each other, read the plan spec, W2's implementation and, as they choose, the authors' checkers; each writes a review in docs/project/reviews/ with a verdict on soundness (every lemma's obligation discharged in code), on the clean-room record, and on the acceptance receipts. Findings become beads. Starts when W2 declares a family complete. Exit: both accept, or findings fixed and re-reviewed.

## Notes

2026-10-03 05:12 Review RA (soundness; branch claude/review-ra-sqverify-fast @0e38246a9; review-2026-10-03-sqverify-fast-soundness.md): REJECT on S1 (blocking): axis.rs direction-0 minimum ignores NaN (value.lo < min_lower false for NaN); admissible format-T certificate with overflowing slope sums reports verified while exact capture is 0. S2: --inject-fault-at-node can exit 0 'verified' without recording the injection. S3: SOUNDNESS N2 wording. S4: other interval primitives drop NaN (not reached outside S1). Mathematics otherwise holds. Fix sent to W2 (NaN fatal everywhere, admission caps, re-run census and controls); RA to re-review after the fix. Review RB (testing/independence) still running.
2026-10-03 05:55 Review RB (testing and independence; claude/review-rb-sqverify-fast @299ce0681; review-2026-10-03-sqverify-fast-testing-and-independence.md): ACCEPT. 9,726 exact-false certificates all refused (deficits to 3.9e-121); 6,772 probes, no certified bound above the exact capture; independence: nothing traceable to the authors' checkers. Non-blocking: TI-1 audit sliver false alarms (sound), TI-2 gzip trailing bytes admitted, TI-3 certificate.D overrides format L's net, TI-4 no independence-record.yaml and fuller reads than spec 2.2-2.4 allow, TI-5 session trailer. Question: format M bins may need B(1+D/(1-D^2/4)) < 1. All sent to W2 with RA's S1-S4; after the fix, RA re-reviews; then the census becomes independent-implementation evidence (think-3ok2).
