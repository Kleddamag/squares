# H260 Closed-Cell Symmetry: Independent Output Review

Reviewed on 2026-10-01 after the single target run at frozen commit
`ba5d35fae7daeada6146a26c991d19c0a5a82bad`. The complete retained outputs satisfy
[H260’s acceptance criterion](../../../../hypotheses/H-260-n17-closed-cell-symmetry.md).
The eight fixed counts sum to **161,244,144**, giving **20,155,518** occupancy orbits
under the eight container symmetries.
This is strictly below the H259 raw count of 161,100,756. There is no mathematical,
input-binding, receipt, or resource blocker to acceptance.
The coordinator owns the recorded verdict.

This review inspected the frozen proof and implementation, complete input mapping, all
eight cycle profiles and counts, both JSON receipts, raw byte bindings, provenance,
commands, wrapper, exits, and timings.
It did not rerun the producer or auditor.
The independently implemented binomial auditor ran in the recorded target group; this
review checks its retained results and their interpretation, without claiming a third
arithmetic implementation.

## Spatial Contract and Symmetry Coverage

The [input contract](input-contract.json) matches its frozen Git blob byte for byte.
The producer receipt and the JSON argument in [commands.txt](run-001/commands.txt) both
match its grid size five, target seventeen, and full row-major capacity list.
Reindexing the H259 contract by its explicit spatial index pairs gives exactly this
list: capacity one on all sixteen boundary cells and capacity two on all nine interior
cells. H260 changes the indexing from H259’s grouped receipt order without changing any
spatial capacity.

The cap remains $U=1169/250$, with closed cell width $919/1250$. The accepted H259
geometric capacity proof remains a premise.
The
[closed-assignment review](../../../../../../docs/project/reviews/review-2026-10-01-n17-closed-cell-symmetry.md)
defines each occupancy case by the existence of an assignment of centres to containing
closed cells. These case domains cover every packing at the cap.

The physical maps induce $R(i,j)=(j,4-i)$ and $F(i,j)=(4-i,j)$, preserving every cell
capacity.
Applying a symmetry to a packing and its assignment produces a valid assignment
in the transformed occupancy case; applying the inverse establishes equality of the
transformed case domains.
Therefore one case representative per occupancy orbit covers packings up to container
symmetry. Overlap among closed assignment domains does not invalidate that coverage.

This proof requires existential closed membership.
The lexicographically preferred seam assignment from H259 does not commute with
reflection. Future representative cases must retain the declared closed membership and
omit lex-priority exclusions.
This is a condition on the later geometry, rather than a convention the arithmetic
checker can establish.

## All Eight Fixed Counts

The producer constructs permutations and counts the cycle factors by dynamic
programming. Its order is `r0`, `r1`, `r2`, `r3`, `f0`, `f1`, `f2`, `f3`, where `rN`
means $R^N$ and `fN` means $R^N F$, with reflection applied first.
This agrees with the frozen proof and the independent auditor’s roster.

In the table, $m(\ell,c)$ means $m$ cycles of length $\ell$ and capacity $c$. Every
retained profile accounts for all twenty-five cells, including sixteen boundary cells
and nine interior cells.
The sorted profile lists agree exactly with the independently derived profiles; all
eight counts agree between [count.json](run-001/count.json) and
[audit.json](run-001/audit.json).

| Action | Complete Cycle Profile | Fixed Assignments |
| --- | --- | ---: |
| `r0` | $16(1,1)+9(1,2)$ | 161,100,756 |
| `r1` | $1(1,2)+4(4,1)+2(4,2)$ | 36 |
| `r2` | $1(1,2)+8(2,1)+4(2,2)$ | 3,748 |
| `r3` | $1(1,2)+4(4,1)+2(4,2)$ | 36 |
| `f0` | $2(1,1)+3(1,2)+7(2,1)+3(2,2)$ | 34,892 |
| `f1` | $2(1,1)+3(1,2)+7(2,1)+3(2,2)$ | 34,892 |
| `f2` | $2(1,1)+3(1,2)+7(2,1)+3(2,2)$ | 34,892 |
| `f3` | $2(1,1)+3(1,2)+7(2,1)+3(2,2)$ | 34,892 |

The quarter turns partition the sixteen boundary cells into four four-cycles and the
eight noncentral interior cells into two four-cycles.
The half turn pairs those cells.
Every reflection fixes two boundary and three interior cells, then pairs the fourteen
remaining boundary and six remaining interior cells.
The centre is a fixed capacity-two cell under every rotation.
These arguments establish the profiles independently of the producer’s cycle traversal.

The independent arithmetic uses the previously reviewed binomial helper

$$
C(p,q,n)=\sum_{k=0}^{\min(q,\lfloor n/2\rfloor)}
\binom{q}{k}\binom{p+q-k}{n-2k},
$$

