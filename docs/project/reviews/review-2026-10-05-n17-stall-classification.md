---
title: n17 Stall Classification
date: 2026-10-05
status: planning-review
---
# n17 Stall Classification

**Session:** 182, lane D (W3, `think-023x`). **Question:** for each kernel run that
stalled tonight, is the stall *loss-limited* (some owner has a supported share below 10
per cent and a median cut margin above the run’s first-order losses at its finest row)
or *consistency-limited* (every owner at least half supported)?
Does the flag-2 reading of session 168 generalise?
Which build comes first: C2, a producer split policy that aims the split budget at the
unsupported owner, or C5, branch predicates that give owners a sub-cell seed?
**Read:** the saved stall nodes of lanes K and A under the session scratchpad, named by
content id below; their kernel receipts (`kernel-k2.json` and the five
`kernel-m*.json`); the lane-A survey receipt `survey-seed182.json`; the
[flag-2 diagnosis](review-2026-10-04-n17-flag2-diagnosis.md) and its committed receipts
under `X048-session-168-pilots/receipts/flag2-diagnosis/`; X-048’s October 5 candidates
C2 and C5; and lane R9’s [capture review](review-2026-10-05-n17-capture-r9.md).
**Method:** the plan’s frozen instrument, `devtools.diagnose_n17_flag` at the run
worktree’s revision, `support NODE --samples 400 --refine 200 --seed 1` and
`domains NODE`, one job at a time at `nice -n 19` with a 1,200 s ceiling, run only while
the one-minute load was below 6 (the coordinator’s relaxation of the plan’s 4.5). One
deviation: at 400 poses per owner the support test on a 17-owner per-state node does not
finish inside the 1,200 s ceiling at tonight’s load (616 CPU-s in 1,200 s of wall on
m2817021, at half a CPU, and the tool writes its receipt only at the end), so the three
per-state nodes were diagnosed at 100 poses per owner, which widens the share estimates
to about $\pm5$ percentage points and leaves the margins’ medians coarser; the receipts
are suffixed `-s100`. The receipts are `support-*.json` and `domains-*.json`, filed
under
[`X048-session-182-overnight/receipts/stall-diagnosis/`](../../../packing/campaign/explorations/X048-session-182-overnight/receipts/stall-diagnosis/)
with the lane’s queue script and summariser as `run-diagnosis.sh.txt` and
`summarise_stall.py.txt`, kept as text so that the repository’s lint does not take them
for tracked code; `summarise_stall.py` turns a kernel receipt and the two diagnosis
receipts into the tables below and applies the plan’s rule, and reproduces the flag-2
review’s numbers from the committed receipts.
First-order losses at a row width are computed as the tool’s `row_losses` does: the
envelope core loses $\tfrac12 - \tfrac{1}{2(\cos(D/2)+\sin(D/2))}$ per face for an
angular width $D$, and a wall row loses the spread of the half-extent over the row, at
most $D/2$; at a chart width $w$ in $t=\tan(\theta/2)$ the widest row is at $t=0$,
$D=2\arctan w$. At $1/512$ that is $0.00097$ core and at most $0.00195$ wall; at $1/32$
it is $0.0149$ core and at most $0.0312$ wall.
Nothing was committed, pushed or posted; lane D writes no shared record.

## Verdict

**One flag stall, loss-limited; seven per-state stalls, four of them a kind the rule did
not anticipate.** Of the eight kernel runs that stalled tonight (one lane-K flag, seven
lane-A per-state nodes), the flag is loss-limited, three per-state nodes are
consistency-limited, and the other four are mixed by the rule’s letter and loss-limited
in substance, at a row width the rule’s second clause cannot see past.
C2 comes first; two zero-build re-runs come before it.

- **K-k2 is loss-limited and aimable at its own floor.** Interior-NW is 0.5 per cent
  supported and interior-W 4.5, with median cut margins of $0.0098$ and $0.0100$, ten
  times the $1/512$ core loss of $0.00097$; the pair is a mutual knot about a unit apart
  that the split policy left at $1/64$ rows (41 of the 704 rows added) while the four
  owners that are 85 to 97 per cent supported took 629. The run stopped at its round cap
  with 2,400 s of producer share unused and the knot still contracting.
  Flag 2’s reading generalises to it, mechanism included.
- **Four per-state stalls (m2817021, m3063677, m2878207 at distances 4, 4 and 6;
  m2784767 at distance 4) are mixed by the rule and loss-limited at a wall in
  substance.** In each, no owner is under 10 per cent, fifteen or sixteen of seventeen
  are over 60, and the one or two under half are neighbours in a five-square wall crowd:
  side-N1 and side-N2 on the north wall in three of them (15 to 39 per cent supported),
  side-W0 and side-W1 on the west wall, flag 2’s own, in m2784767 (20 and 25 per cent).
  The neighbours cannot clear each other by $0.011$ to $0.018$. Those margins are below
  the first-order losses at $1/32$, the only row width lane A’s N1 recipe runs, so the
  rule’s loss clause fails; they are two to four times the losses at lane K’s $1/512$
  floor, where the same nodes would classify as K-k2 does.
  Three of the four never cut a row; m2784767 cut two.
- **Three per-state stalls are consistency-limited: m1964767 and m851903 at distance 2,
  m1949551 at distance 4.** Every owner is at least 63, 72 and 66 per cent supported
  respectively, at fixed points the producer reached in 5, 2 and 13 rounds; a 14-cell
  sub-pattern of m1964767 is float-placeable.
  No pairwise cut at any row width addresses most of their poses.
  m1949551 has the deepest ownership of any stall (side-W0 owns 0.32 of a square), so
  reach is not what these three lack.
- **Flag 2’s reading generalises**, to the flag directly and to four of the seven
  per-state states through the row width: wall crowds held by margins of a few
  thousandths to a hundredth and a half, which the kernel’s first-order losses exceed at
  the rows it was given.
  The consistency-limited stall, where the plan’s negative branch points to a branch
  predicate, occurred three times in seven, twice at the near-endpoint distance.
- **Build C2 first.** It is a producer policy with nothing for a verifier to re-admit,
  it is what the plan’s rule selects on the one flag stall, and the flag is the census’s
  heaviest (2,917 orbits).
  Before it, two re-runs that need no build: K-k2 with more rounds, a 2,304-row cap and
  the octagon core (its knot owners have no wall loss, so the octagon alone puts a
  $1/64$ collision cut near $2.4\times10^{-4}$); and the per-state stalls under the SW9
  adaptive-row recipe instead of N1’s, which is a lane-A recipe question rather than a
  build. C5 second, with the three consistency-limited nodes as its first test and the
  reservation that a branch gives such a node children that are each still pairwise.
- **Limits.** Supported shares are lower bounds and margins upper bounds, in float, on
  sampled poses; the per-state nodes were sampled at 100 poses per owner, not the plan’s
  400, because the frozen run does not finish in 1,200 s on seventeen owners at
  tonight’s load; and the flag class has one member tonight, K-k2, with flag 2 as its
  precedent.

## 1. The Stalls

Eight kernel runs stalled: three before the diagnoses began and five (A-m1964767,
A-m2878207, A-m2784767, A-m1949551, A-m851903) while they ran; lane K’s nine targets
were decided by 11:12 UTC with K-k2 the only stall, and lane A’s twelve draws by 12:07
UTC with five of the ten counted draws closed and both distance-2 draws stalled.
Lane A’s endpoint control, which must stall, is not counted.
Content ids name the saved nodes the diagnoses read.

