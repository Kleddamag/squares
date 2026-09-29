import sys
sys.path.insert(0, '/home/user/squares-docs/packing/src')
from sqpack.yamlio import safe_load
from pathlib import Path
root = Path('/home/user/squares-docs/packing/frontier')
def fm(p):
    t = p.read_text(); return safe_load(t[4:t.index('\n---', 4)])
RECT = {'E-wand125-rectangle-report','E-wand125-rectangle-monotone-report','E-wand125-rectangle-2026-09-28-report','E-wand125-rectangle-2026-09-28-monotone-report'}
out=[]
for p in sorted(root.glob('n-*.md')):
    d = fm(p)['packing']
    rl = d.get('reported_lower_bound') or {}
    if set(rl.get('evidence') or []) & RECT:
        out.append((d['n'], rl.get('exact_form'), rl['evidence'][0].replace('E-wand125-rectangle-','')))
print(len(out))
print(', '.join(f"{n}: {v}" for n,v,e in out))
for n,v,e in out: print(n,v,e)
