---
title: n17 Capture Route After Pilot 2
date: 2026-10-05
status: planning-review
---
# n17 Capture Route After Pilot 2

**Session:** 182, lane R (Session 168’s lane R9, `think-g2qn`). **Question:** capture
pilot 2 met the after-pilot review’s falsifier at round 17: for rounds 15 to 17 every
contracting owner’s widest live row was under a twentieth of its position extent and no
two-sided position extent fell by ten per cent.
Was that another producer limit, and which one, or is n11’s ownership-induction
architecture the wrong engine for n17 capture?
**Read:** the pilot-2 receipts under
[`receipts/capture-pilot2-box1024-need/`](../../../packing/campaign/explorations/X048-session-168-pilots/receipts/capture-pilot2-box1024-need/)
and
[`capture-pilot2-box1024-256/`](../../../packing/campaign/explorations/X048-session-168-pilots/receipts/capture-pilot2-box1024-256/),
the 128-row receipt
[`capture-pilot2-box1024-128.json`](../../../packing/campaign/explorations/X048-session-168-pilots/receipts/capture-pilot2-box1024-128.json),
the [capture feasibility](review-2026-10-02-n17-capture-feasibility.md),
[after-pilot](review-2026-10-02-n17-capture-after-pilot.md),
[widened-projection scope](review-2026-10-02-n17-widened-projection-scope.md) and
[local-radius](review-2026-10-03-n17-local-radius.md) reviews, the
[kernel adaptation spec](review-2026-10-02-n17-kernel-adaptation-spec.md), the endpoint
receipts under `X048-route-review/receipts/`, and the producer and pilot source at the
stack top `451154f60`
([`pilot_n17_capture.py`](../../../packing/devtools/pilot_n17_capture.py),
[`hull_kernel/producer.py`](../../../packing/src/sqpack/hull_kernel/producer.py)).
**Recomputation:** one run of the sanctioned scorer, `devtools.score_n17_capture`, at
`451154f60` in a detached worktree (removed afterwards), over the four pilot-2 logs,
`partial.json` and the capture-form local-radius target
`ratio-composition-capture.json`; its round table reproduces the committed `score.txt`
column for column (the `side/r` column differs only because the committed score used the
cube-form target). Outputs `score-pilot2-need-r9.json` (sha256 `dadde829…`) and `.txt`
(`1a720a1b…`) are in the session scratchpad under `s182/R/` for the coordinator to file.
Every other number below is read from a receipt or re-derived by hand from one.
No new computation was launched; nothing was committed, pushed or posted.

## Verdict

**Undecidable from the receipts, with most of the question decided.** The receipts
settle four things and leave one.

- **None of the four named producer candidates is the limit.** The hull cap of 48 binds
  on all seven tilted owners but its recorded area loss is $1$ to $9\times10^{-6}$ per
  step; the octagon core’s loss is second order ($w^2/2\approx2\times10^{-10}$); the
  measurement is two-sided in pilot 2 and the per-side ratios show the one-sided movers
  converged too; the partner-cover reach test withheld no contact partner.
- **A producer loss no review named is present and quantified.** `producer.compress` and
  `kernel_points` pull every owned-hull vertex $2^{-12}$ of its distance to the hull’s
  vertex mean before the exact check, about $1.22\times10^{-4}$ at unit scale.
  Three independent one-link wall-side bounds converged to $-1.262\times10^{-4}$,
  $-1.262\times10^{-4}$ and $-1.487\times10^{-4}$, identical at 128 and 256 rows.
  That is 13 per cent of the pilot’s box per hull link, 61 per cent of H-261’s radius
  $1/5000$ and 36 per cent of the composed capture-form position floor $1/3072$, so the
  kernel as built cannot deliver those radii through any hull link whatever the rows.
  It does not explain the stall: three links lose $3.7\times10^{-4}$ of a
  $9.8\times10^{-4}$ box.
- **The fixpoint is set by the box, not by the rows, down to the finest rows run.**
  Between the 128-row run (ratios $1/5$ to $1/36$) and the by-need run (ratios $1/20$ to
  $1/72$) every two-sided extent and every turn range changed by at most 6 per cent, and
  10 of 16 owners’ extents are the untouched box to 16 digits in both; the six that
  moved did so on one side only.
  The after-pilot probe’s constants (positions at 12 and angles at 28 to 36 row widths)
  are excluded on every tilted owner by a factor of 4 to 8, and so is that review’s “two
  to four” producer correction.
  No far-side bound arrived anywhere in 17 rounds; everything that moved is a wall-side
  bound fed from the south-west corner over one or two links.