| Run | Cells | Bins, rows | Rounds, steps at stall | Finest live row | Rows live | Producer outcome | Owners under 10 per cent supported (share; median cut margin) | Finest-row losses (core; wall at most) | Classification |
| --- | --- | --- | --- | --- | ---: | --- | --- | --- | --- |
| K-k2, node `a664143e…` | 7: corner-SW, side-N0, side-W0, side-W1, interior-SW, interior-NW, interior-W | 64; adaptive, floor 1/512, cap 1,152 | 24, 168 | 1/512 | 901 of 1,152 | `round_cap`, still contracting | interior-NW (0.5%; 0.0098), interior-W (4.5%; 0.0100) | 0.00097; 0.00195 | loss-limited, aimable |
| A-m2817021, node `e079a4ab…` | 17 (full state, distance 4) | 32; uniform | 11, 187 | 1/32 | 544 of 544 | `stalled`, no row ever cut | none; side-N2 at 15% (median 0.0143) and side-N1 at 33% (0.0140), both below the 1/32 losses; fifteen owners over 70% | 0.0149; 0.0312 | mixed, consistency-dominated |
| A-m3063677, node `44c915ba…` | 17 (full state, distance 4) | 32; uniform | 6, 102 | 1/32 | 544 of 544 | `stalled`, no row ever cut | none; side-N1 at 37% (median 0.0128, below the 1/32 losses), sixteen owners over 60% | 0.0149; 0.0312 | mixed, consistency-dominated |
| A-m1964767, node `90021eed…` | 17 (full state, distance 2) | 32; uniform | 8, 136 | 1/32 | 523 of 544 | `stalled`, fixed point from round 5 | none; weakest interior-SW and interior-W at 63% (medians 0.0090, 0.0145) | 0.0149; 0.0312 | consistency-limited |
| A-m2878207, node `cd339242…` | 17 (full state, distance 6) | 32; uniform | 11, 187 | 1/32 | 544 of 544 | `stalled`, no row ever cut | none; side-N2 at 17% (median 0.0168) and side-N1 at 39% (0.0144), both below the 1/32 losses; fifteen owners over 69% | 0.0149; 0.0312 | mixed, consistency-dominated |
| A-m2784767, node `226b1ec5…` | 17 (full state, distance 4) | 32; uniform | 13, 221 | 1/32 | 542 of 544 | `stalled`, fixed point from round 4 | none; side-W0 at 20% (median 0.0168) and side-W1 at 25% (0.0177), both below the 1/32 losses; fifteen owners over 73% | 0.0149; 0.0312 | mixed, consistency-dominated |
| A-m1949551, node `be7c5c80…` | 17 (full state, distance 4) | 32; uniform | 13, 221 | 1/32 | 544 of 544 | `stalled`, no row ever cut | none; weakest interior-SW 66%, side-W0 68%, side-S2 69% (medians 0.0136, 0.0127, 0.0072) | 0.0149; 0.0312 | consistency-limited |
| A-m851903, node `d1072390…` | 17 (full state, distance 2) | 32; uniform | 2, 34 | 1/32 | 544 of 544 | `stalled` after two rounds, nothing moved | none; weakest side-E1 72%, side-S1 73%, side-N1 74% (medians 0.0138, 0.0164, 0.0186) | 0.0149; 0.0312 | consistency-limited |

### 1.1 K-k2: A Mixed Arity-7 Flag at the Row Cap

The class is arity 7, {corner-SW, side-N0, side-W0, side-W1, interior-SW, interior-NW,
interior-W} (mask `[0, 5, 6, 10, 16, 17, 18]`), best float penetration
$5.0\times10^{-3}$, projected gain 2,917 orbits and 23,300 states, the largest of lane
K’s targets. The run used the SW9 recipe: 64 bins, envelope core, adaptive rows with a
$1/512$ floor and a 1,152-row cap, 24 rounds, a 7,000 s ceiling.
It ended `round_cap` after 24 rounds and 168 steps, with 901 of 1,152 rows live, having
used 1,777 s of its 4,200 s producer share; the checker certified the stall in 1,271 s
(`PASS_CERTIFIED_STALL`, wall 3,048 s, process CPU 2,331 s). Four of the seven owners
owned no point at the seed (side-N0, side-W0, side-W1, interior-W).

**Where the split budget went.** Rows per owner by round, from the receipt:

| Round | corner-SW | side-N0 | side-W0 | side-W1 | interior-SW | interior-NW | interior-W | Planned | Splits |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 64 | 64 | 64 | 64 | 64 | 64 | 64 | 448 | 0 |
| 6 | 64 | 65 | 64 | 64 | 80 | 64 | 70 | 490 | 19 |
| 12 | 81 | 70 | 78 | 70 | 174 | 71 | 81 | 800 | 175 |
| 17 | 192 | 71 | 230 | 143 | 302 | 80 | 89 | 1,152 | 45 |
| 23 | 210 | 98 | 230 | 143 | 302 | 80 | 89 | 1,152 | 0 |

The cap was reached in round 17. Interior-SW took the most rows (64 to 302, 142 of them
at $1/512$) and side-W1 kept every one of its 143 rows live across all 90 degrees; those
two are the wide owners whose rows never die, as interior-SE and side-S1 were on flag 2.
Side-W0 and corner-SW also reached 230 and 210 rows; interior-W, interior-NW and side-N0
stayed at 89, 80 and 98, most of their live rows still at $1/64$ and $1/128$.

**Not a fixed point.** After the cap, with no further splits, live rows fell from 933
(round 17) to 901 (round 23): side-W0 from 213 to 180, interior-W from 30 to 21,
interior-NW from 36 to 30, side-N0 from 53 to 44, corner-SW from 202 to 191. The
producer stopped at the round cap with the small owners still contracting every round,
as flag 2’s 2,304-row run did at its time share.

**Where the survivors are** (`domains-k2.json`; angles in degrees, $65$ to $90$ being a
turn of $-25$ to $0$):

| Owner | Rows (live) | Live rows by width | Live angle | Centre box of live residuals | Cell | Owned hull | Ideal owned | Largest live core / wall loss |
| --- | ---: | --- | ---: | --- | --- | ---: | ---: | --- |
| corner-SW | 210 (191) | 1/64: 1, 1/128: 57, 1/256: 103, 1/512: 30 | 83.1 | $[0.500, 1.215]\times[0.500, 0.777]$ | $[0.5, 1.29]^2$ | 0.195 | 0.197 | 0.0070 / 0.0065 |
| side-N0 | 98 (44) | 1/128: 36, 1/256: 8 | 32.4 | $[1.290, 1.995]\times[3.984, 4.176]$ | $[1.29, 1.995]\times[3.265, 4.176]$ | 0.183 | 0.187 | 0.0039 / 0.0078 |
| side-W0 | 230 (180) | 1/64: 1, 1/128: 34, 1/256: 121, 1/512: 24 | 69.4 | $[0.500, 0.872]\times[1.454, 1.796]$ | $[0.5, 1.411]\times[1.29, 1.995]$ | 0.437 | 0.443 | 0.0076 / 0.0126 |
| side-W1 | 143 (143) | 1/64: 9, 1/128: 86, 1/256: 48 | 90.0 | $[0.500, 1.180]\times[2.458, 2.681]$ | $[0.5, 1.43]\times[1.995, 2.681]$ | 0.165 | 0.169 | 0.0074 / 0.0089 |
| interior-SW | 302 (292) | 1/64: 1, 1/128: 27, 1/256: 122, 1/512: 142 | 87.8 | $[1.497, 1.924]\times[1.411, 1.581]$ | $[1.411, 2.031]^2$ | 0.447 | 0.452 | 0.0069 / 0 |
| interior-NW | 80 (30) | 1/64: 11, 1/128: 17, 1/256: 2 | 33.1 | $[1.464, 1.998]\times[2.992, 3.263]$ | $[1.411, 2.031]\times[2.645, 3.265]$ | 0.362 | 0.371 | 0.0076 / 0 |
| interior-W | 89 (21) | 1/64: 17, 1/128: 4 | 29.9 | $[2.221, 2.338]\times[2.221, 2.356]$ | $[1.43, 2.338]\times[1.998, 2.678]$ | 0.691 | 0.708 | 0.0073 / 0 |

The owned hull and the ideal owned region agree within four per cent for every owner, so
hull compression is not where this run loses either.
The picture is a west column pushed against its cell edges: corner-SW flat on the floor
($y\le0.777$ of a cell reaching 1.29), side-W1 at the top of its cell ($y\ge2.458$ of
$[1.995, 2.681]$) and the west wall, interior-SW at the bottom of its cell
($y\le1.581$), interior-NW at the top of its ($y\ge2.992$), side-N0 against the ceiling
($y\ge3.984$) and interior-W in the east corner of its cell, a box $0.12\times0.14$.
Interior-W has the largest ideal owned region (0.71) and the coarsest rows (17 of 21
live rows at $1/64$); side-W1 the smallest (0.17), with every angle live, and the finest
split allocation among the owners that never lost a row.

**Support** (`support-k2.json`, 400 poses per owner, 438 s; a supported share is a lower
bound and a margin an upper bound, as the tool searches partner poses rather than
enumerating them):

| Owner | Supported | Cut margin: least, tenth percentile, median | Partners that cannot support (poses, median margin) |
| --- | ---: | --- | --- |
| interior-NW | 0.5 per cent | 0.0003, 0.0044, 0.0098 | interior-W (373, 0.0096), side-N0 (268, 0.0052), side-W1 (101, 0.0036) |
| interior-W | 4.5 per cent | 0.0001, 0.0043, 0.0100 | interior-NW (377, 0.0100), interior-SW (45, 0.0034) |
| side-N0 | 71.5 per cent | 0.0001, 0.0007, 0.0030 | interior-NW (114, 0.0030) |
| interior-SW | 85.0 per cent | 0.0000, 0.0004, 0.0018 | interior-W (43, 0.0017), side-W0 (17, 0.0020) |
| side-W1 | 92.5 per cent | 0.0001, 0.0002, 0.0034 | side-W0 (20, 0.0043), interior-NW (10, 0.0018) |
| side-W0 | 93.5 per cent | 0.0001, 0.0003, 0.0015 | side-W1 (15, 0.0024), interior-SW (8, 0.0013), corner-SW (3, 0.0013) |
| corner-SW | 96.8 per cent | 0.0002, 0.0007, 0.0016 | interior-SW (8, 0.0017), side-W0 (6, 0.0007) |

