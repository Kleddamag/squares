# Review: wand125's `s(18) ≥ 588/125` and `s(19) ≥ 48229/10000` on Declared Nets (T-099, T-100)

**Verdict.** I found no defect in either certificate or in the argument from certificate to bound. Every exact premise holds, and I re-derived each one with my own code:

- the measure is nonnegative, exact, D4-symmetric by expansion, and totals n − 1/100000;
- both nets meet lemma N0's premises (a) to (e), with every margin stated below;
- the last bin of each net still has an assigned orientation;
- every shipped record and input is bound to its declared net and to the expanded candidate. I checked this with code of my own, not only with the first-party tool.

Twenty net nodes were reproduced with the producer's code: the import lane's fourteen sampled nodes, and six more I ran myself (three per certificate). All returned the shipped record.

There is one blocking finding, FN-1. It sits in this repository's new `replay` command, not in the certificates:
- `replay` runs the source's driver without refusing `PYTHONOPTIMIZE`.
- The source's checks are Python `assert`s, so under that variable a replay can pass without those checks running, and its run record cannot show this.
- FN-1 blocks only the use of a `replay` receipt to raise either entry's rung. It does not block registration at V0/C0.

Six non-blocking findings and one note cover the tool, the records and the controls. I keep the drafted S3 for both entries.

## Scope and Evidence

**What I read.**
- `AGENTS.md`.
- The packet README, `acquisition/sources.json`, `acquisition/upstream-subtree.sha256`, and all six receipts.
- The two source READMEs, `mixed_n19_L48229/verification/prepublication-replay.txt`, `mixed_n18_L4704/verification/control-results.json`, and both `publication-audit.json` files.
- `packing/devtools/audit_wand125_declared_net.py` in full, and the parts of `audit_wand125_point_and_mixed.py` it calls: `driver_preconditions`, `check_angle_record`, `n50_replay`, `replay_runtime`.
- `audit_wand125_rectangles.least_covered`, `coverage_exact` and `net_rotation`.
- The new tests.
- The source's retained code:
  - `mixed_net_audit.py`, `mixed_density_check.py`, `mixed_rotated_verify.py`, `verify_rotated_result.py`, `verify_axis_certificate.py`, `mixed_axis_cells.py`;
  - `mixed_rotated_verify.cpp`, skimmed for how it reads the header and searches the centre domain;
  - both `verify_mixed_full_proof.py` copies.
- `SOUNDNESS.md`, from the Theorem to lemma N0.
- The branch's diffs to `results.yaml`, `evidence.yaml`, `n-018.md`, `n-019.md`, `source-coverage.yaml`, `bibliography.yaml`, `SYNOPSIS.md`, `STATUS.md`, `VERIFIERS.md` and `INVENTORY.md`.
- `verifiers.yaml` entry `V-wand125-verify-mixed-full-proof-py`.
- The significance and rung tables of `epistemics.md`.
- The 5 October review's DN-1.

I did not open anything named `sqverify-net`.

**What I ran.** Every command ran from `packing/` with `.venv/bin/python3 -I` (Python 3.14.7) under `nice -n 15`. Scratch files are under `…/r2/review/work/`.

1. **Tarball digests.** `sha256sum` gave `a4098f82…d4a709` (31,800,246 bytes) and `03aeca45…629c54` (24,197,004 bytes). Both equal the `pinned_only` entries in `sources.json` and the lines in `upstream-subtree.sha256`.
2. **Unpacking.** My own `unpack.py` re-checked each digest and unpacked into new empty directories `u18/` and `u19/`:
   - n18: 3,351 members (2,516 files, 835 directories), one top-level directory, no absolute or `..` paths, member times from 2026-10-05T09:28Z to 2026-10-06T00:29Z;
   - n19: 1,687 members (1,268 files), times from 2026-09-26 to 2026-10-06T00:28Z.
3. **The tool's own checks.** I ran `audit --certificate {n18-L4704,n19-L48229,n18-L470} --check`, through a wrapper that only sets `sys.path`. All three returned `RECEIPT_MATCHES`. `bundle` on each unpacked tree, written to scratch, was byte-identical to the committed `bundle.json`. `pytest tests/test_audit_wand125_declared_net.py` gave 24 passed.
4. **`net_exact.py`, my own exact re-derivation of both nets.** It covers:
   - the endpoint and the last bin;
   - three containment forms: B(1 + D), the sharp extent at z = D/2, and the tangent form;
   - (d), F3's bounds, and L² ≥ 2B²;
   - at every node: the per-bin floor (2r − 1)D/2, the condition 0 < ρ(floor) < L/2, and ρ(floor) ≥ B(cos θ_r + sin θ_r)/2;
   - the gaps and the separation inequality.

   All values are below.
