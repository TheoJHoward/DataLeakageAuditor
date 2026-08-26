#!/usr/bin/env python3
"""Point the D1/D2 exemption lookups at anchors instead of line numbers.

The tables are already anchor-keyed. This changes the three places that consulted
them by line: the D1 site, the D2 enumeration site, and the stale sweep.

THE UNIQUENESS GUARD IS THE NEW PART. A line key could only ever select one line.
An anchor could select several, and an anchor matching two lines would exempt both
without saying so -- the exemption would widen silently, which is the failure the
value-scoping already exists to prevent. So uniqueness is asserted per anchor per
file, and a non-unique anchor is a finding rather than a tie-break.

CRLF preserved: this file is stored uniformly CRLF.

Written with the Write tool per D2.1.
"""
import ast
import pathlib
import subprocess
import sys

REPO = pathlib.Path(r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01")
SRC = REPO / "tools/check_registration.py"
body = SRC.read_text(encoding="utf-8")


def sub(old, new, why):
    global body
    if body.count(old) != 1:
        sys.exit("HALT: %s -- expected exactly one occurrence, found %d"
                 % (why, body.count(old)))
    body = body.replace(old, new, 1)


HELPER = '''
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


'''

# ---- header comment, then the helper, before the D1 table ------------------
sub("# (path, line) -> (pin, reason). D5 = v30 site. D6 = PREREG registered text.",
    "# (path, ANCHOR TEXT) -> (allowed, reason). D5 = v30 site. D6 = PREREG\n"
    "# registered text. KEYED BY ANCHOR, NEVER BY LINE - see _exempt_by_anchor.",
    "D1 table header")
sub("# (path, line) -> (pin, reason) for D2 path enumerations that are not the set.",
    "# (path, ANCHOR TEXT) -> (enumeration, reason) for D2 path enumerations that\n"
    "# are not the set. Keyed by anchor, never by line.",
    "D2 table header")
sub("_HASH_SET_EXEMPT = {", HELPER.lstrip("\n") + "_HASH_SET_EXEMPT = {",
    "helper placement")

# ---- D1 lookup -------------------------------------------------------------
sub("""            key = (rel, idx)
            entry = _HASH_SET_EXEMPT.get(key)
            if entry is None:""",
    """            key, allowed, reason, problem = _exempt_by_anchor(
                _HASH_SET_EXEMPT, rel, raw, lines)
            if key is not None and problem:
                findings.append(Finding(
                    "hash_set_single_source", rel, idx,
                    "D5/D6: this site's exemption is UNUSABLE - %s" % problem))
                continue
            entry = None if key is None else True
            if entry is None:""",
    "D1 lookup")

sub("""            pin, allowed, reason = entry
            if pin not in raw:
                findings.append(Finding(
                    "hash_set_single_source", rel, idx,
                    "D5/D6: exemption has DRIFTED - the pinned text %r is no longer "
                    "on this line. Re-anchor the exemption; do not widen it." % pin))
                continue
            seen_exempt.add(key)""",
    """            seen_exempt.add(key)""",
    "D1 drift branch (an anchor cannot drift off its own line)")

# ---- D2 enumeration lookup -------------------------------------------------
sub("""            key = (rel, idx)
            entry = _HASH_SET_ENUM_EXEMPT.get(key)
            if entry is None:""",
    """            key, allowed, reason, problem = _exempt_by_anchor(
                _HASH_SET_ENUM_EXEMPT, rel, raw, lines)
            if key is not None and problem:
                findings.append(Finding(
                    "hash_set_single_source", rel, idx,
                    "D6: this site's enumeration exemption is UNUSABLE - %s" % problem))
                continue
            entry = None if key is None else True
            if entry is None:""",
    "D2 enum lookup")

sub("""            pin, allowed, reason = entry
            if pin not in raw:
                findings.append(Finding(
                    "hash_set_single_source", rel, idx,
                    "D6: enumeration exemption has DRIFTED - pinned text %r is no "
                    "longer on this line." % pin))
                continue
            seen_exempt.add(key)""",
    """            seen_exempt.add(key)""",
    "D2 enum drift branch")

# ---- the stale sweep -------------------------------------------------------
sub("""    for key in list(_HASH_SET_EXEMPT) + list(_HASH_SET_ENUM_EXEMPT):
        if key not in seen_exempt:
            entry = _HASH_SET_EXEMPT.get(key) or _HASH_SET_ENUM_EXEMPT.get(key)
            pin = entry[0]
            src = root / key[0]
            where = ""
            if src.exists():
                hits = [n for n, ln in enumerate(
                    src.read_text(encoding="utf-8", errors="replace")
                    .split(chr(10)), 1)
                    if pin in ln]
                if len(hits) == 1:
                    where = (" The pinned text is now at line %d - re-anchor it there."
                             % hits[0])
                elif hits:
                    where = " The pinned text now appears on lines %r." % (hits,)
                else:
                    where = " The pinned text is gone from the file entirely."
            findings.append(Finding(
                "hash_set_single_source", key[0], key[1],
                "D5/D6: this exemption fired on nothing - a stale exemption is a hole, "
                "not a no-op.%s" % where))""",
    """    for key in list(_HASH_SET_EXEMPT) + list(_HASH_SET_ENUM_EXEMPT):
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
                "not a no-op.%s" % where))""",
    "stale sweep")

sub("    seen_exempt: set[tuple[str, int]] = set()",
    "    seen_exempt: set[tuple[str, str]] = set()",
    "seen_exempt type")

head = subprocess.run(["git", "show", "HEAD:tools/check_registration.py"],
                      cwd=str(REPO), capture_output=True).stdout
crlf, lf = head.count(b"\r\n"), head.count(b"\n")
if crlf and crlf != lf:
    sys.exit("HALT: checker is MIXED at HEAD")
out = body.encode("utf-8")
if crlf:
    out = out.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
SRC.write_bytes(out)
ast.parse(SRC.read_text(encoding="utf-8"))
print("lookups converted to anchors; %d CRLF / %d LF; source parses"
      % (out.count(b"\r\n"), out.count(b"\n")))
