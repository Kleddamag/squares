# The ValidTilt9 run: records, how they combine, and its history

**Region.**  Centres [0, 9/2]² (pitch 1/10) × u = tan(θ/2) ∈ [0, 7/16] (14 bins; 7/16 > √2 − 1, so the bins
cover 0 < θ ≤ 45°): 45 × 45 × 14 = 28,350 roots.  Cover `K4_k008_box9.txt` (sha256 4151d7c4…7801).

## The three records

| record | centres | roots | machine |
|---|---|---|---|
| `tilt9_a.jsonl` | x < 38/10 | 23,940 | machine 1 |
| `tilt9_b.jsonl` | x ≥ 39/10 | 3,780 | machine 2 |
| `tilt9_c.jsonl` | 38/10 ≤ x < 39/10 | 630 | machine 2 |

Check: `check_record.py cover/K4_k008_box9.txt tilt9_a.jsonl tilt9_b.jsonl tilt9_c.jsonl --claim tilt` requires
the union of the roots to be exactly the product grid of the region, each root once (result: `check_tilt9.out`).

* `tilt9_a.jsonl` is machine 1's record restricted to the roots with x < 38/10 (header kept).  Machine 1's record
  also held roots with x ≥ 38/10: the 350 pilot roots of [4, 9/2]² (copied verbatim into `tilt9_b.jsonl`) and
  roots of the column 38/10 ≤ x < 39/10 that machine 1 finished before it was stopped (that column is in
  `tilt9_c.jsonl`); these duplicates were dropped by the restriction.
* `tilt9_b.jsonl` starts, after its header, with the 350 pilot roots copied verbatim from machine 1.

## Code

All three records were made with the files of this repository at commit da469ec (`cover.py`, `tier_a.py`,
`tier_b.py`, `tier_b2.py`, `solver.py`, `rf.py`), except the driver `run_all.py`, which was v1 (sha256 899144f9…,
as in da469ec) until 2026-10-05 11:34 UTC and v2 (sha256 cd6627de…) after.  v2 only adds the driver options
`--bmid-u` / `--bmid-w`: a box not touching u = 0 with |u| ≤ bmid_u is handed to the exact Tier B once its centre
width is ≤ bmid_w.  This changes which certifying method is tried on which box, not any certificate.  v2 with the
default `--bmid-u 0` behaves exactly as v1.

## History (UTC, 2026)

* 10-03 22:55: machine 1 starts the whole region (driver v1, default settings), seeded with pilot blocks of the
  same grid and code.
* 10-04 06:10: machine 1 resumed with `--amin 1/1280` (Tier A goes deeper before handing a box to Tier B).
* 10-05 05:06: machine 2 starts on x ≥ 39/10 (its record seeded with the 350 roots of that range already done).
* 10-05 11:34: both machines switch to driver v2 with `--bmid-u 3/16 --bmid-w 1/20`; machine 1 restricted to
  x < 39/10.  Roots already recorded: machine 1 23,012 (incl. the 350 pilot roots with x ≥ 39/10), machine 2 2,432.
* 10-05 13:07: both resumed with `--bmid-u 7/16` (early Tier B hand-off in every u-bin).
* 10-05 14:24: machine 2 was preempted (Spot) and resumed from its record.
* 10-05 15:34: machine 1's stop condition changed to "all roots with x < 38/10 done"; 15:44: reached, stopped.
* 10-05 15:58: machine 2, its own range done, starts the column 38/10 ≤ x < 39/10 in `tilt9_c.jsonl`.
* Both machines' notes as written during the run: `NOTES_machine1.txt`, `NOTES_machine2.txt`.

## Records as published

Only `tilt9_c.jsonl` was edited before publication: in its header line (line 1) the keys of the `sha256` map,
which were absolute paths on the compute machine, were made relative and a `note` field saying so was added.
The hash values and every other line are unchanged; `check_record.py` does not read the header.  The other two
records are published exactly as run.

| record | sha256 as run (uncompressed) | sha256 as published (uncompressed) |
|---|---|---|
| `tilt9_a.jsonl` | 1e7ac2fe55a8292bdd25466aece89f31e7a083afb83601decfb9912642909271 | same |
| `tilt9_b.jsonl` | f802a0e47c3ee3444bf7177dd14f67a4a48ef2d6d593d9c8f6d429e4b9c5fda5 | same |
| `tilt9_c.jsonl` | 4c167fed8a3265ca7205b98967f810a2c4e86963ad80dff98cc8e7bcf6aa1870 | 4a1e798d115ba57ea4504e4714c37420ab31ff7cfb185c291d40428987efefe3 |

`records.sha256` lists the published files, compressed and uncompressed.