- **The stuck quantities are the tilted squares’ turn ranges.** Square 9’s into-the-wall
  side sits at $0.97\,\rho/h'(\theta^\ast)=1.48\times10^{-2}$, the exact wall coupling;
  10 inherits it through their parallel faces; 16’s free side is 27 box radii.
  With those ranges, every corner-to-edge link loses between $1.3\times10^{-4}$
  (universal collision, axis corner) and $1.0\times10^{-2}$ (owned hull, 16’s corner),
  and every partner’s box support along an oblique normal is $1.41\rho$, so each
  far-side cut lands at or outside the owner’s own box edge.
  This loop is homogeneous in $\rho$.
- **What the receipts cannot decide:** whether the loop opens when rows are finer.
  A row-driven fixpoint survives only with an angle constant of at least 290 row widths
  on squares 9, 10 and 16 (the dual-norm reading of X-048’s draft C3, re-derived for the
  octagon core, gives 160 to 250, so it is marginal, not open), and the probe that
  predicted contraction is not on any ref.
  Section 6 specifies the one measurement that separates the readings, staged so the
  first stage costs about 20 CPU-hours and reads the angle ranges rather than the
  position onset; section 7 gives the candidate and the instrument contract the
  architecture branch would codify.

## 1. What the Receipts Show

### 1.1 The Run and Its Fixpoint

The by-need run resumed pilot 2’s 256-row run at round 13 from a checkpoint in another
container’s scratchpad (`scratch:ckpt-256/checkpoint-round-013.json.gz`) with the caps
raised on three owners: `max_live` 256, `max_live_for` side-N0 320, side-N2 576, side-W2
416; 32 bins, box $1/1024$, octagon core, hull limit 48, minimum row width $2^{-22}$ in
$t$, capture cap $U'=935106018721/200000000000$. Rounds 14 to 17 took 17,350 s wall and
15,329 s process CPU; the four log segments ran 8,722, 4,253, 6,998 and 17,341 s, 37,300
s in all including the partial rounds each resume repeated, so a rebuild to round 17 in
one process is about 35,000 s of completed rounds.

The falsifier was met at round 17: rounds 15 to 17 fine (largest ratio 0.0499 on
side-N2) and flat (least two-sided fall 0.988); every ratio first under $1/10$ at round
14 and under $1/20$ at round 15. The scorer’s round table reproduces the committed one.

What the table does not say is that the rows had stopped refining.
Every owner reached its cap between rounds 11 and 15 (`live_rows` 256 on eleven owners,
255 on two, 320, 571 and 415 on the three raised), and the splits per round fell 501,
108, 14, 13 over rounds 14 to 17. `refine` bisects only while an owner has fewer live
rows than its cap, so from round 15 the row partition was frozen except where a row
died. At that frozen partition the state is a fixpoint to the receipt’s precision: at
round 17 `g_sides` is exactly 1.000 on both sides of every coordinate of 13 owners; the
three exceptions are side-N1’s $x$ low side (0.998 a round) and side-W2’s $x$ and $y$
low sides (0.994 and 0.997).

### 1.2 What Moved and What Did Not

Every two-sided extent that fell did so on one side, the side facing the south-west
corner’s walls (coordinates as the pilot names them, offsets from the family in unit
side lengths; the feeding link is inferred from the endpoint’s 21 contact pairs in
`route-endpoint.txt`):

| Side | Owner | Round 17 | Fall of the two-sided extent | Fed from |
| --- | --- | ---: | ---: | --- |
| $\xi_2$ low | side-S0 (2) | $-1.2623\times10^{-4}$ | 0.565 | corner-SW (1), the 1/2 face |
| $\eta_3$ low | side-W0 (3) | $-1.2623\times10^{-4}$ | 0.565 | corner-SW, the 1/3 face |
| $\eta_7$ low | side-E0 (7) | $-1.4866\times10^{-4}$ | 0.576 | corner-SE (5), the 5/7 face |
| $\xi_9$ low | side-W2 (9) | $-3.267\times10^{-4}$ | 0.667 | the west wall, at 9’s own turn range |
| $\eta_9$ low | side-W2 | $-6.149\times10^{-4}$ | 0.815 | side-W0, 9’s corner on 3’s face |
| $\xi_{12}$ low | interior-N (12) | $-8.496\times10^{-4}$ | 0.935 | 11, parallel faces along $u$ |
| $\xi_{15}$ low | side-N1 (15) | $-8.183\times10^{-4}$ | 0.919 | 10, 15’s corner on 10’s face |

Every other side of every coordinate is at the box, $\pm9.7656\times10^{-4}$, or at a
wall ($2.2\times10^{-13}$, the centred cap’s half-slack); no high side moved anywhere.
Squares 1, 4, 5, 8, 10, 14, 16, 17 and the non-slide coordinates $u_{11}$ and $u_{13}$
are the untouched box on both sides, and their floats are identical to 16 digits with
the 128-row run’s, which is what “never cut” looks like in a receipt.

The turn ranges at round 17 (radians about the endpoint turn, in multiples of
$\rho=1/1024$):

