#!/usr/bin/env python3
"""DELTA R47 / P5 — the map artifact is not the map.

P5 requires the amendment to SAY that criterion 3 does not adjudicate the 24
SCORED_DIAGNOSTIC_11TH_CLASS rows.

The RULE already exists and is registered: SC-10(c) ("diagnostic classes are not
declared classes ... not members of the declared scored set"), which the
declaration cites by name at its line 2038 to declare `mbo_all_rows` the 11th
class. SC-10(e) forbids restating it - "these rules are stated here and cited
elsewhere". So this is a CITATION, not a second copy.

What is genuinely unstated, and is the reason three reports read 888 as the
population: SC-3(a) says the artifact holds "one row per scored cell". The
artifact holds 984 rows of which 888 are SCORED. Nothing anywhere says the
artifact may carry rows that are not cells of the map. This states it.

Source of record is SCHEMA_SET_FINAL.md (M1: manifest -> JSON -> artifact), so
the source and the hunk are edited in ONE pass from ONE string; they cannot
drift apart.
"""
import json
import pathlib

D = pathlib.Path(
    "C:/Users/ttbea/AppData/Local/Temp/claude/"
    "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
    "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/amendment")

OLD = ("published as an artifact with a **declared schema**: one row per scored cell, with every field\n"
       "named, including the field that records whether the cell is scored.")

NEW = ("published as an artifact with a **declared schema**: one row per cell of the declared scored\n"
       "population, with every field named, including the field that records whether the cell is\n"
       "scored. **The artifact may in addition carry rows of a class the declaration declares\n"
       "DIAGNOSTIC (SC-10(c)); those rows are not cells of the map.** They are adjudicated by no\n"
       "criterion, enter no denominator and no rate, and **(b)'s dispositions are exhaustive over the\n"
       "map's cells, not over the artifact's row count**. A count taken from the artifact without\n"
       "excluding them counts a different population, and **every figure published from the artifact\n"
       "names which population it counts**.")

# ---- 1. the source of record -------------------------------------------------
ssf = D / "SCHEMA_SET_FINAL.md"
src = ssf.read_text(encoding="utf-8")
old_q = "\n".join("> " + ln for ln in OLD.split("\n"))
new_q = "\n".join("> " + ln for ln in NEW.split("\n"))
assert src.count(old_q) == 1, "source match count %d, expected 1" % src.count(old_q)
ssf.write_text(src.replace(old_q, new_q, 1), encoding="utf-8")
print("SCHEMA_SET_FINAL.md : 1 match replaced (SC-3(a), quoted form)")

# ---- 2. the hunk, from the SAME string ---------------------------------------
p = D / "_X5_hunks_v2.json"
d = json.loads(p.read_text(encoding="utf-8"))
n = 0
for h in d["hunks"]:
    op = h.get("operative_text") or ""
    if OLD in op:
        h["operative_text"] = op.replace(OLD, NEW, 1)
        n += 1
        print("hunk updated        : %s (line %s)" % ((h.get("clause") or "")[:40], h.get("prereg_line")))
assert n == 1, "hunk match count %d, expected 1" % n
json.dump(d, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)

# ---- 3. prove they agree -----------------------------------------------------
src2 = ssf.read_text(encoding="utf-8")
d2 = json.loads(p.read_text(encoding="utf-8"))
hit = [h for h in d2["hunks"] if NEW in (h.get("operative_text") or "")]
assert len(hit) == 1 and new_q in src2
print("\nAGREEMENT PROVEN: the new text is in the source (quoted) and in exactly one hunk.")
print("\n--- NEW SC-3(a) TAIL ---\n" + NEW)
