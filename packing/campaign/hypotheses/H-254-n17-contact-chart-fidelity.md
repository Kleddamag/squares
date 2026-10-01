---
title: H-254 — exact residual audit of the n17 endpoint contact chart
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-254
  kind: hypothesis
  claim: The proposed three-variable endpoint equality chart, including its explicit reconstruction contacts, describes the fixed retained rational n17 witness within 1e-12, with each selected contact axis separated from its alternatives by at least 1e-6.
  lane: proof
  derived_from: [X-048]
  criterion:
    shape: determination
    metric: Exact rational domain, angle-class, anchor, contact, equation, auxiliary-coordinate and full-centre reconstruction checks, with all source containment and pair separations retained.
    direction: Confirm only when every frozen check passes, the synthetic controls pass and an independent reviewer checks the outputs. Any validly evaluated failed clause rejects this fidelity claim. Timeout or invalid controls is unresolved. Rejection does not refute feasibility, the existence of a different chart, or optimality.
    threshold: 'Residual cap 1/1000000000000; alternative-axis gap at most -1/1000000.'
  instrument: devtools.check_n17_contact_chart, to be implemented and independently reviewed against the contact derivation before any target evaluation.
  instrument_ready: false
  regime: Exact Fraction arithmetic on the unchanged H253 source; no fitting, decimal optimization, search or root solving. Single worker on the measured macOS host.
  instance: {axis: n, point: 17}
  priority: 1
  cost_estimate: One 20-minute instrument/control slice, followed by one target evaluation capped at 90 seconds and 10 MiB output, then independent review.
  prereqs: [think-j516]
  replication: false
  registered: '2026-10-01'
  notes: A fidelity screen at an already feasible relaxed rational witness. It cannot establish an algebraic endpoint, a local minimum, a capture theorem or a global optimum.
---
# H-254: n17 Contact-Chart Fidelity

