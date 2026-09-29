import sys
sys.path.insert(0, '/home/user/squares-docs/packing/src')
from sqpack.yamlio import safe_load
from pathlib import Path
root = Path('/home/user/squares-docs/packing/frontier')
def fm(p):
    t = p.read_text()
    return safe_load(t[4:t.index('\n---', 4)])
for p in sorted(root.glob('n-*.md')):
    d = fm(p)['packing']
    n = d['n']
    rl = d.get('reported_lower_bound') or {}
    vl = d.get('verified_lower_bound') or {}
    ev = d.get('evidence') or []
    interesting = [e for e in ev if any(k in e for k in ('wand125','tokoharu','evand','kleddamag','guzhou','mira','massaccesi'))]
    rle = rl.get('evidence') or []
    vle = vl.get('evidence') or []
    if interesting or any('wand125' in e or 'tokoharu' in e or 'evand' in e or 'kleddamag' in e or 'guzhou' in e for e in rle+vle):
        print(f"n={n}: RL {rl.get('value')} [{rl.get('exact_form')}] src={rl.get('source_key')} ev={rle} by={rl.get('proved_by')}")
        print(f"      VL {vl.get('value')} [{vl.get('exact_form')}] ev={vle}")
        print(f"      case-ev-interesting={interesting}")
