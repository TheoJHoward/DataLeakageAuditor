"""R11-batch end-state verifier. Read-only over the declaration file.

Recomputes: whole-file line count / md5 / sha256, and the two FROZEN REGION
digests using MARKER-BASED recovery (the preferred method per PRE_R9_HASHES.txt
section 4), comparing against the PRE_R9 anchor values.
"""
import hashlib
import sys

P = (r"C:\Users\ttbea\AppData\Local\Temp\claude"
     r"\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01"
     r"\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\fixture_spike"
     r"\f4\availability_declaration_DRAFT.md")

ANCHOR_T2_MD5 = "d4dd09b939540bdc2db33a2e13cb049e"
ANCHOR_T2_SHA = "3a82ba45bb83095239f17e5169d11b5724419fe629b5ac08aee313020424ae81"
ANCHOR_T2_LEN = 6170
ANCHOR_TAIL_MD5 = "059bbb1d33e4c93c254ac5f1dabf8dae"
ANCHOR_TAIL_SHA = "ad8b327707ecb9627b56b9e74e757facad55fb14e87a3082470fd7398bf267e0"
ANCHOR_TAIL_LEN = 5744

data = open(P, "rb").read()
text = data.decode("utf-8")

print("## WHOLE FILE")
print("  bytes  :", len(data))
print("  lines  :", text.count("\n") + (0 if text.endswith("\n") else 1))
print("  md5    :", hashlib.md5(data).hexdigest())
print("  sha256 :", hashlib.sha256(data).hexdigest())

# ---- frozen region (i): T2 addendum block ------------------------------
start_marker = b"## Phase-7-added columns [T2 addendum"
end_marker = b"**SUPERSESSION NOTE"
s = data.find(start_marker)
e = data.find(end_marker)
blk = data[s:e]
print()
print("## FROZEN (i) T2 addendum block  [marker-based]")
print("  start offset :", s)
print("  end offset   :", e)
print("  length       :", len(blk), "expected", ANCHOR_T2_LEN,
      "->", "OK" if len(blk) == ANCHOR_T2_LEN else "MISMATCH")
m = hashlib.md5(blk).hexdigest()
h = hashlib.sha256(blk).hexdigest()
print("  md5          :", m, "->", "MATCH" if m == ANCHOR_T2_MD5 else "MISMATCH")
print("  sha256       :", h, "->", "MATCH" if h == ANCHOR_T2_SHA else "MISMATCH")

# ---- frozen region (ii): decision-log tail -----------------------------
tail_marker = b"## Decision log"
t = data.find(tail_marker)
tail = data[t:]
print()
print("## FROZEN (ii) decision-log tail  [marker-based, to EOF]")
print("  start offset :", t)
print("  length       :", len(tail), "expected", ANCHOR_TAIL_LEN,
      "->", "OK" if len(tail) == ANCHOR_TAIL_LEN else "MISMATCH")
m2 = hashlib.md5(tail).hexdigest()
h2 = hashlib.sha256(tail).hexdigest()
print("  md5          :", m2, "->", "MATCH" if m2 == ANCHOR_TAIL_MD5 else "MISMATCH")
print("  sha256       :", h2, "->", "MATCH" if h2 == ANCHOR_TAIL_SHA else "MISMATCH")
print("  tail heading occurrences in file:", data.count(tail_marker))

ok = (len(blk) == ANCHOR_T2_LEN and m == ANCHOR_T2_MD5 and h == ANCHOR_T2_SHA
      and len(tail) == ANCHOR_TAIL_LEN and m2 == ANCHOR_TAIL_MD5
      and h2 == ANCHOR_TAIL_SHA)
print()
print("FROZEN REGIONS:", "ALL BYTE-IDENTICAL TO PRE_R9 ANCHOR" if ok else "*** DRIFT ***")
sys.exit(0 if ok else 1)
