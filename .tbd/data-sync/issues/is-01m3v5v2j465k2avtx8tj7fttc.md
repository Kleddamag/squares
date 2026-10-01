---
type: is
id: is-01m3v5v2j465k2avtx8tj7fttc
title: Three time-limited tests flip under machine load
kind: bug
status: open
priority: 3
version: 1
labels: []
dependencies: []
created_at: 2026-10-01T07:28:40.515Z
updated_at: 2026-10-01T07:28:40.515Z
---
Seen 2026-09-30 and 10-01 at load averages of 30 to 250, each passing alone: tests/test_n11_generic_sequential.py::test_complete_2135_exclusion (INCOMPLETE where PASS_ONE_GENERIC_EXCLUSION is expected; same shape as the 2095 test whose max_seconds jlevy/squares#250 raised from 60 to 300), tests/test_fixed_core_packet_calibration.py::test_real_supervisor_signal_reaps_worker_including_launch_window[1-launch-default], tests/test_rust_rectangle_geometry.py::test_partial_line_timeout_retains_unresolved_event_census (a 0.5 s timeout against a fake server), and the per-test 12 s call-time rule tripping on test_replay_bc303_t1_witness and test_translation_escape_screen. Give each a limit that measures the code, not the machine.