The knot is the pair interior-NW and interior-W, and it is mutual: 373 of 400 sampled
interior-NW poses overlap every surviving interior-W pose, by a median of $0.0096$, and
377 of 400 interior-W poses overlap every surviving interior-NW pose, by $0.0100$. The
two live boxes, interior-W’s $[2.221, 2.338]\times[2.221, 2.356]$ and interior-NW’s
$[1.464, 1.998]\times[2.992, 3.263]$, put the centres about one unit apart at tilts of
$25$ to $55$ degrees, where two unit squares cannot both be placed; the pattern is close
to pairwise infeasible on that one pair, by about a hundredth, and an exact one-partner
cut would remove nine tenths of either owner’s sampled poses (tenth-percentile margins
$0.0044$ and $0.0043$). Side-N0 is the knot’s third strand, unsupported by interior-NW
for 114 poses at $0.0030$. The two knot owners are the run’s coarsest: 17 of
interior-W’s 21 live rows and 11 of interior-NW’s 30 are the seed’s $1/64$, where the
envelope core loses $0.0076$ per square, so a collision region between two such rows
pays about $0.015$, above the medians, and an owned-hull cut pays $0.0076$ against a
hull that is the common region of every partner pose rather than the best one.
At the run’s $1/512$ floor the same cuts would pay $0.00097$ per square, a tenth of the
medians and a quarter of the tenth percentiles.
The split policy never sent a row to either owner after round 12 (interior-W 81 to 89
rows, interior-NW 71 to 80), because it splits rows whose outer domain has stopped
shrinking and theirs were still shrinking every round; the budget went to interior-SW
and side-W1, which are 85.0 and 92.5 per cent supported and whose rows no one-partner
cut can remove at this state.

### 1.2 A-m2817021 and A-m3063677: Per-State Nodes That Never Cut a Row

Both are full 17-cell occupancy states from lane A’s stratified draw (seed 182), run at
N1’s parameters: 32 uniform bins, envelope core, no adaptive rows, 24 rounds, 7,000 s.

| State | Draw | Distance, stratum | Float penetration (full; minimal sub-pattern) | Rounds, steps | Outcome | Wall, CPU |
| --- | ---: | --- | --- | --- | --- | --- |
| m2817021 | index 4 | 4, c3/i$\le$3/d4 | 0.0315; 0.0126 at arity 13 | 11, 187 | `stalled`, 544 of 544 rows live | 2,073 s, 828 s |
| m3063677 | index 1 | 4, c3/i4/d4 | 0.0481; 0.00074 at arity 12 | 6, 102 | `stalled`, 544 of 544 rows live | 1,129 s, 634 s |
| m1964767 | index 5 | 2, c4/i4/d2 | 0.0120; 0.0 at arity 14 (placed) | 8, 136 | `stalled`, fixed point from round 5, 523 of 544 live | 989 s, 623 s |
| m2878207 | index 8 | 6, c4/i4/d6 | 0.0528; 0.0106 at arity 10 | 11, 187 | `stalled`, 544 of 544 rows live | 1,940 s, 925 s |
| m2784767 | index 10 | 4, c4/i$\le$3/d4 | 0.0335; 0.0048 at arity 10 | 13, 221 | `stalled`, fixed point from round 4, 542 of 544 live | 1,997 s, 828 s |
| m1949551 | index 6 | 4, c4/i4/d4 | 0.0552; 0.0073 at arity 10 | 13, 221 | `stalled`, 544 of 544 rows live | 1,613 s, 1,297 s |
| m851903 | index 9 | 2, c4/i$\le$3/d2 | 0.0115; 0.0031 at arity 15 | 2, 34 | `stalled`, 544 of 544 rows live | 88 s, 77 s |
| m5683195 (closed, for comparison) | index 2 | 4, c3/i4/d4 | 0.0288; 0.027 at arity 13 | 8, 135 | `closed` in round 7 | 2,148 s, 869 s |
| m5500414 (closed, for comparison) | index 3 | 6, c3/i4/d6 | 0.0317; 0.0041 at arity 10 | 8, 129 | `closed`, rows dying from round 2 | 1,109 s, 594 s |

The later stalls arrived while the first two were being diagnosed; m1964767 is of a
different kind and is taken in §1.3, m2878207 and m2784767, which repeat the first two’s
shape, in §1.4, and m1949551 and m851903 in §1.5. One column of the table is worth a
remark before the diagnoses: the survey’s minimal sub-pattern, the smallest set of the
state’s cells the float selector could not place, does not separate the closures from
the stalls. Across lane A’s twelve draws the five that closed have minimal margins from
$3.6\times10^{-4}$ to $0.027$ and the seven that stalled from $0$ (a 14-cell sub-pattern
of m1964767 was placed) to $0.0126$; the full-state penetrations overlap the same way.
Nothing in the float survey predicts which per-state nodes the kernel closes; the
diagnoses below are what carry the classification.
In the first two stalls no row of any owner died in any round: every owner keeps all 32
rows, every angle, and a residual box equal to its cell, except four owners that own
something and whose boxes shrank by 0.1 to 0.2 (corner-NW, side-N0, side-W2 and
interior-NW in m2817021). Thirteen of seventeen owners owned no point at the seed in
each; ten (m2817021) and eight (m3063677) still own nothing at the end.
The receipt signature is the same as the feasible endpoint control’s
(`kernel-control-endpoint.json`: 544 of 544 live, thirteen owners with an empty hull
after five rounds), so at the receipt level these two stalls are indistinguishable from
a true state; only the support test can separate them, and only as far as float evidence
goes. The state that closed, m5683195, started the same way (twelve owners owning
nothing, every row live through round 4), then side-S0 and side-S1 lost rows in round 5
and the cascade closed it two rounds later.
What the kernel needs is a first row to die, from a hull cut or a collision cut, and a
partner for the cascade to pass to; the two stalls never got the first row, and the
support tables below say why.

**Why thirteen owners own nothing.** The seed ownership follows the cells’ shapes.
A unit square covers the disc of radius $1/2$ about its centre at every angle, so every
square centred in a cell covers a common point whenever the cell’s half-diagonal is
under $1/2$; when it is over, the squares at the cell’s far corners, at the angles that
turn a face towards each other, share nothing.
The $0.620\times0.620$ interior cells have half-diagonal $0.438$ and own a region from
the seed (interior-NW owns 0.10 of a square in m2817021); the $0.705\times0.911$ side
cells ($0.576$), the $0.685\times0.930$ ones ($0.578$) and the $0.908\times0.680$
interior-W, S, N and E cells ($0.567$) own nothing; the $0.790\times0.790$ corner cells
($0.559$) own a sliver because the two walls pin their squares into the corner.
Halving a side cell along its long axis brings the half-diagonal to $0.41$ to $0.42$ and
the inscribed-disc bound on the common core to a radius of $0.08$ to $0.09$, which is
C5’s mechanism in numbers: every child of a side cell owns a point from its seed.
What the count of empty owners does not do is predict the outcome: the two states that
closed tonight started with eleven and twelve of seventeen owners owning nothing, the
five that stalled with eleven to thirteen.
The closures began where owners did own something (corner-NW, interior-NW, interior-SW
and side-W1 lost rows first on m5500414; side-S0 and side-S1 on m5683195) and cascaded;
the stalls have the same owning region and the cascade did not start.

**Survivors of m2817021** (`domains-m2817021.json`; every owner keeps all 32 rows and
all 90 degrees, so only the owners whose box or ownership moved are listed; the other
twelve have their cell as box and an owned hull and ideal owned region of 0.000 to
0.006):

| Owner | Centre box of live residuals | Cell | Owned hull | Ideal owned | Largest ideal owned in one 15-degree sector |
| --- | --- | --- | ---: | ---: | ---: |
| corner-NW | $[0.500, 1.099]\times[3.511, 4.176]$ | $[0.5, 1.29]\times[3.386, 4.176]$ | 0.148 | 0.151 | 0.39 |
| side-N0 | $[1.442, 1.995]\times[3.534, 4.176]$ | $[1.29, 1.995]\times[3.265, 4.176]$ | 0.138 | 0.148 | 0.33 |
| side-W2 | $[0.500, 1.169]\times[2.681, 3.205]$ | $[0.5, 1.411]\times[2.681, 3.386]$ | 0.109 | 0.118 | 0.24 |
| interior-NW | $[1.451, 2.031]\times[2.645, 3.224]$ | $[1.411, 2.031]\times[2.645, 3.265]$ | 0.093 | 0.103 | 0.18 |

