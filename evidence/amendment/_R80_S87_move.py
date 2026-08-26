#!/usr/bin/env python3
"""§87.4 — move Y3 §6.3's operative pointer text INTO SCHEMA_SET_FINAL.md.

§87.2: SSF is the source of record for APPLIED TEXT. SC-12's §7.7 pointer is
applied text and was not in SSF, so SSF was INCOMPLETE. This is a one-time
correction to the source of record, not a bypass of it.

§87.3(a) SETTLED: SC-12(w) was "adopted at DELTA R35 B3"; Y3 §6.3 is headed
"Consequential and mandatory"; Y3 §7 risk 6 - "not optional … it must be applied
in the same tag". No open-decision marker anywhere in Y3. Precedent: DELTA R37/D1
already moved SC-12(w)'s applied text out of Y3 into SSF because two copies drifted.

§87.4: verbatim transcription, checked by exact substring in BOTH directions, and
Y3 §6.3 gains a note recording that its operative text now lives in SSF.
"""
import pathlib, sys

REPO = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01")
SSF = REPO / "evidence/amendment/SCHEMA_SET_FINAL.md"
Y3 = REPO / "evidence/amendment/Y3_WAIVED_ENTRY_CONDITION.md"

y3 = Y3.read_text(encoding="utf-8")

# ---- lift the operative text VERBATIM from Y3 §6.3 -------------------------
POINTER = ("> **`waived` is defined in \u00a710.2 (v30a).** That definition governs the word "
           "wherever it appears, including this table, and **SC-12(w) registers \nthe condition "
           "under which a detector-case may be reported in this state.** Neither is restated here.")
# Y3 wraps the blockquote; match on its unwrapped form to lift the real bytes.
start = y3.index("> **`waived` is defined in \u00a710.2 (v30a).**")
end = y3.index("Neither is restated here.", start) + len("Neither is restated here.")
verbatim = y3[start:end]
assert "SC-12(w) registers" in verbatim, "lifted text does not contain the operative clause"
print("lifted from Y3 \u00a76.3, %d chars" % len(verbatim))

# ---- insert into SSF, inside SC-12, before the SC-12(w) header -------------
ssf = SSF.read_text(encoding="utf-8")
ANCHOR = "**SC-12(w) \u2014 ENTRY CONDITION FOR \u00a77.7's `waived` COVERAGE STATE"
n = ssf.count(ANCHOR)
assert n == 1, "SC-12(w) header match %d, expected 1" % n

BLOCK = (
 "**INSERTION TEXT \u2014 \u00a77.7 pointer, after `PREREG.md` line 856 \u2014 Y3 \u00a76.3.** *(MOVED INTO THIS FILE\n"
 "at R80/\u00a787. SC-12's INSERTION POINT names this pointer as applied text and said \"The operative\n"
 "pointer text is Y3 \u00a76.3's\" \u2014 so the applied text lived outside the source of record and this file\n"
 "was INCOMPLETE. Transcribed verbatim from `Y3_WAIVED_ENTRY_CONDITION.md` \u00a76.3, which now cites this\n"
 "block as the single normative copy. Same correction DELTA R37/D1 made for SC-12(w)'s own limb text.)*\n"
 "\n"
 + verbatim + "\n"
 "\n")

ssf = ssf.replace(ANCHOR, BLOCK + ANCHOR, 1)
SSF.write_text(ssf, encoding="utf-8")
print("SCHEMA_SET_FINAL.md: \u00a77.7 pointer INSERTION TEXT block added inside SC-12")

# ---- BOTH DIRECTIONS -------------------------------------------------------
ssf2 = SSF.read_text(encoding="utf-8")
d1 = verbatim in ssf2
d2 = verbatim in Y3.read_text(encoding="utf-8")
print("  direction 1 - text now in SSF verbatim   : %s" % d1)
print("  direction 2 - text still in Y3 verbatim  : %s" % d2)
if not (d1 and d2):
    sys.exit("HALT: transcription is not verbatim in both directions")

# ---- Y3 §6.3 gains its note ------------------------------------------------
NOTE_ANCHOR = "**Replacement applied pointer text, after `PREREG.md` line 856:**"
y3b = Y3.read_text(encoding="utf-8")
assert y3b.count(NOTE_ANCHOR) == 1
NOTE = (NOTE_ANCHOR + "\n\n"
        "*(MOVED, R80/\u00a787. **The operative copy of this pointer text now lives in\n"
        "`SCHEMA_SET_FINAL.md`, inside SC-12**, as the `INSERTION TEXT \u2014 \u00a77.7 pointer` block. That file\n"
        "is the source of record for applied text; this file is the HISTORICAL SOURCE and carries the\n"
        "reasoning. The text below is retained verbatim so the derivation is auditable, and it is NOT a\n"
        "second normative copy \u2014 if the two ever differ, `SCHEMA_SET_FINAL.md` governs. This is the same\n"
        "correction DELTA R37/D1 applied to SC-12(w)'s limb text, for the same reason: one rule with two\n"
        "copies and no canonical source is the shape \u00a70.2.1 exists to forbid.)*")
Y3.write_text(y3b.replace(NOTE_ANCHOR, NOTE, 1), encoding="utf-8")
print("Y3 \u00a76.3: note recorded - SSF governs, Y3 is the historical source")
