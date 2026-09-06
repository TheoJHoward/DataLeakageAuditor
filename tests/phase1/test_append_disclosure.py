"""The disclosure applier. R236 housekeeping.

**WHY THIS TEST EXISTS AT ALL.** `OPERATING_RULES.md` §2 has said since R178 that
`DEVIATIONS.md` is append-only *"via the disclosure applier"*, and until R236 the
applier was rebuilt in session scratch every round and committed in none of them
— `git log --all -- tools/` listed nine files and it was not one. **A rule that
names an enforcement mechanism absent from the repository is enforced by memory**,
which is the class D-V30A-60 recorded and the one R231 acted on when it moved
`wholeframe_guard.py` out of a directory that gets cleaned.

Every case below is a wrong case: what the applier does when handed something it
is supposed to refuse, and whether the file survives it. A tool that appends
correctly on good input and mangles the ledger on bad input has not been tested
by watching it work.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
for p in (str(ROOT), str(ROOT / "tools")):
    if p not in sys.path:
        sys.path.insert(0, p)

import append_disclosure as ad                                     # noqa: E402

PRIOR = ("# Deviations\n\n"
         "## D-V30A-1 — the first one\n\nA record of something.\n\n"
         "## D-V30A-2 — the second one\n\nA record of something else.\n")


@pytest.fixture
def ledger(tmp_path):
    """LF, WRITTEN AS BYTES, and the bytes are the point.

    This fixture used `write_text` and the LF test below failed on the first
    run -- because `write_text` opens in text mode and Python translates `\n`
    to the platform terminator, so on Windows the "LF ledger" was CRLF and the
    applier faithfully preserved what it was actually handed. **The tool was
    right and the fixture was lying**, and a line-endings test whose fixture
    cannot state its own line endings is testing nothing it names. The real
    `DEVIATIONS.md` is LF (0 CRLF in 181578 bytes, measured), so the case this
    covers is the live one.
    """
    p = tmp_path / "DEVIATIONS.md"
    p.write_bytes(PRIOR.encode("utf-8"))
    return p


def body(n, text="A record of what happened.", title="a title"):
    return "## D-V30A-%d — %s\n\n%s\n" % (n, title, text)


# ---------------------------------------------------------------------------
# the one thing it is for
# ---------------------------------------------------------------------------
def test_it_appends_and_the_PRIOR_CONTENT_IS_A_PREFIX(ledger):
    tag = ad.append(body(3), ledger)
    assert tag == "D-V30A-3"
    after = ledger.read_text(encoding="utf-8")
    assert after.startswith(PRIOR), (
        "the prior content did not survive as an exact prefix, which is the one "
        "property this tool exists to have")
    assert "## D-V30A-3 — a title" in after


def test_the_NEXT_NUMBER_IS_DERIVED_not_supplied(ledger):
    assert ad.next_number(ledger.read_text(encoding="utf-8")) == 3
    ad.append(body(3), ledger)
    assert ad.next_number(ledger.read_text(encoding="utf-8")) == 4


# ---------------------------------------------------------------------------
# the wrong cases -- and the file has to be untouched after each
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("bad,why", [
    (body(3, "A caller must declare the clock."), "rule-shaped: must"),
    (body(3, "The body should say what happened."), "rule-shaped: should"),
    (body(9), "a skipped number"),
    (body(2), "a reused number"),
    (body(3) + "\n" + body(4), "two headings"),
    ("no heading at all, just prose\n", "no heading"),
    ("", "empty"),
])
def test_a_refused_body_LEAVES_THE_LEDGER_BYTE_IDENTICAL(ledger, bad, why):
    before = ledger.read_bytes()
    with pytest.raises(ad.DisclosureRefused):
        ad.append(bad, ledger)
    assert ledger.read_bytes() == before, (
        "%s was refused and the file changed anyway" % why)


def test_the_RULE_WORD_REFUSAL_SAYS_WHY_not_just_that(ledger):
    """A halt that states a rule without its reason is the thing this project
    keeps finding in its own messages."""
    with pytest.raises(ad.DisclosureRefused) as e:
        ad.append(body(3, "A caller must declare the clock."), ledger)
    msg = str(e.value)
    assert "'must'" in msg, "the refusal does not name the word it caught"
    assert "OPERATING_RULES.md" in msg, (
        "the refusal does not say where rules go, so a reader is told no and "
        "not told what to do instead")
    assert "NOT REWRITTEN AUTOMATICALLY" in msg, (
        "the refusal does not say the wording is the author's; a tool that "
        "silently reworded a disclosure would be editing the record")


def test_a_rule_word_INSIDE_A_LONGER_WORD_is_not_caught(ledger):
    """`\\b` is deliberate. `mustard`, `shoulder` and a quoted `mustn't` are not
    rules, and a check that halted on them would be one a user learns to route
    around rather than read."""
    ad.append(body(3, "The mustard-coloured column shouldered the load."), ledger)
    assert "mustard" in ledger.read_text(encoding="utf-8")


def test_the_number_refusal_NAMES_THE_NUMBER_IT_WANTED(ledger):
    with pytest.raises(ad.DisclosureRefused) as e:
        ad.append(body(9), ledger)
    assert "D-V30A-3" in str(e.value), (
        "the refusal does not say which number was expected, so the author is "
        "made to work it out from a file they were told not to edit")


def test_a_ledger_with_NO_HEADINGS_is_refused_rather_than_started_at_one(tmp_path):
    """Refusing beats guessing: a file with content and no recognised heading is
    more likely a wrong path than an empty ledger, and renumbering is not
    recoverable by reading the result."""
    p = tmp_path / "DEVIATIONS.md"
    p.write_text("# Deviations\n\nprose, but no headings\n", encoding="utf-8")
    with pytest.raises(ad.DisclosureRefused) as e:
        ad.append(body(1), p)
    assert "cannot be derived" in str(e.value)


# ---------------------------------------------------------------------------
# line endings -- delegated, and checked here because delegation is a claim
# ---------------------------------------------------------------------------
def test_CRLF_SURVIVES_an_append(tmp_path):
    p = tmp_path / "DEVIATIONS.md"
    p.write_bytes(PRIOR.replace("\n", "\r\n").encode("utf-8"))  # bytes: see above
    ad.append(body(3), p)
    data = p.read_bytes()
    assert data.count(b"\r\n") > 0 and data.count(b"\n") == data.count(b"\r\n"), (
        "an append changed the file's line endings, which R220 put in "
        "safe_edit to prevent; the delegation is not doing what it claims")


def test_LF_STAYS_LF(ledger):
    ad.append(body(3), ledger)
    data = ledger.read_bytes()
    assert b"\r\n" not in data


def test_the_real_ledger_is_the_default_target():
    """The tool points at this repository's own file, so a round that forgets to
    pass a path does not silently write somewhere else."""
    assert ad.DEVIATIONS == ROOT / "DEVIATIONS.md"
    assert ad.DEVIATIONS.exists()
