# Plan: The First Application of the Result Import Process

**Date:** 2026-10-01

**Author:** Claude (agent), for the repository owner

**Status:** In progress.
Stage 1, triage, is done for all six requests bar the acknowledgements, which are the
owner’s to post, and is what this plan reports.
Step 2 below, stages 2 and 3 for all six, ran on 1 October in jlevy/squares#292: the
sources are retained and the claims registered as reported, as `T-066` to `T-069`. No
certificate has been replayed and no reply posted.

**Workflow:** W10 planning, for six imports that each run a W1 phase and then a W2 phase

**Beads:** `think-5xr9` for the process; one bead for each import, named below

## Summary

Six requests are waiting: five issues opened between 30 September and 1 October, and
Evan Daniel’s answer of 1 October on issue 238. Two older issues, 227 and 247, carry
replies that are out of date, and issue 170 was never answered.
This plan applies
[the result import process](../../../../packing/campaign/result-import.md) to them, and
it is the test of that process: it fixes in advance what would show that the process is
rigorous, consistent and efficient.

The triage ran on the public sources through the GitHub API. No upstream program was
run, so every cost below is the source’s own figure, or an estimate from replays already
measured here and marked as one.

## The Six Imports

| Import | Request | Claim | Register action | Starts at |
| --- | --- | --- | --- | --- |
| A, `think-x73z` | Issue 256, Daniel | $s(60) = 8$ and $s(61) = 8$ | None new: `T-062` and `T-063` hold it, reported, from the survey of 1 October | Stage 4 |
| B, `think-48e1` | Daniel’s comment on issue 238 | A run that certifies the $s(32)$ cover without the symmetry fold; who was allowed to read what | None new: an evidence update to `T-051` | Stage 2 |
| C, `think-oy3i` | Issue 280, wand125 | $s(59) = 8$ | A new optimality entry | Stage 2 |
| D, `think-xujq` | Issue 279, wand125 | $s(77) = 9$ | A new optimality entry | Stage 2 |
| E, `think-6ei5` | Issue 281, wand125 | 34 rectangle-density lower bounds, $n = 19$ to $95$ | A new lower-bound entry; `T-046` keeps its claim | Stage 2 |
| F, `think-ye2x` | Issue 282, wand125 | Mixed rectangle-measure bounds at $n = 37, 65, 66, 90, 92$ | A new lower-bound entry; `T-048` keeps its claim | Stage 2 |

**Pins.** Daniel’s repository is at `08e8a5fa`, which is the revision this record
already retains; the revisions the issues name, `d9f79bc1`, `b91d70b6` and `2bf33bc3`,
are all behind it on one line of history, and the cover files are identical at all four
revisions.
wand125’s repository is at `1a25a5ed`, 34 commits past the retained `39d8ecc`.
C, D, E and F share that release; by the precedent of the 28 September packets they are
retained as two packets by subject, the rectangle certificates in one and the exact
covers with the mixed certificates in the other, with a bibliography key for each
subject.

**Corollaries.** $s(59) = 8$ gives $s(60) = s(61) = 8$ by monotonicity, and $s(77) = 9$
gives $s(78) = 9$, the $k = 9$ case of `T-064`. By the runbook nothing is superseded:
`T-062`, `T-063` and `T-064` each gain a sentence naming the newer route.

**Claims the releases make that no request mentions.** wand125’s release also holds a
point-only cover for $s(61) = 8$ (`think-hxrz`), which Daniel’s repository has already
replayed with `zeromargin.py` and `zmcheck`, of which this project has run the first in
full for $s(32)$ and never the second; a Lean proof of its point-only $s(21) = 5$, which
bears on `T-055`; and standing rectangle certificates at $n = 59, 77, 78$, below the
exact values now claimed there.
The first two are imports of their own.
The rectangle certificates stay in the packet, and are replayed only if C or D is not
confirmed.

## What Triage Found

1. **The source’s verification of C and D cannot pass as published.** Each `SHA256SUMS`
   lists run logs that are not in the repository, whose `.gitignore` excludes `*.log`,
   so `verify.sh`, read and not run here, stops at its checksum step.
   Both issues say the logs are there.
   The replies below ask for them.
