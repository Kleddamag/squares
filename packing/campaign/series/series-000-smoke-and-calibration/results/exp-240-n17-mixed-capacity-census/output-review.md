# H259 Mixed-Capacity Census: Independent Output Review

Reviewed on 2026-10-01 by the independent endpoint-review lane after the single frozen
target run. The retained outputs satisfy the numerical acceptance criterion in
[H259](../../../../hypotheses/H-259-n17-mixed-capacity-cover.md): the mixed cover has
**161,100,756** occupancies summing to seventeen, versus **8,597,496,600** for the
baseline. Both independent binomial audits accept all eighteen coefficients through
degree seventeen and the total number of occupancies.

This review reads the complete receipts, compares their fields and source bindings, and
computes the ratio from the retained counts.
It does not rerun either producer or auditor.
The coordinator owns the recorded scientific verdict.

## Input and Proof Scope

The working [input contract](input-contract.json) matches its Git blob at
`b8e3e170f3141c3d893abdbeefa0bce944783c64` byte for byte.
Both producers and audits report target $17$. The mixed capacity list is sixteen ones
followed by nine twos; the baseline list contains thirty-six ones.

The mixed contract contains all twenty-five spatial index pairs in the five-by-five grid
exactly once. Its order is the sixteen boundary cells in lexicographic order, then the
nine interior cells in lexicographic order.
Every listed boundary cell has capacity one and every interior cell capacity two.
The seam owner is the lexicographically least spatial index pair among containing closed
cells. The grouped receipt order therefore preserves the declared spatial assignment.

The independently reviewed
[geometric proof](../../../../../../docs/project/reviews/review-2026-10-01-n17-mixed-capacity-cover.md)
supplies the capacity premises at $U=1169/250$, with centre-box side $919/250$ and cell
side $919/1250<3/4$. It covers arbitrary orientations and closed seams.
This output review relies on that proof; the counting CLIs establish integer occupancy
counts. Their exact object description is “integer occupancies of indexed cells; square
identities ignored.”
No symmetry quotient or additional compatibility cut is applied.

## Complete Receipt Agreement

The [mixed producer receipt](run-001/mixed.json) and its
[independent audit](run-001/mixed-audit.json), and the
[baseline receipt](run-001/baseline.json) and its
[independent audit](run-001/baseline-audit.json), agree in capacity order, target,
counted objects, target assignments, total assignments, and every coefficient below.
Both audits report `audit_passed: true`, `coefficients_checked: 18`,
`method: closed-binomial-sum`, and `producer_imported: false`.

| Degree | Mixed Coefficient | Baseline Coefficient |
| --- | ---: | ---: |
| 0 | 1 | 1 |
| 1 | 25 | 36 |
| 2 | 309 | 630 |
| 3 | 2,516 | 7,140 |
| 4 | 15,170 | 58,905 |
| 5 | 72,174 | 376,992 |
| 6 | 281,926 | 1,947,792 |
| 7 | 928,840 | 8,347,680 |
| 8 | 2,631,249 | 30,260,340 |
| 9 | 6,501,281 | 94,143,280 |
| 10 | 14,163,137 | 254,186,856 |
| 11 | 27,432,744 | 600,805,296 |
| 12 | 47,548,534 | 1,251,677,700 |
| 13 | 74,119,342 | 2,310,789,600 |
| 14 | 104,303,994 | 3,796,297,200 |
| 15 | 132,878,972 | 5,567,902,560 |
| 16 | 153,541,952 | 7,307,872,110 |
| 17 | 161,100,756 | 8,597,496,600 |

The producer uses dynamic programming.
For $p$ capacity-one and $q$ capacity-two cells, the independently implemented auditor
uses

$$
\operatorname{coeff}_{x^n}\bigl((1+x)^p(1+x+x^2)^q\bigr)
=\sum_{k=0}^{\min(q,\lfloor n/2\rfloor)}
\binom{q}{k}\binom{p+q-k}{n-2k},
$$

with out-of-range binomial coefficients zero.
The audited totals are $2^{16}3^9=1,289,945,088$ and $2^{36}=68,719,476,736$. These
totals range over all occupancy sums; the degree-seventeen coefficients fix the sum to
seventeen.

The exact ratios are

$$
\frac{\text{baseline}}{\text{mixed}}
=\frac{238819350}{4475021}\approx53.3672020757,
\qquad
\frac{\text{mixed}}{\text{baseline}}
=\frac{4475021}{238819350}.
$$

