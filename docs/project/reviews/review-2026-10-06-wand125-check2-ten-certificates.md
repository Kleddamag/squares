# Review: wand125's Ten Declared-Net Certificates of 6 October (T-108 to T-117)

**Verdict: accept all ten claims as stated: T-108 to T-117 at V0/C0, with no change to significance.** The argument from each certificate to its bound holds on all three declared nets. I re-derived lemma N0's premises in exact rationals for each net. The 2073-node net of step 1/5002 at core 4999/5000 meets every premise, and it is inside the scope the declared-net soundness review accepted for `sqverify_fast`. Every candidate is an exact, nonnegative, D4-averaged rectangle measure of mass n − 1/100000, inside its container.

Several independent checks agree with the source:

- **Control witnesses.** I wrote my own exact capture evaluator, apart from both checkers. It reproduces, digit for digit, the exact capture of every control witness in all nine check2 control logs (277 witnesses). Each witness lies in its node's per-bin domain and is exactly below 1, so every control is a provably invalid measure.
- **Falsification search.** A search near the least-bound boxes of 27 nodes found no capture below 1.0015.
- **The C++ checker.** The source's C++ checker (`89b674a6…`) verifies the least-bound node of `mixed_n41_L6775` (index 409) and of `mixed_n18_L4705` on the 1/5002 net (index 1234).
- **n = 29.** All 415 shipped oblique records and their inputs are bound to lemma N0's tangent, its per-bin domain at half-step 1/2002, threshold one and the expanded candidate.

**One finding blocks the binding records, not the claims (FN-1).** In eight of the nine check2 bundles, the verifier's own summary reports an input file whose SHA-256 is not the published `candidate.json`'s. This holds for n = 19, 20, 26, 27, 28, 30, 39 and 41. The records say the source's receipt reports a run "of this candidate", and no check in `audit_check2` or `bundle_check2` reads that digest.

The other findings are non-blocking:

- the control binding in the tool is weak (FN-2);
- a verifier version note describes C++ samples that did not exist at `eb004e7c5` (FN-3);
- the confirmation labels need their reasons written down (FN-4);
- three case records' Status paragraphs are stale (FN-5);
- the bundles' own comparisons are stale (FN-6);
- one platform attribution is not in the records (FN-7).

The `independent-implementation` label for T-114 and `shared-components` for a check2 replay are the right readings of `epistemics.md`, with the qualifications in FN-4. The adapted crate's `SOUNDNESS.md` and `INDEPENDENCE.md` are this repository's 3 October files by Git blob, as the packet says.

This review was written on 2026-10-06 by an AI agent (model `claude-opus-5-5`, tbd-strong tier), separately prompted as the adversarial reviewer of lane R7's import. It shares no context with that lane. It registers nothing and moves no bound.

## Scope and Evidence

**What I read.** The branch diff `ebf232767..eb004e7c5`. The packet README, `acquisition/declaration.json`, `sources.json`, `upstream-subtree.sha256` and all twenty receipts. The ten retained candidates, the source READMEs, `bundle.json`, `files-sha256.json`, the receipts, the controls and the pre-publication receipts. `devtools/audit_wand125_declared_net.py`: `measure`, `declared_net`, `audit_check2`, `bundle_check2`, `cpp_sample`, `check_node_manifest`, the CLI. T-108 to T-117 and their evidence entries, `V-wand125-sqverify-proof-net`, the C++ verifier's version list, the coverage, bibliography and intake-watch entries, and the ten case records' frontmatter and Status paragraphs. Lemma N0 in `packing/sqverify_fast/SOUNDNESS.md`. The declared-net soundness review's verdict, scope table, checklist (b) and re-review triggers. `epistemics.md` (Confirmation, Which Code Confirmed It, Significance). The significance entries of T-068, T-074, T-090, T-096, T-099 and T-100.

**What I read from the bundles.** The bundles' data and prose: `SPEC.md`, `REPRODUCE.md`, `UPSTREAM_COMMIT` and `fine_net_check.sh`, the run and control logs, and the n = 29 bundle in full.

**What I did not open.** I did not open, list, unpack, build or run `sqverify-proof-net-fe12e036c.tar.gz`, and I did not read either `SOUNDNESS.md` or `INDEPENDENCE.md` from the bundles. I unpacked the check2 tarballs with those three members excluded, and digested each by streaming it from the outer tarball to `sha256sum` and `git hash-object`. The first-party tool's own `bundle --tarball` and `cpp-sample` extract them to disk in order to hash them. Those twelve copies in my scratch were deleted unopened.