5. **`bind_own.py`, my own binding of each unpacked bundle**, written independently of `bundle()`'s code. It checks:
   - every `files-sha256.json` entry, with nothing unlisted (2,515 and 1,267 files);
   - the bundle's candidate, certificate and manifest against the retained bytes;
   - my recomputation of the candidate's semantic digest (the fields `n, L, B, rectangles, points, total_mass, proof_net`, sorted and compact), which equals `scaling_source_digest`: `9ae8403b…` and `68706528…`;
   - my own D4 expansion, made by the eight matrices about (L/2, L/2), whose exact integral equals M;
   - at every oblique node: status, empty frontier and witnesses; candidate digest, net index, t = rD and γ = 1; the floor (2r − 1)D/2; `centre_low` = ρ(floor) and `centre_high` = L − ρ(floor); E = L/2 − ρ(floor); the input's SHA-256;
   - in every input: header lines that enclose L, B, E, cos θ_r, sin θ_r and 1, each at most one ulp wide; rectangle lines that enclose my images as a bijection per row; the identical rectangle block at every node; the point count 0;
   - `replayed.json` against the certificate's record;
   - the axis record's `proof_spec` (net step and last index), with its axes running from L/2 to L − 1/2.

   Both certificates passed every check.
6. **The source's checker on six nodes the import lane had not sampled.** I used the tool's `sample` with one worker, its output going to scratch via `--out`:

   | Certificate | Node | Matches shipped | Checker nodes | Recorded lower bound | CPU seconds |
   | --- | ---: | --- | ---: | --- | ---: |
   | n19 | 198 (second-least lower bound) | yes | 188,295 | 1.0000000007754215 | 128.9 |
   | n19 | 414 | yes | 236,451 | 1.0000000720229265 | 186.1 |
   | n19 | 415 (last node) | yes | 236,501 | 1.0000000510044436 | 190.6 |
   | n18 | 2 | yes | 103,459 | 1.0000003206885772 | 25.3 |
   | n18 | 759 (second-least lower bound) | yes | 182,545 | 1.0000000015196813 | 96.5 |
   | n18 | 830 (second-slowest) | yes | 202,153 | 1.0000002513129942 | 109.6 |

   Both runs returned `SAMPLE_REPLAYED`, each after its binding passed. With the lane's samples, the nodes now reproduced with the producer's code are:
   - n18: 0, 1, 2, 208, 416, 636, 759, 797, 830, 831 (10 of 832);
   - n19: 0, 1, 37, 104, 198, 208, 312, 411, 414, 415 (10 of 416).
7. **`cover_search.py`, my own binary64 search** for a low-coverage centre at one node, with an exact rational check at the best point found. It uses its own expansion and clipping and shares no code with the source or with `audit_wand125_rectangles`. Least captures found:

   | Certificate and node | Grid | Least capture found, exact at that point |
   | --- | ---: | --- |
   | n18, node 797 | 30 | 1.0064573120066116 |
   | n18, node 831 | 60 | 1.0075805177889836 |
   | n19, node 37 | 60 | 1.002671438760494 |
   | n19, node 415 | 60 | 1.0018877744037142 |

   This is a heuristic spot check. It decides nothing.
8. **`mutant_nets.py`**: exact containment arithmetic for `control`'s corrupted nets (FN-3).
9. **`PYTHONOPTIMIZE=1 .venv/bin/python3 -c "assert False"`** exits 0. With `-I` it exits 1 (FN-1).

`git status` was clean afterwards at `35a148afa`.

## The Argument From Certificate to Bound

**The measure.** Each candidate has the following properties:

| | n18-L4704 | n19-L48229 |
| --- | --- | --- |
| Rows, all of positive mass | 209 | 313 |
| `points` | empty | empty |
| `scaling_factor` | `"1"` | `"1"` |
| Total mass M | 1799999/100000 = 18 − 1/100000 | 1899999/100000 = 19 − 1/100000 |

- Every row lies inside [0, L]², with 0 ≤ x₁ < x₂ ≤ L and 0 ≤ y₁ < y₂ ≤ L.
- The density is g = Σ w_j/(8|R_j|) Σ_{S∈D4} 1_{S(R_j)}. It is nonnegative and exactly rational.
- It is D4-invariant by construction. I expanded each row by the eight matrices about the centre, independently of the source's `expand` and of the tool's `orbit`.
- ∫g = M exactly, as recomputed.

