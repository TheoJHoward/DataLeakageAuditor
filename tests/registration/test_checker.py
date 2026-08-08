"""Tests for tools/check_registration.py: detection logic on synthetic
documents, plus integration against the real repository."""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

import check_registration as cr  # noqa: E402

BANNED_BLOCK = (
    "### 6.8 Configuration completeness\n"
    "<!-- banned-list: exempt-from-scan -->\n"
    "Current banned terms: `capability matrix`, `noise floor`.\n"
    "<!-- /banned-list -->\n")


def _mk_root(tmp_path: Path, prereg: str, design: str = "# Design\n") -> Path:
    (tmp_path / "PREREG.md").write_text(prereg, encoding="utf-8")
    (tmp_path / "DESIGN.md").write_text(design, encoding="utf-8")
    return tmp_path


# ---------------------------------------------------------------------------
# Banned vocabulary and its declared exemptions
# ---------------------------------------------------------------------------

def test_banned_term_detected_with_hyphen_normalization(tmp_path):
    root = _mk_root(tmp_path, BANNED_BLOCK + "\nA noise-floor fallback is promised here.\n")
    findings = cr.check_banned_vocabulary(root)
    assert len(findings) == 1
    assert "noise floor" in findings[0].message


def test_banned_list_block_itself_is_exempt(tmp_path):
    root = _mk_root(tmp_path, BANNED_BLOCK)
    assert cr.check_banned_vocabulary(root) == []


def test_ledger_note_parenthetical_is_exempt(tmp_path):
    root = _mk_root(tmp_path, BANNED_BLOCK +
                    "\n*(v14 pre-registered a noise floor regime; removed.)*\n")
    assert cr.check_banned_vocabulary(root) == []


def test_history_marker_is_exempt(tmp_path):
    root = _mk_root(tmp_path, BANNED_BLOCK + "\n*(→ `HISTORY.md` H-05: noise floor)*\n")
    assert cr.check_banned_vocabulary(root) == []


def test_non_historical_parenthetical_is_scanned(tmp_path):
    root = _mk_root(tmp_path, BANNED_BLOCK + "\n*(a noise floor aside with no marker)*\n")
    assert len(cr.check_banned_vocabulary(root)) == 1


def test_design_is_scanned_for_banned_terms(tmp_path):
    root = _mk_root(tmp_path, BANNED_BLOCK, design="# D\nBuild the capability matrix.\n")
    findings = cr.check_banned_vocabulary(root)
    assert [f.file for f in findings] == ["DESIGN.md"]


# ---------------------------------------------------------------------------
# banned-exempt markers (PREREG §6.8, v28): two declared ids, reasons
# required, exemptions visible in output, no wildcard
# ---------------------------------------------------------------------------

def test_declared_exempt_marker_exempts_only_the_marked_block(tmp_path):
    root = _mk_root(tmp_path, BANNED_BLOCK +
                    '\n<!-- banned-exempt: id=REG15 reason="must name the parked mechanism" -->\n'
                    "15. The noise-floor mode is parked.\n"
                    "\n"
                    "A second noise-floor mention with no marker.\n")
    findings = cr.check_banned_vocabulary(root)
    failures = [f for f in findings if not f.is_note]
    notes = [f for f in findings if f.is_note]
    assert len(failures) == 1, "the unmarked span must still be flagged"
    assert "no marker" in failures[0].message
    assert len(notes) == 1 and "REG15" in notes[0].message
    assert "must name the parked mechanism" in notes[0].message


def test_exempt_marker_without_reason_fails(tmp_path):
    root = _mk_root(tmp_path, BANNED_BLOCK +
                    "\n<!-- banned-exempt: id=REG15 -->\n"
                    "15. The noise-floor mode is parked.\n")
    failures = [f for f in cr.check_banned_vocabulary(root) if not f.is_note]
    assert any("without an id and reason" in f.message for f in failures)
    assert any("noise floor" in f.message for f in failures), (
        "an invalid marker exempts nothing")


