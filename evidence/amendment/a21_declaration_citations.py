"""A21 -- every clause the declaration cites in `PREREG.md`, against `PREREG.md`.

READ-ONLY.

WHY THIS EXISTS. A20 established that `PREREG.md` is byte-identical to the
approved amendment, so the defect is in the documents that DESCRIBE it. The tag
message is one. `AVAILABILITY_DECLARATION.md` is another -- and it is not a
drafting record. It is one of the TWENTY FILES the tag message hashes, frozen at
the tag by its own §D.1, and `PREREG.md` SC-7(a) names its declared elements as
a gate input. A citation in it to a clause that does not exist is a defect
inside the signed set.

DERIVE, DON'T SAMPLE (§2.1). The question is "does every clause the declaration
names in PREREG.md exist in PREREG.md". So: extract every such citation from the
declaration, and resolve each against the file. Not a search for suspicious
ones -- all of them, with the resolution shown.

THE CITATION FORM IS THE DECLARATION'S OWN. §A's conformance walk names an
amended clause as `PREREG.md` §<n> "<heading> - v30a, operative", and names new
clauses as SC-<n>. Both are extracted. A form this instrument does not know
about would be missed, so the count of citations found is asserted against the
count of `v30a, operative` occurrences, and a shortfall is reported rather than
passed over.

    usage: a21_declaration_citations.py <out.json>
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:                                       # noqa: BLE001
    pass

REPO = pathlib.Path(__file__).resolve().parents[2]
DECL = REPO / "AVAILABILITY_DECLARATION.md"
PREREG = REPO / "PREREG.md"
OUT = pathlib.Path(sys.argv[1])


def text_of(p):
    return p.read_text(encoding="utf-8").replace("\r\n", "\n")


decl_lines = text_of(DECL).split("\n")
prereg = text_of(PREREG)
prereg_lines = prereg.split("\n")

print("=" * 78)
print("POPULATION, ASSERTED BEFORE ANYTHING IS RESOLVED")
print("=" * 78)
print("  AVAILABILITY_DECLARATION.md : %d lines" % (len(decl_lines) - 1))
print("  PREREG.md                   : %d lines" % (len(prereg_lines) - 1))

# --- the two citation forms -------------------------------------------------
OPERATIVE = re.compile(r'"([^"]{6,80}?)\s+[—-]\s+v30a,\s*operative"')
SC = re.compile(r"\bSC-\d+[a-z]?(?:\([a-z0-9]+\))?")

op_hits, sc_hits = [], []
for i, l in enumerate(decl_lines, 1):
    for m in OPERATIVE.finditer(l):
        op_hits.append({"line": i, "clause": m.group(1).strip()})
    for m in SC.finditer(l):
        sc_hits.append({"line": i, "clause": m.group(0)})

total_v30a_operative = sum(l.count("v30a, operative") for l in decl_lines)
print("  citations of the form '<heading> — v30a, operative' : %d" % len(op_hits))
print("  raw occurrences of the string 'v30a, operative'     : %d" % total_v30a_operative)
if len(op_hits) < total_v30a_operative:
    print("  ** %d occurrence(s) did not match the extraction pattern and are "
          "NOT resolved below. Reported, not passed over."
          % (total_v30a_operative - len(op_hits)))
    for i, l in enumerate(decl_lines, 1):
        if "v30a, operative" in l and not OPERATIVE.search(l):
            print("     unmatched at decl l.%d: %s" % (i, l.strip()[:100]))
print("  citations of the form 'SC-n'                        : %d (%d distinct)"
      % (len(sc_hits), len({h["clause"] for h in sc_hits})))
print()

# --- resolve ----------------------------------------------------------------
print("=" * 78)
print("NAMED OPERATIVE CLAUSES -- does PREREG.md contain each?")
print("=" * 78)
rows = []
for h in sorted({(x["clause"], x["line"]) for x in op_hits}):
    clause, line = h
    # THE CITATION IS TO A v30a OPERATIVE CLAUSE, SO THE PROBE MUST REQUIRE THE
    # v30a MARKER. A first version searched for the heading's stem alone and
    # reported "Contamination availability class" and "Sliced variant" as
    # RESOLVING at PREREG.md l.579 and l.580 -- which are v30's OWN UNAMENDED
    # BULLETS, the very lines A20 established were never replaced. The probe
    # found the thing the citation says was superseded and called that
    # resolution. A guard that passes for the wrong reason is worse than one
    # that fails.
    stem = clause.split("—")[0].strip().rstrip(",")
    def _is_hit(l):
        return bool(stem) and stem in l and "v30a" in l
    present = any(_is_hit(l) for l in prereg_lines)
    at = next((i for i, l in enumerate(prereg_lines, 1) if _is_hit(l)), None)
    near = next((i for i, l in enumerate(prereg_lines, 1) if stem and stem in l), None)
    rows.append({"kind": "operative", "clause": clause, "decl_line": line,
                 "resolves": present, "prereg_line": at,
                 "v30_stem_at": near})
    where = ("PREREG.md l.%d" % at if at else
             "NOT in PREREG.md — the stem appears at l.%d, but that is v30's "
             "own unamended line, not a v30a clause" % near if near else
             "not in PREREG.md at all")
    print("  %-11s decl l.%-6d %-40s %s"
          % ("RESOLVES" if present else "** MISSING", line, clause[:40], where))

print()
print("=" * 78)
print("SC-n CLAUSES -- does PREREG.md carry each tag?")
print("=" * 78)
missing_sc = []
for clause in sorted({h["clause"] for h in sc_hits}):
    base = re.match(r"SC-\d+[a-z]?", clause).group(0)
    present = ("[%s]" % base) in prereg or ("**%s" % base) in prereg or \
              re.search(r"\b%s\b" % re.escape(base), prereg) is not None
    if not present:
        missing_sc.append(clause)
        first = next(h["line"] for h in sc_hits if h["clause"] == clause)
        print("  ** MISSING  %-12s first cited at declaration l.%d" % (clause, first))
if not missing_sc:
    print("  every SC-n the declaration cites appears in PREREG.md")

miss = [r for r in rows if not r["resolves"]]
print()
print("=" * 78)
print("SUMMARY")
print("=" * 78)
print("  named operative clauses cited : %d" % len(rows))
print("  ** DO NOT EXIST in PREREG.md  : %d" % len(miss))
for r in miss:
    print("      decl l.%-6d %s" % (r["decl_line"], r["clause"]))
print("  SC-n citations that do not resolve : %d" % len(missing_sc))
print()
if miss:
    print("  These are citations in a file the tag message HASHES, to clauses")
    print("  that are not in the file it describes. Not a drafting record --")
    print("  the declaration is frozen at the tag by its own §D.1 and SC-7(a)")
    print("  names its declared elements as a gate input.")

OUT.write_text(json.dumps({"operative": rows, "missing_sc": missing_sc},
                          indent=1), encoding="utf-8")
print("wrote %s" % OUT)
