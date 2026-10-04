---
title: n17 Flag 2 Diagnosis
date: 2026-10-04
status: planning-review
---
# n17 Flag 2 Diagnosis

**Session:** 168, lane K3. **Question:** flag 2, the arity-9 class {corner-SW, side-S0,
side-W0, side-S1, side-W1, side-W2, interior-NW, interior-W, interior-SE} (mask
`[0, 4, 6, 8, 10, 14, 17, 18, 22]`, 122 orbits), stalled the kernel at 1,152 adaptive
rows and did not close at 2,304, with interior-SE and side-S1 never losing a row.
Is it a false flag, a pattern that fits at the cap and that no sound prover can exclude,
or a true pattern the kernel cannot yet close, and if so, what holds the kernel open?
**Read:** lane K2’s saved objects of both runs, the 1,152-row node `89a19166…` behind
[`kernel-split-flag2-a9-bins64.json`](../../../packing/campaign/explorations/X048-session-168-pilots/receipts/kernel-split-flag2-a9-bins64.json)
and the 2,304-row node `3de853f3…`, saved when its producer stopped and read while its
check was still running; nothing of that run was touched.
That check then reached its 12,000-second ceiling and ended `INCOMPLETE` (“row sweep
timeout: checked=5625, total=17633”), so the 2,304-row node is the producer’s state, not
yet certified; the 1,152-row node passed its saved check as a stall.
**Method:** a new tool,
[`diagnose_n17_flag.py`](../../../packing/devtools/diagnose_n17_flag.py), with
`packing/tests/test_diagnose_n17_flag.py`. It reads a node’s `final_state`, which sorts
before `steps` in the canonical bytes, off the front of the file with the checker’s
`stream_node`, so neither node was loaded whole.
The receipts are in
[`receipts/flag2-diagnosis/`](../../../packing/campaign/explorations/X048-session-168-pilots/receipts/flag2-diagnosis/).

## Verdict

**LIKELY TRUE, with obstruction.** No placement was found, so there is nothing to check
exactly, and nothing in the selector’s flag list or census projections changes.

- **The pattern misses by about 0.8 per cent of a side.** The selector’s own search,
  warm started from 64 poses drawn from the kernel’s survivors, ends at a worst
  violation of $9.80\times10^{-3}$ after 613 attempts; 200 survivor-seeded descents end
  at $1.03\times10^{-2}$; the selector’s earlier receipts give $9.29\times10^{-3}$. The
  search places squares of side $0.99197$ in the nine cells, and none of side $0.99199$.
- **The obstruction is the west wall, carried east.** Four squares stand on the west
  wall with the top centre held at $y\le3.386$ by side-W2’s cell, so they span at most
  $3.886$ and must tilt or stagger; every surviving pose of side-W0, side-W1 and side-W2
  is tilted. Every near placement tilts them together, at about $12°$ or about $17°$, and
  binds side-S0 against side-W0 and the floor, side-W0 against side-W1, side-W1 against
  side-W2 and side-W2 against its cell’s top edge, each by $0.006$ to $0.010$. The push
  reaches side-S1 and interior-SE through side-S0 and interior-W, and both end on their
  cells’ east edges.
- **Interior-SE and side-S1 have room in the kernel, not in a placement.** Holding
  interior-SE at any of $0°, 15°, \dots, 75°$ leaves a violation of at least
  $1.03\times10^{-2}$, and side-S1 at least $9.75\times10^{-3}$. At the 2,304-row state
  90.5 and 96.5 per cent of their sampled surviving poses are supported: every partner
  keeps a pose that clears them.
  No cut that reasons from one partner at a time, however fine its rows or exact its
  core, can remove those poses until the west owners shrink.
  They hold 771 of the run’s 2,138 rows, 36 per cent, none of which could die at that
  state.
- **The knot is side-W0, and losses the size of its margins keep it.** None of 200
  sampled side-W0 survivors is supported: each overlaps every surviving pose of some
  partner, side-W1 for 189 of them and side-S0 for 179, by a margin of at least $0.0016$
  and a median of $0.0042$. At 1,152 rows the losses were larger than such margins (wall
  losses up to $0.015$, the envelope core’s $0.0076$ on the seed’s $1/64$ rows), and the
  run reached a true fixed point.
  At 2,304 the wall losses had fallen to $0.004$ or less and the knot moved again: the
  producer stopped at its time share with side-W0, side-S0, side-W1 and corner-SW still
  losing live rows every round.
  That run is not a fixed point.
