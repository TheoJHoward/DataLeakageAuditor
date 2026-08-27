# INSTALL — `leakaudit`

**Criterion 5 scaffold (B-5). New file; `README.md` is untouched** — `main` is frozen awaiting the
`prereg-v30a` signature, and a pre-tag README edit is a halt. README wiring happens after the tag.

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

The fixture's producing code is committed under `evidence/fixture_spike/f2/`. Note that
`fixture_adapter.F2_DIR` currently points at a **session scratchpad path** rather than that
committed copy — the bytes are identical today, but the path is transient. **A fallback to the
committed copy is a known, unmade one-line change**, recorded here so it is not discovered by a
stranger.

## Not yet done

- README wiring — blocked until the tag lands.
- A published wheel or index presence.
- An install test on a machine other than this one.