**What I ran.** All runs were at `nice -n 15` and one thread, using the project's Python 3.14 (`packing/.venv/bin/python3`), with `-I` for anything reading the bundles. My scripts are under `…/r7/review/work/scripts/`.

| Check | Command or script | Result |
| --- | --- | --- |
| Tarball digests and sizes | `sha256sum`, `stat` on the ten tarballs | all ten equal `upstream-subtree.sha256` and the packet's Prices table |
| Adapted crate and documents | streamed digests from each check2 tarball | tarball `e495f9bf…` in all nine; `SOUNDNESS.md` blob `cadf59b6…`, `INDEPENDENCE.md` blob `9b60b4af…` in all nine |
| Those blobs in this repository | `git rev-parse <commit>:packing/sqverify_fast/…`, `git log --find-object` | `cadf59b6…` is `SOUNDNESS.md` at `b2c98e3bd` (2026-10-03 15:05Z), introduced there and replaced at `f007d7afd`. `9b60b4af…` is `INDEPENDENCE.md` at `61acc9dcb` (2026-10-03 06:15Z), introduced there, unchanged at `b2c98e3bd`, replaced at `f007d7afd` (2026-10-05) |
| `UPSTREAM_COMMIT` `42534d95…` and `fe12e036c` | `git cat-file -t` | neither is in this repository |
| Measure and digest | `cand.py`: exact Fractions, duplicate-key refusal | all ten: n and L are the claim's; every row has nonnegative mass and is nondegenerate in [0, L]²; no points; Σ mass = `total_mass` = n − 1/100000; L² ≥ 2B². The semantic digest recomputed by the source's rule equals the stated one and every `scaling_source_digest` |
| Lemma F3's density cap | `dens.py` | 8 × densest row ≤ 5.24 × 10⁶ ≪ 2³² for all ten; least rectangle side ≈ 0.0010 |
| Net premises | `net.py`, exact | see the next section |
| Run logs | `runlogs.py` | for all nine: indices exactly 0 … last; every record `verified` at threshold `"1"` with lower bound ≥ 1; oblique nodes sum to the summary; summary = the receipt's `verifier_summary`; least nodes and axis bounds as the packet's table states |
| Verifier input digest | from each `verifier_summary.premises.input_sha256` | equals `sha256(candidate.json)` only for n18 (**FN-1**) |
| Control witnesses | `controls.py`, my evaluator: Sutherland–Hodgman clip of the rotated core against each of the 8·k expanded rectangles, area by the shoelace formula, all in Fractions | 29 + 8 × 31 = 277 witnesses: each in its per-bin domain, each scaled capture exactly below 1, each **equal** to the log's `exact_coverage` rational. Factor 197/200 exactly in all nine. The n19 control's axis refusal at its logged vertex evaluates to 0.98858904 < 1 |
| Falsification search | `search.py`: 1,000 random centres over [L/2, L − ρ(a_r)]² plus 200 around the least-bound box, pattern search from the best five, exact re-evaluation at the minimiser | 27 nodes (2 least-bound + 1 random per check2 certificate); least exact capture found 1.0015805 (n39, r = 204); n18 r = 1234 at 1.0135575 |
| n = 29 records | `n29.py` | 1,266 listed files match, none unlisted. All 415 oblique `result.json`: `ANGLE_VERIFIED`, empty frontier, no witnesses, lower ≥ 1, t = r/1001, per-bin floor (2r − 1)/2002, `centre_low` = ρ(floor), `centre_high` = L − ρ, E = L/2 − ρ, `input_sha256` = the input's bytes, header lines enclosing (L, B, E, cos, sin, 1), 4040 rectangles. Every `replayed.json` agrees. Nodes 128,316,129; 152,187 s = 42.27 h; least 1.000000000892745 at 364; axis `AXIS_VERIFIED` over 11,309,769 cells, 72324513115955573/72057594037927936. The ten `code/` files and `requirements.txt` are byte-identical to the retained `mixed_n50_L740` copies. `proof/verify.cpp` and `code/mixed_rotated_verify.cpp` are `89b674a6…`. `proof/candidate.json`, `certificate.json` and `manifest.json` equal the retained files |
| Exact audit | `audit_wand125_declared_net audit --certificate X --check` for all ten | `RECEIPT_MATCHES`, exit 0 |
| Tool tests | `pytest tests/test_audit_wand125_declared_net.py` | 75 passed in 6.2 s |
| Tarball binding | `bundle --tarball … --out <scratch>` for n18-L4705 and n41-L6775 | `BUNDLE_BOUND_TO_PACKET_AND_NET`; receipts identical to the packet's |
| Packet integrity | `acquire_source wand125-mixed-bounds-check2-2026-10-06 --check`; `retained_data check <packet>` | `PACKET_MATCHES_ITS_CONTRACT`; exit 0 |
| C++ checker | `cpp-sample --certificate n41-L6775 --nodes 409` and `--certificate n18-L4705 --nodes 1234`, `--out` to scratch | both `SAMPLE_VERIFIED`. n41 r = 409: `ANGLE_VERIFIED`, lower 1.0000001768444517, 475,593 nodes, no frontier or witnesses, 324.2 CPU s. n18 r = 1234: `ANGLE_VERIFIED`, lower 1.0000000050433526, 185,673 nodes, 147.9 CPU s. g++ 13.3.0, load average about 17 on four cores |