The four owners that own something are the north-west corner, its two wall neighbours
and the interior cell beside them: the one place where the seed’s owned hulls
(corner-NW’s and interior-NW’s) reached a partner.
Everywhere else nothing reached anything, and the first-order losses at $1/32$ (core
$0.0149$, wall up to $0.0302$ on the live rows) are a tenth of a side.
For the twelve owners that own nothing, confining the angle to one 15-degree sector
raises the ideal owned region to at most 0.04, so an angle branch alone would not give
them a core either; a position branch would.

**Survivors of m3063677** (`domains-m3063677-s100.json`; the same reading, with less
reach: every owner keeps all 32 rows and all 90 degrees):

| Owner | Centre box of live residuals | Cell | Owned hull | Ideal owned | Largest ideal owned in one 15-degree sector |
| --- | --- | --- | ---: | ---: | ---: |
| side-N0 | $[1.393, 1.995]\times[3.460, 4.176]$ | $[1.29, 1.995]\times[3.265, 4.176]$ | 0.075 | 0.084 | 0.27 |
| interior-NW | $[1.411, 2.031]\times[2.669, 3.249]$ | $[1.411, 2.031]\times[2.645, 3.265]$ | 0.034 | 0.043 | 0.12 |
| interior-S | $[1.998, 2.678]\times[1.430, 2.091]$ | $[1.998, 2.678]\times[1.43, 2.338]$ | 0.015 | 0.023 | 0.18 |
| corner-NW | $[0.500, 1.235]\times[3.386, 4.176]$ | $[0.5, 1.29]\times[3.386, 4.176]$ | 0.008 | 0.008 | 0.06 |
| side-S1 | $[1.995, 2.681]\times[0.500, 1.303]$ | $[1.995, 2.681]\times[0.5, 1.43]$ | 0.004 | 0.008 | 0.14 |
| interior-W | $[1.430, 2.338]\times[1.998, 2.556]$ | $[1.43, 2.338]\times[1.998, 2.678]$ | 0.000 | 0.002 | 0.34 |

The other eleven owners own nothing, with boxes equal to their cells or shaved by at
most 0.06. Here an angle branch would do something for a few owners: interior-W confined
to one 15-degree sector would own 0.34 of a square, side-N0 0.27 and interior-S 0.18,
because their partners have already trimmed their boxes on one side; for the eight side
cells with the whole cell as box, no sector owns more than 0.05.

**Support on m3063677** (`support-m3063677-s100.json`, 100 poses per owner, 416 s):

| Owner | Supported | Cut margin: least, tenth percentile, median | Partners that cannot support (poses, median margin) |
| --- | ---: | --- | --- |
| side-N1 | 37 per cent | 0.0010, 0.0030, 0.0128 | side-N2 (53, 0.0125), side-N0 (17, 0.0115), interior-NW (6, 0.0165) |
| side-N2 | 63 per cent | 0.0006, 0.0029, 0.0104 | side-N1 (23, 0.0135), corner-NE (16, 0.0042) |
| interior-NW | 70 per cent | 0.0004, 0.0010, 0.0088 | interior-W (18, 0.0074), side-N0 (10, 0.0124), side-N1 (3, 0.0169) |
| interior-W | 71 per cent | 0.0009, 0.0037, 0.0128 | interior-S (12, 0.0165), interior-NW (11, 0.0108), side-W0 (4), side-W1 (3), interior-E (1) |
| side-W0 | 75 per cent | 0.0007, 0.0036, 0.0119 | side-W1 (16, 0.0172), corner-SW (6, 0.0050), side-S0 (2), interior-W (1) |
| side-S0 | 76 per cent | 0.0000, 0.0006, 0.0078 | side-S1 (12, 0.0079), corner-SW (6, 0.0050), side-W0 (5, 0.0103), interior-S (1) |
| side-E2 | 76 per cent | 0.0002, 0.0042, 0.0106 | side-E1 (17, 0.0133), corner-NE (7, 0.0080) |
| side-S1 | 78 per cent | 0.0013, 0.0040, 0.0094 | side-S0 (9, 0.0097), side-S2 (9, 0.0076), interior-S (4, 0.0207) |
| interior-S | 79 per cent | 0.0009, 0.0016, 0.0135 | side-S1 (10, 0.0172), interior-E (8, 0.0135), interior-W (3), side-S2 (1) |
| interior-E | 82 per cent | 0.0003, 0.0034, 0.0142 | interior-S (9, 0.0054), side-E1 (9, 0.0155), interior-W (1) |
| side-N0 | 84 per cent | 0.0012, 0.0038, 0.0110 | side-N1 (11, 0.0103), corner-NW (4, 0.0107), interior-NW (3, 0.0149) |
| side-W1 | 86 per cent | 0.0029, 0.0064, 0.0180 | side-W0 (12, 0.0180), interior-NW (2), interior-W (1) |
| corner-SW | 89 per cent | 0.0020, 0.0038, 0.0121 | side-W0 (6, 0.0134), side-S0 (5, 0.0116) |
| corner-NW | 92 per cent | 0.0054, 0.0066, 0.0171 | side-N0 (8, 0.0171) |
| corner-NE | 92 per cent | 0.0003, 0.0016, 0.0116 | side-E2 (5, 0.0110), side-N2 (4, 0.0062) |
| side-E1 | 93 per cent | 0.0007, 0.0011, 0.0042 | side-E2 (5, 0.0042), interior-E (2, 0.0148) |
| side-S2 | 93 per cent | 0.0035, 0.0049, 0.0110 | side-S1 (5, 0.0097), interior-S (2, 0.0122) |

No owner is under 10 per cent supported and sixteen of seventeen are over 60; the one
exception is side-N1 at 37 per cent, held by its two neighbours along the north wall
(side-N2 cannot clear 53 of its 100 poses, side-N0 17, by medians of $0.0125$ and
$0.0115$). Under the plan’s rule the node is *mixed*, with the weight on the consistent
side: this is a state the pairwise induction has almost nothing to say about, because
with every owner spread over its whole cell nearly every pose of one owner has some
partner pose that clears it.
The margins where poses are unsupported, $0.004$ to $0.018$ with medians near $0.012$,
are all below the run’s first-order losses at its only row width: at $1/32$ the envelope
core loses $0.0149$ per square and a wall row up to $0.0302$, so a collision cut between
two side-wall rows pays about $0.06$ and none of these poses is within reach of the cuts
the run could make.
That is the second thing the receipt says: lane A ran N1’s recipe, 32
uniform bins without adaptive rows, so the per-state nodes never had the $1/512$ floor
under which lane K closed eight flags tonight; the losses that would have to fall below
$0.012$ for side-N1 are five times too large at $1/32$ and would be about $0.003$ at
$1/512$.

**Support on m2817021** (`support-m2817021-s100.json`, 100 poses per owner, 184 s), the
owners under 90 per cent:

| Owner | Supported | Cut margin: least, tenth percentile, median | Partners that cannot support (poses, median margin) |
| --- | ---: | --- | --- |
| side-N2 | 15 per cent | 0.0000, 0.0041, 0.0143 | side-N1 (63, 0.0150), corner-NE (40, 0.0092) |
| side-N1 | 33 per cent | 0.0006, 0.0035, 0.0140 | side-N2 (45, 0.0112), side-N0 (31, 0.0111), interior-NW (10, 0.0076) |
| side-E1 | 72 per cent | 0.0001, 0.0021, 0.0111 | side-E2 (13, 0.0107), side-E0 (12, 0.0091), interior-E (3, 0.0170) |
| side-S1 | 74 per cent | 0.0001, 0.0039, 0.0123 | side-S2 (16, 0.0081), side-S0 (9, 0.0153), interior-S (3, 0.0123) |
| side-N0 | 76 per cent | 0.0009, 0.0027, 0.0098 | side-N1 (14, 0.0062), corner-NW (6, 0.0145), interior-NW (4, 0.0192) |
| interior-E | 82 per cent | 0.0038, 0.0042, 0.0085 | interior-S (9, 0.0073), side-E1 (7, 0.0094), side-E0 (1), side-E2 (1) |
| corner-NE | 83 per cent | 0.0031, 0.0053, 0.0149 | side-N2 (12, 0.0121), side-E2 (5, 0.0188) |
| side-S0 | 84 per cent | 0.0007, 0.0030, 0.0059 | side-S1 (11, 0.0058), corner-SW (4, 0.0098), side-W0 (1, 0.0145) |
| interior-S | 87 per cent | 0.0024, 0.0050, 0.0093 | interior-E (6, 0.0150), side-S1 (6, 0.0096), interior-NW (1) |
| side-E2 | 87 per cent | 0.0002, 0.0014, 0.0081 | side-E1 (7, 0.0094), corner-NE (5, 0.0081), side-N2 (1) |

