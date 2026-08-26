#!/usr/bin/env python3
"""DELTA R52 / X2 + X3 - record the mutation-testing rule as review lesson H-L16."""
import pathlib

REPO = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01")
h = REPO / "HISTORY.md"
L = h.read_text(encoding="utf-8").split("\n")

i = next(k for k, l in enumerate(L) if l.startswith("15. *(21 Aug 2026)* A review reported that a registered surface"))
assert L[i + 1].strip() == "", "lesson 15 does not end where expected"
assert L[i + 2].startswith("### H-30"), L[i + 2][:40]

LESSON = ('16. *(21 Aug 2026)* A check written to replace a failed check inherited a new blind spot '
          'from its own design, and only mutation testing found it. The predecessor sampled five '
          '110-char windows of each hand-assembled amendment hunk \u2014 21% of one 2,612-char hunk \u2014 '
          'and passed every material mutation put to it, including **flipping "fails this gate row" '
          'to "is recorded as a deviation"**, which is precisely the reduction the rule it enforced '
          'exists to forbid. Its replacement tiled 100% of each hunk by longest match and caught '
          'that flip \u2014 and still passed both DELETIONS, because **coverage is deletion-blind by '
          'construction: removing text never lowers the provenance of what remains.** One blind '
          'spot had been traded for another, and reasoning about the design would not have shown '
          'it; mutating the artifact did, in one run. **A check that replaces a failed check is '
          'mutation-tested against two sets: the failures that defeated its predecessor, AND the '
          'failure modes its own design admits.** The second set is the one nobody thinks to '
          'assemble, because a check is written by someone who believes it works. **Reasoning '
          'about a check establishes its intent; mutating the artifact establishes its reach.** '
          'The fix here was a converse direction \u2014 the source block, extracted fresh and required '
          'to survive verbatim \u2014 and deletion is not a hypothetical class for this project: it is '
          'the class that produced hunk 2.33. *(A related property earned its keep in the same '
          'round and is worth naming: the interim check printed "NO SPAN DECLARED (deletion-blind, '
          'reported not assumed)" against the eight hunks it could not fully cover, rather than '
          'rounding the gap to PASS. That is this registration\'s own coverage-accounting '
          'discipline \u2014 declare the population and prove it was covered \u2014 implemented inside the '
          'verification tooling, and it is why the remaining gap was visible to be closed on '
          'purpose rather than discovered later by something failing.)*')

L[i + 1:i + 1] = [LESSON]
h.write_text("\n".join(L), encoding="utf-8")
print("H-L16 recorded (%d lines)" % len(L))
