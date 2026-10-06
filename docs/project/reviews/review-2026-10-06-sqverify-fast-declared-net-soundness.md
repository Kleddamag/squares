# sqverify-fast on `main` (`d97758bb…`): Soundness Re-Review of the Declared-Net Change

**Verdict: accept** `source_sha256`
`d97758bbc9639edc70b8bd7dc83106d4e8d1be034bacb3e88f8c539b88091c88` as reviewed source
for the census route, for standard-net certificates of formats T, M and L and for format
M certificates on a declared net (`proof_net`). The crate keeps every soundness
obligation the 3 October soundness review checked.
Lemma N0 is correct and complete for every net admission accepts.
Admission refuses every malformed declaration tried here, and on every file it admits it
reports the net it decided on.
On the standard net, admission, the net, the domains, the search and the verdicts are
those of the reviewed source `7c49cf79…`: receipts are byte-identical on seven retained
certificates, and no retained candidate meets either new refusal.

The route does not yet carry to a declared-net certificate, and the reason is outside
the crate.
The census control’s independent evaluator, `check_sqverify_fast.mixed_exact`,
always uses the standard step 83/40000. On a declared net it scores the wrong angle: at
`mixed_n18_L470`’s least-bound leaf (index 408) it gives 1.2947, where the crate’s exact
capture is 1.0703. So no declared-net certificate can get a `CONTROLS_REFUSED` receipt
(DR-1, blocking for that scope only).
The failure is closed, not open: the receipt becomes `CONTROL_FAILED`, and no false
`verified` follows. Two further blocking findings are in the `--evidence` text.
It says a main build’s `src/` is unchanged since `4ddf37d9c` (DR-2), and it writes “201”
for every net (DR-3). Neither touches a verdict, and both must be fixed before an entry
made from a main build is pasted.

The verdict also covers `73959cae…` (the build of `f007d7afd`), for any certificate with
no top-level `net` key in a format T or M file.
On those files its admission is main’s, and its receipts on `mixed_n18_L470` are
byte-identical to main’s.

This review was written on 2026-10-06 by an AI agent (model `claude-opus-5-5`,
tbd-strong tier), separately prompted for lane R1 of the 2026-10-06 intake round.
It shares no context with that lane or with the lanes that wrote the change.
It registers nothing and moves no bound.

## Scope and Evidence

