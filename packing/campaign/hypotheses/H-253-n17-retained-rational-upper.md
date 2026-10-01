---
title: H-253 — independent validation of the retained n17 rational upper witness
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-253
  kind: hypothesis
  claim: The retained Kleddamag rational reconstruction contains seventeen unit squares with disjoint interiors in a square of exact side 4675530093604551/1000000000000000.
  lane: proof
  derived_from: [X-048]
  criterion:
    shape: determination
    metric: Exact shape and containment of all 17 squares and all 136 unordered pair separations after lossless conversion to cyclic rational corners.
    direction: Confirm only if both existing local exact checkers accept the identical converted witness, the source checker agrees, fixed controls pass, and independent review finds no blocking defect. A timeout is unresolved; a control failure invalidates the instrument. A rejected witness refutes only these bytes, not Bidwell optimality.
    threshold: '4675530093604551/1000000000000000'
  instrument: devtools.import_half_angle_witness, sqpack.cli.witness verify, devtools.check_rational_witness_independent, and the retained source verify_upper.py; use the frozen commands and caps in Session 165.
  instrument_ready: true
  regime: Exact Fraction arithmetic without tolerances; fixed retained source bytes; single worker on a heavily contended macOS host. Source certificate has already passed its own checker historically; this round adds independent local implementation checks.
  instance: {axis: n, point: 17}
  priority: 1
  cost_estimate: At most 90 seconds per checker or conversion command, 10 minutes for all measurements and controls; no search or candidate tuning.
  prereqs: [think-08sm, think-qc6k]
  replication: false
  registered: '2026-10-01'
  notes: Preregistered before target conversion or target replay. This is a relaxed rational upper witness, not a construction at the algebraic endpoint and not a global lower bound. No new optimum is claimed.
---
# H-253: Independent n17 Upper-Witness Validation

[X-048](../explorations/X-048-n17-optimality-after-n11.md) requires an exact feasible
upper witness before endpoint work.
The September 21 Kleddamag packet already contains a rational reconstruction and a
historical source-checker receipt.
This round tests those fixed bytes using our independently implemented geometry.

The input is
[`upper-packing-certificate.json`](../../resources/web/n17-kleddamag-certified-bound-2026-09-21/kleddamag-17-squares-certified-bound/upper-packing-certificate.json),
retained at baseline `fb0fc2332`. Its SHA-256 at the source-to-local trust boundary is
`24e296f5995abc9424e2d8d39ea0a8e44953b919430a04f006fa84c56fef45f7`. The certificate
fixes rational centres and half-angle parameters.
Conversion must preserve every parameter exactly and emit corners in perimeter order.
Run the source checker with the ordinary interpreter, with PYTHONOPTIMIZE unset and no
-O flag, because its acceptance conditions use Python assertions.
The source verifier’s Cartesian-product vertex order is not perimeter order.

Controls are the existing `grid-n004.yaml` positive and `overlap-negative-control.yaml`
negative, a synthetic rational rotation with half-angle $1/2$, and adapter refusals for
wrong count, wrong side and malformed scalars.
The negative packing must fail both local checkers.
A converted target must pass all unit-edge, orthogonality, parallelogram, containment
and pair-separation checks at zero tolerance.

Freeze the implementation in Git after focused controls and review, before target
conversion. Each command has a 90-second wall ceiling, one worker, a 1 GiB memory cap
where supported, and 10 MiB output-file ceiling.
The complete measurement slice has a 10-minute ceiling, terminates its own children on
timeout, and retains logs and exit statuses.
No retry changes the source, side or acceptance criterion.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
