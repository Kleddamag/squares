# Proof Review: squarepacker’s `s(12) ≥ 31360/7901`, Evan Daniel’s Certificate Rescaled by `7902/7901`

Reviewed 2026-10-02 from the retained packets, by an AI agent of this project working as
lane AA of the 2 October import effort, for stages 1 to 4 of the
[result import](../../../packing/campaign/result-import.md) of
[jlevy/squares#309](https://github.com/jlevy/squares/issues/309) (bead `think-gh2o`).
The same lane ran the replays, so this is not the separately prompted review lane the
runbook asks for (F1). It is evidence for the coordinator, not a verdict of record: it
registers nothing and moves no bound.

**Whose result this is.** The result is squarepacker’s (Ryu Sungjoon), after Evan
Daniel, as squarepacker states it.
The rescaling of the certificate and its verification on the finer angle net are
squarepacker’s. The certificate being rescaled, `s12_lower_3.9686.txt` (`T-049`), and
the verifier that decides it are Daniel’s. This repository’s part is the import, the
replays, the controls and this review, and it is recorded as evidence performed here,
not as authorship.

**In one line:** the certificate is exactly Daniel’s with every coordinate and the side
multiplied by `7902/7901`, decided here in exact arithmetic; the angle-net argument
proves the covering statement from a pass at any one net, so a refusal at `N = 6000` and
`12000` and a pass at `N = 24000` are consistent; Daniel’s verifier, squarepacker’s own
checker and this repository’s native interval branch and bound all accept it at
`N = 24000`, and all three refuse two mutated certificates.
No blocking defect. The draft significance is `S2`: a true and fully replayed step of
`0.000502`, which spends the angle-net slack of an existing certificate.

## 1. What Was Reviewed

| Field | Value |
| --- | --- |
| Request | [jlevy/squares#309](https://github.com/jlevy/squares/issues/309), opened 2026-10-02T16:57:30Z by squarepacker |
| Source | [squarepacker/s12-lower-bound](https://github.com/squarepacker/s12-lower-bound) at `8c53049025b94bb589ed25a90203f0a34c2945e4` (2026-10-02T16:45:25Z), retained whole in [`squarepacker-s12-lower-bound-2026-10-02`](../../../packing/resources/web/squarepacker-s12-lower-bound-2026-10-02/README.md) |
| Archive | Zenodo [10.5281/zenodo.23106582](https://doi.org/10.5281/zenodo.23106582), version `v1.0` of tag `v1.0` = `7acf812c`; the archive’s files equal the pin’s except `README.md`, to which the pin adds the DOI line |
| Certificate | `s12_lower_3.969118.txt`, SHA-256 `6ad9b0e8257166687f4e861b97f024f4993d7b2125897173b2f5e9f6e2167578`, as the issue states; first committed 2026-10-02T15:47:37Z (`be1871bd`) and unchanged since |
| Daniel’s certificate | `s12_lower_3.9686.txt`, SHA-256 `75f1cc89…`, retained in the [26 September packet](../../../packing/resources/web/evand-square-packing-2026-09-26/README.md); the same Git blob `4c3f0bb3` at `167d842c` and at `7d6f46d9`, the revision the source names |
| Daniel’s verifier | `s12/verify/src/main.rs`, Git blob `0e8035a3`, with `Cargo.toml` and `Cargo.lock`, identical at `167d842c` (retained) and `7d6f46d9`; built here by cargo 1.97.0, binary SHA-256 `9e79ec32…` |
| The reporter’s checker | `tools/indep_check.cpp`, SHA-256 `21527e8d…`, built here by g++ 13.3.0 `-O2` |
| First-party checker | [`devtools.verify_evand_angle_net_native`](../../../packing/devtools/verify_evand_angle_net_native.py), case `s12-rescaled`, over [`sqpack.fractional.parent_core`](../../../packing/src/sqpack/fractional/parent_core.py) and `parent_core_interval` |

Read in full: the issue; the source’s `README.md`, `LICENSE`, `SHA256SUMS`,
`tools/indep_check.cpp`, `tools/spot_check.py` and every log; Daniel’s
`verify/src/main.rs` around `read_cert`, `bin_geometry`, `check_symmetry`,
`min_cover_k`’s set-up and `main`; the native reader and `validate_parent_core`; `T-049`
with its three evidence entries, and
[the review of 27 September](review-2026-09-27-evand-s32-s12.md) §6.1 and §8, which
accepted the method for Daniel’s certificate.

## 2. Verdict

**The bound holds as stated.** Every closed unit square in `[0, 31360/7901]²` captures
weight at least `1` from the rescaled certificate, decided by three checkers at
`N = 24000`, and the total weight `119738036/10⁷` is below `12`; the classical reduction
then gives `s(12) ≥ 31360/7901`, and the native theorem gives the strict
`s(12) > 31360/7901`. The advance over `T-049` is exactly
`31360/7901 − 15680/3951 = 15680/31216851`, about `0.000502`, and the gap to the grid’s
`4` goes from `124/3951 ≈ 0.03138` to `244/7901 ≈ 0.03088`.

**The account the source gives is accurate.** The certificate is what the source says it
is, to the integer. The net behaviour it reports is reproduced here: `indep_check`’s
output at `N = 6000`, `12000` and `24000` and on the `31360/7900` control equals the
source’s logs line for line, and `verify` refuses at the coarse nets with the source’s
values. Its credit to Daniel and its limitation, “recovering discretisation slack, not
from a new mathematical idea”, are right.

**Findings:** one process gap (F1), three notes about the checkers (F2 to F4) and one
about the source’s word “independent” (F5). **None is blocking.**

## 3. The Certificate, Decided Exactly

[`devtools.audit_s12_rescaled_certificate`](../../../packing/devtools/audit_s12_rescaled_certificate.py)
reads the two retained files and decides, in rational arithmetic, 16 checks, all passing
([receipt](../../../packing/resources/web/squarepacker-s12-lower-bound-2026-10-02/receipts/preflight.json)):

- both digests are the reviewed ones;
- the new container is `31360/7901` and Daniel’s `15680/3951`, a ratio of exactly
  `7902/7901`;
- both files hold 1,736 points over the weight denominator `10⁷`, and point `i` of the
  new file is point `i` of Daniel’s with both coordinates multiplied by `7902/7901` and
  the same weight; as integers, `X′ = 2X` and `Y′ = 2Y` over `D′ = 7901`, since
  `(X/3951)(7902/7901) = 2X/7901`;
- every weight is positive (the least is `1178/10⁷`), every point lies in the closed
  container, the weighted point set is invariant under the container’s symmetry group,
  and the total is `119738036/10⁷ = 11.9738036 < 12`, Daniel’s total, a counting gap of
  `65491/2500000`;
- the source’s own control `controls/scaled_further_31360_7900.txt` is the same integers
  over `7900`, the new file scaled again by `7901/7900`.

## 4. The Argument From Certificate to Bound

**The reduction.** Suppose twelve unit squares with disjoint interiors fit in a square
of side `s′ < s = 31360/7901`. Scaling the picture by `s/s′ > 1` gives twelve squares of
side `s/s′ > 1` with disjoint interiors in `[0, s]²`; the concentric closed unit square
of each lies in its open interior, so the twelve closed unit squares are pairwise
disjoint. If each captures weight at least `1`, no point is counted twice and
`12 ≤ 11.9738036`, a contradiction.
This is the argument the 27 September review accepted for `T-049` (§6.1, by §3.2), and
the source states it the same way.
It needs the covering statement for closed unit squares, which is what all three
checkers decide.

**What a net decides.** Fix `N` and bins `[θ_k, θ_{k+1}]`, `θ_k = 2 arctan(k/N)`, so
that `cos θ_k` and `sin θ_k` are rational.
Let `Q` be a closed unit square at angle `θ = θ_k + φ`, `0 ≤ φ ≤ δ = θ_{k+1} − θ_k`, and
`S` the concentric square of side `σ` at angle `θ_k`. In `Q`’s frame `S` is turned by
`−φ`, and its axis-parallel extent is `(σ/2)(cos φ + sin φ)` each way, so `S ⊆ Q`
exactly when `σ ≤ 1/(cos φ + sin φ)`. Since `cos φ + sin φ` increases on `[0, 45°]` and
`δ` is far below `45°`, the side `σ_k = 1/(cos δ + sin δ)` works for every `φ` of the
bin. A unit square at angle `θ` lies in `[0, s]²` exactly when its centre is in
`[w/2, s − w/2]²`, `w = cos θ + sin θ`; `w` is concave on `[0, 90°]`, so the union of
these boxes over the bin is the box for the smaller of `w(θ_k)` and `w(θ_{k+1})`. Hence,
**if for every bin every square of side `σ_k` at angle `θ_k` with centre in that box
captures weight at least `1`, then so does every closed unit square in the container**,
since it contains such a square and weights are nonnegative.
Daniel’s verifier and the native checker cover `[0, 45°]` and use the container’s
symmetry, which the point set has exactly (checked by each); the diagonal reflection
takes a square at angle `θ` to one at `90° − θ`, and a square at `90°` is the square at
`0°`. The reporter’s checker covers `[0, 90°]` and uses no symmetry.

**Why a refusal at `N = 12000` and a pass at `N = 24000` are consistent.** The test at
each net is a sufficient condition, complete in itself: a pass at any one `N` proves the
covering statement, whatever coarser nets did.
A refusal proves nothing about unit squares.
It says that some square of side `σ_k` at a net angle, at an admissible centre, misses
weight; that square is smaller than every unit square containing it, so missing weight
is not a counterexample.
The shrink costs about `δ ≈ 2/N` of the side: `σ_0 = (N² + 1)/(N² + 2N − 1)` is about
`1 − 3.3·10⁻⁴` at `N = 6000`, `1 − 1.7·10⁻⁴` at `12000` and `1 − 8.3·10⁻⁵` at `24000`.
The refusals at the coarse nets are shrunk cores that capture less: least `9849809/10⁷`
at `N = 6000` (bin `975`, about `18.5°`) and `9867834/10⁷` at `12000` (bin `361`, about
`3.5°`), at centres the source’s diagnostics place against the left wall, `x ≈ w/2`. A
genuine counterexample, a unit square capturing less than `1`, would contain a core of
every net at an admissible centre, and every net would refuse; the finer nets accept.
The direction is the expected one: halving the net’s step keeps the coarse angles, and
at each of them enlarges the core and narrows the centre box, so it can only remove
refusals there, while the angles it adds are tested with the larger cores.

**What the rescaling asks of the certificate.** In Daniel’s coordinates the new claim
says that every closed square of side `7901/7902` in `[0, 15680/3951]²` captures weight
at least `1`. That is strictly stronger than Daniel’s claim, which is about unit
squares, so it is not a corollary of `T-049` and needed its own computation: the squares
are smaller by `1/7902 ≈ 1.27·10⁻⁴` and can reach closer to the walls.
Daniel’s run at `N = 6000` certified cores about `3.3·10⁻⁴` smaller than unit squares at
his angles, which is room the coarse net spends on the shrink.
In Daniel’s coordinates the rescaled check at `N = 24000` asks for cores only about
`2.1·10⁻⁴` smaller than unit squares, at four times as many angles and over the larger
centre boxes, and the certificate meets it.
It passes with the least captured weight Daniel’s own run recorded, `10000056/10⁷`, at
the axis-parallel bin `k = 0`. One further step, side `31360/7900`, is refused at
`N = 24000` with least `9849809/10⁷` at `θ ≈ 18.43°`, the value and nearly the angle of
the `N = 6000` refusal: the certificate has little more room than the step it was given.

## 5. The Checkers and What They Share

| Checker | Author | Here | Angles | What it trusts | Decides |
| --- | --- | --- | --- | --- | --- |
| `verify` | Evan Daniel | External code, the producer’s verifier, run here | `[0, 45°]` with an exact D4 check | Exact `i128` arithmetic, unchecked in release mode; `σ_k` and `w_min` rounded down to `10⁻⁶` (both conservative) | The exact least captured weight over every arrangement cell of each bin, by a sliding-window sweep |
| `indep_check.cpp` | squarepacker | External code, the producer’s own checker, run here | `[0, 90°]`, no symmetry | `__int128` with every operation overflow-checked; points floored to a `10⁻¹⁵` grid, half-sides floored and lowered one unit, the centre box rounded outward | The least captured weight over every open cell meeting a superset of the centre domain, by a segment tree |
| `verify_evand_angle_net_native` | This repository | First party, independent implementation | `[0, 45°]` with exact premise checks | Python integers and rationals; directed-rounding boxes | That every row reaches the threshold `1` at every parent centre, by interval branch and bound |

**Read here.** `indep_check.cpp` was read line by line against the statement in §4:
counted capture implies true capture (a floored position is within one unit of the true
one and the half-side is at least one unit short), the domain and its `u₁`-range over
each closed slab are rounded outward, the active set of each open slab is exactly the
boxes spanning it, the segment-tree ranges are the open intervals each box covers, and
the least value over open cells meeting the domain equals the least over the closed
domain, because the captured weight takes finitely many values, the set where it is
least is relatively open (each capture is a closed condition), and every relatively open
set of a convex domain with interior meets an open cell.
It is sound as written.
Daniel’s `verify` is the code the 27 September review read; nothing in it depends on `N`
except the size of its integers (F4). The native route’s transfer theorem and interval
engine were reviewed for Kleddamag’s `n = 11` certificate
([review of 22 September](review-2026-09-22-native-n11-parent-core.md)) and applied to
Daniel’s certificate for `T-049`; the reader change here adds the net as a case field
and leaves the `s12` case as it was (§6).

**What they share.** All three rest on the certificate and on the counting theorem.
All three use the same net, `θ_k = 2 arctan(k/N)`, and the same shrink lemma at the left
end of each bin, by design: the native rows are Daniel’s bins, and the native core side
is his `σ_k` rounded down to `10⁻⁶`. What differs is the coverage decision: two
arrangement sweeps written separately by Daniel and by squarepacker, and an interval
branch and bound written here that shares no code with either.
The two sweeps are one method in two implementations; the native decision is a second
method.

## 6. Replays and Controls

On a four-core Linux container shared with other lanes, at load averages of 13 to 30
throughout, so every wall time is contended.
A container restart between 18:07 and 19:22 UTC killed the first full runs of `verify`
and of the native route; `verify` was rerun whole, and the native route resumed from its
journal of the 1,810 rows it had certified on clean commit `119d1bab`, the same tool
code, both reniced to 10. Receipts are in the packet’s
[`receipts/`](../../../packing/resources/web/squarepacker-s12-lower-bound-2026-10-02/receipts/),
each by `devtools.replay_receipt`.

| Checker | Input | Result | CPU |
| --- | --- | --- | ---: |
| `verify`, `N = 24000`, two threads | The certificate | VERIFIED; least `10000056/10⁷` at `k = 0`, over bins `0..9941`; every printed line equals the source’s `logs/daniel_verify_N24000.log` | 982 s |
| `indep_check`, `N = 24000` | The certificate | VERIFIED; least `10000056/10⁷` at `k = 0`; every printed line equals the source’s `logs/indep_check_N24000.log` | 67.7 s |
| `indep_check`, `N = 6000` and `12000` | The certificate | NOT VERIFIED; least `9849809/10⁷` at `k = 976` and `9867834/10⁷` at `k = 362`, both outputs equal to the source’s logs | 16.2 s, 30.9 s |
| `verify`, `N = 6000` and `12000`, bins `970..980` and `355..370` | The certificate | FAIL from bin `975` and from `361`, at the same values | 0.9 s, 1.0 s |
| Native, `N = 24000`, two workers | The certificate | `PASS_COMPLETE`: all 9,942 rows certified at the threshold, 89,403,350 boxes, no stalled box, no exhausted budget, no refutation; 1,810 rows on clean commit `119d1bab`, the rest resumed on `44cf3444` with the tool unchanged | 2,856 s resumed; the first run’s not recorded |

The controls, written by `devtools.audit_s12_rescaled_certificate --write-controls` and
pinned by digest, are two mutations that any correct checker must refuse:

- **`scaled-7901-7900`**, side `31360/7900` (SHA-256 `04d7105c…`, byte for byte the
  source’s own control), one more step of the rescaling; and
- **`weights-minus-57`**, every weight lowered by `57/10⁷` (`61b48f23…`): the pose that
  attains `10000056/10⁷` captures at least one point, so it now captures at most
  `9999999/10⁷`.

| Checker | `scaled-7901-7900` | `weights-minus-57` |
| --- | --- | --- |
| `verify`, bins near the reported failure | FAIL at bins `3893..3899` of `3880..3910`, least `9849809/10⁷` | FAIL at bins `0..6` of `0..15`, least `9988604/10⁷` |
| `indep_check`, every bin | NOT VERIFIED, least `9849809/10⁷` at `k = 3894`, as the source’s log | NOT VERIFIED, least `9985548/10⁷` at `k = 4154` |
| Native, two rows each | rows `3893` and `3894` refuted, admissible witnesses of charge `1973359/2000000` and `9849809/10⁷` | rows `0` and `4154` refuted, each with a witness of charge `39987/40000` |

The `verify` controls sweep a window of bins (`VERIFY_BINS`), which cannot print
VERIFIED; a refused bin in it is refused in the full sweep too, since each bin is an
independent computation and one refused bin makes the full sweep refuse.
This is the precedent of the `s(60)` controls, which ran one root box each.
`tests/test_s12_rescaled_certificate.py` holds every receipt above, regenerates both
controls and checks their digests, and checks that the native reader still builds
Daniel’s 2,486 rows at `N = 6000`.

## 7. Findings

### F1. One lane did the replay and the review (process, non-blocking)

The runbook’s stage 4 has two lanes that share no context.
Here one lane did both, so this document is the replay lane’s own read of the
mathematics.
What it adds to the 27 September review is small and checkable (§3, §4, §5),
and the method is the one that review accepted; a second, separately prompted read would
restore the runbook’s separation.

### F2. `verify` exits 0 when it refuses (note)

Daniel’s `verify` prints `NOT VERIFIED` and exits `0`; its exit status does not carry
the verdict, and a script that tests it would accept a refusal.
Every receipt here is judged by its verdict line, as the T-049 replay was.
`indep_check` exits `1` on a refusal.

### F3. The two sweeps name adjacent bins for the same refusal (note)

At `N = 6000` the least `9849809/10⁷` is first reached at bin `975` in `verify` and
`976` in `indep_check`; at `12000` the least `9867834/10⁷` at `361` and `362`; on the
`31360/7900` control at `24000`, `3893` and `3894`. All six were reproduced here (the
`verify` windows in `receipts/nets/` and `receipts/controls/` show the bins before the
first refusal accepted).
The values agree.
`verify` rounds `σ_k` and `w_min` down to `10⁻⁶` and `indep_check` uses
them exactly, so `verify`’s cores are a little smaller and its centre boxes a little
larger, and it can refuse one bin earlier; that is the conservative direction.
The source’s “agree to the last integer on every net” is true of the values.

### F4. The overflow-checked build of `verify` was not replayed here (note)

`verify` runs `i128` arithmetic without overflow checks in release mode, and at
`N = 24000` its sweep coordinates reach about `10²⁵`, below `i128`’s `1.7·10³⁸` but with
less room than at `N = 6000`. The source rebuilt it with `-C overflow-checks=on` and got
identical output, which was not repeated here.
It is not load-bearing: `indep_check` checks every operation and the native route uses
unbounded integers, and both accept.

### F5. “Independent checker” means independent of Daniel’s code (note)

The source calls `indep_check.cpp` independent: written from the statement, not from
`verify`. As far as one can read, that is true, and it is a second implementation of the
angle-net sweep. It is the producer’s own checker, so the record holds it as
`same-implementation` beside `verify`, and the method-distinct confirmation is the
native route.

## 8. Significance, Novelty and Credit

**Draft significance `S2`.** The result is true and fully replayed, and it raises the
verified lower bound of a case the record follows.
But the step is `0.000502`, it moves the gap to `4` by 1.6 per cent, and it is obtained
by rescaling an existing certificate until a finer angle net stops accepting it, which
spends that certificate’s slack and adds no technique; the source says so itself.
Daniel’s own measurements suggest more room for the method than this step: his README
gives `COVER(3.975) ≈ 11.96` for pure point covers, so a reweighted cover may reach
further. `T-061`, Wang and Li’s rescaling of Kleddamag’s `s(11)` certificate, is the
precedent: a true, replayed step scored by what it changes, `S2`.

**Novelty** `previously-published`: the result is squarepacker’s, published on GitHub on
2 October 2026 and archived on Zenodo the same day.

**Credit and AI assistance.** The source’s README credits Evan Daniel with the
certificate, the verifier, the reduction and its Lean formalisation, Burns and
Massaccesi with the weighted-certificate method, and Göbel and Stromquist with the
unavoidable-set method, and names Ryu Sungjoon (squarepacker) as author.
It says that the rescaling, the verification runs and `tools/indep_check.cpp` were
prepared with the help of an AI assistant from Anthropic.
`LICENSE` reproduces Daniel’s MIT licence for the derived material and releases the
source’s own files under the same terms, copyright Ryu Sungjoon.

**Rungs.** `V3/C3`: an exact-algebraic certificate with passing replays here, two of the
producer’s checkers and a first-party interval-certified decision, with controls.
Not `V4` or `C4`: no two adversarial reviews by distinct reviewers and no human
oversight record are retained, the same position as `T-049`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
