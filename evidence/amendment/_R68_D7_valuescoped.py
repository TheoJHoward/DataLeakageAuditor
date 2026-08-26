#!/usr/bin/env python3
"""D7 fix: exemptions must be VALUE-scoped, not line-scoped.

Caught by D7's own negative test (§21.8 / §16.3): injecting a fresh wrong hash
onto an EXEMPTED line was silent, because the exemption covered the whole line.
An exemption that says "this line is allowed to be wrong" licenses every future
wrongness on it. Each exemption now lists exactly the historical values it
permits; anything else on that line still fails.
"""
import pathlib, re

TOOL = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01/"
                    "tools/check_registration.py")
src = TOOL.read_text(encoding="utf-8")
lines = src.split("\n")

# ---- replace the exemption table -----------------------------------------
i0 = next(i for i, l in enumerate(lines) if l.startswith("_D7_EXEMPT = {"))
i1 = next(i for i in range(i0, len(lines)) if lines[i] == "}")
NEW_TABLE = '''# (path, line) -> (pin, allowed_values, reason).
# ALLOWED_VALUES is the point: an exemption names the specific historical values
# the line may carry. A NEW wrong value on an exempted line still fails. Without
# that, an exemption licenses every future error on its line - which D7's own
# negative test N1/N2 demonstrated before this was fixed.
_D7_EXEMPT = {
    ("evidence/author_review/READ_THROUGH_PACKAGE.md", 1): (
        "Author read-through package",
        frozenset({"f0829bd3a0f11b05170a5e2686b953c5def39104af0bbfa2904afb3da2f53310",
                   "277411", "3684"}),
        "the frozen author-read baseline; recording the bytes as the author read "
        "them is its whole purpose"),
    ("evidence/ceremony/CEREMONY_COMMANDS.md", 26): (
        "do not read the size or hash from here",
        frozenset({"f0829bd3"}),
        "the stale value appears only inside the note recording that it WAS stale"),
    ("evidence/ceremony/COMMIT_PLAN.md", 80): (
        "derived not transcribed",
        frozenset({"f0829bd3"}),
        "same - the superseded value is quoted in the note recording the correction"),
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
}'''
lines[i0:i1 + 1] = NEW_TABLE.split("\n")
src = "\n".join(lines)

# ---- replace the per-line comparison so it yields raw tokens --------------
OLD = '''            bad = []
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
                continue'''
NEW = '''            bad = []            # (raw_token, human_description)
            for hx in _D7_HEX.findall(line):
                if hx.isdigit() or len(hx) < 8:
                    continue
                if not digest.startswith(hx):
                    bad.append((hx, "sha256 %s\\u2026" % hx[:12]))
            for val, unit in _D7_SIZE.findall(line):
                num = int(val.replace(",", ""))
                if unit == "bytes" and num != nbytes:
                    bad.append((val.replace(",", ""), "%s bytes" % val))
                if unit == "lines" and num != nlines:
                    bad.append((val.replace(",", ""), "%s lines" % val))
            if not bad:
                continue'''
assert src.count(OLD) == 1, "comparison block match %d" % src.count(OLD)
src = src.replace(OLD, NEW, 1)

OLD2 = '''            key = (rel, idx)
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
                                        "exempt - %s" % reason, is_note=True))'''
NEW2 = '''            key = (rel, idx)
            entry = _D7_EXEMPT.get(key)
            if entry is None:
                findings.append(Finding(
                    "declaration_values", rel, idx,
                    "D7: states %s for %s; the file is sha256 %s\\u2026 / %d bytes / %d lines. "
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
                                        "exempt - %s" % reason, is_note=True))'''
assert src.count(OLD2) == 1, "exempt block match %d" % src.count(OLD2)
src = src.replace(OLD2, NEW2, 1)

TOOL.write_text(src, encoding="utf-8")
import ast
ast.parse(TOOL.read_text(encoding="utf-8"))
print("D7 exemptions are now VALUE-scoped; syntax OK")
