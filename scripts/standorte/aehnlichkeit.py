import re,sys,glob,itertools,html,os
def text(p):
    s=open(p,encoding='utf-8').read()
    s=re.sub(r'(?is)<(script|style|head|nav|footer)[^>]*>.*?</\1>',' ',s)
    s=re.sub(r'(?s)<[^>]+>',' ',s); s=html.unescape(s)
    return re.findall(r'\w+',s.lower())
def sh(w,k=5): return set(tuple(w[i:i+k]) for i in range(len(w)-k+1))
d=sys.argv[1]; files=sorted(glob.glob(d+'/*.html'))
T={os.path.basename(f)[:-5]:text(f) for f in files}
S={k:sh(v) for k,v in T.items()}
def j(a,b): return len(S[a]&S[b])/len(S[a]|S[b])
svc=sorted(set(k.rsplit('-',1)[0] if not k.endswith('gladbach') else k.split('-bergisch')[0] for k in T))
import collections
print("Wortzahl min/median/max:", min(len(v) for v in T.values()), sorted(len(v) for v in T.values())[len(T)//2], max(len(v) for v in T.values()))
for s in svc:
    ks=[k for k in T if k.startswith(s+'-')]
    vals=[j(a,b) for a,b in itertools.combinations(ks,2)]
    print(f"{s:22} {len(ks)} Seiten, gleiche Leistung/andere Stadt: Ø {sum(vals)/len(vals):.0%} max {max(vals):.0%}")
cities=sorted(set(k[len(s)+1:] for s in svc for k in T if k.startswith(s+'-')))
vals=[]
for c in cities:
    ks=[k for k in T if k.endswith('-'+c) and k.split('-'+c)[0] in svc]
    vals+=[j(a,b) for a,b in itertools.combinations(ks,2)]
print(f"gleiche Stadt/andere Leistung: Ø {sum(vals)/len(vals):.0%} max {max(vals):.0%}")
