---
type: is
id: is-01m3nzy6gqfv60whzzvww0ffa0
title: Review wand125 tools claims and maintain upstream repository references
kind: task
status: in_progress
priority: 1
version: 16
delegate: claude-code@spud10.local
labels: []
dependencies: []
child_order_hints:
  - is-01m3p04ndehpya7g3mbmmad36g
  - is-01m3p04nvawjqqtx8cynyj2pwy
  - is-01m3p04p82z8fm8kb7jxqb1p6x
  - is-01m3p45y3yxphbx0b3w5qfpyce
  - is-01m3p48ygscdcw9rn3bgacsbqw
  - is-01m3p4qcde9qgwr3dyp1b6v8fe
  - is-01m3p5wj25knm7rbx0g4a4tpvg
  - is-01m3p6krj8zr6a0956x7de4xfv
hold: null
hold_until: null
created_at: 2026-09-29T07:09:19.247Z
updated_at: 2026-09-29T09:09:58.178Z
started_at: 2026-09-29T07:09:45.733Z
---
W2 factual review and W8 documentation: pin square-packing-tools, register scoped claims, audit independent rectangle/point verification and tutorial coverage, track remaining proof obligations.

## Notes

PR #246 is pushed through 45eaf8e75. Astra-max review applied the tbd Rust and golden-testing guidelines. Five byte-exact native CLI goldens have independent semantic guards; the Rust gate runs five Rust tests, rustdoc, Clippy, formatting, and one clean plus four negative lint probes. The narrow generated-rustdoc exclusion is verified locally and in hosted CI. Final push validation passed 1,598 tests with only the inherited Session 161 expired phase failing. Final hosted run 36546217991 passed all functional checks but remains red for Session 161 and frontend timing: 134.86 seconds versus the 127.875-second regression threshold, below the 150-second absolute ceiling. No threshold relaxation or retry was performed; timing diagnosis is think-sewp. Pages run 36546218002 passed. Final review and status are recorded at https://github.com/jlevy/squares/pull/246#issuecomment-5887118339 and in repository review documents. Rust-floor and golden children are closed. Parent remains in progress: native external-certificate completion think-bmf3, full T057 census think-190a, upstream admission fixes think-xgjo, broader Rust contracts think-cr8l, and test-selection efficiency think-xcij remain open. No complete external-certificate verification or green full checkpoint is claimed.
