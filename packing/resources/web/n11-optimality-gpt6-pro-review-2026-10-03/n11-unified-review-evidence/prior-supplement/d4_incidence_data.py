"""Load pinned cover/overlay inputs for the independent D4 incidence proof.
Distance-ban data is intentionally not a dependency of the incidence certificate.
"""
from pathlib import Path
import hashlib
import itertools
import json

if not __debug__:
    raise RuntimeError('This mathematical checker refuses optimized Python (-O/-OO).')

ROOT = Path(__file__).resolve().parent / 'squares/packing/resources/web/n11-optimality-2026-09-29/receipts/d4-independent/objects'
INPUT_SHA256 = {
    'cover': 'df7938d9ba27095a38fabe45f8b26b259a2cc896c2ae4aac6bae874f417adc4e',
    'overlay': '845b5f748843dd60fa7e290a5ea1a304da4e439ae229bd73a841aec816f4e700',
}
VIEW_CONVENTION = ['(x,y)', '(1-x,y)', '(1-y,x)', '(y,x)']
CAP_U = '387708359002281417731/100000000000000000000'

def require(condition, message):
    if not condition:
        raise ValueError(message)

def load_bound(role):
    sha = INPUT_SHA256[role]
    raw = (ROOT / (sha + '.json')).read_bytes()
    require(hashlib.sha256(raw).hexdigest() == sha, role + ' input hash mismatch')
    return json.loads(raw)

COVER = load_bound('cover')
OVERLAY = load_bound('overlay')
require(OVERLAY['cover_sha256'] == INPUT_SHA256['cover'], 'overlay parent binding')
require(OVERLAY['symmetries'] == [[0,1,1],[0,-1,1],[1,-1,1],[1,1,1]], 'view convention')
RAW = tuple(itertools.combinations(range(16), 11))
MASKS = tuple(sorted({min(m, tuple(sorted(15-j for j in m))) for m in RAW}))
require(len(RAW) == 4368 and len(MASKS) == 2184, 'mask cardinalities')
require(COVER['all_eleven_cell_subsets'] == [list(m) for m in RAW], 'raw mask inventory')
require(COVER['canonical_eleven_cell_subsets'] == [list(m) for m in MASKS], 'canonical mask inventory')
REGIONS = OVERLAY['regions']
require(type(REGIONS) is list and len(REGIONS) == 220, 'overlay inventory length')
for index, row in enumerate(REGIONS):
    require(type(row) is dict and type(row['index']) is int and row['index'] == index, 'region ordinal')
    require(type(row['labels']) is list and len(row['labels']) == 4 and all(type(x) is int and 0 <= x < 16 for x in row['labels']), 'four-view label grammar')
LABELS = tuple(tuple(r['labels']) for r in REGIONS)
require(len(set(LABELS)) == len(LABELS), 'duplicate overlay labels')
LABEL_SHA256 = hashlib.sha256(json.dumps([list(row) for row in LABELS], separators=(',', ':')).encode()).hexdigest()
CASE_IDS = (999, 1462, 1659)
TARGETS = tuple(sorted({MASKS[i] for i in CASE_IDS} | {tuple(sorted(15-j for j in MASKS[i])) for i in CASE_IDS}))
require(len(TARGETS) == 6, 'target mask count')
require(MASKS[999] == (0,1,2,4,6,7,9,10,12,14,15), 'source 999 convention')
require(MASKS[1462] == (0,1,3,5,6,8,9,11,12,13,14), 'source 1462 convention')
require(MASKS[1659] == (0,2,3,4,5,6,7,11,12,13,14), 'source 1659 convention')
