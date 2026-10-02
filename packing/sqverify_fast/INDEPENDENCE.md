# Independence Record for sqverify-fast

This is the clean-room record that lets this crate count as an independent
implementation of the measure-capture verifier: every file read, every command run, and
every outside reference consulted while writing it, kept as the work went.
The bead is `think-gpe0` (lane W2), with milestones `think-d69e` (soundness and
Milestone A), `think-tgra` (performance loop) and `think-4vf7` (points and segments).

## The Rule

Never opened, grepped, diffed or copied: any `verify*.cpp`, `mixed_rotated_verify.cpp`,
`unified_linear_verify.cpp`, `zmx2.rs`, `zm_mixed.py`, `zeromargin.py`, `qx2_zm.py`, any
`code/` directory under `packing/resources/web/`, and the checker-driving internals of
`packing/devtools/audit_wand125_*.py` and `replay_evand_zmx2.py`. The authors’ checkers
were run only as black boxes, for timing, through the repository’s replay command.

## Files Read

Repository instructions and conventions:

- `AGENTS.md`, `operating-rules.md`, `development.md` (supported environment, tiers,
  performance work), and the `experiment-loop` skill with its `contract.md` and asset
  headers.

Mathematics (reviews under `docs/project/reviews/`):

- `review-2026-09-27-wand125-rectangle-scaling.md`, in full.
  Its sections on fixed-width types, floating-point constants and hard limits describe
  `verify.cpp`’s constants, limits and some line numbers in prose; they were read before
  that was apparent. Nothing in this crate uses them: its arithmetic (directed rounding
  per operation, rational enclosure by exact comparison), its bounds (concave-section
  trapezoids, edge-length enclosures from nine affine terms, classification with slack)
  and its limits are its own, derived in `SOUNDNESS.md`.
- `review-2026-09-22-tokoharu-density-mathematics.md`, lines 1–194 and 225–318: the
  mathematical reduction, the net and shrink argument, the quarter-turn reduction, the
  axis-grid argument, the derivative formula and mean-value bound, optional smoothing
  and the preconditions.
  The section “Inscribed-polygon area and arithmetic” (lines 195–224), which describes
  the checker’s area routine, was skipped.

Lane W1’s clean outputs, checked out from its branch `worktree-agent-a9b6885d64664dd01`
at the coordinator’s instruction (these two files only; the research note, the
`attribution/` folder and the profiling script on that branch were never opened):

- `docs/project/specs/active/plan-2026-10-02-independent-measure-verifier.md`, the
  specification.
- `packing/benchmarks/results/author-checker-profile-2026-10-02/timings.json`, the
  authors’ checkers’ black-box CPU timings.

First-party code of this repository:

- `packing/src/sqpack/rectangle_density.py`, in full: the candidate format
  (`[left, bottom, right, top]`, decimal tokens as exact rationals, `rhs`, `certificate`
  metadata), the D4 images, and the exact oracle used by the differential tests.
- `packing/sqverify_exact/Cargo.toml`, `rust-toolchain.toml`, `clippy.toml` (the
  toolchain pin and lint floor were copied), and the step functions `_rust_quality` and
  `_rust_exact_geometry` and the step registry of `packing/src/sqpack/cli/validate.py`,
  with the cache steps of `.github/workflows/packing-validation.yml`, to wire this crate
  the same way.
- `packing/benchmarks/bench_rectangle_rust_verifier_ab.py` (header only) and
  `packing/benchmarks/math-startup/` (README, ledger head, one hypothesis) for this
  repository’s benchmark conventions.

Certificate data and summaries (packets under `packing/resources/web/`):

- `wand125-rectangle-certificates-2026-09-27/README.md` (lines 1–150) and
  `wand125-rectangle-certificates-2026-10-01/README.md` (lines 1–80).
- `certified_candidate.json.gz`, `certificate_metadata.json`,
  `verification_summary.json` and `verified_angles.jsonl` of `rect_n32_L595` and
  `rect_n78_L8955`, and the candidate files of every certificate verified in Milestone
  A.
- `receipts/replay/audit.json` of the 27 and 28 September packets (case list, status,
  counts and timings only) and `receipts/controls/rect_n41_L676.json` of the 1 October
  packet (mutation descriptions and witness).

## Commands Run

- `python -m devtools.check_bootstrap`, `git submodule update --init --recursive`,
  `npm ci --ignore-scripts`, `uv sync --frozen --all-extras --group dev` (fresh-clone
  setup).
- `python -m devtools.audit_wand125_rectangles --help` (the command-line help text only,
  to learn the replay command’s options).
- `python -m devtools.audit_wand125_rectangles --packet 2026-09-27 --control --n 32
  --direction 1 --out …` and, through `benchmarks/bench_measure_verifier.py`, the same
  command for other certificates and directions: black-box timing of the unchanged
  `verify.cpp`. The tool’s receipts were read for CPU seconds, node counts and verdicts.
- `python -m devtools.audit_wand125_rectangles --packet 2026-09-27 --n 32 --replay
  --workers 1 --out …`, through the harness’s `--whole` mode: a black-box replay of
  every direction of one certificate, for whole-certificate CPU. Only the tool’s
  receipts (status, per-direction rows) were read; the process list showed the checker
  binary’s name and arguments (`./verify R R`), nothing of its source.
- `cargo build`, `cargo test`, `cargo clippy`, `valgrind --tool=callgrind` and
  `callgrind_annotate` on this crate only.
- `packing-validate --edit` and `--only` on this worktree.

The census reads, from the replay receipts, only the authors’ summary fields (status,
node total, least printed bound, wall seconds and the worker count in the recorded
command), to set them beside this verifier’s results.

## Outside References

None beyond the reviews above: the IEEE 754 round-to-nearest model, the Brunn–Minkowski
concavity of sections of convex sets, and Fubini’s theorem are standard.
Lemma I1’s branch-free step is the textbook bound that no gap between adjacent binary64
values exceeds $2^{-52}|x|$, applied directly; no source was consulted for it.
No web source, paper or other implementation was consulted.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
