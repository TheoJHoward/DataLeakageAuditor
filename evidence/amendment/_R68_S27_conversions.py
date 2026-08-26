#!/usr/bin/env python3
"""§27.2 + §28 — convert the ten checks that LIE, plus C2.5.

Every converted block ends in a non-zero exit on failure. Nothing here depends on
a human noticing a printed word.
"""
import pathlib

REPO = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01")
CC = REPO / "evidence/ceremony/CEREMONY_COMMANDS.md"
CP = REPO / "evidence/ceremony/COMMIT_PLAN.md"
EM = "\u2014"; S = "\u00a7"
done = []


def sub(path, old, new, label):
    s = path.read_text(encoding="utf-8")
    n = s.count(old)
    assert n == 1, "%s: match %d, expected 1" % (label, n)
    path.write_text(s.replace(old, new, 1), encoding="utf-8")
    done.append(label)
    print("  %-14s converted" % label)


# ---- 1. C2a : `|| { echo }` exits 0 -> `&&` + exit 1 ----------------------
sub(CC,
'''done
test "$missing" -eq 0 || { echo "C2a FAILED \u2014 halt"; }''',
'''done
test "$missing" -eq 0 && echo "C2a OK \u2014 all six are in the index" || {
  echo "C2a FAILED \u2014 a member of the six is not staged. HALT."; exit 1; }''',
"C2a")

# ---- 2. C2d-2 : "DISAGREE — HALT" exits 0 -> exit 1 ----------------------
sub(CC,
'''[ "$ACTUAL" = "$POINTER" ] && [ "$ACTUAL" = "$MANIFEST" ] \\
  && echo "AGREE \u2014 proceed" || echo "DISAGREE \u2014 HALT"''',
'''if [ "$ACTUAL" = "$POINTER" ] && [ "$ACTUAL" = "$MANIFEST" ]; then
  echo "C2d-2 OK \u2014 declaration, pointer and manifest agree"
else
  echo "C2d-2 FAILED \u2014 the three do not agree. HALT."; exit 1
fi''',
"C2d-2")

# ---- 3. C2g(ii) : trailing git status masks C2g(i)'s verdict -------------
sub(CC,
'''  printf '%s  %s\\n' "$(git show "HEAD:$f" | sha256sum | cut -d' ' -f1)" "$f"
done | diff - v30a.hashes.txt && echo "C2g OK \u2014 the commit carries exactly what was hashed"

git status --porcelain''',
'''  printf '%s  %s\\n' "$(git show "HEAD:$f" | sha256sum | cut -d' ' -f1)" "$f"
done | diff - v30a.hashes.txt || { echo "C2g FAILED \u2014 the commit does not carry what was hashed. HALT."; exit 1; }
echo "C2g OK \u2014 the commit carries exactly what was hashed"

# The tree must be clean apart from the three known untracked paths. This ran as a
# bare `git status --porcelain` until R68, AFTER the diff above \u2014 so the block's exit
# status was git status's, always 0, and C2g's real verdict was discarded by the line
# following it. It is now an assertion, and it runs after the diff has already halted.
unexpected=$(git status --porcelain | grep -vE '^\\?\\? (\\.claude/|tagmsg\\.txt|v30a\\.hashes\\.txt)$' || true)
if [ -n "$unexpected" ]; then
  echo "C2g FAILED \u2014 unexpected working-tree state:"; printf '%s\\n' "$unexpected"; exit 1
fi
echo "C2g OK \u2014 only the three expected untracked paths"''',
"C2g(ii)")

# ---- 4. C1b : key IDENTITY, not just signature validity (§28) ------------
sub(CC,
'''```sh
git tag -v prereg-v30a
```''',
'''```sh
# C1b \u2014 GOOD SIGNATURE **AND THE RIGHT KEY**. Both, or halt.
#
# Until R68 this step was `git tag -v prereg-v30a` and a human reading gpg's prose
# for the fingerprint. `git tag -v` exits 0 for a good signature from ANY key the
# local keyring can verify \u2014 so the exit status attested "signed by a key", while
# the tag message asserts "signed by THIS key". Demonstrated at R68: a tag signed
# by a throwaway key, carrying a message that asserts the registration fingerprint,
# passed `git tag -v` with exit status 0.
#
# The expected fingerprint is NOT restated here. It is read from the signed object's
# own message, so the check is: *the object asserts fingerprint X; prove gpg agrees
# the signature over that object came from X.*
#
# Anchored on `--raw`'s machine-readable [GNUPG:] status lines, never on gpg's prose,
# which is localized and version-dependent. VALIDSIG's LAST field is the PRIMARY key
# fingerprint (verified against prereg-v30 this pass), so a future subkey signature
# still resolves to the registration key.
raw=$(git verify-tag --raw prereg-v30a 2>&1)
body=$(git cat-file tag prereg-v30a)

printf '%s\\n' "$raw" | grep -q '^\\[GNUPG:\\] GOODSIG ' || {
  echo "C1b FAILED \u2014 not a good signature (expired, revoked, or unverifiable). HALT."; exit 1; }

asserted=$(printf '%s\\n' "$body" | sed -n 's/^Key fingerprint = //p' | tr -d ' ' | tr 'a-f' 'A-F')
actual=$(printf '%s\\n' "$raw" | awk '/^\\[GNUPG:\\] VALIDSIG /{print $NF}')

[ -n "$asserted" ] || { echo "C1b FAILED \u2014 the tag message states no fingerprint. HALT."; exit 1; }
[ "$asserted" = "$actual" ] || {
  echo "C1b FAILED \u2014 signed by $actual, but the message asserts $asserted. HALT."; exit 1; }
echo "C1b OK \u2014 good signature, primary key $actual, matching the message"
```''',
"C1b")

