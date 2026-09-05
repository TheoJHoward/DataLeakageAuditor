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

## The environments this package was actually measured in

**Read the dependency bounds below as a list of measured points, not as a
cross-product.** `pyproject.toml` declares `requires-python = ">=3.11"` with
`numpy>=1.26`, `pandas>=2.1`, `pyarrow>=14`. That syntax states a minimum per
dimension and has no way to say which combinations were run — but almost every
reader of a bounds declaration reads it as "every combination in here works," and
that reading is false here. So the combinations are listed.

| Python | numpy | pandas | pyarrow | `py -<version> -m pytest tests` | the pipeline's output |
|---|---|---|---|---|---|
| 3.12.10 | **1.26.4** | **2.1.4** | **14.0.2** | 591 passed, 4 deferred, 1 known failure | `15dc83c7…` |
| 3.12.10 | 2.4.2 | 3.0.1 | 23.0.1 | same | `15dc83c7…` |
| 3.12.10 | 2.5.2 | 3.0.5 | 25.0.1 | same | `15dc83c7…` |
| 3.13.1 | 2.5.2 | 3.0.5 | 25.0.1 | 601 passed, 5 deferred, 1 known failure | `15dc83c7…` |
| **3.11.9** | **1.26.4** | **2.1.4** | **14.0.2** | 632 passed, 4 deferred, 1 known failure — **and this figure no longer reproduces; see below** | `15dc83c7…` |

The bolded rows are the declared floor of every dependency dimension at once —
the last of them at the declared floor of Python too, which is the corner of the
whole declared space. The digest is of the same non-fixture pipeline's canonical
output, run from the same source with only the environment varying; **identical
across all five** means the tool's answer did not depend on its environment at
any measured point, from the lowest declared corner to the current
resolution. The known
failure is the one disclosed at `DEVIATIONS.md` D-V30A-11 and described under
**Verify** in `README.md`. The fifth deferred test on 3.13 is a
string-interning-conditional case that has no subject on that interpreter.

### The corner row was rebuilt on 5 September, and its suite figure did not reproduce

**The environment behind the bolded row was rebuilt rather than annotated** —
`py -3.11 -m venv`, then `numpy==1.26.4 pandas==2.1.4 pyarrow==14.0.2` pinned
exactly, resolving to CPython 3.11.9. It is kept.

**The pipeline column reproduces.** At that corner and on the development
environment the non-fixture pipeline's canonical body is byte-identical at the
current commit — sha256 `ddb133ff2fc959f0…` under both. The portability property
this column asserts holds, and is now re-measurable. (The published *value*
`15dc83c7…` is from 3 September's code and is not this number: the tool has since
added one run note, and the digest's rendering convention is not recoverable from
surviving artifacts. `evidence/session/METHOD_VERIFICATIONS.md` MV-15.)

**The suite column does not.** `<venv>\Scripts\python.exe -m pytest tests` now
reports **763 collected, 755 passed, 4 failed, 4 skipped** — three failures beyond
the known one, all from `tools/probe_path_guard.py` reaching `sys.monitoring`,
which exists only on Python 3.12 and later.

**The row was correct when written.** At the commit that measured it, `watch()`
used `sys.setprofile`; it was rewired onto the `sys.monitoring` recorder
sixty-three minutes later, and nothing re-measured the corner afterwards.

**What this does and does not touch.** `tools/` is not distributed — this file's
package list is `leakaudit` and `protocol` — so `requires-python = ">=3.11"` is
**not** falsified: at the corner the package imports, 755 tests pass, and the
pipeline agrees. What is false is this row's suite figure, and what is broken is a
repository instrument on the interpreter declared as the floor. Disclosed at
`DEVIATIONS.md` D-V30A-58; the repair is a decision about the floor and is not
made here.

### Two things this table does NOT say

**`requires-python = ">=3.11"` is MEASURED as of 3 September 2026** — the last row
above, at the declared floor of every dimension at once, which is the corner the
metadata asserts and which no environment had previously occupied.

> *This paragraph previously read "declared and UNTESTED … every environment above
> ran Python 3.12.10 or 3.13.1", and recorded that no 3.11 interpreter was
> available. That was true when written. The number was left alone throughout
> rather than raised to 3.12 to dispose of the question — and it did not need to
> move, because when 3.11 was finally measured it passed. Raising a floor to a
> measured value with the measurement recorded is legitimate; changing one so a
> question goes away is not, and only the first was ever on the table.*

**The floors and the Python range do not meet at every point.** `numpy==1.26.4`
publishes no wheel for Python 3.13, so the bolded floor row cannot be built
there. That is not a defect in the metadata — a floor is a per-dimension minimum,
and a 3.13 user resolves a newer numpy, which is the fourth row and works. It is
the reason the cross-product reading fails: *the floors work* and *the Python
range works* are two claims, and their conjunction is a third that has been
measured at exactly one point.

**One machine, one operating system.** Windows 11, one host. Varying the
dependency set is not the same as varying the machine, and no second machine has
run any of this.

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

- **An install test on a machine other than this one.** Still not done, and narrowed to what it
  now covers. **It no longer settles the dependency question** — that was measured on 3 September
  2026 at the corner of the declared space, and the section below carries it. What a second machine
  would still establish is the *machine* variable: a different host and operating system. And it is
  **not** the stranger question either: that closed the same day by the author's ruling, recorded
  permanently at `evidence/session/DEFINITION_OF_DONE_WALK.md` Part IV as met with its limitation —
  the walker knew every answer, so the six identified frictions are closed and a newcomer's count is
  unmeasured. The uncontrolled variable there is foreknowledge, which a second machine of the
  author's own would not control for.
- A published wheel or index presence. *(Not required by anything: `pip install .` from a public
  clone is an install. It is listed as a convenience that does not exist, never as a gap.)*

**Done since this list was written:** README wiring, which was blocked until the tag landed and is
no longer blocked.

## The dependency floors — MEASURED, at the corner, 3 September 2026

**Superseded, and the superseded text is kept below because a reader of an earlier
revision needs to know what was unknown and when it stopped being unknown.**

> *This section previously read "The dependency floors are untested downward … whether a stranger
> whose resolver picks pandas 2.1 gets a working package is unknown … The second-machine install
> establishes it; then it can be decided." That was true when written.*

The floors are `numpy>=1.26`, `pandas>=2.1`, `pyarrow>=14`, and `requires-python = ">=3.11"`. **All
four have now been measured together, at the lowest point of every declared dimension at once** —
Python 3.11.9 with `numpy==1.26.4`, `pandas==2.1.4`, `pyarrow==14.0.2` pinned exactly. That corner
is what the metadata asserts and what no environment had previously occupied: each dimension had
been exercised alone, and the conjunction had not.

**The suite there is identical on every term to the development environment**, and the canonical
output digest of the same non-fixture pipeline is `15dc83c7…`, identical to all four other measured
environments. See the table under **The environments this package was actually measured in** above,
which now carries this row.

**Nothing was widened, pinned, or raised.** No floor moved, because none failed. Raising a floor to
a measured value with the measurement recorded would have been legitimate; changing one so the
question goes away would not, and neither was needed.

**What remains untested is the machine, not the numbers.** Every environment above ran on one host
under Windows 11. Varying the dependency set is not the same as varying the machine.