2. **C’s exact evidence is two runs.** The complete `zm_mixed.py` run ends
   `NOT VERIFIED` with six boxes; a second run of one root at greater depth closes them.
   Both used the checker that predates Daniel’s guard against a zero-width angle bin.
   The review decides whether the composite is a proof.
3. **D’s cover has a shape the reviewed covers do not.** It replaces 84 points on loaded
   grid lines by segments of length $2/1000$. The review checks whether either checker’s
   lemmas depend on the earlier shape.
4. **No verifier here is independent of the sources’ code for these formats.** Nothing
   in this repository decides a mixed cover.
   The native rectangle verifier reads E’s format and has never finished an external
   certificate; it refuses F’s. Every confirmation below is therefore a replay of the
   source’s checker on retained bytes, and each entry’s `composition` will say so.
5. **Replays that passed are still off `main`.** All 21 stranded rectangle receipts
   verify a bound above its case’s present verified value.
   Issue 281 has since raised 14 of those certificates; each receipt still proves its
   own bound. The complete replays for `T-048` and `T-055` are unmerged too.
   Landing the 21 rectangle receipts costs no CPU and waits on a merge mode for batch
   receipts (`think-0rrj`).
6. **B has nothing to resume.** The partial re-sweep records for $s(21)$ and $s(45)$
   never reached Git.
7. **Four tools need extending before a replay counts:** `audit_evand_mixed_covers`
   knows only the mixed covers 21 and 45 (`think-ubor`, for A, B, C and D);
   `audit_wand125_rectangles` needs a third packet and `apply_wand125_rectangles` a
   third registration (E); the mixed-rectangle part of `audit_wand125_point_and_mixed`
   is written for $n = 50$ alone (F).
8. **The issues and the record disagree in small ways.** Issue 280 gives the record’s
   value at $n = 59$ as 7.93; it is $198/25 = 7.92$. Issue 282 compares $n = 37$ and
   $n = 90$ with Green and Nagamochi; the record holds wand125’s own 6.425 and 9.55.
   Issue 281 says each directory carries a tarball; none does.

## Order of Work

No order is forced by the mathematics: each cover is checked as its own object.
The order below is by cost, cheapest confirmation first.

| Step | Work | Workflow | Cost |
| --- | --- | --- | --- |
| 1 | Post the acknowledgements and the corrections (`think-75yv`) | Stages 1 and 7 | Minutes |
| 2 | One import pull request for C, D, E and F: the two packets, their keys, four entries as reported, the case records. In the same change, link issue 256 to `T-062` and `T-063` and add the $s(32)$ and $s(60)$ run records to the 1 October Daniel packet | W1, stages 2 and 3 | About 7 MB retained, estimated; the mutation snapshot, which counts only linked files, has 16.9 MiB of headroom |
| 3 | Land the 21 stranded rectangle receipts, which raise the verified lane at 21 counts; `T-048` and `T-055` also need their evidence entries and controls, and `T-055` a comparison still to run | W7 for the merge mode, then W2 | No replay CPU for the 21 receipts |
| 4 | Extend `audit_evand_mixed_covers` (`think-ubor`) | W7 | One slice |
| 5 | Replay A: `zmx2 --d4` and `--full`, root for root | W2 | About 560 CPU-seconds, estimated |
| 6 | Replay C: both `zmx2` sweeps | W2 | About 2,200 CPU-seconds at the source |
| 7 | Replay B: `zmx2 --full --pair-points --sym-atoms` | W2 | 11,592 CPU-seconds at the source |
| 8 | Replay D: `zmx2 --d4 --pair-points`, then `--full` | W2 | At most 4.9 thread-hours, then at most 37.5, from the source’s wall times on 16 threads |
| 9 | Replay F: five mixed certificates | W2, after a W7 slice | 45 to 90 CPU-hours, estimated |
| 10 | Replay E: 34 rectangle certificates | W2 | 148.5 CPU-hours at the source; about 230 worker-hours here, estimated |

The mathematics reviews run beside the replays, in lanes that do not see the replay
results: one for C and D together, since both extend Daniel’s cover; one for A’s
geometric premises; one for B’s account of what the two checkers share; and one short
review each for E and F, whose methods the reviews of 27 and 28 September already cover.

