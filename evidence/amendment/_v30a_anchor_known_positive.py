#!/usr/bin/env python3
"""Known-positive battery for the anchor-keyed exemptions.

A conversion that made every exempted site pass unconditionally would look
identical to a correct one from the gate's exit status alone. So each property
the exemptions are supposed to have is broken deliberately, and the check must
fire:

  1. VALUE SCOPE SURVIVES  - an exempted site that starts stating a DIFFERENT
     value must be reported. The exemption whitelists a historical value, not
     the site.
  2. AMBIGUITY IS REFUSED  - an anchor matching two lines must be reported
     UNUSABLE, not applied to the first match.
  3. A DEAD ANCHOR IS REPORTED - an exemption whose anchor text is gone must be
     reported as a hole, not silently ignored.

Every mutation is reverted byte-exact and verified by sha256.

Written with the Write tool per D2.1.
"""
import hashlib
import pathlib
import subprocess
import sys

REPO = pathlib.Path(r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01")
DECL = REPO / "AVAILABILITY_DECLARATION.md"
SRC = REPO / "tools/check_registration.py"


def gate():
    r = subprocess.run([sys.executable, "tools/check_registration.py", "--stage", "prereg"],
                       cwd=str(REPO), capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return r.stdout + r.stderr


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


results = []
d0, s0 = sha(DECL), sha(SRC)

# -- 1. value scope ---------------------------------------------------------
raw = DECL.read_bytes()
anchor = b"R7 reads:"
assert raw.count(anchor) == 1
line_start = raw.rindex(b"\n", 0, raw.index(anchor)) + 1
line_end = raw.index(b"\r\n", raw.index(anchor))
line = raw[line_start:line_end]
mutated = line.replace(b"ALL FIVE", b"ALL SEVEN")
assert mutated != line, "mutation did not apply"
DECL.write_bytes(raw[:line_start] + mutated + raw[line_end:])
out = gate()
fired = "exempt for [5], but it now also states [7]" in out
results.append(("1. value scope: exempt site states an UNLISTED value", fired))
DECL.write_bytes(raw)
assert sha(DECL) == d0, "declaration not restored byte-exact"

# -- 2. ambiguity -----------------------------------------------------------
src = SRC.read_bytes()
# Narrow a real anchor to a string that occurs many times, without touching
# anything else: 'R7 reads:' -> 'R7' (which appears on many lines).
amb = src.replace(b"'R7 reads:'", b"'R7'", 1)
assert amb != src, "ambiguity mutation did not apply"
SRC.write_bytes(amb)
out = gate()
fired = "UNUSABLE" in out and "matches" in out
results.append(("2. ambiguity: an anchor selecting >1 line is REFUSED", fired))
SRC.write_bytes(src)
assert sha(SRC) == s0, "checker not restored byte-exact"

# -- 3. dead anchor ---------------------------------------------------------
dead = src.replace(b"'R7 reads:'", b"'R7 reads NOTHING AT ALL:'", 1)
assert dead != src
SRC.write_bytes(dead)
out = gate()
fired = "fired on nothing" in out and "anchor text is gone" in out
results.append(("3. dead anchor: reported as a hole, not a no-op", fired))
SRC.write_bytes(src)
assert sha(SRC) == s0, "checker not restored byte-exact"

print("ANCHOR EXEMPTIONS - KNOWN POSITIVE BATTERY\n")
ok = True
for name, fired in results:
    print("  %-56s %s" % (name, "FIRED" if fired else "** DID NOT FIRE **"))
    ok &= fired
print("\n  declaration restored byte-exact: %s" % (sha(DECL) == d0))
print("  checker restored byte-exact:     %s" % (sha(SRC) == s0))
print("\n  RESULT: %s" % ("PASS - anchoring did not weaken the exemptions"
                          if ok else "** FAIL **"))
sys.exit(0 if ok else 1)
