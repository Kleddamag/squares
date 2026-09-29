Complete local replay of wand125's mixed_n50_L740 certificate (s(50) >= 37/5), Session 161.
Transfer branch for think-nnlg; not for merge.

- Bundle: n50-L7.40-proof-bundle.tar.gz, SHA-256 90621d1a7ceb27267ef7b4bf3ffb5906f50e259ac28c955ec6679e64c604638f,
  retained in packing/resources/web/wand125-point-and-mixed-2026-09-28/.
- F1.json: n50-bundle-check on the pristine unpack, BUNDLE_FILES_MATCH (621 files).
- run.log: code/verify_mixed_full_proof.py proof --workers 3, PYTHONOPTIMIZE unset,
  OPENBLAS/OMP threads 1; 2026-09-29T01:29:37Z to 06:54:44Z (start.txt, end.txt);
  final status ALL_ANGLES_VERIFIED_AND_REPLAYED, 201 of 201 directions.
- F2.json: n50-compare on the run, FULL_REPLAY_MATCHES_SHIPPED: 200 oblique angles and the
  axis match the shipped records, no differing fields.
- bundle-outputs/: every file the driver wrote (proof/certificate.json and each
  direction's replayed output).

Next: add the replay evidence entry (replayed-here, interval-certified, replay passed),
set n-050's verified lower bound to 37/5, carry it to n = 51, 52, 53 by monotonicity,
raise T-048 on jlevy/squares#243 to V4/C3, re-pin DATA_REVISION and re-stamp the atlas.
