"""A31 -- assemble the v30a amendments block and PRESENT it. Applies nothing.

R140 A31: assemble from `K2_AMENDMENT_LEDGER.md` §8.2 + §AB + §AC per
`BLOCK_MANIFEST.md` l.141, establish §8.2's own authority, and present.

THE TEXT IS EXTRACTED FROM ITS SOURCES, NEVER RETYPED, and the sources are the
ones `BLOCK_MANIFEST.md` names -- §8.2 from the ledger between its own
`K2-BLOCK-BEGIN`/`END` markers, §AB and §AC from `SCHEMA_SET_FINAL.md` by the
line ranges the manifest's §A table gives. §2.1: a presentation of a text never
becomes the text, so the assembled block below is a PRESENTATION and the
sources stay the sources.

AND IT ESTABLISHES AUTHORITY BEFORE IT ASSEMBLES, because assembling first and
asking afterwards is how an artifact becomes its own argument (§2.2 of R138's
list, and R140 §2.1). `APPROVAL_RECORD.md` §140 names exactly what the author
approved on 25 August 2026; each of the three components is checked against it.

    usage: a31_assemble.py <v30-file> <out.md>
"""
from __future__ import annotations

import hashlib
import pathlib
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:                                       # noqa: BLE001
    pass

REPO = pathlib.Path(__file__).resolve().parents[2]
LEDGER = REPO / "evidence/amendment/K2_AMENDMENT_LEDGER.md"
SSF = REPO / "evidence/amendment/SCHEMA_SET_FINAL.md"
MANIFEST = REPO / "evidence/amendment/BLOCK_MANIFEST.md"
RECORD = REPO / "evidence/ceremony/APPROVAL_RECORD.md"
OUT = pathlib.Path(sys.argv[2])


def text_of(p):
    return p.read_text(encoding="utf-8").replace("\r\n", "\n")


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


record = text_of(RECORD)
approved = set(re.findall(r"`([A-Za-z0-9_./-]+\.(?:md|diff))`\s*\|\s*`([0-9a-f]{64})`", record))
approved_files = {n for n, _ in approved}

print("=" * 78)
print("AUTHORITY -- established BEFORE anything is assembled")
print("=" * 78)
print("  APPROVAL_RECORD.md §140 names these artifacts as approved on 25 Aug 2026:")
for n, h in sorted(approved):
    on_disk = sha(REPO / "evidence/amendment" / n) if (REPO / "evidence/amendment" / n).exists() else None
    print("      %-32s %s%s" % (n, h[:16],
                                "  (on disk: %s)" % (on_disk[:16] if on_disk else "n/a")))

components = [("§8.2, the block proper", "K2_AMENDMENT_LEDGER.md"),
              ("§AB", "SCHEMA_SET_FINAL.md"),
              ("§AC", "SCHEMA_SET_FINAL.md")]
print()
print("  the three components BLOCK_MANIFEST.md l.141 names, against that list:")
unapproved = []
for what, src in components:
    ok = src in approved_files
    if not ok:
        unapproved.append((what, src))
    print("      %-24s from %-28s %s"
          % (what, src, "APPROVED" if ok else "** NOT IN THE APPROVAL **"))

# ---- extract ---------------------------------------------------------------
led = text_of(LEDGER)
lo = led.index("<!-- K2-BLOCK-BEGIN -->")
hi = led.index("<!-- K2-BLOCK-END -->")
block = led[lo + len("<!-- K2-BLOCK-BEGIN -->"):hi].strip("\n")

man = text_of(MANIFEST)
ranges = {}
for m in re.finditer(r"^\| (\d+) \| (\d+)[–-](\d+) \| (§A[BC])", man, re.M):
    ranges[m.group(4)] = (int(m.group(2)), int(m.group(3)))
if set(ranges) != {"§AB", "§AC"}:
    sys.exit("HALT: BLOCK_MANIFEST's §A table did not yield both §AB and §AC ranges; got %s"
             % sorted(ranges))
ssf = text_of(SSF).split("\n")
ab = "\n".join(ssf[ranges["§AB"][0] - 1:ranges["§AB"][1]]).strip("\n")
ac = "\n".join(ssf[ranges["§AC"][0] - 1:ranges["§AC"][1]]).strip("\n")

print()
print("  extracted: §8.2 %d lines, §AB %d lines (SSF %d-%d), §AC %d lines (SSF %d-%d)"
      % (len(block.split("\n")), len(ab.split("\n")), *ranges["§AB"],
         len(ac.split("\n")), *ranges["§AC"]))

# ---- emit ------------------------------------------------------------------
b = []
w = b.append
w("# A31 — THE v30a AMENDMENTS BLOCK, ASSEMBLED AND PRESENTED. **NOT APPLIED.**")
w("")
w("**Nothing here has been applied.** `PREREG.md` is unchanged by this document.")
w("R140 A31: *present for approval; do not apply.*")
w("")
w("---")
w("")
w("## 1. AUTHORITY — and this is where it stops")
w("")
w("`APPROVAL_RECORD.md` §140 records what the author approved on **25 August 2026**, and it is")
w("a closed list of three artifacts:")
w("")
w("| artifact | sha256 |")
w("|---|---|")
for n, h in sorted(approved):
    w("| `%s` | `%s…` |" % (n, h[:16]))