The other seven owners (corner-SW, corner-NW, side-W0, side-E0, side-S2, side-W2,
interior-NW) are 89 to 97 per cent supported.
The same wall, the same pair: side-N2 at 15 and side-N1 at 33 per cent, each the other’s
main obstruction (side-N1 cannot clear 63 of side-N2’s poses, by $0.0150$; side-N2
cannot clear 45 of side-N1’s, by $0.0112$), with corner-NE and side-N0 as the second
strands. Both states fill the north wall, corner-NW, side-N0, side-N1, side-N2 and
corner-NE, five squares on a wall of length $3.676$, which is the configuration the
pilots README calls a north-wall crowd and the $D_4$ image of flag 2’s west wall; its
squares must tilt or stagger, and the pairwise margins of about $0.011$ to $0.015$ are
the amount by which the neighbours along the wall fail to clear each other.
Those margins are again under the $1/32$ losses and four to ten times the $1/512$ ones.

### 1.3 A-m1964767: A Distance-2 State at a Fixed Point

The state is one square move from the endpoint’s occupancy state (stratum c4/i4/d2, draw
index 5; lane A reports the distance-2 stratum separately, and lane E’s question,
whether any distance-2 orbit places at $U$, is about states like it).
Its float penetration is $0.0120$, and the survey’s minimal sub-pattern search placed a
14-cell sub-pattern of it exactly (best penetration $0.0$), so whatever excludes it
needs at least fifteen of its seventeen cells jointly.
The kernel (32 uniform bins, envelope core) did make progress: interior-SW fell from 32
to 23 live rows, side-S0 to 22 and side-W0 to 30 by round 4, then nothing changed in
rounds 5 to 7 and the producer stopped as `stalled` at a true fixed point (8 rounds, 136
steps, 523 of 544 rows live, wall 989 s, process CPU 623 s). Twelve of seventeen owners
owned nothing at the seed; at the end the south-west quarter owns hulls (corner-SW,
side-S0, side-W0, interior-SW, interior-W, interior-S, with interior-N on nine vertices)
and the seven side cells on the north, east and the west wall’s upper half own nothing,
their boxes still their cells.
Residual boxes of the owners that moved: corner-SW $[0.500, 1.055]\times[0.500, 1.081]$,
side-S0 $[1.471, 1.995]\times[0.500, 0.821]$, side-W0 $[0.500, 0.930]\times[1.454,
1.995]$, interior-SW $[1.463, 1.900]\times[1.454, 1.752]$, interior-W $[1.430,
2.191]\times[2.381, 2.678]$, interior-S $[2.335, 2.678]\times[1.430, 2.330]$. So the
induction reached from the south-west corner outwards through four owners and stopped;
the support test says whether it stopped at a knot (some owner unsupported by margins
the $1/32$ losses of $0.015$ to $0.030$ exceed) or at a consistent state.

**Survivors** (`domains-m1964767-s100.json`; the owners that moved):

| Owner | Rows (live) | Live angle | Centre box of live residuals | Owned hull | Ideal owned | Largest ideal owned in one 15-degree sector |
| --- | ---: | ---: | --- | ---: | ---: | ---: |
| interior-SW | 32 (23) | 63.9, in $[0, 37.9]$ and $[64.0, 90]$ | $[1.463, 1.900]\times[1.454, 1.752]$ | 0.356 | 0.373 | 0.66 |
| side-S0 | 32 (22) | 61.4, in $[0, 37.9]$ and $[66.5, 90]$ | $[1.471, 1.995]\times[0.500, 0.821]$ | 0.256 | 0.272 | 0.68 |
| side-W0 | 32 (30) | 84.1 | $[0.500, 0.930]\times[1.454, 1.995]$ | 0.216 | 0.231 | 0.46 |
| corner-SW | 32 (32) | 90.0 | $[0.500, 1.055]\times[0.500, 1.081]$ | 0.180 | 0.183 | 0.45 |
| interior-W | 32 (32) | 90.0 | $[1.430, 2.191]\times[2.381, 2.678]$ | 0.093 | 0.108 | 0.40 |
| interior-S | 32 (32) | 90.0 | $[2.335, 2.678]\times[1.430, 2.330]$ | 0.025 | 0.034 | 0.13 |

Interior-SW and side-S0 lost their middle angles, $38$ to $64$ degrees, and keep two
blocks of tilts; their owned hulls, 0.36 and 0.26 of a square, are the largest any
per-state owner reached tonight.
The eleven other owners own nothing (interior-N 0.005), and the seven side cells on the
north, east and upper west walls keep their whole cells.

**Support** (`support-m1964767-s100.json`, 100 poses per owner, 235 s), the owners under
90 per cent:

| Owner | Supported | Cut margin: least, tenth percentile, median | Partners that cannot support (poses, median margin) |
| --- | ---: | --- | --- |
| interior-SW | 63 per cent | 0.0000, 0.0011, 0.0090 | interior-W (13, 0.0036), interior-S (12, 0.0176), side-W0 (11, 0.0090), side-S0 (7, 0.0133) |
| interior-W | 63 per cent | 0.0000, 0.0016, 0.0145 | interior-SW (25, 0.0107), interior-N (16, 0.0146), side-W2 (6, 0.0067) |
| interior-N | 75 per cent | 0.0012, 0.0025, 0.0128 | interior-W (20, 0.0161), side-N1 (5, 0.0073), side-N2 (2, 0.0073) |
| interior-S | 76 per cent | 0.0008, 0.0036, 0.0121 | interior-SW (19, 0.0135), side-S2 (4, 0.0063), interior-N (1), interior-W (1) |
| side-E1 | 76 per cent | 0.0002, 0.0013, 0.0149 | side-E2 (17, 0.0156), side-E0 (9, 0.0063), interior-S (1) |
| side-N2 | 78 per cent | 0.0003, 0.0022, 0.0107 | side-N1 (13, 0.0124), corner-NE (6, 0.0044), interior-N (3, 0.0128), side-E2 (1) |
| side-E2 | 79 per cent | 0.0004, 0.0029, 0.0098 | side-E1 (11, 0.0098), corner-NE (6, 0.0034), side-N2 (4, 0.0109), interior-N (3, 0.0177) |
| side-E0 | 80 per cent | 0.0017, 0.0032, 0.0076 | side-E1 (8, 0.0089), corner-SE (7, 0.0076), interior-S (5, 0.0061), side-S2 (2) |
| corner-SW | 84 per cent | 0.0015, 0.0026, 0.0149 | side-W0 (8, 0.0116), side-S0 (7, 0.0164), interior-SW (3, 0.0117) |
| side-S0 | 84 per cent | 0.0002, 0.0017, 0.0073 | interior-SW (14, 0.0080), corner-SW (2, 0.0037) |
| side-W0 | 86 per cent | 0.0001, 0.0007, 0.0076 | interior-SW (13, 0.0084), corner-SW (1) |
| corner-SE | 89 per cent | 0.0016, 0.0016, 0.0155 | side-E0 (6, 0.0120), side-S2 (5, 0.0155) |

Corner-NW, corner-NE, side-N1, side-S2 and side-W2 are 91 to 95 per cent supported.
Every owner is at least half supported, so the node is *consistency-limited* under the
rule, the only one of the four.
What unsupport there is sits on the interior ring: interior-W and interior-SW, each 63
per cent, cannot clear a quarter of each other’s poses, and interior-N and interior-S
hang on them; the north wall, the knot of the two distance-4 states, is 75 to 94 per
cent supported here (this state has no side-N0). The margins where poses are unsupported
are the same $0.004$ to $0.018$ as elsewhere, below the $1/32$ losses; but even with
every such pose removed, three fifths or more of every owner’s poses would stand, each
cleared by some pose of every partner, and could fall only through a cascade that the
removed poses would have to start.

### 1.4 A-m2878207 and A-m2784767: The Same Shape Again

Both arrived after lane K was decided, both at N1’s parameters, and both repeat the
distance-4 pair’s receipt: m2878207 (draw index 8, distance 6, c4/i4/d6, float
penetration $0.0528$, minimal sub-pattern $0.0106$ at arity 10) ran 11 rounds and 187
steps without a row dying (544 of 544 live, wall 1,940 s, process CPU 925 s), eleven of
seventeen owners owning nothing at the seed; m2784767 (index 10, distance 4,
c4/i$\le$3/d4, penetration $0.0335$, minimal $0.0048$ at arity 10) lost two rows of
side-W0 in rounds 3 and 4 and then sat at a fixed point for nine rounds (542 of 544
live, 13 rounds, 221 steps, wall 1,997 s, CPU 828 s), twelve owners owning nothing at
the seed. In m2878207 the owners that own something are again the west and north-west
(corner-SW, corner-NW, side-S0, side-N0, side-W0, side-W2, interior-SW, interior-NW,
with side-N1 and interior-S on eight and nine vertices) and their boxes shrank by 0.1 to
0.3; in m2784767 only corner-NW, side-N0, side-W2 and interior-NW own hulls of sixteen
vertices and side-W1 eight, and side-W0, the one owner that lost rows, owns nothing with
its box cut to $y\le1.834$. m2878207 fills the north wall (corner-NW, side-N0, side-N1,
side-N2, corner-NE); m2784767 has no side-N1 and instead fills the south wall
(corner-SW, side-S0, side-S1, side-S2, corner-SE) and the west wall (corner-SW, side-W0,
side-W1, side-W2, corner-NW).

