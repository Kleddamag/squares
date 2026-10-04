# Optional Windows owned-Job supervisor

The opt-in [supervisor](../../../devtools/supervise_windows.py) starts an explicit
executable suspended, assigns it to a kill-on-close Windows Job, confirms the owned
root can be measured, then resumes it. It enumerates only that Job, verifies each
opened handle's membership and creation identity, and applies current/observed OS peak
working-set guards to every owned live process. This catches the venv launcher's real
allocating worker, whose memory can be much larger than the launcher.

This standalone layer transfers an adopted local prototype. It changes no default
workflow, CI configuration, dependency or Windows full-validation refusal. Import/help
are portable and load no Windows DLL; execution on non-Windows explicitly refuses
without launching a child. Root independently accepted the migrated tool after lifecycle/FFI review and a fresh small native replay.

The numeric guards retain timeout<=1800s, interval0.1..5s, worker<=16GiB,
review<=12GiB and available physical memory>=8GiB. Smaller memory/time limits are
accepted. A receipt directory must be empty; prior evidence is never overwritten.
Interruptions, monitor failures and guards all reach owned-tree cleanup; a successful
cleanup requires both Job0 and retained process identities signalled exited. Cleanup
failures override the outcome.

## Bounded controls

20focused tests pass in3.64s after a narrow cross-host FFI annotation repair; Ruff and targeted Linux/Windows BasedPyright report no findings. Three actual
Windows controls launch the project venv redirector, allocate96MiB in its real worker
and create a harmless grandchild. Each stays below the128MiB allocation contract and
30s command bound, serial under the immutable outer supervisor's60s/512MiB guard.

| Control status | Job wall seconds | Launcher peak bytes | Actual worker peak bytes | Remaining Job / cleanup |
| --- | ---: | ---: | ---: | --- |
| success | 1.106 | 5517312 | 119164928 | 0 / True |
| timeout | 1.258 | 5517312 | 118910976 | 0 / True |
| worker-memory-stop | 0.278 | 5517312 | 119164928 | 0 / True |

All retained live identities were signalled exited and cleanup errors were empty.
[Small control receipts](receipts/controls.json) omit local paths/argv; the test file
retains the reconstructible worker and exact command. The identity line is flushed
before allocation so a correctly early memory stop cannot race the evidence output.
Linux CI skips the3native controls by declared platform; those skips are not Windows
acceptance. Portable import/help/refusal/guard/evidence controls run on both hosts.

## Use and limits

From `packing/`, choose the project's interpreter and a new output directory:

```powershell
$ProjectPython = (Resolve-Path .venv/Scripts/python.exe).Path
$WorkDirectory = (Get-Location).Path
$OutputDirectory = Join-Path $WorkDirectory 'supervision-output'
& $ProjectPython -m devtools.supervise_windows --cwd $WorkDirectory `
  --output-dir $OutputDirectory --timeout 30 --interval 0.1 `
  --worker-memory-gib 0.5 --review-memory-gib 0.5 -- `
  $ProjectPython -c 'print("bounded supervised command")'
```

`start.json`, `heartbeat.json`, `samples.jsonl`, `stdout.log`, `stderr.log` and
`final.json` retain execution/guard/cleanup evidence. Return0 means success,
124timeout,130interruption,2other failure/guard. The tool has no shell fallback.
Only this owned Job is terminated, even when nested under a separate outer Job.

Observed per-process OS peaks do not form a perfect maximum for the whole tree:
processes starting/exiting between samples can be missed. Shared-page working-set
sums overcount physical memory; Job committed memory is separately labelled. The
per-worker guard is sampled, so it is not an allocation-enforcing kernel limit.
No process outside the owned Job is admitted to measurement or cleanup by PID alone.
Windows-native checks and root safety review govern publication; non-Windows CI alone
cannot establish the FFI/lifecycle behavior. The adopted local P01C supervisor remains
the recovery path. No packing/research result is claimed.

Base main79419cdfc0da0f253f3fbc8dc622fe85c676b8ec; parent3071525d4e03 observed
without a matching WindowsJob mechanism. Session173's separate contract and actual
clocks precede editing; no dependency on the completed PR333 graph diagnostic.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->

The independent80MiB control observed worker119312384B versus launcher5505024B and stopped in0.2769671s. All5retained identities signalled exit; fresh independent OS checks found their PIDs absent. Inner and outer Jobs ended empty with confirmed cleanup/no errors. The deliberate inner guard returns2, so the outer command-failed classification is expected. No additional replay was needed. Hosted exact-head certification remains a separate gate.

Cross-host type checking exposed Linux stubs omitting Windows-only constructor attributes/APIs. The confined repair declares the dynamic native ABI and resolves named ctypes functions only in guarded execution paths; signatures/layout/lifecycle are unchanged. Missing native APIs still fail before child launch. A fresh focused native check passes; prior independent replay remains valid by unchanged ABI/lifecycle and root acceptance.