**The exact route is a separate decision.** `zm_mixed.py` in exact rationals costs 19.6
CPU-hours for A, 127 for C and 94 for D, and 12.9 and 16.5 for the lost $s(21)$ and
$s(45)$ re-sweeps. It is the same program by the same author as the source’s run, so it
adds a second arithmetic and no independence (`think-mx3k`). The plan runs it on idle
CPU after steps 5 to 8, as the second route that stage 4 names, and not as a condition
of `C3`.

**Ratings.** Each new entry enters at `V0/C0` with a draft score, and `C1` once its
review is recorded.
A complete `zmx2` replay with its control and review derives `V3/C3`,
the rungs `T-052` and `T-053` stand at on the same kind of evidence.
The draft scores of C and D are set beside `T-062`, whose own score is one of the pairs
the rescoring pass will settle (`think-qh3s`).

## The Test

The process is being tried for the first time, so what counts as passing is fixed here,
before any import runs.
`think-daa8` fills this table when the six imports close and revises the runbook where a
measure failed.

| Quality | Measure | Passes when |
| --- | --- | --- |
| Rigor | Exits | Every stage’s exit is met, and the import’s bead cites the commit or comment for each |
|  | Rungs | Every declared rung equals what `check_results` derives |
|  | Verified lane | No bound enters it without a complete replay receipt on `main` and a mapped review with no blocking defect open |
|  | Controls | Every certificate has two mutated controls refused under test |
|  | Two lanes | Every review is committed before its lane sees the replay’s result |
| Consistency | Sequence | Every import declares W1 for stages 1 to 3 and W2 for stage 4 |
|  | Packet | One README shape, with the facts stage 2 lists |
|  | Dates | `published` and `dated` follow the runbook’s rule in every entry |
|  | Replies | Every reply has the same parts and links only to `main` |
| Efficiency | Import | Each request is on `main` as reported on the day its pull request opens |
|  | Rework | No `T-NNN` is renumbered after it is stated outside the repository; one data re-pin for each pull request |
|  | Replay | No receipt is lost; the measured CPU of each replay is recorded beside the source’s figure |
|  | Truth on the issues | At close, no statement on any of the nine issues differs from `main` |

One measure cannot pass for this batch: an acknowledgement within a day.
Issue 256 is already more than a day old.

## Replies Ready for the Owner

Each draft was checked against `main` at `f25a85cb5`. The owner posts them, or says
which an agent should post; nothing is posted by this plan.
The acknowledgements state no `T-NNN` for the new results and no rung, as the runbook
requires.

**Issues 279 and 280, wand125.**

> Thank you for both, and for writing each request in the form the frontier README asks
> for. They are being imported together from `wand125/square-packing-bounds` at
> `1a25a5ed745fdd905a52f48fcc48150a0669032d`. Each will be registered as reported first,
> then replayed and reviewed here, and I will reply at both points.
> 
> One thing blocks the replay as published.
> The `SHA256SUMS` of `k2m5_n59_L8` and `k2m4_n77_L9` list `zmx2_d4/run.log`,
> `zmx2_full/run.log` and the `zm_mixed` run logs, and those files are not in the
> repository (its `.gitignore` excludes `*.log`), so, as we read the script, `verify.sh`
> stops at its checksum step.
> Could you publish them, with the `roots.jsonl` files the manifests name by digest?
> Until then we will run the same checks on the retained bytes and compare totals.
> 
> For 280: the record’s reported lower bound at $n = 59$ is $198/25 = 7.92$, not 7.93.

**Issue 281, wand125.**

> Thank you. These 34 will be registered as a new entry for your release at `1a25a5ed`;
> T-046 keeps its claim as of 28 September, and the case records decide which
> certificate is current at each count.
> Twenty-one of the earlier certificates have already been replayed here in full, and
> those receipts are being landed first: each still proves its own bound.
> A small point: the rectangle directories carry no tarball; from each directory the
> candidate, the metadata, the verification summary and the per-angle rows are retained,
> and the checker input is regenerated from the candidate against the digest your run
> recorded.

**Issue 282, wand125.**

