# wand125 Certificates of 5 October and the Independent Replays: Review of `s(67) ≥ 212/25`, `s(84) ≥ 9411/1000` and the sqverify-fast Route

On 5 October 2026, at 06:06 and 06:07 UTC, wand125/square-packing-bounds published two
rectangle densities checked at coverage one, `mixed_n67_L848` ($s(67) \ge 212/25$) and
`mixed_n84_L9411` ($s(84) \ge 9411/1000$). They are registered as `T-094` at `V0/C0`
with draft significance `S3`. Both were then decided here by `sqverify-fast`, the
repository’s clean-room measure verifier, at all 201 net directions, with negative
controls on each.

This review decides two things.

**The mathematics of `T-094`: accepted, no blocking defect.** The argument from each
measure to its bound is the one the 3 and 5 October reviews re-derived, and every
premise holds in exact arithmetic recomputed here by code written for this review.
Both `code/` directories are the checker read on 28 September and on 2, 3 and 5 October,
byte for byte. Each margin, comparison and supersession in the records is right, and
neither bound carries to $n = 68$ or 85 in either lane.

**The independent replays: a complete replay here.** A passing sqverify-fast census row
and a passing control receipt on the retained candidate are a complete replay in the
sense the policy uses (`epistemics.md`, Integrated; `packing/frontier/README.md`). With
a review of the certificate’s mathematics, they may move a count’s verified lower bound.
The confirmation they give is *independently re-implemented*: code that shares none of
the source’s verification code decided the claim, by the same method.
For `T-094` the receipts pass every check below, so the verified lower bounds at
$n = 67$ and 84 may move to $212/25$ and $9411/1000$, at `V3/C3`. The same decision
carries to the 50 certificates of `T-082`, `T-090` and `T-091` on the per-certificate
conditions in [Carrying the Route](#carrying-the-route-to-t-082-t-090-and-t-091).
`result-import.md`’s sentence that the replay “runs the source’s own verification” is
narrower than the policy it implements.
That is a defect in the process text, not a conflict with the route (IR-2).

Five non-blocking findings are recorded (IR-1 to IR-5). `S3` is confirmed for `T-094`.

The reviewer is an AI agent, the review lane of the 2026-10-05 stage 4 for `T-094` and
the independent replays, prompted separately from the lane that registered `T-094` and
from the lane that ran the replays, sharing no context with either; model
`claude-opus-5-5` (tbd-strong tier).
It was written after the replays and with their receipts in hand, so it is not blind to
them. It registers nothing and moves no bound.

## Scope and Evidence

The subject is the
[5 October packet](../../../packing/resources/web/wand125-mixed-bounds-2026-10-05/README.md),
pinned at `a541afbe` (5 October 06:07:08 UTC), and the census of its two candidates:

| Claim | Directory | Commit (UTC) | Rectangle rows | Distinct images | Mass |
| --- | --- | --- | ---: | ---: | --- |
| $s(67) \ge 212/25$ | `mixed_n67_L848` | `6c0842ed`, 10/05 06:06:37 | 536 | 4,288 | $6699999/100000$ |
| $s(84) \ge 9411/1000$ | `mixed_n84_L9411` | `a541afbe`, 10/05 06:07:08 | 686 | 5,428 | $8399999/100000$ |

Read in full: the packet README, `acquisition/upstream-subtree.sha256`, both directory
READMEs and manifests, the two candidates and certificates, `receipts/mixed-audit.json`
and both `fetch.json`; the root README’s two new sections, its Attribution and its
Status; `T-094`, its two report entries and the intake paragraphs of `n-067.md` and
`n-084.md`, with the lanes of `n-067`, `n-068`, `n-084` and `n-085`. For the replays:
`census.json` (both cases), both `*.jsonl.gz` and both `*.control.json`;
`devtools/sqverify_fast_census.py` (the run, the control and the evidence template),
`mixed_exact` and `mixed_mutant` of `devtools/check_sqverify_fast.py`,
`tests/test_sqverify_fast_census.py`, and the row `V-sqverify-fast` of
`frontier/verifiers.yaml`. For the verifier: its README, `SOUNDNESS.md`,
`INDEPENDENCE.md`, `independence-record.yaml`, `build.rs`, and its two reviews of 3
October, [soundness](review-2026-10-03-sqverify-fast-soundness.md) and
[testing and independence](review-2026-10-03-sqverify-fast-testing-and-independence.md).
Read again, for the argument and its precedents: the
[5 October review](review-2026-10-05-wand125-october-4-certificates.md) of `T-090` and
`T-091`, the [3 October review](review-2026-10-03-wand125-october-3-certificates.md) of
`T-082`, and the process and policy texts the brief names (`result-import.md` stage 4,
`epistemics.md`, `packing/frontier/README.md`, bead `think-mt6e`).

Run here, in the worktree at `e38b78165`, on one core of a shared four-core x86-64 Linux
host:

- this review’s own exact checks (`premises.py` in the lane’s scratch space, standard
  library only, importing nothing from the crate, the census tool, the audit tool or the
  source): every premise below, both measures’ D4 expansions, and the exact capture at
  the least-bound leaf centre of each control receipt and at each control witness, by
  its own polygon clipping;
- `sha256sum` of both `code/` directories’ pinned digests against the retained
  `mixed_n50_L740/code/` and `requirements.txt` (eleven files, all equal), and of the
  decompressed candidates against the packet’s pins (equal);
- `git diff 4ddf37d9c HEAD` over the crate, and `source_sha256` recomputed at both
  revisions by `build.rs`’s rule;
- `cargo build --release -j 1` in `packing/sqverify_fast/` (1 minute 8 seconds; binary
  `af0871c0…`, the census’s binary byte for byte);
- six directions with that binary at one thread: indices 0, 43 and 77 of
  `mixed_n67_L848` (10.5 CPU seconds) and 1, 111 and 170 of `mixed_n84_L9411` (28.9 CPU
  seconds);
- from `packing/` with the project CPython 3.14.7: `pytest -q -n 0
  tests/test_sqverify_fast_census.py` (5 passed), `devtools.retained_data check` on the
  packet (no problem), `devtools.audit_wand125_point_and_mixed mixed-audit
  wand125-mixed-bounds-2026-10-05 --check` (exit 0) and
  `devtools.sqverify_fast_census --family mixed --check --only NAME` for both (“1 of 1
  retained certificates VERIFIED”, exit 0 each).

About 45 CPU seconds of verification and two CPU-minutes in all.
No full census was rerun.

## The Argument From Certificate to Bound

The argument is the one the 3 and 5 October reviews re-derived.
Here it is restated in the form both checkers need, since the route decision turns on
it. For a nonnegative measure $\mu$ on $K = [0, L]^2$ of total mass $M < n$:

1. **Orientation, per square.** A unit square’s angle $\varphi$ is defined modulo
   $\pi/2$. If $\varphi > \pi/4$, reflect the whole configuration in the diagonal.
   The reflection maps $K$ and $\mu$ to themselves (the measure is $D_4$-invariant) and
   sends that square’s angle into $[0, \pi/4]$. A core found for the reflected square
   reflects back to a core of the same measure inside the original square.
   So the bound needs only angles in $[0, \pi/4]$, square by square.
2. **Net.** With $D = 83/40000$ and $t_r = rD$ for $r = 0, \dots, 200$,
   $(1 + t_{200})^2 - 2 = 89/40000 > 0$, so $t_{200} > \tan(\pi/8)$. Every half-angle
   tangent $\tan(\varphi/2) \in [0, \tan(\pi/8)]$ lies within $D/2$ of some $t_r$. The
   last bin is nonempty, since $(1 + t_{200} - D/2)^2 - 2 = -4544311/6400000000 < 0$.
3. **Shrink.** With $z = \tan(\delta/2) \le D/2$ for the offset $\delta$ between
   $\varphi$ and $\theta_r = 2\arctan t_r$, the concentric core of side $B = 9977/10000$
   at $\theta_r$ has extent
   $B(1 + 2z - z^2)/(1 + z^2) \le B(1 + D) = 399908091/400000000 < 1$ along each of the
   square’s axes. So it lies in the square’s open interior.
   The stronger tangent form that sqverify-fast’s admission also checks holds:
   $1 - B(1 + D/(1 - D^2/4)) = 14705281553/63999931110000 > 0$.
4. **Per-bin domain (format M).** $\rho(a) = (1 + 2a - a^2)/(2(1 + a^2))$ is half the
   axis extent of a unit square at half-angle tangent $a$, increasing on
   $[0, \tan(\pi/8)]$. So the centre of a unit square in bin $r$ lies in
   $[\rho(a_r), L - \rho(a_r)]^2$, with $a_r = \max(0, t_r - D/2)$. A quarter turn about
   the centre of $K$ fixes $\mu$, the core’s angle and that domain, so coverage needs
   checking only on the quadrant $[L/2, L - \rho(a_r)]^2$; at $r = 0$ that is
   $[L/2, L - 1/2]^2$. Each domain is nonempty, with least half-side $3.5329$ at
   $n = 67$ and $3.9984$ at $n = 84$. It omits a strip at least $1.2050 \times 10^{-4}$
   wide of Tokoharu’s domain $[L/2, L - B(c_r + s_r)/2]^2$, as for every earlier mixed
   certificate.
5. **Count.** If every core at every net angle and every centre of its domain has
   $\mu \ge 1$, the cores chosen in a packing of $n$ squares are pairwise disjoint, each
   inside its own square’s interior.
   So $n \le \sum_i \mu(C_i) \le M = n - 1/100000 < n$, a contradiction, and no $n$ unit
   squares pack in $K$; hence $s(n) \ge L$, and the same certificate bounds every larger
   count.

The measure is $D_4$-invariant by construction: each stored rectangle is an orbit
representative whose eight images carry density $m/(8|R|)$. That is the only reading
under which the expanded measure integrates to the declared `total_mass`, which this
review checked exactly for both.
The bound holds for whatever measure is decided with mass below $n$ and coverage one, so
a misreading of the format could misattribute the certificate but could not make the
bound false.

## What Is New in the Measures

- **Counts and sides.** Both supersede a mixed certificate of the source at the same
  count, of 4 October: `mixed_n67_L8475` (485 rows) and `mixed_n84_L94075` (569 rows).
  Each directory README says the candidate was built afresh from a structured initial
  measure and repaired on the full net.
- **Size.** 536 and 686 rows; the 686 at $n = 84$ is below the 853 of `mixed_n94_L995`,
  the most of any retained mixed certificate.
  At $n = 84$, 60 of the 5,488 images coincide with another (orbits on a symmetry axis
  or the diagonal), so the expanded measure has 5,428 distinct rectangles, each merged
  by exact key; at $n = 67$ all 4,288 are distinct.
- **Geometry.** Every rectangle lies inside the container with positive mass.
  The least side is $1.0023 \times 10^{-3}$ ($n = 67$) and $1.0000 \times 10^{-3}$
  ($n = 84$). No rectangle comes nearer a wall than $0.326$ and $0.401$, so no boundary
  convention is exercised.
  Both have no point mass, `scaling_factor` $1$ and the candidate’s own digest as
  `scaling_source_digest`.
- **Minima.** The source records its least oblique bound as $1.0000000005520073$ (index
  83\) and $1.0000000003743108$ (index 127), and axis integer minima of $1.00645$ and
  $1.00200$. sqverify-fast, deciding the same coverage by its own search, finds
  $1.000000000605981$ (index 77) and $1.000000000102596$ (index 111), and axis minima of
  $1.0064606$ and $1.0020099$, each above the source’s conservative axis figure.
  Different algorithms give different leaves; both are above one.

None of this bears on soundness.

## Hypotheses the Checker Assumes

Two checkers now bear on these certificates, and they assume different things.

**The source’s checker** (`mixed_rotated_verify.cpp`, `89b674a6…`). The list of the
[mixed review](review-2026-10-02-wand125-mixed-rectangle-bounds.md#hypotheses-the-checker-assumes)
applies unchanged, and the 5 October review’s account of what binds each item applies to
these two. The eleven pinned files of each `code/` directory and `requirements.txt` have
the SHA-256 of the retained `mixed_n50_L740` copies.
The retaining lane’s `mixed-fetch` checked both tarballs against their pins, all 621
listed files, the driver’s preconditions and the enclosure of the exact candidate by all
200 oblique inputs (4,288 and 5,488 images).
This checker was not run here.

**sqverify-fast**, on the census route.
What its verdict rests on:

1. **The theorem and its lemmas** (`SOUNDNESS.md`, “The Claim” and “Formats M and L”,
   lemma D), accepted by review RA at `4ddf37d9c`, with notes R1 and R2 since folded
   into the text. Its statement is the certificate’s own theorem with the per-bin domain:
   the same $n$, $L$, $B$, net, domain and threshold, and the conclusion that no $n$
   unit squares pack in $K$.
2. **Admission’s exact premises**, each recomputed here independently and equal to the
   receipts’ `premises`. They are $n$ and $L$ (67 and $212/25$; 84 and $9411/1000$,
   which the census also checks against the directory name); the masses, nonnegative and
   summing exactly to the declared total $n - 1/100000 < n$; $B$, with $B(1 + D) < 1$
   and $B(1 + D/(1 - D^2/4)) < 1$; the 201 half-angles of step $83/40000$; the endpoint
   polynomial; $t_{200} \le 1/2$ and $L^2 \ge 2B^2$; format M’s per-bin domain, nonempty
   at all 201 nodes; the threshold, $1$, which is never below one; and no point or
   segment.
3. **Binary64 with IEEE semantics**, round to nearest per operation, no fused
   operations: lemma I1’s directed steps.
   The binary was built from the pinned toolchain (rustc 1.98.0) for x86-64 Linux.
4. **Every direction finishes `verified`.** A budget, depth or audit stop is a refusal,
   and the summary is `VERIFIED` only when all 201 are.
5. **The candidate is the retained file** whose decompressed SHA-256 the packet pins
   (IR-1).

The tarball, the certificate’s per-angle records and the source’s kernel are not among
them. On this route the claim depends on the candidate alone, so the tarball binding the
5 October review judged sufficient (its OF-1) matters only to a replay of the source’s
checker.

## The Trust Boundary

On the census route, coverage at all 201 directions is decided by sqverify-fast alone:
the exact-event vertex sweep at the axis, and outward-rounded interval branch and bound
at the other 200. The exact premises are decided by its admission in exact rationals,
and again by this review’s own code.
The census driver decides nothing; it runs the binary, keeps the receipts, and records
`VERIFIED` only when the binary’s summary says so with exit 0 and 201 rows.

What the route shares with the source’s checker is the mathematics, not code: the
net-and-shrink theorem, the core side, the 201-node net, the per-bin domain lemma and
its fold at $\pi/4$, the D4 orbit format and the threshold one.
A defect in that shared mathematics would affect both checkers alike; this review and
RA’s each re-derived it, and it is sound.
A defect in the source’s implementation would not reach sqverify-fast, nor the reverse.
So this is a second implementation and not a second method, which `epistemics.md` says
does not change the rung.

What remains asserted by the source alone: its per-direction records, node counts and
least bounds, its two pre-publication replays, and anything else its tarball holds.
None of that is part of the claim.

## The Comparisons and the Record

Each side and comparison was checked in exact arithmetic:

- **Over the record.** $212/25 - 339/40 = 1/200$ and $9411/1000 - 3763/400 = 7/2000$,
  the $0.005$ and $0.0035$ by which `T-094`’s claim, both report entries and both case
  records say each exceeds `T-090`’s superseded value.
  Over the verified lane, $212/25 - 1691/200 = 1/40$ and $9411/1000 - 47/5 = 11/1000$.
- **Supersession.** `mixed_n67_L848` supersedes `mixed_n67_L8475` and `mixed_n84_L9411`
  supersedes `mixed_n84_L94075`, both of `T-090`, as each directory README, the root
  README and the case records say; `T-090` keeps its claim, which is about what the
  source reported.
- **Reference values.** Each side exceeds Nagamochi’s $1 + \sqrt{n - 2\lfloor\sqrt
  n\rfloor + 1}$: $(212/25 - 1)^2 = 34969/625 > 52$ and $(9411/1000 - 1)^2 > 67$, by
  $0.269$ and $0.226$ in the side.
  Each exceeds Green’s Theorem 9 value, $8.28997$ and $9.26673$ by the audit’s
  enclosure, by $0.190$ and $0.144$.
- **Monotone carry.** A packing of $n + 1$ squares contains one of $n$, so $s(n + 1) \ge
  s(n)$. At $n = 68$ both lanes hold $851/100 > 212/25$, and at $n = 85$ both hold
  $473/50 > 9411/1000$. Neither bound carries in either lane.
- **Rounded decimals.** The $n = 67$ directory README gives the least oblique bound as
  “`1.0000000006`” for $1.0000000005520073$, and both cite Green’s values rounded at the
  fourth place (“$8.2900\ldots$” for $8.289966$). This is OF-3’s kind, and the record
  cites the certificate’s own values.
- **Credit and AI assistance.** The root README’s Attribution section opens “The method
  is not ours.” and its Status section says “Parts of this work were produced with AI
  assistance under human direction.”
  Both commits end in an AI co-author trailer.
  `T-094`’s claim and both case records say so in the source’s terms.
  `attribution.published` is `2026-10-05`, the date of both commits and of the
  bibliography key, whose credit, `wand125 after Tokoharu, Levy, Stromquist, Nagamochi,
  Burns, Massaccesi`, and `builds-on-project` lineage match the 4 October keys (IR-5).

## The Independent Replays

### What the receipts show

For each certificate, `census.json`, the per-direction receipt and its summary line
agree:

|  | `mixed_n67_L848` | `mixed_n84_L9411` |
| --- | --- | --- |
| Directions | 0 to 200, each once, each `verified` | the same |
| Summary, exit | `VERIFIED`, 0; `refused_directions` empty | the same |
| Fault injection | none (`fault_injected_at_box` null) | none |
| Threshold | $1$, the declared one | the same |
| Premises | format M, per-bin domain, $n = 67$, $L = 212/25$, $M = 6699999/100000$ | format M, per-bin domain, $n = 84$, $L = 9411/1000$, $M = 8399999/100000$ |
| Axis | 13,461,561 vertices, least $1.006460609529837$ | 20,748,025 vertices, least $1.0020099373342157$ |
| Oblique | 91,535,166 boxes, least $1.000000000605981$ at index 77 | 110,704,136 boxes, least $1.000000000102596$ at index 111 |
| Exact capture at the least-bound leaf centre | $1.01861\ldots$ | $1.07008\ldots$ |
| CPU, wall | 1,388 s, 2,122 s at two threads | 1,878 s, 2,765 s at two threads |

The candidate digest in each receipt is that of the retained gzip file, which
decompresses to the SHA-256 that the packet README and
`acquisition/upstream-subtree.sha256` pin (IR-1).

### The build that ran

Every receipt names `source_sha256` `7c49cf79…`, rustc 1.98.0, profile `release`, target
`x86_64-unknown-linux-gnu`, and binary `af0871c0…`. `git diff 4ddf37d9c HEAD` shows
`src/`, `Cargo.lock`, `build.rs` and `rust-toolchain.toml` unchanged since the build the
two reviews accepted, and unchanged since `61acc9dcb`, the last commit the independence
record covers. `build.rs` hashes `Cargo.toml`, `Cargo.lock`, `build.rs` and `src/*.rs`,
and `Cargo.toml` has gained a `[profile.gate-test]` (inheriting release, without fat
LTO) for the gate’s test build.
Recomputed by `build.rs`’s rule, the digest is `7c49cf79…` at `HEAD` and `9985c465…` at
`4ddf37d9c`. The difference is that profile, which the release binary does not use
(IR-4). The binary built here from the worktree is byte-identical to the census’s.

### The spot checks

The six directions run here at one thread returned the census’s rows exactly: verdict,
boxes, leaves, depth, least certified bound, least-bound box and, at the axis, vertices
and argmin. These were indices 0, 43 and 77 of `mixed_n67_L848` (77 the least bound,
379,325 boxes) and 1, 111 and 170 of `mixed_n84_L9411` (111 the least, 574,697 boxes).
The census ran at two threads, so the search is deterministic across thread counts here.
This review’s own exact clipping gives the capture at each control receipt’s leaf centre
equal, as a rational, to both the crate’s value and `mixed_exact`’s. Each centre lies in
its per-bin quadrant.

### The controls

Each control receipt runs the original and two mutants at the least-bound direction.
Each mutant scales every mass by one factor and recomputes `total_mass`, so it stays
admissible, with mass below $n$, and is a false certificate:

|  | Mutation | Verdict | Exact capture below one |
| --- | --- | --- | --- |
| $n = 67$, index 77 | original | `verified`, exit 0, 379,325 boxes | — |
|  | every mass $\times\, 99/100$ | `counterexample-candidate`, exit 1 | at the witness, $1 - 8.75 \times 10^{-11}$ |
|  | every mass $\times\, 0.981727\ldots$ (capture at the centre $1 - 10^{-6}$) | `counterexample-candidate`, exit 1 | at the centre, and at the witness $0.99828$ |
| $n = 84$, index 111 | original | `verified`, exit 0, 574,697 boxes | — |
|  | every mass $\times\, 99/100$ | `counterexample-candidate`, exit 1 | at the witness, $0.99944$ |
|  | every mass $\times\, 0.934504\ldots$ (capture at the centre $1 - 10^{-6}$) | `counterexample-candidate`, exit 1, at the first box | at the centre, and at the witness $0.97128$ |

Each refusal is the verifier’s correct answer: each mutant’s exact capture is below one
at a centre of its domain, so each mutant’s claim is false.
This review recomputed every witness capture with its own clipping; all four equal the
receipt’s `capture_at_witness` and the `exact_coverage` the crate’s `--confirm`
evaluated. `tests/test_sqverify_fast_census.py` holds them as `result-import.md` asks.
It requires both receipts `CONTROLS_REFUSED`, each refusal at exit 1, and each mutant’s
capture below one at the centre or the witness.
It also recomputes `mixed_n67_L848`’s centre and witness captures from the candidate,
and once a replay entry names `V-sqverify-fast`, it requires a verified case and a
refused control for it.
IR-3 says what the controls do not show.

## The Confirmation Route

**The relation.** The deciding program is the crate, which `INDEPENDENCE.md` and
`independence-record.yaml` say was written without opening any of the source’s checkers
or the repository’s checker-driving wrappers.
Review RB found no identifier, constant, limit, message or structure that could only
have come from them, and accepted `independent-implementation`. Its departures from the
clean-room protocol (TI-4) are disclosed in the record, which was written in response.
That git cannot show the lane separation (TI-5) still stands, and the record’s machine
audit (`think-3ok2`) has not run.
Neither weakens the code comparison on which the label rests.
The census driver and `check_sqverify_fast.mixed_exact` are premise checks and controls,
first-party, and import nothing from the source or the audit tools; under
`epistemics.md` a premise check never sets the relation.
So `relationship_to_generator: independent-implementation` is right for these replay
entries, and the result’s confirmation is *independently re-implemented* in
`epistemics.md`’s sense.

**What the two routes establish.** The replays of `T-069`, `T-071`, `T-072` and `T-075`
ran the source’s own checker on the source’s own inputs and required each direction to
return the certificate’s own record.
That establishes that the published computation reproduces, bit for bit, and with the
reviews of the checker’s code it establishes the coverage.
Its confirmation is *reproduced with the producer’s code*. The census route decides the
same coverage from the candidate alone, by a separately written implementation whose
soundness argument was itself adversarially reviewed.
It does not reproduce the source’s records, which the claim does not need, and needs no
tarball. It cannot share an implementation defect with the source’s checker; it does
share the method and the per-bin domain lemma.
For the claim, the census route is the stronger confirmation.
For checking the source’s own run, only the source-checker replay serves.
Both are one complete replay, which is what `C3` needs.
Neither is a second method, and both together would still be `C3` until rung 4’s reviews
and oversight are on file.

**Is it a complete replay?** Yes, when the census row and the control receipt pass the
checks above: every one of the 201 directions `verified` with the summary `VERIFIED` and
exit 0, at threshold one, from an admitted candidate whose digest is the packet’s pin,
by a build whose crate source is the reviewed one, with a refused control held by the
test. The policy asks that “a complete replay here and a review of the mathematics have
discharged the certificate’s assumptions” (`epistemics.md`, Integrated) and “a complete
replay here and a review of its mathematics under `docs/project/reviews/`”
(`packing/frontier/README.md`). Neither names the source’s checker.
`think-mt6e`, the open gate, asks for a replay here and a mapped review and nothing
more.

**The process text.** `result-import.md` says “The replay runs the source’s own
verification on the retained bytes, in full.”
The same section then lists `independent-implementation` among the relations a replay
may have, and allows the repository’s own sequence where the source’s script cannot
pass. That sentence describes the only route that existed when it was written, and it is
narrower than the policy it implements.
So the wording is a defect in the process text (IR-2), not a conflict with the route.
A records lane following it literally would refuse this route, so it should be amended
with the first exit that uses the route.

## The Rung

With these receipts, two replay evidence entries (`origin: replayed-here`,
`method: interval-certified`, the retained candidate as `certificate`, the census
command as `replay`, `replay_status: passed`, `verifiers: [V-sqverify-fast]`) and this
review recorded on both report entries, each part of `T-094` derives `V3/C3`, and so
does the entry. The control receipts are the existing control path `C3` asks for.

Rung 4 is not available.
It needs two retained adversarial AI reviews of `T-094` by distinct reviewers, the
latest accepting, and a human oversight record.
This is one review; the two reviews of 3 October are of the crate, not of this claim,
and there is no oversight record.

The verified lower bounds may move: $n = 67$ from $1691/200$ to $212/25$, and $n = 84$
from $47/5$ to $9411/1000$, each on its own certificate.
No other count’s verified bound moves, by the carry above.
The register reads *confirmed, independently re-implemented*, and nowhere *reproduced
with the producer’s code*: the source’s checker has not run here on either certificate.

## Carrying the Route to T-082, T-090 and T-091

The same decision carries to each of the 22 certificates of `T-082`, the 16 of `T-090`
and the 12 of `T-091` when its census row and control receipt land.
Their mathematics was read by the 3 and 5 October reviews, which accepted all 50 with no
defect open. The argument above is the one those reviews derived, and it does not depend
on the count, the side or the number of rows.
All 50 retained candidates are format M rectangle densities with no point mass,
`scaling_factor` $1$ and $B = 9977/10000$; checked here.

A records lane checks, for each certificate:

1. **The case.** `census.json` names the certificate with `n` and `L` equal to its
   report entry’s claim, `status` `VERIFIED`, `returncode` 0, `directions_verified` 201,
   `refused_directions` empty, `threshold` `1`, and
   `least_bound_leaf_exact.clears_threshold` true.
2. **The premises.** The summary’s `premises` say format M, `centre_domain` `per-bin`,
   `angle_count` 201, `D` `83/40000`, `B` `9977/10000`, `mass_exact` equal to
   $n - 1/100000$, and no point or segment; `fault_injected_at_box` is null.
3. **The candidate.** `candidate_sha256` is the retained `.gz` file’s, and
   `devtools.retained_data check` on its packet passes, binding it to the decompressed
   SHA-256 the packet pins.
4. **The build.** `source_sha256` is `7c49cf79…`, or the diff from `4ddf37d9c` touches
   no file of `src/`, `Cargo.lock`, `build.rs` or `rust-toolchain.toml`; profile
   `release`, rustc 1.98.0.
5. **The control.** `CONTROLS_REFUSED`, both mutants refused at exit 1 with an exact
   capture below one, and `tests/test_sqverify_fast_census.py` passing with the new
   entry in the register.
6. **The values.** At $n = 88$ and 94, where `T-091` raised `T-090` the same day, the
   verified value is the larger certificate whose row passes.
   At $n = 67$ and 84, `T-094`’s certificates supersede `T-090`’s for the verified lane;
   `T-090`’s own rung at those counts still waits on its own rows.
   Each move is checked against the next count for the monotone carry.
7. **The words.** The entry says *independently re-implemented*, and `next_rung` no
   longer plans a source-checker replay as the condition of the move.

Another review is needed before the route carries if:

- the crate’s `src/`, lockfile, `build.rs` or toolchain changes; such a diff gets a
  soundness re-review like RA’s;
- a certificate is outside what the 3 and 5 October reviews read: points or segments,
  format L, another core side, net, domain or threshold, or densities near lemma F3’s
  caps;
- the census driver’s verdict, admission arguments or control logic change;
- a defect is found in the shared mathematics (the per-bin domain or the fold), which
  would reopen every certificate on either route.

A row that is `PARTIAL`, `unresolved`, `audit-failed` or otherwise refused, or a control
that is `CONTROL_FAILED`, moves nothing.
It is recorded as a failed replay and needs no review to stay where it is.

## Findings

No blocking finding.

### IR-1 — Note, in the receipts: the candidate digest is the stored gzip file’s

`census.json`, the summary’s `premises.input_sha256` and the control receipt name the
SHA-256 of `candidate.json.gz` as stored (`661bd0a3…` and `facfaba5…`), not the SHA-256
of the decompressed upstream bytes that the packet README and
`acquisition/upstream-subtree.sha256` pin (`d6393c7c…` and `10ad1ed9…`). The binding
still holds. The stored file is deterministic gzip (`gzip -9n`), and
`devtools.retained_data check` passes on the packet, re-deriving the decompressed digest
of each stored file.
This review decompressed both and found the pinned digests.
The crate refuses a gzip input with a second member or trailing bytes (TI-2), so it
reads exactly those bytes.
The evidence entry should state both digests, or that the stored file decompresses to
the pinned one, as the evidence template’s third assumption already says in words.

### IR-2 — Low, in the process: `result-import.md` says the replay runs the source’s own verification

The sentence “The replay runs the source’s own verification on the retained bytes, in
full” (stage 4, “The replay”) is narrower than `epistemics.md` and
`packing/frontier/README.md`, and narrower than the section’s own list of relations.
It should read, for example: “The replay runs a complete verification of the retained
certificate: the source’s own checker, or a first-party implementation of the same
theorem that has been adversarially reviewed for soundness and whose independence is
recorded, in full. A fast tier or a sample of roots is a diagnostic.”
It blocks nothing in the mathematics.
It should land in the same change as the first exit that moves a verified bound on this
route, so that no stage-4 text forbids what the exit does.
The `next_rung` texts of `T-082`, `T-090` and `T-091`, which plan source-checker
replays, change when their rows land.

### IR-3 — Note, in the controls: what they show and what they do not

The controls show that the verifier, given an admissible false certificate near each
original, says no. They do not show discrimination near the threshold at both counts.
The sharp case is the $99/100$ mutant at $n = 67$, refused at a witness
$8.75 \times 10^{-11}$ below one.
The near-threshold mutant at $n = 84$ is refused at its first box, whose centre captures
$0.971$, so its name describes the centre it was scaled at, not the refusal.
The verifier’s discrimination near the threshold rests on RB’s 9,726 refusals of exact
counterexamples, the smallest deficit $3.9 \times 10^{-121}$. The test recomputes the
witness capture from the candidate only for `mixed_n67_L848`. `mixed_n84_L9411`’s rests
on the receipt, and this review recomputed it equal.
Recomputing every receipt’s witnesses in the test would cost a second each.

### IR-4 — Note, in the record of the build and the driver

The build identity differs from the reviewed one for a reason the records should state.
`source_sha256` is `7c49cf79…` against `9985c465…` at `4ddf37d9c` because `build.rs`
hashes `Cargo.toml`, which has gained the gate’s test profile.
The evidence template says the crate’s `src/` is unchanged since `4ddf37d9c`, which is
true, but a reader comparing digests will find them different; one clause saying why
closes that. The census driver’s `--control` and `--evidence` modes postdate both crate
reviews.
This review read them: they decide nothing, the control’s acceptance test is the
one the table above applies, and the evidence template’s fields match the receipts.
Its theorem line, “no $n$ unit squares fit in a square of side below $L$”, understates
the certificate, which excludes side $L$ itself; it is not wrong.
`V-sqverify-fast`’s `source` lists the crate and the census driver but not
`devtools/check_sqverify_fast.py`, whose `mixed_exact` and `mixed_mutant` the driver
runs for the controls.
Adding it would make the row name every program the replay runs, as `result-import.md`
asks.

### IR-5 — Note, register-wide: the credit sentence of the claim

`T-094`’s claim ends “wand125 after Tokoharu and Levy”, the form of every wand125 entry
in the register. The bibliography credit, which the renderers print, is
`wand125 after Tokoharu, Levy, Stromquist, Nagamochi, Burns, Massaccesi`, and
`epistemics.md` says hand-written prose may add to the credit but never drops a link.
This is not `T-094`’s alone, and nothing here changes it.
Whether the register’s short prose form is meant to be exempt is a question for the
register, not a defect of this import.

## Claims by Evidential Status

- **Recomputed here in exact arithmetic, by code sharing nothing with the crate, the
  census tool, the audit tool or the source:** both measures’ count, side, core, rows,
  containment, nonnegativity and mass, and the D4 expansion integrating to the mass;
  every admission premise of format M, including the per-bin domains at all 201 nodes;
  the margins, the comparisons with Green’s and Nagamochi’s values, and the monotone
  carry; the exact capture at both control centres and all four control witnesses.
- **Checked here on the files and in Git:** the decompressed candidates against the
  packet’s pins; both `code/` directories’ pinned digests against the retained copy; the
  crate’s source against `4ddf37d9c`; `source_sha256` at both revisions; the binary,
  rebuilt byte for byte.
- **Replayed here by this review:** six of the 402 directions, each returning the
  census’s row exactly.
- **Decided here by the replay lane, and checked here against its receipts:** all 201
  directions of each certificate `verified`, summary `VERIFIED`, exit 0, and the two
  controls refused, with the census `--check` and the test passing.
- **Reviewed by reading:** that sqverify-fast’s theorem is the certificate’s claim, that
  its verdict and the census’s `VERIFIED` mean what a complete replay needs, that the
  relation is `independent-implementation`, and that the driver’s new modes decide
  nothing.
- **Asserted by the source, not checked here:** its per-direction records, its node
  counts and least bounds, and its two pre-publication replays.

## Significance

`S3` is confirmed. The two bounds are further sizes from the generator and checker of
`T-069`, `T-071`, `T-072`, `T-075`, `T-082`, `T-090` and `T-091`. They raise the
source’s own values of the day before by $0.005$ and $0.0035$, and the verified lane by
$0.025$ and $0.011$. They settle no count: the best known packings have sides
$8 + \sqrt 2/2$ and $9 + \sqrt 2/2$, $0.227$ and $0.296$ above.
These are substantive case results with no new technique.
That they are the first certificates of the source to reach the verified lane by an
independently re-implemented replay is a fact about this repository’s confirmation, not
about the result, and does not raise the score.

## Disposition

Both certificates are accepted by this review with no defect open, and the census route
is accepted as a complete replay here.
For `T-094`: `C1` once this document is recorded as `external_review` on its two report
entries and listed in the entry’s `reviews`, with the document mapped as a retained
review. Then `V3/C3` once the two replay evidence entries are added from the receipts
reviewed here. Then the verified lower bounds at $n = 67$ and 84 move to $212/25$ and
$9411/1000$, and `claim`, `notes` and `next_rung` are rewritten together and `activity`
removed. IR-2’s amendment goes with that exit.
IR-1’s and IR-4’s clauses go into the evidence entries.
IR-3 and IR-4’s registry line are for the replay lane.
IR-5 is for the register.
Nothing here is for the author.
The reply on issue 282 should say that both bounds were confirmed, independently
re-implemented, by this repository’s own verifier, and that the source’s checker was not
run here.

## For the Records Lane

**`reviews:` entry for `T-094`:**

```yaml
- path: docs/project/reviews/review-2026-10-05-wand125-october-5-and-independent-replays.md
  kind: adversarial
  reviewer: >-
    AI agent, the review lane of the 2026-10-05 stage 4 for T-094 and the independent
    replays (claude-opus-5-5, tbd-strong tier), prompted separately from the registering
    and replay lanes
  reviewer_kind: ai
  relation: project
  date: '2026-10-05'
  scope: >-
    The mathematics of mixed_n67_L848 and mixed_n84_L9411, every exact premise recomputed
    by its own code, and the sqverify-fast census rows and control receipts as a complete
    replay here; written after the replays
  verdict: accepted
  covers: [T-094]
```

**`external_review` on `E-n067-wand125-mixed-848-report` and
`E-n084-wand125-mixed-9411-report`:**

```yaml
external_review:
  state: informally-verified
  date: '2026-10-05'
  reviewed_by: >-
    AI agent, the review lane of the 2026-10-05 stage 4 for T-094 and the independent
    replays (claude-opus-5-5, tbd-strong tier), prompted separately from the registering
    and replay lanes, after the replays;
    docs/project/reviews/review-2026-10-05-wand125-october-5-and-independent-replays.md
  note: >-
    No mathematical defect. The argument from the measure to the bound is the one the 3
    and 5 October reviews derived, and every premise (mass n - 1/100000 < n, the core
    side, the 201-node net, the endpoint polynomial, format M's per-bin domain) was
    recomputed in exact arithmetic by code sharing nothing with either checker. The
    code/ directory is the checker read on 28 September, byte for byte. The margin over
    T-090's superseded value and the comparisons are right, and the bound carries to no
    larger count. The sqverify-fast census and control receipts are a complete replay
    here, independently re-implemented. Unchecked: the source's own per-direction
    records and pre-publication replays.
```

Each note may add its own count’s figures (margin $1/200$ or $7/2000$; least certified
bound and index).

**Each replay evidence entry’s `limitations` must state:**

- that sqverify-fast, this repository’s clean-room verifier, decided the retained
  candidate at all 201 directions, every one `verified`, summary `VERIFIED`, exit 0, at
  threshold one, with format M’s per-bin domain; and the axis vertices and least
  capture, the oblique boxes and least bound with its index, CPU and wall seconds,
  threads, and the host;
- the candidate binding: the stored gzip file’s SHA-256 that the receipts name, and the
  decompressed SHA-256 the packet pins, which `devtools.retained_data check` ties
  together (IR-1);
- the build: `source_sha256` `7c49cf79…`, rustc 1.98.0, release, x86-64 Linux; `src/`,
  the lockfile and `build.rs` unchanged since `4ddf37d9c`, the build both 3 October
  reviews accepted, and the digest different from that build’s only because `Cargo.toml`
  gained the gate’s test profile (IR-4);
- that it is a second implementation, not a second method.
  It shares no code with the source’s checker, but shares its theorem, net, core side,
  per-bin domain lemma and threshold, so a defect in that mathematics would affect both.
  That mathematics was re-derived in this review and in the soundness review of 3
  October;
- the controls: the original verified again at the least-bound index; every mass scaled
  by $99/100$, and every mass scaled to put the leaf centre’s capture $10^{-6}$ below
  one, each refused with an exact capture below one at the witness or the centre;
  recomputed apart from the crate; held by `tests/test_sqverify_fast_census.py`;
- that the source’s own checker was not run here on this certificate, its tarball is
  pinned by digest and not retained, and its records are not reproduced: the replay’s
  node counts and bounds are its own;
- that this review reran six directions with a rebuilt, byte-identical binary and
  recomputed the premises and control captures with its own exact code;
- `relationship_to_generator: independent-implementation`, with the independence record
  of `V-sqverify-fast`, and the audit record this document.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
