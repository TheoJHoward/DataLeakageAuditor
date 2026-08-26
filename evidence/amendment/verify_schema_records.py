#!/usr/bin/env python3
"""§57.3(b)+(c)+§77.1 — verify the structured file against its source and its target.

(b) BOTH DIRECTIONS, exact substring:
      - every record's anchor_source appears VERBATIM in SCHEMA_SET_FINAL.md
      - every clause block in SCHEMA_SET_FINAL.md PART 1 has at least one record
    Neither direction alone suffices (§37's lesson).

(c) Every insertion anchor resolves in the CURRENT PREREG.md EXACTLY ONCE.
    Zero matches or two matches is a HALT, not a warning.

§77.1 The anchor is COPIED, not chosen: anchor_quoted must appear inside
    anchor_source, which must itself appear verbatim in the source file. That
    closes the failure both-direction verification cannot see - a record that is
    verbatim-correct but attached to the wrong anchor.
"""
import json, pathlib, re, sys, unicodedata

REPO = pathlib.Path(__file__).resolve().parents[2]
SSF = REPO / "evidence/amendment/SCHEMA_SET_FINAL.md"
REC = REPO / "evidence/amendment/SCHEMA_RECORDS.json"
PRE = REPO / "PREREG.md"

# R93 - THE ANCHORS ARE ANCHORS INTO THE BASE, so the base is what they are
# resolved against. "the CURRENT PREREG.md" below was written when current WAS
# the base; after the v30a diff was applied on 25 Aug 2026 the working file is
# the RESULT, and resolving an insertion anchor against the result asks a
# question this check never claimed to answer: SC-8b's target line is superseded
# by the amendment, so it occurs 0 times in the applied file and every other
# anchor reports MOVED. Reading the registered base from the tag keeps the check
# asking what it was built to ask - exactly-once resolution is still required and
# nothing is relaxed.
def _base():
    import subprocess
    return subprocess.run(["git", "show", "prereg-v30:PREREG.md"], cwd=str(REPO),
                          capture_output=True, check=True).stdout.decode("utf-8")


ssf = SSF.read_text(encoding="utf-8")
pre = _base()
pre_lines = pre.split("\n")
data = json.loads(REC.read_text(encoding="utf-8"))
records = data["records"]

part1 = ssf[ssf.index("# PART 1 "):ssf.index("# PART 2 ")]


def norm(s):
    """Collapse whitespace, drop JSON backslash-escapes, normalise unicode.

    The backslash strip matters: anchor_source quotes text that itself contains
    quotes, so JSON stores them as \\" and a naive comparison reports 7 records
    untraceable when all 7 are transcribed correctly.
    """
    s = unicodedata.normalize("NFC", s).replace('\\"', '"').replace("\\\\", "\\")
    return re.sub(r"\s+", " ", s).strip()


ssf_norm = norm(part1)
fail = []

# ---- (b) direction 1: every record traces to the source ---------------------
print("=== §57.3(b) DIRECTION 1 - every record's anchor_source is verbatim in the source ===")
d1 = 0
for r in records:
    src = r["anchor_source"]
    body = src.split(": ", 1)[1] if ": " in src else src
    body = body.strip().strip('"')
    frags = [f for f in re.split(r"…|\.\.\.", body) if len(norm(f)) > 25]
    hit = all(norm(f) in ssf_norm for f in frags) if frags else norm(body) in ssf_norm
    d1 += hit
    if not hit:
        fail.append("%s: anchor_source not found verbatim in PART 1" % r["id"])
        print("  %-10s NOT FOUND" % r["id"])
print("  traced to source: %d / %d" % (d1, len(records)))

