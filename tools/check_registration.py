"""Registration checker (PREREG §6.8), staged.

Stages: prereg | implementation | release. Every stage prints the checks it
defers and the stage that owns them -- an omitted branch is a failure, not a
pass. The tag gate is `--stage prereg` exit 0.

No exemption may be added to make current files pass: an exemption requires an
affirmative reason grounded in PREREG.md. The exemptions below are the ones
PREREG §6.8 itself declares (the banned-list block, PREREG §0.4, the
parenthetical ledger notes / HISTORY.md markers, PARKING_LOT.md), and
HISTORY.md is out of scan scope because it declares itself non-normative.
"""

from __future__ import annotations

import argparse
import re
import sys
import tomllib
from dataclasses import dataclass
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


def normative_lines(path: Path, text: str) -> list[tuple[int, str]]:
    """Lines of a normative file with PREREG §6.8's declared historical
    regions removed — by explicit range, never by content matching. For
    PREREG.md: the single closed banned-list block, §0.4's line range, and
    parenthetical ledger notes referencing HISTORY.md or a superseded
    version. DESIGN.md has no declared historical regions left (its numbered
    lessons moved to HISTORY.md), so every DESIGN line is scanned."""
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


# Curated detectors for the single-source rule (PREREG §0.2.1): measurement
# formulas, state enumerations, and denominator definitions may not appear in
# DESIGN.md. Rules name the owning PREREG section.
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
)


def check_single_source(root: Path) -> list[Finding]:
    path = root / "DESIGN.md"
    if not path.exists():
        return [Finding("single_source", "DESIGN.md", None, "missing")]
    f: list[Finding] = []
    for lineno, line in normative_lines(path, path.read_text(encoding="utf-8")):
        for pattern, message in _SINGLE_SOURCE_RULES:
            if re.search(pattern, line):
                f.append(Finding("single_source", "DESIGN.md", lineno,
                                 f"{message}: {line.strip()[:110]!r}"))
    # State-set enumerations: three or more schedule/coverage state values on
    # one line is an enumeration, not a mention.
    state_tokens = ("not_applicable", "unsupported", "completed", "incomplete",
                    "short_circuited")
    for lineno, line in normative_lines(path, path.read_text(encoding="utf-8")):
        hits = [t for t in state_tokens if t in line]
        if len(hits) >= 3:
            f.append(Finding("single_source", "DESIGN.md", lineno,
                             f"state enumeration ({', '.join(hits)}); owned by PREREG §6.6"))
    return f


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


def check_installability(root: Path) -> list[Finding]:
    return _artifact_absent("installability", "the installable package", "PREREG §10.2 c5")


# ---------------------------------------------------------------------------
# Stage wiring
# ---------------------------------------------------------------------------

CHECKS: tuple[tuple[str, str, object], ...] = (
    # (stage, name, callable)
    ("prereg", "structure", check_structure),
    ("prereg", "config_schema", check_config_schema),
    ("prereg", "lock_table", check_lock_table),
    ("prereg", "banned_vocabulary", check_banned_vocabulary),
    ("prereg", "deletion_certificate", check_deletion_certificate),
    ("prereg", "single_source", check_single_source),
    ("prereg", "phase_arithmetic", check_phase_arithmetic),
    ("prereg", "requirement_ids", check_requirement_ids),
    ("prereg", "legality_table", check_legality_table),
    ("prereg", "parking_lot", check_parking_lot),
    ("prereg", "reducer_functions", check_reducer_functions),
    ("prereg", "unit_grammar", check_unit_grammar),
    ("prereg", "suppression_anchor", check_suppression_anchor),
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