- **What would close it:** a longer run with the split budget aimed at the knot (side-W0
  first, whose live rows are still mostly $1/64$, then side-W1, side-S0 and interior-W)
  instead of at interior-SE and side-S1, with the octagon core, which removes the core
  loss but not the wall loss.
  Finer rows on interior-SE alone would not.
  The branch and bound is not a practical route at arity 9 (section 5).

## 1. The Pattern

The nine cells fill the south-west of the centre box.
Corner-SW, side-W0, side-W1 and side-W2 run up the west wall, with centre ranges
$y\in[0.5,1.29]$, $[1.29,1.995]$, $[1.995,2.681]$ and $[2.681,3.386]$. Side-S0 and
side-S1 run along the floor to $x\le2.681$. Interior-W ($x\le2.338$) and interior-NW
($y\le3.265$) form a second column, and interior-SE ($x\in[2.645,3.265]$,
$y\in[1.411,2.031]$) closes the east side.
Every pair interacts, so the class has no missing pairs.
The far walls never bind: no square of the pattern reaches $x$ or $y$ above $4.1$,
against $U=4.676$.

## 2. Where the Survivors Are

At the end of the 2,304-row run (live rows 1,381 of 2,138; angles in degrees, where
$65°$ to $90°$ is a turn of $-25°$ to $0°$;
[`domains-2304.json`](../../../packing/campaign/explorations/X048-session-168-pilots/receipts/flag2-diagnosis/domains-2304.json)):

| Owner | Rows | Live | Live angles | Centre box of the live residuals | Owned hull | Ideal owned |
| --- | ---: | ---: | --- | --- | ---: | ---: |
| corner-SW | 512 | 307 | $0$–$27.2$, $65.4$–$90$ | $[0.500,0.788]\times[0.500,0.912]$ | 0.436 | 0.438 |
| side-S0 | 283 | 57 | $0$–$3.6$, $8.5$–$16.9$ (thin), $85.6$–$90$ | $[1.498,1.815]\times[0.500,0.621]$ | 0.594 | 0.597 |
| side-W0 | 80 | 14 | $10.7$–$18.6$, $66.5$–$73.7$ | $[1.360,1.411]\times[1.515,1.670]$ | 0.717 | 0.729 |
| side-S1 | 285 | 285 | all | $[2.454,2.681]\times[0.500,1.310]$ | 0.119 | 0.122 |
| side-W1 | 166 | 52 | $8.5$–$18.6$, $68.4$–$74.3$ | $[0.568,1.185]\times[2.333,2.513]$ | 0.317 | 0.320 |
| side-W2 | 106 | 40 | $8.9$–$18.6$, $70.2$–$74.9$ | $[0.572,0.960]\times[3.371,3.386]$ | 0.550 | 0.556 |
| interior-NW | 96 | 76 | $0$–$51.7$, $76.0$–$90$ | $[1.598,2.004]\times[3.065,3.265]$ | 0.428 | 0.437 |
| interior-W | 124 | 64 | $0$–$51.7$, $88.6$–$90$ | $[2.113,2.338]\times[2.178,2.425]$ | 0.542 | 0.557 |
| interior-SE | 486 | 486 | all | $[2.949,3.265]\times[1.411,2.002]$ | 0.196 | 0.199 |

The owned hull is the kernel’s; the ideal owned region is the intersection of the
squares at every residual vertex and three angles per live row, in floats, which is what
any owned-hull cut at this state could use.
The two agree within three per cent, so the hull compression is not where the kernel
loses. The 1,152-row state
([`domains-1152.json`](../../../packing/campaign/explorations/X048-session-168-pilots/receipts/flag2-diagnosis/domains-1152.json))
has the same shape with wider boxes: interior-SE $[2.891,3.265]\times[1.411,2.004]$,
side-S1 $[2.427,2.681]\times[0.500,1.346]$, interior-NW all 64 rows live.

Three things stand out.

- **The west column survives only tilted, and in two directions.** Side-W0, side-W1 and
  side-W2 keep a tilt of about $+9°$ to $+19°$ and one of about $-15°$ to $-24°$; no
  upright pose survives.
  Side-W2 is pinned to its cell’s top edge, side-W0 to its east edge.
- **Everything east is pushed to its cells’ east edges.** Interior-W sits at $x\ge2.113$
  of $[1.43,2.338]$, side-S1 at $x\ge2.454$ of $[1.995,2.681]$, and interior-SE at
  $x\ge2.949$ of $[2.645,3.265]$.
