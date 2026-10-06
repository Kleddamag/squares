# Proof Review: squarepacker’s k^2 - M(k) >= 0.033 log k

Reviewed 2026-10-05 from the retained packet
[`squarepacker-k2-minus-c-2026-10-05`](../../../packing/resources/web/squarepacker-k2-minus-c-2026-10-05/README.md),
which holds `squarepacker/k2-minus-c` whole at `25f645e8` (tag `v1.1` plus the DOI line
of its README). The reviewer is an AI agent: the adversarial review lane of the
2026-10-05 stage 4 of the result import for
[jlevy/squares#368](https://github.com/jlevy/squares/issues/368). The lane was prompted
separately from the lane that retained the source and from the lane replaying its
certificate. It shares no context with either and has not seen the replay.
The model is `claude-opus-5-5` at the tbd-strong tier, whose configured reasoning
setting is xhigh.

The claim is Sungjoon Ryu’s preprint “Packing $k^2-c$ unit squares: $s(k^2-c)=k$ for all
large $k$”, version 1.1, as #368 reports it.
Let $M(k)$ be the largest number of unit squares in $[0,k]^2$ that are pairwise disjoint
as closed sets. Theorem 1.1 then states $k^2-M(k) \ge 0.033\log k$ for every integer
$k \ge 2$, and $k^2-M(k) \ge (0.99977\log k+0.3819)/30.147$ for $k \ge 10^{13}$.
Corollary 1.2 states $c^*(k) \ge 0.033\log k - 1$, so $c^*(k)\to\infty$. No register id
has been assigned to the claim, so this review covers it as reported and has no draft
significance score to confirm.
It registers nothing and moves no bound.

**This is one AI review, not a referee’s report.** No human has refereed the preprint.
The source’s own reviews, which `reviews/REVIEWS.md` summarises, were all by AI
reviewers that its author describes as “of the same family”.
This reviewer is of that family too, so it may share their blind spots.
Nothing below says the theorem is proved, confirmed or verified.
It says what was read and re-derived here, what was computed here and with what code,
and what remains unchecked.

**In one line:** the whole argument was re-derived here line by line, from the closed
packings of Lemma 2.1 to the bracket $30.147$, and no blocking defect was found; every
numerical constant re-computes at 50 digits in code written here, Roth and Vaughan’s
statements match the retained original page by page, and the reduction of Lemma 4.10 to
the bound $U(I)$ that the programs decide is complete.
The constant $0.033$ and the formula for $k \ge 10^{13}$ rest on one Arb implementation
of the labelling of 78,673 boxes, which this lane ran on 22 boxes only; the qualitative
theorem, with $0.027$, does not depend on it.
Nine findings are recorded, none blocking.

## 1. The Reduction

**Lemma 2.1** (`paper.tex` lines 133–149). If $n$ squares with disjoint interiors fit in
a square of side $s<k$, dilating the centres by $\lambda=k/s$ about the common centre
turns every weak separation $u\cdot(c_2-c_1) \ge h_1(u)+h_2(u)$ into a strict one
(because $h_1+h_2 \ge 1>0$ forces $u\cdot(c_2-c_1)>0$), and keeps each square inside
$[0,k]^2$ by the computation on line 143. So $s(n)<k$ gives a closed packing of $n$
squares. Conversely, a closed packing has a positive gap between every pair of squares,
and contracting the centres by $\mu<1$ near $1$ keeps the strict separations while
putting the squares in a concentric square of side $\mu k+(1-\mu)\sqrt2<k$. Both
directions check. Since $s(n) \le k$ for $n \le k^2$, $s(k^2-c)=k$ holds exactly when
$k^2-c>M(k)$, which gives $c^*(k)=k^2-M(k)-1$.

**Corollary 3.3** (lines 206–214). $W=k^2-N$ is an integer.
If $W=0$, almost every horizontal line is covered up to a null set by finitely many
pairwise disjoint closed intervals, at least two because each has length at most
$\sqrt2<k$; their union is closed of full measure, hence all of $[0,k]$, which is then
not connected. This is right, and it is where closedness first matters.

**Corollary 1.2** (lines 95–98) follows: $c^*(k)=W_{\min}-1 \ge \kappa\log k-1$.

**Integer rounding.** It is handled correctly, and conservatively.
$s(k^2-c)=k \iff W_{\min} \ge c+1$, and since $W$ is an integer, $W \ge F(k)>c$
suffices. With $F(k)=(0.99977\log k+0.3819)/30.147$ this is
$\log k>(30.147c-0.3819)/0.99977$, which is $120.2338$ for $c=4$; the stated
$\log k>120.24$ is that value rounded up (Remark 7.4, line 1174). The general form
“$\log k>30.16c-0.38$” dominates the exact threshold $30.15394c-0.38199$ for every
$c \ge 0$, and for $c \ge 2$ it lies above $\log k_2=29.9336$, as the remark requires.
Corollary 1.2’s own form $\kappa\log k-1$ is weaker than $\lceil F(k)\rceil-1$ and is
not the one the threshold uses.
Nothing is lost by the rounding in either direction.

## 2. The Explicit Roth–Vaughan Fundamental Lemma

**Against the original.** The retained PDF of Roth and Vaughan (1978) was read at
printed pages 170–173. Every statement the preprint attributes to it matches:

| Preprint | Roth and Vaughan, as printed |
| --- | --- |
| Theorem, “p. 170”: $w(\alpha)\gg(\alpha\lVert\alpha\rVert)^{1/2}$ when $\alpha(\alpha-[\alpha])>1/6$ (lines 79–81) | p. 170, Theorem, verbatim. The side condition uses the fractional part and the bound the distance to the nearest integer, as the preprint keeps them |
| Inclination of a square and between squares, $S_0$ the boundary (line 158) | p. 171, §2 |
| $c=10^{-10}$, “p. 171, (3)” (line 508) | p. 171, equation (3) |
| Rectangle $R$ of width 1 about $L$, “§3, p. 172” (lines 289–290) | p. 172: $L$ joins the centres, or is a shortest segment from the centre of $S_1$ to $S_0$; two unit segments perpendicular to $L$ at its ends |
| Distance at most 1, $m \le 20$, strip width $1/(4m+1)$, area $(4m+1)^{-2}\tan(\theta/2m)$, “pp. 172–173” (lines 505–508) | p. 172 (distance at most 1; $m \le 20$ from area $(1+2\sqrt2)(1+3\sqrt2)<21$; strips of width $1/(4m+1)$) and p. 173 (the trapezoid bound $>c\theta$) |

The preprint’s “about $3.8\cdot10^{-6}\theta$ for $m=20$” is $\theta/(81^2\cdot40)$. It
states Roth and Vaughan’s theorem without the $10^{-100}$ that secondary sources attach
to it, which agrees with the record’s reading of the primary in
[`asymptotic-waste-bounds.yaml`](../../../packing/frontier/asymptotic-waste-bounds.yaml).

**Lemmas 4.1, 4.2 and 4.4** (lines 246–285, 361–374) were re-derived.
In Lemma 4.1 the minimum of $1/p+1/q$ under $p,q \ge \varphi$, $p+q \ge 2$ is at
$\{\varphi,2-\varphi\}$, giving $\varphi(2-\varphi)\lambda^2/4$. In Lemma 4.4 the last
case uses $p-\sin\psi\cos\psi=1-\tfrac12(p-1)^2 \ge 0.914>\nu$.

**Proposition 4.3** (lines 294–355). Part (a) holds: a square $Z$ meeting a chord of the
open strip $\Sigma$ cannot cross the segment $\{c_1+tn:|t|<\tfrac12\}$, which lies in
the interior of $S_1$, so $Z\cap\Sigma \subset R$. At most one of $\tau^\pm(Z)$ lies in
$(-\tfrac12,\tfrac12)$ because $\tau^+-\tau^- \ge 1$. Part (b), the constant order of
squares on each sub-band, holds by strict separation.
Part (c), $|g_i'| \ge \theta(Z_{i-1},Z_i)$, holds because $\tan$ has derivative at least
1, and a break point of $g_i$ raises its slope by at least 2. Part (d) holds by the
triangle inequality for the quotient metric and the monotonicity of $x(2-x)$ on $[0,1]$.
The proposition as stated carries no distance hypothesis; the distance enters through
the count $m'$, as it should.

**Lemma 4.8(a)** (lines 564–586): the Steiner bound gives
$m' \le \tfrac{12}{\pi}\Lambda+4=9.4023$ for two squares and
$\tfrac{12}{\pi}(d+\tfrac{\sqrt2}2)+2=4.7013$ at the wall, so $q_0=10$.

**Proposition 4.5, $Q_*=0.32$** (lines 376–502), was re-derived through all seven parts.

- **(b) The wall case.** The inscribed axis-parallel square of side
  $\sigma_\theta=1/(\cos\theta+\sin\theta)$ and $|L|-\sigma_\theta/2<d+\theta$ leave no
  room for a deep point.
- **(c) The coordinates.** All six vertex levels and the four line intersections were
  recomputed from $u=(1,h)/\rho_h$ and $n=(-h,1)/\rho_h$.
- **(d) The free gap.** $\Gamma \le 1.415\,\varepsilon_1$ holds in both regimes
  $h \le 1$ and $h>1$.
- **(e) The depth bounds.** $D_u,D_l \le D(h)+3\varepsilon_1$.
- **(f) The two-point bounds.** The closed forms of $\Gamma_*/2-t(V_2')$ and $\chi_u$
  were derived independently, including the $\sigma_\theta$ correction
  $-(1-\sigma_\theta)(1+h)(1-h)^2/(4h\rho_h)$, and the lower-side analogue $\Gamma_l$
  was re-derived the same way.
- **(g) The three minimisations.** $\tfrac13$, $(2-\chi_*)^2/9$ at $z'=(1+4\chi_*)/9$,
  and $\tfrac23(1-\chi_*)^2$ at $z=z'=(1+2\chi_*)/6$ were re-derived, with
  $\chi'(h)=(h^3+3h-2)/(2\rho_h^3)$.

At 50 digits: $D(0.344)=0.1898386<0.19$, $\chi_*=0.2929443<0.29295$,
$(2-\chi_*)^2/9=0.3237821$, $\tfrac23(1-\chi_*)^2=0.3332852$, and the final lower bound
is $0.3232089>Q_*$ (the small-$D$ branch gives $0.3838512$). The minimum is near
$\tfrac13$, against the $\tfrac13$ the author’s searches report, so $0.32$ is not far
from the truth of this argument.

**Where Q* is applied.** Lemma 4.13 (lines 832–835) and Lemma 4.14 (lines 870–872) apply
Proposition 4.5 with $d=d' \le 3\cdot10^{-6}$, respectively $d=\delta=10^{-5}$, and
$\theta_1=10^{-5}$. Both are within its hypotheses $d,\theta_1 \le 10^{-5}$. For
$\theta_e>\theta_1$ they fall back to Lemma 4.8(a); the needed inequality
$\theta_1(2-\theta_1)/40=4.999975\cdot10^{-7} \ge Q_*\theta_{\max}(2-\theta_{\max})/4=4.7999928\cdot10^{-7}$
holds. A square–side pair whose rectangle $R(X,S_0)$ stands on a side other than the one
it is adjacent to in $G_h$ is covered: its distance to $S_0$ is still less than $d$, and
$\theta(X,S_0)=a(X)$.

## 3. The Overlap Bound

### Lemma 4.9, 13 by Hand

Lemma 4.9 is at lines 611–678. Every relevant edge has a square member whose centre is
within $\rho_1=\sqrt{(d+\tfrac{\sqrt2}2)^2+\tfrac14}$ of $p$: for two squares $p$ is
within $\sqrt{(\Lambda/2)^2+\tfrac14}$ of the nearer centre, and
$\Lambda/2 \le d+\tfrac{\sqrt2}2$.

Part (a). The edges at one centre point into an arc of half-width $\arcsin(1/(2r))$. The
law of cosines on $[1,\Lambda]^2$ has its maximum $1-1/(2\Lambda^2)$ at the corner
$(\Lambda,\Lambda)$, by convexity in each variable.
A side direction is more than $\arccos(d+\tfrac{\sqrt2}2-\tfrac12)=78.04^\circ$ from
every centre direction.
This gives $D(r)=1+\lfloor 2\arcsin(1/(2r))/\gamma_0\rfloor \le 5$.

Part (b). $f$ is increasing in each radius below 1, which gives the class radii $R_m$. A
finite check written here enumerated all $(m_1,\dots,m_n)\in\{2,3,4,5\}^n$, $n \le 5$,
under $\sum\gamma(m_i,m_{i+1}) \le 2\pi$ for $n \ge 3$ and $\sum m_i \le 10$ for
$n \le 2$. It found a maximum sum of 14, attained only by rotations of $(5,2,5,2)$
($358.919^\circ$). Every sequence with sum at least 15 fails by at least $25.942^\circ$.

Part (c). With $\gamma(5,5)=165.6262^\circ$, the law of sines gives
$\psi=7.18688^\circ<7.19^\circ$, and each of the two remaining arcs is shorter than
$55.780^\circ<2\gamma_0=82.813^\circ$. So $\deg(c_1) \le 4$, and the count is at most
13\. The values $\gamma_0=41.40656^\circ$, $\rho_1=0.8661071$, $R_3=0.7559748$,
$R_4=0.5657094$, $R_5=0.5039594$ and $\gamma(2,2)=70.5211^\circ$ all match the text.

### Lemma 4.10, 9 with the Computer: the Reduction

Lemma 4.10 is at lines 685–748. Fix $d=10^{-4}$, which is legitimate because $R_e$ does
not depend on $d$, and put $p=0$. Let $I$ be all centres within $\rho_1$ of $p$. They
satisfy $|c|>\tfrac12$, since $p$ is uncovered and every square contains the closed disc
of radius $\tfrac12$ about its centre, and $n=|I| \le 5$, since two of them subtend at
least $\gamma(2,2)>70.52^\circ$. Each relevant edge then falls into exactly one of three
classes.

1. **An edge between two centres of $I$.** These are at most $E_{II}$, the number of
   pairs closer than $\Lambda$.
2. **An edge between $c_i\in I$ and a side.** There is at most one per centre, since
   $\sqrt2<k-2d$, so these are at most $W_I$.
3. **An edge between $c_i$ and a square with centre $x\notin I$.** Such an $x$ has
   $|x|>\rho_1$, $1 \le |x-c_i|<\Lambda$, $p\in R(c_i,x)$ and $|x-c_j| \ge 1$ for all
   $j\ne i$. Two such $x$ are at least 1 apart, so their directions from $c_i$ differ by
   at least $\gamma_0$, and there are at most $D_i^*(I)$ of them.

Hence the number of relevant edges is at most $U(I)$. The bound never uses the graph
$G$, so it covers all pairs, as Remark 4.11 says.

**The side case.** All relevant square–side rectangles stand on one side $\sigma$. On
opposite sides they would force $k<2d+\sqrt2$. On adjacent sides the computation on line
711 was redone with the bottom and the left side.
With $\sigma$ the bottom, $|c_x-c'_x| \le \tfrac12$, since
$c_x \in [\tfrac12, c'_x+\tfrac12]$ and $c'_x \in [\tfrac12, d+\tfrac{\sqrt2}2)$; with
$\sigma$ the left side, symmetrically $|c_y-c'_y| \le \tfrac12$. So
$|c-c'|^2 \le \tfrac12<1$, which is impossible.

The rectangle $R(P,\sigma)$ contains $p$ exactly when $|c_x| \le \tfrac12$ and
$c_y \ge 0$, in the frame where $\sigma$ is $y=-h$, and the square is within $d$ of
$\sigma$ only if $c_y+h<d+\tfrac{\sqrt2}2$. Those are the conditions $W_I$ counts.
The other sides only add constraints, so dropping them is conservative.
A configuration with no possible side edge is a rotated configuration of the side-free
case. The corners therefore need nothing beyond the one-side model.

**What the programs decide is exactly what the proof needs.**

- **Centre radii.** $[\tfrac12,\rho_1]$ is covered by the float $\rho_1$, which is
  $6.5\cdot10^{-17}$ above the exact value.
- **Outer radii.** $[1,\Lambda)$ is covered by six radial pieces ending at the float
  $\Lambda$, $8.6\cdot10^{-17}$ above the exact value.
- **The height $h$.** $[0,d+\tfrac{\sqrt2}2)$ is covered by a float upper end
  $3.7\cdot10^{-17}$ above the exact value.
  These three margins were computed here at 60 digits.
- **Direction cells.** The 1,440 float cells have 264 one-ulp gaps (also counted here).
  `verify_leaves2.py` closes them by taking cell $k$ as
  $[\phi_k^{\rm lo},\max(\phi_k^{\rm hi},\phi_{k+1}^{\rm lo})]$, and it extends every
  interval that ends at $\widetilde{2\pi}$ (which is $2.449\cdot10^{-16}$ below $2\pi$)
  to the exact $2\pi$ in Arb.
- **The angle arc $(\widetilde{2\pi},2\pi]$, without a side.** It holds no admissible
  configuration: such a centre is within $\rho_1-\tfrac12<1$ of $c_1$.
- **The same arc, with a side.** If only $\vartheta_n$ lies in the arc, the
  configuration with $\vartheta_n$ moved to $\widetilde{2\pi}$ is ordered and lies in a
  recorded box whose $\vartheta_n$-interval ends at $\widetilde{2\pi}$. That box is
  extended. If two angles lie in the arc, the configuration is infeasible.
  The preprint states the extension but not this argument (RF-3).
- **The point count.** `max_points` (`bnb.py` lines 99–123) runs a greedy count from the
  start of each maximal run of allowed cells, with a closing test against
  $\text{first}+2\pi-\gamma_0$. The rotation argument of lines 716–718 is correct, and
  the full circle gives $\lfloor 2\pi/\gamma_0\rfloor=8$.
- **The separation.** $\gamma_0-10^{-12}$ is $1.0\cdot10^{-12}$ below the exact
  $\gamma_0$.

### The Programs’ Trust Boundaries

| Program | Decides | In what arithmetic | Assumes or shares |
| --- | --- | --- | --- |
| `bnb.py`, `bnb_wall.py` | The search: which boxes to record and how to split | float64, with a constraint violated only by more than $10^{-9}$ and cosine bounds widened by $10^{-15}$ | Not relied on for any label. It supplies the box lists, and the verifier and `coverage_check.py` import its grid, prefilter mask, `max_points`, split rule and constants |
| `verify_leaves.py` | `certified_violation` (a cell and radial piece is discarded only if, on each of up to 16 sub-pieces, one constraint fails for the whole box), `check_inf`, `check_nowall` | Arb balls through python-flint, 96 bits; $\Lambda$, $\rho_1^2$ and $d+\tfrac{\sqrt2}2$ in Arb | Its own `rig_bound` is superseded (`SUPERSEDED.md`); only the three routines are used |
| `verify_leaves2.py` (the certificate) | Each recorded box: infeasible, or no side pair, or $E_{II}+W_I+\sum D_i^*\le 9$, sub-bisecting up to 4,096 pieces | $E_{II}$, $W_I$ and every cell discard in Arb. The prefilter mask is float but only proposes cells, so a float error can only keep a cell. The final count is `max_points` in float with $\gamma_0-10^{-12}$ and tolerances $10^{-15}$ and $10^{-12}$, against cell-end rounding near $10^{-15}$ | Imports `bnb.py`, `bnb_wall.py` and `verify_leaves.py`. Box end points are taken exactly into Arb |
| `coverage_check.py` | That the recorded boxes and the ordering-pruned boxes tile the initial boxes: tree rebuild by exact JSON match, exact `Fraction` volumes | Exact | Reuses the search’s split rule and initial boxes (it imports them), so it is not independent of the search. It assumes the float domain constants are upper bounds (true, above) and leaves the arc to the verifier |
| `coverage_independent/exact_volume` | Pairwise interior-disjointness and exact volume of the boxes intersected with the ordered region | Exact rationals of the float end points | Does not import the search. Recomputes $\rho_1$ and $d+\tfrac{\sqrt2}2$ by the same float formula, so it shares the domain description |
| `coverage_independent/recursive_cover` | No query box with ordered points escapes the recorded boxes | Float comparisons of end points | As above. Both independent checks were written by AI reviewers (Claude) in separate sessions |

**What any two share.** All of them share the box lists and the domain description.
The search and the verifier share the `bnb` module: the cell grid, `allowed_cells`,
`max_points`, `split` and the constants.
The search and `coverage_check.py` share the split rule.

None of them checks the reduction from the geometric statement to $U(I)$; that is prose,
re-derived above. Coverage has three implementations.
The labelling has one, the Arb re-verification, and the preprint says so (lines
746–747).

**Run here on 22 boxes.** These runs used the retained programs, Python 3.14.7,
python-flint 0.9.0, numpy 2.5.3 and mpmath 1.4.1. The author used Python 3.12.10 with
the same three packages.

- **Sampled boxes.** `verify_leaves2.py` with threshold 9 accepted five boxes from each
  of `bnb_n3`, `bnb_n5` (task 1 of 2), `bnbw_n3` and `bnbw_n5`, with 0 failures.
- **Positive control.** The no-side $n=2$ box (line 24 of `bnb_n2_T9_0of1`) contains the
  slit configuration $c_{1,2}=\pm(\tfrac12+10^{-9},0)$. On it the verifier accepted at
  threshold 9 and refused at threshold 8, with the split cap lowered to 40 for time.
  The checker is therefore not vacuous at the extremal point.
- **Pointwise evaluation of $U(I)$.** A program written here from the statement alone,
  sampling 7,200 directions and 120 outer radii, gives $U=9$ at that slit configuration
  ($1+4+4$) and at most 7 over 1,500 random trial configurations.
- **Inside recorded boxes.** Random points from 84 accepted `closed` boxes (none exist
  in `bnbw_n5`) never exceeded the box’s recorded bound.
  Admissible points are rare in the thin boxes with $n=4,5$, so that sample is weak
  evidence.

## 4. The Closedness Constraint

**Lemma 3.2** (lines 195–204) uses both closedness and integrality: $k$ disjoint closed
intervals of length at least 1 in $[0,k]$ would cover it and disconnect it.
For non-integer $k$ the argument would give $\lfloor k\rfloor$, not $k-1$.

**Lemma 3.4** (lines 219–239). The long chords number at most $k-1$, each shorter than
$\sec\alpha$, which gives the inequality strictly.
The short-chord set $\Phi(S)$ is two intervals of length $\sin a\cos a$ on which the
chord grows linearly from 0 to 1. Both parts check.

**Remark 7.1** (lines 1130–1140) lists where closedness enters.
The list is correct but incomplete.
Disjointness as closed sets is also used in these places:

- **Lemma 4.12(a).** $G(y_Z)>1$ strictly.
- **Lemma 5.3.** $q\notin X$, and $X$ and $X'$ are separated by a line that is not
  horizontal.
- **Lemma 5.4.** Disjoint chords at one height.
- **Section 6.** Disjoint vertical chords bound the multiplicity of the sets
  $G_Z^{(s)}$.
- **Lemmas 4.13 and 4.14.** Disjoint gap regions for different pairs.

All of these hold under the standing hypothesis, so nothing breaks (RF-4). The
integrality list is complete.
Integrality enters through Lemma 3.2, and through the reflection $y\mapsto k-y$, which
preserves both distance to an integer and the set $H$ of Section 6.

## 5. Height Quantization Across Scales

**Definition 5.1 and its closedness in $s$** (lines 881–893) were re-derived.
The waste of $\sigma^s_x$ is continuous in $s$, and meeting a tilted square is the
closed condition $s+2 \ge b_X$. So $T^*(x)$ is attained, and
$\{x:T^*(x) \le s\}=\mathrm{NR}_s$ is a finite union of intervals.
$T^*$ is therefore Borel and both Tonelli exchanges (lines 1099–1111) are legitimate.

**Lemma 5.2** (lines 899–921). The squares below $Z$ at $x$ have chords in
$[1,\sec\alpha]$ that fill $[0,\beta)$ up to waste less than $\delta$, so
$\beta\in[n,n+1.0159\cdot10^{-5})$. The ramps then lie within $1.07911\cdot10^{-5}<w_0$
of integers. Also $(\sec x-1)/x^2=0.5000002$ at $10^{-3}$.

**Lemma 5.3** (lines 929–976). All three cases were re-derived: the bound on
$w_*\sin a'$, the contradiction $l'(h)<l'(y_q) \le x=r(h)$ in Case 3, and the side of
$p$ from which the free segment leaves $X$ for $u=\pm1$.

**Lemma 5.4** (lines 978–1022). The middle bands of $\mathcal X_{\rm L}$ (and of
$\mathcal X_{\rm R}$) have disjoint interiors because each chord there contains $m_1$
(respectively $m_0$). The covering case $X'=Z$ uses the fact that the left end of $Z$
ends at $m_0$. The bound computes to $|B_Z| \le 0.5000174$, and
$|G_Z| \ge 0.4999819>g_0=0.49998$.

**Section 6, kind (iii)** (lines 1062–1086). Every $Z\in\mathcal Z(s)$ has
$a(Z)<\alpha'((1-\varepsilon)s)<\alpha(s)$, since $C'(1-\varepsilon)=2.8228>C$. A rigid
point of $G_Z^{(s)}$ satisfying (i) would put a ramp point of $Z$ that lies in $H$
within $w_0$ of an integer, which is impossible.
So $G_Z^{(s)}\subset\mathrm{NR}_s$. The multiplicity bound $\varepsilon s+2.01$ uses
vertical extent less than $1.0001$.

**The cost of non-rigid columns** (lines 1088–1112). Type (W) charges vertical waste on
the disjoint segments $\sigma^{T^*}$ and $\tilde\sigma^{\tilde T^*}$. Type (I) is Lemma
4.14 with $\bar y_x=T^*(x)+2 \le k/2-1$ and $\bar\beta=\alpha(y_0)$. The bound
$\alpha(\tau) \ge \int_\tau^{y_1}ds/(Cs^2)$ and the interchange
$\int_y^{y/(1-\varepsilon)}ds/(s(\varepsilon s+2.01)) \ge 1/((1+2.01/(\varepsilon y_0))y)$
both check, and $[y,y/(1-\varepsilon)]\subset[y_0,y_1]$ holds because
$H_b\subset[y_0,(1-\varepsilon)y_1]$.

**The reflection** (lines 1024–1029, 1042) is valid because $k$ is an integer.
It maps closed packings to closed packings, $H_b$ onto $H_t$, and near-integer heights
to near-integer heights.

**Lemma 4.12** (slits, lines 762–797), **Lemma 4.13** (lines 799–848) and **Lemma 4.14**
(lines 850–875) were re-derived.

- **Lemma 4.12(a).** Two short gaps of the same pair lie in one component, by the middle
  chord of an intervening square.
- **Lemma 4.13.** The pairs split at gap $d'=\theta_{\max}$. The far part costs at most
  $s_e^f$. The close part is bounded by Cauchy–Schwarz against $s_e^c$ and $f_e$, with
  $\sum f_e \le K_w^*W$ from Lemma 4.10, and $A\sqrt{(W-x)W}+x$ decreases for $A \ge 2$.
- **Lemma 4.14.** No pair is used both from the bottom and from the top, because no
  square meets both strips.

## 6. The Numbers

Computed here by `ryu_constants.py`, a program written by this lane in `mpmath` at 50
digits, not `code/verify_v10.py`.

- **Inputs taken from the preprint:** $d=10^{-4}$, $Q_*=0.32$, $K_w^*=9$ or $K_w=13$,
  $C=2$, $C'=2\sqrt2$, $\delta=10^{-5}$, $\varepsilon=2\cdot10^{-3}$,
  $\omega_0=2\cdot10^{-4}$, $w_0=1.08\cdot10^{-5}$, $k_2=10^{13}$, $y_0=\sqrt k/4$,
  $\theta_{\max} \le 3\cdot10^{-6}$, and the rounded value $g_0=0.49998$ at which the
  bracket is evaluated.
- **Derived:** everything else.

| Quantity | Computed here | Preprint |
| --- | --- | --- |
| $A=4\sqrt{9/0.32}/(2-3\cdot10^{-6})$ | $10.6066176$ | $<10.6067$ |
| $g_0$ from Lemma 5.4 | $0.4999819$ | $>0.49998$ |
| $1/(\omega_0y_0)$, $2.01/(\varepsilon y_0)$, $\alpha(y_0)/\delta$ at $k_2$ | $0.0063246$, $0.0012712$, $0.0632456$ | $\le$ $6.33\cdot10^{-3}$, $1.272\cdot10^{-3}$, $0.0633$ |
| Bracket, exact $A$ / with $A=10.6067$ | $30.145878$ / $30.146111$ | $30.1462\ldots<30.147$ |
| $(1-\omega_0)(1-2w_0)$ | $0.9997784$ | $\ge 0.99977$ |
| $2\log(2(1-\varepsilon))+2\log\frac{1-6/k_2}{1+8/\sqrt{k_2}}$ | $1.3822853$ | $\ge 1.38228$ |
| Offset $0.99977\cdot1.38228-1.00002$ | $0.3819421$ | $\ge 0.3819$ |
| $\int_H\eta\,dy/d(y)$ bound | $1.00002$ | $1.00002$ |
| Slope $0.99977/30.147$ | $0.0331632$ | $>0.0331$ |
| $0.033\log(k_2-1)$ | $0.98781$ | $<0.99$ |
| $F(k)>1$ from | $\log k>29.7719$ | $29.772$ |
| $\inf_k\max(1,F)/\log k$ | $0.0331632$ (limit) | $0.033163$ |
| Threshold for $c=4$ | $\log k>120.23375$ | $120.24$ |
| $A$ with $K_w=13$; bracket | $12.7475679$; $36.211446$ | $<12.7476$; $<36.212$ |
| Slope with $K_w=13$; $0.027\log(k_2-1)$ | $0.0276088$; $0.80821$ | $\kappa=0.027$ |

Every stated constant holds.
$\kappa=0.033$ holds for every $k \ge 2$: below $k_2$ by Corollary 3.3, and from $k_2$
by the slope $0.0331632$ with a positive offset.
The same holds for $0.027$ without Lemma 4.10. Several margins are thin but correct:
$\psi$ by $0.003^\circ$, $\chi_*$ by $6\cdot10^{-6}$, the offset $1.38228$ by
$5\cdot10^{-6}$ (RF-6).

## 7. Its Place in the Record

**Against Roth and Vaughan** (`asymptotic-waste-bounds.yaml`, `lower_bounds`). The
preprint’s quantity is a one-sided limit of theirs.
For $x<k$ close to $k$, a packing in side $x$ holds at most $M(k)$ squares, and exactly
$M(k)$ once $x \ge s(M(k))$, so $w(x)=x^2-M(k)$ there.
Hence $k^2-M(k)=\lim_{x\to k^-}w(x)$, and the claim says
$w(x) \ge 0.033\log k-(k^2-x^2)$ for every $x<k$.

The two results are complementary, and neither implies the other.

- **What Roth and Vaughan give near integers from below.** Their bound
  $w(x)\gg(\lVert x\rVert x)^{1/2}$ tends to 0 as $x\to k^-$.
- **What they give at $x=k$.** Their side condition fails, and their own remark gives
  $\sup|\mathcal A|=k^2$, so $w(k)=0$ for packings with disjoint interiors.
- **What the claim gives away from integers.** Nothing.
  It does not reach the $\Omega(\sqrt x)$ that Roth and Vaughan give at half-integers.
- **The rows to keep.** The register’s “the only lower bound is $\Omega(\sqrt x)$ at
  worst-case $x$” and its `constant: NONE` both stand.
  The preprint makes explicit the constant of Roth and Vaughan’s fundamental lemma, not
  the constant of their theorem.

**Against T-081** (Evan Daniel’s reported $s(k^2-4)=k$ for $k \ge 5$, `V0/C1`, scope
$k=5$ to 18). T-081 is the statement $c^*(k) \ge 4$ for $k \ge 5$. If it holds, it
contains the preprint’s $c=4$ consequence, which needs $\log k>120.23$, so for $c \le 4$
the preprint adds nothing to it.

T-081 says nothing about $c^*(k)\to\infty$, which is the preprint’s new content.
Conversely, the preprint says nothing about any $k$ within T-081’s scope or within
computational reach, as its Remark 7.4 says.
The two share Lemma 2.1’s reduction $s(k^2-c)=k \iff c<k^2-M(k)$, and nothing else.

**The citations.** The preprint describes Daniel’s announcement as computer-assisted and
unrefereed, which agrees with T-081’s record.
It cites Daniel’s notes at commit `7ff3b21` for $c^*$ and for the openness of
$c^*(k)\to\infty$. That commit is retained here as `evand-square-packing-2026-10-04`,
and its `s12/search/FRIEDMAN.md` says “`A` is open, and so is `c*(k) → ∞`”.

## 8. Credit and Status

The preprint (line 22), the source README and `.zenodo.json` (`"Ryu, Sungjoon"`) all
name Sungjoon Ryu as the sole author.
The preprint’s “Use of AI” (lines 1213–1216) says Claude was used extensively in
developing the arguments, in writing the text and the programs (including the
computation for Lemma 4.10), and in checking them.
It says Claude is not an author, that the author takes full responsibility, and that the
paper has not been refereed.
The README says the same.

`reviews/REVIEWS.md` lists nineteen review rows from version 7 to version 10. All are by
AI reviewers, and it states their shared-family limitation and the absence of a human
referee. The two “independent” coverage checks were written by Claude sessions, as their
README says. The packet README reports all of this faithfully.
Its first sentence writes the name family-first, “Ryu Sungjoon” (RF-7).

The result is credited to its author, after Roth and Vaughan, whose rectangle and
fundamental lemma it sharpens, and to Daniel, whose notes defined $c^*$.

## 9. Findings

None is blocking.

| Id | Pinpoint | Blocking | What it is | What would resolve it |
| --- | --- | --- | --- | --- |
| RF-1 | Lemma 4.10, lines 725–728, 746–747; `verify_leaves2.py` | No | The labels of the 78,673 boxes rest on one implementation, which shares `max_points`, the cell grid, the prefilter and the split rule with the search. $\kappa=0.033$ and the formula for $k \ge 10^{13}$ depend on it; $\kappa=0.027$ does not. This lane ran 22 boxes | The complete replay of `verify_leaves2.py` (the other lane), then an independent implementation of the labelling, ideally with an exact point count |
| RF-2 | `bnb.py` `max_points`, lines 99–123; Lemma 4.10, lines 731–733 | No | The final count of points in the union of arcs is float64. It is protected by $\gamma_0-10^{-12}$ and tolerances of $10^{-15}$ and $10^{-12}$ against rounding of the cell ends near $10^{-15}$, not by ball arithmetic | Do the count in exact rationals on the closed cell ends, or state the float error bound in the text |
| RF-3 | Lemma 4.10, lines 729–731 | No | With a side, why a configuration with $\vartheta_n\in(\widetilde{2\pi},2\pi]$ lies in an extended box is not argued. It does: move $\vartheta_n$ to $\widetilde{2\pi}$; two angles in the arc are infeasible | One sentence in the proof |
| RF-4 | Remark 7.1, lines 1130–1136 | No | The list of uses of closedness omits Lemmas 4.12(a), 4.13, 4.14, 5.3 and 5.4 and the multiplicity step of Section 6. All hold under the standing hypothesis | Extend the list |
| RF-5 | Section 4, line 243; Lemma 4.10, line 710 | No | The section’s standing $k \ge 4$ and the proof’s “$k \ge 2$” disagree; the main proof uses $k \ge 10^{13}$ only | Wording |
| RF-6 | Lemma 4.9(c), line 667; Prop. 4.5(g), line 495; Section 6, line 1048 | No | Margins are thin: $\psi=7.18688^\circ$ against $7.19^\circ$, $\chi_*=0.2929443$ against $0.29295$, offset $1.3822853$ against $1.38228$. All hold at 50 digits here | None needed; a note for later edits |
| RF-7 | Packet `README.md`, first line | No | “Ryu Sungjoon” where the preprint, the source README and `.zenodo.json` write “Sungjoon Ryu” (Zenodo as “Ryu, Sungjoon”) | Use one form in the record |
| RF-8 | `coverage_check.py`; `code/coverage_independent/` | No | One coverage check reuses the search’s split rule. The two independent ones share only the box lists and the domain formula with it, but all three come from the same AI family | The replay should run at least one independent coverage check beside the labelling |
| RF-9 | Remarks 4.11 and 7.2; `check_hand9_indep.py` | No | Unchecked here and not used by the theorem: the sharpness of 9 with real squares, and the dichotomy of Remark 7.2 with its constants | None for the claim |

## 10. What Was Not Checked

- The Arb labelling of all but 22 of the 78,673 boxes, the author’s coverage outputs and
  logs, `make_stats_v10.py` and `verify_v10.py`. These belong to the replay lane, whose
  results this lane has not seen.
- The coverage checks themselves, except by reading `coverage_check.py`, the README of
  `coverage_independent/`, and the parts of the two independent programs that set their
  domain.
- Remark 7.2, Remark 4.11’s 80-digit sharpness check, the searches under
  `code/experiments/`, and Lemma 4.8(b) with Fodor’s and Oler’s theorems, which the
  preprint does not use for the theorem.
- The literature claims of the introduction beyond Roth and Vaughan and Daniel’s notes,
  and the claim that no earlier proof that $c^*(k)$ is unbounded exists.
- The Zenodo records, which this session cannot reach.

**A note on method.** The repository’s `uv run --frozen` from `packing/` failed here
because the `vendor/kpress` submodule is not checked out in this worktree.
Before failing, it created the git-ignored `packing/.venv`, which was removed at once;
nothing tracked changed.
All computation ran in a scratch virtual environment, under `nice -n 10`, on one thread,
each run under ten CPU minutes.

## 11. Verdict

**`accepted`.** No blocking defect is open.

- **What was re-derived.** The argument from closed packings to
  $k^2-M(k) \ge (0.99977\log k+0.3819)/30.147$, and every constant stated for it, was
  re-derived here without finding an error.
  So were the reduction of Lemma 4.10 to $U(I)$ and the match between the programs’
  domain and that reduction.
- **What rests on unreplayed computation.** The constant $0.033$ and the formula for
  $k \ge 10^{13}$ also rest on the Arb labelling of Lemma 4.10. This review has read
  that labelling and run it on 22 boxes; it has not replayed it.
  They stand or fall with the complete replay (RF-1).
- **What rests on the prose alone.** The qualitative statement, $c^*(k)\to\infty$ with
  $\kappa=0.027$ from the analytic Lemma 4.9, needs no computation beyond the constants
  recomputed here.
- **The limit of this verdict.** It is one AI reviewer’s reading.
  It is not a referee’s acceptance, and no human has checked the argument.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
