"""Registration checker (PREREG §6.8), staged.

Stages: prereg | implementation | release. Every stage prints the checks it
defers and the stage that owns them -- an omitted branch is a failure, not a
pass. The tag gate is `--stage prereg` exit 0.

No exemption may be added to make current files pass: an exemption requires an
affirmative reason grounded in PREREG.md. The exemptions below are the ones
PREREG §6.8 itself declares (the banned-list block, PREREG §0.4, the
parenthetical ledger notes / HISTORY.md markers, PARKING_LOT.md), and
HISTORY.md is out of scan scope because it declares itself non-normative.

The banned-vocabulary and deletion-certificate scans read PREREG.md and
DESIGN.md. The single-source scan (PREREG §0.2.1) reads every markdown file in
the repository except the ones named, with reasons, in
SINGLE_SOURCE_EXCLUDED_* below — see the comment block above those constants
for why it is scope-by-exclusion rather than a fixed file list.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import tomllib
from dataclasses import dataclass
import pathlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@dataclass(frozen=True)
class Finding:
    check: str
    file: str
    line: int | None
    message: str
    is_note: bool = False  # notes are printed for auditability, never failures

    def render(self) -> str:
        loc = f"{self.file}:{self.line}" if self.line else self.file
        tag = "note: " if self.is_note else ""
        return f"    {tag}{loc}: {self.message}"


# ---------------------------------------------------------------------------
# Shared parsing
# ---------------------------------------------------------------------------

_HEADING = re.compile(r"^(#{2,4})\s+(\d+(?:\.\d+)*)\.?\s", re.M)


def sections_of(text: str) -> dict[str, str]:
    """Map section number ('6.6.1') -> body text (heading line included)."""
    hits = [(m.start(), m.group(2)) for m in _HEADING.finditer(text)]
    out: dict[str, str] = {}
    for i, (start, num) in enumerate(hits):
        end = hits[i + 1][0] if i + 1 < len(hits) else len(text)
        out.setdefault(num, "")
        out[num] += text[start:end]
    return out


_LEDGER_NOTE = re.compile(r"\*\((?:[^()]|\([^()]*\))*?\)\*")
_HEADING_LINE = re.compile(r"^(#{2,4})\s+(\d+(?:\.\d+)*)\.?\s")
_BLOCK_OPEN = "<!-- banned-list"
_BLOCK_CLOSE = "/banned-list -->"


def _prereg_version(text: str) -> int | None:
    m = re.search(r"\*\*Status:\*\*\s*v(\d+)", text)
    return int(m.group(1)) if m else None


def _is_historical_note(span: str, current_version: int | None) -> bool:
    """A parenthetical ledger note references HISTORY.md or a SUPERSEDED
    version. A note naming only the current version is normative prose in a
    historical costume and stays in the scan."""
    if "HISTORY.md" in span:
        return True
    versions = [int(n) for n in re.findall(r"\bv(\d+)\b", span)]
    if current_version is None:
        return bool(versions)
    return any(n < current_version for n in versions)


def section_line_range(text: str, num: str) -> tuple[int, int] | None:
    """1-based inclusive line range of a section — exemption by explicit
    range, never by content matching (PREREG §6.8)."""
    lines = text.splitlines()
    heads = []
    for i, line in enumerate(lines, start=1):
        m = _HEADING_LINE.match(line)
        if m:
            heads.append((i, m.group(2)))
    for idx, (start, n) in enumerate(heads):
        if n == num:
            end = heads[idx + 1][0] - 1 if idx + 1 < len(heads) else len(lines)
            return (start, end)
    return None


def _banned_list_block_range(text: str) -> tuple[int, int] | None:
    """Line range of the first PROPERLY CLOSED banned-list block. An unclosed
    block exempts nothing (and region_findings flags it)."""
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines, start=1):
        if start is None and _BLOCK_OPEN in line:
            start = i
        elif start is not None and _BLOCK_CLOSE in line:
            return (start, i)
    return None


def region_findings(path: Path, text: str, check: str) -> list[Finding]:
    """Validate the exempt-region machinery itself. PREREG §6.8 declares
    exactly one banned-list block, in §6.8 of PREREG.md — a decoy block
    elsewhere, a second block, or an unclosed one is a failure, and none of
    them exempts anything."""
    f: list[Finding] = []
    lines = text.splitlines()
    opens = [i for i, ln in enumerate(lines, start=1) if _BLOCK_OPEN in ln]
    if path.name != "PREREG.md":
        for i in opens:
            f.append(Finding(check, path.name, i,
                             "banned-list block outside PREREG.md §6.8 exempts "
                             "nothing and is itself a violation (PREREG §6.8)"))
        return f
    closed = _banned_list_block_range(text)
    if opens and closed is None:
        f.append(Finding(check, path.name, opens[0],
                         "unclosed banned-list block would exempt everything "
                         "after it; it exempts nothing and fails (PREREG §6.8)"))
    for i in opens[1:]:
        f.append(Finding(check, path.name, i,
                         "second banned-list block: §6.8 declares exactly one"))
    return f


# ---------------------------------------------------------------------------
# The availability declaration's decision-log tail: a declared historical
# region, exempt ONLY WHILE IT IS FROZEN.
#
# WHAT THE REGION IS. AVAILABILITY_DECLARATION.md ends with an append-only
# verbatim record of the working resolutions that were adopted while the
# amendment was drafted. The declaration declares it, by explicit range, at
# §D.1 item k: "Working-resolution record R1-R9 and R11-R13 (no R10), verbatim
# | file tail | this file (frozen byte-identical; the tail heading occurs
# exactly once, and the tail runs unbroken to EOF)."
#
# WHY IT IS EXEMPT. The record quotes resolutions in the words they were
# adopted in, and some of those words are rule-shaped -- R11 says "Criterion-1
# denominator derives from the DECLARED MAP", which is a denominator
# constitution and fires the scan. But a record of what was resolved is not a
# statement of a rule: the rule itself is registered in PREREG.md (SC-4 for the
# partition and the criterion-1 denominator, SC-3 for the amended acceptance
# criterion 3), which is where §0.2.1 requires it, and the tail is the record
# OF that rule, never its only home. Scanning a frozen quotation of adopted
# text finds the history, not a second normative copy.
#
# WHY THE EXEMPTION IS CONDITIONAL, AND THIS IS THE POINT. The argument above
# holds only while the region is what it claims to be: frozen. An exemption
# that survived an edit would be a licence to add rule-shaped text to the one
# region nothing scans -- the exact hole scope-by-exclusion exists to close.
# So the range is exempt ONLY while its content hash equals the value recorded
# below. Change one byte and the region is scanned again, and every rule-shaped
# line in it is reported. The exemption is not a hole in the freeze; it is an
# enforcement of it, and it is the only mechanism here that fails CLOSED on an
# edit rather than open.
#
# ORDERING CONSTRAINT, LOAD-BEARING. This exemption is sound only once PREREG.md
# carries the rules the tail records. Until SC-4 lands, the tail's R11 text is
# the rule's ONLY statement, and skipping it would mask a real §0.2.1 defect
# rather than excuse a quotation. The checker edit and the amendment therefore
# land in the SAME commit; the ceremony command file carries this as a gate.
#
# UPDATING THE HASH. It is updated only when the tail legitimately grows -- the
# record is append-only, so a new adopted resolution is appended and the hash is
# re-recorded in the same commit, with the appended text visible in that commit's
# diff. A hash updated in a commit that does not also show what changed in the
# region is a hash updated to make something pass, which §6.8's exemption
# standard forbids ("an exemption that cannot be audited is not one").
_DECLARATION_TAIL_HEADING = "## Decision log — working resolutions"
_DECLARATION_TAIL_SHA256 = (
    "ad8b327707ecb9627b56b9e74e757facad55fb14e87a3082470fd7398bf267e0")


def declaration_tail_range(text: str) -> tuple[int, int] | None:
    """The declared tail range (1-based, inclusive, heading to EOF) if and only
    if the region is present exactly once AND still hashes to the recorded
    value. Returns None otherwise, which means the region is scanned.

    Fails closed on every ambiguity: a heading that appears zero times or more
    than once is not the declared region, and an unrecognised hash is not the
    frozen record."""
    lines = text.split("\n")
    starts = [i for i, ln in enumerate(lines)
              if ln.startswith(_DECLARATION_TAIL_HEADING)]
    if len(starts) != 1:
        return None
    first = starts[0]
    region = "\n".join(lines[first:])
    digest = hashlib.sha256(region.encode("utf-8")).hexdigest()
    if digest != _DECLARATION_TAIL_SHA256:
        return None
    return (first + 1, len(lines))


def normative_lines(path: Path, text: str) -> list[tuple[int, str]]:
    """Lines of a normative file with PREREG §6.8's declared historical
    regions removed — by explicit range, never by content matching. For
    PREREG.md: the single closed banned-list block, §0.4's line range, and
    parenthetical ledger notes referencing HISTORY.md or a superseded
    version. For AVAILABILITY_DECLARATION.md: the decision-log tail declared
    at §D.1 item k, and only while it hashes to the recorded frozen value —
    see the comment block above. DESIGN.md has no declared historical regions
    left (its numbered lessons moved to HISTORY.md), so every DESIGN line is
    scanned."""
    lines = text.splitlines()
    keep: list[tuple[int, str]] = []
    skip_ranges: list[tuple[int, int]] = []
    version = None
    if path.name == "PREREG.md":
        version = _prereg_version(text)
        block = _banned_list_block_range(text)
        if block:
            skip_ranges.append(block)
        sect_04 = section_line_range(text, "0.4")
        if sect_04:
            skip_ranges.append(sect_04)
    elif path.name == "AVAILABILITY_DECLARATION.md":
        tail = declaration_tail_range(text)
        if tail:
            skip_ranges.append(tail)
    for i, line in enumerate(lines, start=1):
        if any(lo <= i <= hi for lo, hi in skip_ranges):
            continue
        if path.name == "PREREG.md":
            line = _LEDGER_NOTE.sub(
                lambda m: " " * len(m.group(0))
                if _is_historical_note(m.group(0), version) else m.group(0),
                line)
        keep.append((i, line))
    return keep


def _normalize(s: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[-_/]", " ", s.lower()))


# ---------------------------------------------------------------------------
# prereg-stage checks
# ---------------------------------------------------------------------------

REQUIRED_PATHS = (
    "PREREG.md", "DESIGN.md", "HISTORY.md", "DEVIATIONS.md", "PARKING_LOT.md",
    "VALIDATED_CONFIG.toml", "protocol/runtime_reference.py",
    "tools/check_registration.py", "tests/registration",
)

REQUIRED_PREREG_SECTIONS = (
    "0.1", "0.2", "0.2.1", "2.3", "2.6", "2.7", "3.1", "3.2", "4.3", "6.6",
    "6.6.1", "6.8", "6.10", "6.11", "7.0", "7.1", "7.2", "7.2.1", "7.7",
    "7.8", "8.3", "8.5", "10.2", "11",
)


def check_structure(root: Path) -> list[Finding]:
    f: list[Finding] = []
    for rel in REQUIRED_PATHS:
        if not (root / rel).exists():
            f.append(Finding("structure", rel, None,
                             "required by PREREG §11 item 1 and absent"))
    # §11 item 1 requires tests/registration to CARRY the §6.6.1 suite —
    # an empty directory is not a suite.
    tests_dir = root / "tests" / "registration"
    if tests_dir.is_dir():
        if not list(tests_dir.glob("test_*.py")):
            f.append(Finding("structure", "tests/registration", None,
                             "no test_*.py files: §11 item 1 requires the "
                             "exhaustive small-trace suite of §6.6.1"))
        for required in ("traces.py", "EXPECTED_OUTPUTS.md"):
            if not (tests_dir / required).exists():
                f.append(Finding("structure", f"tests/registration/{required}",
                                 None, "suite artifact required by §6.6.1 and absent"))
    prereg = root / "PREREG.md"
    if prereg.exists():
        secs = sections_of(prereg.read_text(encoding="utf-8"))
        for num in REQUIRED_PREREG_SECTIONS:
            if num not in secs:
                f.append(Finding("structure", "PREREG.md", None,
                                 f"section §{num} not found (renumber drift?)"))
    return f


def check_config_schema(root: Path) -> list[Finding]:
    path = root / "VALIDATED_CONFIG.toml"
    if not path.exists():
        return [Finding("config_schema", "VALIDATED_CONFIG.toml", None, "missing")]
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as e:
        return [Finding("config_schema", "VALIDATED_CONFIG.toml", None, f"does not parse: {e}")]
    f = []
    validated = data.get("validated")
    if not isinstance(validated, dict):
        return [Finding("config_schema", "VALIDATED_CONFIG.toml", None,
                        "no [validated.*] tables (PREREG §6.3)")]
    for part in ("runtime", "split", "static", "review"):
        if part not in validated:
            f.append(Finding("config_schema", "VALIDATED_CONFIG.toml", None,
                             f"[validated.{part}] placeholder missing (PREREG §6.3)"))
    return f


_STOPWORDS = {
    "the", "and", "its", "is", "are", "a", "an", "per", "only", "what",
    "makes", "never", "each", "with", "this", "that", "how", "of", "to",
    "in", "by", "for", "or", "not", "no", "under"}


def check_lock_table(root: Path) -> list[Finding]:
    """Each §0.1 lock-table row's target section must contain the row's key
    phrase -- an existence check cannot catch topic drift after a renumber
    (PREREG §0.1, §6.8)."""
    text = (root / "PREREG.md").read_text(encoding="utf-8")
    secs = sections_of(text)
    body = secs.get("0.1")
    if body is None:
        return [Finding("lock_table", "PREREG.md", None, "§0.1 not found")]
    f: list[Finding] = []
    rows = re.findall(r"^\|\s*(?!Locked here)([^|]+?)\s*\|\s*§([\d.]+)\s*\|", body, re.M)
    if len(rows) < 5:
        f.append(Finding("lock_table", "PREREG.md", None,
                         f"only {len(rows)} lock-table rows parsed from §0.1"))
    # A row the regex cannot parse (e.g. two section targets in one cell) must
    # fail loudly, not silently go unchecked.
    row_re = re.compile(r"^\|\s*(?!Locked here)([^|]+?)\s*\|\s*§([\d.]+)\s*\|")
    for line in body.splitlines():
        if line.startswith("|") and "§" in line and not row_re.match(line):
            f.append(Finding("lock_table", "PREREG.md", None,
                             f"lock-table row failed to parse and went "
                             f"unchecked: {line[:90]!r}"))
    for phrase, target in rows:
        target = target.rstrip(".")
        section = secs.get(target)
        if section is None:
            f.append(Finding("lock_table", "PREREG.md", None,
                             f"lock row targets §{target}, which does not exist"))
            continue
        words = [w for w in re.findall(r"[a-z]{3,}", phrase.lower())
                 if w not in _STOPWORDS]
        needed = min(2, len(words)) or 1
        section_norm = _normalize(section)
        present = [w for w in words if w in section_norm]
        if len(present) < needed:
            f.append(Finding(
                "lock_table", "PREREG.md", None,
                f"topic drift: §{target} contains {len(present)} of key words "
                f"{words} for lock row {phrase!r}"))
    return f


def banned_terms(root: Path) -> list[str]:
    text = (root / "PREREG.md").read_text(encoding="utf-8")
    m = re.search(r"<!-- banned-list.*?-->(.*?)<!-- /banned-list -->", text, re.S)
    if not m:
        return []
    return re.findall(r"`([^`]+)`", m.group(1))


# PREREG §6.8: a deletion is complete only when the symbol's inbound
# normative reference set is empty. Symbols deleted by v19-v27 beyond the
# banned vocabulary itself. These are code symbols (state names, config
# fields), and the documents mark symbols with backticks, so the scan is
# code-context only -- plain-English homographs ("the superseded results",
# §0.2.1) are not references to the deleted state name.
DELETED_SYMBOLS = ("superseded", "select_fixture_branch")


def _scan_code_symbols(root: Path, symbols: tuple[str, ...], check: str) -> list[Finding]:
    f: list[Finding] = []
    for name in ("PREREG.md", "DESIGN.md"):
        path = root / name
        if not path.exists():
            continue
        for lineno, line in normative_lines(path, path.read_text(encoding="utf-8")):
            for span in re.findall(r"`([^`]*)`", line):
                for sym in symbols:
                    if re.search(r"(?<![A-Za-z0-9_])" + re.escape(sym) + r"(?![A-Za-z0-9_])", span):
                        f.append(Finding(check, name, lineno,
                                         f"deleted symbol {sym!r} referenced in normative "
                                         f"range: {line.strip()[:100]!r}"))
    return f


# PREREG §6.8 (v28): exactly two exemptions are declared, both with reasons.
# No wildcard — an undeclared id is a failure, not a third exemption.
DECLARED_EXEMPT_IDS = frozenset({"REG15", "PARK9"})

_EXEMPT_MARKER = re.compile(r"<!--\s*banned-exempt:\s*(.*?)-->")


def _exemptions(path: Path, text: str) -> tuple[list[Finding], dict[int, tuple[str, str]]]:
    """Parse banned-exempt markers. Returns (findings, {exempt line -> (id, reason)}).

    A marker must be a standalone comment line immediately above its block,
    and exempts exactly the next line — nothing wider. Each declared id marks
    one span: PREREG §6.8 declares two spans with two ids, so a reused id is
    a wildcard and fails. Every accepted exemption is returned so the run
    prints it; an exemption that cannot be audited is not one."""
    findings: list[Finding] = []
    exempt: dict[int, tuple[str, str]] = {}
    uses: dict[str, int] = {}
    lines = text.splitlines()
    for i, line in enumerate(lines, start=1):
        m = _EXEMPT_MARKER.search(line)
        if not m:
            continue
        if not re.fullmatch(r"<!--\s*banned-exempt:[^>]*-->", line.strip()):
            findings.append(Finding(
                "banned_vocabulary", path.name, i,
                "banned-exempt marker must be a standalone line immediately "
                "above the exempt block; an inline marker mistargets (PREREG §6.8)"))
            continue
        attrs = m.group(1)
        id_m = re.search(r'id=([\w-]+)', attrs)
        reason_m = re.search(r'reason="([^"]+)"', attrs)
        if not id_m or not reason_m:
            findings.append(Finding(
                "banned_vocabulary", path.name, i,
                "banned-exempt marker without an id and reason is invalid — "
                "an exemption that cannot be audited is not one (PREREG §6.8)"))
            continue
        ex_id = id_m.group(1)
        if ex_id not in DECLARED_EXEMPT_IDS:
            findings.append(Finding(
                "banned_vocabulary", path.name, i,
                f"banned-exempt id {ex_id!r} is not one of the two declared "
                f"exemptions {sorted(DECLARED_EXEMPT_IDS)} (PREREG §6.8); no wildcard"))
            continue
        uses[ex_id] = uses.get(ex_id, 0) + 1
        if uses[ex_id] > 1:
            findings.append(Finding(
                "banned_vocabulary", path.name, i,
                f"declared exemption id {ex_id!r} used more than once — two "
                "spans, two ids, no wildcard (PREREG §6.8)"))
            continue
        target = lines[i] if i < len(lines) else ""  # the line right after the marker
        if not target.strip() or target.lstrip().startswith("<!--"):
            findings.append(Finding(
                "banned_vocabulary", path.name, i,
                "banned-exempt marker is not immediately above a content "
                "block; a floating exemption exempts nothing (PREREG §6.8)"))
            continue
        exempt[i + 1] = (ex_id, reason_m.group(1))
    return findings, exempt


def check_banned_vocabulary(root: Path) -> list[Finding]:
    terms = banned_terms(root)
    findings: list[Finding] = []
    if not terms:
        findings.append(Finding(
            "banned_vocabulary", "PREREG.md", None,
            "no closed banned-list block found in §6.8; the term list is "
            "unreadable and nothing can be scanned against it"))
    for name in ("PREREG.md", "DESIGN.md"):
        path = root / name
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        findings.extend(region_findings(path, text, "banned_vocabulary"))
        marker_findings, exempt = _exemptions(path, text)
        findings.extend(marker_findings)
        for lineno, (ex_id, reason) in sorted(exempt.items()):
            findings.append(Finding(
                "banned_vocabulary", name, lineno,
                f"EXEMPTION APPLIED id={ex_id} reason={reason!r}", is_note=True))
        for lineno, line in normative_lines(path, text):
            if lineno in exempt:
                continue
            norm = _normalize(line)
            for term in terms:
                pat = r"(?<![a-z0-9])" + re.escape(_normalize(term)) + r"(?![a-z0-9])"
                if re.search(pat, norm):
                    findings.append(Finding(
                        "banned_vocabulary", name, lineno,
                        f"deleted/banned term {term!r} in normative range: "
                        f"{line.strip()[:100]!r}"))
    return findings


def check_deletion_certificate(root: Path) -> list[Finding]:
    findings = _scan_code_symbols(root, DELETED_SYMBOLS, "deletion_certificate")
    config = (root / "VALIDATED_CONFIG.toml")
    if config.exists():
        text = config.read_text(encoding="utf-8")
        for sym in (*DELETED_SYMBOLS, "comparison_mode", "routing_policy",
                    "noise_floor", "on_determinism_failure"):
            if sym in text:
                findings.append(Finding("deletion_certificate", "VALIDATED_CONFIG.toml",
                                        None, f"deleted config symbol {sym!r} present"))
    return findings


# ---------------------------------------------------------------------------
# Single-source scan scope (PREREG §0.2.1)
# ---------------------------------------------------------------------------
#
# WHY THIS SCAN READS MORE THAN DESIGN.md
# ---------------------------------------
# Until this change check_single_source opened exactly one file:
#
#     path = root / "DESIGN.md"
#
# so a measurement rule restated in any OTHER non-PREREG file passed CI in
# silence. The hole was found during the G1 review of the v30a amendment form:
# form (ii) would have placed normative measurement semantics in
# AVAILABILITY_DECLARATION.md, and this checker would have printed PASS.
#
# The rule being enforced does not mention DESIGN.md. PREREG §0.2.1's locked
# "Single normative source" clause fails the CI script on any measurement
# formula, state enumeration, or denominator definition "appearing outside this
# file" — outside PREREG.md, wherever it lives. §6.8's later summary sentence
# says "appears in DESIGN.md" because DESIGN.md was the only companion document
# in existence when it was written; the implementation had inherited that
# wording as though it were the rule. It is not. A rule restated outside
# PREREG.md is a §0.2.1 protocol failure wherever it lives, and a scan that
# only knows one filename is a scan the next new document walks past.
#
# So the scan is scope-BY-EXCLUSION, not a fixed file list: every markdown file
# in the repository is scanned unless named below with a reason. This is
# fail-closed — a markdown file added later is scanned by default, and removing
# it from scope costs a visible diff carrying a written reason. That is the
# standard PREREG §6.8 already sets for the banned-list exemptions ("an
# exemption that cannot be audited is not one"), applied to scan scope.
#
# Each decision below is deliberate; none of them was made to help a current
# file pass.

# Directories excluded wholesale, with the reason for each.
SINGLE_SOURCE_EXCLUDED_DIRS: tuple[tuple[str, str], ...] = (
    # Dated capture and record material: measurement logs, CSV/JSON captures,
    # working notes, and _snapshots/ holding superseded drafts BY DESIGN. It is
    # the evidence attachment set behind AVAILABILITY_DECLARATION.md — instances
    # of what was observed, not rules. The document that speaks FOR this
    # evidence, the declaration itself, is scanned; that is where a rule would
    # have to surface to acquire any normative effect.
    ("evidence", "dated evidence records and superseded-draft snapshots; the "
                 "declaration that speaks for them is scanned instead"),
    (".git", "version-control internals, not repository documents"),
    (".pytest_cache", "tool cache, gitignored"),
    ("__pycache__", "tool cache, gitignored"),
)

# Individual files excluded, with the reason for each. Every OTHER markdown file
# — AVAILABILITY_DECLARATION.md, README.md, PRIOR_ART_VERIFICATION.md,
# DEVIATIONS.md, DESIGN.md, and anything added later — is scanned.
SINGLE_SOURCE_EXCLUDED_FILES: tuple[tuple[str, str], ...] = (
    # The source itself. §0.2.1 bans restatement "outside this file"; inside it
    # is where the rules are supposed to be.
    ("PREREG.md", "the single normative source (PREREG §0.2.1)"),
    # Declares itself non-normative in its own first line — "Not a normative
    # file. Nothing here instructs an implementer." — and PREREG §6.8 names it
    # as the file that carries the historical record precisely so that normative
    # and historical prose stop being told apart linguistically. Scanning it
    # would flag the recounting of deleted machinery that is its entire purpose.
    # This exclusion predates this change and is preserved unchanged.
    ("HISTORY.md", "self-declared non-normative ledger (PREREG §6.8)"),
    # PREREG §6.8 declares it an exempt region for the banned scan, and §11 item
    # 1 constrains it to the single §13.9 pointer entry — which check_parking_lot
    # enforces over EVERY line, not just bullets. A rule cannot hide in a file
    # whose second entry is already a failure.
    ("PARKING_LOT.md", "exempt region per PREREG §6.8; §11 item 1 permits "
                       "exactly one entry, enforced by check_parking_lot"),
    # Generated artifact: regenerated from traces.py by
    # generate_expected_outputs.py and machine-pinned to the reducer by
    # test_expected_outputs.py, while the reducer is itself anchored to PREREG.md
    # by check_legality_table, check_unit_grammar and check_suppression_anchor.
    # It is not an implementer's input and it cannot drift silently — a drifted
    # value fails the suite. Scanning it would flag generated state tables that
    # regeneration would immediately reproduce, which is how a check gets turned
    # off. Residual risk, recorded rather than hidden: its hand-written
    # "Interpretation notes" paraphrase denominators, and PREREG §6.6.1's
    # required human read owns that text, not this scan.
    ("tests/registration/EXPECTED_OUTPUTS.md",
     "generated test artifact, pinned to the reducer by test_expected_outputs.py"),
)
# DEVIATIONS.md is deliberately NOT excluded, though it is an append-only
# record. §0.2.1's class machinery is the reason: class A branches and class B
# parameters are recorded there, but a class C change — a new branch, unit,
# denominator, coverage state, tier licence, or acceptance criterion — may NOT
# be, because it requires an amended registration first (PREREG lines 136,
# 1009, 1033: "No DEVIATIONS.md-only criterion"). A rule-shaped line in
# DEVIATIONS.md is therefore, by construction, a class C change recorded in the
# one place §0.2.1 forbids. Scanning it enforces that boundary.


def single_source_scan_set(root: Path) -> list[Path]:
    """Every markdown file in scope for the single-source scan, sorted.

    Scope by exclusion (see the comment block above): everything except the
    named directories and files. New markdown is scanned by default."""
    skip_dirs = {name for name, _reason in SINGLE_SOURCE_EXCLUDED_DIRS}
    skip_files = {rel for rel, _reason in SINGLE_SOURCE_EXCLUDED_FILES}
    out: list[Path] = []
    for path in sorted(root.rglob("*.md")):
        rel_parts = path.relative_to(root).parts
        if any(part in skip_dirs for part in rel_parts[:-1]):
            continue
        if path.relative_to(root).as_posix() in skip_files:
            continue
        out.append(path)
    return out


# Quotation, distinguished from restatement. PREREG §0.2.1 permits referencing a
# rule by its section and bans restating it; a companion document that quotes the
# registered text VERBATIM UNDER AN ATTRIBUTION is doing neither. Two conditions,
# both required:
#
#   1. VERBATIM. Unlike a paraphrase, a verbatim copy cannot drift in silence,
#      because the exemption is re-derived from PREREG.md on every run — edit
#      either side and the match evaporates and the line is flagged again. A
#      paraphrase gets no exemption; that is the restatement §0.2.1 bans.
#   2. ATTRIBUTED. The quoted line, or one of the six lines above it (enough to
#      reach the head of a wrapped quote block), must name PREREG.md. A bare
#      unattributed copy reads to a later implementer as this document's own
#      rule, which is the "two copies, no canonical source" shape §0.2.1 names
#      as the generator of the whole residue class. It stays flagged.
#
# The length floor keeps short fragments from matching PREREG prose by accident.
_QUOTE_MIN_CHARS = 40
_QUOTE_ATTRIBUTION_WINDOW = 6
_PREREG_ATTRIBUTION = re.compile(r"PREREG\.md")


def _quote_normalize(s: str) -> str:
    s = re.sub(r"^\s*>+\s*", "", s.strip()).replace("**", "").replace("`", "")
    return re.sub(r"\s+", " ", s).strip()


def _prereg_quote_blob(root: Path) -> str:
    prereg = root / "PREREG.md"
    if not prereg.exists():
        return ""
    return " ".join(_quote_normalize(ln)
                    for ln in prereg.read_text(encoding="utf-8").splitlines())


def _is_attributed_quote(line: str, raw_lines: list[str], lineno: int,
                         blob: str) -> bool:
    normed = _quote_normalize(line)
    if len(normed) < _QUOTE_MIN_CHARS or not blob or normed not in blob:
        return False
    start = max(0, lineno - 1 - _QUOTE_ATTRIBUTION_WINDOW)
    return any(_PREREG_ATTRIBUTION.search(ln) for ln in raw_lines[start:lineno])


# Attribution, also not restatement: "…are defined by `PREREG.md` §7.2 and are
# not restated here" is the form §0.2.1 asks companion documents to use, and
# DESIGN.md uses it. Only the definitional detectors consult this; it cannot
# exempt a formula, a state enumeration, or a denominator constitution, so
# naming a section does not buy a licence to restate one.
_REFERENCE_NOT_RESTATEMENT = re.compile(
    r"(?:defined|specified|owned|governed|resolved|stated)\s+(?:by|in)\s+"
    r"`?PREREG\.md`?|not restated here")

# Curated detectors for the single-source rule (PREREG §0.2.1): measurement
# formulas, state enumerations, and denominator definitions may not appear
# outside PREREG.md. Rules name the owning PREREG section.
_SINGLE_SOURCE_RULES: tuple[tuple[str, str], ...] = (
    (r"unavailable\s*=\s*a\s*>=?\s*d",
     "ties comparator restated; owned by PREREG §2.3"),
    (r"d\(i\)\s*(?:≤|<=)\s*d.{0,40}finding|finding.{0,40}d\(i\)\s*(?:≤|<=)\s*d",
     "valid-finding rule restated; owned by PREREG §2.6"),
    (r"Silence is recorded only",
     "silence-scope rule restated; owned by PREREG §2.6"),
    (r"promotion_status\s*=\s*\"preserving\"\s*\|\s*\"promoted\"",
     "promotion-status state enumeration restated; owned by PREREG §3.1/§6.6"),
    (r"Reach is \*\*the latest",
     "reach measurement definition restated; owned by PREREG §8.5"),
    (r"÷", "measurement formula (÷) outside PREREG.md; owned by PREREG §7.2/§7.2.1"),
    (r"\b(?:proof yield|evidence yield|feature-cohort precision|"
     r"conditional feature-cohort recall)\s*(?:=|is defined)",
     "metric formula restated; owned by PREREG §7.2/§7.2.1"),
    (r"bitwise equality under a passing determinism guard",
     "comparison-regime definition restated; owned by PREREG §6.9/§6.10"),
    # --- added with the scope extension -----------------------------------
    # The eight detectors above were written against the restatements that had
    # actually appeared in DESIGN.md, so they are DESIGN.md-shaped: widening the
    # file list alone finds nothing in AVAILABILITY_DECLARATION.md, whose
    # rule-shaped text takes different forms. These five catch those forms. Each
    # is file-agnostic, each names the PREREG section that owns the semantics,
    # and each was calibrated to fire on no other scanned file — the point is to
    # catch rules stated outside PREREG.md, not to editorialise about prose.
    #
    # A classification rule stated as a biconditional: "**REQUIRED** iff …" is
    # a rule for assigning a state, which §0.2.1 reserves ("units, states,
    # denominators, gates"). Deriving THIS fixture's per-column enumeration is
    # an instance; stating the rule that yields it is not.
    (r"\*\*[A-Z][A-Z][A-Z _-]*\*\*\s+iff\b",
     "state-classification rule stated as a biconditional; a rule for assigning "
     "a state is owned by PREREG §6.6/§7.0, not by a companion document"),
    # Denominator membership: what enters, and what is excluded from, a
    # denominator is named in §0.2.1's own list of reserved semantics.
    (r"(?:enter(?:s|ing)?|excluded from|included in|removed from|member of)\s+"
     r"(?:the\s+|any\s+|every\s+|a\s+|no\s+)?[\w' -]{0,24}denominator",
     "denominator membership stated outside PREREG.md; owned by PREREG "
     "§7.2/§7.4/§7.7"),
    # Denominator constitution — what the denominator is drawn FROM. Restricted
    # to constitution verbs so that instance-level prose about a denominator
    # ("adopting this family is class C") is not swept in with it.
    (r"\bdenominator\s+(?:derives|comprises|consists|is constituted|is drawn|"
     r"is the set)\b",
     "denominator constitution defined outside PREREG.md; owned by PREREG "
     "§7.2/§7.4"),
    # What a published number means — the fourth item in §0.2.1's reserved list,
    # and the one a companion document is most tempted to settle in passing.
    (r"\bnever (?:reported|counted|scored) as\b|"
     r"\b(?:may|can|shall) (?:not|never) be (?:reported|published|counted) as\b",
     "rule about what may be reported/published stated outside PREREG.md; what "
     "a published number means is owned by PREREG §7.2/§8.3/§10.2"),
)

# Definitional detectors, held separately because these — and only these —
# honour _REFERENCE_NOT_RESTATEMENT. A companion document saying a term "is
# defined by PREREG.md §7.2 and is not restated here" is doing the referencing
# §0.2.1 explicitly permits; a document that opens its own defining clause is
# doing the thing it bans. The distinction is only coherent for definitions, so
# the exemption is confined to them.
_SINGLE_SOURCE_DEFINITIONAL_RULES: tuple[tuple[str, str], ...] = (
    (r"\*\*DEFINITION\b|\bDEFINITION,\s+declared\b|\bdefined here\b|"
     r"\b(?:is|are)\s+defined\s+as\s+follows\b|\bwe define\b|"
     r"\b(?:is|are)\s+hereby\s+defined\b",
     "a defining clause for a term used normatively by PREREG.md is opened "
     "here; what a term means is owned by PREREG.md (§0.2.1)"),
)


def check_single_source(root: Path) -> list[Finding]:
    """PREREG §0.2.1: no measurement formula, state enumeration, or denominator
    definition outside PREREG.md — in ANY companion document, not just
    DESIGN.md. See the scope comment block above SINGLE_SOURCE_EXCLUDED_DIRS."""
    f: list[Finding] = []
    if not (root / "DESIGN.md").exists():
        # Preserved from the single-file implementation. It no longer returns
        # early: a missing DESIGN.md is already a structure failure, and it must
        # not take every other document out of scan scope on its way out.
        f.append(Finding("single_source", "DESIGN.md", None, "missing"))
    quote_blob = _prereg_quote_blob(root)
    # State-set enumerations: three or more schedule/coverage state values on
    # one line is an enumeration, not a mention.
    state_tokens = ("not_applicable", "unsupported", "completed", "incomplete",
                    "short_circuited")
    for path in single_source_scan_set(root):
        name = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8")
        raw_lines = text.splitlines()
        for lineno, line in normative_lines(path, text):
            if _is_attributed_quote(line, raw_lines, lineno, quote_blob):
                continue  # verbatim registered text, re-verified every run
            for pattern, message in _SINGLE_SOURCE_RULES:
                if re.search(pattern, line):
                    f.append(Finding("single_source", name, lineno,
                                     f"{message}: {line.strip()[:110]!r}"))
            if not _REFERENCE_NOT_RESTATEMENT.search(line):
                for pattern, message in _SINGLE_SOURCE_DEFINITIONAL_RULES:
                    if re.search(pattern, line):
                        f.append(Finding("single_source", name, lineno,
                                         f"{message}: {line.strip()[:110]!r}"))
            hits = [t for t in state_tokens if t in line]
            if len(hits) >= 3:
                f.append(Finding(
                    "single_source", name, lineno,
                    f"state enumeration ({', '.join(hits)}); owned by PREREG §6.6"))
    return f


# ---------------------------------------------------------------------------
# The v30a tag-message hash set has exactly ONE authority (R67/§16)
#
# The set is `FILES=` in evidence/ceremony/CEREMONY_COMMANDS.md §3.2. Every gate
# in that ceremony iterates the list; no gate reads a numeral. Every count and
# every enumeration elsewhere in the repository is a RESTATEMENT and is checked
# against the authority here.
#
# Why this check exists: at R67 the same set was asserted with five different
# values across registered text, the hashed declaration and the ceremony package
# (two / three / five / six / seven), each locally plausible, because no site
# derived from the operation. A rule restated as a literal does not merely go
# stale - it forks.
#
# Exemptions are keyed by path AND line, never by pattern (R67/§16.2 D5, D6), and
# each is PINNED to a substring that must still be on that line. Line-keyed
# whitelists drift: the same round found three citations 169 lines out of date.
# A pin turns silent mis-exemption into a loud failure.
# ---------------------------------------------------------------------------

_CEREMONY_REL = "evidence/ceremony/CEREMONY_COMMANDS.md"
_FILES_DECL = re.compile(r'^FILES="([^"]+)"', re.M)

_HASH_SET_CORPUS = (
    "AVAILABILITY_DECLARATION.md", "PREREG.md", "DESIGN.md", "HISTORY.md",
    "README.md", "evidence/ceremony/CEREMONY_COMMANDS.md",
    "evidence/ceremony/COMMIT_PLAN.md", "evidence/ceremony/DEVIATIONS_DRAFT.md",
    "evidence/ceremony/H34_DRAFT.md",
)

# NUMBER HANDLING (rebuilt R70/B5).
#
# The previous matcher was a fixed alternation of number WORDS. Consequences,
# all found by property-testing rather than by review:
#   - numerals were not matched AT ALL: "6 hashes", "42 hashes", "1,000 hashes"
#     were invisible, so a count written in digits could say anything;
#   - compounds mis-resolved: "twenty-five hashes" matched "twenty" and yielded
#     20, a WRONG VALUE, which is worse than a miss because it can accidentally
#     equal the authority and pass;
#   - the vocabulary ceiling was "eight" before R69, then "twenty".
#
# It now matches a number PHRASE and parses it. Range 0-200 is verified by
# property test; above 200 the parser still works for exact hundreds and
# hundred+remainder forms, and anything it cannot parse is reported, never
# silently skipped.
_HS_UNITS = {"zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
             "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
             "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
             "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18,
             "nineteen": 19,
             # ordinals carry the same value: "the sixth hash"
             "first": 1, "second": 2, "third": 3, "fourth": 4, "fifth": 5,
             "sixth": 6, "seventh": 7, "eighth": 8, "ninth": 9, "tenth": 10,
             "eleventh": 11, "twelfth": 12,
             # "both" is a closed quantifier over exactly two
             "both": 2}
_HS_TENS = {"twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60,
            "seventy": 70, "eighty": 80, "ninety": 90}
_HS_NUMTOK = "|".join(sorted(list(_HS_UNITS) + list(_HS_TENS) + ["hundred", "and"],
                             key=len, reverse=True))
_HS_NUMVAL = "|".join(sorted(list(_HS_UNITS) + list(_HS_TENS) + ["hundred"],
                            key=len, reverse=True))
# the phrase must START with a real number token; "and" may only join.
_HS_NUMPHRASE = (r"(?:\d{1,4}(?:,\d{3})*|(?:" + _HS_NUMVAL + r")"
                 r"(?:[-\s]+(?:" + _HS_NUMTOK + r"))*)")


def _hs_number(text: str) -> int | None:
    """Parse a matched number phrase. None = could not parse (reported, not skipped)."""
    t = text.strip().lower().replace(",", "")
    if t.isdigit():
        return int(t)
    total, current, seen = 0, 0, False
    for tok in re.split(r"[-\s]+", t):
        if tok == "and" or not tok:
            continue
        if tok == "hundred":
            current = (current or 1) * 100
            seen = True
        elif tok in _HS_TENS:
            current += _HS_TENS[tok]
            seen = True
        elif tok in _HS_UNITS:
            current += _HS_UNITS[tok]
            seen = True
        else:
            return None
    return (total + current) if seen else None



# STRICT: nouns that are hash-set nouns wherever they appear.
_HS_NOUN = r"(?:hashes|hash\s+lines|hash|SHA-?256\s+lines|SHA-?256|line\s+block)"
# LOOSE: bare "lines" is a hash-set noun ONLY where the sentence is about the
# tag message ("a tag message with five lines"). Applied conditionally, because
# unconditionally it reads "drifted 169 lines" as a count of 169 hashes - which
# it did, until R70/B5 gave the parser numerals to read.
_HS_NOUN_LOOSE = r"(?:lines?)"
# (?<!-) excludes the TAIL of a compound numeral: "one hundred and sixty-nine
# lines" is not a claim that the hash block has nine lines. Found by R69/B1.3,
# when widening the vocabulary to twenty made exactly that phrase match.
_HS_ATTACH = re.compile(r"(?<![-\w])(" + _HS_NUMPHRASE + r")"
                        r"(?:[-\s]+(?:\w+\s+){0,2})?" + _HS_NOUN, re.I)
# Bare "lines" is a hash-set noun in exactly one construction: "a tag message with
# N lines". Requiring the tag-message phrase ADJACENTLY is what separates that from
# "drifted 169 lines" and "by sixty-four lines", which are line-drift figures and
# which an unconditional bare-`lines` rule read as hash counts.
_HS_ATTACH_TAGLINES = re.compile(
    r"tag[- ]message[^.]{0,24}?(?<![-\w])(" + _HS_NUMPHRASE + r")[-\s]+" + _HS_NOUN_LOOSE,
    re.I)
_HS_CTX = re.compile(
    r"(tag[- ]message|\$FILES|FILES=|files whose hashes"
    r"|hash(es)?[^.]{0,18}(block|set)\b"
    r"|(each|all|one|member) of the (five|six|seven|eight|nine|ten)\b"
    r"|the (fifth|sixth|seventh|eighth|ninth|tenth) hash)", re.I)

# (path, ANCHOR TEXT) -> (allowed, reason). D5 = v30 site. D6 = PREREG
# registered text. KEYED BY ANCHOR, NEVER BY LINE - see _exempt_by_anchor.
def _exempt_by_anchor(table, rel, raw, all_lines):
    """Find the exemption whose ANCHOR text sits on this line.

    Returns (key, allowed, reason, problem). `problem` is a string when the
    anchor is not usable and None when it is: an anchor that matches more than
    one line in the file would exempt every one of them, so it is refused rather
    than applied to the first.

    The key carries no line number. An exemption keyed to a line detaches the
    moment anything above it grows, and re-pinning it to the new number restores
    the same defect with a fresher value.
    """
    for (p, anchor), rest in table.items():
        if p != rel or anchor not in raw:
            continue
        hits = sum(1 for ln in all_lines if anchor in ln)
        if hits != 1:
            return (p, anchor), rest[0], rest[1], (
                "its anchor %r matches %d lines in this file; an anchor that "
                "selects more than one line exempts all of them. Narrow the "
                "anchor." % (anchor[:48], hits))
        return (p, anchor), rest[0], rest[1], None
    return None, None, None, None


_HASH_SET_EXEMPT = {
    ('AVAILABILITY_DECLARATION.md',
     'prereg-v30 tag message (five SHA-256 lines'): (
        frozenset([5]),
        'D5 - the parenthetical describes the v30 message, not v30a.'),
    ('AVAILABILITY_DECLARATION.md',
     '- **R7. hash-count:'): (
        frozenset([5]),
        "D5 - working resolution R7. Its 'ALL FIVE' takes the v30 five as its "
        "referent ('matching the prereg-v30 tag as executed') and is TRUE of "
        'a six-file set containing those five. The totality reading came from '
        "R7's topic LABEL, not its predicate; the R67/§14.2 survey "
        'established every label in that block is a topic tag. R7 stands '
        'unamended. See AVAILABILITY_DECLARATION.md §D.3 entry (iii).'),
    ('evidence/ceremony/CEREMONY_COMMANDS.md',
     'a tag message with five lines is not a v30a tag message'): (
        frozenset([5]),
        'D5 - a NEGATED assertion: it says five is wrong for v30a.'),
    ('AVAILABILITY_DECLARATION.md',
     'R7 reads:'): (
        frozenset([5]),
        'D5 - §D.3 entry (iii) QUOTES R7 in order to dispose of it. Quoting '
        'the text under discussion is required; the disposition is in the '
        'same entry.'),
    ('HISTORY.md',
     'it FORKS'): (
        frozenset([2]),
        'D5 - lesson 19 RECORDS the fork. The values two/three/five/six/seven '
        'appear as the historical defect being described, quoted from the '
        'sites that carried them, not as an assertion of the current count. '
        'The lesson states in its own text that the authority is $FILES and '
        'that no gate reads a numeral.'),
    ('PREREG.md',
     'both file hashes in the tag message'): (
        frozenset([2]),
        "D6 - REGISTERED TEXT, not editable. 'both' is a closed quantifier "
        'over exactly two things and lost its referent when the set grew; the '
        "two files' hashes ARE in the tag, so it is satisfied, but it "
        'supplies no rule for files added since. See '
        'AVAILABILITY_DECLARATION.md §D.3 entry (ii).'),
    ('PREREG.md',
     'one hash beside one path'): (
        frozenset([1]),
        'D1 FALSE POSITIVE on REGISTERED, APPROVED text that is not editable. '
        "'one hash beside one path' states the FORM of the enumeration - a "
        'one-to-one pairing of hash to path - not the COUNT of the hashed '
        'set. The same sentence goes on to say the count is read from the '
        "enumeration itself: 'The set is that enumeration and its count is "
        "read from it: no clause of this file states the count as a literal.' "
        'Correcting the content is unavailable (the author approved these '
        'bytes on 25 Aug 2026 and PREREG.md is edited only by an approved '
        'diff), so this is the F1.1 case where an exemption is right: the '
        'content cannot change, and the reason is what gets recorded.'),
}

# (path, ANCHOR TEXT) -> (enumeration, reason) for D2 path enumerations that
# are not the set. Keyed by anchor, never by line.
_HASH_SET_ENUM_EXEMPT = {
    ('AVAILABILITY_DECLARATION.md',
     '| 1 — item 1, named individually |'): (
        ('PREREG.md', 'DESIGN.md', 'HISTORY.md', 'tools/check_registration.py', 'protocol/runtime_reference.py', 'AVAILABILITY_DECLARATION.md', 'DEVIATIONS.md', 'PARKING_LOT.md', 'VALIDATED_CONFIG.toml', 'evidence/fixture_spike/f3/fixture_manifest_DRAFT.json', 'evidence/fixture_spike/n1/declared_map.csv'),
        'D6 - §D.2 enumerates the set BY LIMB, showing which limb of §11 item '
        '8 admits each path. That breakdown is the section argument: the set '
        'is not a list someone chose, it is what three stated rules produce. '
        'Flattening it into the set in order would satisfy this check and '
        'delete the reason the enumeration is there, so the content fix is '
        'unavailable and the exemption is the right instrument. The row is '
        'limb 1 alone; the remaining rows carry the other limbs.'),
    ('PREREG.md',
     'The first commit contains the registration and its checking tools'): (
        ('PREREG.md', 'DESIGN.md', 'HISTORY.md', 'tools/check_registration.py', 'protocol/runtime_reference.py', 'DEVIATIONS.md', 'PARKING_LOT.md', 'VALIDATED_CONFIG.toml'),
        'D6 - REGISTERED TEXT, not editable. §11 item 1 lists the first '
        "COMMIT's contents, which is a different set from the tag message's "
        'hash block: it includes DEVIATIONS.md, PARKING_LOT.md, '
        'VALIDATED_CONFIG.toml and tests/registration/, none of which are '
        'hashed.'),
    ('AVAILABILITY_DECLARATION.md',
     'Registered text: *"SHA-256 of `PREREG.md`, `DESIGN.md`, and `HISTORY.md`'): (
        ('PREREG.md', 'DESIGN.md', 'HISTORY.md'),
        'D6 - §D.3 entry (i) QUOTES PREREG.md §11 item 3 in order to state '
        'its floor reading. The quotation must stay verbatim.'),
    ('evidence/ceremony/COMMIT_PLAN.md',
     '[hashed], DESIGN.md [hashed], HISTORY.md [hashed]'): (
        ('PREREG.md', 'DESIGN.md', 'HISTORY.md', 'tools/check_registration.py', 'AVAILABILITY_DECLARATION.md', 'DEVIATIONS.md'),
        'D5 - the block is explicitly labelled "For the human reader, and NOT '
        'the check". It groups the six by EXPECTED VISIBILITY in `--cached` '
        'output, which deliberately is not $FILES order; V1a/V1b/V1c above it '
        'are the executable checks and they read the set from its authority.'),
    ('PREREG.md',
     'SHA-256 of `PREREG.md`, `DESIGN.md`, and `HISTORY.md` as committed'): (
        ('PREREG.md', 'DESIGN.md', 'HISTORY.md', 'DEVIATIONS.md'),
        'D6 - REGISTERED TEXT, not editable. §11 item 3 is a FLOOR: no '
        "'only', no 'exactly', so a superset satisfies it and over-delivery "
        'is strictly stronger. The executed v30 tag already carried five. See '
        'AVAILABILITY_DECLARATION.md §D.3 entry (i).'),
}


def _hash_set_strip(line: str) -> str:
    """Remove tokens that look like counts but are addresses."""
    out = re.sub(r"[*_]+", " ", line)
    for pat in (r"\u00a7\s*[A-Z]?\.?\d+(\.\d+)*[a-z]?", r"\b[A-Z]\.\d+",
                r"\bl\.\s*\d+", r"\blines?\s+[\d,\u2013-]+", r"\bv\d+[a-z]?\b",
                r"\bC\d[a-z]?\b", r"\b[A-Z]-?\d+\b", r"`[^`]*`",
                r"^\s*\d+\.\s", r"\b[0-9a-f]{8,}\b"):
        out = re.sub(pat, " ", out)
    return re.sub(r"\s+", " ", out)


def hash_set_authority(root: Path) -> tuple[list[str], list[Finding]]:
    """The one place the set is defined. Absence is a failure, never a skip."""
    path = root / _CEREMONY_REL
    if not path.exists():
        return [], [Finding("hash_set_single_source", _CEREMONY_REL, None,
                            "the authority for the tag-message hash set is missing; "
                            "every restatement below is unverifiable")]
    match = _FILES_DECL.search(path.read_text(encoding="utf-8"))
    if not match:
        return [], [Finding("hash_set_single_source", _CEREMONY_REL, None,
                            'no FILES="..." declaration found in \u00a73.2; the set has no authority')]
    return match.group(1).split(), []


def check_hash_set_single_source(root: Path) -> list[Finding]:
    files, findings = hash_set_authority(root)
    if not files:
        return findings
    n = len(files)
    basenames = set(files)
    findings.append(Finding(
        "hash_set_single_source", _CEREMONY_REL, None,
        "authority: %d paths (%s)" % (n, ", ".join(files)), is_note=True))

    seen_exempt: set[tuple[str, str]] = set()

    for rel in _HASH_SET_CORPUS:
        path = root / rel
        if not path.exists():
            continue
        lines = path.read_text(encoding="utf-8", errors="replace").split("\n")

        # ---- D1: count literals -------------------------------------------
        for idx, raw in enumerate(lines, 1):
            if not _HS_CTX.search(raw):
                continue
            saw = set()
            cleaned = _hash_set_strip(raw)
            # strict ALWAYS, plus the one narrow tag-message-lines construction.
            hits = (list(_HS_ATTACH.finditer(cleaned))
                    + list(_HS_ATTACH_TAGLINES.finditer(cleaned)))
            for m in hits:
                val = _hs_number(m.group(1))
                if val is None:
                    findings.append(Finding(
                        "hash_set_single_source", rel, idx,
                        "D1: could not parse the count phrase %r. Unparsed is NOT "
                        "clean - widen the parser or rewrite the phrase."
                        % m.group(1)[:40]))
                else:
                    saw.add(val)
            bad = sorted(v for v in saw if v != n)
            if not bad:
                continue
            key, allowed, reason, problem = _exempt_by_anchor(
                _HASH_SET_EXEMPT, rel, raw, lines)
            if key is not None and problem:
                findings.append(Finding(
                    "hash_set_single_source", rel, idx,
                    "D5/D6: this site's exemption is UNUSABLE - %s" % problem))
                continue
            entry = None if key is None else True
            if entry is None:
                findings.append(Finding(
                    "hash_set_single_source", rel, idx,
                    "D1: states %s for the v30a hash set; the authority "
                    "(%s \u00a73.2) says %d. Correct it against $FILES, or add a "
                    "path+line exemption with its reason."
                    % ("/".join(str(b) for b in bad), _CEREMONY_REL, n)))
                continue
            seen_exempt.add(key)
            unlisted = sorted(v for v in bad if v not in allowed)
            if unlisted:
                findings.append(Finding(
                    "hash_set_single_source", rel, idx,
                    "D5/D6: this line is exempt for %s, but it now also states %s. An "
                    "exemption whitelists a known historical VALUE at a site; it does "
                    "not license whatever appears there next."
                    % (sorted(allowed), unlisted)))
            else:
                findings.append(Finding("hash_set_single_source", rel, idx,
                                        "exempt - %s" % reason, is_note=True))

        # ---- D2: path enumerations purporting to BE the set ---------------
        for idx, raw in enumerate(lines, 1):
            hits = [b for b in basenames if b in raw]
            if len(hits) < 3:
                continue
            if raw.lstrip().startswith("git add "):
                # a staging line states what is STAGED, not what is HASHED.
                # D3 owns it and checks the aggregate; judging it here would
                # demand the two sets be identical, which they are not.
                findings.append(Finding(
                    "hash_set_single_source", rel, idx,
                    "D2: staging line - owned by D3, not judged as an enumeration "
                    "of the hash set", is_note=True))
                continue
            window = " ".join(lines[max(0, idx - 2): idx + 3])
            found = [b for b in files if b in window]
            if found == files:
                findings.append(Finding(
                    "hash_set_single_source", rel, idx,
                    "D2: enumeration matches $FILES in order", is_note=True))
                continue
            key, allowed, reason, problem = _exempt_by_anchor(
                _HASH_SET_ENUM_EXEMPT, rel, raw, lines)
            if key is not None and problem:
                findings.append(Finding(
                    "hash_set_single_source", rel, idx,
                    "D6: this site's enumeration exemption is UNUSABLE - %s" % problem))
                continue
            entry = None if key is None else True
            if entry is None:
                findings.append(Finding(
                    "hash_set_single_source", rel, idx,
                    "D2: enumerates %d of the %d hashed paths but is not the set "
                    "in order (%s). Either make it the set or exempt it by "
                    "path+line with its reason."
                    % (len(found), n, ", ".join(found) or "none in order")))
                continue
            seen_exempt.add(key)
            if tuple(found) != tuple(allowed):
                findings.append(Finding(
                    "hash_set_single_source", rel, idx,
                    "D6: this site is exempt for the enumeration %s, but it now "
                    "enumerates %s. An exemption whitelists a known historical "
                    "enumeration, not any future one."
                    % (list(allowed), found)))
            else:
                findings.append(Finding("hash_set_single_source", rel, idx,
                                        "exempt - %s" % reason, is_note=True))

    # ---- D2a: the tag-message body is ORDER-SENSITIVE ---------------------
    cer = root / _CEREMONY_REL
    if cer.exists():
        body = re.findall(r"^<64 hex>  (\S+)$",
                          cer.read_text(encoding="utf-8"), re.M)
        if not body:
            findings.append(Finding(
                "hash_set_single_source", _CEREMONY_REL, None,
                "D2: the \u00a73.5 tag-message body carries no '<64 hex>  <path>' block; "
                "the message that gets signed is not specified anywhere"))
        elif body != files:
            findings.append(Finding(
                "hash_set_single_source", _CEREMONY_REL, None,
                "D2: the \u00a73.5 tag-message body is %s but $FILES is %s - ORDER "
                "MATTERS here: C2f diffs this block against C2's output line for line"
                % (body, files)))
        else:
            findings.append(Finding(
                "hash_set_single_source", _CEREMONY_REL, None,
                "D2: tag-message body == $FILES, in order (%d paths)" % len(body),
                is_note=True))

    # ---- D3 / D4: the staging plan must cover the set ---------------------
    plan_rel = "evidence/ceremony/COMMIT_PLAN.md"
    plan = root / plan_rel
    if plan.exists():
        text = plan.read_text(encoding="utf-8")
        staged: set[str] = set()
        for line in re.findall(r"^git add (.+)$", text, re.M):
            staged.update(line.split())
        missing = [f for f in files if f not in staged]
        if missing:
            findings.append(Finding(
                "hash_set_single_source", plan_rel, None,
                "D3: \u00a74's git add set omits %s - `git show :<path>` on a tracked "
                "file that was never staged silently returns its HEAD content, so "
                "the tag would be signed over unapproved bytes" % ", ".join(missing)))
        else:
            findings.append(Finding("hash_set_single_source", plan_rel, None,
                                    "D3: \u00a74's git add set covers $FILES", is_note=True))

        # D4: the pre-commit verification must READ the set from its authority
        # rather than restate it, and must name every member for the human reader.
        # (Until R67/A1 this checked a literal "EXPECT, exactly" list. That list
        # WAS a restatement - the very thing this check exists to prevent - so D4
        # now tests derivation, not the presence of a second copy.)
        derives = ("grep -m1 '^FILES=' evidence/ceremony/CEREMONY_COMMANDS.md"
                   in text)
        if not derives:
            findings.append(Finding(
                "hash_set_single_source", plan_rel, None,
                "D4: the pre-commit checks do not READ $FILES from %s §3.2. A "
                "verification block that restates the set becomes a second "
                "authority, which is the defect this check exists to prevent"
                % _CEREMONY_REL))
        unnamed = [f for f in files if f not in text]
        if unnamed:
            findings.append(Finding(
                "hash_set_single_source", plan_rel, None,
                "D4: the plan never names %s. A hashed file nobody names is a "
                "file nobody verifies" % ", ".join(unnamed)))
        if derives and not unnamed:
            findings.append(Finding(
                "hash_set_single_source", plan_rel, None,
                "D4: pre-commit checks derive $FILES from its authority; all %d "
                "members named" % len(files), is_note=True))

    # ---- exemptions that no longer match anything -------------------------
    for key in list(_HASH_SET_EXEMPT) + list(_HASH_SET_ENUM_EXEMPT):
        if key not in seen_exempt:
            rel, anchor = key
            src = root / rel
            where = " The file itself is missing."
            if src.exists():
                hits = [n for n, ln in enumerate(
                    src.read_text(encoding="utf-8", errors="replace")
                    .split(chr(10)), 1)
                    if anchor in ln]
                if not hits:
                    where = (" Its anchor text is gone from the file - the sentence it "
                             "exempted no longer exists, so delete the exemption.")
                elif len(hits) == 1:
                    where = (" Its anchor is at line %d, but that line did not trigger "
                             "the check - the exemption is no longer needed." % hits[0])
                else:
                    where = (" Its anchor matches %d lines (%r); narrow it."
                             % (len(hits), hits[:6]))
            findings.append(Finding(
                "hash_set_single_source", rel, None,
                "D5/D6: this exemption fired on nothing - a stale exemption is a hole, "
                "not a no-op.%s" % where))
    return findings


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
_D7_HEX = re.compile(r"\b([0-9a-f]{8,64})\u2026?")
_D7_SIZE = re.compile(r"\b([\d,]{4,})\s*(bytes|lines)\b")

# (path, line) -> (pin, reason). Dated records and historical narrative.
# (path, line) -> (pin, allowed_values, reason).
# ALLOWED_VALUES is the point: an exemption names the specific historical values
# the line may carry. A NEW wrong value on an exempted line still fails. Without
# that, an exemption licenses every future error on its line - which D7's own
# negative test N1/N2 demonstrated before this was fixed.
_D7_EXEMPT = {
    # --- dated records brought in at R74/\u00a756 -------------------------------
    ("evidence/amendment/_CI_GATE_RESULT_moved.md", 34): (
        'Export HEAD read-only',
        frozenset({"1099", "3650", "f0a8f001"}),
        "dated record brought into the tree at R74/\u00a756 - quotes the declaration as it stood on its own date"),
    ("evidence/amendment/_CI_GATE_RESULT_moved.md", 35): (
        'Copy in working-tree versions of the files that differ from H',
        frozenset({"30d3ad4c", "3684", "39a944c1", "595cb9e7", "f0829bd3"}),
        "dated record brought into the tree at R74/\u00a756 - quotes the declaration as it stood on its own date"),
    ("evidence/amendment/_E2E3_round1_reports.md", 950): (
        'Both files read in full',
        frozenset({"1099", "2268", "3796"}),
        "dated record brought into the tree at R74/\u00a756 - quotes the declaration as it stood on its own date"),
    ("evidence/amendment/_J4c_J6_reports.md", 365): (
        'C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01',
        frozenset({"1c72e7b6b5e1", "8b1d67a4"}),
        "dated record brought into the tree at R74/\u00a756 - quotes the declaration as it stood on its own date"),
    ("evidence/amendment/K2_AMENDMENT_LEDGER.md", 509): (
        'byte-identical to SSF Part 2.4 step C',
        frozenset({"1290186e", "1417", "e7ab52d3"}),
        "dated record brought into the tree at R74/\u00a756 - quotes the declaration as it stood on its own date"),
    ("evidence/amendment/K5_REPLACEMENT_CRITERION_OPTIONS.md", 11): (
        'files as they stand this pass',
        frozenset({"1099", "3684"}),
        "dated record brought into the tree at R74/\u00a756 - quotes the declaration as it stood on its own date"),
    ("evidence/amendment/M1_CANDIDATE_C_CLAUSE.md", 7): (
        'Read state this pass',
        frozenset({"1099"}),
        "dated record brought into the tree at R74/\u00a756 - quotes the declaration as it stood on its own date"),
    ("evidence/amendment/M1_CANDIDATE_C_CLAUSE_CORRECTED.md", 12): (
        'Read state this pass',
        frozenset({"1099"}),
        "dated record brought into the tree at R74/\u00a756 - quotes the declaration as it stood on its own date"),
    ("evidence/amendment/PRACTICES.md", 32): (
        'K4 scrub (`applied\\AVAILABILITY_DECLARAT',
        frozenset({"1290186e", "3695"}),
        "dated record brought into the tree at R74/\u00a756 - quotes the declaration as it stood on its own date"),
    ("evidence/amendment/SC13_SPLIT_ABC.md", 14): (
        'Read state this pass',
        frozenset({"1099"}),
        "dated record brought into the tree at R74/\u00a756 - quotes the declaration as it stood on its own date"),
    ("evidence/amendment/SCHEMA_SET_ADOPTION.md", 15): (
        'Read state this pass',
        frozenset({"1099"}),
        "dated record brought into the tree at R74/\u00a756 - quotes the declaration as it stood on its own date"),
    ("evidence/amendment/X5_FINAL_PREREG_DIFF.md", 936): (
        'states four criteria',
        frozenset({"30d3ad4c", "7425"}),
        "dated record brought into the tree at R74/\u00a756 - quotes the declaration as it stood on its own date"),
    ("evidence/amendment/X5_FINAL_PREREG_DIFF.md", 1965): (
        'THE BLOCK NOW IN K2',
        frozenset({"1462", "fb171ed8"}),
        "dated record brought into the tree at R74/\u00a756 - quotes the declaration as it stood on its own date"),
    ("evidence/killgate/KILL_GATE_STATUS.md", 17): (
        'Fixture declaration reconstruction with evidence',
        frozenset({"3684"}),
        "dated record brought into the tree at R74/\u00a756 - quotes the declaration as it stood on its own date"),
    ("evidence/phase1/REPO_READINESS.md", 86): (
        'DECLARATION.md   42,013 bytes, 11 Aug 2026',
        frozenset({"42013"}),
        "dated record brought into the tree at R74/\u00a756 - quotes the declaration as it stood on its own date"),
    # ROUND_STATE.md carried a stale declaration hash under this exemption until
    # R81. It is NOT a dated record - R36 requires it REWRITTEN EVERY ROUND - so it
    # never belonged in this group, where the rule is "exempted, NEVER updated".
    # The R81 rewrite dropped the quoting line and D7 reported the exemption firing
    # on nothing, which is what D7 is for. Removed rather than re-pinned: there is
    # no longer a line to pin to.
    # evidence/amendment/ - the R20/R24 rulings and the schema source of record,
    # brought inside the signed tree at R73/§51. Each quotes the declaration as it
    # stood on its own date. Dated records are exempted, NEVER updated: rewriting
    # one to match today's file would falsify the drafting record (R13).
    ("evidence/amendment/DECLARATION_SCRUB_LIST.md", 353): (
        "`AVAILABILITY_DECLARATION.md` (277,411 b",
        frozenset({"277411"}),
        "dated drafting record - the 138-row scrub list, written against the "
        "declaration as it stood that day"),
    ("evidence/amendment/SCHEMA_SET_FINAL.md", 13): (
        "`AVAILABILITY_DECLARATION.md` `f0829bd3",
        frozenset({"3684", "f0829bd3"}),
        "dated drafting record - SCHEMA_SET_FINAL's own read-state block"),
    ("evidence/amendment/SCHEMA_SET_FINAL.md", 14): (
        "`30d3ad4c",
        frozenset({"30d3ad4c"}),
        "dated drafting record - this is tools/check_registration.py's hash, on a "
        "line that also names the declaration"),
    ("evidence/amendment/SCHEMA_SET_FINAL.md", 34): (
        "**Read state this pass.**",
        frozenset({"1099", "3684"}),
        "dated drafting record - line counts as read that pass"),
    ("evidence/amendment/SCHEMA_SET_FINAL.md", 2138): (
        "| `applied",
        frozenset({"1290186ed970df65968b5b979aa696e4dca4678e7b46fae40587c4948b8b1c30"}),
        "dated drafting record - the scrub's declared base, pinned deliberately"),
    ("evidence/author_review/READ_THROUGH_PACKAGE.md", 1): (
        "Author read-through package",
        frozenset({"f0829bd3a0f11b05170a5e2686b953c5def39104af0bbfa2904afb3da2f53310",
                   "277411", "3684"}),
        "the frozen author-read baseline; recording the bytes as the author read "
        "them is its whole purpose"),
    # R95: the declaration gained the §146.2 line-reference frame and the §148.1
    # walk frame, so its sha256/size/line-count moved. Both lines below say in
    # terms "do not read the hash from here" / "derived not transcribed"; the
    # values they quote are historical as of their own date, which is exactly what
    # f0829bd3 already is. The values are ADDED as historical, never edited to the
    # current ones - editing a dated record to today's hash is the R13 defect.
    ("evidence/ceremony/CEREMONY_COMMANDS.md", 27): (
        "do not read the size or hash from here",
        frozenset({"f0829bd3", "4c07c76f", "303643"}),
        "the stale value appears only inside the note recording that it WAS stale; "
        "4c07c76f/303,643 became historical at R95 when the declaration gained the "
        "line-reference frame"),
    ("evidence/ceremony/COMMIT_PLAN.md", 80): (
        "derived not transcribed",
        frozenset({"f0829bd3", "4c07c76ffbb2fe7b04a903d01d74d56bd2f80bf266f70f7fe2e45ea73a636403", "4c07c76ffbb2", "303643", "3955"}),
        "same - the superseded value is quoted in the note recording the correction; "
        "4c07c76f/303,643/3,955 joined it at R95, and the line itself says the hash is "
        "derived rather than transcribed"),
    ("evidence/fixture_spike/f5/v30a_ceremony_CHECKLIST.md", 8): (
        "In particular the",
        frozenset({"d1f43f51"}),
        "the SUPERSEDED banner, which quotes the stale hash in order to warn about it"),
    ("evidence/fixture_spike/f5/v30a_ceremony_CHECKLIST.md", 105): (
        "AVAILABILITY_DECLARATION.md",
        frozenset({"d1f43f51e3c31108e42ba53f40ea72b4ac7db0a2f9224ed528acad2a5cf9f83c"}),
        "the 2026-08-12 DRY RUN's hash block. Dated record, superseded in full by "
        "evidence/ceremony/CEREMONY_COMMANDS.md; rewriting it would falsify the walk "
        "it records, and its banner says it is stale by construction"),
    ("evidence/fixture_spike/f5/v30a_ceremony_CHECKLIST.md", 122): (
        "NEW, currently UNTRACKED",
        frozenset({"d1f43f51", "215256"}),
        "same dated dry run"),
}


def check_declaration_values(root: Path) -> list[Finding]:
    """D7 - every declaration hash/size literal agrees with the file."""
    decl = root / _DECL_REL
    if not decl.exists():
        return [Finding("declaration_values", _DECL_REL, None,
                        "the declaration is missing; its recorded values cannot be checked")]
    raw = decl.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    nbytes, nlines = len(raw), raw.count(b"\n")
    findings = [Finding("declaration_values", _DECL_REL, None,
                        "derived: sha256 %s\u2026 / %d bytes / %d lines"
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
        for idx, line in enumerate(full.read_text(encoding="utf-8", errors="replace").split("\n"), 1):
            # POPULATION: lines naming the declaration BY FILENAME.
            # EXCLUDED, deliberately (R68/§30.1 - state exclusions with the result):
            # DECLARATION_POINTER.md's prose. That file is a CHANGE LEDGER; it records
            # every past transition by from-hash and to-hash, so scanning its prose
            # flags 24 historical values that are correct as history. Its one LIVE
            # value is the structured current block, checked separately below.
            if _DECL_REL not in line:
                continue
            bad = []            # (raw_token, human_description)
            for hx in _D7_HEX.findall(line):
                if hx.isdigit() or len(hx) < 8:
                    continue
                if not digest.startswith(hx):
                    bad.append((hx, "sha256 %s\u2026" % hx[:12]))
            for val, unit in _D7_SIZE.findall(line):
                num = int(val.replace(",", ""))
                if unit == "bytes" and num != nbytes:
                    bad.append((val.replace(",", ""), "%s bytes" % val))
                if unit == "lines" and num != nlines:
                    bad.append((val.replace(",", ""), "%s lines" % val))
            if not bad:
                continue
            key = (rel, idx)
            entry = _D7_EXEMPT.get(key)
            if entry is None:
                findings.append(Finding(
                    "declaration_values", rel, idx,
                    "D7: states %s for %s; the file is sha256 %s\u2026 / %d bytes / %d lines. "
                    "A stale verification value reads as tamper evidence. Derive it, or "
                    "exempt this line as a dated record, naming the values it may carry."
                    % (", ".join(d for _, d in bad), _DECL_REL,
                       digest[:12], nbytes, nlines)))
                continue
            pin, allowed, reason = entry
            if pin not in line:
                findings.append(Finding(
                    "declaration_values", rel, idx,
                    "D7: exemption DRIFTED - pinned text %r is no longer on this line" % pin))
                continue
            seen.add(key)
            unlisted = [d for tok, d in bad if tok not in allowed]
            if unlisted:
                findings.append(Finding(
                    "declaration_values", rel, idx,
                    "D7: this line is exempt for %s, but it now also states %s. An "
                    "exemption names the historical values a line may carry; it does not "
                    "license new ones."
                    % (", ".join(sorted(allowed)), ", ".join(unlisted))))
            else:
                findings.append(Finding("declaration_values", rel, idx,
                                        "exempt - %s" % reason, is_note=True))

    # The pointer's CURRENT block is the one live value in that file, and C2d-2
    # gates on it. Parsed structurally, not by scanning the surrounding ledger.
    ptr = root / "evidence/fixture_spike/f4/DECLARATION_POINTER.md"
    if ptr.exists():
        text = ptr.read_text(encoding="utf-8", errors="replace")
        m_h = re.search(r"^    sha256: ([0-9a-f]{64})$", text, re.M)
        m_b = re.search(r"^    bytes:  (\d+)$", text, re.M)
        prel = ptr.relative_to(root).as_posix()
        if not m_h or not m_b:
            findings.append(Finding(
                "declaration_values", prel, None,
                "D7: the pointer's current hash block is missing or malformed; C2d-2 "
                "gates on it and cannot run"))
        elif m_h.group(1) != digest or int(m_b.group(1)) != nbytes:
            findings.append(Finding(
                "declaration_values", prel, None,
                "D7: the pointer's CURRENT block records %s… / %s bytes; the file is "
                "%s… / %d bytes. R15 forbids carrying a hash forward - re-derive the "
                "pointer and its manifest line in the same pass as the declaration change"
                % (m_h.group(1)[:12], m_b.group(1), digest[:12], nbytes)))
        else:
            findings.append(Finding(
                "declaration_values", prel, None,
                "D7: pointer current block agrees with the file (C2d-2's third leg)",
                is_note=True))

    for key in _D7_EXEMPT:
        if key not in seen:
            findings.append(Finding(
                "declaration_values", key[0], key[1],
                "D7: this exemption fired on nothing - the line moved or its text changed"))
    return findings


# ---------------------------------------------------------------------------
# D8 (R69/B3.3) - line-pinned citations must still resolve.
#
# §17.2 preferred anchors over line numbers, and most citations were converted.
# A few must stay line-pinned because their target has no heading: `FILES=` is a
# shell assignment, not a section. Those are registered here with the text that
# must be ON that line.
#
# AN ENTRY WITH `lineno = None` IS ANCHOR-KEYED: the text must occur exactly
# ONCE in the file, and where it occurs is reported rather than required.
# "Has no heading" is a reason not to cite a SECTION; it was never a reason to
# cite a LINE NUMBER, and the declaration's citation drifted twice in two rounds
# before that was noticed (R139/§1.4).
#
# The failure this prevents is specific and worse than a dead link: `l.1516` was
# cited in three files as the §A.11 walk summary and, after the declaration grew,
# resolved to "What this subsection does NOT do." A reader following it lands on
# real prose and has no way to know they are in the wrong place. A dead link
# announces itself; a drifted one does not.
# ---------------------------------------------------------------------------

# (target file, line, text that must be on it, who cites it)
_LINE_PINNED_CITATIONS = (
    ("evidence/ceremony/CEREMONY_COMMANDS.md", 277, 'FILES="PREREG.md',
     "COMMIT_PLAN.md \u00a76 and DEVIATIONS_DRAFT.md cite \u00a73.2 l.180 as the authority "
     "for the hash set; the target is a shell assignment and has no heading"),
    # ANCHOR-KEYED (lineno None) at A15-6, for the reason the declaration's pin
    # was converted at R139/\u00a71.4: this one drifted 277 -> 278 the moment a
    # review lesson was appended, and the lesson list grows by design. HISTORY.md
    # itself already says H-34 is "cited by its `### H-34` heading, not by line --
    # l.264-292 drifted as lessons were appended", so the line number was
    # carrying no information the heading did not, only the ability to go stale.
    # The heading is unique in the file, which is what makes the anchor resolve.
    ("HISTORY.md", None, "### H-34",
     "COMMIT_PLAN.md \u00a73 cites the H-34 heading and its sha256 quotation"),
    ("HISTORY.md", 219, "13. *(12 Aug 2026)*",
     "COMMIT_PLAN.md cites H-L13 by line; the lesson list is numbered, not headed"),
    ("HISTORY.md", 218, "12. *(12 Aug 2026)*",
     "DEVIATIONS_DRAFT.md cites H-L12 by line for the date convention"),
    ("DESIGN.md", 546, "review-lesson",
     "COMMIT_PLAN.md cites DESIGN.md l.546 as the cross-reference H-L13 de-fragilised"),
    # ANCHOR-KEYED (lineno None) at R139/§1.4: this pin drifted 4339 ->
    # 4377 -> 4376 in two rounds of declaration edits. The anchor text is
    # unique, so the line number was carrying no information the text did
    # not already carry -- only the ability to go stale.
    ("AVAILABILITY_DECLARATION.md", None, "R8. H-entry",
     "the decision-log tail is one block with no per-entry heading"),
)


def check_line_citations(root: Path) -> list[Finding]:
    """D8 - every registered line-pinned citation still resolves."""
    findings: list[Finding] = []
    for rel, lineno, expect, why in _LINE_PINNED_CITATIONS:
        path = root / rel
        if not path.exists():
            findings.append(Finding("line_citations", rel, lineno,
                                    "D8: cited file is missing"))
            continue
        lines = path.read_text(encoding="utf-8", errors="replace").split("\n")
        if lineno is None:
            # ANCHOR-KEYED. The citation names TEXT, not a position, so the
            # question is whether that text is still there and still unique.
            # A duplicate fails here; a line pin would have silently taken the
            # first and reported success.
            hits = [i for i, l in enumerate(lines, 1) if expect in l]
            if len(hits) == 1:
                findings.append(Finding(
                    "line_citations", rel, hits[0],
                    "D8: resolves by anchor - %r at line %d" % (expect, hits[0]),
                    is_note=True))
            else:
                findings.append(Finding(
                    "line_citations", rel, None,
                    "D8: anchor %r occurs %d times, expected exactly 1. An "
                    "anchor that is not unique cites whichever copy the reader "
                    "finds first. Cited because: %s" % (expect, len(hits), why)))
            continue
        if lineno > len(lines):
            findings.append(Finding(
                "line_citations", rel, lineno,
                "D8: citation points past the end of the file (%d lines). %s"
                % (len(lines), why)))
            continue
        actual = lines[lineno - 1]
        if expect in actual:
            findings.append(Finding("line_citations", rel, lineno,
                                    "D8: resolves - %r" % expect, is_note=True))
            continue
        hits = [i for i, l in enumerate(lines, 1) if expect in l]
        moved = (" It is now at line %d." % hits[0] if len(hits) == 1
                 else " It now appears on lines %r." % (hits,) if hits
                 else " It is gone from the file.")
        findings.append(Finding(
            "line_citations", rel, lineno,
            "D8: this line no longer contains %r - it reads %r instead.%s "
            "A drifted citation resolves to plausible content and does not "
            "announce itself. Cited because: %s"
            % (expect, actual.strip()[:60], moved, why)))
    return findings


# ---------------------------------------------------------------------------
# D9 (R71/§37) - the manifest's REVERSE direction.
#
# `sha256sum -c MANIFEST.sha256` verifies listed -> disk. It is structurally
# blind to disk -> listed: a file added to the evidence tree without a manifest
# line is invisible to it, and would ship inside the signed commit unattested
# while every check reports OK.
#
# B6 recorded that the two sets happened to coincide (248/248) - a fact about
# that day's contents, not a property of the check. This makes it a property.
# ---------------------------------------------------------------------------

_MANIFEST_REL = "evidence/MANIFEST.sha256"
# Repository-root files the manifest claims via `../` lines. Derived from the
# manifest itself, not restated here.
_MANIFEST_LINE = re.compile(r"^[0-9a-f]{64}  (.+)$", re.M)


def check_manifest_covers_tree(root: Path) -> list[Finding]:
    """D9 - every file in the manifest's claimed scope HAS a manifest line."""
    man = root / _MANIFEST_REL
    if not man.exists():
        return [Finding("manifest_coverage", _MANIFEST_REL, None,
                        "the manifest is missing; nothing attests the evidence tree")]
    listed = set(_MANIFEST_LINE.findall(man.read_text(encoding="utf-8", errors="replace")))
    in_tree = {p for p in listed if not p.startswith("../")}
    up_lines = {p[3:] for p in listed if p.startswith("../")}

    ev = root / "evidence"
    on_disk = {q.relative_to(ev).as_posix() for q in ev.rglob("*") if q.is_file()}
    on_disk.discard("MANIFEST.sha256")          # the manifest cannot list itself

    findings = [Finding("manifest_coverage", _MANIFEST_REL, None,
                        "scope: %d in-tree lines + %d `../` lines; %d files on disk"
                        % (len(in_tree), len(up_lines), len(on_disk)), is_note=True)]

    unlisted = sorted(on_disk - in_tree)
    if unlisted:
        findings.append(Finding(
            "manifest_coverage", _MANIFEST_REL, None,
            "D9: %d file(s) in the evidence tree have NO manifest line and would "
            "ship inside the signed commit unattested: %s. `sha256sum -c` cannot "
            "see this - it only walks what the manifest lists."
            % (len(unlisted), ", ".join(unlisted[:8]) + (" ..." if len(unlisted) > 8 else ""))))
    missing = sorted(in_tree - on_disk)
    if missing:
        findings.append(Finding(
            "manifest_coverage", _MANIFEST_REL, None,
            "D9: the manifest lists %d path(s) that are not on disk: %s"
            % (len(missing), ", ".join(missing[:8]))))
    for rel in sorted(up_lines):
        if not (root / rel).exists():
            findings.append(Finding(
                "manifest_coverage", _MANIFEST_REL, None,
                "D9: the manifest claims repository-root file %r, which does not exist" % rel))
    if not unlisted and not missing:
        findings.append(Finding(
            "manifest_coverage", _MANIFEST_REL, None,
            "D9: manifest coverage is EXACT in both directions (%d files)" % len(on_disk),
            is_note=True))
    return findings


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
    ("/licence/",
     "a draft of the distribution licence. The committed LICENSE lives on the "
     "Phase 1 branch, because the tag attests the registration and not the "
     "distribution -- so on this branch the draft has no content twin and this "
     "check cannot reconcile it by hash. Reproducible: it is the MIT text."),
    # R100/§172.1. NOT committed and NOT deleted: committing it changes what
    # ships; deleting it loses the instrument that produced a recorded finding.
    ("control_char_scan.py",
     "superseded by registered D12. The standalone scanner was the DISCOVERY "
     "instrument for the six control-character findings of R82/D1 - one live "
     "backspace in _K1_enumerate.py, two in prose describing the defect, a "
     "FORM FEED and a BEL in a Windows path inside a dated snapshot, and a BOM "
     "- and D12 now guards the class inside the gate. It is kept as the record "
     "of how the class was found, and declared here because a working file in "
     "neither the repository nor this list is a HALT (§63.2)"),
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
    # Named _bak_*.md / _bak_*.py rather than *.bak, so the suffix rule above does
    # not reach them. Found when one was swept into evidence/ at R80 and D7 flagged
    # its stale declaration hashes.
    ("/_bak_", "pre-edit backup; the post-edit file is in the repo"),
    (".pyc", "compiled bytecode"),
    # Superseded twins: the repository holds a NEWER version of each of these, so
    # the working copy is a stale predecessor, not unlanded content. Verified by
    # name and by the repo file being newer at R76.
    ("/ceremony/CEREMONY_COMMANDS.md", "superseded twin; evidence/ceremony/ is newer"),
    ("/ceremony/COMMIT_PLAN.md", "superseded twin; evidence/ceremony/ is newer"),
    ("/ceremony/DEVIATIONS_DRAFT.md", "superseded twin; evidence/ceremony/ is newer"),
    ("/ceremony/DEVIATIONS_D003_DRAFT.md", "superseded twin; evidence/ceremony/ is newer"),
    ("/ceremony/H34_DRAFT.md", "superseded twin; evidence/ceremony/ is newer"),
    ("/ceremony/X4_REGENERATION_REQUIREMENTS.md", "superseded twin; evidence/ceremony/ is newer"),
    ("/author_review/READ_THROUGH_PACKAGE.md",
     "earlier draft; the repo holds the AUTHORITATIVE frozen baseline 2e23f1f2"),
    ("/fixture_spike/f5/v30a_ceremony_CHECKLIST.md",
     "the repo copy carries the R68 SUPERSEDED banner; this one does not"),
    ("/_x5_truncated_original/", "a deliberately truncated original, kept to reproduce a defect"),
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
                            "reconciled: %d ephemeral, %d large (ruled out at \u00a762.1)"
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


