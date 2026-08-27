"""B-2 step 2 -- run ONE comparator against ONE side of the acceptance fixture.

Invoked once per (tool, side) through that tool's OWN virtualenv interpreter:
the six carry conflicting pandas and scikit-learn pins and none is importable
from the main interpreter. That is by design, and it is why this is a single-tool
script driven from outside rather than one process importing all six.

EVERY ADAPTER USES THE SAME INVOCATION PATH ITS CONTROL USED. A run through a
different path than the one shown to fire is a run whose null means nothing --
which is the whole thesis of W2b.

THE SHAPE LESSONS FROM STEP 2 ARE CARRIED, NOT RE-LEARNED:
  * an unrecognised return shape RAISES; it never scores as "no leakage",
    because an empty result reads as clean
  * a returned `False` is an ANSWER, not an absence
  * a raise is evidence the CALL did not happen, never evidence about the tool
  * severity/label mapping is explicit per tool, never "anything truthy"

NO SAMPLING. The frame is 338,159 x 87 and some tools may not finish. A tool that
cannot complete is recorded `could_not_run` with its reason, which maps to
`covered_with_exclusion` -- never to a pass, and never to a null.

    usage: b2_run_one.py --tool NAME --side SIDE --path P --target T [--time-col C]
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import traceback

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:                                       # noqa: BLE001
    pass

import pandas as pd

ap = argparse.ArgumentParser()
ap.add_argument("--tool", required=True)
ap.add_argument("--side", required=True)
ap.add_argument("--path", required=True)
ap.add_argument("--target", required=True)
ap.add_argument("--time-col", default="timestamp")
ap.add_argument("--out", required=True)
a = ap.parse_args()

rec = {"tool": a.tool, "side": a.side, "target": a.target,
       "time_col": a.time_col, "source": a.path}


class Unsupported(Exception):
    """The tool's question is not posed by this input, or cannot be posed here.

    Kept distinct from an adapter raise. `unsupported` and `could_not_run` are
    different facts from `observed_silence`, and none of the three is a pass --
    R146 §2.1. Collapsing them is how a tool's own limits get published as its
    subject's cleanliness.
    """


def finish(**kw):
    rec.update(kw)
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(rec, f, indent=2, default=str)
    print(json.dumps({k: rec[k] for k in ("tool", "side", "status", "summary")
                      if k in rec}, ensure_ascii=False))
    sys.exit(0)


t0 = time.time()
try:
    # CSV, NOT PARQUET. The first sweep returned could_not_run for all TWELVE
    # runs on one shared cause: none of the three comparator virtualenvs carries
    # pyarrow or fastparquet, so `read_parquet` raised before any tool was
    # reached. Twelve agreeing failures were ONE failure -- the population was
    # the harness, not the tools.
    #
    # Installing a parquet engine into the venvs was refused: the W2b inventory
    # pinned their versions on 14 Aug 2026 BEFORE any result was read, and adding
    # packages would alter the environment the record attests. The inputs are
    # written as CSV instead, which every venv can read unaided.
    df = pd.read_csv(a.path, low_memory=False)
    rec["rows"], rec["cols"] = int(df.shape[0]), int(df.shape[1])
except Exception as e:                                  # noqa: BLE001
    finish(status="could_not_run", reason="input_unreadable",
           detail="%s: %s" % (type(e).__name__, e), seconds=round(time.time() - t0, 1))

# The target must exist and must not be all-null, or every downstream verdict is
# about an empty column rather than about leakage.
if a.target not in df.columns:
    finish(status="could_not_run", reason="target_absent",
           detail="%r not among %d columns" % (a.target, df.shape[1]),
           seconds=round(time.time() - t0, 1))
if df[a.target].notna().sum() == 0:
    finish(status="could_not_run", reason="target_all_null",
           detail="the target column is entirely null",
           seconds=round(time.time() - t0, 1))


def run_leakage_buster():
    import leakage_buster.api as api
    r = api.audit(df, target=a.target, time_col=a.time_col)
    data = getattr(r, "data", None)
    if not isinstance(data, dict):
        raise TypeError("AuditResult.data is %s" % type(data).__name__)
    risks = data.get("risks")
    if not isinstance(risks, list):
        raise TypeError("'risks' is %s" % type(risks).__name__)
    high = [x for x in risks if str(x.get("severity", "")).lower() == "high"]
    return {"n_risks": len(risks), "n_high": len(high),
            "high": [x.get("name") for x in high],
            "all": [x.get("name") for x in risks],
            "finding": bool(high),
            "mapping": "severity == 'high' is a leakage finding; medium/low are advisory"}


def run_leakfence():
    import leakfence
    n = len(df)
    cut = int(n * 0.8)
    tr, te = list(range(cut)), list(range(cut, n))
    rep = leakfence.audit_split(train_idx=tr, test_idx=te)
    v = list(getattr(rep, "violations", None) or [])
    dup = leakfence.check_duplicates(df.select_dtypes("number").to_numpy(),
                                     train_idx=tr, test_idx=te)
    dv = dup[-1] if isinstance(dup, tuple) else (dup if isinstance(dup, list) else None)
    if dv is None:
        raise TypeError("check_duplicates returned %s" % type(dup).__name__)
    names = [getattr(x, "check", str(x)) for x in v] + \
            [getattr(x, "check", str(x)) for x in dv]
    return {"split": "chronological 80/20 by row order",
            "n_violations": len(names), "violations": names,
            "finding": bool(names),
            "mapping": "a non-empty Violation list is a finding"}


def run_temporalcv():
    from temporalcv.gates import GateStatus, gate_suspicious_improvement
    import numpy as np
    y = pd.to_numeric(df[a.target], errors="coerce").to_numpy()
    ok = ~np.isnan(y)
    y = y[ok]
    if len(y) < 100:
        raise ValueError("only %d usable target rows" % len(y))
    cut = int(len(y) * 0.8)
    # PERSISTENCE BASELINE vs THE MEAN PREDICTOR, both as MAE -- an ERROR metric,
    # which is what the gate's formula expects. Feeding an accuracy is defect #7.
    base = float(np.mean(np.abs(y[cut + 1:] - y[cut:-1])))
    model = float(np.mean(np.abs(y[cut + 1:] - np.mean(y[:cut]))))
    r = gate_suspicious_improvement(model, base, metric_name="MAE")
    st = r.status.name if isinstance(r.status, GateStatus) else str(r.status)
    return {"model_mae": model, "baseline_mae": base,
            "improvement_ratio": r.details.get("improvement_ratio"),
            "status": st, "message": r.message,
            "finding": st == "HALT",
            "mapping": "GateStatus.HALT on an ERROR metric is a finding"}


def run_leakly():
    """UNSUPPORTED, and the reason is about the QUESTION, not the plumbing.

    Leakly detects preprocessing leakage by comparing two PIPELINE ORDERINGS --
    where `data_split` sits relative to imputation, scaling and feature
    selection. The acceptance fixture is a built feature table; it has no
    pipeline whose ordering can be varied. **The tool's question is not asked by
    this artefact at all**, which is `unsupported`, not a null and not a miss.
    """
    import leakly
    raise Unsupported(
        "Leakly detects by varying pipeline ORDER (where data_split sits); the "
        "acceptance fixture is a built table with no pipeline to reorder, so the "
        "tool's question is not posed by this input. Version %s."
        % getattr(leakly, "__version__", "?"))


def run_leak_detect():
    """COULD_NOT_RUN(compatibility) -- applicable in principle, blocked in fact.

    leak-detect instruments a data-creation FUNCTION by NaN propagation, and
    `fixture_adapter.builder_for(inputs, side)` is exactly such a function -- this
    is the one tool whose mechanism matches the fixture's shape directly. It
    cannot be pointed at it here: leak-detect lives in the `ld` virtualenv, whose
    pandas pin differs from the one the builder requires, so the builder cannot be
    imported alongside it.

    That is a COMPATIBILITY limit of this harness, not a property of the tool, and
    it is recorded as such -- `covered_with_exclusion`, never a pass. Closing it
    would mean running the builder in `ld`, which the pins forbid, or serving the
    builder across a process boundary, which nobody has asked for.
    """
    raise Unsupported(
        "applicable in principle -- builder_for() is a data-creation function of "
        "exactly the kind leak-detect instruments -- but the `ld` venv's pandas "
        "pin cannot import the fixture builder. could_not_run(compatibility).")


def run_deepchecks():
    from deepchecks.tabular import Dataset
    from deepchecks.tabular.checks import FeatureLabelCorrelation
    d = df.drop(columns=[c for c in (a.time_col,) if c in df.columns])
    d = d.select_dtypes(include=["number"]).copy()
    if a.target not in d.columns:
        d[a.target] = pd.to_numeric(df[a.target], errors="coerce")
    d = d.dropna(subset=[a.target])
    ds = Dataset(d, label=a.target)
    r = FeatureLabelCorrelation().run(dataset=ds)
    v = r.value
    if isinstance(v, dict):
        top = sorted(v.items(), key=lambda kv: -(kv[1] or 0))[:8]
    elif isinstance(v, pd.Series):
        top = list(v.sort_values(ascending=False).head(8).items())
    else:
        raise TypeError("CheckResult.value is %s" % type(v).__name__)
    worst = float(top[0][1]) if top else 0.0
    return {"top_pps": [[str(k), float(x)] for k, x in top], "max_pps": worst,
            "finding": worst > 0.5,
            "mapping": "predictive-power score > 0.5 for any single feature"}


RUNNERS = {"leakage-buster": run_leakage_buster, "leakfence": run_leakfence,
           "temporalcv": run_temporalcv, "Leakly": run_leakly,
           "leak-detect": run_leak_detect, "deepchecks": run_deepchecks}

fn = RUNNERS.get(a.tool)
if fn is None:
    finish(status="could_not_run", reason="unknown_tool",
           detail="no adapter for %r" % a.tool, seconds=0)

try:
    out = fn()
    finish(status="ran", result=out,
           summary="finding=%s" % out.get("finding"),
           seconds=round(time.time() - t0, 1))
except Unsupported as e:
    # NOT a pass, NOT a null, NOT an adapter defect. The tool's question is not
    # posed by this input; §9.2 maps this to `covered_with_exclusion`.
    finish(status="unsupported", reason="question_not_posed_by_input",
           detail=str(e), seconds=round(time.time() - t0, 1))
except Exception as e:                                  # noqa: BLE001
    finish(status="could_not_run", reason="adapter_raised",
           detail="%s: %s" % (type(e).__name__, str(e)[:400]),
           traceback=traceback.format_exc()[-1200:],
           seconds=round(time.time() - t0, 1))
