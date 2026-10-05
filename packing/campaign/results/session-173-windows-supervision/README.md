# Session 173: Windows owned-Job supervision

This retained session transferred a local Windows supervisor into a standalone, opt-in
devtool. The maintained interface, policy and platform limitations are in
[Windows owned-Job supervision](../../../devtools/windows-supervision.md).
This record describes the original measurement, rather than current usage policy.

The original 20 focused tests passed in 3.64 seconds after a narrow cross-host FFI
annotation repair.
Three native controls used a venv launcher, a 96 MiB allocating worker
and a harmless grandchild.
Each stayed below the 128 MiB allocation contract and 30 second command bound.
Linux declared three native skips; those skips were not Windows acceptance.

| Historical control | Job wall seconds | Launcher peak bytes | Actual worker peak bytes | Remaining Job / cleanup |
| --- | ---: | ---: | ---: | --- |
| success | 1.106 | 5517312 | 119164928 | 0 / True |
| timeout | 1.258 | 5517312 | 118910976 | 0 / True |
| worker-memory-stop | 0.278 | 5517312 | 119164928 | 0 / True |

[Retained control summaries](receipts/controls.json) omit local paths and argv.
They are `packing.windows-supervisor.v1` receipts, from before Review A, when the review
threshold also stopped the run; the guide says what version 2 changed.
All retained live identities were signalled exited and cleanup errors were empty.
An independent 80 MiB guard observed a 119312384 byte worker versus a 5505024 byte
launcher, stopping in 0.2769671 seconds.
Five retained identities signalled exit; independent OS checks found their PIDs absent.
Both nested Jobs ended empty with confirmed cleanup.
The deliberate inner guard returned 2, so the outer command-failed classification was
expected.

The original source/evidence head `130d693d8e4e888efc0346ae007073abb4d696d8` and
metadata head `8896be292f8b3ac14744ad2658fdd78a8a258c70` each had 19 passing checks, 36
declared skips and successful required jobs.
These are historical certifications, not certification of later maintenance changes.
The recorded session clocks and native task-tree lower bound remain unchanged.

The initial base was main `79419cdfc0da0f253f3fbc8dc622fe85c676b8ec`; parent PR307
`1525d4e03` had no matching Windows Job mechanism.
This tool has no code dependency on the PR333 diagnostics.
No packing or mathematical result is claimed.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
