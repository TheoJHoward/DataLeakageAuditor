# Data Leakage Auditor — pre-registration (v30)

**Working name:** TBD (placeholder: `leakaudit`)
**Author:** Theo Johann Howard
**Repository:** https://github.com/TheoJHoward/DataLeakageAuditor.git

This repository is a **pre-registration, not a tool**. It contains the locked
specification (`PREREG.md` v30), its revisable companion (`DESIGN.md`), the
version ledger (`HISTORY.md`), and the protocol tooling `PREREG.md` §11
item 1 requires in the first commit: a reference reducer for the runtime
measurement semantics, its exhaustive trace suite, and a staged registration
checker. **No detector implementation exists.**

**Phase 0 — the kill gate that can end the project (`PREREG.md` §10.1) — is
partly run.** Of its four work items, **prior-art verification is signed off**
(`HISTORY.md` H-34, 12 August 2026, verdict: the project proceeds). The
**cross-tool comparison ran on 14 August 2026 but does not satisfy §9.2**, and
the licence check is incomplete. Under the author's routing of 25 August 2026,
**§9.2 and the licence check are Phase 1 entry obligations, not open blockers on
this tag** — H-34's verdict is the sign-off the tag requires, and neither
outstanding item is waived.

## Registration integrity (`PREREG.md` §11)

Signed tag: `prereg-v30`, pointing at the registration commit. The commit
hash is externally timestamped via OpenTimestamps, with the `.ots` receipt
committed in a follow-up commit — a commit cannot contain the receipt for
its own hash. The tag never moves.

**These hashes are of the files as of tag `prereg-v30`.** `PREREG.md` is
locked and never changes; `DESIGN.md` and this README are revisable, so
`HEAD` may legitimately differ from the tagged state — verify against the
tag (`git show prereg-v30:PREREG.md | sha256sum`), not against `HEAD`. A
hash mismatch at the tag is tampering; a mismatch at `HEAD` need not be.

SHA-256 of the documents and tooling as committed at `prereg-v30`:

```
f0a8f00164c217a40f87a4dc9fee6193ee7e4e125c68e3ecc84863fd6e2c7cc6  PREREG.md
039240e3c57497cc8eda65fbfcdc3d1120f1d7a12ad0f41b48d71c98ef063428  DESIGN.md
e8cf5bbbc42762838318e2ffc8cf85b6f44ed701c3ee88f8e93a6e734fc43e0d  HISTORY.md
72ffc7c69899844644ff79a9f6a12b083bbbe2c1160aca8d90dbe9415a0322e2  tools/check_registration.py
215194c15ab89f208198ce6bc3f8dd726d652fa6bee3d7bd868d1234c9bec31a  protocol/runtime_reference.py
```

### v30a — amended registration

<!-- V30A-HASH-BLOCK: FILLED AT CEREMONY TIME FROM v30a.hashes.txt. DO NOT TRANSCRIBE. -->

SHA-256 of the documents and tooling as committed at `prereg-v30a` — **six files**, the five above
recomputed at their v30a state plus the availability declaration:

```
0c8da19f237cd2437b91ef38c570f0ca2159863edcd7f05b10c5cdab9873d3a7  PREREG.md
39a944c1cef2f4cea8cac3d84648ecec5407997ee010ef4e33ea6131cd0dcc00  DESIGN.md
d19e49645a6143bd3fbd4827860bbc2b49954bd879e6a2f04d137a031f76ccc1  HISTORY.md
e82daa5171fee76346fd0cd83e4eeed729375c1c284e3f0e9c21a06634321a73  tools/check_registration.py
215194c15ab89f208198ce6bc3f8dd726d652fa6bee3d7bd868d1234c9bec31a  protocol/runtime_reference.py
10b65a00651b6e8c79db26a7eab165361e0bb9122d746806f987996eefb2bb42  AVAILABILITY_DECLARATION.md
```

**Both blocks stand.** The `prereg-v30` block above is not edited: it records the files as of that
tag, and `prereg-v30a` is a second tag, not a replacement. A reader verifying the v30 tag needs the
v30 hashes.

The tag `prereg-v30` is signed by the author's key:

```
RSA 4096 — Theo Johann Howard
Key fingerprint = 991F 5331 C584 CE5E AF7D  6939 B29C F0E8 4711 9AD7
```

## Verify

```
python -m pytest tests/registration
python tools/check_registration.py --stage prereg
```

The trace suite must be green and the prereg stage must exit 0 — that is
the tag gate (`PREREG.md` §6.8). The `implementation` and `release` stages
are expected to fail until the phases that own their artifacts exist; every
stage prints the checks it defers and the stage that owns them.

## What this registration claims

Only what `PREREG.md` §5.4 licenses, and nothing on its "Never" list. The
scope, the metrics, the acceptance gates, and every published number's
meaning are locked in `PREREG.md`; changes route through `DEVIATIONS.md`
and, where they change what a published number means, a class C amendment
(`PREREG.md` §0.2.1).
