# Changes in v0.1.4 of the Eleven-Square Optimality Review, for Its W2 Exposition Review

**Date:** October 4, 2026\
**Author:** Claude Code, one sub-agent session; human oversight pending\
**Subject:** the
[paper](../../../packing/devtools/templates/n11-optimality-review-article.md), v0.1.3 to
v0.1.4, answering
[wand125’s comment of October 4](https://github.com/jlevy/squares/issues/317#issuecomment-5975093980)
on jlevy/squares#317\
**Status:** the first W2 exposition review, required by
[stage 6 of the result import process](../../../packing/campaign/result-import.md#stage-6-explain),
returned two Medium and eight Low findings.
All ten are applied, as recorded [below](#the-w2-review-and-its-findings).

wand125 cross-checked v0.1.3 against their Lean formalization data and raised three
points and a remark on dependencies.
Each was checked against the retained packet before the text changed.
No rung, claim, composition, receipt or checker changes; T-060 stays at S5/V3/C3, and
its register entry gains one dated note.

## What Changed

| # | Change | Why | Evidence |
| --- | --- | --- | --- |
| 1 | The section on what was verified names the two in-progress Lean 4 formalizations, [wand125/n11-optimality-lean](https://github.com/wand125/n11-optimality-lean) and [Queuingtheorydotcom/11SquaresFormalized](https://github.com/Queuingtheorydotcom/11SquaresFormalized). It reports, attributed to wand125, that the 76 prior-family and 173 returned cases are kernel-checked using only the standard axioms. It says an independent replay of the 173 is recorded in an open pull request that was not merged as of October 4. It says the project has reviewed neither formalization and that T-060’s rungs do not rest on them. The sentence saying that no proof-assistant formalization is claimed stays. The `[^lean]` footnote cites the comment and wand125’s prior-family theorem. | The paper said no formalization is claimed, without saying that any existed. | The comment. [11SquaresFormalized pull request 7](https://github.com/Queuingtheorydotcom/11SquaresFormalized/pull/7), by Guzhou0806, is open against `codex/stronger-computer-handoff-20261002`; it records a Lean 4.34.1 replay of 173/173 returned cases whose axiom queries print only `propext`, `Classical.choice` and `Quot.sound`. For the prior-family theorem, see the U2Prior entry under “Read but not checked here”. |
| 2 | “The root node then runs fourteen further updates” becomes “completes thirteen further updates”. A new sentence says the fourteenth step covers only part of its angle range and is checked but changes no ownership. “All of this is verified” becomes “replayed here, in the capture receipts cited below”. The capture footnote links the two receipts that hold the count. | The retained data show 13 completed updates. | [`capture-step0/result.json`](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/capture-step0/result.json) is the first update, `PASS_FIRST_CAPTURE_STEP_TRANSITION`. [`capture-root-node-full-integer/result.json`](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/capture-root-node-full-integer/result.json) lists steps 1–13 with steps 1–12 `complete: true`; step 13 is `complete: false` after 103 rows, with `steps_checked: 14`. The [checker](../../../packing/devtools/check_n11_capture_root_node.py) promotes only complete steps with index at most 12, and requires the partial step to be step 13 with no kernel. The register counts the 14 root rounds, not the root node’s updates. |
| 3 | The Figure 8 caption says the composed proof’s symmetry lemma rests on the accepted check’s exhaustive assignment search over the 220 regions and 1,572 bans, and that the shorter proof, which needs one ban, is checked beside it and is not a premise. The text says the same where it introduces the shorter proof. | The caption called the exhaustive search “a separate obligation” while the text offered a one-ban proof. A reader could not tell which one the lemma rests on. | [`final-composition.json`](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/final-composition.json) binds `d4-independent` (`PASS_INDEPENDENT_CONDITIONAL_D4_BRIDGE`, 1,572 strict bans, three UNSAT searches). The [receipts register](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/README.md) files `d4-incidence` as a replacement that only the validation guide reads. |
| 4 | The paragraph on cases 2175 and 2176 says they are two of the publisher’s 76 prior-family cases, and the only two whose accepted certificates carry the 1,931-case premise. It says the cuts are checked only against the 253 cases the baseline leaves, and that the premise is a premise of those certificates. It adds that wand125 reports a Lean proof of all 76 prior-family cases that does not use the premise. The `[^premises]` footnote cites the manifest, both cut reports and the census review. The sentence giving the publisher’s grouping $1931+76+173$ now names its groups (baseline, **prior-family**, **returned**). | wand125’s remark that their prior-family proof needs no baseline premise. | The [`nonfield-manifest`](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/nonfield-manifest/manifest.json.gz) has 76 A2 cases: 73 wall-seed, one closed center partition and two `baseline_necessary_d4`, with `required_baseline_cases: 1931` on 2175 and 2176 only. The cut reports for [2175](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/generic-case2175-complete/replay-d4-cuts.json) and [2176](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/generic-case2176-complete/replay-d4-cuts.json) admit the baseline premise over 506 raw survivor masks. See the [census review, special adapters](review-2026-09-29-n11-optimality-census-contract.md#the-three-special-adapters). The group names follow the original’s stages `prior-76-full-geometry` and `returned-173-full-geometry` in [§12](../../../packing/resources/web/n11-optimality-2026-09-29/source/PROOF.md#12-how-the-23-verification-stages-support-the-theorem). |
| 5 | T-060’s `notes` gain a dated entry for 2026-10-04. It names the two formalizations and gives wand125’s report: the kernel-checked cases, and that the prior-family proof does not use the baseline premise. It says the project has not reviewed or replayed either formalization and that no rung rests on them. `DATA_REVISION` is re-pinned in its own commit. | So that the paper states nothing the register does not hold (stage 6). | [`packing/frontier/results.yaml`](../../../packing/frontier/results.yaml); the register, inventory, tables and headline re-render unchanged |
| 6 | The version is v0.1.4 and “Last revised” is October 4, 2026. The history entry says wand125’s comment is answered. The three documents that quote the version line quote the new one. | The precedent of v0.1.1–v0.1.3. | `packing/src/sqpack/release.py`, `packing/devtools/paper_front.py`, `packing/devtools/templates/paper-design.md`, `development.md` |

## Read but Not Checked Here

- **wand125’s prior-family theorem.**
  [`U2Prior.lean`](https://github.com/wand125/n11-optimality-lean/blob/112f91a0a0a30539472718b88e06e71f64d61694/lean/Sqpack/S11Opt/Split/U2Prior.lean)
  is on the `split` branch of wand125/n11-optimality-lean, at commit `112f91a0a`
  (October 1: “prior_excluded for the 76 prior cases (kernel-checked, standard axioms
  only)”).
  - It states `prior_excluded : ∀ i ∈ priorIdx, CaseExcluded (maskAt i)` with no
    baseline hypothesis.
  - Its 76 cases are exactly the manifest’s A2 case IDs, 2175 and 2176 among them.
  - Its docstring says “Nothing of the author’s prior certificates is used”.
  - Its `scripts/u2p/README.md` states the axioms are `propext`, `Classical.choice` and
    `Quot.sound` only.
  - The per-case proofs are generated files kept in release archives, not in the
    repository.
  - The `split` head, `8126ef4d5` of October 2, differs from the pin in this file only
    by a manifest file name in the docstring.

  The repository’s `main`, last committed on September 30 (`ee96259ef`), still lists the
  76 cases under “Not yet formalized”.
  This project has neither reviewed nor replayed the theorem, so the paper attributes
  the report to wand125 and links the pinned file.

- **The 173 returned cases.** The replay in pull request 7 is read from that pull
  request’s description and has not been replayed here.

## The W2 Review and Its Findings

| Finding | Disposition |
| --- | --- |
| M1: this list wrongly said the comment was the only source for the prior-family status, and wrongly dated wand125’s `main` | Applied. U2Prior is described above and linked, pinned, from `[^lean]`. |
| M2: the register held nothing on formalizations | Applied as change 5. |
| L1: pull request 7 is open and unmerged | Applied in change 1. |
| L2: start the sentence with “Cases 2175 and 2176 are two of…” | Applied. |
| L3: attribute the baseline-free proof | Applied in change 4. |
| L4: “the shorter proof, which needs one ban” | Applied. |
| L5: “prior” clashed with the bolded **common prior** | Applied: “prior-family” wherever it names the 76 cases. |
| L6: say which verification precedes the local theorem | Applied in change 2. |
| L7: cite case 2176’s cut report | Applied. |
| L8: the history entry says the comment is answered | Applied. |

## For the Reviewer

Read the four passages in the rendered paper, under these headings:

- “Charge Budgets Exclude Many Patterns at Once”;
- “Symmetry Reduces the Four Survivors to One”;
- “Capture Forces Case 438 Near the Construction”;
- “What Was Verified, and What the Verification Means”.

Check that each new sentence is supported by the evidence cited in its row, and that
wand125’s report and the 2026-10-04 note on T-060 say the same thing.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