# ---- (b) direction 2: every source clause has a record ----------------------
print("\n=== §57.3(b) DIRECTION 2 - every PART 1 clause block has a record ===")
clauses = re.findall(r"^### (SC-[0-9a-z]+) — ", part1, re.M)
# A record id maps to the LONGEST clause header it starts with: SC-6a and SC-6b
# both belong to clause SC-6; SC-13c-1 and SC-13c-2 both belong to SC-13c. A
# naive split reported SC-6, SC-8 and SC-11 as uncovered when each has records.
def clause_of(rid):
    return max((c for c in clauses if rid.startswith(c)), key=len, default=None)
covered = {clause_of(r["id"]) for r in records}
missing = [c for c in clauses if c not in covered]
print("  clause blocks in PART 1 : %d  (%s)" % (len(clauses), ", ".join(clauses)))
print("  covered by a record     : %d" % (len(clauses) - len(missing)))
if missing:
    fail.append("clauses with no record: %s" % missing)
    print("  *** NO RECORD: %s ***" % missing)

# ---- §77.1: the anchor is copied, not chosen --------------------------------
print("\n=== §77.1 - anchor_quoted is COPIED from anchor_source ===")
c77 = q77 = 0
for r in records:
    if r["anchor_quoted"] is None:
        continue
    q77 += 1
    if norm(r["anchor_quoted"]) in norm(r["anchor_source"]):
        c77 += 1
    else:
        fail.append("%s: anchor_quoted is not inside its own anchor_source" % r["id"])
        print("  %-10s NOT COPIED" % r["id"])
print("  quoted anchors: %d   copied from their own INSERTION POINT: %d" % (q77, c77))

# ---- (c) anchors resolve EXACTLY ONCE in the current PREREG.md --------------
print("\n=== §57.3(c) - every anchor resolves in PREREG.md EXACTLY ONCE ===")
halts = []
for r in records:
    if r.get("operation") == "INSERT_AFTER_RELATIVE":
        print("  %-10s relative to %-8s (resolved after its parent applies)"
              % (r["id"], r["relative_to"]))
        continue
    q = r["anchor_quoted"]
    ln = r["prereg_line"]
    if q:
        hits = [i for i, l in enumerate(pre_lines, 1) if q in l]
        if len(hits) == 1 and hits[0] == ln:
            print("  %-10s OK        l.%-5d exactly once" % (r["id"], ln))
        elif len(hits) == 1:
            print("  %-10s MOVED     cited l.%d, resolves at l.%d" % (r["id"], ln, hits[0]))
            halts.append((r["id"], q, hits, ln, "resolves once but NOT at the cited line"))
        else:
            print("  %-10s **HALT**  %d matches: %s" % (r["id"], len(hits), hits[:6]))
            halts.append((r["id"], q, hits, ln, "zero" if not hits else "multiple"))
    else:
        actual = pre_lines[ln - 1] if 1 <= ln <= len(pre_lines) else "(out of range)"
        cnt = sum(1 for l in pre_lines if l == actual and l.strip())
        if cnt == 1:
            print("  %-10s OK        l.%-5d line-anchored, unique: %r"
                  % (r["id"], ln, actual.strip()[:44]))
        else:
            print("  %-10s **HALT**  l.%d content occurs %d times" % (r["id"], ln, cnt))
            halts.append((r["id"], actual.strip()[:60], [], ln, "line content not unique"))

print("\n" + "=" * 72)
if halts:
    print("HALTS: %d  (§66.2 - an anchor matching twice is the author's call, not mine)" % len(halts))
    for cid, anchor, hits, ln, why in halts:
        print("\n  %s  [%s]" % (cid, why))
        print("    anchor text : %r" % anchor[:90])
        print("    cited line  : %d" % ln)
        print("    candidates  : %s" % (hits[:8] if hits else "none"))
        for h in hits[:4]:
            print("        l.%-5d %r" % (h, pre_lines[h - 1].strip()[:76]))
if fail:
    print("\nVERIFICATION FAILURES: %d" % len(fail))
    for f in fail:
        print("  " + f)
if not halts and not fail:
    print("ALL CHECKS PASS")
sys.exit(1 if (halts or fail) else 0)
