"""EXPECTED_OUTPUTS.md is generated, never hand-edited: regenerating must
reproduce the committed file byte for byte."""

from pathlib import Path

from generate_expected_outputs import OUT, render


def test_expected_outputs_file_matches_generator():
    assert OUT.exists(), (
        "EXPECTED_OUTPUTS.md missing — run "
        "python tests/registration/generate_expected_outputs.py")
    assert OUT.read_text(encoding="utf-8") == render(), (
        "EXPECTED_OUTPUTS.md has drifted from the fixtures/reducer — "
        "regenerate and re-review it")
