#!/usr/bin/env python3
"""DELTA R67 / §16 - install the hash-set single-source detector."""
import pathlib

TOOL = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01/"
                    "tools/check_registration.py")
s = TOOL.read_text(encoding="utf-8")

DETECTOR = '''
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

_HS_WORD = {"both": 2, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
            "seven": 7, "eight": 8, "fifth": 5, "sixth": 6, "seventh": 7}
_HS_NOUN = r"(?:hashes|hash\\s+lines|hash|SHA-?256\\s+lines|SHA-?256|line\\s+block|lines)"
_HS_ATTACH = re.compile(
    r"\\b(both|two|three|four|five|six|seven|eight|fifth|sixth|seventh)\\b"
    r"(?:[-\\s]+(?:\\w+\\s+){0,2})?" + _HS_NOUN, re.I)
_HS_CTX = re.compile(
    r"(tag[- ]message|\\$FILES|FILES=|files whose hashes"
    r"|hash(es)?[^.]{0,18}(block|set)\\b"
    r"|(each|all|one|member) of the (six|seven|five)\\b"
    r"|the (fifth|sixth|seventh) hash)", re.I)

# (path, line) -> (pin, reason). D5 = v30 site. D6 = PREREG registered text.
_HASH_SET_EXEMPT = {
    ("AVAILABILITY_DECLARATION.md", 3591): (
        "The `prereg-v30` tag message carries",
        "D5 - states the EXECUTED v30 count, which is five. Correct as written."),
    ("AVAILABILITY_DECLARATION.md", 3811): (
        "prereg-v30 tag message (five SHA-256 lines",
        "D5 - the parenthetical describes the v30 message, not v30a."),
    ("AVAILABILITY_DECLARATION.md", 3833): (
        "R7. hash-count:",
        "D5 - working resolution R7. Its 'ALL FIVE' takes the v30 five as its "
        "referent ('matching the prereg-v30 tag as executed') and is TRUE of a "
        "six-file set containing those five. The totality reading came from R7's "
        "topic LABEL, not its predicate; the R67/§14.2 survey established every "
        "label in that block is a topic tag. R7 stands unamended. "
        "See AVAILABILITY_DECLARATION.md §D.3 entry (iii)."),
    ("evidence/ceremony/CEREMONY_COMMANDS.md", 238): (
        "a tag message with five lines is not a v30a tag message",
        "D5 - a NEGATED assertion: it says five is wrong for v30a."),
    ("PREREG.md", 97): (
        "both file hashes in the tag message",
        "D6 - REGISTERED TEXT, not editable. 'both' is a closed quantifier over "
        "exactly two things and lost its referent when the set grew; the two "
        "files' hashes ARE in the tag, so it is satisfied, but it supplies no "
        "rule for files added since. See AVAILABILITY_DECLARATION.md §D.3 "
        "entry (ii)."),
}

# (path, line) -> (pin, reason) for D2 path enumerations that are not the set.
_HASH_SET_ENUM_EXEMPT = {
    ("PREREG.md", 1050): (
        "SHA-256 of `PREREG.md`, `DESIGN.md`, and `HISTORY.md` as committed",
        "D6 - REGISTERED TEXT, not editable. §11 item 3 is a FLOOR: no 'only', "
        "no 'exactly', so a superset satisfies it and over-delivery is strictly "
        "stronger. The executed v30 tag already carried five. See "
        "AVAILABILITY_DECLARATION.md §D.3 entry (i)."),
}


def _hash_set_strip(line: str) -> str:
    """Remove tokens that look like counts but are addresses."""
    out = re.sub(r"[*_]+", " ", line)
    for pat in (r"\\u00a7\\s*[A-Z]?\\.?\\d+(\\.\\d+)*[a-z]?", r"\\b[A-Z]\\.\\d+",
                r"\\bl\\.\\s*\\d+", r"\\blines?\\s+[\\d,\\u2013-]+", r"\\bv\\d+[a-z]?\\b",
                r"\\bC\\d[a-z]?\\b", r"\\b[A-Z]-?\\d+\\b", r"`[^`]*`",
                r"^\\s*\\d+\\.\\s", r"\\b[0-9a-f]{8,}\\b"):
        out = re.sub(pat, " ", out)
    return re.sub(r"\\s+", " ", out)


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
                            'no FILES="..." declaration found in \\u00a73.2; the set has no authority')]
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

    seen_exempt: set[tuple[str, int]] = set()

    for rel in _HASH_SET_CORPUS:
        path = root / rel
        if not path.exists():
            continue
        lines = path.read_text(encoding="utf-8", errors="replace").split("\\n")

        # ---- D1: count literals -------------------------------------------
        for idx, raw in enumerate(lines, 1):
            if not _HS_CTX.search(raw):
                continue
            saw = {_HS_WORD[m.group(1).lower()]
                   for m in _HS_ATTACH.finditer(_hash_set_strip(raw))}
            bad = sorted(v for v in saw if v != n)
            if not bad:
                continue
            key = (rel, idx)
            entry = _HASH_SET_EXEMPT.get(key)
            if entry is None:
                findings.append(Finding(
                    "hash_set_single_source", rel, idx,
                    "D1: states %s for the v30a hash set; the authority "
                    "(%s \\u00a73.2) says %d. Correct it against $FILES, or add a "
                    "path+line exemption with its reason."
                    % ("/".join(str(b) for b in bad), _CEREMONY_REL, n)))
                continue
            pin, reason = entry
            if pin not in raw:
                findings.append(Finding(
                    "hash_set_single_source", rel, idx,
                    "D5/D6: exemption has DRIFTED - the pinned text %r is no longer "
                    "on this line. Re-anchor the exemption; do not widen it." % pin))
            else:
                seen_exempt.add(key)
                findings.append(Finding("hash_set_single_source", rel, idx,
                                        "exempt - %s" % reason, is_note=True))

        # ---- D2: path enumerations purporting to BE the set ---------------
        for idx, raw in enumerate(lines, 1):
            hits = [b for b in basenames if b in raw]
            if len(hits) < 3:
                continue
            window = " ".join(lines[max(0, idx - 1): idx + 3])
            found = [b for b in files if b in window]
            if found == files:
                findings.append(Finding(
                    "hash_set_single_source", rel, idx,
                    "D2: enumeration matches $FILES in order", is_note=True))
                continue
            key = (rel, idx)
            entry = _HASH_SET_ENUM_EXEMPT.get(key)
            if entry is None:
                findings.append(Finding(
                    "hash_set_single_source", rel, idx,
                    "D2: enumerates %d of the %d hashed paths but is not the set "
                    "in order (%s). Either make it the set or exempt it by "
                    "path+line with its reason."
                    % (len(found), n, ", ".join(found) or "none in order")))
                continue
            pin, reason = entry
            if pin not in raw:
                findings.append(Finding(
                    "hash_set_single_source", rel, idx,
                    "D6: enumeration exemption has DRIFTED - pinned text %r is no "
                    "longer on this line." % pin))
            else:
                seen_exempt.add(key)
                findings.append(Finding("hash_set_single_source", rel, idx,
                                        "exempt - %s" % reason, is_note=True))

    # ---- D2a: the tag-message body is ORDER-SENSITIVE ---------------------
    cer = root / _CEREMONY_REL
    if cer.exists():
        body = re.findall(r"^<64 hex>  (\\S+)$",
                          cer.read_text(encoding="utf-8"), re.M)
        if not body:
            findings.append(Finding(
                "hash_set_single_source", _CEREMONY_REL, None,
                "D2: the \\u00a73.5 tag-message body carries no '<64 hex>  <path>' block; "
                "the message that gets signed is not specified anywhere"))
        elif body != files:
            findings.append(Finding(
                "hash_set_single_source", _CEREMONY_REL, None,
                "D2: the \\u00a73.5 tag-message body is %s but $FILES is %s - ORDER "
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
                "D3: \\u00a74's git add set omits %s - `git show :<path>` on a tracked "
                "file that was never staged silently returns its HEAD content, so "
                "the tag would be signed over unapproved bytes" % ", ".join(missing)))
        else:
            findings.append(Finding("hash_set_single_source", plan_rel, None,
                                    "D3: \\u00a74's git add set covers $FILES", is_note=True))

        expect = re.search(r"# EXPECT, exactly(.*?)\\n\\n", text, re.S)
        block = expect.group(1) if expect else ""
        absent = [f for f in files if f not in block]
        if absent:
            findings.append(Finding(
                "hash_set_single_source", plan_rel, None,
                "D4: V1's EXPECT list does not name %s. Every member of the set "
                "belongs in that list, in whichever half - a member absent from "
                "both halves is a member nobody verifies" % ", ".join(absent)))
        else:
            findings.append(Finding("hash_set_single_source", plan_rel, None,
                                    "D4: V1's EXPECT list names all of $FILES",
                                    is_note=True))

    # ---- exemptions that no longer match anything -------------------------
    for key in list(_HASH_SET_EXEMPT) + list(_HASH_SET_ENUM_EXEMPT):
        if key not in seen_exempt:
            findings.append(Finding(
                "hash_set_single_source", key[0], key[1],
                "D5/D6: this exemption fired on nothing. Either the line moved or "
                "the text changed - a stale exemption is a hole, not a no-op."))
    return findings

'''

ANCHOR = "def check_phase_arithmetic(root: Path) -> list[Finding]:"
n = s.count(ANCHOR)
assert n == 1, "anchor match %d" % n
s = s.replace(ANCHOR, DETECTOR.lstrip("\n") + "\n" + ANCHOR, 1)

REG = '    ("prereg", "single_source", check_single_source),\n'
n = s.count(REG)
assert n == 1, "registry match %d" % n
s = s.replace(REG, REG + '    ("prereg", "hash_set_single_source", check_hash_set_single_source),\n', 1)

TOOL.write_text(s, encoding="utf-8")
print("check_registration.py: check_hash_set_single_source installed and registered (prereg stage)")
