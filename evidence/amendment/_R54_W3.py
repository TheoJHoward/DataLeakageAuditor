#!/usr/bin/env python3
"""DELTA R54/W3 - the line-459 marker must state what actually happens.

It read "ADDED NOT SUPERSEDED. Criterion 1 stands byte-exact." Byte-level that is true.
At the OUTCOME it is not: of the 25 columns the manifest classes LEAK-SOURCE, 11 stay
REQUIRED and 14 move to OUT OF JURISDICTION or UNSCORED, where SC-4(b) makes an
availability-class finding a FALSE POSITIVE. On those 14 the requirement REVERSES SIGN -
"absence is a miss" becomes "a finding fails the gate" - under a marker telling the
reader nothing changed. SS0.2.1 line 97 measures at the outcome.

The narrowing may well be right and it is being made as class C, which is permitted.
Recording it as "ADDED NOT SUPERSEDED" is what is not.
"""
import json
import pathlib

D = pathlib.Path("C:/Users/ttbea/AppData/Local/Temp/claude/"
                 "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
                 "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/amendment")

OLD = """**\u00a76.2 line 459 \u2014 v30a, ADDED NOT SUPERSEDED.** Criterion 1 stands byte-exact.
**SUPERSEDED BY v30a is the inference** that the denominator is any construction-taxonomy count
recorded elsewhere in the fixture's evidence. That inference is not operative; SC-4(a) replaces it."""

NEW = """**\u00a76.2 line 459 \u2014 v30a. THE TEXT IS UNCHANGED; THE REQUIREMENT IS NOT.** *(Corrected at R54/W3.
This marker previously read "**ADDED NOT SUPERSEDED.** Criterion 1 stands byte-exact." The first
clause is true byte-for-byte and false at the outcome, and \u00a70.2.1 line 97 measures at the outcome.)*

**What is superseded is the INFERENCE** that the denominator is any construction-taxonomy count
recorded elsewhere in the fixture's evidence. That inference is not operative; SC-4(a) replaces it.

**WHAT THAT DOES, STATED AS ARITHMETIC BECAUSE THE CONSEQUENCE IS NOT VISIBLE IN THE DIFF.** The
fixture manifest classes **25** of the 35 fed columns as leaking sources. Under the SC-4(b)
partition:

| manifest class | gate class | count | what a finding on it means |
|---|---|---|---|
| LEAK-SOURCE | REQUIRED | **11** | absence is a **miss** |
| LEAK-SOURCE | OUT OF JURISDICTION | **13** | a finding is a **FALSE POSITIVE** |
| LEAK-SOURCE | UNSCORED | **1** | neither for nor against |

**On 14 of those 25 columns the gate's requirement REVERSES SIGN** \u2014 from *absence is a miss* to
*a finding fails the gate*. **That is a supersession at the outcome, and it is recorded as one
here**, whatever the byte-level text of line 459 does. It is made under the class C rule, which
permits it; what \u00a70.2.1 line 97 does not permit is making it while recording that nothing changed.

**A reader comparing v30 and v30a byte-for-byte at line 459 will see no change and conclude
wrongly.** That is why this is also carried as a disclosure on the face of the amendment (R54/W4,
disclosure 7) rather than left here alone."""

ssf = D / "SCHEMA_SET_FINAL.md"
s = ssf.read_text(encoding="utf-8")
oq = "\n".join(("> " + x).rstrip() for x in OLD.split("\n"))
nq = "\n".join(("> " + x).rstrip() for x in NEW.split("\n"))
assert s.count(oq) == 1, "source match %d" % s.count(oq)
ssf.write_text(s.replace(oq, nq, 1), encoding="utf-8")
print("SCHEMA_SET_FINAL.md: line-459 marker corrected (+%d lines)"
      % (len(nq.split("\n")) - len(oq.split("\n"))))

p = D / "_X5_hunks_v2.json"
d = json.loads(p.read_text(encoding="utf-8"))
n = 0
for h in d["hunks"]:
    op = h.get("operative_text") or ""
    if OLD in op:
        h["operative_text"] = op.replace(OLD, NEW, 1)
        n += 1
assert n == 1, "hunk match %d" % n
json.dump(d, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("SC-4 marker hunk updated from the same string")
