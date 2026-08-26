"""Run Leakly 0.1.2 against its eligible cases (C2, C3, C5, C6 per PRE_RUN_RECORD 4.7).

Leakly's documented mechanism is a permutation test over an ML pipeline whose STAGE ORDER the
user declares. Its own `load_example_leakage_config()` differs from
`load_example_nonleakage_config()` in exactly one respect:

    leakage    : ['imputation','normalization','feature_selection','data_split','model']
    nonleakage : ['data_split','imputation','normalization','feature_selection','model']

i.e. whether preprocessing and selection are fitted before or after the split.

FIRING RULE, DECLARED BEFORE LEAKLY WAS RUN ON ANY CASE
-------------------------------------------------------
Leakly signals leakage when a pipeline still performs ABOVE CHANCE on PERMUTED labels -- if the
split came after selection, the selection saw the labels and the advantage survives permutation.

    fired  <=>  one-sided t-test of {permuted-label AUCs} > 0.5 is significant at alpha = 0.05

n_permutations = 25, random_state = 0. No other threshold is used, and this one is fixed here.

ADAPTER, judged SETUP (CROSS_TOOL_COMPARISON 2.6 item 4):
  - C2/C3 are cases ABOUT pipeline construction, so the side is expressed in Leakly's own stage
    order -- contaminated = split last, clean = split first. Same content, tool's input form.
  - C5/C6 are cases about the DATA, so both sides use the non-leaking stage order and only the
    feature matrix differs. Encoding the answer in the config would be a case modification.
"""
import json
import os
import sys
import traceback
import warnings

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.abspath(os.path.join(HERE, "..", "raw"))

import numpy as np  # noqa: E402
from scipy import stats as sps  # noqa: E402

import case_defs as cd  # noqa: E402
import leakly  # noqa: E402
from leakly import MLPipeline, permute_label  # noqa: E402

N_PERM = 25
ALPHA = 0.05
PIPELINE_IS_THE_CASE = {"C2", "C3"}   # side expressed as stage order
DATA_IS_THE_CASE = {"C5", "C6"}       # side expressed as the feature matrix


def config_for(case, side):
    if case in PIPELINE_IS_THE_CASE and side == "contaminated":
        return leakly.load_example_leakage_config()
    return leakly.load_example_nonleakage_config()


def one(case, side):
    d = cd.get(case, side)
    m = d["meta"]
    full = d["full"].dropna().reset_index(drop=True)
    X = full[m["features"]].to_numpy(dtype=float)
    y = full[m["target"]].to_numpy().astype(int)
    cfg = config_for(case, side)
    rec = dict(tool="Leakly", version="0.1.2", case=case, side=side,
               config=dict(pipeline_order=cfg["pipeline"], n_permutations=N_PERM,
                           alpha=ALPHA, metric="auc", random_state=0,
                           firing_rule="one-sided t-test of permuted-label AUCs > 0.5"))
    try:
        p = MLPipeline(X, y, config=cfg).fit()
        observed = float(p.evaluate())
        null = []
        for i in range(N_PERM):
            yp = permute_label(y, random_state=i)
            null.append(float(MLPipeline(X, np.asarray(yp).astype(int),
                                         config=cfg).fit().evaluate()))
        null = np.asarray(null, dtype=float)
        t, pv_two = sps.ttest_1samp(null, 0.5)
        pval = pv_two / 2 if t > 0 else 1 - pv_two / 2
        fired = bool(pval < ALPHA)
        rec.update(status="ran", fired=fired,
                   observed_auc=observed, permuted_auc_mean=float(null.mean()),
                   permuted_auc_std=float(null.std()), p_value=float(pval),
                   fired_labels=["Leakly permutation verdict"] if fired else [])
    except Exception as e:
        rec.update(status="crash", error=f"{type(e).__name__}: {e}",
                   traceback=traceback.format_exc()[-1200:])
    return rec


def main():
    recs = []
    for case in ["C2", "C3", "C5", "C6"]:
        for side in cd.SIDES:
            r = one(case, side)
            recs.append(r)
            print(f"  LY {case} {side:13s} {r['status']:5s} fired={r.get('fired')} "
                  f"obs={r.get('observed_auc')} perm_mean={r.get('permuted_auc_mean')} "
                  f"p={r.get('p_value')}" + (f" ERR={r.get('error','')[:60]}"
                                             if r["status"] == "crash" else ""))
    with open(os.path.join(OUT, "Leakly.json"), "w") as f:
        json.dump(recs, f, indent=2)


if __name__ == "__main__":
    main()
