#!/usr/bin/env python3
"""§29.3 — D7: declaration hash/size literals must derive from the file."""
import pathlib

TOOL = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01/"
                    "tools/check_registration.py")
s = TOOL.read_text(encoding="utf-8")

D7 = '''
# ---------------------------------------------------------------------------
# D7 (R68/§29.3) — a declaration hash or byte size is a VERIFICATION VALUE.
#
# A stale one does not merely mislead: a reader who checks it against the file
# sees a mismatch, and a hash mismatch inside an evidence tree reads as tamper
# evidence. That is a different class from a stale prose count, and it is why
# this check exists separately from D1.
#
# POPULATION INCLUDES TABLE ROWS. A3's first sweep skipped lines beginning with
# `|` and therefore never saw three of these sites (R68/§30.1).
#
# Scoped to values ATTRIBUTED TO THE DECLARATION BY FILENAME. A hash on a line
# that merely says "the declaration" may belong to PREREG.md or to the evidence
# tree; requiring the filename is what keeps this from flagging those.
# ---------------------------------------------------------------------------

_DECL_REL = "AVAILABILITY_DECLARATION.md"
_D7_HEX = re.compile(r"\\b([0-9a-f]{8,64})\\u2026?")
_D7_SIZE = re.compile(r"\\b([\\d,]{4,})\\s*(bytes|lines)\\b")

# (path, line) -> (pin, reason). Dated records and historical narrative.
_D7_EXEMPT = {
    ("evidence/author_review/READ_THROUGH_PACKAGE.md", 1): (
        "Author read-through package",
        "the frozen author-read baseline; its whole purpose is to record the "
        "bytes as they were when the author read them"),
    ("evidence/ceremony/CEREMONY_COMMANDS.md", 26): (
        "do not read the size or hash from here",
        "the stale value appears only inside the note recording that it WAS stale"),
    ("evidence/ceremony/COMMIT_PLAN.md", 80): (
        "derived not transcribed",
        "same - the old value is quoted in the note recording the correction"),
    ("evidence/ceremony/DEVIATIONS_DRAFT.md", 310): (
        "for several rounds after the file had moved",
        "same - historical note"),
    ("evidence/fixture_spike/f4/DECLARATION_POINTER.md", 25): (
        "The declaration moved again",
        "historical narrative: records a past transition, from-hash and to-hash"),
    ("evidence/fixture_spike/f4/DECLARATION_POINTER.md", 102): (
        "That moved the declaration to",
        "historical narrative"),
    ("evidence/fixture_spike/f4/DECLARATION_POINTER.md", 117): (
        "still read",
        "historical narrative - records the lateness that R15 prohibits"),
    ("evidence/ceremony/COMMIT_PLAN.md", 111): (
        "tracked the declaration at 3,650 lines",
        "TRUE of ffa6d94, verified: `git show ffa6d94:AVAILABILITY_DECLARATION.md "
        "| wc -l` = 3650. A claim about a commit, not about the working tree"),
}


def check_declaration_values(root: Path) -> list[Finding]:
    """D7 - every declaration hash/size literal agrees with the file."""
    decl = root / _DECL_REL
    if not decl.exists():
        return [Finding("declaration_values", _DECL_REL, None,
                        "the declaration is missing; its recorded values cannot be checked")]
    raw = decl.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    nbytes, nlines = len(raw), raw.count(b"\\n")
    findings = [Finding("declaration_values", _DECL_REL, None,
                        "derived: sha256 %s\\u2026 / %d bytes / %d lines"
                        % (digest[:12], nbytes, nlines), is_note=True)]

    corpus = [Path(p) for p in ("AVAILABILITY_DECLARATION.md", "PREREG.md", "DESIGN.md",
                                "HISTORY.md", "README.md", "PRACTICES.md",
                                "PRIOR_ART_VERIFICATION.md", "DEVIATIONS.md")]
    corpus += sorted((root / "evidence").rglob("*.md")) if (root / "evidence").exists() else []
    seen: set[tuple[str, int]] = set()

    for path in corpus:
        full = path if path.is_absolute() else root / path
        if not full.exists() or not full.is_file():
            continue
        rel = full.relative_to(root).as_posix()
        for idx, line in enumerate(full.read_text(encoding="utf-8", errors="replace").split("\\n"), 1):
            if _DECL_REL not in line:            # attributed by FILENAME, not "the declaration"
                continue
            bad = []
            for hx in _D7_HEX.findall(line):
                if hx.isdigit() or len(hx) < 8:
                    continue
                if not digest.startswith(hx):
                    bad.append("sha256 %s\\u2026" % hx[:12])
            for val, unit in _D7_SIZE.findall(line):
                num = int(val.replace(",", ""))
                if unit == "bytes" and num != nbytes:
                    bad.append("%s bytes" % val)
                if unit == "lines" and num != nlines:
                    bad.append("%s lines" % val)
            if not bad:
                continue
            key = (rel, idx)
            entry = _D7_EXEMPT.get(key)
            if entry is None:
                findings.append(Finding(
                    "declaration_values", rel, idx,
                    "D7: states %s for %s; the file is sha256 %s\\u2026 / %d bytes / %d lines. "
                    "A stale verification value reads as tamper evidence. Derive it, or "
                    "exempt this line as a dated record with its reason."
                    % (", ".join(bad), _DECL_REL, digest[:12], nbytes, nlines)))
                continue
            pin, reason = entry
            if pin not in line:
                findings.append(Finding(
                    "declaration_values", rel, idx,
                    "D7: exemption DRIFTED - pinned text %r is no longer on this line" % pin))
            else:
                seen.add(key)
                findings.append(Finding("declaration_values", rel, idx,
                                        "exempt - %s" % reason, is_note=True))

    for key in _D7_EXEMPT:
        if key not in seen:
            findings.append(Finding(
                "declaration_values", key[0], key[1],
                "D7: this exemption fired on nothing - the line moved or its text changed"))
    return findings

'''

ANCHOR = "def check_phase_arithmetic(root: Path) -> list[Finding]:"
assert s.count(ANCHOR) == 1
s = s.replace(ANCHOR, D7.lstrip("\n") + "\n" + ANCHOR, 1)

REG = '    ("prereg", "hash_set_single_source", check_hash_set_single_source),\n'
assert s.count(REG) == 1
s = s.replace(REG, REG + '    ("prereg", "declaration_values", check_declaration_values),\n', 1)

TOOL.write_text(s, encoding="utf-8")
import ast
ast.parse(TOOL.read_text(encoding="utf-8"))
print("D7 installed and registered; syntax OK")
