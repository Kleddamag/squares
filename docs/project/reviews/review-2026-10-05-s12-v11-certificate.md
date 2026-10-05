# Proof Review: squarepacker’s v1.1, `s(12) ≥ 7943/2000 = 3.9715`

This review was carried out on 2026-10-05 from the retained packet
[`squarepacker-s12-lower-bound-2026-10-05`](../../../packing/resources/web/squarepacker-s12-lower-bound-2026-10-05/README.md),
pinned at `7a96bec3`. The checkout was the detached worktree at `3ae63093a`. The
reviewer is an AI agent: the separately prompted review lane of stage 4 of the result
import for provisional `T-095`. It shares no context with the lane that retained the
source and registers the result, and it shares none with the lane that is replaying the
certificate. It is blind to that replay.
The model is `claude-opus-5-5` at the tbd-strong tier.

The claim is jlevy/squares#363, opened on 2026-10-05 by squarepacker (Ryu Sungjoon):
$s(12) \ge 7943/2000 = 3.9715$, from `s12_lower_3.9715.txt` of
squarepacker/s12-lower-bound release v1.1.
If the claim holds it supersedes `T-079`, $s(12) \ge 15680000/3949423$, as the verified
lower bound at n = 12. `T-079` stays true.
This review registers nothing and moves no bound.

**In one line:** No mathematical defect was found. The argument is `T-079`’s: Daniel’s
points, dilated to a new container, with new weights. Every lemma it needs re-derives
here. The producer’s logs agree with each other and with every quantity that could be
recomputed by hand. **This review ran no computation**, because this session’s tool
permissions refused every command that executes a program (F1). So the entry of the
claim into the verified lane rests entirely on the complete replay (Daniel’s verifier
over all 39,765 bins at N = 96000, and the native parent-core route) and on the retaining
lane’s exact preflight audit. Nothing found here blocks it. `S3` is kept.

## 1. What Was Reviewed

| Field | Value |
| --- | --- |
| Claim | $s(12) \ge 7943/2000 = 3.9715$, provisional `T-095` |
| Source | squarepacker/s12-lower-bound at `7a96bec36bc6811c3715ef581598f22ff9b7ba3a`, release `v1.1` |
| Certificate | `s12_lower_3.9715.txt`, SHA-256 `e2f326b2…` per the source’s `SHA256SUMS` and the packet manifest, retained as `.gz` |
| Header | `15886000 4000000 / 4000000 / 10000000 / 1736` |
| Total weight | $119974808/10^7 = 11.9974808$ |
| Reported least captured weight | $10000050/10^7$ at bin 0, $N = 96000$, by both of the producer’s checkers |
| Base | Daniel’s `s12_lower_3.9686.txt` (`T-049`); verifier `s12/verify` at `7d6f46d9`, retained at `167d842c` |
| Superseded if confirmed | `T-079`, $15680000/3949423$ |

**Read in full.** From the v1.1 source: `README.md`, `paper/s12_lower_3.9715.tex`, `LICENSE`,
`.zenodo.json`, `tools/exact_pose.py`, every log under `logs/3.9715/`, every log and
`.time` file under `controls/3.9715/`, `logs/control_scaled_further_31360_7900_N96000.log`,
both `logs/exact_pose_*.log`, and the three `search/lp_*.jsonl` files.
From the 2 October packet: `tools/indep_check.cpp`, line by line.
From Daniel’s packet: `s12/verify/src/main.rs`. I read `read_cert`, `bin_geometry`,
`check_symmetry`, `main` in full and `min_cover_k` as far as the strip test, the y-range
padding and the u1 breakpoint merge; I did not reread the clique and anchor paths, which
a plain point certificate never enters.
Also read: the packet `README.md`, `acquisition/sources.json` (head),
`github-release-v1.1.json` and `receipts/preflight.json`; `T-049`, `T-078`, `T-079` and
`T-093` in `packing/frontier/results.yaml`; the two 2026-10-02 reviews of `T-078` and
`T-079`; the template review of `T-093`; stage 4 of `packing/campaign/result-import.md`;
the rungs in `epistemics.md`; the lines of the T-079 research note that describe Route B;
the head of `devtools/verify_evand_angle_net_native.py` (cases, `sigma`, `net_rows`,
`parse_certificate`); and the module docstring and row type of
`sqpack/fractional/parent_core.py`.

**Not read:** the text of jlevy/squares#363 itself, because `gh issue view` was refused (F1, F7).
Statements attributed to the issue below are taken from the brief and the packet README,
which say the issue repeats the source README. Also not read: the paper PDF, which is
the rendering of the `.tex`; the `colgen_*` logs and `tools/search/`, which play no part
in the proof; and `logs/3.9715/tightscan_N96000.txt.gz`, which is pinned by digest only.

## 2. The Argument, Re-Derived

**The counting reduction.** Let points $p_i \in [0, s]^2$ carry weights $w_i \ge 0$
with $\sum w_i < 12$, such that every closed unit square $Q \subseteq [0, s]^2$ captures
$\sum_{p_i \in Q} w_i \ge 1$.
Suppose twelve unit squares with pairwise disjoint interiors fit in a square of side
$s' < s$. Move that square to $[0, s']^2$ and dilate by $\lambda = s/s' > 1$. Each image
is a square of side $\lambda$, and the closed unit square concentric with it lies in its
open interior. The twelve closed unit squares are therefore pairwise disjoint and lie in
$[0, s]^2$. Each captures at least 1, and no point is counted twice, so
$12 \le \sum w_i < 12$, a contradiction.
The step needs exactly three facts about the file: the weights are nonnegative, the
points lie in the closed container, and the total is below 12. The closed-square
convention is what turns $s' < s$ into disjointness, so the conclusion is $s(12) \ge s$,
not $>$. This is the paper’s Lemma 2.2. Daniel has formalised it in Lean; that file was
not reread here.

