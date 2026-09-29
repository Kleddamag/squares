# Recorded verification runs

`split-replay.json` records the fresh six-worker Intel frontier replay and exact
assembly with the local root and sieve replays. All six workers exited zero.
`split-linkage.json.gz` is the byte-preserved complete assembly record, including
source hashes and output bindings. Its decompressed SHA256 is recorded in the
summary. Absolute paths identify historical run outputs; the reproducer creates
new paths and new output bindings on the reader's machine.

The prefix comparison records show exact proof-object agreement with the earlier
run. The distribution records describe byte-preserving copying and an actual
archive extraction with all input hashes checked. These packaging records do
not perform mathematical verification.

`m1-full-replay.json` records the successful one-command M1 run: four numerical
processes exited zero, and full assembly accepted all required regions in
8,577.313 seconds with two frontier workers. `m1-full-linkage.json.gz` retains
the complete linkage record without changing its decompressed bytes.
`m1-collection-check.json` records verification of all 45,446 output bindings
and 75,130 source inputs after transfer.

`m1-distribution-binding.json` checks that every actual input read by that run
is present byte-for-byte in the trimmed distribution. The numerical run used
the original frozen bundle; packaging and extraction were checked separately.
The compressed/decompressed linkage SHA256 values are in this binding record.
Historical absolute paths identify the original run and are not required paths
for reproduction.
Use `verify_portable.py` for a fresh complete numerical check; do not treat these
historical JSON records as a substitute for executing the checker.
