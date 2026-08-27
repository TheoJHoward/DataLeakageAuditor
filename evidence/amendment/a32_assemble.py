"""A32 -- assemble ONE fresh approval diff, four independently approvable hunks.

APPLIES NOTHING. R141 §1.3: §1.1 and §1.2 authorise assembling and presenting a
fresh diff; they do not authorise applying it.

EXTRACTION AND DRAFTING ARE DIFFERENT ACTS AND ARE LABELLED AS SUCH (§1.2).
Every hunk below says which it is, names its source file and that file's sha256,
and -- where the provenance is weaker than SSF's -- says so in the hunk, because
approving newly drafted text is a different act from approving extracted text
and the author must see which one is being asked for.

  1. §AB              EXTRACTED from SCHEMA_SET_FINAL.md, at the approved hash
  2. §AC              EXTRACTED from SCHEMA_SET_FINAL.md, at the approved hash
  3. SC-12(w)'s limb  EXTRACTED from SCHEMA_SET_FINAL.md, at the approved hash
  4. §7.7's row       EXTRACTED from X5_FINAL_PREREG_DIFF.md -- NOT an approved
                      artifact, and the operative row's own provenance is a
                      recovery from a scratch file, recorded at O-11. Flagged.

PLACEMENT. §AB and §AC were anchored inside §8.2's block, which does not land.
They do NOT need a container: `SCHEMA_SET_FINAL.md` line 77 fixes the
application order as "SC-12 (revised) -> SC-13a -> SC-13b -> SC-13c -> §13c-P ->
§AB", so §AB's anchor is the §13c-P pointer -- which IS applied -- and
`BLOCK_MANIFEST.md` row 36 puts §AC immediately after §AB. A32-placement's first
branch fires and no new container text is invented.

    usage: a32_assemble.py <out.md>
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
SSF = REPO / "evidence/amendment/SCHEMA_SET_FINAL.md"
X5 = REPO / "evidence/amendment/X5_FINAL_PREREG_DIFF.md"
PREREG = REPO / "PREREG.md"
OUT = pathlib.Path(sys.argv[1])

APPROVED_SSF = "32358f6dfc7f96d2ac1e97cea9b6743dde674c78ac05cc114cc42e41ca33f2dc"


def text_of(p):
    return p.read_text(encoding="utf-8").replace("\r\n", "\n")


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


ssf_sha, x5_sha = sha(SSF), sha(X5)
print("=" * 78)
print("SOURCES")
print("=" * 78)
print("  SCHEMA_SET_FINAL.md    %s  %s" % (ssf_sha[:16],
      "== the approved hash" if ssf_sha == APPROVED_SSF else "** NOT the approved hash **"))
if ssf_sha != APPROVED_SSF:
    sys.exit("HALT: SSF is not at the approved hash; extraction from it would "
             "not be extraction from approved content.")
print("  X5_FINAL_PREREG_DIFF.md %s  NOT an approved artifact" % x5_sha[:16])

ssf = text_of(SSF).split("\n")
x5 = text_of(X5)
prereg = text_of(PREREG).split("\n")


HEADINGS = {"§AB": "### §AB", "§AC": "## §AC",
            "SC-12(w) limb": "**SC-12(w) — ENTRY CONDITION"}


def _true_extent(first, last, expect_in, label):
    """A block's real extent, from its own heading -- not from a declared range.

    `BLOCK_MANIFEST.md` is an assertion about where a block sits; the file is the
    fact. For §AB and §AC the assertion is eight lines out.
    """
    head = HEADINGS.get(label)
    if head is None:
        return first, last
    idx = [n for n, l in enumerate(ssf) if l.startswith(head)]
    if len(idx) != 1:
        sys.exit("HALT: %s -- heading occurs %d times, expected 1" % (label, len(idx)))
    i = idx[0]
    while i < len(ssf) and not ssf[i].startswith(">"):
        i += 1
    lo = i
    while i < len(ssf) and ssf[i].startswith(">"):
        i += 1
    if (lo + 1, i) != (first, last):
        print("      %-16s declared ll.%d-%d -> TRUE ll.%d-%d (offset %+d)"
              % (label, first, last, lo + 1, i, (lo + 1) - first))
    return lo + 1, i


def ssf_span(first, last, expect_in, label):
    """The APPLIED text inside a manifest range: its blockquote, and only that.

    `BLOCK_MANIFEST.md`'s §A ranges cover the whole block INCLUDING its
    apparatus -- §AB's range opens on a change note, not on the text that
    enters `PREREG.md`. SSF §0.2 draws the line: "only THE CLAUSE, SUPERSESSION
    MARKER text ... and the INSERTION TEXT blocks enter PREREG.md; REGISTERS /
    INSERTION POINT / DATA / ROWS / Instance record are apparatus." So the
    extraction narrows to the maximal contiguous blockquote inside the range,
    which is the applied form, and the apparatus stays where it belongs.
    """
    # SUPERSEDED AT R142/A33 -- KEPT ONLY SO THIS SCRIPT STILL RUNS.
    # `BLOCK_MANIFEST.md`'s declared ranges for §AB and §AC are the RIGHT LENGTH
    # and OFFSET BY +8: they cover each block's apparatus plus all but its last
    # eight lines. Extracting inside them cut §AC's disclosure 7 mid-sentence and
    # dropped its closing paragraph. `a33_apply.py` derives each block's extent
    # from its own heading instead, and THAT is what was applied. This presenter
    # is left pointing at the same derivation so the two cannot disagree.
    first, last = _true_extent(first, last, expect_in, label)
    block = ssf[first - 1:last]
    runs, cur = [], []
    for l in block:
        if l.startswith(">"):
            cur.append(l)
        elif cur:
            runs.append(cur)
            cur = []
    if cur:
        runs.append(cur)
    hit = [r for r in runs if expect_in in "\n".join(r)]
    if len(hit) != 1:
        sys.exit("HALT: %s -- %d of the %d blockquote runs inside SSF ll.%d-%d "
                 "carry %r; expected exactly 1."
                 % (label, len(hit), len(runs), first, last, expect_in[:40]))
    out = hit[0]
    lo = block.index(out[0])
    hi = lo + len(out) - 1
    joined = "\n".join(out).strip("\n")
    print("      %-18s SSF ll.%d-%d -> blockquote ll.%d-%d (%d lines)"
          % (label, first, last, first + lo, first + hi, len(out)))
    return joined


print()
print("EXTRACTION -- applied text only, apparatus excluded (SSF §0.2)")
ab = ssf_span(1632, 1679, "RECORDED DEFECT", "§AB")
ac = ssf_span(1687, 1737, "WHAT THIS AMENDMENT DISCLOSES", "§AC")
limb = ssf_span(1145, 1181, "(w) ENTRY CONDITION", "SC-12(w) limb")

m = re.search(r"### 2\.21 .*?```markdown\n(.*?)\n```", x5, re.S)
if not m:
    sys.exit("HALT: X5 §2.21's operative-text block not found")
row_marker = m.group(1).strip("\n")

m2 = re.search(r"\(…/scratchpad/applied/PREREG\.md line \d+\):\s*(`\| \*\*Detector-case coverage\*\*.*?\|`)",
               x5, re.S)
if not m2:
    sys.exit("HALT: O-11's operative row not found in X5")
row_operative = m2.group(1).strip().strip("`")

print()
print("  extracted: §AB %d lines · §AC %d lines · SC-12(w) limb %d lines"
      % (len(ab.split("\n")), len(ac.split("\n")), len(limb.split("\n"))))
print("  extracted: §7.7 retention marker %d lines; operative row %d chars"
      % (len(row_marker.split("\n")), len(row_operative)))


def anchor(text, label):
    hits = [i for i, l in enumerate(prereg, 1) if l == text]
    if len(hits) != 1:
        sys.exit("HALT: %s -- anchor matches %d lines, expected 1" % (label, len(hits)))
    return hits[0]


# §13c-P's anchor is its BLOCK, not one of its lines. The pointer paragraph sits
# inside a fenced code block under the SC-13c-2 marker, so anchoring on the
# paragraph text would place §AB INSIDE the fence. Located from the marker, and
# the block's end found by its closing fence -- never by counting lines.
_m = anchor("<!-- v30a SC-13c-2 — INSERT_AFTER -->", "§13c-P's marker")
_fences = [i for i in range(_m, min(_m + 20, len(prereg) + 1))
           if prereg[i - 1].strip() == "```"]
if len(_fences) < 2:
    sys.exit("HALT: §13c-P -- expected an opening and a closing fence within 20 "
             "lines of its marker; found %d" % len(_fences))
A_13CP = _fences[1]
print()
print("=" * 78)
print("ANCHORS, located never offset")
print("=" * 78)
print("  §13c-P (for §AB, then §AC) : applied l.%d" % A_13CP)
tbl = [i for i, l in enumerate(prereg, 1) if l == "| Level | States |"]
print("  §7.7's table header        : applied l.%s" % tbl)
sc12 = [i for i, l in enumerate(prereg, 1) if "**“Waived”, defined — v30a [SC-12]**" in l
        or '**"Waived", defined — v30a [SC-12]**' in l]
print("  SC-12's clause heading     : applied l.%s" % sc12)

b = []
w = b.append
w("# A32 — ONE FRESH APPROVAL DIFF, FOUR HUNKS. **NOT APPLIED.**")
w("")
w("**Nothing here is applied.** `PREREG.md` is unchanged at `%s…`." % sha(PREREG)[:16])
w("R141 §1.3: §1.1 and §1.2 authorise **assembling and presenting**; they do not authorise applying.")
w("")
w("**Each hunk is independently approvable — take some and refuse others.**")
w("")
w("| # | hunk | act | source | source sha256 |")
w("|---|---|---|---|---|")
w("| 1 | §AB — the 816/830 duplicated-authority record | **EXTRACTED** | `SCHEMA_SET_FINAL.md` ll.1632–1679 | `%s…` **= the approved hash** |" % ssf_sha[:16])
w("| 2 | §AC — the seven `PREREG.md` disclosures | **EXTRACTED** | `SCHEMA_SET_FINAL.md` ll.1687–1737 | `%s…` **= the approved hash** |" % ssf_sha[:16])
w("| 3 | SC-12(w)'s limb | **EXTRACTED** | `SCHEMA_SET_FINAL.md` ll.1145–1181 | `%s…` **= the approved hash** |" % ssf_sha[:16])
w("| 4 | §7.7's row — operative + retention | **EXTRACTED, weaker provenance** | `X5_FINAL_PREREG_DIFF.md` | `%s…` **not an approved artifact** |" % x5_sha[:16])
w("")
w("---")
w("")
w("## Placement — §AB and §AC need no container")
w("")
w("They were anchored inside §8.2's block, which does not land. **They do not need a new one.**")
w("`SCHEMA_SET_FINAL.md` l.77 fixes the application order:")
w("")
w("> **SC-12 (revised) → SC-13a → SC-13b → SC-13c → §13c-P → §AB**")
w("")
w("§13c-P is the §7.2.1 line-816 pointer and **is applied**, at `PREREG.md` **l.%d**. §AB follows it;" % A_13CP)
w("`BLOCK_MANIFEST.md` row 36 puts §AC immediately after §AB. **A32-placement's first branch fires**")
w("and no container text is invented — which matters, because §8.2's item 1 is exactly the kind of")
w("claim a container must not reintroduce.")
w("")
w("---")
w("")
w("## Hunk 1 — §AB. EXTRACTED, verbatim, from approved content")
w("")
w("**Anchor:** insert after `PREREG.md` l.%d (the §13c-P pointer paragraph), match count 1." % A_13CP)
w("")
w("```markdown")
w(ab)
w("```")
w("")
w("---")
w("")
w("## Hunk 2 — §AC. EXTRACTED, verbatim, from approved content")
w("")
w("**Anchor:** immediately after hunk 1's §AB. **Seven items, and they are distinct from the")
w("declaration's §D.6 five** — mapped at R136 and re-confirmed: no overlap, the one adjacency being")
w("§AC-5 against `D-ARCHIVE`, which are different objects with different consequences.")
w("")
w("```markdown")
w(ac)
w("```")
w("")
w("---")
w("")
w("## Hunk 3 — SC-12(w)'s limb. EXTRACTED, verbatim, from approved content")
w("")
w("**Why it is needed:** two operative clauses already cite it — SC-12p's pointer (*\"SC-12(w)")
w("registers the condition under which a detector-case may be reported in this state\"*) and §8.3's")
w("assertion (*\"whose (w1) prohibits the state outright\"*). Both cite a limb that is not in the file.")
w("")
w("**Anchor:** after SC-12's clause at `PREREG.md` l.%s, before the SC-13b marker." % (sc12 or "?"))
w("")
w("```markdown")
w(limb)
w("```")
w("")
w("---")
w("")
w("## Hunk 4 — §7.7's row. EXTRACTED, but read the provenance before approving")
w("")
w("**Why it is needed:** SC-6b is operative and ranges over *\"every detector-case coverage state")
w("**that row** carries\"*. The row is deleted, so the clause has an **empty domain** — closer to two")
w("registered texts in conflict than to a citation defect (R141 §1.2).")
w("")
w("**⚠️ PROVENANCE, stated because it is weaker than the other three.** `X5_FINAL_PREREG_DIFF.md` is")
w("**not** one of the three approved artifacts. Worse, its own finding **O-11** records that the")
w("operative row *\"is nowhere quoted verbatim in `SCHEMA_SET_FINAL.md`\"* and that the form below was")
w("**recovered from a scratch applied file** — and O-11 says in terms: *\"the author should not have")
w("to reconstruct operative registered text from a scratch artifact in order to sign it.\"* **That is")
w("what this hunk asks. It is flagged rather than smoothed.**")
w("")
w("**4a — the operative row**, into §7.7's table, which currently has a header, a separator and no")
w("body row at all:")
w("")
w("```markdown")
w(row_operative)
w("```")
w("")
w("**4b — the retention marker**, after the table, so the deleted v30 row is retained the way §8.2")
w("item 1 promises and the way A24's two clauses already do:")
w("")
w("```markdown")
w(row_marker)
w("```")
w("")
w("**A third option not taken here, flagged for you.** The `| **Strategy diagnostic** |` row sits")
w("orphaned at l.%s, 37 lines below its header, where markdown renders it as a paragraph. Landing 4a" % (tbl[0] + 38 if tbl else "?"))
w("makes the table well-formed with **one** row and leaves that orphan where it is; R141 §A15")
w("disposes it as a disclosure. **Moving it back into the table would repair the structure instead**")
w("— that is a third hunk nobody has asked for, so it is named, not drafted.")
OUT.write_text("\n".join(b) + "\n", encoding="utf-8")
print()
print("wrote %s (%d lines) -- NOT APPLIED." % (OUT, len(b)))
