---
title: "exp-255 — Session 182 lane E: the 95 distance-2 n17 orbits searched at the cap"
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-255
  series: series-000
  title: Every distance-2 orbit of the arity8 frame searched for a float placement at U = 1169/250, ten shards
    each with the endpoint's state as its positive control
  date: '2026-10-05'
  hypotheses:
  - H-273
  tier: confirmatory
  subject:
    label: The 95 orbits at Hamming distance 2 from the endpoint's state in survey_n17_residue's arity8 frame (the
      orbits of the H-266 unique-state cover that survive the 90 arity-at-most-8 selector flags), each searched
      for a placement of 17 unit squares in a square of side U = 1169/250.
    engine: devtools.survey_n17_residue (seeded multi-start placement search with confirm rounds, finished by an
      L-BFGS-B descent) from the clean run worktree at the H-273 registration commit f7b45bdbb
    assurance: numerically-checked
    method: numerical-f64
    precision:
      binary_bits: 64
      rounding: IEEE 754 binary64 in NumPy and SciPy L-BFGS-B
    tolerance: >-
      A placement needs every signed margin at least the confirm margin of 1e-6. A float
      search that finds no placement certifies nothing about infeasibility.
    host_system: Linux x86_64 remote session container, project Python 3.14.7, one or two workers per shard at
      nice 10
    engine_commit: f7b45bdbbea084109185fd32298c31cf8af3f693
  instance:
    axis: n
    point: 17
    role: target
  method:
    control: Each shard first searches the endpoint's own state, which is feasible at U, and must place it; all
      ten placed it (penetration 0).
    candidate: The shard's distance-2 orbits, each searched to the survey's full rounds; a placement would stop
      the lane for an exact check.
    runs_per_condition: 1
    interleaved: false
    operator: Claude Session 182; the run operator's lane E queue ran the ten shards on a second clean run
      worktree in the slot left after the kernel lanes
    entry_point: packing/devtools/survey_n17_residue.py
    command: 'From packing/ of the run worktree at f7b45bdbb: nice -n 10 timeout -k 60 3900 .venv/bin/python3 -m
      devtools.survey_n17_residue --flag-set arity8 --distance 2 --sample 0 --shard K/10 --workers W
      --timeout 3600 --output FILE, for K = 0 to 9, with W = 2 when at most two other jobs ran and 1 otherwise.'
    budget: At most 6 CPU-hours, ten shards each at a 3,600 s survey ceiling under a 3,900 s hard timeout
    record: packing/campaign/explorations/X048-session-182-overnight/receipts/E
    dirty: false
    commit: f7b45bdbbea084109185fd32298c31cf8af3f693
  results:
  - shape: determination
    role: outcome
    question: Does the float search place any of the 95 distance-2 orbits at U, which is H-273's reject criterion?
    outcome: criterion_missed
    checked_by: The ten shard receipts (receipts/E/survey-d2-shard-K.json) cover 95 distinct distance-2 orbits,
      10 in each of shards 0 to 4 and 9 in each of shards 5 to 9, every shard complete and none placed. The
      closest misses had best penetrations of 0.00027 (mask 3963647, stratum c4/i4/d2), 0.0015 (mask 1899775)
      and 0.0033 (mask 1900495); the median was 0.032 and the largest 0.073. The distance-2 searches took
      17,311 s of per-state time in all.
  - shape: determination
    role: guard
    question: Does each shard's positive control, the endpoint's own state, place?
    outcome: criterion_met
    checked_by: Every shard's control placed with penetration 0, so the search can find a placement on this
      cover at U.
  verdict:
    decision: unresolved
    primary_criterion: Reject H-273 on one exact placement of a distance-2 orbit at U; a float search can refute
      it but never confirm it, so 95 searches without a placement leave it unresolved.
    reason: >-
      All 95 distance-2 orbits were searched and none placed, while every shard's control
      placed. Under the frozen criterion that is no placement in 95 searches, not a proof
      of infeasibility, so H-273 stays unresolved. The 0.00027 near miss on mask 3963647 is
      the orbit a later exact or longer search would take first.
    needs_review: false
  effort:
    timebox: 3,600 s per shard under a 3,900 s hard timeout, one or two workers
    wall_seconds: 13549
    stopped_by: criterion
---
# exp-255: Session 182 Lane E, the Distance-2 Orbits at the Cap

[H-273](../../../hypotheses/H-273-n17-distance-two-infeasible-at-cap.md) claims that
each of the 95 orbits one cell away from the endpoint’s state, among those the
arity-at-most-8 flags leave, is infeasible at $U$. This round is lane E (BC-421) of
[agenda-042](../../../agendas/agenda-042-overnight-n11-settlement-and-low-n-angles.md),
registered in `f7b45bdbb` before its first shard.
A float search can refute the claim with one placement and never confirm it.

No orbit placed in 95 searches, and every shard’s control placed, so H-273 is unresolved
under its frozen criterion.
Nothing here excludes a state from the certified census.

## Shards

| Shard | Distance-2 orbits | Workers | Wall | Ended (UTC) |
| --- | --- | --- | --- | --- |
| 0 | 10 | 1 | 1,390 s | 12:04 |
| 1 | 10 | 2 | 1,083 s | 12:22 |
| 2 | 10 | 2 | 1,040 s | 12:39 |
| 3 | 10 | 1 | 1,437 s | 15:47 |
| 4 | 10 | 1 | 1,385 s | 16:10 |
| 5 | 9 | 1 | 1,408 s | 16:33 |
| 6 | 9 | 2 | 1,149 s | 16:53 |
| 7 | 9 | 1 | 2,036 s | 17:27 |
| 8 | 9 | 1 | 1,634 s | 17:54 |
| 9 | 9 | 2 | 988 s | 18:10 |

The round’s wall, 13,549 s, is the sum of the ten receipts’ walls.
The second container restart killed shard 3’s first attempt, about four orbits in, and
the third restart came while it waited for a slot; neither attempt left a receipt, and
neither is counted.

## What It Leaves

The near miss on mask 3963647 (penetration 0.00027) is the orbit an exact check or a
longer search would take first.
A placement there would make the near-endpoint stage non-empty, as H-273’s notes say.
The receipts are under
[receipts/E](../../../explorations/X048-session-182-overnight/receipts/E/).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