> Thank you. The five will be registered as a new entry beside T-048, from the same
> release as 279 to 281. The proof bundles will be pinned by digest and not retained, as
> for $n = 50$. Two of the comparisons differ from this record: at $n = 37$ its reported
> lower bound is already your 6.425, and at $n = 90$ your 9.55 by transfer from
> $n = 89$. Later counts can be added to this issue as you publish them; each release is
> imported and answered separately.

**Issue 256, Daniel.**

> $s(60) = 8$ and $s(61) = 8$ are registered as T-062 and T-063, from your repository at
> `08e8a5fa`; the cover is byte for byte the one at the `d9f79bc1` this issue names.
> Both read *reviewed*: the argument from the cover to the bound was read here and no
> defect was found, and nothing has been replayed yet, so the verified lower bounds at
> $n = 60$ and $61$ are unchanged.
> Next is a replay of both of your checkers on the retained bytes, `zmx2` first,
> compared root for root with your logs, and a review of the geometric premises.
> I will reply here when they are done.

**Issue 238, Daniel.**

> Thank you for the `--full --sym-atoms` run and for the answer on provenance.
> Both will be imported as an update to T-051’s evidence: the run’s records retained,
> the run replayed here, and the entry’s account of what the two checkers share
> rewritten, with the fold removed and the note that zmx2’s author could read
> `zeromargin.py` added.
> The brief you cite, `tasks/s21-finish/xcheck.md`, is not in the public tree; could you
> publish it?
> 
> Four statements in my reply of 29 September are out of date.
> T-051, T-052 and T-053 now read `V3/C3`: the ladder changed on 30 September, rung 4
> now needs two adversarial reviews and a human oversight record, and a second machine
> method is recorded beside the rung instead of raising it.
> Pull request 245 merged.
> The `zm_mixed.py` re-sweeps for $s(21)$ and $s(45)$ had reached 35% and 29% of the
> source’s CPU total when last recorded, and their partial records were lost with the
> session that ran them, so they restart from nothing.
> And `s13_eq_4` and the conditional $s(21)$ and $s(32)$ theorems were built here on 30
> September; `s32_eq_6` has not been.

**Issue 247, Wang and Li.**

> A correction to my reply of 30 September.
> Your result is registered as **T-061**, not T-058: an id is a row’s position in the
> register, and yours moved when two branches merged.
> Its rungs read `V3/C3`: the ladder changed on 30 September, rung 4 now needs two
> adversarial reviews and a human oversight record, and nothing about your certificate
> changed. It does not hold the verified lower bound at $n = 11$, because $s(11)$ is
> settled (T-060); T-061 stays registered as true and is marked superseded.
> The review is on `main` at
> `docs/project/reviews/review-2026-09-30-issue-247-wang-li-n11.md`. This issue stays
> open for the revised Zenodo record.

**Issue 227, Couzo.**

> An update. The import is on `main` (pull requests 248 and 249), so the earlier links
> into a working branch no longer resolve; the review is at
> `docs/project/reviews/review-2026-09-29-issue-227-upper-bound-packings.md` and the
> interval route is in
> `packing/resources/web/franciscouzo-square-packing-2026-09-27/README.md`. T-056 and
> T-057 read `V3/C3`: the ladder changed on 30 September, and the second method is
> recorded beside the rung.
> Nothing you asked for is queued.
> The three trailing cases at $n = 206$, $259$ and $305$ stay as recorded conflicts; if
> you have poses refined beyond binary64, post them here and the records will take them.

**Issue 170, wand125, closed.**

> A late reply, with an apology for the silence here.
> Your point certificates are registered as T-044: ten exact weighted certificates,
> fourteen counts with the four that follow from them, replayed here in full and
> credited “wand125 after Levy, Stromquist, Nagamochi, Burns, Massaccesi”.
> They read `V3/C3` and hold the verified lower bound at twelve of those counts.

## Limits

- Every upstream cost is the source’s figure.
  Every local estimate is marked as one.
- Earlier `zmx2` replays ran on x86-64 Linux.
  The source’s caveat about outward rounding names x86-64, and this host is an Apple M1
  Pro, so the platform is a question for the review of A before the replays run.
- The triage read the sources’ READMEs, scripts, manifests and checksum files, and did
  not re-read the checker sources.
- One earlier cloud session refused to run external code.
  Every replay here runs the retained copy of a source’s checker, so the sessions that
  run them need that permission.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
