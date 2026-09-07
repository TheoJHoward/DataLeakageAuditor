#!/usr/bin/env python3
"""Which coverage assertions still pass when their population is emptied.

    $ py -3.12 tools/empty_population_probe.py

Exit 0 always: this REPORTS candidates. An empty population is sometimes a
legitimate vacuous truth and sometimes a masked bug, and only a per-assertion
judgment separates them — the defaults-tracer shape (R222). **Nothing here
returns anything named a finding.**

**THE PROBE THAT HUNTS VACUITY WAS ITSELF VACUOUS.** Its first version patched
the population helpers on the TEST module, while the tests call them on the tool
they imported — `mv.entries()`, `cas.population()`. So the populations were never
emptied, and it reported **37 candidates having emptied almost nothing**: the
instrument built to find checks that do not exercise their subject did not
exercise its own.

It was caught by chasing a number that looked wrong, not by a mechanism. Had the
bug produced a plausible count, nothing would have prompted the look. **So this
module owes what it demands of everything else** — a known positive — and
`tests/phase1/test_empty_population_probe.py` supplies it: a constructed vacuous
assertion has to come back `candidate`, a constructed healthy one has to come
back `reddens`. Five real assertions reddening shows it can fire; the
constructed pair shows it fires on the shape it exists to catch and not on
everything.

**HOW MANY PATCHES ACTUALLY APPLIED IS PART OF THE RESULT.** A test whose
population helper this mechanism cannot reach is reported `unprobed`, never
`candidate` — the distinction the first version collapsed.

Written with the Write tool per D2.1.
"""
from __future__ import annotations

import importlib.util
import inspect
import io
import pathlib
import subprocess
import sys
import types

REPO = pathlib.Path(__file__).resolve().parents[1]

#: Names that return a repository population. Replaced with empty results.
EMPTIERS = {
    "tracked_files": lambda *a, **k: [],
    "tracked_python_files": lambda *a, **k: [],
    "population": lambda *a, **k: [],
    "entries": lambda *a, **k: [],
    "_entries": lambda *a, **k: set(),
    "_families": lambda *a, **k: {},
    "_text": lambda *a, **k: "",
    "scan": lambda *a, **k: ([], [], []),
    "files_containing_the_needle": lambda *a, **k: ([], []),
    "verify": lambda *a, **k: {"checked": 0, "stale": [], "absent": [],
                               "lines": 0},
    "_modules": lambda *a, **k: set(),
    "state": lambda *a, **k: {"rows": [], "functions": set(),
                              "established": set(), "outstanding": [],
                              "stray": []},
}


def load(rel: str, root: pathlib.Path = None):
    root = root or REPO
    name = "eprobe_" + str(rel).replace("/", "_").replace("\\", "_").replace(
        ".py", "")
    spec = importlib.util.spec_from_file_location(name, root / rel)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def patch_targets(mod, root: pathlib.Path = None) -> list:
    """The module itself, plus every repository module it holds.

    THE FIRST VERSION STOPPED AT THE FIRST ELEMENT, which is why it emptied
    nothing: a test calls `mv.entries()`, not `entries()`.
    """
    root = root or REPO
    out = [mod]
    for v in vars(mod).values():
        if isinstance(v, types.ModuleType) and v not in out:
            if str(root) in (getattr(v, "__file__", "") or ""):
                out.append(v)
    return out


def probe(rel: str, func: str, root: pathlib.Path = None) -> tuple:
    """(verdict, detail). verdict in candidate | reddens | errored | unprobed."""
    root = root or REPO
    try:
        mod = load(rel, root)
    except Exception as e:
        return "unprobed", "import failed: %s" % type(e).__name__
    fn = getattr(mod, func, None)
    if fn is None:
        return "unprobed", "not a module attribute"
    params = inspect.signature(fn).parameters
    if params:
        return "unprobed", "takes fixture(s): %s" % ",".join(params)

    saved, applied = [], 0
    for target in patch_targets(mod, root):
        for name, stub in EMPTIERS.items():
            if hasattr(target, name) and callable(getattr(target, name)):
                saved.append((target, name, getattr(target, name)))
                setattr(target, name, stub)
                applied += 1
    real_run = subprocess.run

    def empty_run(cmd, *a, **k):
        if isinstance(cmd, (list, tuple)) and any("ls-files" in str(c)
                                                  for c in cmd):
            return types.SimpleNamespace(returncode=0, stdout="", stderr="")
        return real_run(cmd, *a, **k)

    for target in patch_targets(mod, root):
        if hasattr(target, "subprocess"):
            target.subprocess.run = empty_run
            applied += 1

    if applied == 0:
        for target, name, orig in saved:
            setattr(target, name, orig)
        return "unprobed", ("no population helper this mechanism can empty")

    out, old = io.StringIO(), sys.stdout
    try:
        sys.stdout = out
        fn()
        return "candidate", "passed with %d helper(s) emptied" % applied
    except AssertionError:
        return "reddens", "asserted with %d helper(s) emptied" % applied
    except Exception as e:
        return "errored", type(e).__name__
    finally:
        sys.stdout = old
        for target, name, orig in saved:
            setattr(target, name, orig)
        subprocess.run = real_run


def probe_all() -> dict:
    sys.path.insert(0, str(REPO / "tools"))
    import coverage_assertion_sweep as cas
    out = {}
    for f, fn in sorted({(r["file"], r["func"]) for r in cas.population()}):
        out[(f, fn)] = probe(f, fn)
    return out


def main(argv=None) -> int:
    res = probe_all()
    counts = {}
    for verdict, _ in res.values():
        counts[verdict] = counts.get(verdict, 0) + 1
    print("EMPTY-POPULATION PROBE -- candidates, never findings")
    for k in ("candidate", "reddens", "errored", "unprobed"):
        print("  %-12s %d" % (k, counts.get(k, 0)))
    print()
    print("CANDIDATES:")
    for (f, fn), (v, d) in sorted(res.items()):
        if v == "candidate":
            print("  %-46s %-56s %s" % (f.replace("tests/phase1/", ""), fn, d))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
