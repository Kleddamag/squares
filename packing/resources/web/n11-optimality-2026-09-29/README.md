# Eleven-Square Optimality Source Packet

[Queuingtheorydotcom/11SquaresOptimal](https://github.com/Queuingtheorydotcom/11SquaresOptimal)
publishes a proposed computer-assisted proof that the known eleven-square packing is
globally optimal under independent rotations and boundary contact.
Its claimed minimum side is the algebraic Trump construction side, about 3.8770835900.
**T-060 is now confirmed at S5/V4/C5.** The complete independent geometric
execution ensemble covers all 2,180 exclusions and ten capture nodes. Astra at max
reasoning reviewed their mathematical composition; the
[final receipt](receipts/final-composition.json) has no pending obligations.
The initial intake was V0/C0, followed by a scoped C1 review; the checkpoints below
retain that history without substituting metadata checks for geometry.
Shared arithmetic dependencies and reproduction limits are stated below.

For a human or agent reviewing T-060, start with the
[validation guide](VALIDATION.md): proof obligations, certificate and checker links,
available commands, and the remaining requirements for a standalone release.

This packet pins source commit `f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c` and tree
`3fed944c5a0c1dda5e61cb9f45f0dd3d4dc6360c`. The selected files in [`source/`](source/)
are verbatim; [`provenance.json`](provenance.json) records their hashes.
The original `data/INDEX.json` is stored as deterministic
[`INDEX.json.gz`](source/data/INDEX.json.gz); provenance records both its decoded and
stored hashes. Start with the [claim](source/README.md),
[proof exposition](source/PROOF.md),
[reproduction instructions](source/docs/REPRODUCING.md), and
[publication scope](source/docs/PUBLICATION.md).

The published data store uses Git LFS.
[`lfs-pointer-inventory.json.gz`](lfs-pointer-inventory.json.gz) lists 2,638 unresolved
pointer files representing 2,344,331,966 declared bytes at initial intake.
The subsequent [independent symmetry receipt](receipts/d4-independent/result.json)
retains three selected compressed objects totaling 102,046 bytes, with provenance and a
replay script beside it.
The [local residual receipt](receipts/local-dual-residual/result.json) subsequently
retains two further objects totaling 1,560,204 compressed bytes and checks all 8,448
signed-coordinate residuals.
Its status remains incomplete: curvature, feature margins and geometric capture are
separate obligations.
Adjacent provenance and replay files bind the inputs and implementation, including
shared source primitives.
The later [fixed-T local-isolation receipt](receipts/local-isolation/result.json)
confirms all curvature, feature-margin and nonlinear-branch obligations using the same
two objects. It isolates the labelled Trump pose inside the supplied rectangle; the
[pose inclusion receipt](receipts/pose-inclusion/result.json) checks the supplied near
domains conditionally.
The [case census](receipts/case-census/result.json) checks all case lists, and the
[first field receipt](receipts/field-mask0/result.json) independently accepts 459
exclusions. The [exclusion inventory](receipts/exclusion-inventory.json) binds accepted
geometric executions for all 2,180 excluded cases.
The [capture refusal](receipts/capture-ancestry/refusal-result.json) retains a confirmed
mismatch between the actual near-state digest and its published audit; it blocks that
proof-packet binding, without refuting global optimality.
The independent [capture receipts](receipts/capture-child-near/) instead check the
source-state chain. The [completion inventory](receipts/completion-inventory.json) and
[final composition](receipts/final-composition.json) bind the completed proof; an
inventory does not rerun geometry.
The symmetry check passed conditionally; it does not establish global optimality.
The source’s publication note says the privacy-normalized public derivative has not had
a fresh full geometric replay.
No publisher checker was used as proof authority in these independent checks.

## Reproducing the Independent Checks

There are two distinct tasks.
To **recheck retained evidence**, use Python 3.14 and the external-scratch environment
required by `AGENTS.md`. On the recorded Mac, run:

```bash
source /Volumes/spud-ext1/agent-scratch/wand125-tools-01a0ebfc/env.sh
cd packing
.venv/bin/python3 -m devtools.inventory_n11_completion --out "$TMPDIR/n11-completion-new.json"
.venv/bin/python3 -m devtools.check_n11_final_composition --out "$TMPDIR/n11-composition-new.json"
```

Use new output names.
The [completion inventory tool](../../../devtools/inventory_n11_completion.py) and
[final composer](../../../devtools/check_n11_final_composition.py) bind reviewed
receipts, case IDs, source hashes, and state joins.
**Neither command reruns geometry**; the composer refuses a missing or changed premise.
Its conclusion is conditional on the recorded executions and their mathematical review.

For a **fresh geometric replay**, pin the published commit and tree recorded above,
verify each compressed and decoded object against [the index](source/data/INDEX.json.gz)
and its Git LFS pointer, and run the first-party checkers at the source revisions bound
by their receipts. The checked-out upstream source is in `attic/11SquaresOptimal/`; the
larger acquired object cache is
`attic/n11-proof-inputs/f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c/objects/`. The cache is
local and ignored by Git, so a new checkout must acquire its objects.
The [field acquisition tool](../../../devtools/prepare_n11_field_manifest.py) and
[non-field acquisition tool](../../../devtools/prepare_n11_nonfield_batch.py) check
source-index, LFS-pointer, compressed, and decoded identities before retaining inputs.
The [non-field manifest](receipts/nonfield-manifest/summary.json) describes the 276
source-bound recipes; a recipe or publisher `PASS` string grants no geometry credit.

| Obligation | Exact replay entry point and recorded execution |
| --- | --- |
| Symmetry, case census, and local geometry | The [D4](receipts/d4-independent/replay.sh), [case census](receipts/case-census/replay.sh), [local isolation](receipts/local-isolation/replay.sh), and [pose inclusion](receipts/pose-inclusion/replay.sh) scripts record commands and input bindings. The [source graph](receipts/source-graph/replay.sh) checks capture ancestry separately. |
| Field exclusions | [Field selections](receipts/field-batch-a/selection.json) feed [the batch runner](../../../devtools/run_n11_field_batch.py). The [accepted field inventory](receipts/field-batch-a/field-coverage-inventory.json) names every credited receipt and its checker hash; each `summary.json` records the actual invocation and full-result hashes. |
| Non-field exclusions | [The bounded batch runner](../../../devtools/run_n11_nonfield_batch.py) uses the [manifest](receipts/nonfield-manifest/manifest.json.gz) and pinned objects. Its [final sequential batch](receipts/nonfield-batch-final-sequential/summary.json) and other reviewed batch summaries record case IDs, backends, ceilings, checker hashes, invocation parameters, and result hashes. The exceptional [center partition](receipts/center-partition-1383-indexed/provenance.json) has its own recorded eight-node replay; the two conditional D4 cases retain [cut reports for 2175](receipts/generic-case2175-complete/replay-d4-cuts.json) and [2176](receipts/generic-case2176-complete/replay-d4-cuts.json) beside their geometric results. |
| Capture induction and descendants | The [root bridge](receipts/capture-root-bridge-final2/provenance.json), [first step](receipts/capture-step0/provenance.json), [root node](receipts/capture-root-node-full-integer/provenance.json), and [14-round chain](receipts/capture-root-chain/result.json) precede the [r1 branch](receipts/capture-branch-r1-full/provenance.json). Each descendant records its parent and command: [r10](receipts/capture-child-r10/provenance.json), [far13](receipts/capture-child-far13/provenance.json), [near13](receipts/capture-child-near13/provenance.json), [r11](receipts/capture-child-r11/provenance.json), [far2](receipts/capture-child-far2/provenance.json), [r111](receipts/capture-child-r111/provenance.json), [far15](receipts/capture-child-far15/provenance.json), and [near](receipts/capture-child-near/provenance.json). |

The root-chain checker reads 14 separately executed round receipts; it does not redo
their geometry. The
[round consumer](../../../devtools/check_n11_capture_root_continue.py) checks each owner
update, and the retained `capture-root-round1-final/` through
`capture-root-round14-final/` directories hold their owner and round results.

These are independent first-party consumers of untrusted published proposals, not
independent implementations of every arithmetic primitive: several checkers share
first-party exact clipping, closed-cover, and collision kernels.
Each receipt binds the applicable checker and helper bytes, which may differ from the
current checkout. The child capture checkers also pin **byte-exact retained parent
results**, including timing fields.
A newly replayed parent can have the same mathematical state but a different receipt
hash; the existing child CLI cannot automatically admit it.
A fresh end-to-end replay therefore needs a reviewed state-equivalence and rebinding
workflow (tracked as `think-e2ot`); the retained-evidence composer does not supply one.
Do not repin a new result merely because its status says `PASS`.

The construction is credited to Walter Trump, and the bundled `jlevy/squares` source
credits David Ellsworth’s reconstruction diagram.
The source’s [third-party notices](source/THIRD_PARTY_NOTICES.md) assert no blanket
license over the collection; each file retains its applicable terms.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