**Support on m2878207** (`support-m2878207-s100.json`, 100 poses per owner, 203 s), the
owners under 80 per cent:

| Owner | Supported | Cut margin: least, tenth percentile, median | Partners that cannot support (poses, median margin) |
| --- | ---: | --- | --- |
| side-N2 | 17 per cent | 0.0004, 0.0073, 0.0168 | side-N1 (58, 0.0166), corner-NE (43, 0.0145) |
| side-N1 | 39 per cent | 0.0004, 0.0055, 0.0144 | side-N2 (43, 0.0134), side-N0 (30, 0.0125), interior-NW (13, 0.0129) |
| interior-S | 69 per cent | 0.0003, 0.0038, 0.0093 | interior-SW (22, 0.0081), interior-E (17, 0.0093) |
| side-E1 | 70 per cent | 0.0013, 0.0035, 0.0131 | side-E0 (17, 0.0080), side-E2 (14, 0.0172) |
| interior-SW | 73 per cent | 0.0010, 0.0032, 0.0149 | interior-S (13, 0.0157), side-W0 (11, 0.0112), side-S0 (4, 0.0101) |
| side-N0 | 75 per cent | 0.0005, 0.0036, 0.0145 | side-N1 (14, 0.0162), corner-NW (6, 0.0098), interior-NW (6, 0.0084) |
| side-E2 | 76 per cent | 0.0012, 0.0027, 0.0098 | side-E1 (11, 0.0138), interior-E (5, 0.0146), side-N2 (5, 0.0088), corner-NE (4, 0.0068) |

The other ten owners are 81 to 96 per cent supported.
This is the north-wall crowd a third time: side-N2 at 17 and side-N1 at 39 per cent,
side-N1 unable to clear 58 of side-N2’s poses by $0.0166$ and corner-NE 43 of them by
$0.0145$, side-N2 unable to clear 43 of side-N1’s by $0.0134$ and side-N0 30 by
$0.0125$. The margins, $0.013$ to $0.017$ at the medians, are the largest of the three
crowds and still under the $1/32$ losses; at $1/512$ they would be three to four times a
collision cut’s cost.
Under the rule: *mixed*, consistency-dominated, and loss-limited at the north wall
relative to the finer floor, as the distance-4 pair.

**Support on m2784767** (`support-m2784767-s100.json`, 100 poses per owner, 172 s), the
owners under 80 per cent:

| Owner | Supported | Cut margin: least, tenth percentile, median | Partners that cannot support (poses, median margin) |
| --- | ---: | --- | --- |
| side-W0 | 20 per cent | 0.0014, 0.0036, 0.0168 | side-W1 (58, 0.0168), corner-SW (35, 0.0134) |
| side-W1 | 25 per cent | 0.0008, 0.0049, 0.0177 | side-W0 (54, 0.0163), side-W2 (29, 0.0145), interior-NW (15, 0.0126) |
| side-S0 | 73 per cent | 0.0008, 0.0021, 0.0144 | side-S1 (17, 0.0146), side-W0 (7, 0.0132), corner-SW (3, 0.0144), interior-S (1) |
| side-S2 | 75 per cent | 0.0002, 0.0016, 0.0095 | side-S1 (21, 0.0084), corner-SE (2), side-E0 (2), interior-S (1) |
| side-S1 | 79 per cent | 0.0014, 0.0035, 0.0184 | side-S2 (11, 0.0187), side-S0 (10, 0.0175) |

The other twelve owners are 81 to 97 per cent supported.
Here the crowd is on the west wall, flag 2’s own: corner-SW, side-W0, side-W1, side-W2
and corner-NW fill it, and side-W0 (20 per cent) and side-W1 (25 per cent) are each
other’s obstruction (58 and 54 of 100 poses, by $0.0168$ and $0.0163$), with corner-SW
and side-W2 as the second strands.
The south wall is also full and its three side cells are 73 to 79 per cent supported,
with side-S1 against both its neighbours at $0.018$: a second, weaker crowd.
Side-W0 is the one owner that lost rows (two of 32, cutting its box to $y\le1.834$) and
it owns nothing; the induction got exactly as far as the losses allowed and stopped.
*Mixed* under the rule, consistency-dominated, loss-limited at the west wall relative to
the finer floor.

### 1.5 A-m1949551 and A-m851903: Lane A’s Last Two Stalls

These two arrived after the review was first filed, with lane A’s twelve draws then all
run. m1949551 (draw index 6, distance 4, c4/i4/d4, float penetration $0.0552$, minimal
sub-pattern $0.0073$ at arity 10 on the north wall and the west side) ran 13 rounds and
221 steps without a row dying (544 of 544 live, wall 1,613 s, process CPU 1,297 s),
twelve of seventeen owners owning nothing at the seed.
It has the most reach of any stall: eleven owners end with a sixteen-vertex hull and
boxes cut by 0.3 to 0.5 (corner-SW to $y\le0.845$, side-W0 to $[0.500, 0.957]\times
[1.393, 1.849]$, side-S1 to $y\le1.011$, interior-SW to $[1.463, 1.970]\times[1.411,
1.728]$, interior-S to $x\ge2.400$), and still no row died.
Its north wall is full (corner-NW, side-N0, side-N1, side-N2, corner-NE). m851903 (index
9, distance 2, c4/i$\le$3/d2, penetration $0.0115$, minimal $0.0031$ at arity 15) is the
quickest stall of the night: two rounds and 34 steps in 88 s, nothing moved, every box
its cell, only the four corners owning a five-vertex sliver, thirteen owners owning
nothing. It fills the north, south and east walls and has no side-W0.

**Survivors and support on m1949551** (`domains-m1949551-s100.json`,
`support-m1949551-s100.json`, 100 poses per owner, 256 s). Ownership is the deepest of
any stall: side-W0 owns 0.32 of a square (ideal 0.34), interior-SW 0.26, side-W1 0.19,
interior-W 0.13, side-S1 0.12, corner-SW 0.08, interior-S 0.06, corner-SE 0.05; the four
north side cells, side-E1 and side-E2 own nothing.
The owners under 80 per cent supported:

| Owner | Supported | Cut margin: least, tenth percentile, median | Partners that cannot support (poses, median margin) |
| --- | ---: | --- | --- |
| interior-SW | 66 per cent | 0.0010, 0.0034, 0.0136 | interior-S (17, 0.0098), side-W0 (13, 0.0157), interior-W (9, 0.0133) |
| side-W0 | 68 per cent | 0.0018, 0.0039, 0.0127 | side-W1 (16, 0.0127), corner-SW (14, 0.0107), interior-SW (5, 0.0066) |
| side-S2 | 69 per cent | 0.0003, 0.0012, 0.0072 | side-S1 (13, 0.0097), corner-SE (10, 0.0120), interior-S (10, 0.0035) |
| side-N2 | 71 per cent | 0.0007, 0.0038, 0.0108 | side-N1 (13, 0.0087), corner-NE (9, 0.0065), interior-N (6, 0.0203), side-E2 (2) |
| side-N0 | 72 per cent | 0.0031, 0.0049, 0.0137 | side-N1 (15, 0.0165), corner-NW (6, 0.0068), interior-W (4, 0.0116), side-W1 (3) |
| interior-W | 73 per cent | 0.0003, 0.0016, 0.0102 | interior-SW (12, 0.0050), interior-N (8, 0.0112), interior-S (4), side-W1 (4) |
| interior-S | 78 per cent | 0.0044, 0.0078, 0.0130 | interior-SW (13, 0.0165), interior-W (4, 0.0149), side-S1 (3), side-S2 (2) |
| interior-N | 79 per cent | 0.0025, 0.0027, 0.0077 | interior-W (15, 0.0064), side-N1 (4, 0.0127), side-N2 (2) |

The other nine owners are 81 to 93 per cent supported.
Every owner is at least two thirds supported, so the node is *consistency-limited*, the
second of the night and the first at distance 4. Its north wall is full, as in the three
north-wall crowds, but here the crowd is not a knot: side-N0, side-N1 and side-N2 are
72, 81 and 71 per cent supported, each by every partner for most of its poses.
What little unsupport there is sits on the owners that own the most (interior-SW,
side-W0, side-W1, interior-W), in the south-west where the induction did its work;
margins where poses are unsupported run $0.004$ to $0.020$, below the $1/32$ losses as
everywhere.
This state and m1964767 are the two the pairwise kernel cannot address at any
row width, and the two with the deepest reach among the stalls, which is one more reason
to doubt that ownership is what the stalls lack.

