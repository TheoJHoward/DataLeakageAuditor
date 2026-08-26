#!/usr/bin/env python3
"""Re-point D4: check DERIVATION, not a restated EXPECT list.

A1.4's reshape removed the literal "EXPECT, exactly" list, because that list was
itself a restatement of the set - the exact thing this detector exists to prevent.
D4 now asserts the pre-commit block READS $FILES from its authority and that every
member is named somewhere in the plan.
"""
import pathlib, re

P = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01/"
                 "tools/check_registration.py")
lines = P.read_text(encoding="utf-8").split("\n")

i0 = next(i for i, l in enumerate(lines) if 'expect = re.search(r"# EXPECT, exactly' in l)
i1 = next(i for i in range(i0, len(lines))
          if '"D4: V1\'s EXPECT list names all of $FILES",' in l)
# the block ends two lines after that (the is_note=True closer)
i1 = next(i for i in range(i1, len(lines)) if "is_note=True))" in lines[i]) + 1
assert i1 > i0, "D4 bounds"

NEW = '''        # D4: the pre-commit verification must READ the set from its authority
        # rather than restate it, and must name every member for the human reader.
        # (Until R67/A1 this checked a literal "EXPECT, exactly" list. That list
        # WAS a restatement - the thing this check exists to prevent - so D4 now
        # tests derivation, not the presence of a second copy.)
        derives = ("grep -m1 '^FILES=' evidence/ceremony/CEREMONY_COMMANDS.md"
                   in text)
        if not derives:
            findings.append(Finding(
                "hash_set_single_source", plan_rel, None,
                "D4: the pre-commit checks do not READ $FILES from %s \\u00a73.2. A "
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
                "members named" % len(files), is_note=True))'''

lines[i0:i1] = NEW.split("\n")
P.write_text("\n".join(lines), encoding="utf-8")
import ast
ast.parse(P.read_text(encoding="utf-8"))
print("D4 re-pointed at derivation; syntax OK")
