"""The manifest's hashes match the files it attests. R241, R242, R243 §1.

**THE GAP WAS DEMONSTRATED, NOT SUSPECTED.** R241 edited a file in the evidence
tree, its manifest line went stale, and nothing caught it. R242 established why
by producing the defect: a manifest line corrupted to a hash of zeros left
`check_registration.py --stage prereg` reporting exactly what it reports on a
clean tree. The gate's `manifest_coverage` asks which paths are listed against
which are on disk and passes on a listed path whatever the file now contains,
and its own message names the complement it does not perform:

> *"`sha256sum -c` cannot see this — it only walks what the manifest lists."*

**THIS FILE TESTS THE SHIPPED INSTRUMENT AND DOES NOT RE-IMPLEMENT IT.**
`tools/manifest_verify.py` is the one implementation; certification runs it
beside the frozen checker. An earlier draft of this file carried its own copy of
the verification, which is the two-lists hazard in the file written to close an
integrity gap — two statements of one rule, free to drift, and the drift would
be invisible precisely because both would be green.

**WHY A SIBLING INSTRUMENT RATHER THAN A CHECK IN THE GATE** is recorded in
`tools/manifest_verify.py`: `check_registration.py` is frozen, differences from
the tagged instrument are ruled against a ceiling of four, and an addition does
not need a slot when it can stand beside.
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
for p in (str(ROOT), str(ROOT / "tools")):
    if p not in sys.path:
        sys.path.insert(0, p)

import manifest_verify as mv                                       # noqa: E402


# ---------------------------------------------------------------------------
# the real tree
# ---------------------------------------------------------------------------
def test_the_manifest_has_entries_to_check():
    """A pass over an empty manifest would read exactly like a real one — the
    zero-coverage shape `OPERATING_RULES.md` §3 bans."""
    assert len(mv.entries()) > 500, (
        "the manifest yielded %d attesting lines, too few to be this one; "
        "every assertion below would be made over almost nothing"
        % len(mv.entries()))


def test_EVERY_manifest_hash_MATCHES_the_file_it_attests():
    r = mv.verify()
    assert r["checked"], "nothing was verified, so this reports nothing"
    assert not r["stale"], (
        "these files have changed since the manifest attested them, so the "
        "manifest states a hash the file does not have and a commit would ship "
        "a false attestation. `manifest_coverage` passes on this, because the "
        "path IS listed -- coverage and content are different claims: %s"
        % r["stale"])
    assert not r["absent"], (
        "the manifest attests files that are not on disk: %s" % r["absent"])


def test_the_manifest_does_not_attest_ITSELF():
    """It cannot: writing its own hash into itself changes the hash. Asserted so
    the absence reads as a property rather than an oversight."""
    assert not [rel for _, rel in mv.entries()
                if rel.endswith("MANIFEST.sha256")]


def test_the_verifier_runs_CLEAN_as_a_command():
    """Certification runs it as a command, so the command is what is checked."""
    assert mv.main([]) == 0


# ---------------------------------------------------------------------------
# the wrong cases, against the SHIPPED functions
# ---------------------------------------------------------------------------
def _tree(tmp_path, body=b"original", digest=None):
    ev = tmp_path / "evidence"
    (ev / "sub").mkdir(parents=True)
    (ev / "sub" / "a.txt").write_bytes(body)
    d = digest or hashlib.sha256(body).hexdigest()
    man = ev / "MANIFEST.sha256"
    man.write_text("# header\n%s  sub/a.txt\n" % d, encoding="utf-8")
    return man, tmp_path


def test_a_TAMPERED_file_is_CAUGHT(tmp_path):
    """The wrong case. A checker that hashed the manifest's own text, or
    compared a digest to itself, would pass every assertion above."""
    man, repo = _tree(tmp_path)
    assert mv.verify(man, repo)["stale"] == []
    (repo / "evidence" / "sub" / "a.txt").write_bytes(b"tampered")
    assert mv.verify(man, repo)["stale"] == ["sub/a.txt"], (
        "a changed file was NOT caught, so this cannot detect the one thing it "
        "exists to detect")


def test_an_ATTESTED_FILE_THAT_VANISHES_is_caught(tmp_path):
    man, repo = _tree(tmp_path)
    (repo / "evidence" / "sub" / "a.txt").unlink()
    r = mv.verify(man, repo)
    assert r["absent"] == ["sub/a.txt"] and r["checked"] == 0


def test_ZERO_COVERAGE_IS_NOT_A_PASS(tmp_path):
    """A manifest with no attesting lines verifies nothing, and saying so with
    silence would read exactly like verifying everything."""
    ev = tmp_path / "evidence"
    ev.mkdir(parents=True)
    man = ev / "MANIFEST.sha256"
    man.write_text("# header only, no lines\n", encoding="utf-8")
    assert mv.verify(man, tmp_path)["checked"] == 0


def test_a_MISSING_manifest_is_UNVERIFIABLE_not_clean(tmp_path):
    """Absence of the manifest is not agreement with it."""
    with pytest.raises(mv.ManifestUnverifiable):
        mv.entries(tmp_path / "nope.sha256")


def test_the_UP_PATHS_resolve_to_the_repository_root(tmp_path):
    """`../` lines attest repository-root files, and resolving them against
    `evidence/` instead would look for files that are not there and report six
    spurious absences."""
    assert mv.resolve("../PRACTICES.md", ROOT) == ROOT / "PRACTICES.md"
    assert mv.resolve("session/X.md", ROOT) == ROOT / "evidence" / "session" / "X.md"