def test_undeclared_exempt_id_fails(tmp_path):
    root = _mk_root(tmp_path, BANNED_BLOCK +
                    '\n<!-- banned-exempt: id=WILDCARD reason="because" -->\n'
                    "15. The noise-floor mode is parked.\n")
    failures = [f for f in cr.check_banned_vocabulary(root) if not f.is_note]
    assert any("not one of the two declared" in f.message for f in failures)
    assert any("noise floor" in f.message for f in failures)


def test_exemption_notes_never_fail_a_stage(tmp_path):
    root = _mk_root(tmp_path, BANNED_BLOCK +
                    '\n<!-- banned-exempt: id=PARK9 reason="names what an amendment restores" -->\n'
                    "9. A noise-floor fallback is parked.\n")
    findings = cr.check_banned_vocabulary(root)
    assert all(f.is_note for f in findings)


def test_declared_id_cannot_be_reused(tmp_path):
    """A reused declared id would turn two declared exemptions into a
    wildcard (PREREG §6.8: two spans, two ids)."""
    root = _mk_root(tmp_path, BANNED_BLOCK +
                    '\n<!-- banned-exempt: id=REG15 reason="r1" -->\n'
                    "15. The noise-floor mode is parked.\n"
                    '<!-- banned-exempt: id=REG15 reason="r2" -->\n'
                    "16. A second noise-floor span.\n")
    findings = cr.check_banned_vocabulary(root)
    failures = [f for f in findings if not f.is_note]
    assert any("used more than once" in f.message for f in failures)
    assert any("noise floor" in f.message for f in failures), (
        "the second span stays in the scan")


def test_marker_separated_by_blank_line_is_floating(tmp_path):
    root = _mk_root(tmp_path, BANNED_BLOCK +
                    '\n<!-- banned-exempt: id=REG15 reason="r" -->\n'
                    "\n"
                    "The noise floor governs detector decisions.\n")
    failures = [f for f in cr.check_banned_vocabulary(root) if not f.is_note]
    assert any("not immediately above" in f.message for f in failures)
    assert any("noise floor" in f.message for f in failures)


def test_inline_marker_is_rejected_and_line_stays_scanned(tmp_path):
    root = _mk_root(tmp_path, BANNED_BLOCK +
                    '\n15. The noise-floor mode is parked. '
                    '<!-- banned-exempt: id=REG15 reason="r" -->\n')
    failures = [f for f in cr.check_banned_vocabulary(root) if not f.is_note]
    assert any("standalone line" in f.message for f in failures)
    assert any("noise floor" in f.message for f in failures)


def test_stacked_markers_are_floating(tmp_path):
    root = _mk_root(tmp_path, BANNED_BLOCK +
                    '\n<!-- banned-exempt: id=REG15 reason="r" -->\n'
                    '<!-- banned-exempt: id=PARK9 reason="r" -->\n'
                    "15. The noise-floor mode is parked.\n")
    findings = cr.check_banned_vocabulary(root)
    failures = [f for f in findings if not f.is_note]
    assert any("not immediately above" in f.message for f in failures)
    notes = [f for f in findings if f.is_note]
    assert len(notes) == 1 and "PARK9" in notes[0].message


def test_decoy_banned_list_block_in_design_is_flagged_and_scanned(tmp_path):
    root = _mk_root(tmp_path, BANNED_BLOCK,
                    design="# D\n<!-- banned-list: decoy -->\n"
                           "Build the noise floor.\n"
                           "<!-- /banned-list -->\n")
    failures = [f for f in cr.check_banned_vocabulary(root) if not f.is_note]
    assert any("outside PREREG.md" in f.message for f in failures)
    assert any("noise floor" in f.message for f in failures), (
        "a decoy block exempts nothing")