**Orientations.** A unit square's angle φ is taken modulo π/2. If φ > π/4, reflect the whole configuration in y = x. That maps K to itself, preserves g and disjointness, and sends φ to π/2 − φ. So φ ∈ [0, π/4], and u = tan(φ/2) ∈ [0, √2 − 1].

**Nodes.** Take t_r = rD for r = 0, …, m. They cover [0, mD + D/2] to within D/2. Because mD > √2 − 1, every u has a node with |u − t_r| ≤ D/2. Then z = tan(δ/2) = |u − t_r|/(1 + u·t_r) ≤ D/2, where δ = |φ − θ_r| and θ_r = 2 arctan t_r.

**Containment.** Seen in the unit square's frame, the concentric core of side B at angle θ_r has extent

B(cos δ + sin δ) = B(1 + 2z − z²)/(1 + z²) ≤ B(1 + 2z) ≤ B(1 + D) < 1.

So the closed core lies in the open unit square. Distinct unit squares have disjoint interiors, so their cores are pairwise disjoint.

**Centre domain (format M's per-bin domain).** A square assigned to node r ≥ 1 has u ≥ a_r = (2r − 1)D/2. On [0, √2 − 1] the half-width ρ(u) = (1 + 2u − u²)/(2(1 + u²)) increases, since ρ′(u) is proportional to −(u² + 2u − 1). So the square's centre lies in [ρ(a_r), L − ρ(a_r)]². For r = 0 the floor is 0 and ρ = 1/2.

The C++ searches the quadrant [L/2, L/2 + E]² with E = L/2 − ρ(a_r). It uses lemma C1: g is invariant under the quarter turn, and so is a square at θ_r about its own centre. The axis checker uses [L/2, L − 1/2]² at core B and angle 0. Both are the right sets.

**Counting.** Each core captures ∫g ≥ 1, so n ≤ Σ∫_{Q_i} g ≤ ∫g = M = n − 1/100000. That is a contradiction. Containment of the cores in K is not needed, because g is supported in K.

### The 832-node net, exactly

The net has B = 1999/2000, D = 1/2006, m = 831, L = 588/125.

| Check | Exact value | Size |
| --- | --- | --- |
| (c) endpoint: t_max = 831/2006, t² + 2t − 1 | 497/4024036 > 0 | t_max − tan(π/8) ≈ 4.37 × 10⁻⁵ |
| Last bin floor 1661/4012: (a + 1)² − 2 | −9359/16096144 < 0 | tan(π/8) − floor ≈ 2.06 × 10⁻⁴ |
| (b) B(1 + D) | 4011993/4012000 | margin 7/4012000 ≈ 1.745 × 10⁻⁶ |
| Sharp extent B(1 + D − D²/4)/(1 + D²/4) | 32192229833/32192290000 | margin 60167/32192290000 ≈ 1.87 × 10⁻⁶ |
| (e) tangent form B(1 + D/(1 − D²/4)) | 32192229833/32192286000 | margin 56167/32192286000 ≈ 1.745 × 10⁻⁶ |
| (d) t_max ≤ 1/2 | holds | |
| (a) and F3 | N = 832 ≤ 2¹⁶; D > 2⁻¹⁸ | |
| L² ≥ 2B² | holds | |

The last-bin row means tan(π/8) lies strictly inside node 831's bin, so the last node has assigned orientations, and the nearest node to every u ≤ √2 − 1 is at most 831.

At every node r = 1, …, 831, ρ((2r − 1)/4012) ≥ B(cos θ_r + sin θ_r)/2, with the least gap about 1.18 × 10⁻⁶. So the per-bin domain lies inside Tokoharu's.

Every shipped `domain` block equals ρ((2r − 1)/4012) exactly. With D = 1/2006, B could go up to 2006/2007; 1999/2000 is inside that limit.

### The 416-node net (T-096's), exactly

The net has B = 999/1000, D = 1/1001, m = 415, L = 48229/10000.

| Check | Exact value | Size |
| --- | --- | --- |
| (c) endpoint: 415/1001 | 1054/1002001 > 0 | ≈ 3.72 × 10⁻⁴ past tan(π/8) |
| Last floor 829/2002: (a + 1)² − 2 | −1447/4008004 < 0 | ≈ 1.28 × 10⁻⁴ below tan(π/8) |
| (b) B(1 + D) | 500499/500500 | margin 1/500500 |
| Sharp extent | 4007994993/4008005000 | margin 10007/4008005000 |
| (e) tangent form | 1335998331/1336001000 | margin 2669/1336001000 |

The least per-bin gap over the core's half-width is about 2.25 × 10⁻⁶.

**Lemma N0.** The lemma as `SOUNDNESS.md` states it is correct at both steps. Nothing in N1 to N4 depends on D's value. Premises (a) to (e) hold exactly on both nets, as tabulated. Its parenthetical sharp condition is right: the extent increases in z on [0, √2 − 1]. There is one notation clash, FN-7.

## The Source's Runs

**Binding.** The shipped records and inputs at every node are bound to the declared net and to the expanded candidate. The first-party `bundle` and my `bind_own.py` both show this, and they share no code:
- both read the inputs' header and rectangle lines against exact values;
- the candidate digest, which covers `proof_net`, is the same at every node and in the axis record;
- the axis `proof_spec` names step 1/2006 and last index 831, or 1/1001 and 415.

**Checker and driver.** The checker is the one the earlier reviews read:
- `proof/verify.cpp` and `code/mixed_rotated_verify.cpp` in both bundles are SHA-256 `89b674a6…3652`;
- the other nine `code/` files of each bundle equal the retained `mixed_n50_L740` copies, except n18's driver;
- n19's driver is `2719e482…`, the `mixed_n50_L740` copy and T-096's.

n18's driver is `477d613f…`. It differs from the n50 copy in one line only: `assert 1<=a.workers<=16` in place of `<=3`.

That change does not matter:
- `workers` only sizes the `ProcessPoolExecutor`;
- every node from 1 to count − 1 is submitted;
- the driver asserts `set(checked)==set(range(count))`;
- no check depends on how many workers there are.

The shipped `proof/manifest.json` records the original run at `"workers": 3`. Both drivers keep a stale docstring ("201-angle").

**The path-metadata redaction.** Per `publication-audit.json`, the redaction rewrote 834 files for n18 and 417 for n19:
- `bundle.json`;
- `proof/manifest.json`;
- every oblique `result.json`;
- `proof/axis/result.json`.

All 834 "after" digests equal the n18 bundle's files. No JSON file in the bundle still holds an absolute path; the rewritten fields are `candidate` and `source_candidate`, which now read `proof/candidate.json`.

What the redaction could not affect:
- `candidate.json`, `certificate.json`, every `input.txt`, every `replayed.json`, `integer-tables.npz` and the code are not on the list;
- `replay` re-derives each record's spec, input bytes, status, nodes, leaves, lower bound and frontier from the candidate, and asserts equality;
- the driver passes the candidate path explicitly, so the rewritten `candidate` field is never read.

What it could affect:
- unreplayed fields of rewritten files, such as `seconds`, which feeds only the pricing;
- the link between the source's pre-redaction runs and the published tarball. The "before" bytes (archives `ed4537e6…` and `d13351a4…`) are not published, so that link rests on the source's word.

The n19 pre-publication replay log reports "files 1266 mismatch 0". The README says "1266 original bundle file hashes", so the replay was of the pre-redaction bundle, not of the pinned tarball, which lists 1,267 files (FN-5).

**What the recorded lower bounds mean.** The least recorded lower bound (≈ 1 + 10⁻⁹ at nodes 797 and 37) is the minimum of the branch-and-bound leaf bounds, each just over threshold one. It is not the measure's slack. My search's least captures, 1.0065 at n18 node 797 and 1.0027 at n19 node 37, are of a different order. That is consistent with this reading, and no record misstates it.

## Where the Records Stand

I checked against my own arithmetic:
- the masses, nets and margins;
- the least bounds and their indices: 1.000000001066446 at 797, and 1.0000000005351664 at 37;
- the axis cells and minima: 1,623,076 and 1108824296663/1099511627776 ≈ 1.008469823012092; 4,717,584 and 1.0026527162381171;
- the node totals, 114,915,109 and 75,131,365;
- the second totals, 43,585.2 and 42,239.3;
- the CPU-hours, 12.1 and 11.7;
- all digests;
- the packet's 70 files and 57,841,419 bytes, which are 50 pinned-only files of 56,377,399 bytes plus 20 retained files of 1,464,020 bytes;
- the sample pricing: 408.3 ÷ 386.7 = 1.056 and 639.5 ÷ 559.7 = 1.143;
- T-096's 4.40-hour replay;
- the STATUS gaps, 0.1189 and 0.0627.

The gaps are 588/125 − 47/10 = 1/250 = 0.004, and 48229/10000 − 1927/400 = 27/5000 = 0.0054.

The separation holds: (48229/10000 − 7/2)² − 7/4 = 6441/100000000 > 0. The amount is 4.8229 − (7 + √7)/2 ∈ (2.4340 × 10⁻⁵, 2.4345 × 10⁻⁵), bracketed with rational bounds on √7. (7 + √7)/2 = 4.82287566 is correctly rounded.

T-096 and T-074 are V3/C3, so "the reported and verified lower bound" is correct for each. The statements about what was and was not done here are accurate, with these exceptions:
- the sample replays are not mentioned in T-099, T-100 or their evidence (FN-5);
- the driver verifier's record does not cover n18's driver (FN-4);
- T-100's `composition` names evidence that its `evidence` list lacks (FN-6).

## The First-Party Tool

- **`audit`.** It checks what its docstring says and decides no coverage. It does not check the tangent form in the net blocks, because the source does not state it there; it computes (e) itself.
- **`bundle`.** It is sound as written:
  - the file list must equal the files present;
  - every header line is checked at every node;
  - the rectangle block is matched as a bijection once, then held byte for byte at every node.

  It reads the axis record but not the axis `proof_spec`. The source's own axis replay asserts that, and node 0 is in both samples.
- **`sample`.** It calls `replay_runtime()`, which refuses `-O` and `PYTHONOPTIMIZE`, repeats the driver's preconditions, and returns only the nodes it ran.

  It cannot be run under `-I` as is. With 3.14's default forkserver, the workers fail with `ConnectionResetError` because they cannot import `devtools`. I ran it with a wrapper that sets `sys.path` and the `fork` start method. This is a note, not a defect of the result.
- **`replay`.** It does not call `replay_runtime()`, and it passes `os.environ` through (FN-1).
- **`compare`.** Its run checks hold against a run on these bundles:
  - the shipped bundles hold no `replay-progress.json` and no `replay-verify`;
  - every member time is before 2026-10-06T00:30Z, so the time test is meaningful.

  It would not report a mismatch on a correct replay. Its `bundle.json` test cannot fail: the shipped `bundle.json` already reports `REPLAYED_PROOF_BUNDLE`, and the driver never writes that file. It also does not require `proof/certificate.json` to have been rewritten (FN-2).
- **`control`.** It was not run on either new certificate; no receipt exists, and the records say the controls are still to be run.
  - The two mass mutants are provably invalid at the chosen node. The tool requires an exact capture below 1 at a centre that `least_covered` clamps into [L/2, centre_high]², at the node's exact rotation.
  - The `short-net` mutant is provably invalid. At φ = π/4 the nearest node's core extent is at least 1.000276 for n18 and 1.000069 for n19, from an exact rational lower bound on tan(π/8).
  - The `coarser-step` mutant is not provably invalid (FN-3).
  - `extra-field` is a format refusal.

## Findings

### FN-1: blocking for the replay exit: `replay` can report a match with the source's checks disabled

`replay` launches `sys.executable code/verify_mixed_full_proof.py` with `environment = os.environ | {…}`. It neither refuses nor strips `PYTHONOPTIMIZE`, and it does not call `replay_runtime()`, which `sample` and `control` both call.

Every check the source's driver and `verify_rotated_result.replay` make is a Python `assert`. These include:
- `rebuilt==spec` and the "Input tampered" check;
- `result[key]==saved[key]` for status, nodes, leaves, lower bound and frontier;
- `set(checked)==set(range(count))`.

`PYTHONOPTIMIZE=1 python -c "assert False"` exits 0. Under that variable the driver still writes `replayed.json` from the fresh lower bound and node count, exits 0, and writes the progress record and the binary. `compare` then reports `FULL_REPLAY_MATCHES_SHIPPED`, although none of the source's checks ran. `run.meta` does not record the variable, so the receipt cannot show this.

This is DN-1's class of defect: a receipt that cannot distinguish a real replay. It blocks using any `replay` receipt to move T-099 or T-100 to V3/C3.

**Fix:** call `replay_runtime()` first, drop `PYTHONOPTIMIZE` from the child's environment, record `sys.flags.optimize` and the variable in `run.meta`, and add a test that `replay` refuses when the variable is set. `next_rung` should name the fixed tool.

### FN-2: non-blocking, tool: two of `compare`'s run checks prove nothing

The `bundle.json` status test passes with or without a run. The rewritten-certificate test passes when the certificate was not rewritten, because the shipped copy equals the retained one.

**Fix:** drop the `bundle.json` test from the docstring's evidence, and require `proof/certificate.json`'s modification time to be after the start.

### FN-3: non-blocking, tool: `coarser-step` is not a provably invalid mutant, and its docstring is wrong

At D′ = (1 − B)/B, B(1 + D′) = 1, but the sharp extent B(1 + D′ − D′²/4)/(1 + D′²/4) is below 1:
- n18: 31968006001/31968010000, margin 3999/31968010000;
- n19: 3992003001/3992005000, margin 1999/3992005000.

So every core still fits strictly inside the unit square, contrary to the docstring's "the core need not fit inside the unit square". The control tests admission rule (b), not soundness.

**Fix:** use a step whose sharp extent is at least 1, such as the source's own control of 1/1001 at B = 1999/2000, and reword the docstring.

### FN-4: non-blocking, record: the driver's verifier record omits n18's driver

`V-wand125-verify-mixed-full-proof-py` pins only `2719e482…` and the n50 source path. `E-n018-wand125-mixed-4704-report` cites it for `477d613f…`.

**Fix:** add that version, with the retained n18 path and the one-line difference.

### FN-5: non-blocking, record: the sample replays and the pre-redaction replay are described incompletely

T-099, T-100 and both evidence entries do not mention the committed seven-node samples, which are partial reproductions with the producer's code that include node 0. They also do not list those samples among their artifacts.

The packet README and T-100's evidence say the source's pre-publication replay checked "every bundle file hash". The source says 1,266 original hashes. That replay was of the pre-redaction bundle (`d13351a4…`), and it binds to the pinned tarball only through the source's unpublished before-digests.

**Fix:** reword both points, and list the sample receipts.

### FN-6: non-blocking, record: T-100 names evidence it does not list

T-100's `composition` says the separation "adds E-lifted-q7-upper", but its `evidence` list and scope (n = 19) do not include it.

**Fix:** add it, or say the separation is cited from n = 18's record.

### FN-7: note, `SOUNDNESS.md`: `a_r` means two different things

The Theorem uses a_r = B(cos θ_r + sin θ_r)/2, while lemma N0 uses a_r = max(0, t_r − D/2). The mathematics is right, but the reuse invites misreading.

**Fix:** rename one of them.

## Significance

**T-099: S3, unchanged.** It is the same kind of result as T-096 (S3): the same certificate kind and checker, and a finer net that the same driver reads from the candidate. There is no new technique, as with T-074 and T-045 (S3).

**T-100: S3, unchanged.** It is a case bound like T-074, raised by 0.0054. The separation s(18) < s(19) is a corollary of that bound and Hämäläinen's packing. It is not a reusable technique, and it settles no disputed value. It answers a question raised on #281 by a margin of 2.43 × 10⁻⁵, which the rationale already records. S4 would need a method or a family of bounds.

## Disposition

**T-099: accepted as reported.** No blocking defect touches the certificate, the 832-node net, lemma N0 at step 1/2006, or the binding of the source's runs. As a read with a retained review, this review can support C1. V stays V0 and C goes no higher than C1 until a complete replay passes. That replay is a separate lane, and it must use `replay` after FN-1 is fixed, or a reviewed `sqverify-fast` route. Ten of 832 nodes, axis included, are reproduced with the producer's code. That decides those nodes only.

**T-100: accepted as reported, with the separation s(18) < s(19) conditional on it.** The same rung applies: C1 at most from this review, and V0 until a complete replay with the fixed `replay`. Ten of 416 nodes, axis included, are reproduced with the producer's code.

**What I did not check:**
- I ran no complete replay of either certificate, and did not price one beyond the samples.
- I did not run `control` or `sqverify-fast`.
- I did not re-review the soundness of the C++ checker. I relied on the 28 September and 2, 3 and 5 October reviews, and only skimmed its domain and header handling.
- I did not recompute the axis integer tables, beyond the source's replay of node 0 in the samples.
- I did not check the redaction's "before" bytes, which are not published.
- I did not check the source's `sqverify-net` runs and controls, which I deliberately did not read.
- I did not check the GitHub comments or issue #281, because I had no network access.
- I did not run `packing-validate`.
- I did not read `result-import.md` stage 4 in full; my search for its section did not match.
- My coverage search is binary64 and heuristic, and decides nothing.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