**Support on m851903** (`support-m851903-s100.json`, 100 poses per owner, 117 s), the
owners under 80 per cent:

| Owner | Supported | Cut margin: least, tenth percentile, median | Partners that cannot support (poses, median margin) |
| --- | ---: | --- | --- |
| side-E1 | 72 per cent | 0.0030, 0.0072, 0.0138 | side-E2 (17, 0.0136), side-E0 (12, 0.0158) |
| side-S1 | 73 per cent | 0.0026, 0.0072, 0.0164 | side-S2 (18, 0.0133), side-S0 (13, 0.0165) |
| side-N1 | 74 per cent | 0.0006, 0.0051, 0.0186 | side-N2 (14, 0.0171), side-N0 (13, 0.0189) |
| side-S0 | 78 per cent | 0.0012, 0.0016, 0.0087 | side-S1 (15, 0.0069), corner-SW (7, 0.0093) |
| side-N0 | 78 per cent | 0.0012, 0.0016, 0.0063 | side-N1 (13, 0.0144), corner-NW (8, 0.0034), side-W2 (2) |

The other twelve owners are 82 to 95 per cent supported.
Every owner is at least 72 per cent supported, so the node is *consistency-limited*, the
third of the night and the second at distance 2. It has three full walls (north, south
and east) and each wall’s middle square is the least supported owner, at 72 to 74 per
cent, held by its two wall neighbours by $0.013$ to $0.019$; but with every owner spread
over its whole cell and nothing having moved, three quarters of every owner’s poses
clear some pose of every partner, and the crowds are spread rather than knotted.
The producer saw this in two rounds, which is the cheapest stall of the night (88 s) and
the clearest statement of what the pairwise induction can and cannot do from a
whole-cell seed: at this state no one-partner cut, however exact, removes a quarter or
more of any owner.

## 2. The Flag-2 Baseline Under the Plan’s Rule

Applying the plan’s rule to the committed flag-2 receipts, as the generalisation test
needs a stated baseline:

- At the 1,152-row fixed point no owner is under 10 per cent supported; side-W0 (27.0),
  side-W1 (24.5) and side-W2 (46.5 per cent) are under half.
  Under the rule that state is *mixed*, not loss-limited, although the review read it as
  “losses larger than the margins” (median cut margins 0.0031 to 0.0050 against the
  envelope core’s 0.0076 on $1/64$ rows and wall losses of 0.0073 to 0.0154).
- At the 2,304-row producer state side-W0 is 0.0 per cent supported with a median cut
  margin of 0.0042, above the finest-row core loss of 0.00097 (side-W0 has no wall
  loss), so that state is *loss-limited* and aimable at the current floor; side-W1 is at
  13.5 per cent.

So flag 2’s own reading is a reading of the second state: the knot becomes unsupported
only after the partners’ survivors have shrunk around it, and the 1,152-row fixed point,
which is the kind of state a stalled run leaves behind, sits between the rule’s two
classes.

## 3. Classification

**K-k2 is loss-limited, and aimable at the run’s own floor.** Two owners are under 10
per cent supported (interior-NW 0.5, interior-W 4.5 per cent) with median cut margins of
$0.0098$ and $0.0100$, ten times the $1/512$ core loss of $0.00097$ and five times a
collision region’s $0.0019$ at that width; neither owner touches a wall, so no wall loss
applies. The remaining five owners are 71.5 to 96.8 per cent supported.
Under the plan’s rule that is the loss-limited class, with no owner in the 10-to-50
band.

**Flag 2’s reading generalises to this flag, mechanism included.** The three elements of
the flag-2 diagnosis recur: a knot of two or three owners that no partner can clear, by
margins of a few thousandths to a hundredth; wide owners (here interior-SW and side-W1,
there interior-SE and side-S1) that every partner supports, whose rows never die and
that nonetheless take the split budget because the policy splits rows whose outer domain
has stopped shrinking; and knot owners left at the seed’s $1/64$ rows, where the
envelope core’s $0.0076$ exceeds the margins.
Two things are stronger here than on flag 2. The knot’s margins are a hundredth rather
than $0.003$ to $0.004$, so the gap between what an exact one-partner cut could remove
and what the $1/64$ cuts remove is wider, and the knot is a mutual pair rather than one
owner against several.
And the run stopped at the round cap with 2,400 s of its producer share unused and the
knot still contracting, so the cheapest next observation is the same run with more
rounds, before any policy change.
One thing is weaker: the least margins ($0.0001$ to $0.0003$) are below the finest-row
losses, so a cut at the floor would not remove every sampled knot pose at this state;
flag 2’s side-W0 had a least margin of $0.0016$ at 2,304 rows.
Whether those few poses die as the partners shrink around them, as side-W0’s did between
1,152 and 2,304 rows, is what the aimed run would show.

**m3063677 is consistency-dominated, with one owner the row width hides.** No owner is
under 10 per cent and sixteen of seventeen are over 60, so the rule’s loss-limited class
is empty; side-N1 at 37 per cent keeps the node out of the consistency-limited class by
its letter. But side-N1’s margins, median $0.0128$, sit below every first-order loss the
run could pay at $1/32$ (core $0.0149$, wall up to $0.0302$), so no cut available to
that run could have removed them, and the rule’s second clause, margins above the
finest-row losses, fails for the only owner that is unsupported at all.
The reading is that the state is held jointly: its full-state penetration is large
($0.048$), its minimal infeasible sub-pattern misses by only $7.4\times10^{-4}$ at arity
12, and the pairwise induction, with whole cells as every owner’s survivors, sees almost
none of it. The knot that exists, side-N1 against the north wall, is one the row width
hides rather than one the policy could aim at: nothing in a run where no row has died
gives an aimed split anything to act on, and the owners that own nothing are the side
cells whose half-diagonal exceeds $1/2$. A finer floor comes before either candidate
here.

**m2817021 is the same case with a sharper knot.** Side-N2 at 15 and side-N1 at 33 per
cent, mutually unsupported by $0.011$ to $0.015$, fifteen owners over 70 per cent, no
owner under 10: *mixed* by the rule, consistency-dominated in count, and again the
unsupported margins are below the $1/32$ losses, so the rule’s loss clause cannot fire
at this row width. The knot is real and it is flag 2’s: a wall crowd whose neighbours
cannot clear each other by about a hundredth.
Had this node been run at lane K’s floor, where a collision cut between two wall rows
pays at most about $0.006$ (two envelope cores of $0.00097$ at $1/512$ plus two wall
losses of up to $0.002$; about $0.004$ with the octagon), side-N2’s median margin would
exceed the losses by a factor of two to three and the state would classify as
loss-limited and aimable, as K-k2 does.
**m2878207 and m2784767 repeat it**, the first on the north wall (side-N2 17, side-N1 39
per cent, margins $0.013$ to $0.017$), the second on the west wall (side-W0 20, side-W1
25 per cent, $0.013$ to $0.018$), each with fifteen owners over 69 per cent.
So for the four wall-crowd stalls the honest classification is in two parts: under the
rule as written, at the row width they were run, *mixed*; relative to the floor the rest
of tonight’s kernel work used, *loss-limited at one wall, with the rest of the state
consistent*. What they are not is evidence that the induction has nothing to cut: in
each, 63 to 85 of 100 sampled poses of the least supported owner are removable by an
exact one-partner cut.

**m1964767 is consistency-limited, the first of three.** Every owner is at least 63 per
cent supported at a true fixed point, so under the rule, and under any row width, this
is the stall of a pairwise induction that has run out of pairwise facts: for three
fifths or more of every owner’s poses some pose of every partner clears them, and no cut
that reasons from one partner at a time removes a pose like that, however fine the rows
or exact the core. m1949551 (every owner at least 66 per cent, the deepest ownership of
any stall) and m851903 (at least 72 per cent, nothing moved in two rounds) are the same
class, in §1.5; with them the consistency-limited stalls are three of seven per-state
stalls and both of the distance-2 draws.
It is also the state whose survey record says the exclusion is joint: a 14-cell
sub-pattern of it was placed in float, so nothing smaller than fifteen of its cells is
infeasible, and its full penetration of $0.012$ is the smallest of the six.
It is one square move from the endpoint’s state, in the stratum lane A reports
separately and lane E would search.
What it is not, on tonight’s evidence, is a false flag: a float penetration of $0.012$
is twelve times the selector’s margin and the survey’s searches did not place it; but
the pairwise kernel is the wrong instrument for it at any row width, and a branch (C5)
would give it children that are each still pairwise.

## 4. C2 Against C5

The two candidates answer different stalls, and tonight’s stalls split by lane.