- **The small owned regions are the wide owners.** Interior-SE and side-S1 own 0.20 and
  0.12 of a square because their survivors span every angle and boxes of
  $0.32\times0.59$ and $0.23\times0.81$. Confining either to one $15°$ sector raises its
  ideal owned region only to 0.26 to 0.32, so their position spread, not their angle
  spread, is what keeps them from cutting anything.
  The west column is the opposite: confining side-W0 or side-W2 to one tilt direction
  raises its owned region from 0.73 or 0.56 to between 0.86 and 0.93.

**The two runs ended differently.** The 1,152-row run stopped as stalled, its cap spent:
its rows were unchanged from round 19 to round 22 and no row was split.
The 2,304-row run stopped at its producer’s time share, 7,200 of 12,000 seconds, after
step 210 in round 23, and the knot was still contracting (live rows after each owner’s
step, from the run’s log; a split adds a live row, as in round 19):

| Round | corner-SW | side-S0 | side-W0 | side-W1 | side-W2 | interior-W |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 17 | 326 | 70 | 20 | 41 | 25 | 63 |
| 18 | 320 | 70 | 20 | 41 | 23 | 70 |
| 19 | 320 | 78 | 23 | 63 | 32 | 67 |
| 20 | 318 | 78 | 17 | 62 | 30 | 66 |
| 21 | 315 | 64 | 17 | 58 | 42 | 65 |
| 22 | 309 | 58 | 16 | 52 | 40 | 64 |
| 23 | 307 | 57 | 14 | — | — | — |

The run’s total live rows rose from about 1,300 to about 1,390 because a split live row
counts twice, mostly side-S1’s, interior-SE’s and interior-NW’s, not because the knot
grew.

## 3. The Placement Search

Every search uses the selector’s penalty, descent, margin ($10^{-6}$) and finish
unchanged, seeded from the survivors (an owner’s live row by residual area, an angle
uniform in the row, a centre uniform in a residual), since any placement lies in them.
The receipt is
[`place-2304.json`](../../../packing/campaign/explorations/X048-session-168-pilots/receipts/flag2-diagnosis/place-2304.json).

| Search | Attempts | Best worst violation |
| --- | ---: | ---: |
| Selector `search`, 64 survivor warm starts, default budget (12 starts, 24 hops, 256 deep starts, 256 deep hops, finish) | 613 | $9.80\times10^{-3}$ |
| 200 survivor-seeded descents, the best polished and finished | 201 | $1.03\times10^{-2}$ (median start $1.25\times10^{-2}$) |
| The selector’s earlier receipts (residue universe; arity-8 residue survey) | — | $9.29\times10^{-3}$; $9.72\times10^{-3}$ |
| Largest side placed, bisection from $0.9$ | — | side $0.99197$ placed, $0.99199$ not |

The two best poses are two families of the same arrangement.
In the selector’s, seven squares turn $16.4°$ to $17.0°$, corner-SW stands upright, and
interior-SE turns $-7.1°$. Its tightest constraints, as gaps in length units:

| Constraint | Gap |
| --- | ---: |
| side-S0 / side-W0 | $-0.0098$ |
| side-W1 / side-W2 | $-0.0088$ |
| side-W0 / side-W1 | $-0.0085$ |
| side-S0 into the floor | $-0.0064$ |
| side-W2 past its cell’s top edge ($y\le3.386$) | $-0.0058$ |
| corner-SW / side-W0 | $-0.0037$ |
| interior-W / interior-SE | $-0.0034$ |
| side-W0 / interior-W | $-0.0027$ |
| interior-SE past its cell’s east edge ($x\le3.265$) | $-0.0023$ |
| side-S0 / side-S1 | $-0.0021$ |
| side-W2 into the west wall | $-0.0020$ |
| side-S1 past its cell’s east edge ($x\le2.681$) | $-0.0017$ |

The multistart’s best tilts the west column and the floor squares $11.9°$ to $12.4°$,
interior-W and interior-NW $32.9°$ and interior-SE $53.7°$, and is led by the same five
constraints. The penetration is spread over the chain, not carried by one pair, as the
branch-and-bound pilot found for pattern A.

The profiles hold one stuck owner at a fixed angle and search the rest:

| Held at | $0°$ | $15°$ | $30°$ | $45°$ | $60°$ | $75°$ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| interior-SE | 0.0103 | 0.0125 | 0.0124 | 0.0115 | 0.0104 | 0.0116 |
| side-S1 | 0.0127 | 0.00975 | 0.0164 | 0.0134 | 0.0136 | 0.0136 |

No angle of either comes near placing the pattern.
Yet each is needed, and needed only just: without interior-SE the other eight squares
fit at side $1.0066$, and without side-S1 at $1.0115$, against $1.029$ to $1.076$
without any of the other seven (interior-W the least, side-W1 the most;
[`margins-2304.json`](../../../packing/campaign/explorations/X048-session-168-pilots/receipts/flag2-diagnosis/margins-2304.json),
bisection steps of $0.001$). They are the loose ends of the chain.

