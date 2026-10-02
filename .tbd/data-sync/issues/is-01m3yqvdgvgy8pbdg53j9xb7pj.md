---
type: is
id: is-01m3yqvdgvgy8pbdg53j9xb7pj
title: Restore the model names in session-168's eleven cost rollups
kind: chore
status: open
priority: 1
version: 1
assignee: jlevy
labels:
  - session-168
dependencies: []
parent_id: is-01m3xgkna3m3w1w50ky6gqyxyk
created_at: 2026-10-02T16:41:09.403Z
updated_at: 2026-10-02T16:41:09.403Z
---
Session-168's eleven cost rollups are committed in fefca54a5 with the two model
identifiers replaced, because that session could not push model identifiers.
Every count is the rollup's own; only four labels differ from the originals.

The owner restores them in one commit on claude/ecstatic-archimedes-62hj6a
(PR jlevy/squares#305):

1. Either extract `session-168-rollups-original.tar.gz` (sent in the session
   chat) into `packing/campaign/resource-usage/`, or apply the reverse
   substitution given in the chat to the eleven files below. It maps
   `model-withheld-a`, `model-withheld-b`, `withheld-word-1` and
   `withheld-word-2` back to their originals.
2. Run `uv run --frozen --all-extras --group dev python -m devtools.close_session --render`
   and `packing-ledger render` from `packing/`; neither output should change,
   since the tables carry no model names. Then `packing-validate --records`.
3. Commit and push.
4. Replace the two labels in the PR body's "Model use" table.

| Rollup | Lane | Label | Turns |
| --- | --- | --- | ---: |
| `6179239e-fec5-52e8-aabb-a0e229f3f822.yaml` | Coordinator | a | 956 |
| `agent-a665a16af102749a0.yaml` | Literature: packing families | a | 216 |
| `agent-a68c888b24723b197.yaml` | Family census tool | a | 181 |
| `agent-a9f4406a56646937f.yaml` | Contact-shade census tool | a | 213 |
| `agent-a92ea862bac5a1405.yaml` | Asymptotics: limits of families | b | 111 |
| `agent-ae1c5c75727ba7c4d.yaml` | Exact regularization feasibility | b | 183 |
| `agent-a86fe91008fdb802b.yaml` | T-007 review A: Nagamochi Lemma 1 audit | b | 130 |
| `agent-ad8c36a04ebcd61d9.yaml` | T-007 review B: consumer inventory | a | 296 |
| `agent-a30ab1dd97b959c63.yaml` | Archive sources, fix asymptotic record | a | 404 |
| `agent-abfdcf4d3642c3fe2.yaml` | Codify X-049 hypotheses | b | 110 |
| `agent-a4a764a6285487659.yaml` | Regularized-view atlas layer | a | 297 |

Totals: label a 2,563 turns, label b 534, one synthetic turn; 3,098 in all.
`withheld-word-1` and `withheld-word-2` occur only in the coordinator's rollup,
as two command-name keys. Done when the eleven files carry the real names,
the records tier passes, and the PR body's table matches.
