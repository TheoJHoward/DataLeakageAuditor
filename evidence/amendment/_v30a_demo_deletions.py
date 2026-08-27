#!/usr/bin/env python3
"""A4.2 — demonstrate that the three DELETED exemptions were doing real work.

WHY A DELETION NEEDS DEMONSTRATING AT ALL. Deleting an exemption is invisible in
a green gate: if the sentence it covered is gone, the check has nothing to fire
on either way, and "no finding" looks identical whether the exemption was
load-bearing or decorative. So each deleted exemption's original sentence is put
BACK into the declaration, and the detector must FIRE on it. A firing proves two
things at once -- the exemption was suppressing a real detection, and its
deletion did not silently license that value at some other position.

The inverse is what makes the deletion safe: the text that replaced each sentence
does NOT fire, which the current gate already shows (one D1 finding, and it is
the legitimate 20-vs-6).

Every mutation is reverted and verified by sha256.

Written with the Write tool per D2.1.
"""
import hashlib
import pathlib
import subprocess
import sys

REPO = pathlib.Path(r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01")
DECL = REPO / "AVAILABILITY_DECLARATION.md"

# (label, the deleted exemption's original sentence, what the detector must say)
CASES = [
    ("D5 / value 5 - the v30 count statement",
     "The `prereg-v30` tag message carries **five** SHA-256 lines - read this pass",
     "states 5"),
    ("D6 / value 2 - the line 97 verbatim quotation",
     "  \u00a711's integrity chain in full:** signed tag, both file hashes in the "
     "tag message, external",
     "states 2"),
    ("D6 / enumeration - the executed v30 five",
     "  covering `PREREG.md`, `DESIGN.md`, `HISTORY.md`, "
     "`tools/check_registration.py`,",
     "enumerates"),
]

ANCHOR = "### D.6 \u2014 Disclosures at the tag"


def gate():
    r = subprocess.run([sys.executable, "tools/check_registration.py",
                        "--stage", "prereg"], cwd=str(REPO),
                       capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return r.stdout + r.stderr


raw = DECL.read_bytes()
h0 = hashlib.sha256(raw).hexdigest()
anchor_b = ANCHOR.encode("utf-8")
if raw.count(anchor_b) != 1:
    sys.exit("HALT: expected one §D.6 heading, found %d" % raw.count(anchor_b))
at = raw.index(anchor_b)

print("A4.2 - DELETED EXEMPTIONS, DEMONSTRATED\n")
ok = True
for label, sentence, expect in CASES:
    inject = sentence.encode("utf-8") + b"\r\n\r\n"
    DECL.write_bytes(raw[:at] + inject + raw[at:])
    out = gate()
    fired = expect in out and "AVAILABILITY_DECLARATION.md" in out
    # the finding must be a FAILURE, not an exempt note
    unexempt = fired and not any(
        expect in ln and ln.strip().startswith("note:") for ln in out.split("\n"))
    print("  %-46s %s" % (label, "FIRED, unexempt" if unexempt
                          else "** DID NOT FIRE **"))
    if not unexempt:
        for ln in out.split("\n"):
            if "AVAILABILITY_DECLARATION" in ln and ("D1:" in ln or "D2:" in ln):
                print("      %s" % ln.strip()[:150])
    ok &= unexempt
    DECL.write_bytes(raw)
    if hashlib.sha256(DECL.read_bytes()).hexdigest() != h0:
        sys.exit("HALT: declaration not restored byte-exact after %r" % label)

print("\n  declaration restored byte-exact: %s"
      % (hashlib.sha256(DECL.read_bytes()).hexdigest() == h0))
print("  RESULT: %s" % ("PASS - each deleted exemption was suppressing a real "
                        "detection" if ok else "** FAIL **"))
sys.exit(0 if ok else 1)
