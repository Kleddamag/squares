---
type: is
id: is-01m3nrt6qdv71mpn53gj361hrq
title: "ResultsRegister v2: attribution block (source_keys, published) on previously-published results, typed bibliography lineage, derived standing, and the coverage, attribution and credit-consistency gates"
kind: feature
status: closed
priority: 1
version: 3
labels:
  - packing
  - results-register
dependencies:
  - type: blocks
    target: is-01m3nqe6bqy3bx879h33d7qycd
parent_id: is-01m3nrt5zy2g6dpegq1fbczpzg
created_at: 2026-09-29T05:04:48.365Z
updated_at: 2026-09-29T05:50:54.480Z
closed_at: 2026-09-29T05:50:54.470Z
close_reason: Done in 68903d852 on claude/magical-davinci-ueqmu1-results-register
resolution: null
duplicate_of: null
---
Per the plan's Schema and Gates sections: results.schema.yaml v2; check_results resolves attribution.source_keys in bibliography.yaml and fails when a case lower bound (reported or verified) cites evidence from a source dated >= RECENT_SINCE that no register entry cites; bibliography 'lineage' enum (builds-on-project, credits-project, independent) with a test holding it consistent with the credit string; render_results groups RESULTS.md by origin and lineage with credit, published date, V/C and derived standing, awaiting-verification entries first.
