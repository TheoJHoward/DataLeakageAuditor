#!/usr/bin/env python3
"""DELTA R59/E1 - land the at-risk record, add the citation gate, install check (xi)."""
import pathlib

D = pathlib.Path("C:/Users/ttbea/AppData/Local/Temp/claude/"
                 "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
                 "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad")

# ---- 1. X4: land Z1/Z2/Z5, and add the citation-resolution gate --------------
x = D / "ceremony" / "X4_REGENERATION_REQUIREMENTS.md"
t = x.read_text(encoding="utf-8")
B = ("- `HISTORY.md` **H-35, H-36, H-37**, plus **H-38** (\u00a710.1 registers no third state \u2014 R47/P10)")
assert t.count(B) == 1, "C4 anchor match %d" % t.count(B)
t = t.replace(B, "- **`errata/Z1_Z2_Z5_RECORDS.md`** \u2014 the three records drafted at R33/Z, which say of "
                 "themselves *\"these entries land at the ceremony, with `HISTORY.md`'s other open items\"* "
                 "and which **no ceremony step referenced until R59/E1**. A staged file no step applies is "
                 "a record that does not exist.\n" + B, 1)

A = "## C3 \u2014 THE FULL C1\u2013C5 / R15 SET, INTACT"
assert t.count(A) == 1
GATE = """## C2.4 \u2014 CEREMONY GATE: EVERY LEDGER CITATION MUST RESOLVE BEFORE THE TAG

The amendment's operative text cites ledger entries by identifier. Three do not exist yet and are
written **by the ceremony itself**, so that `HISTORY.md` and `DEVIATIONS.md` each take **one** hashed
state rather than several unhashed ones:

| cited by operative text | written by |
|---|---|
| **H-38** \u2014 \u00a710.1 registers no third state | this ceremony, `HISTORY.md` |
| **H-39** \u2014 the deferred contaminated-side tightening | this ceremony, `HISTORY.md` |
| **D-003** \u2014 the \u00a79.2 comparison set | this ceremony, `DEVIATIONS.md` |

**REQUIRED before `git tag`:** run `_ledger_citations.py` and confirm **ORPHAN = 0 and PENDING = 0**.
PENDING is legitimate while drafting and **fatal at the tag** \u2014 a pending citation the ceremony
forgets becomes text resting on authority that does not exist, which is the SC-8(g) defect in a
different file. **A pending citation is only safe while somebody is still looking.**

"""
t = t.replace(A, GATE + A, 1)
x.write_text(t, encoding="utf-8")
print("X4: Z1/Z2/Z5 added to the landed set; C2.4 citation gate added")

# ---- 2. install check (xi) ---------------------------------------------------
p = D / "amendment" / "_X5_selfcheck.py"
s = p.read_text(encoding="utf-8")
assert "check (xi)" not in s
ANCHOR = 'head("SELF-CHECK RESULT")'
NEW = '''# ---------------------------------------------------------------- (xi) R59/E1
head("(xi) EVERY LEDGER CITATION IN OPERATIVE TEXT RESOLVES, OR IS PLANNED")
print("  A citation to a ledger entry that does not exist and that NOTHING will write is")
print("  the SC-8(g) defect in a different file. PENDING is legitimate while drafting -")
print("  the ledgers take one hashed state at the ceremony - but it is fatal at the tag,")
print("  and it is reported every run so it cannot quietly become an orphan.")
print()
_sp = _ilu.spec_from_file_location("_lc", str(D / "_ledger_citations.py"))
_lc = _ilu.module_from_spec(_sp)
_sp.loader.exec_module(_lc)
if _lc.run():
    fail += 1
    print(chr(10) + "  *** operative text cites a ledger entry nothing will write ***")

'''
s = s.replace(ANCHOR, NEW + ANCHOR, 1)
s = s.replace('print(f"  assertions failed: {fail} of 10")',
              'print(f"  assertions failed: {fail} of 11")', 1)
p.write_text(s, encoding="utf-8")
print("check (xi) installed - self-check now scores 11")
