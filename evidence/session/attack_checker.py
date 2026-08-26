"""Adversarial constructions against tools/check_registration.py."""
import sys, tempfile, shutil
from pathlib import Path

sys.path.insert(0, r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01\tools")
import check_registration as cr

BANNED_BLOCK = (
    "### 6.8 Configuration completeness\n"
    "<!-- banned-list: exempt-from-scan -->\n"
    "Current banned terms: `capability matrix`, `noise floor`.\n"
    "<!-- /banned-list -->\n")

results = []

def case(name):
    def deco(fn):
        d = Path(tempfile.mkdtemp())
        try:
            fn(d)
            results.append(f"OK   {name}")
        except AssertionError as e:
            results.append(f"FAIL {name}: {e}")
        finally:
            shutil.rmtree(d, ignore_errors=True)
        return fn
    return deco

def mk(d, prereg, design="# Design\n"):
    (d / "PREREG.md").write_text(prereg, encoding="utf-8")
    (d / "DESIGN.md").write_text(design, encoding="utf-8")
    return d

# A1: reuse of a declared id on many markers -> unlimited exemptions
@case("A1 id reuse: 3 markers with id=REG15 exempt 3 separate banned lines, zero failures")
def a1(d):
    mk(d, BANNED_BLOCK +
       '\n<!-- banned-exempt: id=REG15 reason="r1" -->\n'
       "First noise-floor sentence.\n"
       '<!-- banned-exempt: id=REG15 reason="r2" -->\n'
       "Second noise-floor sentence.\n"
       '<!-- banned-exempt: id=REG15 reason="r3" -->\n'
       "Third noise-floor sentence.\n")
    f = cr.check_banned_vocabulary(d)
    failures = [x for x in f if not x.is_note]
    notes = [x for x in f if x.is_note]
    assert failures == [], [x.message for x in failures]
    assert len(notes) == 3

# A2: marker exempts across blank lines onto a distant line
@case("A2 blank-line skip: marker + 3 blank lines exempts a distant normative line")
def a2(d):
    mk(d, BANNED_BLOCK +
       '\n<!-- banned-exempt: id=REG15 reason="r" -->\n'
       "\n\n\n"
       "The noise floor governs all detector decisions.\n")
    f = [x for x in cr.check_banned_vocabulary(d) if not x.is_note]
    assert f == [], [x.message for x in f]

# A3: trailing inline marker: own line flagged, NEXT line silently exempted
@case("A3 inline marker: marked line flagged, following unrelated line exempted")
def a3(d):
    mk(d, BANNED_BLOCK +
       '\n15. The noise-floor mode is parked. <!-- banned-exempt: id=REG15 reason="r" -->\n'
       "The noise floor is mandatory for every comparison.\n")
    f = [x for x in cr.check_banned_vocabulary(d) if not x.is_note]
    # marked line IS flagged (wrong), unrelated next line is NOT flagged (wrong)
    assert len(f) == 1 and "parked" in f[0].message, [x.message for x in f]

# A4: fake banned-list block in DESIGN.md hides banned terms + formulas
@case("A4 fake banned-list block in DESIGN.md hides banned term AND single-source formula")
def a4(d):
    mk(d, BANNED_BLOCK, design=(
        "# D\n<!-- banned-list: decoy -->\n"
        "Build the noise floor. proof yield = correct pairs over labelled pairs. x \u00f7 y\n"
        "<!-- /banned-list -->\n"))
    bv = [x for x in cr.check_banned_vocabulary(d) if not x.is_note]
    ss = cr.check_single_source(d)
    assert bv == [] and ss == [], (bv, ss)

# A5: unclosed banned-list marker exempts the rest of the file
@case("A5 unclosed banned-list marker exempts everything after it")
def a5(d):
    mk(d, BANNED_BLOCK +
       "\n<!-- banned-list: oops unclosed\n"
       "The noise floor is mandatory.\n"
       "The capability matrix ships in v0.1.\n")
    f = [x for x in cr.check_banned_vocabulary(d) if not x.is_note]
    assert f == [], [x.message for x in f]

# A6: sect 0.4 exemption is by line CONTENT, so an identical line elsewhere is skipped
@case("A6 line identical to a section-0.4 line is skipped anywhere in PREREG.md")
def a6(d):
    mk(d, "### 0.4 Ledger\nThe noise floor is mandatory.\n\n"
          "### 2.3 Comparator\nThe noise floor is mandatory.\n" + BANNED_BLOCK)
    f = [x for x in cr.check_banned_vocabulary(d) if not x.is_note]
    assert f == [], [x.message for x in f]

# A7: ledger-note parenthetical in DESIGN.md hides restatement from single_source
@case("A7 *(v28 ...)* parenthetical in DESIGN.md hides banned term and formula")
def a7(d):
    mk(d, BANNED_BLOCK, design=(
        "# D\n*(v28: build the noise floor; proof yield = hits \u00f7 labelled pairs.)*\n"))
    bv = [x for x in cr.check_banned_vocabulary(d) if not x.is_note]
    ss = cr.check_single_source(d)
    assert bv == [] and ss == [], (bv, ss)

# A8: parking lot with the one good bullet plus arbitrary extra normative prose
@case("A8 PARKING_LOT.md with extra non-bullet normative text still passes")
def a8(d):
    (d / "PARKING_LOT.md").write_text(
        "# P\n"
        "- A potential noise-floor fallback for nondeterministic pipelines; "
        "amended registration; evaluation partition\n"
        "\n## A second mechanism, parked without any amendment\n"
        "The detector shall also ship a statistical comparison regime.\n"
        "* an asterisk-bullet second entry\n"
        "1. a numbered third entry\n",
        encoding="utf-8")
    assert cr.check_parking_lot(d) == [], [x.message for x in cr.check_parking_lot(d)]

# A9: reducer functions satisfied by lines inside a docstring; stubs also pass
@case("A9 reducer_functions satisfied by def-lines inside a string literal")
def a9(d):
    mk(d, BANNED_BLOCK +
       "\n## 11. Registration integrity\n" +
       "".join(f"`{n}` " for n in cr.REQUIRED_REDUCER_FUNCTIONS) + "\n")
    (d / "protocol").mkdir()
    body = '"""doc\n' + "".join(
        f"def {n}(...):\n" for n in cr.REQUIRED_REDUCER_FUNCTIONS) + '"""\n'
    (d / "protocol" / "runtime_reference.py").write_text(body, encoding="utf-8")
    assert cr.check_reducer_functions(d) == [], \
        [x.message for x in cr.check_reducer_functions(d)]

# A10: marker with banned term in the reason string -> is the marker line scanned?
@case("A10 banned term inside the marker's own reason IS flagged (no hiding)")
def a10(d):
    mk(d, BANNED_BLOCK +
       '\n<!-- banned-exempt: id=REG15 reason="names the noise floor" -->\n'
       "15. The parked mechanism entry.\n")
    f = [x for x in cr.check_banned_vocabulary(d) if not x.is_note]
    assert len(f) == 1, [x.message for x in f]

# A11: two markers stacked above one line: both accepted, only one note printed
@case("A11 stacked markers overwrite: only the LAST exemption is printed as a note")
def a11(d):
    mk(d, BANNED_BLOCK +
       '\n<!-- banned-exempt: id=REG15 reason="r1" -->\n'
       '<!-- banned-exempt: id=PARK9 reason="r2" -->\n'
       "The noise-floor entry.\n")
    f = cr.check_banned_vocabulary(d)
    notes = [x for x in f if x.is_note]
    failures = [x for x in f if not x.is_note]
    assert failures == [] and len(notes) == 1, ([x.message for x in f])

for r in results:
    print(r)
