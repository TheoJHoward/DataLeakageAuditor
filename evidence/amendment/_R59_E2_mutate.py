#!/usr/bin/env python3
"""DELTA R59/E2 - mutation-test the re-anchor tool across every structural change.

It has been patched four times, each at a coupling, and has never been mutation-tested.
H-L16 applies to tools as much as to checks.

For each mutation: the CORRECT outcome is declared FIRST, then the tool is run DRY (it
never writes here), and the observed behaviour is compared to it. **Refusing is a correct
outcome. Passing wrongly is not**, and neither is passing when the answer happens to be
right for the wrong reason.
"""
import json
import pathlib
import re
import subprocess
import sys

D = pathlib.Path("C:/Users/ttbea/AppData/Local/Temp/claude/"
                 "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
                 "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/amendment")
SSF = D / "SCHEMA_SET_FINAL.md"
FROZ = D / "_K1_population_FROZEN.json"
MAN = D / "BLOCK_MANIFEST.md"


def snapshot():
    return (SSF.read_text(encoding="utf-8"),
            FROZ.read_text(encoding="utf-8"),
            MAN.read_text(encoding="utf-8"))


def restore(s):
    SSF.write_text(s[0], encoding="utf-8")
    FROZ.write_text(s[1], encoding="utf-8")
    MAN.write_text(s[2], encoding="utf-8")
    subprocess.run([sys.executable, str(D / "_K1_enumerate2.py")], capture_output=True)


def run_tool():
    r = subprocess.run([sys.executable, str(D / "_reanchor2.py")],
                       capture_output=True, text=True, encoding="utf-8")
    return r.stdout or "", r.returncode


def blocks():
    return json.loads((D / "_K1_population.json").read_text(encoding="utf-8"))


# ---------------------------------------------------------------- mutations
def m_displacement(L):
    """Insert plain prose ABOVE the first block: everything below moves, nothing changes."""
    i = next(k for k, l in enumerate(L) if l.startswith("# PART 1"))
    return L[:i + 2] + ["", "Displacement-test paragraph, not a block.", ""] + L[i + 2:]


def m_growth_single(L):
    """Grow a block that has exactly ONE manifest row spanning it."""
    i = next(k for k, l in enumerate(L) if l.startswith("> **(k) TWO MECHANISMS"))
    return L[:i + 1] + ["> SIMULATED GROWTH INSIDE A SINGLE-ROW BLOCK."] + L[i + 1:]


def m_growth_multi(L):
    """Grow a block that has TWO sub-entry rows (7a/7b). Correct outcome: REFUSE."""
    i = next(k for k, l in enumerate(L) if l.startswith("> **\u00a76.2 line 459"))
    return L[:i + 1] + ["> SIMULATED GROWTH INSIDE A MULTI-ROW BLOCK."] + L[i + 1:]


def m_insert(L):
    """Insert a whole new fenced block mid-file."""
    i = next(k for k, l in enumerate(L) if l.startswith("**THE CLAUSE.**"))
    return L[:i] + ["```", "SIMULATED INSERTED BLOCK, MID-FILE.", "```", ""] + L[i:]


def m_delete(L):
    """Delete a whole blockquote block."""
    i = next(k for k, l in enumerate(L) if l.startswith("> **(k) TWO MECHANISMS"))
    j = i
    while j < len(L) and L[j].startswith(">"):
        j += 1
    return L[:i] + L[j:]


def m_reorder(L):
    """Swap two adjacent fenced blocks (the R53 C2op/C2ret pair)."""
    i = next(k for k, l in enumerate(L) if "\u00a710.1-C2op" in l and l.startswith("###"))
    j = next(k for k, l in enumerate(L) if "\u00a710.1-C2ret" in l and l.startswith("###"))
    end = j
    while end < len(L) and not L[end].startswith("---"):
        end += 1
    return L[:i] + L[j:end] + L[i:j] + L[end:]


