# Review: Evan Daniel’s Kernel-Checked `s(13) = 4`, Built Here

**Where the evidence lives.** Paths under `scratchpad/` below name the session’s scratch
area, which is not retained.
The build and axiom receipts that are retained are in the 2026-09-28 evand packet’s
[`receipts/lean/`](../../../packing/resources/web/evand-square-packing-2026-09-28/receipts/lean/).

Reviewed 2026-09-30 from the build lane’s overlay at `scratchpad/lean/overlay/s12/lean`
and its logs under `scratchpad/lean/logs/`, read only, by the independent adversarial
reviewer of this session.
Nothing in the repository was modified, no git state was changed, and no Lean build was
started; every check below is a file read, a hash, a diff, or a small script in
`scratchpad/review-lean/`. The network actions were two `gh api` reads of the upstream
tree, refused by the session’s GitHub access policy, and then a blob-less
`git clone --filter=blob:none --no-checkout` of `github.com/evand/square-packing` into
`scratchpad/review-lean/upstream-blobless/`, used only for `git ls-tree` at the pinned
commit.

**In one line:** the Lean constant `SquarePacking.s13_eq_4 : minSide 13 = 4`, checked by
Lean 4.33.1 with the standard three axioms, states exactly this record’s $s(13) = 4$
(closed unit squares, independent real rotations, pairwise disjoint open interiors,
inside the closed $[0, s]^2$, $s(n)$ the least such side, attained at $4$ by
`packs_grid 4 13`); nothing in the source bypasses the kernel; the regenerated data
enters only as kernel input, so its correctness is not assumed; and the result should be
recorded as new evidence on `T-006`, taking it to `V5`, with one thing to retain before
the replay recipe is honest.

## 1. What Was Reviewed

| Field | Value |
| --- | --- |
| Source | `github.com/evand/square-packing`, directory `s12/lean/`, at `6aa82ba457e9eaeaaa3af0833600f27f91a2fce3` (tree `c9d23e3a…`) |
| Theorem | `SquarePacking.s13_eq_4 : SquarePacking.minSide 13 = 4`, `Sqpack/S13Lower.lean` (blob `2012970e…`), with `s13_ge_4 : (4 : ℝ) ≤ minSide 13` |
| Definitions | `coord`, `sq`, `sqInt` (`Sqpack/Basic.lean`, blob `cbfe567f…`); `box` (`Sqpack/Chord.lean`, `913bd7df…`); `Packs`, `minSide`, `packs_grid` (`Sqpack/S32.lean`, `065a2c43…`) |
| Verifier | `Sqpack/ZMTree.lean` (`fb64e304…`), `Sqpack/BoxTree.lean` (`0499d1f0…`): `ZMTree.sound`, `BoxTree.le_minSide` |
| Certificate | `certificates/rung2/s13_closed_cover_4.txt`, sha256 `ea303acea08cc17a13cecc24d3714c2df409f91eba048cd5546050ed064b53ed`, 3,621 points, total weight $12955972155 / 10^9 = 12.955972155 < 13$ |
| Generator | `lean/scripts/gen_zmtree.py` (`06f22b4d…`); trees pickled at `scratchpad/lean/work/s13_trees.pkl`; emitted as 4 parts (`work/S13_4parts/`) and as the 16 parts that were built (`Sqpack/S13/`) |
| Toolchain | `lean-toolchain` = `leanprover/lean4:v4.33.1`; `lean --version` = 4.33.1, commit `819816b2`; `lakefile.toml` requires mathlib `v4.33.1`; `lake-manifest.json` pins mathlib `0df444a360eaa60ab8c11dca51a86af692955474` |
| Lane logs | `logs/build_s13_*.log` (19 targets), `logs/s13_table.txt`, `logs/axioms_s13.log`, `logs/axioms_default.log`, `logs/statements.log`, `logs/gen_S13.log`, `logs/emit_S13_16.log`; probes `scratchpad/lean/probe/AxiomsS13.lean`, `Statements.lean` |
| Register context | `T-006` (`V3/C1`), `T-049`, `T-051`, `T-052` in `packing/frontier/results.yaml`; `E-n013-evand-casefree-cover-report` in `evidence.yaml`; `packing/frontier/n-013.md`; the 2026-09-26 and 2026-09-28 packets under `packing/resources/web/`; `epistemics.md`; `devtools/check_results.py`; `sqpack/assurance.py` |

