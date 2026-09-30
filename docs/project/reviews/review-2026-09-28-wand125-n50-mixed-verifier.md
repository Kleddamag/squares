# wand125 n = 50 Mixed Certificates: The Threshold-One Verifier and the Containment Argument

The argument behind `mixed_n50_L740` is sound.
Given a passing local replay of the shipped checker, it proves $s(50)\ge 37/5$. The
certificate is the same object Tokoharu’s format carries, a D4-expanded family of
uniform-density axis-aligned rectangles with total mass below the count, and the checker
is Tokoharu’s `verify.cpp` with two changes of substance: the acceptance threshold
$\Gamma$ is read from the input and set to $1$ instead of the compiled-in $10001/10000$,
and the centre domain at each net angle is the union of unit-square centres whose
orientation the net assigns to that angle, a subset of Tokoharu’s domain.
Both changes are legitimate.
The $10001/10000$ margin pays for nothing in the proof: every quantity the checker
compares is a rigorously rounded bound with no dropped term, and the theorem needs only
$\Gamma\ge 1$ with mass below $n$. What the margin bought was insurance against an
undetected over-estimation in the checker of size below $10^{-4}$; with $\Gamma=1$ that
insurance is gone, so this review re-derived every step of the bound and ran a one-sided
exact control against the compiled checker (72 boxes, no violation).
No blocking finding was found for any of the three certificates.
Six non-blocking observations are recorded, one of them a wrong figure in the L7318
README.

This is the correctness lane (W2 factual review) of the coordinator’s 2026-09-28 wand125
intake, written by a Fable max sub-agent under a one-core budget.
It registers nothing and moves no bound.

## Scope and Evidence

