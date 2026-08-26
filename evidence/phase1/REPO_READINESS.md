# REPO_READINESS — Item F3

**Scope:** environment and repo readiness for Phase 1. **Report only.** Nothing was
created, edited, installed, or removed in either the archive or the pre-registration
repo. No detector code, no availability-model implementation, no `audit()` surface,
no corpus contact. This document is a planning artifact.

**Repo inspected:** `C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01`
**HEAD:** `0ee26c4` · **registration commit:** `fe0d5a5708cfe1f817bd50e12a2cd02c2b4456ac` · **tag:** `prereg-v30` (signed, RSA 4096, fpr `991F 5331 C584 CE5E AF7D 6939 B29C F0E8 4711 9AD7`)
**Date of inspection:** 12 Aug 2026

---

## 0. Method — how the suite was run without writing into the repo

The brief permits running the test suite read-only and requires me to say so if
running it would write into the repo. **It would.** pytest writes
`.pytest_cache/` at rootdir and CPython writes `__pycache__/*.pyc` beside every
imported module. Both already exist in the repo from an earlier run:

```
protocol/__pycache__/                     (2 .pyc)
tests/registration/__pycache__/           (7 .pyc)
tools/__pycache__/                        (1 .pyc)
.pytest_cache/                            (dir, with v/cache/lastfailed, v/cache/nodeids)
```

All three are covered by `.gitignore` (`__pycache__/`, `*.pyc`, `.pytest_cache/`),
so they are invisible to git — but they are still file creations inside the repo,
which the hard boundary forbids. **So I did not run anything in the repo directory.**

Instead I extracted a byte-exact copy with `git archive HEAD | tar -x` into
`…\scratchpad\phase1\repo_copy\` and ran there. I verified the copy is byte-identical
to the working tree: SHA-256 of all 22 tracked files matched pairwise (`OK` on every
row). The working tree is also byte-identical to `HEAD` — `git status --porcelain`
reports zero modified tracked files. **Every result below is therefore a result about
the repo's own bytes, obtained without touching the repo.**

Read-only git commands used: `status`, `log`, `ls-files`, `ls-tree`, `show`,
`cat-file -p`, `check-attr`, `config --get/--list`, `archive`, and one `clone`
(reads the source, writes only into scratchpad). No state-changing git command was run.

---

## (a) Package layout

### What exists now

```
MBO_2025(4mon)+2026-01/
├── .gitattributes              4 lines    tracked
├── .gitignore                  3 lines    tracked
├── PREREG.md                1099 lines    tracked · LOCKED · hashed at tag
├── DESIGN.md                 546 lines    tracked · revisable · hashed at tag
├── HISTORY.md                280 lines    tracked · hashed at tag
├── DEVIATIONS.md               0 lines    tracked · append-only (§11 item 6)
├── PARKING_LOT.md              5 lines    tracked
├── VALIDATED_CONFIG.toml       5 lines    tracked · self-described placeholder
├── README.md                  63 lines    tracked · revisable · carries the hash block
├── registration-commit.txt     1 line     tracked (added AFTER the tag, commit 5842857)
├── registration-commit.txt.ots 10 lines   tracked (added AFTER the tag, commit 0ee26c4)
├── protocol/
│   ├── __init__.py             0 bytes    tracked  ← empty, makes `protocol` a package
│   └── runtime_reference.py  871 lines    tracked · hashed at tag
├── tools/
│   └── check_registration.py 827 lines    tracked · hashed at tag · NO __init__.py
└── tests/
    └── registration/                                 NO __init__.py at either level
        ├── conftest.py                 7 lines
        ├── traces.py                 657 lines
        ├── generate_expected_outputs.py 186 lines
        ├── EXPECTED_OUTPUTS.md       864 lines
        ├── test_checker.py           434 lines
        ├── test_invariants.py        376 lines
        ├── test_traces.py            147 lines
        └── test_expected_outputs.py   15 lines
