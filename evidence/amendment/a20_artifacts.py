"""A20, part 3 -- every artifact that DESCRIBES the amendment, against reality.

READ-ONLY.

PARTS 1 AND 2 SETTLED THE FILE. Part 1: the applied `PREREG.md` is byte-identical
to v30 with the approval record applied, so nothing unapproved was applied and
nothing approved was missed. Part 2: the approval record's population is
CLAUSES, so every MARKER block was ineligible for it by construction.

WHAT IS LEFT IS THE DESCRIPTIONS. Five rounds each found another document
asserting something about `PREREG.md` that is not true of `PREREG.md`, and each
was found by tripping over it rather than by looking. This looks. Every claim
below is enumerated with the probe that decides it, and the probe runs whether
or not anyone suspects the claim.

FOUR PROBE KINDS, and each says what it can and cannot decide:

  v30_line          is v30's line N still standing in the applied file, as a
                    line? "Standing" means the amendment did not replace it.
  text_present      is this exact string in the applied file?
  block_exists      is there a heading or marker of this shape anywhere?
  hash_matches      does this recorded digest match the file on disk?

A claim whose probe cannot decide it is reported UNDETERMINED with the reason.
It is never resolved by inference from the file's current state -- that
inference is what produced five rounds of fragments.

    usage: a20_artifacts.py <v30-file> <out.json>
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:                                       # noqa: BLE001
    pass

REPO = pathlib.Path(__file__).resolve().parents[2]

V30 = pathlib.Path(sys.argv[1])
OUT = pathlib.Path(sys.argv[2])

# ONE TREE, READ CONSISTENTLY. A first version read the describing artifacts from
# the working directory while hashing against a tree passed on the command line.
# Run from the Phase 1 branch that mixed two sources: it read Phase 1's README --
# which still carries the PRE-GROWTH six-file v30a block -- and reported that the
# registered branch's README enumerates six files. It enumerates twenty. An audit
# that reads two trees and calls the difference a finding is the failure mode
# this audit exists to end, so the tree is fixed once, here, and everything is
# read from it.
TREE = pathlib.Path(sys.argv[3]) if len(sys.argv) > 3 else REPO
APPLIED = TREE / "PREREG.md"
README = TREE / "README.md"
# `tagmsg.txt` is the ceremony's working file and is UNTRACKED, so it is in no
# tree. It is read from the working directory, and that is stated rather than
# left to look like an oversight.
TAGMSG = REPO / "tagmsg.txt"


def text_of(p):
    return p.read_text(encoding="utf-8").replace("\r\n", "\n")


v30_lines = text_of(V30).split("\n")
applied_lines = text_of(APPLIED).split("\n")
applied = "\n".join(applied_lines)


def v30_line(n):
    """Is v30's line n still standing, unreplaced, in the applied file?"""
    if n >= len(v30_lines):
        return ("UNDETERMINED", "v30 has no line %d" % n)
    t = v30_lines[n - 1]
    if not t.strip():
        return ("UNDETERMINED", "v30 line %d is blank" % n)
    for i, l in enumerate(applied_lines, 1):
        if l == t:
            return ("STANDING", "unchanged, applied l.%d" % i)
    # not a line any more -- is it quoted anywhere (a retention block)?
    frag = t.strip()[:80]
    for i, l in enumerate(applied_lines, 1):
        if frag in l:
            return ("REPLACED+RETAINED", "quoted at applied l.%d" % i)
    return ("REPLACED+GONE", "not present as a line or as a quotation")


def text_present(s):
    for i, l in enumerate(applied_lines, 1):
        if s in l:
            return ("PRESENT", "applied l.%d" % i)
    return ("ABSENT", "no line contains it")


def block_exists(pattern):
    hits = [i for i, l in enumerate(applied_lines, 1) if re.search(pattern, l)]
    return (("PRESENT", "applied l.%s" % hits[0]) if hits
            else ("ABSENT", "no line matches /%s/" % pattern))


# EVERY CLAIM NAMES THE VERDICTS THAT SATISFY IT. A verdict is not a judgement
# on its own: `REPLACED+GONE` FALSIFIES §8.2's item 1 ("no registered sentence is
# deleted") and SATISFIES tagmsg's ("this line is amended"), from the same probe
# on the same line. A first version scored the raw verdict and put tagmsg's one
# TRUE claim about §6.2 into the list of false ones.
SATISFIED_BY = {
    "tagmsg-amends": {"REPLACED+GONE", "REPLACED+RETAINED"},
    "exists": {"PRESENT"},
    "not-deleted": {"STANDING", "REPLACED+RETAINED"},
}

