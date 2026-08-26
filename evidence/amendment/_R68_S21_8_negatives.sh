#!/bin/bash
# §21.8 — every converted check: run clean, then run against a deliberate failure.
# Each block below is the CONVERTED code, executed in an isolated scratch repo.
# A conversion counts only if the clean run exits 0 AND the broken run exits non-zero.

SCR="$1"
PASS=0; FAIL=0
report() {  # name, clean_rc, broken_rc
  if [ "$2" -eq 0 ] && [ "$3" -ne 0 ]; then
    printf "  %-10s clean=exit0  broken=exit%-3s  FIRED\n" "$1" "$3"; PASS=$((PASS+1))
  else
    printf "  %-10s clean=exit%-3s broken=exit%-3s  *** NOT PROVEN ***\n" "$1" "$2" "$3"; FAIL=$((FAIL+1))
  fi
}

setup() {
  rm -rf "$SCR/r"; mkdir -p "$SCR/r/tools" "$SCR/r/protocol" "$SCR/r/evidence/ceremony"
  cd "$SCR/r" || exit 1
  git init -q .; git config user.email t@t; git config user.name t
  for f in PREREG.md DESIGN.md HISTORY.md AVAILABILITY_DECLARATION.md README.md DEVIATIONS.md; do echo "base $f" > "$f"; done
  echo "base tool" > tools/check_registration.py
  echo "base proto" > protocol/runtime_reference.py
  printf 'FILES="PREREG.md DESIGN.md HISTORY.md tools/check_registration.py protocol/runtime_reference.py AVAILABILITY_DECLARATION.md"\n' \
    > evidence/ceremony/CEREMONY_COMMANDS.md
  printf 'git add PREREG.md DEVIATIONS.md HISTORY.md DESIGN.md README.md\ngit add AVAILABILITY_DECLARATION.md\ngit add tools/check_registration.py protocol/runtime_reference.py\ngit add evidence\n' \
    > evidence/ceremony/COMMIT_PLAN.md
  git add -A >/dev/null 2>&1; git commit -qm base
  eval "$(grep -m1 '^FILES=' evidence/ceremony/CEREMONY_COMMANDS.md)"
  intended=$(grep -E '^git add ' evidence/ceremony/COMMIT_PLAN.md | sed 's/^git add //' | tr ' ' '\n' | sed '/^$/d' | sort -u)
}

# ---------- C2a : every member of the six is in the index -----------------
c2a() { missing=0
  for f in $FILES; do git show ":$f" >/dev/null 2>&1 || missing=1; done
  test "$missing" -eq 0 && echo "C2a OK" || { echo "C2a FAILED"; exit 1; }; }
setup; ( c2a ) >/dev/null 2>&1; A=$?
setup; git rm -q --cached tools/check_registration.py >/dev/null 2>&1; ( c2a ) >/dev/null 2>&1; B=$?
report C2a $A $B

# ---------- V1c : index bytes == worktree bytes ---------------------------
v1c() { v=0
  for f in $FILES; do
    git show ":$f" >/dev/null 2>&1 || { v=1; continue; }
    git show ":$f" | cmp -s - "$f" || v=1
  done
  [ "$v" -eq 0 ] || { echo "V1c FAILED"; exit 1; }; echo "V1c OK"; }
setup; ( v1c ) >/dev/null 2>&1; A=$?
setup; echo "edited after staging" >> HISTORY.md; ( v1c ) >/dev/null 2>&1; B=$?
report V1c $A $B

# ---------- V1a : intended-and-changed must be staged ---------------------
v1a() { v=0
  for p in $intended; do
    [ -d "$p" ] && continue
    git diff --quiet HEAD -- "$p" && continue
    git diff --cached --quiet HEAD -- "$p" && { echo "NOT STAGED: $p"; v=1; }
  done
  [ "$v" -eq 0 ] || { echo "V1a FAILED"; exit 1; }; echo "V1a OK"; }
setup; echo change >> DESIGN.md; git add DESIGN.md; ( v1a ) >/dev/null 2>&1; A=$?
setup; echo change >> DESIGN.md;                    ( v1a ) >/dev/null 2>&1; B=$?
report V1a $A $B