**The D4 fold.** $S(c, \theta + 90°) = S(c, \theta)$, so angles in $[0°, 90°]$
suffice. The diagonal reflection $\rho(x, y) = (y, x)$ maps the container to itself and
$S(c, \theta)$ to $S(\rho c, 90° - \theta)$. If the weighted multiset is
$\rho$-invariant, a square and its image capture the same weight, so angles in
$[0°, 45°]$ suffice (the paper’s Lemma 3.4).
Of the point set, the fold needs only that the weighted multiset is invariant under
$\rho$. Daniel’s `check_symmetry` tests the full group, through the generators
$x \mapsto s - x$, $y \mapsto s - y$ and the swap, by comparing sorted
`(x, y, w)` multisets in exact integers, which is more than enough. The verifier sweeps
bins $0, \ldots, K-1$, with $K$ the least integer such that $(K + N)^2 \ge 2N^2$, which
means $\theta_K \ge 45°$. At $N = 96000$, $N(\sqrt2 - 1) = 39764.57$, so $K = 39765$; the
log’s `angles: k=0..39765` and the partial runs’ `of 0..39764` agree.

**The rational net.** $\theta_k = 2\arctan(k/N)$ gives
$\cos\theta_k = (N^2 - k^2)/(N^2 + k^2)$ and $\sin\theta_k = 2kN/(N^2 + k^2)$. The
gap $\delta_k$ has rational cosine $cd/(g_0 g_1)$ and sine $sd/(g_0 g_1)$, with
`cd = c0*c1 + s0*s1` and `sd = c0*s1 - s0*c1`, as in `bin_geometry` and `main`.

**The shrink lemma.** For $\theta = \theta_k + \varphi$, $0 \le \varphi \le \delta_k$,
the square of side $\sigma$ at angle $\theta_k$ is contained in the concentric unit
square at $\theta$ when $\sigma(\cos\varphi + \sin\varphi) \le 1$. Each coordinate of a
vertex, in the unit square’s frame, is bounded by $(\sigma/2)(\cos\varphi + \sin\varphi)$,
and convexity does the rest. Since $\cos t + \sin t$ increases on $[0, \pi/4]$ and
$\delta_k < \pi/4$, the choice $\sigma_k = 1/(\cos\delta_k + \sin\delta_k)$ works.
Daniel computes `sg_n = (g0*g1*10^6)/(cd+sd)` with truncating division of positive
integers. That is $\lfloor 10^6\sigma_k \rfloor / 10^6 \le \sigma_k$: a smaller
concentric square, so a lower bound for it is a lower bound for the unit square.
At $k = 0$, $\sigma_0 = (N^2+1)/(N^2+2N-1) = 9216000001/9216191999$ exactly. By hand,
$10^6\sigma_0 = 999979.17$, so Daniel’s $\sigma_0 = 999979/10^6$. Both agree with the
preflight receipt.

**The admissible centre box.** For $\theta \in [0°, 90°]$, $S(c, \theta) \subseteq [0, s]^2$
exactly when $c \in [\omega/2, s - \omega/2]^2$, with
$\omega = \cos\theta + \sin\theta = \sqrt2\sin(\theta + 45°)$. This function is concave
on the range, so its minimum over a bin is at an endpoint. Daniel takes the smaller
endpoint value, rounded down to $10^{-6}$ (`wm_n`), which enlarges the box. The upper end
`u_c` divides `2*sg_d*wm_d*D*s_num` by `s_den` exactly, because `read_cert` refuses a
file where `s_den` does not divide `s_num*D`. Per strip, the y-range of the rotated box
is computed in `f64` and padded outward by
`1e-9*range + 1e-6*hh`. The numerators are about $10^{29}$, so the `f64` error is about
$10^{13}$ units against a pad of about $4 \times 10^{22}$. The padding can only add
centres.

**Closedness at cell boundaries.** In a strip $(a, b)$ between consecutive u0
breakpoints, an atom counts when $q_0 - h \le a$ and $q_0 + h \ge b$, that is, when it
lies in the closed square for every $u_0 \in [a, b]$. The u1 cells are the open
intervals between the merged breakpoints $q_1 \pm h$ and the padded box ends.
The captured weight is constant on each open cell and, by closedness, no larger than its
value at any point of the cell’s closure (the paper’s Lemma 3.5). Every admissible centre
lies in the closure of some swept cell, so the minimum over swept cells is a lower bound
for the minimum over the box. A strip in which no atom is active gives value 0, which is
a failure.

**The overflow-checked build.** The sweep runs in `i128`. The release profile in
`Cargo.toml` does not check overflow, so a wrap could in principle print a false pass. The
source states that it built with `CARGO_PROFILE_RELEASE_OVERFLOW_CHECKS=true`, and its log
names say `ovf`, but the logs bind no binary digest (F2). With checks on, an overflow
panics a worker thread; `join().unwrap()` then aborts `main` before any verdict is printed.
The `cmul` and `cadd` helpers die with exit 2 and never print a verdict. The verifier exits
0 on `NOT VERIFIED`, so the verdict line decides, not the exit status.

