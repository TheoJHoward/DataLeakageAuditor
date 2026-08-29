#!/usr/bin/env python3
"""D1 — CONTROL-CHARACTER SCAN of the shipping corpus.

D1.1 POPULATION: the six-file tag hash set, plus every file with an entry in
`evidence/MANIFEST.sha256`. Stated with the result, per §30.1, together with the
exclusion list.

D1.2 A hit is content no decision produced. Reported with file, BYTE OFFSET, the
character, and surrounding text. Nothing is fixed by this script.

WHY THIS CLASS EARNED A DETECTOR
--------------------------------
Four incidents this phase, all from the same mechanism: a `\\b` intended as a
regex word boundary, written through a shell heredoc or a non-raw Python string,
becomes a literal BACKSPACE byte (0x08). The regex still compiles. It simply can
never match. Twice this produced a FALSE CLEAN from a sweep (§88), and once a
false positive (R81/C2). A control byte is invisible in every display the work
passes through - terminal, editor, diff, and code review alike.

The scan is byte-exact and needs no vocabulary, which is what makes it the right
shape of instrument for a class that defeated inspection four times.
"""
import pathlib
import sys
import unicodedata

REPO = pathlib.Path(__file__).resolve().parents[1]
EVID = REPO / "evidence"

SIX = [
    "PREREG.md", "DESIGN.md", "HISTORY.md",
    "tools/check_registration.py", "protocol/runtime_reference.py",
    "AVAILABILITY_DECLARATION.md",
]

# TAB, LF, CR are the permitted control characters. Everything else in the C0
# range, DEL, and the C1 range is a hit.
ALLOWED = {0x09, 0x0A, 0x0D}
# Unicode general categories that do not render as visible text.
INVISIBLE_CATS = {"Cc", "Cf", "Co", "Cs", "Cn", "Zl", "Zp"}
# Rendered as a space but not U+0020 - reported separately, as an ADVISORY,
# because "printable" is arguable for them and overclaiming is its own defect.
ADVISORY = {0x00A0, 0x2007, 0x202F, 0x205F, 0x3000, 0x1680} | set(range(0x2000, 0x200B))


def population():
    """Six-file set + every manifest entry. Returns {abs_path: [labels]}."""
    pop = {}
    for rel in SIX:
        pop.setdefault((REPO / rel).resolve(), []).append("six-file set")
    mf = EVID / "MANIFEST.sha256"
    for line in mf.read_text(encoding="utf-8").split("\n"):
        if not line or line.startswith("#") or "  " not in line:
            continue
        rel = line.split("  ", 1)[1]
        pop.setdefault((EVID / rel).resolve(), []).append("manifest")
    pop.setdefault(mf.resolve(), []).append("the manifest itself")
    return pop


def scan_text(text):
    """Yield (byte_offset, char) for every non-printing character."""
    off = 0
    for ch in text:
        cp = ord(ch)
        if cp not in ALLOWED:
            if cp < 0x20 or cp == 0x7F or 0x80 <= cp <= 0x9F:
                yield off, ch, "CONTROL"
            elif unicodedata.category(ch) in INVISIBLE_CATS:
                yield off, ch, "INVISIBLE"
            elif cp in ADVISORY:
                yield off, ch, "ADVISORY"
        off += len(ch.encode("utf-8"))


def describe(ch):
    try:
        name = unicodedata.name(ch)
    except ValueError:
        name = {0x08: "BACKSPACE", 0x00: "NULL", 0x1B: "ESCAPE", 0x7F: "DELETE",
                0x0B: "LINE TABULATION", 0x0C: "FORM FEED"}.get(ord(ch), "<unnamed control>")
    return "U+%04X %s" % (ord(ch), name)


def context(text, idx_char, width=48):
    lo, hi = max(0, idx_char - width), min(len(text), idx_char + width)
    seg = text[lo:hi]
    return "".join(("<%s>" % describe(c).split()[0]) if (ord(c) < 0x20 and ord(c) not in (0x09,))
                   else ("\\n" if c == "\n" else c) for c in seg)


def main():
    pop = population()
    hits, skipped, scanned = [], [], 0
    for path in sorted(pop):
        if not path.exists() or path.is_dir():
            skipped.append((path, "MISSING"))
            continue
        raw = path.read_bytes()
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            skipped.append((path, "not UTF-8 text"))
            continue
        scanned += 1
        chars = list(text)
        for off, ch, kind in scan_text(text):
            idx = None
            # locate the character index for context (first exact byte match)
            b = 0
            for i, c in enumerate(chars):
                if b == off:
                    idx = i
                    break
                b += len(c.encode("utf-8"))
            hits.append((path, off, ch, kind, context(text, idx if idx is not None else 0)))

    print("D1 — CONTROL-CHARACTER SCAN")
    print("  POPULATION (§30.1): six-file tag hash set + every `evidence/MANIFEST.sha256`")
    print("                      entry + the manifest itself = %d distinct paths." % len(pop))
    print("  SCANNED           : %d files that decode as strict UTF-8." % scanned)
    print("  EXCLUSIONS (§30.1): %d — listed below by reason, none waived silently.\n"
          % len(skipped))

    real = [h for h in hits if h[3] != "ADVISORY"]
    adv = [h for h in hits if h[3] == "ADVISORY"]

    print("  CONTROL / INVISIBLE HITS: %d" % len(real))
    for path, off, ch, kind, ctx in real:
        rel = path.relative_to(REPO) if REPO in path.parents or path == REPO else path
        print("\n    %s" % rel)
        print("      byte offset : %d" % off)
        print("      character   : %s   [%s]" % (describe(ch), kind))
        print("      context     : %s" % ctx)
        print("      population  : %s" % ", ".join(pop[path]))

    print("\n  ADVISORY (renders as a space, not U+0020): %d" % len(adv))
    for path, off, ch, kind, ctx in adv[:20]:
        rel = path.relative_to(REPO) if REPO in path.parents or path == REPO else path
        print("    %s  byte %d  %s" % (rel, off, describe(ch)))
    if len(adv) > 20:
        print("    ... and %d more" % (len(adv) - 20))

    if skipped:
        print("\n  EXCLUDED, WITH REASON:")
        by = {}
        for path, why in skipped:
            by.setdefault(why, []).append(path)
        for why, paths in sorted(by.items()):
            print("    %-16s %d file(s)" % (why, len(paths)))
            exts = {}
            for p in paths:
                exts[p.suffix or "<none>"] = exts.get(p.suffix or "<none>", 0) + 1
            print("      by extension: %s" % ", ".join("%s×%d" % (e, n)
                                                       for e, n in sorted(exts.items())))
            if why == "MISSING":
                for p in paths:
                    print("      MISSING: %s" % p)

    print("\n  RESULT: %s" % ("CLEAN — no control or invisible character in the corpus"
                              if not real else "**%d HIT(S)**" % len(real)))
    return 1 if real else 0


if __name__ == "__main__":
    sys.exit(main())
