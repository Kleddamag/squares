# Windows owned-Job supervision

`python -m devtools.supervise_windows` is an opt-in, standard-library subprocess tool.
It starts an explicit executable suspended, assigns it to its own kill-on-close Job,
checks measurement, and resumes it.
Only that Job’s members are measured or terminated.
Import and help work on other hosts; execution outside Windows refuses before launch.
It has no code dependency on the n17 diagnostics or their PR stack.

**Exit 0 means the root exited zero and owned-tree cleanup succeeded.
It does not mean all descendants completed their work.** Live descendants are forcibly
terminated when the root exits.
Read `root_status`, `root_exited_before_cleanup`, `live_descendants_before_cleanup`,
`descendants_termination_requested` and `tree_cleanup_confirmed` together.
The request field records the cleanup action, not proof that termination caused each
individual exit; unavailable cleanup observations remain null.
Cleanup errors override success.
If root reaping fails, `root_status` is `exit-unconfirmed`, rather than claiming exit.

## Use

From `packing/`, select the project’s Python 3.14 interpreter and a new receipt
directory:

```powershell
$SupervisorPython = (Resolve-Path .venv/Scripts/python.exe).Path
$SupervisorDirectory = (Get-Location).Path
$SupervisorOutput = Join-Path $SupervisorDirectory 'new-supervision-output'
& $SupervisorPython -m devtools.supervise_windows --cwd $SupervisorDirectory `
  --output-dir $SupervisorOutput --timeout 30 --interval 0.1 `
  --worker-memory-gib 0.25 --review-memory-gib 0.25 --min-available-gib 0.25 -- `
  $SupervisorPython -c 'print("bounded supervised command")'
```

The executable must be an existing absolute path; arguments are passed directly with no
shell fallback. The output directory must be empty, so prior evidence is preserved.
`start.json`, `heartbeat.json`, `samples.jsonl`, `stdout.log`, `stderr.log` and
`final.json` contain execution, guard and cleanup evidence.
CLI exit codes are 0 for root success with cleanup, 124 for timeout, 130 for
interruption and 2 for other stops.

## Limits and precedence

Timeout is finite and in `(0, 1800]` seconds; sample interval is in `[0.1, 5]` seconds.
Worker and review thresholds accept any finite positive GiB value.
Available physical memory accepts a finite floor of zero or more.
Defaults remain worker 16 GiB, review 12 GiB and available 8 GiB; these are conservative
defaults, not universal host policy.
Choosing a lower available floor does not relax a separate outer supervisor’s policy.

The smaller worker/review threshold is the effective early stop.
By default review at 12 GiB normally precedes hard stop at 16 GiB. If one sample crosses
both, the hard stop label wins.
A review threshold at or above the hard threshold cannot preempt it.
Both worker limits apply to each live owned process’s current or observed OS peak
working set, including the venv redirector’s real worker.
They are sampled guards, not kernel allocation quotas.

## Native gate and platform boundary

The `Windows supervision` workflow runs exactly three native normal/timeout/memory
controls on `windows-latest` and refuses skipped-only results.
Each worker allocates 96 MiB, below the 128 MiB test contract, with a harmless
grandchild and a subprocess timeout of 30 seconds.
Tests use an explicit 0.25 GiB available floor for small CI hosts.
Portable import/help/refusal/parser/IO controls also run in the regular suite.
The full packing-validation runner’s Windows refusal is unchanged.

This gate covers this supervisor, not every Windows branch of unrelated helpers.
Native behavior requires CPython’s private `Popen._handle` and the undocumented
`NtResumeProcess`; this implementation does not promise other Python implementations or
replacement Windows APIs.
Missing native APIs fail before child launch.
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
