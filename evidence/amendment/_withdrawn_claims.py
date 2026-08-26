#!/usr/bin/env python3
"""WITHDRAWN-CLAIM REGISTER, asserted against operative text.  DELTA R55/W5.

THE GAP THIS FILLS. Every other check compares a hunk against its source. When a claim
is withdrawn and the correction is applied to only ONE of the places carrying it, source
and hunk still AGREE - on the withdrawn text - so coverage is 100%, the span is intact,
and every check reports green. **A provenance check is blind to source and hunk agreeing
on something false, by construction.**

That is not hypothetical. The claim "the anchor's model family changed" was withdrawn at
R48/Q4. The correction was applied to H10's `justification` - the field a reviewer reads -
and NOT to its `operative_text`, the field that lands in PREREG.md. The justification was
then edited to say the claim "is struck from both". So the falsified claim shipped for two
further rounds, in the only field that matters, under a sentence asserting its removal.
A partial landing is worse than none, because the surviving instance reads as verified.

THE RULE. A withdrawn claim may appear in operative text ONLY where it is QUOTED - inside
quotation marks - AND a struck-marker is within WINDOW characters. Quoting is what makes it
a mention rather than a use. Anywhere else it is a live assertion of something known false.

The quoting requirement is not decoration, and this check nearly shipped without it. The
first draft asked only for a nearby marker, and MISSED the very defect it was written for:
the pre-W5 text read "RETIRED because ... and because the anchor's model family changed",
so a struck-marker sat well inside the window - but it referred to the sentence's SUBJECT,
while the claim itself was a GROUND FOR the retirement, asserted live. Mutation testing
against the historical text found that in one run; reading the code did not. (H-L16.)

Registering a claim here is cheap and permanent; the register is append-only in spirit.
"""
import json
import pathlib
import re

D = pathlib.Path("C:/Users/ttbea/AppData/Local/Temp/claude/"
                 "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
                 "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/amendment")

WINDOW = 320
QUOTED_AS_DEAD = re.compile(
    r"struck|WITHDRAWN|withdrawn|SUPERSEDED|superseded|retired|Retired|NOT operative|"
    r"not operative|is false|was FALSE|was false|no longer|previously read|stood here until",
    re.I)

# (claim text, round that withdrew it, why it is false)
REGISTER = [
    ("the anchor's model family changed",
     "R48/Q4",
     "false against its own cited source: `MASTER_FINDINGS\\preregistration_v4.txt` names six "
     "architectures with LightGBM listed FIRST and XGBoost second, with hyperparameters for both. "
     "No family changed."),
    ("SC-8(g)",
     "R49/R6 B1",
     "SC-8's applied text runs (a)-(f). SC-8(g) exists only in an unapplied drafting document, and "
     "'(g)(a)' matched nothing even there."),
    ("every declared reference-anchor entry reproduces within its registered acceptance interval",
     "J3",
     "the withdrawn C1: it replaced a test the fixture demonstrably fails with one that compares a "
     "recomputation of committed bytes against itself."),
    ("SC-14",
     "R33/Z-series",
     "SC-14 is WITHDRAWN and must appear nowhere in applied text."),
]


def run(verbose=True):
    hunks = json.loads((D / "_X5_hunks_v2.json").read_text(encoding="utf-8"))["hunks"]

    def ln(h):
        m = re.search(r"\d+", h.get("prereg_line", "") or "")
        return int(m.group(0)) if m else 9999

    HN = {f"H{i}": h for i, h in enumerate(sorted(hunks, key=ln), 1)}
    live, quoted = [], 0
    for hid, h in HN.items():
        op = h.get("operative_text") or ""
        for claim, rnd, why in REGISTER:
            for m in re.finditer(re.escape(claim), op):
                a = max(0, m.start() - WINDOW)
                b = min(len(op), m.end() + WINDOW)
                # PROXIMITY ALONE IS NOT ENOUGH, and assuming it was is a defect this
                # check nearly shipped with. The pre-W5 text read "RETIRED because ...
                # and because the anchor's model family changed" - a struck-marker sits
                # well inside the window, but the claim there is a GROUND FOR the
                # retirement, asserted live. The marker referred to the sentence's
                # subject, not to the claim.
                #
                # So a withdrawn claim is permitted only where it is QUOTED - inside
                # quotation marks - AND a struck-marker is near. Quoting is what makes
                # it a mention rather than a use.
                lo = op.rfind('"', a, m.start())
                lo2 = op.rfind("“", a, m.start())
                hi = op.find('"', m.end(), b)
                hi2 = op.find("”", m.end(), b)
                in_quotes = (max(lo, lo2) >= 0 and max(hi, hi2) >= 0)
                if in_quotes and QUOTED_AS_DEAD.search(op[a:b]):
                    quoted += 1
                else:
                    live.append((hid, claim, rnd, op[a:b][:160]))
    if verbose:
        print("  register: %d withdrawn claim(s); scanned %d hunks' OPERATIVE text"
              % (len(REGISTER), len(HN)))
        print("  appearances quoted as withdrawn (permitted) : %d" % quoted)
        print("  appearances asserted LIVE (forbidden)       : %d" % len(live))
        for hid, claim, rnd, ctx in live:
            print("    *** %s asserts %r, withdrawn at %s" % (hid, claim[:60], rnd))
            print("        context: %r" % ctx)
        if not live:
            print("  PASS \u2014 no withdrawn claim is asserted live in any hunk's operative text")
    return live


if __name__ == "__main__":
    import sys
    sys.exit(1 if run() else 0)