**What a `VERIFIED` line at N = 96000 proves.** Suppose the line comes from that program,
built with overflow checks from the retained source, run on the certificate whose
SHA-256 is `e2f326b2…`, with no `VERIFY_BINS` set. Then:

- the file parsed with every weight at least 0, every point in $[0, s]^2$, and
  `s_den | s_num*D`;
- the weighted multiset is D4-invariant;
- the total is below $12W$; and
- for each $k \in \{0, \ldots, 39764\}$, every centre in the enlarged box, rotated, lies
  in the closure of a swept cell whose square of side $\lfloor 10^6\sigma_k\rfloor/10^6$
  at $\theta_k$ captures at least $W$.

With the shrink lemma, the box lemma and the fold, every closed unit square in
$[0, 7943/2000]^2$, at every angle, captures weight at least 1, and the reduction gives
$s(12) \ge 7943/2000$.
Besides the sweep, the line needs four things: the build provenance (F2), the digest of
the input, the absence of `VERIFY_BINS` (whose runs print `PARTIAL RUN` and never
`VERIFIED`), and the four elementary lemmas above, which are proved in the paper and
re-derived here.
The weight margin, $50/10^7$, says how close the tightest test square came. The slack
that covers the angles between net points is $\sigma_k < 1$, which is built into every
bin. Any minimum of at least 1 would prove the bound.

**The independent checker’s version of the same argument** (`indep_check.cpp`, read
line by line):

- It sweeps all $N$ bins over $[0°, 90°]$ with no fold, uses $\sigma_k$ exactly, and
  works on a grid of pitch $1/Q$, $Q = 10^{15}$.
- Points are floored and the half-side becomes $\lfloor Q\sigma_k/2\rfloor - 1$. The
  paper’s Lemma 3.6 shows that a rounded capture implies a true capture.
- The box is rounded outward ($L$ floored, $U$ ceiled).
- The u1 range of the box over a closed slab is taken exactly, from the vertices inside
  the slab and the edge crossings at $u_0 = a, b$; I checked the two crossing formulas
  $u_1 = (c\,t - gX_0)/s$ and $(gY_0 - s\,t)/c$ by hand.
- A segment tree over the open elementary u1 intervals takes the minimum over every
  interval that meets that range.
- All geometric arithmetic is `__int128` with builtin overflow checks; weight sums are
  64-bit, about $1.2 \times 10^8$.
- The worst product is $g_0 g_1 Q \approx 5 \times 10^{36}$ at $N = 192000$, below
  $1.7 \times 10^{38}$.

I found no defect. A run accepts when the minimum is at least $W$ and the total is
below $nW$.

## 3. The Certificate, Checked

**No code of this review’s own ran.** In this session, every command that executes a
program needed an approval that could not be given, and so was refused (F1):

| Command attempted | Purpose | Result |
| --- | --- | --- |
| `gh issue view 363 --repo jlevy/squares --comments` (with and without the `NO_PROXY` prefix) | Read the issue | refused: “requires approval” |
| `mkdir -p …/-home-user-squares/…/scratchpad/laneA-review` | The brief’s scratch directory | refused: outside the session’s working directories |
| `uv run --frozen --all-extras --group dev [--project packing] python -c …` | The project interpreter | refused |
| `cargo build --release --locked -j 1 --manifest-path …/s12/verify/Cargo.toml --target-dir <scratch>` with overflow checks | Build Daniel’s verifier | refused |
| `gunzip -c`, `zcat`, `zgrep -c ''` on `s12_lower_3.9715.txt.gz` | Read the certificate | refused |
| `git hash-object` on the retained `verify` files | Blob identity with `7d6f46d9` | refused |
| `cp -r` of the crate to scratch | Build outside the worktree | refused |

So there is no scratch code. The scratch directory holds one note file, and the
certificate’s integers were never read in this review. The planned checks were header and
format, positivity, containment, D4, the total, the dilation relation to Daniel’s points,
both controls, the corner square, and single-bin decisions at bins 0, 1 to 27 and 30000
by Daniel’s verifier and by an exact sweep of the review’s own. All of them remain
undone here.

**What did run**, all read-only:

| Command | Result |
| --- | --- |
| `git log -1 --format='%H %ci'` | `3ae63093ab0cb64b71200642acad9f238350ba31 2026-10-05 17:18:16 +0000` |
| `sha256sum` of the 2 October packet’s `tools/indep_check.cpp` | `21527e8d…d029`, equal to the entry in v1.1’s `SHA256SUMS` and in the v1.1 packet manifest (`grep`), so v1.1’s checker is the bytes read and replayed for `T-078` |
| `sha256sum` of the retained `s12/verify/src/main.rs` | `226ef3f1…c94c`, the pin the `T-079` review records |
| `diff indep_check.cpp indep_scan.cpp` | The scan adds `scan_thresh`, `kmax` and `kmin` arguments, a per-bin minimum and a `BIN k value` print, and changes nothing else: it is the same checker restricted to a bin range |
| `grep -r ''` over `logs/3.9715/`, `controls/3.9715/`, the 31360/7900 control log, and the `exact_pose` and `search/lp_*` logs | Quoted below |

**The producer’s logs, cross-read:**

