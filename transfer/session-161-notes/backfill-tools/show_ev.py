import sys, yaml
sys.path.insert(0, '/home/user/squares-docs/packing/src')
from sqpack.yamlio import safe_load
from pathlib import Path
ev = {e['id']: e for e in safe_load(Path('/home/user/squares-docs/packing/frontier/evidence.yaml').read_text())['evidence']}
for i in sys.argv[1:]:
    print(yaml.safe_dump([ev[i]], sort_keys=False, width=120, allow_unicode=True))
