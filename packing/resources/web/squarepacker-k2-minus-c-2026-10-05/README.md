# squarepacker’s `k² − M(k) ≥ 0.033 log k`, Pinned 2026-10-05

Sungjoon Ryu (GitHub `squarepacker`) reports a preprint on the integer-side case of the
asymptotic problem. Let `M(k)` be the largest number of unit squares that fit in
`[0,k]²` pairwise disjoint as closed sets.
The preprint’s Theorem 1.1 says that for every integer `k ≥ 2`,

`k² − M(k) ≥ 0.033 log k` (natural logarithm),

and `k² − M(k) ≥ (0.99977 log k + 0.3819)/30.147` for `k ≥ 10¹³`.
Its Lemma 2.1 shows that `s(n) < k` exactly when `n ≤ M(k)`. Corollary 1.2 follows:
`c*(k) := max{c : s(k² − c) = k}` is at least `0.033 log k − 1`. Hence, for every fixed
`c`, `s(k² − c) = k` for all large `k`.
The constant `0.033` uses the computer-assisted Lemma 4.10. With the analytic Lemma 4.9
alone, the same proof gives `0.027`.
The claim reached this repository as
[jlevy/squares#368](https://github.com/jlevy/squares/issues/368), opened by
squarepacker on 2026-10-05 at 14:16 UTC.

The result is squarepacker’s, after Roth and Vaughan: the proof sharpens the fundamental
lemma of their 1978 paper and builds on it.
This packet holds the source repository whole at a pinned commit, and the replay run
here. What the record makes of the claim is in
[`asymptotic-waste-bounds.yaml`](../../../frontier/asymptotic-waste-bounds.yaml).

## Source and Pin

| Field | Value |
| --- | --- |
| Source | <https://github.com/squarepacker/k2-minus-c> |
| Revision | [`25f645e8fcadb3c2768f4da42d80e977fb1a508d`](https://github.com/squarepacker/k2-minus-c/tree/25f645e8fcadb3c2768f4da42d80e977fb1a508d), `main` when fetched, tree `d384face` |
| Committed | 2026-10-05T15:15:50Z (`2026-10-06T00:15:50+09:00` by the author’s clock). Seven commits in all. The first, `987c8068` at 14:00:55Z, adds the preprint, every program and the data |
| Versions | Tag `v1.0` is `0eb29d44` (released 14:07Z). Tag `v1.1` is `525da4e3` (released 15:10Z). The pin is `v1.1` plus the DOI line in `README.md`. Version 1.1 adds `code/coverage_independent/` and one sentence in the proof of Lemma 4.10, and changes the preprint’s date line. The README says “The mathematics is unchanged”, and the diff of `paper/paper.tex` bears that out |
| Archive | Zenodo, as the source’s `README.md` gives it: [10.5281/zenodo.23165736](https://doi.org/10.5281/zenodo.23165736) for `v1.1` and [10.5281/zenodo.23164302](https://doi.org/10.5281/zenodo.23164302) for `v1.0`, which the issue cites; the concept DOI is `10.5281/zenodo.23164301`. Zenodo was not reachable from this session (the proxy refused the connection), so neither record was read |
| Retrieved | 2026-10-05T17:10Z, a complete clone; tags at 17:15Z |
| Licence | MIT for `code/` and `data/` (`LICENSE`, copyright Sungjoon Ryu). CC BY 4.0 for `paper/paper.tex` and `paper/paper.pdf` (`paper/LICENSE`) |
| Request | [jlevy/squares#368](https://github.com/jlevy/squares/issues/368) |

**Credit and AI assistance, as the source states them.** The README and the preprint
name Sungjoon Ryu as the sole author. The README says the work was “developed with
extensive assistance from Claude (Anthropic), including the proofs, the text, the
programs and the computation for Lemma 4.10; the author takes full responsibility. Not
peer reviewed.” The preprint’s “Use of AI” section says the same and adds that Claude
“is not an author”. `reviews/REVIEWS.md` summarises the reviews the author ran. All of
them were by AI reviewers, which it says “are AI systems of the same family and may share
blind spots”, and no human has refereed the manuscript.

## What Is Retained

Every file of the tree, 78 files and 1,679,573 bytes, under
[`k2-minus-c/`](k2-minus-c/), byte-identical. The manifest is
[`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256) and the
record [`acquisition/sources.json`](acquisition/sources.json). Both are written by
`devtools.acquire_source` from
[`acquisition/declaration.json`](acquisition/declaration.json). The source’s own
`SHA256SUMS` lists 75 of the 78 files; all 75 match. It omits `README.md`, `.zenodo.json`
and itself, as its README says.

| Upstream path | What it is |
| --- | --- |
| `paper/paper.pdf`, `paper/paper.tex` | The preprint, version 1.1, 25 pages |
| `data/kw9_data.zip` | The certificate of Lemma 4.10: the 13 lists of accepted boxes (`*_T9_*_final_leaves.jsonl`, 78,673 boxes in all), with the author’s verification and coverage outputs and logs. 435,000 bytes, SHA-256 `32634874…`; 29,515,409 bytes in 94 files unpacked |
| `code/verify_leaves2.py`, `code/verify_leaves.py` | The Arb re-verification. `verify_leaves2.py` is the certificate’s checker, and it imports `verify_leaves.py` |
| `code/bnb.py`, `code/bnb_wall.py` | The floating-point branch-and-bound searches. Their cell, mask, split and point-count routines are also called by the verifier |
| `code/coverage_check.py` | The author’s coverage check, which rebuilds the bisection tree with the search’s own split rule |
| `code/coverage_independent/` | Two coverage checks written apart from the search, by exact volumes and by recursive covering, with their results |
| `code/verify_v10.py`, `code/consts_v10.py`, `code/kw13_check.py`, `code/check_hand9_indep.py` | The preprint’s numerical constants in `mpmath`, the facts used in Lemma 4.9(c), and the nine-pair configuration at 80 digits |
| `code/make_stats_v10.py`, `code/run_v2.py`, `code/run_seq.py` | Statistics and job runners |
| `code/SUPERSEDED.md` | Why the first verifier, which left one-ulp gaps between direction cells, is withdrawn |
| `code/experiments/` | Search programs behind the numerical experiments of Remark 7.5, not part of the proof |
| `reviews/REVIEWS.md` | The author’s summary of the AI reviews |

From `packing/`,
`uv run --frozen --all-extras --group dev python -m devtools.acquire_source squarepacker-k2-minus-c-2026-10-05 --check`
re-derives the packet from its manifest.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
