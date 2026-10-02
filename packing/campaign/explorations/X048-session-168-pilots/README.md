# X-048 Session 168 Pilots: Receipts

Session 168 ran BC-418, the coordinating entry after Session 167. Its sub-pattern
selector lane built H-267’s heuristic selector as a retained tool, and its outputs are
kept here.

These are **planning evidence, not admitted results**. The selector proposes forbidden
sub-patterns and certifies none.
Until an independent prover certifies a pattern infeasible, nothing it flags excludes a
case.

## H-267: The Sub-Pattern Selector

`devtools/select_n17_sub_patterns.py` (SHA-256 `a40f34fb…`), built by lane S1, Opus at
extra-high effort, runs on the unique-state cover `ring-3-voronoi-8-tabbed-unique` at
cap $1169/250$. It enumerates the sub-patterns of $k$ occupied cells that are connected
in the cells’ interaction graph, up to D4. For each one it searches hard for a feasible
placement: unit squares with centres in their cells, any orientations, inside the
container, pairwise disjoint.
It flags a pattern only when every attempt leaves positive penetration, including a deep
second stage. An exact consumer then counts the D4 orbits that contain no flagged
pattern.

| Receipt | What it holds |
| --- | --- |
| `receipts/selector-arity6-seed1.json` | The run to arity 6 with seed 1, its controls and survivor counts, and the certification priority |
| `receipts/selector-arity6-seed1.log` | Its progress log, 264 s on two workers |
| `receipts/selector-seed-study.json` | The three flagged classes re-searched under seeds 1 to 4 |
| `receipts/selector-arity7-seed1.json` | The run to arity 7 with seed 1 at commit d674e665, 2,028 s on two workers: 44 flagged classes and the certification priority |
| `receipts/selector-arity7-seed1.log` | Its progress log |
| `receipts/selector-lane-f-retest.json` | The bulk-exclusion lane’s exploratory arity-5 flags re-searched on its own design |

The findings:

- **Nothing is flagged at arity 5 or below.** All 6,589 connected classes are placed.
  This corrects the bulk-exclusion design review’s exploratory proxy, whose 10 arity-5
  flags (and 11,939 orbits) were false: on that lane’s own design this search places all
  of them.
- **Three classes are flagged at arity 6,** all crowds of interior cells, with best
  penetrations of $1.49\times10^{-2}$, $5.6\times10^{-3}$ and $2.0\times10^{-3}$, stable
  across four seeds. If all three are certified, 185,424 states and 23,354 orbits
  survive. That is still above H-267’s threshold of $10^4$, so arity 7 (43,086 connected
  classes) is needed.
- **Arity 7 reaches the threshold, heuristically.** 44 classes are flagged, with best
  penetrations from $6.2\times10^{-5}$ to $2.3\times10^{-2}$. If all are certified,
  40,016 states and **5,084 orbits** survive, below H-267’s $10^4$. The thinnest flags
  are the likeliest to be false, and the top-priority class is now a west-wall column
  plus two interior cells.
- **The endpoint survives at every arity.** Its own sub-pattern classes are witnessed at
  its pose to penetration $7\times10^{-16}$ and are never flagged.
- **One false flag can remove half the census.** Before the deep stage was added, two
  classes were flagged that other seeds placed, and one of them alone excluded 171,604
  states. The prover is load-bearing.

Reproduce, from `packing/`:
`uv run --frozen --all-extras --group dev python -m devtools.select_n17_sub_patterns --max-arity 6 --seed 1 --workers 2 --output FILE`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