Read in full: `Basic.lean`, `S13Lower.lean`, the `Packs`/`minSide`/`packs_grid`/
`not_packs_of_cover` section of `S32.lean`, `box` in `Chord.lean`, `BoxTree.sound`,
`Cov`, and `le_minSide` in `BoxTree.lean`, `ZMTree.sound` and the encoding comment in
`ZMTree.lean`, the headers and `cov_root` of `S13/Cov.lean`, `S13/Pts.lean`, and
`S13/Part0.lean`, `emit()` and `main()` of `gen_zmtree.py`, `Axioms.lean`, the rung-2
section of `LADDER.md`, both packet READMEs’ Lean sections, `notes/s13-casefree.md` §1,
and the lane’s logs and scripts.
The upstream tree was compared blob for blob; the Lean sources were not built again.

## 2. Verdict

**No blocking finding against the theorem.** The statement is faithful, the axioms are
the standard three, and the build the lane ran is a genuine kernel check of every chunk.

**One blocking finding against the register entry as a replayable record (B1):**
`Sqpack/S32Data.lean` is in the import closure of `s13_eq_4` (through `S32.lean`, which
defines `Packs` and `minSide`) and is retained by neither packet, so the replay recipe
cannot be run from the record until it is retained.
It is 439 KB, blob `b8ea5d9487edc11cb7c801af7f4c1c4724f79be0`, sha256
`d26cd11073aef59ebb411586cb3eed18cb37ce250eb770156b16ed43903f22cf`, and byte-identical
to upstream.

**Should-fix:** the confirmation rung must be derived by the literal rule, which today
gives `C2` for a `proof-assistant-checked` entry on its own (S1); the packet’s complete
`zmx2 --d4` replay of the same cover is on disk but unregistered, and registering it is
what makes `T-006` `C3` (S2); the evidence entry must record the replay as it was
actually done, sixteen parts and single-threaded, not the source’s four (S3); and the
credit line must say this is not the first kernel-checked $s(13) = 4$ anywhere, only the
first on this record (S4).

**Nits:** `s13_eq_4` is the infimum form and attainment is a separate constant (N1); the
trusted base should be written down once (N2); the lane’s file-level “same lines” claim
is true per chunk but not per file (N3); build-cost figures should be reported with the
thread setting (N4).

**Recommended register change:** new evidence on `T-006`, not a new result;
`method: proof-assistant-checked`, `origin: replayed-here`, `performed_by: repository`;
`T-006` to `V5`, and to `C3` once the `zmx2` replay is registered beside it.
The $s(12)$ bounds and the two conditional theorems change no field (§6.4).

## 3. Statement Faithfulness

The rung `V5` says a proof assistant checked a formalization, not that the formal
statement matches the prose claim (`epistemics.md`, Verification), so this is the
section that decides whether `minSide 13 = 4` is $s(13) = 4$. Everything the statement
mentions is in three files, and Lean printed the definitions itself
(`logs/statements.log`, `#print` from the built environment); the printed forms agree
with the sources.

### 3.1 The definitions, one by one

`coord c θ p = ((p.1 − c.1) cos θ + (p.2 − c.2) sin θ, −(p.1 − c.1) sin θ + (p.2 − c.2) cos θ)`
is the rotation of $p - c$ by $-\theta$, so `sq c θ L = {p | |x'| ≤ L/2 ∧ |y'| ≤ L/2}`
is the closed square of side $L$ centred at $c$ and rotated by $\theta$, and `sqInt`
with strict inequalities is its open interior.
With $L = 1$ the half-width is $1/2$ in real division, so `sq c θ 1` has side exactly
$1$, not $2$ and not $1/2$. `box t = {p | 0 ≤ p.1 ∧ p.1 ≤ t ∧ 0 ≤ p.2 ∧ p.2 ≤ t}` is the
closed $[0, t]^2$.

