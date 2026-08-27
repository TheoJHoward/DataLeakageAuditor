#!/usr/bin/env python3
"""A4(e) — H-L25 into HISTORY.md's numbered review-lesson list.

Anchored on lesson 24's opening, not on a line number.

Written with the Write tool per D2.1.
"""
import pathlib
import sys

REPO = pathlib.Path(r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01")
H = REPO / "HISTORY.md"

s = H.read_text(encoding="utf-8")
if "\n25. *(26 Aug 2026)*" in s:
    sys.exit("HALT: lesson 25 already present")

anchor = "\n\n### H-30 — from `PREREG.md` \u00a76.6"
if s.count(anchor) != 1:
    sys.exit("HALT: expected exactly one H-30 anchor, found %d" % s.count(anchor))

LESSON = (
    "\n25. *(26 Aug 2026)* **Four failures of the same kind: a record made to look discharged by "
    "the things that referred to it.** **(a) An adversarial fleet found nothing its own search step "
    "had not already found.** Seventy-six per-occurrence refuters were spawned over a corpus sweep; "
    "seventy-two refuted, four survived, and every survivor confirmed what the sweep had already "
    "reported. A single completeness pass over the same corpus found a defect in the object about "
    "to be signed \u2014 an enumeration short by fourteen of the paths the registered text requires. "
    "**Redundancy tests whether a finding is right; it cannot test whether the question was the "
    "right one.** Scale the critic, not the refuters. **(b) An interface validated only against the "
    "harness that motivated it inherits that harness's blind spot.** The comparison harness passes a "
    "single frame in all eight of its cases; the acceptance fixture joins three, twice, on a "
    "wall-clock floor \u2014 and that join is the project's own headline leak channel. A contract "
    "validated against the harness alone would have been an instrument narrower than its claim, in "
    "the direction that hides findings. **(c) A fault in the auditor was reported as a fault in the "
    "audited pipeline.** A build raising on its own unperturbed input was recorded "
    "`could_not_run(determinism)`. It had not been shown nondeterministic; it had been shown not to "
    "run, which the reason precedence names `crash`. **A wrong reason is worse than an absent one: "
    "it sends the next reader to look for a fault that was never there**, and here it would have "
    "sent them into the user's pipeline for a defect in ours. Instruments that attribute their own "
    "failure to their subject are the failure mode this tool exists to detect, and it appeared "
    "first inside the tool. **(d) A disclosure that lives only in a drafting record discloses "
    "nothing.** Five disclosure lines \u2014 the attestation boundary, the deferred advisory steps, "
    "the stale-description floor, the instrument-domain gaps, and the external-input dependency "
    "\u2014 were written as they should appear and none was ever deployed into a registered file. "
    "**Three working records cited them as operative, and those citations are what made the absence "
    "invisible:** a reference reads as evidence that the thing referred to exists. One citation was "
    "in the registered declaration itself, which stated that a known-false sentence \"is handled "
    "instead by specific disclosure at D-STALE\" \u2014 a registered pointer into a disclosure that "
    "was not there. **The test is not whether a record is cited; it is whether the cited text "
    "resolves.**\n")

s = s.replace(anchor, LESSON + anchor, 1)
H.write_text(s, encoding="utf-8", newline="\n")
print("H-L25 added; HISTORY.md now %d lines" % len(s.split("\n")))