def m_change_and_move(L):
    """A block whose content changes AND whose position moves."""
    L = m_displacement(L)
    return m_growth_single(L)


CASES = [
    ("pure displacement", m_displacement,
     "shift rows by the block delta; 0 added, 0 unmatched", "SHIFT"),
    ("internal growth, single-row block", m_growth_single,
     "re-derive that block's end; other rows shift", "EXTEND"),
    ("internal growth, MULTI-row block", m_growth_multi,
     "REFUSE - sub-entry boundaries are not recoverable by arithmetic", "REFUSE"),
    ("insertion mid-file", m_insert,
     "report ADDED and shift the rest; do not guess an assignment", "ADDED"),
    ("deletion of a whole block", m_delete,
     "report the frozen block as unmatched; must NOT silently re-point its rows", "DELETE"),
    ("reordering of two blocks", m_reorder,
     "content-match both; rows follow their own block", "REORDER"),
    ("content changes AND position moves", m_change_and_move,
     "the changed block is unmatched; must not be confused with a displaced one", "CHANGE+MOVE"),
]

snap = snapshot()
print("  %-38s %-9s %s" % ("STRUCTURAL CHANGE", "EXIT", "OBSERVED"))
print("  " + "-" * 104)
verdicts = []
try:
    for name, mut, expect, kind in CASES:
        restore(snap)
        L = SSF.read_text(encoding="utf-8").split("\n")
        SSF.write_text("\n".join(mut(L)), encoding="utf-8")
        out, code = run_tool()
        head = [l for l in out.split("\n") if l.startswith("blocks frozen")]
        added = re.search(r"added: (\d+)", head[0]) if head else None
        unmatched = re.search(r"unmatched frozen: (\d+)", head[0]) if head else None
        shifted = re.search(r"rows shifted \(displaced blocks\): (\d+)", out)
        extended = re.search(r"rows extended \(grown, single-row\): (\d+)", out)
        refused = "REFUSED TO SHIFT" in out
        obs = "added=%s unmatched=%s shifted=%s extended=%s refused=%s" % (
            added.group(1) if added else "?", unmatched.group(1) if unmatched else "?",
            shifted.group(1) if shifted else "?", extended.group(1) if extended else "?",
            refused)
        # verdict per declared-correct outcome
        ok = None
        if kind == "SHIFT":
            ok = (not refused and added and added.group(1) == "0"
                  and unmatched and unmatched.group(1) == "0" and shifted and int(shifted.group(1)) > 0)
        elif kind == "EXTEND":
            ok = (not refused and unmatched and unmatched.group(1) == "1"
                  and extended and int(extended.group(1)) >= 1)
        elif kind == "REFUSE":
            ok = refused and code == 1
        elif kind == "ADDED":
            ok = (not refused and added and int(added.group(1)) >= 1)
        elif kind == "DELETE":
            ok = (unmatched and int(unmatched.group(1)) >= 1)
        elif kind == "REORDER":
            ok = (not refused and unmatched and unmatched.group(1) == "0")
        elif kind == "CHANGE+MOVE":
            ok = (unmatched and int(unmatched.group(1)) >= 1)
        verdicts.append((name, ok, obs, expect, refused))
        print("  %-38s %-9s %s" % (name[:38], code, obs))
finally:
    restore(snap)
    print("\n  [source, frozen population and manifest restored]")

print()
print("  %-38s %-8s %s" % ("STRUCTURAL CHANGE", "VERDICT", "DECLARED-CORRECT OUTCOME"))
print("  " + "-" * 104)
bad = 0
for name, ok, obs, expect, refused in verdicts:
    v = "HANDLED" if ok else "*** WRONG ***"
    if not ok:
        bad += 1
    print("  %-38s %-8s %s" % (name[:38], v, expect[:56]))
print()
print("  handled correctly: %d of %d" % (len(verdicts) - bad, len(verdicts)))
