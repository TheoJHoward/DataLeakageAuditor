#!/usr/bin/env python3
"""Bank A4.4/A4.5/A4.6 and A5's blast radius into ROUND_STATE.md, then resync.

ROUND_STATE.md is the report (§0.1). It is manifest-attested, so its line is
recomputed from disk after the append, in the same pass.

Written with the Write tool per D2.1.
"""
import hashlib
import pathlib
import sys

REPO = pathlib.Path(r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01")
RS = REPO / "evidence/session/ROUND_STATE.md"
MAN = REPO / "evidence/MANIFEST.sha256"

APPEND = """
---

## A4.4 — THE THREE CITING RECORDS

| record | kind | treatment |
|---|---|---|
| `evidence/ceremony/F3_MANIFEST_VERIFICATION.md` | dated evidence record | **SUPERSEDED** by a dated entry above the warning. The warning is retained unedited — it was true on its date. |
| `evidence/session/DEFERRED_ITEMS.md` | live working record | updated in place; the item is marked DISCHARGED with its date |
| `evidence/session/ROUND_STATE.md` | live working record | updated in place |

**The scope collision is now stated rather than left to be inferred.** The
`D-ARCHIVE` draft said *"The producing code IS committed"*; the F3 verification
said *"THE PRODUCING CODE IS NOT IN THE REPOSITORY"*. **Both were true — of
different sets:** the first of the three spike producers, the second of
`phase7_l2_sim.py`, which was not among them. Nothing anywhere said they were
speaking about different sets, so the pair read as a contradiction. It was not
one, and it is no longer live either way.

---

## A4.5 / A4.6 — INSTRUMENTS IN, REPORT FOLDED, EVERYTHING STAGED

Ten build instruments from this closeout are in `evidence/amendment/` with
manifest entries, hashes computed from disk. §187's alternative — a D10 ephemeral
line — would have been inert: **D10's `_WORK_ROOT` names a different session's
scratchpad**, so a line for a file in the current one exempts something D10 never
looks at. That gap is recorded separately below.

Staged: **18 files**. Unstaged diff **EMPTY**, which is A5's precondition — C2
reads the index, so a modified-but-unstaged file would be hashed at its old
content and the tag would attest bytes that are not in the tree.

`tools/control_char_scan.py` remains untracked, deliberately: its own ephemeral
entry says committing it changes what ships.

---

## A5 — FILES GROWN TO TWENTY; THE BLAST RADIUS, DERIVED

`FILES` in `CEREMONY_COMMANDS.md` §3.2 now carries the twenty paths item 8
defines. Order is **not** alphabetical and must not be made so: the `prereg-v30`
five come first in the v30 order, so the v30 block stays a verbatim prefix and no
v30-era verification instruction is invalidated.

**Every restatement that now disagrees was named by the gate, not by a grep.**
Twenty findings, reported here before any of them is edited:

| check | sites |
|---|---|
| **D1** — states 6, authority says 20 | declaration l.1008 · `CEREMONY_COMMANDS.md` l.625 · `COMMIT_PLAN.md` l.459 · `DEVIATIONS_DRAFT.md` l.262 |
| **D2** — enumeration is not the set | declaration l.3707 (the limb-1 table row) · `DEVIATIONS_DRAFT.md` l.263 · `CEREMONY_COMMANDS.md` §3.5's tag-message body |
| **D3 / D4** — staging plan | `COMMIT_PLAN.md` §4's add-set omits `PARKING_LOT.md`, `VALIDATED_CONFIG.toml` and the eight `tests/registration/` files; the plan never names them |
| **D7** — stale declaration hash | `README.md` l.59 · `DECLARATION_POINTER.md` · `F3_MANIFEST_VERIFICATION.md` l.21 |
| **D8** — drifted line citations | `CEREMONY_COMMANDS.md` l.268 (moved by the FILES edit) · `HISTORY.md` l.275 → 277 · declaration l.4008 → 4294 |
| **D10** | three working files in neither the repository nor the ephemeral list |

**One of the D7 hits is a mis-attribution, not a stale value.**
`F3_MANIFEST_VERIFICATION.md` l.21 is read as stating the declaration's sha256,
but the hash on that line is `phase7_l2_sim.py`'s, sitting near the declaration's
name in the supersession note added at A4.4. The value is correct for what it
names; the parser attributed it to the wrong file.

**Nothing in this list has been edited.** The repair is the next item.

---

## OPEN — FOR THE AUTHOR

**D10's population is a session directory that is no longer the working one.**
`tools/check_registration.py` pins `_WORK_ROOT` to one session's scratchpad; the
work now happens in another. Every file created this round is outside D10's
domain, including the instruments that edited registered files. D10 prints
*"every working file is in the repository or declared ephemeral"* while not
looking at the directory the work happens in — which is the instrument-domain
failure the project's own review lessons record, occurring in the check that
exists to catch it.

**Recommended: disclose, do not re-pin.** Re-pinning to the current session
reproduces a stale literal that detaches at the next session; deriving the
directory is a design change to a registered tool under a tag deadline. A sixth
entry in D-INSTRUMENT plus the substance in `DEFERRED_ITEMS.md` fits the closeout
test; the code change does not.
"""

raw = RS.read_bytes()
if raw.count(b"\r\n") != raw.count(b"\n"):
    sys.exit("HALT: ROUND_STATE.md is not uniformly CRLF")
text = raw.decode("utf-8").replace("\r\n", "\n").rstrip("\n") + "\n" + APPEND
RS.write_bytes(text.replace("\n", "\r\n").encode("utf-8"))

lines = MAN.read_bytes().decode("utf-8").split("\n")
n = 0
for i, line in enumerate(lines):
    if not line or line.startswith("#") or "  " not in line:
        continue
    digest, rel = line.split("  ", 1)
    t = (REPO / rel[3:]) if rel.startswith("../") else (REPO / "evidence" / rel)
    if t.exists():
        a = hashlib.sha256(t.read_bytes()).hexdigest()
        if a != digest:
            lines[i] = "%s  %s" % (a, rel)
            n += 1
MAN.write_bytes("\n".join(lines).encode("utf-8"))
print("ROUND_STATE.md: %d CRLF / %d LF" % (RS.read_bytes().count(b"\r\n"),
                                           RS.read_bytes().count(b"\n")))
print("manifest lines resynced: %d" % n)
