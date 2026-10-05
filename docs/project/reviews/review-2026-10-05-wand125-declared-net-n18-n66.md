# wand125’s `s(18) ≥ 47/10` on a Declared Net and `s(66) ≥ 843/100`: Review of T-096, T-097 and the sqverify-fast Declared-Net Change

On 5 October 2026 wand125/square-packing-bounds published two more rectangle densities
checked at coverage one, both pinned in this repository at `43050edc`. `mixed_n66_L843`
proves $s(66) \ge 843/100$ on the standard net, superseding the source’s
`mixed_n66_L842` (T-069), and is registered as T-097. `mixed_n18_L470` proves
$s(18) \ge 47/10$ on a net its candidate declares, core side $999/1000$ and 416
half-angle tangents of step $1/1001$, where every earlier mixed certificate of the
source has core $9977/10000$ on 201 tangents of step $83/40000$; it is registered as
T-096. To decide that certificate, this repository’s clean-room verifier `sqverify-fast`
was changed (commit `f007d7afd`) to admit a format M file on the net it declares, under
a new lemma N0.

The argument from each certificate to its bound holds.
For $n = 66$ nothing differs from T-069’s kind but the measure.
For $n = 18$ the declared net carries the argument: re-derived here in exact arithmetic,
$999/1000 \cdot (1 + 1/1001) = 500499/500500 < 1$, the last tangent $415/1001$ is past
$\tan(\pi/8)$, and the per-bin centre domain at half-step $1/2002$ is nonempty and
correct at all 416 nodes.
Lemma N0 is correct and complete, and admission cannot be led by any declaration tried
here to accept a net the lemma does not cover.
Every number and comparison in the records is right but two statements about work done
here.
`sqverify-fast` decided all 416 directions of `mixed_n18_L470` in this review’s own
run.

One finding is blocking, and it is in this repository’s tool rather than in either
certificate: `audit_wand125_declared_net compare`, which T-096’s `next_rung` names for
the $n = 18$ exit, reports `FULL_REPLAY_MATCHES_SHIPPED` for a copy of the bundle on
which no replay ran, if the copy did not keep file times, and reports `MISMATCH` for a
complete, correct replay (DN-1). The verified lower bound at $n = 18$ must not move on a
receipt from it until it is fixed.
Nine further findings are non-blocking.
`S3` is confirmed for both.
Both entries can take `C1` from this review; each takes `V3/C3`, and its count’s
verified lower bound moves, only when a complete replay of the source’s own checker
returns the certificate’s record at every direction of its net.
A `sqverify-fast` pass, complete or not, moves neither the rungs nor the verified lower
bound under the present rules.

This is the review of stage 4 of the result import for jlevy/squares#366 and the 5
October comment on jlevy/squares#282 that requests $n = 66$, and of the verifier change
the first of them needed.
It was written on 2026-10-05 by an AI agent, the review lane of the 2026-10-05 evening
intake’s lane B (T-096, T-097 and the `sqverify-fast` declared net), separately
prompted, sharing no context with the lane that retained and registered the results,
changed the verifier and is replaying the certificates; model `claude-opus-5-5`
(tbd-strong tier). It was written after retention and registration and before any
complete replay. It registers nothing and moves no bound.

## Scope and Evidence

| Entry | Claim | Directory | Commit (UTC) | Rectangles | Mass | Core $B$ | Net |
| --- | --- | --- | --- | ---: | --- | --- | --- |
| T-096 | $s(18) \ge 47/10$ | `mixed_n18_L470` | `43050edc`, 10/05 09:21:25 | 136 | $1799999/100000$ | $999/1000$ | step $1/1001$, 416 nodes, declared |
| T-097 | $s(66) \ge 843/100$ | `mixed_n66_L843` | `d73ce20d`, 10/05 08:11:44 | 713 | $6599999/100000$ | $9977/10000$ | step $83/40000$, 201 nodes, standard |

