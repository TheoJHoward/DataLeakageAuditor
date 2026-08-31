# INSTALL — `leakaudit`

**Criterion 5 scaffold (B-5).** *Written while `main` was frozen awaiting the `prereg-v30a`
signature, when a pre-tag README edit was a halt. **That block is discharged: the tag is signed, and
`README.md` now carries the install and verify blocks and links here.** The sentence is corrected
rather than deleted, because a reader of an earlier revision needs to know why this file once stood
alone.*

## Install

```bash
python -m pip install .
```

Editable, for development:

```bash
python -m pip install -e ".[dev]"
```

Requires **Python ≥ 3.11**.

## What was actually verified, and what "verified" means here

**Building is not installing, and installing is not importing.** All three were run:

| step | result |
|---|---|
| metadata build | **OK** *(failed first — see below)* |
| `pip install --target` into a clean directory | **OK** — `leakaudit/` and `protocol/` both land |
| import from the installed copy alone | **OK** — `leakaudit`, `.detectors`, `.corruption`, `.contract`, `.fixture_adapter`, `protocol.runtime_reference` |
| recorded metadata | `leakaudit 0.1.0.dev0`, licence **MIT**, requires `numpy>=1.26`, `pandas>=2.1`, `pyarrow>=14` |

**Two defects were found by doing this rather than by reading the file.**

1. **The metadata build failed** on a PEP 639 conflict: the project declared both an SPDX
   `license = "MIT"` and the legacy `License :: OSI Approved :: MIT License` classifier, which
   setuptools refuses. The file **parsed cleanly** throughout — parsing was never the test.
2. **The first successful install could not be imported.** `leakaudit.contract` imports
   `protocol.runtime_reference`, and `protocol/` was not in the distribution. A stranger would have
   installed a package that raises `ModuleNotFoundError` on first use.

`protocol` is now shipped **from its existing location**, not moved: `protocol/runtime_reference.py`
is one of the twenty registered paths whose hashes the `prereg-v30a` tag message carries, and
relocating it would alter a registered path while the tree is frozen.

## Runtime dependencies and their licences

Derived from the installed distributions, not asserted (§D.5(ii)):

| package | version here | licence |
|---|---|---|
| `numpy` | 2.4.2 | BSD-3-Clause AND 0BSD AND MIT |
| `pandas` | 3.0.1 | BSD-3-Clause |
| `pyarrow` | 23.0.1 | Apache-2.0 |
| `pytest` *(dev only, not shipped)* | 9.1.1 | MIT |

**Versions are floors, not pins.** A stranger should not have to fight our lockfile. The
registration's determinism claims are made about the pinned development environment, never about an
arbitrary install.

### `deepchecks` is **not** a dependency

It is a **comparator**, invoked as a separate program in its own virtualenv. Its
**AGPL-3.0-or-later is not engaged by this distribution**: nothing here contains, links to, or
redistributes it. Interoperation is not vendoring — the determination is recorded at
[`W2B_STEP3_DISCHARGE.md`](evidence/killgate/w2b/W2B_STEP3_DISCHARGE.md). Listing it as a dependency
would be false **and** would drag AGPL obligations onto a package that does not carry it.

## What a stranger gets, and what they do not

**They get the auditor.** They do **not** get the acceptance fixture.

`leakaudit.fixture_adapter` imports `fixture` and `phase5_ml_fixture` — the fixture's own producing
modules. Those are **not packaged**, and the import is **lazy**: `import leakaudit` succeeds without
them, verified. `fixture_adapter` raises `FixtureUnavailable` **with its reason** when they are
absent, which is the correct behaviour for someone who has no fixture to audit.

The fixture's producing code is committed under `evidence/fixture_spike/f2/`, and
`fixture_adapter.F2_DIR` **now resolves to that committed copy**, relative to the package's own
location. `LEAKAUDIT_F2_DIR` overrides it explicitly and is never the default.

> *Corrected 31 August 2026. This paragraph previously recorded the defect it describes: `F2_DIR`
> was a hard-coded absolute path into one machine's session scratchpad, so four of the suite's tests
> could run on exactly one computer, and the skip message told everyone else the fixture's code "is
> not part of this repository", which was untrue. The repair is at `src/leakaudit/fixture_adapter.py`
> and the record of it stays here rather than vanishing with the defect.*

**Known limit of that repair, stated rather than left to be met.** The path resolves relative to the
source tree. From an **installed** copy it resolves to somewhere that does not exist, and the adapter
raises `FixtureUnavailable` naming the path it looked for — which is the correct behaviour for a
stranger who has no fixture, but is not the same thing as the fixture being found.

## Not yet done

- **An install test on a machine other than this one.** This is the one item nothing incidental can
  discharge, and it is the only one that bears on whether a *stranger* can install. It would also
  settle the dependency question below as a by-product.
- A published wheel or index presence. *(Not required by anything: `pip install .` from a public
  clone is an install. It is listed as a convenience that does not exist, never as a gap.)*

**Done since this list was written:** README wiring, which was blocked until the tag landed and is
no longer blocked.

## The dependency floors are untested downward

The floors are `numpy>=1.26`, `pandas>=2.1`, `pyarrow>=14`. The environment every result in this
file was measured in runs **numpy 2.4.2, pandas 3.0.1, pyarrow 23.0.1** — and pandas 3.0 is a major
version break from pandas 2.x. **Nothing here has been run against a 2.x resolution**, so whether a
stranger whose resolver picks pandas 2.1 gets a working package is unknown.

It is recorded as unknown rather than disposed of. Widening or pinning the floors to make the
question go away would replace an untested risk with an untested claim, which is the same defect
with better manners. The second-machine install establishes it; then it can be decided.