```

22 tracked files. This matches PREREG §11 item 1 exactly.

**Untracked and never committed in any commit** (verified: `git log --all -- evidence
AVAILABILITY_DECLARATION.md tagmsg.txt` returns empty):

```
?? .claude/                      (launch.json, settings.local.json)
?? AVAILABILITY_DECLARATION.md   42,013 bytes, 11 Aug 2026
?? evidence/                     the fixture_spike tree
?? tagmsg.txt                    source text used to build the tag message
```

> ⚠️ **Correction to the brief.** The task brief states there is "a committed copy at
> `…\MBO_2025(4mon)+2026-01\evidence\fixture_spike\`." The directory exists on disk,
> but it is **not committed** — it is untracked, and `git log --all` shows it has never
> appeared in any commit. Same for `AVAILABILITY_DECLARATION.md`. Whether that is
> intended is outside my scope; I only record that the "committed" characterization
> does not hold at `HEAD` `0ee26c4`.

### Is there a package root? A `pyproject.toml`?

**No, and no.** A filesystem-wide search for `pyproject.toml`, `setup.py`, `setup.cfg`,
`tox.ini`, `pytest.ini`, `*.cfg`, `requirements*.txt`, `*.yml`, `*.yaml` under the repo
returned **zero hits**. There is no distribution metadata of any kind, no console-script
entry point, and nothing installable. The repo is a directory of scripts that run from
the repo root, which is exactly what §11 item 1 asks for and no more.

There is no `leakaudit/` directory. The name appears only as a placeholder in prose
(`PREREG.md:3`, `README.md:3`: "**Working name:** TBD (placeholder: `leakaudit`)") and
as the literal string the checker's not-yet-built stubs report against:

`tools/check_registration.py:715` — `return [Finding(check, "leakaudit/", None, …)]`

### Import conventions, as actually practiced

There is no installed package, so **every entry point bootstraps `sys.path` by hand**.
Three distinct bootstraps exist, and they do not agree with each other:

1. **`tools/check_registration.py:23-25`** — self-anchoring, so the tool runs from anywhere:
   ```python
   ROOT = Path(__file__).resolve().parents[1]
   if str(ROOT) not in sys.path:
       sys.path.insert(0, str(ROOT))
   ```
   `parents[1]` because the file is one level down (`tools/`). It then imports the
   reducer lazily, inside functions, four times (lines 596, 616, 648, 669):
   `import protocol.runtime_reference as rr_module`. Lazy so that an import failure is
   a *check* failure rather than a crash at module load.

2. **`tests/registration/conftest.py`** (whole file, 7 lines):
   ```python
   import sys
   from pathlib import Path

   ROOT = Path(__file__).resolve().parents[2]
   for p in (str(ROOT), str(ROOT / "tests" / "registration")):
       if p not in sys.path:
           sys.path.insert(0, p)
   ```
   `parents[2]` because the file is two levels down. This puts *both* the repo root
   (so `protocol.runtime_reference` resolves) and the test directory itself (so bare
   `from traces import …` resolves) on the path.

3. **`tests/registration/test_checker.py:9-12`** — conftest does *not* add `tools/`,
   so this file adds it itself and imports the checker as a **top-level module**:
   ```python
   ROOT = Path(__file__).resolve().parents[2]
   sys.path.insert(0, str(ROOT / "tools"))

   import check_registration as cr  # noqa: E402
   ```
   Note `check_registration`, not `tools.check_registration` — `tools/` has no
   `__init__.py`, so it is not a package.

4. **`tests/registration/generate_expected_outputs.py:13-16`** repeats bootstrap (2)
   in-file, because it is also runnable standalone
   (`python tests/registration/generate_expected_outputs.py`).

**`protocol/runtime_reference.py` imports nothing local at all** — lines 40-45 are
`from __future__ import annotations`, then `math`, `dataclasses`, `enum`, `typing`.
That is deliberate and stated in its docstring at line 4: *"It is pure protocol tooling:
no I/O, no randomness, no pandas, no detector implementation."*

**Net:** `protocol` is a real (if empty-`__init__`) package; `tools` and `tests` are
loose script directories reached by path injection. It works, it is only 22 files, and
nothing here is broken — but it is a per-file convention, not a project convention.

### What Phase 1 code would need

Phase 1 is defined by **PREREG §10.0** (`PREREG.md:1004-1012`), quoted verbatim:

> `PREREG.md:1004` — `### 10.0 Phase 1 internal ordering, locked`
> `PREREG.md:1007` — `1. Write the throwaway mechanical tests for the §0.3 verification list.`
> `PREREG.md:1008` — `2. Verify Claims A–C and the comparator cases.`
> `PREREG.md:1010` — `4. Freeze the final comparator, permitted promotion sets, terminal-decision policy, compatibility-threshold form, and reach definitions.`
> `PREREG.md:1011` — `5. Generate and hash the evaluation-generator snapshot.`
> `PREREG.md:1012` — `6. Generate and hash the conformance suite.`

So the Phase 1 code is: **throwaway mechanical test scripts** (8 cases minimum,
`PREREG.md:125-132`), a **result-recording path**, an **evaluation generator** plus its
**parameter distributions**, a **conformance-suite generator**, and **hashing/manifest
tooling** for both. It is explicitly *not* detector code — `PREREG.md:123` places the
verification "**before L3.1 and L2a are built**."

Those artifacts have their own registration requirement:

> `PREREG.md:1054` — `7. Evaluation generator snapshot, conformance suite, adjudication rubrics, parameter distributions, beacon records, and generated manifests frozen in their own files with their own hashes.`

**What the current layout does not provide for that:**

- **No location convention for throwaway code.** §10.0 step 1 calls the tests
  "throwaway", and they must be distinguishable from the registered suite. Putting them
  under `tests/registration/` would be wrong twice: they are not registration tests, and
  `check_structure` globs that directory (`tools/check_registration.py:198` —
  `tests_dir.glob("test_*.py")`) so it would silently start counting them toward the
  §6.6.1 suite's existence proof. There is no `tests/phase1/`, no `scratch/`, no
  `experiments/`.
