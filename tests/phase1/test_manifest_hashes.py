"""The manifest's hashes match the files it attests. R241, beyond its asks.

**THE GAP WAS DEMONSTRATED, NOT SUSPECTED.** This round edited a file in the
evidence tree, which made its manifest line stale, and **nothing caught it** —
not the suite, not `check_registration --stage prereg`. The gate's
`manifest_coverage` verifies COVERAGE in both directions, which paths are listed
against which are on disk, and its own message names the complement:

> *"`sha256sum -c` cannot see this — it only walks what the manifest lists."*

The two checks are complements and only one of them ran. A file listed with the
wrong hash is covered, so coverage passes; and `sha256sum -c` is a command
somebody has to remember to type.

**MEASURED WHEN THIS WAS WRITTEN: 826 lines, 0 stale, 0 missing.** The hash side
had not drifted — so this pins a property that currently holds rather than
repairing one that had failed, and the reason it held is that the discipline was
kept every round, which is precisely the thing that does not survive the round
where somebody is busy.

Cheap by construction: it hashes the evidence tree once. The manifest cannot
list itself, so that line's absence is expected rather than a gap.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "evidence"
MANIFEST = EVIDENCE / "MANIFEST.sha256"


def _entries():
    """(digest, path-relative-to-evidence) for every attesting line.

    THE RECIPE, stated where it is used: sha256 over the file's RAW BYTES, and
    the line is `<hex>  <path>` with two spaces, paths relative to `evidence/`.
    R229 §0 — a digest carries its recipe, and a reader who cannot reproduce the
    number is reading an authoritative-looking figure with no frame.
    """
    out = []
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "  " not in line:
            continue
        digest, rel = line.split("  ", 1)
        out.append((digest, rel.strip()))
    return out


def test_the_manifest_has_entries_to_check():
    """A pass over an empty manifest would read exactly like a real one — the
    zero-coverage shape OPERATING_RULES §3 bans."""
    assert len(_entries()) > 500, (
        "the manifest yielded %d entries, too few to be this one; every "
        "assertion below would then be made over almost nothing"
        % len(_entries()))


def test_EVERY_manifest_hash_MATCHES_the_file_it_attests():
    """The side `manifest_coverage` explicitly does not cover."""
    stale, absent = [], []
    for digest, rel in _entries():
        p = EVIDENCE / rel
        if not p.is_file():
            absent.append(rel)
            continue
        if hashlib.sha256(p.read_bytes()).hexdigest() != digest:
            stale.append(rel)
    assert not stale, (
        "these files have changed since the manifest attested them, so the "
        "manifest states a hash the file does not have. `manifest_coverage` "
        "passes on this, because the path IS listed -- coverage and content "
        "are different claims: %s" % stale)
    assert not absent, (
        "the manifest attests files that are not on disk: %s" % absent)


def test_the_manifest_does_not_attest_ITSELF():
    """It cannot: writing its own hash into itself changes the hash. Asserted so
    the absence reads as a property rather than an oversight."""
    assert not [rel for _, rel in _entries()
                if rel.endswith("MANIFEST.sha256")]


def test_a_TAMPERED_file_is_CAUGHT(tmp_path):
    """The wrong case. A checker that hashed the manifest's own text, or
    compared a digest to itself, would pass every assertion above."""
    ev = tmp_path / "evidence"
    (ev / "sub").mkdir(parents=True)
    target = ev / "sub" / "a.txt"
    target.write_bytes(b"original")
    good = hashlib.sha256(b"original").hexdigest()
    (ev / "MANIFEST.sha256").write_text(
        "# header\n%s  sub/a.txt\n" % good, encoding="utf-8")

    import test_manifest_hashes as m
    saved_ev, saved_man = m.EVIDENCE, m.MANIFEST
    m.EVIDENCE, m.MANIFEST = ev, ev / "MANIFEST.sha256"
    try:
        m.test_EVERY_manifest_hash_MATCHES_the_file_it_attests()   # clean
        target.write_bytes(b"tampered")
        try:
            m.test_EVERY_manifest_hash_MATCHES_the_file_it_attests()
        except AssertionError as e:
            assert "sub/a.txt" in str(e)
        else:
            raise AssertionError(
                "a changed file was NOT caught, so this checker cannot detect "
                "the one thing it exists to detect")
    finally:
        m.EVIDENCE, m.MANIFEST = saved_ev, saved_man