| Owner | Turn range | In $\rho$ | What sets it |
| --- | --- | --- | --- |
| the nine axis squares | $[-1.97, +1.98]\times10^{-3}$ (corner-SW $-1.70$) | $\pm2.0$ | the wall coupling $h(\theta)-\tfrac12\approx\theta/2\le\rho$ |
| interior-E (14) | $[-0.69, +4.88]\times10^{-3}$ | $-0.7,\ +5.0$ | partner levers |
| interior-N (12) | $[-0.86, +6.44]\times10^{-3}$ | $-0.9,\ +6.6$ | partner levers |
| interior-W (11) | $[-5.26, +3.97]\times10^{-3}$ | $-5.4,\ +4.1$ | partner levers |
| side-S1 (13) | $[-3.29, +6.50]\times10^{-3}$ | $-3.4,\ +6.7$ | partner levers |
| side-N0 (10) | $[-1.64, +14.18]\times10^{-3}$ | $-1.7,\ +14.5$ | 9, through the parallel 9/10 faces |
| side-W2 (9) | $[-4.97, +14.78]\times10^{-3}$ | $-5.1,\ +15.1$ | the west wall: $\rho/h'(\theta^\ast)=15.2\rho$ |
| side-N2 (16) | $[-26.83, +1.46]\times10^{-3}$ | $-27.5,\ +1.5$ | partner levers, the weakest |

Square 9’s into-the-wall side is the wall coupling to 3 per cent: a square tilted by
$\theta^\ast=0.6947$ rad (39.80°) has wall support $h(\theta)=(\cos\theta+\sin\theta)/2$
with $h'(\theta^\ast)=0.0641$, so a box slack of $\rho$ away from the wall allows a turn
of $\rho/0.0641=1.52\times10^{-2}$; measured $1.478\times10^{-2}$. Its $x$ low side is
the same coupling read the other way: $h'\cdot(-4.97\times10^{-3})
=-3.18\times10^{-4}$ against the measured $-3.27\times10^{-4}$. In pilot 1 the same
square stopped at $1.77\times10^{-2}$ from the $1/1024$ box and at 0.23 to 0.26 from the
$1/64$ box, where $16\rho=0.25$: the coupling held at both box scales and at 24, 128,
256 and 415 rows.

### 1.3 The Same Fixpoint at Half the Rows

The 128-row run (`MEASURED_STALLED_AT_ROW_CAP`, 13 rounds) reached the same box with
rows twice as wide, and four and a half times as wide on side-N2. Per owner, the turn
range and the ratio of widest row to extent in the two runs, and the range as a multiple
of the widest row’s turn width (the “row-width constant” a row-driven reading needs):

| Owner | Ratio, 128 | Ratio, need | Range, 128 | Range, need | Need over 128 | Range in row widths, 128 | need |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| side-N2 | 0.200 | 0.050 | $2.98\times10^{-2}$ | $2.83\times10^{-2}$ | 0.949 | 76 | 290 |
| side-W2 | 0.131 | 0.034 | $2.11\times10^{-2}$ | $1.97\times10^{-2}$ | 0.935 | 83 | 298 |
| side-N0 | 0.110 | 0.028 | $1.66\times10^{-2}$ | $1.58\times10^{-2}$ | 0.955 | 77 | 294 |
| interior-E | 0.028 | 0.014 | $5.64\times10^{-3}$ | $5.57\times10^{-3}$ | 0.988 | 105 | 207 |
| interior-N | 0.055 | 0.028 | $7.66\times10^{-3}$ | $7.30\times10^{-3}$ | 0.954 | 71 | 136 |
| interior-W | 0.055 | 0.028 | $9.45\times10^{-3}$ | $9.23\times10^{-3}$ | 0.977 | 87 | 171 |
| side-S1 | 0.055 | 0.028 | $1.05\times10^{-2}$ | $9.79\times10^{-3}$ | 0.931 | 97 | 182 |
| axis squares | 0.031 to 0.063 | 0.014 to 0.031 | $4.00\times10^{-3}$ | $3.95\times10^{-3}$ | 0.989 | 66 | 130 |

The two-sided position extents are identical between the runs on 13 owners and differ by
2 to 4 per cent on side-W2, side-N1 and interior-N; side-S0’s $x$ extent is
$1.1028\times10^{-3}$ in both, so the one-link residual of section 3 is independent of
the row width.

Two readings fit a table like this.
A row-driven fixpoint, extent $=C\,w$, fits only if $C\,w$ exceeded the box-set values
in both runs, which needs $C\ge290$ to $298$ on the three binding owners and $\ge207$ on
interior-E; it then predicts that the ranges fall once $C\,w$ drops below them, that is,
at rows 1.5 to 3 times finer than the by-need run’s on those owners.
A box-set fixpoint predicts that they do not fall at any row width while the position
box stands.
The after-pilot probe’s figures, positions at about 12 and angles at 28 to 36
row widths, are excluded on every owner: at those constants the by-need run’s extents
would be 4 to 8 times smaller than the box.

