import re, math, sys
ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
ORDER = [("12-sided cookie","12-sided-cookies"),("9-sided cookie","9-sided-cookies"),("7-sided cookie","7-sided-cookies"),("6-sided cookie","6-sided-cookies"),("4-sided cookie","4-sided-cookies"),("Circle","circle")]
shapes = [(n, re.search(r' d="([^"]+)"', open(f"{ROOT}/shapes/{f}.svg").read()).group(1)) for n, f in ORDER]
assert len(shapes) == 6, len(shapes)
C, K, INTERVAL, STIFF, ZETA = 190.0, 240, 650, 1000.0, 0.6

def sample(d):
    toks = re.findall(r'[MCLZ]|-?\d*\.?\d+(?:e-?\d+)?', d)
    pts=[]; i=0; cur=None; start=None; cmd=None
    def num():
        nonlocal i; v=float(toks[i]); i+=1; return v
    while i < len(toks):
        t = toks[i]
        if t in "MCLZ": cmd=t; i+=1
        if cmd=="M": cur=(num(),num()); start=cur; pts.append(cur)
        elif cmd=="L":
            p=(num(),num())
            for s in range(1,41): pts.append((cur[0]+(p[0]-cur[0])*s/40, cur[1]+(p[1]-cur[1])*s/40))
            cur=p
        elif cmd=="C":
            a=(num(),num()); b=(num(),num()); p=(num(),num())
            for s in range(1,41):
                u=s/40; v=1-u
                pts.append((v*v*v*cur[0]+3*v*v*u*a[0]+3*v*u*u*b[0]+u*u*u*p[0], v*v*v*cur[1]+3*v*v*u*a[1]+3*v*u*u*b[1]+u*u*u*p[1]))
            cur=p
        elif cmd=="Z": cur=start
    return pts

def radii(d):
    pol = sorted(((math.atan2(y-C,x-C))%(2*math.pi), math.hypot(x-C,y-C)) for x,y in sample(d))
    n=len(pol); out=[]; j=0
    for k in range(K):
        a=k/K*2*math.pi
        while j<n and pol[j][0]<a: j+=1
        hi=pol[j%n]; lo=pol[(j-1)%n]
        ha=hi[0]+2*math.pi if j>=n else hi[0]
        la=lo[0]-2*math.pi if j==0 else lo[0]
        t=0 if ha==la else (a-la)/(ha-la)
        out.append(lo[1]+(hi[1]-lo[1])*t)
    return out

R=[radii(d) for _,d in shapes]
W0=math.sqrt(STIFF); WD=W0*math.sqrt(1-ZETA*ZETA)
def spring(ms):
    if ms>=INTERVAL: return 1.0
    t=ms/1000
    return 1-math.exp(-ZETA*W0*t)*(math.cos(WD*t)+(ZETA*W0/WD)*math.sin(WD*t))

def pathd(r):
    return "M"+"L".join(f"{C+r[k]*math.cos(k/K*2*math.pi):.1f} {C+r[k]*math.sin(k/K*2*math.pi):.1f}" for k in range(K))+"Z"

OFFS=[0,20,40,60,80,100,125,150,180,220,280]
N=len(R)
morph_t=[]; morph_v=[]
for s in range(N):
    a,b=R[s],R[(s+1)%N]
    for o in OFFS:
        p=spring(o)
        morph_t.append((s*INTERVAL+o)/(N*INTERVAL))
        morph_v.append(pathd([max(0,a[k]+(b[k]-a[k])*p) for k in range(K)]))
morph_t.append(1.0); morph_v.append(pathd(R[0]))

kick_t=[]; kick_v=[]
for s in range(2*N):
    for o in OFFS:
        kick_t.append((s*INTERVAL+o)/(2*N*INTERVAL)); kick_v.append(f"{(s+spring(o))*90:.2f} 190 190")
kick_t.append(1.0); kick_v.append("1080 190 190")

kt=lambda ts:";".join(f"{t:.5f}" for t in ts)
anim = (
f'<g><animateTransform attributeName="transform" type="rotate" from="0 190 190" to="360 190 190" dur="4666ms" repeatCount="indefinite"/>'
f'<g><animateTransform attributeName="transform" type="rotate" dur="{2*N*INTERVAL}ms" repeatCount="indefinite" keyTimes="{kt(kick_t)}" values="{";".join(kick_v)}"/>'
f'<path class="loader-path" d="{morph_v[0]}"><animate attributeName="d" dur="{N*INTERVAL}ms" repeatCount="indefinite" keyTimes="{kt(morph_t)}" values="{";".join(morph_v)}"/></path>'
'</g></g>')
open(f"{ROOT}/cookie-morph-loader.svg","w").write(f'<svg width="380" height="380" viewBox="0 0 380 380" fill="#6750A4" xmlns="http://www.w3.org/2000/svg">{anim}</svg>\n')
print(len(anim))
