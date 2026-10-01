#!/usr/bin/env bash
# Run from packing/. One immutable n17 source, one fresh output directory.
set -eu
if [ "$#" -ne 1 ] || [ -e "$1" ]; then
  echo 'Usage: bash replay.sh FRESH_OUTPUT_DIRECTORY (from packing/)' >&2
  exit 2
fi
: "${TMPDIR:?Set external scratch TMPDIR}"
: "${CARGO_TARGET_DIR:?Set task CARGO_TARGET_DIR}"
: "${UV_CACHE_DIR:?Set task UV_CACHE_DIR}"
test -w "$TMPDIR"
export PYTHONDONTWRITEBYTECODE=1
unset PYTHONOPTIMIZE
ulimit -d 1048576
ulimit -f 20480
output=$1
mkdir -p "$output"
source_dir=resources/web/n17-kleddamag-certified-bound-2026-09-21/kleddamag-17-squares-certified-bound
source_json=$source_dir/upper-packing-certificate.json
expected_side=4675530093604551/1000000000000000
printf '%s  %s\n' 24e296f5995abc9424e2d8d39ea0a8e44953b919430a04f006fa84c56fef45f7 "$source_json" | shasum -a 256 -c - > "$output/source-integrity.log"
{
  date -u '+started_at=%Y-%m-%dT%H:%M:%SZ'
  git rev-parse HEAD
  git status --short
  .venv/bin/python3 -c 'import sys; print(sys.version); assert __debug__ and not sys.flags.optimize'
  uptime
  printf 'workers=1\ncommand_timeout_seconds=90\nheap_limit_kib=1048576\nfile_limit_blocks=20480\n'
} > "$output/provenance.log"
printf 'step\texit\texpected\n' > "$output/exits.tsv"
run() {
  label=$1
  expected=$2
  shift 2
  printf '%q ' "$@" >> "$output/commands.log"
  printf '\n' >> "$output/commands.log"
  set +e
  /usr/bin/time -l gtimeout --signal=TERM --kill-after=5s 90s "$@" > "$output/$label.stdout" 2> "$output/$label.stderr"
  result=$?
  set -e
  printf '%s\t%s\t%s\n' "$label" "$result" "$expected" >> "$output/exits.tsv"
  if [ "$result" -ne "$expected" ]; then
    printf 'Refused at %s: exit %s, expected %s\n' "$label" "$result" "$expected" >&2
    exit 1
  fi
}
run grid-main 0 .venv/bin/python3 -m sqpack.cli.witness verify witnesses/grid-n004.yaml --json
run grid-independent 0 .venv/bin/python3 -m devtools.check_rational_witness_independent witnesses/grid-n004.yaml
run overlap-main 1 .venv/bin/python3 -m sqpack.cli.witness verify witnesses/overlap-negative-control.yaml --json
run overlap-independent 1 .venv/bin/python3 -m devtools.check_rational_witness_independent witnesses/overlap-negative-control.yaml
run conversion 0 .venv/bin/python3 -m devtools.import_half_angle_witness "$source_json" --expected-n 17 --expected-side "$expected_side" --output "$output/witness.yaml"
run target-main 0 .venv/bin/python3 -m sqpack.cli.witness verify "$output/witness.yaml" --json
run target-independent 0 .venv/bin/python3 -m devtools.check_rational_witness_independent "$output/witness.yaml"
run target-source 0 .venv/bin/python3 "$source_dir/verify_upper.py" "$source_json"
date -u '+finished_at=%Y-%m-%dT%H:%M:%SZ' >> "$output/provenance.log"
echo 'All fixed commands returned the expected statuses; review counts, side and complete outputs before acceptance.'