## 2. The Named Producer Candidates

| Candidate | What the receipts say | Verdict |
| --- | --- | --- |
| Hull cap 48 | `owned_hull_vertices` is 48 on interior-N, interior-W, side-N0, side-N2, side-S1 and side-W2 and 47 on interior-E by round 13 and from then on (17 to 23 on the axis owners); `hull_area_lost` per step is $1.1$ to $9.4\times10^{-6}$ on those owners and 0 elsewhere. Spread along a unit perimeter that is a recession of $10^{-6}$; concentrated on one per cent of it, $10^{-4}$, the pull’s size. `bounded_vertices` drops the vertex of least triangle area, so the loss is bounded by what it records. | Binding, harmless at the $10^{-3}$ scale of the stall; at most a tenth of the box even in the worst placement |
| Octagon core | `octagon_core` intersects the row’s two end squares and scales by $1-w^2/2-10^{-12}$; `strict_core` passes it. Along a face normal the loss is $w^2/2\approx2\times10^{-10}$ at $w=2\times10^{-5}$; at a corner it is $w/(2\sqrt2)\approx7\times10^{-6}$. | Not a limit; the envelope core’s first-order loss ($2.4\times10^{-4}$ in pilot 1) is gone, as the review asked |
| One-sided measurement | Pilot 2 records `range`, `extent`, `g_extent` and `g_sides` per coordinate; the falsifier was read on two-sided extents; the one-sided movers of section 1.2 are visible and have converged. | A measurement defect of pilot 1, repaired; not a limit on the dynamics |
| Partner pruning | A step offers a partner’s cover only when its residual box comes within $3B/2$ of the owner’s domain in both coordinates (`produce_step`, `separated`), which excludes nothing that can overlap; `partners_offered` is 7 for the interior owners, 4 to 5 for the side owners, 2 for corner-SW and corner-NW and 1 for corner-NE, matching their contact neighbours within reach (17 and 8 are not in contact: the east column’s four axis squares leave 0.68 of gaps). Corner-NW and corner-NE record 0 collision regions because none exists in their domains, not because covers were withheld. | Sound and inactive; not a limit |

Universal collision itself is active, not dormant: 8,257 regions were certified in round
17 against 1,161 in round 1, 10,515 partner rows were admitted of 17,629 offered, and
interior-E’s round-17 step ran 14.8 million collision checks (producer 145 s, checker
159 s). What it did not do is move a single far-side bound.

## 3. A Loss No Review Named: The Compression Pull

**The code path.** After a complete step, `producer.kernel_points` locates the owner’s
common-owned kernel in floating point as the intersection of every row’s common-core
planes, then proposes grid points: the region’s vertex mean, and each vertex pulled
toward that mean by $2^{-12}$, $2^{-6}$, $1/4$ and $1/2$ of its distance, rounded to the
$2^{-20}$ grid and kept only if it satisfies every plane exactly (`producer.py` lines
681 to 715 at `451154f60`). `produce_step` then takes the hull of the old owned hull and
these points and passes it through `producer.compress`, which keeps grid points as they
are (lines 191 to 228), and through `bounded_vertices` when it exceeds the cap.
So an owned hull’s face sits inside the common-core plane by $2^{-12}$ times the face’s
distance from the vertex mean: for a hull filling the unit square,
$2^{-12}\times0.4995=1.22\times10^{-4}$. The forbidden region a partner derives from the
hull, `forbidden_regions` in `induction.py`, is the Minkowski set $K_j-Q_i$, so every
hull-mediated bound inherits the same $1.22\times10^{-4}$. Universal-collision regions
do not pass through the hull; their own pull in `collision_region` is $2^{-12}$ of a
region the size of the box, below $10^{-6}$.

**The match.** The three wall-side bounds that are one face-to-face link from a
wall-pinned corner square converged to $-1.2623\times10^{-4}$ (side-S0’s $x$ and
side-W0’s $y$, from corner-SW; equal to five digits, as the symmetric geometry requires)
and $-1.4866\times10^{-4}$ (side-E0’s $y$, from corner-SE, whose hull is 0.75 wide
because square 5 slides and whose 17 vertices put the vertex mean off centre).
The prediction with no free parameter is $1.22\times10^{-4}$ plus a row-width term under
$8\times10^{-6}$: within 3.5 per cent for the first two and within the vertex-mean
offset for the third.
The alternatives do not fit: the octagon core and the hull’s own face are second order,
the row’s wall loss is $w/2\approx8\times10^{-6}$, and a universal-collision cut from an
axis partner pinned at a wall is exact to second order and would have given about $0$
had it been located.
The residual is the same at 128 rows (side-S0’s $x$ extent $1.1028\times10^{-3}$ in both
runs), so it is not a row-width loss; and in pilot 1, with the envelope core at
$w=4.9\times10^{-4}$, the same bound had reached $-2.77\times10^{-4}$ and was still
moving, which the review read as two envelope cores ($2.4\times10^{-4}$) and which is
also one core plus this pull.
Confirming the identification exactly takes five minutes with a node in hand: compare a
hull face to its common-core planes.
No pilot-2 node is on any ref here.