- **No location convention for frozen snapshots + their hash files.** §11 item 7 wants
  "their own files with their own hashes". There is no `snapshots/`, `benchmarks/`, or
  `manifests/` directory, and no manifest format precedent in the repo. (One precedent
  exists *outside* the repo, in the untracked evidence tree:
  `evidence\fixture_spike\f3\fixture_manifest_DRAFT.json` and the `.sha256` sidecars
  under `evidence\fixture_spike\f2\out\`. Not registered; treat as prior art, not as a
  standard.)
- **The path-injection convention does not scale past three consumers.** Each new entry
  point currently reimplements `parents[N]`. A fourth and fifth bootstrap is where the
  off-by-one lands.
- **`protocol/__init__.py` is empty**, so there is no curated public surface. Phase 1
  code wanting the reducers must spell `from protocol.runtime_reference import …`. That
  is fine, but note the reducer exposes 40 public names including leaked stdlib
  re-exports (`Enum`, `Mapping`, `Iterable`, `math`, `dataclass`, `annotations`) —
  `import *` would be a trap.

### The layout question PREREG does not answer, and DESIGN answers differently

`PREREG.md:1048` pins the reducer's path verbatim as **`protocol/runtime_reference.py`**
— top-level `protocol/`. `check_structure` enforces it (`REQUIRED_PATHS`,
`tools/check_registration.py:176-181`). But DESIGN.md illustrates the eventual import as:

> `DESIGN.md:411` — `from leakaudit.protocol import (`

with `DESIGN.md:20` showing `leakaudit.audit(...)`, `DESIGN.md:418` — "Eleven files,
one per detector", and `DESIGN.md:42` naming pip extras
`leakaudit[static]`, `leakaudit[deepchecks]`.

**These are two different layouts** (top-level `protocol/` vs. `leakaudit/protocol/`).
DESIGN.md also imports `resolve_tier` from that path, and I verified **`resolve_tier`
does not exist in `protocol/runtime_reference.py`** (`hasattr(rr, "resolve_tier")` →
`False`; the module exposes `resolve_schedule_state`, `resolve_evidence_outcome`,
`resolve_state_pair`, `resolve_reach_basis`, but no tier resolver).

I am **not** asserting a conflict requiring an amendment. DESIGN.md is revisable
(`README.md:23`) and its code blocks are illustrative; `DESIGN.md:7` states the file
"restates no measurement semantics." Whether `DESIGN.md:411` is a forward-looking sketch
or a layout commitment is **genuinely ambiguous and I did not resolve it**. What is *not*
ambiguous: `PREREG.md:1048` is locked, and moving `protocol/runtime_reference.py` would
break §11 item 1 and `check_structure`. **The reducer stays where it is.**

---

## (b) Test harness

### How it runs

- **No pytest config anywhere.** No `pytest.ini`, `pyproject.toml`, `setup.cfg`,
  `tox.ini`. No markers, no options, no `testpaths`, no `filterwarnings`, no
  `--strict-markers`.
- **rootdir is inferred, not configured.** With no config file present, pytest fell back
  to the invocation directory. Header from the run:
  `rootdir: …\scratchpad\phase1\repo_copy`.
- **`conftest.py` is the entire harness** — 7 lines, `sys.path` only. No fixtures, no
  hooks, no plugins, no collection customization.
- **No `__init__.py` in `tests/` or `tests/registration/`**, so pytest uses rootdir-based
  `prepend` import mode and inserts the test directory on `sys.path`. Combined with
  conftest doing the same explicitly, bare `from traces import …` works.

### Exact invocation

From `README.md:47-50`, verbatim:

```
python -m pytest tests/registration
python tools/check_registration.py --stage prereg
```

### Does it pass today?

**Yes — 137 passed, 0 failed, 0 skipped, 0 xfail, in 0.66 s.**

```
platform win32 -- Python 3.12.10, pytest-9.1.1, pluggy-1.6.0
plugins: anyio-4.12.1, dash-4.0.0
collected 137 items
137 passed in 0.66s          exit code 0
```

Per file:

| File | Tests |
|---|---|
| `tests/registration/test_checker.py` | 52 |
| `tests/registration/test_traces.py` | 51 |
| `tests/registration/test_invariants.py` | 33 |
| `tests/registration/test_expected_outputs.py` | 1 |
| **Total** | **137** |

Also verified **cwd-independent**: invoking with an absolute path from a different
working directory gave the same 137 passed. That is `conftest.py`'s self-anchoring
doing its job.

The checker, all three stages, run against the same bytes:

| Stage | Result | Exit |
|---|---|---|
| `--stage prereg` | **PASS** — 13/13 checks pass, 8 deferred and named | **0** |
| `--stage implementation` | FAIL — 5 checks, each "does not exist yet", 16 deferred and named | 1 |
| `--stage release` | FAIL — 3 checks, each "does not exist yet", 18 deferred and named | 1 |

`--stage prereg` also emits two exemption notes, printed rather than hidden:

```
[PASS] banned_vocabulary
    note: PREREG.md:414: EXEMPTION APPLIED id=REG15 reason='the registry entry must name the parked mechanism to state what a user does not get'
    note: PREREG.md:1097: EXEMPTION APPLIED id=PARK9 reason='the parking-lot pointer must name the parked mechanism to state what an amendment would restore'
```

**The tag gate holds.** `--stage prereg` exit 0 and the suite green, which is what
`PREREG.md:647` defines as green and, in its own words, "nothing more."

### What Phase 1 code would need

- **No `tests/phase1/` and no way to add one safely.** As noted in (a),
  `check_structure` globs `tests/registration/test_*.py`. A sibling directory
  `tests/phase1/` is untouched by that glob and is the clean answer — but it does not
  exist and no conftest covers it. A `tests/phase1/conftest.py` would need
  `parents[2]` (same depth), which is a copy-paste of the existing bootstrap.
- **Selective invocation is un-namable.** With no markers and no `testpaths`, there is
  no way to say "run only the registration suite" other than by path. Once a second
  suite exists, `python -m pytest` bare would run both, and the *registration* suite's
  greenness — the thing the tag gate cites — would be entangled with throwaway Phase 1
  tests that are *expected* to fail while a claim is under investigation. Nothing today
  separates them.
- **Plugin autoload is uncontrolled.** `anyio-4.12.1` and `dash-4.0.0` loaded into the
  session purely because they are installed in the user's global interpreter. Neither
  is used by this project. They are benign today; they are also an unpinned surface that
  could change collection behavior on any unrelated `pip install`. There is no
  `-p no:cacheprovider`, no `PYTEST_DISABLE_PLUGIN_AUTOLOAD`, no isolation.
- **No environment record.** §11 item 7 wants generated artifacts hashed. Reproducing a
  Phase 1 measurement also needs the interpreter and library versions recorded. There is
  no such file in the repo. (Prior art again outside it:
  `evidence\fixture_spike\c5\env_records.md`.)

---

## (c) CI hooks for the existing checker

### What exists

**Nothing.** Verified:

- `.github/` — **does not exist** (`ls: cannot access '.github': No such file or directory`).
- No `.gitlab-ci.yml`, no `azure-pipelines.yml`, no `Jenkinsfile`, no `*.yml`/`*.yaml`
  anywhere under the repo.
- `.git/hooks/` contains **only `*.sample` files** — no active hook.
- No `Makefile`, no `noxfile.py`, no task runner.

So every "the CI script does X" clause in PREREG is, today, satisfied by
`tools/check_registration.py` being **run by hand**. That is not a defect at
registration — §11 item 1 requires the checker to exist in the first commit, not a CI
service — but it means there is no automation enforcing it.

### What `check_registration.py`'s argparse exposes

`tools/check_registration.py:815-823`:

```python
def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", choices=("prereg", "implementation", "release"),
                        required=True)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    return run_stage(args.stage, args.root)
```

Two flags, no subcommands:

| Flag | Type | Required | Default | Notes |
|---|---|---|---|---|
| `--stage` | choice of `prereg` \| `implementation` \| `release` | **yes** | — | no default: you cannot run it without naming a stage |
| `--root` | `Path` | no | `Path(__file__).resolve().parents[1]` | lets CI point at a checkout dir |

Exit contract (`run_stage`, lines 789-812): `0` on PASS, `1` on FAIL. Findings print
per check; `is_note=True` findings print but never fail (line 796:
`failures = [f for f in findings if not f.is_note]`). Stdout is forced to UTF-8 —
which matters on Windows, since the notes contain `§`.

The 21 checks are wired in the `CHECKS` table at lines 763-786: 13 `prereg`,
5 `implementation`, 3 `release`.

### The governing staged-check clause, verbatim

> `PREREG.md:647` — **The checker runs in stages, and a deferred check is named rather than skipped.** Two of the checks below cannot pass before detector code exists — shipping defaults against the frozen `[validated.runtime]`, and the `ties` comparator against the shipped mask — while §11 requires the checker in the first commit. So it takes `--stage prereg | implementation | release`, **every stage prints the checks it defers and the stage that owns them**, and an omitted branch is a failure rather than a pass. **The tag gate is `--stage prereg` exit 0**, which is what "the checker is green" means at registration time and nothing more.

And the clause listing what the CI script must additionally check:

> `PREREG.md:649` — A CI script diffs shipping defaults against the frozen section, and additionally checks: that stated totals match their addends; that the `ties` comparator is consistent across §2.3, §4.3, and the shipped mask; that §4.3's inequalities match the shipped rule; and **that each §0.1 lock-table row's target section contains that row's key phrase.**

Supporting clauses:

> `PREREG.md:645` — **The script also enforces the single-source rule and certifies deletions.** It fails if any measurement formula, state enumeration, or denominator definition appears in `DESIGN.md`; and a deletion is not complete until the symbol's inbound normative reference set is empty, with the CI artifact recording the removed symbols, the removed requirement IDs, zero remaining references, and negative tests showing the old configuration is rejected. The banned-vocabulary scan is a smoke alarm behind that, not the proof.

> `PREREG.md:637` — **Subtractive rounds get a banned-vocabulary check.** When a version deletes a mechanism, its distinctive terms are added to a banned list, and the CI script fails if any appears outside §0.4, the `DESIGN.md` lessons, or `PARKING_LOT.md`.

> `PREREG.md:1000` — **13–20 working weekends** (minimum 1+2+2+1+2+2+2+1 = 13; maximum 2+3+3+1+3+3+3+2 = 20). Computed by the CI script of §6.8, not by hand.

### What invocation CI would use

Reading `PREREG.md:647` literally: the gate that CI must enforce today is
`--stage prereg` exit 0, alongside the suite. That is exactly the `README.md:47-50`
pair. A CI job that reproduced the current, hand-run gate would be:

```
python -m pytest tests/registration        # must be green
python tools/check_registration.py --stage prereg   # must exit 0
```

`--stage implementation` and `--stage release` **must not** be added as required CI
jobs yet: `PREREG.md:647` states an omitted branch is "a failure rather than a pass",
and the checker honors that by returning exit 1 with explicit
`"does not exist yet"` findings (`_artifact_absent`, lines 714-717). Wiring them as
required now would make CI permanently red for a correct repo. They become gates when
Phase 1 / release produce the artifacts they name — which is precisely what the
staged design exists to express.

**One thing I could not determine and am not inferring:** whether `PREREG.md:649`'s
"CI script" is meant to *be* `tools/check_registration.py` or a separate script. The
checker's own docstring (line 1) says "Registration checker (PREREG §6.8), staged" and
it already implements the lock-table key-phrase check (`check_lock_table`), the
phase-arithmetic check (`check_phase_arithmetic`), the single-source check, and the
banned-vocabulary scan — i.e. most of §6.8's list. But §12's cost script
(`PREREG.md:1070`, "The CI cost script computes the total including refinement under
the frozen cap") appears in the CHECKS table only as a stub named `cost_script_total`
that reports the script does not exist. So at least one *separate* script is implied.
**Whether there is one CI script or several is not stated in a clause I found.**

---

## (d) Line-ending / byte-exactness protections

### `.gitattributes` — full contents (4 lines, tracked, present at the registration commit)

```
# Registration integrity: every file is stored and checked out byte-exact.
# The SHA-256 hashes in README.md and the tag message are of these bytes;
# EOL conversion on checkout would silently break hash verification.
* -text
```

Confirmed present at `fe0d5a5` (`git show fe0d5a5:.gitattributes` returns the identical
four lines; `git ls-tree --name-only fe0d5a5` lists `.gitattributes`). So the protection
was in force *for* the registration commit, not added after.

### `core.autocrlf` — and why the answer is layered

| Scope | Value | Travels with a clone? |
|---|---|---|
| System (`C:/Program Files/Git/etc/gitconfig`) | `core.autocrlf=true` | n/a — machine-local, and **hostile** to byte-exactness |
| Repo-local (`.git/config`) | `core.autocrlf=false` | **No** |
| `.gitattributes` `* -text` | disables all conversion for every path | **Yes** |

The system default on this machine is the dangerous one. Two things override it, and
only one of them is inside the repository.

### Verification that the protection actually holds

`git check-attr text eol` over all 22 tracked files: **every file reports
`text: unset`, `eol: unspecified`** — i.e. no conversion on any path.

Byte census of the blobs and the working tree:

| | Result |
|---|---|
| CRLF pairs in any tracked blob at `prereg-v30` | **0** |
| LF-only line endings in blobs | all (e.g. `PREREG.md` 1099, `runtime_reference.py` 871) |
| CRLF pairs in the working tree | **0** |
| Working tree byte-identical to blob | **yes**, all files |

*(An earlier `grep -c $'\r'` pass in my session reported CR on every line. That was a
tooling artifact of the shell, not a property of the files; the Python byte census above
supersedes it and I discarded the grep result.)*

### Hash chain — verified end to end

`git show prereg-v30:<file> | sha256sum`, compared against both the tag message and
`README.md:31-35`. All five match:

```
f0a8f00164c217a40f87a4dc9fee6193ee7e4e125c68e3ecc84863fd6e2c7cc6  PREREG.md
039240e3c57497cc8eda65fbfcdc3d1120f1d7a12ad0f41b48d71c98ef063428  DESIGN.md
e8cf5bbbc42762838318e2ffc8cf85b6f44ed701c3ee88f8e93a6e734fc43e0d  HISTORY.md
72ffc7c69899844644ff79a9f6a12b083bbbe2c1160aca8d90dbe9415a0322e2  tools/check_registration.py
215194c15ab89f208198ce6bc3f8dd726d652fa6bee3d7bd868d1234c9bec31a  protocol/runtime_reference.py
```

Note `PREREG.md:1050` (§11 item 3) requires SHA-256 of **three** files
(`PREREG.md`, `DESIGN.md`, `HISTORY.md`). The tag and README publish **five**, adding
the two tooling files. A superset, so no violation — but it raises the bar on those two,
which matters for the gap list below.

### The adversarial test

The real question is not "is it correct here" but "does it survive a stranger's clone on
a machine where `autocrlf=true`". I forced exactly that:

```
git -c core.autocrlf=true clone <repo> …/clone_test
```

Result — the clone's own `core.autocrlf` is `true`, and:

```
files with CRLF after autocrlf=true clone: NONE
f0a8f00164c217a40f87a4dc9fee6193ee7e4e125c68e3ecc84863fd6e2c7cc6 PREREG.md
039240e3c57497cc8eda65fbfcdc3d1120f1d7a12ad0f41b48d71c98ef063428 DESIGN.md
e8cf5bbbc42762838318e2ffc8cf85b6f44ed701c3ee88f8e93a6e734fc43e0d HISTORY.md
72ffc7c69899844644ff79a9f6a12b083bbbe2c1160aca8d90dbe9415a0322e2 tools/check_registration.py
215194c15ab89f208198ce6bc3f8dd726d652fa6bee3d7bd868d1234c9bec31a protocol/runtime_reference.py
```

**Verdict: the protections hold, and they hold for the right reason.** `.gitattributes`
is what does the work — it is tracked, it was in the registration commit, `*` covers
files that do not exist yet, and it beats `core.autocrlf` under git's own precedence.
The repo-local `core.autocrlf=false` is a redundant second belt that does *not* travel;
if it were the only defense, the clone above would have produced five hash mismatches.
It did not.

Two lesser observations, neither a hash-chain risk:

- `.git/config` has `core.ignorecase=true` and `core.symlinks=false` (Windows
  defaults). Case-only filename collisions would be invisible here and visible on a
  Linux CI runner. No such collision exists among the 22 files.
- `core.filemode=false`. Mode bits are not part of the published SHA-256s, so this is
  immaterial to the hash chain.

---

## (e) Dependencies

### What the code imports

Exhaustive scan of `^\s*(import|from)\s` across all tracked `.py`:

| Module | Where | Kind |
|---|---|---|
| `__future__` | `runtime_reference.py:40`, `check_registration.py:14`, `traces.py:20`, `generate_expected_outputs.py:8` | stdlib |
| `math` | `runtime_reference.py:42` | stdlib |
| `dataclasses` | `runtime_reference.py:43`, `traces.py:22`, `check_registration.py:20` | stdlib |
| `enum` | `runtime_reference.py:44` | stdlib |
| `typing` | `runtime_reference.py:45` | stdlib |
| `argparse` | `check_registration.py:16` | stdlib |
| `re` | `check_registration.py:17` | stdlib |
| `sys` | `check_registration.py:18`, `conftest.py:1`, and 2 more | stdlib |
| **`tomllib`** | `check_registration.py:19` | **stdlib, Python ≥ 3.11 only** |
| `pathlib` | 4 files | stdlib |
| `inspect` | `test_invariants.py:3` | stdlib |
| **`pytest`** | `test_checker.py:7`, `test_invariants.py:5`, `test_traces.py:4` | **third party — the only one** |

Plus first-party: `protocol.runtime_reference`, `traces`, `check_registration`,
`generate_expected_outputs`.

**The entire third-party dependency footprint is `pytest`, and only in the test suite.**
Neither `protocol/runtime_reference.py` nor `tools/check_registration.py` imports
anything outside the standard library. `runtime_reference.py:4` states this as a design
property: *"no I/O, no randomness, no pandas, no detector implementation."* I confirmed
it by scan, not by trusting the docstring.

### What is installed (import-probe only — nothing installed, nothing upgraded)

Interpreter: **Python 3.12.10**, `C:\Users\ttbea\AppData\Local\Programs\Python\Python312\python.exe`

| Package | Status | Version |
|---|---|---|
| `pytest` | installed | 9.1.1 |
| `tomllib` | installed | stdlib (3.12) |
| `numpy` | installed | 2.4.2 |
| `pandas` | installed | 3.0.1 |
| `scipy` | installed | 1.17.1 |
| `sklearn` | installed | 1.8.0 |
| `packaging` | installed | 26.0 |
| `tomli` | **not installed** | — (not needed on ≥3.11) |
| `hypothesis` | **not installed** | — |

pytest also autoloads `anyio-4.12.1` and `dash-4.0.0` from the global environment.
Neither is a project dependency.

### Pins

**There is no pin file of any kind.** No `requirements.txt`, no `requirements-dev.txt`,
no `constraints.txt`, no `pyproject.toml` `[project.dependencies]`, no lockfile, no
`environment.yml`. Nothing declares a Python floor either.

**The effective Python floor is 3.11**, forced by `import tomllib`
(`check_registration.py:19`) — `tomllib` entered the stdlib in 3.11. I verified 3.12.10
works; **I did not test 3.11, 3.10, or any other version**, so 3.11 is a floor derived
from a known stdlib fact, not a tested minimum, and there may be other version-gated
syntax I did not audit.

**There is no virtual environment.** No `.venv/`, no `venv/`. Everything runs against
the user's global interpreter, which is the same interpreter carrying pandas 3.0.1,
numpy 2.4.2 and scikit-learn 1.8.0 for unrelated work in this Desktop tree.

### What Phase 1 will need

Phase 1 does need real numerics. `PREREG.md:125-132` lists eight verification cases —
mixed frames, forward-filled joins, dtype promotion to complex, row-dropping pipelines —
which are dataframe work. numpy/pandas/scipy/sklearn are present but **unpinned and
shared with unrelated projects**. A Phase 1 measurement recorded against
"pandas" with no version is not reproducible, and `PREREG.md:1054` requires the
generated artifacts to be "frozen in their own files with their own hashes" — a hash of
data generated by an unrecorded library version proves the file did not change, not
that it can be regenerated.

---

## GAP LIST

Each gap: **what is missing → why Phase 1 needs it → what would create it → does creating
it touch a locked/registered file?**

The registered-document status I am working from, so the classification is auditable:

| File | Status | Source |
|---|---|---|
| `PREREG.md` | **LOCKED, never changes.** Change = class C amendment + new tag | `README.md:22-23`; `PREREG.md:1048` "(locked, unchanged)" |
| `DESIGN.md` | **Revisable** | `README.md:23` |
| `README.md` | **Revisable** | `README.md:23` |
| `HISTORY.md` | Hashed at tag; **revisability not stated** in `README.md:22-26` | *ambiguous — see §Unresolved* |
| `DEVIATIONS.md` | **Append-only**, and Phase 1 is required to append | `PREREG.md:1053`; `PREREG.md:1009` |
| `VALIDATED_CONFIG.toml` | Registered **placeholder**, meant to be filled per phase | `PREREG.md:1048`; file header line 1 |
| `PARKING_LOT.md` | Registered; §13.9 entry only | `PREREG.md:1048` |
| `tools/check_registration.py` | Registered **and hashed at tag**; designed to grow stage checks | `PREREG.md:647`; tag message |
| `protocol/runtime_reference.py` | Registered **and hashed at tag**; "at minimum" list, growth anticipated | `PREREG.md:1048`; module docstring lines 29-32 |
| `tests/registration/*` | Registered (in commit `fe0d5a5`), not individually hashed | `PREREG.md:1048` |

---

### GROUP 1 — Gaps fillable WITHOUT touching any registered document

These are all **new files in new locations**. None edits a file that exists at
`fe0d5a5`. None affects the tag, the five published hashes, or `--stage prereg`.

| # | What is missing | Why Phase 1 needs it | What would create it | Touches a registered file? |
|---|---|---|---|---|
| **G1** | A directory for the §10.0 step 1 **throwaway mechanical tests**, separate from `tests/registration/` | `PREREG.md:1007` requires them; putting them in `tests/registration/` would feed `check_structure`'s `test_*.py` glob (`check_registration.py:198`) and let throwaway files stand in as evidence the §6.6.1 suite exists | New `tests/phase1/` (or similar) + its own `conftest.py` replicating the `parents[2]` bootstrap | **No** — new path, invisible to `REQUIRED_PATHS` and to the glob |
| **G2** | **Suite separation** — a marker, `testpaths`, or a documented two-command split so the registration suite's greenness is not entangled with Phase 1 tests that are expected to fail mid-investigation | The tag gate cites suite greenness (`PREREG.md:647`); a bare `python -m pytest` after G1 would mix them | A `pyproject.toml` `[tool.pytest.ini_options]`, or `pytest.ini`, or a documented convention | **No** — new file. ⚠️ **Caveat:** creating `pyproject.toml` changes pytest's inferred rootdir anchor. Same directory, so no behavioral change expected, but this should be confirmed by re-running the 137 tests before and after, not assumed |
| **G3** | **Dependency pins + a declared Python floor** | Phase 1 measurements on pandas/numpy frames must be reproducible; §11 item 7 hashes artifacts, which proves immutability but not regenerability | `requirements-phase1.txt` (or `pyproject.toml` `[project]` with `requires-python = ">=3.11"`) | **No** — new file |
| **G4** | **A virtual environment**, isolated from the global interpreter shared with unrelated Desktop work | Prevents an unrelated `pip install` from silently changing a Phase 1 result or pytest's plugin set (`anyio`, `dash` autoload today) | `python -m venv .venv` + a `.gitignore` line. ⚠️ the `.gitignore` line is a Group-2-adjacent edit (see G12) | **No** for the venv itself (gitignorable); the `.gitignore` line is a registered-file edit |
| **G5** | **An environment record** — interpreter, OS, library versions, captured at measurement time | Reproducing a Phase 1 number needs the environment, not just the artifact hash. Prior art exists outside the repo at `evidence\fixture_spike\c5\env_records.md` | New file under the Phase 1 artifact directory | **No** — new path |
| **G6** | **A location + format convention for §11 item 7 artifacts** (evaluation generator snapshot, conformance suite, parameter distributions, adjudication rubrics, beacon records, generated manifests) with their own hash files | `PREREG.md:1054` verbatim requires them "frozen in their own files with their own hashes"; there is no `snapshots/`, `manifests/`, or precedent format in the repo | New directories + a manifest format decision. Prior art outside the repo: `evidence\fixture_spike\f3\fixture_manifest_DRAFT.json`, `.sha256` sidecars in `evidence\fixture_spike\f2\out\` | **No** — new paths |
| **G7** | **Hashing / manifest tooling** to produce and re-verify G6's hashes | §10.0 steps 5 and 6 both say "**Generate and hash**"; there is no hashing utility in the repo | New script, e.g. `tools/hash_manifest.py` | **No** — new file in `tools/`. `tools/` is not a package and has no `__init__.py`, so a new module there imports nothing and is imported by nothing |
| **G8** | **CI configuration** running the two gate commands | `PREREG.md:647` defines the gate; today it is enforced only by hand. No `.github/`, no hooks | New `.github/workflows/*.yml` running `python -m pytest tests/registration` and `python tools/check_registration.py --stage prereg`. Must **not** make `--stage implementation`/`release` required yet — `_artifact_absent` correctly returns exit 1 today | **No** — new path |
| **G9** | **A shared path-bootstrap** (or a decision to keep duplicating it) | Four hand-written `sys.path` bootstraps with two different `parents[N]` values already exist; each new Phase 1 entry point adds a fifth | Either a `pyproject.toml` making the repo installable in editable mode, or an accepted convention documented once | **No** for a new `pyproject.toml`. ⚠️ **But see C1** — an installable package raises the `leakaudit/` layout question, which is not mine to settle |

---

### GROUP 2 — Gaps that CANNOT be filled without touching a registered document

| # | What is missing | Why Phase 1 needs it | What would create it | Which registered file, and its status |
|---|---|---|---|---|
| **C1** | **The implementation-stage checks are stubs.** All five return `_artifact_absent(...)` (`check_registration.py:714-717`, wired at 778-782). When Phase 1 freezes the comparator and permitted promotion sets (§10.0 step 4), `shipping_defaults_vs_validated_runtime`, `ties_comparator_vs_shipped_mask`, `l31b_inequalities_vs_shipped_rule`, `deleted_config_fields_rejected` must become real checks | `PREREG.md:649` requires the CI script to diff shipping defaults against the frozen section and check comparator consistency; §6.8's design (`PREREG.md:647`) explicitly anticipates this — the stubs exist *to be replaced* | Editing `tools/check_registration.py` | **`tools/check_registration.py`** — registered at `fe0d5a5` **and SHA-256-published in both the tag message and `README.md:34`**. `README.md:23` names only `DESIGN.md` and the README as revisable; it does **not** say this file is. Growth is clearly anticipated by `PREREG.md:647`, but the README's own revisability sentence does not cover it |
| **C2** | **`DEVIATIONS.md` is empty and Phase 1 must write to it** | `PREREG.md:1009` — "A class A branch or class B parameter is applied and recorded in `DEVIATIONS.md` and the frozen configuration" | Appending entries | **`DEVIATIONS.md`** — registered, but `PREREG.md:1053` makes it **append-only**, and §10.0 step 3 *requires* the append. Writing to it is mandated, not a violation. **Constraint:** append only, never edit or reorder |
| **C3** | **`VALIDATED_CONFIG.toml` carries no values** (four empty tables) | §10.0 step 4 freezes the comparator, permitted promotion sets, terminal-decision policy, compatibility-threshold form and reach definitions; `PREREG.md:635` requires each to be "serialized into, and hashed with, the applicable `VALIDATED_CONFIG` section" | Populating `[validated.runtime]` etc. | **`VALIDATED_CONFIG.toml`** — registered, but its own first line reads "Placeholder — PREREG.md §6.8 / §11.1. Values are frozen per phase; no value here yet." Filling it is the designed lifecycle. `check_config_schema` requires all four tables to remain present — **do not remove a table**, only add keys |
| **C4** | **The reducer does not compute §7.5 per-strategy diagnostics or §6.11 compatibility-escalation arithmetic** | `runtime_reference.py:29-32`: "Deliberately outside this reference reducer … Per §6.6.1 a runtime number is publishable only once the reducer computes it, so neither may be published until this module grows them." Phase 1 step 4 freezes the compatibility-threshold form, whose arithmetic (`f ≥ m` **and** `f/n > q`, `PREREG.md:696`) lands here | Editing `protocol/runtime_reference.py` | **`protocol/runtime_reference.py`** — registered **and SHA-256-published at the tag** (`README.md:35`). `PREREG.md:1048` says "**at minimum**" those seven functions, so growth is licensed by the locked text; the published hash still moves |
| **C5** | **The README's hash block does not say which of the five files are allowed to move** | Once C1 or C4 lands, `HEAD` hashes for `tools/check_registration.py` and `protocol/runtime_reference.py` will differ from the tag's, and a reader has no in-repo statement that this is legitimate for those two | Editing `README.md:22-26` to extend the revisability sentence, or adding a note under the hash block | **`README.md`** — explicitly **revisable** (`README.md:23`, "this README"). This is the cheapest Group-2 item and the one that keeps C1/C4 legible to an outside auditor |
| **C6** | **`DESIGN.md` illustrates a `leakaudit.protocol` import path** (`DESIGN.md:411`) that does not exist, importing a `resolve_tier` that does not exist | If Phase 1 tooling is written against `DESIGN.md:411`, it will not import. `PREREG.md:1048` pins `protocol/runtime_reference.py` and `check_structure` enforces it | Either revise `DESIGN.md` to match the registered layout, or leave it as a forward sketch and document the distinction | **`DESIGN.md`** — explicitly **revisable** (`README.md:23`). ⚠️ **Constraint:** `check_single_source` fails if any measurement formula, state enumeration, or denominator definition appears in `DESIGN.md` (`PREREG.md:645`, `DESIGN.md:7`). Any edit must re-run `--stage prereg` |
| **C7** | **No cost script exists**, and `cost_script_total` is a stub (`check_registration.py:741-743`, wired at 782) | `PREREG.md:1000` — "Computed by the CI script of §6.8, not by hand"; `PREREG.md:1070` — "**The CI cost script computes the total including refinement under the frozen cap**, and the README quotes the script" | A new script (Group 1) **plus** rewiring `check_cost_script` (Group 2) **plus** a README edit to quote its output | Script itself: **no**. Rewiring: **`tools/check_registration.py`** (see C1). Quoting the total: **`README.md`** (revisable) |
| **C8** | **`.gitignore` does not cover the Phase 1 working tree** — no `.venv/`, and the currently-untracked `.claude/`, `evidence/`, `AVAILABILITY_DECLARATION.md`, `tagmsg.txt` show as `??` on every `git status` | Noise in `git status` is how an accidental commit of scratch material gets missed in a registration repo | Editing `.gitignore` | **`.gitignore`** — registered at `fe0d5a5` (it is in `git ls-tree fe0d5a5`), **not** in the published hash list, and not named in any §11 clause. Lowest-consequence Group-2 edit, but it is still a file that existed at the registration commit |

---

### Summary of the split

- **Group 1 (9 gaps)** — every one is a *new file in a new path*. None edits anything
  that existed at `fe0d5a5`. `--stage prereg` and the five published hashes are
  untouched. **These can proceed on repo-readiness grounds alone.**
- **Group 2 (8 gaps)** — split three ways by consequence:
  - **Explicitly licensed lifecycle** (C2 `DEVIATIONS.md` append-only, C3
    `VALIDATED_CONFIG.toml` placeholder-fill): PREREG *requires* Phase 1 to write these.
    Not a hazard; a schedule.
  - **Revisable files** (C5, C6, and the README half of C7): `README.md:23` licenses
    both `DESIGN.md` and `README.md`. C6 must be re-checked against `check_single_source`.
  - **Hash-published tooling** (C1, C4, the rewiring half of C7): editing
    `tools/check_registration.py` or `protocol/runtime_reference.py` moves a SHA-256
    that appears in the **signed tag message**. The tag never moves and remains
    verifiable, and `PREREG.md:647` / `PREREG.md:1048` ("at minimum") anticipate exactly
    this growth — but `README.md:22-26` currently names only `DESIGN.md` and the README
    as revisable. **C5 is the prerequisite that makes C1 and C4 legible to an auditor.**
- **`PREREG.md` is not in any gap above.** No Phase 1 repo-readiness item requires
  editing it. The one thing that would — a class C change discovered during §0.3
  verification — is `PREREG.md:1009`'s own branch and routes through an amended
  registration, not through repo setup.

---

## Unresolved / not verified — labelled, not inferred

1. **Is `HISTORY.md` revisable?** `README.md:22-23` classifies `PREREG.md` (locked) and
   `DESIGN.md` + README (revisable) and says nothing about `HISTORY.md`, which is hashed
   alongside them and required by `PREREG.md:1050`. `PREREG.md:0.4` says the version
   ledger lives there, and `check_registration.py:11` treats it as out of scan scope
   because "it declares itself non-normative." **Genuinely ambiguous. Not resolved.**
2. **One CI script or several?** `PREREG.md:649` says "A CI script"; `PREREG.md:1070`
   says "The CI cost script". `tools/check_registration.py` implements most of §6.8's
   list but carries the cost check only as a stub. **No clause I found states the
   intended decomposition.**
3. **Is `DESIGN.md:411`'s `leakaudit.protocol` a layout commitment or a sketch?** See
   (a). `PREREG.md:1048` pins the current path. **Not resolved.**
4. **Python floor.** 3.11 is derived from `tomllib` being stdlib-since-3.11, not from
   testing. I tested only 3.12.10. Other version-gated constructs were not audited.
5. **Whether `evidence/` and `AVAILABILITY_DECLARATION.md` are *meant* to be committed.**
   I verified they are not, in any commit. I make no claim about intent.
6. **`--stage implementation` / `--stage release` failure text.** All eight report
   `"does not exist yet"` against the path `leakaudit/` — a placeholder name
   (`PREREG.md:3`: "Working name: TBD"). Whether the eventual package is named
   `leakaudit` is **not settled** by any clause I read.
7. **G2's rootdir caveat** (creating `pyproject.toml` changes pytest's rootdir anchor)
   is reasoning from pytest's documented inference order, **not** something I tested by
   creating the file — which the boundaries forbid.

---

## Bottom line

The repo is **exactly what `PREREG.md` §11 item 1 asks for and nothing more**: 22 files,
no packaging, no CI, no pins, stdlib-only tooling, `pytest` in the tests alone. The tag
gate is green today — **137 tests pass, `--stage prereg` exits 0** — and byte-exactness
is genuinely protected, verified against a hostile `autocrlf=true` clone rather than
assumed from the config.

What is missing is not correctness; it is **project infrastructure that was deliberately
not built yet**. Nine of the seventeen gaps are new files in new paths and touch nothing
registered. Of the eight that do touch registered files, five are the designed lifecycle
(`DEVIATIONS.md` append, `VALIDATED_CONFIG.toml` fill, revisable-doc edits) and three
move a SHA-256 published in the signed tag — anticipated by `PREREG.md:647` and by
§11's "at minimum", but currently unexplained by `README.md:22-26`, which is the one
gap worth closing first because it costs nothing and it is what an outside auditor will
check.
