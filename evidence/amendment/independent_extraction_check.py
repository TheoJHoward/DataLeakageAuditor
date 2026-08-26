#!/usr/bin/env python3
"""§82 — INDEPENDENT EXTRACTION. Closes the self-consistency hole.

§82.1's hole: a range mis-pinned AT AUTHORING TIME is self-consistent. The digest
covers whatever span the range names, both directions pass, nothing fires. It is
exactly what happened at R79: five records pointed at THE CLAUSE when their own
INSERTION POINT named a distinct operative block, and every existing check passed.

§82.3: two paths to the same content, NEITHER DERIVED FROM THE OTHER.
  path A - what the generator actually inserted, read back out of the DIFF.
  path B - located by HEADER SEARCH in SCHEMA_SET_FINAL.md, reading to the next
           clause boundary. It never touches clause_first_line / clause_last_line.

A second check that re-read the stored range would not be a check (§82.3).
"""
import json, pathlib, re, sys

REPO = pathlib.Path(__file__).resolve().parents[2]
SSF = REPO / "evidence/amendment/SCHEMA_SET_FINAL.md"
REC = REPO / "evidence/amendment/SCHEMA_RECORDS.json"
DIFF = REPO / "evidence/amendment/PREREG_v30a_APPROVAL.diff"

L = SSF.read_text(encoding="utf-8").split("\n")
records = json.loads(REC.read_text(encoding="utf-8"))["records"]
diff = DIFF.read_text(encoding="utf-8").split("\n")

# ---- path A: what the diff actually inserted, per record --------------------
inserted, cur = {}, None
for line in diff:
    m = re.match(r"^\+<!-- v30a (\S+) — ", line)
    if m:
        cur = m.group(1)
        inserted[cur] = []
        continue
    if cur and line.startswith("+") and not line.startswith("+++"):
        inserted[cur].append(line[1:])
    elif cur and not line.startswith("+"):
        cur = None

# ---- path B: locate by HEADER SEARCH, never by the stored range -------------
BOUNDARY = re.compile(
    r"^\*\*(DATA THE DECLARATION MUST SUPPLY|ROWS COVERED|INSERTION TEXT|INSERTION POINT"
    r"|SUPERSESSION|THE CLAUSE|WHY|Why|SC-12\(w\)|Corroboration)|^### |^#### "
    # A horizontal rule and a top-level heading also end a block. Without them
    # the LAST block before `# PART 2` had no boundary and path B read on to the
    # end of the region - which is where §10.1-C2ret sits.
    r"|^---\s*$|^## |^# ")


def locate(header_prefix, occurrence=1):
    """Find the nth line starting with header_prefix; read to the next boundary."""
    hits = [i for i, l in enumerate(L, 1) if l.startswith(header_prefix)]
    if len(hits) < occurrence:
        return None, None, None
    s = hits[occurrence - 1]
    e = next((i for i in range(s + 1, len(L) + 2) if i > len(L) or BOUNDARY.match(L[i - 1])),
             len(L) + 1) - 1
    # A `**THE CLAUSE.**` marker IS the first line of its record's declared
    # range, so it belongs to the body. A `### ` SECTION HEADING is not
    # applied text and no record's range starts at one - excluding it keeps
    # path B comparable to path A without either path consulting the other.
    body = L[s - 1:e]
    if header_prefix.startswith("###"):
        body = body[1:]
    return s, e, body


# Each record's path-B locator, derived from its own INSERTION POINT wording -
# NOT from the stored range.
LOCATORS = {
    "SC-1": ("**THE CLAUSE.**", 1), "SC-2": ("**THE CLAUSE.**", 2),
    "SC-3": ("**THE CLAUSE.**", 3), "SC-4": ("**THE CLAUSE.**", 4),
    "SC-5": ("**THE CLAUSE.**", 5),
    "SC-6a": ("**THE CLAUSE.**", 6),
    "SC-6b": ("**INSERTION TEXT — §8.2,", 1),
    "SC-7": ("**THE CLAUSE.**", 7),
    "SC-8a": ("**THE CLAUSE.**", 8),
    "SC-8b": ("**INSERTION TEXT — §11 item 8,", 1),
    "SC-9": ("**THE CLAUSE.**", 9), "SC-10": ("**THE CLAUSE.**", 10),
    "SC-11a": ("**THE CLAUSE.**", 11),
    "SC-11b": ("**INSERTION TEXT — §8.6,", 1),
    "SC-12": ("**THE CLAUSE.**", 12),
    "SC-12p": ("**INSERTION TEXT — §7.7 pointer,", 1),
    "SC-12w": ("**OPERATIVE v30a TEXT at line 929", 1),
    "SC-13a": ("**THE CLAUSE.**", 13), "SC-13b": ("**THE CLAUSE.**", 14),
    "SC-13c-1": ("**THE CLAUSE.**", 15),
    "SC-13c-2": ("**INSERT AFTER (one paragraph", 1),
    # R87/§108 - located by their own section headings, which is where these
    # two name their target. Neither has an INSERTION POINT field.
    "SC-3-C2op": ("### §10.1-C2op", 1),
    "SC-3-C2ret": ("### §10.1-C2ret", 1),
}

print("§82.4 — INDEPENDENT EXTRACTION, per record")
print("  path A = read back out of the generated diff")
print("  path B = located by HEADER SEARCH in the source; the stored range is never read\n")
ok = mismatch = 0
bad = []
for r in records:
    rid = r["id"]
    a = inserted.get(rid)
    prefix, occ = LOCATORS[rid]
    s, e, b = locate(prefix, occ)
    if a is None or b is None:
        print("  %-10s **NOT COMPARABLE** (A=%s B=%s)" % (rid, a is not None, b is not None))
        bad.append(rid); mismatch += 1
        continue
    # Fence markers are block DELIMITERS in the source and are not applied
    # text, so they are not part of either body. Path B saw them and path A
    # never could; §10.1-C2op is the first record whose clause is fenced.
    a_body = [x for x in a if x.strip() and not x.lstrip().startswith("```")]
    b_body = [x for x in b if x.strip() and not x.lstrip().startswith("```")]
    if a_body == b_body:
        ok += 1
        print("  %-10s MATCH      path B l.%-5d-%-5d  %d lines" % (rid, s, e, len(b_body)))
    else:
        mismatch += 1
        bad.append(rid)
        print("  %-10s **MISMATCH**  A=%d lines  B=%d lines (B at l.%d-%d)"
              % (rid, len(a_body), len(b_body), s, e))
        for i in range(min(len(a_body), len(b_body))):
            if a_body[i] != b_body[i]:
                print("      first difference at body line %d" % (i + 1))
                print("        A: %r" % a_body[i][:88])
                print("        B: %r" % b_body[i][:88])
                break

print("\n  %d of %d records match on two independent paths" % (ok, len(records)))
if bad:
    print("  MISMATCHES: %s" % bad)
sys.exit(1 if bad else 0)