The best poses lie outside the survivors for eight owners, as they must: a pose that
penetrates by $0.01$ is not a placement, and the survivors hold only what a placement
could use, plus the kernel’s losses.

## 4. Why the Kernel Does Not Cut

The kernel removes a pose of one owner when its strict core meets another owner’s owned
hull, or when the pose lies in a collision region, where it overlaps every pose a
partner row can still take.
Both reason from one partner at a time.
The support test asks, for poses sampled from an owner’s survivors, whether each partner
has a surviving pose that clears it.
A pose every partner supports is beyond any such cut, however fine the rows.
A pose some partner cannot support could be cut by an exact one-partner rule, and the
margin by which it fails is the loss such a rule may have.
Partner poses are searched over every residual’s vertices, centroid and two interior
points at each row’s ends and middle, then locally inside the residual, so a supported
share is a lower bound and a margin an upper bound.
At the 2,304-row state, 200 poses per owner
([`support-2304.json`](../../../packing/campaign/explorations/X048-session-168-pilots/receipts/flag2-diagnosis/support-2304.json)):

| Owner | Supported | Partners that cannot support (poses, median margin) | Cut margin: least, tenth percentile, median |
| --- | ---: | --- | --- |
| side-W0 | 0 per cent | side-W1 (189, 0.0029), side-S0 (179, 0.0028), corner-SW (27, 0.0032), interior-W (24, 0.0044) | 0.0016, 0.0026, 0.0042 |
| side-W1 | 13.5 per cent | side-W0 (139, 0.0026), side-W2 (49, 0.0012), interior-NW (3, 0.0036) | 0.0002, 0.0006, 0.0022 |
| side-S0 | 53 per cent | side-W0 (93, 0.0030), side-S1 (5, 0.0006) | 0.0001, 0.0007, 0.0030 |
| side-W2 | 71.5 per cent | side-W1 (57, 0.0010) | 0.00002, 0.0003, 0.0010 |
| interior-W | 72.5 per cent | side-W0 (37, 0.0133), interior-NW (18, 0.0053) | 0.0001, 0.0031, 0.0082 |
| interior-NW | 89 per cent | interior-W (18, 0.0027), side-W2 (4, 0.0007) | 0.0002, 0.0003, 0.0024 |
| interior-SE | 90.5 per cent | interior-W (15, 0.0021), side-S1 (4, 0.0010) | 0.0006, 0.0007, 0.0018 |
| corner-SW | 95.5 per cent | side-W0 (8, 0.0036), side-S0 (1, 0.0001) | 0.0001, 0.0005, 0.0035 |
| side-S1 | 96.5 per cent | interior-SE (4, 0.0002), side-S0 (2, 0.0018), interior-W (1), side-W0 (1) | 0.00003, 0.0001, 0.0004 |

The cut margin of an unsupported pose is its largest margin over the partners: the loss
a one-partner cut may have and still remove it.
Every sampled side-W0 pose has one of at least $0.0016$, so a pairwise cut losing less
than that would remove all 200; one losing $0.0042$ would remove half.

The table separates two kinds of stall.

- **Interior-SE and side-S1 are supported, so for them the induction is stuck.** At this
  state each of their poses is compatible with some surviving pose of every partner.
  That is the gap of any pairwise propagation, arc consistency: the pattern is
  infeasible jointly, through a chain of contacts, and no single pair sees it.
  Their rows can die only after the west owners shrink, and refining their rows cannot
  change that. The split policy refined them anyway.
  It splits rows whose outer domain stopped shrinking, wall-loss rows first and then the
  widest, and theirs were the rows that never shrank, so they ended with 771 rows,
  side-S1’s split for its wall loss and interior-SE’s for their width.
- **Side-W0 is unsupported, by small margins.** Every sampled side-W0 pose overlaps
  every surviving pose of side-W1, of side-S0 or of another partner, typically by about
  $0.003$. An exact one-partner cut would remove every sampled side-W0 pose; if that
  holds for all of side-W0, removing it closes the pattern.
  The kernel’s cuts are not exact, and their losses are the size of the margins.
  Eight of side-W0’s 14 live rows are still the seed’s $1/64$ in $t$, about $1.8°$,
  where the envelope core is $0.0076$ inside the square on each face; interior-W and
  interior-NW each keep 16 live rows at $1/64$. Side-S0, side-W1 and side-W2 rest on
  walls, and their rows carry wall losses up to $0.0029$, $0.0034$ and $0.0032$. A
  collision region pays both squares’ core losses, and an owned hull pays for every pose
  of the partner at once.

