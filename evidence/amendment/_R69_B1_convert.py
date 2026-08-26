#!/usr/bin/env python3
"""B1.2 — convert all 13 line-pinned exemptions in D1/D2 to VALUE-specific.

An exemption must whitelist "this known-historical value at this site", never
"anything that appears at this site". D7's N1/N2 silence was the mechanism flaw;
these tables share it.
"""
import pathlib, re

TOOL = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01/"
                    "tools/check_registration.py")
src = TOOL.read_text(encoding="utf-8")

# ---- the allowed sets, measured by _R69_B1_audit.py ----------------------
COUNTS = {
    ("AVAILABILITY_DECLARATION.md", 3591): "{5}",
    ("AVAILABILITY_DECLARATION.md", 3875): "{5}",
    ("AVAILABILITY_DECLARATION.md", 3897): "{5}",
    ("evidence/ceremony/CEREMONY_COMMANDS.md", 239): "{5}",
    ("AVAILABILITY_DECLARATION.md", 3614): "{2}",
    ("AVAILABILITY_DECLARATION.md", 3689): "{5}",
    ("HISTORY.md", 225): "{2, 4}",
    ("PREREG.md", 97): "{2}",
}
ENUMS = {
    ("AVAILABILITY_DECLARATION.md", 3611):
        '("PREREG.md", "DESIGN.md", "HISTORY.md", "tools/check_registration.py",\n'
        '         "protocol/runtime_reference.py")',
    ("PREREG.md", 1048):
        '("PREREG.md", "DESIGN.md", "HISTORY.md", "tools/check_registration.py",\n'
        '         "protocol/runtime_reference.py")',
    ("AVAILABILITY_DECLARATION.md", 3666):
        '("PREREG.md", "DESIGN.md", "HISTORY.md")',
    ("evidence/ceremony/COMMIT_PLAN.md", 321):
        '("PREREG.md", "DESIGN.md", "HISTORY.md", "tools/check_registration.py",\n'
        '         "AVAILABILITY_DECLARATION.md")',
    ("PREREG.md", 1050):
        '("PREREG.md", "DESIGN.md", "HISTORY.md")',
}

n = 0
for (path, line), allowed in list(COUNTS.items()) + list(ENUMS.items()):
    anchor = '("%s", %d): (\n' % (path, line)
    i = src.find(anchor)
    assert i != -1, "anchor not found: %s:%d" % (path, line)
    # the pin string ends at the first line ending in '",'
    j = src.index('",\n', i + len(anchor)) + 3
    src = src[:j] + "        frozenset(%s),\n" % allowed + src[j:]
    n += 1

# ---- D1's exempt branch: reject values the exemption does not list -------
OLD1 = '''            pin, reason = entry
            if pin not in raw:
                findings.append(Finding(
                    "hash_set_single_source", rel, idx,
                    "D5/D6: exemption has DRIFTED - the pinned text %r is no longer "
                    "on this line. Re-anchor the exemption; do not widen it." % pin))
            else:
                seen_exempt.add(key)
                findings.append(Finding("hash_set_single_source", rel, idx,
                                        "exempt - %s" % reason, is_note=True))'''
NEW1 = '''            pin, allowed, reason = entry
            if pin not in raw:
                findings.append(Finding(
                    "hash_set_single_source", rel, idx,
                    "D5/D6: exemption has DRIFTED - the pinned text %r is no longer "
                    "on this line. Re-anchor the exemption; do not widen it." % pin))
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
                                        "exempt - %s" % reason, is_note=True))'''
assert src.count(OLD1) == 1, "D1 exempt branch match %d" % src.count(OLD1)
src = src.replace(OLD1, NEW1, 1)

# ---- D2's exempt branch: the enumeration must be the allowed one ---------
OLD2 = '''            pin, reason = entry
            if pin not in raw:
                findings.append(Finding(
                    "hash_set_single_source", rel, idx,
                    "D6: enumeration exemption has DRIFTED - pinned text %r is no "
                    "longer on this line." % pin))
            else:
                seen_exempt.add(key)
                findings.append(Finding("hash_set_single_source", rel, idx,
                                        "exempt - %s" % reason, is_note=True))'''
NEW2 = '''            pin, allowed, reason = entry
            if pin not in raw:
                findings.append(Finding(
                    "hash_set_single_source", rel, idx,
                    "D6: enumeration exemption has DRIFTED - pinned text %r is no "
                    "longer on this line." % pin))
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
                                        "exempt - %s" % reason, is_note=True))'''
assert src.count(OLD2) == 1, "D2 exempt branch match %d" % src.count(OLD2)
src = src.replace(OLD2, NEW2, 1)

# ---- the stale-exemption sweep reads entry[0]; keep it index-safe --------
src = src.replace(
    "            entry = _HASH_SET_EXEMPT.get(key) or _HASH_SET_ENUM_EXEMPT.get(key)\n"
    "            pin = entry[0]",
    "            entry = _HASH_SET_EXEMPT.get(key) or _HASH_SET_ENUM_EXEMPT.get(key)\n"
    "            pin = entry[0]", 1)

TOOL.write_text(src, encoding="utf-8")
import ast
ast.parse(TOOL.read_text(encoding="utf-8"))
print("converted %d exemptions to VALUE-scoped; D1 and D2 branches updated; syntax OK" % n)
