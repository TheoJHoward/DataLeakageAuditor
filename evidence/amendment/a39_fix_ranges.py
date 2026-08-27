"""A39 -- re-derive BLOCK_MANIFEST's §A ranges from the structures themselves.

R146 §1.4: the off-by-eight rows are FIXED, not disclosed. `BLOCK_MANIFEST.md` is
a working document, not one of the twenty, and a stale range is a stale
verification value (§187).

WHY THIS MATTERS RATHER THAN BEING TIDINESS. Extracting inside a stale range
truncated §AB and §AC by eight lines each, cutting §AC's disclosure 7
mid-sentence. The ranges are read by extractors; leaving them wrong leaves the
next extractor to repeat it.

THE DECLARED RANGE IS A SEARCH HINT, NEVER THE EXTENT. The extent comes from the
structure's OWN delimiters -- the contiguous run of its opening mark. Using the
declared range to bound the extent is what caused the defect, so it is used only
to find the neighbourhood and to supply the expected LENGTH.

LENGTH PRESERVATION IS THE ACCEPTANCE TEST. A block that MOVED keeps its length,
so a candidate is written only when its span equals the declared span at a
non-zero offset. That test is not decoration: without it, this script expanded
rows declaring a SUB-range of a longer run -- row 1a's 150-153 became 150-159,
swallowing row 1b whole -- and short-circuited on row 32, whose `extent(1604)`
found the ANCHOR fence so the INSERT fence at 1612 was never tried. Both wrote
invented numbers over known-stale ones, which is strictly worse, because an
invented number looks derived.

ROWS WITH NO LENGTH-PRESERVING CANDIDATE ARE LEFT ALONE AND REPORTED -- sixteen
of them. Several are certainly stale too (rows 26, 31 and 32 among them), but
this instrument cannot resolve a sub-range within a longer structure, and a
number it cannot derive is one it must not write.

    usage: a39_fix_ranges.py
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
MAN = REPO / "evidence/amendment/BLOCK_MANIFEST.md"
APPROVED = "32358f6dfc7f96d2ac1e97cea9b6743dde674c78ac05cc114cc42e41ca33f2dc"
NOTE_MARK = "**RANGES ARE DERIVED, NOT DECLARED**"

sha = hashlib.sha256(SSF.read_bytes()).hexdigest()
if sha != APPROVED:
    sys.exit("HALT: SSF is %s, not the approved %s" % (sha[:16], APPROVED[:16]))
print("SSF at the approved hash %s" % sha[:16])

ssf = SSF.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")

raw = MAN.read_bytes()
crlf, lf = raw.count(b"\r\n"), raw.count(b"\n")
if crlf and crlf != lf:
    sys.exit("HALT: BLOCK_MANIFEST.md is mixed (%d CRLF / %d LF)" % (crlf, lf))
nl = "\r\n" if crlf else "\n"
print("BLOCK_MANIFEST.md before: %s (%d lines, %s)"
      % (hashlib.sha256(raw).hexdigest()[:16], lf, "CRLF" if crlf else "LF"))
text = raw.decode("utf-8").replace("\r\n", "\n")
if NOTE_MARK in text:
    print("ALREADY APPLIED. Nothing written.")
    sys.exit(0)

MARKS = ("#", ">", "|", "```")


def opener(n):
    cur = ssf[n - 1].lstrip() if 1 <= n <= len(ssf) else ""
    prev = ssf[n - 2].lstrip() if 2 <= n <= len(ssf) else ""
    for m in MARKS:
        if cur.startswith(m):
            return None if prev.startswith(m) else m
    return None


def extent(first):
    m = opener(first)
    if m is None:
        return None
    i = first
    while i <= len(ssf) and ssf[i - 1].lstrip().startswith(m):
        i += 1
    return first, i - 1


ROW = re.compile(r"^(\|\s*[0-9]+[a-z]?\s*\|\s*)(\d+)(\s*[–—-]\s*)(\d+)(\s*\|.*)$")

out, fixed, ok, unlocatable = [], [], 0, []
for line in text.split("\n"):
    m = ROW.match(line)
    if not m:
        out.append(line)
        continue
    pre, a, dash, b, rest = m.groups()
    first, last = int(a), int(b)
    rid = pre.strip("| ").strip()
    # LENGTH PRESERVATION IS THE TEST, and it is what makes this safe.
    #
    # A first version took `extent(first) or extent(first + 8)` and wrote whatever
    # came back. That was wrong twice over. It EXPANDED rows that deliberately
    # declare a SUB-range of a longer contiguous run -- row 1a's 150-153 became
    # 150-159, swallowing row 1b whole -- and it SHORT-CIRCUITED: row 32's
    # `extent(1604)` found the ANCHOR fence, so `extent(1612)`, where the INSERT
    # fence actually is, was never tried. Both replaced a known-stale number with
    # an invented one, which is worse, because an invented number looks derived.
    #
    # A row that MOVED keeps its length. So both offsets are tried, and a
    # candidate is accepted only if its span equals the declared span. Anything
    # else is REPORTED, never written.
    want = last - first
    cand = None
    for off in (0, 8):
        got = extent(first + off)
        if got and got[1] - got[0] == want and off != 0:
            cand = got
            break
    if cand is None:
        if extent(first) and extent(first)[1] - extent(first)[0] == want:
            ok += 1                      # declared range already correct
        else:
            unlocatable.append((rid, first, last))
        out.append(line)
        continue
    nf, nl_ = cand
    fixed.append((rid, first, last, nf, nl_, nf - first))
    out.append("%s%d%s%d%s" % (pre, nf, dash, nl_, rest))

print()
print("rows already correct : %d" % ok)
print("rows CORRECTED       : %d" % len(fixed))
print("rows NOT resolved    : %d  (left untouched, reported -- never guessed)" % len(unlocatable))
print()
for rid, a, b, na, nb, off in fixed:
    print("  row %-4s %4d-%-4d -> %4d-%-4d  (%+d)" % (rid, a, b, na, nb, off))
if unlocatable:
    print()
    for rid, a, b in unlocatable:
        print("  row %-4s %4d-%-4d  no length-preserving candidate at %d or %d -- NOT GUESSED"
              % (rid, a, b, a, a + 8))

if not fixed:
    print("\nnothing to change")
    sys.exit(0)

# The note goes immediately above the §A table's header row, so a reader meets it
# before the numbers. Anchored on the header, never on a line number.
body = "\n".join(out)
hdr = [i for i, l in enumerate(body.split("\n"))
       if l.startswith("| # |") or l.startswith("| id |")]
lines = body.split("\n")
NOTE = (
    "%s. Every range below was re-derived at R146/A39 from the structure's own "
    "delimiters in `SCHEMA_SET_FINAL.md` at the approved hash `%s…`, and %d of them were "
    "wrong — %d by exactly eight lines. **Do not extract inside a range from this table without "
    "re-deriving it**: the previous values ended before their blockquotes did, and extracting "
    "inside them truncated §AB and §AC by eight lines each, cutting §AC's disclosure 7 "
    "mid-sentence. A declared range is an assertion; the block's extent is a fact about the file."
    % (NOTE_MARK, sha[:16], len(fixed), sum(1 for f in fixed if f[5] == 8)))
if hdr:
    lines.insert(hdr[0], NOTE)
    lines.insert(hdr[0] + 1, "")
else:
    lines.insert(0, NOTE)
    lines.insert(1, "")
    print("note: §A header row not found; note placed at the top")

o = lines
for k, l in enumerate(o):
    if l.strip() == "---" and k and o[k - 1].strip() and not o[k - 1].lstrip().startswith("|"):
        sys.exit("HALT: a `---` at l.%d sits flush against %r" % (k + 1, o[k - 1][:60]))
print("\nstructure: no rule flush against text")

MAN.write_bytes(("\n".join(o)).replace("\n", nl).encode("utf-8"))
b2 = MAN.read_bytes()
print("BLOCK_MANIFEST.md after : %s (%d lines, %d CRLF / %d LF)"
      % (hashlib.sha256(b2).hexdigest()[:16], b2.count(b"\n"),
         b2.count(b"\r\n"), b2.count(b"\n")))
bad = sorted({c for c in b2 if c < 32 and c not in (9, 10, 13)})
print("control chars beyond tab/LF/CR: %s" % (bad or "none"))
print("SSF unchanged: %s"
      % (hashlib.sha256(SSF.read_bytes()).hexdigest() == APPROVED))
