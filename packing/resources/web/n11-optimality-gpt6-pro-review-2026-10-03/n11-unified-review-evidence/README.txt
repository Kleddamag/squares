N11 OPTIMALITY: UNIFIED REVIEW EVIDENCE

This companion archive makes the new reconciliation computations inspectable.
It is not an end-to-end proof runner and does not certify global optimality.
The unified report is delivered separately and is deliberately not an input to
this archive. All verification is offline after installing dependencies.

WHAT THE DEFAULT COMMAND CHECKS

1. File identities for every immutable supplied source, input, prior-supplement
   member and recorded result, including both original review snapshots.
2. The historical/corrected interval predicates on 12,180 exact small cases:
   616 historical singleton false acceptances, no corrected errors on this grid;
   positive-area/degenerate-domain controls, exact seams and gaps of 10^-50;
   reconstruction and raw-order convexity of the 16 pinned cover cells.
3. The publisher's separate coverage helpers on seven tiny point/segment/area
   cases using its unchanged nine-module import closure and Fraction backend.
4. B's 8,448 retained local duals in published, tighter-curvature and simplified
   configurations. It directly bounds weighted residuals, reconstructs the
   canonical dictionary of 56 derivative rows and 128 branches, and verifies
   exact rank 25 and nullity 8 for the 30 common rows. It compares A's printed
   33 radii with B's pinned input. It does not have or verify A's newly generated
   dual vectors.
5. Exact equality with the recorded coverage results and canonical dictionary;
   local result equality ignores only the measured top-level seconds field.
6. All immutable file identities again after execution, including every byte
   of the historical prior supplement. New output goes only to fresh-results/.

This default run does not run the prior 11-stage supplement driver, regenerate
any D4 trace, rerun field certificates, or replay the capture graph or complete
global proof. The small coverage controls diagnose selected contracts; they do
not prove all implementations correct on arbitrary inputs. The local checker
replays B's source/data, not an independent reconstruction of A's unavailable
calculation. Recorded-only endpoint/radii/commit results remain labelled as
recorded evidence; inclusion is not execution attestation.

INSTALL AND RUN

Tested with Python 3.12.14 and the exact versions in requirements.txt. Create
an environment OUTSIDE this immutable directory; adding a virtual environment
inside the bundle intentionally fails the inventory check.

  python3 -m venv ../n11-unified-review-env
  ../n11-unified-review-env/bin/python -m pip install -r requirements.txt
  ../n11-unified-review-env/bin/python -B verify_reconciliation.py

The driver resolves its own location and changes its subprocess working
directory to the bundle root. It can be invoked by absolute path from any
working directory. Python -O/-OO is refused because the scientific helpers
use assertions. For identities only, with no mathematical replay:

  ../n11-unified-review-env/bin/python -B verify_reconciliation.py --hashes-only

Outputs: fresh-results/verification-summary.json, fresh-results/local/,
fresh-results/reconciliation-coverage-check.json,
fresh-results/reconciliation-original-coverage-check.json, and stage logs.
The archive includes results from a relocated complete run; rerunning replaces
only new fresh-results outputs. Those outputs are excluded from the immutable
manifest, so their inclusion does not supply the mathematical verification.

To run a helper directly, first change to this bundle root. Coverage helpers
use the intentionally preserved relative squares/, original/ and geometry-audit/
layout; the wrapper supplies the same setup automatically.

  PYTHONPATH=squares/packing python3 -B reconciliation-coverage-check.py
  ELEVEN_RATIONAL_BACKEND=fraction python3 -B reconciliation-original-coverage-check.py
  python3 -B reconciliation_local_checks.py --bundle prior-supplement \
    --review-a source-reviews/report-A.md --output-dir fresh-results/local

PRESERVED PRIOR SUPPLEMENT

prior-supplement/ contains every file from the original B archive, unchanged,
with only the outer directory renamed from n11-review-supplement. The original
archive SHA-256 was:
4f9065c61fa188b74d124912f4213677492b21330e3753c89d34214395bb7536
Each manifest entry records the original archive member path. Historical source,
recorded receipts, old manifests, old README and old fresh-results all retain
exact archived bytes. They describe B's earlier scope, not new reconciliation.

To rerun the prior 11 stages, copy that subtree OUTSIDE this directory first:

  cp -a prior-supplement ../n11-prior-supplement-replay
  ../n11-unified-review-env/bin/python -B ../n11-prior-supplement-replay/verify_review.py

This copy preserves the archived prior results here. The prior driver verifies
the supplied v2 D4 trace read-only and does not regenerate it. Its field stage
checks the 44-selection and minimum from 59 recorded fresh field receipts;
it does not rerun their geometry. The 71-certificate baseline selection is a
TOP-LEVEL certificate count, NOT a 71-file transitive source closure. Shared
ancestors and source-bound downstream inputs remain required. Neither the old
nor new driver is the whole global optimality proof.

CONTENTS AND PROVENANCE

source-reviews/report-A.md and report-B.md: original supplied report bytes.
recorded-results/: new coverage, symbolic endpoint, radii, original Git commit,
local replay and canonical-row evidence, unchanged from the reconciliation.
reconciliation_local_checks.py: unchanged portable reconciliation helper.
reconciliation-coverage-check.py and reconciliation-original-coverage-check.py:
raw reconciliation helpers, with only explicit -O/-OO refusal added before
imports. Their pinned imported scientific modules are unchanged.
squares/packing/devtools/: exactly five coverage imports from
jlevy/squares@ea0a3b19a70085683c3b65946cded03ffe4e2415.
original/src/evidence/research/phase3/work/: exactly nine coverage imports from
Queuingtheorydotcom/11SquaresOptimal@f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c.
geometry-audit/: the pinned small decoded cover input.
original/.../upstream-notices/: retained upstream licensing and attribution.
prior-supplement/UPSTREAM-LICENSES.txt: the prior complete project license notice.

manifest.json records bytes, SHA-256, classifications and provenance for every
immutable file. manifest.sha256 checks the manifest's own identity. These hashes
provide an integrity chain, not external attestation that executions occurred;
the delivered ZIP digest anchors the complete package. The driver excludes only
the root manifest files, top-level fresh-results/, and __pycache__ caches from
its immutable inventory. It does not exempt historical prior fresh-results.
No dependency binaries, large capture object, discovery tree or source tar is
included. The entire extracted prior supplement is retained for reproducibility.