My computation totalled about 15 CPU-minutes. The working tree is unchanged (`git status --short` is empty).

**Not checked.**

- Coverage at any node but the two C++ nodes. No complete run of any checker, as the brief required. The census is a separate lane.
- The adapted crate itself, and whether the source's runs used it as stated.
- The pre-publication runs beyond their receipts.
- The search code and the provenance notes beyond reading them.
- Whether `42534d95…` exists on GitHub.
- The C++ checker's internals. It was read by the reviews behind T-096 and T-099, and I took their acceptance as given.

## The Argument From Certificate to Bound

Each candidate gives a measure g = Σ_j (w_j / (8|R_j|)) Σ_{S ∈ D4} 1_{S(R_j)} on K = [0, L]².

- **The measure.** g is nonnegative because every w_j ≥ 0 (checked exactly). It is D4-invariant by construction. It is exact, because every decimal parses to its literal rational. It has no atoms, so the boundaries of closed cores carry no mass. It integrates to M = n − 1/100000 < n, with every rectangle inside K. The threshold is Γ = 1, so M < nΓ.
- **Orientations.** A unit square's angle φ is defined modulo π/2. If φ > π/4, reflect the configuration in y = x, which preserves K, g and disjointness and sends φ to π/2 − φ. So φ ∈ [0, π/4], and tan(φ/2) ∈ [0, √2 − 1].
- **Net.** Nodes are t_r = rD for r = 0 … m. If (c) mD > √2 − 1, every u ∈ [0, √2 − 1] has a node with |u − t_r| ≤ D/2. The rotation between the square and the core at θ_r then satisfies z = tan(δ/2) = |u − t_r|/(1 + u t_r) ≤ D/2.
- **Containment.** The concentric core of side B at θ_r, seen in the unit square's frame, has extent B(cos δ + sin δ) = B(1 + 2z − z²)/(1 + z²) along each axis. This increases in z on [0, √2 − 1] and is at most B(1 + 2z) ≤ B(1 + D). Under (b) the core is therefore strictly inside the open unit square, and hence in K.
- **Centre domain (per-bin).** A unit square assigned to node r has u ≥ a_r = max(0, t_r − D/2). Its half-width ρ(u) = (1 + 2u − u²)/(2(1 + u²)) increases on [0, √2 − 1], so its centre, which is the core's centre, lies in [ρ(a_r), L − ρ(a_r)]². The last bin straddles √2 − 1. Its orientations are those in [a_m, √2 − 1], and ρ(a_m) is still the least, because the fold is at π/4, not at the net's end.
- **Counting.** Distinct squares have disjoint interiors, so their cores are pairwise disjoint closed sets in K. If every core at every node and admissible centre captures ∫ g ≥ 1, then n ≤ Σ ∫_{Q_i} g ≤ ∫_K g = M < n, a contradiction. So s(n) ≥ L.

The checkers assume only these hypotheses, plus coverage, which they decide. The source's `SPEC.md` §3–4 states the same argument, with the same per-bin formula and the same endpoint condition (1 + mD)² > 2.

**The three nets, exactly.**

