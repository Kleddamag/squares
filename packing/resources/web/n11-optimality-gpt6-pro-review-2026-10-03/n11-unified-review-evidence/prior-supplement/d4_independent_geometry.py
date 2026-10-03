if not __debug__:
    raise RuntimeError('This mathematical checker refuses optimized Python (-O/-OO).')

"""Exact cover and closed D4 overlay reconstruction without proof-checker imports.
Uses pairwise boundary-line intersections, not the source clipping algorithm.
"""
from fractions import Fraction as F
from itertools import combinations
from math import gcd,lcm
import json,pathlib,time,hashlib
BASE=pathlib.Path(__file__).resolve().parent
ROOT=BASE/'squares/packing/resources/web/n11-optimality-2026-09-29/receipts/d4-independent/objects'
U=F(387708359002281417731,10**20)

def point(s):return tuple(map(F,s))
def primitive(h):
    den=lcm(*(x.denominator for x in h));v=[int(x*den) for x in h];g=gcd(*v)
    return tuple(F(x//g) for x in v)
def canonical_hs(hs):return tuple(sorted({primitive(h) for h in hs}))
def vertices(hs):
    found=set()
    for (a,b,c),(d,e,f) in combinations(hs,2):
        det=a*e-b*d
        if not det:continue
        x=(c*e-b*f)/det;y=(a*f-c*d)/det
        if all(g*x+h*y<=k for g,h,k in hs):found.add((x,y))
    return tuple(sorted(found))
def reduce_hs(hs,vs):
    if len(vs)==1:
        x,y=vs[0];return canonical_hs([(F(1),F(0),x),(-F(1),F(0),-x),(F(0),F(1),y),(F(0),-F(1),-y)])
    if len(vs)==2:
        (x,y),(u,v)=vs;dx,dy=u-x,v-y;c=-dy*x+dx*y;lo=dx*x+dy*y;hi=dx*u+dy*v
        return canonical_hs([(-dy,dx,c),(dy,-dx,-c),(dx,dy,hi),(-dx,-dy,-lo)])
    return canonical_hs([h for h in hs if sum(a*x+b*y==c for x,y in vs for a,b,c in [h])>=2])
def bbox(vs):return min(x for x,y in vs),max(x for x,y in vs),min(y for x,y in vs),max(y for x,y in vs)
def overlap(b,c):return max(b[0],c[0])<=min(b[1],c[1]) and max(b[2],c[2])<=min(b[3],c[3])
def transform(h,k):
    a,b,c=h
    return [(a,b,c),(-a,b,c-a),(b,-a,c-a),(b,a,c)][k]
def det(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def sqdist(a,b):return (a[0]-b[0])**2+(a[1]-b[1])**2

def independent_geometry():
    start=time.monotonic()
    for sha in ['df7938d9ba27095a38fabe45f8b26b259a2cc896c2ae4aac6bae874f417adc4e','845b5f748843dd60fa7e290a5ea1a304da4e439ae229bd73a841aec816f4e700']:
        assert hashlib.sha256((ROOT/(sha+'.json')).read_bytes()).hexdigest()==sha
    cover=json.loads((ROOT/'df7938d9ba27095a38fabe45f8b26b259a2cc896c2ae4aac6bae874f417adc4e.json').read_text())
    overlay=json.loads((ROOT/'845b5f748843dd60fa7e290a5ea1a304da4e439ae229bd73a841aec816f4e700.json').read_text())
    sites=[point(c['center']) for c in cover['cells']]
    cells=[];maximum_diameter=F(0)
    for i,(px,py) in enumerate(sites):
        hs=[(F(1),F(0),F(1)),(-F(1),F(0),F(0)),(F(0),F(1),F(1)),(F(0),-F(1),F(0))]
        hs +=[(2*(qx-px),2*(qy-py),qx*qx+qy*qy-px*px-py*py) for j,(qx,qy) in enumerate(sites) if i!=j]
        hs=canonical_hs(hs);vs=vertices(hs)
        assert set(vs)=={point(p) for p in cover['cells'][i]['vertices']}
        assert any(det(*t) for t in combinations(vs,3))
        d=max(sqdist(a,b) for a in vs for b in vs)*(U-1)**2
        assert d<1;maximum_diameter=max(maximum_diameter,d)
        hs=reduce_hs(hs,vs);cells.append((hs,vs,bbox(vs)))
    for i,c in enumerate(cells):assert {(1-x,1-y) for x,y in c[1]}==set(cells[15-i][1])
    print('independent cells passed',time.monotonic()-start,flush=True)
    current={(i,):c for i,c in enumerate(cells)};counts=[len(current)]
    for k in [1,2,3]:
        trans=[]
        for hs,_,_ in cells:
            hs=canonical_hs([transform(h,k) for h in hs]);vs=vertices(hs);trans.append((hs,vs,bbox(vs)))
        nex={}
        for labs,(hs,vs,box) in current.items():
            for i,(ihs,ivs,ibox) in enumerate(trans):
                if not overlap(box,ibox):continue
                chs=canonical_hs(hs+ihs);cvs=vertices(chs)
                if cvs:nex[labs+(i,)]=(reduce_hs(chs,cvs),cvs,bbox(cvs))
        current=nex;counts.append(len(current));print('overlay prefix',k+1,'count',len(current),'seconds',time.monotonic()-start,flush=True)
    assert counts==[16,56,124,220]
    reported={tuple(r['labels']):{point(p) for p in r['vertices']} for r in overlay['regions']}
    assert set(current)==set(reported)
    assert all(set(current[lab][1])==vs for lab,vs in reported.items())
    dimensions={}
    for c in current.values():dimensions[min(2,len(c[1])-1)]=dimensions.get(min(2,len(c[1])-1),0)+1
    r={i:current[tuple(overlay['regions'][i]['labels'])][1] for i in [13,26,57]}
    assert {(1-x,y) for x,y in r[13]}==set(r[13])
    assert {(1-x,y) for x,y in r[26]}==set(r[57])
    # Simple rational boxes suffice for both distance obstructions.
    box13=(F(23,50),F(27,50),F(0),F(11,100))
    box26or57=(F(11,25),F(14,25),F(23,100),F(7,25))
    for i,box in [(13,box13),(26,box26or57),(57,box26or57)]:
        assert all(box[0]<=x<=box[1] and box[2]<=y<=box[3] for x,y in r[i])
    coarse=(U-1)**2*(F(1,10)**2+F(7,25)**2)
    assert coarse<1
    maxima={str(j):max(sqdist(a,b) for a in r[13] for b in r[j])*(U-1)**2 for j in [26,57]}
    assert maxima['26']==maxima['57']<1
    # A much simpler cap bound U<4 makes distance < 9*(.1^2+.28^2)=1989/2500<1.
    assert U<4
    report={'method':'Independent exact boundary-line intersection enumeration; no proof-checker imports','counts':counts,'dimensions':dimensions,'maximum_cell_squared_physical_diameter':str(maximum_diameter),'reflection_13_fixed_26_to_57':True,'region13_box':list(map(str,box13)),'region26_and57_box':list(map(str,box26or57)),'exact_distance_maxima':{k:str(v) for k,v in maxima.items()},'coarse_distance_using_actual_U':str(coarse),'simple_distance_bound_using_U_lt_4':'1989/2500','seconds':time.monotonic()-start}
    target=BASE/'fresh-results/d4-independent-geometry.json'
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
    return report
if __name__=='__main__':independent_geometry()
