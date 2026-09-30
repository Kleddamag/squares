---
type: is
id: is-01m3sp12jsvbfsveyd1cqq2msj
title: Keep frozen PR validation reproducible when active session clocks expire
kind: task
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-09-29-proof-verification-consolidation.md
labels: []
dependencies: []
parent_id: is-01m3ra1hjvn4bdh3h13aggqgvb
created_at: 2026-09-30T17:33:05.495Z
updated_at: 2026-09-30T17:33:05.495Z
---
PR246 at ebbfec10e failed only because an in-progress session deadline elapsed while final CI ran (plus an unrelated test-node inventory rename). Clock accounting must remain honest, but a frozen reviewed source should not need repeated metadata-only commits solely to reset wall-clock checks. Review the distinction between contemporaneous local session deadline enforcement, timestamped historical-record consistency, and hosted integration checks. Design a bounded explicit handoff/terminal path compatible with composed checkpoint evidence; retain overruns and failures rather than erasing them or manufacturing a full-gate PASS. Add focused controls and document the rule before changing enforcement.
