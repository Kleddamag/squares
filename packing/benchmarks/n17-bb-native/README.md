# Native n17 Branch-and-Bound Benchmark

This instrument compares the retained Python branch-and-bound pilot with its native
kernel and the resumable multiprocess driver.
The search algorithm, relaxation, and outward-rounded checks remain the pilot’s. The
native arms change the implementation of the hot paths.

## Runbook

Build the extension, then run the three arms on pattern A from `packing/`:

```shell
NATIVE_DIR="$(uv run --frozen python -m devtools.build_n17_bb_native | tail -1)"
uv run --frozen python -m benchmarks.bench_n17_bb_native \
  --native-dir "$NATIVE_DIR" \
  --arms python,native,parallel \
  --patterns A \
  --workers 8 \
  --max-seconds 900 \
  --out benchmarks/n17-bb-native/results.jsonl
```

Use `--patterns A,F7,F6` to include the feasible controls.
`--cells` adds a custom comma-separated cell list and may be repeated.
Each arm and pattern appends one JSON object to the output.
Every object records the verdict, nodes, closed share, CPU seconds, wall seconds, worker
count, machine description, and Git revision.

`cpu_seconds` is the process CPU used by a single-process search.
For the parallel arm, it is coordinator CPU plus reaped worker CPU, including worker
startup and shutdown; `search_cpu_seconds` separately sums the workers’ bounded search
chunks. The time cap stops new chunks.
A chunk already running finishes before the driver saves its result, so wall time can
exceed the cap by one chunk.

The parallel arm keeps its queue and cumulative timings under the directory selected by
`--state-dir`. Its checkpoint binds the mathematical search settings and pattern.
A later invocation may use another worker count, checkout revision, or native build; the
state retains each invocation’s provenance and continues the same open tree.
The final receipt lists every Git revision that contributed work and marks a
mixed-revision resume.
A checkpoint written during an interrupted invocation also sets `cpu_seconds_complete`
to false because the operating system cannot recover CPU used by workers killed before
they reported a chunk; its cumulative CPU value is then a lower bound.

The parallel driver refuses certificate options.
Certificate recording uses the unchanged single-process Python path because the
certificate recorder depends on one ordered traversal.

## Local Integration Run

[The three receipts](results-2026-10-05.jsonl) were recorded on 2026-10-04 UTC, at
source revision `9bbc3200d`, on arm64 macOS 25.2.0 with Python 3.14.7. The extension was
built with installed Rust 1.99.0; the repository-pinned 1.98.0 toolchain was
unavailable. Each arm used a 30-second cap and fresh state.

| Arm | Workers | Verdict | Nodes | Closed share | CPU s | Wall s |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| Python | 1 | unresolved-at-budget | 2,388 | 0.020187377929687556 | 23.443 | 30.018 |
| Native | 1 | unresolved-at-budget | 21,147 | 0.4779340955946184 | 21.677 | 30.003 |
| Native parallel | 8 | certified-infeasible | 41,958 | 1.0 | 52.440 | 21.686 |

The parallel search CPU was 40.456 seconds; its total also includes coordinator and
worker startup/shutdown CPU. The capped single-process runs do not measure time to
completion, so they do not establish a full-run speedup.

## Retained Measurements

These measurements predate the repository instrument.
They are retained as historical observations rather than converted into invented JSONL.
The source is the dated `PERF_LOOP.md` from the port work; the baseline Linux row also
has the original pilot receipt.
CPU time is the comparison metric on the loaded Apple host.

| Date | Machine | Arm | Pattern | Workers | Verdict | Nodes | CPU s | Wall s |
| --- | --- | --- | --- | ---: | --- | ---: | ---: | ---: |
| 2026-10-04 | Apple M4, arm64 macOS, shared host | Python pilot | A | 1 | certified-infeasible | 41,617 | 463 | 830 |
| 2026-10-04 | Apple M4, arm64 macOS, shared host | Native S4 | A | 1 | certified-infeasible | 41,958 | 47.2 | 108.4 |
| 2026-10-04 | Apple M4, arm64 macOS, shared host | Native S4 parallel | A | 8 | certified-infeasible | 41,958 | 44.8 | 13.3 |
| Not recorded | Google Cloud c2d-highcpu-16, x86-64 Ubuntu 24.04, quiet host | Python pilot | A | 1 | certified-infeasible | 41,598 | 434.5 | 434.5 |
| Not recorded | Google Cloud c2d-highcpu-16, x86-64 Ubuntu 24.04, quiet host | Native S4 | A | 1 | certified-infeasible | 41,958 | 42.6 | 44.0 |
| Not recorded | Google Cloud c2d-highcpu-16, x86-64 Ubuntu 24.04, quiet host | Native S4 parallel | A | 16 | certified-infeasible | 41,958 | 61.2 | 5.2 |

The native tree has 41,958 nodes on both recorded architectures.
Different optimal LP duals make it 0.8% larger than the Python and HiGHS tree; all
closures still pass the pilot’s outward-rounded dual check.
The controls `F7` and `F6` remained unresolved in the retained 900-second runs.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
