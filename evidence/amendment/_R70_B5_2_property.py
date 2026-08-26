#!/usr/bin/env python3
"""B5.2 — property-test D1 over 0-200 in every form, inside and outside tables.

For each value v in 0..200 and each surface form, build a line that a correct D1
must read as v, run D1's own matcher + parser, and record:
  DETECTED-CORRECT   value read == v
  DETECTED-WRONG     value read != v          <- worse than a miss
  MISSED             no match
Then report the range covered and the gaps LEFT OPEN.

Runs the detector's REAL objects, imported from the tool source, so the test
cannot drift from the implementation.
"""
import re, pathlib, sys

TOOL = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01/"
                    "tools/check_registration.py")
src = TOOL.read_text(encoding="utf-8")

# lift D1's number machinery verbatim, without importing the module (dataclass issue)
ns = {"re": re}
start = src.index("_HS_UNITS = {")
end = src.index("_HS_CTX = re.compile(")
exec(src[start:end], ns)                                    # noqa: S102 - test harness
NUM = ns["_hs_number"]
ATTACH, TAGLINES = ns["_HS_ATTACH"], ns["_HS_ATTACH_TAGLINES"]

# and the stripper
s0 = src.index("def _hash_set_strip(")
s1 = src.index("def hash_set_authority(")
exec(src[s0:s1], ns)                                        # noqa: S102
STRIP = ns["_hash_set_strip"]

UNITS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
         "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
         "sixteen", "seventeen", "eighteen", "nineteen"]
TENS = {20: "twenty", 30: "thirty", 40: "forty", 50: "fifty", 60: "sixty",
        70: "seventy", 80: "eighty", 90: "ninety"}


def words(n):
    if n < 20:
        return UNITS[n]
    if n < 100:
        t, u = divmod(n, 10)
        return TENS[t * 10] + ("-" + UNITS[u] if u else "")
    h, r = divmod(n, 100)
    out = UNITS[h] + " hundred"
    return out + (" and " + words(r) if r else "")


def forms(n):
    w = words(n)
    return [
        ("numeral", "the tag message carries %d hashes" % n),
        ("numeral+comma", "the tag message carries %s hashes" % format(n, ",")),
        ("word", "the tag message carries %s hashes" % w),
        ("word+emphasis", "the tag message carries **%s** hashes" % w),
        ("numeral+emphasis", "the tag message carries **%d** hashes" % n),
        ("table row", "| tag message | carries %s hashes | ok |" % w),
        ("table row numeral", "| tag message | carries %d hashes | ok |" % n),
        ("sha-256 lines", "the tag message carries %s SHA-256 lines" % w),
        ("line block", "the v30a %s-line block" % w),
        ("tag message with N lines", "a tag message with %s lines" % w),
    ]


def read(line):
    cleaned = STRIP(line)
    hits = list(ATTACH.finditer(cleaned)) + list(TAGLINES.finditer(cleaned))
    vals = set()
    for m in hits:
        v = NUM(m.group(1))
        if v is not None:
            vals.add(v)
    return vals


tally = {}
gaps = []
for n in range(0, 201):
    for name, line in forms(n):
        vals = read(line)
        if not vals:
            k = "MISSED"
            gaps.append((n, name, line, "no match"))
        elif n in vals:
            k = "DETECTED-CORRECT"
        else:
            k = "DETECTED-WRONG"
            gaps.append((n, name, line, "read %s" % sorted(vals)))
        tally[(name, k)] = tally.get((name, k), 0) + 1

print("B5.2 - PROPERTY TEST: values 0-200 x %d surface forms = %d cases\n"
      % (len(forms(0)), 201 * len(forms(0))))
names = [n for n, _ in forms(0)]
print("  %-26s %8s %8s %8s" % ("form", "CORRECT", "WRONG", "MISSED"))
for name in names:
    print("  %-26s %8d %8d %8d"
          % (name, tally.get((name, "DETECTED-CORRECT"), 0),
             tally.get((name, "DETECTED-WRONG"), 0),
             tally.get((name, "MISSED"), 0)))
tot_c = sum(v for (_, k), v in tally.items() if k == "DETECTED-CORRECT")
tot_w = sum(v for (_, k), v in tally.items() if k == "DETECTED-WRONG")
tot_m = sum(v for (_, k), v in tally.items() if k == "MISSED")
print("  %-26s %8d %8d %8d" % ("TOTAL", tot_c, tot_w, tot_m))

print("\n  GAPS LEFT OPEN (first 20 of %d):" % len(gaps))
for n, name, line, why in gaps[:20]:
    print("    n=%-4d %-24s %-14s %s" % (n, name, why, line[:58]))