def check_phase_arithmetic(root: Path) -> list[Finding]:
    text = (root / "PREREG.md").read_text(encoding="utf-8")
    f: list[Finding] = []
    m = re.search(
        r"\*\*(\d+)[–-](\d+) working weekends\*\*\s*\(minimum ([\d+\s]+?)=\s*(\d+);\s*"
        r"maximum ([\d+\s]+?)=\s*(\d+)\)", text)
    if not m:
        return [Finding("phase_arithmetic", "PREREG.md", None,
                        "weekend-total sentence not found or not parseable")]
    head_min, head_max = int(m.group(1)), int(m.group(2))
    min_addends = [int(x) for x in m.group(3).split("+")]
    max_addends = [int(x) for x in m.group(5).split("+")]
    stated_min, stated_max = int(m.group(4)), int(m.group(6))
    if sum(min_addends) != stated_min or head_min != stated_min:
        f.append(Finding("phase_arithmetic", "PREREG.md", None,
                         f"minimum addends {min_addends} sum to {sum(min_addends)}, "
                         f"stated {stated_min}, headline {head_min}"))
    if sum(max_addends) != stated_max or head_max != stated_max:
        f.append(Finding("phase_arithmetic", "PREREG.md", None,
                         f"maximum addends {max_addends} sum to {sum(max_addends)}, "
                         f"stated {stated_max}, headline {head_max}"))
    rows = re.findall(
        r"^\|\s*\*\*(\d)\*\*\s*\|[^|]*\|\s*(\d+)(?:[–-](\d+))?\s*wknds?\s*\|", text, re.M)
    if len(rows) != 8:
        f.append(Finding("phase_arithmetic", "PREREG.md", None,
                         f"parsed {len(rows)} phase rows, expected 8"))
    else:
        table_min = [int(lo) for _p, lo, _hi in rows]
        table_max = [int(hi) if hi else int(lo) for _p, lo, hi in rows]
        if table_min != min_addends or table_max != max_addends:
            f.append(Finding("phase_arithmetic", "PREREG.md", None,
                             f"phase-table estimates {table_min}/{table_max} do not "
                             f"match stated addends {min_addends}/{max_addends}"))
    return f