The 1,152-row fixed point
([`support-1152.json`](../../../packing/campaign/explorations/X048-session-168-pilots/receipts/flag2-diagnosis/support-1152.json))
shows the same knot with larger losses.
Side-W0 is 27 per cent supported, side-W1 24.5, side-W2 46.5 and side-S0 64.5, with
median cut margins of $0.0031$ to $0.0050$. Against them stood the envelope core’s
$0.0076$ on the $1/64$ rows that side-W0, side-W2, interior-W and interior-NW still had
there, and wall losses of $0.0073$ to $0.0154$ on side-W1, side-S0, side-W2 and side-S1.
A fixed point that leaves this much of the knot pairwise unsupported is what losses
larger than the margins look like.
At 2,304 rows the wall losses had fallen to about $0.003$, below most of the margins,
and the knot moved: side-W0 went from 24 live rows to 14 and from 27 per cent supported
to none, as its partners’ survivors shrank around it.

So the stall is the west knot, held by first-order losses the size of its margins, with
the east owners waiting on it; the 2,304-row run was still eating into the knot when it
stopped.

## 5. What Would Close It

- **A longer run, with rows on the knot, not on the east.** Split side-W0’s rows first,
  then side-W1’s, side-S0’s and interior-W’s, until their losses fall below the cut
  margins above, and give the producer more than 7,200 seconds.
  The current policy cannot aim this way: it splits only rows whose outer domain has
  stopped shrinking, and while interior-SE’s and side-S1’s, which never shrank, took the
  budget, side-W0 kept eight live rows at $1/64$ to the end.
  A policy that skips owners whose poses are supported, or that splits first the rows of
  the owner with the smallest residual, would aim it.
  That is a producer change only; the checker already admits any complete refinement.
- **The octagon core.** At $1/64$ the octagon loses about $1.2\times10^{-4}$ a face
  against the envelope’s $0.0076$, which removes side-W0’s core loss outright.
  It does nothing for the wall losses of side-S0, side-W1 and side-W2. Near their $15°$
  tilts the wall loss is about $0.35$ of the row’s width in radians, so a loss of
  $0.001$ needs rows of about $1/700$ in $t$, finer than the run’s split floor of
  $1/512$; and lane K2 found on W7 that the octagon does not remove a coarse row’s
  domain loss.
- **Finer rows only on interior-SE: no.** Interior-SE is 90.5 per cent supported;
  splitting its rows cuts nothing until the knot shrinks.
  The 2,304-row run is that experiment: 486 rows, none dead.
- **A branch on the west column’s tilt.** Side-W0, side-W1 and side-W2 survive in two
  tilt directions, and confining side-W0 or side-W2 to one raises its ideal owned region
  from 0.73 or 0.56 to about 0.9. The n17 node admits no parent and no constraints
  (`node.admit_header`), so this is a grammar change, and second to the two above.
- **The branch and bound is out of reach.** Its Knuth estimates at arity 8 stay above
  $10^{6}$ nodes in every relaxation tried
  ([pruning review](review-2026-10-02-n17-cost-reduction-pruning.md)), and on W7, at
  arity 7 with a best violation of $9.0\times10^{-3}$, it closed 0.4 per cent of its
  tree in 30 minutes. Flag 2 is arity 9 with a best violation of $9.3\times10^{-3}$. That
  does not prove the method cannot close it, but it rules it out as the route.

A falsifier for the first two: a run with the octagon core and the split budget aimed at
side-W0, side-W1, side-S0 and interior-W, at the same 2,304-row cap and run to a fixed
point, that ends with side-W0 still live and its cut margins unchanged would mean the
losses named here are not what holds it.

## Evidence Status

| Kind | Items |
| --- | --- |
| Read exactly from the saved nodes, converted to floats | Every row count, live row, row width, angle block, centre box and owned hull area in section 2; the 1,152-row node is certified, the 2,304-row node is the producer’s output, its check `INCOMPLETE` |
| Read from the producer’s logs | The per-round live rows and how each run stopped |
| Float estimates | Ideal owned regions; row losses; every search result, profile and largest side; the support shares and margins |
| Search results, not bounds | No placement found, so a true pattern is likely, not proved; the largest side is a lower estimate; the supported shares are lower bounds and the margins upper bounds |
| Exact | Nothing new: no placement was found to check, and the kernel’s stall certificates are lane K2’s |
| Not done | The aimed, longer octagon run of section 5; an exact or interval form of the support test |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