| Run | Least captured weight | Bin | Verdict |
| --- | --- | --- | --- |
| `verify`, N = 24000 (`k=0..9942`) | 6737611 | 0; also fails at k = 1 to 6 | `NOT VERIFIED` |
| `verify`, N = 96000 (`k=0..39765`), 01:45:00 to 02:33:51 KST on 4 October | 10000050 | 0 | `VERIFIED` |
| `indep_check`, N = 24000 | 6737611, near (0.500004, 0.500004) | 0 | `NOT VERIFIED` |
| `indep_check`, N = 48000 | 9288526, near (1.49995, 1.49995) | 0 | `NOT VERIFIED` |
| `indep_check`, N = 96000, 8 min 11 s | 10000050, near (0.5433, 0.5433) | 0 | `VERIFIED` |
| `indep_check`, N = 192000 | 10000050 | 0 | `VERIFIED` |
| Control 1, `indep_check`, N = 96000 | 9999850, total 119974008 | 0 | `NOT VERIFIED` |
| Control 1, `verify`, `VERIFY_BINS=0:0` and `30000:30000` | 9999850 at both | 0, 30000 | `PARTIAL RUN`, `FAIL` |
| Control 2, `indep_check`, N = 96000, s = 15886000/3999600 | 6737611, near (0.500039, 0.500039) | 0 | `NOT VERIFIED` |
| Control 2, `verify`, bins 0 and 30000 | 6737611 at 0, `FAIL`; 10000050 at 30000 | 0, 30000 | `PARTIAL RUN` |

On the two nets where both programs ran, they agree. Control 1 lowers eight points by
100 units each, so the total falls by exactly 800 ($119974808 \to 119974008$), and the
minimum falls by exactly 200 at bin 0 and at bin 30000. That is the two points of the
orbit that lie in $[0, 1]^2$ in both bins, as the source says.

**Re-derived by hand, in exact arithmetic:**

- **Container.** $7943/2000 \times 4000000 = 15886000$, the header’s `s_num` over
  `s_den = D`.
- **Dilation.** $(7943/2000)/(15680/3951) = 7943 \cdot 3951 / 31360000 = 31382793/31360000$.
  $7943 \cdot 3951 = 31772000 - 389207 = 31382793$. The numerator is odd, not divisible
  by 5, and leaves remainder 1 on division by 7, so the fraction is reduced.
- **Advance over `T-079`.** $7943 \cdot 3949423 = 31370266889$, minus
  $2000 \cdot 15680000 = 31360000000$, gives $10266889/7898846000$. A Euclidean gcd by
  hand with $3949423$ is 1. This is about $0.0012998$.
- **Advance over Daniel.** $22793/7902000 \approx 0.002884$.
- **Counting gap.** $12 - 11.9974808 = 25192/10^7 = 3149/1250000$.
- **Heaviest orbit**, from the preflight receipt’s listing. Under $x \mapsto 15886000 - x$:
  $15886000 - 3175174 = 12710826$ and $15886000 - 3999868 = 11886132$, and the eight
  listed points are exactly the D4 images of $(3175174, 3999868)$. Two of them,
  $(0.7938, 0.999967)$ and its transpose, lie in $[0, 1]^2$.
- **The first row.** $\alpha = 141 s/560 = 1119963/1120000 = 0.99996696$, which is
  $3999867.86/D$. The file’s row is at $3999868/D$, an error of 0.14 grid units.
- **The second row.** $2\alpha = 7999735.71/D$. The file’s row is at $7999735/D$, an
  error of 0.71 units, or $1.8 \times 10^{-7}$. That is within the stated
  $11/39200000 = 2.806 \times 10^{-7}$ and is consistent with rounding in three steps
  rather than to the nearest point.
- **Row counts.** The receipt’s 112 points on $x = \alpha$ give the paper’s 223 points
  “with $x$ or $y$” on that value, with one point at $(\alpha, \alpha)$. Its 15 points on
  $x = 2\alpha$ give 30, with none at $(2\alpha, 2\alpha)$.

**Relied on and not re-derived here.** The retaining lane’s audit
(`receipts/preflight.json`, 21 checks, all `true`) records several facts that this review
could not decide by its own code:

- every weight is positive;
- every point is in the container and distinct;
- the multiset is D4-invariant, in 223 orbits;
- the total is 119974808;
- the points match Daniel’s, one to one, within $11/39200000$;
- the corner $[0, 1]^2$ holds 58 points of weight 10000050; and
- both controls rebuild byte for byte from their descriptions.

None of these is load-bearing beyond what Daniel’s verifier re-checks itself when it is
replayed: positivity, containment, D4 and the total. The native route’s
`validate_parent_core` re-checks D4 and the total again. The relation to Daniel’s points
bears on credit, not on the bound.

## 4. The Checkers’ Trust Boundaries

| Checker | What it decides | What it trusts |
| --- | --- | --- |
| Daniel’s `verify` (`7d6f46d9`; the retained `167d842c` copy has main.rs SHA-256 `226ef3f1…`, and its blobs equal `7d6f46d9`’s per the packet README) | The file’s premises; then the bins covering $[0°, 45°]$ via the fold, by exact arrangement sweep in `i128` with $\sigma_k$ and $\omega$ rounded down to $10^{-6}$ | The four lemmas; the build (overflow checks, F2); `f64` padding that is only outward |
| squarepacker’s `indep_check.cpp` (`21527e8d…`, unchanged since v1.0) | All $N$ bins on $[0°, 90°]$, with no fold, $\sigma_k$ exact and the grid rounded conservatively | The same four lemmas, its own segment tree, and the compiler |
| This repository’s native route, `verify_evand_angle_net_native --case s12-v11` | Rows $[k/N, (k+1)/N]$ of half-tangents up to the first right end with $r^2 + 2r \ge 1$; `validate_parent_core` proves D4, the counting gap and the half-tangent cover, and proves each core strictly inside every parent of its row in exact rationals; `verify_parent_core_rows` decides coverage by directed-rounding interval branch and bound over centre boxes, with the exact centre margin rather than a rounded one | The reader (reviewed as F5 of the `T-079` review), the parent-core theorem, and the interval arithmetic; it does not trust the shrink lemma, which it re-proves per row |

