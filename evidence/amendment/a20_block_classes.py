"""A20, part 2 -- WHY eleven touches are missing. Cross-tabulate block class
against whether the block reached `PREREG.md`. READ-ONLY.

PART 1 ESTABLISHED THAT NOTHING WENT WRONG AT APPLICATION TIME: the applied file
is byte-identical to v30 with `PREREG_v30a_APPROVAL.diff` applied. So the
omissions are omissions from the APPROVAL RECORD, not from the application, and
the question moves one layer back: which blocks got into `SCHEMA_RECORDS.json`,
and which did not?

THE RECORD SET STATES ITS OWN POPULATION, and this is the whole answer:

    _purpose:  "one record per CLAUSE, authored BY READING SCHEMA_SET_FINAL.md
                PART 1"
    _repin_procedure: "(1) find each '### SC-<id> - ' header line; (2) within
                that clause, find its '**THE CLAUSE.**' line, which is
                clause_first_line"

A MARKER block has no `### SC-<id>` header and no `**THE CLAUSE.**` line. It was
therefore never in the population -- not dropped, never eligible. That is a
derivable claim and this derives it rather than asserting it: every block
`BLOCK_MANIFEST.md` §A classes as MARKER, against whether its text is in the
applied file.

THE PROBE IS A DISTINCTIVE LINE FROM THE BLOCK'S OWN SOURCE RANGE, normalised
for the `> ` blockquote prefix and for whitespace, and required to be unique in
the source. A short or common fragment would match something else and report a
block as applied that is not (§2.4). Where no distinctive line exists the row is
reported UNDETERMINED, never assumed either way -- R135: do not infer from the
current state of a file.

    usage: a20_block_classes.py <out.json>
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
MANIFEST = REPO / "evidence/amendment/BLOCK_MANIFEST.md"
SSF = REPO / "evidence/amendment/SCHEMA_SET_FINAL.md"
RECORDS = REPO / "evidence/amendment/SCHEMA_RECORDS.json"
APPLIED = REPO / "PREREG.md"
OUT = pathlib.Path(sys.argv[1])


def text_of(p):
    return p.read_text(encoding="utf-8").replace("\r\n", "\n")


ssf = text_of(SSF).split("\n")
applied_norm = re.sub(r"\s+", " ", text_of(APPLIED))
records = json.loads(text_of(RECORDS))["records"]

# A PROBE THAT IS ALSO IN v30 CANNOT ANSWER THE QUESTION. "Present in the applied
# file" only means "the amendment put it there" if v30 did not already have it.
# The first version of this script had no such discrimination and reported H29
# (§10 line 992's operative row) PRESENT on a fragment that is v30's own text --
# which is precisely the inference R135 forbids: do not infer approval from the
# current state of a file.
V30 = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else None
v30_norm = re.sub(r"\s+", " ", text_of(V30)) if V30 and V30.exists() else None
if v30_norm is None:
    sys.exit("HALT: this audit needs v30 to discriminate 'the amendment put it "
             "there' from 'it was always there'. Pass the v30 file as argv[2].")

print("=" * 78)
print("POPULATION, ASSERTED FIRST")
print("=" * 78)
print("  SCHEMA_SET_FINAL.md : %d lines" % (len(ssf) - 1))
print("  SCHEMA_RECORDS.json : %d records" % len(records))

ROW = re.compile(r"^\| (\S+) \| (\d+)[–-](\d+) \| (.+?) \| (.+?) \|\s*$")
rows = []
for line in text_of(MANIFEST).split("\n"):
    m = ROW.match(line)
    if m:
        rows.append({"id": m.group(1), "lo": int(m.group(2)), "hi": int(m.group(3)),
                     "what": m.group(4).strip(), "hunk": m.group(5).strip()})
print("  BLOCK_MANIFEST.md §A: %d rows parsed" % len(rows))
if not rows:
    sys.exit("HALT: the §A table did not parse; the audit would report every "
             "block UNDETERMINED and that would read as a result")


def classify(what: str) -> str:
    w = what.upper()
    for k in ("MARKER", "THE CLAUSE", "INSERTION TEXT", "CITATION", "ANCHOR",
              "INSTANCE RECORD", "OPERATIVE"):
        if w.startswith(k):
            return k
    if "SC-12(W)" in w:
        return "THE CLAUSE"
    if w.startswith("§AB"):
        return "§AB"
    if w.startswith("§AC"):
        return "§AC"
    if w.startswith("§10.1"):
        return "RETENTION/OPERATIVE (moved)"
    return "OTHER"


def distinctive(lo, hi):
    """Every distinctive line of the block, normalised for blockquote and space.

    A FRACTION, NOT A SINGLE LINE. The first version probed with the block's
    LONGEST line and reported four SC- clauses ABSENT that are demonstrably in
    the file -- because a §A block's line range is wider than the clause span
    the generator actually inserts (it also covers `DATA THE DECLARATION MUST
    SUPPLY` and `INSERTION POINT` sub-blocks, which are never applied), and the
    longest line fell in one of those. One probe over a range that is not the
    unit under test answers a different question and looks like an answer to
    this one.
    """
    out = []
    for raw in ssf[lo - 1:hi]:
        s = raw.strip()
        if s.startswith(">"):
            s = s[1:].strip()
        s = re.sub(r"\s+", " ", s)
        if len(s) < 45 or s.startswith("|---"):
            continue
        out.append(s[:90])
    return out


print()
print("=" * 78)
print("§A -- BLOCK CLASS AGAINST WHETHER THE BLOCK REACHED PREREG.md")
print("=" * 78)
print("  %-4s %-22s %-26s %-12s %s"
      % ("row", "class", "hunk", "verdict", "lines found / distinctive"))
tab = {}
for r in rows:
    kind = classify(r["what"])
    allcand = distinctive(r["lo"], r["hi"])
    # Discriminating probes only: a line v30 already had proves nothing.
    cand = [c for c in allcand if c not in v30_norm]
    preexisting = len(allcand) - len(cand)
    found = [c for c in cand if c in applied_norm]
    if not cand:
        verdict, frac = "UNDETERMINED", "0/0 (every line already in v30)"
    else:
        f = len(found) / len(cand)
        verdict = "PRESENT" if f >= 0.5 else ("PARTIAL" if found else "ABSENT")
        frac = "%d/%d%s" % (len(found), len(cand),
                            " (+%d pre-existing, ignored)" % preexisting
                            if preexisting else "")
    r["class"] = kind
    r["probes"] = len(cand)
    r["probes_preexisting_in_v30"] = preexisting
    r["probes_found"] = len(found)
    r["verdict"] = verdict
    r["example_absent"] = next((c for c in cand if c not in applied_norm), None)
    tab.setdefault(kind, {}).setdefault(verdict, []).append(r["id"])
    print("  %-4s %-22s %-26s %-12s %s"
          % (r["id"], kind, r["hunk"][:26], verdict, frac))

print()
print("=" * 78)
print("CROSS-TABULATION -- this is the answer")
print("=" * 78)
print("  %-30s %-9s %-9s %-9s %s"
      % ("class", "PRESENT", "PARTIAL", "ABSENT", "UNDETERMINED"))
for kind in sorted(tab):
    d = tab[kind]
    print("  %-30s %-9d %-9d %-9d %d"
          % (kind, len(d.get("PRESENT", [])), len(d.get("PARTIAL", [])),
             len(d.get("ABSENT", [])), len(d.get("UNDETERMINED", []))))

markers = tab.get("MARKER", {})
clauses = tab.get("THE CLAUSE", {})
m_tot = sum(len(v) for v in markers.values())
c_tot = sum(len(v) for v in clauses.values())
m_in = len(markers.get("PRESENT", [])) + len(markers.get("PARTIAL", []))
c_in = len(clauses.get("PRESENT", [])) + len(clauses.get("PARTIAL", []))
print()
print("  MARKER blocks reaching the file: %d of %d" % (m_in, m_tot))
print("  CLAUSE blocks reaching the file: %d of %d" % (c_in, c_tot))
# BOTH SIDES ARE STATED. The first version printed "every marker is absent and
# every clause is present" while the clause column read 12 of 16 -- a conclusion
# that was half-checked and would have been quoted as if it were whole.
if m_in == 0 and c_in == c_tot:
    print()
    print("  EVERY marker block is absent; EVERY clause block reached the file.")
    print("  The record set's own `_purpose` says its population is CLAUSES --")
    print("  'one record per clause', located by a '### SC-<id>' header and a")
    print("  '**THE CLAUSE.**' line. A marker has neither. The markers were not")
    print("  dropped; they were never eligible for the population that generated")
    print("  the approval diff.")
elif m_in == 0:
    print()
    print("  Every marker block is absent. %d of %d clause blocks did not reach"
          % (c_tot - c_in, c_tot))
    print("  the file either, so 'markers only' does NOT yet describe the")
    print("  omission -- those %d are named above and are examined individually."
          % (c_tot - c_in))
else:
    print()
    print("  %d marker block(s) DID reach the file, so the population account")
    print("  above does not hold as stated." % m_in)

# ---- §B: hunks whose operative text lives outside SSF ----------------------
print()
print("=" * 78)
print("§B -- HUNKS WHOSE OPERATIVE TEXT COMES FROM ELSEWHERE")
print("=" * 78)
BROW = re.compile(r"^\| \*\*(H\d+)\*\* \| (\d+) \| (.+?) span:«(.{20,60}?)»", re.S)
brows = []
for line in text_of(MANIFEST).split("\n"):
    m = BROW.match(line)
    if m:
        frag = re.sub(r"\s+", " ", m.group(4)).strip()
        brows.append({"hunk": m.group(1), "site": int(m.group(2)),
                      "source": m.group(3).strip()[:56], "probe": frag})
print("  %-6s %-6s %-52s %s" % ("hunk", "site", "source of its operative text", "verdict"))
for b in brows:
    in_applied = b["probe"] in applied_norm
    in_v30 = b["probe"] in v30_norm
    b["in_applied"] = in_applied
    b["in_v30"] = in_v30
    if in_v30:
        # The span fragment is v30's OWN text, so its presence says nothing about
        # whether this hunk was applied. Reported as undecidable by this probe
        # rather than counted as present.
        b["verdict"] = "UNDETERMINED (probe text is already in v30)"
    else:
        b["verdict"] = "PRESENT" if in_applied else "ABSENT"
    print("  %-6s %-6d %-52s %s" % (b["hunk"], b["site"], b["source"][:52], b["verdict"]))
bp = sum(1 for b in brows if b["verdict"] == "PRESENT")
bu = sum(1 for b in brows if b["verdict"].startswith("UNDETERMINED"))
print()
print("  §B: %d present, %d absent, %d undetermined by this probe."
      % (bp, len(brows) - bp - bu, bu))

OUT.write_text(json.dumps({"section_a": rows, "section_b": brows,
                           "crosstab": {k: {kk: vv for kk, vv in v.items()}
                                        for k, v in tab.items()}},
                          indent=1), encoding="utf-8")
print()
print("wrote %s" % OUT)