CLAIMS = [
    # ---- tagmsg.txt -------------------------------------------------------
    ("tagmsg.txt l.3", "Amends §6.2 — reference AUC (l.445)", v30_line, 445,
     "tagmsg-amends"),
    ("tagmsg.txt l.3", "Amends §6.2 — contamination availability class (l.450)",
     v30_line, 450, "tagmsg-amends"),
    ("tagmsg.txt l.4", "Amends §6.2 — sliced CI variant (l.451)", v30_line, 451,
     "tagmsg-amends"),
    ("tagmsg.txt l.4", "Amends §6.2 — criterion 3 (l.461)", v30_line, 461,
     "tagmsg-amends"),
    ("tagmsg.txt l.5", 'defines "waived" for §10.2\'s replacement-criterion floor',
     text_present, '**"Waived", defined', "exists"),

    # ---- the amendments block and everything that cites it ----------------
    ("PREREG.md", "an amendments block exists at all",
     block_exists, r"^## v30a amendments", "exists"),
    ("PREREG.md l.6", "an amendment status line exists",
     block_exists, r"^\*\*Amendment status:\*\*", "exists"),
    ("PREREG.md l.1338", "cites §10.2 (v30a) [SC-13c(c2)]",
     text_present, "SC-13c(c2)", "exists"),
    ("PREREG.md l.1849", 'cites "the amendments block records"',
     block_exists, r"^## v30a amendments", "exists"),
    ("PREREG.md l.1853", 'cites "recorded in the v30a amendments block"',
     block_exists, r"^## v30a amendments", "exists"),
    ("PREREG.md l.1915", 'cites "amendments block in terms"',
     block_exists, r"^## v30a amendments", "exists"),
    ("PREREG.md l.1917", 'cites "recorded in the amendments block"',
     block_exists, r"^## v30a amendments", "exists"),

    # ---- clauses that describe their own neighbours ------------------------
    ("PREREG.md l.1415", 'SC-6b: "after marker M2 where placed"',
     text_present, "M2 — §8.2 line 915", "exists"),
    ("PREREG.md l.1544", 'SC-6b: "every ... state that row carries"',
     text_present, "**Detector-case coverage**", "exists"),
    ("PREREG.md l.2013", 'SC-8b: "the item-3 marker ... follow the list"',
     text_present, "§11 item 3 —", "exists"),
    ("PREREG.md l.2013", 'SC-8b: "the line-97 marker is placed after line 97"',
     text_present, "§0.2.1 line 97 —", "exists"),
    ("PREREG.md l.2013", "SC-8b: \"SC-8's revised M2\"",
     text_present, "M2 — §8.2 line 915", "exists"),

    # ---- SC-12(w), cited three times ---------------------------------------
    ("PREREG.md l.1427", "§7.7 pointer: SC-12(w) registers the entry condition",
     text_present, "ENTRY CONDITION FOR", "exists"),
    ("PREREG.md l.1565", "§8.3 assertion: SC-12(w)'s (w1) prohibits the state",
     text_present, "closed list of licensed grounds", "exists"),
    ("PREREG.md l.1425", "SC-12p note: SC-12(w)'s own limb text",
     text_present, "a prohibition, and a closed list", "exists"),

    # ---- §8.2's own invariant, item 1 --------------------------------------
    ("K2 §8.2 item 1", "No registered sentence is deleted — v30 l.461",
     v30_line, 461, "not-deleted"),
    ("K2 §8.2 item 1", "No registered sentence is deleted — v30 l.855",
     v30_line, 855, "not-deleted"),
    ("K2 §8.2 item 1", "No registered sentence is deleted — v30 l.929",
     v30_line, 929, "not-deleted"),
    ("K2 §8.2 item 1", "No registered sentence is deleted — v30 l.1022",
     v30_line, 1022, "not-deleted"),
    ("K2 §8.2 item 1", "No registered sentence is deleted — v30 l.1030",
     v30_line, 1030, "not-deleted"),
]

print("=" * 78)
print("DESCRIBING ARTIFACTS -- every claim, with the probe that decides it")
print("=" * 78)
print("  %-18s %-56s %-18s %-4s %s"
      % ("artifact", "claim", "verdict", "ok?", "evidence"))
