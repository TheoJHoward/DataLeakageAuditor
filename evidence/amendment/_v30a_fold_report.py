#!/usr/bin/env python3
"""A4.5 + A4.6 — bring in this round's remaining instruments, fold the running
report into ROUND_STATE.md, and resync every manifest line that moved.

ORDER MATTERS AND IS WHY THIS IS ONE SCRIPT. ROUND_STATE.md is itself
manifest-attested, so folding the report into it changes its hash. Resyncing the
manifest before the fold would leave it stale again immediately. The manifest is
therefore recomputed LAST, from disk, in one pass.

Register form: the report carries facts and outcomes. Round numbers stay out of
the shipping prose; the ledger's own columns already record when an item moved.

Written with the Write tool per D2.1.
"""
import hashlib
import pathlib
import shutil
import sys

REPO = pathlib.Path(r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01")
SCRATCH = pathlib.Path(
    r"C:\Users\ttbea\AppData\Local\Temp\claude"
    r"\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01"
    r"\33e8c843-30fa-4bfb-aa9f-814c77bdb2e6\scratchpad")
RS = REPO / "evidence/session/ROUND_STATE.md"
MAN = REPO / "evidence/MANIFEST.sha256"

# ---- A4.5: the instruments this round added --------------------------------
NEW = [("demo_deletions.py", "_v30a_demo_deletions.py"),
       ("a44_citing_records.py", "_v30a_citing_records.py")]
brought = []
for src_name, dst_name in NEW:
    src, dst = SCRATCH / src_name, REPO / "evidence/amendment" / dst_name
    if not src.exists():
        sys.exit("HALT: %s not found" % src)
    if not dst.exists():
        shutil.copyfile(src, dst)
        brought.append("amendment/" + dst_name)

# ---- A4.6: fold the running report into ROUND_STATE.md ---------------------
raw = RS.read_bytes()
if raw.count(b"\r\n") != raw.count(b"\n"):
    sys.exit("HALT: ROUND_STATE.md is not uniformly CRLF")
text = raw.decode("utf-8").replace("\r\n", "\n")

OLD_HEAD = text[text.index("**CURRENT ROUND:"):text.index("---\n\n## \u00a70 \u2014 THE LEDGER")]
NEW_HEAD = """**CURRENT STATE: v30a closeout, Track A. The whole A4 edit batch is staged and
UNCOMMITTED.** `main` is at `3257f07752a352ac4c56e595f8bd1caebc7bf857`; tags are `prereg-v30`
only. Nothing has been committed, tagged, pushed or stamped.

**Track B runs in parallel on branch `phase1` and waits on none of this.**

**THIS FILE IS THE REPORT.** Each item is banked here when it completes, before the next begins.
A record that lives only in a chat message dies with the turn, and a turn that ends mid-item then
costs a full relay to reconstruct a state that was already on disk.

"""
text = text.replace(OLD_HEAD, NEW_HEAD, 1)

# The ledger's stale head row: the C2.5 halt was cleared by the author's sign-off.
text = text.replace(
    "| 1 | **C2.5 — fixture manifest is DRAFT, and absent from \u00a7D.1's freeze "
    "list** | \u26d4 **HALT — ceremony stopped here** | R97 | R97 |",
    "| 1 | **C2.5 — fixture manifest DRAFT + absent from \u00a7D.1** | \u2705 CLEARED — "
    "author sign-off 26 Aug 2026; \u00a7D.1 pins it by path and bytes | R99 | R99 |", 1)

report = (SCRATCH / "round_report.md").read_text(encoding="utf-8")
body = report[report.index("## A0 \u2014 STATE DISCOVERED"):]
text = text.rstrip("\n") + "\n\n---\n\n# v30a CLOSEOUT \u2014 ITEM RECORD\n\n" + body.rstrip("\n") + "\n"

RS.write_bytes(text.replace("\n", "\r\n").encode("utf-8"))

# ---- resync every manifest line whose file moved, and add the new ones -----
lines = MAN.read_bytes().decode("utf-8").split("\n")
resynced, added = [], []
for i, line in enumerate(lines):
    if not line or line.startswith("#") or "  " not in line:
        continue
    digest, rel = line.split("  ", 1)
    target = (REPO / rel[3:]) if rel.startswith("../") else (REPO / "evidence" / rel)
    if not target.exists():
        continue
    actual = hashlib.sha256(target.read_bytes()).hexdigest()
    if actual != digest:
        lines[i] = "%s  %s" % (actual, rel)
        resynced.append(rel)

last = max(i for i, l in enumerate(lines) if "  amendment/" in l)
for k, rel in enumerate(brought):
    d = hashlib.sha256((REPO / "evidence" / rel).read_bytes()).hexdigest()
    lines.insert(last + 1 + k, "%s  %s" % (d, rel))
    added.append(rel)

MAN.write_bytes("\n".join(lines).encode("utf-8"))

print("A4.5 brought in : %s" % (", ".join(brought) or "(none new)"))
print("A4.6 fold       : ROUND_STATE.md, %d CRLF / %d LF"
      % (RS.read_bytes().count(b"\r\n"), RS.read_bytes().count(b"\n")))
print("manifest resync : %d line(s) -> %s" % (len(resynced), ", ".join(resynced)))
print("manifest added  : %d line(s) -> %s" % (len(added), ", ".join(added)))
print("manifest entries: %d"
      % len([l for l in lines if l and not l.startswith("#") and "  " in l]))