EXPECTED_REQUIREMENT_IDS = frozenset({
    "R6.6-SCHEDULE-RESOLUTION", "R6.6-EVIDENCE-OUTCOME", "R6.6-LEGAL-PAIRS",
    "R7.2-PROOF-YIELD", "R7.2-EVIDENCE-YIELD", "R7.2-CONDITIONAL-RECALL",
    "R7.2-COHORT-SENSITIVITY", "R7.2-DISCOVERY-RECALL", "R7.2-UNPROBED-RATE",
    "R7.2.1-FEATURE-COHORT-PRECISION", "R7.2.1-COMPLETION-RATE",
    "R7.2.1-INCOMPLETION-RATE", "R7.7-CLEAN-FINDING-RATE",
    "R10.2-RUNTIME-GATES", "R8.3-PROVEN-ASSERTION"})

_RID = re.compile(r"\bR\d+(?:\.\d+)*-[A-Z][A-Z0-9-]*[A-Z0-9]\b")


def check_requirement_ids(root: Path) -> list[Finding]:
    reducer = root / "protocol" / "runtime_reference.py"
    if not reducer.exists():
        return [Finding("requirement_ids", "protocol/runtime_reference.py", None, "missing")]
    found = frozenset(_RID.findall(reducer.read_text(encoding="utf-8")))
    f = []
    for missing in sorted(EXPECTED_REQUIREMENT_IDS - found):
        f.append(Finding("requirement_ids", "protocol/runtime_reference.py", None,
                         f"requirement ID {missing} not implemented in the reducer"))
    for unknown in sorted(found - EXPECTED_REQUIREMENT_IDS):
        f.append(Finding("requirement_ids", "protocol/runtime_reference.py", None,
                         f"unknown requirement ID {unknown}: IDs label existing "
                         "clauses and may not be invented"))
    secs = sections_of((root / "PREREG.md").read_text(encoding="utf-8"))
    for rid in sorted(EXPECTED_REQUIREMENT_IDS):
        section = rid[1:].split("-", 1)[0]
        if section not in secs:
            f.append(Finding("requirement_ids", "PREREG.md", None,
                             f"{rid} points at §{section}, which does not exist"))
    return f