def test_unclosed_banned_list_block_exempts_nothing(tmp_path):
    root = _mk_root(tmp_path,
                    "<!-- banned-list: exempt-from-scan -->\n"
                    "Current banned terms: `noise floor`.\n")
    failures = [f for f in cr.check_banned_vocabulary(root) if not f.is_note]
    assert any("unclosed" in f.message for f in failures)


def test_second_banned_list_block_in_prereg_is_flagged(tmp_path):
    root = _mk_root(tmp_path, BANNED_BLOCK +
                    "\n<!-- banned-list: second -->\nThe noise floor ships.\n"
                    "<!-- /banned-list -->\n")
    failures = [f for f in cr.check_banned_vocabulary(root) if not f.is_note]
    assert any("second banned-list block" in f.message for f in failures)
    assert any("noise floor" in f.message for f in failures), (
        "only the first closed block is exempt")


def test_section_04_exemption_is_by_range_not_content(tmp_path):
    prereg = (BANNED_BLOCK +
              "### 0.4 The version ledger\nThe noise floor is history.\n"
              "### 2.3 The comparator\nThe noise floor is history.\n")
    root = _mk_root(tmp_path, prereg)
    failures = [f for f in cr.check_banned_vocabulary(root) if not f.is_note]
    assert len(failures) == 1, "only the §2.3 copy is scanned, and it fails"


def test_design_parentheticals_are_scanned(tmp_path):
    """PREREG §6.8 declares the ledger-note exemption for PREREG.md only;
    DESIGN.md's declared historical region (the numbered lessons) moved to
    HISTORY.md, so every DESIGN line is normative and scanned."""
    root = _mk_root(tmp_path, BANNED_BLOCK,
                    design="# D\n*(v14 carried a noise floor regime here.)*\n")
    failures = [f for f in cr.check_banned_vocabulary(root) if not f.is_note]
    assert len(failures) == 1


def test_current_version_parenthetical_in_prereg_is_scanned(tmp_path):
    """A note naming only the CURRENT version is not a ledger note — a
    normative sentence in historical costume stays in the scan."""
    prereg = ("**Status:** v28 — current.\n" + BANNED_BLOCK +
              "\n*(v28: the noise floor is mandatory.)*\n"
              "*(v14 pre-registered a noise floor regime; removed.)*\n")
    root = _mk_root(tmp_path, prereg)
    failures = [f for f in cr.check_banned_vocabulary(root) if not f.is_note]
    assert len(failures) == 1, "the v28 note is scanned; the v14 note is exempt"


def test_parking_lot_rejects_non_bullet_content(tmp_path):
    (tmp_path / "PARKING_LOT.md").write_text(
        "# P\n\nReviewed Sundays only (PREREG.md §4.4).\n\n"
        "- A potential noise-floor fallback for nondeterministic pipelines; "
        "requires an amended registration, separate development tuning, and a "
        "new unseen evaluation partition before any result is published.\n\n"
        "## A second mechanism, parked informally\n"
        "The detector shall also ship a second regime.\n"
        "* an asterisk-bullet entry\n",
        encoding="utf-8")
    findings = cr.check_parking_lot(tmp_path)
    assert any("beyond the single" in f.message for f in findings)


def test_structure_requires_a_real_test_suite(tmp_path):
    (tmp_path / "tests" / "registration").mkdir(parents=True)
    findings = cr.check_structure(tmp_path)
    assert any("no test_*.py files" in f.message for f in findings)
    assert any("traces.py" in f.file for f in findings)


# ---------------------------------------------------------------------------
# Deletion certificate: code symbols, not English homographs
# ---------------------------------------------------------------------------

def test_deleted_symbol_in_code_context_is_flagged(tmp_path):
    root = _mk_root(tmp_path, BANNED_BLOCK + "\nThe state `superseded` still applies.\n")
    findings = cr.check_deletion_certificate(root)
    assert len(findings) == 1


