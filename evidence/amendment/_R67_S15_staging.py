#!/usr/bin/env python3
"""DELTA R67 / §15 - the staging defect.

§15.1 adds the two tooling files to COMMIT_PLAN.md §4's `git add` set and to V1's
EXPECT list. Executing the V1 half LITERALLY would install a known-false gate:
`git diff --cached --name-only` prints only paths whose STAGED bytes differ from
HEAD, and `protocol/runtime_reference.py` is identical to HEAD (verified this pass).
The EXPECT list already carries that bug for `PREREG.md`, which is locked and
byte-identical to v30 by design and therefore can never appear.

So V1's list is split into ALWAYS-APPEARS and MUST-NOT-APPEAR-WHILE-UNCHANGED.
Both halves together name all six, which is what §16.2 D4 asserts. A new V1b tests
MEMBERSHIP, and derives the set from CEREMONY_COMMANDS.md §3.2 l.180 rather than
restating it - restating it would be §15.2's own defect in a third costume.
"""
import pathlib, sys

P = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01/"
                 "evidence/ceremony/COMMIT_PLAN.md")
s = P.read_text(encoding="utf-8")
orig = s
EM = "\u2014"

# ---- edit 1: the git add set ------------------------------------------------
OLD1 = ("# (3) the evidence tree " + EM + " currently untracked\n"
        "git add evidence\n")
NEW1 = ("# (3) the checking tools " + EM + " BOTH ARE IN THE HASHED SIX, and both were absent from\n"
        "#     this block until R67/" + "\u00a7" + "15. `tools/check_registration.py` is ` M ` today.\n"
        "#     A hashed file that is never `git add`ed does not fail: `git show :<path>`\n"
        "#     silently returns its HEAD content, so the tag is signed over bytes the\n"
        "#     author never approved (CEREMONY_COMMANDS.md " + "\u00a7" + "3.3). `git add` on the\n"
        "#     unchanged one is a no-op and is named anyway, because the set is the\n"
        "#     authority " + EM + " not which members happen to be dirty this pass.\n"
        "git add tools/check_registration.py protocol/runtime_reference.py\n"
        "\n"
        "# (4) the evidence tree " + EM + " currently untracked\n"
        "git add evidence\n")
n = s.count(OLD1)
assert n == 1, "edit 1: match count %d, expected 1" % n
s = s.replace(OLD1, NEW1, 1)

# ---- edit 2: V1's EXPECT list, split by what git can actually print ---------
OLD2 = ("# EXPECT, exactly:\n"
        "#   AVAILABILITY_DECLARATION.md\n"
        "#   DESIGN.md\n"
        "#   DEVIATIONS.md\n"
        "#   HISTORY.md\n"
        "#   PREREG.md\n"
        "#   README.md\n"
        "#   evidence/...            (245 paths)\n"
        "# PRIOR_ART_VERIFICATION.md will NOT appear " + EM + " it is unchanged, and that is correct.\n"
        "# Any other path, and the commit is wrong. `.claude/` and `tagmsg.txt` MUST NOT appear.\n")
NEW2 = ("# EXPECT, exactly. `git diff --cached --name-only` prints ONLY paths whose staged\n"
        "# bytes differ from HEAD, so the intended set splits in two. The two halves together\n"
        "# must cover the hashed six ($FILES, CEREMONY_COMMANDS.md " + "\u00a7" + "3.2 l.180); that coverage\n"
        "# is the only relation between this list and the hash set.\n"
        "#\n"
        "#   ALWAYS APPEARS " + EM + " modified by this ceremony:\n"
        "#     AVAILABILITY_DECLARATION.md      [hashed]\n"
        "#     DESIGN.md                        [hashed]\n"
        "#     HISTORY.md                       [hashed]\n"
        "#     tools/check_registration.py      [hashed]\n"
        "#     DEVIATIONS.md                    (D-001 appended at ceremony time)\n"
        "#     README.md                        (v30a block written at ceremony time)\n"
        "#     evidence/...                     (245 paths, all new)\n"
        "#\n"
        "#   MUST NOT APPEAR WHILE UNCHANGED " + EM + " absence here is CORRECT, not a missed file:\n"
        "#     PREREG.md                        [hashed] locked; byte-identical to v30 BY DESIGN\n"
        "#     protocol/runtime_reference.py    [hashed] expected identical to v30\n"
        "#     PRIOR_ART_VERIFICATION.md        tracked and clean since ffa6d94\n"
        "#\n"
        "# If either HASHED file in the second group DOES appear, that is a finding to record,\n"
        "# not a typo to correct (CEREMONY_COMMANDS.md " + "\u00a7" + "3.1 item 4: \"Expected identical\" is a\n"
        "# prediction to be tested, not a value to be copied).\n"
        "# Any other path, and the commit is wrong. `.claude/` and `tagmsg.txt` MUST NOT appear.\n"
        "\n"
        "# V1b " + EM + " MEMBERSHIP, not appearance. This is the check V1 cannot make: absence from\n"
        "#       V1's first group proves nothing at all, because an unstaged file and an\n"
        "#       unchanged file are indistinguishable in that output. The set is READ from its\n"
        "#       single authority, never restated here " + EM + " a second copy of the list is exactly\n"
        "#       the defect " + "\u00a7" + "15.2 names.\n"
        "eval \"$(grep -m1 '^FILES=' evidence/ceremony/CEREMONY_COMMANDS.md)\"\n"
        "for f in $FILES; do\n"
        "  git show \":$f\" >/dev/null 2>&1 || { echo \"NOT IN INDEX: $f\"; break; }\n"
        "  git show \":$f\" | cmp -s - \"$f\"  || { echo \"INDEX != WORKTREE: $f\"; break; }\n"
        "done\n"
        "# EXPECT no output. Any line here halts the ceremony.\n")
n = s.count(OLD2)
assert n == 1, "edit 2: match count %d, expected 1" % n
s = s.replace(OLD2, NEW2, 1)

assert s != orig
P.write_text(s, encoding="utf-8")
print("COMMIT_PLAN.md \u00a74   : tooling files added to the git add set as group (3); evidence -> (4)")
print("COMMIT_PLAN.md \u00a74.1 : V1 EXPECT split (always-appears / must-not-appear-while-unchanged)")
print("COMMIT_PLAN.md \u00a74.1 : V1b added - membership test, set read from CEREMONY_COMMANDS \u00a73.2")
