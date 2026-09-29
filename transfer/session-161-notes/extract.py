import yaml, glob, re, sys
from pathlib import Path
rows=[]
for p in sorted(glob.glob('frontier/n-*.md')):
    t=Path(p).read_text()
    m=re.match(r'^---\n(.*?)\n---\n', t, re.S)
    d=yaml.safe_load(m.group(1))['packing']
    n=d['n']
    rl=d.get('reported_lower_bound') or {}
    vl=d.get('verified_lower_bound') or {}
    ru=d.get('reported_upper_bound') or {}
    vu=d.get('verified_upper_bound') or {}
    rows.append((n,d.get('status'),d.get('reported_status'),rl.get('value'),rl.get('exact_form'),rl.get('proved_by'),rl.get('proved_year'),rl.get('source_key'),rl.get('kind'),vl.get('value'),vl.get('exact_form'),vl.get('evidence'),ru.get('value'),vu.get('value')))
for r in rows:
    if r[6] and int(r[6])>=2026 or (r[5] and any('Levy' in x or 'Squares' in x for x in r[5])):
        print(r)