`Packs n s` is
`∃ (ctr : Fin n → ℝ × ℝ) (ang : Fin n → ℝ), (∀ i, sq (ctr i) (ang i) 1 ⊆ box s) ∧ ∀ i j, i ≠ j → Disjoint (sqInt (ctr i) (ang i) 1) (sqInt (ctr j) (ang j) 1)`.
That is $n$ closed unit squares, each with its own real angle, each inside the closed
container, with pairwise disjoint open interiors; Mathlib’s `Disjoint` on sets is empty
intersection. Boundary contact between squares, and between a square and the container’s
edge, is allowed, which is the record’s convention (`E-n032-…-source-run`,
`proof.scope`). Nothing restricts the angles: the $\theta \in [0, \pi/4]$ and
centre-in-the-fundamental-region restrictions live inside the proof (`d4_reduction`,
`exists_u_of_theta'` in `BoxTree.lean`) and do not reach the statement.

`minSide n = sInf {s | Packs n s}` over $\mathbb{R}$, with $13 : \mathbb{N}$ and
$4 : \mathbb{R}$.

### 3.2 The infimum, junk values, and attainment

`Real.sInf` returns $0$ on the empty set and on any set not bounded below
(`Real.sInf_empty`, `Real.sInf_of_not_bddBelow`). So a junk value cannot produce
`minSide 13 = 4`: if the packing set were empty or unbounded below the left side would
be $0$. The proof of `s13_eq_4` is explicit about both: nonemptiness is
`packs_grid 4 13` (`Packs 13 4`, the $4 \times 4$ grid), and boundedness below is
derived by contradiction from `s13_ge_4` using `Real.sInf_of_not_bddBelow`; then
`le_antisymm (csInf_le hb hp) h1`.

The lower half is not merely an inequality about an infimum.
`BoxTree.le_minSide` proves `Mq/D ≤ minSide n` through `le_csInf` over the nonempty set,
with every member $s$ shown to satisfy $m \le s$ by `not_packs_of_cover`, whose
statement is `∀ s < m, ¬ Packs n s`. So the kernel-checked content is the strong form:
no packing of 13 unit squares exists at any side below $4$. With `packs_grid 4 13` the
value is attained, and $s(13) = 4$ in the record’s least-side sense follows; see N1 for
why the register should cite both constants.

### 3.3 The instance

`s13_ge_4` instantiates `le_minSide` at $D = 1000$, $S = 4096$, `Mq = 4000`,
$R = 2^{32}$, `Um = 2³¹`, $W = 10^9$, $n = 13$, $k = 4$: the container side `Mq/D = 4`,
the angle range $u \in [0, 1/2]$ with `29·R ≤ 70·Um` (so $\tan(\pi/8) < 29/70 \le 1/2$),
$13 \le 4\cdot4$, and the total `pts.wsum = 12955972155 < 13 · 10⁹`, which is
$2591194431/200000000 \cdot 10^9$, the certificate’s stated total.
The root box of `cov_root` is $[0, 8192000]^2 \times [0, 2^{31}]$ at scale
$Q = D\cdot S$, and `Mq·S − Mq·S/2 = 8192000`, as `le_minSide` requires.

## 4. Nothing Smuggled

- **Axioms.** `logs/axioms_s13.log` is genuine `#print axioms` output for the constants
  the prose names:
  `'SquarePacking.s13_eq_4' depends on axioms: [propext, Classical.choice, Quot.sound]`,
  the same for `s13_ge_4`, `ZMTree.sound`, and `BoxTree.le_minSide`; the probe
  `AxiomsS13.lean` imports `Sqpack.S13Lower` and nothing else, exit $0$. The
  default-target log has 97 constants on the standard three and 4 on `propext` alone,
  none on anything else.
  `#print axioms` walks the stored proof terms, so this covers the 209 chunk theorems
  and everything below them.
- **Source grep** over every project `.lean`, `.toml`, and `.json` outside `.lake/`: no
  `sorry`, `admit`, `axiom`, `native_decide`, `ofReduceBool`, `implemented_by`,
  `@[extern`, `unsafe`, `opaque`, `partial`, `csimp`, or `debug.skipKernelTC`; the three
  hits for `native_decide` are docstrings saying it is not used.
  Every `set_option` in project sources is `maxRecDepth 100000`, `maxHeartbeats 0`
  (elaboration budgets), or `linter.style.longLine false`; none touches the kernel.
  `lakefile.toml`’s `leanOptions` are pretty-printing, `relaxedAutoImplicit = false`,
  the Mathlib linter set, and `maxSynthPendingDepth`.