Thus the mixed census is approximately 1.87381005769% of the baseline census.
The exact fractional decrease is $234344329/238819350$. These compare cardinalities for
two different indexed covers; they do not identify one census as a subset of the other.
The preregistration disclosed that the mixed total already guaranteed a reduction before
evaluating the degree-seventeen coefficient.

The audit metadata binds the raw mixed receipt to 424 bytes and SHA-256
`ee71cc9f1a6a94f1b1ce965e7fe095b525a71caa28203f2d15420fd7ec400a37`, and the baseline
receipt to 463 bytes and SHA-256
`c5a34cb8f2d0387996e4539e49e872df7209e31bd24045858d94009409a9c6a1`. This review
independently recomputed both byte counts and hashes; all four match.

## Execution and Resource Accounting

The retained [commands](run-001/commands.txt) run four CLIs sequentially under the
project interpreter, with external-volume `TMPDIR`, `CARGO_TARGET_DIR`, and
`UV_CACHE_DIR`, and bytecode writes disabled.
They set `ulimit -f 1024` and record each successful command in
[exits.tsv](run-001/exits.tsv).
All four recorded exits are zero; [group-exit.txt](run-001/group-exit.txt) is also zero
and `group.stdout` is empty.
Each output is complete JSON.

The coordinator supplies this executed outer invocation as execution evidence:

```bash
/usr/bin/time -l gtimeout --signal=TERM --kill-after=5s 30s \
  /bin/bash --noprofile --norc -e "$run_dir/commands.txt"
```

It sets the 30-second combined ceiling with a five-second forced-termination grace; the
shell’s `-e` makes the recorded zero markers conditional on command success.
This invocation is coordinator-reported evidence, rather than text present in the
retained `commands.txt`. The retained timing and group status provide the observed
completion evidence.
The file limit and sequential process order are directly present in `commands.txt`.

The [provenance receipt](run-001/provenance.txt) names frozen commit
`b8e3e170f3141c3d893abdbeefa0bce944783c64`. At review, tracked files are unchanged and
only the new run directory is untracked.
The input contract agrees with the frozen commit.
Start and end records both read `2026-10-01T14:02:38Z`; their one-second resolution is
consistent with the subsecond measured duration.
The [host-load record](run-001/host-load.txt) reports load averages 26.93, 30.67 and
36.76.

| Process | Wall Seconds | User Seconds | System Seconds | Peak RSS Bytes | JSON Bytes |
| --- | ---: | ---: | ---: | ---: | ---: |
| Mixed producer | 0.08 | 0.05 | 0.01 | 20,971,520 | 424 |
| Mixed independent audit | 0.08 | 0.05 | 0.01 | 24,772,608 | 1,004 |
| Baseline producer | 0.07 | 0.05 | 0.01 | 20,824,064 | 463 |
| Baseline independent audit | 0.07 | 0.05 | 0.01 | 24,969,216 | 1,098 |
| Complete group | 0.35 | 0.22 | 0.08 | 24,969,216 | — |

The four per-process `.time` receipts and [group timing](run-001/group.time) supply
these measurements. At their printed precision, producer wall times total 0.15 seconds,
independent audit wall times total 0.15 seconds, and group overhead is 0.05 seconds.
All report zero swaps.
The four JSON outputs total 2,989 bytes; the largest run artifact is the 1,321-byte
command file. Every artifact is below the 1 MiB output ceiling, and measured group wall
time is below the 30-second ceiling.
The sequential commands use one worker.

These are process timings, including interpreter startup and JSON handling.
They do not isolate the arithmetic kernel or include mathematical review,
implementation, synthetic controls, documentation, or proof preparation.
They also do not measure the cost of geometrically excluding an occupancy.

## Acceptance Scope

There is no count, input-binding, completeness, or observed-resource blocker to H259’s
acceptance criterion.
The previously reviewed geometry and target-free controls remain separate premises.
The retained independent audit proves the arithmetic census for the supplied capacities;
this review additionally binds those capacities to the frozen spatial contract.

The accepted reduction leaves 161,100,756 necessary integer occupancy vectors.
Their geometric realizability, compatible poses and orientation domains, and exclusion
costs remain unresolved.
It supplies no new lower bound or global optimality proof for seventeen unit squares.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
