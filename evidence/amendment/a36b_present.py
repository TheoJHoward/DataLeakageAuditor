"""A36b -- present §13c-P for the author's read. R146 §1.3. HALTS.

DECISION A36b, first branch: the pointer text IS in `SCHEMA_SET_FINAL.md` at the
approved hash, so it is extracted verbatim and presented in full. Nothing is
applied; R146 §1.3 requires the author read it first.

EXTENT FROM THE STRUCTURE'S OWN DELIMITERS. `BLOCK_MANIFEST.md` row 32 declares
ll.1604-1608 and the fence actually runs 1612-1616 -- the same eight-line offset
that truncated §AB and §AC. The fence is located from §13c-P's own heading and
its `INSERT AFTER` apparatus, and the declared range is reported as a
cross-check, never used as a source.

THE THING THE AUTHOR MUST SEE. The pointer cites *"the v30a amendments block"* --
the container that does not exist and never will, and the exact phrase A34
removed from all four operative sites one commit ago. Applying this text verbatim
would put that false citation back into registered prose. This script states the
consequence and the options and CHOOSES NONE: which way it goes is the author's,
and presenting a recommendation as if it were an extraction is how a
presentation becomes an argument.

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
DATE = "27 August 2026"

sha = hashlib.sha256(SSF.read_bytes()).hexdigest()
if sha != APPROVED:
    sys.exit("HALT: SSF is %s, not the approved %s" % (sha[:16], APPROVED[:16]))
print("SSF verified at the approved hash: %s" % sha[:16])

ssf = SSF.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")
pre = PREREG.read_text(encoding="utf-8").split("\n")

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
    sys.exit("HALT: expected a fenced specimen after INSERT AFTER, found %d fence(s)"
             % len(fences))
lo, hi = fences[0] + 1, fences[1]
body = [l for l in ssf[lo:hi] if l.strip()]
if len(body) != 1:
    sys.exit("HALT: the pointer is %d non-blank line(s); expected exactly 1" % len(body))
pointer = body[0]
print("§13c-P heading SSF l.%d | fence ll.%d-%d | declared ll.%d-%d %s"
      % (i + 1, fences[0] + 1, fences[1] + 1, DECLARED[0], DECLARED[1],
         "MATCH" if (fences[0] + 1, fences[1] + 1) == DECLARED
         else "** OFFSET BY %+d **" % ((fences[0] + 1) - DECLARED[0])))

spec = [n for n, l in enumerate(pre, 1) if l == pointer]
print("byte-identical copies already in PREREG.md: %d %s"
      % (len(spec), spec if spec else ""))

cites = "amendments block" in pointer
print("cites the non-existent container: %s" % cites)

anchor_line = next((n for n, l in enumerate(pre, 1)
                    if l.startswith("**A combination that is `not_applicable`")), None)

L = []
w = L.append
w("# A36b — §13c-P, THE LINE-816 POINTER. **NOT APPLIED.** ⛔ HALTS FOR YOUR READ.")
w("")
w("**%s.** R146 §1.3: *the pointer is extracted and presented if it is in SSF at the approved "
  "hash; the author reads it before it lands.* **It is there. Nothing is applied.**" % DATE)
w("")
w("`SCHEMA_SET_FINAL.md` verified at `%s…` — **the approved hash** — before a line was read out "
  "of it." % sha[:16])
w("")
w("---")
w("")
w("## The text, in full")
w("")
w("**Extracted verbatim from SSF ll.%d–%d**, the fence under §13c-P's `INSERT AFTER` apparatus "
  "(heading at SSF l.%d)." % (fences[0] + 1, fences[1] + 1, i + 1))
w("")
w("```")
w(pointer)
w("```")
w("")
w("**Extent derived from the fence's own delimiters, not from a declared range.** "
  "`BLOCK_MANIFEST.md` row 32 declares ll.%d–%d — **eight lines early**, the same offset that "
  "truncated §AB and §AC. Had this been extracted inside the declared range it would have come "
  "out empty." % DECLARED)
w("")
w("## Where it would go")
w("")
w("After `PREREG.md` line %s — the registered line-816 suppression clause — and before line 818, "
  "one paragraph with a blank line each side. **A byte-identical copy is already in the file at "
  "l.%d, inside the fenced `INSERT AFTER` specimen** that has sat unapplied since the amendment "
  "was drafted: §13c-P is the only one of 23 v30a markers still carrying its apparatus."
  % (anchor_line or "816", spec[0] if spec else 0))
w("")
w("---")
w("")
w("## ⚠️ WHAT THIS COSTS, AND IT IS THE REASON THIS HALTS")
w("")
w("**The pointer's last sentence cites “the v30a amendments block.”** That container does not "
  "exist and never will — §8.2 was ruled never to land. **It is the exact phrase A34 removed from "
  "all four operative sites one commit ago.**")
w("")
w("> …is recorded in the v30a **amendments block** and is not changed by the exception.")
w("")
w("**Applying this text verbatim puts that false citation back into registered prose.** The three "
  "ways out are set down here and **none is chosen** — which way it goes is yours:")
w("")
w("| | what it costs |")
w("|---|---|")
w("| **apply verbatim** | faithful to approved content; **plants a citation to a container that does not exist**, which then needs its own A34-class correction |")
w("| **apply with the citation corrected** to A34's form — *“the v30a recorded-defect block in §7.2.1”* | leaves the file consistent; **but it is no longer verbatim extraction from approved content**, so it needs its own approval, exactly as the sixteen lines did |")
w("| **do not apply** | nothing false is added; **§AB's assertion that “a pointer to the exception is inserted at line 816's own site” stays false**, and joins HELD as a disclosed false describer |")
w("")
w("**No recommendation is offered.** R146 §1.3 asks for an extraction and a read; a presentation "
  "that arrives with its own preferred answer has stopped being an extraction.")
w("")
w("---")
w("")
w("## What was verified")
w("")
w("| | |")
w("|---|---|")
w("| SSF at the approved hash **before extraction** | `%s…` |" % sha[:16])
w("| extent from **the fence's own delimiters** | ll.%d–%d; the declared range is **%+d off** and is used only as a cross-check |"
  % (fences[0] + 1, fences[1] + 1, (fences[0] + 1) - DECLARED[0]))
w("| the paragraph is **exactly one line** | asserted, not assumed |")
w("| **byte-identical** to the specimen already in `PREREG.md` | at l.%d — so applying it changes no wording, only its status from apparatus to registered text |"
  % (spec[0] if spec else 0))
w("| it **cites the non-existent container** | `%s` |" % cites)
w("")
w("**Nothing is applied. `PREREG.md` is unchanged at `%s…`.**"
  % hashlib.sha256(PREREG.read_bytes()).hexdigest()[:16])

OUT.write_text("\n".join(L) + "\n", encoding="utf-8")
b = OUT.read_bytes()
print("written: %s (%d lines, %d CRLF / %d LF, sha %s)"
      % (OUT.name, b.count(b"\n"), b.count(b"\r\n"), b.count(b"\n"),
         hashlib.sha256(b).hexdigest()[:16]))
