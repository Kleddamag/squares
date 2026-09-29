Replay of wand125 certificates/mixed_n50_L740 (s(50) >= 37/5): NOT RUN.

Completed:
- Sparse clone of https://github.com/wand125/square-packing-bounds at
  39d8ecc74d651b54ec977c331c8f2015b442a6c4; HEAD^{tree} verified as
  936e2524c09ca137cf9e02dcd955d6737549253b.
- n50-L7.40-proof-bundle.tar.gz SHA-256 verified:
  90621d1a7ceb27267ef7b4bf3ffb5906f50e259ac28c955ec6679e64c604638f.
- Host facts recorded in host.txt.

Failed at step 1 (environment setup), before unpacking:
- `python3 -m venv /tmp/n50-venv && pip install -r requirements.txt` (requirements: `numpy`,
  unpinned) was refused by this session's auto-mode permission classifier
  ("Code from External"). The session is not permitted to install packages for, or execute,
  code fetched from the external repository without an explicit user permission rule.
- Consequently not done: bundle unpack, files-sha256.json validation (621 files), the
  checker run, the comparison, and every receipt that depends on them.

Note for the rerun: the upstream README's Reproduce command uses `--workers 3`, not 4:
  tar xzf n50-L7.40-proof-bundle.tar.gz && cd n50-L7.40-proof-bundle
  OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 code/verify_mixed_full_proof.py proof --workers 3
requirements.txt is the single unpinned line `numpy`, so a pip freeze is the only version record.

To unblock: add a Bash permission rule allowing pip install into /tmp/n50-venv and execution
of the upstream checker (python3 code/verify_mixed_full_proof.py, which compiles
code/mixed_rotated_verify.cpp with c++), or run the replay on a host where that is allowed.