def check_parking_lot(root: Path) -> list[Finding]:
    """PREREG §11 item 1 (v28): PARKING_LOT.md contains ONLY the §13.9 entry.
    'Only' is enforced over every line, not just dash bullets — headings, the
    review-cadence pointer, and blank lines are structure; any other content
    is a second entry however it is punctuated."""
    path = root / "PARKING_LOT.md"
    if not path.exists():
        return [Finding("parking_lot", "PARKING_LOT.md", None,
                        "missing (PREREG §11 item 1)")]
    text = path.read_text(encoding="utf-8")
    f: list[Finding] = []
    entries: list[str] = []
    for i, ln in enumerate(text.splitlines(), start=1):
        stripped = ln.strip()
        if not stripped or stripped.startswith("#") or "Reviewed Sundays only" in stripped:
            continue
        if stripped.startswith("- "):
            entries.append(stripped)
            continue
        f.append(Finding("parking_lot", "PARKING_LOT.md", i,
                         f"content beyond the single §13.9 entry: {stripped[:80]!r} "
                         "(PREREG §11 item 1: 'containing only the §13.9 entry')"))
    if len(entries) != 1:
        f.append(Finding("parking_lot", "PARKING_LOT.md", None,
                         f"{len(entries)} entries found; §11 item 1 requires "
                         "exactly the one §13.9 entry"))
        return f
    for phrase in ("noise-floor fallback", "nondeterministic pipelines",
                   "amended registration", "evaluation partition"):
        if phrase not in entries[0]:
            f.append(Finding("parking_lot", "PARKING_LOT.md", None,
                             f"the single entry does not carry the §13.9 phrase "
                             f"{phrase!r}"))
    return f


