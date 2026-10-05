# wand125’s Independent Valid7 Checker, Pinned 2026-10-02

This packet retains
[wand125/valid7-independent-check](https://github.com/wand125/valid7-independent-check),
a second exact checker for the finite statement **Valid7** on which T-064’s lower half
rests, and pins the records of its run by SHA-256. Valid7 says that every closed unit
square in $[0,7]^2$, at every position and angle, has mass at least 1 under Evan
Daniel’s $k = 7$ measure `L4_k02_box7.txt`; Daniel’s Lean reduction derives
$s(k^2 - 3) = k$ for every $k \ge 6$ from it.
Until this source, Valid7 was decided by one program, Daniel’s `qx2_zm.py`. The request
is [jlevy/squares#296](https://github.com/jlevy/squares/issues/296), also announced on
[#279](https://github.com/jlevy/squares/issues/279).

## Source and Pin

| Field | Value |
| --- | --- |
| Source | <https://github.com/wand125/valid7-independent-check> |
| Revision | [`38dd31b369991b0d96c917a4af0c7139b44a038d`](https://github.com/wand125/valid7-independent-check/tree/38dd31b369991b0d96c917a4af0c7139b44a038d), tree `5667d8de`, the repository’s only commit: “Independent checker for Valid7 (s(k^2 - 3) = k): code, cover, tests, design notes” |
| Committed | 2026-10-02T02:49:17Z; the commit’s author name is Hiroaki Hosono, and `LICENSE` reads “Copyright (c) 2026 wand125” |
| Retrieved | 2026-10-02T07:42Z, a full clone |
| Release | `records-v1`, assets downloaded 2026-10-02T07:42Z; GitHub reports them last modified 2026-10-02T02:49:36Z and 02:49:39Z |
| Licence | MIT. `NOTICE` says `cover/L4_k02_box7.txt` is Evan Daniel’s, MIT, taken unchanged from evand/square-packing `d9f79bc1` |
| Request | [jlevy/squares#296](https://github.com/jlevy/squares/issues/296), opened 2026-10-02T03:02Z by wand125 |

The repository has no credit or AI-assistance statement beyond `LICENSE`, `NOTICE` and
`READ_LOG.md`; none of them says how the code was written.

## What Is Retained

All 29 tracked files are in the manifest
([`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256)), 216,830
bytes. Twenty-eight are retained under
[`valid7-independent-check/`](valid7-independent-check/), byte-identical: the checker
(`src/`, eight modules), the record checker `src/check_record.py`, `verify.sh`, the
mutant tests (`tests/`), the V1 and V2 copies of the two files changed during the run
(`versions/`), and `README.md`, `DESIGN.md`, `READ_LOG.md`, `LICENSE`, `NOTICE`.

`cover/L4_k02_box7.txt` (18,238 bytes, SHA-256 `c0a67509…`) is **pinned by digest
only**, because the
[October 1 evand packet](../evand-square-packing-2026-10-01/README.md) retains the same
bytes at `source/s12/certificates/k2m3/L4_k02_box7.txt`, the cover T-064 cites.
The independent checker therefore decided the statement about the very cover the
register holds.

**The release records are pinned, not retained.** Their checksum file is retained as
[`release/records.sha256`](release/records.sha256), byte-identical to the release asset.

| Release asset | Bytes | SHA-256 | Decompressed |
| --- | ---: | --- | --- |
| `full.jsonl.gz` | 48,233,250 | `f553751df065f06708ea4226b1e18cb36a47f6fb1a47f0f0afd9ba0b628a4845` | 935,226,793 bytes, 123,201 lines, `bff065fe…` |
| `full_b.jsonl.gz` | 2,338,077 | `8eaf90f342429cae3245965a18e08452f73b9270b1f61aa9b129e08de45d6a4f` | 39,909,832 bytes, 33,601 lines, `e0fb45b6…` |
| `records.sha256` | 318 | retained | lists the four digests above |

At 50.6 MB compressed they are too large for the archive’s retained-data rule; the
digests make any copy checkable.
[`devtools.acquire_source`](../../../devtools/acquire_source.py) `--check` re-derives
the packet from its manifest; it does not cover the release.

## The Claim and the Independence Statement, as the Source Makes Them

The source’s README states the result: “Every pose was certified, with no symmetry
reduction: 156,800 root boxes covering centres $[0,7]^2$ × $u = \tan(\theta/2) \in
[-1/2, 1/2]$, 0 uncertified, 0 counterexamples; 9,640,060 leaves; about 626 core-hours.”
The $u$-range is $\theta \in [-53.13°, 53.13°]$, more than the square’s period of $90°$.

Its independence statement, in the README and `READ_LOG.md`:

- **Read:** the k2m3 bundle’s `README.md` (claim, proof paragraph, leaf-kind names,
  lemma names without proofs), `s21/FORMAT.md`, lines 1–60 of the bundle’s `verify.sh`,
  and the cover, all at evand/square-packing `d9f79bc1`; and the author’s own earlier
  `checker2/README.md` in wand125/squares-in-triangle.
- **Not read, by design:** `qx2_zm.py`, `zm_mixed.py`, `zeromargin.py`,
  `mixed_cover.py`, `QUADRANT_EXACT.md`, `ZM_MIXED.md`, `qx2_records.py`,
  `qx2_family_check.py`, the V3 run record and `lemmaZ.out`.
- **Contact:** another checker for covers of the same kind, for a different container
  with C4 symmetry, was being written at the same time, “possibly with reference to the
  upstream checker”; only specifications and usage were exchanged with it.
- **Different by design:** no D4 reduction; $\theta = 0$ by a closure argument (mass is
  upper semicontinuous in the pose) rather than an enumeration; its own exact
  primitives, `fractions.Fraction` and python-flint polynomials with its own
  Sturm-sequence root isolation, with no floating-point number in any decision.

What the two checkers share is the statement, the cover file and its format
specification.
Whether they share a lemma is a question for the review lane: the source’s
proofs are in `DESIGN.md` and the module docstrings, and were not reviewed here.

**History of the run** (`versions/VERSIONS.md`). Roots 1–31,825 of `full.jsonl` ran
under V1 and the rest under V2; V2 changed the hand-off rule between the two tiers and
the failure messages, and the source says no proof step.
A defect in the algebraic-number class found before V1 was fixed and every record made
before it discarded.
From 2026-10-01T20:47Z the remaining roots were split over two machines, `full.jsonl`
taking centres $x < 11/2$ and `full_b.jsonl` the rest.
Before publication only each record’s header line was edited, to make its file paths
relative.

## Replay Here, 2 October 2026

Stage 4 of the [result import](../../../campaign/result-import.md), within what this
container affords: the source’s own `verify.sh`, run as published, and an audit of what
it leaves out. The source’s run took about 626 core-hours and was **not** repeated.

**`verify.sh`** ([`receipts/valid7_verify.log`](receipts/valid7_verify.log)), written by
`devtools.replay_receipt`. The three release files were downloaded first and checked
against `records.sha256`, so the script’s `curl` and `gunzip` steps found them present
and fetched nothing.
The cover was the October 1 evand packet’s copy.
The interpreter was CPython 3.14.7 with python-flint 0.9.0, as `requirements.txt` pins.
The script:

1. checks the four SHA-256 digests (all `OK`);
2. runs `check_record.py` on both records with `--recheck 2000 --recheck-b 300`:
   `RECORD OK`, with `roots 156800 leaf kinds {'EMPTY': 79927, 'TIERB2': 2886043,
   'CORE': 6674090}`;
3. runs the three mutant covers of `tests/run_mutants.sh`, each the cover with one tight
   family lighter by a relative $10^{-4}$: Tier B returns `'ok': False` with an exact
   pose of mass below 1 for the wall mutant M1 on both sides of $u = 0$ and for the
   corner mutant M3, and the driver reports two counterexamples and `NOT VERIFIED` for
   the Lebesgue-square mutant M2.

Exit 0, 623 s of wall and 451 CPU-s on a 4-core container shared with other replays,
from 2026-10-02T07:44:47Z.

**The audit** by
[`devtools.audit_valid7_independent`](../../../devtools/audit_valid7_independent.py)
([`receipts/valid7_records_audit.json`](receipts/valid7_records_audit.json)) reads the
two records again and checks what `check_record.py` does not read, in 16 CPU-s, with its
log in [`receipts/valid7_records_audit.log`](receipts/valid7_records_audit.log):

- both files, compressed and decompressed, have the release’s digests;
- each header names, by SHA-256, the retained cover and the retained code: the
  `versions/V1/` copies of `run_all.py` and `tier_b2.py` for `full.jsonl`, whose header
  V1 wrote, and `src/` for `full_b.jsonl`, written by V2. The V2 roots that `full.jsonl`
  gained on resuming carry no header of their own; `versions/VERSIONS.md` alone names
  them;
- the 156,800 roots are exactly the grid `run_all.py` builds by default, each once, with
  `full.jsonl` holding the 123,200 at $x < 11/2$ and `full_b.jsonl` the other 33,600;
- no root records an uncertified box or a counterexample; and
- the totals are the README’s: 9,640,060 leaves, and 626.36 core-hours summed over the
  roots’ recorded CPU times.

[`packing/tests/test_audit_valid7_independent.py`](../../../tests/test_audit_valid7_independent.py)
holds both receipts, re-deriving the header linkage from the retained files.

### What the Replay Establishes, and What It Does Not

It establishes that the published records are the ones the release names; that their
roots are exactly the whole pose grid, each once, with no uncertified box and no
counterexample; that inside every root the leaves are an exact bisection partition; that
every `EMPTY` leaf has no admissible centre and no Tier B leaf contains $u = 0$; that
the code each record’s header names is the code retained here; and that 2,000 random
Tier A leaves and 300 random Tier B leaves re-certify under the retained V2 code.
Three covers each made lighter by $10^{-4}$ on a tight family are refused.

It does not re-certify the other 9.6 million leaves: each was accepted on the label the
run gave it. That is the 626 core-hours, the certification itself, and stands as the
source reports it. Nor does it review the method: the closure argument at $\theta = 0$,
the core bound of Tier A, the two lemmas of the fixed-angle solver, and the symbolic
execution of Tier B are proved in `DESIGN.md` and the module docstrings, and a review of
them is the other lane of stage 4.

## Method Review and Replay Plan, 2 October 2026

The [method review](../../../../docs/project/reviews/review-2026-10-02-valid7-independent-checker.md)
found every lemma sound, under premises this cover meets.
It found one implementation defect, D-1: `tier_b2.nonneg_open` accepts a polynomial
that vanishes at its one sample point. D-1 is non-blocking for `T-064`, and it is closed
by a replay staged with `--guard-d1`.
Its receipts here, written by
[`devtools.plan_valid7_replay`](../../../devtools/plan_valid7_replay.py) and
`devtools.replay_receipt`:

- [`receipts/valid7_calibration_x51-52_y25-26.log`](receipts/valid7_calibration_x51-52_y25-26.log)
  and
  [`receipts/valid7_calibration_x54-55_y63-64.log`](receipts/valid7_calibration_x54-55_y63-64.log):
  two centre cells of `run_all.py` V2, 64 roots, with every leaf list equal to the
  published one
  ([`valid7_calibration_compare.json`](receipts/valid7_calibration_compare.json)). They
  took 0.35 and 0.40 of the recorded time, which is wall time in the source’s 32-process
  pool. The run was launched under the `fork` start method; under the default
  `forkserver`, the receipt misses the workers’ CPU
  ([`valid7_calibration_forkserver_x51-52_y25-26.log`](receipts/valid7_calibration_forkserver_x51-52_y25-26.log)).
- [`receipts/valid7_leaf_recheck_x54-55_y63-64.log`](receipts/valid7_leaf_recheck_x54-55_y63-64.log):
  `check_record.py` re-certifying every leaf of one cell costs as much as the search.
- [`receipts/valid7_replay_plan.json`](receipts/valid7_replay_plan.json): the full
  replay at V2, 540.5 priced hours, about 216 CPU-hours here, in fourteen 4-core shards
  of about 4 hours each.

## Full Replay Here, 2 and 3 October 2026

The checker was replayed in full with D-1 guarded, in the fourteen shards of
[`valid7_replay_plan.json`](receipts/valid7_replay_plan.json), on 4-core cloud runners.
Each run was staged by `devtools.plan_valid7_replay stage --checker wand125 --guard-d1`
from the retained V2 `src/` and the October 1 packet’s cover, ran the plan’s command for
one rectangle of centres under CPython 3.14.7 and python-flint 0.9.0, and was resumed
from its own record after interruptions.
The receipts are in [`receipts/replay/`](receipts/replay/), each log written by
`devtools.replay_receipt`:

- **Records:** `wand125_shardNN_M.jsonl.gz`, one for each of the 33 region runs, as the
  runners compressed them ([Compressed Files](#compressed-files)).
- **Receipts:** `wand125_shardNN_M.log` for each run, and `_try2.log` to `_try4.log` for
  the 20 attempts that resumed an interrupted run, 53 in all.
  Every run’s last receipt reads `VERIFIED` and exit 0. None records an uncertified box,
  a counterexample or a Tier B error, so the guard refused nothing.
  A relaunch of shard 8’s third run overwrote its partial receipt and rebuilt its record
  from empty, so that one receipt covers the whole run.
- **Comparison:** `devtools.plan_valid7_replay compare --checker wand125 --guard-d1` on
  the 33 records, against the release records checked against
  [`release/records.sha256`](release/records.sha256)
  ([`wand125_replay_compare.json`](receipts/replay/wand125_replay_compare.json)): `ok`,
  exactly the 156,800 published roots, each once, in 9,808,968 leaves, and the leaf list
  of each of the 124,975 roots the source ran under V2 equal to the published one.
  The 31,825 roots it ran under V1, whose hand-off rule split differently, were certified
  again and not compared.
- **Cost:** from 2026-10-02T20:12Z to 2026-10-03T21:18Z.
  The 33 completing attempts’ receipts give 85.3 CPU-hours for the 76,767 roots they
  ran; the records’ per-root times, wall time in the worker as the source’s are, sum to
  205.8 hours over all the roots, against the plan’s 216.2.

This is wand125’s code, not Daniel’s, deciding Valid7 on the cover `T-064` cites, an
independent implementation by its read log.
The evidence entry is `E-k2m3-wand125-valid7-independent`.
No mutated cover was run in the replay; the three refused here are `verify.sh`’s, above.

## A Later Revision

On 3 October 2026 the author fixed the review’s D-1 to D-3 upstream, at `da469ec`, with
the release records unchanged.
The [3 October packet](../wand125-valid7-independent-check-2026-10-03/README.md) retains
that revision, its `verify.sh` run here on 5 October, and a probe showing each finding
present in this packet’s code and gone in that one.

## Compressed Files

The 33 shard records are receipts, compressed by the runners with `gzip -9n`: 51,005,708
bytes stored, 988,117,328 decompressed.
Each row gives the Git blob and SHA-256 of the decompressed bytes, as
`devtools.retained_data.describe` computes them.
Five records, shards `01_1`, `07_2`, `09_2`, `12_1` and `14_2`, decompress past the
64 MiB that `devtools.retained_data` reads, so this packet is outside its generic check;
`devtools.plan_valid7_replay` reads them unbounded.
`gunzip -k` on a stored file restores the record beside it.

| Stored file | Origin | Git blob | SHA-256, decompressed |
| --- | --- | --- | --- |
| `receipts/replay/wand125_shard01_1.jsonl.gz` | receipt | `ce4db9aa2de06ec1c767521398e3abaab71296f1` | `1e21370e1eba00f1231715e20cd671a3d136b82d9bfc49d9889b722d3923dcf3` |
| `receipts/replay/wand125_shard01_2.jsonl.gz` | receipt | `0ae936c8f737e3832c1655eda98cdd570f7a5b67` | `6b71972fef41cbbe220ffa1b898e344503c6cbfaa6e5a46de83b408a6ab461da` |
| `receipts/replay/wand125_shard02_1.jsonl.gz` | receipt | `8722ee32d67a61ef7535de7d261f9d0682306773` | `163ee6b5fff45fe06aa0b01d454f268216e7cdf94eaa3a1a1ee95bc2c4753435` |
| `receipts/replay/wand125_shard02_2.jsonl.gz` | receipt | `a3ed1e64ad6549936a877278fcf9b3490c88efaf` | `93e6a00d87fd476b2754585b6b190673526bd2111e9891876f472fc42869358a` |
| `receipts/replay/wand125_shard02_3.jsonl.gz` | receipt | `f9e54aaec0999816883c80206d7c6c6cf0c810b3` | `fba531dec716b1d4611903f943bfb3fc401a34a2ddb8b8a789e0bc46b2171063` |
| `receipts/replay/wand125_shard03_1.jsonl.gz` | receipt | `afe5e89fa2ca089f03f31b03f2db988f277da349` | `87a6d597c3eea6679673b289738e8d3fcc9c7b5d1cb8edfd941c2805f3bfb321` |
| `receipts/replay/wand125_shard04_1.jsonl.gz` | receipt | `a27fb9058bc426e44b4331256431da0c989225a4` | `9e7e85e880b4676a70d7e32163e7ebf734fb09a01f4ee46577d3de7dc2dc891b` |
| `receipts/replay/wand125_shard04_2.jsonl.gz` | receipt | `859fd009a1bb49067ce65884260c3d320637706a` | `7a1afafde625e0d5325979a89d722ab94d29a488f30e0b77c8a84a0a7cdf9f1d` |
| `receipts/replay/wand125_shard05_1.jsonl.gz` | receipt | `79d7db0d6eafa83655b6dac3fe6ea003c59571ef` | `a1eb6fe59140be6deea895db11267abd9b4fc39bdf7d43664ab8bf2292432dca` |
| `receipts/replay/wand125_shard05_2.jsonl.gz` | receipt | `6063e48f0bf9613169ca48b31eebfc07a73e3a44` | `7b8583df104e30708baff14dc22793d313a894ab7d8a733fd196d750d972fdac` |
| `receipts/replay/wand125_shard05_3.jsonl.gz` | receipt | `96a2bb1d61cac290c632031a72788cb18746f716` | `686abc45050c70fb0eb32e1bf237650dd11caea8d9803342c5468e86bd911ded` |
| `receipts/replay/wand125_shard06_1.jsonl.gz` | receipt | `91d1eff18f85da3abaf3f07a2f3a20a5775fbc72` | `65d05d2b4d54caba6d6b4bebb4111735013167372a586c18eb6f47ef566faf72` |
| `receipts/replay/wand125_shard06_2.jsonl.gz` | receipt | `b291a2dcd0443ff6024b9744d8afe566354c1e7c` | `9ca7ad20b3cba0830c7d8330904f53a1bb812af16e3b447c9a06f7edd3f1b438` |
| `receipts/replay/wand125_shard06_3.jsonl.gz` | receipt | `51af6f54937be95f72f63cdfa891f5b9a893b5c5` | `096bbb6095263a8ecc663544dfbe75d8daa2474fb55639a812d7a71b1c0c7e72` |
| `receipts/replay/wand125_shard07_1.jsonl.gz` | receipt | `a1059df1231600efc44fb94a2a100b8f4f968847` | `3a9cd4c7f67dae367e0ec2c2f10b5ab007eaca21e79de4ee0434033d0d5def4a` |
| `receipts/replay/wand125_shard07_2.jsonl.gz` | receipt | `622fc01c42fd5e88645c7c37df866f34ade22da8` | `c23860135d23f705d4ba2bde2e7b90f710eb0914e620fa15218f249f5ee5737a` |
| `receipts/replay/wand125_shard07_3.jsonl.gz` | receipt | `aa3930f16524e30f61d7c31708bf4c1b9d0c569e` | `f28e173f3e8c1c6e030daa6af14a7165bfa0d526dc322aa69b7d812730758174` |
| `receipts/replay/wand125_shard08_1.jsonl.gz` | receipt | `c87df72a08941a929b97bd03972ee94d2828527e` | `86c937ef8c5c7947c14fae2d475d83706f5f59a6e61580c9b3c807d48b516d84` |
| `receipts/replay/wand125_shard08_2.jsonl.gz` | receipt | `d9747cfab98d12bc86159b8e3fe89be8fe92c644` | `320d949b3258626d965da9d3cd633a4f6118e586075fa89528987b03e9406bba` |
| `receipts/replay/wand125_shard08_3.jsonl.gz` | receipt | `6e952d09a73c99efd88a5ba9a4fdc7155fa0476a` | `56fed0530d11232dda561e03c429230b2db8d79cd15d291fc21db54dbe96f4fe` |
| `receipts/replay/wand125_shard09_1.jsonl.gz` | receipt | `d4ce0746407e2aa51ec1c15863d60b9d75e5b84d` | `4a2f689fe81478dca92780367eee3cd5977931c5844ffbadc47bb6b0cf0a8c19` |
| `receipts/replay/wand125_shard09_2.jsonl.gz` | receipt | `63547e4fafe7efeef53fd126c07b245f221f4c00` | `326b2417561a114d1348ea03bbd059a746f46e0c578e1e8d232a578e9ffc3665` |
| `receipts/replay/wand125_shard09_3.jsonl.gz` | receipt | `90931b157c056d5c1cbdf6e4993dd2f1fe64d0ec` | `48f9b37d62666f03187e075cfed8a6a17dc9015e4ce50b95faa7d78a340270d8` |
| `receipts/replay/wand125_shard10_1.jsonl.gz` | receipt | `58e9cfaca1ffed19c5b7303b325907f52c27d42d` | `168c9f9fe381218ad7da7c9341654b1fbbdd51d09e1aa04385d1c86561d9da64` |
| `receipts/replay/wand125_shard10_2.jsonl.gz` | receipt | `cd220ec2b1391fd1530d65e3d4ba07f3096402e9` | `cfa65198cb0e9164d5a06c2ef6f3b039b310291ca057a37be7056619e31fee78` |
| `receipts/replay/wand125_shard10_3.jsonl.gz` | receipt | `8e52ef53161387e79e3877c26f56bccac7394a62` | `9e4a9e3c50b5733474ccc414803aaccdde12d53bebd03b7e3ce253a05675d63e` |
| `receipts/replay/wand125_shard11_1.jsonl.gz` | receipt | `64a3f09f27669535e1a2abd257f2ce12e96a167d` | `424cce05428085652699f20309cce0d76824034a4b9ed78d0c102a2d4d73bc8b` |
| `receipts/replay/wand125_shard11_2.jsonl.gz` | receipt | `88bdc8662651cd48a74fb49837d7471f3291a26f` | `6d6f28a8680ed5076a0b7b3ee181ae6534c196c752583a5939b51680fb17aae1` |
| `receipts/replay/wand125_shard12_1.jsonl.gz` | receipt | `fa1ef31a4a3a952dc5f0b19ab6a110be74015b51` | `236e84784a530f5c22ff76b3b457e25421006ddc9ab28a38cd49ad6f8aef1594` |
| `receipts/replay/wand125_shard13_1.jsonl.gz` | receipt | `0266be4614b7e53cfc92f70c1c6665caf12edc64` | `d45b0b40743813f5074b406208ed82e3aa8d75e4b3a0ecc54714c715a4295ba9` |
| `receipts/replay/wand125_shard13_2.jsonl.gz` | receipt | `18cc42be396e943ad1bdf965a652c606a9b0a3c0` | `c3ec2f4e07113c9e7edcc6264ff7450a88a2aa9b6903d24e546f4db97716f52d` |
| `receipts/replay/wand125_shard14_1.jsonl.gz` | receipt | `5c918252b2c3fdb54d9d1295205c84eb3d20a68c` | `6245cbe00a61ef54a3bcd616ac569968937c1c8c921a830653e279c425c7ccc8` |
| `receipts/replay/wand125_shard14_2.jsonl.gz` | receipt | `4311818d0ca7ef682ee4396d30a104e659a601de` | `57cf6c70d8deeee379afa9036c59eaea6189f40eaf96013aecef6fefa88e2dc2` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
