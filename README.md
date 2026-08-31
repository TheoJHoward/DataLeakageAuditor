# Data Leakage Auditor

**Working name:** TBD (placeholder: `leakaudit`)
**Author:** Theo Johann Howard
**Repository:** https://github.com/TheoJHoward/DataLeakageAuditor.git

This repository holds a **pre-registration** and the **tool being built against
it**. They are kept apart deliberately, and the front page says which is which,
because a reader who cannot tell a specification from a claim has been given no
way to check either.

## The pre-registration

Signed and externally timestamped. The specification is changed only through the
class C amendment route it registers for itself, and has been changed once —
`v30a`.

- **`PREREG.md`** — the locked specification: scope, metrics, acceptance gates,
  and what every published number is allowed to mean.
- **`DESIGN.md`** — its revisable companion.
- **`HISTORY.md`** — the version ledger and the review register.
- **`AVAILABILITY_DECLARATION.md`** — the acceptance fixture's reconstructed
  availability declaration, which carries the ground truth the acceptance gate
  is scored against.
- **`DEVIATIONS.md`** — append-only. Every departure, defect and disclosure,
  including the ones that make the project look worse.
- **`protocol/runtime_reference.py`** and `tools/check_registration.py` — the
  protocol tooling `PREREG.md` §11 item 1 requires in the first commit: a
  reference reducer for the runtime measurement semantics, its exhaustive trace
  suite, and a staged registration checker.

## The tool

**`leakaudit`** — Phase 1, under development, and installable now. Install
instructions, verified by execution rather than by reading, are in
[`INSTALL.md`](INSTALL.md).

**Status, stated plainly so that nothing here is mistaken for a result.** **No
acceptance gate has been executed.** No detector output in this repository is
published as a satisfied gate, none of it carries acceptance weight, and the
question of which detectors the acceptance criteria are even evaluated on was
settled — from the specification's own text — later than the code that assumed
an answer to it. What exists is an installable package, a runtime probe suite,
and a test suite that runs. That is not a validated instrument and is not
offered as one.

> *Two sentences stood here until 31 August 2026 and were false by the time
> anyone read them: "This repository is a pre-registration, not a tool" and "No
> detector implementation exists." Both were true when written. They are
> recorded as corrected rather than quietly deleted, because a public front page
> asserting something untrue about its own contents is the most visible possible
> instance of the defect class this project exists to detect.*

**Phase 0 — the kill gate that can end the project (`PREREG.md` §10.1) — is
partly run.** Of its four work items, **prior-art verification is signed off**
(`HISTORY.md` H-34, 12 August 2026, verdict: the project proceeds). The
**cross-tool comparison ran on 14 August 2026 but does not satisfy §9.2**, and
the licence check is incomplete. Under the author's routing of 25 August 2026,
**§9.2 and the licence check are Phase 1 entry obligations, not open blockers on
this tag** — H-34's verdict is the sign-off the tag requires, and neither
outstanding item is waived.

## Install

```bash
python -m pip install .
```

Editable, for development:

```bash
python -m pip install -e ".[dev]"
```

Requires **Python ≥ 3.11**. Two packages are installed: the auditor and the
protocol reducers it imports.

**What a stranger gets, and what they do not.** They get the auditor. They do
**not** get the acceptance fixture, which is not packaged; `import leakaudit`
succeeds without it and the adapter raises with its reason when the fixture's
own producing code is absent.

Runtime dependencies and their licence determinations, the record of what was
verified by execution rather than by reading, and the two defects that record
found are in [`INSTALL.md`](INSTALL.md).

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

**These hashes are of the files as of tag `prereg-v30a`.** `PREREG.md` is
locked and never changes; `DEVIATIONS.md` is append-only, and `HISTORY.md`,
`tools/check_registration.py`, `DESIGN.md` and this README are revisable, so
`HEAD` may legitimately differ from the tagged state — verify against the
tag (`git show prereg-v30a:PREREG.md | sha256sum`), not against `HEAD`. A
hash mismatch at the tag is tampering; a mismatch at `HEAD` need not be.

SHA-256 of every file the `prereg-v30a` tag message enumerates, as committed at
`prereg-v30a`. The set is the one
`PREREG.md` §11 item 8 defines and `AVAILABILITY_DECLARATION.md` §D.2 sets out; its count is read
from the enumeration below, not stated separately:

```
fcacebb231438e311f20f0c8179eb73cbebbd5fad6ad0ccf308459422557b6cc  PREREG.md
39a944c1cef2f4cea8cac3d84648ecec5407997ee010ef4e33ea6131cd0dcc00  DESIGN.md
cb3e7065890b8989b9eb7cd775803b8712d7b7a775dc9d8aefa4f18d18586fc5  HISTORY.md
bdd64bd7211d57055b6c741e4d6505696ca5905c10fa01de74da8149acfa5591  tools/check_registration.py
215194c15ab89f208198ce6bc3f8dd726d652fa6bee3d7bd868d1234c9bec31a  protocol/runtime_reference.py
79357d774b330dfaa0e517fcb0ca1026164cce9620730e903753adab2053047f  AVAILABILITY_DECLARATION.md
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  DEVIATIONS.md
7d00fcf5597f71c0f4581475b66014b264e2f1914c81af6980510e0214c1b392  PARKING_LOT.md
7e3149e6ad8fcc3e4730a159e81acbeee11571849ab8224f9079c3b37f04bc71  VALIDATED_CONFIG.toml
6a1b2a4db70b8fe1ef69dec2b6c1a7cebef42c13dcd2a8138ed11557ca487ea9  tests/registration/EXPECTED_OUTPUTS.md
cd3ebb73f6ef20df48e8a61ca8ca549d6f79cdd843441efd4836fa4a81bf49a5  tests/registration/conftest.py
44e98f60541a05ede2c4581cf1ddab0c43a3cb018033f948acc02846c818cc8c  tests/registration/generate_expected_outputs.py
00e19fa631fbc2e46936e666f535965b4bee046c93ea705e3b05c4f3dda2b1ee  tests/registration/test_checker.py
94793a25a1a756c26c55fbf20ce6445e628cb855c6b03104efa9d8424cffbd72  tests/registration/test_expected_outputs.py
08e77b3d427d752627573ddbf2f4635611c62dd297149ea1ada9735126da6a3e  tests/registration/test_invariants.py
f9d5f5e1f98c13f7c1b7645c33e6f19058ab33e7bfb2cc53d3d5f111bd895619  tests/registration/test_traces.py
b4961c44b6d87338b94de4ee4897c2d0a5e0db3be842598a00d91659349d4a36  tests/registration/traces.py
0da59d53982188712073c9b7f5addcd66221babcd8555efabbbd0c3d3f208a1d  evidence/fixture_spike/f3/fixture_manifest_DRAFT.json
763ac6c8382752aff954550e759eac4c138ac976ffec6d09fc93dd289876b467  evidence/fixture_spike/n1/declared_map.csv
c659d3ac167a13afb52651d4521ecc9fd5c8fabd59fd2d712eb4afa5b4669665  evidence/fixture_spike/f3/phase7_l2_sim.py
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

```bash
python -m pytest tests/registration
```

```bash
python tools/check_registration.py --stage prereg
```

The trace suite must be green and the prereg stage must exit 0 — that is
the tag gate (`PREREG.md` §6.8).

### What you will actually see, and what it means

**Both of those commands are currently red, and both are red for the same
disclosed reason.** A stranger who cannot tell a disclosed false positive from a
real failure has not been given a working front door, so it is stated here
beside the commands that produce it rather than left to be found in the ledger.

Measured 31 August 2026 at `HEAD` on the author's machine, Python 3.12.10:

| command | what it prints |
|---|---|
| `python -m pytest tests/registration` | 137 collected — **136 passed, 1 failed** |
| `python tools/check_registration.py --stage prereg` | **exit 1 — 1 check failed, 1 finding** |

The single finding is `hash_set_single_source`, and the single failing test is
`test_prereg_stage_on_real_repo_exits_zero`, which asserts that stage exits zero
and therefore fails on that same finding. **They are one fact reported twice, not
two problems.**

**It is a known false positive, disclosed at `DEVIATIONS.md` entry D-V30A-11.**
The check exists to catch prose that restates the registered path enumeration
without carrying the digests, because a restated list drifts from the list the
signed tag attests. It fires on a note in the version ledger that names several
registered paths in passing and asserts nothing about them.

**It is pinned, not silenced, and that is the point.** Adding an exemption to
make the tree pass is exactly what this file's own header forbids — "no
exemption may be added to make current files pass" — and an instrument that can
be edited into agreement with the tree certifies nothing. A red gate that is
disclosed and understood is worth more than a green one that was arranged.

**Any other finding, and any other failing test, is a real one.**

The full suite, `python -m pytest tests`, additionally runs the Phase 1 tests:
330 collected on the same machine and date, of which 4 skip. Those 4 are opt-in
behind `LEAKAUDIT_FIXTURE=1` because they build the acceptance fixture and take
minutes.

The `implementation` and `release` stages are expected to fail until the phases
that own their artifacts exist; every stage prints the checks it defers and the
stage that owns them.

## What this registration claims

Only what `PREREG.md` §5.4 licenses, and nothing on its "Never" list. The
scope, the metrics, the acceptance gates, and every published number's
meaning are locked in `PREREG.md`; changes route through `DEVIATIONS.md`
and, where they change what a published number means, a class C amendment
(`PREREG.md` §0.2.1).
