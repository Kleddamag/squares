---
type: is
id: is-01m3p04nvawjqqtx8cynyj2pwy
title: Resolve wand125 tools ceiling and certificate admission findings
kind: task
status: open
priority: 1
version: 10
labels: []
dependencies: []
parent_id: is-01m3nzy6gqfv60whzzvww0ffa0
child_order_hints:
  - is-01m3q334yhrpa4nzahc9e8sw67
  - is-01m3q335am18z87zzbvvshk1c1
  - is-01m3q335pvv0mr0bgr5623m3bb
  - is-01m3q3362x0jttkppzvf27tabm
created_at: 2026-09-29T07:12:51.561Z
updated_at: 2026-09-29T23:13:11.299Z
---
W2 tools review retained: T-058 general B*UB ceiling lacks net-orientation premise and rigorous UB rounding. Admission defect executed: unchanged source scale_and_verify/certify/verify.cpp passes all201 then falsely prints s(1)>=1.5 for mass289/10. Reproducer devtools.audit_wand125_tools and receipts in wand125-tools-2026-09-29. Native checker must refuse same input. Remaining: corrected ceiling tooling and safe integration; do not send external maintainer messages without authorization.

## Notes

Reviewed source 0d33ab6. The general B*UB ceiling needs net-orientation and rigorous outward-witness premises; the review derives the sufficient factor B*(1+D). The executed rescaling control lets the upstream wrapper announce false s(1)>=1.5 with mass28.9 after all201 coverage checks pass. Integration must enforce strict mass admission, pinned source/patch/builder identities, a positive complete root census, explicit refusals under Python -O, and compiled cached-axis differential controls. Astra-max review also identified build-status loss in archived zmx2_run.sh:14 and zmx2_tests.sh:10; use actual compiler status and a fresh source-bound binary. The unchecked u32 point index at zmx2.rs:555 needs a count cap or checked conversion for unrestricted inputs. That enormous-input case was identified statically and does not invalidate retained certificates. Detailed findings: docs/project/reviews/review-2026-09-29-wand125-tools-mathematics.md. Archived source remains unchanged.

2026-09-29 upstream integration: wand125 provisional T-056/T-057 map to canonical T-058/T-059. Published Couzo/de Winter retain T-056/T-057. Historical notes and archived receipts retain their original labels; no evidence bytes or acceptance level changed.