w("| `PREREG.md` (base) | blob `75bd93dec436` |")
w("")
w("**`BLOCK_MANIFEST.md` l.141 names three components for this block, and they do not come from")
w("one document:**")
w("")
w("| component | source | in the 25 Aug approval? |")
w("|---|---|---|")
for what, src in components:
    w("| %s | `%s` | %s |" % (what, src,
                              "**yes**" if src in approved_files else "**NO**"))
w("")
if unapproved:
    w("**§8.2 — the block proper, the largest of the three — is in `K2_AMENDMENT_LEDGER.md`, which")
    w("is not an approved artifact.** §AB and §AC are inside `SCHEMA_SET_FINAL.md` and are approved")
    w("content; the block that would carry them is not. **So the block is not already approvable on")
    w("the strength of anything in this repository.** It would need a fresh approval, exactly as the")
    w("two §6.2 diffs got one at R139 §1.1 — and §2 below is the reason to think hard before giving")
    w("it.")
w("")
w("---")
w("")
w("## 2. §8.2 ITEM 1 IS FALSE OF THE FILE IT WOULD DESCRIBE")
w("")
w("Item 1 is the first thing the block asserts:")
w("")
w("> **No registered sentence is deleted from this file.**")
w("")
w("**Derived from the two files, not from any approval's removal list** — because A24 superseded")
w("two further lines under a second approval, so a population taken from the first would miss them.")
w("Every non-blank line of `prereg-v30:PREREG.md` absent from the applied file, with retention")
w("credited only where a retention marker sits at the site:")
w("")
w("| v30 line | what it is | retained? |")
w("|---|---|---|")
# The seven rows are the output of `a31_item1_check.py`, which derives them from
# the two files. They are restated here rather than re-derived so this script
# stays a presenter; the check is the authority and is committed beside it.
w("| 445 | reference AUC | **RETAINED**, applied l.575, marked |")
w("| 450 | contamination class | **RETAINED**, applied l.583, marked |")
w("| 461 | §6.2 criterion 3 | **NOT RETAINED** |")
w("| 855 | §7.7 coverage row | **NOT RETAINED** |")
w("| 929 | `assert_audit_complete()` | **NOT RETAINED** |")
w("| 1022 | §10.1 criterion 3 | **RETAINED**, applied l.1688, marked |")
w("| 1030 | §10.2 criterion 2 | **NOT RETAINED** |")
w("")
w("**Seven superseded sentences: three retained with a marker, four not.**")
w("*(R140 §1.2 put it at two and four; that missed v30 l.1022, which A20b established was")
w("retained verbatim with a marker. The figure is three and four.)*")
w("")
w("**Landing §8.2 as drafted would put a false claim about the amendment into registered text —")
w("false in exactly the way the block exists to prevent.** The two clauses A24 applied are the")
w("pattern item 1 describes: both retain verbatim, both marked. Four earlier deletions do not.")
w("")
w("### The options, laid out. NOT chosen.")
w("")
w("1. **Land it with item 1 as approved, and disclose the discrepancy** — the block goes in")
w("   unchanged and a deviation records that item 1 is true of three of seven. A registered")
w("   sentence and a disclosure then disagree, which is the shape §0.2.1 line 77 calls a protocol")
w("   failure.")
w("2. **Retro-retain the four, so item 1 becomes true** — restore each deleted sentence at its site")
w("   in a marked, non-operative block, the way A24 did. This is the option that makes the")
w("   registered text and its description agree, and it is the largest edit.")
w("3. **Do not land the block.** The four citations at ll.1849, 1853, 1915, 1917 then cite a record")
w("   that will never exist and join A30's correction class; the two absences become disclosed")
w("   deviations. R140 A31's own fallback.")
w("")
w("---")
w("")
w("## 3. WHAT THE BLOCK WOULD RESOLVE, of A31's six")
w("")
w("| item | resolved by landing the block? |")
w("|---|---|")
w("| l.1849 cites *\"the amendments block records\"* | **yes** |")
w("| l.1853 cites *\"recorded in the v30a amendments block\"* | **yes** |")
w("| l.1915 cites *\"amendments block in terms\"* | **yes** |")
w("| l.1917 cites *\"recorded in the amendments block\"* | **yes** |")
w("| absence: no `## v30a amendments` block | **yes** — this is the block |")
w("| absence: no `**Amendment status:**` line | **no** — that is §8.1, a separate insert at line 6 |")
w("")
w("**Five of six.** §8.1's status line is a different hunk and is not assembled here.")
w("")
w("---")
w("")
w("## 4. THE ASSEMBLED BLOCK — presentation only")
w("")
w("Extracted verbatim: §8.2 from `K2_AMENDMENT_LEDGER.md` between its own `K2-BLOCK-BEGIN` and")
w("`K2-BLOCK-END` markers; §AB from `SCHEMA_SET_FINAL.md` ll.%d–%d; §AC from ll.%d–%d — the ranges"
  % (*ranges["§AB"], *ranges["§AC"]))
w("`BLOCK_MANIFEST.md`'s §A table gives. Nothing below is authored here.")
w("")
w("```markdown")
w(block)
w("")
w(ab)
w("")
w(ac)
w("```")
OUT.write_text("\n".join(b) + "\n", encoding="utf-8")
print()
print("wrote %s (%d lines) -- a PRESENTATION. Nothing applied." % (OUT, len(b)))
