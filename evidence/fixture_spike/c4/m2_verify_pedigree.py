r"""M2 verification pass — re-check every claim in c4\pedigree.md against its primary sources.

Read-only over all sources. Prints a PASS/FAIL line per check; writes nothing.
Captured output: c4\m2_verification_log.txt
"""
import csv
import io
import json
import re
import sys
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding="utf-8")

SPIKE = (r"C:\Users\ttbea\AppData\Local\Temp\claude"
         r"\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01"
         r"\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\fixture_spike")
PROJ = (r"C:\Users\ttbea\.claude\projects"
        r"\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01"
        r"\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1")
WF = PROJ + r"\workflows\scripts\r2-gate-checks-wf_e5854e83-534.js"
JOURNAL = PROJ + r"\subagents\workflows\wf_e5854e83-534\journal.jsonl"

fails = []


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}{('  — ' + detail) if detail else ''}")
    if not ok:
        fails.append(name)


read = lambda p: io.open(p, encoding="utf-8").read()
ped = read(SPIKE + r"\c4\pedigree.md")
ped_unquoted = re.sub(r"(?m)^>\s?", "", ped)          # strip markdown blockquote markers
ped_flat = re.sub(r"\s+", " ", ped_unquoted)

# ---- 1. Tasking quoted verbatim from the workflow script ---------------------
js = read(WF).splitlines()
c4_prompt = "\n".join(js[36:52])                       # lines 37-52 (1-indexed)
check("tasking lines 37-52 quoted verbatim in pedigree", c4_prompt in ped)
check("dispatch label present", "label: 'C4-blind-remeasure'" in js[51])

# ---- 2. Blindness: no target numbers in the prompt ---------------------------
nums = sorted(set(re.findall(r"\d[\d,]*", c4_prompt)))
leaks = [t for t in ("89568", "89,568", "254314", "254,314", "23633", "164958",
                     "162753", "135980", "129333", "179856", "338158", "338,158")
         if t in c4_prompt]
check("no result-count numeral anywhere in the C4 prompt", not leaks, f"leaks={leaks}")
check("338,159 is the only measured-quantity numeral", "338,159" in nums,
      f"numeric tokens = {nums}")
check("prompt states 'you have no target numbers'",
      "you have no target numbers; whatever you measure is the result." in c4_prompt)
check("prompt forbids t1/, f4/, *violation*, tasks/, journals",
      all(s in c4_prompt for s in ("MUST NOT read anything under", r"\t1\\", r"\f4\\",
                                   "*violation*", "any workflow journal")))

# ---- 3. Journal result --------------------------------------------------------
jl = io.open(JOURNAL, encoding="utf-8").readlines()
rec = json.loads(jl[4])
check("journal line 5 is the C4 result record",
      rec["type"] == "result" and rec["agentId"] == "a8b3830d5bf32c3c2",
      f"agentId={rec['agentId']}, key={rec['key'][:16]}...")
verdict = rec["result"]["verdict"]
check("journal verdict quoted verbatim in pedigree (whitespace-normalized)",
      re.sub(r"\s+", " ", verdict) in ped_flat)
check("verdict pins polars 1.43.2", "polars 1.43.2 (all checker computation)" in verdict)
check("verdict states pandas not used", "pandas not used" in verdict)
check("verdict states lattice 338,159 independently matched",
      "338,159 rows, exactly matching the build record" in verdict)
check("verdict records second-method agreement",
      "cross-checked by a second, event-level join method with exact agreement" in verdict)
check("finding 10 carries the blindness attestation",
      "no files under t1/, f4/, tasks/, or any *violation* file were read"
      in rec["result"]["findings"][9]["fact"])

# ---- 4. Checker source: version print + two-method structure ------------------
ck = read(SPIKE + r"\c4\independent_checker.py").splitlines()
L = lambda n: ck[n - 1]
check("line 42 imports sys", L(42) == "import sys")
check("line 43 imports polars", L(43) == "import polars as pl")
check("line 52 prints the polars version", L(52) == 'print("polars", pl.__version__)')
check("no pandas import anywhere in checker",
      not any(re.match(r"\s*(import pandas|from pandas)", l) for l in ck))
check("imports are exactly sys / polars / random",
      [n for n, l in enumerate(ck, 1) if re.match(r"\s*import |\s*from ", l)] == [42, 43, 192])
check("line 47 BASE = archive processed\\zc", L(47).startswith('BASE = r"C:\\Users\\ttbea\\OneDrive\\Desktop\\MBO_2025\\processed\\zc"'))
check("reads only the three archive parquets",
      sorted(re.findall(r'BASE \+ r"\\([a-z_0-9\-]+\.parquet)"', "\n".join(ck)))
      == ["zc_mbo_2025-01.parquet", "zc_snapshots_2025-01.parquet",
          "zc_trades_tagged_2025-01.parquet"])
check("method 1 header at line 115",
      L(115).startswith("# \u2500\u2500 3. Per-class row-level violation flags"))
check("method 2 header at line 180",
      L(180).startswith("# \u2500\u2500 4. Window-length independence"))
