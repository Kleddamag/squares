N11 OPTIMALITY REVIEW — REPRODUCIBILITY SUPPLEMENT
================================================

This archive accompanies the adversarial review of the tentative optimality
proof for eleven independently rotated unit squares. It supplies runnable
checks for the review's new mathematical components and finite-set reductions,
plus the principal recorded results of the larger audit.

THIS IS NOT A STANDALONE REPLAY OF THE WHOLE GLOBAL OPTIMALITY PROOF.

The driver does not replay all 2,180 exclusions or the entire capture graph.
It does not turn retained execution receipts into newly executed geometry.
Its success status is PASS_REVIEW_SUPPLEMENT_COMPONENTS, with
global_optimality_proved=false and whole_global_proof_replayed=false.


QUICK START
-----------

Use Python 3.12 or newer. Python 3.12.14 was used for the relocated test.
The local checks import numpy, scipy, and sympy; mpmath is a sympy dependency.
The tested versions are pinned in requirements.txt. All other entry points
use only the Python standard library. No dependency packages are bundled.

For a separate virtual environment, run from this archive's extracted root:

    python3 -m venv ../n11-review-env
    ../n11-review-env/bin/python -m pip install -r requirements.txt
    ../n11-review-env/bin/python -B verify_review.py

Use the corresponding interpreter path on your operating system. Keep a
virtual environment outside this bundle: undeclared input files are refused
by the integrity checker. An already prepared Python environment also works.

The verification scripts make no network requests. Installing dependencies
can be done separately, including from a locally supplied wheel directory.

The driver resolves its own location and changes to the bundle root, so it
can also be invoked from another directory:

    /path/to/python /path/to/n11-review-supplement/verify_review.py

For identity checking without mathematical replay:

    python -B verify_review.py --hashes-only

That mode prints PASS_HASHES_ONLY and makes no mathematical verification claim.
Every mathematical entry point refuses Python -O and -OO because assertions
are part of the checked implementation.


WHAT THE DRIVER RERUNS
---------------------

1. Independent rational root isolation, endpoint/cap comparison, the short
   cap certificate, and irreducibility checks for the parameter and side
   polynomials.

2. Independent exact witness arithmetic: unit-square geometry, all scalar
   wall-containment inequalities, all 55 pair separations, and both spans.
   The symbolic-contact helper verifies that the nonautomatic closing gap
   has the stated polynomial numerator.

3. Read-only consumption of all 648 supplied v2 D4 incidence records.
   verify_d4_review.py calls the independent verify() consumer. It never
   calls generate(), and it verifies that the trace bytes did not change.
   The bundle copy of d4_propagation_certificate.py also has a read-only
   direct entry point. Running the driver DOES NOT REGENERATE THE TRACE.

4. Independent reconstruction of the 16 center cells and all 220 closed
   four-view overlay regions, including their eight singleton regions.
   It checks the reflection relation, simple rational enclosing boxes, and
   the distance obstruction needed by the review's simplified FINAL D4
   bridge. It does not replace the older baseline-dependent support proofs
   for cases 2175 and 2176. Their larger distance-ban inventory is omitted.

5. Both implementations of the proposed two-radius local lemma. Each
   checks all 8,448 signed-coordinate residual/nonlinear inequalities and
   all 88 negative features. The second reconstructs elementary functions
   and gradients with separate exact field arithmetic. Both retain the
   original branch inventory and rational dual certificate data. The
   driver compares their newly produced radii and exact maximum ratio.
   Global capture and pose inclusion remain separate premises.

6. Exact finite-set verification of the 44-certificate field selection
   against the 59 full fresh field receipts produced during this review.
   This stage DOES NOT RERUN FIELD GEOMETRY. It checks source bindings,
   complete recorded row inventories, every transfer set, the 1,904-case
   union, the 43 mandatory-certificate uniqueness witnesses, and the sole
   residual case 1456. The result proves that 44 is a minimum within these
   fixed 59 field certificates and their checked transfer sets.

The field reduction retains 17,963 of the original 24,373 whole-angle rows
and 4,233 of the original 5,877 ownership-point checks. The mathematical
geometry of all 59 certificates was freshly checked during the review;
the included 59 receipts preserve those executions. This compact driver
performs the finite selection check using those recorded results.

TOP-LEVEL 71-CERTIFICATE CAVEAT: The original 93-certificate baseline has
a sufficient top-level selection of 44 field plus 27 generic certificates.
Seven generic case conclusions are already in the field union. This is
an inventory-level statement, NOT a 71-file source closure. Shared ancestors,
checker inputs, and downstream source bindings must still be retained or
replaced by independently checked equivalents. A terminal case being
redundant does not by itself authorize removal of a source needed elsewhere.
The 27 generic proofs are not freshly replayed by this supplement.


