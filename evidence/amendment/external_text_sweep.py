#!/usr/bin/env python3
"""§88 — sweep every INSERTION POINT field for operative text living OUTSIDE
SCHEMA_SET_FINAL.md.

§88.4: SC-12's pointer was found because the generator needed it, not because
anyone looked. One instance found by accident is not evidence there is only one.

POPULATION (§30.1, stated with the result): every `**INSERTION POINT.**` field in
SCHEMA_SET_FINAL.md PART 1, read from the field header to the next blank-line
break. NO EXCLUSIONS - all 16 are scanned, and every filename-shaped reference in
each is reported, including ones that turn out to be benign.
"""
import pathlib, re, sys

REPO = pathlib.Path(__file__).resolve().parents[2]
SSF = REPO / "evidence/amendment/SCHEMA_SET_FINAL.md"
L = SSF.read_text(encoding="utf-8").split("\n")
part1_end = next(i for i, l in enumerate(L, 1) if l.startswith("# PART 2 "))

# a reference to text that lives somewhere else
# A filename regex is NOT enough and this sweep proved it on itself: SC-12's field
# reads "The operative pointer text is Y3 §6.3's" - a DOCUMENT IDENTIFIER with no
# extension. A sweep that only matched filenames returned 16/16 clean while the
# known instance sat in the population. Both forms are matched now.
FILEREF = re.compile(r"`?([A-Za-z0-9_\-]+\.(?:md|json|txt|py))`?"
                     r"|((?:Y|K|M|J|T|S|H|Q|X)\d+[a-z]?)\s*§"
                     r"|(Part\s+\d)"
                     r"|(item\s+[A-Z]\d+)")
TEXTREF = re.compile(r"text (?:is|at|in) |operative (?:text|pointer)|drafted (?:this pass|as)|"
                     r"Text at |see |below\b|Part \d", re.I)

fields = [i for i, l in enumerate(L, 1)
          if l.startswith("**INSERTION POINT.**") and i < part1_end]
print("§88 — INSERTION POINT fields scanned: %d  (population: all of PART 1, no exclusions)\n"
      % len(fields))

hits, clean = [], 0
for start in fields:
    end = next((i for i in range(start, part1_end)
                if not L[i - 1].strip() and i > start), start + 1)
    body = " ".join(L[start - 1:end])
    clause = None
    for i in range(start, 0, -1):
        m = re.match(r"^### (SC-[0-9a-z]+) — ", L[i - 1])
        if m:
            clause = m.group(1)
            break
    refs = sorted({g for m in FILEREF.finditer(body) for g in m.groups() if g})
    external = [r for r in refs if r not in ("PREREG.md", "SCHEMA_SET_FINAL.md")]
    if external:
        hits.append((clause, start, external, body))
    else:
        clean += 1

print("  fields naming NO external file : %d" % clean)
print("  fields naming an external file : %d\n" % len(hits))

for clause, start, external, body in hits:
    print("  %-8s ssf l.%-5d -> %s" % (clause, start, ", ".join(external)))
    print("      %s" % body[:190].replace("**", ""))
    for f in external:
        if f.startswith("Part "):
            print("        %-30s INTERNAL to SCHEMA_SET_FINAL.md - not an external file" % f)
            continue
        cands = sorted((REPO / "evidence/amendment").glob(f + "_*")) +                 sorted((REPO / "evidence/amendment").glob(f + ".*"))
        where = cands[0].name if cands else "(no file found)"
        in_repo = bool(cands)
        print("        %-30s -> %-34s in repo: %s" % (f, where, in_repo))
    print()

print("=" * 72)
print("Every field naming a non-PREREG, non-SSF file is listed above. A field")
print("naming only PREREG.md (the target) or SSF itself carries no external")
print("dependency. %d of %d fields are in that clean category." % (clean, len(fields)))
sys.exit(0)
