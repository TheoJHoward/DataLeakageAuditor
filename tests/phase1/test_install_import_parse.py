"""The installability checker reads IMPORTS, not sentences. R218 §4.

WHAT WAS WRONG. `_INSTALL_IMPORT` matched any line beginning `from ` or
`import ` over raw source text, so it could not tell code from prose. A docstring
sentence explaining the identity control -- *"it is what someone implementing /
from the registered sentence alone would most likely build"* -- was reported as
importing a module named `the`.

WHY THE FIX IS THE PARSER AND NOT THE PROSE. Two rules point opposite ways here.
*Fix the world, not the instrument* is about not weakening an instrument so a
TRUE finding goes away, and this finding was false, so it does not govern. *Never
adjust content toward an instrument* does govern: rewording the sentence would
leave the parser wrong and the next such sentence undefended. The prose was
restored and the parser replaced.

AND AN INSTRUMENT THAT PARSES TEXT WITH A HEURISTIC will eventually be handed
text that defeats the heuristic — and the text most likely to defeat it is the
text written to explain the instrument.

THE PLAUSIBLE WRONG REPAIR is a parser tightened until it stops choking and also
stops seeing: a narrower regex that passes today's two cases and misses a real
import tomorrow. So the positive runs in BOTH directions — the prose must stop
being flagged AND a real import in the same neighbourhood must still be caught —
because only the second rules that repair out.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
for p in (str(ROOT), str(ROOT / "tools")):
    if p not in sys.path:
        sys.path.insert(0, p)

import check_registration as cr                                   # noqa: E402


def _mods(text: str) -> list[str]:
    return [m for m, _line in cr._install_imports(text, "t.py")]


# ---------------------------------------------------------------------------
# DIRECTION 1 -- prose is no longer read as code.
# ---------------------------------------------------------------------------

PROSE = '''"""A docstring that broke the previous checker.

    It is not a strawman: it is what someone implementing
    from the registered sentence alone would most likely build.

    import the module that does not exist, said no one.
"""
'''


def test_the_exact_sentence_that_broke_it_is_not_an_import():
    assert _mods(PROSE) == [], (
        "prose inside a docstring is still being read as imports: %s"
        % _mods(PROSE))


def test_the_real_docstring_in_the_repository_is_clean():
    """Not a synthetic case -- the file that actually triggered it."""
    text = (ROOT / "src" / "leakaudit" / "identity_control.py").read_text(
        encoding="utf-8")
    assert "from the registered sentence alone" in text, (
        "the sentence was reworded. R218 §4 rules that the parser is fixed and "
        "the prose is not, so its absence means the wrong repair was taken")
    assert "the" not in _mods(text), (
        "the identity control is still reported as importing `the`")


@pytest.mark.parametrize("text", [
    "# from collections import nothing\n",
    "s = 'from os import path'\n",
    '"""\nimport antigravity\n"""\n',
    "x = 1  # import subprocess\n",
])
def test_comments_and_strings_are_not_imports(text):
    assert _mods(text) == [], "%r -> %s" % (text, _mods(text))


# ---------------------------------------------------------------------------
# DIRECTION 2 -- real imports are STILL caught. This is the direction that
# rules out the tightened-until-blind repair, and without it the fix is
# untested where it matters.
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("text,want", [
    ("import numpy\n", ["numpy"]),
    ("import numpy as np\n", ["numpy"]),
    ("import numpy.linalg\n", ["numpy"]),
    ("from pandas import DataFrame\n", ["pandas"]),
    ("from pandas.api import types\n", ["pandas"]),
    ("import os, sys\n", ["os", "sys"]),
    ("def f():\n    import pyarrow\n", ["pyarrow"]),   # indented, in a function
    ("if True:\n    import scipy\n", ["scipy"]),    # conditional
    ("try:\n    import ujson\nexcept ImportError:\n    ujson = None\n", ["ujson"]),
])
def test_real_imports_are_still_found(text, want):
    assert sorted(_mods(text)) == sorted(want), (
        "a real import was missed, which is the failure mode of a parser "
        "tightened until it stops seeing: %r -> %s" % (text, _mods(text)))


def test_an_import_BESIDE_the_prose_is_still_found():
    """The discriminating case: both in one file, one flagged and one not."""
    text = PROSE + "import numpy\n"
    assert _mods(text) == ["numpy"], (
        "the neighbourhood test: the prose must be ignored and the real import "
        "beside it must still be caught. Got %s" % _mods(text))


def test_a_lazy_import_inside_a_function_is_found():
    """This package imports lazily on purpose in several places, so missing
    these would hide exactly the dependencies most likely to be undeclared."""
    text = ("def f():\n"
            "    from leakaudit.availability import ProbeError\n"
            "    import pyarrow\n"
            "    return ProbeError, pyarrow\n")
    assert sorted(_mods(text)) == ["leakaudit", "pyarrow"]


# ---------------------------------------------------------------------------
# The properties the superseded pattern also had, kept deliberately.
# ---------------------------------------------------------------------------

def test_relative_imports_are_skipped_as_before():
    """`from .availability import X` never matched the old pattern either --
    a leading dot is not an identifier -- so skipping them is not a widening."""
    assert _mods("from . import availability\n") == []
    assert _mods("from .availability import ProbeError\n") == []
    assert _mods("from ..protocol import x\n") == []


def test_an_unparseable_module_is_REPORTED_not_skipped():
    """The old pattern read unparseable files happily and found whatever it hit.

    A checker reporting on text it cannot understand is reporting on something
    other than the code, so this is a finding rather than a silence.
    """
    mods = _mods("def f(:\n    pass\n")
    assert mods and mods[0].startswith("<unparseable"), mods


def test_line_numbers_are_the_import_s_own():
    text = "\n\n\nimport numpy\n"
    assert list(cr._install_imports(text, "t.py")) == [("numpy", 4)]
