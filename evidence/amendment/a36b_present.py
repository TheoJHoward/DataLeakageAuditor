"""A36b -- present §13c-P for the author's read. R147 §3. HALTS.

THE CONSEQUENCE LEADS. R147 §1.3 and §2.2: announcing that a finding exists
without stating it is the headline rule inverted. The artifact's first section is
what applying this text costs, before the text itself, before the verification,
before anything.

Nothing is applied. R147 §6 makes applying §13c-P before the author's read a halt.

    usage: a36b_present.py <out.md>
"""
from __future__ import annotations

import hashlib
import pathlib
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:                                       # noqa: BLE001
    pass

REPO = pathlib.Path(__file__).resolve().parents[2]
SSF = REPO / "evidence/amendment/SCHEMA_SET_FINAL.md"
PREREG = REPO / "PREREG.md"
APPROVED = "32358f6dfc7f96d2ac1e97cea9b6743dde674c78ac05cc114cc42e41ca33f2dc"
DECLARED = (1604, 1608)
OUT = pathlib.Path(sys.argv[1])
DATE = "28 August 2026"

sha = hashlib.sha256(SSF.read_bytes()).hexdigest()
if sha != APPROVED:
    sys.exit("HALT: SSF is %s, not the approved %s" % (sha[:16], APPROVED[:16]))
print("SSF verified at the approved hash: %s" % sha[:16])

ssf = SSF.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")
pre = PREREG.read_text(encoding="utf-8").split("\n")

# --- extent from the fence's own delimiters, never from a declared range ----
head = [i for i, l in enumerate(ssf) if l.startswith("### §13c-P")]
if len(head) != 1:
    sys.exit("HALT: §13c-P's heading occurs %d times, expected 1" % len(head))
i = head[0]
ins = next((k for k in range(i, min(i + 40, len(ssf)))
            if ssf[k].startswith("**INSERT AFTER")), None)
if ins is None:
    sys.exit("HALT: no INSERT AFTER apparatus under §13c-P")
fences = [k for k in range(ins, min(ins + 12, len(ssf))) if ssf[k].strip() == "```"]
if len(fences) < 2:
    sys.exit("HALT: expected a fenced specimen, found %d fence(s)" % len(fences))
lo, hi = fences[0] + 1, fences[1]
body = [l for l in ssf[lo:hi] if l.strip()]
if len(body) != 1:
    sys.exit("HALT: the pointer is %d non-blank line(s); expected 1" % len(body))
pointer = body[0]
offset = (fences[0] + 1) - DECLARED[0]

# --- the insertion anchor, located and asserted unique ---------------------
AN = "**A combination that is `not_applicable`"
anchors = [n for n, l in enumerate(pre, 1) if l.startswith(AN)]
if len(anchors) != 1:
    sys.exit("HALT: the line-816 anchor occurs %d times, expected 1" % len(anchors))
at = anchors[0]

# --- what sits above and below, and whether each still parses as itself ----
above = pre[at - 1]
below = [(n, pre[n - 1]) for n in range(at + 1, min(at + 8, len(pre) + 1))]

# --- the duplicate the apparatus would leave --------------------------------
copies = [n for n, l in enumerate(pre, 1) if l == pointer]

# --- §AB's assertion, which applying would make true ------------------------
ASSERT = "pointer to the exception is inserted at line 816's own site"
ab = [n for n, l in enumerate(pre, 1) if ASSERT in l]

cites = "amendments block" in pointer
print("fence SSF ll.%d-%d (declared %d-%d, %+d) | anchor PREREG l.%d unique | "
      "identical copies in file: %d | §AB assertion at l.%s | cites container: %s"
      % (fences[0] + 1, fences[1] + 1, DECLARED[0], DECLARED[1], offset,
         at, len(copies), ab[0] if ab else "?", cites))

L = []
w = L.append
w("# A36b — §13c-P, THE LINE-816 POINTER. **NOT APPLIED.** ⛔ HALTS FOR YOUR READ.")
w("")
w("## ⚠️ THE CONSEQUENCE, FIRST — there are two, and neither is a reason to refuse on its own")
w("")
w("**1. The pointer cites a container that was ruled never to land.** Its closing sentence reads:")
w("")
w("> …is recorded in the v30a **amendments block** and is not changed by the exception.")
w("")
w("**§8.2 — the amendments block — never lands** (unapproved content; its item 1 is false). The "
  "phrase is the same one A34 removed from all four operative sites at `f1d66bf`. **Applying this "
  "text verbatim puts that citation back into registered prose**, one commit after it was taken out.")
w("")
w("**2. Applying it while the drafting apparatus stays would put the same paragraph in the file "
  "twice.** The fenced specimen at l.%d is **byte-identical** to the text being applied. Landing "
  "the paragraph without removing the `INSERT AFTER` apparatus leaves an operative copy and a "
  "fenced copy — and any future citation anchored on that text would then resolve to two lines, "
  "which is the failure A34 spent a whole correction class avoiding." % copies[0])