**C2, aimed splits** (a producer policy: split first the rows of the owner with the
smallest supported share or the smallest residual, skip owners whose poses are
supported; the checker already admits any complete refinement, so no grammar, checker or
verifier change and no new admission review).
*What tonight bears on it:* K-k2 is the first half of its test, met: a classified
loss-limited flag whose knot the current policy starved at $1/64$: the four owners that
are 85 to 97 per cent supported took 629 of the 704 rows added, the two knot owners 41.
Flag 2 at 2,304 rows is the same reading.
The second half, that the aimed run closes the flag, is untested; the falsifier stands
(an aimed run to a fixed point that leaves the knot live with its margins unchanged).
*Expected gain:* K-k2 alone is 2,917 orbits and 23,300 states of projected gain, the
largest single flag in the census; flag 2 is 122 orbits at arity 9. *What it cannot do:*
nothing for a node where no row has died, since there is no shrinking owner to aim at
and the $1/32$ losses exceed the knot’s margins; and nothing for an owner that is
supported, which is why it must skip them.
*Cost:* one producer slice; the diagnostic that would drive the policy at run time
(`pairwise_support`) is float and about 400 to 900 s per node at the plan’s sample size,
so a production policy would use a cheaper proxy (the owner’s residual area or its
row-death rate, both in the receipt) and the support test stays a diagnostic.

**C5, branch predicates** (a grammar change: a closed centre-halfplane split of a cell
along its long axis, two children, with producer, checker and verifier changes and a
review before any certificate is admissible; the consumer needs a rule that admitted
children cover the parent).
*What tonight bears on it:* the half-diagonal arithmetic of §1.2 confirms the mechanism
for every side cell (no common core from the whole cell, a core of radius $0.08$ to
$0.09$ from a half-cell), and the four wall-crowd stalls are exactly the states C5
names, where eleven to thirteen of seventeen owners own nothing and the induction never
starts. What the support receipts add cuts the other way: on all four wall-crowd states
the induction’s failure to start is not the absence of a knot but a knot held by margins
that the $1/32$ losses hide (two wall neighbours, 63 to 85 of 100 poses removable by an
exact one-partner cut), and the collision cut that removes such poses needs no
ownership, which is how m5683195 and m5500414 closed from seeds where eleven and twelve
owners owned nothing.
So the premise that reach is what stalls per-state nodes is not what these four nodes
show; resolution is.
The nodes where consistency rather than resolution is the limit are the three
consistency-limited fixed points (m1964767, m1949551, m851903), and a branch would hand
each to two pairwise children; m1949551, with the deepest ownership of any stall, says
that reach is not what they lack either.
*Expected gain:* per-state exclusion in the residue tail (2,197 orbits in 17,168 states
at the recheck), which lane A prices tonight.
*What it cannot do:* a half-cell seed gives an owner a core, not a closure; whether the
children close within the ceiling is the claim’s untested half, and each branch doubles
the per-state cost. *Cost:* a multi-slice build (producer, checker, verifier, consumer
rule) with a review, against C2’s single producer slice.

**Where they meet:** on K-k2 the knot owners are interior cells with half-diagonal under
$1/2$, so they own a core already and a branch would not help them; on the wall-crowd
states the knot exists but an aimed split has nothing to act on until a row dies, which
at $1/32$ almost none can.
Flag stalls and per-state wall-crowd stalls are two failure modes; the first has its
remedy in C2, the second in the row floor first and C5 after, and the three
consistency-limited states are a third mode that neither candidate addresses directly.

## 5. What to Build First

**C2 first, as a producer slice, with two zero-build observations before it.** The
reasons, in order of weight:

1. The plan’s own decision rule: a loss-limited lane-K stall selects the aimed-split
   policy. K-k2 is loss-limited by a wide margin (medians ten times the floor’s loss),
   and it is the only stall among lane K’s nine targets: k1 and k3 to k9 closed under
   the SW9 recipe as it stands, the last of them at 11:12 UTC. It is also the heaviest
   flag in the census (2,917 orbits).
2. C2 changes nothing that a verifier checks.
   The checker admits any complete refinement, so an aimed run’s closure is admissible
   under the standing verifier the same night it is produced, and no review gates it.
   C5 is four components and a review before its first admissible certificate.
3. The cheapest observation needs no build at all: re-run K-k2 with `--max-rounds`
   raised (the run used 24 rounds and 1,777 s of a 4,200 s producer share),
   `--max-rows 2304` as flag 2 was given, and `--core octagon`. The octagon matters here
   more than it did on flag 2: K-k2’s knot owners have no wall loss, so the envelope
   core’s $0.0076$ on their $1/64$ rows is their whole first-order loss, and the
   octagon’s $1.2\times10^{-4}$ a face would put a collision cut between two $1/64$ rows
   at about $2.4\times10^{-4}$, below the knot’s tenth-percentile margins of $0.0043$,
   without a single split.
   The caveat is lane K2’s W7 finding that the octagon does not remove a coarse row’s
   domain loss, so the hull side of the cut may still need the rows.
   If the knot closes under that run, the aimed policy is confirmed cheaper than
   expected; if the wide owners again take the budget while interior-NW and interior-W
   stay at $1/64$ and live, that run is C2’s control.
   Either way it costs about an hour of one worker.
   The second observation is lane A’s: re-run the four wall-crowd stalls under the SW9
   recipe (`--split-floor 512 --max-rows 1152`, or the 2,304 cap) rather than N1’s, so
   that their knots meet losses of $0.003$ to $0.006$ instead of $0.015$ to $0.03$.
   H-264 registered N1’s parameters, so whether that re-run is a new experiment or a
   rewrite of the unlanded record is the coordinator’s call, not this review’s.
4. The aimed policy’s selector should be a receipt quantity, not the support test: the
   owner whose live rows are still dying each round, or whose residual area is smallest,
   with owners whose rows have not died in $k$ rounds skipped.
   On K-k2 both proxies pick interior-W and interior-NW; on flag 2 both pick side-W0.
   The support test remains the diagnostic that validates the proxy on a saved node, at
   400 to 900 s for a flag and 180 to 420 s for a per-state node at 100 poses.

**C5 second, and only after the per-state stalls have been re-run at the finer floor.**
C5 is aimed at the per-state nodes, but four of tonight’s seven per-state stalls turn
out to be resolution stalls with a wall-crowd knot, which the adaptive-row recipe
addresses without a grammar change, and a per-state closure removes one orbit where a
flag removes thousands; lane A’s survey exists to price exactly that trade.
If the re-run at $1/512$ still leaves them, or if lane A ends with fewer than half its
counted draws closed, the plan already names a grammar change as the consequence, and
C5’s half-cell seed is the version of it that tonight’s numbers support for the hull
side of the cut: every side cell’s children own a core, no angle sector of a whole-cell
parent does. Its first falsifier test is then cheap: run both children of one half-split
on the three consistency-limited nodes (m1964767, m1949551, m851903) and on m3063677,
and see whether any pair closes where the parent stalled.
On the consistency-limited three the expectation should be modest: each parent is at a
fixed point with every owner over 60 per cent supported, and each child is a pairwise
induction over a smaller seed; what C5 would show there is whether a smaller seed
changes the supported shares, which is the measurement to take before and after.

**Not recommended first:** the octagon core as a candidate build on its own (it is a
setting, taken into the re-run above; it does nothing for wall-loss knots such as flag
2’s side-S0, side-W1 and side-W2); the branch and bound (out of reach at these arities,
per the flag-2 review); and finer rows on the supported owners, which is the experiment
K-k2 already ran.

## Evidence Status

| Kind | Items |
| --- | --- |
| Read exactly from the saved nodes, converted to floats | every row count, live row, row width, angle block, centre box and owned hull area in the domains tables; the four nodes are the producers’ certified stall states (`PASS_CERTIFIED_STALL`) |
| Read from the kernel receipts | per-round rows, live rows and splits; producer outcomes, wall and CPU; seed ownership; the recipes (K: 64 bins, adaptive rows to $1/512$, cap 1,152; A: 32 uniform bins) |
| Read from the survey receipt | each lane-A state’s draw index, distance, stratum, full-state and minimal-sub-pattern float penetrations |
| Float estimates | supported shares (lower bounds) and cut margins (upper bounds) from sampled poses, 400 per owner on K-k2 and 100 on the per-state nodes; ideal owned regions; first-order losses |
| Measured for this review | the diagnoses’ cost: `support` at 400 poses, 367 CPU-s on the 7-owner node and over 616 CPU-s without finishing on a 17-owner node; at 100 poses 111 to 256 CPU-s on 17 owners; `domains` 3 to 5 CPU-s; about 0.7 CPU-h for the lane, the restart loss included |
| Derived here | the finest-row losses from the row-loss formulas; the cell half-diagonal argument for seed ownership; the classification under the plan’s rule and its reading at the $1/512$ floor; the flag-2 baseline under the same rule; the minimal-sub-pattern remark (four states); the C2 and C5 assessment and the build order |
| Not done | any placement search on tonight’s nodes (`place`); any exact or interval form of the support test; any run of an aimed policy, an octagon or finer-row re-run, or a branched child; any change to a record |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
