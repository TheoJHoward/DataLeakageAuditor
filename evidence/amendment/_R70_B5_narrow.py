#!/usr/bin/env python3
"""B5 follow-up: the number parser exposed two matcher defects.

(1) bare `lines` is not a hash-set noun. With numerals now parsed, "drifted 169
    lines" and "by sixty-four lines" were read as hash-set counts of 169 and 64.
    Bare `lines` is only hash-set-ish when the sentence is about the tag message
    ("a tag message with five lines"), so it now requires that context.
(2) the phrase alternation admitted "and" on its own, which parses to nothing.
"""
import pathlib

TOOL = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01/"
                    "tools/check_registration.py")
s = TOOL.read_text(encoding="utf-8")

# (1) split the noun set: strict always, bare `lines` only in tag-message context
OLD_NOUN = ('_HS_NOUN = r"(?:hashes|hash\\s+lines|hash|SHA-?256\\s+lines|SHA-?256|'
            'line\\s+block|lines)"')
NEW_NOUN = ('# STRICT: nouns that are hash-set nouns wherever they appear.\n'
            '_HS_NOUN = r"(?:hashes|hash\\s+lines|hash|SHA-?256\\s+lines|SHA-?256|line\\s+block)"\n'
            '# LOOSE: bare "lines" is a hash-set noun ONLY where the sentence is about the\n'
            '# tag message ("a tag message with five lines"). Applied conditionally, because\n'
            '# unconditionally it reads "drifted 169 lines" as a count of 169 hashes - which\n'
            '# it did, until R70/B5 gave the parser numerals to read.\n'
            '_HS_NOUN_LOOSE = r"(?:lines?)"')
assert s.count(OLD_NOUN) == 1, "noun match %d" % s.count(OLD_NOUN)
s = s.replace(OLD_NOUN, NEW_NOUN, 1)

# (2) the phrase must contain a real number token, not just "and"
OLD_P = ('_HS_NUMPHRASE = (r"(?:\\d{1,4}(?:,\\d{3})*|(?:" + _HS_NUMTOK + r")"\n'
         '                 r"(?:[-\\s]+(?:" + _HS_NUMTOK + r"))*)")')
NEW_P = ('_HS_NUMVAL = "|".join(sorted(list(_HS_UNITS) + list(_HS_TENS) + ["hundred"],\n'
         '                            key=len, reverse=True))\n'
         '# the phrase must START with a real number token; "and" may only join.\n'
         '_HS_NUMPHRASE = (r"(?:\\d{1,4}(?:,\\d{3})*|(?:" + _HS_NUMVAL + r")"\n'
         '                 r"(?:[-\\s]+(?:" + _HS_NUMTOK + r"))*)")')
assert s.count(OLD_P) == 1, "phrase match %d" % s.count(OLD_P)
s = s.replace(OLD_P, NEW_P, 1)

# a second matcher for the loose noun
OLD_A = ('_HS_ATTACH = re.compile(r"(?<![-\\w])(" + _HS_NUMPHRASE + r")"\n'
         '                        r"(?:[-\\s]+(?:\\w+\\s+){0,2})?" + _HS_NOUN, re.I)')
NEW_A = ('_HS_ATTACH = re.compile(r"(?<![-\\w])(" + _HS_NUMPHRASE + r")"\n'
         '                        r"(?:[-\\s]+(?:\\w+\\s+){0,2})?" + _HS_NOUN, re.I)\n'
         '_HS_ATTACH_LOOSE = re.compile(r"(?<![-\\w])(" + _HS_NUMPHRASE + r")"\n'
         '                              r"(?:[-\\s]+(?:\\w+\\s+){0,2})?" + _HS_NOUN_LOOSE, re.I)\n'
         '_HS_TAGMSG = re.compile(r"tag[- ]message", re.I)')
assert s.count(OLD_A) == 1, "attach match %d" % s.count(OLD_A)
s = s.replace(OLD_A, NEW_A, 1)

# call site: use the loose matcher only in tag-message context
OLD_U = "            for m in _HS_ATTACH.finditer(_hash_set_strip(raw)):"
NEW_U = ("            cleaned = _hash_set_strip(raw)\n"
         "            matcher = (_HS_ATTACH_LOOSE if _HS_TAGMSG.search(raw)\n"
         "                       else _HS_ATTACH)\n"
         "            for m in matcher.finditer(cleaned):")
assert s.count(OLD_U) == 1, "use match %d" % s.count(OLD_U)
s = s.replace(OLD_U, NEW_U, 1)
s = s.replace("            saw = set()\n", "            saw = set()\n", 1)

TOOL.write_text(s, encoding="utf-8")
import ast
ast.parse(TOOL.read_text(encoding="utf-8"))
print("noun set split (strict / tag-message-loose); phrase must start with a number; syntax OK")