| | step 1/5002, B = 4999/5000, m = 2072 (n18, n19) | step 1/2006, B = 1999/2000, m = 831 (n20, n26, n27, n30) | step 1/1001, B = 999/1000, m = 415 (n28, n29, n39, n41) |
| --- | --- | --- | --- |
| (a) D > 0, 2 ≤ N ≤ 2¹⁶ | N = 2073 | N = 832 | N = 416 |
| t_max = mD | 1036/2501 ≈ 0.4142343 | 831/2006 ≈ 0.4142572 | 415/1001 ≈ 0.4145854 |
| (c) t² + 2t − 1 | 367/6255001 > 0 | 497/4024036 > 0 | 1054/1002001 > 0 |
| t_max − tan(π/8) | 2.074 × 10⁻⁵ (< D/2 = 9.996 × 10⁻⁵) | 4.367 × 10⁻⁵ | 3.719 × 10⁻⁴ |
| (d) t_max ≤ 1/2 | yes | yes | yes |
| (b) B(1 + D) | 25009997/25010000, margin 3/25010000 ≈ 1.1995 × 10⁻⁷ | 4011993/4012000, margin 7/4012000 | 500499/500500, margin 1/500500 |
| Largest B under (b), 1/(1 + D) | 5002/5003; B is below it by 3/25015000 | 2006/2007 | 1001/1002 |
| Sharp extent B(1 + D − D²/4)/(1 + D²/4) | 500400014977/500400085000, margin 70023/500400085000 ≈ 1.399 × 10⁻⁷ | 32192229833/32192290000 | 4007994993/4008005000 |
| (e) B(1 + D/(1 − D²/4)) | 500400014977/500400075000, margin 60023/500400075000 ≈ 1.1995 × 10⁻⁷ | 32192229833/32192286000 | 1335998331/1336001000 |
| Per-bin half-step | 1/10004 | 1/4012 | 1/2002 |
| Last bin [a_m, t_m + D/2] | [4143/10004, 4145/10004]; tan(π/8) − a_m ≈ 7.92 × 10⁻⁵ > 0 | [1661/4012, 1663/4012]; 2.06 × 10⁻⁴ | [829/2002, 831/2002]; 1.28 × 10⁻⁴ |
| F3: D > 2⁻¹⁸ | yes | yes | yes |

On the 1/5002 net, the node nearest tan(π/8) is the last one: tan(π/8)/D ≈ 2071.896. Every orientation in [0, π/4] has a node within half a step in half-angle tangent. The offset obeys z ≤ 1/10004, which gives B(cos δ + sin δ) ≤ 1 − 70023/500400085000 at the worst. The last node reaches past tan(π/8) by 2.07 × 10⁻⁵, and its bin still holds orientations in [4143/10004, √2 − 1].

Every figure in the packet's net table and in each audit receipt's `net` block equals mine. The core margin on this net is about 1.2 × 10⁻⁷. That is tight but exact, and only admission uses it; no float in the branch and bound depends on it.

**Scope of the crate's acceptance.** The declared-net soundness review accepted `d97758bb…` for a format M certificate on a declared `proof_net` whose premises lemma N0 states. It found N0 "correct and complete for every net admission accepts", and it requires another review only for a net outside N0, a non-uniform or listed-node net, or a format other than M. The 1/5002 net is uniform, declared exactly as `{step, last}`, and meets (a) to (e). It also meets checklist (b) item 1 of that review:

- points are empty;
- `scaling_factor` is `"1"` or absent, and the census test reads an absent field as `"1"`;
- there is no top-level `net` key;
- 8 × the densest row is ≤ 2³².

The crate's cap is `MAX_ANGLE_COUNT = 1 << 16`. The census tool after DR-1's fix takes the step from `proof_net` (`check_sqverify_fast.net_step`), and this branch adds only the packet to `MIXED_PACKETS`. Item 7 of that checklist asks that a review read the certificate and accept it, and this review does so for all ten. The review's own exact table covered only the 1/2006 and 1/1001 nets; the 1/5002 row above supplies the missing one.

## What Check2 Changes and Which Code Confirms It

**The format does not change.** Each check2 candidate is format M: `{rectangle, mass}` rows, D4-averaged, empty `points`, `B`, `total_mass` and `proof_net {step, last}`. This is T-099's format and the source's `SPEC.md` §2. T-099's `mixed_n18_L4704` was on the 1/2006 net. n18 and n19 here declare the finer 1/5002 net.

**The claim is bound to the candidate, except in one place.** Each `bundle.json` states n, L, B, the net, the mass, the semantic digest and the file SHA-256, and these equal mine. Each receipt states the same digest and file SHA-256. The run log's summary is the receipt's, and its premises carry this L, B, D, count and mass, with format M and a per-bin domain. The controls are of this candidate scaled by 197/200: every witness capture equals my exact evaluation of the published candidate scaled. The pre-publication receipts name the published file's bytes as `input_sha256`.

The exception is the verifier's own record of what it read. In the published run logs of eight bundles, `verifier_summary.premises.input_sha256` is another file:

| Certificate | Published `candidate.json` | Verifier's `input_sha256` |
| --- | --- | --- |
| n19 | `f6b0c354…` | `9132b84e…` |
| n20 | `45a17658…` | differs |
| n26 | `842bee84…` | differs |
| n27 | `210af226…` | differs |
| n28 | `8438a806…` | differs |
| n30 | `32f2e77d…` | differs |
| n39 | `c05781e7…` | differs |
| n41 | `854e8b34…` | differs |

