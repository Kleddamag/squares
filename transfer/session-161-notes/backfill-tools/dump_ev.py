import sys
sys.path.insert(0, '/home/user/squares-docs/packing')
sys.path.insert(0, '/home/user/squares-docs/packing/src')
from sqpack.yamlio import safe_load
from pathlib import Path
from devtools.check_results import derive_verification, derive_confirmation
ev = safe_load(Path('/home/user/squares-docs/packing/frontier/evidence.yaml').read_text())['evidence']
for e in ev:
    er = e.get('external_review') or {}
    print(f"{e['id']}\n   scope={e.get('scope')} assur={e.get('assurance')} method={e.get('method')} origin={e.get('origin')} perf={e.get('performed_by')}\n   src={e.get('source_key')} cert={'Y' if e.get('certificate') else 'N'} replay={'Y' if e.get('replay') else 'N'} rstat={e.get('replay_status')} review={er.get('state')} V={derive_verification([e])} C={derive_confirmation([e])}")
