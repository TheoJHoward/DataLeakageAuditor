"""A33b -- generate the superseding presentation. R143 §3.

THE SIXTEEN LINES ARE READ OUT OF SSF, NEVER RETYPED. They are the object of the
approval this document asks for, and a presentation that spells its own subject
can misspell it -- the same class as D2.1, one layer up. SSF's hash is verified
equal to the approved hash before a line is read.

`A32_PROPOSED_DIFF.md` IS NOT TOUCHED. It is the frozen record of what the author
read on the day, and rewriting it would destroy the only evidence of what was
actually approved -- which is precisely the gap this document exists to close.

    usage: a33b_present.py <out.md>
"""
from __future__ import annotations

import hashlib
import pathlib
import subprocess
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:                                       # noqa: BLE001
    pass

REPO = pathlib.Path(__file__).resolve().parents[2]
SSF = REPO / "evidence/amendment/SCHEMA_SET_FINAL.md"
PREREG = REPO / "PREREG.md"
PRESENTED = REPO / "evidence/amendment/A32_PROPOSED_DIFF.md"
APPROVED_SSF = "32358f6dfc7f96d2ac1e97cea9b6743dde674c78ac05cc114cc42e41ca33f2dc"
OUT = pathlib.Path(sys.argv[1])
DATE = "27 August 2026"

ssf_sha = hashlib.sha256(SSF.read_bytes()).hexdigest()
if ssf_sha != APPROVED_SSF:
    sys.exit("HALT: SSF is %s, not the approved %s" % (ssf_sha[:16], APPROVED_SSF[:16]))

dirty = subprocess.run(["git", "status", "--porcelain", "--", str(PRESENTED)],
                       cwd=REPO, capture_output=True, text=True).stdout.strip()
if dirty:
    sys.exit("HALT: A32_PROPOSED_DIFF.md is modified (%r). The approved bytes are "
             "the committed ones." % dirty)

ssf = SSF.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")
prereg = PREREG.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")
pres = PRESENTED.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")
prereg_sha = hashlib.sha256(PREREG.read_bytes()).hexdigest()


def blockquote(heading, label):
    """True extent, from the block's own delimiters -- never a declared range."""
    idx = [n for n, l in enumerate(ssf) if l.startswith(heading)]
    if len(idx) != 1:
        sys.exit("HALT: %s -- heading occurs %d times, expected 1" % (label, len(idx)))
    i = idx[0]
    while i < len(ssf) and not ssf[i].startswith(">"):
        i += 1
    lo = i
    while i < len(ssf) and ssf[i].startswith(">"):
        i += 1
    return lo + 1, i, ssf[lo:i]


def presented_run(first_line, label):
    hits = [i for i, l in enumerate(pres) if l == first_line]
    if len(hits) != 1:
        sys.exit("HALT: %s -- opening line occurs %d times in the presentation"
                 % (label, len(hits)))
    i = hits[0]
    j = i
    while j < len(pres) and pres[j].startswith(">"):
        j += 1
    return pres[i:j]


BLOCKS = (("§AB", "### §AB", (1632, 1679)),
          ("§AC", "## §AC", (1687, 1737)),
          ("SC-12(w)'s limb", "**SC-12(w) — ENTRY CONDITION", (1145, 1181)))

rows, extras, checked = [], [], []
for label, heading, declared in BLOCKS:
    first, last, body = blockquote(heading, label)
    p = presented_run(body[0], label)
    # PREFIX EQUALITY, line by line. Substring containment would also pass if a
    # line had been inserted in the middle -- a different and worse fact.
    if len(p) > len(body) or any(p[k] != body[k] for k in range(len(p))):
        sys.exit("HALT: %s -- the applied block is not the presented block plus a "
                 "suffix. This document's central claim is false." % label)
    tail = body[len(p):]
    at = next(i + 1 for i, l in enumerate(prereg) if l == body[0])
    rows.append((label, len(p), len(body), first, last, declared, at, len(tail)))
    if tail:
        extras.append((label, declared[1] + 1, last, tail))
    checked.append(label)

total_extra = sum(len(t[3]) for t in extras)
print("SSF verified at the approved hash; %d block(s) compared; %d extra line(s)"
      % (len(rows), total_extra))

L = []
w = L.append
w("# A33b — THE SIXTEEN LINES THAT WERE APPLIED BUT NEVER PRESENTED")
w("")
w("**%s. Supersedes `A32_PROPOSED_DIFF.md` as a presentation of hunks 1–3 — it does not replace it "
  "as a record.** That document is the frozen account of what was read on the day it was approved "
  "and **is not touched**; rewriting it would destroy the only evidence of what was actually "
  "approved, which is the very gap this document exists to close." % DATE)
w("")
w("**Nothing here is applied.** `PREREG.md` already carries this text, at `%s…`, %d lines. "
  "**On approval the applied state stands as approved and nothing is re-applied.** Refused, the "
  "sixteen lines come back out." % (prereg_sha[:16], len(prereg) - 1))