The n19 to n41 receipts are not the output of `fine_net_check.sh`, which would copy the verifier's input digest beside the file digest. They are a different wrapper, "copied" at upload time, whose `file_sha256` and `candidate_digest` are computed on the published file. No re-serialization I tried reproduces the input digest: indents 1, 2 and 4 or none, sorted or unsorted keys, compact separators, a trailing newline, with or without the scaling fields. So the logged runs read a file whose bytes are not published.

The equality of the 277 control captures on the published measure, and the matching counts, mass and expanded-rectangle totals, make it very likely that the measure is the same. The pre-publication runs read the published bytes but published no log. FN-1 covers this.

**Which code confirms it.** `epistemics.md` defines the relation by how the deciding program stands to "the code the result's producer used".

- **Check2 (T-108 to T-113, T-115 to T-117).** The producer decided these with `sqverify-proof-net` (build `ab6e33e1…`), which is this repository's crate with one change to its net reader. A replay here by `sqverify-fast` `d97758bb…` is not the producer's checker by digest, so it is not `same-implementation`. It shares the crate's parser, loader, interval kernel, branch and bound and axis sweep, so it is not `independent-implementation`. `shared-components` is the right reading, but the record should state two things:
  - The shared component is nearly the whole program, all of it but the declared-net reader. The replay is much closer to reproduction than the label suggests.
  - The direction is reversed: the producer reused our code, while the definition's sentence describes a confirmer reusing the producer's.
- **T-114.** The claim the source publishes rests on `mixed_rotated_verify.cpp` (`89b674a6…`), whose 415 records and replay ship in the bundle. `sqverify_fast` shares no code with it, and its `INDEPENDENCE.md` records the clean room. `independent-implementation`, as for T-099 and T-100, is right. But the source's n = 29 README also reports a pre-publication run of the adapted crate, 416/416 in 584 s, so the producer did run a copy of our crate on this candidate. The label holds because the claim rests on the C++ records and that run has no published receipt. The record mentions the run and does not give that reason (FN-4).
- **The C++ checker on check2 candidates.** The packet and records say that a C++ run "shares no code with" the crate. That is true. But the C++ checker is the producer's own code. A complete run of it here would be the producer's code re-run, not an independent re-implementation, even though it is independent of the crate. Its value is diversity against the crate, and the records should not later call it independent confirmation (FN-4).

**The blob claims are correct.** The adapted crate's `SOUNDNESS.md` is Git blob `cadf59b6…`, which this repository introduced at `b2c98e3bd` (3 October) and replaced at `f007d7afd` (5 October). Its `INDEPENDENCE.md` is `9b60b4af…`, introduced at `61acc9dcb` (3 October) and replaced at `f007d7afd`. So the adapted crate's soundness document predates lemma N0, as the packet says. `SPEC.md` §5's statement that the lemmas "are stated for a general step D" is the source's paraphrase. Here lemma N0 is what supplies that.

## The Source's Runs

**Check2 run logs.** For every bundle:

- one record per node r = 0 … m;
- each `verified` at threshold `"1"` with a certified lower bound ≥ 1;
- the axis by `axis-vertex-sweep` and every oblique node by `interval-branch-and-bound`;
- nodes summing to the summary;
- the summary byte-for-byte the receipt's;
- `fault_injected_at_box` null and `refused_directions` empty.

The least oblique bounds and indices, the axis bounds, the node totals and the seconds are those in the packet's Claims and Prices tables. The n18 run was on x86_64 Linux at 6 threads, 2,877.8 CPU s. The others were on arm64 macOS at 4 threads, with the CPU recorded as −0, so their direction seconds are the price. Pre-publication runs on x86_64 took 490 to 1,411 s, as stated.

The "least oblique bound" of about 1 + 10⁻¹⁰ is a branch-and-bound stopping artefact, not a margin. At n18's least-bound box (r = 1234) the exact capture at the box centre is 1.0944. The least capture my search found at that node is 1.01356. At every node searched, the true minimum appears to be 0.15–1.6 % above 1.

**Controls.** Every control scales all masses by exactly 197/200, giving mass (n − 10⁻⁵) × 197/200, for example 374299803/20000000 at n = 19. Each is on 32 directions spread over the net, with the same L, B, D and count, at threshold 1, and `REFUSED`:

- n18: 29 refused, 29 with exact witnesses. Its axis and two oblique directions verify at the scaled mass.
- The other eight: 32 refused, 31 with exact witnesses, plus the axis refused by the vertex sweep.

