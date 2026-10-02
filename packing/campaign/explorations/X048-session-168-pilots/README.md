# X-048 Session 168 Pilots: Receipts

Session 168 ran BC-418, the coordinating entry after Session 167. Its sub-pattern
selector lane built H-267’s heuristic selector as a retained tool, and its kernel lane
ran the adapted n11 prover on the first flagged patterns; their outputs are kept here.

These are **planning evidence, not admitted results**. The selector proposes forbidden
sub-patterns and certifies none, and the kernel has not yet closed one.
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
| `receipts/selector-arity7-seed1.json` | The run to arity 7 with seed 1 at commit d674e665, 2,028 s on two workers: 44 flagged classes (3 at arity 6, 41 at arity 7) and the certification priority |
| `receipts/selector-arity7-seed2.json` | The same run with seed 2 on one worker, 3,498 s; see the provenance note below |
| `receipts/selector-arity7-seed2.log` | Its progress log |
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
- **Arity 7 reaches the threshold, heuristically.** 41 more classes are flagged, 44 in
  all, with best penetrations from $6.2\times10^{-5}$ to $2.3\times10^{-2}$. If all are
  certified, 40,016 states and **5,084 orbits** survive, below H-267’s $10^4$. The
  thinnest flags are the likeliest to be false, and the top-priority class is now a
  west-wall column plus two interior cells.
- **The flags are stable under a second seed.** Seed 2 flags exactly the same 44
  classes, with best penetrations within 5% of seed 1’s, and the same survivors at every
  arity. The seed-2 run imported the committed selector (`a40f34fb…`) at launch; its
  receipt’s `module_sha256` names `d33762ab…`, a later working-tree edit by another
  lane, because the selector hashes its file when it writes the receipt rather than when
  it imports it. That defect is being fixed in the selector.
- **The endpoint survives at every arity.** Its own sub-pattern classes are witnessed at
  its pose to penetration $7\times10^{-16}$ and are never flagged.
- **One false flag can remove half the census.** Before the deep stage was added, two
  classes were flagged that other seeds placed, and one of them alone excluded 171,604
  states. The prover is load-bearing.

Reproduce, from `packing/`:
`uv run --frozen --all-extras --group dev python -m devtools.select_n17_sub_patterns --max-arity 6 --seed 1 --workers 2 --output FILE`.

## The Kernel on Flagged Patterns

Lane K2, Opus at extra-high effort, extended `sqpack.hull_kernel` with a sequential
grammar (refinement, revisits, derived closures, stall reporting) and a producer.
It ran them on three arity-6 flags and one arity-7 flag through
`devtools/check_n17_subpattern.py` (SHA-256 `893b5206…`). The producer proposes rows
over uniform angle bins; the checker certifies exactly what it emits, so a certified
stall is a sound statement that these rows exclude nothing.

| Receipt | Pattern | Bins | Outcome | Wall |
| --- | --- | ---: | --- | ---: |
| `receipts/kernel-A-bins16.json` | A: interior-{SW,NW,W,S,N,SE}, penetration $1.49\times10^{-2}$ | 16 | round cap at 4 rounds, still changing slowly | 35.6 s |
| `receipts/kernel-B-bins16.json` | B: side-S1, side-W1, interior-{NW,W,S,SE} | 16 | stall | 6.4 s |
| `receipts/kernel-C-bins16.json` | C: interior-{NW,W,S,N,E,SE} | 16 | stall | 7.4 s |
| `receipts/kernel-W7-bins64.json` | W7: the top arity-7 flag, the west-wall column with side-N0, interior-SW and interior-W | 64 | round cap at 6 rounds, still contracting | 990 s |
| `receipts/kernel-endpoint6-bins64.json` | Control: six cells of the endpoint’s own state | 64 | stall, as required | 15.6 s |

Nothing is excluded yet.
The obstacle is reach, not splitting: the axis interior cells have least enclosing
radius about $0.52$, so they own no point from the cell alone, and most of B’s and C’s
cells never own anything.
W7 is the lead: at 64 bins its west-wall owners grew hulls of 32 to 66 vertices and
shrank to $0.57\times0.36$ and $0.85\times0.20$ before the round cap.
The levers are collision regions from partner pose covers, which reach owners with empty
hulls; a bounded compression that holds step cost flat; and finer bins for A, whose
64-bin producer run eliminated rows that 16 bins did not.
A two-cell closure control certifies, and the n11 mask-0 and case-2095 replays are
unchanged and exact on the same kernel.

Reproduce, from `packing/`:
`uv run --frozen --all-extras --group dev python -m devtools.check_n17_subpattern --pattern W7 --bins 64 --max-rounds 6 --output FILE`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
