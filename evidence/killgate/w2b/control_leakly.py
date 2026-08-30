"""W2b step 2, Leakly -- THE CONTROL, using the vendor's own pair.

R142 §1.3: WHERE A VENDOR SUPPLIES THE PAIR, USE THE PAIR. Leakly ships both
`load_example_leakage_config()` and `load_example_nonleakage_config()`, and they
differ in EXACTLY ONE DIMENSION -- where `data_split` sits in the pipeline:

    leakage    : imputation, normalization, feature_selection, data_split, model
    nonleakage : data_split, imputation, normalization, feature_selection, model

Every other key is identical. So the pair isolates preprocessing leakage and
nothing else, which is what makes it a control rather than a demonstration.

WHY THE LABELS ARE PERMUTED. Leakly is not a detector that emits a finding; it is
a pipeline runner, and leakage shows up as an inflated test score. On a dataset
with real signal, a high AUC is ambiguous -- it could be the signal. So the label
is permuted first, with the vendor's own `permute_label`. After permutation there
is NO relationship between features and label, so THE ONLY THING THAT CAN PRODUCE
AN ABOVE-CHANCE TEST SCORE IS LEAKAGE. Chance is 0.5 and it is a known constant,
not an estimate.

WHAT WOULD FALSIFY THE CONTROL, stated before it runs:
  * leaky ordering at chance      -> the tool did not fire; a null in the real run
                                     is UNINTERPRETABLE, not a clean result
  * clean ordering above chance   -> the tool fires on a clean pipeline too, so it
                                     is not discriminating and the positive proves
                                     nothing
  * both above chance             -> same; a positive control alone would have
                                     called this a success

MANY SEEDS, NOT ONE. A single AUC on 200 samples is noisy enough that one draw
could land either way by luck. The verdict is taken on the MEDIAN across seeds and
on how many seeds individually separate, so a lucky or unlucky draw cannot decide
it. Seeds are explicit integers -- never `hash()`, which PYTHONHASHSEED salts on
`str` and which would make this unreproducible across processes.

    usage: control_leakly.py [n_seeds]
"""
from __future__ import annotations

import json
import pathlib
import statistics
import sys
import time

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:                                       # noqa: BLE001
    pass

import leakly
from leakly import MLPipeline, SimulationConfig, permute_label, simulate_dataset

CHANCE = 0.5
N_SEEDS = int(sys.argv[1]) if len(sys.argv) > 1 else 7
OUT = pathlib.Path(__file__).resolve().parent / "control_leakly_result.json"

leak_cfg = leakly.load_example_leakage_config()
clean_cfg = leakly.load_example_nonleakage_config()

# The pair's difference is ASSERTED, not assumed. If a future version changes any
# other key, this control silently stops isolating pipeline order -- and would go
# on reporting a separation caused by something else.
diff = {k for k in set(leak_cfg) | set(clean_cfg)
        if leak_cfg.get(k) != clean_cfg.get(k)}
if diff != {"pipeline"}:
    sys.exit("HALT: the vendor pair differs in %s, expected {'pipeline'} alone. "
             "It no longer isolates preprocessing leakage." % sorted(diff))
print("vendor pair differs in 'pipeline' ALONE -- the control isolates split order")
print("  leaky : %s" % " -> ".join(leak_cfg["pipeline"]))
print("  clean : %s" % " -> ".join(clean_cfg["pipeline"]))
if leak_cfg["pipeline"].index("data_split") <= clean_cfg["pipeline"].index("data_split"):
    sys.exit("HALT: data_split is not later in the leakage config; the pair is "
             "not oriented the way the vendor's names claim")
print()

rows = []
for i in range(N_SEEDS):
    seed = 1000 + i * 17          # explicit, reproducible, no hash()
    sim = simulate_dataset(SimulationConfig(
        n_samples=200, n_features=100, n_covariates=3, random_state=seed))
    y_perm = permute_label(sim.y, perc_permutation=1.0, random_state=seed)

    scores = {}
    for label, cfg in (("leaky", leak_cfg), ("clean", clean_cfg)):
        t0 = time.time()
        try:
            p = MLPipeline(sim.X, y_perm, config=cfg,
                           problem_type="binary_classification").fit()
            scores[label] = float(p.evaluate(metric="auc"))
        except Exception as e:                          # noqa: BLE001
            scores[label] = None
            print("  seed %-5d %-6s RAISED %s: %s" % (seed, label, type(e).__name__, e))
        scores[label + "_s"] = round(time.time() - t0, 1)
    rows.append({"seed": seed, **scores})
    if scores["leaky"] is not None and scores["clean"] is not None:
        print("  seed %-5d leaky AUC %.3f | clean AUC %.3f | separation %+.3f"
              % (seed, scores["leaky"], scores["clean"],
                 scores["leaky"] - scores["clean"]))

ok = [r for r in rows if r["leaky"] is not None and r["clean"] is not None]
if not ok:
    sys.exit("HALT: every seed raised; the control did not run")

leaky = [r["leaky"] for r in ok]
clean = [r["clean"] for r in ok]
m_leaky, m_clean = statistics.median(leaky), statistics.median(clean)
sep = sum(1 for r in ok if r["leaky"] > r["clean"])

print()
print("=== VERDICT, on %d completed seed(s) ===" % len(ok))
print("  leaky ordering  median AUC %.3f   (chance %.1f, delta %+.3f)"
      % (m_leaky, CHANCE, m_leaky - CHANCE))
print("  clean ordering  median AUC %.3f   (chance %.1f, delta %+.3f)"
      % (m_clean, CHANCE, m_clean - CHANCE))
print("  seeds where leaky > clean: %d of %d" % (sep, len(ok)))

# The two limbs are reported SEPARATELY and neither is allowed to stand in for the
# other. A tool that fires on the positive is reachable; only the negative shows
# it is discriminating, and W2b exists because a null was once read as a clean
# result when it was really an unfired instrument.
POS = m_leaky - CHANCE > 0.05
NEG = abs(m_clean - CHANCE) <= 0.05
print()
print("  POSITIVE limb (leaky must fire)        : %s" % ("FIRES" if POS else "** DID NOT FIRE **"))
print("  NEGATIVE limb (clean must stay silent) : %s" % ("SILENT" if NEG else "** ALSO FIRES **"))

verdict = "DISCRIMINATING" if (POS and NEG) else "NOT ESTABLISHED"
print()
if verdict == "DISCRIMINATING":
    print("RESULT: DISCRIMINATING. Leakly separates the vendor's own leaky and clean "
          "pipeline orderings on permuted labels, where any above-chance score is "
          "leakage by construction. Its acceptance-fixture result is interpretable.")
else:
    print("RESULT: NOT ESTABLISHED. Until both limbs pass, Leakly's "
          "acceptance-fixture result is `uninterpretable`, NOT a null.")

OUT.write_text(json.dumps({
    "tool": "Leakly", "version": getattr(leakly, "__version__", "0.1.2"),
    "chance": CHANCE, "n_seeds": len(ok),
    "median_leaky": m_leaky, "median_clean": m_clean,
    "seeds_separating": sep, "positive_fires": POS, "negative_silent": NEG,
    "verdict": verdict, "rows": rows,
}, indent=2), encoding="utf-8")
print("\nwritten: %s" % OUT.name)
sys.exit(0 if verdict == "DISCRIMINATING" else 1)
