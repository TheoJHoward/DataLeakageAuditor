#!/usr/bin/env python3
"""DELTA R48 / Q8 - harden H-L15 IN THE CHECK, not only in the lesson.

Four absence findings at `confidence: PROVEN` in one workflow each declared a
population that excluded the active root declared in ROUND_STATE §0, and all four
were wrong. H-L15 already said an absence finding is only as good as the search
behind it. Saying it again would not have caught this.

So: assertion (vii) in the self-check.

  Population: every finding in `findings_triaged` whose text makes an absence
  claim and whose status is not WITHDRAWN (a withdrawn finding asserts nothing).

  Requirement: the finding carries an explicit `SEARCHED:` clause naming the
  artifact(s) searched. An UNSCOPED absence claim - one asserting a thing exists
  nowhere, rather than that it is absent from a named artifact - must in addition
  name the active root, because that is the class that failed.

This script installs the assertion AND formalises the 11 live claims by restating
the artifact each already names. It does not invent a search that was not run: a
finding that names no artifact is left to fail the check.
"""
import json
import pathlib
import re

D = pathlib.Path("C:/Users/ttbea/AppData/Local/Temp/claude/"
                 "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
                 "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/amendment")

ART = re.compile(r"(SCHEMA_SET_FINAL\.md|K2_AMENDMENT_LEDGER\.md|X5_FINAL_PREREG_DIFF\.md|"
                 r"BLOCK_MANIFEST\.md|PREREG\.md|AVAILABILITY_DECLARATION\.md|"
                 r"SCHEMA_SET_ADOPTION\.md|DESIGN\.md|HISTORY\.md)")
SIG = re.compile(r"\b(no hunk|does not exist|do(es)? not appear|is absent|are absent|nowhere|"
                 r"never (ran|runs)|not present|no such|has no|carried by no|no clause|appears in no)\b", re.I)

p = D / "_X5_hunks_v2.json"
d = json.loads(p.read_text(encoding="utf-8"))
tri = d["findings_triaged"]

annotated, unnamed = 0, []
for i, t in enumerate(tri):
    if not SIG.search(t["text"]) or t["status"] == "WITHDRAWN":
        continue
    if "SEARCHED:" in t["text"]:
        continue
    arts = sorted(set(ART.findall(t["text"])))
    if not arts:
        unnamed.append(i)
        continue
    t["text"] = t["text"].rstrip() + (
        "  **SEARCHED:** " + ", ".join("`%s`" % a for a in arts) +
        " \u2014 the artifact(s) this finding itself names, restated here as the declared search "
        "population (R48/Q8 formalisation; no new search was run). This is a SCOPED absence claim: "
        "it asserts absence from the named artifact(s), not from the corpus. Any disposition that "
        "would DELETE a registered surface requires the artifact named to be authoritative for the "
        "question \u2014 H-L15.")
    annotated += 1

json.dump(d, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("findings formalised with a SEARCHED: clause : %d" % annotated)
print("findings naming NO artifact (left to fail)  : %d %s" % (len(unnamed), unnamed or ""))

# ------------------------------------------------------------------ install (vii)
sc = D / "_X5_selfcheck.py"
s = sc.read_text(encoding="utf-8")
assert "check (vii)" not in s, "assertion (vii) already installed"

ANCHOR = 'head("SELF-CHECK RESULT")'
assert s.count(ANCHOR) == 1, s.count(ANCHOR)

NEW = '''# ---------------------------------------------------------------- (vii) R48/Q8
head("(vii) EVERY LIVE ABSENCE CLAIM DECLARES ITS SEARCH POPULATION  [R48/Q8, H-L15]")
print("  Four absence findings at PROVEN confidence in one workflow each declared a population")
print("  that excluded the active root in ROUND_STATE \\u00a70. All four were wrong. The lesson text")
print("  already said 'an absence finding is only as good as the search behind it'; repeating it")
print("  would not have caught this, so it is asserted here instead.")
print()
_SIG = re.compile(r"\\b(no hunk|does not exist|do(es)? not appear|is absent|are absent|nowhere|"
                  r"never (ran|runs)|not present|no such|has no|carried by no|no clause|appears in no)\\b", re.I)
_UNSCOPED = re.compile(r"\\b(nowhere|does not exist|never ran|anywhere in the (corpus|repository|archive))\\b", re.I)
_ROOT = "8b1d67a4"

_tri = json.loads((D / "_X5_hunks_v2.json").read_text(encoding="utf-8")).get("findings_triaged") or []
_abs = [(i, t) for i, t in enumerate(_tri)
        if _SIG.search(t["text"]) and t.get("status") != "WITHDRAWN"]
_nopop = [i for i, t in _abs if "SEARCHED:" not in t["text"]]
_unscoped_norot = [i for i, t in _abs
                   if _UNSCOPED.search(t["text"]) and _ROOT not in t["text"]
                   and "SCOPED absence claim" not in t["text"]]

print(f"  live absence claims (OPEN/FIXED)      : {len(_abs)}")
print(f"  without a declared SEARCHED: population: {len(_nopop)}  {_nopop if _nopop else ''}")
print(f"  UNSCOPED and not naming the active root: {len(_unscoped_norot)}  {_unscoped_norot if _unscoped_norot else ''}")
if _nopop or _unscoped_norot:
    fail += 1
    print("  *** an absence claim whose population is undeclared may not carry a disposition ***")
    print("  *** remedy (H-L15): name the artifact and why it is authoritative, or downgrade  ***")
    print("  *** the claim to 'not found in X' and let no disposition follow from it.        ***")
else:
    print("  PASS \\u2014 every live absence claim declares the population it searched")

'''
s = s.replace(ANCHOR, NEW + ANCHOR, 1)
s = s.replace('print(f"  assertions failed: {fail} of 6")',
              'print(f"  assertions failed: {fail} of 7")', 1)
if "\nimport re" not in s and "^import re" not in s:
    s = s.replace("import json", "import json\nimport re", 1)
sc.write_text(s, encoding="utf-8")
print("assertion (vii) installed - self-check now scores 7")
