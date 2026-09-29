---
title: Validation Parallelism Efficiency Block
date: 2026-09-29
status: in_progress
---
# Validation Parallelism Efficiency Block

**Workflow:** pipeline improvement, efficiency focus.
**Tracking:** `think-xcij` (local allocation) and `think-tddk` (hosted fanout), within
Session 164. The repository owner requested this block while PR 246 completes
certification.

## Problem and Evidence

The published integration checkpoint `5d276119c52b98ac6770b08bc9b1e582746abe02` passed
its local push tier in 856.20 seconds: 51 selected steps, 2,959 passing tests, 6 skips
and 19 deselections.
Pytest took 824.46 seconds for 114 selected test files.
The [retained log](../../../packing/campaign/agent-sessions/session-164-push-final.log)
is a successful operational baseline, not a repeated performance experiment.

The scheduler defaults to as many outer jobs as CPUs.
Pytest receives `max(1, cpus - jobs + 1)` workers, so the default on this ten-CPU host
gave this large proper subset one worker.
Other checks finished while pytest continued serially.
The existing whole-suite fallback gets a different allocation; subset size must not
silently determine whether the host is used.

Simply allowing two outer jobs is insufficient: another exact-verification step can
itself launch nine subprocesses.
The fix must account for nested pools as well as the number of top-level jobs.
Explicit operator resource choices remain authoritative.

The hosted audit identified two critical paths in retained runs: exhaustive tests and
the serial deferred-check job.
Ordinary PR CI already distributes its work over seven roughly balanced jobs.
Further ordinary-PR fanout is not selected without new evidence.

## Parallel Work and Acceptance

Sol owns local scheduling and its behavioral regressions.
A second Sol lane owns hosted scheduling and partition contracts.
A third reviews resource use, unchanged coverage, failure propagation and integration.
The coordinator owns measurements, research-status records and publication.

The local change must give the reachable pytest selection an exclusive CPU allocation
while allowing independent edit checks to retain their existing concurrency.
It must preserve the selected files and marker, propagate failures, respect explicit
resource overrides, and bound nested pools.
Focused regressions must demonstrate these properties on both a single-CPU host and a
multi-CPU host.

The hosted change assigns whole existing tests and whole validation steps to concurrent
jobs. It does not split a mathematical decision into partial claims.
Every job must use one resolved immutable commit.
A contract must reject missing or duplicate assignments, and the final required job must
fail if any necessary job fails, is cancelled, or skips.
Artifact names must be unique.
Existing per-test mathematical assertions and receipts remain intact.

## Measurement Plan

The separate selector-precision slice is `think-6izq`. It may discard comments and known
benign metadata imports as evidence of a repository walk, but must retain marker-bearing
code strings, including strings passed through subprocess aliases or helpers.
It does not attempt temporary-directory dataflow analysis.
Its selected-file changes require their own positive and conservative-fallback tests;
they are not part of a same-selection scheduler comparison.

Before timing, freeze the affected implementation and the exact selected targets.
Use the maintained [timing instrument](../../../packing/benchmarks/validation_timing.py)
for any paired pytest measurements, with raw output and JUnit identities.
Keep temporary outputs and caches on the external scratch volume.
Do not run competing heavy local work during a timing trial; remote CI and lightweight
review can continue.

The first full candidate run is an operational check: require the unchanged workload to
pass and record elapsed time, worker allocation, skips, and collection counts.
Compare it with the retained successful baseline, naming any source or workload
differences. A single observation supports no general speedup estimate.
A repeated performance claim requires the existing
[campaign protocol](../../../packing/benchmarks/validation-efficiency/README.md), with
predeclared matched pairs, identical test identities and nonoverlapping timing ranges.
Do not repeat long serial runs solely to manufacture a percentage when an operational
result and scheduler regression establish the fix.

Hosted acceptance requires every new job and its required aggregator to pass on the
published candidate.
Record individual job durations and the overall critical path; sum of runner time is a
separate cost. Derived initial ceilings are not fresh timing measurements.
Any remaining indivisible long test is an explicit follow-up, not a reason to omit its
assertions.