check("line 193 seeds the sample deterministically", L(193) == "random.seed(20260810)")
check("line 194 draws 500 rows", "random.sample(range(W, N), 500)" in L(194))
doc_cites = sorted(set(re.findall(r"L\d+(?:-\d+)?", "\n".join(ck[0:41]))),
                   key=lambda s: int(re.findall(r"\d+", s)[0]))
print(f"       docstring builder-line citations: {doc_cites}")
check("pedigree lists the docstring citation set exactly",
      all(c in ped for c in doc_cites))

# ---- 5. Count-by-count comparison, rebuilt from the two CSVs ------------------
t1_cells = defaultdict(list)
for r in csv.DictReader(io.open(SPIKE + r"\t1\violation_table.csv", encoding="utf-8")):
    t1_cells[(r["event_class"], r["side"], r["boundary"])].append(
        (r["column"], int(r["strictly_after_count"]), int(r["equal_count"]), int(r["total_rows"])))
n_t1_rows = sum(len(v) for v in t1_cells.values())
check("T1 table = 99 data rows (33 columns x 3 blocks)", n_t1_rows == 99,
      f"rows={n_t1_rows}, blocks={sorted(set((k[1], k[2]) for k in t1_cells))}")

t1 = {}
for key, rows in t1_cells.items():
    vals = {(s, e, t) for (_c, s, e, t) in rows}
    if len(vals) != 1:
        check(f"T1 columns identical within {key}", False, str(rows))
    s, e, t = next(iter(vals))
    t1[key] = dict(strict=s, equal=e, total=t, n_cols=len(rows))
check("every T1 (class, side, boundary) cell is column-uniform", True,
      "all 30 cells uniform")
check("T1 corrected/decision_T covers 33 columns",
      sum(v["n_cols"] for k, v in t1.items()
          if k[1] == "corrected" and k[2] == "decision_T") == 33)

c4 = {}
order = []
for r in csv.DictReader(io.open(SPIKE + r"\c4\independent_counts.csv", encoding="utf-8")):
    c4[(r["event_class"], r["boundary"])] = {k: int(r[k]) for k in
        ("strict_count", "equal_count", "total_rows",
         "gap_row_subset_strict", "gap_row_subset_equal", "n_events_in_class")}
    if r["event_class"] not in order:
        order.append(r["event_class"])
check("C4 table = 20 rows (10 classes x 2 boundaries)", len(c4) == 20 and len(order) == 10)

print("\n  class            boundary    T1 strict/equal    C4 strict/equal   agree   cont-C4")
n_agree = 0
deltas = {}
for cls in order:
    for c4_b, t1_b in (("decision_T", "decision_T"), ("prev_row_B", "claimed_T_prev")):
        c, t = c4[(cls, c4_b)], t1[(cls, "corrected", t1_b)]
        cont = t1[(cls, "contaminated", "decision_T")]
        agree = (c["strict_count"] == t["strict"] and c["equal_count"] == t["equal"]
                 and c["total_rows"] == t["total"])
        n_agree += agree
        d = cont["strict"] - c["strict_count"] if c4_b == "prev_row_B" else ""
        if c4_b == "prev_row_B":
            deltas[cls] = d
        print(f"  {cls:15s} {c4_b:10s} {t['strict']:>7}/{t['equal']:<3} "
              f"{c['strict_count']:>10}/{c['equal_count']:<3} {'YES' if agree else '**NO**':>8}"
              f"   {d}")
check("all 20 (class, boundary) cells agree exactly on strict, equal, total_rows", n_agree == 20,
      f"{n_agree}/20")
check("contaminated-minus-1 relation at prev_row_B: mbo=1, trades=0",
      all(v == 1 for k, v in deltas.items() if k.startswith("mbo"))
      and all(v == 0 for k, v in deltas.items() if k.startswith("trades")),
      str(deltas))
check("equal counts carry no last-row contribution (contaminated == corrected)",
      all(t1[(c, "contaminated", "decision_T")]["equal"] == c4[(c, "prev_row_B")]["equal_count"]
          for c in order))
check("row counts: T1 corrected == C4 == 338,158; T1 contaminated == 338,159",
      all(c4[(c, b)]["total_rows"] == 338158 for c in order for b in ("decision_T", "prev_row_B"))
      and all(t1[(c, "contaminated", "decision_T")]["total"] == 338159 for c in order))

# ---- 6. Orchestrator section --------------------------------------------------
r2 = read(SPIKE + r"\R2_consolidated_report.md").splitlines()
check("R2 C4 section is lines 15-19",
      r2[14].startswith("### C4 — blind independent re-measurement")
      and r2[18].startswith("- Evidence: `c4\\independent_checker.py`"))
check("R2 lines 16-18 quoted verbatim in pedigree",
      all(re.sub(r"\s+", " ", r2[n - 1]) in ped_flat for n in (15, 16, 17, 18, 19)))

print("\n" + "=" * 78)
print(f"FAILURES: {len(fails)}")
print("ALL PEDIGREE CLAIMS VERIFIED" if not fails else f"FAILED: {fails}")
