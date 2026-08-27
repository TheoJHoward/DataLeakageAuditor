"""A20 -- the differential audit of `PREREG.md` v30 -> v30a. READ-ONLY.

WHY A RECONSTRUCTION AND NOT A SEARCH. Five rounds classified changes by looking
for them: is this marker present, does that citation resolve. Each round found
more than the last, because a search only ever finds what it thought to look
for. This does not search. It REBUILDS the file the approval record describes --
`git show prereg-v30:PREREG.md` with `PREREG_v30a_APPROVAL.diff` applied -- and
then diffs that reconstruction against the file on disk. Every difference
between them is, by construction, either something applied that nobody approved
or something approved that was never applied. There is no third possibility and
nothing to overlook.

    approval record  = SCHEMA_RECORDS.json -> PREREG_v30a_APPROVAL.diff
    reconstruction   = v30 + that diff, applied with full context verification
    applied          = PREREG.md on disk

    diff(reconstruction, applied):  insert -> UNAPPROVED-APPLIED
                                    delete -> APPROVED-MISSING
    diff(v30, applied):             delete -> DELETED
    everything else                        -> APPROVED-APPLIED

THE APPLIER VERIFIES EVERY CONTEXT AND EVERY REMOVAL LINE against v30 before it
writes anything into the reconstruction. A diff applied without that check would
produce a reconstruction that is not what the approval record says, and the
audit would then measure the applier's mistakes. Any mismatch is a HALT, not a
fuzzy match: this is the one place where being approximately right is worse than
stopping.

THE THREE PROBES STAY SEPARATE. Where a row is reported, the approval record,
the marker in the applied file and whether v30's own sentence still stands there
are printed as three columns. Collapsing them is what would have mis-read §6.2
line 451, where a record exists (`SC-2`) but inserts AFTER the line rather than
superseding it, and v30's sentence is still standing unmarked.

READ-ONLY. This script opens no file for writing except its own JSON result
under the path given on the command line.

    usage: a20_differential_audit.py <v30-file> <out.json>
"""
from __future__ import annotations

import difflib
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
APPLIED = REPO / "PREREG.md"
DIFF = REPO / "evidence/amendment/PREREG_v30a_APPROVAL.diff"
RECORDS = REPO / "evidence/amendment/SCHEMA_RECORDS.json"
LEDGER = REPO / "evidence/amendment/K2_AMENDMENT_LEDGER.md"
TAGMSG = REPO / "tagmsg.txt"

V30_PATH = pathlib.Path(sys.argv[1])
OUT = pathlib.Path(sys.argv[2])


def lines_of(p: pathlib.Path) -> list[str]:
    return p.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")


