"""The frame fork's question and its answers are one contract. R236 §2.

**WHAT R235 MEASURED AND THIS CLOSES.** The fork text named TWO branches; the
`accept()` that reads the reply knew ONE string plus a fallthrough. So a user
could read a question, answer it in the question's own words -- "this frame
carries my decision instant" -- and have that answer silently become *"not an
aggregate"*, indistinguishable from a typo and from an empty box.

**THE STRUCTURAL READ CAME BEFORE ANY VOCABULARY WAS WRITTEN**, and it is what
made this round routing rather than invention. R235 enumerated five frame cases
and reported three inexpressible. Read against the declarable set -- `ALL_MODES`
plus the frame-level `aggregate_frames` key -- two of those three were expressible
all along: *read at its own stamp* is `at_timestamp` and *no time semantics* is
`always`, both file-declarable since R204 P5. **The gap was in the question, not
in the vocabulary**, and `test_the_mode_set_ALREADY_CONTAINED_the_missing_cases`
below is that read as an assertion rather than a claim.

**WHY THE MONKEYPATCH TEST IS THE ONE THAT DISCRIMINATES.** R215 §0: a positive
every plausible wrong implementation also produces tests wiring, not validity.
Asserting "the fork mentions `source` and `accept()` takes `source`" passes just
as happily against two hand-typed lists that currently agree -- which is the
state R235 found, one round after they had already drifted. Adding a role to the
table at runtime and requiring BOTH halves to follow it fails against any copy.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[2]
for p in (str(ROOT), str(ROOT / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

from leakaudit import inference                                    # noqa: E402
from leakaudit.inference import (                                  # noqa: E402
    UnknownFrameRole, accept, draft, fork_lines)
from leakaudit.model_file import SCHEMA_DOC                        # noqa: E402
from leakaudit.modes import (                                      # noqa: E402
    AGGREGATE, ALL_MODES, ALWAYS, AT_TIMESTAMP, FILE_MODES, FRAME_ROLE_TABLE,
    FRAME_ROLES, MODE_ARITHMETIC, SOURCE, SPINE, FrameRole)


@pytest.fixture
def d():
    """One aggregate-shaped frame and one reference table with no clock."""
    return draft({
        "agg": pd.DataFrame({"k": pd.date_range("2026-01-01", periods=4,
                                                freq="1s"),
                             "v": [1.0, 2.0, 3.0, 4.0]}),
        "ref": pd.DataFrame({"sym": ["a", "b"], "tick": [0.25, 0.5]}),
    })


def _answers(d, **frames):
    """Every blank filled, so a refusal below is about the fork and not about
    an unfilled column -- the two are different refusals and a test that cannot
    tell them apart is not testing either."""
    out = {f: "at_timestamp" for f in d.unfilled_fields}
    for fname, ans in frames.items():
        out["%s (availability mode)" % fname] = ans
    return out


# ---------------------------------------------------------------------------
# the structural read, as an assertion
# ---------------------------------------------------------------------------
def test_the_mode_set_ALREADY_CONTAINED_the_missing_cases():
    """R236 §2(a). The population is stated: the whole declarable vocabulary."""
    assert AT_TIMESTAMP in FILE_MODES, (
        "R235's case 3, 'a source frame read at its own stamp', was reported "
        "inexpressible; it is this mode and it is declarable in a file")
    assert ALWAYS in FILE_MODES, "R235's case 4 is this mode"
    assert set(MODE_ARITHMETIC) == set(ALL_MODES), (
        "the printable arithmetic and the mode set have diverged, which is the "
        "two-lists hazard the generation was introduced to remove")


def test_NO_NEW_AVAILABILITY_VOCABULARY_WAS_INVENTED():
    """The roles are a ROLE vocabulary, and none of them is a mode name.

    A role that shadowed a mode name would be a second name for one thing --
    the failure this section was opened to fix, committed again in the fix.
    """
    assert not set(FRAME_ROLES) & set(ALL_MODES)


# ---------------------------------------------------------------------------
# totality: disjoint, jointly covering, third state fails
# ---------------------------------------------------------------------------
def test_the_three_roles_are_the_whole_answer_set():
    assert set(FRAME_ROLE_TABLE) == set(FRAME_ROLES)
    assert len(FRAME_ROLES) == len(set(FRAME_ROLES))


def test_every_role_is_ACCEPTED_and_lands_where_the_table_says(d):
    got = accept(d, _answers(d, agg="aggregate:k", ref="source"))
    assert got["aggregate_frames"] == {"agg": "k"}
    assert "decision_column" not in got, (
        "no frame was answered `spine`, so the key is absent and the ONE "
        "refusal in availability.require_decision_column fires at load. A "
        "second message here would be a second refusal for one condition")

    got = accept(d, _answers(d, agg="spine:k", ref="source"))
    assert got["decision_column"] == "k"
    assert got["aggregate_frames"] == {}


@pytest.mark.parametrize("bad", [
    "not an aggregate",   # R235's fallthrough, in the words accept() implied
    "decision",           # the branch the OLD fork text named, verbatim
    "",                   # an empty box
    "aggregate_frames",   # the config key rather than the role
    "at_timestamp",       # a COLUMN mode offered as a FRAME answer
])
def test_a_FOURTH_ANSWER_IS_REFUSED_not_read_as_one_of_the_three(d, bad):
    """The third state of the totality guard.

    `"decision"` is in this list deliberately: it is what the fork text said
    before R236, so a user following the old prose is now told their answer is
    not offered instead of having it discarded.
    """
    with pytest.raises(UnknownFrameRole) as e:
        accept(d, _answers(d, agg=bad, ref="source"))
    assert "not one of the answers the fork offered" in str(e.value)
    for role in FRAME_ROLES:
        assert role in str(e.value), "the refusal does not list the answers"


def test_a_role_that_NAMES_A_COLUMN_is_refused_without_one(d):
    with pytest.raises(UnknownFrameRole) as e:
        accept(d, _answers(d, agg="aggregate", ref="source"))
    assert "names a column" in str(e.value)


def test_a_role_that_takes_NO_column_is_refused_with_one(d):
    with pytest.raises(UnknownFrameRole) as e:
        accept(d, _answers(d, agg="aggregate:k", ref="source:sym"))
    assert "takes no column" in str(e.value)


def test_TWO_SPINES_ARE_REFUSED(d):
    """Disjointness, enforced where the answers arrive. Two decision clocks are
    two answers to one question with nothing to choose between them."""
    with pytest.raises(UnknownFrameRole) as e:
        accept(d, _answers(d, agg="spine:k", ref="spine:sym"))
    assert "two frames were answered `spine`" in str(e.value)


# ---------------------------------------------------------------------------
# one source -- the discriminating form
# ---------------------------------------------------------------------------
def test_the_fork_TEXT_and_the_ACCEPTED_TOKENS_come_from_ONE_TABLE(monkeypatch, d):
    """Add a role at runtime; BOTH halves have to follow it.

    Against two hand-typed lists that happen to agree -- R235's measured state,
    one round after they had drifted -- this fails. Against generation it passes
    without either half being touched.
    """
    extra = FrameRole("windowed", "aggregate_frames", True, "made up here",
                      "a role that exists only inside this test.")
    monkeypatch.setattr(inference, "FRAME_ROLES",
                        FRAME_ROLES + ("windowed",))
    monkeypatch.setattr(inference, "FRAME_ROLE_TABLE",
                        dict(FRAME_ROLE_TABLE, windowed=extra))

    text = " ".join(fork_lines("agg", ["k"]))
    assert "windowed" in text and "only inside this test" in text, (
        "the fork text did not follow the table, so it is a copy of it")

    accept(d, _answers(d, agg="windowed:k", ref="source"))


def test_every_role_the_fork_PRINTS_is_a_role_accept_TAKES(d):
    text = " ".join(fork_lines("agg", ["k"]))
    for role in FRAME_ROLES:
        assert role in text, "the fork does not offer %r" % role
        spec = FRAME_ROLE_TABLE[role]
        answer = "%s:k" % role if spec.takes_column else role
        accept(d, _answers(d, agg=answer, ref="source"))


@pytest.mark.parametrize("cols", [[], ["k"], ["ts_event", "ts_recv"]])
def test_the_ANSWER_SET_IS_THE_SAME_for_every_frame_shape(cols):
    """Only the preamble varies. R234 §0 is why the no-clock case still offers
    all three: the last narrowing from shape handed `aggregate_frames` to the
    frame carrying the decision instant, and here the premise would be
    `_is_datetimeish`'s output -- a detector that returned nothing at all on CSV
    columns for a whole round, silently."""
    text = " ".join(fork_lines("f", cols))
    for role in FRAME_ROLES:
        assert role in text


def test_the_draft_ASKS_THE_FORK_for_a_frame_with_no_clock(d):
    """The two-clock and no-clock branches used to report what was undetermined
    and never say what the answers were."""
    assert any("THE FORK" in e for e in d.forks["ref"].evidence)


# ---------------------------------------------------------------------------
# leakaudit schema -- R236 §2(d)
# ---------------------------------------------------------------------------
def test_the_SCHEMA_prints_the_mode_set_rather_than_restating_it():
    for m in FILE_MODES:
        assert m in SCHEMA_DOC and MODE_ARITHMETIC[m] in SCHEMA_DOC
    assert "The %d modes a file may declare" % len(FILE_MODES) in SCHEMA_DOC, (
        "the count is hand-typed again; it was 'five' beside a five-entry "
        "FILE_MODES with nothing checking the two")


def test_the_SCHEMA_documents_the_THREE_FRAME_ROLES():
    for role in FRAME_ROLES:
        spec = FRAME_ROLE_TABLE[role]
        assert "%s -> %s" % (role, spec.lands_in) in SCHEMA_DOC
    assert "DISJOINT" in SCHEMA_DOC and "COVER EVERY FRAME" in SCHEMA_DOC
    assert "is NOT a fourth role" in SCHEMA_DOC, (
        "the schema does not answer the question R235 left open -- whether "
        "'read at its own stamp' is a frame-level answer -- and that is the "
        "question a reader of the fork will arrive with")


def test_the_SCHEMA_no_longer_advertises_the_REMOVED_default():
    """The one live stale site R236 §1's sweep found."""
    assert 'Default "timestamp"' not in SCHEMA_DOC
    assert "NO DEFAULT" in SCHEMA_DOC
    assert "observed_silence" in SCHEMA_DOC, (
        "the schema says there is no default and not what the default did; a "
        "reader meets a rule rather than a reason")
