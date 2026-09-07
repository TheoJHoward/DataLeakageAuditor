"""The Track B classification is TOTAL, and a new lesson fails until it is placed.

R224 §4 item 3 asked for a classification made by hand, with its membership list.
A hand-made list is a claim about a file that drifts from it -- which is the
failure this project keeps recording -- so the claim is held here by measurement
instead: the entries are read from the file, the membership lines are read from
the file, and the two are required to agree exactly.

THE TOTALITY SHAPE, the same one `PROBE_PATH_SET.json`'s on-path/off-path lists
and the config-key complement use. Disjoint and jointly covering: every entry in
exactly one family, no family naming an entry that does not exist. A
classification with an unassigned entry has not classified anything, and the
twenty-second lesson will fail this file until somebody decides where it goes --
which is the point, because deciding where it goes is the work.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LESSONS = ROOT / "evidence/session/TRACKB_LESSONS.md"
MARKER = "THE CLASSIFICATION"


def _text() -> str:
    return LESSONS.read_text(encoding="utf-8")


def _entries(text: str) -> set[str]:
    return set(re.findall(r"^## (TB-\d\d)", text, re.M))


def _families(text: str) -> dict[str, set[str]]:
    """family heading -> the TB ids its Members line names."""
    section = text.split(MARKER)[-1]
    out: dict[str, set[str]] = {}
    current = None
    for line in section.splitlines():
        m = re.match(r"^## (F\d) — (.+)$", line)
        if m:
            current = "%s %s" % (m.group(1), m.group(2))
            continue
        if current and line.startswith(("**Members:", "**Member:")):
            out[current] = set(re.findall(r"TB-\d\d", line))
            current = None
    return out


def test_the_classification_section_exists_at_all():
    assert MARKER in _text(), (
        "the hand-made classification is gone from %s, so the membership list "
        "this file checks does not exist" % LESSONS.name)


def test_every_lesson_is_classified():
    text = _text()
    entries = _entries(text)
    assert entries, "no TB entries found; the heading form must have changed"
    classified = set().union(*_families(text).values())
    unassigned = entries - classified
    assert not unassigned, (
        "these lessons are in the file and in no family, so the classification "
        "is silent about them -- place each one or say why it has no family: %s"
        % sorted(unassigned))


def test_no_family_names_a_lesson_that_does_not_exist():
    text = _text()
    phantom = set().union(*_families(text).values()) - _entries(text)
    assert not phantom, (
        "these are named in a membership list and are not entries in the file, "
        "so the list is a claim about lessons that are not there: %s"
        % sorted(phantom))


def test_the_families_are_DISJOINT():
    """An entry in two families is a classification nobody has made."""
    fams = _families(_text())
    seen: dict[str, str] = {}
    doubled = []
    for name, members in fams.items():
        for tb in members:
            if tb in seen:
                doubled.append("%s is in both %r and %r" % (tb, seen[tb], name))
            seen[tb] = name
    assert not doubled, doubled


#: The one form the total may be declared in. Parsed, not searched: a search
#: over the section is satisfied by any coincidental digit, and this section is
#: full of them -- entry labels, round numbers, and prose about counts.
TOTAL_DECLARATION = re.compile(r"All \*\*(\d+)\*\* entries")


def declared_total(section: str) -> int:
    """The stated total, or a reason it cannot be read.

    EXACTLY ONE DECLARATION. Zero means nothing states the total; two or more
    means the section says it twice and a reader cannot tell which is the claim
    -- and that is not hypothetical, it is what R245 produced by quoting the
    declaration verbatim inside a paragraph explaining the bug.
    """
    found = TOTAL_DECLARATION.findall(section)
    if len(found) != 1:
        raise AssertionError(
            "the classification section carries %d total declarations and "
            "exactly one is expected. Zero means no reader can tell how many "
            "entries it claims to classify; more than one means the section "
            "states it twice, and a second copy in prose is how the previous "
            "repair was silently undone. Found: %s" % (len(found), found))
    return int(found[0])


def test_every_family_names_members_and_the_section_states_the_TOTAL():
    """A membership list without its denominator is a figure without its frame.

    The denominator is asserted at the SECTION level rather than per family: the
    families write their counts in prose ("Five of twenty-one"), and a test that
    demanded digits in each line would be a checker dictating the writing rather
    than checking the claim -- the shape R218 ruled against when a docstring was
    reworded to satisfy a parser.
    """
    text = _text()
    total = len(_entries(text))
    section = text.split(MARKER)[-1]
    for name, members in _families(text).items():
        assert members, "%s names no members" % name
    assert declared_total(section) == total, (
        "the classification declares %d entries and the file holds %d"
        % (declared_total(section), total))


# ---------------------------------------------------------------------------
# THE MUTATIONS. R246 §2.
# ---------------------------------------------------------------------------
#
# **"ENFORCED" IS ITSELF AN ABSENCE CLAIM** -- no violation passes -- so it needs
# its own known positive showing the enforcement fires. A green test believed
# without ever being shown to go red is a decoration, in the same family as the
# manifest hash nothing verified.
#
# THIS FILE EARNED THE SWEEP. Its total assertion could not fail: it searched
# the section for the total's digits, and entry labels carry digits, so with
# contiguous numbering the newest label always satisfied it. Two repairs were
# believed before one worked -- the second undone by the paragraph documenting
# the first. A file with one can't-fail assertion earns a check of its
# neighbours (TB-25's sweep-the-siblings, pointed at assertions).

def _mutate(fn, *args):
    """Run one assertion against a mutated file. True = it went RED."""
    original = LESSONS.read_text(encoding="utf-8")
    try:
        LESSONS.write_bytes(fn(original).encode("utf-8"))
        try:
            for a in args:
                a()
            return False
        except AssertionError:
            return True
    finally:
        LESSONS.write_bytes(original.encode("utf-8"))


TOTAL_ASSERTION = test_every_family_names_members_and_the_section_states_the_TOTAL


def test_the_total_assertion_REDDENS_on_a_wrong_total_that_matches_an_ID():
    """**THE IMMUNE POSITIVE.** The stated total is wrong AND the wrong number
    is an existing entry label, so a bare-digit search finds it either way. This
    is the case both earlier repairs passed."""
    assert _mutate(lambda t: t.replace("All **27** entries",
                                       "All **25** entries", 1),
                   TOTAL_ASSERTION), (
        "a wrong stated total coinciding with an entry id did NOT redden the "
        "assertion, which is the exact vacuity R246 was opened on")


def test_the_total_assertion_REDDENS_on_a_wrong_total_with_prose_digits():
    """Defeats the strip-the-labels repair: the true total appears in prose for
    an unrelated reason, so stripping labels does not save a search."""
    def mut(t):
        t = t.replace("All **27** entries", "All **25** entries", 1)
        return t.replace("**The rule for membership.**",
                         "**The rule for membership.** (27 rounds sit behind "
                         "this list.)", 1)
    assert _mutate(mut, TOTAL_ASSERTION)


def test_the_total_assertion_REDDENS_when_the_declaration_is_MISSING():
    assert _mutate(lambda t: t.replace("All **27** entries",
                                       "All ** ** entries", 1),
                   TOTAL_ASSERTION), (
        "with no declaration at all the assertion stayed green, so it is not "
        "checking that a total is stated")


def test_the_total_assertion_REDDENS_on_a_DUPLICATED_declaration():
    """Ambiguity is a failure, not something to resolve by taking the first.
    R245 created exactly this by quoting the declaration in prose."""
    assert _mutate(lambda t: t.replace(
        "**The rule for membership.**",
        "**The rule for membership.** (Restated: All **27** entries.)", 1),
        TOTAL_ASSERTION)


def test_the_total_assertion_PASSES_on_the_real_file():
    """The negative control. An assertion that reddened on everything would
    pass every mutation above and be useless."""
    TOTAL_ASSERTION()


def test_the_SIBLING_assertions_redden_too():
    """R246 §2's sweep. Each of the three was mutated and each went red, so the
    file's other assertions are enforcement rather than decoration."""
    assert _mutate(
        lambda t: t.replace("---\n\n# THE CLASSIFICATION",
                            "## TB-91 — an unclassified entry\n\nbody.\n\n"
                            "---\n\n# THE CLASSIFICATION", 1),
        test_every_lesson_is_classified), "an unclassified entry passed"
    assert _mutate(
        lambda t: t.replace("**Members: TB-11, TB-27.**",
                            "**Members: TB-11, TB-27, TB-92.**", 1),
        test_no_family_names_a_lesson_that_does_not_exist), "a phantom passed"
    assert _mutate(
        lambda t: t.replace("**Members: TB-11, TB-27.**",
                            "**Members: TB-11, TB-27, TB-02.**", 1),
        test_the_families_are_DISJOINT), "a doubled entry passed"
