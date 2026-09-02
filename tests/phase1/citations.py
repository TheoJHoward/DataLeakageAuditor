"""Every module path cited in the package's own prose resolves. R200 P0.

WHY THIS IS A CLASS AND NOT AN INSTANCE. `__init__.py` records fixing a citation
to `leakaudit.trace.assert_key_free`, a function that did not exist, and states
the reason plainly: "a cited checker that is absent is a false statement in the
code carrying the claim." That fix addressed the instance. This addresses the
class, and the first thing it did was find two more.

A dead citation is worse than a dead link. A reader who follows it finds nothing
and knows they are lost; a reader who does NOT follow it believes a checker
exists, and the claim the citation supports is the claim they carry away. In a
package whose whole subject is silence that looks like a clean result, prose
asserting a safeguard that is absent is the same defect in the documentation.

WHAT IS CHECKED. Backtick-quoted dotted names rooted at one of this
repository's own top-level packages -- the form the package uses when it points
at its own machinery. Third-party and standard-library names are out of scope:
they are not this repository's to keep true.

THE EXEMPTION, AND WHY IT IS NARROW. A citation may be QUOTED as historically
wrong -- that is how a correction stays on the record instead of vanishing. Such
a line carries the marker below, and every exempt line is REPORTED as a note, so
an exemption is visible rather than silent. Nothing is exempt by being old.
"""
from __future__ import annotations

import importlib
import re
from pathlib import Path

ROOTS = ("leakaudit", "protocol")
MARKER = "[dead-citation-recorded]"

_CITATION = re.compile(r"`((?:%s)(?:\.[A-Za-z_][A-Za-z0-9_]*)+)`" % "|".join(ROOTS))


class DeadCitation(Exception):
    """The package's prose points at something that is not there."""


def _resolves(dotted: str) -> bool:
    """True when the dotted path names an importable module or an attribute of
    one. Walks from the longest importable prefix and then uses getattr, so
    `pkg.mod.func` resolves whether `pkg.mod` is a module or `mod` is an
    attribute of `pkg`."""
    parts = dotted.split(".")
    module = None
    consumed = 0
    for i in range(len(parts), 0, -1):
        try:
            module = importlib.import_module(".".join(parts[:i]))
            consumed = i
            break
        except Exception:                                   # noqa: BLE001
            continue
    if module is None:
        return False
    obj = module
    for name in parts[consumed:]:
        if not hasattr(obj, name):
            return False
        obj = getattr(obj, name)
    return True


def scan(package_dir: Path) -> tuple[list[dict], list[dict], int]:
    """(dead, exempt, n_citations_checked) over every module under the directory."""
    files = sorted(Path(package_dir).rglob("*.py"))
    if not files:
        raise DeadCitation(
            "no modules found under %s; a scan over an empty population "
            "reports nothing and proves nothing" % package_dir)
    dead: list[dict] = []
    exempt: list[dict] = []
    checked = 0
    for path in files:
        if "__pycache__" in path.parts:
            continue
        for lineno, line in enumerate(
                path.read_text(encoding="utf-8").split("\n"), 1):
            for m in _CITATION.finditer(line):
                dotted = m.group(1)
                entry = {"file": path.name, "line": lineno, "cites": dotted}
                if MARKER in line:
                    exempt.append(entry)
                    continue
                checked += 1
                if not _resolves(dotted):
                    dead.append(entry)
    return dead, exempt, checked


def render(dead: list[dict]) -> str:
    return "\n".join(
        "  %s:%d cites `%s`, which does not resolve" % (d["file"], d["line"], d["cites"])
        for d in dead)


def assert_citations_resolve(package_dir: Path) -> int:
    """Raise on any unresolvable citation. Returns the number checked."""
    dead, _exempt, checked = scan(package_dir)
    if dead:
        raise DeadCitation(
            "%d citation(s) in the package's own prose point at nothing:\n%s"
            % (len(dead), render(dead)))
    return checked