# ---------- V1b : nothing outside the intended set is staged --------------
v1b() { v=0
  for p in $(git diff --cached --name-only); do
    ok=0; for q in $intended; do case "$p" in "$q"|"$q"/*) ok=1; break;; esac; done
    [ "$ok" = 1 ] || { echo "UNEXPECTED: $p"; v=1; }
  done
  [ "$v" -eq 0 ] || { echo "V1b FAILED"; exit 1; }; echo "V1b OK"; }
setup; echo change >> DESIGN.md; git add DESIGN.md; ( v1b ) >/dev/null 2>&1; A=$?
setup; echo junk > tagmsg.txt;   git add -f tagmsg.txt; ( v1b ) >/dev/null 2>&1; B=$?
report V1b $A $B

# ---------- V4 : manifest-line arithmetic ---------------------------------
v4() { [ "$hashed" -eq "$((staged - 1 + uplines))" ] || { echo "V4 FAILED"; exit 1; }; echo "V4 OK"; }
staged=249; hashed=251; uplines=3; ( v4 ) >/dev/null 2>&1; A=$?
staged=249; hashed=246; uplines=3; ( v4 ) >/dev/null 2>&1; B=$?
report V4 $A $B

# ---------- V5 : no unfilled placeholder reached the index ----------------
v5() { if git diff --cached | grep -n 'CEREMONY-FILL' >/dev/null; then echo "V5 FAILED"; exit 1; fi; echo "V5 OK"; }
setup; echo clean >> DESIGN.md; git add DESIGN.md; ( v5 ) >/dev/null 2>&1; A=$?
setup; echo 'x CEREMONY-FILL y' >> DEVIATIONS.md; git add DEVIATIONS.md; ( v5 ) >/dev/null 2>&1; B=$?
report V5 $A $B

# ---------- V6 : DEVIATIONS.md append-only --------------------------------
v6() { removed=$(git diff --cached -- DEVIATIONS.md | grep -c '^-[^-]' || true)
  [ "$removed" -eq 0 ] || { echo "V6 FAILED"; exit 1; }; echo "V6 OK"; }
setup; printf 'line1\nline2\n' > DEVIATIONS.md; git add DEVIATIONS.md; git commit -qm d
        printf 'line1\nline2\nline3\n' > DEVIATIONS.md; git add DEVIATIONS.md; ( v6 ) >/dev/null 2>&1; A=$?
setup; printf 'line1\nline2\n' > DEVIATIONS.md; git add DEVIATIONS.md; git commit -qm d
        printf 'line1\n'            > DEVIATIONS.md; git add DEVIATIONS.md; ( v6 ) >/dev/null 2>&1; B=$?
report V6 $A $B

# ---------- C2d-2 : three-way agreement -----------------------------------
c2d2() { if [ "$ACTUAL" = "$POINTER" ] && [ "$ACTUAL" = "$MANIFEST" ]; then echo OK; else echo "FAILED"; exit 1; fi; }
ACTUAL=aaa; POINTER=aaa; MANIFEST=aaa; ( c2d2 ) >/dev/null 2>&1; A=$?
ACTUAL=aaa; POINTER=bbb; MANIFEST=aaa; ( c2d2 ) >/dev/null 2>&1; B=$?
report C2d-2 $A $B

# ---------- C2g(ii) : no unexpected working-tree state --------------------
c2g2() { u=$(git status --porcelain | grep -vE '^\?\? (\.claude/|tagmsg\.txt|v30a\.hashes\.txt)$' || true)
  if [ -n "$u" ]; then echo "C2g FAILED"; exit 1; fi; echo "C2g OK"; }
setup; echo x > tagmsg.txt; echo y > v30a.hashes.txt; ( c2g2 ) >/dev/null 2>&1; A=$?
setup; echo x > tagmsg.txt; echo "unstaged edit" >> PREREG.md; ( c2g2 ) >/dev/null 2>&1; B=$?
report C2g\(ii\) $A $B

# ---------- C2.5 : SC-4(k2)'s two conditions ------------------------------
c25() { c=0
  case "$STATUS" in ''|*DRAFT*|*draft*) c=1;; esac
  printf '%s\n' "$FREEZE" | grep -q 'fixture_manifest_DRAFT\.json' || c=1
  [ "$c" -eq 0 ] || { echo "C2.5 FAILED"; exit 1; }; echo "C2.5 OK"; }
STATUS="FROZEN 2026-08-24"; FREEZE="... the manifest fixture_manifest_DRAFT.json ..."; ( c25 ) >/dev/null 2>&1; A=$?
STATUS="DRAFT - author review required"; FREEZE="... nothing ..."; ( c25 ) >/dev/null 2>&1; B=$?
report C2.5 $A $B

echo ""
echo "  CONVERSIONS PROVEN: $PASS   NOT PROVEN: $FAIL"
cd /; rm -rf "$SCR/r"