The subject is `packing/sqverify_fast/` at `34e87a86b` (`origin/main`, the merge of
jlevy/squares#369). It differs from the reviewed source `e020eb1e2` by two commits:
`f007d7afd` (the declared net, lemma N0) and `910b6b12c` (fixes for DN-2, DN-4 to DN-6
and DN-9). The census driver and check tool are also in scope, as changed since
`e38b78165`.

**Read in full:** `git diff e020eb1e2 34e87a86b -- packing/sqverify_fast`, and
`src/certificate.rs` at main (`read_json` and `DuplicateKeyVisitor`, `sources`,
`declared_net`, `admit`, `domain_upper`, `direction`). Also read:

- `src/lib.rs` (`run_direction_inner`, `premises`), `src/main.rs` lines 130–295
  (`parse_directions`, `probe`, `run`, the summary), and every use of `cert.step` and
  `cert.angle_count` in `rotated.rs`, `axis.rs` and `main.rs`, found by grep: `frame`,
  `verify_direction`, the confirm and probe paths, the axis sweep’s
  `domain_upper(cert, 0)`;
- `SOUNDNESS.md` at main and at `e020eb1e2`;
- `tests/declared_net.rs`, and `tests/adversarial.rs` in the parts on admission, the
  metadata net (TI-3) and the tangent form;
- the `INDEPENDENCE.md` and `independence-record.yaml` additions;
- the declared-net review (`review-2026-10-05-wand125-declared-net-n18-n66.md`) in full;
- the 3 October soundness review’s §1–§4.1, §4.6, §5’s headings, and §7 including §7.2,
  §7.3, §7.4, R1 and R2;
- the 3 October testing review’s TI-1 to TI-5, by heading and the parts the crate cites;
- the route review’s “The build that ran”, “The Confirmation Route” (including “Is it a
  complete replay?”), “Carrying the Route to T-082, T-090 and T-091” and IR-3, IR-4;
- `devtools/sqverify_fast_census.py`: `net_directions`, `mixed_reference`,
  `replay_status`, `run`, `direction_row`, `control` and `evidence_entry`, with the diff
  since `e38b78165`;
- `devtools/check_sqverify_fast.py`: `direction`, `read_raw`, `mixed_exact`,
  `mixed_mutant`, `summary_of` and `declared_net`, with the diff since `e38b78165`;
- `devtools/audit_wand125_declared_net.py`: `audit`, `rectangle_block` and `bundle`;
- `tests/test_sqverify_fast_census.py` lines 1–200.

**Not opened:** any `code/` folder or `proof/verify.cpp` under
`packing/resources/web/wand125-*`. No section of this review depends on the source’s
checkers, and none of the audit tool’s subcommands was run.

**Commands and results.** All of them ran in the worktree at `34e87a86b`, or in
`git archive` copies of `e020eb1e2` and `f007d7afd` under the worktree, which have since
been deleted. Python was `packing/.venv/bin/python3` (3.14.7) or `uv run --frozen`; Rust
was 1.98.0 (`rustc 1.98.0 (88d9e12ae 2026-08-18)`).

| # | Command | Result |
| --- | --- | --- |
| 1 | `git diff --quiet e020eb1e2 34e87a86b --` on `Cargo.toml`, `Cargo.lock`, `build.rs`, `rust-toolchain.toml`, `clippy.toml` | unchanged |
| 2 | `git diff --stat e020eb1e2 34e87a86b -- packing/sqverify_fast` | code changes only in `src/certificate.rs` (+98 −8), `src/lib.rs` (+3), `src/rotated_tests.rs` (+1), `tests/declared_net.rs` (+264, new); `axis.rs`, `rotated.rs`, `interval.rs`, `exact.rs`, `oracle.rs`, `main.rs` untouched |
| 3 | `git diff f007d7afd 910b6b12c -- packing/sqverify_fast/src` | one hunk: the 8-line `net`-block refusal in `admit` |
| 4 | scratch `srcsha.py` (build.rs’s rule, over `git show` blobs, from the repository root) | `4ddf37d9c` `9985c465…a7`; `e020eb1e2` `7c49cf79…00`; `f007d7afd` `73959cae…ba`; `910b6b12c` and `34e87a86b` `d97758bb…88`, all equal to the brief’s table |
| 5 | `cargo build --release -j 2` (main) | exit 0; binary SHA-256 `567a0fd58f7ae4e9…`; embeds `d97758bb…` |
| 6 | `cargo fmt --check` | exit 0 |
| 7 | `cargo clippy --release --all-targets -j 2` | exit 0, no warnings |
| 8 | `cargo test --release -j 2 -- --test-threads 2` | lib 13, `adversarial` 17, `declared_net` 8 passed; none failed or ignored |
| 9 | `packing-validate --only "measure verifier Rust"` | passed, 87.06 s, `SQVERIFY-FAST CHECKS PASSED` |
| 10 | `python -m devtools.check_sqverify_fast --binary … --only declared-net` (full) | 10 of 10 ok, the 0.985 mutant refused at 326 of 416 directions, each with an exact witness; 82 s |
| 11 | `pytest -q tests/test_sqverify_fast_census.py` | 20 passed |
| 12 | `git archive e020eb1e2`, `cargo build --release` | binary SHA-256 `af0871c0d7210aaa…`, the binary the route review names; embeds `7c49cf79…` |
| 13 | scratch `compare_builds.py`, reviewed build vs main, directions 0, 1, 57, 200, `--confirm`, on `cert_n11_L381`, `rect_n18_L4695` (T), `mixed_n37_L644`, `mixed_n42_L68475`, `mixed_n66_L843` (M), `mixed_n50_L735`, `mixed_n82_L932` (L) | every receipt and summary byte-identical after dropping timing fields, `build`, and main’s three added premises; `ALL IDENTICAL` |
| 14 | `git archive f007d7afd`, build, `compare_builds.py` vs main on `mixed_n18_L470` at 0, 1, 207, 408, 415 | embeds `73959cae…`; identical |
| 15 | main on `mixed_n18_L470` at 0, 1, 408, 415 vs the retained census rows | identical apart from timing |
| 16 | scratch `scan_nets.py` (the 203 census cases) and `scan_all.py` (every `*candidate*.json*` under `packing/resources/web`) | no format T or M file has a top-level `net`; no format T or L file has `proof_net` (details under question 3) |
| 17 | scratch `exact/net_premises.py` (Python `fractions` only, nothing imported from the crate or the tools) | all premises hold on the 832-node, 416-node and standard nets (question 1) |
| 18 | synthetic format M files on both nets through main’s binary | results under question 1 |
| 19 | scratch `exact/probes.py`: 22 declarations through main’s binary | results under question 2 |
| 20 | scratch `control_net.py`: `check_sqverify_fast.mixed_exact` at `mixed_n18_L470`’s least-bound leaf | 1.2947048866 against the crate’s 1.0703183550; `agree False` (DR-1) |
| 21 | seven mutated copies of main’s crate, each `cargo test --release --no-fail-fast` | every mutant fails at least one test (question 6) |

What failed along the way, and what was redone:

- The first digest script ran `git ls-tree` from `packing/`, which lists nothing there;
  rerun from the repository root with `--full-tree`.
- `/usr/bin/time` is not installed; wall time was taken from `date`.
- One wait loop used `pgrep -f` on a pattern its own command line contained.
  It was stopped, and every later wait polled a PID with `kill -0`.
- The first mutant pass ran `cargo test` without `--no-fail-fast`, so a failing
  `adversarial` suite hid `declared_net`; the whole pass was rerun.
- The first domain probe was too weak (question 1) and was redesigned.
- For about a minute a 2-thread receipt comparison overlapped a `cargo -j 2` mutant
  build, which is above the brief’s two-thread limit.

Nothing the brief asked for went unestablished because of a tool or permission failure.

## 1. Lemma N0 and Containment on Every Admitted Net

**What admission checks.** These are in exact rationals, in this order, on the net that
results after `proof_net` and any certificate metadata are read:

- (a) $D > 0$ and $2 \le N_\theta \le 2^{16}$;
- (b) $B(1 + D) < 1$;
- (c) $t_{\max}^2 + 2t_{\max} - 1 > 0$ with $t_{\max} = (N_\theta - 1)D$;
- (d) $t_{\max} \le 1/2$;
- then, once the format is known, for format M (`Domain::PerBin`), (e)
  $B(1 + D/(1 - D^2/4)) < 1$.

`declared_net` admits only `step` (an exact rational), `last` (a JSON integer with
`last + 1` fitting `u32`), and optionally `count = last + 1`. The step and count admit
writes into `Certificate` are the ones every later computation reads: `direction`,
`frame`, `domain_upper` and `premises`. They are the same for every net origin (read).

**The proof, checked step by step (read and re-derived):**

- *N1* uses only the spacing and (c).
- *N2* folds at $\pi/4$. For a folded orientation $u = \tan(\varphi/2) \in [0,
  \tan(\pi/8)]$ in bin $r$: when $r \ge 1$, $u \ge t_r - D/2 \ge D/2 > 0$; when $r = 0$,
  $t_r = 0$. Either way $1 + u t_r \ge 1$, so $z = |u - t_r|/(1 + u t_r) \le D/2$ for
  every admitted $D$.
- *N3*: $(1 + 2z)(1 + z^2) - (1 + 2z - z^2) = 2z^2 + 2z^3 \ge 0$, so the extent is at
  most $B(1 + 2z) \le B(1 + D) < 1$ by (b).
- *Lemma D:* $\rho(a) = (\cos\varphi + \sin\varphi)/2$ increases on $[0, \tan(\pi/8)]$.
  Every folded square assigned to node $r$ has $u \ge a_r = \max(0, t_r - D/2)$, so its
  centre lies in $[\rho(a_r), L - \rho(a_r)]$. A node whose $a_r$ exceeds $\tan(\pi/8)$
  only enlarges the checked set.
  The admitted $D$ enters `domain_upper` through `cert.step`, as the M5 mutant below
  confirms. An empty domain at some node is an `Err` and exit 2, never a skipped node.
- *F3:* $D = t_{\max}/(N_\theta - 1) > \tan(\pi/8)/(2^{16} - 1) > 2^{-18}$ by (a) and
  (c). Then $s_1 = 2D/(1 + D^2) > D$ since $D \le 1/2$, and $c_r \ge 3/5$ by (d). These
  are the bounds the code relies on: `frame` divides by the enclosures of the exact $s$
  and $c$, and every other F3 bound is in $L$, density, row count and $n$, which
  admission caps for every format alike.

The new code adds no new arithmetic path.
Every declared net admission accepts lies in the $(D, N_\theta)$ region that format T’s
metadata could already reach in the reviewed source.
The 3 October re-review tested that region’s extreme corner
(`lemma_f3_holds_at_its_extremes`). What is new is the per-bin domain at a non-standard
$D$, which is lemma D above.

N0 is correct and complete.
Condition (e) is not needed given (b); it can only refuse.
The parenthetical “sharp condition” is right: $D/2 \le 1/4 < \sqrt2 - 1$.

**The two nets the next lane needs, in exact arithmetic.** Computed with
`exact/net_premises.py`, which uses Python fractions alone:

| Net | $B(1 + D)$ | Reach polynomial | (e) | Least $\rho(a_r) - B(c_r + s_r)/2$ over nodes |
| --- | --- | --- | --- | --- |
| 832 nodes, $D = 1/2006$, $B = 1999/2000$ | $4011993/4012000$ (margin $7/4012000$) | $497/4024036 > 0$, $t_{\max} = 831/2006$ | $32192229833/32192286000 \approx 0.99999825527$ | $1.183 \times 10^{-6}$ |
| 416 nodes, $D = 1/1001$, $B = 999/1000$ (`mixed_n18_L470`) | $500499/500500$ | $1054/1002001$ | $1335998331/1336001000 \approx 0.99999800225$ | $2.247 \times 10^{-6}$ |
| standard, $B = 9977/10000$ | $399908091/400000000$ | $89/40000$ | $63985225828447/63999931110000$ | $1.205 \times 10^{-4}$ |

On each net, (a) and (d) hold, and $s_1 > 2^{-18}$ (for the 832-node net,
$s_1 = 9.970 \times 10^{-4}$). $\tan(\pi/8)$ lies in the last node’s bin.
At $L = 588/125$ and at $L = 47/10$ the per-bin domain is nonempty at every node.
At every node whose bin meets $[0, \tan(\pi/8)]$, the core at the node’s angle, with its
centre at the domain’s end, lies inside $K$: the last column is positive.
At nine sampled tangents per bin, N3’s extent is below 1 and $\rho(u) \ge \rho(a_r)$,
with no failure.

For `mixed_n19_L48229` on 416 nodes, (c) and (d) confine the step to
$D \in (\tan(\pi/8)/415, 1/830]$, that is
$(0.000998104970\ldots, 0.001204819277\ldots]$. A step $1/k$ is admitted exactly for
$k \in [830, 1001]$. The core must then satisfy $B < 1/(1 + D/(1 - D^2/4))$:

- at $D = 1/1001$, $B < 4008003/4012007 \approx 0.999001996$;
- at $D = 1/1000$, $B < 3999999/4003999 \approx 0.999000999$;
- at $D = 1/830$, $B < 2755599/2758919 \approx 0.998796630$, which refuses
  $B = 999/1000$.

**Synthetic format M files through main’s binary.** Each has one row, the whole
container $[0, L]^2$, so the density is uniform.
An inside core then captures exactly mass times $B^2/L^2$, so the verdict tests the
domain and the shrink step directly:

- `A832-uniform-tight` ($n = 5$, $L = 11/5$, on the 832-node net, an inside capture of
  $1 + 10^{-7}$): `VERIFIED`, 832 of 832 directions; least certified bound
  $1.0000000999999945$; premises `D 1/2006`, `angle_count 832`, `net_origin proof_net`,
  `net_last_tangent 831/2006`, `shrink_bound 4011993/4012000`, `centre_domain per-bin`.
- `B416-uniform-tight` (the same on 416 nodes at $1/1001$, $B = 999/1000$): `VERIFIED`,
  416 of 416; least bound $1.0000000999999952$.
- The `-short` versions, at an inside capture of $1 - 10^{-7}$: `REFUSED` at directions
  0, 1, 415 and 831 (respectively 0, 1, 207 and 415). Each oblique refusal carries an
  exact witness below the threshold.
- `A832-n18-L4704` ($n = 18$, $L = 588/125$, mass $1799999/100000$, $B = 1999/2000$) and
  `B416-n19-L48229` ($n = 19$, $L = 48229/10000$, $B = 999/1000$): admitted with the
  premises above; refused at the sampled directions with exact witnesses (least bounds
  0.8126 and 0.8152), as a uniform measure of that mass must be.
- `A832-n18-L4704` without its `proof_net` is refused at admission: “B (1 + D) >= 1”.

**A probe of the domain’s lower end.** I built a uniform density on $[w, L - w]^2$ on
the 832-node net, with $w = 78453939/250000000000$ and an inside capture of
$1 + 10^{-10}$. At node 400, the core with its centre at the correct domain’s end
$\rho(t_r - D/2)$ reaches within $1.972 \times 10^{-4}$ of the wall.
With its centre at $\rho(t_r)$, it reaches within $3.268 \times 10^{-4}$. The value of
$w$ lies between the two.

- Main’s binary refuses node 400 (`counterexample-candidate`, `exact_below_threshold`
  true).
- Mutant M1, whose bins drop the half step, verifies it (least bound
  $1.0000000000999965$): a false `verified`.

So the verifier itself separates the correct per-bin domain from a too-small one at a
non-standard step. My first version of this probe, with a $10^{-7}$ margin, verified
under both builds: a corner poking past the wall loses only about $6 \times 10^{-9}$ of
area. It was replaced, and is reported here only so that the record shows what was run.

## 2. Malformed Declarations

**Probes (main’s binary, `--directions 1`, on the `A832-uniform-tight` file):**

| Declaration | Outcome |
| --- | --- |
| `proof_net: null` | refused, “must be an object” |
| a second `proof_net` key; the same key spelled `proof_net` | refused by the reader: duplicate JSON key (the visitor compares decoded keys) |
| `last` `831.0`; `count` `"832"`, `832.0` or `null`; a nested `net` inside `proof_net` | refused |
| `last` `4294967294` ($2^{32} - 2$) or `-0` | refused by (a) |
| `last` 830 at step $1/2006$ | refused, “does not reach past pi/4” |
| step $1/1999$ at $B = 1999/2000$ | refused by (b) at equality |
| step `0.0005` as a JSON number; `"1000/2006000"` | admitted as $1/2000$ and $1/2006$; the summary’s `D` is that value |
| a 30-digit decimal near $1/2006$ | admitted as its exact literal, reported as that literal, a different net that meets (a) to (e) |
| metadata restating the net as `2/4012`, 832 | admitted, `D 1/2006` |
| metadata giving the standard net beside the declaration | refused (the metadata step replaces the declared one, and (b) fails before the metadata rule is reached) |
| `proof_net` only inside `certificate`; a key `"proof_net "` | ignored, so the file is on the standard net, where (b) refuses it |
| `net: null` in format M | refused, “declares no net block” |
| format L (`schema`) with `proof_net` | refused |
| the file gzipped | admitted, the same premises |

Together with the eighteen variants of `a_corrupted_declaration_is_refused` and the
declared-net review’s probes, I found no declaration that leads admission to decide on a
net N0 does not cover.
None leads to a reported net other than the one decided.
The reported values are `angle_count`, `D`, `net_origin`, `net_last_tangent` (computed
as `step × (angle_count − 1)`) and `shrink_bound` ($B(1 + D)$). All five are read from
the same `Certificate` fields the search uses.

`shrink_bound` is the half-angle form (b), not the stronger (e), which admission also
checked for format M. It is a true statement of a premise, not a claim of (e).

Format detection works as before.
Format L is chosen by `schema`; format M when the first `rectangles` row is an object;
format T otherwise. The format-specific refusals follow detection:

- `proof_net` outside M;
- `net` outside L;
- metadata that changes an M or L net;
- (e) for M.

A file cannot get the per-bin domain without being format M, and so without (e).

**The census count.**

- `run` sets the row’s status from the summary only when the number of per-direction
  rows equals the summary’s `premises.angle_count`, which is the net admission decided.
- The summary is `VERIFIED` only when the directions run equal `cert.angle_count` and
  all verified (`main.rs`). `run` passes `--directions all`.
- So a row cannot be complete on less than the net admission read.

`tests/test_sqverify_fast_census.py` compares that net with the file:

- `directions_verified` must equal `net_directions(case)`, which is
  `proof_net.last + 1`, else 201;
- the receipt’s indices must be exactly `range(total)`.

The two readers can differ only where the crate refuses: duplicate keys, a non-integer
`last`, a non-object `proof_net`, a multi-member gzip, which Python’s `gzip.decompress`
accepts.
Such a row is never `VERIFIED`. Where the crate admits, its count is `last + 1`,
which is Python’s.

So the count is closed.
The one remaining gap is the control (DR-1).

## 3. Nothing Changes on the Standard Net

**From the code (read).** For a file without `proof_net`, `declared` is `None`, so the
step and count start at $83/40000$ and 201, as before, and the metadata handling and the
five net premises are unchanged lines.
After `sources`, the net pin for M and L is the old condition written with constants.
`domain_upper`, `direction`, `axis.rs`, `rotated.rs`, `interval.rs`, `exact.rs`,
`oracle.rs` and `main.rs` are byte-identical to the reviewed source.

The only behavioural differences are additions:

- three summary fields;
- the refusal of a top-level `net` key in format T or M (`910b6b12c`);
- the refusal of a `proof_net` key in format T or L (`f007d7afd`). Before, such a key
  was ignored. The brief does not list it among the intended differences.

**Receipts (computed).** On seven retained certificates (two of format T, three of M,
two of L) at directions 0, 1, 57 and 200 with `--confirm`, the reviewed build
(`af0871c0…`, source `7c49cf79…`) and main’s agree byte for byte: every per-direction
receipt and the summary, after dropping wall and CPU times, `build`, and `net_origin`,
`net_last_tangent`, `shrink_bound`. Exit codes agree.
Main’s added fields read:

- `shrink_bound 399908091/400000000`;
- `net_last_tangent 83/200`;
- `net_origin standard` for formats M and L, and `metadata` for the two format T files,
  whose `certificate` block restates $83/40000$ and 201 (DR-5).

**Retained candidates (computed).** The 203 census cases are:

| Census family | Format | Count | Top-level net keys |
| --- | --- | ---: | --- |
| rectangle | T | 129 | none (metadata restates $83/40000$ and 201) |
| mixed | M | 69 | none |
| mixed | M | 1 | `proof_net` (`mixed_n18_L470`) |
| mixed | L | 4 | `net` |

Over every `*candidate*.json*` under `packing/resources/web` (207 certificate files),
the counts are 132 T, 69 M without either key, 1 M with `proof_net` and 4 L with `net`.
No format T or M file carries `net`, and no format T or L file carries `proof_net`.
Neither new refusal turns any retained census verdict into a refusal.

## 4. The Fixes of `910b6b12c`

- **DN-5** refuses any top-level `net` key outside format L, including `null` and the
  standard net (probed).
  It is a refusal only, it touches no admitted file in the tree, and it cannot create a
  `verified`. It refuses nothing the route needs.
  Mutant M4, which removes it, fails
  `a_net_block_outside_format_l_is_refused_not_ignored`.
- **DN-6.** I traced every one of the eighteen variants of
  `a_corrupted_declaration_is_refused` through `admit`, and each reaches the premise its
  expected message names (for example, `last 0` passes `declared_net` and is refused by
  (a), and the $2^{16}$-cap variant passes (c)). The duplicate-key test reaches the
  reader. The `declared-net` controls now match messages, and in run 10 each was refused
  by the rule it names.
  Example: the metadata step $1/1000$ meets (a) to (e) at $B = 999/1000$
  ($B(1 + D) = 999999/1000000$, $B$ below $3999999/4003999$), and is refused by “may not
  change it”. `metadata_may_restate_a_declared_net_but_never_change_it` is weaker: two of
  its four variants are refused by other premises, which its loose `contains("net")`
  accepts (DR-4).
- **DN-4.** $1335998331/1336001000$ and $0.99999800225$ are right (recomputed).
  N2 now reads “$t_{\max} + D/2$” and “the last node’s $\rho(a_r)$”, which is correct
  for every net.
- **DN-2.** `bundle` now encloses every input’s rectangle lines against the expanded
  candidate, as a multiset of eight images per row with density $m/8/|R|$ and a point
  count of 0, and holds every node’s lines byte for byte to node 1’s. The digest
  sentence of E-n018-wand125-mixed-470-report was corrected to “checks that one
  candidate digest is stated throughout”, which closes the other half.
  The check is containment only: it does not bound an enclosure’s width (DR-7). This
  tool serves the source-checker route and decides no `sqverify-fast` verdict.

No fix introduces a path to a false `verified`: the crate changes are a refusal and
tests.

## 5. The Census Driver and Check Tool Since `e38b78165`

`check_sqverify_fast.py` gained the `declared-net` group and nothing else.
`mixed_exact`, `mixed_mutant`, the differential and the controls are unchanged.

`sqverify_fast_census.py` changed in these places:

1. **The row status.** `run` now compares the row count with the summary’s `angle_count`
   instead of 201. On every standard-net file `angle_count` is 201, so no standard-net
   row’s status can change.
   For a format T file whose metadata declared another count, the row could now be
   complete on that net, which the 3 October reviews accepted.
   The census test still pins 201 for every cited entry.
2. **The control’s acceptance (`held`).** A refused mutant must now also capture below 1
   at the leaf’s centre or at the refusal’s witness.
   That only tightens.
3. **Labels.** `net_directions`, `mixed_reference`, `replay_status` and the reports.
4. **The evidence template.** It now names `ROUTE_REVIEW`, the stored and pinned
   digests, and the build sentence.

So for standard-net certificates nothing a row or a control receipt can claim has
loosened.
For declared-net certificates, the row is right, but the control is not (DR-1).
Its independent capture uses `check_sqverify_fast.direction(index)`, which is
`index × 83/40000` whatever the file declares.
The near-threshold factor, `captures_agree` and the mutants’ witness captures are all
evaluated at the wrong angle.

It fails closed. The control needs `captures_agree`, and the two angles’ captures differ
except by coincidence; at index 0 the angles coincide and the control is correct.
The `--evidence` text is wrong for any main build (DR-2) and for any declared net
(DR-3).

## 6. The 3 October Obligations

| Obligation | State at main | Evidence |
| --- | --- | --- |
| S1 (axis NaN) | unchanged | `axis.rs` byte-identical; `adversarial` S1 tests pass |
| S2 (fault injection never verified) | unchanged | `lib.rs` change is three `premises` lines; `a_fault_injected_run_is_never_verified` passes |
| S3 (fold at $\pi/4$) | holds on every net | N2 folds at $\pi/4$; DN-4’s edit removed the last $t_{200}$; M1 fails `per_bin_domain_needs_the_fold_at_pi_over_four` and the declared-net domain test |
| S4, I1 finiteness, NaN handling | unchanged | `interval.rs`, `rotated.rs` byte-identical; F3’s premises are the same checks, read by every net origin |
| S5 | unchanged |  |
| S6 (what tests could not catch) | improved | mutants below |
| F3’s caps | hold on every admitted net | question 1 |
| Format M’s shrink step | holds on every declared step | (b) for N3, (e) checked for every per-bin domain; M7 fails both tangent-form tests |
| Admission’s exact premises | same five checks, one more refusal | M2 and M6 are caught by both suites |
| R1 (N2’s “$\delta \le \arctan D$”) | closed | N2 says $\delta$ may reach $2\arctan(D/2)$ and uses only $z$ |
| R2 (audit tolerance) | unchanged, a note | A3 text says so |

**Mutation controls.** Each mutant is a fresh copy of main’s crate with one edit, run
with `cargo test --release --no-fail-fast`:

| Mutant | Edit | Tests that failed |
| --- | --- | --- |
| M1 | bins without the half step (`a = t`) | `per_bin_domain_needs_the_fold_at_pi_over_four`, `a_declared_net_replaces_the_standard_one` |
| M2 | no $B(1 + D) < 1$ check | `admission_refuses_each_broken_premise`, `without_its_declaration_…`, `a_corrupted_declaration_is_refused` |
| M3 | metadata may change an M or L net | `metadata_may_restate_a_declared_net_but_never_change_it` only (DR-4) |
| M4 | no DN-5 refusal | `a_net_block_outside_format_l_is_refused_not_ignored` |
| M5 | per-bin half step from $83/40000$ | `a_declared_net_replaces_the_standard_one` |
| M6 | reach polynomial on $N_\theta D$ | `admission_refuses_each_broken_premise`, `a_corrupted_declaration_is_refused` |
| M7 | no tangent form (e) | both tangent-form tests |

Every mutant is caught, and M1 also yields a false `verified` on the domain probe
(question 1) that main refuses.
M5 is the bug a declared net would most plausibly introduce, and it is caught only by
the declared-net test, because on the standard net the two half steps coincide.

## 7. Verdict

- **Standard-net certificates (formats T, M, L): accept `d97758bb…`.** It decides
  exactly what `7c49cf79…` decided, by code reading and by byte-identical receipts.
  Its two new refusals reach no retained file.
- **Declared-net format M certificates: accept `d97758bb…` as the crate.** The census
  route carries to such a certificate only after DR-1 is fixed, with that fix read by a
  reviewer as the route review requires for a change to control logic, and after DR-3.
  The certificate must also meet checklist (b) below.
- **`73959cae…`: covered**, for certificates with no top-level `net` key in a format T
  or M file, which is every retained one.
  Its source differs from main’s only by DN-5’s 8-line refusal (computed in run 3), and
  its receipts are identical on `mixed_n18_L470` (run 14). On a T or M file with a `net`
  block it ignores the block, and its verdict is still on the net its summary reports.
  That is sound, but the route should not rest on it.
  The existing `mixed_n18_L470` census row was built with it.

## Findings

### DR-1 — Blocking for the declared-net census route: the control’s independent evaluator ignores the declared net

`check_sqverify_fast.direction(index)` returns the angle at `index × STEP`, with
`STEP = Fraction(83, 40000)`. `mixed_exact` uses it for every certificate, and the
census `control` uses `mixed_exact` for the independent capture, the near-threshold
factor and the mutants’ witness captures.

The evidence is run 20. At `mixed_n18_L470`’s least-bound leaf (index 408, centre
`(3.445831961381131, 3.9656702563847714)`), the tool evaluates half-angle tangent
$4233/5000$ instead of $408/1001$. It gets $1.2947048866$ against the crate’s
$1.0703183550$, so `captures_agree` is false and the receipt would be `CONTROL_FAILED`.

This fails closed, but it means the route cannot carry to any declared-net certificate.

The fix:

- have `mixed_exact` take the step from the file’s `proof_net`, or better from the
  summary’s `premises.D`, and refuse a file whose two disagree;
- add a test that recomputes one declared-net control capture from the candidate, as
  `test_one_control_capture_is_recomputed_from_the_candidate` does for `mixed_n67_L848`;
- have a reviewer read the change before a declared-net control receipt counts.

### DR-2 — Blocking for an evidence entry from a main build: the build sentence is false

`evidence_entry` writes that the build’s “src/, Cargo.lock and build.rs are unchanged
since 4ddf37d9c”, and that the digest differs from `9985c465…` “only because Cargo.toml
gained the gate’s test profile”.
For a `d97758bb…` build both are false (runs 2 and 4). Nothing about the verdict
changes.

The fix: state, per accepted digest, which review accepted it.
For `d97758bb…`, name this review and the declared-net change, and update
`REVIEWED_BUILD` and `REVIEWED_SOURCE`.

### DR-3 — Blocking for a declared-net evidence entry: the template writes 201

The `--evidence` text says “at all 201 net directions”, “the net of 201 half-angles of
step …” and “the other 200 by interval branch and bound”, and the `replay` text says “at
all 201 net directions”.
For `mixed_n18_L470` these would be false.

The fix: take the count from `premises.angle_count`, the step from `premises.D`, and the
oblique count as `angle_count − 1`; name the net’s origin.

### DR-4 — Non-blocking, tests: the metadata rule is held only for format M, and loosely

Of `metadata_may_restate_a_declared_net_but_never_change_it`’s four variants:

- `{"D": "83/40000"}` is refused by (b);
- `{"angle_count": 201}` is refused by (c), whose message contains “net”, which the test
  accepts.

In `tests/adversarial.rs`, both of `format_l_and_m_nets_cannot_be_overridden`’s variants
are refused before the metadata rule: format L’s by (d) ($t_{\max} = 9/10$), format M’s
by (c). Mutant M3 is caught by the declared-net test alone.
A mutation that disabled the rule for format L only would pass every test.

The fix: give each variant a net that meets (a) to (e), and match “may not change it”,
for format L as well as M.

### DR-5 — Note, receipts: format T reports `net_origin` `metadata` when its metadata only restates the standard net

Every retained format T file carries `certificate.D = 83/40000` and `angle_count = 201`,
so its summary says `metadata`. The value is accurate as to where the net came from, but
a records lane must not read `metadata` as “non-standard”.
No change is needed.
If one is wanted, report `standard` when the metadata net equals it.

### DR-6 — Note, scope of the change: `f007d7afd` also refuses a `proof_net` in format T or L

The brief lists DN-5’s refusal and the three fields as the only intended differences.
The refusal of `proof_net` outside format M is a third.
It is a refusal only, and no retained file has the key (question 3), so no verdict
moves. `SOUNDNESS.md` already states it.

### DR-7 — Note, source-checker route only: `rectangle_block` checks containment, not width

`rectangle_block` requires each input line’s ten hexadecimal ends to contain the image’s
exact coordinates and density.
A line with very wide enclosures passes.
Whether that matters depends on which end of each enclosure the source’s checker uses,
and this review did not open the checker.

The fix: bound each enclosure.
For example, require each end to be within a few units in the last place of the exact
value, or to be its directed binary64 rounding, as an input generated from the exact
candidate would be. This does not affect the census route.

## Disposition

`d97758bb…` is accepted as reviewed source for standard-net certificates now, and for
declared-net format M certificates once DR-1 and DR-3 are fixed and DR-1’s fix has been
read. DR-2 must be fixed before any `--evidence` entry is made from a main build.
DR-4 should be fixed with DR-1. DR-5 to DR-7 need no action for the route.
`73959cae…` is covered as stated under question 7. No finding is in the shared
mathematics.

## For the Records Lane

**(a) `REVIEWED_SOURCES`.** Add
`d97758bbc9639edc70b8bd7dc83106d4e8d1be034bacb3e88f8c539b88091c88`, with this comment:

```python
# d97758bb…: main at 910b6b12c/34e87a86b, the declared-net change (lemma N0) and its
# DN-2/DN-4–DN-6 fixes, accepted by review-2026-10-06-sqverify-fast-declared-net-soundness.md
# for standard-net certificates and, once its DR-1 and DR-3 are fixed, for format M on a
# declared proof_net.
```

`73959cae12d65ce2a594255ddb0b677b899fd6d87b99b079f57d4fe50d1ababa` may be added with the
scope “f007d7afd’s build; accepted only for files with no top-level `net` key in format
T or M”. That condition holds for every retained candidate, and the census test already
asserts it for cited entries.

**(b) Carrying the route to a declared-net format M certificate.** A records lane checks
each of the following for the certificate:

1. **The file.**
   - The candidate is format M, with `points` empty and `scaling_factor` 1.
   - It has a `proof_net` object with exactly `step` and `last`, plus `count = last + 1`
     if present.
   - It has no top-level `net` key, and any `certificate` metadata only restates the
     net.
   - Eight times its densest row’s density is at most $2^{32}$.

2. **The case.**
   - `census.json` names it with `n` and `L` equal to the report entry’s claim.
   - `status` is `VERIFIED`, `returncode` 0 and `refused_directions` empty.
   - `directions_verified` equals `proof_net.last + 1`, and the receipt’s indices are
     exactly `0 … last`, each `verified`.
   - `threshold` is `1`, and `least_bound_leaf_exact.clears_threshold` is true.

3. **The premises.** The summary’s `premises` give:
   - `format` `M`, `centre_domain` `per-bin`, `net_origin` `proof_net`;
   - `D` equal, as an exact rational, to `proof_net.step`, and `angle_count` equal to
     `last + 1`;
   - `net_last_tangent` equal to $(N_\theta - 1)D$, and `B` equal to the file’s;
   - `mass_exact` equal to the claim’s $n - 1/100000$ (or the gap the certificate’s
     review states), and below $n$;
   - `expanded_points` and `expanded_segments` 0, and `fault_injected_at_box` null.

   Lemma N0’s (a) to (e) must be recomputed in exact arithmetic from the file by a tool
   apart from the crate, as `audit_wand125_declared_net audit` does for
   `mixed_n18_L470`. For 416 nodes this means $D \in (\tan(\pi/8)/415, 1/830]$ and
   $B < 1/(1 + D/(1 - D^2/4))$. For the 832-node net at $1/2006$ with $B = 1999/2000$,
   the premises hold with $B(1 + D) = 4011993/4012000$.

4. **The candidate.** `candidate_sha256` is the retained `.gz` file’s, and
   `devtools.retained_data check` on its packet passes.

5. **The build.** `source_sha256` is `d97758bb…`, profile `release`, rustc 1.98.0. A
   `73959cae…` row also qualifies under (a)'s condition.

6. **The control.**
   - The receipt is `CONTROLS_REFUSED` from a control driver whose independent evaluator
     reads the declared net (DR-1 fixed, and the fix read by a reviewer).
   - `captures_agree` is true.
   - Both mutants are refused at exit 1, each with a capture below 1 evaluated on the
     declared net.
   - `tests/test_sqverify_fast_census.py` passes with a declared-net branch in place of
     its blanket `not {"proof_net", "net"}` and `201`/`83/40000`/`9977/10000`
     assertions, holding items 1 to 5 above.

7. **The mathematics.** A review under `docs/project/reviews/` read this certificate and
   accepted it. Neither the 832-node `mixed_n18_L4704` nor `mixed_n19_L48229` has had
   one, and this review is of the crate, not of either certificate.

8. **The words.** The evidence text names the declared net’s step and count (DR-3) and
   the accepted build by this review (DR-2), says *independently re-implemented*, and
   cites this review beside the route review.

Another review is needed before the route carries if:

- the crate’s `src/`, lockfile, `build.rs` or toolchain changes;
- a certificate has a net outside lemma N0, a non-uniform or listed-node net, or any
  format other than M on a declared net;
- the census driver’s verdict, admission arguments or control logic change again;
- a defect is found in the per-bin domain or the fold.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
