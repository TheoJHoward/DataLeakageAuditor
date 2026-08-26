import hashlib, sys
P = r"C:\Users\ttbea\AppData\Local\Temp\claude\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\fixture_spike\f4\availability_declaration_DRAFT.md"
EXP1_MD5 = "d4dd09b939540bdc2db33a2e13cb049e"; EXP1_LEN = 6170
EXP2_MD5 = "059bbb1d33e4c93c254ac5f1dabf8dae"; EXP2_LEN = 5744
EXP1_SHA = "3a82ba45bb83095239f17e5169d11b5724419fe629b5ac08aee313020424ae81"
EXP2_SHA = "ad8b327707ecb9627b56b9e74e757facad55fb14e87a3082470fd7398bf267e0"

d = open(P, "rb").read()
print("WHOLE FILE  bytes=%d  lines=%d" % (len(d), d.count(b"\n")))
print("  md5    :", hashlib.md5(d).hexdigest())
print("  sha256 :", hashlib.sha256(d).hexdigest())

# ---- region (i): T2 addendum block, marker-recovered ----
m1 = b"## Phase-7-added columns [T2 addendum"
m1e = b"**SUPERSESSION NOTE"
i = d.find(m1); assert i >= 0 and d.find(m1, i+1) == -1, "marker 1 not unique"
j = d.find(m1e, i); assert j > i and d.find(m1e, j+1) == -1, "marker 1-end not unique"
r1 = d[i:j]
print("\nFROZEN (i) T2 addendum block   offsets [%d,%d) len=%d" % (i, j, len(r1)))
print("  md5    : %s  %s" % (hashlib.md5(r1).hexdigest(),
      "MATCH" if hashlib.md5(r1).hexdigest() == EXP1_MD5 else "*** MISMATCH ***"))
print("  sha256 : %s  %s" % (hashlib.sha256(r1).hexdigest(),
      "MATCH" if hashlib.sha256(r1).hexdigest() == EXP1_SHA else "*** MISMATCH ***"))
print("  length : %d  %s" % (len(r1), "MATCH" if len(r1) == EXP1_LEN else "*** MISMATCH ***"))

# ---- region (ii): decision-log tail, marker-recovered ----
m2 = b"## Decision log"
k = d.find(m2); assert k >= 0 and d.find(m2, k+1) == -1, "marker 2 not unique"
r2 = d[k:]
print("\nFROZEN (ii) decision-log tail  offsets [%d,EOF) len=%d" % (k, len(r2)))
print("  md5    : %s  %s" % (hashlib.md5(r2).hexdigest(),
      "MATCH" if hashlib.md5(r2).hexdigest() == EXP2_MD5 else "*** MISMATCH ***"))
print("  sha256 : %s  %s" % (hashlib.sha256(r2).hexdigest(),
      "MATCH" if hashlib.sha256(r2).hexdigest() == EXP2_SHA else "*** MISMATCH ***"))
print("  length : %d  %s" % (len(r2), "MATCH" if len(r2) == EXP2_LEN else "*** MISMATCH ***"))

ok = (hashlib.md5(r1).hexdigest() == EXP1_MD5 and hashlib.md5(r2).hexdigest() == EXP2_MD5
      and len(r1) == EXP1_LEN and len(r2) == EXP2_LEN)
print("\nBOTH FROZEN REGIONS INTACT:", ok)
sys.exit(0 if ok else 1)
