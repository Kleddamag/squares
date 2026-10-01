# Independent Review of exp-236

Astra max approved H-254 on October 1, 2026 after reviewing the complete
[raw receipt](run-001/result.json), provenance, command, timing and exit status.
The reviewer parsed the recorded arithmetic without loading the source certificate or
rerunning the target.
The reviewed instrument is commit `74480b0a0139aafaef4fa15c778cef9464569ca1`.

## Coverage and Arithmetic

The reviewer reconstructed the complete unique clause-name set and frozen bounds, then
independently recomputed every rational comparison and chart scalar/vector from the
recorded side and half-angles.
All 458 checks pass, with no missing, duplicate or extra clause:

| Clause Group | Count |
| --- | ---: |
| Domain | 3 |
| Strict support signs | 6 |
| Orientation classes | 16 |
| Wall anchors | 15 |
| Selected contact gaps, support sums and axis membership | 60 |
| Alternative unoriented SAT axes | 42 |
| Equation residuals | 3 |
| Auxiliary projection residuals | 4 |
| Centre coordinates | 34 |
| Closing-contact identities | 3 |
| Containment coordinates | 136 |
| Unordered square pairs | 136 |

The largest equation residual is approximately $1.346412991990249\times10^{-16}$, below
the frozen $10^{-12}$ cap.
The weakest alternative axis has gap approximately $-0.05579984657519721$, below the
required $-10^{-6}$. Exact fractions are retained in the JSON; these decimal summaries
do not decide acceptance.

The source digest, row-to-label map and exact side match H-253. Git inspection confirmed
that the reviewed checker and tests equal the frozen commit.
Launch status has no tracked changes; only the new output directory was untracked.
Seven synthetic controls were independently replayed before target access and passed in
0.70 seconds. Pretarget review corrected the final bridge’s mixed-orientation support
sum; the control now covers all 20 support identities.

## Cost and Limits

The target exited zero after 1.13 seconds wall, 0.52 seconds user and 0.17 seconds
system CPU time.
Maximum resident memory was 74,268,672 bytes and JSON output was 208,788
bytes. The launch used one worker, a 90-second timeout and a 10 MiB output-file ceiling.
The optional data-segment memory cap was unavailable on macOS, explicitly recorded in
[memory-guard.log](run-001/memory-guard.log).
Host contention was measured separately in [provenance.log](run-001/provenance.log).
These single-run timings are not a benchmark comparing implementations.

## Decision

**Accept H-254 at its declared scope:** the fixed relaxed rational witness has the
preregistered contact and reconstruction fidelity.
This is not an exact endpoint construction, root-existence proof, local optimum, or
global optimum. The separately reviewed conditional minimum theorem does not substitute
small residuals for exact equalities.
Root isolation and joint endpoint-slider feasibility are tracked by `think-bj81`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
