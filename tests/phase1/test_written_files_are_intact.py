"""B8.2 — detect the damage D2.1 exists to prevent, instead of restating D2.1.

THE RULE HAS NOT HELD. "Never write file content through a shell heredoc or a
non-raw string literal" has been stated in every delta and violated three times:

  * `\\b` inside a non-raw literal became a literal BACKSPACE in a regex, so the
    marker it guarded never matched and an enumeration silently under-split.
  * The same class, twice more, in prose describing the first one.
  * A heredoc where `\\n` became a REAL NEWLINE inside a regex literal, breaking
    the file outright.

A rule restated in every round and violated in three of them is not a discipline
problem. It needs a detector.

TWO CHECKS, because the three violations failed in two different ways:

  1. **Control characters.** The backspace class. A stray `\\x08` is invisible in
     every editor and every diff, and the file keeps working -- wrongly.
  2. **Every source file parses.** The newline-in-a-regex class. That one is not
     a control character at all; it is a syntax break, and only a parse catches
     it. Both failures came from the same cause, so both are checked here.

§2.4: THE POPULATION EXCLUDES THE INSTRUMENT. This file is skipped, and not for
convenience -- it necessarily discusses the byte values it hunts, so scanning
itself would either force it to be written unreadably or produce a finding about
its own documentation. Every earlier instance of a too-narrow domain HID
findings; a self-scanning instrument INVENTS them. Same root, opposite direction.
"""
import ast
import pathlib

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[2]
SELF = pathlib.Path(__file__).resolve()

# Files this project's own tooling writes. Not the whole tree: the registration
# gate owns that population and has its own scanner for it. This is scoped to
# what Phase 1 produces, which is where the violations happened.
ROOTS = (ROOT / "src" / "leakaudit", ROOT / "tests" / "phase1")

# TAB, LF and CR are legitimate text. Everything else below 0x20, plus DEL and
# the BOM, is damage.
ALLOWED = {0x09, 0x0A, 0x0D}


def population():
    out = []
    for r in ROOTS:
        for p in sorted(r.rglob("*")):
            if not p.is_file() or p.suffix not in (".py", ".json"):
                continue
            if "__pycache__" in p.parts:
                continue
            if p.resolve() == SELF:          # §2.4
                continue
            out.append(p)
    return out


def scan(data: bytes):
    """Return [(offset, byte)] for every control or invisible byte."""
    hits = [(i, b) for i, b in enumerate(data)
            if b < 0x20 and b not in ALLOWED or b == 0x7F]
    if data[:3] == b"\xef\xbb\xbf":
        hits.append((0, 0xFEFF))
    return hits


def test_the_population_is_not_empty():
    """A scanner over nothing passes. That is the shape of every instrument
    defect this project has recorded, so the population is asserted first."""
    files = population()
    assert len(files) >= 10, "population is %d files; the scanner is not looking" % len(files)
    assert any(p.suffix == ".py" for p in files)


@pytest.mark.parametrize("path", population(), ids=lambda p: p.name)
def test_no_control_characters(path):
    hits = scan(path.read_bytes())
    assert not hits, "%s carries %d control/invisible byte(s): %s" % (
        path.relative_to(ROOT), len(hits),
        ["offset %d = 0x%02X" % (o, b) for o, b in hits[:5]])


@pytest.mark.parametrize("path", [p for p in population() if p.suffix == ".py"],
                         ids=lambda p: p.name)
def test_every_python_file_parses(path):
    """The newline-in-a-regex class. Not a control character -- a syntax break,
    and only a parse catches it."""
    try:
        ast.parse(path.read_text(encoding="utf-8"))
    except SyntaxError as e:
        pytest.fail("%s does not parse: line %s: %s"
                    % (path.relative_to(ROOT), e.lineno, e.msg))


# --------------------------------------------------------------------------
# KNOWN POSITIVES. A scanner that has only ever run over clean files has not
# been shown to detect anything.
# --------------------------------------------------------------------------

def test_known_positive_a_backspace_is_caught(tmp_path):
    """The exact defect: `\\b` written through a non-raw literal.

    The byte is produced with chr(), so this file's own source stays clean and
    the test does not depend on the very hazard it checks for.
    """
    bad = tmp_path / "mangled.py"
    bad.write_bytes(('MARK = re.compile(r"^item' + chr(8) + '")\n').encode("utf-8"))
    hits = scan(bad.read_bytes())
    assert hits, "a literal BACKSPACE was not detected"
    assert hits[0][1] == 0x08


def test_known_positive_a_bom_is_caught(tmp_path):
    bad = tmp_path / "bom.py"
    bad.write_bytes(b"\xef\xbb\xbfx = 1\n")
    assert scan(bad.read_bytes()), "a BOM was not detected"


def test_known_positive_a_broken_regex_literal_fails_the_parse(tmp_path):
    """The heredoc defect: `\\n` became a real newline inside a string literal."""
    bad = tmp_path / "broken.py"
    bad.write_bytes(b'import re\npat = re.compile(r"^@dec\\s*\ndef\\s+(\\w+)")\n')
    with pytest.raises(SyntaxError):
        ast.parse(bad.read_text(encoding="utf-8"))


def test_clean_content_is_not_flagged(tmp_path):
    """The companion negative: tabs, newlines and CRLF are legitimate text, and
    a scanner that rejects them would be unusable rather than strict."""
    ok = tmp_path / "fine.py"
    ok.write_bytes(b"def f():\r\n\tx = 1\r\n\treturn x\r\n")
    assert not scan(ok.read_bytes())
    ast.parse(ok.read_text(encoding="utf-8"))