- **Chunk proofs.** Each `okI` is
  `ZMTree.sound … ptsL … ptsL_nodup (ZMTree.dec 1048576 128 cI dI).1 … (List.Sublist.refl _) (by decide +kernel)`:
  the tree is decoded from two numerals, `ZMTree.check` is evaluated by the kernel, and
  soundness is the once-proved `ZMTree.sound`. `decide +kernel` is kernel reduction, not
  compiled evaluation.
- **Closure and gluing.** The import closure of `Sqpack.S13Lower` is 28 project modules
  plus `Mathlib`: `Basic`, `Chord`, `Cover`, `D4`, `S32`, `S32Data`, `ZeroMargin`,
  `BoxTree`, `ZMTree`, `S13Lower`, and the 18 generated `S13.*`. `S13/Cov.lean` imports
  `Part0` through `Part15`, and `cov_rootL` is one term over `ok0 … ok208` (209 distinct
  `okI` across the 16 files, $13 \times 15 + 14$), so `S13Lower` cannot have been built
  without every chunk.
  `S13Lower` is opt-in (not in `Sqpack.lean`), which is why the lane built it by name.
- **Pins and provenance.** All 43 entries of
  `git ls-tree -r 6aa82ba4 -- s12/lean s12/certificates/rung2/s13_closed_cover_4.txt`
  (every non-generated Lean file, `Axioms.lean`, `LADDER.md`, the lakefile, manifest,
  toolchain, all five scripts, and the certificate) have `git hash-object` equal to the
  overlay’s file. The only overlay files absent upstream are the generated `S13/` (18),
  `S11/` (50), and `S32P/` (7). `S32Data.lean`’s 2026-09-30 mtime is a re-copy, not an
  edit. The certificate’s sha256 equals the `Pts.lean` header, the 09-26 packet’s
  `retained-files.sha256` line 10, and the gunzipped retained `.gz`.

## 5. The Regenerated Data

The data files `Sqpack/S13/*` are not in the source repository and are not retained by
either packet; the lane generated them with the retained generator from the retained
cover. Their correctness is not assumed anywhere.
`Pts.lean` states `pts_nodup`, `pts_d4`, `pts_wsum`, and `pts_toList` by
`decide +kernel`; each `Part` file proves its chunks by `decide +kernel`; `Cov.lean`
glues them by `Cov.splitX`/`splitY` terms; `S13Lower.lean` feeds `cov_root`,
`pts_nodup`, `pts_d4`, and `pts_wsum` to `le_minSide`. A wrong generator produces a file
that fails to build, never a false theorem.
The generator itself trusts nothing either: `zeromargin.py` is its read-only oracle for
which leaf and which witnesses, and the emitted tree is what the kernel decides.

**Census.** `logs/gen_S13.log` reports 10,024 boxes, max depth 13, $E$ 1,738, $Z$ 4,079
(`ADM` 1,416, one chain 1,133, two chains 1,530), `C` 1,590, 2,617 splits, $F$ 374,
1,325,532 claimed entries, 203,367 chain points, 16,717 pivots, 1,803,938 digits, 209
chunks; every figure equals the source’s `LADDER.md` rung-2 paragraph.
The search ran with `--nproc 1` and `--save`; the source says a fresh run reproduces the
files byte for byte, which cannot be checked against source bytes that were never
published, but the census match is the check available.

**Sixteen parts against four.** The 16-part emission was `--load` from the same pickle
with `--parts 16`. In `emit()`, `--parts` only drives a greedy cost-balanced assignment
of chunks to files and the census line of `Cov.lean`’s docstring; the digit streams, the
`cI`/`dI` numerals, the `okI` statements, and the `cov_rootL` term depend only on the
trees and the certificate.
Checked: `Pts.lean` is byte-identical (`cmp`); every one of the 209 chunks has identical
`/-- Chunk I -/` docstring, `def cI`, `def dI`, and `theorem okI` text in both emissions
(`chunkcmp2.py`; the only differences were my splitter absorbing a file-boundary
`open BoxTree ZMTree` line); `Cov.lean` differs only in the twelve extra `import` lines
and `4 files` → `16 files`. The re-emission is harmless; it changes which file the
kernel checks a chunk in, not what it checks.

