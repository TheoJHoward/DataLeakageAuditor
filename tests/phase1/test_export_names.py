"""A public export does not shadow a submodule. R273 §1(h), closing backlog item G.

`leakaudit/__init__.py` re-exported the modes FUNCTION `availability`, which bound
over the `leakaudit.availability` SUBMODULE, so `from leakaudit import
availability` returned the function. The function is now `column_availability`,
with no alias under the old name -- an alias would shadow the module again. And
the check `EXPORT_SUBMODULE_COLLISION.md` said would close it as a defect: every
submodule, resolved as an attribute of the package, comes back a module.
"""
from __future__ import annotations

import importlib
import inspect
import pkgutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for p in (str(ROOT), str(ROOT / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

import leakaudit                                               # noqa: E402


def test_from_leakaudit_import_availability_is_the_MODULE():
    from leakaudit import availability
    assert inspect.ismodule(availability), availability
    assert availability.__name__ == "leakaudit.availability"


def test_EVERY_submodule_resolves_as_a_MODULE_on_the_package():
    names = [m.name for m in pkgutil.iter_modules(leakaudit.__path__)]
    assert "availability" in names and "modes" in names
    shadowed = []
    for name in names:
        importlib.import_module("leakaudit." + name)
        obj = getattr(leakaudit, name, None)
        if obj is not None and not inspect.ismodule(obj):
            shadowed.append((name, obj))
    assert not shadowed, "exports shadowing submodules: %s" % shadowed


def test_the_function_is_COLUMN_AVAILABILITY_with_NO_alias():
    assert "column_availability" in leakaudit.__all__
    assert "availability" not in leakaudit.__all__
    assert callable(leakaudit.column_availability)
    from leakaudit.modes import column_availability
    assert leakaudit.column_availability is column_availability
    import leakaudit.modes as modes
    assert not hasattr(modes, "availability"), "no alias under the old name"
