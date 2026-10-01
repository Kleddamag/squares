---
title: "H-259 \u2014 n17 mixed-capacity cover and exact census"
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-259
  kind: hypothesis
  claim: At side cap1169/250, a closed5by5 centre grid has16 boundary cells of capacity1 and9 interior
    cells of capacity2; its complete raw n17 occupancy census is smaller than the valid6by6 capacity-one
    baseline.
  lane: proof
  derived_from:
  - X-048
  criterion:
    shape: determination
    metric: Exact finite cell-capacity proof plus coefficient ofx17 in(1+x)^16(1+x+x^2)^9 compared with
      binomial(36,17).
    direction: Confirm only after independent support-inequality, closed-cover, seam-ownership and capacity
      review; exact DP and independent binomial audit agree for complete coefficient lists and total assignments;
      target count is strictly smaller than baseline; synthetic controls and resource limits hold.
    threshold: Exact count agreement and strict integer reduction versus binomial(36,17); no geometry
      exclusion or optimality inference.
  instrument: devtools.count_cell_occupancies with independent devtools.audit_cell_occupancies; reviewed
    exact geometric capacity lemmas.
  instrument_ready: true
  regime: Fixedcap1169/250, centrebox[1/2,U-1/2]^2,5equalcellsperaxis withside919/1250;16capacity1 and9capacity2
    cells. Baseline36capacity1 cells. No symmetry quotient or unproved compatibility restrictions.
  instance:
    axis: n
    point: 17
  priority: 1
  cost_estimate: One15minute controlled implementation/review slice; one30second combined counting/audit
    target, oneworker,1MiB per output.
  prereqs:
  - think-70sf
  replication: false
  registered: '2026-10-01'
  notes: Analytic proposal already establishes the total-state upperbound2^16*3^9<binomial(36,17). Exact
    target coefficient is not observed before freeze. This measures raw occupancy enumeration only, not
    orientations, labels, geometric realizability, exclusion costs or global capture.
---
# H-259: An n17 Mixed-Capacity Cover

Registered on October1 by13:49UTC before coefficient evaluation.
The
[geometric review](../../../docs/project/reviews/review-2026-10-01-n17-mixed-capacity-cover.md)
fixes the boundary-cell support lemma, complete closed cover, seam ownership and
capacity-two interior split.
The cap is $U=1169/250=4.676$; its centre box has side $U-1=919/250$. Five equal
divisions give cell side $919/1250<3/4$.

The16boundary cells have capacity one, by exact containment and support inequalities.
Each of the9interior cells has capacity two because its two half-rectangles each have
diameter strictly below one.
Assign a centre on a seam to the lexicographically least containing closed cell.
This makes the occupancy vector unique without dropping boundary configurations.
The6by6 baseline also has strict diameter below one in every cell.
All orientations are included; square labels and symmetry quotients are absent.

The retained input contract orders boundary cells lexicographically first, followed by
interior cells lexicographically.
Seam ownership still uses spatial lexicographic indices; the grouped capacity list is an
explicit bijection, not row-major grid order.

The exact target is the coefficient of $x^{17}$ in $(1+x)^{16}(1+x+x^2)^9$. The baseline
is $\binom{36}{17}$. The proposal already bounds all mixed-cell states by $2^{16}3^9$,
below that baseline; this prior expectation is disclosed.
The selected computation quantifies the exact fixed-sum census and independently checks
the implementation. It is not a blind search for a favourable grid or threshold.

Freeze proof contract, producer and independent auditor after synthetic controls.
Use one worker, a30second combined process ceiling and1MiB per output.
Controls include empty/impossible inputs, a small brute-force census, coefficient
mutation, permutations, invalid types and nonnegative-capacity guards.
The independent checker uses a binomial sum for capacities zero, one and two, without
importing the producer.
No target evaluation or exact coefficient has occurred at registration.

Accept only complete exact agreement and the independently reviewed capacity proof.
A count mismatch or invalid proof premise leaves the cover unaccepted.
Even success leaves all compatible poses, orientation domains, geometrically impossible
occupancy vectors and global exclusions unresolved.
It is a census reduction, not a proof that seventeen squares cannot fit below the
endpoint.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