**Build.** Nineteen targets, `Pts`, `Part0`–`Part15`, `Cov`, `S13Lower`, each `rc 0`
with `Build completed successfully`, oleans present under `.lake/build/lib/lean/`; 104
min wall and 66 min CPU in total, single-threaded on a loaded four-core host, max RSS
9.54 GB of which about 6.6 GB is the Mathlib import, peak anonymous memory 4.1 GB
(`Part13`). The source reports 538 s wall and 1,995 CPU-s with four parts in parallel at
13.2 GB RSS; the CPU here is twice that, which the thread setting and host load account
for, and the memory is lower because the parts are smaller.
The probe that printed the axioms ran in 12 s.

## 6. Relation to the Register

### 6.1 New evidence on `T-006`, not a new result

`T-006`’s claim is `s(13) = 4 (Bentz 2010, Theorem 9)`; a classification attaches to the
exact statement in `claim`, and this is the same statement.
The record has already taken this position for the same cover: `n-013.md` says “the
theorem is Bentz’s; the source claims only the proof”, and the 2026-09-27 review calls
the case-free proof “a second proof of a `V3` value”.
The source’s own `CREDITS.md` says the same (“Our case-free $s(13) = 4$ was
kernel-checked later”). A new result row would also break `T-006`’s history and the case
file’s citation. So: one new evidence entry, cited by `T-006`; `T-006`’s `verification`
derived to `V5`; its `composition` and `next_rung` rewritten.

### 6.2 The evidence entry

A sketch, with the fields the schema requires (`frontier-evidence.schema.yaml`,
`assurance.py`: a machine-formal method needs `certificate` and `replay`):

- `id: E-n013-evand-casefree-cover-lean-kernel`; `claim: exact-value` (or `lower-bound`
  with `E-basic-grid-upper` for the other half, as `T-051` does; the theorem itself is
  the equality, so `exact-value` is the honest reading); `scope: {n_values: [13]}`.
- `assurance: verified`; `method: proof-assistant-checked`; `performed_by: repository`;
  `origin: replayed-here`; `novelty: previously-published`;
  `source_key: '[evand square-packing 2026-09-28]'` (the commit that introduced
  `S13Lower.lean`, `6e1223cf`, is between the two intakes; the 09-28 key covers it).
- `relationship_to_generator`: the kernel verifier `ZMTree.check` is a separate
  implementation from the certificate’s search and from `zeromargin.py`, proved sound
  once; `independent-implementation` is defensible, with the common mode, one author and
  one agent wrote generator, oracle, and verifier, stated in `limitations`. The
  coordinator should choose; the soundness of the theorem does not turn on it.
- `certificate: resources/web/evand-square-packing-2026-09-26/square-packing/s12/certificates/rung2/s13_closed_cover_4.txt.gz`
  (sha256 of the gunzipped file `ea303ace…`, which the `Pts.lean` header names).
- `replay`: elan with `leanprover/lean4:v4.33.1`; overlay the two packets’ `s12/` so
  that `lean/` holds the 09-26 files (`Basic`, `Chord`, `Cover`, `D4`, `S32`,
  `ZeroMargin`, `lakefile.toml`, `lake-manifest.json`, `lean-toolchain`) and the 09-28
  files (`BoxTree`, `ZMTree`, `S13Lower`, `Sqpack.lean`, `Axioms.lean`,
  `scripts/gen_zmtree.py`), plus `Sqpack/S32Data.lean` once retained (B1);
  `lake exe cache get` for Mathlib `0df444a3`; from `s12/`,
  `python3 lean/scripts/gen_zmtree.py certificates/rung2/s13_closed_cover_4.txt --n 13 --name S13 --outdir lean/Sqpack/S13 --nproc 1 --save TREES.pkl`
  (37 min wall here), then the same with `--load TREES.pkl --parts 16` (32 s); then
  `lake build Sqpack.S13.Pts Sqpack.S13.Part0 … Part15 Sqpack.S13.Cov Sqpack.S13Lower`
  one at a time with `LEAN_NUM_THREADS=1` (66 CPU-min, ≤ 9.6 GB RSS), or as four parts
  with more memory; then `lake env lean AxiomsS13.lean`, which must print
  `SquarePacking.s13_eq_4 : SquarePacking.minSide 13 = 4` and
  `depends on axioms: [propext, Classical.choice, Quot.sound]`. The generated files need
  not be retained: they are deterministic from retained inputs, and the kernel is what
  checks them.
