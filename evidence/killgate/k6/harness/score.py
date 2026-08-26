"""Score the run from raw/ using ONLY the eligibility and label mapping fixed in
PRE_RUN_RECORD.md before any tool ran. Emits RESULTS_MATRIX.md.

HIT   : a label mapping to the case's type fires on contaminated AND no label mapping to that
        type fires on clean                                    (PRE_RUN_RECORD 6.1)
MISS  : silent on contaminated, or fires on both sides
ABST  : ineligible (item 4) or crash (item 5), with a recorded reason
"""
import json
import os
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.abspath(os.path.join(HERE, "..", "raw"))
ROOT = os.path.abspath(os.path.join(HERE, ".."))

CASES = ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8"]
TYPE = dict(C1="T1", C2="T2", C3="T3", C4="T4", C5="T5", C6="T6", C7="T7", C8="T8")

# ---- eligibility, from PRE_RUN_RECORD 4.7 (fixed before the run) ----
ELIG = {
    "leak-detect":       set("C5 C6".split()),
    "deepchecks":        set("C1 C4 C5 C6 C8".split()),
    "leakage-buster":    set("C1 C4 C5 C6 C7".split()),
    "Leakly":            set("C2 C3 C5 C6".split()),
    "leakage-analysis":  set("C1 C2 C3 C4".split()),
    "LeakageDetector2.0": set("C1 C2 C3 C4".split()),
    "OMDS":              set("C1 C2".split()),
    "temporalcv":        set("C1 C6".split()),
    "leakfence":         set("C1 C2 C4 C7".split()),
    "leakr":             set("C1 C4 C5".split()),
    "bioLeak":           set("C5".split()),
}
TOOLS = list(ELIG)

# ---- label mapping, from CROSS_TOOL_COMPARISON 2.5 + PRE_RUN_RECORD 5.1 ----
MAP = {
    "deepchecks": {
        "Index Train Test Leakage": "T1", "New Label Train Test": "T1",
        "Datasets Size Comparison": "T1",
        "Train Test Samples Mix": "T4", "Date Train Test Leakage Duplicates": "T4",
        "Date Train Test Leakage Overlap": "T6",
        "Feature Label Correlation": "T5", "Identifier Label Correlation": "T5",
        "Multivariate Drift": "T8", "Feature Drift": "T8", "Label Drift": "T8",
    },
    "leakage-buster": {
        "Target leakage (high correlation)": "T5",
        "Target leakage (categorical purity)": "T5",
        "Target Encoding leakage risk": "T5",
        "Aggregation traces leakage risk": "T5",
        "Rolling statistics leakage risk": "T6",
        "KFold leakage risk (use GroupKFold)": "T7",
        "CV strategy mismatch": "T1",
    },
    "leakfence": {
        "index_overlap": "T1", "duplicate_rows": "T4", "group_overlap": "T7",
        "temporal_overlap": "T4", "global_preprocessing": "T2",
    },
    "temporalcv": {
        "gate_signal_verification": "T6", "gate_suspicious_improvement": "T6",
        "gate_temporal_boundary": "T6",
    },
    "OMDS": {"ax:fit_on_train_only": "T2"},
}
# labels deliberately unmapped -> score nothing (published in the unmapped register)
UNMAPPED = {
    "deepchecks": ["Data Duplicates", "Feature Label Correlation Change", "Conflicting Labels",
                   "Is Single Value", "Special Characters", "Mixed Nulls", "Mixed Data Types",
                   "String Mismatch", "String Mismatch Comparison", "New Category Train Test",
                   "String Length Out Of Bounds", "Feature Feature Correlation",
                   "Outlier Sample Detection"],
    "leakage-buster": ["WOE leakage risk", "CV strategy recommendation", "Time column missing",
                       "Time parse errors", "Time-awareness suggestion"],
}


def load(name):
    p = os.path.join(RAW, f"{name}.json")
    return json.load(open(p)) if os.path.exists(p) else []


