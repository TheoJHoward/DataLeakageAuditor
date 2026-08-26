#!/usr/bin/env python3
"""§21.5 — file H-L19, with this round's 245-vs-249 as its EVIDENCE.

H-L13 (lesson 13) already covers a numeral that POINTS AT an enumeration going
stale, and already draws the closure-constraint exception. H-L19 is the adjacent
but distinct failure: a rule RESTATED as a literal in many places FORKS into
several values, none of which is a reference to the others. It cites 13 rather
than repeating it.
"""
import pathlib

H = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01/HISTORY.md")
L = H.read_text(encoding="utf-8").split("\n")
i = next(k for k, l in enumerate(L)
         if l.startswith("18. *(21 Aug 2026)* **A registered redesign changes"))
assert L[i + 1].strip() == "", "lesson 18 does not end where expected"

LESSON = (
 "19. *(24 Aug 2026)* **A rule restated as a literal does not merely go stale \u2014 it FORKS.** "
 "Lesson 13 covers a numeral that *points at* an enumeration and goes stale when the target grows; "
 "this is the adjacent failure, and its signature is different. The v30a tag message's hash set is "
 "defined once, as `FILES=` in the ceremony's \u00a73.2, and every gate in the ceremony iterates that "
 "list \u2014 **no gate reads a numeral at all.** The count was nevertheless restated in prose about "
 "thirty-nine times, and by August 2026 the same set was being asserted with **five different "
 "values**: **two** (`PREREG.md` line 97's \"both file hashes\", a closed quantifier written when "
 "the block held two files), **three** (\u00a711 item 3's enumeration by path), **five** (working "
 "resolution R7, true of the inherited v30 five), **six** (the declaration's \u00a7D.2 and the whole "
 "ceremony package) and **seven** (an open author decision that had sat unresolved for twenty "
 "rounds). Each was locally plausible and none was a reference to the others, so nothing could "
 "disagree with anything: **independent assertions do not contradict, they diverge.** "
 "**The evidence that this is structural and not carelessness is that it recurred inside the round "
 "that named it.** While rewriting the staging plan to fix the defect, the agent doing the fixing "
 "carried the figure \"245 paths\" forward into its own new text without re-deriving it; the tree "
 "had been 249 files for some time. The same round then drifted two line-keyed detector exemptions "
 "by sixty-four lines by inserting a section above them, and found three cross-references that had "
 "been one hundred and sixty-nine lines out of date. **A count that is not computed from the thing "
 "it counts is not a description of that thing; it is an independent claim about it, and "
 "independent claims drift apart.** The remedy is never a corrected numeral, because a corrected "
 "numeral is the same object again: it is **one authority plus a check that fails when a "
 "restatement disagrees with it**, and where a count cannot be mechanised, the form lesson 13's own "
 "neighbours already use \u2014 state the count, name the enumeration, and pre-empt the likely "
 "miscount, as the H-B addendum does with \"a verifier counting entries rather than firings will "
 "get twenty-three; the reconciliation is here.\" **Lesson 13's exception is carried forward "
 "unchanged and matters more here, not less:** a numeral that *forbids* growth is a closure "
 "constraint, not a reference, and deriving it away deletes the rule. The test is unchanged \u2014 ask "
 "what happens when the target grows. **And the corollary that makes this checkable: a check whose "
 "failure mode is \"the human did not notice\" is not a check.** The staging verification that "
 "should have caught the miscount was `git diff --cached --name-only | sort` under the words "
 "\"EXPECT, exactly\" \u2014 a print with no assertion, which had never been executed, and whose "
 "expected list named a file that is byte-identical to the previous tag by design and therefore "
 "could never have appeared in it.")

L[i + 1:i + 1] = [LESSON]
H.write_text("\n".join(L), encoding="utf-8")
print("HISTORY.md: H-L19 recorded as lesson 19 (%d lines)" % len(L))
