# Windows owned-Job supervision

`python -m devtools.supervise_windows` is an opt-in, standard-library subprocess tool.
It starts an explicit executable suspended, assigns it to its own kill-on-close Job,
checks measurement, and resumes it.
Only that Job’s members are measured or terminated.
Import and help work on other hosts; execution outside Windows refuses before launch.
It has no code dependency on the n17 diagnostics or their PR stack.

## Outcomes

`final.json`’s `status` is the outcome, and the CLI exit code follows from it:

| `status` | Exit | Meaning |
| --- | ---: | --- |
| `success` | 0 | The root exited zero and no owned descendant was still running |
| `success-with-cleanup` | 0 | The root exited zero, and owned descendants still running were terminated |
| `timeout` | 124 | The timeout elapsed and the owned tree was terminated |
| `interrupted` | 130 | The supervisor was interrupted and the owned tree was terminated |
| `command-failed` | 2 | The root exited nonzero |
| `worker-memory-stop` | 2 | An owned process reached the hard stop |
| `system-memory-stop` | 2 | Available physical memory fell below the floor while running |
| `guard-refused-system-memory` | 2 | Available physical memory was below the floor at start |
| `worker-measurement-failed` | 2 | Owned processes went unmeasured for three consecutive samples |
| `cleanup-failed` | 2 | Any cleanup error, which overrides every other outcome |
| `technical-failure` | 2 | Any other error |

**Exit 0 does not mean every descendant finished its work.** `success-with-cleanup` says
that some were terminated when the root exited.
`root_status`, `root_exited_before_cleanup`, `live_descendants_before_cleanup`,
`descendants_termination_requested` and `tree_cleanup_confirmed` give the detail.
The request field records the cleanup action, not proof that termination caused each
individual exit; unavailable cleanup observations remain null.
If root reaping fails, `root_status` is `exit-unconfirmed` rather than claiming an exit.

## Use

From `packing/`, select the project’s Python 3.14 interpreter and a new receipt
directory:

```powershell
$SupervisorPython = (Resolve-Path .venv/Scripts/python.exe).Path
$SupervisorDirectory = (Get-Location).Path
$SupervisorOutput = Join-Path $SupervisorDirectory 'new-supervision-output'
& $SupervisorPython -m devtools.supervise_windows --cwd $SupervisorDirectory `
  --output-dir $SupervisorOutput --timeout 30 --interval 0.1 `
  --worker-memory-gib 0.25 --review-memory-gib 0.125 --min-available-gib 0.25 -- `
  $SupervisorPython -c 'print("bounded supervised command")'
```

The executable must be an existing absolute path; arguments are passed directly with no
shell fallback. The output directory must be empty, so prior evidence is preserved.
`start.json`, `heartbeat.json`, `samples.jsonl`, `stdout.log`, `stderr.log` and
`final.json` contain execution, guard and cleanup evidence.

## Memory guards

Three guards, each a named default in `supervise_windows.py` that the command line can
change:

| Guard | Option | Default | Action |
| --- | --- | ---: | --- |
| Hard stop | `--worker-memory-gib` | 16 GiB | Terminates the owned tree when one owned process reaches it |
| Review mark | `--review-memory-gib` | 12 GiB | Recorded and warned about the first time one owned process reaches it; the run continues |
| Host floor | `--min-available-gib` | 8 GiB | Refuses to start below it, and stops the run once available memory falls below it |

The review mark sits below the hard stop, so a growing worker meets the mark first and
the stop afterwards, and both are reachable at the defaults.
The receipt records the mark in `worker_memory_review_crossed` and
`worker_memory_review_trigger`, with the time and the workers that reached it, and the
supervisor prints a warning on its own stderr.
A review mark at or above the hard stop is accepted with a warning, since it can then
only be recorded on the sample that stops the tree.

The defaults suit a large developer workstation and are not host policy.
Worker thresholds accept any finite positive value, and the floor any finite value of
zero or more. A floor below the 8 GiB default is accepted with a warning, printed and
kept in the receipt’s `guard_warnings`, because the host can then page or run out of
memory before the supervisor acts.
Lowering it does not relax a separate outer supervisor’s policy.

Both worker thresholds judge each live owned process by the larger of its current and OS
peak working set, the venv redirector’s real worker included.
They are sampled guards, not kernel allocation quotas.

Receipts carry `schema: packing.windows-supervisor.v2`. Version 1 receipts, the ones
retained from Session 173, predate Review A: there the review threshold also stopped the
run, under `worker_memory_review_stop_bytes` and the status `worker-memory-review`, and
root success with terminated descendants was reported as `success`.

## Native gate and platform boundary

The `Windows supervision` workflow runs exactly three native normal, timeout and memory
cases on `windows-latest` and refuses a skipped result.
`normal` crosses an 80 MiB review mark and finishes as `success-with-cleanup`; `memory`
reaches an 80 MiB hard stop.
Each worker allocates 96 MiB, below the 128 MiB test contract, with a harmless
grandchild and a subprocess timeout of 30 seconds.
Tests use an explicit 0.25 GiB available floor for small CI hosts.
Portable import, help, refusal, parser, guard and status controls run in the regular
suite, along with a contract test on the workflow itself.

The workflow runs on pull requests and pushes to `main` that touch the supervisor, its
test, the workflow or the locked interpreter and dependencies, and on demand.
It is not part of `packing-required`, and `devtools/gate-budgets.yaml` does not clock
it: registering a workflow there takes an aggregator, a wall-check step and recorded
samples, which is far more than one job that measured 55 seconds cold.
Its ceiling is `timeout-minutes: 5`, which the contract test holds.
The full packing-validation runner’s Windows refusal is unchanged.

This gate covers this supervisor, not every Windows branch of unrelated helpers.
Native behaviour relies on two interfaces outside the documented surface:

- **CPython’s private `Popen._handle`.** `subprocess` exposes no public process handle
  on Windows, and the suspended root has to be assigned and resumed through one.
- **ntdll’s undocumented `NtResumeProcess`.** The documented `ResumeThread` needs the
  primary thread’s handle, which `subprocess` closes without returning.

Other Python implementations are not supported.
A missing native API fails before child launch.
The ABI, suspended assignment, owned membership and cleanup protocol are unchanged by
Review A.

Each opened process handle is checked for owned-Job membership and creation identity.
Successful cleanup needs an empty Job and signalled retained handles, including under a
separate outer Job. Processes that start and exit between samples can be missed, so
observed peaks are not a perfect whole-tree RSS maximum.
Working-set sums overcount shared pages; Job committed memory is separately labelled.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