# PREREG §11 item 1 (v28): the reducer's minimum public surface.
REQUIRED_REDUCER_FUNCTIONS = (
    "resolve_schedule_state", "resolve_evidence_outcome",
    "derive_evidence_events", "derive_reported_findings",
    "compute_runtime_metrics", "apply_runtime_gates",
    "evaluate_runtime_assertions",
)


def check_reducer_functions(root: Path) -> list[Finding]:
    """§11 item 1's minimum reducer surface, checked on the imported module
    rather than by source grep — a `def` line inside a docstring is not a
    function. (The import resolves against this repository's protocol
    package; semantic adequacy is the trace suite's job, not this check's.)"""
    reducer = root / "protocol" / "runtime_reference.py"
    if not reducer.exists():
        return [Finding("reducer_functions", "protocol/runtime_reference.py",
                        None, "missing")]
    import protocol.runtime_reference as rr_module
    prereg = (root / "PREREG.md").read_text(encoding="utf-8")
    sec_11 = sections_of(prereg).get("11", "")
    f: list[Finding] = []
    for name in REQUIRED_REDUCER_FUNCTIONS:
        if not callable(getattr(rr_module, name, None)):
            f.append(Finding("reducer_functions", "protocol/runtime_reference.py",
                             None, f"§11 item 1 minimum function {name} is not "
                             "a callable in the module"))
        if f"`{name}`" not in sec_11:
            f.append(Finding("reducer_functions", "PREREG.md", None,
                             f"§11 item 1 does not list required reducer function {name}"))
    return f


