#!/usr/bin/env python3
"""§21.7 — write C2.5, which never had a command.

Condition (ii) is scoped to §D.1 ITEM 3's "Specifically and exhaustively"
enumeration, not to §D.1 as a whole. A first draft grepped the whole section and
returned a FALSE OK: `fixture_manifest_DRAFT.json` does appear in §D.1, but inside
item 2's prose about the criterion-1 partition, not in the exhaustive list that
SC-4(k2) requires membership of. Same false-clean shape this project keeps hitting.
"""
import pathlib

CC = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01/"
                  "evidence/ceremony/CEREMONY_COMMANDS.md")
s = CC.read_text(encoding="utf-8")
EM = "\u2014"; SS = "\u00a7"

BLOCK = r'''### C2.5 @EM@ SC-4(k2)'s TWO CONDITIONS ON THE FIXTURE MANIFEST. A GATE, NOT A NOTE.

SC-4(k2) makes the gate read the fixture manifest's list of leaking-source columns, and imposes
two conditions on it. **SC-4(k4) indexes both as ways the limb FAILS.** Until R68 those conditions
lived only as prose in the regeneration requirements: **a condition stated by a clause and enforced
by no step.** That is the §21 class one stage earlier than a print @EM@ not a check that fails to
assert, but a check that was never written.

**Both conditions are UNMET as this is written, and this gate is expected to FAIL today.** That is
its purpose: it turns a known blocker from a paragraph somebody must remember into a step that
stops the ceremony.

```sh
# C2.5 @EM@ the manifest SC-4(k2) reads must be frozen, and must not be a draft.
MANIFEST='evidence/fixture_spike/f3/fixture_manifest_DRAFT.json'
c25=0

# (i) recorded status must not be DRAFT at the tag
status=$(python -c "import json,sys;print(json.load(open(sys.argv[1],encoding='utf-8')).get('manifest_status',''))" "$MANIFEST")
case "$status" in
  ''|*DRAFT*|*draft*) echo "C2.5 (i) FAILED @EM@ manifest_status is '$status'"; c25=1 ;;
  *)                  echo "C2.5 (i) OK @EM@ manifest_status is '$status'" ;;
esac

# (ii) the manifest must be enumerated in the declaration's SC-8(a) freeze.
#      SCOPED TO @SS@D.1 ITEM 3's "Specifically and exhaustively" list @EM@ NOT to @SS@D.1 as a whole.
#      Grepping the whole section returns a FALSE OK: the filename does appear in @SS@D.1,
#      inside item 2's prose, which is not membership of the exhaustive enumeration.
exhaustive=$(sed -n '/^### D\.1 /,/^### D\.2 /p' AVAILABILITY_DECLARATION.md \
             | sed -n '/Specifically and exhaustively/,/^4\. /p')
if printf '%s\n' "$exhaustive" | grep -q 'fixture_manifest_DRAFT\.json'; then
  echo "C2.5 (ii) OK @EM@ the manifest is enumerated in the @SS@D.1 exhaustive freeze list"
else
  echo "C2.5 (ii) FAILED @EM@ @SS@D.1 item 3's exhaustive list does not name the manifest"; c25=1
fi

[ "$c25" -eq 0 ] || { echo "C2.5 FAILED @EM@ SC-4(k4) makes each of these a limb failure. HALT."; exit 1; }
echo "C2.5 OK @EM@ both SC-4(k2) conditions hold"
```

**Why this halts rather than warns.** Tagging with either condition unmet ships an amendment whose
own gate limb is unsatisfied on the day it is signed, **by its own registered text**. `PREREG.md`
@SS@0.2.1 line 97: an amendment weaker than the thing it amends is not one.

'''.replace("@EM@", EM).replace("@SS@", SS)

ANCHOR = "## 3.4 C2 " + EM + " THE SINGLE OPERATION"
assert s.count(ANCHOR) == 1, "anchor match %d" % s.count(ANCHOR)
s = s.replace(ANCHOR, BLOCK + ANCHOR, 1)
CC.write_text(s, encoding="utf-8")
print("C2.5 written into CEREMONY_COMMANDS.md, before \u00a73.4")
