---
type: is
id: is-01m44qz1asb40jr4qgd1kcytft
title: "Import David Ellsworth / Allen Chang via the Kingbird catalogue: s(69) <= 8.82719465572973, s(83) <= 9.63475764863108, s(87) <= 9.83881526994826 (no issue)"
kind: task
status: in_progress
priority: 1
version: 4
delegate: claude-code@vm
labels:
  - result-import
dependencies:
  - type: blocks
    target: is-01m44qz5cez2hhdr2b5p4m1sya
parent_id: is-01m44qz0rxvkakmyqaj7qdgagv
hold: null
hold_until: null
created_at: 2026-10-05T00:38:34.584Z
updated_at: 2026-10-05T01:32:11.316Z
started_at: 2026-10-05T00:40:48.766Z
---
source-coverage.yaml pending_catalogue_intake lists n = 69, 83, 87: the 2026-09-30 Kingbird capture prints sides below the record. Register (T-088 n=69 Ellsworth; T-089 n=83, 87 Allen Chang), take the sides into the case records, remove the pending entries, witness from evand's parse of the SVGs at evand/square-packing 7ff3b21 site/www/data/p/ (kingbird.myphotos.cc is blocked by this session's egress policy). Stage 4 witness check if cheap.

## Notes

2026-10-05 progress (claude-code lane kingbird): T-088 (n=69, Ellsworth) and T-089 (n=83, 87, Chang) registered at V0/C0 with reported evidence E-n069-ellsworth-2026-09-report, E-n083-chang-2026-09-report, E-n087-chang-2026-09-report; bibliography keys [Ellsworth n69 2026-09-24], [Chang n83 2026-09-24], [Chang n87 2026-09-24] dated by the page's server date 2026-09-24 (entries say September 2026). Case records take the catalogue sides; pending_catalogue_intake emptied; UnitSquare n=69 now a superseded report (check_source_coverage lets the baseline supersede when no override is selected). Witnesses from evand/square-packing@7ff3b21 site/www/data/p via new derive_kingbird_facts --from-parse (source.revision records the parse); --compare-parse: 90 of 92 comparable counts agree with our own SVG parse to one binary64 ulp (83, 87 differ because their pictures changed). Numerical receipts pass at 1e-8 (also 1e-14). Diagnostic only, not recorded: packing-witness promote robust-rational finds exact rational certificates within ~1e-12 of each printed side in seconds - the cheap stage-4 route. Stage 4 left as next_rung (needs certificate evidence + review).