I re-evaluated every witness exactly with my own code. Each centre lies in its node's per-bin domain, each scaled capture is below 1, and each equals the logged `exact_coverage` rational exactly. So each control is provably an invalid certificate, and the source's exact capture agrees with an implementation that shares nothing with it. The n19 axis refusal evaluates to 0.98858904 at the logged vertex.

A 197/200 control shows that the checker can refuse. Because the true minima are 0.15–1.6 % above 1, it does not probe the threshold closely.

**n = 29.** The bundle is bound to the net and the expanded candidate: see the table above. Its checker is `89b674a6…`, and its driver `code/verify_mixed_full_proof.py` is `2719e482…`, byte-identical to the retained `mixed_n50_L740` code that the earlier reviews read. `bundle.json`'s platform (macOS-26.2-arm64, Python 3.14.7, NumPy 2.5.3) describes the replay that wrote it (`REPLAYED_PROOF_BUNDLE`). No per-node record carries a platform, and the run paths are `/opt/sp/runs/…` (FN-7).

**The C++ checker on two check2 nodes.** Both agree with check2 at the least-bound node of their logs:

- n41 r = 409: `ANGLE_VERIFIED`, lower 1.0000001768, against check2's 1.0000000001.
- n18 r = 1234 on the 1/5002 net: `ANGLE_VERIFIED`, lower 1.0000000050, against 1.0000000001.

In both, the manifest's tangent, per-bin domain, E, threshold and input digest are lemma N0's, and the input's rectangle lines enclose the expanded candidate. These two nodes decide nothing beyond themselves.

## Where the Records Stand

Every number I recomputed agrees with the records:

- masses, rectangle counts, cores, nets and margins;
- the semantic digests;
- least bounds and their indices, and axis bounds;
- node totals, seconds and platforms;
- tarball digests and sizes;
- the 15/9/5 file split of each check2 bundle;
- n29's 1,266 files, 415 records, 128,316,129 nodes, 152,187 s (42.27 h) and 11,309,769 axis cells.

**Gaps.** Each is checked exactly against the case's structured `verified_lower_bound`:

| Count | Claim | Gap |
| --- | --- | --- |
| 18 | 941/200 | 0.001 over 588/125 (T-099) |
| 19 | 193/40 | 0.0021 over 48229/10000 (T-100) |
| 20 | 981/200 | 0.005 over the reported 49/10 (T-077), 0.0075 over the verified 1959/400 (T-074) |
| 26 | 1109/200 | 0.0125 over 2213/400 |
| 27 | 11287/2000 | 0.0085 over 1127/200 |
| 28 | 1147/200 | 0.0125 over 2289/400 |
| 29 | 581/100 | 0.0125 over 2319/400 |
| 30 | 11767/2000 | 0.0085 over 47/8 |
| 39 | 133/20 | 0.015 over 1327/200 |
| 41 | 271/40 | 0.015 over 169/25 |

Every claim is below its case's best known packing.

**Supersession.** T-108 and T-109 supersede T-099 and T-100 in the reported lane only, as the records say. The other eight supersede the source's own 1 October rectangle certificates (T-068, T-077) in the reported lane.

**Monotonicity.** Nothing carries to a neighbouring count, because each count above holds a higher verified bound already:

- s(21) ≥ 5000/1001 against 4.905;
- s(31) ≥ 5.92 against 5.8835;
- s(40) ≥ 1339/200 against 6.65;
- s(42) ≥ 1363/200 against 6.775.

No new separation of s(n − 1) from s(n) arises either. T-074 already put s(20), s(27) and s(28) above the best packings of 19, 26 and 27 squares, and T-100 did so for 19 over 18.

**Sentences about what was done here.** They are accurate except the following:

- The packet README, the audit receipts' scope and every check2 evidence entry say the receipt reports the run "of this candidate". For eight bundles the verifier's own input digest says otherwise (FN-1).
- `verifiers.yaml` gives `V-wand125-mixed-rotated-verify-cpp` a version for "the C++ samples of the nine check2 candidates", which did not exist at `eb004e7c5`. The packet says "Not yet run" (FN-3).
- T-114's evidence attributes its run's platform to "the bundle's own records" (FN-7).
- The Status paragraphs of `n-026.md`, `n-029.md` and `n-030.md`, which this branch edited, still name 553/100 (T-045), 579/100 (T-070) and 1173/200 (T-045) as the verified lower bounds. Their frontmatter and lower-bound sections say 2213/400, 2319/400 and 47/8 (T-074). The text is older than this branch, but contradicts the records beside it (FN-5).
- The bundles' own `bundle.json` and README compare n18 with `mixed_n18_L470` (4.7) and n19 with `rect_n19_L48175` (4.8175). The root README says they supersede `mixed_n18_L4704` and `mixed_n19_L48229`. The packet follows the root README without noting the difference (FN-6).

