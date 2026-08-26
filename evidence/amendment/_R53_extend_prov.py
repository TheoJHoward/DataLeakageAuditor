#!/usr/bin/env python3
"""DELTA R53/Y1 - make the provenance check reach EVERY hunk, not just section B.

Before: it walked section B only, and skipped any hunk section A also claimed. After
the R53 move that would have left the two most-revised hunks unreached by the very
check the move was made for - the architecture resisting the goal instead of serving it.

Now: section A rows are covered too. Their span is the block text at the manifest's
declared line range, extracted fresh from SCHEMA_SET_FINAL.md; their forward coverage
is measured the same way as section B's. Section A was already bound by M6 check (II)
(`src in op`); this adds the forward direction and puts every hunk in one report.
"""
import pathlib

D = pathlib.Path("C:/Users/ttbea/AppData/Local/Temp/claude/"
                 "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
                 "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/amendment")
p = D / "_provenance.py"
s = p.read_text(encoding="utf-8")

OLD = """    rows, failures = [], []
    for line in secB.split("\\n"):
        if not (line.startswith("|") and "**H" in line):
            continue
        hid = re.search(r"\\*\\*(H\\d+)\\*\\*", line).group(1)
        if re.search(r"\\*\\*" + hid + r"\\*\\*", secA):
            continue                      # also claimed in section A; M6 (II) binds it
        files = re.findall(r"`([A-Za-z0-9_.\\-]+\\.(?:md|json))`", line)"""
NEW = '''    # SECTION A rows: the source is SCHEMA_SET_FINAL.md and the span is the block at
    # the manifest's declared line range. Covering them here is the point of R53/Y1 -
    # a check that cannot reach the hunks most likely to drift is checking the wrong set.
    ssf_lines = (D / "SCHEMA_SET_FINAL.md").read_text(encoding="utf-8").split("\\n")

    def block_text(a, b):
        out = []
        for raw in ssf_lines[a - 1:b]:
            if raw.startswith("```"):
                continue
            out.append(re.sub(r"^>\\s?", "", raw) if raw.startswith(">") else raw)
        return norm("\\n".join(out))

    ROW_A = re.compile(r"^\\|\\s*\\S+?\\s*\\|\\s*(\\d+)(?:\\s*[\\u2013-]\\s*(\\d+))?\\s*\\|.*?\\*\\*(H\\d+)\\*\\*")
    secA_rows = {}
    for line in secA.split("\\n"):
        m = ROW_A.match(line)
        if m:
            a = int(m.group(1))
            b = int(m.group(2)) if m.group(2) else a
            secA_rows.setdefault(m.group(3), []).append((a, b))

    rows, failures, seen = [], [], set()
    for hid, spans in sorted(secA_rows.items(), key=lambda kv: int(kv[0][1:])):
        h = HN.get(hid) or {}
        op = norm(h.get("operative_text"))
        if not op:
            continue
        seen.add(hid)
        srcs = [norm(h.get("anchor_text")), prereg, norm((D / "SCHEMA_SET_FINAL.md").read_text(encoding="utf-8"))]
        cov, gaps = coverage(op, [x for x in srcs if x])
        pct = 100.0 * cov / len(op)
        st = "INTACT"
        for a, b in spans:
            blk = block_text(a, b)
            if blk and blk not in op:
                st = "BROKEN"
                break
        rows.append((hid, len(op), pct, gaps, True, st, "A"))
        if pct < 100.0 or st != "INTACT":
            failures.append(hid)

    for line in secB.split("\\n"):
        if not (line.startswith("|") and "**H" in line):
            continue
        hid = re.search(r"\\*\\*(H\\d+)\\*\\*", line).group(1)
        if hid in seen:
            continue                      # covered above as a section-A hunk
        files = re.findall(r"`([A-Za-z0-9_.\\-]+\\.(?:md|json))`", line)'''
assert s.count(OLD) == 1, "loop head match %d" % s.count(OLD)
s = s.replace(OLD, NEW, 1)

s = s.replace('        rows.append((hid, len(op), pct, gaps, bool(files), span_state))',
              '        rows.append((hid, len(op), pct, gaps, bool(files), span_state, "B"))', 1)

s = s.replace('        print("  section-B hunks bound here: %d   (rule: 100%% of each hunk must have provenance)" % len(rows))',
              '        na = sum(1 for r in rows if r[6] == "A")\n'
              '        print("  hunks bound here: %d   (\\u00a7A %d, \\u00a7B %d)   rule: 100%% provenance + span intact"\n'
              '              % (len(rows), na, len(rows) - na))', 1)

s = s.replace('        for hid, n, pct, gaps, named, sp in sorted(rows, key=lambda r: r[2]):',
              '        for hid, n, pct, gaps, named, sp, sec in sorted(rows, key=lambda r: (r[2], int(r[0][1:]))):', 1)
s = s.replace('            print("    %-5s %5d chars  coverage %6.2f%%  gaps %d  span %-7s%s"\n'
              '                  % (hid, n, pct, len(gaps), sp, "" if ok else "   <-- FAIL"))',
              '            print("    %-5s \\u00a7%s %5d chars  coverage %6.2f%%  gaps %d  span %-7s%s"\n'
              '                  % (hid, sec, n, pct, len(gaps), sp, "" if ok else "   <-- FAIL"))', 1)
p.write_text(s, encoding="utf-8")
print("provenance check now covers section A and section B")
