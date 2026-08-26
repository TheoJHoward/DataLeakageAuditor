#!/usr/bin/env python3
"""FULL-COVERAGE PROVENANCE for manifest section-B hunks.  DELTA R51/W1.

WHY THIS REPLACES THE PROBE CHECK. The previous check (viii) sampled five 110-char
windows, first hit wins - 21.1% of a 2,612-char hunk. Mutation-tested at R49, it passed
ALL of: tolerance 0.010 -> 0.100; deleting the fails-this-gate-row sentence; dropping
`tier` from the key; flipping "fails this gate row" -> "is recorded as a deviation";
deleting the pass/fail-evidence sentence. It reported green on the exact reduction it
existed to catch, including the one R47/P7 was written to eliminate.

WHAT THIS DOES INSTEAD. Greedy longest-match tiling over 100% of the hunk. Walk the
operative text left to right; at each position take the LONGEST substring that appears
in any authorised source; advance by it. A span that matches nothing at least MIN_RUN
long is UNCOVERED and is reported with its text.

AUTHORISED SOURCES, and why each is legitimate:
  - the document(s) the manifest row names       -> drafted text
  - the hunk's own anchor_text                   -> registered v30 text being replaced
  - PREREG.md                                    -> registered text quoted in retentions
A span found in none of those is text with no provenance, which is the thing being
looked for.

Coverage is REPORTED as a number, not asserted as a boolean, so a partial landing is
visible rather than rounded to PASS.
"""
import json
import pathlib
import re

D = pathlib.Path("C:/Users/ttbea/AppData/Local/Temp/claude/"
                 "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
                 "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/amendment")
REPO = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01")

MIN_RUN = 40          # a match shorter than this is noise, not provenance
MAX_PROBE = 600       # cap on the binary search for the longest match


def norm(x):
    x = re.sub(r"(?m)^>\s?", "", x or "")
    return re.sub(r"\s+", " ", x).strip()


def longest_match_at(op, i, sources):
    """Longest substring of op starting at i that occurs in any source."""
    lo, hi, best = MIN_RUN, min(MAX_PROBE, len(op) - i), 0
    if hi < lo:
        seg = op[i:]
        return len(seg) if seg and any(seg in s for s in sources) else 0
    if not any(op[i:i + lo] in s for s in sources):
        return 0
    while lo <= hi:                      # binary search on match length
        mid = (lo + hi) // 2
        if any(op[i:i + mid] in s for s in sources):
            best, lo = mid, mid + 1
        else:
            hi = mid - 1
    return best


def coverage(op, sources):
    """Return (covered_chars, [uncovered spans])."""
    i, covered, gaps, gap = 0, 0, [], ""
    while i < len(op):
        n = longest_match_at(op, i, sources)
        if n:
            if gap.strip():
                gaps.append(gap.strip())
            gap = ""
            covered += n
            i += n
        else:
            gap += op[i]
            i += 1
    if gap.strip():
        gaps.append(gap.strip())
    return covered, gaps


