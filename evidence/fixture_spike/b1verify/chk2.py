import hashlib, os
D = r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01\AVAILABILITY_DECLARATION.md"
d = open(D,'rb').read()

def h(b): return hashlib.md5(b).hexdigest(), hashlib.sha256(b).hexdigest(), len(b)

i = d.find(b"## Phase-7-added columns")
print("T2 start marker idx:", i, "occurrences:", d.count(b"## Phase-7-added columns"))
j = d.find(b"**SUPERSESSION NOTE")
print("SUPERSESSION marker idx:", j, "occurrences:", d.count(b"**SUPERSESSION NOTE"))
blk = d[i:j]
print("T2 block:", h(blk))
print("expect md5 d4dd09b939540bdc2db33a2e13cb049e sha256 3a82ba45bb83095239f17e5169d11b5724419fe629b5ac08aee313020424ae81 len 6170")

k = d.find(b"## Decision log")
print("Decision log idx:", k, "occurrences:", d.count(b"## Decision log"))
tail = d[k:]
print("tail:", h(tail))
print("expect md5 059bbb1d33e4c93c254ac5f1dabf8dae sha256 ad8b327707ecb9627b56b9e74e757facad55fb14e87a3082470fd7398bf267e0 len 5744")
print("tail last byte:", repr(tail[-1:]))

base = r"C:\Users\ttbea\AppData\Local\Temp\claude\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\fixture_spike"
for rel in [r"d1\pre_tail.txt", r"p2\frozen_tail_before.bin", r"d1\post_tail.txt"]:
    p = os.path.join(base, rel)
    b = open(p,'rb').read()
    print(rel, "len", len(b), "is prefix of live tail:", tail.startswith(b), "md5", hashlib.md5(b).hexdigest())
    if not tail.startswith(b):
        for x in range(min(len(b),len(tail))):
            if b[x]!=tail[x]:
                print("  first diff at", x)
                print("  snapshot:", repr(b[max(0,x-80):x+80]))
                print("  live    :", repr(tail[max(0,x-80):x+80]))
                break
        else:
            print("  no diff in common prefix; lengths", len(b), len(tail))

for rel in [r"d1\pre_t2_block.txt", r"d1\post_t2_block.txt", r"p2\frozen_t2_before.bin"]:
    p = os.path.join(base, rel)
    b = open(p,'rb').read()
    print(rel, "len", len(b), "identical to live T2 block:", b==blk)
