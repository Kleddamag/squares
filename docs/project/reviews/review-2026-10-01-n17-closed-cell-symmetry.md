# n17 Symmetry of Closed-Cell Assignment States

## Registered Scope and Acceptance Criterion

**Registered:** October 1, 2026, 14:07 UTC, before the symmetry counts.
**Scope:** a bounded continuation of the
[mixed-capacity cover](review-2026-10-01-n17-mixed-capacity-cover.md) under
[X-048 R2](../../../packing/campaign/explorations/X-048-n17-optimality-after-n11.md).
The coordinator owns the separate H260 registration, execution and acceptance.
This review fixes the geometric interpretation, eight group actions and counting
polynomials before any new target arithmetic.
The previous H259 census is unchanged.

Use the same rational cap $U=1169/250$, closed centre box $[1/2,U-1/2]^2$, cell width
$a=919/1250$, and five-by-five grid.
Its 16 boundary cells have capacity one; its nine interior cells have capacity two.
All orientations remain admissible.
Count orbits of integer occupancy vectors of total 17 under the eight physical
symmetries of the container.
No packing feasibility test, orientation search, endpoint evaluation or H258 retry is
part of this round.

Acceptance requires the following exact checks, with integer arithmetic and a separate
audit:

- Construct all eight distinct cell permutations, verify their group action and capacity
  preservation, and retain their complete cycle manifests as multisets of cycle length
  and capacity.
- Compute the coefficient of degree 17 in each of the eight frozen fixed-state
  polynomials below; independently reconstruct all eight counts.
- Match the identity count to the accepted H259 raw census.
- Require the sum of the eight fixed counts to be divisible by eight and the resulting
  orbit count to be strictly smaller than the raw census.
  No additional reduction factor is required.
- Retain the exact sum, quotient, comparison and input manifests within the
  coordinator’s resource limits.
  A timeout, malformed record or failed identity match leaves the proposed discriminator
  unresolved.

The instrument must be ready by 14:15 UTC and its target execution and review complete
by 14:25 UTC. The session’s 14:30 UTC finalization remains unchanged.
No numerical count is reported at this registration checkpoint.

## Closed Assignments Supply the Symmetry Coverage

Index cells by $(i,j)\in\lbrace0,1,2,3,4\rbrace^2$, with the first index increasing in
the $x$ direction and the second in the $y$ direction.
Write

$$
C_{ij}=[1/2+ia,1/2+(i+1)a]\times[1/2+ja,1/2+(j+1)a].
$$

The capacity $c_{ij}$ is one when $i$ or $j$ is zero or four, and two otherwise.
The previous cover proves these capacities for the closed cells themselves, including
all seams. Define the finite state space

$$
V=\left\lbrace v\in\mathbb Z^{25}:0\le v_{ij}\le c_{ij},\quad
\sum_{i,j}v_{ij}=17\right\rbrace.
$$

For each state $v$, its geometric case domain consists of packings for which there
**exists** an assignment of each centre to a containing closed cell, with occupancy
vector $v$. A centre on a seam may admit several assignments.
No lexicographic ownership restriction belongs to this case domain.

Every packing in the cap has at least one such assignment because the cells cover the
complete centre box.
The capacity proofs guarantee that every assignment has its occupancy in $V$. A physical
symmetry $g$ maps each cell to another cell of the same capacity.
Applying $g$ to a packing and its assignment therefore gives a valid assignment with
occupancy $gv$. In particular, the image of the case domain of $v$ is the case domain of
$gv$; applying $g^{-1}$ proves equality, not merely inclusion.

Choose one representative of every orbit in $V$. Every physical packing is congruent, by
a container symmetry, to a packing in at least one representative’s closed-assignment
case domain.
Thus excluding all such representative domains would exclude all packings at
this cap. The count below only measures the number of necessary occupancy cases; it
performs none of those exclusions.