def run(verbose=True):
    man = (D / "BLOCK_MANIFEST.md").read_text(encoding="utf-8")
    secB = man[man.index("## \u00a7B"):]
    if "## \u00a7C" in secB:
        secB = secB[:secB.index("## \u00a7C")]
    secA = man[:man.index("## \u00a7B")]
    hunks = json.loads((D / "_X5_hunks_v2.json").read_text(encoding="utf-8"))["hunks"]

    def ln(h):
        m = re.search(r"\d+", h.get("prereg_line", "") or "")
        return int(m.group(0)) if m else 9999

    HN = {f"H{i}": h for i, h in enumerate(sorted(hunks, key=ln), 1)}
    prereg = norm(REPO.joinpath("PREREG.md").read_text(encoding="utf-8"))

    # SPANS ARE DECLARED IN THE MANIFEST (M1: the manifest is the authority), as
    # span:<<start>>...<<end>> on the section-B row, or span:SELF-SOURCED where the
    # JSON itself is the source of record and no external document exists to check
    # against. The checker extracts the span FRESH from the named source each run and
    # requires it to survive verbatim in the hunk.
    #
    # This is the CONVERSE direction and it is not optional: coverage tiling is
    # deletion-blind by construction - removing text never lowers the provenance of
    # what remains - and deletion is the class that produced hunk 2.33.
    SPAN_RE = re.compile("span:«(.+?)»…«(.+?)»")

    def span_from_row(row_line, fn):
        if "span:SELF-SOURCED" in row_line:
            return "SELF"
        m = SPAN_RE.search(row_line)
        if not m:
            return None
        fp = D / fn
        if not fp.exists():
            return None
        t = norm(fp.read_text(encoding="utf-8"))
        a, b = m.group(1), m.group(2)
        i, j = t.find(a), t.find(b)
        if i < 0 or j < i:
            return "MARKERS-LOST"
        return t[i:j + len(b)]

    # SECTION A rows: the source is SCHEMA_SET_FINAL.md and the span is the block at
    # the manifest's declared line range. Covering them here is the point of R53/Y1 -
    # a check that cannot reach the hunks most likely to drift is checking the wrong set.
    ssf_lines = (D / "SCHEMA_SET_FINAL.md").read_text(encoding="utf-8").split("\n")

    def block_text(a, b):
        out = []
        for raw in ssf_lines[a - 1:b]:
            if raw.startswith("```"):
                continue
            out.append(re.sub(r"^>\s?", "", raw) if raw.startswith(">") else raw)
        return norm("\n".join(out))

    ROW_A = re.compile(r"^\|\s*\S+?\s*\|\s*(\d+)(?:\s*[\u2013-]\s*(\d+))?\s*\|.*?\*\*(H\d+)\*\*")
    secA_rows = {}
    for line in secA.split("\n"):
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
        # A hunk may be claimed in §A AND carry a §B row naming a further source -
        # H2 is "the amendments block (plus §A-33)". Both sources must be admitted, or
        # the §A branch reports a gap that is really a source it was not shown.
        srcs = [norm(h.get("anchor_text")), prereg,
                norm((D / "SCHEMA_SET_FINAL.md").read_text(encoding="utf-8"))]
        for bl in secB.split(chr(10)):
            if bl.startswith("|") and ("**" + hid + "**") in bl:
                for fn in re.findall(r"`([A-Za-z0-9_.\-]+\.(?:md|json))`", bl):
                    fp = D / fn
                    if fp.exists():
                        srcs.append(norm(fp.read_text(encoding="utf-8")))
        cov, gaps = coverage(op, [x for x in srcs if x])
        pct = 100.0 * cov / len(op)
        st = "INTACT"
        for a, b in spans:
            blk = block_text(a, b)
            if blk and blk not in op:
                st = "BROKEN"
                break
        # A dual-claimed hunk also honours its §B span. H2 draws 77% of its text from
        # K2_AMENDMENT_LEDGER.md and only ~17% from its §A block, so the §A span alone
        # left most of it deletion-blind - which the mutation test found, not reasoning.
        if st == "INTACT":
            for bl in secB.split(chr(10)):
                if bl.startswith("|") and ("**" + hid + "**") in bl:
                    for fn in re.findall(r"`([A-Za-z0-9_.\-]+\.(?:md|json))`", bl):
                        sp = span_from_row(bl, fn)
                        if sp and sp not in ("SELF", "MARKERS-LOST") and sp not in op:
                            st = "BROKEN"
        rows.append((hid, len(op), pct, gaps, True, st, "A"))
        if pct < 100.0 or st != "INTACT":
            failures.append(hid)

    for line in secB.split("\n"):
        if not (line.startswith("|") and "**H" in line):
            continue
        hid = re.search(r"\*\*(H\d+)\*\*", line).group(1)
        if hid in seen:
            continue                      # covered above as a section-A hunk
        files = re.findall(r"`([A-Za-z0-9_.\-]+\.(?:md|json))`", line)
        h = HN.get(hid) or {}
        op = norm(h.get("operative_text"))
        if not op:
            continue
        srcs = [norm(h.get("anchor_text")), prereg]
        for fn in files:
            fp = D / fn
            if fp.exists():
                srcs.append(norm(fp.read_text(encoding="utf-8")))
        srcs = [s for s in srcs if s]
        cov, gaps = coverage(op, srcs)
        pct = 100.0 * cov / len(op)
        # CONVERSE: where a span is declared, it must survive in the hunk verbatim.
        span_state = "NONE"
        for fn in files:
            sp = span_from_row(line, fn)
            if sp == "SELF":
                span_state = "SELF"
            elif sp == "MARKERS-LOST":
                span_state = "MARKERS-LOST"
            elif sp:
                span_state = "INTACT" if sp in op else "BROKEN"
            break
        rows.append((hid, len(op), pct, gaps, bool(files), span_state, "B"))
        if pct < 100.0 or not files or span_state in ("BROKEN", "MARKERS-LOST", "NONE"):
            failures.append(hid)

    if verbose:
        na = sum(1 for r in rows if r[6] == "A")
        print("  hunks bound here: %d   (\u00a7A %d, \u00a7B %d)   rule: 100%% provenance + span intact"
              % (len(rows), na, len(rows) - na))
        nospan = [r[0] for r in rows if r[5] == "NONE"]
        selfs = [r[0] for r in rows if r[5] == "SELF"]
        for hid, n, pct, gaps, named, sp, sec in sorted(rows, key=lambda r: (r[2], int(r[0][1:]))):
            ok = pct >= 100.0 and named and sp in ("INTACT", "SELF")
            print("    %-5s \u00a7%s %5d chars  coverage %6.2f%%  gaps %d  span %-7s%s"
                  % (hid, sec, n, pct, len(gaps), sp, "" if ok else "   <-- FAIL"))
            for g in gaps[:3]:
                print("            UNPROVENANCED: %r" % g[:150])
        if nospan:
            print("  NO SPAN DECLARED (deletion-blind, reported not assumed): %s" % nospan)
        if selfs:
            print("  SELF-SOURCED (the JSON is the source of record; no external document")
            print("    exists to check against, so the converse test cannot apply and these")
            print("    are checkable by review only): %s" % selfs)
    return failures, rows


if __name__ == "__main__":
    import sys
    f, _ = run()
    print("\n  failures: %d %s" % (len(f), f or ""))
    sys.exit(1 if f else 0)
