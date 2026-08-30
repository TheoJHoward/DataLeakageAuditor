"""SC-7(c), stated executably: the tool never receives the scoring key.

`PREREG.md` SC-7(b)/(c) withhold the declared ground-truth map from the tool. A
detector that could read it would be graded against a key it had seen, and the
run would measure retrieval rather than discrimination. The map is an artifact of
the harness, not an input to the tool.

`src/leakaudit`'s own docstring asserted this and cited a checker that did not
exist. The assertion was true -- verified by hand at R173 §1.1 over nine modules
and 1,984 lines -- but a correct invariant with no check is an unverified
assertion, so this is that check.

WHY AST AND NOT TEXT SEARCH. The package's docstring *discusses* `CaseLabels` by
name, and so does this module. A text scan therefore has to guess which
occurrences are code, which is what the earlier attempt did -- it tried to strip
docstrings by splitting on triple quotes, and the assertion carried `or True`, so
it could never fail. Parsing removes the guess: a docstring is a string constant
and simply is not a Name or an alias, so it cannot be mistaken for a reference.

WHAT COUNTS AS A VIOLATION, and each is a real route rather than a hypothetical:
  * importing the name, in any form, at module level or inside a function;
  * binding the harness module itself (`import protocol...`), which makes
    `protocol.runtime_reference.CaseLabels` reachable by attribute;
  * naming or constructing it anywhere in code;
  * reaching it by attribute off any object.
"""
from __future__ import annotations

import ast
import pathlib

KEY_NAMES = frozenset({"CaseLabels"})
HARNESS_MODULE = "protocol.runtime_reference"


class KeyLeak(AssertionError):
    """The tool can reach the scoring key. No run from here is a gate result."""


def _violations(path: pathlib.Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    out: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            for a in node.names:
                if a.name in KEY_NAMES:
                    out.append("L%d: imports %s from %s"
                               % (node.lineno, a.name, node.module))
        elif isinstance(node, ast.Import):
            for a in node.names:
                # Binding the harness module makes the key reachable by
                # attribute even though the name is never imported.
                if a.name == HARNESS_MODULE or a.name.split(".")[0] == "protocol":
                    out.append("L%d: binds the harness module %r; the key is "
                               "then reachable by attribute" % (node.lineno, a.name))
        elif isinstance(node, ast.Name) and node.id in KEY_NAMES:
            out.append("L%d: names %s in code" % (node.lineno, node.id))
        elif isinstance(node, ast.Attribute) and node.attr in KEY_NAMES:
            out.append("L%d: reaches .%s by attribute" % (node.lineno, node.attr))
    return out


def assert_key_free(package_dir: pathlib.Path) -> int:
    """Raise KeyLeak if any module under `package_dir` can reach the key.

    Returns the number of modules checked, so a caller can tell a real pass from
    a scan that silently found nothing to look at. A check whose population is
    empty reports success for the wrong reason.
    """
    package_dir = pathlib.Path(package_dir)
    modules = sorted(package_dir.glob("*.py"))
    if not modules:
        raise KeyLeak("no modules found under %s: the check scanned nothing and "
                      "its clean result means nothing" % package_dir)
    found: dict[str, list[str]] = {}
    for p in modules:
        v = _violations(p)
        if v:
            found[p.name] = v
    if found:
        detail = "; ".join("%s -> %s" % (k, ", ".join(v)) for k, v in found.items())
        raise KeyLeak(
            "the scoring key is reachable from the tool: %s. PREREG SC-7(c) "
            "withholds the declared map from the tool; a run that received it "
            "has not produced a gate result, whatever it reports." % detail)
    return len(modules)
