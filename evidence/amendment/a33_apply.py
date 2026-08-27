"""A33 -- apply hunks 1-3 of A32's diff. R142 §1.1 approves them by name.

THIS ONE WRITES. Hunk 4 is NOT here: R142 §1.2 rules it does not land, and §6
makes applying it in any form a halt.

EXTRACTED FROM SSF, NOT FROM `A32_PROPOSED_DIFF.md`. That document is a
PRESENTATION of this text (§2.5), and applying from a presentation puts a second
copy in the chain so the two can drift. SSF's hash is verified equal to the
approved hash before a single line is read out of it -- if the source is not the
approved bytes, extraction from it is not extraction from approved content.

APPLIED BOTTOM-TO-TOP. SC-12(w)'s limb goes in around l.1818 and §AB/§AC around
l.1346, so the limb goes first: applying the earlier insertion first would shift
the later anchor, which is how an applier writes correct text into the wrong
place.

NO CONTAINER IS INVENTED. §AB and §AC open with self-describing headline
sentences -- "RECORDED DEFECT, NOT RESOLVED BY THIS AMENDMENT" and "WHAT THIS
AMENDMENT DISCLOSES" -- so they need no wrapper, and §8.2's item 1 is exactly
the kind of claim a wrapper would have reintroduced.

Structure is checked BEFORE the write; write-once guarded on a distinctive line
of each hunk.

    usage: a33_apply.py
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
APPROVED_SSF = "32358f6dfc7f96d2ac1e97cea9b6743dde674c78ac05cc114cc42e41ca33f2dc"


def text_of(p):
    return p.read_text(encoding="utf-8").replace("\r\n", "\n")


ssf_sha = hashlib.sha256(SSF.read_bytes()).hexdigest()
if ssf_sha != APPROVED_SSF:
    sys.exit("HALT: SSF is %s, not the approved %s. Extraction from it would not "
             "be extraction from approved content."
             % (ssf_sha[:16], APPROVED_SSF[:16]))
print("SSF verified at the approved hash: %s" % ssf_sha[:16])

ssf = text_of(SSF).split("\n")
raw = PREREG.read_bytes()
if raw.count(b"\r\n"):
    sys.exit("HALT: PREREG.md carries CRLF; this applier assumes LF")
before = hashlib.sha256(raw).hexdigest()
print("PREREG.md before: %s  (%d lines)" % (before[:16], raw.count(b"\n")))
lines = raw.decode("utf-8").split("\n")


def blockquote(heading, expect_in, declared, label):
    """The block's TRUE extent: the contiguous blockquote after its heading.

    NOT the range `BLOCK_MANIFEST.md` declares. A first version trusted those
    ranges and applied §AB EIGHT LINES SHORT and §AC EIGHT LINES SHORT --
    cutting disclosure 7 mid-sentence and dropping §AC's closing paragraph
    entirely ("These seven are disclosed because the record should not have to
    be reverse-engineered to find them"). The manifest's §AC range even STARTS
    inside §AB's blockquote, which is why an earlier contiguity check tripped on
    it. **A declared range is an assertion; the block's extent is a fact about
    the file**, and the extent is what gets applied.

    The declared range is still passed in, and any disagreement is REPORTED --
    a manifest that understates a block is a finding, not a detail to route
    around silently.
    """
    idx = [n for n, l in enumerate(ssf) if l.startswith(heading)]
    if len(idx) != 1:
        sys.exit("HALT: %s -- its heading occurs %d times in SSF, expected 1"
                 % (label, len(idx)))
    i = idx[0]
    while i < len(ssf) and not ssf[i].startswith(">"):
        i += 1
    lo = i
    while i < len(ssf) and ssf[i].startswith(">"):
        i += 1
    body = ssf[lo:i]
    if expect_in not in "\n".join(body):
        sys.exit("HALT: %s -- %r is not in the blockquote after its heading"
                 % (label, expect_in[:40]))
    first, last = lo + 1, i
    note = ""
    if (first, last) != declared:
        # OFFSET, NOT SHORT. Both declared ranges are the RIGHT LENGTH and start
        # eight lines early, so they cover the block's apparatus plus all but its
        # last eight lines. A first version of this message computed a length
        # difference, got zero, and printed "0 lines SHORT" -- a number that says
        # nothing about the actual defect. Something shifted SSF by eight lines
        # after BLOCK_MANIFEST recorded these ranges and the ranges were never
        # re-derived.
        note = ("  ** BLOCK_MANIFEST declares ll.%d-%d: same length, OFFSET BY %+d **"
                % (declared[0], declared[1], first - declared[0]))
    print("  extracted %-16s SSF ll.%d-%d, %d lines%s"
          % (label, first, last, len(body), note))
    return body


ab = blockquote("### §AB", "RECORDED DEFECT", (1632, 1679), "§AB")
ac = blockquote("## §AC", "WHAT THIS AMENDMENT DISCLOSES", (1687, 1737), "§AC")
limb = blockquote("**SC-12(w) — ENTRY CONDITION", "(w) ENTRY CONDITION",
                  (1145, 1181), "SC-12(w) limb")

for name, body in (("§AB", ab), ("§AC", ac), ("SC-12(w)", limb)):
    probe = max(body, key=len)
    if probe in lines:
        print("ALREADY APPLIED (%s). Nothing written." % name)
        sys.exit(0)


def only(pred, label):
    hits = [i for i, l in enumerate(lines, 1) if pred(l)]
    if len(hits) != 1:
        sys.exit("HALT: %s matches %d lines, expected 1" % (label, len(hits)))
    return hits[0]


# --- anchor 1: the end of §13c-P's fenced block ----------------------------
m13 = only(lambda l: l == "<!-- v30a SC-13c-2 — INSERT_AFTER -->", "§13c-P's marker")
fences = [i for i in range(m13, min(m13 + 20, len(lines) + 1))
          if lines[i - 1].strip() == "```"]
if len(fences) < 2:
    sys.exit("HALT: §13c-P -- expected two fences near its marker, found %d" % len(fences))
at_ab = fences[1]

# --- anchor 2: immediately before SC-13b's marker, i.e. after SC-12's clause
at_limb = only(lambda l: l == "<!-- v30a SC-13b — INSERT_AFTER_RELATIVE -->",
               "SC-13b's marker") - 1

print()
print("anchors, located never offset:")
print("  §AB + §AC  after l.%d  (§13c-P's block closes there)" % at_ab)
print("  SC-12(w)   before l.%d (SC-13b's marker; i.e. after SC-12's clause)" % (at_limb + 1))

# --- apply BOTTOM-TO-TOP ---------------------------------------------------
print()
print("applying bottom-to-top: SC-12(w)@l.%d then §AB+§AC@l.%d" % (at_limb, at_ab))
lines[at_limb:at_limb] = [""] + limb
lines[at_ab:at_ab] = [""] + ab + [""] + ac

out = "\n".join(lines)
o = out.split("\n")

# --- structure, BEFORE the write -------------------------------------------
for name, body in (("§AB", ab), ("§AC", ac), ("SC-12(w)", limb)):
    j = o.index(body[0])
    if o[j - 1].strip():
        sys.exit("HALT: %s opens at l.%d flush against %r -- a blockquote needs "
                 "its blank line or it merges into the paragraph above"
                 % (name, j + 1, o[j - 1][:60]))
    end = j + len(body) - 1
    nxt = next((o[k] for k in range(end + 1, len(o)) if o[k].strip()), "")
    print("  %-9s l.%-5d .. l.%-5d  above=%r  below=%r"
          % (name, j + 1, end + 1, o[j - 1][:20], nxt[:44]))
for k, l in enumerate(o):
    if l.strip() == "---" and k and o[k - 1].strip() and not o[k - 1].lstrip().startswith("|"):
        sys.exit("HALT: a `---` at l.%d sits flush against %r" % (k + 1, o[k - 1][:60]))
print("structure: every hunk opens after a blank line; no rule flush against text")

PREREG.write_bytes(out.encode("utf-8"))
b = PREREG.read_bytes()
print()
print("PREREG.md after : %s  (%d lines, %d CRLF / %d LF)"
      % (hashlib.sha256(b).hexdigest()[:16], b.count(b"\n"),
         b.count(b"\r\n"), b.count(b"\n")))
bad = sorted({c for c in b if c < 32 and c not in (9, 10, 13)})
print("control chars beyond tab/LF/CR: %s" % (bad or "none"))
