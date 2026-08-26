#!/usr/bin/env python3
"""§53.2 / §84.1 — THE LOAD-BEARING CHECK.

Every inserted line must fall inside a declared clause range. A line in the diff
outside every range is content NO CLAUSE PRODUCED - undecided text entering a
locked registration under cover of an approved amendment.

Also §53.3, the other direction: every SC- clause in SCHEMA_SET_FINAL.md that
does NOT appear in the diff.
"""
import json, pathlib, re, sys

REPO = pathlib.Path(__file__).resolve().parents[2]
SSF = REPO / "evidence/amendment/SCHEMA_SET_FINAL.md"
REC = REPO / "evidence/amendment/SCHEMA_RECORDS.json"
DIFF = REPO / "evidence/amendment/PREREG_v30a_APPROVAL.diff"

L = SSF.read_text(encoding="utf-8").split("\n")
records = json.loads(REC.read_text(encoding="utf-8"))["records"]
diff = DIFF.read_text(encoding="utf-8").split("\n")

# every line the records authorise, plus the generator's own framing
authorised = set()
for r in records:
    for i in range(r["clause_first_line"], r["clause_last_line"] + 1):
        authorised.add(L[i - 1])
FRAMING = re.compile(r"^<!-- v30a \S+ — [A-Z_]+ -->$")

added = [l[1:] for l in diff if l.startswith("+") and not l.startswith("+++")]
removed = [l[1:] for l in diff if l.startswith("-") and not l.startswith("---")]

untraceable, framing, blank = [], 0, 0
for line in added:
    if not line.strip():
        blank += 1
    elif FRAMING.match(line):
        framing += 1
    elif line in authorised:
        pass
    else:
        untraceable.append(line)

print("§53.2 — UNTRACEABLE LINES (content no clause produced)\n")
print("  inserted lines total            : %d" % len(added))
print("    blank (generator spacing)     : %d" % blank)
print("    generator framing comments    : %d" % framing)
print("    inside a declared clause range: %d" % (len(added) - blank - framing - len(untraceable)))
print("    ** UNTRACEABLE **             : %d" % len(untraceable))
if untraceable:
    print("\n  Every line below is in the diff but in no declared clause range:")
    for u in untraceable[:40]:
        print("    %r" % u[:100])
else:
    print("\n  HOW THIS WAS ESTABLISHED (B6.2 - not asserted):")
    print("    The authorised set is built by expanding EVERY record's")
    print("    [clause_first_line .. clause_last_line] into its literal source lines.")
    print("    Each added line is then tested for membership in that set. The only")
    print("    lines exempt are blanks and the generator's own '<!-- v30a ID -->'")
    print("    framing, both counted above rather than waived. A line that is neither")
    print("    blank, nor framing, nor a member, is reported - there is no residual")
    print("    category. %d of %d non-blank non-framing lines were members." %
          (len(added) - blank - framing, len(added) - blank - framing))

print("\n§53.3 — the other direction: clauses in the source NOT in the diff\n")
clauses = re.findall(r"^### (SC-[0-9a-z]+) — ", "\n".join(L), re.M)
in_diff = {m.group(1) for m in (re.match(r"^\+<!-- v30a (\S+) — ", d) for d in diff) if m}
# Longest-prefix mapping, same fix as the verifier: SC-6a and SC-6b both belong
# to clause SC-6. A naive prefix regex reported SC-6, SC-8 and SC-11 as absent
# from a diff that in fact carries both of each one's insertion points.
def clause_of(rid):
    return max((c for c in clauses if rid.startswith(c)), key=len, default=None)
base = {clause_of(i) for i in in_diff}
missing = [c for c in clauses if c not in base]
print("  clause blocks in PART 1 : %d" % len(clauses))
print("  represented in the diff : %d" % (len(clauses) - len(missing)))
if missing:
    print("  ** NOT IN THE DIFF: %s **" % missing)
print("\n  removed lines (supersessions/replacements): %d" % len(removed))
for r_ in removed:
    print("    - %r" % r_[:96])
sys.exit(1 if (untraceable or missing) else 0)
