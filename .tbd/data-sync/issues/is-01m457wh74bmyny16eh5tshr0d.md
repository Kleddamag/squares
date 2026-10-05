---
type: is
id: is-01m457wh74bmyny16eh5tshr0d
title: "Re-record suite-file-costs.json: main's shard 4 sits at the 10% unrecorded threshold"
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-10-05T05:16:49.764Z
updated_at: 2026-10-05T05:16:49.764Z
---
On main 6dbd6f69e, `python -m devtools.suite_files check` reports shard 4/4 at 13 of 130 files unrecorded (10.0%), exactly the UNRECORDED_SHARE_WARNING threshold that test_suite_files.py::test_check_passes_on_the_real_tree enforces. Any PR that adds one test file hashing to shard 4 fails suite-d. PR #336 hit it at 1fcb74fdf (run 37266380194, job 111623996216) and renamed its test to test_windows_supervision.py, which hashes to shard 2, rather than re-record: the session that found it could not download the hosted validation-timings-suite-* artifacts, because the egress proxy denies the Actions blob storage host. Remedy, as the check prints: rebuild the record from a complete green four-shard hosted cohort with `python -m devtools.suite_files record REPORT.json ...`, keeping target_ceiling_seconds, as eb8c15a35 did from run 37057794692.