The
[independent derivation](../../../docs/project/reviews/review-2026-10-01-post-optimality-w3-opening.md#independent-contact-chart-derivation)
identifies the contacts behind the proposed three-variable system.
This screen asks whether those contacts describe the retained witness accurately enough
to justify exact endpoint work.
It is separate from H-027’s local angle-cone question.

## Frozen Inputs and Criteria

Use the exact source, side and source digest fixed by
[H-253](H-253-n17-retained-rational-upper.md).
Map source rows to labels by `[1,5,2,6,3,7,4,8,9,10,11,12,13,14,15,16,17]`. Without
fitting, take $t=\tan(\theta/2)$ from square 9 and $b=\tan(\beta/2)$ as the negative of
square 16’s source half-angle.
Freeze

$$
S\in[4.675,4.676],\qquad t\in[0.36,0.37],\qquad b\in[0.33,0.34].
$$

Require exact common orientations of squares 9 through 14 and exact axis alignment of
squares 1 through 8, 15 and 17. All support signs in the independent derivation must
hold. Evaluate the chart’s $F_1,F_2,F_3,X,Y,A,B$ by exact rational arithmetic.
The following clauses all have to pass:

1. Every declared wall-anchor defect and directed contact gap is in $[0,10^{-12}]$.
2. Each $|F_i|$, $|X-x_{15}|$, $|Y-y_{17}|$, $|A-p\cdot r_{16}|$ and $|B-q\cdot r_{16}|$
   is at most $10^{-12}$.
3. For every selected contact pair, every other distinct unoriented SAT axis has gap at
   most $-10^{-6}$. Deduplicate parallel axes exactly.
   A failure records feature ambiguity; it does not authorize selecting another axis.
4. The explicit contact reconstruction matches all 34 centre coordinates within
   $10^{-12}$, keeping only source slider coordinates $x_6$ and $v\cdot r_{13}$. The
   complete anchor/contact table must be retained and reviewed before execution.
   In particular, square 11 requires its own tangential defining contact; the three
   equations alone do not fix that coordinate.
5. The exact source geometry still satisfies every containment inequality and all 136
   pair separations. This check applies to the source, not the reconstructed approximate
   chart.

## Frozen Reconstruction and Contact Table

For $u=(c,s)$, $v=(-s,c)$, $w=-v$, $p=(d,-e)$, $q=(e,d)$, put $h=(c+s)/2$, $k=(d+e)/2$,
$\alpha=cd-se$, $\gamma=ce+sd$. Let $R(U,V)=(cU-sV,sU+cV)$, $\lambda_6=x_6$, and
$\lambda_{13}=v\cdot r_{13}$, using the source values for both sliders.
The explicit reconstruction is

| ID | Centre |
| --- | --- |
| 1 | $(1/2,1/2)$ |
| 2 | $(3/2,1/2)$ |
| 3 | $(1/2,3/2)$ |
| 4 | $(1/2,S-1/2)$ |
| 5 | $(S-1/2,1/2)$ |
| 6 | $(\lambda_6,1/2)$ |
| 7 | $(S-1/2,3/2)$ |
| 8 | $(S-1/2,S-1/2)$ |
| 9 | $(h,2+h)$ |
| 10 | $R(U_{10},V_{10})$ |
| 11 | $R(U_{11},V_{11})$ |
| 12 | $R(U_{12},V_{12})$ |
| 13 | $R(U_{13},\lambda_{13})$ |
| 14 | $R(U_{14},V_{14})$ |
| 15 | $(X,S-1/2)$ |
| 16 | $(dA+eB,-eA+dB)$ |
| 17 | $(S-1/2,Y)$ |

Here

$$
\begin{aligned}
U_{10}&=3/2+cs+2s,&V_{10}&=c(S-1)-s-1/2,\\
U_{11}&=c+2s+1/2,&V_{11}&=2c+(c^2-s^2)/2-1,\\
U_{12}&=U_{11}+1,&V_{12}&=V_{10}-1,\\
U_{13}&=2c+s+1/2,\\
U_{14}&=U_{13}+1,&V_{14}&=V_{10}-2.
\end{aligned}
$$

Use $X,Y,A,B,F_1,F_2,F_3$ exactly as stated in the linked independent derivation.
These rational formulas remain defined when the closing residuals are nonzero.

The 15 wall anchors are: square 1 left/bottom; 2 bottom; 3 left; 4 left/top; 5
right/bottom; 6 bottom; 7 right; 8 right/top; 9 left; 15 top; 17 right.
The 17 defining directed pair contacts are:

| Pair | Normal | Support Sum |
| --- | --- | --- |
| $1\to2$ | $e_x$ | $1$ |
| $1\to3$ | $e_y$ | $1$ |
| $5\to7$ | $e_y$ | $1$ |
| $3\to9$ | $e_y$ | $h+1/2$ |
| $9\to10$ | $u$ | $1$ |
| $4\to10$ | $w$ | $h+1/2$ |
| $3\to11$ | $u$ | $h+1/2$ |
| $9\to11$ | $w$ | $1$ |
| $11\to12$ | $u$ | $1$ |
| $10\to12$ | $w$ | $1$ |
| $2\to13$ | $u$ | $h+1/2$ |
| $13\to14$ | $u$ | $1$ |
| $12\to14$ | $w$ | $1$ |
| $10\to15$ | $u$ | $h+1/2$ |
| $14\to17$ | $u$ | $h+1/2$ |
| $15\to16$ | $p$ | $k+1/2$ |
| $16\to8$ | $q$ | $k+1/2$ |

The three closing contacts are $14\to7$ along $w$, $16\to17$ along $p$, and $12\to16$
along $u$. On reconstructed centres their directed gaps must equal $F_1,F_2,F_3$,
respectively. Include all 20 selected pairs in clauses 1 and 3. For an alternative
unoriented unit axis $a$, the pair gap is $|a\cdot(r_j-r_i)|-H_i(a)-H_j(a)$; the
selected contact’s gap remains directed.

For fixed side, orientations and sliders, the sequential formulas establish uniqueness
within this equality model.
They do not establish rigidity outside it.
The sliders have a joint domain: selected source-side branches would require
$\lambda_{13}+s\lambda_6\ge c+s/2+1/2$, $\lambda_6\le S-3/2$, and
$\lambda_{13}\le V_{11}-1$. These are useful future slider-certificate obligations, not
added acceptance clauses or an exhaustive feasibility certificate; clause 5 checks the
full source geometry.

## Controls and Run Limits

Before target evaluation, test a synthetic exact rotated contact and an overlapping
pair, axis deduplication and opposite-axis equivalence, sign/domain refusals, and a
deliberately displaced contact whose residual exceeds the frozen cap.
Reconstruction controls must verify the declared equations directly on a synthetic
parameter triple, without claiming the synthetic chart is a feasible packing or a root.
An independent reviewer must compare the implementation with the separately derived
contact table.

Commit the instrument and the complete contact table before target execution.
Use one worker, a 90-second wall ceiling, a 10 MiB output ceiling and a 1 GiB memory cap
where supported; report unsupported memory guards explicitly.
Retain all exact residuals, failures, source identity, Git state, wall/CPU costs and the
command. Do not retry with a changed tolerance or source.

A pass would establish fidelity at this rational witness only.
Exact endpoint admission still requires root isolation, certified feature inequalities,
slider domains and all pair separations at that root.
Local minimality additionally needs necessary inequalities or a capture argument for
slack contacts and split orientations; global optimality needs complete capture.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
