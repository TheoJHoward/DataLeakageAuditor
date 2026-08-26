#!/usr/bin/env python3
"""DELTA R55/A2 - record the re-anchor observation as review lesson H-L17."""
import pathlib

REPO = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01")
h = REPO / "HISTORY.md"
L = h.read_text(encoding="utf-8").split("\n")

i = next(k for k, l in enumerate(L) if l.startswith("16. *(21 Aug 2026)* A check written to replace a failed check"))
assert L[i + 1].strip() == "", "lesson 16 does not end where expected"

LESSON = ('17. *(21 Aug 2026)* One tool produced three separate failures in one session and each was '
          'patched where it surfaced before anyone asked what they had in common. A re-anchoring tool '
          'recomputes manifest line ranges after the source document moves. Its failures: a marker '
          'extracted without its trailing newline made the growth figure one short, leaving every '
          'shifted row one line shy of its block; a pairing rule matched blocks by start line, so an '
          'earlier block growing made a later changed block read as one block removed and a different '
          'one added; and sub-entry boundaries were shifted through a block that had grown from three '
          'lines to twenty-five, leaving one sub-entry pointing at text that was no longer there. '
          '**All three are the same assumption: that every change is DISPLACEMENT.** A block that '
          'moved but whose content is identical is displaced, and arithmetic on its offsets is valid. '
          'A block whose own content changed has **invalidated every boundary inside it**, and no '
          'offset arithmetic can recover them \u2014 they have to be re-derived from the markers in the '
          'source. **Patching each instance leaves the assumption in place, which is why there were '
          'three; the fix belongs at the coupling**, and the tool now detects which case it is in and '
          '**refuses** to shift sub-entries through a block that grew internally, reporting them for '
          're-derivation instead of guessing. **The sharper half is which checks saw any of it.** Not '
          'the re-anchoring tool \u2014 its arithmetic was self-consistent every time and it reported '
          'success. Every one of the three was caught by a check that goes back to the SOURCE and '
          'compares text: byte-exact containment of a source block in its hunk, and a character-count '
          'proof over reconstructed content. **A check that re-derives from source catches what a '
          'check that recomputes offsets cannot, because the second one shares the first one\'s '
          'assumption** \u2014 they are not two independent opinions, they are one opinion stated twice. '
          'Where a value can be either recomputed or re-read, the re-read is the check and the '
          'recomputation is the thing being checked.')

L[i + 1:i + 1] = [LESSON]
h.write_text("\n".join(L), encoding="utf-8")
print("H-L17 recorded (%d lines)" % len(L))
