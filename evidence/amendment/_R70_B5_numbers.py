#!/usr/bin/env python3
"""B5 — give D1 a real number parser, then property-test it.

Found by B5's premise: D1 detected NO numerals at all ("6 hashes", "42 hashes",
"1,000 hashes" all invisible), and mis-parsed compounds ("twenty-five hashes"
resolved to 20 - a WRONG VALUE, which is worse than a miss). Its batteries passed
because every mutation was authored from inside its vocabulary.
"""
import pathlib

TOOL = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01/"
                    "tools/check_registration.py")
src = TOOL.read_text(encoding="utf-8")

lines = src.split("\n")
# replace ONLY the comment block + _HS_WORD dict; _HS_NOUN and _HS_ATTACH follow it
# and are edited separately below.
i0 = next(i for i, l in enumerate(lines) if l.startswith("# Vocabulary caps the check's reach"))
i1 = next(i for i in range(i0, len(lines)) if lines[i].startswith("_HS_NOUN = "))

NEW = '''# NUMBER HANDLING (rebuilt R70/B5).
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
_HS_NUMPHRASE = (r"(?:\\d{1,4}(?:,\\d{3})*|(?:" + _HS_NUMTOK + r")"
                 r"(?:[-\\s]+(?:" + _HS_NUMTOK + r"))*)")


def _hs_number(text: str) -> int | None:
    """Parse a matched number phrase. None = could not parse (reported, not skipped)."""
    t = text.strip().lower().replace(",", "")
    if t.isdigit():
        return int(t)
    total, current, seen = 0, 0, False
    for tok in re.split(r"[-\\s]+", t):
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


'''

lines[i0:i1] = NEW.split("\n")
src = "\n".join(lines)

# the matcher now uses the phrase, and captures it for parsing
OLD = '''_HS_ATTACH = re.compile(
    r"(?<!-)\\b(both|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
    r"thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|"
    r"fifth|sixth|seventh|eighth|ninth|tenth)\\b"
    r"(?:[-\\s]+(?:\\w+\\s+){0,2})?" + _HS_NOUN, re.I)'''
NEW_ATT = '''_HS_ATTACH = re.compile(r"(?<![-\\w])(" + _HS_NUMPHRASE + r")"
                        r"(?:[-\\s]+(?:\\w+\\s+){0,2})?" + _HS_NOUN, re.I)'''
assert src.count(OLD) == 1, "attach match %d" % src.count(OLD)
src = src.replace(OLD, NEW_ATT, 1)

# the call site parses instead of dict-lookup
OLD_USE = '''            saw = {_HS_WORD[m.group(1).lower()]
                   for m in _HS_ATTACH.finditer(_hash_set_strip(raw))}'''
NEW_USE = '''            saw = set()
            for m in _HS_ATTACH.finditer(_hash_set_strip(raw)):
                val = _hs_number(m.group(1))
                if val is None:
                    findings.append(Finding(
                        "hash_set_single_source", rel, idx,
                        "D1: could not parse the count phrase %r. Unparsed is NOT "
                        "clean - widen the parser or rewrite the phrase."
                        % m.group(1)[:40]))
                else:
                    saw.add(val)'''
assert src.count(OLD_USE) == 1, "call-site match %d" % src.count(OLD_USE)
src = src.replace(OLD_USE, NEW_USE, 1)

TOOL.write_text(src, encoding="utf-8")
import ast
ast.parse(TOOL.read_text(encoding="utf-8"))
print("D1 number parser rebuilt (numerals + compounds + ordinals); syntax OK")
