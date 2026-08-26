#!/usr/bin/env python3
"""DELTA R67 / §14.3(c) + §19.6 - the §D.3 interpretation entries.

§D.3 already exists and already carries the bounding rule. Three entries are
appended under it: (i) and (ii) are §14.3(c)'s two registered values, in the two
distinct categories the ruling names; (iii) records R7's disposition and the
label-vs-predicate distinction that produced it (§14.2(b)).

Note the corroboration, found rather than assumed: §D.3's existing text already
reads R7 as "reading 'both' as the executed five, not as a licence to publish
two" - the inheritance reading, written before the R67 survey and independent of it.
"""
import pathlib

P = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01/"
                 "AVAILABILITY_DECLARATION.md")
s = P.read_text(encoding="utf-8")
EM = "\u2014"; S = "\u00a7"

ANCHOR = ("this rule governs anything appended after them.\n"
          "\n"
          "## " + S + "E. Gate protocol input surface")

ENTRIES = """this rule governs anything appended after them.

#### D.3 entries {em} the registered hash-set language, read (R67/{s}14.3)

`PREREG.md` specifies the tag message's hash block in two places, written when the set was
smaller. **Neither is edited** {em} both are registered text. They fall into two **distinct**
categories, and collapsing them would hide the difference that matters.

**(i) `PREREG.md` {s}11 item 3 {em} a FLOOR, satisfied and exceeded. NOT violated.**
Registered text: *"SHA-256 of `PREREG.md`, `DESIGN.md`, and `HISTORY.md` as committed in the tag
message and the README."* It carries **no "only" and no "exactly"**, so it states a minimum, and a
superset satisfies it. **Over-delivery is strictly stronger**, so {s}0.2.1's "an amendment weaker
than the thing it amends is not one" is *satisfied* here rather than strained. The executed
`prereg-v30` tag already carried five, and v30a carries six; both include item 3's three. **A reader
who takes item 3 as exhaustive would conclude the v30 tag over-delivered.** That reading is
available on the text, and it is not a defect {em} it describes a tag that carried more than it had
to. The reading applied here is the floor reading; a reader is free to disagree with it.

**(ii) `PREREG.md` line 97 ({s}0.2.1) {em} NOT a floor. A closed quantifier that lost its referent.**
Registered text: *"An amendment inherits {s}11's integrity chain in full: signed tag, **both** file
hashes in the tag message, external timestamp receipt committed, repository publicly reachable at
lock."* **"Both" is a closed quantifier over exactly two things.** It is not a minimum, and it
cannot be read as one without changing the word. It was written when the block held two files;
`HISTORY.md` and the two tooling files joined later, and at that moment "both" lost its referent.
**Consequence, stated precisely:** the two files' hashes **are** in the tag message, so line 97 is
**not violated** {em} but it **supplies no rule for the files added since** and **does not govern the
current set**. The governing enumeration is `$FILES` at `CEREMONY_COMMANDS.md` {s}3.2; line 97 governs
its own two and nothing else. *(This is the same conclusion working resolution R7 reached, and R7's
own basis for it {em} that "both" is "a stale count predating `HISTORY.md` and the tooling files
joining the block" {em} is recorded as a class A mechanical fact.)*

**(iii) Working resolution R7 {em} STANDS UNAMENDED. There is no contradiction with {s}D.2.**
R7 reads: *"**R7. hash-count:** the v30a tag message carries ALL FIVE hashes, matching the
prereg-v30 tag as executed."* Read as a totality claim, that is false of a six-line message and
would put R7 against {s}D.2, which the same file hashes. **It is not a totality claim.** The survey at
R67/{s}14.2 resolved it by structure rather than by intent:

- **The predicate is true.** "Carries ALL FIVE hashes" is satisfied by any set **containing** those
  five, and the clause *"matching the prereg-v30 tag as executed"* fixes "FIVE" to the v30 five.
  A six-file set containing them satisfies it exactly.
- **The totality reading comes from the LABEL, not the predicate.** `hash-count:` is a topic tag.
  **Every label in that block is a topic tag** {em} R1 `ties`, R2 `boundary`, R3 `35-column`, R4
  `as-built defects`, R5 `weighted_mid`, R6 `weighted_mid flavor`, R7 `hash-count`, R8 `H-entry`.
  In each, the label names the QUESTION and the body supplies the ANSWER; **no label asserts a
  predicate its body does not.** The closest case is R4, whose label carries a *referent* (which
  defects) rather than a predicate {em} which is what a topic tag does.
- **The decisive structural evidence: half the block has no labels at all.** R9, R11, R12 and R13
  are recorded as bare `**R9.**`, `**R11.**` and carry their referents in the body. If labels were
  normative, dropping them would drop content; their absence is only intelligible if the label is
  an optional convenience tag.
- **Corroborated independently and earlier:** {s}D.3's own rule paragraph above already describes R7
  as *"reading 'both' as the executed five, not as a licence to publish two"* {em} the inheritance
  reading, written before this survey and not derived from it.

**So R7 stands, {s}D.2's inheritance reading is the literal reading, and nothing is edited.** The
verbatim block is not amended under any branch: it is a transcript of an author delta, and editing
it would falsify the word "verbatim" that introduces it.

**What this class of defect actually was.** None of (i){en}(iii) is arithmetically wrong. The defect
was **structural**: the set was asserted independently in many places instead of derived once, and
independent assertions drift apart {em} at R67 the same set carried **five different values** across
registered text, this declaration and the ceremony package. The remedy is not a corrected numeral
but a single authority plus a detector: `$FILES` at `CEREMONY_COMMANDS.md` {s}3.2, enforced by
`tools/check_registration.py`'s `hash_set_single_source` check, whose D5/D6 exemptions point back
at these three entries by name.

## {s}E. Gate protocol input surface""".format(em=EM, s=S, en="\u2013")

n = s.count(ANCHOR)
assert n == 1, "anchor match %d" % n
s = s.replace(ANCHOR, ENTRIES, 1)
P.write_text(s, encoding="utf-8")
print("AVAILABILITY_DECLARATION.md \u00a7D.3: entries (i), (ii), (iii) appended")
