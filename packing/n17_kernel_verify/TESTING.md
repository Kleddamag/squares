# Tests

`cargo test --release` runs, without Python: the geometry and sweep helpers on exact
inputs; the sweep against an exact area-subtraction reference on random rational
polygons; facets against the hull of vertex differences; the 256-bit product comparison;
canonical JSON and float `repr` tables taken from CPython 3.14; the
`random.Random(seed).sample` table; and the receipts of the fixtures in `tests/data/` at
1, 2 and 4 threads against the standing verifier’s results.
The stalled W7 certificate is read from
`packing/campaign/explorations/X048-session-168-pilots/audit-verifier-rewrites/fixture-w7-bins8/`.

The fixtures and expected results were produced by Python scripts that run the standing
verifier as the oracle.
Those scripts are kept outside this repository, with the same crate, in
[wand125/square-packing, `tools/n17_kernel_verifier/tests/`](https://github.com/wand125/square-packing/tree/main/tools/n17_kernel_verifier/tests):

| script | what it checks |
| --- | --- |
| `make_fixtures.py` | the tiny closed, stalled, sampled and dead-row fixtures and their oracle results |
| `make_fixture_ohi.py` | a fixture closed by `owned_hulls_intersect` (no recorded certificate closes this way) and two controls: a wrong declared kind, and the point moved out of the hull |
| `differential.py` | 185 mutations of the fixtures at 1 and 4 threads: status, failure text, counts and content ids equal to the oracle’s |
| `cli_check.py` | receipt bytes equal to Python’s `json.dumps(indent=1)`, exit codes, progress lines, the embedded cover |
| `make_compatibility_data.py` | the CPython float `repr`, sampling and Unicode tables |

## The review’s mutations

The 34 certificate mutations of the 2026-10-03 verifier review (lane R6,
`audit-verifier-rewrites/mutate_cert.py.txt`) were applied to the stalled W7
certificate, with a local loader and saver (canonical JSON, gzip, SHA-256 names) in
place of the generator’s. Both verifiers refuse all 34, naming the expected check, with
identical failure text.

## Certificates from the standard procedure

Seven certificates produced with the standard procedure at `4148483da`
(`--bins 64 --max-rounds 24 --hull-limit 16 --producer-share 0.6 --split-floor 512
--max-rows 1152 --split-patience 1` for BC-428; W7 variants at bins 16, 32 and 64):
receipts equal at 1 and 16 threads, and the timings in README.md.
They are not included (215 MB).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