def sha(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


v30 = lines_of(V30_PATH)
applied = lines_of(APPLIED)

print("=" * 78)
print("POPULATION, ASSERTED BEFORE ANYTHING IS CLASSIFIED")
print("=" * 78)
print("  v30      %-8d lines   sha256 %s" % (len(v30) - 1, sha(V30_PATH)[:16]))
print("  applied  %-8d lines   sha256 %s" % (len(applied) - 1, sha(APPLIED)[:16]))
print("  approval diff                 sha256 %s" % sha(DIFF)[:16])
records = json.loads(RECORDS.read_text(encoding="utf-8"))["records"]
print("  SCHEMA_RECORDS.json: %d records" % len(records))


# ---------------------------------------------------------------------------
# 1. parse the approval diff
# ---------------------------------------------------------------------------
HUNK = re.compile(r"^@@ -(\d+),(\d+) \+(\d+),(\d+) @@")
hunks = []
cur = None
for raw in DIFF.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n"):
    m = HUNK.match(raw)
    if m:
        cur = {"src": int(m.group(1)), "srclen": int(m.group(2)),
               "dst": int(m.group(3)), "dstlen": int(m.group(4)),
               "ops": [], "s": 0, "d": 0}
        hunks.append(cur)
        continue
    if cur is None:
        continue                                   # the --- / +++ header
    # THE DECLARED COUNTS ARE THE AUTHORITY, not the shape of the line. A first
    # version read every line until the next `@@` and treated a bare empty line
    # as an empty context line -- which is correct INSIDE a hunk (trailing
    # whitespace is routinely stripped from " " context lines) and wrong for the
    # empty string `split("\n")` yields from the file's final newline. That one
    # phantom context line pushed the last hunk one line past its anchor and the
    # applier halted, correctly, on a mismatch it had itself created. Consuming
    # exactly `srclen` source and `dstlen` destination lines cannot make that
    # mistake, and it is what a unified diff actually means.
    if cur["s"] >= cur["srclen"] and cur["d"] >= cur["dstlen"]:
        continue                                   # this hunk is complete
    if raw.startswith("+"):
        cur["ops"].append(("+", raw[1:]))
        cur["d"] += 1
    elif raw.startswith("-"):
        cur["ops"].append(("-", raw[1:]))
        cur["s"] += 1
    elif raw.startswith(" ") or raw == "":
        cur["ops"].append((" ", raw[1:] if raw else ""))
        cur["s"] += 1
        cur["d"] += 1
    else:
        sys.exit("HALT: unparseable diff line %r" % raw[:60])

for n, h in enumerate(hunks, 1):
    if h["s"] != h["srclen"] or h["d"] != h["dstlen"]:
        sys.exit("HALT: hunk %d (@@ -%d,%d +%d,%d @@) carries %d source and %d "
                 "destination lines. A hunk whose body disagrees with its own "
                 "header is not a diff this audit can trust."
                 % (n, h["src"], h["srclen"], h["dst"], h["dstlen"],
                    h["s"], h["d"]))

print("  approval diff: %d hunks, +%d -%d  (every hunk body matches its header)"
      % (len(hunks),
         sum(1 for h in hunks for k, _ in h["ops"] if k == "+"),
         sum(1 for h in hunks for k, _ in h["ops"] if k == "-")))
print()


# ---------------------------------------------------------------------------
# 2. apply it to v30, verifying every context and every removal
# ---------------------------------------------------------------------------
recon: list[str] = []
pos = 0                                             # 0-based index into v30
for h in hunks:
    start = h["src"] - 1
    if start < pos:
        sys.exit("HALT: hunk at v30 l.%d overlaps the previous one" % h["src"])
    recon.extend(v30[pos:start])
    pos = start
    for kind, text in h["ops"]:
        if kind in (" ", "-"):
            if pos >= len(v30):
                sys.exit("HALT: hunk at v30 l.%d runs past the end of v30" % h["src"])
            if v30[pos] != text:
                sys.exit("HALT: hunk at v30 l.%d -- %s line does not match v30 "
                         "l.%d.\n  diff says: %r\n  v30 has  : %r\n"
                         "A diff applied over a mismatch produces a "
                         "reconstruction that is not what the approval record "
                         "says, and this audit would then measure the applier."
                         % (h["src"], "context" if kind == " " else "removal",
                            pos + 1, text[:70], v30[pos][:70]))
            if kind == " ":
                recon.append(text)
            pos += 1
        else:
            recon.append(text)
recon.extend(v30[pos:])

print("=" * 78)
print("THE RECONSTRUCTION -- v30 with the approval record applied")
print("=" * 78)
print("  every context and removal line verified against v30: %d checks"
      % sum(1 for h in hunks for k, _ in h["ops"] if k in (" ", "-")))
print("  reconstruction: %d lines (v30 %d, applied %d)"
      % (len(recon) - 1, len(v30) - 1, len(applied) - 1))
recon_sha = hashlib.sha256("\n".join(recon).encode("utf-8")).hexdigest()
print("  reconstruction sha256 %s" % recon_sha[:16])
print("  applied        sha256 %s" % sha(APPLIED)[:16])
print("  BYTE-IDENTICAL TO THE APPLIED FILE: %s"
      % ("YES" if "\n".join(recon) == "\n".join(applied) else "NO"))
print()


# ---------------------------------------------------------------------------
# 3. classify
# ---------------------------------------------------------------------------
def blocks(a, b):
    """Non-equal opcodes of a -> b, as (tag, a-slice, b-slice)."""
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    return [(t, a[i1:i2], b[j1:j2], i1, j1)
            for t, i1, i2, j1, j2 in sm.get_opcodes() if t != "equal"]


approved_additions = {t for h in hunks for k, t in h["ops"] if k == "+"}
approved_removals = {t for h in hunks for k, t in h["ops"] if k == "-"}

rows = []

# (a) reconstruction vs applied: the whole of UNAPPROVED-APPLIED and
#     APPROVED-MISSING lives here, by construction.
for tag, aslice, bslice, ai, bj in blocks(recon, applied):
    if [x for x in bslice if x.strip()]:
        rows.append({"class": "UNAPPROVED-APPLIED", "at_applied": bj + 1,
                     "n": len([x for x in bslice if x.strip()]),
                     "sample": next(x for x in bslice if x.strip())[:110]})
    if [x for x in aslice if x.strip()]:
        rows.append({"class": "APPROVED-MISSING", "at_recon": ai + 1,
                     "n": len([x for x in aslice if x.strip()]),
                     "sample": next(x for x in aslice if x.strip())[:110]})

# (b) v30 vs applied: DELETED is every v30 line that is gone AS A LINE.
#
# "Gone as a line" is not the same as "gone". §8.2's item 1 -- the amendment's
# own invariant -- says the v30 text is "retained inline, verbatim, at its own
# site, in a block marked SUPERSEDED BY v30a". A retention block QUOTES the old
# sentence inside a longer line, so the line disappears while the sentence
# survives. Reporting those as deletions would accuse the amendment of breaching
# an invariant it kept; reporting them all as retained would hide the ones it
# did breach. So each deleted line gets a THIRD probe: is its text present as a
# substring anywhere in the applied file, and is a retention marker near it.
applied_text = "\n".join(applied)


def retention_probe(text):
    """Where, if anywhere, this v30 sentence survives in the applied file."""
    frag = text.strip()
    if frag.startswith("- ") or frag.startswith("| "):
        frag = frag[2:]
    frag = frag[:80]
    hits = [i + 1 for i, l in enumerate(applied) if frag and frag in l]
    if not hits:
        return {"retained": False, "at": None, "marked": False, "probe": frag[:60]}
    at = hits[0]
    near = "\n".join(applied[max(0, at - 6):at + 2])
    marked = ("SUPERSEDED BY v30a" in near
              or "retained verbatim" in near
              or "NOT operative" in near
              or "v30 text" in near)
    return {"retained": True, "at": at, "marked": marked,
            "probe": frag[:60], "occurrences": len(hits)}


for tag, aslice, bslice, ai, bj in blocks(v30, applied):
    if tag in ("delete", "replace"):
        for k, text in enumerate(aslice):
            if not text.strip():
                continue
            if text in applied:
                continue                            # still present as a line
            rows.append({
                "class": "DELETED", "at_v30": ai + k + 1,
                "approved_removal": text in approved_removals,
                "retention": retention_probe(text),
                "sample": text[:110]})

# (c) APPROVED-APPLIED: every hunk whose additions are all present.
for n, h in enumerate(hunks, 1):
    adds = [t for k, t in h["ops"] if k == "+" and t.strip()]
    dels = [t for k, t in h["ops"] if k == "-" and t.strip()]
    present = sum(1 for t in adds if t in applied)
    rows.append({"class": "APPROVED-APPLIED" if present == len(adds)
                 else "APPROVED-PARTIAL",
                 "hunk": n, "v30_line": h["src"],
                 "added": len(adds), "added_present": present,
                 "removed": len(dels),
                 "sample": (adds[0][:110] if adds else (dels[0][:110] if dels else ""))})

counts = {}
for r in rows:
    counts[r["class"]] = counts.get(r["class"], 0) + 1

print("=" * 78)
print("CLASSES")
print("=" * 78)
for c in ("UNAPPROVED-APPLIED", "APPROVED-MISSING", "DELETED",
          "APPROVED-PARTIAL", "APPROVED-APPLIED"):
    print("  %-20s %d" % (c, counts.get(c, 0)))
print()

for c in ("UNAPPROVED-APPLIED", "APPROVED-MISSING", "APPROVED-PARTIAL"):
    sel = [r for r in rows if r["class"] == c]
    if not sel:
        print("  %s: EMPTY" % c)
        continue
    print("  %s:" % c)
    for r in sel:
        print("      %s" % json.dumps(r, ensure_ascii=False)[:150])
print()
print("  DELETED (%d) -- three probes, kept separate:" % counts.get("DELETED", 0))
print("      %-9s %-9s %-24s %s" % ("v30 line", "approved", "retained in applied", "text"))
for r in [x for x in rows if x["class"] == "DELETED"]:
    ret = r["retention"]
    where = ("l.%d %s" % (ret["at"], "MARKED" if ret["marked"] else "UNMARKED")
             if ret["retained"] else "NOWHERE")
    print("      %-9d %-9s %-24s %s"
          % (r["at_v30"], "yes" if r["approved_removal"] else "NO",
             where, r["sample"][:70]))
breaches = [r for r in rows if r["class"] == "DELETED" and not r["retention"]["retained"]]
unmarked = [r for r in rows if r["class"] == "DELETED"
            and r["retention"]["retained"] and not r["retention"]["marked"]]
print()
print("  §8.2 item 1 -- \"No registered sentence is deleted from this file\":")
print("      retained NOWHERE (a deletion in breach of the invariant): %d" % len(breaches))
print("      retained but with NO retention marker near it:            %d" % len(unmarked))

OUT.write_text(json.dumps({
    "v30_sha256": sha(V30_PATH), "applied_sha256": sha(APPLIED),
    "diff_sha256": sha(DIFF), "reconstruction_sha256": recon_sha,
    "v30_lines": len(v30) - 1, "applied_lines": len(applied) - 1,
    "reconstruction_lines": len(recon) - 1,
    "reconstruction_matches_applied": "\n".join(recon) == "\n".join(applied),
    "hunks": len(hunks), "records": len(records),
    "counts": counts, "rows": rows,
}, indent=1), encoding="utf-8")
print()
print("wrote %s" % OUT)