**What it costs.** At the pilot’s box the pull is 13 per cent per hull link, so a
three-link closure (for instance the east wall to square 2 through 17, 14 and 13) loses
$3.7\times10^{-4}$ before any geometry.
That is not the stall: $0.63$ of the box would still have shown as contraction.
At the local theorem’s radii it is decisive: H-261’s $r=1/5000=2\times10^{-4}$ is 1.6
pull lengths, the composed capture-form position floor $1/3072=3.26\times10^{-4}$ is
2.7, and the cube-form floor $1/1216$ is 6.7. Any kernel capture to those radii through
hull links is impossible with this constant, independently of everything else in this
review. The repair is one constant (the first pull $2^{-12}\to2^{-18}$, two grid steps,
with the exact check kept; the checker verifies the convex-combination witnesses, so
soundness is untouched), and it carries a falsifiable prediction: the one-link residual
falls from $1.26\times10^{-4}$ to under $10^{-5}$, and two-sided contraction does not
start.

## 4. Why Nothing Two-Sided Arrives

The endpoint has 21 contact pairs (`route-endpoint.txt`) and the stress’s 52 positive
rows (`endpoint-n17_stress.txt`) are its contacts and wall touches: three axis
face-to-face pairs (1/2, 1/3, 5/7; the 2/3 pair touches at a point and carries no row),
six parallel-face pairs among the six squares tilted by $\theta^\ast$ (9/10, 11/12,
10/12, 13/14, 12/14, and 9/11 at zero weight), and twelve corner-to-edge rows, the
after-pilot review’s “smooth” rows: 9’s corner on the west wall, 9’s on 3, 4’s on 10,
3’s on 11, 2’s on 13, 15’s on 10, 17’s on 14, 7’s on 14, 15’s on 16, 8’s on 16, 17’s on
16, and 16’s on 12. Only square 9 among the tilted squares touches a wall, and only axis
squares touch the north and east walls.
So every chain that could close a two-sided bound passes a corner-to-edge link whose
feature is an axis square’s corner on a tilted face, or 9’s or 16’s corner.

Three exact facts about one such link, for a feature square whose turn range is
$2\alpha$ and whose centre is uncertain by $\rho$ in each coordinate:

1. **The owned-hull rule loses the corner recession.** The intersection of the unit
   square rotated by $\pm\alpha$ about its centre has its corner vertex at distance
   $1/(\sqrt2(\cos\alpha+\sin\alpha))\approx(1-\alpha)/\sqrt2$ from the centre, so a
   corner feature recedes by $\alpha/\sqrt2$: $1.4\times10^{-3}$ for an axis square
   ($2\alpha=3.95\times10^{-3}$), $5.6$ to $7.0\times10^{-3}$ for 9 and 10, and
   $1.0\times10^{-2}$ for 16. Every one exceeds the box, so no hull-mediated corner cut
   can reach any owner’s domain.
   Face features lose only second order, which is why the three face links of section
   1.2 moved and the corner links did not.
2. **Universal collision loses the support derivative.** The least intrusive pose of the
   feature square over its turn range reduces its support along a contact normal at
   angle $\varphi$ from its axes by $\tfrac12|\sin\varphi-\cos\varphi|\,\alpha$:
   $0.0641\alpha$ for the $39.8°$ normals and $0.103\alpha$ for 16’s, that is
   $1.3\times10^{-4}$ (axis corner on a tilted face), $5.1$ to $6.3\times10^{-4}$ (9 and
   10\) and $1.5\times10^{-3}$ (16). Only 16’s exceeds the box on its own.
3. **An oblique normal sees both coordinates of the partner’s box.** Along $u$ at
   $39.8°$ a box of radius $\rho$ has support $(0.768+0.640)\rho=1.41\rho$, which is
   also the owner’s own support along $u$. A corner cut from a partner still at its box
   therefore lands at the owner’s box corner and removes nothing until the partner’s box
   has shrunk, and the partner’s box waits on the owner’s.