**What pairs share.**

- *Daniel and `indep_check`:* the elementary framework (the net, the shrink lemma, the
  admissible box, the cell-minimum lemma) and no code. They differ in the rounding of
  $\sigma$, the fold and the sweep structure.
- *Daniel and native:* the bin decomposition and the rounded $\sigma_k$ formula, by design
  (F9), together with the fold, which native validates itself.
- *`indep_check` and native:* the net and the shrink construction, in different forms.

**What all three share:** the certificate bytes, the counting reduction with closed
squares, and the decision of coverage through a finite angle net at N = 96000 with a
shrunk test square per bin.
All three come from AI-assisted work: Daniel’s `CREDITS.md`, the source’s statement, and
this repository. An error in the common framework would affect all three. The framework
consists of four short lemmas, proved in the paper and re-derived in §2, and the native
route re-proves the containment row by row.

**The search was fitted to two of the checkers.** That is the point of the brief’s third
question, and it is where the confirmation has to come from (F3).
The v1.1 LP took its rows from Daniel’s verifier’s `TIGHT_DUMP` cells, on bin 0, on the
bins $k \equiv r \pmod{96}$ and on flagged bins, with capture sets recomputed at cell
midpoints by the search scripts. It stopped when `indep_scan`, which is `indep_check`
restricted to a bin range (the `diff` above), found no violated bin on
$[0°, 45°]$ (`search/lp_3.9715.jsonl`, last line: `scan_bad: 0`, `scan_least: 10000050`).
An optimiser run until a checker is silent will exploit any blind spot that checker has.

- **`indep_check`’s acceptance of bins on $[0°, 45°]$** is therefore the search’s stopping
  condition, not evidence beyond it. Its runs on $(45°, 90°]$, where the net is not
  reflection-symmetric, so the test squares there are new, and its run at N = 192000 were
  not targets of the search. They are weaker confirmations than they look, because they
  share the producer and the code that the search was stopped on.
- **Daniel’s full sweep** was never the stopping criterion. The search consulted it only on
  the sampled and flagged bins, about 415 to 726 bins a round, through its dump. The
  `lp_3.9715` log shows that the sampled bins were clean twice when complete scans still
  found 695 and 67 violated bins. A defect in Daniel’s sweep would therefore not have been
  steered around elsewhere. Its full sweep shares no code with `indep_check`, so a blind
  spot of one is caught by the other unless it lies in the shared framework.
- **The native route** is untouched by the search. It is the only method-distinct decider.

The confirmation is carried by two runs: a complete replay of Daniel’s verifier at
N = 96000 with overflow checks, and a complete native parent-core run. The producer’s
`indep_check` runs are producer evidence.

## 5. Why It Stops Near Here

**The rows (data, audited, not re-read here).** Daniel’s points include rows at
$x = 1 - 3/3951 = 3948/3951$ and $x = 2 \cdot 3948/3951$, and their images. Since
$3948/15680 = 141/560$, after dilation to side $s$ the rows lie at $\alpha = 141s/560$ and
$2\alpha$. That is exact, up to the grid rounding computed in §3.

**The two ways to slip (proved, elementary).** An axis-parallel closed square of side
$\sigma$, centred in $[1/2, s - 1/2]^2$, can:

- (i) sit strictly between $x = \alpha$ and $x = 2\alpha$ if and only if $\sigma < \alpha$,
  and do the same in $y$ with centre near $(1.5\alpha, 1.5\alpha)$; or
- (ii) stay below $x = \alpha$ with centre $1/2$ if and only if $(1 + \sigma)/2 < \alpha$.

So (i) is available from $s > (560/141)\sigma$. By hand, with
$560/141 = 3.97163121$, the thresholds for bin 0 are:

| N | $1 - \sigma_0$ | (i) | (ii) |
| --- | --- | --- | --- |
| 24000 | $8.33 \times 10^{-5}$ | 3.97130 | 3.97147 |
| 48000 | $4.17 \times 10^{-5}$ | 3.97147 | 3.97155 |
| 96000 | $2.08 \times 10^{-5}$ | 3.9715485 (exact $\sigma_0$), 3.9715478 (Daniel’s) | 3.97159 |
| 192000 | $1.04 \times 10^{-5}$ | 3.97159 | 3.97161 |

These match the paper’s table and the receipt. They also explain the producer’s
rejections at the claimed $s = 3.9715$:

- N = 24000 is past (ii), and its minimum is near the corner centre
  $(0.500004, 0.500004)$;
- N = 48000 is past (i) only, and its minimum is near $(1.49995, 1.49995)$, between
  the rows; and
- N = 96000 and 192000 are past neither.