- `replay_status: passed`; `source_reviewed: '2026-09-30'`; `limitations`: what is
  trusted (N2), the common mode, that the generated data was regenerated rather than
  compared to source bytes, and that the probe ran against the built oleans.
- Receipts to retain beside the entry: `axioms_s13.log`, `statements.log`,
  `s13_table.txt`, `gen_S13.log`, `emit_S13_16.log`, and the nineteen build logs, with
  the probe source.

### 6.3 The rungs

- **`V5`** follows from `method: proof-assistant-checked` (`derive_verification`), and
  it is deserved: the prose claim and the formal statement match (§3), and the check is
  hypothesis-free (`#check` shows no premises).
- **`C`:** `derive_confirmation` counts a machine-proof-shaped entry only when its
  `method` is `exact-algebraic` or `interval-certified` (`MACHINE_METHODS` in
  `check_results.py`, matching the `C3` wording in `epistemics.md`). A
  `proof-assistant-checked` entry with a passing replay therefore derives **`C2`** on
  its own. The 09-28 packet’s `receipts/s13_zmx2_d4.log` is a complete `zmx2 --d4` run of
  this cover, 1,600 roots, 47,162 boxes, 0 uncertified, `VERIFIED-D4`, 11 s, recorded in
  `replays.json` and `audit.json` but cited by no evidence entry.
  Registered as an `interval-certified`, `replayed-here` entry on `T-006`, it makes
  `T-006` **`C3`**; a complete `zeromargin.py` sweep (exact-algebraic, 16,872 boxes; the
  source’s 1 h 42 min on 8 processes) would make it `C4`. Whether a kernel check should
  itself count as machine-proof-shaped is a policy question for the owner, not for this
  review; it should be a bead, and the entry should carry the literal rung until it is
  decided.
- `T-006` would then need a `controls` path (a `C3` result must name one); a contract
  test that the retained `S13Lower.lean` statement text and the retained axioms receipt
  say what the entry says is the natural one.
- **Firsts.** This would be the first `proof-assistant-checked` entry and the first `V5`
  on this record (`grep` finds none today), and the first hypothesis-free kernel-checked
  exact value of $s(n)$ the record holds.
  It is not the first kernel-checked $s(13) = 4$ anywhere: chelokot’s Lean archive holds
  Bentz’s argument, kernel-checked on 2026-09-05, which the source credits and
  `n-013.md` already reports; that archive is not retained here.
  Credit: Evan Daniel (the `LICENSE` holder), building on Burns and Massaccesi, with an
  AI agent under human direction as `CREDITS.md` states; nothing peer reviewed.

### 6.4 What the other theorems change

- `s12_ge_35_9` ($3.888\ldots$) and `s12_ge_3920_997` ($3.9318\ldots$), kernel-checked
  on the standard axioms (`axioms_default.log`), are the source’s pilot rungs and are
  below `T-049`’s $15680/3951 = 3.96862\ldots$. They move no bound and earn no rung; a
  line in `n-012.md`’s ladder prose that two weaker bounds are now kernel-checked is the
  most they warrant.
- `s21_eq_five_of_checker : S21CheckerCover → minSide 21 = 5` and
  `s32_eq_six_of_checker : S32CheckerCover → minSide 32 = 6` are implications from
  checker-cover hypotheses; a compound claim takes its weakest load-bearing part, so
  `T-051` and `T-052` stay `V4`. The source reports a hypothesis-free `s32_eq_6`
  (`S32Lower.lean`, 96 parts, 13.8 CPU-hours); the lane built only a probe of its data
  (`S32P.Pts`, `Part0`, `Q1`), not the theorem, so `T-051` is unchanged until that build
  is replayed.

## 7. Findings

### B1. The replay recipe cannot run from the retained packets (blocking for the entry)