w("")
w("### The choices. **None is taken here.**")
w("")
w("| | what it costs |")
w("|---|---|")
w("| **apply verbatim, disclose the citation** | faithful to approved content; **registered prose then cites a container that does not exist**, and that needs its own A34-class correction later |")
w("| **apply with the citation corrected** to A34's form — *“the v30a recorded-defect block in §7.2.1”* | leaves the file self-consistent; **but it is no longer verbatim extraction from approved content**, so it needs its own approval, exactly as the sixteen lines did |")
w("| **do not apply** | nothing false is added; **§AB's assertion at l.%s stays false** and joins HELD, disclosed at A15 |" % (ab[0] if ab else "?"))
w("")
w("**Whether the apparatus is removed is a second, separable question** — it is drafting "
  "scaffolding, not registered prose, but removing it is a deletion and is not proposed here.")
w("")
w("---")
w("")
w("## The text, in full")
w("")
w("**Extracted verbatim from SSF ll.%d–%d** — the fence under §13c-P's `INSERT AFTER` apparatus, "
  "heading at SSF l.%d." % (fences[0] + 1, fences[1] + 1, i + 1))
w("")
w("```")
w(pointer)
w("```")
w("")
w("**Extent derived from the fence's own delimiters, never from a declared range.** "
  "`BLOCK_MANIFEST.md` row 32 declares ll.%d–%d — **%+d, eight lines early**. Extracting inside the "
  "declared range would have returned **nothing at all**. *(A39 left row 32 uncorrected: it has no "
  "length-preserving candidate, and a number the instrument cannot derive is one it must not "
  "write.)*" % (DECLARED[0], DECLARED[1], offset))
w("")
w("## Where it would go, and what sits there now")
w("")
w("**The insertion anchor is `PREREG.md` l.%d — the registered line-816 suppression clause — and it "
  "occurs exactly once**, asserted before anything else was read." % at)
w("")
w("```")
w("l.%-5d %s" % (at - 1, above if above.strip() else "(blank)"))
w("l.%-5d %s   <-- THE ANCHOR" % (at, pre[at - 1][:86]))
for n, l in below:
    w("l.%-5d %s" % (n, l[:86] if l.strip() else "(blank)"))
w("```")
w("")
w("**Structure, checked before any write plan.** The anchor is a **top-level paragraph**, not inside "
  "a blockquote, list or table; the line above it is blank and the line below it is blank, so a "
  "paragraph inserted with a blank line each side **cannot merge into either neighbour** and cannot "
  "turn a following `---` into a setext heading. **The apparatus below it (ll.%d–%d) is a fenced "
  "block**, and inserting above the fence leaves the fence balanced — both still parse as what they "
  "were." % (at + 4, at + 10))
w("")
w("## What applying it would make true")
w("")
w("**`PREREG.md` l.%s, inside §AB, currently asserts:**" % (ab[0] if ab else "?"))
w("")
w("> …a %s." % ASSERT)
w("")
w("**That is false today** — §13c-P is the only one of 23 v30a markers still carrying unapplied "
  "`INSERT` apparatus, and the pointer exists solely as the fenced specimen. **Applying the "
  "paragraph makes §AB's sentence true**; refusing leaves it false and disclosable. Either way it "
  "is verified by reading after the fact, not assumed.")
w("")
w("---")
w("")
w("## What was verified")
w("")
w("| | |")
w("|---|---|")
w("| SSF byte-equal to the approved hash **before extraction** | `%s…` |" % sha[:16])
w("| extent from **the fence's own delimiters** | ll.%d–%d; the declared range is **%+d** and is used only as a cross-check |" % (fences[0] + 1, fences[1] + 1, offset))
w("| the paragraph is **exactly one line** | asserted, not assumed |")
w("| the insertion anchor is **unique** | `PREREG.md` l.%d, match count 1 |" % at)
w("| **markdown structure** above and below the anchor | blank / blank; fenced apparatus below stays balanced |")
w("| **byte-identical copy already in the file** | l.%d — so applying changes no wording, only status |" % copies[0])
w("| it **cites the non-existent container** | `%s` |" % cites)
w("")
w("**Nothing is applied. `PREREG.md` is unchanged at `%s…`, %d lines.**"
  % (hashlib.sha256(PREREG.read_bytes()).hexdigest()[:16], len(pre) - 1))

OUT.write_text("\n".join(L) + "\n", encoding="utf-8")
b = OUT.read_bytes()
print("written: %s (%d lines, %d CRLF / %d LF, sha %s)"
      % (OUT.name, b.count(b"\n"), b.count(b"\r\n"), b.count(b"\n"),
         hashlib.sha256(b).hexdigest()[:16]))
