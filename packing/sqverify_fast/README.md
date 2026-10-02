# sqverify-fast

A clean-room verifier for measure-capture lower-bound certificates: given a nonnegative
measure on $[0, L]^2$ of mass below $n$, it checks that every shrunk square of side $B$,
at each of the 201 net directions and every centre, captures at least the threshold,
which proves $s(n) \ge L$. It is lane W2 of `think-gpe0`, written without reading the
authors’ checkers ([INDEPENDENCE.md](INDEPENDENCE.md)), with every lemma it relies on
proved in [SOUNDNESS.md](SOUNDNESS.md).

Milestone A, rectangle-density certificates, is implemented: exact admission, the axis
direction by an exact-event vertex sweep, the rotated directions by interval branch and
bound. Points and segments (Milestone B, `think-4vf7`) and continuous-angle covers are
not.

## Use

From `packing/sqverify_fast/`, `cargo build --release`, then:

```bash
target/release/sqverify-fast --candidate PATH.json.gz --n N [--side P/Q] \
    [--directions all|a-b|r1,r2] [--threshold P/Q] [--threads K] \
    [--receipts DIR] [--confirm]
```

Standard output is one JSON receipt per direction and a summary line; the exit status is
0 only when every requested direction is verified (`VERIFIED` for the whole net,
`PARTIAL` for a subset), 1 when one is refused, and 2 on an admission refusal.
The default threshold is the certificate’s declared one, else 1. `--confirm` evaluates a
refusal’s witness in exact rationals.
`--probe r,x,y[,dx,dy]` prints the certified centre (and box) bound beside the exact
capture, for differential tests.

## Checks

- `cargo test --release`: unit, property and exact-oracle tests.
- `packing-validate --only "measure verifier Rust"`: fmt, clippy, tests, docs, release
  build, then `devtools.check_sqverify_fast --quick` (differential against
  `sqpack.rectangle_density` and the mutation controls).
  Without `--quick` the check covers more certificates and directions.
- `devtools.sqverify_fast_census`: every replayed certificate at all 201 directions;
  results and the generated table are in
  [`benchmarks/measure-verifier/census/`](../benchmarks/measure-verifier/census/).

## How to Resume

Everything needed is on the branch; nothing lives only in a session.

1. Read [SOUNDNESS.md](SOUNDNESS.md) (the obligations every change must keep) and the
   clean-room rule at the top of [INDEPENDENCE.md](INDEPENDENCE.md).
   Append to the independence record every file you read and every command you run.
2. The performance campaign is
   [`benchmarks/measure-verifier/`](../benchmarks/measure-verifier/): its README is the
   runbook (metric vector, accept rule, commands), `ideas.md` the idea board,
   `hypotheses/` the registry, `experiments/` one record per round, `results/` the raw
   JSONL. The standing best build is the one the latest accepted experiment produced,
   which is the committed source.
3. To run one round: build the control and the candidate, copy both binaries aside, then
   from `packing/` run `python -m benchmarks.bench_measure_verifier --arm
   fast:control=A --arm fast:candidate=B --callgrind --repeats 1 --cells
   rect_n32_L595@r1,rect_n32_L595@r100,rect_n61_L796@r100 --out results/exp-NNN.jsonl`,
   then the same without `--callgrind` and with `--repeats 2` for the CPU guard.
   Apply the accept rule and write the experiment record, whatever the verdict.
4. To extend the census, `python -m devtools.sqverify_fast_census --binary
   sqverify_fast/target/release/sqverify-fast --out benchmarks/measure-verifier/census
   --threads 2 --resume`, then `--report` to regenerate its table and `--check` to
   confirm every case.
5. Open work is in the beads under `think-gpe0`: `think-tgra` (this loop), `think-4vf7`
   (points and segments), `think-na5a` (a release-build audit with a fault-injection
   control), `think-j1pd` (a reference timing route for `verify.cpp` at any direction).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
