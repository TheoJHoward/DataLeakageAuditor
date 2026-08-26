"""Per-edit line ledger for the R11-batch pass on availability_declaration_DRAFT.md.

Every row: (anchor, match count, lines added, lines removed, net).
Match count is 1 for every row: the Edit tool refuses a non-unique or
non-matching anchor, so each successful call is exactly one match.

`added` is measured in the FINAL file wherever the edit produced a contiguous
block (the block's extent is printed and can be re-measured); `removed` is the
line count of the old_string that was replaced.

The sum of `net` must equal the measured whole-file delta 2943 - 2415 = 528.
"""
P = (r"C:\Users\ttbea\AppData\Local\Temp\claude"
     r"\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01"
     r"\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\fixture_spike"
     r"\f4\availability_declaration_DRAFT.md")

L = open(P, encoding="utf-8").read().split("\n")


def idx(prefix, start=1):
    for i in range(start - 1, len(L)):
        if L[i].startswith(prefix):
            return i + 1
    raise SystemExit("ANCHOR NOT FOUND: " + prefix[:70])


def block(a, b):
    """lines of the contiguous block [a, b) measured in the final file"""
    return idx(b, idx(a)) - idx(a)


# name, anchor-at-line, added, removed
ROWS = [
    ("E1  header Fixture paragraph rewritten (Z1)",
     idx("Fixture: Phase 5/7"), block("Fixture: Phase 5/7", "---"), 6),
    ("E33 assembly-status: this pass recorded",
     idx("**This R11-batch pass"),
     block("**This R11-batch pass", "**Where the boundary rule lives"), 0),
    ("E34 numbering convention now names §0",
     idx("**Numbering convention adopted"), 4, 3),
    ("E2  Part II preamble: R14-R17 delta-issued box",
     idx("> **Working resolutions R14-R17"), 13, 2),
    ("E3  §0 THE TWO ARTIFACTS inserted (Z1) [incl. E4/E4b/E30 below]",
     idx("## §0."), block("## §0.", "## §A."), 0),
    ("E3b §A heading -> 'First CONFORMANCE section' + §0 note",
     idx("**First CONFORMANCE section"), 4, 3),
    ("E4  §0.1 f2 build-output naming (inside §0)", idx("`...\\scratchpad"), 4, 2),
    ("E4b §0.1 mbo-parquet 'where it exists' (inside §0)",
     idx("parquets that the f2 build reads"), 4, 3),
    ("E30 §0.3 reading rule: archive-level third case (inside §0)",
     idx("may be quoted as ground truth"), 7, 4),
    ("E5  §A.1 tag  SCORED ON ARTIFACT B",
     idx("> **SCORED ON ARTIFACT B** (§0.2) — the trio"),
     block("> **SCORED ON ARTIFACT B** (§0.2) — the trio",
           "**Registered text, PREREG.md line 445"), 0),
    ("E6  §8 tag    SCORED ON ARTIFACT B",
     idx("> **SCORED ON ARTIFACT B** (§0.2). This section IS"),
     block("> **SCORED ON ARTIFACT B** (§0.2). This section IS",
           "**The v30a acceptance fixture"), 0),
    ("E7  §9 tag    SCORED ON ARTIFACT B",
     idx("> **SCORED ON ARTIFACT B** (§0.2) — a raw-bytes"),
     block("> **SCORED ON ARTIFACT B** (§0.2) — a raw-bytes", "All 64 main-set pairs"), 0),
    ("E8  §10 tag   MEASURED ON ARTIFACT A",
     idx("> **MEASURED ON ARTIFACT A** (§0.1) — the f2 lineage"),
     block("> **MEASURED ON ARTIFACT A** (§0.1) — the f2 lineage",
           "**This section states no rule.**"), 0),
    ("E9  §11 tag   MEASURED ON ARTIFACT A",
     idx("> **MEASURED ON ARTIFACT A** (§0.1) — the ZC 2025-01 lineage lattice."),
     block("> **MEASURED ON ARTIFACT A** (§0.1) — the ZC 2025-01 lineage lattice.",
           "`shift(-h)` labels are POSITIONAL"), 0),
    ("E10 §B tag    MEASURED ON ARTIFACT A",
     idx("> **MEASURED ON ARTIFACT A** (§0.1) — the lineage's own"),
     block("> **MEASURED ON ARTIFACT A** (§0.1) — the lineage's own",
           "The element-level statements live"), 0),
    ("E11 §12 tag   MEASURED ON ARTIFACT A",
     idx("> **MEASURED ON ARTIFACT A** (§0.1) — both-branch counts"),
     block("> **MEASURED ON ARTIFACT A** (§0.1) — both-branch counts",
           "**The registered default `available` stands**"), 0),
    ("E12 §13 tag   MEASURED ON A / APPLIED TO B",
     idx("> **MEASURED ON ARTIFACT A** (§0.1) — every cell of the map"),
     block("> **MEASURED ON ARTIFACT A** (§0.1) — every cell of the map",
           "**This section replaces the former"), 0),
    ("E13 §C tag    DUAL (B's universe / A's counts)",
     idx("> **DUAL TAG"),
     block("> **DUAL TAG", "**Everything in this section is stated POST-LAG**"), 0),
    ("E14 §14 tag   MEASURED ON ARTIFACT A",
     idx("> **MEASURED ON ARTIFACT A** (§0.1) — the ZC 2025-01 lineage lattice and its"),
     block("> **MEASURED ON ARTIFACT A** (§0.1) — the ZC 2025-01 lineage lattice and its",
           "**Scope: ZC 2025-01 only**"), 0),
    ("E15 §15 tag   MEASURED ON A (defect in both lineages)",
     idx("> **MEASURED ON ARTIFACT A** (§0.1) — the f2 rebuild is the execution"),
     block("> **MEASURED ON ARTIFACT A** (§0.1) — the f2 rebuild is the execution",
           "**Two as-built defects are properties"), 0),
    ("E16 §17 tag   MEASURED ON A onto B's 35-set",
     idx("> **MEASURED ON ARTIFACT A** (§0.1) — T4 reads the f2 build"),
     block("> **MEASURED ON ARTIFACT A** (§0.1) — T4 reads the f2 build",
           "Projection of the F2 fixture builds"), 0),
    ("E31 §16 tag   NEITHER ARTIFACT (archive-level)",
     idx("> **NEITHER ARTIFACT — this section is about the ARCHIVE"),
     block("> **NEITHER ARTIFACT — this section is about the ARCHIVE",
           "Assumptions the declaration RELIES ON"), 0),
    ("E32 §F tag    NEITHER ARTIFACT (archive-level)",
     idx("> **NEITHER ARTIFACT — these are measurements OF THE ARCHIVE"),
     block("> **NEITHER ARTIFACT — these are measurements OF THE ARCHIVE",
           "**F.1 — Grep undercount"), 0),
    ("E17 §13(i) BOTH MAPS + §13(j) MBO classes [incl. E28]",
     idx("### (i) BOTH MAPS"), block("### (i) BOTH MAPS", "## §C. Two-sided"), 0),
    ("E28   of which: restricted map IS/IS-NOT a scoring key",
     idx("**What the restricted map IS AND IS NOT") if False else
     idx("**What the restricted map IS and IS NOT"),
     block("**What the restricted map IS and IS NOT", "**R17(iii) — THE CHECK"), 0),
    ("E18 §C.3 heading corrected + note (Y2)",
     idx("> **Heading corrected this pass (Y2)"),
     block("> **Heading corrected this pass (Y2)",
           "The columns that read the decision row"), 0),
    ("E19 §C.3 SCOPE QUALIFIER -> retirement + FOUR CATEGORIES (Y2) [incl. E20/E21]",
     idx("> **THE 27-COLUMN LIST ABOVE IS RETIRED"),
     block("> **THE 27-COLUMN LIST ABOVE IS RETIRED", "> **DELETED THIS PASS") - 1, 22),
    ("E22 §C.3 R11-deletion note: referent named",
     idx("> **DELETED THIS PASS"), 14, 9),
    ("E23 §B nq TRADES-CLASSES-ONLY label + reason (Z2)",
     idx("| cl, es, gc, **nq (TRADES-CLASSES-ONLY)**"),
     block("**Label carried on nq in the row above", "For he and le the fixture file") + 1, 1),
    ("E29 §A.6.3 book_imbalance_ratio ONE CLASS ONLY (R16)",
     idx("- **`book_imbalance_ratio` — gate status EXCLUDED"), 5, 2),
    ("E24 §18 row f nq label (Z2) + (i)/(j) pointers",
     idx("| f | **The DECLARED GROUND-TRUTH MAP (R9)**"), 1, 1),
    ("E25 §18 new index row for §0",
     idx("| — | **THE TWO ARTIFACTS**"), 6, 5),
    ("E26 §18 §C row: four categories named",
     idx("| — | **Two-sided ground-truth enumeration"), 1, 1),
    ("E27 §18 preamble names §0",
     idx("Covers **every** element and **every** section"), 3, 2),
]

print(f"{'edit (anchor)':78s} {'@ln':>5s} {'match':>5s} {'+':>4s} {'-':>4s} {'net':>5s}")
total = 0
for name, ln, added, removed in ROWS:
    net = added - removed
    inner = name[:3].strip() in ("E28",)
    inner0 = name[:3].strip() in ("E4", "E4b", "E30") or name.startswith("E4b")
    note = "   (inside E17)" if inner else ("   (inside E3)" if inner0 else "")
    print(f"{name:78s} {ln:5d} {1:5d} {added:4d} {removed:4d} {net:5d}" + note)
    if not (inner or inner0):
        total += net

print()
print("SUM of net line deltas :", total)
print("MEASURED file delta    : 2943 - 2415 =", 2943 - 2415)
print("RECONCILES             :", total == 2943 - 2415)
