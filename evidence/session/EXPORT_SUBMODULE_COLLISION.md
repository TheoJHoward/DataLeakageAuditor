# A public export that shadows a submodule — candidate defect, recorded not repaired

Nothing here is a `PREREG.md` §6.2 result and no figure here belongs beside the
Phase 1 acceptance figures.

**The ask.** R238 §3: record it as a candidate defect **with its class**, and
with what it would take to establish whether anything but the test is exposed.
**Do not rename this round** — a public export is an API surface and renaming it
has its own blast radius.

---

## The class

**A name re-exported onto a package namespace, colliding with a submodule of the
same name.** Python binds submodules as attributes of their package; an
`__init__.py` that binds a different object under the same name wins, and the
submodule becomes unreachable by attribute access — including the attribute
access that `import pkg.sub as x` performs. Nothing warns.

It is a near neighbour of the two-lists hazard this project keeps finding: **one
name, two things, and no mechanism keeping them apart.** The difference is that
here the collision is between a name and a *namespace*, so it is invisible to
any check that reads either one alone.

---

## The population, and both halves of it

Read from the installed package rather than from the source text:

| | count | which |
|---|---|---|
| submodules of `leakaudit` | **15** | availability, availability_trace, checks, cli, contract, corruption, detectors, determinism, findings, fixture_adapter, identity_control, inference, model_file, modes, probe |
| names in `__all__` that collide with a submodule name | **2** | `availability`, `fixture_adapter` |
| submodules **actually shadowed** | **1** | `availability` |

**The second half is the one worth stating: a collision is not a shadowing.**
`fixture_adapter` collides and resolves correctly, because `__init__.py:57` binds
it with `from . import fixture_adapter` — the module itself. `availability` is
shadowed because `__init__.py:55` binds it with `from .modes import (…,
availability, …)` — the *function* `modes.availability`, over the submodule.

So the rule is not "a name in `__all__` matching a submodule is a defect." It is
**"a name bound to a non-module object over a submodule attribute"**, and exactly
one exists.

---

## What it does

    import leakaudit.availability as av      ->  <function availability>
    leakaudit.availability                   ->  <function availability>
    from leakaudit.availability import X     ->  works
    sys.modules["leakaudit.availability"]    ->  the module, present and correct

The submodule is imported and reachable; only the attribute lookup is wrong. A
caller then meets

    AttributeError: 'function' object has no attribute 'AvailabilityModel'

— **a detection arriving as an error that names the wrong thing**, which is the
failure mode `modes.availability` was hardened against twice, in the function
doing the shadowing.

---

## Exposure — measured, not estimated

**No in-repo caller is exposed.** Every use in this repository is the working
form. Searched for `import leakaudit.availability` and `from leakaudit import …
availability` across all `.py` outside `.git`, `__pycache__` and `build/`:
**zero hits.** `tools/wholeframe_guard.py:154` and
`tools/portability_digest.py:84` both use `from leakaudit.availability import
…`, which is unaffected.

**One exposure is inside the package's own user-facing text**, and it is the
reason this is a candidate defect rather than a curiosity:

- `src/leakaudit/contract.py:238` — *"…is `leakaudit.availability.run_probe_a`,
  which takes an…"*
- `src/leakaudit/contract.py:243` — *"`leakaudit.availability.AvailabilityModel
  .decision_column` is where a…"*

**The contract text names the dotted path, and the obvious import form for that
path returns the wrong object.** A reader doing what the text points at gets a
function and an `AttributeError` naming something they never typed.

**What is NOT established, and cannot be from inside this repository:** whether
any external caller uses the breaking form. That is unmeasurable here and is
stated as unmeasured rather than assumed empty.

**How it was found:** by hitting it while writing R237 §4's library-path test —
not by a check. No check would have found it; nothing in this project inspects
the package's attribute namespace against its submodule list.

---

## What a repair would cost, so the decision has its blast radius

Three shapes, none taken:

1. **Rename the exported function** (`modes.availability` → e.g.
   `column_availability`). Changes `__all__`, a documented public name, and any
   external caller of `leakaudit.availability(frame, column, spec)`.
2. **Drop the function from `__init__`'s re-export**, leaving
   `leakaudit.modes.availability`. Smaller, still removes a public name.
3. **Bind the submodule explicitly after the function**, so the module wins.
   Smallest, and the worst: it makes `leakaudit.availability` the module and
   silently removes the function from the package namespace — the same class of
   surprise pointed the other way.

**Each changes the public surface**, which is why R238 §3 rules it out of this
round. Recorded for the author.

---

## What would close it as a defect rather than a candidate

A check that enumerates the package's submodules, resolves each as an attribute
of the package, and refuses any that does not come back a module. That is four
lines and would have caught this the round it was introduced. **Not built here**
— the ruling on the repair comes first, because a check pinning behaviour nobody
has decided to keep would pin the defect.
