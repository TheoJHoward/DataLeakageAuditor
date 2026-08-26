#!/usr/bin/env python3
"""B6.3 / B5.3 — file the instrument-domain lesson in its own right."""
import pathlib

H = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01/HISTORY.md")
L = H.read_text(encoding="utf-8").split("\n")
i = next(k for k, l in enumerate(L) if l.startswith("20. *(24 Aug 2026)*"))
assert L[i + 1].strip() == "", "lesson 20 does not end where expected"

LESSON = (
 "21. *(24 Aug 2026)* **An instrument's PASS is a statement about its DOMAIN, not about the "
 "world \u2014 and until the domain is measured, nobody knows which.** Lesson 20 requires a sweep to "
 "publish its population; this is the harder case, because a CHECK does not look like it has a "
 "population. It looks like it has a rule. **Ten instances, and the direction is what matters: "
 "every one narrowed what could be seen, and every one therefore produced a PASS.** The "
 "conformance walk enumerated \u00a76.2 by line and omitted one normative line. Four archive sweeps "
 "excluded the very directory the work was happening in. A count sweep excluded lines beginning "
 "with a table pipe, and three stale verification values were living in table rows. A "
 "declaration-value check had to be widened twice. A hash-count check had a vocabulary ceiling at "
 "\"eight\"; **the same check detected no NUMERALS at all**, so a count written in digits could "
 "have said anything, and it had reported PASS for its whole life; it also read \"twenty-five\" as "
 "twenty, which is worse than a miss because a wrong value can accidentally equal the right one "
 "and pass. Exemptions were keyed to a LINE rather than to a VALUE, so an exemption meant \"this "
 "line may be wrong\" rather than \"this line may say this\". A staging verification was a print "
 "with no assertion that had never once been executed. A registered condition had no command at "
 "all. **Not one of the ten was found by reviewing the instrument.** Reviewing an instrument "
 "recruits the same assumptions that built it \u2014 the reviewer and the author share a mental model "
 "of what counts as an input, and the gap lives exactly where that model is silent. **They were "
 "found by running the instrument against something outside its domain, or by accident.** The "
 "remedy is a BOUNDARY TEST: exercise the instrument at the edge of what it accepts and just "
 "beyond it, and record what it cannot see, as a property of the instrument rather than as a "
 "result about the corpus. **A mutation drawn from inside the accepted domain tests only that the "
 "instrument does what it does; it cannot test whether it does what it CLAIMS.** And an instrument "
 "whose gap is \"none\" must say how that was established: the evidence manifest's gap is none "
 "today only because a set comparison showed 248 listed and 248 on disk \u2014 the check itself can "
 "verify listed-against-disk and is structurally blind to disk-against-listed, so a file added "
 "without a manifest line would ship inside the signed tree with nothing attesting it. **Where the "
 "gap cannot be closed it is disclosed, because a verification apparatus that claims more than it "
 "delivers is the exact defect this project exists to detect in other people's pipelines.**")

L[i + 1:i + 1] = [LESSON]
H.write_text("\n".join(L), encoding="utf-8")
print("HISTORY.md: H-L21 recorded as lesson 21 (%d lines)" % len(L))