def check_suppression_anchor(root: Path) -> list[Finding]:
    """v30 §7.2.1's suppression rule is anchored against the reducer the same
    way the legality table and unit grammar are: the prose sentence must be
    present while the reducer implements suppression, so neither can be
    edited away while the other stands (PREREG §6.6.1)."""
    import protocol.runtime_reference as rr_module
    prereg = (root / "PREREG.md").read_text(encoding="utf-8")
    sec = sections_of(prereg).get("7.2.1", "")
    f: list[Finding] = []
    reducer_suppresses = all(
        isinstance(getattr(rr_module, name, None), type)
        for name in ("SuppressedMetric", "SuppressedGate"))
    prose_has_rule = (
        "publishes its counts and suppresses its yields, rates, and gates" in sec)
    # v30 closure: the rule's granularity definition is pinned alongside the
    # rule itself — the reducer's suppression trigger iterates every labelled
    # case (clean included), and that reading must stay stated in §7.2.1.
    prose_has_definition = (
        "every labelled case in the body, clean cases included" in sec)
    if reducer_suppresses and not prose_has_rule:
        f.append(Finding("suppression_anchor", "PREREG.md", None,
                         "the reducer suppresses all-not_applicable combinations "
                         "but §7.2.1 no longer carries the suppression sentence"))
    if reducer_suppresses and not prose_has_definition:
        f.append(Finding("suppression_anchor", "PREREG.md", None,
                         "§7.2.1 no longer defines 'scope-eligible case' as every "
                         "labelled case in the body, clean cases included — the "
                         "reading the reducer's whole-body trigger implements"))
    if prose_has_rule and not reducer_suppresses:
        f.append(Finding("suppression_anchor", "protocol/runtime_reference.py", None,
                         "§7.2.1 declares the suppression rule but the reducer "
                         "does not implement SuppressedMetric/SuppressedGate"))
    return f


def check_unit_grammar(root: Path) -> list[Finding]:
    """Diff the reducer's UNIT_GRAMMAR against §7.0 rule 2's enumeration."""
    from protocol.runtime_reference import UNIT_GRAMMAR
    prereg = (root / "PREREG.md").read_text(encoding="utf-8")
    m = re.search(r"Units come from the fixed grammar:\s*([^.]+)\.", prereg)
    if not m:
        return [Finding("unit_grammar", "PREREG.md", None,
                        "§7.0 rule 2's unit-grammar sentence not found")]
    doc_units = frozenset(
        u.strip("*` ").replace("-", "_")
        for u in m.group(1).split(",") if u.strip("*` "))
    f = []
    for unit in sorted(doc_units - UNIT_GRAMMAR):
        f.append(Finding("unit_grammar", "protocol/runtime_reference.py", None,
                         f"grammar unit {unit!r} (§7.0 rule 2) missing from the reducer"))
    for unit in sorted(UNIT_GRAMMAR - doc_units):
        f.append(Finding("unit_grammar", "PREREG.md", None,
                         f"reducer unit {unit!r} absent from §7.0 rule 2's grammar"))
    return f


def check_legality_table(root: Path) -> list[Finding]:
    """Diff PREREG §6.6's legality table against the reducer's LEGAL_PAIRS."""
    from protocol.runtime_reference import (
        LEGAL_PAIRS, EvidenceOutcome, ScheduleStateKind)
    text = (root / "PREREG.md").read_text(encoding="utf-8")
    lines = [ln.lstrip("> ").strip() for ln in text.splitlines()]
    header = None
    for i, ln in enumerate(lines):
        if re.match(r"\|\s*`schedule_state`\s*\|\s*`finding`\s*\|"
                    r"\s*`observed_silence`\s*\|\s*`none`\s*\|", ln):
            header = i
            break
    if header is None:
        return [Finding("legality_table", "PREREG.md", None, "§6.6 legality table not found")]
    doc_pairs = set()
    outcome_order = (EvidenceOutcome.FINDING, EvidenceOutcome.OBSERVED_SILENCE,
                     EvidenceOutcome.NONE)
    for ln in lines[header + 2:]:
        if not ln.startswith("|"):
            break
        cells = [c.strip() for c in ln.strip("|").split("|")]
        if len(cells) != 4:
            break
        name = re.sub(r"\(.*\)", "", cells[0].strip("`* ")).strip("`")
        try:
            kind = ScheduleStateKind(name)
        except ValueError:
            return [Finding("legality_table", "PREREG.md", None,
                            f"unknown schedule_state {name!r} in §6.6 table")]
        for cell, outcome in zip(cells[1:], outcome_order):
            if "✓" in cell:
                doc_pairs.add((kind, outcome))
    f = []
    for kind, outcome in sorted(doc_pairs - LEGAL_PAIRS, key=lambda p: (p[0].value, p[1].value)):
        f.append(Finding("legality_table", "PREREG.md", None,
                         f"§6.6 legal pair {kind.value} x {outcome.value} missing from reducer"))
    for kind, outcome in sorted(LEGAL_PAIRS - doc_pairs, key=lambda p: (p[0].value, p[1].value)):
        f.append(Finding("legality_table", "protocol/runtime_reference.py", None,
                         f"reducer legal pair {kind.value} x {outcome.value} absent from §6.6"))
    return f


# ---------------------------------------------------------------------------
# implementation / release stages (owned checks; artifacts do not exist yet,
# so running them now fails loudly rather than passing silently)
# ---------------------------------------------------------------------------

def _artifact_absent(check: str, what: str, owner_section: str) -> list[Finding]:
    return [Finding(check, "leakaudit/", None,
                    f"{what} does not exist yet ({owner_section}); this check "
                    "cannot pass before the implementation it verifies")]


def check_ties_comparator_vs_mask(root: Path) -> list[Finding]:
    return _artifact_absent("ties_comparator_vs_shipped_mask",
                            "the shipped availability mask", "PREREG §6.8")


def check_l31b_inequalities(root: Path) -> list[Finding]:
    return _artifact_absent("l31b_inequalities_vs_shipped_rule",
                            "the shipped L3.1b rule", "PREREG §4.3, §6.8")


def check_shipping_defaults(root: Path) -> list[Finding]:
    return _artifact_absent("shipping_defaults_vs_validated_runtime",
                            "shipping defaults / frozen [validated.runtime]",
                            "PREREG §6.8")


def check_deleted_config_rejected(root: Path) -> list[Finding]:
    return _artifact_absent("deleted_config_fields_rejected",
                            "the config loader", "PREREG §6.8")


def check_cost_script(root: Path) -> list[Finding]:
    return _artifact_absent("cost_script_total",
                            "the CI cost script over VALIDATED_CONFIG", "PREREG §12")


def check_readme_numbers(root: Path) -> list[Finding]:
    return _artifact_absent("readme_numbers_regenerated",
                            "the README and its generating scripts", "PREREG §6.8")


def check_package_defaults(root: Path) -> list[Finding]:
    return _artifact_absent("package_defaults", "the built package", "PREREG §6.8")


# ---------------------------------------------------------------------------
# CRITERION 5 - INSTALLABLE BY A STRANGER (PREREG.md section 10.2 item 5).
#
# WHY THIS CHECK HAS TEETH AND ITS PREDECESSOR DID NOT. Until 31 August 2026
# this function returned `_artifact_absent(...)`: "the installable package does
# not exist yet; this check cannot pass before the implementation it verifies".
# The package had existed for days. The criterion carrying the only DATE in the
# kill list had an instrument that had never looked at the thing it names, and
# that stated a falsehood while declining to look.
#
# WHAT IT TESTS. Every limb below is a defect that HAPPENED here, not one
# imagined for completeness:
#
#   (1) PACKAGING METADATA EXISTS AND PARSES. A project with no build backend
#       cannot be installed by anyone, and a pyproject that only PARSES is not
#       evidence of anything - the metadata build failed on a PEP 639 licence
#       conflict while the file parsed cleanly throughout.
#   (2) THE DECLARED LICENCE FILE IS PRESENT. `license-files` naming a file that
#       is not in the tree ships a package a stranger has no licence to use.
#   (3) EVERY FIRST-PARTY PACKAGE A SHIPPED MODULE IMPORTS IS ITSELF SHIPPED.
#       This is the limb that fired for real. `leakaudit.contract` imports
#       `protocol.runtime_reference`; `protocol/` was not in the distribution;
#       the first SUCCESSFUL install raised ModuleNotFoundError on first use,
#       after the metadata build had already gone green. BUILDING IS NOT
#       INSTALLING AND INSTALLING IS NOT IMPORTING.
#   (4) EVERY DECLARED PACKAGE DIRECTORY EXISTS AND CARRIES A MODULE.
#   (5) EVERY THIRD-PARTY IMPORT OF A SHIPPED MODULE IS A DECLARED DEPENDENCY.
#       An import satisfied by the development environment and undeclared in the
#       metadata works on this machine and nowhere else, which is precisely the
#       failure mode "installable by a stranger" names.
#   (6) THE FRONT DOOR IS TRUE AND REACHABLE. A public README asserting that no
#       implementation exists, beside a package that installs, is a stranger's
#       first and worst encounter with this repository. It stood for days. The
#       assertion is a check now rather than a memory.
#
# WHAT IT DOES NOT TEST, stated so a green result is not read as more than it
# is: it does not build, install, or import anything, and it reads one
# machine's checkout. It cannot see a dependency floor that fails to resolve
# elsewhere - `numpy>=1.26`, `pandas>=2.1`, `pyarrow>=14` are untested downward
# against a pandas 2.x resolution (INSTALL.md records this). AN INSTALL ON A
# SECOND MACHINE IS THE TEST THIS CANNOT BE, and this check never stands in for
# it.
# ---------------------------------------------------------------------------
_INSTALL_PYPROJECT = "pyproject.toml"
_INSTALL_README = "README.md"
_INSTALL_DOC = "INSTALL.md"

# Any import, indented or not, so a LAZY import inside a function is seen. The
# lazy ones are exactly the ones a stranger discovers at run time rather than at
# install time, which makes them the ones worth catching.
_INSTALL_IMPORT = re.compile(
    r"^[ \t]*(?:from|import)[ \t]+([A-Za-z_][A-Za-z0-9_]*)", re.M)

# Imports that are deliberately NOT dependencies, each with its ground. An
# exemption that matches nothing is reported as a note, per the D12 rule: an
# exemption nobody exercises is either stale or was never right.
_INSTALL_UNDECLARED_OK = {
    "fixture":
        "the acceptance fixture's own producing module, imported lazily by "
        "fixture_adapter and NOT packaged. A stranger installing this gets the "
        "auditor, not the fixture; the adapter raises FixtureUnavailable with "
        "its reason when it is absent. Declared in pyproject.toml's own header "
        "and in INSTALL.md's 'what a stranger gets' section.",
    "phase5_ml_fixture":
        "same ground: the fixture's second producing module, same lazy import "
        "site, same non-packaging decision.",
}

# The sentence that stood on the public front page while the package installed.
# Keyed to the claim, not to a line, because the line will move.
_INSTALL_README_FALSE_CLAIMS = (
    "No detector implementation exists",
    "pre-registration, not a tool",
)

# QUOTING A RETIRED CLAIM IS ALLOWED. PARKING A LIVE ONE IN A BLOCKQUOTE IS NOT.
#
# R190 §3. The first version excluded EVERY blockquoted line, which is too wide
# in the direction that matters: a false assertion sitting in an unmarked
# blockquote passes the check and reads to a human as the page's own voice --
# blockquotes are used for emphasis at least as often as for quotation. The
# exemption is meant for the RECORD of a claim that has been withdrawn, so it
# now asks the block to say so.
#
# A blockquote block is excluded from the scan only if the block itself carries
# one of these markers. They are matched case-insensitively over the whole
# block, not per line, because the marker and the claim are rarely on the same
# line once the text wraps. Each excluded block is REPORTED as a note naming the
# marker that excused it, so the exemption is visible rather than silent.
_INSTALL_RETIREMENT_MARKERS = (
    "stood here until", "retired", "no longer", "superseded", "corrected",
    "was false", "were false", "formerly", "used to say", "withdrawn",
)


def _install_first_party(root: Path) -> dict[str, Path]:
    """Top-level importable directories of this repository, by name."""
    out: dict[str, Path] = {}
    for parent in (root, root / "src"):
        if not parent.is_dir():
            continue
        for child in sorted(parent.iterdir()):
            if not child.is_dir() or child.name.startswith((".", "_")):
                continue
            if any(child.glob("*.py")):
                out.setdefault(child.name, child)
    return out


def _install_requirement_names(deps) -> set[str]:
    names = set()
    for spec in deps or ():
        m = re.match(r"[A-Za-z0-9._-]+", str(spec))
        if m:
            names.add(m.group(0).lower().replace("-", "_"))
    return names


def _install_readme_body(text: str) -> tuple[str, list[tuple[int, str]]]:
    """The page's own assertions, with MARKED retirement blocks removed.

    Returns the body with whitespace collapsed -- a claim that wraps across two
    lines is the same claim, and a line-by-line scan misses it, which is how the
    real one survived -- together with (line, marker) for each block excused, so
    every exemption is printed.
    """
    lines = text.split("\n")
    kept: list[str] = []
    excused: list[tuple[int, str]] = []
    i = 0
    while i < len(lines):
        if not lines[i].lstrip().startswith(">"):
            kept.append(lines[i])
            i += 1
            continue
        start = i
        block = []
        while i < len(lines) and lines[i].lstrip().startswith(">"):
            block.append(lines[i])
            i += 1
        joined = " ".join(block).lower()
        marker = next((m for m in _INSTALL_RETIREMENT_MARKERS if m in joined), None)
        if marker is None:
            # An unmarked blockquote is the page speaking, not the page quoting.
            kept.extend(block)
        else:
            excused.append((start + 1, marker))
    return re.sub(r"\s+", " ", " ".join(kept)), excused


def check_installability(root: Path) -> list[Finding]:
    """Criterion 5 - is this installable by a stranger? Reads, never installs."""
    root = Path(root).resolve()
    f: list[Finding] = []

    # ---- (1) metadata --------------------------------------------------
    ppath = root / _INSTALL_PYPROJECT
    if not ppath.exists():
        return [Finding("installability", _INSTALL_PYPROJECT, None,
                        "C5: there is no packaging metadata. Nothing below can "
                        "be judged and the criterion is not discharged.")]
    try:
        cfg = tomllib.loads(ppath.read_text(encoding="utf-8"))
    except Exception as exc:                                # noqa: BLE001
        return [Finding("installability", _INSTALL_PYPROJECT, None,
                        "C5: packaging metadata does not parse: %s" % exc)]

    project = cfg.get("project") or {}
    build = cfg.get("build-system") or {}
    if not build.get("build-backend"):
        f.append(Finding("installability", _INSTALL_PYPROJECT, None,
                         "C5: no [build-system] build-backend; pip has nothing "
                         "to build this with"))
    for field in ("name", "version", "requires-python"):
        if not project.get(field):
            f.append(Finding("installability", _INSTALL_PYPROJECT, None,
                             "C5: [project] declares no %s" % field))

    # ---- (2) licence ---------------------------------------------------
    if not project.get("license"):
        f.append(Finding("installability", _INSTALL_PYPROJECT, None,
                         "C5: no licence expression; a stranger has no licence "
                         "to use what they installed"))
    licence_files = project.get("license-files") or []
    if not licence_files:
        f.append(Finding("installability", _INSTALL_PYPROJECT, None,
                         "C5: license-files is empty; the licence text is not "
                         "shipped with the distribution"))
    for pattern in licence_files:
        if not list(root.glob(str(pattern))):
            f.append(Finding("installability", _INSTALL_PYPROJECT, None,
                             "C5: license-files names %r and no file in the "
                             "tree matches it" % pattern))

    # ---- (3)/(4) what ships, and whether it holds together -------------
    tools_cfg = (cfg.get("tool") or {}).get("setuptools") or {}
    shipped = list(tools_cfg.get("packages") or [])
    pkg_dir = dict(tools_cfg.get("package-dir") or {})
    if not shipped:
        f.append(Finding("installability", _INSTALL_PYPROJECT, None,
                         "C5: no explicit package list. Auto-discovery decides "
                         "what ships, and what ships is exactly the question "
                         "this check exists to answer."))
    dirs: dict[str, Path] = {}
    for name in shipped:
        rel = pkg_dir.get(name, name)
        d = root / rel
        if not d.is_dir():
            f.append(Finding("installability", _INSTALL_PYPROJECT, None,
                             "C5: package %r maps to %s, which is not a "
                             "directory" % (name, rel)))
            continue
        if not any(d.glob("*.py")):
            f.append(Finding("installability", _INSTALL_PYPROJECT, None,
                             "C5: package %r maps to %s, which carries no "
                             "module" % (name, rel)))
            continue
        dirs[name] = d

    first_party = _install_first_party(root)
    declared = _install_requirement_names(project.get("dependencies"))
    stdlib = set(getattr(sys, "stdlib_module_names", ()))
    seen_exempt: set[str] = set()
    modules = 0
    for name, d in sorted(dirs.items()):
        for src in sorted(d.rglob("*.py")):
            modules += 1
            text = src.read_text(encoding="utf-8", errors="replace")
            rel = src.relative_to(root).as_posix()
            for m in _INSTALL_IMPORT.finditer(text):
                mod = m.group(1)
                line = text.count("\n", 0, m.start()) + 1
                if mod in ("__future__",) or mod in stdlib or mod in dirs:
                    continue
                if mod in first_party:
                    f.append(Finding(
                        "installability", rel, line,
                        "C5: imports first-party package %r, which is NOT in "
                        "the shipped package list. This installs and then "
                        "fails to import - the exact defect that shipped once "
                        "already." % mod))
                    continue
                if mod in _INSTALL_UNDECLARED_OK:
                    seen_exempt.add(mod)
                    continue
                if mod.lower().replace("-", "_") not in declared:
                    f.append(Finding(
                        "installability", rel, line,
                        "C5: imports %r, which is neither stdlib, nor shipped, "
                        "nor a declared dependency. It resolves here because "
                        "this environment happens to carry it." % mod))
    for mod, why in sorted(_INSTALL_UNDECLARED_OK.items()):
        if mod not in seen_exempt:
            f.append(Finding("installability", _INSTALL_PYPROJECT, None,
                             "C5: the exemption for %r fired on nothing. An "
                             "exemption nobody exercises is stale or was never "
                             "right. Ground on record: %s" % (mod, why),
                             is_note=True))

    # ---- (6) the front door --------------------------------------------
    readme = root / _INSTALL_README
    doc = root / _INSTALL_DOC
    if not doc.exists():
        f.append(Finding("installability", _INSTALL_DOC, None,
                         "C5: there are no install instructions"))
    if not readme.exists():
        f.append(Finding("installability", _INSTALL_README, None,
                         "C5: there is no front page"))
    else:
        rtext = readme.read_text(encoding="utf-8", errors="replace")
        if doc.exists() and _INSTALL_DOC not in rtext:
            f.append(Finding("installability", _INSTALL_README, None,
                             "C5: the front page never mentions %s. "
                             "Instructions a stranger cannot find are not "
                             "instructions." % _INSTALL_DOC))
        flat, excused = _install_readme_body(rtext)
        for line, marker in excused:
            f.append(Finding("installability", _INSTALL_README, line,
                             "C5: blockquote excluded from the scan as the "
                             "record of a retired claim, on the marker %r"
                             % marker, is_note=True))
        for claim in _INSTALL_README_FALSE_CLAIMS:
            if claim in flat:
                f.append(Finding(
                    "installability", _INSTALL_README, None,
                    "C5: the front page asserts %r beside a package that "
                    "installs. A blockquote excuses it only where the block "
                    "says the claim is retired; an unmarked blockquote is the "
                    "page speaking, not the page quoting." % claim))

    f.append(Finding(
        "installability", _INSTALL_PYPROJECT, None,
        "C5: %d package(s) shipped (%s), %d module(s) scanned, %d declared "
        "dependency(ies). NOT TESTED HERE: build, install, import, or any "
        "resolution other than this machine's."
        % (len(dirs), ", ".join(sorted(dirs)) or "none", modules,
           len(declared)), is_note=True))
    return f