`S32.lean` imports `S32Data.lean` and defines `Packs` and `minSide`, so `S32Data.lean`
is in the closure of `s13_eq_4`. The 09-26 packet retains `S32.lean` but not
`S32Data.lean`; the 09-28 packet retains neither.
Retain `S32Data.lean` (439 KB, blob `b8ea5d94…`, sha256 `d26cd110…`, identical to
upstream `6aa82ba4`) with a `retained-files.sha256` line, in a small addendum packet or
beside the receipts, before recording `replay_status: passed`. No other closure file is
missing: the ten hand-written modules are split across the two packets exactly as §6.2
lists.

### S1. Derive the confirmation rung literally

`C2` from the Lean entry alone; `C3` with the `zmx2` entry (S2). Do not write `C3` on
the strength of “the kernel is a machine”.

### S2. Register the packet’s `zmx2 --d4` replay of this cover

It exists (`receipts/s13_zmx2_d4.log`, exit 0, 0 uncertified), it was made by the intake
lane, and it is what lifts `T-006` from `C2` to `C3`.
`E-n013-evand-casefree-cover-report` stays as the reported entry, or is superseded by
it.

### S3. Record the replay as performed

Sixteen parts, `--nproc 1`, `LEAN_NUM_THREADS=1`, one `lake build` per target, the
memory guard, and the walls in `s13_table.txt`; not the source’s four parts in parallel.
Say why (a four-core host busy with `zm_mixed.py`), and that four parts are the source’s
layout for a machine with 13 GB per process.

### S4. Say what is first and what is not

First `V5` and first `proof-assistant-checked` entry on this record; not the first
kernel-checked proof of the value (chelokot, 2026-09-05, Bentz’s argument).

### N1. Cite attainment beside the infimum

`minSide` is `sInf`; `s13_eq_4` plus `packs_grid 4 13 : Packs 13 4` is the least-side
statement.
`S32.lean` exports `s32_isLeast : IsLeast {s | Packs 32 s} 6`; `S13Lower.lean`
has no `IsLeast` constant.
The entry should name both constants, and can note that `Real.sInf`’s junk value $0$
rules out a vacuous $= 4$.

### N2. Write the trusted base down once

Lean 4.33.1’s kernel, including its built-in GMP arithmetic on `Nat` literals (which
`decide +kernel` leans on); the elan-installed toolchain binary; the Mathlib oleans for
`0df444a3` from the community cache, not rebuilt here; and the statement’s definitions.
Everything else, the generator, `zeromargin.py`, and the search, is outside the base.

### N3. “Same lines” is true per chunk, not per file

The greedy balancer puts chunk 33 first in the 16-part `Part0` and chunk 0 first in the
4-part one; a file diff shows 14 differing boundaries and a per-chunk comparison shows
none. `scratchpad/review-lean/chunkcmp2.py` is the check to keep.

### N4. Report CPU with the thread setting

66 CPU-min here against the source’s 33 is a thread and load effect; recorded without
`LEAN_NUM_THREADS=1` it reads as a discrepancy in what was checked.

## 8. Verified

