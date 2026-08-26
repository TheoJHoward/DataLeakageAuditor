#!/usr/bin/env python3
"""§83 — generate the v30a approval diff FROM RECORDS.

§57.3(d)  reads SCHEMA_RECORDS.json; the only thing it takes from
          SCHEMA_SET_FINAL.md is the declared byte span, whose digest it VERIFIES
          before use. It never parses prose.
§77.2     applies BOTTOM-TO-TOP, descending anchor position, so an earlier
          insertion never shifts a later anchor.
§77.3     deterministic: no timestamps, sorted ordering, byte-identical on
          repeat runs.
§83.2     emits FULL CLAUSE TEXT into the diff - an author cannot approve a digest.

DOES NOT APPLY ANYTHING. Writes a diff for approval and exits.
"""
import difflib, hashlib, json, pathlib, sys

REPO = pathlib.Path(__file__).resolve().parents[2]
SSF = REPO / "evidence/amendment/SCHEMA_SET_FINAL.md"
REC = REPO / "evidence/amendment/SCHEMA_RECORDS.json"
PRE = REPO / "PREREG.md"
OUT = REPO / "evidence/amendment/PREREG_v30a_APPROVAL.diff"

data = json.loads(REC.read_text(encoding="utf-8"))
records = data["records"]
ssf_lines = SSF.read_text(encoding="utf-8").split("\n")     # universal newlines -> LF
pre_lines = PRE.read_text(encoding="utf-8").split("\n")
original = list(pre_lines)


def clause_text(r):
    """Slice the declared span and VERIFY its digest before using it."""
    lo, hi = r["clause_first_line"], r["clause_last_line"]
    text = "\n".join(ssf_lines[lo - 1:hi])
    got = hashlib.sha256(text.encode("utf-8")).hexdigest()
    if got != r["clause_sha256"]:
        sys.exit("HALT %s: declared span l.%d-%d digests %s, record says %s. The source "
                 "moved; re-pin by LOCATING HEADERS (see _repin_procedure), never by offset."
                 % (r["id"], lo, hi, got[:16], r["clause_sha256"][:16]))
    return text.split("\n")


def resolve(r, lines):
    """Anchor -> 1-based line index. Exactly once, or halt (§57.3(c))."""
    q = r["anchor_quoted"]
    if q:
        hits = [i for i, l in enumerate(lines, 1) if q in l]
        if len(hits) != 1:
            sys.exit("HALT %s: anchor resolves %d times: %s (§66.2 - the author's call)"
                     % (r["id"], len(hits), hits[:8]))
        return hits[0]
    ln = r["prereg_line"]
    target = lines[ln - 1]
    if sum(1 for l in lines if l == target and l.strip()) != 1:
        sys.exit("HALT %s: line-anchored content at l.%d is not unique" % (r["id"], ln))
    return ln


# ---- resolve every absolute anchor against the ORIGINAL file ----------------
placed = {}
for r in records:
    if r["operation"] != "INSERT_AFTER_RELATIVE":
        placed[r["id"]] = resolve(r, original)

# a relative record shares its parent's anchor; ordering among siblings at the
# same anchor is by declared order, which the tie-break below preserves.
order = {r["id"]: i for i, r in enumerate(records)}
for r in records:
    if r["operation"] == "INSERT_AFTER_RELATIVE":
        placed[r["id"]] = placed[r["relative_to"]]

# ---- §77.2 BOTTOM-TO-TOP ----------------------------------------------------
# Descending anchor line. Within one anchor, descending declared order, so that
# after all insertions the siblings read in their declared order top-to-bottom.
plan = sorted(records, key=lambda r: (placed[r["id"]], order[r["id"]]), reverse=True)

new_lines = list(original)
applied = []
for r in plan:
    at = placed[r["id"]]
    body = clause_text(r)
    header = ["", "<!-- v30a %s — %s -->" % (r["id"], r["operation"]), ""]
    block = header + body + [""]
    if r["operation"] in ("REPLACE_LINE", "REPLACE_ROW_THEN_INSERT"):
        new_lines[at - 1:at] = block
    else:
        new_lines[at:at] = block
    applied.append((r["id"], at, r["operation"], len(block)))

diff = list(difflib.unified_diff(original, new_lines,
                                 fromfile="PREREG.md (v30, blob 75bd93dec436)",
                                 tofile="PREREG.md (v30a, PROPOSED - NOT APPLIED)",
                                 lineterm="", n=3))
OUT.write_text("\n".join(diff) + "\n", encoding="utf-8")

ins = sum(1 for d in diff if d.startswith("+") and not d.startswith("+++"))
dele = sum(1 for d in diff if d.startswith("-") and not d.startswith("---"))
hunks = sum(1 for d in diff if d.startswith("@@"))
digest = hashlib.sha256(OUT.read_bytes()).hexdigest()

print("applied bottom-to-top (§77.2):")
for cid, at, op, n in applied:
    print("  l.%-5d %-10s %-24s %d lines" % (at, cid, op, n))
print("\n  base   %d lines -> proposed %d lines" % (len(original) - 1, len(new_lines) - 1))
print("  diff   +%d  -%d  hunks %d" % (ins, dele, hunks))
print("  DIFF  sha256 %s" % digest)
print("  SSF   sha256 %s" % hashlib.sha256(SSF.read_bytes()).hexdigest())
print("  PREREG unchanged: %s" % (PRE.read_text(encoding="utf-8").split("\n") == original))
