"""C1(c): all-writers survey.

Walk every *.py under the read-only archive C:\\Users\\ttbea\\OneDrive\\Desktop\\MBO_2025
and report every line mentioning `aggressor_side` or `is_buy_aggressor`, classified
as WRITER (the line assigns/creates the column) vs READ/OTHER.

Read-only: opens archive files for reading only. Output goes to stdout.
"""
import hashlib
import os
import re
from datetime import datetime, timezone

ARCHIVE = r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025"
COLS = ("aggressor_side", "is_buy_aggressor")

MENTION = re.compile(r"aggressor_side|is_buy_aggressor")

# Writer forms. Each is (label, compiled regex).
WRITER_PATTERNS = [
    ("subscript-assign",
     re.compile(r"""\[\s*["'](?:aggressor_side|is_buy_aggressor)["']\s*\]\s*(?:\+|-|\*|/|\|)?=(?!=)""")),
    ("loc/iloc-assign",
     re.compile(r"""\.(?:loc|iloc|at|iat)\s*\[[^\]]*["'](?:aggressor_side|is_buy_aggressor)["'][^\]]*\]\s*=(?!=)""")),
    ("kwarg-assign(assign/agg/NamedAgg)",
     re.compile(r"""(?<![\w."'])(?:aggressor_side|is_buy_aggressor)\s*=(?!=)""")),
    ("dict-literal-key",
     re.compile(r"""["'](?:aggressor_side|is_buy_aggressor)["']\s*:""")),
    ("rename-target",
     re.compile(r"""rename\s*\(.*["'](?:aggressor_side|is_buy_aggressor)["']""")),
    ("schema/field-decl",
     re.compile(r"""(?:pa\.field|pd\.Series|astype)\s*\(\s*["']?(?:aggressor_side|is_buy_aggressor)""")),
]


def classify(line):
    hits = [lab for lab, rx in WRITER_PATTERNS if rx.search(line)]
    stripped = line.strip()
    if stripped.startswith("#"):
        return "COMMENT", hits
    if hits:
        return "WRITER", hits
    return "READ/OTHER", hits


def main():
    print("C1 (c) all-writers survey: aggressor_side / is_buy_aggressor")
    print("run_utc: %s" % datetime.now(timezone.utc).isoformat())
    print("archive root (read-only): %s" % ARCHIVE)
    print("columns surveyed: %s" % ", ".join(COLS))
    print("scope: every *.py under the archive root, recursive")
    print()
    print("writer classification patterns:")
    for lab, rx in WRITER_PATTERNS:
        print("  %-34s %s" % (lab, rx.pattern))
    print("  (a line starting with '#' is classified COMMENT even if it matches)")
    print()

    py_files = []
    for root, dirs, files in os.walk(ARCHIVE):
        for f in files:
            if f.endswith(".py"):
                py_files.append(os.path.join(root, f))
    py_files.sort()

    per_file = []
    n_mentions = 0
    n_writer = 0
    for path in py_files:
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as fh:
                lines = fh.read().splitlines()
        except OSError as e:
            print("!! could not read %s: %s" % (path, e))
            continue
        rows = []
        for i, line in enumerate(lines, 1):
            if MENTION.search(line):
                kind, labs = classify(line)
                rows.append((i, kind, labs, line.rstrip()))
        if rows:
            per_file.append((path, rows))
            n_mentions += len(rows)
            n_writer += sum(1 for r in rows if r[1] == "WRITER")

    print("total *.py scanned: %d" % len(py_files))
    print("files with >=1 mention: %d" % len(per_file))
    print("total mention lines: %d" % n_mentions)
    print("total WRITER lines: %d" % n_writer)
    print()

    print("=" * 78)
    print("SECTION 1 - WRITER LINES ONLY (verbatim, grouped by file)")
    print("=" * 78)
    writer_files = []
    for path, rows in per_file:
        w = [r for r in rows if r[1] == "WRITER"]
        if not w:
            continue
        writer_files.append((path, len(w)))
        print()
        print("FILE: %s" % path)
        for i, kind, labs, line in w:
            print("  L%-5d [%s]" % (i, ",".join(labs)))
            print("        %s" % line)

    print()
    print("=" * 78)
    print("SECTION 2 - WRITER FILE ROLL-UP (%d files)" % len(writer_files))
    print("=" * 78)
    for path, cnt in sorted(writer_files, key=lambda t: (-t[1], t[0])):
        print("  %3d writer line(s)  %s" % (cnt, path))

    print()
    print("=" * 78)
    print("SECTION 3 - WRITER FILES DEDUPLICATED BY CONTENT (whole-file MD5)")
    print("=" * 78)
    print("Purpose: the archive keeps several mirrored script trees; identical")
    print("MD5 means the same tagger source, not an independent writer.")
    print()
    groups = {}
    for path, _cnt in writer_files:
        h = hashlib.md5(open(path, "rb").read()).hexdigest()
        groups.setdefault((os.path.basename(path), h), []).append(path)
    print("distinct (basename, md5) writer sources: %d" % len(groups))
    print()
    for (base, h), paths in sorted(groups.items()):
        print("%-24s md5=%s  copies=%d" % (base, h, len(paths)))
        for p in sorted(paths):
            print("    %s" % p)
    print()
    by_base = {}
    for (base, h), paths in groups.items():
        by_base.setdefault(base, set()).add(h)
    print("basenames with MORE THAN ONE distinct content hash (divergent copies):")
    div = {b: hs for b, hs in by_base.items() if len(hs) > 1}
    if not div:
        print("  (none)")
    for b, hs in sorted(div.items()):
        print("  %s -> %d distinct hashes: %s" % (b, len(hs), ", ".join(sorted(hs))))

    print()
    print("=" * 78)
    print("SECTION 4 - ALL MENTIONS (verbatim, incl. readers and comments)")
    print("=" * 78)
    for path, rows in per_file:
        print()
        print("FILE: %s   (%d mention line(s))" % (path, len(rows)))
        for i, kind, labs, line in rows:
            tag = kind if not labs else "%s:%s" % (kind, ",".join(labs))
            print("  L%-5d %-46s | %s" % (i, tag, line.strip()))


if __name__ == "__main__":
    main()