At $s = 3.9715$, $\alpha = 0.99996696 < \sigma_0$, so neither escape is open on N = 96000,
with $4.8 \times 10^{-5}$ to spare. At $s = 3.97155$, $\alpha = 0.99997955$, which
exceeds the exact $\sigma_0$ by $3.9 \times 10^{-7}$, as the paper says.

**“The LP is 12.0052 at 3.97155, a lower bound from 2244 rows” (numerical, right
direction, verifier-specific).** `search/lp_3.97155.jsonl` holds one round: 415 bins,
2244 rows, `lp` 12.005229. Minimising the total subject to a subset of the constraints
gives at most the optimum under all of them, so the restricted value is a lower bound on
the least total of any D4-invariant weighting that meets all of them. The direction is
right. Three qualifications:

1. **The right-hand side.** The rows ask $\ge 1 + 2 \times 10^{-6}$. The LP is
   homogeneous, so with right-hand side 1 the optimum is $12.005229/1.000002 = 12.005205$,
   still above 12.
2. **The solver.** The value is the primal objective of a floating-point interior-point
   solve without crossover. Only a dual-feasible point certifies a lower bound. The
   margin, $4 \times 10^{-4}$ relative, makes the conclusion very likely, not proved.
3. **What the rows describe.** The rows are cells of Daniel’s arrangement, with rounded
   $\sigma$ and $\omega$, and those cells may extend past the centre box. So the
   statement is about acceptance by Daniel’s verifier on that net, at that rounding of the
   points to the side 3.97155. It is not about covers, and it is not about `indep_check`,
   whose exact $\sigma$ makes each row weaker. The source phrases it as acceptance by
   Daniel’s verifier, which is correct.

**What the D4 restriction costs.** For true covers, nothing: averaging a cover over the
group keeps it a cover and keeps its total. For acceptance on a net, the 90° rotations
cost nothing either. Rotation about the centre maps each bin’s family of test squares to
itself, and the centre box is invariant, so averaging over $C_4$ preserves acceptance.
The reflections map $\theta_k$ to $90° - \theta_k$, which is not a net angle. The source’s
caveat about non-invariant weights is therefore correct, and it is narrower than the
source states: the $C_4$ part costs nothing.
Bin 0’s family is D4-invariant, so if the bin-0 rows alone pushed the LP above 12, the
restriction would cost nothing at all. The retained logs do not show whether they do
(F4).

**Finer nets and the limit of these points (heuristic).** As $N \to \infty$,
$\sigma_0 \to 1$ and the thresholds tend to $560/141 = 3.9716312$. Past that point,
actual unit squares at $\theta = 0$ avoid the rows, and that is a geometric fact.
One scaling link makes the heuristic sharper. Bin 0’s test squares of side $\sigma$ in the
container $s$, with Daniel’s points dilated to $s$, become, after scaling by $1/\sigma$,
actual axis-parallel unit squares in the container $s/\sigma$. Their centres are confined
to a sub-box. The points become Daniel’s points dilated to $s/\sigma$, up to grid rounding.
Every bin-0 row at $s$ is therefore a true-cover constraint at $s/\sigma_0$. If the
bin-0 rows alone gave a value above 12 just past $(560/141)\sigma_0$, no weighting of these
points could be a cover just past $560/141$.
That is plausible from the 3.97155 run but not established (F5). Either way the cap is
about $1.3 \times 10^{-4}$ above the claim, and it concerns these points only. New points
in the gaps are not limited by it; the source’s column-generation attempts were
inconclusive. The method as a whole is capped below 3.99 by Daniel’s fractional packing.

## 6. The Clarification of #309

**The logic is right.** A refusal on a net shows that some shrunk test square, of side
$\sigma_k < 1$ at $\theta_k$ with centre in an enlarged box, captures less than 1. The
proposition is sufficient and not necessary, so a refusal does not show that any actual
unit square captures less than 1. It does not show that $31360/7900$ fails.

**What the evidence is.** `exact_pose.py` evaluates actual unit squares at a single
angle, $\theta_{2557}$ or $\theta_{2558}$ (the two ends of `indep_check`’s rejecting bin
2557). It uses a $401 \times 401$ grid of centres within $\pm 0.003$ of `indep_check`’s
floating-point diagnostic centre $(0.525827, 2.488851)$, clipped to the admissible box at
that angle. The grid step is about $1.5 \times 10^{-5}$.
Capture is tested in `float64` with `<= 0.5`, and only the grid minimiser is
re-evaluated in exact `Fraction` arithmetic. Both logs report a float minimum of
1.0048468 and an exact value of $10048468/10^7$ at a rational centre inside the container.

**What it does not establish.** It covers only two angles and not the angles inside the
bin. It covers only finitely many centres: the captured weight is a step function whose
cells can be far thinner than the grid step, and boundary cases in floating point can go
either way. It covers no centre outside the window and no other bin.
So it shows that the refusal at that pose is, as far as sampled, an artefact of the
shrink. It does not show that the 31360/7900 set is a cover, and the source says this
itself (“How far that rescaled set is a cover was not determined”). The source also
retracts v1.0’s “essentially critical”.
None of this changes `T-078`, whose claim is $31360/7901$ (F6).

## 7. Credit, Licence, AI Statement and Dates

**Who did what, as the source states it and the files support:**

- *Evan Daniel:* the 1,736 points, the verifier, the reduction and its Lean
  formalisation.
- *This project:* the idea of keeping Daniel’s points and re-weighting them on a fine net
  (Route B, `T-079`), with `s12_reweight.py` and Daniel’s `tighten.py` named as guides
  for `tools/search/`, which is said to be written from scratch.
