"""C1(c) supplement: for one representative of each distinct writer source,
extract the enclosing def block of every writer line and hash the normalized
block, so the survey answers "how many distinct tagging RULES exist", not just
"how many files mention the column".

Read-only against the archive.
"""
import ast
import hashlib
import os
import re
from datetime import datetime, timezone

REPS = [
    r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025\scripts\pipeline\process_zc.py",
    r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025\scripts\pipeline\process_mbo.py",
    r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025\pc2_transfer\scripts\pipeline\process_mbo.py",
    r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025\scripts\pipeline\process_gc.py",
    r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025\scripts\pipeline\process_gapfill.py",
    r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025\pc2_transfer\scripts\pipeline\process_gapfill.py",
    r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025\scripts\pipeline\process_gapfill_jan.py",
    r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025\pc2_transfer\scripts\pipeline\process_gapfill_jan.py",
    r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025\scripts\pipeline\flow_tagger.py",
    r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025\pc2_transfer\scripts\pipeline\flow_tagger.py",
    r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025\scripts\phase4\phase4_ml.py",
    r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025\scripts\analysis\phase4_ml.py",
]

WRITE = re.compile(
    r"""(\[\s*["'](?:aggressor_side|is_buy_aggressor)["']\s*\]\s*=(?!=))"""
    r"""|(\.(?:loc|iloc|at|iat)\s*\[[^\]]*["'](?:aggressor_side|is_buy_aggressor)["'][^\]]*\]\s*=(?!=))"""
    r"""|((?<![\w."'])(?:aggressor_side|is_buy_aggressor)\s*=(?!=))"""
    r"""|(["'](?:aggressor_side|is_buy_aggressor)["']\s*:)"""
)


def enclosing_defs(path, lines):
    """Map line number -> (def name, start, end) using the AST."""
    try:
        tree = ast.parse("\n".join(lines))
    except SyntaxError as e:
        return None, "SyntaxError: %s" % e
    spans = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            spans.append((node.lineno, getattr(node, "end_lineno", node.lineno), node.name))
    spans.sort(key=lambda t: (t[0], -(t[1])))
    return spans, None


def main():
    print("C1 (c) supplement - distinct tagging RULES among writer sources")
    print("run_utc: %s" % datetime.now(timezone.utc).isoformat())
    print()
    blocks = {}
    for path in REPS:
        if not os.path.exists(path):
            print("MISSING: %s" % path)
            continue
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            lines = fh.read().splitlines()
        spans, err = enclosing_defs(path, lines)
        wlines = [i for i, ln in enumerate(lines, 1)
                  if WRITE.search(ln) and not ln.strip().startswith("#")]
        print("=" * 78)
        print("FILE: %s" % path)
        print("  file md5: %s" % hashlib.md5(open(path, "rb").read()).hexdigest())
        print("  writer lines: %s" % ", ".join(str(x) for x in wlines))
        if err:
            print("  AST: %s" % err)
            continue
        seen = set()
        for w in wlines:
            enc = [s for s in spans if s[0] <= w <= s[1]]
            if not enc:
                print("  L%d is at module scope (no enclosing def)" % w)
                continue
            start, end, name = enc[-1]
            if (start, end, name) in seen:
                continue
            seen.add((start, end, name))
            body = lines[start - 1:end]
            norm = "\n".join(l.rstrip() for l in body if l.strip() and
                             not l.strip().startswith("#"))
            h = hashlib.md5(norm.encode("utf-8")).hexdigest()
            print()
            print("  --- def %s()  lines %d-%d  block_md5=%s" % (name, start, end, h))
            for off, l in enumerate(body, start):
                print("      %4d | %s" % (off, l.rstrip()))
            blocks.setdefault(h, []).append("%s::%s()" % (os.path.basename(path), name))
        print()

    print("=" * 78)
    print("DISTINCT WRITER BLOCKS BY NORMALIZED BLOCK MD5: %d" % len(blocks))
    print("=" * 78)
    for h, owners in sorted(blocks.items(), key=lambda kv: -len(kv[1])):
        print("  %s  used by %d representative(s):" % (h, len(owners)))
        for o in owners:
            print("      %s" % o)


if __name__ == "__main__":
    main()
