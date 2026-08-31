"""Known positives for the criterion-5 installability check.

WHY THIS FILE EXISTS AT ALL. `check_installability` returned "the installable
package does not exist yet" for as long as the package had existed. Its
replacement now returns PASS on this repository, and a check whose only
observed behaviour is passing has not been shown to detect anything. R189 §4
item 3 makes the known positive a precondition of believing the clean result,
not a follow-up to it.

ONE VIOLATING SYNTHETIC PER ROUTE, plus a negative control, which is the same
shape as `test_sc7c.py`. Each synthetic differs from the clean one in exactly
one respect, so a firing is attributable to that respect and to nothing else.
A route that fires on the clean control as well would prove nothing, which is
what the control is for.

THE ROUTE THAT MATTERS MOST is `test_unshipped_first_party_package_fires`. That
is not a hypothetical: `leakaudit.contract` imports `protocol.runtime_reference`,
`protocol/` was absent from the first distribution, and the install succeeded
and then raised ModuleNotFoundError on first use. Building is not installing and
installing is not importing.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

import check_registration as cr  # noqa: E402

CHECK = "installability"

CLEAN_PYPROJECT = """\
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "widget"
version = "0.1.0"
requires-python = ">=3.11"
license = "MIT"
license-files = ["LICENSE"]
dependencies = ["numpy>=1.26"]

[tool.setuptools]
packages = ["widget"]

[tool.setuptools.package-dir]
widget = "src/widget"
"""

CLEAN_README = """\
# Widget

Install instructions are in INSTALL.md.
"""

CLEAN_CORE = """\
import os

import numpy


def go():
    return os, numpy
