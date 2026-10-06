---
title: "exp-257 — Session 182 BC-428: n17 residue states from the strata H-264's draw never reached"
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-257
  series: series-000
  title: A seeded draw of 31 residue states from the 21 unsampled strata of the arity8 frame, run as whole
    17-cell patterns under SW9's frozen adaptive-row kernel recipe, each closure admitted on the standing
    verifier's full pass
  date: '2026-10-05'
  hypotheses:
  - H-275
  tier: exploratory
  subject:
    label: The 31 states frozen in packing/campaign/explorations/X048-session-182-overnight/kernel-targets-bc428.txt,
      one from each of the 21 strata of survey_n17_residue's arity8 frame that H-264's seed-182 draw never
      reached and a second from each of the ten larger than the mean, each run as a whole 17-cell pattern on
      the unique-state 24-cell cover at U = 1169/250.
    engine: devtools.check_n17_subpattern (producer and checker) and devtools.verify_n17_kernel_certificate in
      full mode under the kernel-streamed listing, both from the clean run worktree at the session-182
      registration commit
    assurance: verified
    method: exact-algebraic
    host_system: Linux x86_64 remote session container, project Python 3.14.7, one worker per job at nice 10
    selftest_passed: true
    engine_commit: cebb5d15aaa17d0cc13aa302ecbd750a54bfc57d
  instance:
    axis: n
    point: 17
    role: target
  method:
    control: BC-424's endpoint-state control under the same recipe, the endpoint's own state and feasible at U,
      returned PASS_CERTIFIED_STALL at its 24-round cap in 6,599 s (receipts/A/kernel-control-endpoint-sw9.json),
      and lane K's endpoint7 control returned PASS_CONTROL_STALLED (receipts/K/kernel-control-endpoint7.json).
      This round runs that recipe unchanged, so no new control runs. The endpoint's state must survive every
      admitted entry, which the census checks.
    candidate: Each frozen state's seed and node, re-proved in full by the standing kernel verifier on a closure.
    runs_per_condition: 1
    interleaved: false
    operator: Claude Session 182; the run operator's BC-428 queue runs the states in the frozen order on two
      workers, verifies each closure, and admits it in the session checkout
    entry_point: packing/devtools/check_n17_subpattern.py
    command: 'From packing/ of the run worktree: nice -n 10 timeout -k 120 7600 .venv/bin/python3 -m
      devtools.check_n17_subpattern --cells CELLS17 --bins 64 --max-rounds 24 --hull-limit 16 --producer-share
      0.6 --split-floor 512 --max-rows 1152 --split-patience 1 --max-seconds 7000 --save-objects DIR --output
      FILE; on a closure, nice -n 10 timeout -k 120 4000 .venv/bin/python3 -m devtools.verify_n17_kernel_certificate
      --progress --output CERT/verification.json CERT; then devtools.census_n17_certified in the session
      checkout.'
    budget: 7,000 s per state and 4,000 s per verification on one worker, two workers, until 2026-10-06T07:14:04Z
    record: packing/campaign/series/series-000-smoke-and-calibration/results/exp-257-n17-unsampled-strata
    dirty: false
    commit: cebb5d15aaa17d0cc13aa302ecbd750a54bfc57d
  results:
  - shape: determination
    role: outcome
    question: Is draw 2 (mask 4061102, stratum c3/i>=5/d4) infeasible at U, by a certificate the kernel's checker
      accepts and the standing verifier re-proves in full?
    outcome: criterion_met
    checked_by: The run (receipts/U/kernel-u2-bc428.json) returns PASS_CERTIFIED_CLOSED in 1,891 s of wall and 1,231 s
      of process CPU (producer 1,229 s, checker 660 s) on 56 steps and 3,712 rows in 4 rounds, rows finest at
      1/128, closure all_parent_poses_forbidden for side-E0 at step 55. The standing verifier at cebb5d15a
      passes it in full mode in 560 s, checking all 3,712 live rows in full and 13,050 collision regions by
      73,627,372 exact facet checks. It excludes its own 8 states, one orbit; the certified census after it is
      36,980 states in 4,710 orbits.
  - shape: determination
    role: outcome
    question: Is draw 3 (mask 4439807, stratum c4/i<=3/d>=8) infeasible at U, by a certificate the kernel's checker
      accepts and the standing verifier re-proves in full?
    outcome: criterion_met
    checked_by: The run (receipts/U/kernel-u3-bc428.json) returns PASS_CERTIFIED_CLOSED in 1,218 s of wall and 1,174 s
      of process CPU (producer 688 s, checker 529 s) on 95 steps and 6,336 rows in 6 rounds, rows finest at
      1/128, closure all_parent_poses_forbidden for side-W1 at step 94. The standing verifier at cebb5d15a
      passes it in full mode in 472 s, checking all 6,004 live rows in full and 16,200 collision regions by
      76,354,712 exact facet checks. It excludes its own 8 states, one orbit; the certified census after it is
      36,972 states in 4,709 orbits.
  - shape: determination
    role: outcome
    question: Is draw 4 (mask 6020797, stratum c3/i>=5/d6) infeasible at U, by a certificate the kernel's checker
      accepts and the standing verifier re-proves in full?
    outcome: criterion_met
    checked_by: The run (receipts/U/kernel-u4-bc428.json) returns PASS_CERTIFIED_CLOSED in 749 s of wall and 726 s of
      process CPU (producer 385 s, checker 362 s) on 49 steps and 3,200 rows in 3 rounds, rows finest at
      1/128, closure all_parent_poses_forbidden for interior-S at step 48. The standing verifier at cebb5d15a
      passes it in full mode in 312 s, checking all 3,200 live rows in full and 9,625 collision regions by
      50,455,248 exact facet checks. It excludes its own 8 states, one orbit; the certified census after it is
      36,964 states in 4,708 orbits.
  - shape: determination
    role: outcome
    question: Is draw 5 (mask 3931626, stratum c<=2/i>=5/d6) infeasible at U, by a certificate the kernel's checker
      accepts and the standing verifier re-proves in full?
    outcome: criterion_met
    checked_by: The run (receipts/U/kernel-u5-bc428.json) returns PASS_CERTIFIED_CLOSED in 1,221 s of wall and 1,135 s
      of process CPU (producer 581 s, checker 639 s) on 59 steps and 3,904 rows in 4 rounds, rows finest at
      1/128, closure all_parent_poses_forbidden for side-E1 at step 58. The standing verifier at cebb5d15a
      passes it in full mode in 563 s, checking all 3,897 live rows in full and 12,929 collision regions by
      74,192,232 exact facet checks. It excludes its own 8 states, one orbit; the certified census after it is
      36,956 states in 4,707 orbits.
  - shape: determination
    role: outcome
    question: Is draw 1 (mask 1900509, stratum c3/i<=3/d2) (distance 2, reported apart) excluded within the 7,000 s
      ceiling?
    outcome: criterion_missed
    checked_by: The run (receipts/U/kernel-u1-bc428.json) returns INCOMPLETE in 7,001 s of wall and 6,101 s of process
      CPU (capture row wall ceiling). Not a closure; nothing is concluded from it, and its saved node is kept.
  - shape: determination
    role: outcome
    question: Is draw 6 (mask 5491711, stratum c4/i4/d>=8) excluded within the 7,000 s ceiling?
    outcome: criterion_missed
    checked_by: The run (receipts/U/kernel-u6-bc428.json) returns PASS_CERTIFIED_STALL in 2,009 s of wall and 1,863 s of
      process CPU, the producer at a fixed point after 15 rounds (255 steps, 17,152 rows, finest 1/128),
      inside its ceiling. A non-closure; its node is kept.
  - shape: determination
    role: outcome
    question: Is draw 7 (mask 5959674, stratum c<=2/i4/d6) infeasible at U, by a certificate the kernel's checker
      accepts and the standing verifier re-proves in full?
    outcome: criterion_met
    checked_by: The run (receipts/U/kernel-u7-bc428.json) returns PASS_CERTIFIED_CLOSED in 1,606 s of wall and 1,475 s
      of process CPU (producer 790 s, checker 812 s) on 79 steps and 5,248 rows in 5 rounds, rows finest at
      1/128, closure all_parent_poses_forbidden for side-N2 at step 78. The standing verifier at cebb5d15a
      passes it in full mode in 714 s, checking all 5,160 live rows in full and 16,556 collision regions by
      93,568,844 exact facet checks. It excludes its own 8 states, one orbit; the certified census after it is
      36,948 states in 4,706 orbits.
  - shape: determination
    role: outcome
    question: Is draw 8 (mask 3078077, stratum c3/i4/d2) (distance 2, reported apart) infeasible at U, by a
      certificate the kernel's checker accepts and the standing verifier re-proves in full?
    outcome: criterion_met
    checked_by: The run (receipts/U/kernel-u8-bc428.json) returns PASS_CERTIFIED_CLOSED in 622 s of wall and 572 s of
      process CPU (producer 315 s, checker 306 s) on 44 steps and 2,880 rows in 3 rounds, rows finest at
      1/128, closure all_parent_poses_forbidden for side-S2 at step 43. The standing verifier at cebb5d15a
      passes it in full mode in 277 s, checking all 2,880 live rows in full and 9,094 collision regions by
      52,565,640 exact facet checks. It excludes its own 8 states, one orbit; the certified census after it is
      36,940 states in 4,705 orbits.
  - shape: determination
    role: outcome
    question: Is draw 10 (mask 5996459, stratum c3/i>=5/d>=8) infeasible at U, by a certificate the kernel's checker
      accepts and the standing verifier re-proves in full?
    outcome: criterion_met
    checked_by: The run (receipts/U/kernel-u10-bc428.json) returns PASS_CERTIFIED_CLOSED in 602 s of wall and 581 s of
      process CPU (producer 290 s, checker 311 s) on 33 steps and 2,112 rows in 2 rounds, rows finest at 1/64,
      closure all_parent_poses_forbidden for interior-N at step 32. The standing verifier at cebb5d15a passes
      it in full mode in 322 s, checking all 2,112 live rows in full and 7,237 collision regions by 43,019,764
      exact facet checks. It excludes its own 8 states, one orbit; the certified census after it is 36,932
      states in 4,704 orbits.
  - shape: determination
    role: outcome
    question: Is draw 9 (mask 5931001, stratum c<=2/i4/d>=8) infeasible at U, by a certificate the kernel's checker
      accepts and the standing verifier re-proves in full?
    outcome: criterion_met
    checked_by: The run (receipts/U/kernel-u9-bc428.json) returns PASS_CERTIFIED_CLOSED in 1,319 s of wall and 1,264 s
      of process CPU (producer 690 s, checker 628 s) on 77 steps and 5,120 rows in 5 rounds, rows finest at
      1/128, closure all_parent_poses_forbidden for side-W1 at step 76. The standing verifier at cebb5d15a
      passes it in full mode in 574 s, checking all 5,113 live rows in full and 16,161 collision regions by
      89,940,404 exact facet checks. It excludes its own 8 states, one orbit; the certified census after it is
      36,924 states in 4,703 orbits.
  - shape: determination
    role: outcome
    question: Is draw 11 (mask 3079158, stratum c<=2/i4/d4) infeasible at U, by a certificate the kernel's checker
      accepts and the standing verifier re-proves in full?
    outcome: criterion_met
    checked_by: The run (receipts/U/kernel-u11-bc428.json) returns PASS_CERTIFIED_CLOSED in 1,246 s of wall and 1,199 s
      of process CPU (producer 643 s, checker 601 s) on 68 steps and 4,480 rows in 4 rounds, rows finest at
      1/128, closure all_parent_poses_forbidden for interior-E at step 67. The standing verifier at cebb5d15a
      passes it in full mode in 562 s, checking all 4,468 live rows in full and 14,254 collision regions by
      78,128,736 exact facet checks. It excludes its own 8 states, one orbit; the certified census after it is
      36,916 states in 4,702 orbits.
  - shape: determination
    role: outcome
    question: Is draw 12 (mask 2818035, stratum c<=2/i<=3/d6) excluded within the 7,000 s ceiling?
    outcome: criterion_missed
    checked_by: The run (receipts/U/kernel-u12-bc428.json) returns PASS_CERTIFIED_STALL in 1,681 s of wall and 1,597 s
      of process CPU, the producer at a fixed point after 6 rounds (102 steps, 6,784 rows, finest 1/128),
      inside its ceiling. A non-closure; its node is kept.
  - shape: determination
    role: outcome
    question: Is draw 13 (mask 4061110, stratum c<=2/i>=5/d4) infeasible at U, by a certificate the kernel's checker
      accepts and the standing verifier re-proves in full?
    outcome: criterion_met
    checked_by: The run (receipts/U/kernel-u13-bc428.json) returns PASS_CERTIFIED_CLOSED in 1,041 s of wall and 984 s of
      process CPU (producer 536 s, checker 504 s) on 50 steps and 3,264 rows in 3 rounds, rows finest at
      1/128, closure all_parent_poses_forbidden for interior-N at step 49. The standing verifier at cebb5d15a
      passes it in full mode in 452 s, checking all 3,224 live rows in full and 11,550 collision regions by
      66,166,252 exact facet checks. It excludes its own 8 states, one orbit; the certified census after it is
      36,908 states in 4,701 orbits.
  - shape: determination
    role: outcome
    question: Is draw 14 (mask 4456442, stratum c<=2/i<=3/d>=8) infeasible at U, by a certificate the kernel's checker
      accepts and the standing verifier re-proves in full?
    outcome: criterion_met
    checked_by: The run (receipts/U/kernel-u14-bc428.json) returns PASS_CERTIFIED_CLOSED in 1,328 s of wall and 1,281 s
      of process CPU (producer 647 s, checker 680 s) on 65 steps and 4,288 rows in 4 rounds, rows finest at
      1/128, closure all_parent_poses_forbidden for side-E2 at step 64. The standing verifier at cebb5d15a
      passes it in full mode in 572 s, checking all 4,232 live rows in full and 13,327 collision regions by
      75,606,652 exact facet checks. It excludes its own 8 states, one orbit; the certified census after it is
      36,900 states in 4,700 orbits.
  - shape: determination
    role: outcome
    question: Is draw 16 (mask 4648955, stratum c3/i<=3/d>=8) infeasible at U, by a certificate the kernel's checker
      accepts and the standing verifier re-proves in full?
    outcome: criterion_met
    checked_by: The run (receipts/U/kernel-u16-bc428.json) returns PASS_CERTIFIED_CLOSED in 2,010 s of wall and 1,972 s
      of process CPU (producer 1,064 s, checker 945 s) on 114 steps and 7,616 rows in 7 rounds, rows finest at
      1/128, closure all_parent_poses_forbidden for side-N2 at step 113. The standing verifier at cebb5d15a
      passes it in full mode in 842 s, checking all 7,571 live rows in full and 21,980 collision regions by
      123,141,184 exact facet checks. It excludes its own 8 states, one orbit; the certified census after it
      is 36,892 states in 4,699 orbits.
  - shape: determination
    role: outcome
    question: Is draw 17 (mask 5503965, stratum c3/i4/d>=8) infeasible at U, by a certificate the kernel's checker
      accepts and the standing verifier re-proves in full?
    outcome: criterion_met
    checked_by: The run (receipts/U/kernel-u17-bc428.json) returns PASS_CERTIFIED_CLOSED in 1,366 s of wall and 1,335 s
      of process CPU (producer 727 s, checker 637 s) on 79 steps and 5,248 rows in 5 rounds, rows finest at
      1/128, closure all_parent_poses_forbidden for side-N2 at step 78. The standing verifier at cebb5d15a
      passes it in full mode in 592 s, checking all 5,113 live rows in full and 15,236 collision regions by
      76,511,316 exact facet checks. It excludes its own 8 states, one orbit; the certified census after it is
      36,884 states in 4,698 orbits.
  - shape: determination
    role: outcome
    question: Is draw 18 (mask 13090300, stratum c<=2/i>=5/d>=8) infeasible at U, by a certificate the kernel's
      checker accepts and the standing verifier re-proves in full?
    outcome: criterion_met
    checked_by: The run (receipts/U/kernel-u18-bc428.json) returns PASS_CERTIFIED_CLOSED in 963 s of wall and 936 s of
      process CPU (producer 493 s, checker 469 s) on 50 steps and 3,200 rows in 3 rounds, rows finest at 1/64,
      closure all_parent_poses_forbidden for interior-SE at step 49. The standing verifier at cebb5d15a passes
      it in full mode in 420 s, checking all 3,153 live rows in full and 10,583 collision regions by
      56,600,352 exact facet checks. It excludes its own 8 states, one orbit; the certified census after it is
      36,876 states in 4,697 orbits.
  - shape: determination
    role: outcome
    question: Is draw 15 (mask 1900531, stratum c<=2/i<=3/d4) excluded within the 7,000 s ceiling?
    outcome: criterion_missed
    checked_by: The run (receipts/U/kernel-u15-bc428.json) returns INCOMPLETE in 7,002 s of wall and 6,844 s of process
      CPU (capture row wall ceiling). Not a closure; nothing is concluded from it, and its saved node is kept.
  - shape: determination
    role: outcome
    question: Is draw 19 (mask 506879, stratum c4/i<=3/d6) infeasible at U, by a certificate the kernel's checker
      accepts and the standing verifier re-proves in full?
    outcome: criterion_met
    checked_by: The run (receipts/U/kernel-u19-bc428.json) returns PASS_CERTIFIED_CLOSED in 629 s of wall and 589 s of
      process CPU (producer 347 s, checker 281 s) on 48 steps and 3,136 rows in 3 rounds, rows finest at
      1/128, closure all_parent_poses_forbidden for side-E2 at step 47. The standing verifier at cebb5d15a
      passes it in full mode in 257 s, checking all 3,123 live rows in full and 9,066 collision regions by
      53,982,528 exact facet checks. It excludes its own 8 states, one orbit; the certified census after it is
      36,868 states in 4,696 orbits.
  - shape: determination
    role: outcome
    question: Is draw 20 (mask 2351099, stratum c3/i<=3/d6) infeasible at U, by a certificate the kernel's checker
      accepts and the standing verifier re-proves in full?
    outcome: criterion_met
    checked_by: The run (receipts/U/kernel-u20-bc428.json) returns PASS_CERTIFIED_CLOSED in 1,135 s of wall and 1,090 s
      of process CPU (producer 604 s, checker 530 s) on 79 steps and 5,236 rows in 5 rounds, rows finest at
      1/128, closure all_parent_poses_forbidden for side-E1 at step 78. The standing verifier at cebb5d15a
      passes it in full mode in 458 s, checking all 5,087 live rows in full and 15,067 collision regions by
      79,073,220 exact facet checks. It excludes its own 8 states, one orbit; the certified census after it is
      36,860 states in 4,695 orbits.
  - shape: determination
    role: outcome
    question: Is draw 21 (mask 5750671, stratum c4/i>=5/d>=8) infeasible at U, by a certificate the kernel's checker
      accepts and the standing verifier re-proves in full?
    outcome: criterion_met
    checked_by: The run (receipts/U/kernel-u21-bc428.json) returns PASS_CERTIFIED_CLOSED in 989 s of wall and 945 s of
      process CPU (producer 524 s, checker 464 s) on 91 steps and 6,024 rows in 6 rounds, rows finest at
      1/128, closure all_parent_poses_forbidden for side-S1 at step 90. The standing verifier at cebb5d15a
      passes it in full mode in 414 s, checking all 4,955 live rows in full and 14,229 collision regions by
      62,476,280 exact facet checks. It excludes its own 8 states, one orbit; the certified census after it is
      36,852 states in 4,694 orbits.
  - shape: determination
    role: outcome
    question: Is draw 23 (mask 6224571, stratum c3/i>=5/d6) infeasible at U, by a certificate the kernel's checker
      accepts and the standing verifier re-proves in full?
    outcome: criterion_met
    checked_by: The run (receipts/U/kernel-u23-bc428.json) returns PASS_CERTIFIED_CLOSED in 572 s of wall and 550 s of
      process CPU (producer 309 s, checker 262 s) on 42 steps and 2,752 rows in 3 rounds, rows finest at
      1/128, closure all_parent_poses_forbidden for side-E1 at step 41. The standing verifier at cebb5d15a
      passes it in full mode in 267 s, checking all 2,752 live rows in full and 9,487 collision regions by
      50,427,592 exact facet checks. It excludes its own 8 states, one orbit; the certified census after it is
      36,844 states in 4,693 orbits.
  - shape: determination
    role: outcome
    question: Is draw 22 (mask 4061101, stratum c3/i>=5/d4) infeasible at U, by a certificate the kernel's checker
      accepts and the standing verifier re-proves in full?
    outcome: criterion_met
    checked_by: The run (receipts/U/kernel-u22-bc428.json) returns PASS_CERTIFIED_CLOSED in 1,462 s of wall and 1,384 s
      of process CPU (producer 730 s, checker 728 s) on 65 steps and 4,288 rows in 4 rounds, rows finest at
      1/128, closure all_parent_poses_forbidden for interior-W at step 64. The standing verifier at cebb5d15a
      passes it in full mode in 954 s, checking all 4,234 live rows in full and 14,058 collision regions by
      77,032,316 exact facet checks. It excludes its own 8 states, one orbit; the certified census after it is
      36,836 states in 4,692 orbits.
  - shape: determination
    role: outcome
    question: Is draw 24 (mask 5504319, stratum c4/i4/d>=8) infeasible at U, by a certificate the kernel's checker
      accepts and the standing verifier re-proves in full?
    outcome: criterion_met
    checked_by: The run (receipts/U/kernel-u24-bc428.json) returns PASS_CERTIFIED_CLOSED in 1,381 s of wall and 939 s of
      process CPU (producer 651 s, checker 728 s) on 70 steps and 4,608 rows in 5 rounds, rows finest at
      1/128, closure all_parent_poses_forbidden for corner-SE at step 69. The standing verifier at cebb5d15a
      passes it in full mode in 430 s, checking all 4,433 live rows in full and 12,711 collision regions by
      58,656,548 exact facet checks. It excludes its own 8 states, one orbit; the certified census after it is
      36,828 states in 4,691 orbits.
  - shape: determination
    role: outcome
    question: Is draw 26 (mask 12843002, stratum c<=2/i4/d>=8) infeasible at U, by a certificate the kernel's checker
      accepts and the standing verifier re-proves in full?
    outcome: criterion_met
    checked_by: The run (receipts/U/kernel-u26-bc428.json) returns PASS_CERTIFIED_CLOSED in 1,097 s of wall and 1,034 s
      of process CPU (producer 553 s, checker 543 s) on 49 steps and 3,136 rows in 3 rounds, rows finest at
      1/64, closure all_parent_poses_forbidden for interior-NW at step 48. The standing verifier at cebb5d15a
      passes it in full mode in 493 s, checking all 3,136 live rows in full and 10,034 collision regions by
      55,092,172 exact facet checks. It excludes its own 4 states, one orbit; the certified census after it is
      36,824 states in 4,690 orbits.
  - shape: determination
    role: outcome
    question: Is draw 25 (mask 5685241, stratum c<=2/i4/d6) infeasible at U, by a certificate the kernel's checker
      accepts and the standing verifier re-proves in full?
    outcome: criterion_met
    checked_by: The run (receipts/U/kernel-u25-bc428.json) returns PASS_CERTIFIED_CLOSED in 1,944 s of wall and 1,722 s
      of process CPU (producer 1,101 s, checker 842 s) on 95 steps and 6,331 rows in 6 rounds, rows finest at
      1/128, closure all_parent_poses_forbidden for side-E1 at step 94. The standing verifier at cebb5d15a
      passes it in full mode in 754 s, checking all 6,263 live rows in full and 20,278 collision regions by
      106,004,980 exact facet checks. It excludes its own 8 states, one orbit; the certified census after it
      is 36,816 states in 4,689 orbits.
  - shape: determination
    role: outcome
    question: Is draw 27 (mask 6023931, stratum c3/i>=5/d>=8) infeasible at U, by a certificate the kernel's checker
      accepts and the standing verifier re-proves in full?
    outcome: criterion_met
    checked_by: The run (receipts/U/kernel-u27-bc428.json) returns PASS_CERTIFIED_CLOSED in 800 s of wall and 757 s of
      process CPU (producer 442 s, checker 357 s) on 49 steps and 3,200 rows in 3 rounds, rows finest at
      1/128, closure all_parent_poses_forbidden for interior-S at step 48. The standing verifier at cebb5d15a
      passes it in full mode in 329 s, checking all 3,165 live rows in full and 9,724 collision regions by
      52,324,060 exact facet checks. It excludes its own 8 states, one orbit; the certified census after it is
      36,808 states in 4,688 orbits.
  - shape: determination
    role: outcome
    question: Is draw 28 (mask 5470206, stratum c3/i4/d>=8) infeasible at U, by a certificate the kernel's checker
      accepts and the standing verifier re-proves in full?
    outcome: criterion_met
    checked_by: The run (receipts/U/kernel-u28-bc428.json) returns PASS_CERTIFIED_CLOSED in 743 s of wall and 717 s of
      process CPU (producer 389 s, checker 352 s) on 48 steps and 3,136 rows in 3 rounds, rows finest at
      1/128, closure all_parent_poses_forbidden for interior-SW at step 47. The standing verifier at cebb5d15a
      passes it in full mode in 333 s, checking all 3,111 live rows in full and 9,914 collision regions by
      50,307,872 exact facet checks. Its own 8 states, one orbit, were already excluded by earlier admitted
      entries, so the certified census after it is unchanged at 36,808 states in 4,688 orbits.
  - shape: determination
    role: outcome
    question: Is draw 30 (mask 2785277, stratum c3/i<=3/d6) infeasible at U, by a certificate the kernel's checker
      accepts and the standing verifier re-proves in full?
    outcome: criterion_met
    checked_by: The run (receipts/U/kernel-u30-bc428.json) returns PASS_CERTIFIED_CLOSED in 1,866 s of wall and 1,807 s
      of process CPU (producer 973 s, checker 892 s) on 129 steps and 8,626 rows in 8 rounds, rows finest at
      1/128, closure all_parent_poses_forbidden for side-W1 at step 128. The standing verifier at cebb5d15a
      passes it in full mode in 786 s, checking all 8,262 live rows in full and 23,575 collision regions by
      126,048,356 exact facet checks. It excludes its own 8 states, one orbit; the certified census after it
      is 36,800 states in 4,687 orbits.
  - shape: determination
    role: outcome
    question: Is draw 29 (mask 769791, stratum c4/i<=3/d6) infeasible at U, by a certificate the kernel's checker
      accepts and the standing verifier re-proves in full?
    outcome: criterion_met
    checked_by: The run (receipts/U/kernel-u29-bc428.json) returns PASS_CERTIFIED_CLOSED in 4,644 s of wall and 4,522 s
      of process CPU (producer 2,574 s, checker 2,069 s) on 337 steps and 22,720 rows in 20 rounds, rows
      finest at 1/128, closure all_parent_poses_forbidden for side-E2 at step 336. The standing verifier at
      cebb5d15a passes it in full mode in 1,899 s, checking all 20,706 live rows in full and 53,800 collision
      regions by 230,813,492 exact facet checks. It excludes its own 8 states, one orbit; the certified census
      after it is 36,792 states in 4,686 orbits.
  verdict:
    decision: accepted
    primary_criterion: The fraction of the frozen states the kernel excludes under SW9's recipe within the 7,000 s
      ceiling, each closure re-proved in full by the standing kernel verifier with the endpoint surviving, and
      the cost per state; the distance-2 draws reported apart.
    reason: >-
      Accepted means the frozen measurement ran and answered H-275's question for the
      draws it reached; it does not mean a falsifier survived, because H-275 is an open
      question and registers none. Of the 27 counted draws that finished, 24 (89%)
      closed within the 7,000 s ceiling, each re-proved in full by the standing kernel
      verifier and admitted with the endpoint surviving. Of the other three, u6 and u12
      reached producer fixed points inside the ceiling; u15 ended INCOMPLETE at the
      7,000 s ceiling, where the checker ran out of time, so it is neither a closure nor
      a fixed point. The distance-2 draws are reported apart: u8 closed and was admitted
      and u1 ended INCOMPLETE at the ceiling. A closure cost 550 to 1,972 s of process
      CPU (median 1,090) and its verification 257 to 954 s (median 472); the
      non-closures cost u6 1,863 s (at a fixed point), u12 1,597 s (at a fixed point),
      u1 6,101 s (INCOMPLETE) and u15 6,844 s (INCOMPLETE). Every one of the 21 strata
      has a finished draw (21/21), and eight of the ten second draws finished. Not run:
      u31, because no draw started after 06:17 UTC, when a 7,000 s ceiling would have
      ended after the session deadline (the coordinator's re-plan of future slices).
      Draw u29's producer closed at 07:06 UTC after 4,644 s of wall, but its standing
      verification was still running at the verdict, so it is not counted; it is
      admitted only if that verification passes. The 29 finished draws' receipts record
      47,492 s of wall and 43,806 s of process CPU, and their verifications 12,709 s,
      over 31,588 s on two workers from 21:51 UTC. A stratum with one draw describes
      that draw, not a closure rate.
    needs_review: true
    commit: 8464ffcfe
  effort:
    timebox: 7,000 s per state and 4,000 s per verification, one worker per job, two workers, to
      2026-10-06T07:14:04Z
    wall_seconds: 31588
    stopped_by: criterion
---
# exp-257: Session 182 BC-428, H-264’s Unsampled Strata

[H-275](../../../hypotheses/H-275-n17-unsampled-strata-per-state-price.md) asks what
per-state exclusion costs in the 21 strata of the arity8 frame that
[exp-252](exp-252-h264-n17-overnight-per-state-price.md) reported as unsampled, 827
orbits that H-264 did not price.
This round is BC-428 of
[agenda-042](../../../agendas/agenda-042-overnight-n11-settlement-and-low-n-angles.md).
It runs the states under the adaptive-row recipe that closed all four of H-264’s counted
stalls in [exp-253](exp-253-h274-n17-stalls-under-adaptive-rows.md).

The draw is seeded and frozen before the first run: one state per stratum, and a second
from each of the ten strata larger than the mean of 827/21 orbits.
The run order puts every stratum’s first state before any second.
[draw-bc428.cmd.txt](../../../explorations/X048-session-182-overnight/receipts/U/draw-bc428.cmd.txt)
writes the draw from the frame listing and the seed-182 receipt.
Each closed state removes only its own orbit.
The two distance-2 states are reported apart, and any state not run by the deadline is
reported as not run.

## Verdict

Accepted, with needs_review true for the W2 review the coordinator commissions.
Accepted means the frozen measurement ran and answered H-275’s question for the draws it
reached; H-275 is an open question and registers no falsifier, so none survived.

- **Counted draws:** 24 of the 27 that finished closed (89%), each re-proved in full by
  the standing kernel verifier and admitted, the endpoint surviving.
- **Producer fixed points:** u6 and u12, inside the ceiling.
- **INCOMPLETE at the 7,000 s ceiling:** u15; the checker ran out of time, so neither a
  closure nor a fixed point.
- **Distance-2 draws, reported apart:** u8 closed and was admitted and u1 ended
  INCOMPLETE at the ceiling.
- **Cost per closure:** 550 to 1,972 s of process CPU, median 1,090 s; verification 257
  to 954 s, median 472 s. Non-closures: u6 1,863 s (at a fixed point), u12 1,597 s (at a
  fixed point), u1 6,101 s (INCOMPLETE) and u15 6,844 s (INCOMPLETE).
- **Coverage:** 21/21 strata have a finished draw; eight of the ten second draws
  finished.
- **Not run:** u31, because no draw started after 06:17 UTC, when a 7,000 s ceiling
  would have ended after the session deadline.
- **Closed, verification running at the verdict:** u29, whose producer closed at 07:06
  UTC after 4,644 s of wall; not counted, and admitted only if the standing verifier
  passes it.
- **Totals:** the 29 finished draws’ receipts record 47,492 s of wall and 43,806 s of
  process CPU, and their verifications 12,709 s, over 31,588 s on two workers from 21:51
  UTC.

A stratum with one draw describes that draw, not a closure rate.

Added 2026-10-06 at 07:39 UTC, after the verdict: draw 29’s standing verification passed
in full in 1,899 s, and s182-bc428-u29 is admitted, taking the certified census to
36,792 states in 4,686 orbits.
The verdict’s figures above are unchanged.

## Runs

| Order | Stratum | Mask | Outcome | Process CPU | Verifier |
| --- | --- | --- | --- | --- | --- |
| 2 | c3/i>=5/d4 | 4061102 | closed, 4 rounds, admitted | 1,231 s | full pass, 560 s |
| 3 | c4/i<=3/d>=8 | 4439807 | closed, 6 rounds, admitted | 1,174 s | full pass, 472 s |
| 4 | c3/i>=5/d6 | 6020797 | closed, 3 rounds, admitted | 726 s | full pass, 312 s |
| 5 | c<=2/i>=5/d6 | 3931626 | closed, 4 rounds, admitted | 1,135 s | full pass, 563 s |
| 1 | c3/i<=3/d2 (d2) | 1900509 | incomplete at 7,001 s | 6,101 s | — |
| 6 | c4/i4/d>=8 | 5491711 | fixed point after 15 rounds, not closed | 1,863 s | — |
| 7 | c<=2/i4/d6 | 5959674 | closed, 5 rounds, admitted | 1,475 s | full pass, 714 s |
| 8 | c3/i4/d2 (d2) | 3078077 | closed, 3 rounds, admitted | 572 s | full pass, 277 s |
| 10 | c3/i>=5/d>=8 | 5996459 | closed, 2 rounds, admitted | 581 s | full pass, 322 s |
| 9 | c<=2/i4/d>=8 | 5931001 | closed, 5 rounds, admitted | 1,264 s | full pass, 574 s |
| 11 | c<=2/i4/d4 | 3079158 | closed, 4 rounds, admitted | 1,199 s | full pass, 562 s |
| 12 | c<=2/i<=3/d6 | 2818035 | fixed point after 6 rounds, not closed | 1,597 s | — |
| 13 | c<=2/i>=5/d4 | 4061110 | closed, 3 rounds, admitted | 984 s | full pass, 452 s |
| 14 | c<=2/i<=3/d>=8 | 4456442 | closed, 4 rounds, admitted | 1,281 s | full pass, 572 s |
| 16 | c3/i<=3/d>=8 | 4648955 | closed, 7 rounds, admitted | 1,972 s | full pass, 842 s |
| 17 | c3/i4/d>=8 | 5503965 | closed, 5 rounds, admitted | 1,335 s | full pass, 592 s |
| 18 | c<=2/i>=5/d>=8 | 13090300 | closed, 3 rounds, admitted | 936 s | full pass, 420 s |
| 15 | c<=2/i<=3/d4 | 1900531 | incomplete at 7,002 s | 6,844 s | — |
| 19 | c4/i<=3/d6 | 506879 | closed, 3 rounds, admitted | 589 s | full pass, 257 s |
| 20 | c3/i<=3/d6 | 2351099 | closed, 5 rounds, admitted | 1,090 s | full pass, 458 s |
| 21 | c4/i>=5/d>=8 | 5750671 | closed, 6 rounds, admitted | 945 s | full pass, 414 s |
| 23 | c3/i>=5/d6 | 6224571 | closed, 3 rounds, admitted | 550 s | full pass, 267 s |
| 22 | c3/i>=5/d4 | 4061101 | closed, 4 rounds, admitted | 1,384 s | full pass, 954 s |
| 24 | c4/i4/d>=8 | 5504319 | closed, 5 rounds, admitted | 939 s | full pass, 430 s |
| 26 | c<=2/i4/d>=8 | 12843002 | closed, 3 rounds, admitted | 1,034 s | full pass, 493 s |
| 25 | c<=2/i4/d6 | 5685241 | closed, 6 rounds, admitted | 1,722 s | full pass, 754 s |
| 27 | c3/i>=5/d>=8 | 6023931 | closed, 3 rounds, admitted | 757 s | full pass, 329 s |
| 28 | c3/i4/d>=8 | 5470206 | closed, 3 rounds, admitted | 717 s | full pass, 333 s |
| 30 | c3/i<=3/d6 | 2785277 | closed, 8 rounds, admitted | 1,807 s | full pass, 786 s |
| 29 | c4/i<=3/d6 | 769791 | closed, 20 rounds, admitted | 4,522 s | full pass, 1,899 s |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
