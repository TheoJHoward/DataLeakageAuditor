#!/usr/bin/env python3
"""DELTA R67 / A1.4 - give V1 the two-check shape, executably.

A1.1 finding: the ORIGINAL V1 was neither a completeness guard nor a superset
guard. It was `git diff --cached --name-only | sort` - a PRINT - under the words
"the staged set is exactly the intended paths, and nothing else" and "EXPECT,
exactly:". "Exactly" is SET EQUALITY, i.e. both directions, enforced by eye. There
was no assertion, no comparison command and no exit code anywhere in it.

A1.4 asks for two checks. This writes three, all executable, and derives the
intended set from §4's own `git add` lines so the list is not restated a second
time (which would be the very defect §15.2 names):

  V1a  COMPLETENESS over the subset that actually changed
  V1b  SUPERSET over everything staged
  V1c  MEMBERSHIP over $FILES - kept, because it is the only one that can see an
       unchanged-but-unstaged hashed file, which is the trap §3.3 is about and
       which completeness-over-changed-subset structurally cannot detect.
"""
import pathlib

P = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01/"
                 "evidence/ceremony/COMMIT_PLAN.md")
s = P.read_text(encoding="utf-8")
EM = "\u2014"; S = "\u00a7"

lines = s.split("\n")
i0 = next(i for i, l in enumerate(lines)
          if l.startswith("# V1 " + EM + " the staged set is exactly"))
i1 = next(i for i in range(i0, len(lines)) if lines[i].startswith("# V2 " + EM))
assert i1 > i0, "V1 block bounds"

NEW = """# THE INTENDED SET, derived from §4's own `git add` lines. Never restated here:
# a second copy of a set is the defect §15.2 names, and this file already carried
# one (the "245 paths" figure below was stale by four when R67 measured the tree).
intended=$(grep -E '^git add ' evidence/ceremony/COMMIT_PLAN.md \\
           | sed 's/^git add //' | tr ' ' '\\n' | sed '/^$/d' | sort -u)

# V1a — COMPLETENESS, over the subset that ACTUALLY CHANGED.
#       `git diff --cached --name-only` prints only paths whose staged bytes differ
#       from HEAD, so a path identical to HEAD can never appear and is not a miss.
#       Those are V1c's job, not this one.
for p in $intended; do
  [ -d "$p" ] && continue
  git diff --quiet HEAD -- "$p" && continue          # identical to HEAD: nothing to print
  git diff --cached --quiet HEAD -- "$p" && echo "V1a NOT STAGED: $p"
done
# EXPECT no output.

# V1b — SUPERSET. Nothing outside the intended set may be staged.
git diff --cached --name-only | while IFS= read -r p; do
  ok=0
  for q in $intended; do
    case "$p" in "$q"|"$q"/*) ok=1; break;; esac
  done
  [ "$ok" = 1 ] || echo "V1b UNEXPECTED STAGED PATH: $p"
done
# EXPECT no output. `.claude/` and `tagmsg.txt` are untracked and not ignored;
# either one appearing here means a blanket `git add` was used.

# V1c — MEMBERSHIP over the HASHED SIX. The only check that can see an
#       unchanged-but-unstaged hashed file. V1a cannot: an unstaged file and an
#       unchanged file are indistinguishable in `--cached` output, and `git show
#       :<path>` on a never-staged tracked file silently returns its HEAD content
#       (§3.3). The set is READ from its single authority, never restated.
eval "$(grep -m1 '^FILES=' evidence/ceremony/CEREMONY_COMMANDS.md)"
for f in $FILES; do
  git show ":$f" >/dev/null 2>&1 || { echo "V1c NOT IN INDEX: $f"; continue; }
  git show ":$f" | cmp -s - "$f"  || echo "V1c INDEX != WORKTREE: $f"
done
# EXPECT no output. Any line from V1a/V1b/V1c halts the ceremony.

# For the human reader, and NOT the check — the check is above:
#   expected to appear (modified by this ceremony): AVAILABILITY_DECLARATION.md
#   [hashed], DESIGN.md [hashed], HISTORY.md [hashed], tools/check_registration.py
#   [hashed], DEVIATIONS.md, README.md, and the evidence tree.
#   expected NOT to appear while unchanged, which is CORRECT and not a miss:
#   PREREG.md [hashed] — locked, byte-identical to v30 BY DESIGN and must stay so;
#   protocol/runtime_reference.py [hashed] — expected identical to v30;
#   PRIOR_ART_VERIFICATION.md — tracked and clean since ffa6d94.
# If either HASHED file in the second group DOES appear, that is a finding to
# record, not a typo to correct (CEREMONY_COMMANDS.md §3.1 item 4: "Expected
# identical" is a prediction to be tested, not a value to be copied).
#
# *(R67/A1: this block replaced a PRINT. The original V1 ran
# `git diff --cached --name-only | sort` under the words "EXPECT, exactly:" and
# listed PREREG.md among the expected paths. PREREG.md is byte-identical to v30 by
# design, so under set equality that list could never have been satisfied. Per the
# run record the ceremony has never been executed — no `prereg-v30a` tag, no
# `v30a.hashes.txt`, and §0 of CEREMONY_COMMANDS.md states in terms that nothing in
# it has been run — so V1 never passed and never failed. It had never been
# exercised at all.)*
"""
lines[i0:i1] = NEW.split("\n")
P.write_text("\n".join(lines), encoding="utf-8")
print("COMMIT_PLAN \u00a74.1: V1 print -> V1a completeness / V1b superset / V1c membership, all executable")
print("                 intended set DERIVED from \u00a74's git add lines; stale '245 paths' removed")