"""


def _mk(tmp_path: Path, *, pyproject: str | None = CLEAN_PYPROJECT,
        readme: str | None = CLEAN_README, core: str = CLEAN_CORE,
        licence: bool = True, install_doc: bool = True,
        helper_pkg: bool = False) -> Path:
    """A synthetic repository that passes, minus whatever the caller removes."""
    if pyproject is not None:
        (tmp_path / "pyproject.toml").write_text(pyproject, encoding="utf-8")
    if readme is not None:
        (tmp_path / "README.md").write_text(readme, encoding="utf-8")
    if install_doc:
        (tmp_path / "INSTALL.md").write_text("python -m pip install .\n",
                                             encoding="utf-8")
    if licence:
        (tmp_path / "LICENSE").write_text("MIT\n", encoding="utf-8")
    pkg = tmp_path / "src" / "widget"
    pkg.mkdir(parents=True)
    (pkg / "__init__.py").write_text("", encoding="utf-8")
    (pkg / "core.py").write_text(core, encoding="utf-8")
    if helper_pkg:
        helper = tmp_path / "helper"
        helper.mkdir()
        (helper / "__init__.py").write_text("VALUE = 1\n", encoding="utf-8")
    return tmp_path


def _failures(root: Path):
    return [f for f in cr.check_installability(root) if not f.is_note]


# ---------------------------------------------------------------------------
# The negative control, first. Every assertion below is worthless without it.
# ---------------------------------------------------------------------------

def test_clean_synthetic_is_silent(tmp_path):
    assert _failures(_mk(tmp_path)) == []


def test_clean_synthetic_still_reports_its_scope_as_a_note(tmp_path):
    notes = [f for f in cr.check_installability(_mk(tmp_path)) if f.is_note]
    assert any("NOT TESTED HERE" in f.message for f in notes), (
        "a passing result that does not say what it did not test is the "
        "silence-as-pass failure this project exists to catch")


def test_unused_exemptions_are_reported_not_hidden(tmp_path):
    """The synthetic imports neither exempted module, so both exemptions fire
    on nothing -- and an exemption nobody exercises is stale or was never
    right. It is a note, never a failure."""
    findings = cr.check_installability(_mk(tmp_path))
    stale = [f for f in findings if "fired on nothing" in f.message]
    assert len(stale) == 2
    assert all(f.is_note for f in stale)


# ---------------------------------------------------------------------------
# Known positives -- one route each
# ---------------------------------------------------------------------------

def test_missing_metadata_fires(tmp_path):
    f = _failures(_mk(tmp_path, pyproject=None))
    assert len(f) == 1 and "no packaging metadata" in f[0].message


def test_unparseable_metadata_fires(tmp_path):
    f = _failures(_mk(tmp_path, pyproject="[project\nname = broken\n"))
    assert len(f) == 1 and "does not parse" in f[0].message


def test_missing_build_backend_fires(tmp_path):
    bad = CLEAN_PYPROJECT.replace(
        'build-backend = "setuptools.build_meta"\n', "")
    f = _failures(_mk(tmp_path, pyproject=bad))
    assert any("build-backend" in x.message for x in f)


@pytest.mark.parametrize("field", ["name", "version", "requires-python"])
def test_missing_required_metadata_field_fires(tmp_path, field):
    bad = "\n".join(l for l in CLEAN_PYPROJECT.split("\n")
                    if not l.startswith(field + " ="))
    f = _failures(_mk(tmp_path, pyproject=bad))
    assert any("declares no %s" % field in x.message for x in f)


def test_absent_licence_expression_fires(tmp_path):
    bad = CLEAN_PYPROJECT.replace('license = "MIT"\n', "")
    f = _failures(_mk(tmp_path, pyproject=bad))
    assert any("no licence to use" in x.message for x in f)


def test_licence_file_named_but_absent_fires(tmp_path):
    f = _failures(_mk(tmp_path, licence=False))
    assert any("no file in the tree matches" in x.message for x in f)


def test_package_dir_that_does_not_exist_fires(tmp_path):
    bad = CLEAN_PYPROJECT.replace('packages = ["widget"]',
                                  'packages = ["widget", "ghost"]')
    f = _failures(_mk(tmp_path, pyproject=bad))
    assert any("not a directory" in x.message for x in f)


def test_unshipped_first_party_package_fires(tmp_path):
    """THE HISTORICAL DEFECT. A shipped module imports a first-party package
    that is not in the shipped list: it installs, then fails to import."""
    f = _failures(_mk(tmp_path, core="import helper\n", helper_pkg=True))
    assert len(f) == 1
    assert "NOT in the shipped package list" in f[0].message
    assert f[0].file.endswith("core.py") and f[0].line == 1


def test_shipping_the_first_party_package_clears_it(tmp_path):
    """The pair to the test above: the same tree, with the package shipped,
    is silent. Without this the check could be firing on the import itself."""
    good = CLEAN_PYPROJECT.replace('packages = ["widget"]',
                                   'packages = ["widget", "helper"]')
    assert _failures(_mk(tmp_path, pyproject=good, core="import helper\n",
                         helper_pkg=True)) == []


def test_undeclared_third_party_import_fires(tmp_path):
    f = _failures(_mk(tmp_path, core="import scipy\n"))
    assert len(f) == 1
    assert "nor a declared dependency" in f[0].message


def test_lazy_import_inside_a_function_is_seen(tmp_path):
    """Indented imports are the ones a stranger meets at run time rather than
    at install time, so they are the ones worth catching."""
    f = _failures(_mk(tmp_path, core="def go():\n    import scipy\n    return scipy\n"))
    assert len(f) == 1 and "nor a declared dependency" in f[0].message


def test_relative_and_stdlib_imports_do_not_fire(tmp_path):
    assert _failures(_mk(
        tmp_path, core="from . import __init__ as _i\nimport json\n")) == []


def test_readme_not_naming_the_install_document_fires(tmp_path):
    f = _failures(_mk(tmp_path, readme="# Widget\n\nNothing here.\n"))
    assert any("never mentions" in x.message for x in f)


def test_readme_asserting_no_implementation_fires(tmp_path):
    f = _failures(_mk(tmp_path, readme=(
        "# Widget\n\nSee INSTALL.md.\n\nNo detector implementation exists.\n")))
    assert any("No detector implementation exists" in x.message for x in f)


def test_the_false_claim_is_caught_across_a_line_wrap(tmp_path):
    """The claim as it actually stood was wrapped. A line-by-line scan would
    have read the wrapped form as clean, which is how it survived."""
    f = _failures(_mk(tmp_path, readme=(
        "# Widget\n\nSee INSTALL.md.\n\nNo detector implementation\nexists.\n")))
    assert any("No detector implementation exists" in x.message for x in f)


def test_the_claim_in_a_blockquote_MARKED_AS_RETIRED_does_not_fire(tmp_path):
    """Keeping a retired claim on the record must stay available, or the check
    would push the repository into deleting its own history to go green."""
    assert _failures(_mk(tmp_path, readme=(
        "# Widget\n\nSee INSTALL.md.\n\n"
        "> This stood here until August and is corrected: No detector\n"
        "> implementation exists.\n"))) == []


def test_an_excused_blockquote_is_reported_with_the_marker_that_excused_it(tmp_path):
    findings = cr.check_installability(_mk(tmp_path, readme=(
        "# Widget\n\nSee INSTALL.md.\n\n"
        "> Retired: No detector implementation exists.\n")))
    notes = [x for x in findings if "blockquote excluded" in x.message]
    assert len(notes) == 1 and notes[0].is_note
    assert "'retired'" in notes[0].message


def test_the_claim_in_an_UNMARKED_blockquote_still_fires(tmp_path):
    """R190 §3. A blockquote is used for emphasis at least as often as for
    quotation, so an unmarked one reads to a human as the page's own voice. The
    exemption is for the record of a withdrawn claim, and it now asks the block
    to say that it is one."""
    f = _failures(_mk(tmp_path, readme=(
        "# Widget\n\nSee INSTALL.md.\n\n"
        "> No detector implementation exists.\n")))
    assert any("No detector implementation exists" in x.message for x in f)


def test_an_unmarked_blockquote_of_innocent_text_is_still_silent(tmp_path):
    """The pair to the test above: including unmarked blockquotes in the scan
    may not make the check fire on blockquotes as such."""
    assert _failures(_mk(tmp_path, readme=(
        "# Widget\n\nSee INSTALL.md.\n\n> A perfectly ordinary quotation.\n"))) == []


def test_the_marker_and_the_claim_may_sit_on_different_lines(tmp_path):
    """Matched over the whole block, because once the text wraps the marker and
    the claim are rarely on the same line -- which is the same wrapping mistake
    the line-by-line body scan already made once."""
    assert _failures(_mk(tmp_path, readme=(
        "# Widget\n\nSee INSTALL.md.\n\n"
        "> No detector implementation exists.\n"
        ">\n"
        "> That sentence is retired.\n"))) == []


# ---------------------------------------------------------------------------
# The claim itself
# ---------------------------------------------------------------------------

def test_this_repository_passes(tmp_path):
    """Criterion 5's state at HEAD, asserted rather than reported. This fails
    the moment the front page or the packaging regresses -- which is the whole
    reason the check was pointed at the real thing."""
    failures = _failures(ROOT)
    assert failures == [], "\n".join(f.render() for f in failures)