def test_plain_english_homograph_is_not_flagged(tmp_path):
    root = _mk_root(tmp_path, BANNED_BLOCK +
                    "\nThe superseded results are published alongside.\n")
    assert cr.check_deletion_certificate(root) == []


def test_deleted_config_symbol_flagged(tmp_path):
    root = _mk_root(tmp_path, BANNED_BLOCK)
    (root / "VALIDATED_CONFIG.toml").write_text(
        "[validated.runtime]\ncomparison_mode = 'exact'\n", encoding="utf-8")
    findings = cr.check_deletion_certificate(root)
    assert any("comparison_mode" in f.message for f in findings)


# ---------------------------------------------------------------------------
# Single source
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("span", [
    'unavailable = a > d    if ties == "available"',
    "Any change at rows with d(i) <= d is a finding.",
    'promotion_status = "preserving" | "promoted"',
    "Reach is **the latest boundary at which a change was observed.",
    "proof yield = correct pairs over labelled pairs",
    "x ÷ y",
    "the states are not_applicable, unsupported, completed and incomplete",
])
def test_single_source_rules_fire(tmp_path, span):
    root = _mk_root(tmp_path, BANNED_BLOCK, design=f"# D\n{span}\n")
    assert cr.check_single_source(root), span


def test_single_source_allows_section_references(tmp_path):
    root = _mk_root(tmp_path, BANNED_BLOCK,
                    design="# D\nTier is resolved by PREREG.md §3.1 and is "
                           "not restated here.\n")
    assert cr.check_single_source(root) == []


# ---------------------------------------------------------------------------
# Arithmetic, lock table, requirement IDs, legality table
# ---------------------------------------------------------------------------

def test_phase_arithmetic_catches_wrong_sum(tmp_path):
    root = _mk_root(tmp_path, BANNED_BLOCK +
                    "\n**14–20 working weekends** (minimum 1+2+2+1+2+2+2+1 = 14; "
                    "maximum 2+3+3+1+3+3+3+2 = 20).\n")
    findings = cr.check_phase_arithmetic(root)
    assert any("minimum" in f.message for f in findings)


def test_lock_table_catches_topic_drift(tmp_path):
    prereg = (
        "### 0.1 What is locked\n"
        "| Locked here | Section | Revisable |\n"
        "|---|---|---|\n"
        "| The tie comparator and its default | §9.9 | mask construction |\n"
        "| A second row about cohorts probed | §9.9 | scheduling |\n"
        "| A third row about availability cells | §9.9 | matrices |\n"
        "| A fourth row about scoring units | §9.9 | collection |\n"
        "| A fifth row about conformance suites | §9.9 | running |\n"
        "### 9.9 An unrelated section\n"
        "Entirely about penguins.\n" + BANNED_BLOCK)
    root = _mk_root(tmp_path, prereg)
    findings = cr.check_lock_table(root)
    assert any("drift" in f.message for f in findings)


def test_requirement_ids_on_real_repo():
    assert cr.check_requirement_ids(ROOT) == []


def test_legality_table_matches_reducer_on_real_repo():
    assert cr.check_legality_table(ROOT) == []


def test_lock_table_on_real_repo():
    assert cr.check_lock_table(ROOT) == []


def test_phase_arithmetic_on_real_repo():
    assert cr.check_phase_arithmetic(ROOT) == []


def test_requirement_id_regex_matches_expected_ids():
    for rid in cr.EXPECTED_REQUIREMENT_IDS:
        assert cr._RID.fullmatch(rid), rid


# ---------------------------------------------------------------------------
# Stages
# ---------------------------------------------------------------------------

def test_every_check_is_owned_by_exactly_one_stage():
    names = [name for _stage, name, _fn in cr.CHECKS]
    assert len(names) == len(set(names))
    stages = {stage for stage, _n, _f in cr.CHECKS}
    assert stages == {"prereg", "implementation", "release"}


