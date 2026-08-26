import re, difflib, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
base = r"C:\Users\ttbea\AppData\Local\Temp\claude\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\amendment"
def load(p): return open(p, encoding='utf-8').read().split('\n')
k1 = load(base+r"\K1_SCHEMA_CLAUSES.md")
sp = load(base+r"\SC13_SPLIT_ABC.md")
ssa = load(base+r"\SCHEMA_SET_ADOPTION.md")

def sections(lines, hdr_re):
    # returns dict name -> (start,end) line idx for each clause header
    idx = [(i, m.group(1)) for i,l in enumerate(lines) for m in [re.match(hdr_re, l)] if m]
    out = {}
    for j,(i,name) in enumerate(idx):
        end = idx[j+1][0] if j+1 < len(idx) else len(lines)
        out[name] = (i,end)
    return out

k1s = sections(k1, r"^### (SC-\d+) ")
sps = sections(sp, r"^## (SC-13[abc]) ")
ssas = sections(ssa, r"^### (SC-\d+[abc]?) ")

def block(lines, s, e, start_marker, end_markers):
    seg = lines[s:e]
    st = None
    for i,l in enumerate(seg):
        if l.startswith(start_marker):
            st = i; break
    if st is None: return None
    en = len(seg)
    for i in range(st+1, len(seg)):
        if any(seg[i].startswith(m) for m in end_markers):
            en = i; break
    return seg[st:en]

def norm(lines):
    # join wrapped lines within paragraphs to be robust to rewrap; keep blank lines as separators
    txt = '\n'.join(lines)
    paras = re.split(r'\n\s*\n', txt)
    out=[]
    for p in paras:
        p = re.sub(r'\n>\s?', ' ', p)  # blockquote wraps
        p = re.sub(r'\n', ' ', p)
        p = re.sub(r'\s+', ' ', p).strip()
        out.append(p)
    return out

parts = ["**REGISTERS", "**INSERTION POINT", "**SUPERSESSION MARKER", "**THE CLAUSE", "**DATA THE DECLARATION", "**ROWS COVERED"]
allm = parts + ["---", "*(", "*Instance record", "### "]
def compare(name, old_lines, old_rng, new_lines, new_rng):
    print("="*100); print("CLAUSE", name)
    for i,pm in enumerate(parts):
        ends = [m for m in allm if m!=pm]
        ob = block(old_lines, *old_rng, pm, ends)
        nb = block(new_lines, *new_rng, pm, ends)
        if ob is None and nb is None: continue
        on = norm(ob or []); nn = norm(nb or [])
        if on == nn:
            print(f"  [{pm.strip('*')}] IDENTICAL (normalized)")
        else:
            print(f"  [{pm.strip('*')}] DIFFERS:")
            sm = difflib.SequenceMatcher(a=on, b=nn, autojunk=False)
            for tag,i1,i2,j1,j2 in sm.get_opcodes():
                if tag=='equal': continue
                if tag=='replace' and i2-i1==1 and j2-j1==1:
                    aw=on[i1].split(' '); bw=nn[j1].split(' ')
                    wm=difflib.SequenceMatcher(a=aw,b=bw,autojunk=False)
                    for t,a1,a2,b1,b2 in wm.get_opcodes():
                        if t=='equal': continue
                        ctx=' '.join(aw[max(0,a1-6):a1])
                        print(f"      {t}: ...{ctx} [-{' '.join(aw[a1:a2])}-] {{+{' '.join(bw[b1:b2])}+}}")
                else:
                    for x in on[i1:i2]: print("      - "+x[:600])
                    for x in nn[j1:j2]: print("      + "+x[:600])

for n in ["SC-%d"%i for i in range(1,13)]:
    compare(n, k1, k1s[n], ssa, ssas[n])
for n in ["SC-13a","SC-13b","SC-13c"]:
    compare(n, sp, sps[n], ssa, ssas[n])
