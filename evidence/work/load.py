# -*- coding: utf-8 -*-
import importlib.util, os, sys, json, hashlib
BASE = r"C:\Users\ttbea\AppData\Local\Temp\claude\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\applied"
def load(name):
    p = os.path.join(BASE, name)
    spec = importlib.util.spec_from_file_location(name[:-3], p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.EDITS
ALL = []
for i in (1,2,3,4):
    e = load("_k4_edits_part%d.py" % i)
    print("part%d: %d edits, %s .. %s" % (i, len(e), e[0]['id'], e[-1]['id']))
    ALL.extend(e)
print("TOTAL", len(ALL))
ids = [e['id'] for e in ALL]
print("dupes:", len(ids) != len(set(ids)))
# expected sequence
exp = ["E%02d" % i for i in range(1, len(ALL)+1)]
print("sequential:", ids == exp)
if ids != exp:
    for a,b in zip(ids, exp):
        if a != b:
            print("first mismatch", a, b); break
for e in ALL:
    print(e['id'], e['rows'], '|', e['clause'][:70].replace("\n"," "))