# ---------------------------------------------------------------------------
# Stage wiring
# ---------------------------------------------------------------------------

# --------------------------------------------------------------------------
# D12 - control characters in the shipping corpus
# --------------------------------------------------------------------------
# WHY. Four incidents this phase from one mechanism: a `\b` intended as a regex
# word boundary, written through a shell heredoc or a non-raw Python string,
# becomes a literal BACKSPACE (0x08). The regex still compiles; it can never
# match. Twice that produced a FALSE CLEAN from a sweep (§88); once a false
# positive (R81/C2). A control byte is invisible in terminal, editor, diff and
# review alike, so inspection cannot find it - only a byte-exact scan can.
#
# DOMAIN (stated, per H-L21). Bytes only: the C0 range except TAB/LF/CR, DEL,
# the C1 range, and Unicode format/unassigned characters (categories Cc, Cf, Co,
# Cs, Cn, Zl, Zp). It does NOT judge whether a character is semantically wrong -
# a THIN SPACE renders, so it is reported as a note, never as a failure.
#
# EXEMPTIONS ARE VALUE-SCOPED, NOT LINE-SCOPED (the D5/D6/D7 lesson). Keyed by
# (path, codepoint), so a NEW control character in an exempted file still fires.
# An exemption that fires on nothing is REPORTED - that is what caught the §87
# regression.
_CTRL_ALLOWED = {0x09, 0x0A, 0x0D}
_CTRL_INVISIBLE_CATS = {"Cc", "Cf", "Co", "Cs", "Cn", "Zl", "Zp"}
_CTRL_NOTE_ONLY = {0x00A0, 0x2007, 0x2009, 0x202F, 0x205F, 0x3000, 0x1680}

_CTRL_EXEMPT: dict[tuple[str, int], str] = {
    ("evidence/fixture_spike/_snapshots/PRE_R9_HASHES.txt", 0x0C):
        "dated snapshot (R13 - evidence artifacts are never adjusted). A Windows "
        "path `fixture_spike\\f4\\...` written through a non-raw string: `\\f` "
        "became FORM FEED. The corrupted path is the record; correcting it would "
        "falsify what was written that day.",
    ("evidence/fixture_spike/_snapshots/PRE_R9_HASHES.txt", 0x07):
        "same line, same cause: `\\a` in `availability_...` became BEL (R13).",
    ("evidence/fixture_spike/c4/build_t1_c4_comparison_output.txt", 0xFEFF):
        "BOM at offset 0 of a captured console output file (R13, dated record). "
        "Emitted by the capturing shell, not by any decision.",
    ("evidence/amendment/_K1_enumerate.py", 0x08):
        "**RECORDED LIVE DEFECT, R81/D1 - exempted so the gate reports rather "
        "than blocks; NOT waived.** `MARK = re.compile(r\"^\\*\\*§[\\d.]+\\s+"
        "(line|item|items)<BS>\")` - the `\\b` is a literal BACKSPACE, so MARK "
        "never matches and the marker split it guards never runs: the enumeration "
        "UNDER-SPLITS. The file is a dated build record brought in at R74/§56; no "
        "shipping document quotes a count derived from it. Author ruling pending.",
}


def check_control_characters(root: Path) -> list[Finding]:
    """D12 - no non-printing control character in the shipping corpus."""
    import unicodedata

    six = ["PREREG.md", "DESIGN.md", "HISTORY.md", "tools/check_registration.py",
           "protocol/runtime_reference.py", "AVAILABILITY_DECLARATION.md"]
    man = root / _MANIFEST_REL
    if not man.exists():
        return [Finding("control_characters", _MANIFEST_REL, None,
                        "the manifest is missing; D12's population cannot be built")]

    pop: dict[str, Path] = {}
    for rel in six:
        pop[rel] = root / rel
    for rel in _MANIFEST_LINE.findall(man.read_text(encoding="utf-8", errors="replace")):
        p = (root / "evidence" / rel).resolve()
        try:
            pop[p.relative_to(root).as_posix()] = p
        except ValueError:
            pop[rel] = p
    pop[_MANIFEST_REL] = man

    findings: list[Finding] = []
    scanned = notonly = skipped = 0
    fired: set[tuple[str, int]] = set()

    for rel, path in sorted(pop.items()):
        if not path.exists() or path.is_dir():
            continue
        try:
            text = path.read_bytes().decode("utf-8")
        except (UnicodeDecodeError, OSError):
            skipped += 1
            continue
        scanned += 1
        off = 0
        for idx, ch in enumerate(text):
            cp = ord(ch)
            step = len(ch.encode("utf-8"))
            if cp in _CTRL_ALLOWED:
                off += step
                continue
            bad = (cp < 0x20 or cp == 0x7F or 0x80 <= cp <= 0x9F
                   or unicodedata.category(ch) in _CTRL_INVISIBLE_CATS)
            if bad:
                if (rel, cp) in _CTRL_EXEMPT:
                    fired.add((rel, cp))
                else:
                    ctx = text[max(0, idx - 34):idx + 34].replace("\n", "\\n")
                    findings.append(Finding(
                        "control_characters", rel, None,
                        "D12: non-printing character U+%04X at byte offset %d - "
                        "content no decision produced. Context: %r" % (cp, off, ctx)))
            elif cp in _CTRL_NOTE_ONLY:
                notonly += 1
            off += step

    findings.insert(0, Finding(
        "control_characters", _MANIFEST_REL, None,
        "population: %d paths (six-file set + manifest entries + the manifest); "
        "%d scanned as UTF-8, %d not UTF-8 text (binary/console captures, "
        "separately verified control-free at R81/D1); %d note-only space "
        "characters; %d value-scoped exemptions"
        % (len(pop), scanned, skipped, notonly, len(_CTRL_EXEMPT)), is_note=True))

    for key, why in sorted(_CTRL_EXEMPT.items()):
        if key in fired:
            findings.append(Finding("control_characters", key[0], None,
                                    "exempt U+%04X - %s" % (key[1], why), is_note=True))
        else:
            findings.append(Finding(
                "control_characters", key[0], None,
                "D12: this exemption fired on nothing - U+%04X is no longer present. "
                "Remove it, or find what moved." % key[1]))
    return findings


# --------------------------------------------------------------------------
# D13 - BLOCK_MANIFEST.md's summary must equal its own table
# --------------------------------------------------------------------------
# This is D1's class: a count restated away from its authority drifts, and the
# drift is invisible because both copies read plausibly. It is registered as its
# own check rather than folded into check_single_source so that a failure names
# the thing that failed instead of surfacing under an unrelated heading.
#
# The TABLE is the authority (R84/§100.2): it carries the growth declared in
# `_POPULATION_CHANGES.md`. The prose does not, and for three rounds it said 33
# blocks / 42 entries while the table held 36 / 45.
_BM_REL = "evidence/amendment/BLOCK_MANIFEST.md"
_BM_ROW = re.compile(r"^\|\s*(\d+)([a-z]?)\s*\|")


def check_block_manifest_counts(root: Path) -> list[Finding]:
    """D13 - every count in the summary is derived from the §A table."""
    p = root / _BM_REL
    if not p.exists():
        return [Finding("block_manifest_counts", _BM_REL, None, "missing")]
    lines = p.read_text(encoding="utf-8").split("\n")
    try:
        s = next(i for i, l in enumerate(lines) if l.startswith("## §A —"))
        e = next(i for i, l in enumerate(lines[s + 1:], s + 1)
                 if l.startswith("## §B") or l.startswith("## §C"))
    except StopIteration:
        return [Finding("block_manifest_counts", _BM_REL, None,
                        "D13: the §A table could not be located; the summary cannot be checked")]

    rows = [l for l in lines[s:e] if _BM_ROW.match(l)]
    groups: dict[int, int] = {}
    for l in rows:
        m = _BM_ROW.match(l)
        groups[int(m.group(1))] = groups.get(int(m.group(1)), 0) + 1
    blocks = len(groups)
    multi = sum(1 for v in groups.values() if v > 1)
    entries = len(rows)
    apparatus = sum(1 for l in rows if "APPARATUS" in l.upper())
    claimed = entries - apparatus

    text = "\n".join(lines)
    f = [Finding("block_manifest_counts", _BM_REL, None,
                 "derived from the §A table: %d blocks, %d multi-site, %d entries, "
                 "%d claimed, %d apparatus" % (blocks, multi, entries, claimed, apparatus),
                 is_note=True)]

    def want(pattern, expected, what):
        m = re.search(pattern, text)
        if not m:
            f.append(Finding("block_manifest_counts", _BM_REL, None,
                             "D13: could not find the summary's %s - the assertion fired on "
                             "nothing, which means the wording moved" % what))
            return
        got = int(m.group(1))
        if got != expected:
            f.append(Finding("block_manifest_counts", _BM_REL, None,
                             "D13: summary says %s = %d; the §A table gives %d. The TABLE is the "
                             "authority (§100.2)." % (what, got, expected)))

    want(r"`_K1_population_FROZEN\.json`:\s*\*\*(\d+) blocks\*\*", blocks, "block count")
    want(r"of the (\d+) are multi-site runs", blocks, "multi-site denominator")

    # F2.3 - THE MULTI-SITE COUNT ITSELF, not just its denominator.
    # Until R85 this check asserted only the denominator, so it would have caught
    # "Six of the 33" going stale to "Six of the 36" and NOT the fact that "Six"
    # was arithmetically wrong at the freeze: 33 blocks with six expanded runs
    # cannot give 42 entries, only five can. Staleness and a wrong original are
    # DIFFERENT failures and a check that catches one is not guarding the other.
    # The figure is spelled as a word, so the word is what gets compared.
    _WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
              "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12}
    m = re.search(r"\*\*([A-Za-z]+)\*\* of the \d+ are multi-site runs", text)
    if not m:
        f.append(Finding("block_manifest_counts", _BM_REL, None,
                         "D13: could not find the summary's multi-site COUNT - the assertion "
                         "fired on nothing, which means the wording moved"))
    else:
        got = _WORDS.get(m.group(1).lower())
        if got is None:
            f.append(Finding("block_manifest_counts", _BM_REL, None,
                             "D13: the multi-site count reads %r, which is not a number word "
                             "this check can read - it is REPORTED rather than skipped"
                             % m.group(1)))
        elif got != multi:
            f.append(Finding("block_manifest_counts", _BM_REL, None,
                             "D13: summary says %s (%d) multi-site runs; the §A table has %d "
                             "(blocks with more than one lettered row). The TABLE is the "
                             "authority (§100.2)." % (m.group(1), got, multi)))
    # The entry arithmetic must close, independently of any prose figure.
    if entries != blocks - multi + sum(v for v in groups.values() if v > 1):
        f.append(Finding("block_manifest_counts", _BM_REL, None,
                         "D13: the table's own arithmetic does not close: %d blocks - %d "
                         "multi-site + %d expanded rows != %d entries"
                         % (blocks, multi, sum(v for v in groups.values() if v > 1), entries)))

    want(r"giving\s*\*\*(\d+) entries\*\*", entries, "entry count")
    want(r"## §A — Population A: (\d+) blocks", blocks, "§A heading block count")
    want(r"## §A — Population A: \d+ blocks, (\d+) entries", entries, "§A heading entry count")
    want(r"\*\*Entries: (\d+)\.", entries, "totals line entries")
    want(r"Claimed by a hunk: (\d+)\.", claimed, "totals line claimed")
    want(r"Apparatus: (\d+)\.", apparatus, "totals line apparatus")
    return f


# --------------------------------------------------------------------------
# D14 - BLOCK REACHABILITY: every normative block in the source of record is
# reachable by at least one record
# --------------------------------------------------------------------------
# WHY IT IS A DIFFERENT QUESTION FROM §57.3(b) (§109.2). Both directions of
# §57.3(b) range over CLAUSE blocks - the `### SC-*` headers. §10.1-C2op and
# §10.1-C2ret are not clause blocks; each names its target in its own heading.
# They were therefore outside the population of every existing check, sat in the
# source of record for three rounds unreachable by any record, and the diff had
# no hunk at PREREG.md line 1022 while every check reported clean.
#
# POPULATION (§30.1): every block in SCHEMA_SET_FINAL.md PART 1 carrying
# operative text - blockquoted or fenced body lines longer than 25 characters.
# BLOCKS, not clause blocks.
#
# EXCLUSIONS (§30.1), each justified, none silent:
#   - lines VERBATIM IN PREREG.md: anchors quoted for matching and instance
#     records quoting registered sites. Excluded by what they ARE, mechanically.
#   - SUPERSESSION MARKER: metadata, carried in each record's `supersession`
#     field and never inserted. Uniform - no such block reaches the diff.
#   - SC-12(w): descriptive wrapper; the applied limb is the separate
#     `OPERATIVE v30a TEXT at line 929` block, which IS reachable.
#   - §AB / §AC: the source declares them "drafted, not applied".
_D14_HDR = re.compile(
    r"^\*\*(INSERTION TEXT|INSERTION POINT|THE CLAUSE|SUPERSESSION MARKER|DATA THE"
    r"|ROWS COVERED|OPERATIVE v30a TEXT|INSERT AFTER|ANCHOR|WHY|Why|Corroboration"
    r"|SC-12\(w\))|^### |^#### |^## |^# ")
_D14_EXCLUDED_KINDS = {
    "SUPERSESSION MARKER": "metadata - carried in each record's `supersession` field, "
                           "never inserted into PREREG.md",
    "SC-12(w)": "descriptive wrapper - the applied limb is the separate "
                "`OPERATIVE v30a TEXT at line 929` block, which is reachable",
}
_D14_EXCLUDED_SECTIONS = {
    "§AB": 'the source declares it "(revised; drafted, not applied)"',
    "§AC": "appended to §AB and claimed by the same hunk; §AB is not applied",
}


def check_block_reachability(root: Path) -> list[Finding]:
    """D14 - no normative block in PART 1 is unreachable by every record."""
    ssf_p = root / "evidence/amendment/SCHEMA_SET_FINAL.md"
    rec_p = root / "evidence/amendment/SCHEMA_RECORDS.json"
    pre_p = root / "PREREG.md"
    if not (ssf_p.exists() and rec_p.exists() and pre_p.exists()):
        return [Finding("block_reachability", "evidence/amendment/SCHEMA_SET_FINAL.md", None,
                        "source, records or PREREG.md missing; D14 cannot run")]
    ssf = ssf_p.read_text(encoding="utf-8").split("\n")
    records = json.loads(rec_p.read_text(encoding="utf-8"))["records"]
    base = {l.strip() for l in pre_p.read_text(encoding="utf-8").split("\n")}
    part1_end = next((i for i, l in enumerate(ssf, 1) if l.startswith("# PART 2 ")), len(ssf))

    reach = set()
    for r in records:
        reach.update(range(r["clause_first_line"], r["clause_last_line"] + 1))

    blocks, cur = [], None
    for i, l in enumerate(ssf, 1):
        if i >= part1_end:
            break
        if _D14_HDR.match(l):
            if cur:
                blocks.append(cur)
            cur = [l, i, i]
        elif cur:
            cur[2] = i
    if cur:
        blocks.append(cur)

    f, examined, excluded, unreachable = [], 0, 0, []
    for hdr, s, e in blocks:
        body, fenced = [], False
        for j in range(s, e + 1):
            raw = ssf[j - 1]
            if raw.lstrip().startswith("```"):
                fenced = not fenced
                continue
            if fenced or raw.lstrip().startswith(">"):
                t = raw.strip()
                if t.startswith(">"):
                    t = t[1:].strip()
                if len(t) > 25 and t not in base:
                    body.append(j)
        if not body:
            continue
        kind = (re.match(r"^\*\*([^,.]+)", hdr) or re.match(r"^#+\s+(\S+)", hdr))
        kind = re.sub(r"\s*—.*", "", kind.group(1)).strip() if kind else hdr[:30]
        if kind in _D14_EXCLUDED_KINDS or kind in _D14_EXCLUDED_SECTIONS:
            excluded += 1
            continue
        examined += 1
        if not any(j in reach for j in body):
            unreachable.append((kind, s, len(body)))

    f.append(Finding("block_reachability", "evidence/amendment/SCHEMA_SET_FINAL.md", None,
                     "population: %d PART 1 blocks carrying operative text; %d examined, "
                     "%d excluded by kind; %d records span %d source lines"
                     % (examined + excluded, examined, excluded, len(records), len(reach)),
                     is_note=True))
    for kind, why in sorted({**_D14_EXCLUDED_KINDS, **_D14_EXCLUDED_SECTIONS}.items()):
        f.append(Finding("block_reachability", "evidence/amendment/SCHEMA_SET_FINAL.md", None,
                         "excluded: %s — %s" % (kind, why), is_note=True))
    for kind, s, n in unreachable:
        f.append(Finding("block_reachability", "evidence/amendment/SCHEMA_SET_FINAL.md", s,
                         "D14: block `%s` at ssf l.%d carries %d line(s) of operative text and is "
                         "reachable by NO record, so it reaches no hunk. Either a record is "
                         "missing, or the block is not applied text and belongs in D14's stated "
                         "exclusions with a reason." % (kind, s, n)))
    return f