rows = []
for artifact, claim, probe, arg, expect in CLAIMS:
    verdict, detail = probe(arg)
    holds = verdict in SATISFIED_BY[expect]
    rows.append({"artifact": artifact, "claim": claim,
                 "probe": probe.__name__, "arg": str(arg)[:80],
                 "verdict": verdict, "expect": expect,
                 "claim_holds": holds, "detail": detail})
    print("  %-18s %-56s %-18s %-4s %s"
          % (artifact, claim[:56], verdict, "yes" if holds else "NO", detail))

# ---- the hash enumerations ------------------------------------------------
print()
print("=" * 78)
print("HASH ENUMERATIONS -- every recorded digest against the file on disk")
print("=" * 78)
# THE TREE TO HASH AGAINST IS AN ARGUMENT, NOT THE WORKING DIRECTORY. This audit
# runs from the Phase 1 branch, where HISTORY.md, the checker and the declaration
# legitimately differ from the registered branch and `phase7_l2_sim.py` is not
# present at all. Hashing the working tree reported four MISMATCHes that are
# facts about which branch is checked out, not about the tag message.
#
# AND README's v30 BLOCK IS NOT THE v30a BLOCK. Its v30 hashes are a dated record
# of what v30 was and are CORRECT AS WRITTEN; scoring them against today's files
# manufactures three more false mismatches. Each hash line is attributed to the
# block it sits in and the v30 block is reported separately, never as a defect.
print("  tree read and hashed: %s" % TREE)
print("  tagmsg.txt read from the working directory (untracked, in no tree)")

HASHLINE = re.compile(r"^([0-9a-f]{64})  (\S+)\s*$")
hash_rows = []


def block_of(name, lineno, blocks):
    which = "?"
    for start, label in blocks:
        if lineno >= start:
            which = label
    return which


for name, p in (("tagmsg.txt", TAGMSG), ("README.md", README)):
    if not p.exists():
        print("  %-12s ABSENT from the working tree" % name)
        continue
    lines = text_of(p).split("\n")
    blocks = [(1, "v30a" if name == "tagmsg.txt" else "v30")]
    for i, l in enumerate(lines, 1):
        if re.search(r"v30a", l) and l.startswith("#"):
            blocks.append((i, "v30a"))
    tally = {}
    for i, raw in enumerate(lines, 1):
        m = HASHLINE.match(raw)
        if not m:
            continue
        digest, rel = m.group(1), m.group(2)
        blk = block_of(name, i, blocks)
        f = TREE / rel
        if not f.exists():
            verdict = "FILE ABSENT"
        else:
            verdict = ("MATCH" if hashlib.sha256(f.read_bytes()).hexdigest() == digest
                       else "MISMATCH")
        got = (hashlib.sha256(f.read_bytes()).hexdigest()[:16] if f.exists() else "")
        tally.setdefault(blk, {}).setdefault(verdict, 0)
        tally[blk][verdict] += 1
        hash_rows.append({"artifact": name, "block": blk, "path": rel,
                          "verdict": verdict, "recorded": digest[:16],
                          "actual": got})
    for blk in sorted(tally):
        d = tally[blk]
        note = ("  <- a DATED record of what v30 was; not scored as a defect"
                if blk == "v30" else "")
        print("  %-12s %-5s block: %d enumerated -- %d match, %d mismatch, "
              "%d file absent%s"
              % (name, blk, sum(d.values()), d.get("MATCH", 0),
                 d.get("MISMATCH", 0), d.get("FILE ABSENT", 0), note))
    for r in hash_rows:
        if r["artifact"] == name and r["verdict"] != "MATCH" and r["block"] == "v30a":
            print("      %-12s %-52s recorded %s actual %s"
                  % (r["verdict"], r["path"], r["recorded"], r["actual"]))

# ---- summary ---------------------------------------------------------------
print()
print("=" * 78)
print("SUMMARY")
print("=" * 78)
by = {}
for r in rows:
    by[r["verdict"]] = by.get(r["verdict"], 0) + 1
for k in sorted(by):
    print("  %-20s %d" % (k, by[k]))
false_claims = [r for r in rows if not r["claim_holds"]]
print()
print("  CLAIMS THAT DO NOT HOLD AGAINST THE FILE: %d of %d"
      % (len(false_claims), len(rows)))
for r in false_claims:
    print("      %-18s %-62s (%s)" % (r["artifact"], r["claim"][:62], r["verdict"]))

OUT.write_text(json.dumps({"claims": rows, "hashes": hash_rows},
                          indent=1), encoding="utf-8")
print()
print("wrote %s" % OUT)