The lexicographically least seam owner used to make H259 assignments deterministic is
not equivariant. For example, reflect a centre on the first interior vertical seam and
strictly inside a horizontal cell.
The original lexicographic column is zero; its reflected column is four.
At the reflected seam, lexicographic ownership instead chooses column three.
Hence a symmetry may carry a lex-owned assignment to a valid closed assignment that is
not lex-owned. Future symmetry-reduced leaves must retain the existential closed-cell
domains above; adding the original lexicographic exclusions would invalidate this
coverage argument.

## Future Use Below the Endpoint

The accepted
[H256 endpoint](../../../packing/campaign/hypotheses/H-256-n17-exact-endpoint-feasibility.md)
has side $S_{\ast}<U$ and therefore belongs to the present cover.
Consequently, excluding every occupancy case at $U$ is impossible: at least one case
contains that certified packing.
The registered H260 experiment only counts orbits and does not attempt such an
exclusion.

For a future lower-bound proof, retain the actual container side $S$ in each geometric
case and impose $S<S_{\ast}$, or select a separately declared rational cap below
$S_{\ast}$. A bound at one smaller rational cap does not by itself establish exact
optimality at $S_{\ast}$. Using the fixed $U$ grid remains sound: embed the actual
container concentrically as

$$
\left[\frac{U-S}{2},\frac{U+S}{2}\right]^2.
$$

Its centres lie in the covered centre box, and every physical symmetry about the centre
of the $U$ container preserves this smaller container as well as the grid.
The stronger containment inequalities for the actual side must remain in every case.
An uncentred embedding $[0,S]^2$ is also contained in the cap, but its side constraints
are not preserved by the fixed grid’s rotations about $(U/2,U/2)$ when $S<U$. The
symmetry transport above must not be applied to that uncentred domain unchanged.

This clarification concerns future geometric use and changes none of H260’s registered
cap, states, fixed polynomials or arithmetic acceptance conditions.

## The Eight Frozen Actions and Their Cycles

Let composition act from right to left and define

$$
R(i,j)=(j,4-i),\qquad F(i,j)=(4-i,j).
$$

These are a quarter turn and a reflection of the physical grid.
They satisfy $R^4=F^2=I$ and $FRF=R^{-1}$. Use the frozen action order

$$
I,\ R,\ R^2,\ R^3,\ F,\ RF,\ R^2F,\ R^3F.
$$

The state action is $(gv)_{g(i,j)}=v_{ij}$. Every cycle has a constant capacity.
In the table, a term $m(\ell,c)$ denotes $m$ cell cycles of length $\ell$ and capacity
$c$.

| Actions | Multiplicity | Cycle manifest |
| --- | ---: | --- |
| $I$ | 1 | $16(1,1)+9(1,2)$ |
| $R,R^3$ | 2 | $4(4,1)+2(4,2)+1(1,2)$ |
| $R^2$ | 1 | $8(2,1)+4(2,2)+1(1,2)$ |
| $F,RF,R^2F,R^3F$ | 4 | $2(1,1)+3(1,2)+7(2,1)+3(2,2)$ |

For either nontrivial rotation, the central cell is the only fixed cell.
A quarter turn puts the other 16 boundary cells into four cycles and the other eight
interior cells into two cycles, all of length four.
A half turn pairs those cells instead.
Each reflection fixes five cells on its axis: two boundary cells and three interior
cells. The remaining 14 boundary cells and six interior cells form pairs.
This establishes the table for both axial and diagonal reflections.

## Fixed-State Polynomials and Burnside’s Formula

A state fixed by a permutation is constant on each cell cycle.
If a cycle has length $\ell$ and capacity $c$, its common occupancy $q$ may be any
integer from zero to $c$ and contributes total occupancy $\ell q$. Its generating factor
is therefore

$$
1+x^\ell+\cdots+x^{c\ell}.
$$