## Results

The frozen candidate `1afb75ca6` ran the default push tier against `5d276119c`. Changing
a workflow selected the whole non-exhaustive suite: 7,714 tests passed and 9 skipped in
968.77 seconds, using ten pytest workers with `PACK_JOBS=1`. The complete tier took
1,034.70 seconds and failed one documentation check because this review was missing from
the document map. The map is now corrected; the failed
[run log](../../../packing/campaign/agent-sessions/session-164-efficiency-push.log)
retains that omission rather than presenting the run as a passing gate.
The earlier 2,959-test run selected a different workload, so these observations do not
establish a speedup.

The previous published checkpoint `5d276119c` passed required packing and page CI and
the complete
[deferred checkpoint](https://github.com/jlevy/squares/actions/runs/36630574302). Those
results certify the predecessor tree, not the new scheduling implementation.
Hosted execution of the new fanout remains pending.

The local run also exposed an allocation limit: nine workers had drained their queues
while one remained CPU-active.
Its quiet output does not identify the active node.
Retained earlier timings show that the whole-atlas composite test can take 1,327.87
seconds in one call, and its existing per-case pool obeys `PACK_JOBS=1`. `think-14lz`
adds child-pytest timing and live worker receipts; `think-ysvk` gives explicitly
pool-heavy tests a separate, exclusive inner-worker phase while keeping the remaining
tests parallel. Neither follow-up changes the test assertions.
Post-merge and daily workflow parity is implemented and independently reviewed in an
isolated checkout under `think-08ht`; it awaits integration and hosted validation.

The full native external rectangle replay and T-057 complete row-minimum census remain
separate mathematical obligations; changing validation scheduling establishes neither.

### Independent Review

The first local scheduler candidate gave large narrow pushes exclusive pytest workers
without reserving the load marker.
The corrected scheduler reserves it atomically when free and retains the former
conservative allocation while another gate holds it.
It also refuses missing or extra selector-summary lines, preserves explicit worker
settings, keeps edit failures in the ordered report, and releases the marker on
interruption. Its 28 focused tests and clean lint and type checks cover those controls;
an integrated candidate push is still needed to confirm the selected workload and wall.

The separate selector refinement has a narrow coverage claim: it may remove walker
evidence that exists only in comments or in the exact benign
`from importlib.metadata import version` import.
A comparison of the current test roots found precisely two files whose old raw marker
disappears for those reasons.
Review also found dynamic-import attributes, imported helper names, bytes literals, and
helper calls that an initial AST implementation could miss.
The final selector parses and unparses source after removing only the exact benign
metadata-version import, then applies the old marker scan to the executable text.
The 54 focused selector tests, Ruff and BasedPyright passed.
The integrated candidate push still needs to confirm its selected-file receipt.

The hosted fanout resolves one immutable commit before workers start.
Each worker checks its checkout against that commit and writes a tree receipt before
validation. Four jobs divide existing deferred Steps without splitting a Step.
Three exhaustive jobs use a whole-file partition that includes new paths through a
stable hash fallback.
The partition contract covers every discoverable test file, so module, class,
parametrized, inherited, and dynamic marker styles remain eligible.
A collect-only integration check found 60 exhaustive nodes split 2, 30, and 28, with no
duplicates or omissions.
The aggregate tests every prerequisite for success, and artifact names include the job
and attempt.
The final focused workflow, shard and budget suite passed 93 tests with Ruff
and BasedPyright clean.
The separate pending-measurement budget contract passed 55 tests.
The hosted jobs still need to execute on the published candidate.

New hosted ceilings are derived from predecessor Step or JUnit times plus setup.
Their measured-wall fields remain null with `pending_measurement: think-tddk`; the first
hosted run must record observed walls and clear that state.
Artifact upload remains advisory and may warn without failing a passing validation job;
the in-job checkout equality test is fail-closed.
For a manual pull-request dispatch, GitHub’s event SHA names the dispatch ref while
workers validate the resolved merge SHA. The tree receipt and custom validated-SHA field
in exhaustive per-file reports name the latter.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
