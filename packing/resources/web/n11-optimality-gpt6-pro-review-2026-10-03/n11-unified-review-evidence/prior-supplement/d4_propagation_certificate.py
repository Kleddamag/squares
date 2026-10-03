"""Produce and independently consume elementary D4 incidence traces.
The trace uses only bijection consequences, never geometric distance bans.
"""
from pathlib import Path
import itertools,json
import d4_incidence_data as data

if not __debug__:
    raise RuntimeError("This mathematical checker refuses optimized Python (-O/-OO).")

require = data.require

def initial(source,targets):
    return {o:set(r for r,labs in enumerate(data.LABELS) if labs[0]==o and all(labs[k+1] in targets[k] for k in range(3))) for o in source}

def generate(dom,targets):
    trace=[]
    while True:
        for owner in sorted(dom):
            if not dom[owner]:return trace,{'type':'empty_owner','owner':owner}
        for k in range(1,4):
            for label in sorted(targets[k-1]):
                possible=[o for o in dom if any(data.LABELS[r][k]==label for r in dom[o])]
                if not possible:return trace,{'type':'unused_label','view':k,'label':label}
        move=None
        for k in range(1,4):
            for owner in sorted(dom):
                labels={data.LABELS[r][k] for r in dom[owner]}
                if len(labels)==1:
                    label=next(iter(labels))
                    drops={o:sorted(r for r in dom[o] if data.LABELS[r][k]==label) for o in dom if o!=owner}
                    drops={o:rs for o,rs in drops.items() if rs}
                    if drops:move={'type':'fixed_owner_label','view':k,'owner':owner,'label':label,'drops':drops};break
            if move:break
        if move is None:
            for k in range(1,4):
                for label in sorted(targets[k-1]):
                    possible=[o for o in dom if any(data.LABELS[r][k]==label for r in dom[o])]
                    if len(possible)==1:
                        owner=possible[0];drops=[r for r in dom[owner] if data.LABELS[r][k]!=label]
                        if drops:move={'type':'unique_owner_for_label','view':k,'owner':owner,'label':label,'drops':{owner:sorted(drops)}};break
                if move:break
        if move is None:return trace,{'type':'survives','domains':{o:sorted(rs) for o,rs in dom.items()}}
        trace.append(move)
        for o,rs in move['drops'].items():dom[o].difference_update(rs)

def owner_map(value, owners, label):
    require(type(value) is dict, label + ' must be an object')
    result = {}
    for key, values in value.items():
        require(type(key) is str and key.isdecimal(), label + ' owner key grammar')
        owner = int(key)
        require(str(owner) == key and owner in owners, label + ' owner outside source')
        require(type(values) is list and all(type(r) is int and 0 <= r < len(data.LABELS) for r in values), label + ' region grammar')
        require(len(set(values)) == len(values), label + ' duplicate region')
        result[owner] = set(values)
    return result


def view_label(value, targets, label):
    require(type(value) is dict, label + ' must be an object')
    k, l = value['view'], value['label']
    require(type(k) is int and 1 <= k <= 3, label + ' view must be 1, 2, or 3')
    require(type(l) is int and 0 <= l < 16 and l in targets[k-1], label + ' target label')
    return k, l


def verify(cert):
    require(type(cert) is dict, 'certificate must be an object')
    require(cert['schema'] == 'independent_d4_bijection_trace_v2', 'certificate schema')
    require(cert['input_sha256'] == data.INPUT_SHA256, 'pinned source input bindings')
    require(cert['four_view_labels_sha256'] == data.LABEL_SHA256, 'label inventory binding')
    require(cert['view_convention'] == data.VIEW_CONVENTION and cert['cap_U'] == data.CAP_U, 'view/frame binding')
    require(cert['target_raw_masks'] == [list(m) for m in data.TARGETS], 'target mask inventory')
    require(type(cert['cases']) is list and len(cert['cases']) == 648, 'complete case count')
    expected = {(cid, ts) for cid in data.CASE_IDS for ts in itertools.product(range(6), repeat=3)}
    found, survivors = set(), []
    summary = {cid: {'initial_contradictions': 0, 'propagated_contradictions': 0, 'survivors': 0, 'maximum_operations': 0} for cid in data.CASE_IDS}
    for record in cert['cases']:
        require(type(record) is dict, 'case record grammar')
        cid, targets_raw = record['source'], record['target_indices']
        require(type(cid) is int and cid in data.CASE_IDS, 'source index')
        require(type(targets_raw) is list and len(targets_raw) == 3 and all(type(t) is int and 0 <= t < 6 for t in targets_raw), 'target indices')
        ts = tuple(targets_raw)
        key = (cid, ts)
        require(key in expected and key not in found, 'case duplicate or mismatch')
        found.add(key)
        targets = [set(data.TARGETS[t]) for t in ts]
        dom = initial(data.MASKS[cid], targets)
        require(type(record['trace']) is list, 'trace grammar')
        for step in record['trace']:
            k, l = view_label(step, targets, 'propagation step')
            o = step['owner']
            require(type(o) is int and o in dom, 'step owner')
            drops = owner_map(step['drops'], dom, 'drops')
            require(bool(drops) and any(drops.values()), 'step does not remove a region')
            if step['type'] == 'fixed_owner_label':
                require(bool(dom[o]) and {data.LABELS[r][k] for r in dom[o]} == {l}, 'owner does not force label')
                for p, rs in drops.items():
                    require(p != o and rs <= dom[p] and all(data.LABELS[r][k] == l for r in rs), 'invalid reserved-label deletion')
            else:
                require(step['type'] == 'unique_owner_for_label', 'unknown propagation rule')
                possible = {p for p in dom if any(data.LABELS[r][k] == l for r in dom[p])}
                require(possible == {o} and set(drops) == {o} and drops[o] <= dom[o] and all(data.LABELS[r][k] != l for r in drops[o]), 'invalid unique-owner restriction')
            for p, rs in drops.items():
                dom[p] -= rs
        final = record['terminal']
        require(type(final) is dict, 'terminal grammar')
        summary[cid]['maximum_operations'] = max(summary[cid]['maximum_operations'], len(record['trace']))
        if final['type'] == 'empty_owner':
            o = final['owner']
            require(type(o) is int and o in dom and not dom[o], 'terminal owner is not empty')
        elif final['type'] == 'unused_label':
            k, l = view_label(final, targets, 'terminal unused_label')
            require(all(data.LABELS[r][k] != l for rs in dom.values() for r in rs), 'terminal label is still available')
        else:
            require(final['type'] == 'survives', 'unknown terminal rule')
            require(all(dom.values()) and owner_map(final['domains'], dom, 'terminal domains') == dom, 'surviving domain mismatch')
            survivors.append((cid, ts, dom))
            summary[cid]['survivors'] += 1
            continue
        summary[cid]['initial_contradictions' if not record['trace'] else 'propagated_contradictions'] += 1
    require(found == expected, 'case inventory omission')
    require({(cid, ts) for cid, ts, _ in survivors} == {(999, (1,1,0)), (1462, (0,2,4))}, 'survivor table mismatch')
    for cid, ts, dom in survivors:
        require(dom[1] == {13}, 'first forced region mismatch')
        require(dom[2 if cid == 999 else 5] == {26 if cid == 999 else 57}, 'second forced region mismatch')
    return summary

if __name__=='__main__':
    # Bundle entry point consumes the supplied trace; it never regenerates it.
    trace_path=Path(__file__).resolve().parent/'d4-propagation-traces.json'
    summary=verify(json.loads(trace_path.read_bytes()))
    print(json.dumps(summary,indent=2))
