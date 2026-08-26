#!/usr/bin/env python3
"""§30.3 — file the sweep-population rule as its own lesson, NOT folded into H-L15."""
import pathlib

H = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01/HISTORY.md")
L = H.read_text(encoding="utf-8").split("\n")
i = next(k for k, l in enumerate(L) if l.startswith("19. *(24 Aug 2026)*"))
assert L[i + 1].strip() == "", "lesson 19 does not end where expected"

LESSON = (
 "20. *(24 Aug 2026)* **A sweep result is not a result until its POPULATION and its EXCLUSIONS are "
 "stated with it.** Lesson 15 requires an absence finding to state its population and prove it "
 "covered the whole of it; this is that rule made **prospective**, and it is separate because it "
 "binds at a different moment. Lesson 15 is applied when a finding is written. This one binds when "
 "the sweep is DESIGNED, because by the time the finding is written the exclusion has already "
 "become invisible: it is a line of code, not a claim, and nobody reviews it as a claim. **The "
 "instance.** A sweep for count literals across the shipping corpus reported eleven verified sites "
 "and closed. Its matcher skipped every line beginning with a table pipe \u2014 a reasonable-looking "
 "choice, made because tables are mostly data \u2014 and **three stale declaration hashes and byte "
 "sizes lived in table rows**, so they were never in the population at all. They surfaced a round "
 "later, by accident, in the output of an unrelated command. The sweep was not wrong about what it "
 "examined; it was silent about what it did not, and a silence about coverage reads exactly like "
 "coverage. **The rule: state the population definition and the explicit exclusion list WITH the "
 "result, before anyone finds the gap.** And where an exclusion cannot be justified on the record, "
 "**it is not an exclusion, it is a miss \u2014 re-run rather than caveat.** A caveat added after the "
 "gap is found is a description of the gap, not a defence of the method. **The same discipline "
 "applies to a check's exemption list**, which is a population definition wearing different "
 "clothes: an exemption keyed to a line rather than to a value licenses every future error on that "
 "line, which is how the declaration-hash check passed a freshly injected wrong hash on an "
 "exempted line until its own negative test caught it.")

L[i + 1:i + 1] = [LESSON]
H.write_text("\n".join(L), encoding="utf-8")
print("HISTORY.md: H-L20 recorded as lesson 20 (%d lines)" % len(L))