The reviewed source is
[wand125/square-packing-bounds at `39d8ecc`](https://github.com/wand125/square-packing-bounds/tree/39d8ecc74d651b54ec977c331c8f2015b442a6c4),
read from a sparse checkout and from copies of its three proof bundles, each unpacked
into the scratchpad and validated against the hash list it carries:

| Certificate | Claim | Bundle SHA-256 | Files | Verifier source SHA-256 |
| --- | --- | --- | ---: | --- |
| `mixed_n50_L740` | $s(50)\ge 37/5$ | `90621d1a…` | 621 | `code/mixed_rotated_verify.cpp`, `89b674a6…` |
| `mixed_n50_L735` | $s(50)\ge 147/20$ | `b7e8ac31…` | 1,043 | `src/unified_linear_verify.cpp`, `0249726a…` |
| `mixed_n50_L7318` | $s(50)\ge 3659/500$ | `239e4ac5…` | 621 | `code/mixed_rotated_verify.cpp`, `89b674a6…` |

Every listed file’s digest matched; the top-level `candidate.json`, `certificate.json`
and `manifest.json` of each certificate directory are byte-identical to the copies
inside its bundle, and the `certificate_sha256` in `completion-audit.json` (L740) and
`final-audit.json` (L735) names the shipped `certificate.json`. The L740 and L7318
`code/` directories are identical to each other and to the `code/` directories inside
their bundles.

The reference checker is Tokoharu’s, retained with the
[September 22 packet](../../../packing/resources/web/external-square-certificates-2026-09-22/tokoharu-density/README.md):
`verify.cpp` (SHA-256 `a75140df…`, 126 lines) and `run_verify.py` (`7bce2467…`), with
`certify.py` for the input conversion, and the proof note
`docs/continuous-density-certificate.ja.md`. The upstream head
[`84bebef`](https://github.com/tokoharu/square-packing-density-bounds/tree/84bebef51856d46a19c145b035664324ba9572d3)
carries the same two files.
The prior reviews relied on are the
[density mathematics review](review-2026-09-22-tokoharu-density-mathematics.md) and the
[rectangle scaling review](review-2026-09-27-wand125-rectangle-scaling.md); the rungs
are those of [epistemics.md](../../../epistemics.md).

Read in full: both C++ verifiers and Tokoharu’s, side by side; every Python file in the
L740 `code/` directory (`mixed_rotated_verify.py`, `verify_rotated_result.py`,
`verify_mixed_full_proof.py`, `verify_axis_certificate.py`, `mixed_axis_cells.py`,
`mixed_density_check.py`, `mixed_net_audit.py`, `score.py`, `endpoint_cells.py`); the
L735 `audit.py`, `replay.py`, `unified_linear_verify.py`,
`unified_linear_full_verify.py` and `unified_measure.py`; the three READMEs, manifests
and audits; and the n = 50 section of the source README.

Run here on one core, x86-64 Linux, `g++` 13.3.0, project CPython 3.14.7, always on
scratchpad copies:

- exact-rational recomputation, using the shipped `expand`, of the L740 mass, digest,
  rectangle validity, net identities and all 201 centre domains;
- byte-identical regeneration of all 200 oblique `input.txt` files of L740 from
  `candidate.json` through the shipped `export` (32.7 s), which also exercises the
  enclosure assertion inside `interval()` on every one of the 22,126 values per angle;
- compilation of `mixed_rotated_verify.cpp` with the shipped compile line and a
  `query`-mode control: 72 random centre boxes at net indices 1, 150 and 200, each
  checker lower bound compared with the exact rational coverage at the box centre and
  its four corners;
- statistics over every per-angle record of all three bundles.

No replay of the 201 directions was run; that is the replay lane’s work, and the budget
it needs is in the last section.

## What the 10001/10000 Margin Pays For

Tokoharu’s checker fixes the threshold at
[`verify.cpp:99`](../../../packing/resources/web/external-square-certificates-2026-09-22/tokoharu-density/src/verify.cpp),
`threshold = up(10001./10000.)`, compares against it at lines 110 (axis vertices) and
118 (branch-and-bound leaves), and `run_verify.py:8` asserts the printed bound is at
least $1.0001$ again.
Nothing else in the checker mentions it.
To decide whether the margin absorbs an error term, one has to ask what the accepted
inequality actually certifies.

At a leaf with normalized box $(u,v,d_u,d_v)$ the checker returns

$$
\text{lower}=\downarrow\!\big(\downarrow\!(f-r_x)-r_y\big),\qquad
f=\sum_j\downarrow\!\big(\rho_j^{\,l}\,A_j\big),\qquad
r_x=\uparrow\!\big(d_x^{\,h}\,\sup_{X\times Y}|\partial_xF|\big),
$$

where $\downarrow,\uparrow$ are `nextafter` roundings, $\rho_j^{\,l}$ is the lower end
of the density enclosure, $A_j$ is `area_lower`, and $X\times Y$ is the outward-rounded
enclosure of the physical box.
Each factor is a proven bound in the safe direction:

- **Input enclosures.** `certify.py:18–24` converts every rational to two adjacent
  binary64 endpoints and refuses the conversion unless the exact value lies between
  them. The checker reads them with `stod`, which parses hexadecimal exactly.
- **Area.** `area_lower` (lines 32–71) builds a candidate polygon with plain doubles,
  then proves with interval tests that every vertex lies inside the rectangle (line 62)
  and inside the core for every parameter value in the enclosures (line 64), and that
  the polygon is strictly convex and counterclockwise (lines 66–69). The `1e-9` shrink
  and the `1e-14` hull cutoff touch only the candidate; a failed test returns $0$, which
  is always a valid lower bound on an area.
  The fully-contained branch (line 37) uses the enclosure’s upper ends against the
  core’s lower half-side.
- **Derivative.** `slice` (lines 74–77) encloses the length of a rectangle edge inside
  the core as the centre ranges over the whole box; `fx`, `fy` are interval sums of
  left-minus-right and bottom-minus-top lengths, which is the exact almost-everywhere
  derivative of a Lipschitz function, and $r_x,r_y$ round the products upward.
- **Comparison.** `lower >= threshold` with `threshold` an upward enclosure of the
  rational; the axis case compares an interval lower end the same way.

So `lower` $\le F(x,y)$ for every centre in the box, with nothing omitted; the review of
2026-09-22 reached the same conclusion in its words “a sufficient certificate
inequality, not a tolerance that admits violations”.
The angular step is an exact containment (next section), not an interpolation, and the
proof note’s smoothing lemma (§5) loses nothing either.
Tokoharu’s own corollary in §0 of the note,
$N\le\sum_i\int_{Q_i}f\le\int_Kf=\sum_jw_j<N$, uses only $\int_Qf\ge1$; the
$10001/10000$ in its theorem statement is what the checker happened to certify, not what
the corollary consumes.

The number comes from the search side.
`master.py:25` solves the LP with `rhs = 1.001` and rescales weights to restore
feasibility (lines 143–146); `global_separation.py:23` requires its screening target to
sit in $(1.0001,\ \text{rhs})$; `point_engine.py:240` defaults its own `rhs` to
$1.0001$. The gap from $1.001$ down to $1.0001$ is the cushion between the LP’s finite
pose sample and the continuous check; the gap from $1.0001$ down to $1$ is spent by
nobody. The answer to the coordinator’s question is therefore (b): a numerical safety
factor with no role in the proof.
Its practical value is that a certificate accepted at $10001/10000$ would still be a
proof if the checker over-estimated coverage by anything under $10^{-4}$ through an
undetected defect. At $\Gamma=1$ no such defect is tolerated, which is why the next
section reads the modified checker with that in mind and why the control in this review
measures the direction of the bound, not merely its reproducibility.

## The Verifier Against Tokoharu’s, Line by Line

A mechanical `diff` between the retained `verify.cpp` and
[`mixed_rotated_verify.cpp`](https://github.com/wand125/square-packing-bounds/blob/39d8ecc74d651b54ec977c331c8f2015b442a6c4/certificates/mixed_n50_L740/code/mixed_rotated_verify.cpp)
shows the interval primitives, `area_lower` and `slice` byte-identical (the three
function bodies hash the same in both files and in the L735 verifier).
Every change is in `bound`’s interface and in `main`:

| Change (line in the mixed source) | Effect | Soundness |
| --- | --- | --- |
| `bound` takes interval `cx, cy, dx, dy` and an atom list instead of `(u, v, du, dv, L)` (81) | `E` is no longer computed as $L/2-B(c+s)/2$ inside C++; it is read from the input (110) and applied at 130 | Preserved: the enclosure of the exact centre is unchanged, and the input `E` is the exact per-node value enclosed by `interval()` (below) |
| Point-mass term (97–103): a point counts only if inside the core for every centre of the box | Adds a nonnegative certain-capture term; one extra `dn` | Preserved; unexercised here, `points` is empty in all three candidates |
| $c, s$ read from the input (110) rather than formed from $83r$ and $40000$ in C++ (Tokoharu 113) | Exact rationals $(1-t^2)/(1+t^2)$, $2t/(1+t^2)$ enclosed in Python | Preserved: both are enclosures; the Python one is asserted |
| `gamma` read from the input; leaf test `b.lower >= gamma.h` (131) | Threshold $10001/10000$ becomes an input; here `0x1p+0 0x1p+0`, so `gamma.h` is exactly $1$ | Preserved: `lower` is a rigorous bound, `gamma.h` $\ge\Gamma$ |
| `assert(r.rho.l >= 0)`, `assert(p.w.l >= 0)` on input (112, 114) | Refuses negative densities and weights | Strengthening |
| Node limit from `argv[2]` (121, 128) instead of $10^7$; depth floor $2^{-40}$ instead of $2^{-45}$ (132) | Resource limits; a breach pushes the box back and stops | Preserved: an unresolved box is reported, never certified |
| Status in JSON, exit code $0$ in every case (139–143) instead of `return 3` | `ANGLE_VERIFIED` only when the stack is empty | Preserved for a driver that reads the status; see MV-1 |
| Split heuristic: anisotropy cap and `1e-14` tie-break (134–136) | Choice of split axis only | No bearing on soundness |
| `region` mode (124–127) and `query` mode (116–120) | A sub-box run, and a bound oracle on stdin | Not in the proof path; the replay re-runs the whole domain, so a region result cannot substitute for an angle |
| Axis direction removed from C++ | Handled by `verify_axis_certificate.py` | Reviewed separately below |

No tolerance was loosened.
The two approximate constants of `area_lower` are unchanged, and the only threshold that
moved is $\Gamma$ itself, which the theorem permits.
The one extra `dn` in the return value makes the bound weaker, not stronger.

### Input conversion

[`mixed_rotated_verify.py:16–22`](https://github.com/wand125/square-packing-bounds/blob/39d8ecc74d651b54ec977c331c8f2015b442a6c4/certificates/mixed_n50_L740/code/mixed_rotated_verify.py#L16-L22)
is `certify.py`’s `enclosing` under another name: nearest binary64, one `nextafter` step
outward on whichever side falls short, and an assertion that the exact value lies in the
result. `export` (lines 29–42) writes $L$, $B$, $E$, $c$, $s$, $\Gamma$, then the 4,424
images as $(x_0,y_0,x_1,y_1,\rho)$ with $\rho=m/(8|R|)$ formed exactly in `expand`, then
the (empty) point list.
It refuses $\Gamma<1$ (line 33): the runner’s theorem form is $\Gamma\ge1$ with mass
below $n$. Regenerating all 200 files here reproduced the shipped bytes and manifests
exactly, so the enclosure assertion held for every endpoint and weight of every angle.
The $E$ written for net index 1 is $102366944669/32000034445$, which is $L/2-\rho(a_1)$
for the domain formula derived in the next section.

### The oblique drivers

`verify_mixed_full_proof.py` (lines 19–45) is the single entry point the README names.
It reads `candidate.json`, expands and digests it, checks the point measure’s symmetry,
recomputes the net certificate and the 201 domains, requires the manifest’s net to equal
the recomputation and the digests to agree, requires the bundle’s `verify.cpp` to equal
the source in `code/` and to hash to the manifest’s `source_sha256`, replays the axis
table, compiles, and for every $j=1,\dots,200$ requires the saved `result.json` to say
`ANGLE_VERIFIED` with an empty frontier and a manifest whose digest, index, domain and
$\Gamma\ge1$ match, then hands it to `verify_rotated_result.replay`, which regenerates
the input, requires byte equality with the saved one, re-runs the binary with the saved
node count as the limit and requires `status`, `nodes`, `leaves`, `lower` and `frontier`
to be equal. `expand` itself refuses a candidate whose masses do not sum to `total_mass`
or whose sum is not below $n$ (`mixed_density_check.py:28–29`), so the mass inequality
is machine-checked on every path that touches the candidate.

### The axis direction: an integer-table checker

At net index 0 the coverage is bilinear on every cell of the event grid, so its minimum
over a cell is at a corner; the 2026-09-22 review established this for Tokoharu’s vertex
loop.
[`verify_axis_certificate.py`](https://github.com/wand125/square-packing-bounds/blob/39d8ecc74d651b54ec977c331c8f2015b442a6c4/certificates/mixed_n50_L740/code/verify_axis_certificate.py)
replaces the interval vertex loop by integer tables and verifies the tables rather than
trusting them:

- lines 18–28 rebuild the event set $\{x_0\pm B/2,\ x_1\pm B/2\}\cap(L/2,\ L-1/2)$ over
  all 4,424 images for each axis, add the two domain endpoints, and require the stored
  axis lists to equal it (3,635 events per axis, 13,205,956 cells);
- lines 29–39 require integer coordinates after scaling by $D=5\times10^{16}$, weights
  $w_j\le 2^{24}\,m_j$ per image (checked exactly), and $(\sum w_j)\,2^{32}<2^{63}$ so
  that the `int64` products cannot overflow;
- lines 40–52 check every table entry: $f_{ij}\,(x_1-x_0)\le 2^{16}\,\ell_{ij}$ with
  $\ell_{ij}$ the exact overlap of $[x_i-B/2,x_i+B/2]$ with $[x_0,x_1]$, so
  $f_{ij}/2^{16}$ is a lower approximation of the overlap fraction;
- lines 53–61 form $\sum_j f_{ij}w_jf'_{kj}$ by integer matrix product, take the cell
  minimum over its four corners, compare with $\lceil\Gamma\cdot 2^{56}\rceil$, and
  require every failing cell to appear in `exact_patches` with an exact rational
  recomputation (`mixed_axis_cells.py`) at or above $\Gamma$, and no patch elsewhere.

The product is at most $2^{56}$ times the exact corner coverage, so the integer minimum
is a lower bound; here it is $277199759147/274877906944\approx1.00845$ with no patches,
a margin of $0.8\%$ that none of the oblique directions has.
This is a different implementation from the C++ for one of the 201 directions.
It does not make a second method for the claim.

### The L735 verifier

`unified_linear_verify.cpp` is the mixed verifier plus three things: a `Segment` type
with `segment_lower` (lines 86–106), a `singular_lower` that sums point and segment
captures (107–113), and an axis branch inside `bound` taken when $s=[0,0]$ (125–138).
The shared functions are byte-identical.
The axis branch bounds $f$ by the interval product of the two overlap lengths at the
centre and the derivative by `axis_slice` (116–121), which returns the exact edge length
when the edge lies inside the core’s $x$-extent for every centre of the box, $0$ when it
never does, and $[0,\text{length}^h]$ otherwise; that encloses the left-minus-right
derivative, so the leaf inequality is the same FTC bound as at oblique angles.
The L735 export (`unified_linear_verify.py:22`) uses Tokoharu’s domain $E=(L-B(c+s))/2$,
hard-wires $\Gamma=1$ (line 30), and `net_check` (`unified_measure.py:67–72`) requires
$B(1+D)<1$ and the net to reach $\tan(\pi/8)$. `validate` expands each primitive to its
eight images at $m/8$ each.
The candidate carries 499 rectangle primitives and no point or segment, so the two new
capture routines are dead code for this certificate; `segment_lower` was read for the
direction of its bound (it proves both endpoints of a numerically proposed sub-segment
inside every core of the box and charges only the proven parameter length) and not
further. The axis direction ran through this branch: 230,167 nodes, printed bound
$1.000000035$. `audit.py` and `replay.py` check the 1,043 hashes, the mass
$4999999/100000$ against $n=50$, $L=147/20$, the net, the source digest, and replay
every direction with byte-compared regenerated input, as the L740 driver does.

## The Containment Argument in Exact Arithmetic

Write $D=83/40000$, $t_r=rD$, $\theta_r=2\arctan t_r$, $B=9977/10000$. The identities
below were recomputed here as rationals; the manifests record the same values.

- **Reach.** $t_{200}=83/200$ and $t_{200}^2+2t_{200}-1=89/40000>0$, so
  $\theta_{200}>\pi/4$ and every $t\in[0,\sqrt2-1]$ has a nearest node
  $r=\operatorname{round}(t/D)\le200$ with $|t-t_r|\le D/2$.
- **Last node is used.** Its bin’s lower end is $a_{200}=t_{200}-D/2=33117/80000$ with
  $a_{200}^2+2a_{200}-1=-4544311/6400000000<0$, so the bin reaches below $\pi/4$;
  `net_certificate` (`mixed_net_audit.py:27–28`) checks both facts.
- **Half-angle to angle.** For $t,t_r\ge0$,
  $\tan\tfrac{|\theta-\theta_r|}{2}=\dfrac{|t-t_r|}{1+tt_r}\le|t-t_r|\le\dfrac D2=:z$.
- **Projection width.** With $\delta=|\theta-\theta_r|$ and $z=\tan(\delta/2)$,
  $\cos\delta+\sin\delta=\dfrac{1+2z-z^2}{1+z^2}\le1+2z$, because
  $(1+2z)(1+z^2)-(1+2z-z^2)=2z^2+2z^3\ge0$. At $z=D/2$ the left side is
  $6413273111/6400006889$ and $1+2z=1+D$.
- **Strict containment.** In the frame of the unit square at $\theta$, the concentric
  $B$-square at $\theta_r$ has axis half-width $B(\cos\delta+\sin\delta)/2\le B(1+D)/2$,
  and $B(1+D)=9977\cdot40083/(10000\cdot40000)=399908091/400000000<1$, leaving
  $91909/800000000\approx1.15\times10^{-4}$ on each side.
  A closed core therefore lies in the open interior of its unit square.

The reduction to $[0,\pi/4]$ uses the diagonal reflection, which maps orientation
$\theta$ to $\pi/2-\theta$ and centre $(x,y)$ to $(y,x)$; the density is invariant
because `expand` writes all eight D4 images of every rectangle with mass $m/8$ each
(`mixed_density_check.py:17–22`), whatever the listed set looks like.
The listed 553 rectangles are not themselves reflection-closed (checked here); they are
a fundamental-domain representation, and the total mass is $\sum m_j$ regardless of
coincident images.

### The per-node centre domain

A unit square at orientation $\theta\in[0,\pi/4]$ fits in $[0,L]^2$ exactly when its
centre lies in $[\rho(\theta),L-\rho(\theta)]^2$ with
$\rho(\theta)=\tfrac12(\cos\theta+\sin\theta)=\dfrac{1+2t-t^2}{2(1+t^2)}$, which
increases on $[0,\pi/4]$ since its derivative is $\tfrac12(\cos\theta-\sin\theta)\ge0$.
The bin of node $r$ is $t\in[a_r,t_r+D/2]$ with $a_r=\max(0,t_r-D/2)$, so the union of
admissible centres over the bin is $[\rho(a_r),L-\rho(a_r)]^2$, and after a quarter-turn
about the container’s centre (a rotation, under which both the density and a square’s
orientation class are invariant) the representative lies in $[L/2,\ L-\rho(a_r)]^2$.
That is what `centre_domains` (`mixed_net_audit.py:51–67`) writes and what the checker
covers with $E=L/2-\rho(a_r)$: for node 0, $\rho=1/2$ and $E=16/5$; for node 1,
$a_1=83/80000$ and $\rho(a_1)=6413273111/12800013778$; for node 200,
$\rho(a_{200})=10601984311/14993471378$. All 201 domains exist (no node is skipped),
each recorded `centre_low` equals $\rho(a_r)$ recomputed here at the six indices
checked, and $\rho(a_r)\ge B(c_r+s_r)/2$ at every node, which the code asserts.

Tokoharu’s domain is $[L/2,\ L-B(c_r+s_r)/2]^2$, every centre at which the core fits in
the container. The mixed domain omits a strip of width $\rho(a_r)-B(c_r+s_r)/2$ (about
$1.2\times10^{-4}$ at node 1, the manifest’s `eliminated_boundary_width`) whose centres
cannot belong to any unit square the bin assigns to node $r$. Coverage need not be
proved there, so the smaller domain is correct; it is also a departure from Tokoharu’s
certificate language that the README does not mention (MV-3). The L735 export keeps
Tokoharu’s domain.

With the domain settled, the theorem is the disjoint-core count: choose in each of 50
packed unit squares its closed core at the assigned net angle; the cores lie in the
squares’ disjoint interiors, so they are pairwise disjoint; each has measure at least
$\Gamma=1$ by the 201 directional checks; their union has measure at most
$M=4999999/100000$; and $50\le M<50$ is impossible.
Compactness makes the inequality strict, as before; the source claims $\ge$.

## Certificate Language and “Green’s Approach”

The phrase quoted in the intake brief does not occur in the tree at `39d8ecc`. What the
README says is that the certificates exceed Green’s reported bound at $n=50=7^2+1$
(Friedman’s DS7 Theorem 9, retained here as `E-green-ds7-theorem9-reported-lower`), that
L740 was “built directly at L = 7.4, from a structured initialization”, and that L735
was contracted from an “L7.40 rectangle initialization”; the run names are
`green_rect_740_fullnet` and `green_plus_one`. Whatever structure seeded the search,
none of it reaches the certificate:

- `candidate.json` (L740) has `"points": []`, 553 `rectangles` each with a rational
  `rectangle` and `mass`, `scaling_factor` `"1"`, and no `proof_net` field, so the net
  defaults to $D=83/40000$, 200; the certificate records `point_mass` `"0"`;
- the densities are uniform per rectangle by construction ($\rho=m/(8|R|)$), spanning
  $2.4\times10^{-8}$ to $2.4\times10^{4}$ per unit area with a smallest side of
  $1.0\times10^{-3}$, which is why the oblique node counts (251,507 to 605,563 per
  direction, against a largest of 237,591 among the standard certificates) are what they
  are and why the leaf bounds sit so near $1$;
- L735’s `primitives` are 499 `rectangle` entries under schema
  `point_line_rectangle_v1`; the schema admits points and segments, and none is present;
- the centre domains are those derived above: per-node bins for L740 and L7318,
  Tokoharu’s for L735.

The two language differences from Tokoharu’s format are therefore $\Gamma$ and, for two
of the three, the centre domain; both are reviewed above.
The search provenance (`completion-audit.json` describes an agent pipeline) is not an
input to the checker.

## Findings

No blocking finding.

### MV-1 — Non-blocking: the C++ exits zero on an unresolved angle, and every check is an `assert`

`mixed_rotated_verify.cpp:139` reports `ANGLE_UNRESOLVED` in JSON and returns $0$, where
Tokoharu’s returns $3$. Every shipped driver reads the status and the frontier
(`verify_rotated_result.py:11`, `verify_mixed_full_proof.py:33`), so the proof path is
safe, but a consumer that trusts exit codes is not.
All acceptance checks in the Python drivers, and Tokoharu’s `run_verify.py:8`, are
`assert` statements, which `python -O` or `PYTHONOPTIMIZE` removes without a message.
The replay must run without either.

### MV-2 — Non-blocking: centre domains are indexed by list position

`centre_domains` skips a node whose bin lies entirely above $\pi/4$ (`continue` at
`mixed_net_audit.py:60`) and returns a list; `export` and the full-proof driver index it
by net index. A net with a skipped node would silently pair angles with the wrong
domains.
Here no node is skipped (201 domains, position equal to index, checked exactly),
so the certificates are unaffected; a reusable importer should key domains by index.

### MV-3 — Note: the READMEs name one of the two format departures

Each README explains “not in tokoharu’s format” by the threshold alone.
The per-node centre domain of L740 and L7318 is the second departure; it is correct, and
it is documented in the code (`eliminated_boundary_width`), but a reader comparing with
`verify.cpp` should know the domain also changed.

### MV-4 — Note: the shipped replay proves determinism, not direction

`verify_rotated_result.replay` requires bit-identical `nodes`, `leaves`, `lower` and
`frontier`, which is what correctly rounded arithmetic without FMA predicts and what the
2026-09-27 review observed across compilers.
It cannot detect a bound that is wrong in the same way twice.
With $\Gamma=1$ that is the property that matters, so this review’s control fed 72 boxes
(half-widths $10^{-3}$ to $10^{-7}$ of $E$, indices 1, 150, 200) to the compiled
checker’s `query` mode and evaluated the exact rational coverage at each box’s centre
and corners with the shipped `evaluate`: the checker’s bound was at or below every exact
value, the smallest gap being $6.6\times10^{-13}$ on a $10^{-5}$ box.
That is a one-sided finite control, not a proof, and an audit tool of the kind
`audit_tokoharu_density.py` provides for the standard certificates would be the natural
place to keep it.

### MV-5 — Note: the L7318 README’s minimum is not the minimum

The L7318 README and the source README give the lowest oblique leaf bound as
$1.0000019\ldots$. The certificate records $1.0000000069521284$ at net index 81; the
quoted figure is the printed bound of other angles (it appears in the records of indices
28, 57 and 79). The L740 ($1.0000000004\ldots$, index 150) and L735
($1.0000000005\ldots$, index 149) figures are right.
The printed minimum is a branch-and-bound artefact in any case, as the 2026-09-27 review
explains: a leaf is accepted the moment it clears $\Gamma$, so the least accepted bound
always sits just above the threshold and says nothing about the true minimum, which a
120-point random probe here never saw below $1.0098$.

### MV-6 — Note: dependency statements and dead paths in L735

The L735 README asks for SciPy, Numba and HiGHS; `replay.py`’s import chain
(`unified_linear_full_verify`, `unified_linear_verify`, `unified_measure`,
`mixed_rotated_verify`, `mixed_density_check`, `mixed_net_audit`, `score`) needs only
the standard library, and the L740 driver needs NumPy for the axis tables.
The L735 verifier’s point and segment paths, and its `region` and `query` modes, are
unexercised by the certificate and were read only for the direction of their bounds.

## Verdict and Rung

**L740.** The argument is sound: the exact identities above, the D4 and quarter-turn
reductions, the per-node domain, the rigor of every rounded step in `bound`, and the
mass inequality $4999999/100000<50$ together prove that 50 unit squares do not pack in
side $37/5$, provided the 201 directional statements hold; those are what the shipped
checker decides, and a passing local replay of
`verify_mixed_full_proof.py proof --workers 3` on the unpacked bundle is the evidence
for them. With that replay recorded as repository-origin, interval-certified evidence
with a certificate, a replay command and a passing status, the result supports V4 and C3
in the register’s vocabulary (`assurance: verified`, `method: interval-certified`), and
C5 once this review is mapped and a control path is named.
C4 is not available: the axis integer-table check is a second implementation for one
direction, not a second method for the claim.

**L735** ($147/20$) and **L7318** ($3659/500$) rest on the same argument.
L735’s verifier differs by the additions listed above and uses Tokoharu’s centre domain;
its replay is `audit.py` then `replay.py --workers 3`. L7318 uses the L740 code
unchanged. Both are superseded by L740 for the register and remain valid certificates in
their own right.

**Assumptions not machine-checked.** The containment lemma and the bin-domain lemma are
prose; only their rational instances ($B(1+D)<1$, the reach polynomials,
$\rho(a_r)\ge B(c_r+s_r)/2$) are computed.
The D4 reduction, the quarter-turn reduction, the bilinear-cell argument for the axis,
the FTC bound with an almost-everywhere derivative, and the disjoint-core count are
prose. The trusted base is the reviewed C++ logic, the compiler with the fixed flags,
`stod`, `nextafter`, binary64 with round-to-nearest, NumPy’s `int64` matrix product, and
CPython’s `Fraction`; none is proof-assistant checked.
The theorem is about closed unit squares with disjoint interiors in the closed
container.

**The standard rectangle certificates, n = 18 to 95.** Nothing found here touches them.
Their checker is the unmodified `verify.cpp` at $\Gamma=10001/10000$ with Tokoharu’s
domain; the shared kernel was re-read here in the stricter $\Gamma=1$ setting and no
over-estimation was found, which if anything adds confidence to the margined family.
One consequence for the register: the L740 certificate refutes 50 squares, so by
monotonicity $s(52)\ge37/5$ and $s(53)\ge37/5$, above the verified $369/50=7.38$ those
cases hold from the n53 point file; the transfer stops at $n=54$, where Nagamochi’s
$1+\sqrt{41}\approx7.4031$ is larger, and at $n=51$ the register’s reported $743/100$
stays ahead.

## What the Replay Lane Must Check

- Unpack a copy of `n50-L7.40-proof-bundle.tar.gz` (SHA-256 `90621d1a…`) and validate
  all 621 entries of `files-sha256.json` first; the checker writes `certificate.json`,
  `replay-progress.json`, `replay-verify` and every `replayed.json` into `proof/`, so
  keep a pristine copy for comparison.
  (This review’s own runs left `__pycache__` directories in its scratch copy; the
  shipped bundle has none.)
- Run exactly the README command with the project interpreter,
  `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1`, `--workers` at most 3 (the driver refuses
  more), `PYTHONOPTIMIZE` unset and no `-O` (MV-1), and `c++` resolving to a C++17
  compiler; record `c++ --version`. The compile line is fixed inside `compile_verifier`
  (`-O2 -std=c++17 -ffp-contract=off -fno-fast-math`, no `NDEBUG`, so the divisor and
  rounding-mode asserts are live).
  NumPy is required for the axis replay.
- Expect `ALL_ANGLES_VERIFIED_AND_REPLAYED`; the axis `replayed.json` with `cells`
  13,205,956 and `integer_minimum` 1.0084468491077132; and per-angle `replayed.json`
  with `nodes` and `lower` equal to the shipped `result.json` (the driver asserts this,
  so a mismatch is a nonzero exit).
  The regenerated `certificate.json` will not be byte-identical to the shipped one
  because `results` is written in completion order; compare it field by field.
- Budget: upstream, 200 oblique directions took 7.88 CPU-hours (mean 142 s, maximum 297
  s at index 200, 80.7 million nodes in all) plus 59 s for the axis on Apple arm64; plan
  on roughly three hours with three workers here, and set a wall ceiling above the
  slowest direction rather than a per-run default.
- Record independently, outside the shipped code, the mass, the digest `fdfaed93…`, the
  verifier digest `89b674a6…`, and the identities of this review; the exact regeneration
  of all 200 inputs (33 s) is cheap enough to repeat.
- For L735: `python3 audit.py` then `python3 replay.py --workers 3` inside the unpacked
  `green-n50-L735` (1,043 hashes, 63.7 million nodes, 3.48 CPU-hours upstream); expect
  `FINAL_CERTIFICATE_AUDITED` and `ALL_201_ANGLES_REPLAYED`. For L7318 the L740
  procedure applies (25.2 million nodes, 1.33 CPU-hours upstream).

## What Remains Unchecked

The 201 directional statements themselves, pending the replay.
Any global second method (an exact-rational or independently written interval coverage
check over the whole domain), which would be the route to C4. The `segment_lower` and
point paths of the L735 verifier beyond the direction of their bounds, and the `region`
mode of both verifiers, none of which the certificates use.
The exact Green comparison in `completion-audit.json` was checked only to the extent
that $37/5-(2\sqrt2+101/25+3\sqrt{14}/25)=0.08257\ldots$ agrees in floating point with
the recorded rational; the register’s Green entry is a reported bound and this
comparison moves nothing.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
