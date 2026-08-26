#!/usr/bin/env python3
"""§62.2 — move group C out of the temp scratchpad to durable storage.

COPY, RE-HASH AT DESTINATION, COMPARE, and only then delete the source. A move
that fails halfway on 1.5 GB of irreplaceable-until-proven-otherwise bytes would
be the §56 failure with the loss actually realised.

Destination is a sibling of the read-only archive on the same OneDrive Desktop
the project already uses (the archive itself is 684 GB there), so this follows
the project's existing convention rather than inventing a location.
"""
import hashlib, pathlib, shutil

SCR = pathlib.Path("C:/Users/ttbea/AppData/Local/Temp/claude/"
                   "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
                   "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad")
DST = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025_v30a_large_artifacts")
BIG = 5_000_000


def sha(p, buf=1 << 20):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        while True:
            b = f.read(buf)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


targets = [p for p in sorted(SCR.rglob("*"))
           if p.is_file() and p.stat().st_size > BIG
           and p.suffix.lower() not in {".py", ".sh", ".pyc", ".bak"}]
print("group C files: %d   total %.2f GB\n"
      % (len(targets), sum(p.stat().st_size for p in targets) / 1073741824))

DST.mkdir(parents=True, exist_ok=True)
records, failed = [], []
for p in targets:
    rel = p.relative_to(SCR)
    src_hash = sha(p)
    out = DST / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(p, out)
    dst_hash = sha(out)
    ok = (src_hash == dst_hash)
    print("  %-9s %8.1f MB  %s  %s"
          % ("VERIFIED" if ok else "MISMATCH", p.stat().st_size / 1048576,
             src_hash[:12], rel.as_posix()))
    (records if ok else failed).append((rel.as_posix(), src_hash, p.stat().st_size))

print("\n  verified at destination: %d / %d" % (len(records), len(targets)))
if failed:
    print("  *** NOT DELETING SOURCE - %d mismatch(es) ***" % len(failed))
else:
    for p in targets:
        p.unlink()
    print("  source copies deleted from temp: %d" % len(targets))

import json
(DST / "_MOVE_RECORD.json").write_text(
    json.dumps({"destination": str(DST), "files": [
        {"path": r, "sha256": h, "bytes": b} for r, h, b in records]}, indent=1),
    encoding="utf-8")
print("  move record written: %s" % (DST / "_MOVE_RECORD.json"))