w("")
w("---")
w("")
w("## What went wrong")
w("")
w("`BLOCK_MANIFEST.md`'s declared ranges **end eight lines before each blockquote actually ends**. "
  "A32 extracted inside them, so the presentation carried §AB and §AC each eight lines short. The "
  "ranges are the **right length** and **start eight lines early** — they cover each block's "
  "apparatus plus all but its last eight lines, which is why nothing looked obviously wrong.")
w("")
w("| block | presented | applied | declared range | true extent | difference |")
w("|---|---|---|---|---|---|")
for label, np_, nb, first, last, declared, at, ntail in rows:
    diff = ("**+%d appended**" % ntail) if ntail else "identical"
    w("| %s | %d lines | **%d lines** | ll.%d–%d | **ll.%d–%d** | %s |"
      % (label, np_, nb, declared[0], declared[1], first, last, diff))
w("")
w("**SC-12(w)'s limb is identical** because A32 happened to use ll.1145–1181 for it rather than "
  "`BLOCK_MANIFEST.md`'s own entry 23, which declares ll.1137–1173 and is **also eight early**. "
  "The limb was applied correctly by luck, not by check.")
w("")
w("## The claim, proved mechanically rather than asserted")
w("")
w("> **The applied text is the presented text plus exactly %d lines, appended at the end of two "
  "blocks. No presented line was removed, reordered or altered.**" % total_extra)
w("")
w("`a33b_divergence.py` establishes this by **prefix equality, line by line** — deliberately not by "
  "substring containment, which would also pass if a line had been inserted in the *middle* of a "
  "block. That is a different and worse fact, so the test is written to be able to fail on it. "
  "This generator re-runs the same comparison and **halts rather than emitting** if it does not hold.")
w("")
w("---")
w("")
w("## The %d lines, in full" % total_extra)
w("")
w("**Read out of `SCHEMA_SET_FINAL.md` at `%s…` — the approved hash, verified before a line was "
  "read.** Not retyped: a presentation that spells its own subject can misspell it." % ssf_sha[:16])
w("")
for label, lo, hi, tail in extras:
    w("### %s — SSF ll.%d–%d, %d lines" % (label, lo, hi, len(tail)))
    w("")
    w("```")
    L.extend(tail)
    w("```")
    w("")
w("## Why these lines are not a formality")
w("")
w("**§AB's eight carry the block's central holding.** Without them §AB records the conflict and "
  "never says where it lies:")
w("")
w("> **The operative conflict is registered-text-internal — line 816 against line 830.**")
w("")
w("**§AC's eight carry disclosure 7's conclusion and the block's closing paragraph.** Without them "
  "the block ends mid-sentence inside item 7, and the sentence that says why the disclosures exist "
  "is absent:")
w("")
w("> **These seven are disclosed because the record should not have to be reverse-engineered to "
  "find them.**")
w("")
w("---")
w("")
w("## What was verified")
w("")
w("| | |")
w("|---|---|")
w("| SSF at the approved hash **before extraction** | `%s…` — extraction from unapproved bytes is "
  "not extraction from approved content |" % ssf_sha[:16])
w("| extents derived from **the blockquotes' own delimiters** | a declared range is an assertion; "
  "the block's extent is a fact about the file |")
w("| `A32_PROPOSED_DIFF.md` **committed and unmodified** | the approved bytes are the committed "
  "ones; a presentation edited after approval is not what was approved |")
w("| applied text = presented text **+ suffix only** | prefix equality line by line, not substring "
  "containment |")
w("| **no other applied block is truncated** | `a33d_block_completeness.py`: 41 manifest rows, "
  "**0 truncated**, 24 complete — including SC-13a (59 lines), SC-13b (68) and SC-13c (101), whose "
  "declared ranges are also eight early |")
w("")
w("**The offset is wider than two blocks.** `a33c_manifest_offset.py` finds **seven** decidable §A "
  "rows eight lines early — 23, 24, 26, 28, 31, 33, 36 — against twenty-one correct. Rows 34 and "
  "35, annotated *“moved here R53/Y1”*, are correct because they were re-derived after the shift. "
  "**Only §AB and §AC were ever extracted inside a stale range**; the completeness sweep above is "
  "what establishes that, rather than assumption.")
w("")
w("---")
w("")
w("## What approval means")
w("")
w("**Approve** — the applied state stands as approved. Nothing is re-applied, no file changes, and "
  "A34 unblocks.")
w("")
w("**Refuse** — the %d lines are removed from `PREREG.md`, returning §AB and §AC to the extents "
  "that were presented. The blocks then end mid-sentence, which is why this document recommends "
  "nothing and simply shows what is at stake." % total_extra)

OUT.write_text("\n".join(L) + "\n", encoding="utf-8")
b = OUT.read_bytes()
print("written: %s  (%d lines, %d CRLF / %d LF, sha256 %s)"
      % (OUT.name, len(b.decode("utf-8").split("\n")) - 1,
         b.count(b"\r\n"), b.count(b"\n"), hashlib.sha256(b).hexdigest()[:16]))
bad = sorted({c for c in b if c < 32 and c not in (9, 10, 13)})
print("control chars beyond tab/LF/CR: %s" % (bad or "none"))
after = hashlib.sha256(PREREG.read_bytes()).hexdigest()
print("PREREG.md unchanged: %s" % (after == prereg_sha))
