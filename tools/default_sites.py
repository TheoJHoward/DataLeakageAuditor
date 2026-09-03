"""Where this package supplies a default, statically and at run time. R222 §2.

THE DEFECT CLASS is a default supplied where the rule says REFUSE. `PREREG.md`
§2.4 says label availability "is never defaulted"; `contract._UNWIRED` refuses
five parameters rather than defaulting them; `leakaudit schema` says a column
with no mode "is not given one" because an assumed mode is an availability model
the user did not write. Each of those is a place where a default would be a
silent wrong answer.

MOST DEFAULTS ARE CORRECT, so this instrument CANNOT REPORT DEFECTS. It reports
CANDIDATES. Whether a given default should refuse is a per-site judgment, and the
judgment lives in `DEFAULT_SITE_CLASSIFICATION` below, not in the tracer.

    A tracer that reported every default taken and called the list a finding
    would be the plausible wrong instrument here, and it is ruled out by
    construction: nothing in this module returns anything named "finding".

TWO POPULATIONS, AND THEY ARE NOT THE SAME NUMBER.

    STATIC   every site that COULD supply a default -- function parameters with
             defaults, two-argument `.get`, three-argument `getattr` -- read from
             the source by parsing it. Everything reachable.

    RUNTIME  every site that DID supply one during named runs. Everything
             reached.

    The difference between them is the set of defaults that exist and are never
    taken, which is its own finding and is reported as such. **Any number from
    this module says which population it belongs to**, because "defaults taken"
    is entirely a function of which runs were traced -- exactly as
    `PROBE_PATH_SET.json`'s module set is a function of which runs measured it.
    A candidate list without its runs named is an absence claim without its
    population.

WHAT THE RUNTIME TRACER CANNOT SEE, stated before it is used rather than
discovered afterwards:

  * a call through a name bound before the trace started -- `from m import f`
    elsewhere at import time keeps the unwrapped function;
  * `.get(k, default)` and `getattr(o, n, default)`, which are builtin calls with
    no wrappable boundary. They are in the STATIC population only, and the
    classification covers them from there;
  * anything on a code path the traced runs do not execute, which is the whole
    of what (b) is about.
"""
from __future__ import annotations

import ast
import contextlib
import inspect
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
PKG = REPO / "src" / "leakaudit"


# ---------------------------------------------------------------------------
# POPULATION 1 -- STATIC. Everything reachable.
# ---------------------------------------------------------------------------


def _is_dataclass(node: ast.ClassDef) -> bool:
    for d in node.decorator_list:
        t = d.func if isinstance(d, ast.Call) else d
        if (getattr(t, "id", None) == "dataclass"
                or getattr(t, "attr", None) == "dataclass"):
            return True
    return False


def static_sites() -> list[tuple[str, int, str, str]]:
    """(module, line, kind, site) for every place a default COULD be supplied.

    Parsed, not matched: a default in a docstring is not a default, and this
    project has already had one checker read English as code (D-V30A-51).
    """
    out: list[tuple[str, int, str, str]] = []
    for p in sorted(PKG.glob("*.py")):
        tree = ast.parse(p.read_text(encoding="utf-8"), filename=p.name)
        for n in ast.walk(tree):
            if isinstance(n, ast.ClassDef) and _is_dataclass(n):
                # A @dataclass's __init__ is GENERATED, so its defaulted
                # parameters exist at run time and appear in no FunctionDef.
                # The runtime tracer saw thirteen such sites that this
                # enumeration had missed, which is the two populations
                # disagreeing in the direction that matters: the static one
                # was under-reporting, so "everything reachable" was smaller
                # than "everything reached".
                for stmt in n.body:
                    if isinstance(stmt, ast.AnnAssign) and stmt.value is not None:
                        name = getattr(stmt.target, "id", None)
                        if name:
                            out.append((p.name, stmt.lineno, "param",
                                        "__init__(%s=)" % name))
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                a = n.args
                positional = a.args[len(a.args) - len(a.defaults):] if a.defaults else []
                for arg in list(positional) + list(a.kwonlyargs):
                    out.append((p.name, n.lineno, "param",
                                "%s(%s=)" % (n.name, arg.arg)))
            elif isinstance(n, ast.Call):
                f = n.func
                if (isinstance(f, ast.Attribute) and f.attr == "get"
                        and len(n.args) == 2):
                    out.append((p.name, n.lineno, "dict.get",
                                ast.unparse(n)[:70]))
                elif (isinstance(f, ast.Name) and f.id == "getattr"
                        and len(n.args) == 3):
                    out.append((p.name, n.lineno, "getattr",
                                ast.unparse(n)[:70]))
    return out