## The First-Party Tool

**`audit_check2`** holds what its docstring says:

- the measure, as for every format;
- (a)–(e) exactly;
- the last bin, checked as (1 + (m − ½)D)² < 2;
- `bundle.json`'s claim, net block and digests;
- the receipt's status, count, failures, digest and file SHA-256, and its summary's threshold, fault field, refused list and L, B, D, count, mass, format and domain;
- the control's status and exit;
- the pre-publication receipt's status, verdict, counts, digests, build and control;
- every listed file by retained bytes or pin.

It does not read `verifier_summary.premises.input_sha256`, the only field the verifier itself wrote about its input. So it passes a receipt whose run read other bytes, which is what eight of nine do (FN-1). `control_refused` checks a status and an exit code only. It does not check the control's candidate (`candidate_file_sha256` in eight `control.json` files), its factor or its premises (FN-2).

**`bundle_check2`** checks the following:

- the listed files, with nothing unlisted;
- the retained list;
- the directory's files by bytes or pin;
- one run record per node, `verified` at `"1"` with bound ≥ 1 by the right method;
- the node total;
- the summary equal to the receipt's;
- one control log, ending `REFUSED`, with refused and witness counts as stated and mass ratio below 1.

The control check accepts any log whose mass is below this candidate's and whose counts match `control.json`. A control of another candidate would pass, and so would a factor other than 197/200 (FN-2). For this review, my exact recomputation of every witness closes that gap for all nine bundles.

**`cpp_sample`** decides what it says at the nodes it runs:

- the tarball is pinned and bound first;
- the checker is the retained `89b674a6…`, and its import path is asserted to be the fresh copy;
- the source's `candidate_net` must equal the declared net, and `symmetry` and the digest are rechecked;
- the budget is 4,000,000 nodes and the threshold is `Fraction(1)`;
- a node passes only on `ANGLE_VERIFIED` with an empty frontier, no witnesses and lower ≥ 1;
- `check_node_manifest` holds the tangent, the per-bin floor, ρ, E, the threshold, the checker digest and the input digest, the six header enclosures, the rectangle count and every rectangle line against the expanded candidate.

The axis node is refused as input, rightly, since `run` is oblique-only. The tool writes its receipt under the packet by default, and a reviewer must pass `--out` to avoid touching tracked files. That is not a defect. All 75 tests pass, and the audit receipts recompute byte for byte.

## Findings

### FN-1: The check2 run logs were made on a file other than the published candidate, and the records say otherwise

**Blocking for the binding records and the tool. Not blocking for the claims or for the replay lane.**

In eight of nine check2 bundles, `verifier_summary.premises.input_sha256` in `check2/run.jsonl.gz` and `check2/receipt.json` is not `sha256(candidate.json)`. Only n18's matches. The receipt's `file_sha256` and `candidate_digest` are the wrapper's, computed on the published file, so `audit_check2` passes. The packet README says the receipt reports every node "of this candidate and net … by a run that read this side, core, step, node count and mass", and the evidence entries repeat that the source's run was "bound to the declared net and its receipt". That overstates the binding. The run read that side, core, step, count and mass, from a file whose bytes are not published.

Mitigating evidence:

- the pre-publication receipts, which have no log, read the published bytes;
- every control witness's exact capture equals the published measure's scaled by 197/200.

**Fix:**

1. Make `audit_check2` and `bundle_check2` compare `premises.input_sha256` with the candidate's SHA-256, and report the result in the receipts. Refuse on a mismatch, or record it as a named exception.
2. Reword the packet README, the audit scope and the eight evidence entries to say the logged run read an unpublished file of digest X, with the same summary premises.
3. Optionally ask the source which file it was.

No coverage verdict depends on this, because the replay here reads the published bytes.

### FN-2: The tool does not bind the control to this candidate

**Non-blocking.** `bundle_check2` accepts any control log with mass ratio below 1 and matching counts. `audit_check2` reads only `status` and `exit`.

**Fix:** require the factor to be exactly 197/200 (or the stated factor). Hold the control summary's L, B, D and count to the candidate's, and `control.json`'s `candidate_file_sha256`, where present, to the candidate. Preferably also recompute each witness's exact capture on the scaled candidate, as `controls.py` does here in about 30 CPU-seconds per bundle.