Read in full: the
[packet README](../../../packing/resources/web/wand125-mixed-bounds-finer-net-2026-10-05/README.md),
its `acquisition/` records and its four receipts; both directory READMEs and
`manifest.json` files, the retained candidates and certificates, and the root README
(diffed against the morning packet’s copy, from which it differs by the two new sections
alone); T-096 and T-097, with T-045, T-046, T-069 and T-094 for comparison; the two
report entries, the two case records’ changes, the coverage entry, the bibliography key
and its row; `V-wand125-mixed-rotated-verify-cpp` and
`V-wand125-verify-mixed-full-proof-py`; the whole of `git show f007d7afd`, with
`certificate.rs` around it (`read_json`, the duplicate-key visitor, `sources`,
`domain_upper`, `direction`, `admit`) and `SOUNDNESS.md`’s theorem, lemmas D and F3 and
the new section; `tests/declared_net.rs`; the `declared-net` group of
`devtools/check_sqverify_fast.py` and the census change; `INDEPENDENCE.md` and
`independence-record.yaml`; `devtools/audit_wand125_declared_net.py` and its test; the
`n66-L843` row of `devtools/audit_wand125_point_and_mixed.py`, with its
`_semantic_digest`, `check_inputs` and `compare_driver_run` for comparison; and the
`check_standing` change of `52d8e8bd7` with its test.
Read for what they require: `result-import.md` (stage 4 and the exit), `epistemics.md`
(Verification, Confirmation, Which Code Confirmed It, Review Records, Significance and
Novelty, Results by Others), the frontier README’s verified-lane rule, the verifier plan
and the four precedent reviews.
The source’s retained `code/` files were read for one section,
[What the Authors’ Code Shows](#what-the-authors-code-shows), and for nothing else here.
The #366 reporter’s patch was neither requested nor read.

Run here, with the project CPython 3.14.7 on x86-64 Linux, one core under `nice`:

- `audit_wand125_declared_net audit --check` and `audit_wand125_point_and_mixed
  mixed-audit wand125-mixed-bounds-finer-net-2026-10-05 --check`: `RECEIPT_MATCHES` for
  both; `retained_data check` on the packet: no problem; `acquire_source … --check`:
  `PACKET_MATCHES_ITS_CONTRACT`; `pytest` on `test_audit_wand125_declared_net.py` and
  `test_check_standing.py`: 51 passed.
- This review’s own exact arithmetic, in a scratch script sharing nothing with
  `sqverify-fast`, the source’s checkers or the audit tools: each candidate’s mass,
  rows, containment and digest; each net’s identities; the per-bin domain at every node;
  the records’ least bounds, node totals and axis figures; and every margin and
  comparison in the records.
- `cargo build --release` of `sqverify-fast` at this commit, then
  `sqverify-fast --candidate … --n 18 --directions all`: all 416 directions verified
  (see [What a sqverify-fast Pass Supports](#what-a-sqverify-fast-pass-supports));
  `--n 66 --directions 0,157`: both verified.
- `check_sqverify_fast --only declared-net` without `--quick`.
- Seventeen hand-made declarations against admission (DN-6), and a probe of `compare` on
  two synthetic bundle trees (DN-1), both in scratch space.

The proof-bundle tarballs were not fetched here, so nothing in this review rests on a
bundle file but through the retaining lane’s receipts.
No direction was replayed with the source’s checker.

## The Argument From Certificate to Bound

For a nonnegative measure $\mu$ on $[0, L]^2$, invariant under its $D_4$ symmetries, of
mass $M < n$, a core side $B$ and half-angle tangents $t_r = rD$, $r = 0, \dots, m$:

1. **Fold.** A unit square’s orientation $\varphi$ is defined modulo $\pi/2$, and the
   reflection in the diagonal maps the container and $\mu$ to themselves and sends
   $\varphi \in (\pi/4, \pi/2)$ to $\pi/2 - \varphi$. So $\varphi \in [0, \pi/4]$ and
   $u = \tan(\varphi/2) \in [0, \sqrt 2 - 1]$.
2. **Reach.** If $t_m^2 + 2t_m - 1 > 0$, then $t_m > \sqrt 2 - 1$, and every
   $u \in [0, \sqrt 2 - 1]$ lies within $D/2$ of a node $t_r$.
3. **Shrink.** The square’s angle differs from $\theta_r = 2\arctan t_r$ by $\delta$
   with $z = \tan(\delta/2) = |u - t_r|/(1 + u t_r) \le D/2$. A square of side $B$
   rotated by $\delta$ about the unit square’s centre has extent
   $B(\cos\delta + \sin\delta) = B(1 + 2z - z^2)/(1 + z^2)$ along each of the unit
   square’s axes, and the unit square is the intersection of the two slabs those axes
   bound, so the core lies in its open interior exactly when that extent is below $1$.
   The extent is at most $B(1 + 2z) \le B(1 + D)$, so $B(1 + D) < 1$ is sufficient.
   It is not necessary: the extent increases in $z$ on $[0, \sqrt 2 - 1]$, and $D/2$
   lies far inside that range, so the sharp condition is the extent at $z = D/2$,
   $B(1 + D - D^2/4)/(1 + D^2/4) < 1$, which $B(1 + D) < 1$ implies.
4. **Domain.** The squares assigned to node $r \ge 1$ have $u \ge a_r = \max(0,
   t_r - D/2)$, and on $[0, \pi/4]$ a unit square’s half extent
   $\rho(u) = (1 + 2u - u^2)/(2(1 + u^2)) = (\cos\varphi + \sin\varphi)/2$ increases, so
   its centre, which is its core’s centre, lies in $[\rho(a_r), L - \rho(a_r)]^2$. By a
   quarter turn it suffices to check $[L/2, L - \rho(a_r)]^2$. A node whose $a_r$ lay
   past $\sqrt 2 - 1$ would get a larger domain than needed, which costs work and not
   soundness.
5. **Count.** If every core of side $B$ at a net angle with its centre in its node’s
   domain has $\mu$-measure at least $1$, the $n$ disjoint cores of a packing give
   $n \le M < n$. So $s(n) \ge L$, and every larger count too.

The hypotheses the checker assumes are the ten of the
[2 October review](review-2026-10-02-wand125-mixed-rectangle-bounds.md#hypotheses-the-checker-assumes),
with the domains, the tangents and the node count now read from the candidate rather
than fixed.

### `n = 66`: what carries over from T-069

Everything. The net is the standard one ($B = 9977/10000$, $D = 83/40000$, 201 nodes),
the candidate declares none, and the `net` blocks of its manifest and certificate equal
the recomputed facts: $B(1 + D) = 399908091/400000000$, $t_{200}^2 + 2t_{200} - 1 =
89/40000$, the last bin’s floor $399/2 \cdot 83/40000$ below $\sqrt 2 - 1$. The mass is
exactly $6599999/100000$, the 713 rows have positive mass on nondegenerate rectangles
inside $[0, 843/100]^2$, `points` is empty, the scaling factor is $1$, and the candidate
digest recomputed here by the source’s rule, `24cdd5b6…`, is the one the manifest, the
certificate and the audit name.
`mixed-fetch` found all 200 oblique inputs enclosing the exact candidate recomputed
here. As for T-069, coverage at the 200 oblique directions is the source’s C++ alone and
the axis its integer tables.

### `n = 18`: the declared net, re-derived

Recomputed here in exact rationals from the retained candidate:

- **The measure.** 136 rows, every one of positive mass on a nondegenerate rectangle
  inside $[0, 47/10]^2$; mass $1799999/100000 = 18 - 1/100000$, equal to `total_mass`;
  `points` empty; scaling factor $1$; candidate digest by the source’s rule, which
  covers `proof_net`, `c860286b…`, equal to the manifest’s, the certificate’s and the
  candidate’s own `scaling_source_digest`.
- **Containment.** $D = 1/1001$, so $B(1 + D) = (999/1000)(1002/1001) =
  500499/500500$, a margin of $1/500500$, and $1/1001000$ on each edge.
  The sharp condition gives $4007994993/4008005000$, a margin of about
  $2.50 \times 10^{-6}$. The core rotates by at most $2\arctan(1/2002)$, whose tangent
  is $D/(1 - D^2/4) = 4008004/4012011003$, and the tangent form is
  $B(1 + D/(1 - D^2/4)) = 1335998331/1336001000 \approx 0.99999800225$, also below $1$.
- **Reach.** $t_{415} = 415/1001$ and $t_{415}^2 + 2t_{415} - 1 = 1054/1002001 > 0$; the
  last bin’s floor $414.5/1001 \approx 0.414086$ is below
  $\sqrt 2 - 1 \approx 0.414214$, so every node has an assigned orientation and none is
  skipped. The last tangent is below $1/2$.
- **Domains.** At each of the 416 nodes, $L - \rho(a_r) > L/2$, with $a_r$ at half-step
  $1/2002$.
- **The records.** The certificate has 416 records, the axis `AXIS_CERTIFICATE_REPLAYED`
  at $\gamma = 1$ and 415 `ANGLE_RESULT_REPLAYED`; its `net` block equals the manifest’s
  and the recomputed facts.
  The least oblique bound is $1.000000000165181$ at index 161, the oblique node total
  37,874,941, the axis integer minimum $1.0174496711115353 = 17479652251/2^{34}$ over
  725,904 cells.

So $B(1 + D) < 1$ is the right condition, sufficient though not sharp, and it is
sufficient for the per-bin domain at half-step $1/2002$ because the domain lemma uses
only the bin $|u - t_r| \le D/2$ that the shrink uses.
The finer net is what lets a larger core fit: at $B = 999/1000$ the standard step fails,
$999/1000 \cdot (1 + 83/40000) > 1$.

## Lemma N0 and the sqverify-fast Change

**The proof.** N0 assumes (a) $D > 0$ and $2 \le N_\theta \le 2^{16}$, (b)
$B(1 + D) < 1$, (c) the reach polynomial, (d) $t_{\max} \le 1/2$ and (e) the tangent
form, and claims that the theorem, lemma D’s per-bin domain and lemma F3 hold on the
declared net. Each step was checked:

- N1 and N2 use only the spacing $D$ and the reach; the fold is at $\pi/4$, so nothing
  depends on the net’s end beyond (c).
- N3 is step 3 above, with the extent formula and the inequality
  $(1 + 2z)(1 + z^2) - (1 + 2z - z^2) = 2z^2 + 2z^3 \ge 0$ both correct.
  The parenthetical claim about the sharp condition needs $D/2 \le \sqrt 2 - 1$, which
  (a), (c) and (d) give: $D = t_{\max}/(N_\theta - 1) \le 1/2$.
- The per-bin domain is step 4 above; `domain_upper` reads the admitted step, and the
  test checks four indices against an independent formula.
- F3: by (a) and (c), $D = t_{\max}/(N_\theta - 1) > \tan(\pi/8)/(2^{16} - 1) >
  2^{-18}$, since $\tan(\pi/8) > 1/4$; F3’s caps rest on $s_1 = 2D/(1 + D^2) > D$, so
  every bound it derives holds.
  At $D = 1/1001$, $s_1 \approx 2.0 \times 10^{-3}$, half the standard net’s, and the
  line coefficients double, far inside F3’s $2^{19}$.

The proof is complete and correct.
Condition (e) is not needed for soundness, given (b); it is checked anyway, as for the
standard net. One numerical statement in the section is wrong (DN-4).

**Admission.** `admit` reads `proof_net` before the format is known, checks (a) to (d)
on whatever net results, refuses a `proof_net` in a format T or L file, refuses metadata
that changes a format M net, and checks (e) for every per-bin domain, which is every
format M file. No declaration tried here passes a premise it breaks:

- a net that does not cover $[0, \pi/4]$ (`last` 414) is refused by (c), and one that
  covers it at too coarse a step for the core (step $1/999$) by (b);
- metadata that changes the step or the count is refused, metadata that restates it is
  admitted, including $2/2002$ for $1/1001$;
- a `proof_net` in format T or L is refused, not ignored;
- `last` as a string, a fraction, $415.0$, $4.15\mathrm{e}2$, $-1$, $2^{40}$, or $0$ is
  refused, the first five because only a JSON integer is read as one, $2^{40}$ by the
  `u32` bound, and $0$ by (a); a step of $10^{-6}$ with 414,215 nodes, which reaches
  past $\pi/4$, is refused by the $2^{16}$ cap;
- an unknown field is refused; a duplicate `last` inside `proof_net`, and a second
  `proof_net`, are refused by the document-wide duplicate-key check, which recurses into
  nested objects;
- `null`, a string and an array in place of the object are refused.

A decimal step, $0.000999000999000999$, is admitted as its exact literal value, a
different net from $1/1001$ that still meets (a) to (e), and is reported as such in the
summary’s `D`. That is sound: the verdict is on the net admission read, which the
summary names with `net_origin`, `D`, `angle_count` and $B(1 + D)$. One structural gap
is noted as DN-5.

**The tests and controls.** `tests/declared_net.rs` holds what `SOUNDNESS.md` says it
holds: the declared net replaces the standard one, the direction at index 415 and the
domain at four indices are the declared net’s exactly, $B = 999/1000$ without its
declaration is refused on the standard net, thirteen corrupted declarations are refused
with messages naming the premise they break, metadata may restate and never change a
declared net, format T and L are refused, and a $B$ between the two limits is refused at
$D = 1/1001$. The `declared-net` group holds the retained certificate to it: the
original verified with the summary’s premises checked, seven corruptions refused at
admission, and the masses scaled by $0.985$ refused with an exact witness at every
refused direction. It checks only that a corruption exits with status 2, not that the
refusal names the intended premise, and in the run here the corruption “metadata
changing the step” was refused by $B(1 + D) \ge 1$, not by the rule that metadata may
not change a declared net (DN-6).

**The 0.985 control and #366’s five directions.** #366 reports the masses scaled by
$0.985$ refused in five directions by the reporter’s copy; this repository’s control
refuses them in 326 of 416 (run here without `--quick`, 85 CPU-seconds).
The difference does not bear on any verdict here, but it is not a difference of taste
between checkers. Every refusal counted here carries an exact witness: a centre in the
node’s domain at the node’s angle where the scaled measure captures, in exact rationals,
less than one. Any sound checker run on the scaled measure at those directions must
refuse each of them.
So if the reporter’s copy ran all 416 directions and refused only five, it accepted
directions with exact counterexamples; more likely it stopped early or ran a subset.
The number was not checked here, and the reply on #366 may ask which.

**The census.** `sqverify_fast_census` now takes each certificate’s direction count from
the verifier’s own summary for its verdict, and from the file’s `proof_net` only for
labels. That is consistent: the census can never call a run complete on a net other than
the one admission read.

## The Source’s Runs on the Declared Net

The bundle receipt (`receipts/n18-L470/bundle.json`, made by `audit_wand125_declared_net
bundle` on the pinned tarball) establishes, for the run the source shipped: the
tarball’s 1,266 listed files match their digests with none unlisted; its candidate,
certificate and manifest are the retained files; its ten `code/` files are the
`mixed_n50_L740` copies and its `proof/verify.cpp` is `89b674a6…`; at every one of the
415 oblique nodes, the record names this candidate’s digest, net index $r$, tangent
$r/1001$, bin floor $\max(0, r/1001 - 1/2002)$, the per-bin domain and half-width $E$
for that floor, threshold one, status `ANGLE_VERIFIED` with an empty frontier and no
witness, and a lower bound at least one; its input’s first six lines enclose $L$, $B$,
$E$, $c_r$, $s_r$ and $1$ exactly and list 1,088 rectangle images; and the axis record
is complete at threshold one.
Since the candidate digest covers `proof_net`, the records are bound to the declared net
by digest as well as by value.
So the source ran its checker on the declared net, at every node of it.

What the receipt does not establish: that each input’s 1,088 rectangle lines enclose the
expanded candidate. `mixed-fetch` checks that at $n = 66$ and at every earlier mixed
import; the declared-net tool checks the count only (DN-2). And none of it decides
coverage.

**What a complete replay must show for the exit at `n = 18`.** The bundle’s own driver,
run from the pinned tarball as its README says, with assertions on and one BLAS thread,
ending in `ALL_ANGLES_VERIFIED_AND_REPLAYED` over all 416 nodes; every oblique record
regenerated and equal to the shipped one in status, nodes, leaves, lower bound and empty
frontier; the axis record equal; the receipts committed.
Expected: 37,874,941 oblique nodes, least $1.000000000165181$ at 161, axis
$1.0174496711115353$ over 725,904 cells, about 2.7 CPU-hours by the source’s 9,819
oblique seconds. The comparison must be made by a tool that checks the run happened and
compares the rewritten certificate field by field, which `compare` does not yet do
(DN-1).

**What it must show at `n = 66`.** T-069’s standard: `mixed-replay n66-L843` over ranges
by `--via git`, every direction passing only because the shipped function returned the
certificate’s own record, and `mixed-merge` printing `FULL_REPLAY_MATCHES_SHIPPED` with
no missing or refused direction.
Expected: 120,072,600 oblique nodes, least $1.0000000007136982$ at 157, axis
$1.0051859714394813$ over 21,622,500 cells, about 15.5 CPU-hours planned (16.2 by the
source’s 58,309 oblique seconds).

## Where the Records Stand

Checked in exact rationals against the retained files:

- **Masses and sides**: as stated in T-096, T-097, both report entries, both case
  records, the coverage entry and the bibliography note.
- **Margins**: $47/10 - 939/200 = 1/200$ over T-045’s value, and $843/100 - 421/50 =
  1/100$ over T-069’s, as stated.
  Before the import those were the reported and the verified lower bounds at their
  counts, as T-096 and T-097 say.
- **Least bounds and indices, node counts, cells and seconds**: as stated (9,819 and
  58,309 oblique seconds are the bundle receipts’ 9,818.8 and 58,309.2).
- **Green and Nagamochi at `n = 66`**: $843/100 > 2\sqrt 2 + 71/13 = 8.2899656\ldots$,
  since $843/100 - 71/13 = 3859/1300$ and $(3859/1300)^2 = 14891881/1690000 > 8$; and
  $843/100 > 1 + \sqrt{51}$, since $(743/100)^2 = 552049/10000 > 51$. The source’s
  “8.2900…” is Green’s value rounded up at the fourth place (DN-9).
- **Monotonicity**: neither carries.
  At $n = 19$ the record reports and verifies $1927/400 = 4.8175 > 4.7$; at $n = 67$ it
  reports $212/25$ and verifies $1691/200 = 8.455 > 8.43$, as both entries say.
- **The packet README**: 35 pinned files, 40,621,100 bytes; 9 retained, 536,631 bytes
  upstream; the root README changed by the two sections alone; the declared net’s
  identities as stated.
- **Credit and dating**: `attribution.published` is 2026-10-05, the UTC date of both
  commits. The credit line follows the root README’s Attribution section, which opens
  “The method is not ours.”
  and names Stromquist, Nagamochi, Burns and Massaccesi, and this repository; its Status
  section says “Parts of this work were produced with AI assistance under human
  direction.”, which both entries, both case records and the bibliography note repeat.

Three statements about work done here are not supported by the files (DN-2, DN-3), and
the verifier registry’s summary of the source’s checker still says 201 directions
(DN-7). The packet README’s and report entry’s statement that the $n = 18$ bundle
records its run on macOS arm64 was not checked here, the tarball not being fetched.

## The First-Party Tools

**`audit_wand125_declared_net`.** `audit` checks what its docstring lists, from the
retained bytes, and its receipt reproduces.
Its “one candidate digest throughout” is accurate: it compares the candidate’s own
stated digest with the manifest’s and the certificate’s and does not recompute it,
unlike `mixed-audit`’s `_semantic_digest`. This review recomputed it, and it is right.
`bundle` checks what its docstring lists, which is less than `mixed-fetch` checks at
$n = 66$ (DN-2). `compare` does not say “matches” only when it should (DN-1).

**The `check_standing` change.** A superseded entry at `C0` or `C1` is now judged in the
reported lane alone.
That is principled under `epistemics.md`. The frontier README admits a value to the
verified lane only after a complete replay here and a review, so an entry no replay has
confirmed can hold the reported lane and never the verified one, and whether it is
beaten is a question in that lane.
Requiring such an entry to be strictly worse than the verified bound would hold a report
to a lane it cannot enter; T-046 at $n = 18$, equal to the verified $939/200$ that
T-045’s replay holds and beaten in the reported lane by T-096, is the case.
Keying on the confirmation rung rather than on verification is the right axis, since `V`
may be earned by a source’s own replay and only `C` says what was replayed here.
An entry at `C2` or above is still held to both lanes, and the test shows the same entry
at `C3` refused.

## What a sqverify-fast Pass Supports

This review ran `sqverify-fast` at this commit on `mixed_n18_L470` at all 416
directions: every direction `verified`, summary status `VERIFIED` on
`net_origin: proof_net` with $D = 1/1001$, 416 directions and
$B(1 + D) = 500499/500500$; 37,882,813 nodes, least oblique certified bound
$1.0000000000740676$ at index 408, axis $1.0174533215531854$; 168 CPU-seconds, 4 minutes
26 seconds of wall time on a host at load 10. Its least bound falls at a different index
from the source’s ($1.000000000165181$ at 161) and its node total is within 0.03 per
cent of the source’s; both checkers report a lower bound of their own search, so neither
figure is expected to match the other.
At $n = 66$ it ran directions 0 and 157, the least recorded: both verified, at least
bounds $1.0051945942$ and $1.0000000626$, 15 CPU-seconds for 157.

A complete `sqverify-fast` pass is a decision of coverage by code that shares none of
the source’s, written under a clean-room record that names what each lane read.
It is the strongest evidence of correctness the repository can produce for these
certificates. Under the present rules it supports no rung and moves no verified lower
bound, for either certificate:

- `sqverify-fast` is not in `verifiers.yaml`, and no evidence entry cites it; slice 4 of
  the verifier plan (`think-3ok2`, open) is to add them, after two adversarial reviews.
  Of the two reviews of 3 October, the soundness review calls itself evidence for the
  coordinator rather than a verdict of record, and neither read lemma N0, which is
  newer.
- The plan’s non-goals exclude any certificate not already replayed here from acceptance
  (T-096 and T-097 are stretch targets) and say no rung moves by its entries alone.
- `result-import.md` defines stage 4’s replay as the source’s own verification run in
  full, a sample being a diagnostic, and the frontier README moves the verified lane for
  a result by others only after that replay and a review.

So, for T-096, a complete `sqverify-fast` pass is a reviewer’s check, recorded here, and
the exit waits for the bundle’s own driver.
For T-097, a complete `sqverify-fast` pass with a sampled replay of the bundle leaves it
at `V0/C1`, with the verified lower bound at $421/50$; the sampled directions are a
diagnostic. Only a complete replay with the source’s checker gives `V3/C3`.

The literal `C3` predicate of `epistemics.md` would be met by a registered
`sqverify-fast` entry of confirming origin with a certificate, a replay command and a
passing status; what gates it is stage 4’s definition and the plan.
Letting a complete independent pass stand for the source’s replay, for a reported
certificate, would be a change to those two documents, for the owner to make, and is not
made by this review.
Once slice 4 records them, `sqverify-fast` entries would show beside each rung as
*independently re-implemented*, the attribute the plan intends.

## What the Authors’ Code Shows

This section depends on the source’s retained `code/` (byte-identical copies under
`wand125-point-and-mixed-2026-09-28/…/mixed_n50_L740/code/`). Nothing outside it depends
on that code.

- `mixed_net_audit.candidate_net` reads `proof_net` when present (fields exactly `step`
  and `last`), and the standard net otherwise; so the declared net was already supported
  by the code reviewed on 28 September, and `mixed_n18_L470` is the first certificate to
  exercise that branch.
  `net_certificate` checks $0 < B < 1$, $D > 0$, an integer `last` $\ge 1$,
  $0 < t_{\max} < 1$, the reach, that the last node has an assigned orientation, and
  $B(1 + D) < 1$. It checks no node cap and no tangent form, and allows $t_{\max}$ up to
  $1$ where `sqverify-fast` requires $1/2$; on this certificate both sets of premises
  hold.
- `centre_domains` computes the per-bin domain at $a_r = \max(0, t_r - D/2)$ for the
  declared step, skipping nodes with no assigned orientation; none is skipped here.
- `mixed_density_check.expand` includes `proof_net` in the digest when present, so every
  per-angle record’s digest binds it to the declared net.
- `mixed_rotated_verify.export` writes $E$, $c_r$ and $s_r$ for the declared step;
  `mixed_rotated_verify.cpp` reads them, with $\gamma$, from the input and contains no
  constant of the standard net.
- The driver asserts the manifest’s `net` block, every record’s domain and digest; each
  oblique replay regenerates its input from the candidate, requires it byte-identical to
  the shipped one, runs the checker with the shipped node count and requires the same
  status, nodes, leaves, lower bound and frontier.
  So a complete replay closes DN-2’s gap by itself, which is why DN-2 is not blocking;
  the first-party check is still the independent binding the earlier imports have.
- The driver rewrites `proof/certificate.json` with its results in completion order and
  writes `proof/replay-progress.json` and a compiled `proof/replay-verify`; it writes no
  `bundle.json` or `files-sha256.json`. So DN-1’s false `MISMATCH` is certain on any
  real run, and `compare`’s `fresh_status`, read from `bundle.json`, reports the shipped
  file’s field.

## Findings

One blocking finding, DN-1, in this repository’s tool.
None in either certificate or in `sqverify-fast`.

### DN-1 — Blocking for the `n = 18` exit: `compare` can match without a replay and mismatch a correct one

`audit_wand125_declared_net compare` treats a record as regenerated when the fresh
file’s modification time is later than the shipped one’s, and compares every other
shipped file byte for byte except `bundle.json`, `files-sha256.json` and
`proof/replay-progress.json`. Probed here on synthetic trees: a copy of a 416-node
bundle made without keeping file times, on which nothing ran, gives
`FULL_REPLAY_MATCHES_SHIPPED` with 416 records matching; a complete, correct replay
whose rewritten `proof/certificate.json` lists the same records in another order gives
`MISMATCH` (“proof/certificate.json: changed by the replay”). The retained certificate’s
records are in completion order (0 to 5, 7, 6, …), as `compare_driver_run`’s docstring
says of the $n = 50$ run.
It also never checks that the fresh certificate says `ALL_ANGLES_VERIFIED_AND_REPLAYED`.
The fix is `compare_driver_run`’s shape: require the replay’s progress record at 416 of
416 and its binary, compare the rewritten certificate with the retained one field by
field (results as a mapping), require every regenerated record’s status, nodes and lower
bound to equal the shipped run’s, and keep the time test, if at all, as a secondary
check; with tests for both probes above.
Until then no receipt from `compare` moves the verified lower bound at $n = 18$, and
T-096’s `next_rung` should name the fixed tool.

### DN-2 — Non-blocking, first-party tool and record: the `n = 18` inputs are bound to the net, not to the candidate

`bundle` checks each oblique input’s six header lines and its rectangle count, not its
1,088 rectangle lines, which `check_inputs` encloses against the expanded candidate at
$n = 66$ and at every earlier mixed import; and `audit` reads the candidate digest
rather than recomputing it.
E-n018-wand125-mixed-470-report says the audit “recomputes … the candidate digest from
the retained bytes”, which it does not, though the value is right (recomputed here).
Generalize `check_inputs` to a declared step and run it on the $n =
18$ bundle before the exit, and recompute the digest in `audit` (or correct the
sentence).

### DN-3 — Non-blocking, record: the `sqverify-fast` passes the claims state have no receipt

T-096 says `sqverify-fast` “decided all 416 directions here” and T-097 “all 201
directions here”, but at `569b54ebf` no receipt of either run is in the tree: the mixed
census has no entry for the packet, and the `declared-net` group runs the original at
four directions. By `result-import.md`, a run that was not committed did not happen.
Commit the census receipts for the packet, or drop the sentences until they are.
This review’s own run of all 416 directions is above; it is a reviewer’s check, not a
receipt.

### DN-4 — Note, `SOUNDNESS.md`: the tangent form at `n = 18` is about 0.9999980022

The Declared Nets section gives $B(1 + D/(1 - D^2/4)) \approx 0.999998001$; it is
$1335998331/1336001000 \approx 0.99999800225$, as the audit receipt’s `tangent_form`
says. The premise holds either way.
Also, step N2 of the theorem still speaks of $t_{200}$, the standard net’s last node;
“the last node” would cover both.

### DN-5 — Note, `sqverify-fast`: format M ignores unknown top-level fields

A format M file carrying both a `proof_net` and a format L `net` block is admitted on
the `proof_net` and the `net` block ignored.
This is not a soundness matter, since the verdict is on the net admission reports, but
the principle the change states, that a declaration this reader would not use is refused
and not ignored, holds only for `proof_net`. Refusing a `net` key in format M would
extend it.

### DN-6 — Note, tests: five refusals rest on untested paths, and the controls check exit codes only

All refused correctly in this review’s probes, but not held by a test: `last` $0$, a
reaching net above $2^{16}$ directions, `last` above the `u32` range, `last` in exponent
form, and duplicate keys inside `proof_net`. The `declared-net` group accepts any exit
status 2 for a corruption; matching the refusal message to the intended premise, as the
Rust test does, would keep a control from passing on an unrelated refusal: in the run
here, “metadata changing the step” to $83/40000$ was refused by $B(1 + D) \ge 1$,
because the metadata step replaces the declared one before the net premises are checked,
and never reached the metadata rule it is named for.
Either refusal is correct; the control does not hold the rule its name says.

### DN-7 — Note, verifier registry: the source’s checker is described on 201 directions

`V-wand125-mixed-rotated-verify-cpp`’s summary says it decides “each of the 201 net
directions”; with T-096 it decides the 415 oblique directions of a declared net.
“Each net direction of the certificate’s net” would be true of both.

### DN-8 — Note, for the reply on #366: five refused directions against 326

As argued under Lemma N0, every direction refused here carries an exact witness, so the
five of #366 can only be a partial run or a different count.
Worth one question to the reporter; nothing here depends on it.

### DN-9 — Note, in the source: rounded decimals

`mixed_n18_L470`’s README gives the least oblique bound as “1.0000000002” for
$1.000000000165181$, and the $n = 66$ README Green’s value as “8.2900…” for
$8.2899656\ldots$, each rounded up.
The records cite exact values; OF-3’s kind, no reply needed.

### DN-10 — Note: `INDEPENDENCE.md` records lane B’s reads, and nothing here contradicts it

The change’s files and the lane’s record name no `code/` file, and nothing in
`declared_net`, the net checks of `admit` or lemma N0 follows the source’s code rather
than the mathematics: the premises differ in the ways listed in
[What the Authors’ Code Shows](#what-the-authors-code-shows), which is what separately
written checks look like.
A record cannot prove what was not read, as TI-5 of the 3 October review says.

## Significance

`S3` confirmed for both, as each would stand if its replay passes.
T-096 raises the bound at $n = 18$ by $0.005$, to within $0.123$ of Hämäläinen’s
$7/2 + \sqrt 7/2$; the finer net is a parameter choice within Burns and Massaccesi’s
framework that the source’s driver already supported, not a new technique.
T-097 is a further size from the generator and checker of T-069 and later, $0.01$ over
its own predecessor.
Substantive case results; neither resolves a disputed value.

## Disposition

Both certificates are accepted by this review with no defect in either.
DN-1 is open and blocks the $n = 18$ exit until fixed; DN-2 and DN-3 should be closed
with it.

- **T-096**: `C1` once this document is recorded as `external_review` on
  E-n018-wand125-mixed-470-report and listed in `reviews`. `V3/C3`, and the verified
  lower bound $47/10$ at $n = 18$, when the bundle driver’s complete replay returns the
  certificate’s record at all 416 nodes, compared by a fixed tool (DN-1).
- **T-097**: `C1` likewise, on E-n066-wand125-mixed-843-report.
  `V3/C3`, and $843/100$ at $n = 66$, when `mixed-replay` and `mixed-merge` return the
  record at all 201 directions.
  A complete `sqverify-fast` pass with a sampled replay leaves it at `V0/C1` and
  $421/50$.

## For the Records Lane

`reviews:` entry, the same for T-096 and T-097 except `covers`, which lists both:

```yaml
- path: docs/project/reviews/review-2026-10-05-wand125-declared-net-n18-n66.md
  kind: adversarial
  reviewer: AI agent, the review lane of the 2026-10-05 evening intake's lane B (T-096, T-097 and the sqverify-fast declared net), separately prompted, sharing no context with the lane that retained and registered the results, changed the verifier and is replaying the certificates, after registration and before any complete replay; model claude-opus-5-5 (tbd-strong tier)
  reviewer_kind: ai
  relation: project
  date: '2026-10-05'
  scope: >-
    wand125's mixed_n18_L470 (s(18) >= 47/10, on the net its candidate declares, core 999/1000 and 416 half-angle tangents of step 1/1001) and mixed_n66_L843 (s(66) >= 843/100, on the standard net), pinned at 43050edc, and sqverify-fast's declared-net change of f007d7afd: the argument from certificate to bound with the declared net re-derived in exact arithmetic, lemma N0 and the admission of a declared net, the tests and controls, the source's runs on the declared net, every number in the records, the first-party audit tools and the check_standing change, and what a sqverify-fast pass supports; before any complete replay.
  verdict: accepted
  covers: [T-096, T-097]
```

`external_review` on E-n018-wand125-mixed-470-report:

```yaml
external_review:
  state: informally-verified
  date: '2026-10-05'
  reviewed_by: >-
    AI agent, the review lane of the 2026-10-05 evening intake's lane B, separately prompted, model claude-opus-5-5 (tbd-strong tier)
    (docs/project/reviews/review-2026-10-05-wand125-declared-net-n18-n66.md)
  note: >-
    No defect in the certificate. The declared net's premises hold in exact arithmetic
    (B (1 + 1/1001) = 500499/500500 < 1, t_415^2 + 2 t_415 - 1 = 1054/1002001 > 0, the
    per-bin domain at half-step 1/2002 at all 416 nodes), as do the mass, rows and digest,
    and lemma N0 is correct. The 415 oblique coverage statements and the axis tables are
    the source's until the replay here passes; the comparison tool for it must be fixed
    first (finding DN-1, blocking for the exit).
```

`external_review` on E-n066-wand125-mixed-843-report:

```yaml
external_review:
  state: informally-verified
  date: '2026-10-05'
  reviewed_by: >-
    AI agent, the review lane of the 2026-10-05 evening intake's lane B, separately prompted, model claude-opus-5-5 (tbd-strong tier)
    (docs/project/reviews/review-2026-10-05-wand125-declared-net-n18-n66.md)
  note: >-
    No defect. The certificate is of T-069's kind on the standard net, checked by the
    same checker byte for byte; every exact premise readable from the retained files
    holds, the candidate digest is reproduced here, and the side exceeds T-069's 421/50 by
    1/100 and Green's and Nagamochi's values in exact arithmetic. The 200 oblique
    coverage statements and the axis tables are the source's until the complete replay
    here passes.
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
