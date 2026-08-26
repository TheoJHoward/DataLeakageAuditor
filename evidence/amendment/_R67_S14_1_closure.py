#!/usr/bin/env python3
"""DELTA R67 / §14.1 + §19.4 - close blocker item 8 as SIX.

Rewrites COMMIT_PLAN.md §6 from OPEN AUTHOR DECISION to CLOSED, carrying the four
reasons verbatim in substance and NAMING the declined seventh candidate. Also:
  - retires the R7 parenthetical, which §14.2's survey resolved (R7 stands unamended);
  - converts the stale line citations to ANCHORS (§17.2) rather than re-deriving them;
  - flips blocker item 8 in the table.
"""
import pathlib

P = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01/"
                 "evidence/ceremony/COMMIT_PLAN.md")
L = P.read_text(encoding="utf-8").split("\n")
EM = "\u2014"; S = "\u00a7"

# §6 spans from its heading to the line before "## 7."
i0 = next(i for i, l in enumerate(L) if l.startswith("## 6. OPEN AUTHOR DECISION"))
i1 = next(i for i, l in enumerate(L) if l.startswith("## 7. The commit message"))
assert i1 > i0, "section bounds"
old_len = i1 - i0

NEW = """## 6. CLOSED {em} the tag message carries SIX hashes (R67/{s}14.1, blocker item 8)

**DECIDED: SIX.** The set is `$FILES` at `CEREMONY_COMMANDS.md` {s}3.2 l.180, which is the single
authority; this section records the decision, not the set.

**The declined seventh candidate, named so the record shows what was refused:**
**`PRIOR_ART_VERIFICATION.md`** {em} tracked and clean since `ffa6d94`
(sha256 `b97a28044edcff7612d6deba5a8ae9cc5f6c14b99b1d11a6414f5ba9a0e733bb`, 3,610 bytes). *The
staging half of the old {s}3.3 was already discharged: the file is in the tagged tree whatever was
decided here. Only the hashing half was open, and it is now closed against admission.*

**The four reasons:**

**(a) Six is the implemented state.** `$FILES` ({s}3.2 l.180) names six; the tag-message body
({s}3.5) enumerates six by path; and **every gate iterates the list** {em} C2a, C2b, C2c, C2, C2e,
C2f, C1c. Nothing in the chain reads a numeral. Choosing seven would mean changing the thing that
already works to match an argument, rather than the reverse.

**(b) The enumerated list is not the integrity boundary.** The tag references a commit, the commit
references a tree, and the tree fixes **every tracked file** {em} `PRIOR_ART_VERIFICATION.md`
included, since `ffa6d94`. The list's function is **citation**: it tells a reader which documents
the registration turns on and lets them check those without cloning. It is not what makes the
content tamper-evident; the commit object already does that.

**(c) The cost is real and the gain is near zero.** A seventh entry means re-touching the tag body,
`README.md`'s block, and the count literals this round is already correcting {em} at seven weeks out
from the {s}11 item 5 reachability deadline {em} to add a citation for a file whose hash is **already**
quoted inside `HISTORY.md` H-34, which the tag hashes, and whose content the tree already fixes.

**(d) It is reversible, so this is not a one-way door.** Adding a file to the block later is a
**Class B** change {em} a parameter of a locked procedure, not a change to what the registration
claims. If a later reader wants the citation, a supplement can carry it under `PREREG.md` {s}12
without disturbing this tag.

**The case for seven, preserved rather than deleted, because a closure that hides the counterargument
is not a record:**

- `{s}0.2.1` line 97: *"An amendment weaker than the thing it amends is not one."* The file is cited
  by two documents the tag hashes, and a reader verifying the **tag message alone** {em} without
  cloning the tree {em} cannot check it. **Answered by (b):** verifying the message alone was never
  the property the chain provides; the message cites, the commit protects.
- If `PRIOR_ART_VERIFICATION.md` is a **registration document** rather than an **evidence
  artifact**, {s}11 item 3's pattern says its hash belongs in the message. It is the written record of
  a kill-gate verdict, which is closer to registration than to evidence. **Answered by (d):** the
  classification question survives this decision and can be revisited without re-cutting the tag.

**Consequence for {s}D.2.** The declaration's {s}D.2 declares SIX by name and is itself hashed by the
tag, so this closure and the declaration now agree. **No {s}D.2 edit is required** {em} which was the
strongest argument for six, and it is now simply the state.

*(The R7 question that sat here is resolved and is no longer an open flag: working resolution **R7**
predicates that the v30a message "carries ALL FIVE hashes", which is **TRUE** of a six-file set
containing those five. The totality reading came from R7's topic **label**, not its predicate; the
label survey at R67/{s}14.2 established that every label in that block is a topic tag. **R7 stands
unamended and does not contradict {s}D.2.** See `AVAILABILITY_DECLARATION.md` {s}D.3 and the survey
recorded in the amendment package.)*""".format(em=EM, s=S)

L[i0:i1] = NEW.split("\n") + [""]
s = "\n".join(L)

# blocker item 8 -> closed
OLD8 = "| 8 | Six-vs-seven tag-hash decision (\u00a76) | AUTHOR | decision |"
NEW8 = "| 8 | ~~Six-vs-seven tag-hash decision (\u00a76)~~ **CLOSED as SIX, R67/\u00a714.1** | AUTHOR | **done** |"
n = s.count(OLD8); assert n == 1, "blocker item 8: match %d" % n
s = s.replace(OLD8, NEW8, 1)

# §17.2 - line citations -> anchors
CIT = [("Declaration **\u00a7D.2 (l.3420) declares SIX** by name", None),   # inside replaced block; skip
       ]
n1 = s.count("\u00a7D.2 (l.3420)")
s = s.replace("\u00a7D.2 (l.3420)", "\u00a7D.2 (heading: \"D.2 \u2014 The v30a tag message carries SIX hashes\")")
P.write_text(s, encoding="utf-8")
print("COMMIT_PLAN.md \u00a76        : OPEN -> CLOSED as SIX (%d lines -> %d)" % (old_len, len(NEW.split("\n"))+1))
print("COMMIT_PLAN.md blocker 8 : flipped to CLOSED")
print("COMMIT_PLAN.md citations : %d line-citation(s) converted to anchor" % n1)
