#!/usr/bin/env python3
"""§63 — D10: ROUND-END RECONCILIATION."""
import pathlib

TOOL = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01/"
                    "tools/check_registration.py")
s = TOOL.read_text(encoding="utf-8")

D10 = '''
# ---------------------------------------------------------------------------
# D10 (R76/§63) - ROUND-END RECONCILIATION.
#
# Every file produced anywhere by a round is either in the repository with a
# manifest entry, or on an explicit EPHEMERAL list with a one-line reason. A
# file in neither is a HALT.
#
# Why this exists: R20 and R24 - the rulings that define what the v30a amendment
# IS - lived only in a temp directory for weeks. So did the entire §9.2 kill-gate
# evidence, and ROUND_STATE.md, the designated post-compaction recovery file. The
# mechanism was that the scratchpad was the working directory and the repository
# was the output, and nothing ever asked "did this round's output land?"
#
# The ephemeral list is NOT a loophole (§63.3). Scratch probes and throwaway
# harnesses belong on it. Analysis, rulings, decision records, and anything a
# later round might cite do not.
# ---------------------------------------------------------------------------

_WORK_ROOT = pathlib.Path(
    "C:/Users/ttbea/AppData/Local/Temp/claude/"
    "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
    "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad")

# Explicit EPHEMERAL list: path suffix -> reason. Each entry is a claim that the
# file is reproducible or throwaway, and is auditable as such.
_EPHEMERAL = (
    ("__pycache__", "compiled bytecode, regenerated on import"),
    ("/applied/", "scratch copy of the repo used to trial an application; the "
                  "applied state is regenerated from SCHEMA_SET_FINAL.md"),
    ("/_verify/", "throwaway verification clone"),
    ("/_verify2/", "throwaway verification clone"),
    ("/_K2_verify/", "throwaway verification clone"),
    ("/s47check/", "throwaway diff-comparison clone"),
    ("/backup_R33/", "pre-edit backup; the post-edit file is in the repo"),
    ("/_retired/", "superseded draft, retired by name"),
    ("/tree/", "snapshot of repo files taken inside a run directory"),
    ("/clone_test/", "clone-test copy of repo files"),
    ("/repo_copy/", "copy of repo files"),
    (".bak", "pre-edit backup of a file whose post-edit state is in the repo"),
    (".pyc", "compiled bytecode"),
)


def check_round_reconciliation(root: Path) -> list[Finding]:
    """D10 - every working-directory file is in the repo or declared ephemeral."""
    findings: list[Finding] = []
    if not _WORK_ROOT.exists():
        return [Finding("round_reconciliation", "(work root)", None,
                        "the working directory is absent - nothing to reconcile",
                        is_note=True)]

    repo_hashes = set()
    for p in root.rglob("*"):
        if p.is_file() and ".git" not in p.parts:
            try:
                repo_hashes.add(hashlib.sha256(p.read_bytes()).hexdigest())
            except OSError:
                pass

    man = root / "evidence/MANIFEST.sha256"
    manifest = set()
    if man.exists():
        manifest = set(re.findall(r"^([0-9a-f]{64})  ",
                                  man.read_text(encoding="utf-8", errors="replace"), re.M))

    unreconciled, ephemeral, large = [], 0, 0
    for p in _WORK_ROOT.rglob("*"):
        if not p.is_file():
            continue
        posix = "/" + p.relative_to(_WORK_ROOT).as_posix()
        if any(tok in posix or posix.endswith(tok) for tok, _ in _EPHEMERAL):
            ephemeral += 1
            continue
        try:
            digest = hashlib.sha256(p.read_bytes()).hexdigest()
        except OSError:
            continue
        if digest in repo_hashes:
            if digest not in manifest and not posix.endswith(".md"):
                pass                       # in repo but outside evidence/: acceptable
            continue
        if p.stat().st_size > 5_000_000:
            large += 1                     # ruled out at §62.1, recorded separately
            continue
        unreconciled.append(posix.lstrip("/"))

    findings.append(Finding("round_reconciliation", "(work root)", None,
                            "reconciled: %d ephemeral, %d large (ruled out at \\u00a762.1)"
                            % (ephemeral, large), is_note=True))
    if unreconciled:
        findings.append(Finding(
            "round_reconciliation", "(work root)", None,
            "D10: %d working file(s) are in NEITHER the repository NOR the ephemeral "
            "list. A file in neither is a HALT - bring it in, or declare it ephemeral "
            "with a reason: %s"
            % (len(unreconciled), ", ".join(sorted(unreconciled)[:6])
               + (" ..." if len(unreconciled) > 6 else ""))))
    else:
        findings.append(Finding("round_reconciliation", "(work root)", None,
                                "D10: every working file is in the repository or "
                                "declared ephemeral", is_note=True))
    return findings

'''

ANCHOR = "def check_phase_arithmetic(root: Path) -> list[Finding]:"
assert s.count(ANCHOR) == 1
s = s.replace(ANCHOR, D10.lstrip("\n") + "\n" + ANCHOR, 1)
REG = '    ("prereg", "manifest_coverage", check_manifest_covers_tree),\n'
assert s.count(REG) == 1
s = s.replace(REG, REG + '    ("prereg", "round_reconciliation", check_round_reconciliation),\n', 1)
if "\nimport pathlib\n" not in s:
    s = s.replace("from pathlib import Path", "import pathlib\nfrom pathlib import Path", 1)
TOOL.write_text(s, encoding="utf-8")
import ast
ast.parse(TOOL.read_text(encoding="utf-8"))
print("D10 installed and registered; syntax OK")
