# Changes in v0.1.4 of the Eleven-Square Optimality Review, for Its W2 Exposition Review

**Date:** October 4, 2026\
**Author:** Claude Code, one sub-agent session; human oversight pending\
**Subject:** the
[paper](../../../packing/devtools/templates/n11-optimality-review-article.md), v0.1.3 to
v0.1.4, answering
[wand125’s comment of October 4](https://github.com/jlevy/squares/issues/317#issuecomment-5975093980)
on jlevy/squares#317\
**Status:** awaiting the paper’s W2 exposition review, as
[stage 6 of the result import process](../../../packing/campaign/result-import.md#stage-6-explain)
requires

wand125 cross-checked v0.1.3 against their Lean formalization data and raised three
points and a remark on dependencies.
Each was checked against the retained packet before the text changed.
No register entry, receipt, checker or rung changes; T-060 stays at S5/V3/C3.

## What Changed

| # | Change | Why | Evidence |
| --- | --- | --- | --- |
| 1 | The section on what was verified now names the two in-progress Lean 4 formalizations, [wand125/n11-optimality-lean](https://github.com/wand125/n11-optimality-lean) and [Queuingtheorydotcom/11SquaresFormalized](https://github.com/Queuingtheorydotcom/11SquaresFormalized). It gives their status as wand125 reports it: the 173 returned cases and the 76 prior cases are kernel-checked using only the standard axioms. It says the project has reviewed neither, and that T-060’s rungs do not rest on them. A new footnote cites the comment. The sentence saying that no proof-assistant formalization is claimed stays. | The paper stated that no formalization is claimed but did not say that any existed. | The comment; both repositories exist (read on October 4); [11SquaresFormalized pull request 7](https://github.com/Queuingtheorydotcom/11SquaresFormalized/pull/7), open, records a Lean 4.34.1 replay of 173/173 returned cases whose axiom queries print only `propext`, `Classical.choice` and `Quot.sound` |
| 2 | “The root node then runs fourteen further updates” becomes “completes thirteen further updates”. A new sentence says the fourteenth step covers only part of its angle range and is checked but changes no ownership. The capture footnote now links the two receipts that hold the count. | The retained data show 13 completed updates. | [`capture-step0/result.json`](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/capture-step0/result.json) is the first update, `PASS_FIRST_CAPTURE_STEP_TRANSITION`. [`capture-root-node-full-integer/result.json`](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/capture-root-node-full-integer/result.json) lists steps 1–13 with steps 1–12 `complete: true`; step 13 is `complete: false` after 103 rows, with `steps_checked: 14`. The [checker](../../../packing/devtools/check_n11_capture_root_node.py) promotes only complete steps with index at most 12 and requires the partial step to be step 13, with no kernel. The register counts the 14 root rounds, not the root node’s updates. |
| 3 | The Figure 8 caption now says that the composed proof’s symmetry lemma rests on the accepted check’s exhaustive assignment search over the 220 regions and 1,572 bans, and that the one-ban proof is checked beside it but is not a premise. The text gains the same statement where it introduces the shorter proof. | The caption called the exhaustive search “a separate obligation” while the text offered a one-ban proof, and a reader could not tell which the lemma rests on. | [`final-composition.json`](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/final-composition.json) binds `d4-independent` (`PASS_INDEPENDENT_CONDITIONAL_D4_BRIDGE`, 1,572 strict bans, three UNSAT searches). The [receipts register](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/README.md) files `d4-incidence` as a replacement that the validation guide alone reads. The paper already says that none of the October 3 components is a premise. |
| 4 | The paragraph on cases 2175 and 2176 now says that they are two of the publisher’s 76 prior cases and the only two whose accepted certificates carry the 1,931-case premise. It says the cuts are checked only against the 253 cases the baseline leaves, and that the premise belongs to those certificates rather than to the cases. A new footnote cites the manifest, the cut report and the census review. The sentence giving the publisher’s grouping $1931+76+173$ now names its three groups (baseline, **prior**, **returned**), the terms changes 1 and 4 use. | wand125’s remark that their prior-family proof needs no baseline premise. Only the parts the retained data verify are stated (see below). | [`nonfield-manifest/manifest.json.gz`](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/nonfield-manifest/manifest.json.gz): 76 A2 cases (the prior cases: 73 wall-seed, one closed center partition, two `baseline_necessary_d4`), with `required_baseline_cases: 1931` on 2175 and 2176 only. [`replay-d4-cuts.json`](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/generic-case2175-complete/replay-d4-cuts.json) has `baseline_execution_premise_admitted: true` over 506 raw survivor masks. See the [census review, special adapters](review-2026-09-29-n11-optimality-census-contract.md#the-three-special-adapters). The group names follow the stages `prior-76-full-geometry` and `returned-173-full-geometry` in [the original’s §12](../../../packing/resources/web/n11-optimality-2026-09-29/source/PROOF.md#12-how-the-23-verification-stages-support-the-theorem). |
| 5 | The version is v0.1.4, “Last revised” is October 4, 2026, and the history gains its entry. The three documents that quote the version line now quote the new one. | The precedent of v0.1.1–v0.1.3. | `packing/src/sqpack/release.py`, `packing/devtools/paper_front.py`, `packing/devtools/templates/paper-design.md`, `development.md` |

## What Was Not Stated

- **A baseline-free proof of cases 2175 and 2176.** wand125 reports one, and the
  retained data cannot check it.
  The accepted certificates depend on the premise: their cuts are justified by an
  exhaustive search over the 506 raw masks of the 253 baseline survivors.
  The Lean prior-family proof is not retained here.
  The README on `main` of wand125’s repository, which was last pushed on October 2,
  still lists the 76 prior cases as not yet formalized.
  The comment of October 4 is the only source for that status, and the paper attributes
  it.
- **Which repository kernel-checks the 76 prior cases.** The comment does not say, so
  the paper does not assign them.

## For the Reviewer

Read the four passages in the rendered paper, under “Charge Budgets Exclude Many
Patterns at Once”, “Symmetry Reduces the Four Survivors to One”, “Capture Forces Case
438 Near the Construction” and “What Was Verified, and What the Verification Means”.
Check that each new sentence is supported by the evidence cited in its row.
The paper must still state nothing the T-060 register entry does not hold.
The attributed report of external work in change 1 is the only statement the register
does not itself hold.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
