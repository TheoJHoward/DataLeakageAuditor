#!/usr/bin/env python3
"""Restore CRLF to files that carried it, after an LF-based edit.

WHY THIS EXISTS. `AVAILABILITY_DECLARATION.md` and `HISTORY.md` are stored CRLF,
uniformly (4027/4027 and 365/365 at HEAD). `.gitattributes` sets `* -text`, so
git stores bytes as given and does not normalise. `pathlib.read_text` opens in
universal-newline mode and silently returns `\\n`; `write_text(newline="\\n")`
then writes LF. The round trip changes EVERY LINE of a file the tag hashes, and
the diff reports it as a full rewrite -- which buries the actual edit.

The conversion is safe here only because each file is UNIFORMLY CRLF: every LF is
preceded by a CR, so LF -> CRLF restores the original bytes on untouched lines
exactly. That is asserted below rather than assumed, per file, before writing.

Written with the Write tool per D2.1.
"""
import hashlib
import pathlib
import subprocess
import sys

REPO = pathlib.Path(r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01")


def head_bytes(rel: str) -> bytes:
    return subprocess.run(["git", "show", "HEAD:" + rel], cwd=str(REPO),
                          capture_output=True).stdout


def to_crlf(rel: str) -> None:
    p = REPO / rel
    raw = p.read_bytes()

    hb = head_bytes(rel)
    crlf, lf = hb.count(b"\r\n"), hb.count(b"\n")
    if crlf == 0:
        print("%-32s HEAD is LF; nothing to do" % rel)
        return
    if crlf != lf:
        sys.exit("HALT: %s is MIXED at HEAD (%d CRLF of %d LF). A blanket "
                 "conversion would change lines the edit never touched." % (rel, crlf, lf))

    if b"\r\n" in raw:
        sys.exit("HALT: %s already contains CRLF; refusing to double-convert" % rel)

    out = raw.replace(b"\n", b"\r\n")
    p.write_bytes(out)
    print("%-32s -> CRLF  (%d lines, %d bytes, sha256 %s)"
          % (rel, out.count(b"\r\n"), len(out),
             hashlib.sha256(out).hexdigest()[:16] + "\u2026"))


for rel in ("AVAILABILITY_DECLARATION.md", "HISTORY.md"):
    to_crlf(rel)
