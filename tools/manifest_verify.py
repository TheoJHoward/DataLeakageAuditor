#!/usr/bin/env python3
"""Every hash the manifest attests matches the file it attests. R243 §1.

    $ py -3.12 tools/manifest_verify.py

Exit 0 when every attested hash matches, 1 otherwise. Certification is the
frozen checker AND this, and it passes only if both pass.

**WHY THIS IS A SIBLING AND NOT A CHECK INSIDE `check_registration.py`.**
R242 established the hole by producing it: a manifest line was corrupted to a
hash of zeros, and the gate returned the result it returns on a clean tree —
`manifest_coverage` asks which paths are listed against which are on disk, and
passes on a listed path whatever the file now contains. So the instrument that
CERTIFIES the registration was certifying content it never checked.

The first repair put the check inside `check_registration.py`, and **the frozen
comparison caught it**: that file is compared against the tagged one, every
difference has to be RULED, and R223 §1 fixed the ceiling at four before there
was pressure on it — *"it is not a budget to spend."* Spending a slot took the
count from 2 to 3.

**A frozen instrument tripping on an edit is the design saying the change belongs
elsewhere.** The two spent slots are repairs to what a frozen check DOES;
an ADDITION does not need to go inside. So the rule, recorded where the addition
lives:

    NEW verification is added as a NEW INSTRUMENT. Frozen-difference slots are
    for changes to behaviour that is already frozen, not for additions that
    could stand beside it.

Keeping the count at 2 is the win. Distance from the re-examination trigger is
the whole point of not treating it as a budget, and a slot spent on an avoidable
addition is distance lost for nothing.

**THE TWO INTEGRITY MECHANISMS ARE DISJOINT. THEY DO NOT JOINTLY COVER, and the
difference is measured rather than assumed.** R243 §3 asked for the disjointness
to be recorded so *"the instruments are not in the manifest"* reads as by design.
Half of that survives measurement over the 956 tracked files:

    attested by the MANIFEST      826   a sha256 per file over `evidence/` plus
                                        six `../` lines; coverage checked by the
                                        gate, content checked here
    covered by the FROZEN COMPARISON 2   `tools/check_registration.py` and
                                        `protocol/runtime_reference.py`, run
                                        beside their tagged forms with VERDICTS
                                        compared — not bytes
    in BOTH                         0   disjoint, as claimed
    in NEITHER                    132   88 tests, 16 `src/`, 9 `tools/`, and
                                        several root documents including
                                        `DEVIATIONS.md` and `DESIGN.md`

So *"the instruments are not in the manifest"* IS by design. *"Nothing is in
neither"* is not true, and the honest statement of what covers those 132 is
narrower than it first looks: **Phase 2 commits are not signed** (`git log
--format=%G?` reports `N` for every one of them). The signed `prereg-v30a` tag
attests one commit, `b5a05c0`, not the current tree.

**What covers the 132 is therefore git's content addressing and review**, which
detects corruption and does not attest authorship or intent. That is a smaller
claim than "two mechanisms cover everything", and it is recorded here rather
than left for a reader to discover, because a coverage story that sounds total
and is not is the failure this project names most often.

**THE RECIPE**, because a digest without one is not evidence (R229 §0): sha256
over each file's RAW BYTES. A line is `<64 lowercase hex>  <path>`, two spaces.
Paths are relative to `evidence/`, except `../` lines which are relative to the
repository root. The manifest cannot list itself and does not.

Written with the Write tool per D2.1.
"""
from __future__ import annotations

import hashlib
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
EVIDENCE = REPO / "evidence"
MANIFEST = EVIDENCE / "MANIFEST.sha256"
HEX = set("0123456789abcdef")


class ManifestUnverifiable(Exception):
    """The manifest could not be read, so nothing here is a result."""


def entries(manifest: pathlib.Path = None) -> list:
    """(digest, path-as-written) for every attesting line."""
    man = manifest or MANIFEST
    if not man.is_file():
        raise ManifestUnverifiable(
            "%s does not exist, so nothing attests the evidence tree and this "
            "reports nothing rather than reporting agreement" % man)
    out = []
    for line in man.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "  " not in line:
            continue
        digest, rel = line.split("  ", 1)
        if len(digest) != 64 or set(digest) - HEX:
            continue
        out.append((digest, rel.strip()))
    return out


def resolve(rel: str, repo: pathlib.Path = None) -> pathlib.Path:
    root = repo or REPO
    return (root / rel[3:]) if rel.startswith("../") else (root / "evidence" / rel)


def verify(manifest: pathlib.Path = None, repo: pathlib.Path = None) -> dict:
    """Compare every attested hash against its file.

    ZERO IS NOT A PASS. A verifier that checked nothing and said so with silence
    would read exactly like one that checked everything, which is the shape
    `OPERATING_RULES.md` §3 bans and D-V30A-48 recorded.
    """
    rows = entries(manifest)
    stale, absent, checked = [], [], 0
    for digest, rel in rows:
        target = resolve(rel, repo)
        if not target.is_file():
            absent.append(rel)
            continue
        if hashlib.sha256(target.read_bytes()).hexdigest() != digest:
            stale.append(rel)
        checked += 1
    return {"checked": checked, "stale": stale, "absent": absent,
            "lines": len(rows)}


def main(argv=None) -> int:
    try:
        r = verify()
    except ManifestUnverifiable as e:
        print("UNVERIFIABLE: %s" % e)
        return 1

    print("MANIFEST CONTENT VERIFICATION -- %s" % MANIFEST)
    print("  recipe: sha256 over raw bytes; `<64 hex>  <path>`; paths relative "
          "to evidence/, `../` to the repository root")
    print("  attesting lines : %d" % r["lines"])
    print("  verified        : %d" % r["checked"])
    print("  STALE           : %d" % len(r["stale"]))
    print("  absent from disk: %d" % len(r["absent"]))

    if not r["checked"]:
        print()
        print("COVERAGE IS ZERO. No attesting line was verified, so this "
              "reports nothing rather than reporting agreement.")
        return 1
    for rel in r["stale"]:
        print("  STALE: %s -- the file has changed since the manifest recorded "
              "it, so the commit would ship a false attestation" % rel)
    for rel in r["absent"]:
        print("  ABSENT: %s -- attested and not on disk" % rel)
    print()
    if r["stale"] or r["absent"]:
        print("FAIL. `manifest_coverage` in the gate passes on this: the path "
              "IS listed, and coverage and content are different claims.")
        return 1
    print("OK. Every attested hash matches its file (%d verified)."
          % r["checked"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
