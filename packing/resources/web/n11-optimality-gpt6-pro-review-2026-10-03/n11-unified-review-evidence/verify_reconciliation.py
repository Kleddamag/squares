#!/usr/bin/env python3
"""Verify new reconciliation checks only; no end-to-end global proof replay."""
if not __debug__:
    raise RuntimeError("This mathematical checker refuses Python -O/-OO.")

import argparse
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys
import time

BASE = Path(__file__).resolve().parent
MANIFEST = BASE / 'manifest.json'
MANIFEST_PIN = BASE / 'manifest.sha256'
sys.dont_write_bytecode = True


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_files():
    expected_manifest = MANIFEST_PIN.read_text().strip()
    require(len(expected_manifest) == 64 and sha(MANIFEST) == expected_manifest, 'Manifest SHA-256 mismatch')
    manifest = json.loads(MANIFEST.read_text())
    require(manifest['schema'] == 'n11-unified-review-evidence-v1', 'Unsupported manifest')
    expected = set()
    for row in manifest['files']:
        rel = row['path']
        path = PurePosixPath(rel)
        require(isinstance(rel, str) and '\\' not in rel and path.parts and not path.is_absolute() and '..' not in path.parts, 'Invalid manifest path')
        require(path.parts[0] != 'fresh-results' and rel not in expected, 'Duplicate or mutable input listed')
        expected.add(rel)
        p = BASE / path
        require(p.is_file() and not p.is_symlink(), 'Missing/nonregular input: ' + rel)
        require(p.stat().st_size == row['bytes'] and sha(p) == row['sha256'], 'Input identity mismatch: ' + rel)
    actual = {p.relative_to(BASE).as_posix() for p in BASE.rglob('*') if p.is_file()
              and p.relative_to(BASE).parts[0] != 'fresh-results' and '__pycache__' not in p.relative_to(BASE).parts
              and p.relative_to(BASE).as_posix() not in {'manifest.json', 'manifest.sha256'}}
    require(actual == expected, 'Immutable file inventory differs')
    require({'verify_reconciliation.py', 'requirements.txt', 'source-reviews/report-A.md', 'source-reviews/report-B.md'} <= expected, 'Required top-level inputs missing')
    return manifest, expected_manifest


def compare_json(fresh, recorded, ignore_seconds=False):
    a, b = json.loads(fresh.read_text()), json.loads(recorded.read_text())
    if ignore_seconds:
        a.pop('seconds', None)
        b.pop('seconds', None)
    require(a == b, 'Exact recorded-result comparison failed: ' + fresh.name)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--hashes-only', action='store_true', help='Verify file identities only; no mathematics is executed')
    args = parser.parse_args()
    os.chdir(BASE)
    started = time.monotonic()
    manifest, manifest_sha = check_files()
    print(f"Checked {len(manifest['files'])} immutable file identities.", flush=True)
    if args.hashes_only:
        print('PASS_HASHES_ONLY; no mathematical checks performed.')
        return 0
    require(sys.version_info >= (3, 12), 'Use Python 3.12 or newer; Python 3.12 was tested')
    packages = {name: importlib.metadata.version(name) for name in ('numpy', 'scipy', 'sympy', 'mpmath')}
    output = BASE / 'fresh-results'
    logs = output / 'logs'
    logs.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    env['ELEVEN_RATIONAL_BACKEND'] = 'fraction'
    env['PYTHONPATH'] = str(BASE / 'squares/packing') + (os.pathsep + env['PYTHONPATH'] if env.get('PYTHONPATH') else '')
    for name in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS'):
        env[name] = '1'
    stages = []
    def run(name, script, arguments=(), json_stdout=False):
        print('Running ' + name + ' ...', flush=True)
        begin = time.monotonic()
        result = subprocess.run([sys.executable, '-B', str(BASE / script), *map(str, arguments)], cwd=BASE, env=env, text=True, capture_output=True)
        (logs / (name + '.stdout.txt')).write_text(result.stdout)
        (logs / (name + '.stderr.txt')).write_text(result.stderr)
        require(result.returncode == 0, f'{name} failed; see fresh-results/logs')
        if json_stdout:
            json.loads(result.stdout)
            target = output / (script.removesuffix('.py') + '.json')
            target.write_text(result.stdout)
            compare_json(target, BASE / 'recorded-results' / target.name)
        stages.append({'stage': name, 'exit_code': result.returncode, 'seconds': time.monotonic() - begin})
        print('PASS ' + name, flush=True)
    run('coverage-controls', 'reconciliation-coverage-check.py', json_stdout=True)
    run('publisher-coverage-controls', 'reconciliation-original-coverage-check.py', json_stdout=True)
    run('local-reconciliation', 'reconciliation_local_checks.py', (
        '--bundle', BASE / 'prior-supplement', '--review-a', BASE / 'source-reviews/report-A.md', '--output-dir', output / 'local'))
    compare_json(output / 'local/reconciliation-local-check-results.json', BASE / 'recorded-results/reconciliation-local-check-results.json', ignore_seconds=True)
    compare_json(output / 'local/reconciliation-local-canonical-rows.json', BASE / 'recorded-results/reconciliation-local-canonical-rows.json')
    _, ending_manifest_sha = check_files()
    require(ending_manifest_sha == manifest_sha, 'Manifest changed during execution')
    summary = {
        'status': 'PASS_NEW_RECONCILIATION_CHECKS',
        'scope': 'Small exact boundary/coverage controls and B retained-dual local reconciliation only. Review A new dual vectors were not supplied and are not verified.',
        'whole_global_proof_replayed': False, 'global_optimality_proved': False,
        'field_geometry_rerun': False, 'capture_graph_replayed': False,
        'prior_eleven_stage_driver_run': False, 'd4_trace_regenerated': False,
        'all_recorded_comparisons_exact_except_local_seconds': True,
        'prior_source_and_receipt_bytes_unchanged': True,
        'manifest_sha256': manifest_sha, 'immutable_files_checked': len(manifest['files']),
        'dependency_versions': packages, 'stages': stages, 'seconds': time.monotonic() - started,
    }
    (output / 'verification-summary.json').write_text(json.dumps(summary, indent=2, sort_keys=True) + '\n')
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError, OSError, KeyError, importlib.metadata.PackageNotFoundError) as error:
        print('REFUSED: ' + str(error), file=sys.stderr)
        raise SystemExit(2)