with out-of-range binomial coefficients zero.
Its identity term is $C(16,9,17)$. Odd occupancy forces central occupancy one for both
nonidentity rotation types, giving $C(4,2,4)$ for each quarter turn and $C(8,4,8)$ for
the half turn. Each reflection uses

$$
\sum_{j\in\lbrace1,3,5,7\rbrace} C(2,3,j)\quad C(7,3,(17-j)/2).
$$

The auditor imports no producer arithmetic.
It validates the fixed capacity array, eight named profiles and counts, total sum,
divisibility by eight, quotient, and strict reduction.
Its reported `audit_passed` and `strict_reduction` are both true.
Target-free controls covered the producer’s small-grid direct orbit enumeration,
eight-action group laws and capacity preservation, central fixed occupancy, malformed
inputs, and the auditor’s hand-derived empty and one-unit counts and receipt mutations.
This lane’s twelve auditor controls passed before freeze; their run did not evaluate
target seventeen.

Summing the retained terms and dividing by eight gives

$$
161100756+2\cdot36+3748+4\cdot34892
=161244144=8\cdot20155518.
$$

The exact raw-to-orbit ratio is $8950042/1119751$, approximately $7.99288591839$. The
nonidentity fixed counts sum to 143,388, so the quotient exceeds the raw count divided
by eight by $35847/2$. This agrees with the explicit fully symmetric state having
occupancy one on every boundary cell and the centre; a free-action division would be
invalid.

## Receipt Binding and Execution

The count receipt is 1,420 bytes with SHA-256
`bef48b79ae60b3ff7ee78478191754acb285b21fae7659d082c7bef14ea9134d`. Its audit reports
both values, which this review independently checked against the raw bytes.
The audit’s identity binding is the accepted H259 receipt SHA-256
`ee71cc9f1a6a94f1b1ce965e7fe095b525a71caa28203f2d15420fd7ec400a37`. The current H259
bytes match that binding.
Its target count, this input contract’s `identity_count`, `r0`, and the auditor’s
`identity_count` all equal 161,100,756.

[provenance.txt](run-001/provenance.txt) records the full frozen commit.
The coordinator reports that tracked files were clean at execution; review also found no
tracked changes, with only the new run directory untracked.
The code, proof, input contract, and accepted H259 receipt are part of the frozen
checkout.

The complete [wrapper](run-001/wrapper.txt) retains the timed invocation:

```bash
/usr/bin/time -l gtimeout --signal=TERM --kill-after=5s 30s \
  /bin/bash --noprofile --norc -e /absolute/path/to/run-001/commands.txt
```

The linked wrapper contains the actual absolute path.
It imposes a 30-second group ceiling and five-second forced-termination grace.
The inner script uses the project interpreter, external-volume scratch variables,
disabled bytecode writes, and `ulimit -f 1024`. The invoked Bash documents file limits
in 1,024-byte units, so this is a 1 MiB per-file limit.
Its two CLIs run sequentially on one worker.
With `-e`, each zero marker is written only after its command succeeds.

Both [exit markers](run-001/exits.tsv) and the [group exit](run-001/group-exit.txt) are
zero. Both JSON outputs are complete; `group.stdout` is empty.
The start and end timestamps are `2026-10-01T14:15:58Z`, consistent with their
one-second resolution and the subsecond elapsed time.
The host-load receipt records 18.74, 24.48, and 30.30.

| Process | Wall Seconds | User Seconds | System Seconds | Peak RSS Bytes | JSON Bytes |
| --- | ---: | ---: | ---: | ---: | ---: |
| Producer | 0.05 | 0.04 | 0.01 | 20,840,448 | 1,420 |
| Independent auditor | 0.07 | 0.05 | 0.01 | 24,707,072 | 729 |
| Complete group | 0.14 | 0.09 | 0.03 | 24,707,072 | — |

The [producer](run-001/count.time), [auditor](run-001/audit.time), and
[group](run-001/group.time) timing receipts all report zero swaps.
At printed precision, the group includes 0.02 seconds beyond the two CLI wall times.
The two JSON files total 2,149 bytes.
All fourteen run artifacts are below the output ceiling; the largest is the 1,802-byte
command file. The recorded group duration satisfies the time ceiling.

These measurements include interpreter startup and JSON handling.
They exclude mathematical derivation, implementation, controls, review, and
documentation. The counting cost does not measure a geometric exclusion for any
representative case.

The result supplies 20,155,518 necessary occupancy cases modulo container symmetry.
It retains geometrically impossible states and leaves their compatible poses,
orientation domains, and exclusion costs unresolved.
It changes neither the certified packing bound nor the open global optimality status of
seventeen squares.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
