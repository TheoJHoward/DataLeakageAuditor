#!/usr/bin/env python3
"""B2.2 / B2.3 — three-way key chain, matching C2d-2's pattern.

The declaration is in the six-file hash set, so a fingerprint stated there is
covered by the tag AND by the OpenTimestamps receipt over the commit. That makes
it TIMESTAMPED rather than merely asserted.
"""
import pathlib

REPO = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01")
EM = "\u2014"; S = "\u00a7"
FPR = "991F5331C584CE5EAF7D6939B29CF0E847119AD7"

# ---- 1. §D.4 in the declaration ------------------------------------------
D = REPO / "AVAILABILITY_DECLARATION.md"
s = D.read_text(encoding="utf-8")
ANCHOR = "## " + S + "E. Gate protocol input surface"
assert s.count(ANCHOR) == 1, "declaration anchor %d" % s.count(ANCHOR)

BLOCK = """### D.4 {em} The signing key, stated here so it is TIMESTAMPED and not merely asserted (R69/B2.2)

**DECLARED: the `prereg-v30a` tag is signed by the OpenPGP key whose primary fingerprint is**

```
991F 5331 C584 CE5E AF7D  6939 B29C F0E8 4711 9AD7
```

**Why this belongs in THIS file and not only in the tag message.** The tag message asserts the
fingerprint, but a tag message is only as good as the signature over it {em} a message asserting a
fingerprint proves nothing about which key signed it, since the signer writes both. This file is
one of the six the tag message hashes, and the commit it is committed in is the commit
OpenTimestamps stamps. **So a fingerprint stated here is covered by the signature AND carries an
external Bitcoin-anchored timestamp**, which the tag message's own copy does not add.

**The verification chain this creates is three-way, deliberately mirroring {s}D.2's C2d-2 pattern:**

| leg | value | read from |
|---|---|---|
| 1 | the key that actually made the signature | `git verify-tag --raw`'s `[GNUPG:] VALIDSIG` **last field** (the PRIMARY key fingerprint, so a subkey signature still resolves here) |
| 2 | the fingerprint the tag message asserts | the signed tag body's `Key fingerprint = ` line |
| 3 | the fingerprint this declaration states | the block above |

**All three must agree, and C1b halts if they do not.** Two legs agreeing proves less than it
appears to: legs 1 and 2 together only establish that the signer was internally consistent.

**The key material itself ships.** `prereg-signing-key.asc` at the repository root is the
ASCII-armored public key, so the tagged tree carries the key a verifier needs. **It is deliberately
NOT added to the six-file hash list** {em} {s}14.1(b) holds: that list is a citation device, and the
commit tree already fixes every tracked file. **SIX is not reopened by this.**

**WHAT THIS DOES NOT ESTABLISH, stated plainly rather than left to inference.** Every leg above is
INTERNAL to this repository. Together they prove that the key which signed the tag is the key this
registration names {em} **they do not prove who holds that key.** Key-to-person binding cannot be
established by any repository-local check, because an attacker who could rewrite the tag could
rewrite all three legs. **That binding rests entirely on the key's publication outside this
repository, and {s}12's disclosure states where.**

## {s}E. Gate protocol input surface""".format(em=EM, s=S)

s = s.replace(ANCHOR, BLOCK, 1)
D.write_text(s, encoding="utf-8")
print("AVAILABILITY_DECLARATION.md: \u00a7D.4 added")

# ---- 2. C1b becomes three-way -------------------------------------------
CC = REPO / "evidence/ceremony/CEREMONY_COMMANDS.md"
c = CC.read_text(encoding="utf-8")
OLD = '''[ -n "$asserted" ] || { echo "C1b FAILED \u2014 the tag message states no fingerprint. HALT."; exit 1; }
[ "$asserted" = "$actual" ] || {
  echo "C1b FAILED \u2014 signed by $actual, but the message asserts $asserted. HALT."; exit 1; }
echo "C1b OK \u2014 good signature, primary key $actual, matching the message"'''
NEW = '''# Leg 3: the fingerprint the DECLARATION states (\u00a7D.4). The declaration is in the six
# and is OTS-covered, so this leg is timestamped rather than merely asserted. Legs 1 and 2
# alone only prove the signer was internally consistent with themselves.
declared=$(sed -n '/^### D\\.4 /,/^## /p' AVAILABILITY_DECLARATION.md \\
           | grep -oE '[0-9A-F]{4}( [0-9A-F]{4})+' | head -1 | tr -d ' ')

[ -n "$asserted" ] || { echo "C1b FAILED \u2014 the tag message states no fingerprint. HALT."; exit 1; }
[ -n "$declared" ] || { echo "C1b FAILED \u2014 \u00a7D.4 states no fingerprint. HALT."; exit 1; }
[ "$asserted" = "$actual" ] || {
  echo "C1b FAILED \u2014 signed by $actual, but the message asserts $asserted. HALT."; exit 1; }
[ "$declared" = "$actual" ] || {
  echo "C1b FAILED \u2014 signed by $actual, but \u00a7D.4 declares $declared. HALT."; exit 1; }
echo "C1b OK \u2014 good signature; signing key, tag message and \u00a7D.4 all read $actual"

# The public key ships in the tree, so a verifier needs no keyserver:
#   gpg --import prereg-signing-key.asc
# NOTE THE BOUNDARY. All three legs are INTERNAL to this repository. They prove the tag
# was signed by the key this registration names; they do NOT prove who holds that key.
# That binding rests on the key's publication outside this repository (\u00a712 disclosure).'''
assert c.count(OLD) == 1, "C1b match %d" % c.count(OLD)
CC.write_text(c.replace(OLD, NEW, 1), encoding="utf-8")
print("CEREMONY_COMMANDS.md: C1b is now three-way, with the boundary stated")

# ---- 3. stage the key file ----------------------------------------------
CP = REPO / "evidence/ceremony/COMMIT_PLAN.md"
p = CP.read_text(encoding="utf-8")
OLDA = "git add PREREG.md DEVIATIONS.md HISTORY.md DESIGN.md README.md"
NEWA = ("git add PREREG.md DEVIATIONS.md HISTORY.md DESIGN.md README.md prereg-signing-key.asc")
assert p.count(OLDA) == 1, "git add match %d" % p.count(OLDA)
p = p.replace(OLDA, NEWA, 1)
CP.write_text(p, encoding="utf-8")
print("COMMIT_PLAN.md: prereg-signing-key.asc added to the staging set")