# ---- 5-7. V1a / V1b / V1c : counters + exit 1 ----------------------------
sub(CP,
'''for p in $intended; do
  [ -d "$p" ] && continue
  git diff --quiet HEAD -- "$p" && continue          # identical to HEAD: nothing to print
  git diff --cached --quiet HEAD -- "$p" && echo "V1a NOT STAGED: $p"
done
# EXPECT no output.''',
'''v1a=0
for p in $intended; do
  [ -d "$p" ] && continue
  git diff --quiet HEAD -- "$p" && continue          # identical to HEAD: nothing to print
  git diff --cached --quiet HEAD -- "$p" && { echo "V1a NOT STAGED: $p"; v1a=1; }
done
[ "$v1a" -eq 0 ] || { echo "V1a FAILED. HALT."; exit 1; }
echo "V1a OK"''',
"V1a")

sub(CP,
'''git diff --cached --name-only | while IFS= read -r p; do
  ok=0
  for q in $intended; do
    case "$p" in "$q"|"$q"/*) ok=1; break;; esac
  done
  [ "$ok" = 1 ] || echo "V1b UNEXPECTED STAGED PATH: $p"
done''',
'''# NOTE: no pipe into the loop. A `cmd | while` runs the loop in a SUBSHELL, so a
# counter set inside it is lost and the check can only ever print.
v1b=0
for p in $(git diff --cached --name-only); do
  ok=0
  for q in $intended; do
    case "$p" in "$q"|"$q"/*) ok=1; break;; esac
  done
  [ "$ok" = 1 ] || { echo "V1b UNEXPECTED STAGED PATH: $p"; v1b=1; }
done
[ "$v1b" -eq 0 ] || { echo "V1b FAILED. HALT."; exit 1; }
echo "V1b OK"''',
"V1b")

sub(CP,
'''eval "$(grep -m1 '^FILES=' evidence/ceremony/CEREMONY_COMMANDS.md)"
for f in $FILES; do
  git show ":$f" >/dev/null 2>&1 || { echo "V1c NOT IN INDEX: $f"; continue; }
  git show ":$f" | cmp -s - "$f"  || echo "V1c INDEX != WORKTREE: $f"
done
# EXPECT no output. Any line from V1a/V1b/V1c halts the ceremony.''',
'''eval "$(grep -m1 '^FILES=' evidence/ceremony/CEREMONY_COMMANDS.md)"
v1c=0
for f in $FILES; do
  git show ":$f" >/dev/null 2>&1 || { echo "V1c NOT IN INDEX: $f"; v1c=1; continue; }
  git show ":$f" | cmp -s - "$f"  || { echo "V1c INDEX != WORKTREE: $f"; v1c=1; }
done
[ "$v1c" -eq 0 ] || { echo "V1c FAILED. HALT."; exit 1; }
echo "V1c OK \u2014 all six staged at their worktree bytes"''',
"V1c")

# ---- 8. V4 : "FAILED" exits 0 -> exit 1 ---------------------------------
sub(CP,
'''[ "$hashed" -eq "$((staged - 1 + uplines))" ] && echo "V4 OK" || echo "V4 FAILED"''',
'''[ "$hashed" -eq "$((staged - 1 + uplines))" ] || {
  echo "V4 FAILED \u2014 hashed=$hashed staged=$staged uplines=$uplines. HALT."; exit 1; }
echo "V4 OK"''',
"V4")

# ---- 9. V5 : bare grep, INVERTED exit -----------------------------------
sub(CP,
'''git diff --cached | grep -n '\u00abCEREMONY-FILL'               # MUST return nothing''',
'''# A bare `grep` here was INVERTED: it exits 1 when it finds nothing, i.e. non-zero
# on success and zero on failure. Wired into any `set -e` runner it halted on a clean
# tree and passed on a dirty one.
if git diff --cached | grep -n '\u00abCEREMONY-FILL'; then
  echo "V5 FAILED \u2014 an unfilled \u00abCEREMONY-FILL\u00bb placeholder reached the index. HALT."; exit 1
fi
echo "V5 OK \u2014 no placeholder staged"''',
"V5")

# ---- 10. V6 : grep -c, INVERTED exit ------------------------------------
sub(CP,
'''git diff --cached -- DEVIATIONS.md | grep -c '^-[^-]'      # MUST be 0''',
'''# Same inversion as V5, and worse: `grep -c` prints a count, so the human had to
# read a number rather than a verdict.
removed=$(git diff --cached -- DEVIATIONS.md | grep -c '^-[^-]' || true)
[ "$removed" -eq 0 ] || {
  echo "V6 FAILED \u2014 $removed line(s) removed from DEVIATIONS.md; PREREG \u00a711 item 6 is append-only. HALT."; exit 1; }
echo "V6 OK \u2014 append-only holds"''',
"V6")

print("\\nconverted: %d \u2014 %s" % (len(done), ", ".join(done)))