- *Burns and Massaccesi:* the weighted-certificate method.
- *Göbel and Stromquist:* unavoidable sets.
- *squarepacker:* the dilation and rounding, the weights, the search and its in-cycle full
  scan, `indep_check`, and the runs.

This is the attribution the packet README gives, and nothing read here contradicts it.

**Route B is described accurately.** The source says Route B took rows from every 96th
bin with a rotating offset, and that its first complete sweep refused six bins, which
three focused rounds repaired. The research note’s lines 101 and 113 to 118 say the same.
“The difference here is only that the complete scan is part of every cycle” is a fair
summary. `s12_reweight.py` lives in `packing/devtools/`, which this repository’s
`LICENSE` places under MIT, as the source says. The research note and the review it
links are CC BY 4.0, and the source cites and links them, which that licence asks.

**Licence.** `LICENSE` reproduces Daniel’s MIT notice for the derived material and names
`s12_lower_3.9715.txt` and `controls/3.9715/` as derived material. The other v1.1 files
are released under MIT terms, copyright Ryu Sungjoon, and `.zenodo.json` says MIT. The
copy retained here sits under `packing/resources/`, which this repository’s grants
exclude. No defect.

**AI statement.** The README says “the rescaling, the re-weighting, the verification runs
and the tools in `tools/` were prepared with the help of Claude (Anthropic)”. The paper’s
acknowledgements say the same of “the re-weighting, the scans, the verification runs and
the independent checker”, and the paper’s §7 says the checker “has not been reviewed by
anyone else”. The issue is said to end with the same sentence; not read here (F7).

**Dates.**

- *The claim date* is the UTC date of the first commit containing the certificate:
  **2026-10-05**, from `98ffe373` at 08:26:42Z, which the packet README says adds every
  v1.1 file. This review could not read the source’s history itself (F7).
- *The pin* `7a96bec3` is at 08:31:05Z.
- *The release* was published at 08:37:31Z (`github-release-v1.1.json`).
- *The issue* was opened at 08:43 UTC, per the packet README.
- *The computations* came earlier. The `.time` files put Daniel’s N = 96000 run at
  01:45 to 02:33 KST on 4 October, which is 16:45 to 17:33 UTC on 3 October.
  `indep_check` at N = 96000 and 192000 started at 02:33:51 KST, and the controls ran
  from 03:05 to 03:13 KST.

By the rule, the date is 2026-10-05.

## 8. Significance

The draft is `S3`: “Raises the verified lower bound at n = 12, if confirmed, by 0.0013 over
T-079, the largest step since T-049; new weights on Daniel’s points, the recipe of T-079
(Route B) with a complete scan in every cycle, so no new technique; not S4.”

**Kept.** The steps at n = 12 are:

- `T-049`: 0.0086 over `T-017`, a new instance, `S3`;
- `T-078`: $0.000502$, a rescaling that adds no weight or technique, `S2`;
- `T-079`: $0.0010824$ over `T-078` (0.0016 over `T-049`), new weights, `S3`; and
- this claim: $0.0012998$ over `T-079`.

The step is larger than `T-079`’s and of the same kind, new weights on fixed points, so
consistency with `T-079` gives `S3`. “The largest step since T-049” is exact by these
figures.
`T-093` was scored `S2` as “the end of a recipe rather than an opening”, but its step was
$2.75 \times 10^{-6}$, the charge unchanged. The comparison matters here only because
the source’s own analysis (§5) puts re-weighting of these points near its end: about
$1.3 \times 10^{-4}$ left on finer nets, by a heuristic. That is a fact about the next
step, not about this one, whose size and kind match `T-079`.
I suggest adding one clause to the rationale: “and its source shows these points nearly
exhausted for re-weighting, about 1.3e-4 below 560/141, which answers T-079’s open ‘the
same points may carry the bound further’.” Not `S4`: the in-cycle complete scan is a
search discipline, not a technique the proof uses. Not `S5`: point covers are capped below
3.99.

## 9. Findings

**None is blocking.** F1 limits what this review can be cited for. The rest are for the
replay or records lanes, or are notes.

### F1 — Non-blocking for the claim: this review ran no computation

Every command that executes a program was refused in this session (§3): the project
interpreter, cargo, decompression of the certificate, `gh`, and `git hash-object`.
No certificate integer was read and no bin was decided here.
The claim does not depend on this review’s computation. Daniel’s verifier, when
replayed, re-checks positivity, containment, D4 and the total, and so does the native
route’s `validate_parent_core`. The exact premises are also in the retaining lane’s
preflight audit.
The record must not cite this review as computed evidence of anything, only as a reading
of the argument and the source. If stage 4 is meant to carry an exact check written by
the review lane, separate from the audit, this lane should be re-run with execution
permitted, running the checks listed in §3.

### F2 — Non-blocking, for the replay lane: the logs bind no binary

The producer’s logs are plain stdout. They name no binary digest, build flags, source
commit or input digest. The overflow-checked build is asserted by the README and by the
`ovf` in file names.
The replay should build the retained crate with
`CARGO_PROFILE_RELEASE_OVERFLOW_CHECKS=true --locked` and record the binary’s and the
input’s digests, as the `T-079` review did. It should also confirm that no `VERIFY_BINS`
was set.

### F3 — Non-blocking, for the records lane: the search was fitted to two checkers

