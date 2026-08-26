#!/usr/bin/env python3
"""DELTA R60/F3 - W6 group 2: B5 and P5.

B5  (k2) requires the manifest to be enumerated in the declaration's SC-8(a) freeze and
    to carry a non-DRAFT status at the tag. **Neither holds today**, and (k4) indexed
    neither as a failure - so the limb stated conditions nothing would enforce. Both are
    now failure conditions, and both are on the ceremony landing list.
P5  PART 5 is headed "EVERY DIFFERENCE BETWEEN THIS FILE'S PART 1 AND SSA's PART 1" and
    says "Anything not listed is byte-identical to SSA". SC-4(k)'s applied lines are not
    listed. A completeness claim with an unlisted difference under it is false on its face.
"""
import json
import pathlib

D = pathlib.Path("C:/Users/ttbea/AppData/Local/Temp/claude/"
                 "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
                 "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/amendment")
ssf = D / "SCHEMA_SET_FINAL.md"
s = ssf.read_text(encoding="utf-8")

# ---- B5: index both breaches in (k4) -----------------------------------------
OLD_K4 = ("**(k4) WHAT MAKES THIS LIMB FAIL.** This limb fails where the REQUIRED list is empty on a declared\n"
          "side; **or where the reconciliation is absent**; or where any difference in it is unnamed, is named\n"
          "without the registered predicate that produced its class, **or is named with a ground that cites no\n"
          "artifact and location (k2)(i)**.")
NEW_K4 = ("**(k4) WHAT MAKES THIS LIMB FAIL.** This limb fails where the REQUIRED list is empty on a declared\n"
          "side; **or where the reconciliation is absent**; or where any difference in it is unnamed, is named\n"
          "without the registered predicate that produced its class, **or is named with a ground that cites no\n"
          "artifact and location (k2)(i)**; **or where the manifest the reconciliation reads is not enumerated\n"
          "in the declaration's SC-8(a) freeze, or carries a `DRAFT` status at the tag (k2)**. *(Both of those\n"
          "last two are conditions (k2) states, and until R60 neither was indexed here \u2014 a limb may not impose\n"
          "a condition and leave nothing to enforce it. **Both are unmet as at the date of this amendment**:\n"
          "the freeze's \"specifically and exhaustively\" list does not name the manifest, and the manifest's\n"
          "recorded status is still `DRAFT - author review required`.)*")
assert s.count(OLD_K4.replace("\n", "\n> ")) + s.count(OLD_K4) >= 0
oq = "\n".join(("> " + x).rstrip() for x in OLD_K4.split("\n"))
nq = "\n".join(("> " + x).rstrip() for x in NEW_K4.split("\n"))
assert s.count(oq) == 1, "k4 source match %d" % s.count(oq)
s = s.replace(oq, nq, 1)

# ---- P5: list SC-4(k) among the differences ----------------------------------
LAST_F = ('| F-15 | \u00a70.1 cross-citation list (this file\'s \u00a70, not Part 1) | X | omitted SC-6(c)\'s '
          '"(SC-3)"/"(SC-4)" | added; S2/R32 citations added | Q4 nit |')
assert s.count(LAST_F) == 1, "F-15 row match %d" % s.count(LAST_F)
NEW_F = (LAST_F + "\n| F-16 | **SC-4(k)** | **A** | *(absent \u2014 SSA's SC-4 runs (a)\u2013(j))* | the whole of "
         "**(k)**: (k1) the floor, (k2) the reconciliation and (k2)(i) its provenance bar, (k3) the "
         "disclosure carve-out and the verifiability limit, (k4) the failure conditions | **R49/R5, "
         "restructured R49 addendum S1\u2013S3, extended R60/F3-B5.** *Listed at R60/F3: (k)'s applied lines "
         "were an unlisted difference under this table's own completeness claim.* |")
s = s.replace(LAST_F, NEW_F, 1)
ssf.write_text(s, encoding="utf-8")
print("SC-4(k4): both (k2) conditions indexed as failures")
print("PART 5  : F-16 added for SC-4(k)")

# ---- propagate (k4) into its hunk --------------------------------------------
hp = D / "_X5_hunks_v2.json"
d = json.loads(hp.read_text(encoding="utf-8"))
n = 0
for h in d["hunks"]:
    op = h.get("operative_text") or ""
    if OLD_K4 in op:
        h["operative_text"] = op.replace(OLD_K4, NEW_K4, 1)
        n += 1
assert n == 1, "k4 hunk match %d" % n
json.dump(d, open(hp, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("SC-4 hunk: (k4) updated from the same string")
