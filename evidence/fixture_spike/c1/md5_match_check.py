"""C1(a): recompute MD5 of the two ZC 2025-01 archive parquets and compare
against pc2_transfer/transfer/checksums.txt lines 49 and 61.

Read-only against the archive. Prints a full capture to stdout.
"""
import hashlib
import os
from datetime import datetime, timezone

ARCHIVE = r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025"
CHECKSUMS = os.path.join(ARCHIVE, "pc2_transfer", "transfer", "checksums.txt")
ZC = os.path.join(ARCHIVE, "processed", "zc")

TARGETS = [
    (49, os.path.join(ZC, "zc_snapshots_2025-01.parquet")),
    (61, os.path.join(ZC, "zc_trades_tagged_2025-01.parquet")),
]


def md5_of(path, chunk=1 << 20):
    h = hashlib.md5()
    with open(path, "rb") as fh:
        while True:
            b = fh.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def main():
    print("C1 (a) MD5 match capture")
    print("run_utc: %s" % datetime.now(timezone.utc).isoformat())
    print("python: hashlib.md5, 1 MiB chunks, binary read")
    print()
    print("checksums file: %s" % CHECKSUMS)
    with open(CHECKSUMS, "r", encoding="utf-8", errors="replace") as fh:
        lines = fh.read().splitlines()
    print("checksums file total lines: %d" % len(lines))
    print()

    all_match = True
    for lineno, path in TARGETS:
        raw = lines[lineno - 1]
        expected, _, name = raw.partition("  ")
        expected = expected.strip()
        print("line %d (verbatim): %r" % (lineno, raw))
        print("  -> expected md5: %s" % expected)
        print("  -> named file:   %s" % name.strip())
        print("file recomputed: %s" % path)
        print("  exists: %s" % os.path.exists(path))
        print("  size_bytes: %d" % os.path.getsize(path))
        print("  mtime_utc: %s" % datetime.fromtimestamp(
            os.path.getmtime(path), timezone.utc).isoformat())
        got = md5_of(path)
        print("  recomputed md5: %s" % got)
        print("  expected  md5 (checksums.txt line %d): %s" % (lineno, expected))
        ok = (got == expected)
        all_match = all_match and ok
        print("  verdict: %s" % ("MATCH" if ok else "MISMATCH"))
        print()

    print("overall: %s" % ("BOTH MATCH" if all_match else "AT LEAST ONE MISMATCH"))


if __name__ == "__main__":
    main()