`indep_check`’s acceptance on $[0°, 45°]$ was the search’s stopping condition, and
Daniel’s verifier supplied the LP rows on sampled bins (§4). The confirmation is carried
by the complete replay of Daniel’s verifier and by the complete native run.
The `composition` should not count the producer’s `indep_check` runs as a confirming
method. They are the producer’s evidence, from a checker that is its own and that the
paper says no one else has reviewed.

### F4 — Note: “a lower bound from 2244 rows”

The direction is right. With right-hand side 1 the value is still about 12.0052. But it
comes from a floating-point interior-point solve with no dual certificate, the rows are
Daniel’s verifier’s cells, and the conclusion concerns acceptance by that verifier at
N = 96000 for D4-invariant weights. Averaging over $C_4$ is free; the reflections are
not. Whether the bin-0 rows alone exceed 12, which would remove the D4 caveat, is not
shown. Nothing here bears on the claim.

### F5 — Note: the limit of these points is heuristic

The slip thresholds are proved, and the limit $560/141$ is a geometric fact. That these
points admit no cover just past $560/141$ follows only if the bin-0 rows alone exceed 12
(§5, scaling link). That has not been checked, and it does not limit other point sets.

### F6 — Note: the #309 clarification is a sample

Two angles and a $401 \times 401$ float grid near one pose, with one exact
re-evaluation. It shows the refusal is plausibly a shrink artefact. It does not show
$31360/7900$, and the source says so. `T-078` is unchanged.

### F7 — Note: the issue text and the source history were not read here

`gh` was refused. The issue’s statements and the commit `98ffe373` come from the brief
and the packet README.
The records lane should check that the issue’s quoted statements, “a lower bound from
2244 rows” and “at least 1.0048468”, match the source README, which this review did read.

### F8 — Note: the corner and every-bin statements rest on unread data

“The minimum is $10000050$ in every one of the 39765 bins” rests on
`tightscan_N96000.txt.gz`, which is pinned by digest only. “Attained by corner squares
capturing exactly the 58 points of $[0, 1]^2$” rests on dumps that are not included.
Control 1, lowered by exactly 200 at bins 0 and 30000, and the receipt’s corner count are
consistent with both. Neither statement is load-bearing.

### F9 — Note: the native route shares Daniel’s bins and $\sigma_k$ by design

The native route copies `bin_geometry`’s rounded $\sigma_k$ and the bins. It does not
trust them: it proves each core strictly inside its parents. The record’s
`composition` should keep saying so, as `T-079`’s does.

## 10. Verdict

**No mathematical defect was found.** The argument from `s12_lower_3.9715.txt` to
$s(12) \ge 7943/2000$ is `T-079`’s: Daniel’s reduction, fold, net, shrink lemma and box,
applied to Daniel’s 1,736 points dilated by $31382793/31360000$ with new weights. Every
step re-derives here.
The producer’s logs are mutually consistent. They are also consistent with every quantity
recomputed by hand: the container, the dilation, the advance, the gap, the orbit, the
rows, the slip thresholds and the control arithmetic. The two controls are refused by both
of the producer’s checkers.
The claim’s confirmation rests on two runs: a complete, overflow-checked replay of
Daniel’s verifier at N = 96000 (`VERIFIED`, with the least weight at least $W$), and a
complete native parent-core run. It does not rest on the producer’s `indep_check`, whose
acceptance was the search’s stopping rule (F3), and it does not rest on this review,
which computed nothing (F1).
Once that replay passes and is recorded, nothing found here makes it wrong to move
n = 12’s verified lower bound to $7943/2000$. `S3` is kept (§8).

**For the records lane.** The `reviews:` entry for `T-095`:

```yaml
reviews:
  - path: docs/project/reviews/review-2026-10-05-s12-v11-certificate.md
    kind: adversarial
    reviewer: AI agent, the separately prompted stage-4 review lane for provisional T-095, sharing no context with the registering and replay lanes, blind to the replay; claude-opus-5-5, tbd-strong tier
    reviewer_kind: ai
    relation: project
    date: '2026-10-05'
    scope: >-
      squarepacker's v1.1 certificate for s(12) >= 7943/2000, pinned at 7a96bec3: the argument from certificate to bound with every hypothesis of Daniel's verify, indep_check.cpp and the native parent-core route; the producer's logs and controls cross-read; container, dilation, advance, gap, heaviest orbit, row positions and slip thresholds re-derived by hand; the trust boundaries and the search's fitting to two checkers; the source's account of why it stops near 3.9715 and its clarification of #309; credit, licence, AI statement and dates; significance. Reading only: no computation ran in this lane (F1).
    verdict: accepted
    covers: [T-095]
```

**`external_review` on `T-095`’s report evidence entry:** `state: informally-verified`,
`date: '2026-10-05'`, with this path. The note should say:

- No mathematical defect was found, and every lemma re-derives.
- Unchecked here: every computed fact. The certificate’s integers were not read, and no
  bin was decided, because execution was refused in this lane.
- The bound rests on the complete replay of Daniel’s verifier and the native route.
- F1 to F9, none blocking.

Recording it moves `T-095` to `C1` under `epistemics.md`, and its status reads
*reviewed*.

**At the exit, after the replay passes:**

- add the replayed-here evidence, with the binary and input digests (F2);
- write the `composition` per F3 and F9;
- add the clause of §8 to the significance rationale; and
- set the claim’s date to 2026-10-05.

If the replay fails, record it with `replay_status: failed` and leave the verified field
at `T-079`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