Facts 2 and 3 are homogeneous in $\rho$: if every square is uncertain by $\rho$, every
far-side cut misses by at least $\rho$, at every box scale.
The turn ranges close the loop.
A row at turn offset $\delta$ sees each corner-contact bound shifted by $\tau\delta$,
$\tau$ the contact’s tangential lever (0.2 to 0.5 for the interior contacts, $h'=0.064$
for 9 at the wall, smaller for 16’s), so with partners at the box the rows survive out
to $|\delta|\approx\rho/\tau$: 2 to 7 $\rho$ for 11 to 14, 15 $\rho$ for 9 (and 10
through the parallel faces), 27 $\rho$ for 16; the measured union over live rows is
exactly that.
Wide turn ranges then enlarge the losses of facts 1 and 2, and the position
box is what sets the ranges.
The ordering of the stuck ranges (16 loosest, then 9 and 10, then 11 to 14) follows the
lever arms, the same first-order coefficients that make $-\omega_{16}$ the softest
direction of the scope review’s LP; it supports the coordinator’s F5 reading
qualitatively, but it is box-scale pairwise geometry, not an LP measurement, and pilot
2’s ranges should not be quoted as evidence for either LP slope.

Where this account and the after-pilot probe part: the probe enforces each first-order
row between an owner’s slab and the partner’s whole pose set and contracts at the
bisection rate once rows are about a tenth of the extent, with no fixpoint above zero.
The kernel’s two rules are weaker than that ideal rule in two measured ways, the hull
rule by fact 1 and the compression pull, and the probe itself
(`lanes/r5/pairwise_probe.py` in a Session 168 scratchpad) is on no ref, so neither its
claim that pairwise induction can do no better nor its constants can be re-run here.
The receipts show the kernel 4 to 8 times worse than the probe at every row width run,
and they do not show whether finer rows would open the loop.

## 5. The Two Readings That Survive, and Where This Review Disagrees

**Reading A, row-driven (X-048 draft v2’s C3).** The angle extents settle at a constant
times the row width, the constant being the dual-norm bound
$|\omega_{11}|\le\lVert\lambda\rVert_1\,\ell$ with $\lVert\lambda\rVert_1$ between 921
and 1,439 and $\ell$ the per-row loss.
The draft’s “about 230” is $921/4$, that is $\ell=w/4$, the envelope core’s loss.
With the octagon core the face rows lose second order and the twelve corner rows lose
$0.35w$; the local-radius review puts the largest $-\omega_{11}$ dual weights on 10/15,
16/17, 15/16, 14/17 and 2/13, all corner rows, at 8 to 9 per cent each, so about half
the mass is on corner rows and the constant is about $0.175\lVert\lambda\rVert_1$, 160
to 250. Pilot 2’s ranges are 290 to 298 row widths on 9, 10 and 16 and did not move when
the rows were refined 2 to 4.5 times.
Reading A therefore survives only in the upper part of its own range, above 290, and its
draft falsifier window (onset between a twentieth and a fortieth) is replaced by: the
turn ranges of 9, 10 and 16 fall by at least a fifth when their rows are halved again,
and position contraction begins when every owner’s rows are under about $1/100$ of its
extent (positions at a third of the angle constant, the probe’s 12-to-36 proportion).

**Reading B, box-set (the architecture reading).** Facts 1 to 3 hold at every scale; the
turn ranges are lever-limited by the position box; no row refinement moves either while
partners are at their boxes; pairwise induction from a box seed has a fixpoint at the
box on this contact graph, as the feasibility review’s own stop condition ($g>0.95$ at
the $10^{-3}$ scale) anticipated and as four runs at two box scales and four row counts
have now shown. Its falsifier: the turn ranges of 9, 10 and 16 fall by a fifth or more
when their rows are halved again, or any far-side bound moves at the finer rows.

**Disagreements with the record, each with its derivation above:**

- With the after-pilot review’s section 2: “extents settle at about 12 times the widest
  live row in position and 28 to 36 in angle” is not what this kernel does.
  At row widths of $1.5$ to $9.7\times10^{-5}$ rad the angle extents are 130 to 298 row
  widths and did not follow the rows (section 1.3). Its list of producer losses omitted
  the compression pull, the only first-order loss the receipts actually show (section
  3), and its reading of pilot 1’s square-2 residual as “two envelope cores” is equally
  one core plus the pull.
- With the plan’s framing of lane R: the four named candidates are all excluded by
  receipt numbers (section 2), so a “producer-limited” exit with pilot-3 settings alone
  is not available; the one producer defect found is a code constant whose repair is
  predicted not to start contraction.
- With X-048 draft v2’s C3: its constant, recomputed for the core pilot 2 used, is 160
  to 250 and sits below the receipts’ lower bound; the window $1/20$ to $1/40$ is
  replaced as above. The coordinator’s F4 note stands in its conclusion (a producer limit
  and a larger constant predict the same receipt) but the “producer limit” half now has
  a name and a size, and the “larger constant” half has a lower bound of 290.
- With the coordinator’s F5 observation: the arithmetic is right ($0.0155$ against
  $1/74.2=0.0135$; $0.088$ against $1/175.8$ is 15.5 times) and the lever-arm ordering
  of section 4 is consistent with it; it bears on C4’s mechanism, not on R9.