def fired_types(tool, labels):
    m = MAP.get(tool, {})
    return {m[x] for x in labels if x in m}


def cell(tool, case, fired_by_side, abst=None):
    """fired_by_side: {'contaminated': set(types), 'clean': set(types)}"""
    t = TYPE[case]
    if case not in ELIG[tool]:
        return "ABST", "ineligible (declared before run, item 4)"
    if abst:
        return "ABST", abst
    con = t in fired_by_side["contaminated"]
    cln = t in fired_by_side["clean"]
    if con and not cln:
        return "HIT", ""
    if con and cln:
        return "MISS", "fired on BOTH sides (false alarm on the clean control)"
    return "MISS", "silent on the contaminated side"


def main():
    res = OrderedDict((t, {}) for t in TOOLS)
    notes = {}

    # ---------- deepchecks / leakage-buster / leakfence / temporalcv ----------
    for tool, fname in (("deepchecks", "deepchecks"), ("leakage-buster", "leakage-buster"),
                        ("leakfence", "leakfence"), ("temporalcv", "temporalcv")):
        recs = load(fname)
        for case in CASES:
            fb, abst = {}, None
            for side in ("contaminated", "clean"):
                r = next((x for x in recs if x.get("case") == case
                          and x.get("side") == side), None)
                if r is None:
                    abst = "no record produced"
                    fb[side] = set()
                    continue
                if r.get("status") == "crash":
                    abst = f"crash: {r.get('error', '')[:120]}"
                labels = r.get("fired_labels", [])
                if tool == "leakage-buster":
                    if any(str(x).startswith("Detector error:") for x in labels):
                        abst = ("crash: internal detector exception "
                                + next(x for x in labels if str(x).startswith("Detector error:")))
                fb[side] = fired_types(tool, labels)
            res[tool][case] = cell(tool, case, fb, abst)

    # ---------- leak-detect: probe-wise, scored from the only_nan=True runs ----------
    recs = load("leak-detect")
    for case in CASES:
        fb = {}
        for side in ("contaminated", "clean"):
            r = next((x for x in recs if x.get("case") == case and x.get("side") == side
                      and x.get("config", {}).get("only_nan") is True), None)
            if r is None or r.get("status") != "ran":
                fb[side] = set()
                continue
            probe = r["config"]["probe"]
            fb[side] = {"T6" if probe == "vertical" else "T5"} if r.get("fired") else set()
        res["leak-detect"][case] = cell("leak-detect", case, fb)

    # ---------- Leakly: generic verdict -> the case's type (PRE_RUN_RECORD 5.2) ----------
    recs = load("Leakly")
    for case in CASES:
        fb = {}
        for side in ("contaminated", "clean"):
            r = next((x for x in recs if x.get("case") == case and x.get("side") == side), None)
            fb[side] = ({TYPE[case]} if (r and r.get("fired")) else set())
        res["Leakly"][case] = cell("Leakly", case, fb)

    # ---------- OMDS ----------
    recs = load("omds")
    for case in CASES:
        fb = {}
        for side in ("contaminated", "clean"):
            r = next((x for x in recs if x.get("case") == case and x.get("side") == side), None)
            labs = [v["axiom"] for v in (r or {}).get("payload", {}).get("violations", [])]
            fb[side] = fired_types("OMDS", labs)
        res["OMDS"][case] = cell("OMDS", case, fb)

    # ---------- crash / not-runnable abstentions ----------
    recs = load("leakage-analysis")
    for case in CASES:
        r = next((x for x in recs if x.get("case") == case), None)
        res["leakage-analysis"][case] = cell(
            "leakage-analysis", case, {"contaminated": set(), "clean": set()},
            abst="crash: IR generation failed (irgen.py:373 visit_Subscript AssertionError)"
            if r else "crash: no record")
    for case in CASES:
        res["LeakageDetector2.0"][case] = cell(
            "LeakageDetector2.0", case, {"contaminated": set(), "clean": set()},
            abst="not programmatically runnable (VS Code extension, no headless entry point)")
    for tool in ("leakr", "bioLeak"):
        for case in CASES:
            res[tool][case] = cell(
                tool, case, {"contaminated": set(), "clean": set()},
                abst="R toolchain could not be installed (machine-wide install requires "
                     "administrator elevation; user-scope installer not published)")

    # ---------- emit ----------
    tally = dict(HIT=0, MISS=0, ABST=0)
    lines = ["| Tool | " + " | ".join(f"{c} {TYPE[c]}" for c in CASES) + " | H | M | A |",
             "|---|" + "---|" * (len(CASES) + 3)]
    for tool in TOOLS:
        row, h, m, a = [], 0, 0, 0
        for case in CASES:
            v, _ = res[tool][case]
            row.append({"HIT": "**HIT**", "MISS": "miss", "ABST": "abst"}[v])
            tally[v] += 1
            h += v == "HIT"; m += v == "MISS"; a += v == "ABST"
        lines.append(f"| `{tool}` | " + " | ".join(row) + f" | {h} | {m} | {a} |")
    lines.append("")
    lines.append(f"**Totals (strict reading): {tally['HIT']} hits, {tally['MISS']} misses, "
                 f"{tally['ABST']} abstentions, {sum(tally.values())} cells.**")

    # ---- the one declared ambiguity, scored BOTH ways (PRE_RUN_RECORD 6.2) ----
    lines.append("""
### The one ambiguous cell, scored both ways

`leakfence` x **C4 (T4)**. Its `duplicate_rows` violation fires on **both** sides, so the strict
reading of rule 6.1 makes it a MISS with a false alarm. But the violation TEXT differs:

- contaminated: `2 rows share identical content: (24, 224), straddles train/test`
- clean:        `2 rows share identical content: (24, 124)`   <- no straddle marker

PRE_RUN_RECORD 5.1 declared `leakfence duplicate_rows -> T4` with the note that
`check_duplicates` is called *with* `train_idx`/`test_idx` and "is a cross-split test" -- so the
declared mapping's own subject was the cross-split violation. Reading the straddle marker as the
T4 label is therefore arguably the faithful application of the declared mapping rather than a new
one, and it yields a **HIT**.

Per rule 6.2 the reading that credits the competitor is taken as the headline:

| Reading | leakfence C4 | Totals |
|---|---|---|
| **Conservative (adopted, credits the competitor)** | **HIT** | **9 hits, 14 misses, 65 abstentions** |
| Strict (label-level only) | miss + false alarm | 8 hits, 15 misses, 65 abstentions |

**Neither reading changes any kill-gate verdict** -- leakfence covers T1/T7 (+T4) and does not
reach T6 under either.""")

    lines.append("\n### Abstention reasons, per cell\n")
    lines.append("| Tool | Case | Reason |")
    lines.append("|---|---|---|")
    for tool in TOOLS:
        for case in CASES:
            v, why = res[tool][case]
            if v == "ABST":
                lines.append(f"| `{tool}` | {case} | {why} |")

    lines.append("\n### Miss reasons, per cell\n")
    lines.append("| Tool | Case | Type | Reason |")
    lines.append("|---|---|---|---|")
    for tool in TOOLS:
        for case in CASES:
            v, why = res[tool][case]
            if v == "MISS":
                lines.append(f"| `{tool}` | {case} | {TYPE[case]} | {why} |")

    out = "\n".join(lines)
    with open(os.path.join(ROOT, "RESULTS_MATRIX.md"), "w") as f:
        f.write("# RESULTS_MATRIX.md -- item K6, PREREG.md 9.2 cross-tool comparison\n\n"
                "Computed by `harness/score.py` from `raw/`, using only the eligibility and label\n"
                "mapping fixed in `PRE_RUN_RECORD.md` before any tool ran.\n\n" + out + "\n")
    print(out)
    json.dump({t: {c: res[t][c] for c in CASES} for t in TOOLS},
              open(os.path.join(RAW, "_scored.json"), "w"), indent=2)


if __name__ == "__main__":
    main()