### FN-3: A verifier version line describes runs that did not exist

**Non-blocking.** `V-wand125-mixed-rotated-verify-cpp` gains revision `2fad66e0` with the note "and the C++ samples of the nine check2 candidates", while the packet says "Not yet run".

**Fix:** keep only the n = 29 bundle in that note until a `cpp-sample` receipt is committed.

### FN-4: The confirmation labels need their reasons recorded

**Non-blocking.**

- **Check2.** `shared-components` is right. The future census evidence should list the shared component as "the `sqverify_fast` crate: all of it but the declared-net reader". It should also say that the producer adapted this repository's code, not the reverse, so that no reader takes the replay as more independent than it is.
- **T-114.** `independent-implementation` is right because the published claim rests on the C++ records. The evidence should give that reason beside its mention of the source's pre-publication run of a copy of this crate.
- **The C++ checker.** Any C++ run here on a check2 candidate is the producer's code. It should be recorded as such, `same-implementation` with respect to the producer, and never as independent confirmation, even though it shares no code with the crate.

### FN-5: Three case records' Status paragraphs contradict their structured bounds

**Non-blocking.** `n-026.md`, `n-029.md` and `n-030.md` were edited by this branch. Their Status paragraphs still name 553/100 (T-045), 579/100 (T-070) and 1173/200 (T-045) as the verified lower bounds, against `verified_lower_bound` 2213/400, 2319/400 and 47/8 (T-074).

**Fix:** update the three paragraphs.

### FN-6: The bundles' own comparisons are stale

**Non-blocking.** n18's `bundle.json` gives "compared_with 47/10, mixed_n18_L470, improvement 1/200". n19's gives 1927/400 (`rect_n19_L48175`) and 3/400. The root README says they supersede T-099's and T-100's certificates.

**Fix:** one sentence in the packet README noting that the bundle-level comparisons predate the root README's.

### FN-7: T-114's platform attribution is not in the records

**Non-blocking.** T-114's evidence says its oblique run was "on macOS (arm64) by the bundle's own records". The only platform recorded, in `bundle.json`, is the replay's. No per-node record names a platform.

**Fix:** say that the bundle's replay was on macOS arm64 and that the original run's platform is not recorded.

## Significance

S3 stands for all ten. Each is a substantive case result in the certificate kind and checker family of T-069 onward, on declared nets that are parameter choices. T-099 and T-100 are S3 for the same kind on the 1/2006 and 1/1001 nets, T-096 for the first declared net, and T-074 for the replayed rectangle bounds these supersede. None brings a new technique or a new separation of neighbouring counts:

- s(19) > s(18) was settled by T-100;
- s(20) > s(19), s(27) > s(26) and s(28) > s(27) were already settled by T-074's verified bounds.

The 1/5002 net is finer, but it is the same framework at a smaller step. The check2 form changes the source's checking practice, not the mathematics. Each rationale's "if the replay passes" is the right condition.

## Disposition

The mathematics of all ten is accepted. The argument, the nets, the measures and the bindings hold as above, subject to FN-1's correction of what the source's check2 logs bind.

| Result | Claim | Accepted | What this review supports |
| --- | --- | --- | --- |
| T-108 | s(18) ≥ 941/200 | yes | V0/C0 now. V3/C3 once the complete `sqverify-fast` replay over all 2073 directions passes with its census control, re-implemented sharing named components (the crate), and FN-1 is fixed |
| T-109 | s(19) ≥ 193/40 | yes | as T-108, 2073 directions |
| T-110 | s(20) ≥ 981/200 | yes | as T-108, 832 directions |
| T-111 | s(26) ≥ 1109/200 | yes | as T-108, 832 directions |
| T-112 | s(27) ≥ 11287/2000 | yes | as T-108, 832 directions |
| T-113 | s(28) ≥ 1147/200 | yes | as T-108, 416 directions |
| T-114 | s(29) ≥ 581/100 | yes | V0/C0 now. V3/C3 once the complete `sqverify-fast` replay over 416 directions passes, independently re-implemented. FN-1 does not apply |
| T-115 | s(30) ≥ 11767/2000 | yes | as T-108, 832 directions |
| T-116 | s(39) ≥ 133/20 | yes | as T-108, 416 directions |
| T-117 | s(41) ≥ 271/40 | yes | as T-108, 416 directions |

No result is confirmed by anything this review ran. My exact evaluator decided no direction. The two C++ nodes are samples: on n18 and n41 they are the producer's own checker re-run at one node each, and they decide only those nodes. This is one adversarial AI review. Rung 4 on either axis needs a second, by a distinct reviewer, and a human oversight record.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