def test_stage_prints_deferred_checks_with_owner(capsys):
    cr.run_stage("prereg", ROOT)
    out = capsys.readouterr().out
    for _stage, name, _fn in cr.CHECKS:
        assert name in out, f"stage output must name every check; missing {name}"
    assert "owned by --stage implementation" in out
    assert "owned by --stage release" in out


def test_implementation_stage_fails_before_implementation_exists(capsys):
    assert cr.run_stage("implementation", ROOT) == 1
    out = capsys.readouterr().out
    assert "cannot pass before the implementation" in out


def test_prereg_stage_on_real_repo_exits_zero(capsys):
    """v28 declares the two noise-floor spans exempt (REG15, PARK9), so the
    tag gate — `--stage prereg` exit 0 — is now reachable, and both applied
    exemptions must be visible in the run with their ids and reasons."""
    assert cr.run_stage("prereg", ROOT) == 0
    out = capsys.readouterr().out
    assert "RESULT: PASS" in out
    assert out.count("EXEMPTION APPLIED") == 2
    assert "id=REG15" in out and "id=PARK9" in out
    assert "reason=" in out


def test_parking_lot_on_real_repo():
    assert cr.check_parking_lot(ROOT) == []


def test_parking_lot_rejects_extra_or_wrong_entries(tmp_path):
    (tmp_path / "PARKING_LOT.md").write_text(
        "# P\n- entry one about a noise-floor fallback for nondeterministic "
        "pipelines; amended registration; evaluation partition\n- entry two\n",
        encoding="utf-8")
    assert any("exactly" in f.message for f in cr.check_parking_lot(tmp_path))
    (tmp_path / "PARKING_LOT.md").write_text("# P\n- something else\n", encoding="utf-8")
    assert cr.check_parking_lot(tmp_path)


def test_reducer_functions_on_real_repo():
    assert cr.check_reducer_functions(ROOT) == []


def test_unit_grammar_on_real_repo():
    assert cr.check_unit_grammar(ROOT) == []


def test_suppression_anchor_on_real_repo():
    assert cr.check_suppression_anchor(ROOT) == []


def test_suppression_anchor_fires_when_prose_drops_the_rule(tmp_path):
    (tmp_path / "PREREG.md").write_text(
        "### 7.2.1 The runtime formulas\nNo suppression here.\n", encoding="utf-8")
    findings = cr.check_suppression_anchor(tmp_path)
    assert any("no longer carries the suppression sentence" in f.message
               for f in findings)


def test_suppression_anchor_fires_when_reducer_side_missing(tmp_path, monkeypatch):
    """The anchor pins both directions: prose declaring the rule while the
    reducer lacks the suppression types must also fire."""
    import protocol.runtime_reference as rr
    (tmp_path / "PREREG.md").write_text(
        "### 7.2.1 The runtime formulas\n"
        "A combination publishes its counts and suppresses its yields, rates, "
        "and gates. \"Scope-eligible case\" means every labelled case in the "
        "body, clean cases included.\n", encoding="utf-8")
    monkeypatch.delattr(rr, "SuppressedMetric")
    findings = cr.check_suppression_anchor(tmp_path)
    assert any("does not implement SuppressedMetric/SuppressedGate" in f.message
               for f in findings)


def test_suppression_anchor_fires_when_definition_dropped(tmp_path):
    """The v30 closure pass tightened the anchor: the rule sentence alone is
    not enough — the 'scope-eligible case' granularity definition the
    whole-body trigger implements must also stay stated."""
    (tmp_path / "PREREG.md").write_text(
        "### 7.2.1 The runtime formulas\n"
        "A combination publishes its counts and suppresses its yields, rates, "
        "and gates when it never applied.\n", encoding="utf-8")
    findings = cr.check_suppression_anchor(tmp_path)
    assert any("no longer defines 'scope-eligible case'" in f.message
               for f in findings)