| Claim | Evidence |
| --- | --- |
| `s13_eq_4 : minSide 13 = 4`, no premises, standard axioms | `logs/axioms_s13.log`: `#check` and `#print axioms` lines for `s13_ge_4`, `s13_eq_4`, `ZMTree.sound`, `BoxTree.le_minSide`; exit 0 |
| Definitions as printed equal the sources | `logs/statements.log` against `Basic.lean` (`coord`, `sq`, `sqInt`), `Chord.lean` (`box`), `S32.lean` (`Packs`, `minSide`) |
| Side 1, closed square, open interior, closed container, independent real angles, `Fin 13`, $4 : \mathbb{R}$ | §3.1, read from the definitions |
| No junk infimum; attainment | `Real.sInf_of_not_bddBelow` used in `s13_eq_4`; `packs_grid 4 13`; `le_csInf` and `not_packs_of_cover` in `le_minSide` |
| Instance arithmetic | $\frac{4000}{1000} = 4$; $29\cdot2^{32} \le 70\cdot2^{31}$; $13 \le 16$; $12955972155 < 13\cdot10^9$; root box $8192000 = 4000\cdot4096 - 4000\cdot\frac{4096}{2}$ |
| No kernel bypass in project sources | grep over `Sqpack/**`, `Sqpack.lean`, `Axioms.lean`, `lakefile.toml`, `lake-manifest.json`: no `sorry`, `admit`, `axiom`, `native_decide`, `ofReduceBool`, `implemented_by`, `extern`, `unsafe`, `opaque`, `partial`, `skipKernelTC`; `set_option`s are `maxRecDepth`, `maxHeartbeats`, `linter.style.longLine` only |
| Toolchain and Mathlib pins | `lean --version` 4.33.1 (`819816b2`); `lean-toolchain`, `lakefile.toml`, `lake-manifest.json` blob-identical to upstream |
| Overlay provenance | 43 of 43 upstream `s12/lean/**` and certificate entries at tree `c9d23e3a…` blob-identical to the overlay (`upstream_tree.txt`, `git hash-object`); overlay-only files are the generated `S13/`, `S11/`, `S32P/` |
| Certificate identity | sha256 `ea303ace…` in `Pts.lean` header, overlay file, retained `.gz` gunzipped, and `retained-files.sha256` of the 09-26 packet |
| Census equals the source’s | `gen_S13.log` vs `LADDER.md`: 10,024 boxes, depth 13, $E$ 1,738, $Z$ 4,079 (1,416 / 1,133 / 1,530), `C` 1,590, splits 2,617, $F$ 374, claimed 1,325,532, chain points 203,367, pivots 16,717, 209 chunks |
| 16-part emission equals the 4-part one | `Pts.lean` `cmp` identical; 209 chunks with identical `cI`, `dI`, `okI` text (`chunkcmp2.py`); `Cov.lean` differs in imports and the census line only; `emit()` shows `--parts` affects only file assignment |
| Every chunk in the closure | `Cov.lean` imports `Part0`–`Part15`; `cov_rootL` uses `ok0 … ok208`; 209 distinct `okI` ($13 \times 15 + 14$); `S13Lower` imports `Cov` |
| All targets built | 19 `build_s13_*.log` with `rc 0` and `Build completed successfully`; `.lake/build/lib/lean/Sqpack/S13Lower.olean` and `S13/` oleans present |
| Import closure | 28 project modules + `Mathlib`; `S32Data` in, `S21`, `S21Data`, `MixedMeasure`, `SegTree` out |
| Cost | `s13_table.txt`: 6,255 s wall, 3,978 s CPU, max RSS 9.54 GB, peak anon 4.1 GB; probe 12 s |
| `s12` bounds and conditional theorems on standard axioms | `logs/axioms_default.log` |
| No existing `V5` on the record | `grep proof-assistant-checked packing/frontier/results.yaml` → 0 |
| Unregistered `zmx2` replay of this cover | `evand-square-packing-2026-09-28/receipts/s13_zmx2_d4.log`, `replays.json` entry “s13 point cover, zmx2 --d4”; no `E-n013-…` cites it |

## Disposition

Accept the theorem as a faithful, hypothesis-free, kernel-checked $s(13) = 4$. Record it
as new evidence on `T-006` with `method: proof-assistant-checked`,
`origin: replayed-here`, `performed_by: repository`, and the recipe of §6.2; take
`T-006` to `V5`; retain `S32Data.lean` first (B1); register the `zmx2` replay beside it
for `C3` (S2); open a bead on whether kernel checks count as machine-proof-shaped for
the confirmation rung (S1); leave `T-049`, `T-051`, and `T-052` as they are (§6.4).

## Disposition

- **Recorded on T-006, not as a new result.** The review recommended recording this as
  evidence on T-006, `E-n013-evand-casefree-cover-lean-kernel`, with the `zmx2` replay
  of the same cover as `E-n013-evand-casefree-cover-zmx2-replay`. T-006 is `V5/C3` on
  these entries.
- **B1 is addressed by regenerating `S32Data.lean`.** The replay recipe regenerates it
  with the retained `gen_s32_data.py` from the retained $s(32)$ cover, before the build.
  The kernel checks every data fact, so the file needs no separate retention.
- **The should-fix items are applied in the evidence entry.** S1 (the rungs as derived),
  S3 (the replay as performed: 16 parts, single-threaded, on a loaded host) and S4 (what
  is and is not a first) are stated there.
  S2 is the `zmx2` entry.
- **The open question under S1 is a bead.** Whether a kernel check counts as
  machine-proof-shaped for the confirmation rung is filed for the owner.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