Independent choices on disjoint cycles multiply.
Let $N_g$ be the coefficient of $x^{17}$ in the product of these factors for $g$. The
complete frozen polynomials are

$$
\begin{aligned}
N_I&=\operatorname{coeff}_{x^{17}}\thinspace(1+x)^{16}(1+x+x^2)^9,\cr
N_R=N_{R^3}&=\operatorname{coeff}_{x^{17}}\thinspace(1+x+x^2)(1+x^4)^4(1+x^4+x^8)^2,\cr
N_{R^2}&=\operatorname{coeff}_{x^{17}}\thinspace(1+x+x^2)(1+x^2)^8(1+x^2+x^4)^4,\cr
N_F=N_{RF}=N_{R^2F}=N_{R^3F}
&=\operatorname{coeff}_{x^{17}}\thinspace(1+x)^2(1+x+x^2)^3(1+x^2)^7(1+x^2+x^4)^3.
\end{aligned}
$$

Burnside’s formula gives the exact orbit count

$$
\lvert V/D_4\rvert=
\frac{N_I+N_R+N_{R^2}+N_{R^3}+N_F+N_{RF}+N_{R^2F}+N_{R^3F}}8.
$$

For completeness, count the pairs $(g,v)$ with $gv=v$. Counting first by $g$ gives the
numerator. Within a state orbit, every state has stabilizer size eight divided by the
orbit size, so that orbit contributes exactly eight pairs.
This proves the formula and integrality without assuming that the action is free.

Odd occupancy does not make the rotational fixed counts zero: the central cell can carry
occupancy one while other occupied cycles contribute an even total.
For example, occupancy one in all 16 boundary cells and in the central cell is a
17-occupancy state fixed by every action.
Dividing the raw count by eight would therefore require a false free-action premise.

## Independent Arithmetic Route and Controls

For the quarter turns, reduction modulo four forces the central occupancy to equal one.
For the half turn, parity does the same.
Thus equivalent lower-degree expressions are

$$
N_R=N_{R^3}=\operatorname{coeff}_{y^{4}}\thinspace(1+y)^4(1+y+y^2)^2,
\qquad
N_{R^2}=\operatorname{coeff}_{y^{8}}\thinspace(1+y)^8(1+y+y^2)^4.
$$

For a reflection, define the complete coefficient sequences

$$
A_j=\operatorname{coeff}_{x^{j}}\thinspace(1+x)^2(1+x+x^2)^3,\qquad
B_k=\operatorname{coeff}_{y^{k}}\thinspace(1+y)^7(1+y+y^2)^3.
$$

The fixed cells contribute degree at most eight; the paired cells contribute an even
degree. Consequently,

$$
N_F=N_{RF}=N_{R^2F}=N_{R^3F}
=A_1B_8+A_3B_7+A_5B_6+A_7B_5.
$$

These expressions permit an audit independent of the generic cycle dynamic program.
For an ordinary capacity list with $p$ ones and $q$ twos, its coefficient of degree $k$
is

$$
\sum_{j=0}^{q}\binom qj\binom{p+q-j}{k-2j},
$$

where an out-of-range binomial coefficient is zero.
Choosing the $j$ doubly occupied cells first proves this identity directly.
It supplies all coefficients required by the reduced formulas and also independently
reconstructs the identity count.

Before the target, synthetic controls should cover a small grid whose occupancy states
can be exhaustively listed, a central fixed cell with odd total occupancy, the seam
non-equivariance example, and rejection of corrupted permutations, cycle manifests,
fixed counts or the Burnside denominator.
The producer and auditor must agree on composition order, cell indices and the
distinction between cycles and their member cells.
No target occupancy enumeration is needed.

This quotient removes only duplicate occupancy cases related by physical symmetries.
It leaves geometrically impossible states in the count, does not assign square
identities, and does not measure the cost of a future exclusion for one case.
No local or global optimality claim follows from the arithmetic comparison.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