## 6. The Discriminating Measurement

One instrument, three stages, pre-registered readings; it is pilot 3 only in the sense
that it starts from round 0 with `--checkpoints` (no checkpoint resumes here, Opus
review F3) and the pull repaired.
Nothing here runs tonight (plan, “Not Tonight”).

**Stage 0, the positive control pilot 2 omitted (2 to 4 CPU-hours).** The after-pilot
review’s item 5: the same producer on n11’s case-438 state from its sixteen cells, in
the pilot’s `--system n11` frame, at `--max-live 64 --max-rounds 15`, octagon core, hull
limit 48, with the pull repaired.
Reading: the worst two-sided position extent is below half its round-0 value by round 15
(the record’s $g\approx0.84$ a round gives 0.07, the probe’s 0.50 gives
$3\times10^{-5}$); if it stays above 0.9, the producer stalls where n11’s did not, the
producer is defective, and no n17 reading is drawn until it is fixed.
Cost from pilot 2’s early rounds (66 s a step at about 54 live rows per owner with 40
contact pairs; n11 has 11 owners and 14 pairs): about 6 minutes a round at 64 rows, 15
rounds under 2 hours; a 128-row repeat about 4 hours.

**Stage 1, the angle ranges (about 20 CPU-hours, one process).** Rebuild to round 17
with pilot 2’s exact settings and the repaired pull (about 35,000 s; the one-link
residuals must land under $10^{-5}$, which confirms section 3 or refutes it), then
resume with `--max-live-for side-W2=832 --max-live-for side-N0=640
--max-live-for side-N2=1152` (twice the by-need caps on the three binding owners;
`load_checkpoint` admits cap changes) for one bisection round and two holding rounds,
then `1664`, `1280`, `2304` for the same.
Live rows about 6,000 then 8,600; from the scorer’s fit (wall
$=c\cdot\mathrm{live}^{1.27}$, reference round 17 at 4,664 live rows and 4,050 s) about
6,000 and 8,800 s a round, six rounds about 12 hours, 22 with the rebuild.
Reading, on side-W2’s into-the-wall turn side ($1.478\times10^{-2}$, $0.97\rho/h'$) and
the full ranges of side-N0 and side-N2: a fall of a fifth at twice the rows and two
fifths at four times is reading A and sends the run to stage 2; ranges within 5 per cent
of pilot 2’s at four times the rows is reading B, the kernel route is
architecture-limited on this state, and the run stops.

**Stage 2, the position onset (about 20 to 25 CPU-hours more, only after reading A at
stage 1).** Raise every owner so its widest row is under $1/100$ of its extent: from
pilot 2’s state that is 512 rows on side-S0, interior-E, corner-SW, side-E1 and side-N1,
1,024 on the three remaining corners, side-W0, side-E0, interior-W, interior-N and
side-S1, 1,280 on side-N0, 1,664 on side-W2 and 4,608 on side-N2, about 18,300 live rows
and 23,000 s a round; three bisection rounds at growing cost (about 12 hours) and three
fine rounds (about 19 hours).
Falsifier: the after-pilot review’s, read at $1/100$ in place of $1/20$. Met: both
constants are excluded and reading B stands.
Not met, with a two-sided fall of ten per cent at some ratio between $1/20$ and $1/100$:
the row cap under a measured constant was the limit; the kernel route continues and its
cost model is re-priced with that constant.
A continuation to $1/240$ (the far end of reading A’s range) is about 70,000 live rows
and 35 hours a round, priced separately and not proposed.

**Resources.** One process throughout (the pilot is sequential); memory unmeasured above
4,664 live rows, so the plan’s watchdog and a budget of 3 GB apply; checkpoints at
18,300 rows will be hundreds of megabytes each, so keep the last two.
Every stage writes the receipts the scorer reads, and the scorer is the instrument that
reads them. Two additions the receipt should carry for stage 1, both small: per row,
which rule set each residual bound (wall, hull region or collision region, with the
partner), so that a residual at the hull prediction with a collision region located can
be read; and the owned hull’s face offsets from its common-core planes, which decides
section 3 directly.

**What each outcome selects.** Reading B at stage 1: the kernel leaves the capture
route, the widened projection theorem’s instrument is the next build (section 7), and
the cells-to-feature-forcing stage needs an engine that is not pairwise from a box seed
(the after-pilot review’s route (b) in its Taylor form is the candidate on the record).
Reading A with contraction at stage 2: capture is a row-budget problem at the measured
constant; the pull repair is permanent; the composed target of the local-radius review
(angles $8.2\times10^{-4}$, $\omega_{11}$ $4\times10^{-3}$) is priced from the measured
rows.

## 7. If It Goes the Architecture Way: Candidate and Instrument Contract

Written now so that a W7 slice can be scoped without another review round; it is a
candidate for codification only after stage 1 reads B.

**Candidate: the widened projection theorem as the terminal theorem.** *Claim:* every
packing of side at most $U'$ in the family’s occupancy state whose 17 angles lie within
$\rho_a=5\times10^{-3}$ of the family’s, whose centres lie within $10^{-2}$, and whose
sliders lie in the H256 domain widened by $10^{-2}$, has $S\ge S^\ast$ with equality
only on the family.
*Mechanism* (scope review, sections 1 to 3): with the 135 unavailable
options forced negative (least margin $0.0558$ at the centroid), feasibility at fixed
angles is a linear program in the 32 centre coordinates and $S$, whose value is a
minimum of dual sheets $S_B(\psi)=\lambda_B(\psi)\cdot b_B(\psi)$; the sheets are
conical to $3\times10^{-2}$ with curvature about $0.3$ per squared radian against
H-261’s $33$, and the softest coordinate slope is $0.0155$ along $-\omega_{16}$.
*Falsifier:* a sheet with a negative slope anywhere in the box (the co-moving 11/12
direction first, where H-261’s bound is $1/175.8$); a centroid margin failing along the
slider family; or a patch count above the threshold below.
*Expected information:* the capture target moves from the local radius to the
feature-forcing region, and capture becomes “angles to $5\times10^{-3}$ from the cells”,
which no pairwise run has delivered either (pilot 2 left 9, 10 and 16 at $1.5$ to
$2.8\times10^{-2}$). *Limits:* the frame, cap and $u^\ast$-enclosure obligations of the
composition review are unchanged; square 6 stays coarse; the outer route from the cells
is open.

**Instrument contract: the patch counter.** *Inputs:* exp-244’s exact kernel (the 52
positive stress rows), the H256 slider domain plus $10^{-2}$ as rows, the 135 option
margins, the seven backbone angles (9, 10, 11, 12, 13, 14, 16) as the sphere $S^6$ of
directions with the nine other angles handled by the scope review’s one-dimensional
wall-weight check. *Enumeration:* for each sampled direction $d$ and radius
$r\in\{10^{-4},10^{-3},
5\times10^{-3},10^{-2}\}$, solve the LP at $\psi^\ast+rd$ in floating point, record the
optimal basis as the sorted tuple of active rows, and count distinct bases per radius;
record each basis’s slope and the largest second difference along $d$. *Sample size,
fixed now:* 2,000 directions per radius, 8,000 LPs, minutes on one worker; a second
independent draw of 2,000 at $10^{-2}$ for the estimator’s variance.
*Decision thresholds:* the Chao1 estimate of the total basis count
$\hat N=N_{\rm seen}+f_1^2/(2f_2)$ ($f_1$ singletons, $f_2$ doubletons) at or under
$10^4$, with singletons under a fifth of the sample, selects the exact build (under a
second a patch, by the scope review); $10^4$ to $10^5$ selects it with a CPU-day budget;
above $10^5$, or singletons above half the sample at 8,000 (the count has not
saturated), the patch count is uncontrolled and the instrument is not the route.
Any negative slope in any sample falsifies the candidate before the build.
*Not part of the contract:* soundness, which is the exact build’s (interval Krawczyk
solves and outward rounding, per the scope review).

## Evidence Status

| Kind | Items |
| --- | --- |
| Proved (exact geometry, by hand) | $h'(\theta^\ast)=(\cos\theta^\ast-\sin\theta^\ast)/2=0.0641$ and $-0.103$; the wall-coupling bound $\rho/h'$; the corner recession $\alpha/\sqrt2$ of a square’s rotations; the support derivative $\tfrac12\lvert\sin\varphi-\cos\varphi\rvert$; the box support $1.41\rho$ along $u$; the second-order octagon loss |
| Computationally verified | the scorer’s round table, per-side extents, target factors and cost fit at `451154f60` (JSON `dadde829…`), identical to the committed `score.txt` except the target column; every receipt figure in sections 1 to 3 (settings, splits, `g_sides`, ranges, turn ranges, hull vertices and areas, `hull_area_lost`, collision counts, the 128-row `final_round_per_owner`); the code path of the pull (`producer.py` lines 66, 191 to 228, 573 to 584, 681 to 715; `pilot_n17_capture.py` lines 730 to 757, 942 to 966, 1491 to 1520); the 21 contact pairs and 52 positive rows |
| Asserted | the identification of the $1.26\times10^{-4}$ residual with the pull (a prediction with no free parameter, matched to 3.5 per cent, not yet checked against a node); the loop account of section 4 and the lever-arm reading of the turn ranges; the re-derived constant of reading A (160 to 250); every cost in section 6, from the scorer’s $\alpha=1.27$ fit; the n11 control’s cost; the thresholds of section 7 |
| Not done | any new computation beyond the scorer; the n11 control; a node-level check of the hull faces; a re-run of the after-pilot probe, which is on no ref |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