# --------------------------------------------------------------------------
# D15 - the approval package's stated figures agree with the artifacts
# --------------------------------------------------------------------------
# R89(iv). The package carries the same quantities in three places: the reader
# section, the §53.2 table and the verification ledger. Two of the three went
# stale at R87 and nothing noticed for three rounds - the ledger said 23/23 and
# 845 while the reader section still said 21/21 and 843. This is D1's class one
# more time: a figure restated away from what produces it drifts, and both copies
# read plausibly.
#
# GROUND TRUTH IS DERIVED, NEVER READ FROM THE PACKAGE: record count from
# SCHEMA_RECORDS.json, hunk and line counts from the generated diff. The package
# is then asserted against that.
_PKG_REL = "evidence/amendment/APPROVAL_PACKAGE.md"


def check_package_figures(root: Path) -> list[Finding]:
    """D15 - every figure the package states matches what produced it."""
    pkg = root / _PKG_REL
    rec = root / "evidence/amendment/SCHEMA_RECORDS.json"
    dif = root / "evidence/amendment/PREREG_v30a_APPROVAL.diff"
    if not (pkg.exists() and rec.exists() and dif.exists()):
        return [Finding("package_figures", _PKG_REL, None,
                        "package, records or diff missing; D15 cannot run")]

    n_rec = len(json.loads(rec.read_text(encoding="utf-8"))["records"])
    dl = dif.read_text(encoding="utf-8").split("\n")
    added = [l for l in dl if l.startswith("+") and not l.startswith("+++")]
    removed = [l for l in dl if l.startswith("-") and not l.startswith("---")]
    hunks = sum(1 for l in dl if l.startswith("@@"))
    framing = sum(1 for l in added if l.startswith("+<!-- v30a "))
    blank = sum(1 for l in added if not l[1:].strip())
    inside = len(added) - framing - blank

    text = pkg.read_text(encoding="utf-8")
    f = [Finding("package_figures", _PKG_REL, None,
                 "derived: %d records, %d hunks, +%d -%d, %d framing, %d blank, %d inside"
                 % (n_rec, hunks, len(added), len(removed), framing, blank, inside),
                 is_note=True)]

    def want(pattern, expected, what, flags=0):
        ms = re.findall(pattern, text, flags)
        if not ms:
            f.append(Finding("package_figures", _PKG_REL, None,
                             "D15: the package states no %s where one is expected - the "
                             "assertion fired on nothing, so the wording moved" % what))
            return
        for got in {int(x) for x in ms}:
            if got != expected:
                f.append(Finding("package_figures", _PKG_REL, None,
                                 "D15: package states %s = %d; the artifacts give %d. The "
                                 "ARTIFACTS are the authority." % (what, got, expected)))

    # Label-specific, NOT a general "N/N" sweep: 10/10 (copied anchors) and 15/15
    # (clause blocks) are DIFFERENT quantities and are correct at those values. A
    # pattern that cannot tell three denominators apart reports two false hits and
    # buries the real one - which is what this check's first version did.
    want(r"records trace to source \| \*\*(\d+) / \d+\*\*", n_rec, "ledger dir-1 denominator")
    want(r"anchors resolve exactly once \| \*\*(\d+) / \d+, ZERO HALTS\*\*", n_rec,
         "ledger anchor-resolution denominator")
    want(r"two unlinked paths \| \*\*(\d+) / \d+\*\*", n_rec, "ledger extraction denominator")
    want(r"\(\*\*(\d+)/\d+\*\* and \*\*15/15\*\*\)", n_rec, "reader-section dir-1 denominator")
    want(r"anchors resolving exactly once \(\*\*(\d+)/\d+, zero halts\*\*\)", n_rec,
         "reader-section anchor denominator")
    want(r"two unlinked paths \(\*\*(\d+)/\d+\*\*\)", n_rec, "reader-section extraction denominator")
    want(r"untraceable inserted lines \*\*0 of (\d+)\*\*", inside, "reader-section traced count")
    want(r"\(\s*(\d+) of \d+ traced\)", inside, "ledger traced count")
    want(r"\| \*\*inside a declared clause range\*\* \| \*\*(\d+)\*\* \|", inside,
         "§53.2 inside-range count")
    want(r"\| inserted lines \| (\d+) \|", len(added), "§53.2 inserted-line count")
    want(r"\| generator framing \(`<!-- v30a ID -->`\) \| (\d+) \|", framing, "§53.2 framing count")
    want(r"\| blank \(generator spacing\) \| (\d+) \|", blank, "§53.2 blank count")
    want(r"\+(\d+) −\d+; \d+ hunks", len(added), "net-line insertion count")
    want(r"\+\d+ −(\d+); \d+ hunks", len(removed), "net-line removal count")
    want(r"\+\d+ −\d+; (\d+) hunks", hunks, "net-line hunk count")
    want(r"(\d+) insertion points across", n_rec, "net-line insertion-point count")
    want(r"(\d+) insertion points across \d+ hunks", n_rec,
         "reader-section insertion-point count")
    want(r"Zero questions across (\d+) insertion points", n_rec,
         "reader-section zero-questions count")
    return f


# --------------------------------------------------------------------------
# D16 - THE THIRD DIRECTION: listed -> IN THE COMMIT
# --------------------------------------------------------------------------
# D9 checks disk -> listed: every file in the evidence tree has a manifest line.
# D10 checks the WORK ROOT -> repo-or-ephemeral. NOTHING checked listed -> will
# actually be in the commit, and that is the direction that matters at tag time:
# a manifest entry for a file the commit does not contain means THE SIGNED TREE
# ATTESTS CONTENT IT DOES NOT CONTAIN. `sha256sum -c` cannot see it - it runs in a
# working directory where the file is present and green.
#
# Found by hand at R98: `../PRACTICES.md` is manifest-attested, untracked, and
# absent from COMMIT_PLAN §4's `git add` set. It would have been hashed into the
# manifest, the manifest committed, and the file left behind.
#
# A path passes if it is EITHER already tracked (so the commit inherits it) OR
# covered by the staging set. Both are ways of being in the commit; neither is a
# substitute for being one of them.
_D16_PLAN_REL = "evidence/ceremony/COMMIT_PLAN.md"


def check_manifest_paths_committed(root: Path) -> list[Finding]:
    """D16 - every manifest-attested path is tracked, or staged by the plan."""
    import subprocess
    man = root / _MANIFEST_REL
    plan = root / _D16_PLAN_REL
    if not (man.exists() and plan.exists()):
        return [Finding("manifest_paths_committed", _MANIFEST_REL, None,
                        "the manifest or the commit plan is missing; D16 cannot run")]

    addset = set()
    for line in plan.read_text(encoding="utf-8").split("\n"):
        if line.startswith("git add "):
            addset.update(line[len("git add "):].split())

    listed = []
    for line in man.read_text(encoding="utf-8", errors="replace").split("\n"):
        if not line or line.startswith("#") or "  " not in line:
            continue
        rel = line.split("  ", 1)[1]
        listed.append(rel[3:] if rel.startswith("../") else "evidence/" + rel)

    try:
        tracked = set(subprocess.run(["git", "ls-files"], cwd=str(root),
                                     capture_output=True, text=True,
                                     check=True).stdout.split("\n"))
    except Exception as e:                                    # pragma: no cover
        return [Finding("manifest_paths_committed", _MANIFEST_REL, None,
                        "git ls-files failed (%s); D16 cannot run" % e)]

    def staged_by_plan(p):
        return any(p == a or p.startswith(a + "/") for a in addset)

    missing = [p for p in listed
               if p not in tracked and not staged_by_plan(p)]

    f = [Finding("manifest_paths_committed", _MANIFEST_REL, None,
                 "%d manifest-attested paths; %d already tracked, %d covered by "
                 "COMMIT_PLAN §4's add-set"
                 % (len(listed), sum(1 for p in listed if p in tracked),
                    sum(1 for p in listed if staged_by_plan(p))), is_note=True)]
    for p in missing:
        f.append(Finding("manifest_paths_committed", _MANIFEST_REL, None,
                         "D16: `%s` is attested by the manifest but is NEITHER tracked NOR in "
                         "COMMIT_PLAN §4's staging set. The signed tree would attest content it "
                         "does not contain. Add it to the staging set, or remove its manifest "
                         "line - not both, and not neither." % p))
    return f


# ---------------------------------------------------------------------------
# D17 - THE FROZEN INSTRUMENT.
#
# Every other check in this file can be silenced by editing this file. This one
# cannot: it runs the checker AS IT WAS AT THE TAG, fetched from git by content,
# against THIS SAME TREE, and compares the two verdict sets.
# ---------------------------------------------------------------------------
_FROZEN_TAG = "prereg-v30a"
_FROZEN_CHECKER_REL = "tools/check_registration.py"
_FROZEN_SELF = "frozen_instrument_delta"
_FROZEN_INNER_ENV = "LEAKAUDIT_FROZEN_DELTA_INNER"
_FROZEN_STAGE = "prereg"

# Verdict differences that are RULED and disclosed. Anything else is a failure.
#   line_citations - R163 §3. The H-34 pin carried a line number while its own
#   recorded reason said the citation is by heading, and no document in the tree
#   has ever cited HISTORY.md by line for H-34. The pin was re-keyed to the
#   anchor, which is what the table's own convention assigns to heading-cited
#   entries. The tag's checker still carries the line number, so it fails here.
_FROZEN_PERMITTED = frozenset({"line_citations"})

_FROZEN_VERDICT = re.compile(r"^\[(PASS|FAIL)\] (\S+)", re.M)


def _frozen_verdicts(text: str) -> dict[str, str]:
    return {m.group(2): m.group(1) for m in _FROZEN_VERDICT.finditer(text)}


def check_frozen_instrument_delta(root: Path) -> list[Finding]:
    """D17 - run the TAG's checker on THIS tree and diff the verdicts.

    HARNESS, and it is tested before the tools are. Two properties matter and
    neither is cosmetic:

    (1) ABSOLUTE ROOT. check_control_characters does `p.relative_to(root)`
        against a path it has already resolved to absolute. A RELATIVE root
        makes that raise, the fallback keys the entry by its manifest-relative
        name, the "evidence/" prefix is lost, a real exemption misses, and a
        control_characters failure appears that belongs to neither instrument.
        That artifact was one step from being reported as a third instrument
        change.
    (2) NOT A WORKTREE. A fresh worktree lacks the untracked and ignored files
        the real tree carries, and D9/D10 then report on the difference between
        two trees rather than between two instruments. Measured: a HEAD
        worktree produced manifest_coverage and round_reconciliation failures
        over four .pytest_cache paths.

    The tag's checker is therefore extracted with `git show` into the same
    relative location (tools/) in a temporary directory, and run against the
    real root, absolute, with PYTHONPATH set so its sibling packages import.

    Compares the prereg stage only; that is the stage this check is registered
    in and the one the registration is gated on.
    """
    import os
    import subprocess
    import tempfile

    rel = _FROZEN_CHECKER_REL
    if os.environ.get(_FROZEN_INNER_ENV) == "1":
        return [Finding(_FROZEN_SELF, rel, None,
                        "D17: nested run - not re-entered", is_note=True)]

    root = Path(root).resolve()

    def git(*args):
        return subprocess.run(["git", *args], cwd=str(root), text=True,
                              capture_output=True, encoding="utf-8",
                              errors="replace")

    peel = git("rev-parse", "%s^{commit}" % _FROZEN_TAG)
    if peel.returncode != 0:
        return [Finding(_FROZEN_SELF, rel, None,
                        "D17: cannot resolve tag %r - the frozen instrument is "
                        "unavailable and this check cannot be believed absent. "
                        "git said: %s" % (_FROZEN_TAG, peel.stderr.strip()))]
    commit = peel.stdout.strip()

    # Fetched as BYTES, not text: the digest below must be the digest of the
    # file the tag attests, and decoding it first would hash something else.
    blob = subprocess.run(
        ["git", "show", "%s:%s" % (commit, _FROZEN_CHECKER_REL)],
        cwd=str(root), capture_output=True)
    if blob.returncode != 0:
        return [Finding(_FROZEN_SELF, rel, None,
                        "D17: %s is absent from %s - cannot compare"
                        % (_FROZEN_CHECKER_REL, commit[:12]))]
    frozen_sha = hashlib.sha256(blob.stdout).hexdigest()

    env = dict(os.environ)
    env["PYTHONPATH"] = str(root)
    env[_FROZEN_INNER_ENV] = "1"

    with tempfile.TemporaryDirectory() as td:
        frozen = Path(td) / "tools" / "check_registration.py"
        frozen.parent.mkdir(parents=True, exist_ok=True)
        frozen.write_bytes(blob.stdout)
        runs = {}
        for label, script in (("frozen", frozen),
                              ("current", root / _FROZEN_CHECKER_REL)):
            runs[label] = subprocess.run(
                [sys.executable, str(script), "--stage", _FROZEN_STAGE,
                 "--root", str(root)],
                cwd=str(root), text=True, capture_output=True,
                encoding="utf-8", errors="replace", env=env)

    old = _frozen_verdicts(runs["frozen"].stdout)
    new = _frozen_verdicts(runs["current"].stdout)
    if not old or not new:
        return [Finding(_FROZEN_SELF, rel, None,
                        "D17: a run produced no verdicts (frozen %d, current "
                        "%d) - the harness is broken and its silence proves "
                        "nothing" % (len(old), len(new)))]

    findings = [Finding(
        _FROZEN_SELF, rel, None,
        "D17: frozen instrument sha256 %s… from %s: exit %d, %d checks; "
        "current: exit %d, %d checks"
        % (frozen_sha[:16], commit[:12], runs["frozen"].returncode,
           len(old), runs["current"].returncode, len(new)), is_note=True)]

    diff = sorted(n for n in set(old) | set(new)
                  if n != _FROZEN_SELF and old.get(n) != new.get(n))
    for name in diff:
        was, now = old.get(name, "absent"), new.get(name, "absent")
        if name in _FROZEN_PERMITTED:
            findings.append(Finding(
                _FROZEN_SELF, rel, None,
                "D17: %s %s -> %s - RULED difference, disclosed" % (name, was, now),
                is_note=True))
            continue
        extra = ""
        if name == "control_characters":
            extra = (" This one is the known harness artifact: if it appears "
                     "here the root was not absolute. Check the harness before "
                     "reading it as an instrument difference.")
        findings.append(Finding(
            _FROZEN_SELF, rel, None,
            "D17: %s reads %s on the frozen instrument and %s on the current "
            "one, and is not a ruled difference. The instrument that certifies "
            "the registration disagrees with the one the tag attests.%s"
            % (name, was, now, extra)))
    if not diff:
        findings.append(Finding(
            _FROZEN_SELF, rel, None,
            "D17: the two instruments agree on every check", is_note=True))
    return findings


CHECKS: tuple[tuple[str, str, object], ...] = (
    # (stage, name, callable)
    ("prereg", "frozen_instrument_delta", check_frozen_instrument_delta),
    ("prereg", "structure", check_structure),
    ("prereg", "config_schema", check_config_schema),
    ("prereg", "lock_table", check_lock_table),
    ("prereg", "banned_vocabulary", check_banned_vocabulary),
    ("prereg", "deletion_certificate", check_deletion_certificate),
    ("prereg", "single_source", check_single_source),
    ("prereg", "hash_set_single_source", check_hash_set_single_source),
    ("prereg", "declaration_values", check_declaration_values),
    ("prereg", "line_citations", check_line_citations),
    ("prereg", "manifest_coverage", check_manifest_covers_tree),
    ("prereg", "round_reconciliation", check_round_reconciliation),
    ("prereg", "phase_arithmetic", check_phase_arithmetic),
    ("prereg", "requirement_ids", check_requirement_ids),
    ("prereg", "legality_table", check_legality_table),
    ("prereg", "parking_lot", check_parking_lot),
    ("prereg", "reducer_functions", check_reducer_functions),
    ("prereg", "unit_grammar", check_unit_grammar),
    ("prereg", "suppression_anchor", check_suppression_anchor),
    ("prereg", "control_characters", check_control_characters),
    ("prereg", "block_manifest_counts", check_block_manifest_counts),
    ("prereg", "block_reachability", check_block_reachability),
    ("prereg", "package_figures", check_package_figures),
    ("prereg", "manifest_paths_committed", check_manifest_paths_committed),
    ("implementation", "ties_comparator_vs_shipped_mask", check_ties_comparator_vs_mask),
    ("implementation", "l31b_inequalities_vs_shipped_rule", check_l31b_inequalities),
    ("implementation", "shipping_defaults_vs_validated_runtime", check_shipping_defaults),
    ("implementation", "deleted_config_fields_rejected", check_deleted_config_rejected),
    ("implementation", "cost_script_total", check_cost_script),
    ("release", "readme_numbers_regenerated", check_readme_numbers),
    ("release", "package_defaults", check_package_defaults),
    ("release", "installability", check_installability),
)


def run_stage(stage: str, root: Path) -> int:
    own = [(name, fn) for st, name, fn in CHECKS if st == stage]
    deferred = [(st, name) for st, name, _fn in CHECKS if st != stage]
    print(f"== check_registration --stage {stage} (root: {root}) ==")
    total_findings: list[Finding] = []
    for name, fn in own:
        findings = fn(root)
        failures = [f for f in findings if not f.is_note]
        status = "FAIL" if failures else "PASS"
        print(f"[{status}] {name}")
        for finding in findings:  # notes print too — exemptions must be visible
            print(finding.render())
        total_findings.extend(failures)
    print("\nDeferred at this stage (owned elsewhere; an omitted branch is a "
          "failure, not a pass):")
    for st, name in deferred:
        print(f"    {name}  -> owned by --stage {st}")
    failed = len({f.check for f in total_findings})
    if total_findings:
        print(f"\nRESULT: FAIL — {failed} check(s) failed, "
              f"{len(total_findings)} finding(s)")
        return 1
    print("\nRESULT: PASS")
    return 0


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", choices=("prereg", "implementation", "release"),
                        required=True)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    return run_stage(args.stage, args.root)


if __name__ == "__main__":
    raise SystemExit(main())