def site_key(module: str, kind: str, site: str) -> str:
    """A line-independent key, so classification survives an edit above it."""
    return "%s::%s::%s" % (module, kind, site)


# ---------------------------------------------------------------------------
# POPULATION 2 -- RUNTIME. Everything reached, by the runs named.
# ---------------------------------------------------------------------------

@contextlib.contextmanager
def trace_defaults(runs: str):
    """Record which DEFAULTED PARAMETERS were omitted by callers.

    `runs` is a description of what is being executed inside the block, and it
    is REQUIRED rather than optional: the result is meaningless without it, and
    an optional argument for the thing that gives a number its meaning would be
    this project's own defect in the instrument built to find it.

    Yields a dict: site key -> number of calls that omitted that parameter.
    """
    if not runs or not runs.strip():
        raise ValueError(
            "trace_defaults(runs=...) needs a description of the runs. "
            "'Defaults taken' is entirely a function of which runs were traced, "
            "so a result without them named is an absence claim without its "
            "population.")

    taken: dict[str, int] = {}
    patched: list[tuple[object, str, object]] = []

    def wrap(owner, name, fn, module_name):
        try:
            sig = inspect.signature(fn)
        except (TypeError, ValueError):
            return
        defaulted = [p.name for p in sig.parameters.values()
                     if p.default is not inspect.Parameter.empty]
        if not defaulted:
            return

        def wrapper(*a, **kw):
            try:
                bound = sig.bind_partial(*a, **kw)
                for pname in defaulted:
                    if pname not in bound.arguments:
                        key = site_key(module_name, "param",
                                       "%s(%s=)" % (fn.__name__, pname))
                        taken[key] = taken.get(key, 0) + 1
            except TypeError:
                pass
            return fn(*a, **kw)

        wrapper.__name__ = fn.__name__
        wrapper.__doc__ = fn.__doc__
        wrapper.__wrapped__ = fn
        setattr(owner, name, wrapper)
        patched.append((owner, name, fn))

    for mod_path in sorted(PKG.glob("*.py")):
        mod_name = "leakaudit." + mod_path.stem
        mod = sys.modules.get(mod_name)
        if mod is None:
            continue
        for name, obj in list(vars(mod).items()):
            if inspect.isfunction(obj) and obj.__module__ == mod_name:
                wrap(mod, name, obj, mod_path.name)
            elif inspect.isclass(obj) and obj.__module__ == mod_name:
                for mname, mobj in list(vars(obj).items()):
                    if inspect.isfunction(mobj):
                        wrap(obj, mname, mobj, mod_path.name)
    try:
        yield taken
    finally:
        for owner, name, fn in patched:
            setattr(owner, name, fn)


# ---------------------------------------------------------------------------
# THE CLASSIFICATION. Three states, and unclassified is not one of them.
# ---------------------------------------------------------------------------

LEGITIMATE = "legitimate"          # a default that is the right answer
SHOULD_REFUSE = "should_refuse"    # a rule says refuse and this defaults
NOT_APPLICABLE = "not_applicable"  # not a user-facing declaration at all

STATES = (LEGITIMATE, SHOULD_REFUSE, NOT_APPLICABLE)
