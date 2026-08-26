#!/usr/bin/env python3
"""DELTA R49 - R3 (H-34 correction note) and R7 (the LF-manifest ceremony record)."""
import pathlib

REPO = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01")
SCR = pathlib.Path("C:/Users/ttbea/AppData/Local/Temp/claude/"
                   "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
                   "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad")

# ------------------------------------------------------------------ R3
h = REPO / "HISTORY.md"
t = h.read_text(encoding="utf-8")
ANCHOR = "\n\n### H-B addendum \u2014 firings v18 through v30"
assert t.count(ANCHOR) == 1, "H-B anchor match %d" % t.count(ANCHOR)

NOTE = """

**CORRECTION NOTE \u2014 21 August 2026. Recorded below the sign-off, not as an edit to it, per this
file's convention that a later contradiction is written under the original and never over it.**

*The verdict above stands and is not disturbed by anything here. What follows is a disclosure of
method that was owed when the entry was written and was not made.*

**1. The equivalence test applied above adjudicates criterion 1, not criterion 3.** The entry states
one test \u2014 *"does the tool probe a user-supplied callable at runtime against a declared per-cell
availability model?"* \u2014 and applies it to all ten candidates. \u00a710.1's **criterion 1** is coverage of
the published types at the same tier or better; **criterion 3** asks what a tool's runtime findings
do on `fixture_contaminated` and on `fixture_corrected`. The test above is a proxy for criterion 1.
The entry does not say so, and a reader would reasonably take the ten verdicts for five-criterion
scoring.

**2. Criterion 3 was not evaluated, for any candidate, and still has not been.** No candidate was
run against either fixture side. The verdicts rest on criterion 1 failing, which is **sufficient** \u2014
\u00a710.1 is a five-way conjunction and a candidate failing criterion 1 cannot fire the stop \u2014 but
sufficiency is not evaluation, and the entry should have recorded which criteria were reached and
which were not.

**3. What happened with \u00a79.2, established from artifacts on 21 August 2026 and recorded at
`DEVIATIONS.md` D-003.** Two days after this sign-off, on **14 August 2026**, a cross-tool comparison
was executed: **eleven tools over eight hand-written cases and their eight clean paired controls, 88
tool \u00d7 case cells**, with the case set authored and hashed **before the first tool ran** (29.261 s,
corroborated independently of the clock by a hash chain \u2014 112 declared case hashes recomputed, 0
mismatches). **It reached the same verdict as this entry, on the same ground: the kill gate does not
fire, and criterion 1 fails for every tool.** That corroborates the outcome above and does not repair
the method disclosure.

**It does not satisfy \u00a79.2, which remains un-run in its registered form.** \u00a79.2 requires the
comparison set *"committed with this protocol"*; the set is in no commit and the tagged tree of
`prereg-v30` is fixed, so that clause is **breached and uncurable for this tag**. The
acceptance-fixture half of \u00a79.2 was not run. **\u00a710.1 criterion 3 therefore remains unevaluated.** The
run is **unverified by any party that did not perform it**, and no result of it is cited
load-bearing here or anywhere else in the registration.

**4. Why this note exists at all.** v30a amends \u00a710.1's criterion 3 \u2014 the criterion this gate was
signed off under. A reader comparing the two texts is entitled to learn, from the face of the record
rather than by reconstruction, that the criterion being amended had never been evaluated under
either wording. **The re-fire condition above is unaffected and remains operative.**"""

t = t.replace(ANCHOR, NOTE + ANCHOR, 1)
h.write_text(t, encoding="utf-8")
print("HISTORY.md: H-34 correction note appended below the entry (%d lines)" % len(t.split("\n")))

# ------------------------------------------------------------------ R7
x = SCR / "ceremony" / "X4_REGENERATION_REQUIREMENTS.md"
tx = x.read_text(encoding="utf-8")
A = "## C3 \u2014 THE FULL C1\u2013C5 / R15 SET, INTACT"
assert tx.count(A) == 1, "C3 anchor match %d" % tx.count(A)
R7 = """## C2.3 \u2014 CEREMONY-CRITICAL: `evidence/MANIFEST.sha256` IS WRITTEN **LF**, ALONE IN THIS REPOSITORY

**This repository is natively CRLF.** `PREREG.md`, `DESIGN.md`, `HISTORY.md`, `PRACTICES.md`,
`AVAILABILITY_DECLARATION.md`, `declared_map.csv` \u2014 all CRLF. Any tool that rewrites them should
match that, and on Windows Python's `write_text` does so by default.

**`evidence/MANIFEST.sha256` is the exception and must be written with `newline="\\n"`.**
`sha256sum -c` parses each line as `<hash>  <path>` and takes a trailing carriage return **as part
of the filename**. A CRLF manifest therefore fails **every** entry with
`No such file or directory` \u2014 observed this round: 251 of 251 failed after an otherwise correct
rewrite, and 251 of 251 passed once the file was rewritten with LF.

**Why this is ceremony-critical and not a footnote.** X4 **regenerates from current state** (C1).
A regenerator that adopts the repository's own convention will produce a CRLF manifest, and
`sha256sum -c` will fail at tag time \u2014 after the commit, during verification, at the point where the
operator is least able to tell a line-ending problem from a real hash mismatch. **The failure mode
looks exactly like corrupted evidence.**

**The check:** after regenerating the manifest, `file evidence/MANIFEST.sha256` must not report CRLF,
and `sha256sum -c` from inside `evidence/` must exit 0 with 251 OK before anything is committed.

"""
tx = tx.replace(A, R7 + A, 1)
x.write_text(tx, encoding="utf-8")
print("X4_REGENERATION_REQUIREMENTS.md: C2.3 added (%d lines)" % len(tx.split("\n")))

# and in the runnable command file
c = REPO / "evidence" / "ceremony" / "CEREMONY_COMMANDS.md"
tc = c.read_text(encoding="utf-8")
MARK = "# C2d-2 \u2014 the declaration, the pointer's recorded hash, and the manifest line must agree."
if tc.count(MARK) == 1:
    ADD = """# C2d-0 \u2014 LINE ENDINGS. Run BEFORE C2d. `evidence/MANIFEST.sha256` must be LF while the rest
# of this repository is CRLF: sha256sum -c takes a trailing CR as part of the filename, so a CRLF
# manifest fails all 251 entries with "No such file or directory" - which looks exactly like
# corrupted evidence. Observed 21 Aug 2026: 251/251 failed, then 251/251 passed after an LF rewrite.
if grep -q $'\\r' evidence/MANIFEST.sha256; then
  echo "MANIFEST.sha256 has CRLF - HALT. Rewrite it with LF before verifying."; exit 1
else
  echo "MANIFEST.sha256 is LF - proceed"
fi

"""
    tc = tc.replace(MARK, ADD + MARK, 1)
    c.write_text(tc, encoding="utf-8")
    print("CEREMONY_COMMANDS.md: C2d-0 line-ending gate added before C2d-2")
else:
    print("CEREMONY_COMMANDS.md: C2d-2 marker not found (%d) - X4 will carry C2.3 instead" % tc.count(MARK))