DIRECT COMPONENT COMMANDS
-------------------------

From the bundle root with the same Python environment:

    python -B independent_endpoint_check.py
    python -B independent_cap_short_certificate.py
    python -B independent_irreducibility.py
    python -B independent_side_irreducibility.py
    python -B independent_exact_witness.py
    python -B independent_witness_simplify.py
    python -B verify_d4_review.py
    python -B d4_independent_geometry.py
    python -B local-isolation-audit/verify_simplified_local.py
    python -B second_review_simplified_local.py
    python -B verify_field_subset.py

The symbolic helper expects the exact witness output, and the full driver
runs these in the appropriate order. The second local implementation also
compares its exact maximum ratio with the retained simplified-local result.
The full driver additionally compares both newly generated local results.


FILES, IDENTITIES, AND OUTPUTS
-----------------------------

source-manifest.json lists the byte count and SHA-256 of every supplied
file except the manifest itself. It distinguishes:

- unchanged source modules copied from the pinned Squares Project;
- exact pinned certificate inputs;
- new review helpers, including recorded bundle-only path/entry-point
  adaptations;
- produced review evidence and the 59 recorded fresh field results;
- documentation and licensing/attribution notices.

The driver checks all listed identities before importing proof helpers,
checks the complete supplied file inventory, and checks identities again
after the replay. The source manifest is an integrity and provenance map,
not a proof of the mathematical rules or an independent execution attestation.

All newly produced results and logs go in fresh-results/. That directory
is excluded from the immutable input inventory. Repeated runs may replace
those generated outputs. Recorded evidence is separately held under
recorded-results/ and fields/receipts/ and is not overwritten by the driver.

Important payloads are:

    d4-propagation-traces.json
        Supplied v2 incidence trace, consumed read-only.

    squares/packing/resources/web/n11-optimality-2026-09-29/
      receipts/d4-independent/objects/<SHA-256>.json
        The two exact cover/overlay inputs, retaining the paths expected
        by the portable D4 loader. Their decoded hashes are checked.

    local-isolation-audit/weighted.json
    local-isolation-audit/focused.json
    local-isolation-audit/sq/packing/
        Two exact certificate inputs and the minimal ten unchanged
        source modules used by the local implementations.

    fields/A1-baseline.json
    fields/minimal-44-field-manifest.json
    fields/receipts/<packet SHA-256>.json
        Pinned original A1 baseline, the complete subset/uniqueness
        evidence, and all 59 complete fresh review receipts.

    recorded-results/
        Principal audit observations: exact witness, D4, local checks,
        field summary/negative controls, one nonfield exclusion, retained
        final composition, near-state source binding, and historical
        T-025 verification. Inclusion of a receipt does not imply this
        driver reexecutes its underlying computation.

The archive deliberately omits the large near-capture raw object, the full
original source archive, discovery histories, binary dependencies, and the
complete field/capture source closure needed for a full global replay.


SOURCE PINS AND ATTRIBUTION
---------------------------

Squares Project: Joshua Levy, the squares project
https://github.com/jlevy/squares
revision ea0a3b19a70085683c3b65946cded03ffe4e2415

Original optimality proof/certificate package:
https://github.com/Queuingtheorydotcom/11SquaresOptimal
revision f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c

The known packing is credited in the source to Walter Trump, with David
Ellsworth credited for its reconstruction diagram. This supplement makes
no priority claim for the original construction or optimality argument.

The copied Squares Project license is in UPSTREAM-LICENSES.txt. Original
source-module and certificate identities are recorded in source-manifest.json.
Upstream modules are unchanged. Bundle-only modifications to new review
helpers are limited to portable paths, output destinations, explicit failure
guards/checks, and read-only consumer entry points, as recorded there.

The accompanying report explains the mathematical arguments, unresolved
global replay scope, and the distinction between repaired exposition,
newly checked simplifications, and retained execution evidence.

REVIEW TARGET SNAPSHOT

reviewed-paper.md preserves the exact Markdown document fetched for this review:
https://jlevy.github.io/squares/papers/n11-optimality-review.md
It is 153,686 bytes, SHA-256
428da02fd5b99a6133736113e564097e9281aae213076265f968ceefd4bd3d68.
The source manifest records its URL and byte identity. This reference snapshot is
not used as a mathematical premise by the executable component checks.
