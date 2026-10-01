---
type: is
id: is-01m3vhn2999hsq7sahyrbetyxe
title: Make half-angle witness exports resolve their declared schema without fallback
kind: bug
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-10-01-post-optimality-w3-session.md
labels: []
dependencies: []
parent_id: is-01m3v9vq36ykk2jdzce75req44
created_at: 2026-10-01T10:55:06.535Z
updated_at: 2026-10-01T10:55:06.535Z
---
Exp235 raw witness geometry passed all exact checks but importer default schema:witness.schema.yaml points beside deep output where absent. Main CLI fallback masks metadata portability defect; schema corpus omits campaign result witnesses. Preserve immutable raw run001. Fix exporter relative schema path plus no-fallback validation regression; publish separately identified schema-normalized witness with unchanged geometry and retained provenance.
