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
import pathlib
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
    # DATETIME COLUMNS ARE RESTORED FROM A SIDECAR WRITTEN OFF THE PARQUET.
    # The CSV round-trip turns `timestamp` and `ts_floor` into strings, and
    # leakage-buster -- handed `time_col="timestamp"` -- reported "Time parse
    # errors" for exactly that reason. A verdict that hinges on a dtype the
    # transport changed is a verdict about the transport. The column list is
    # DERIVED from the parquet, never hardcoded here.
    side = pathlib.Path(a.path).with_suffix(".dtypes.json")
    if side.exists():
        spec = json.loads(side.read_text(encoding="utf-8"))
        for c in spec.get("datetime_columns", []):
            if c in df.columns:
                df[c] = pd.to_datetime(df[c], errors="coerce")
        rec["restored_datetime_columns"] = spec.get("datetime_columns", [])
    else:
        rec["restored_datetime_columns"] = None      # reported, never silent
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
    """R148 §1.3 -- the tool's best shot.

    The first sweep handed it the frame whole and its `target_leakage` detector
    errored with "Input y contains NaN": `fwd_move_ticks_5s` is forward-looking,
    so the tail rows have no label. **Rows with no target are dropped**, which is
    ordinary preparation rather than a favour -- a row with no label cannot be
    audited for label leakage, and leaving them in silenced the one detector that
    matters. The count dropped is reported, because a comparison run on a
    different row set than it claims is a different comparison.
    """
    import leakage_buster.api as api
    n0 = len(df)
    # COMPLETE-CASE ON ALL 87 COLUMNS. NO FEATURE IS REMOVED.
    #
    # Dropping only target-nulls left "Input X contains NaN" -- the detector is
    # LinearRegression-based and takes neither. The obvious shortcut is to drop
    # the offending columns (`vwap_distance` alone carries 243,000 NaNs, and 66
    # of 87 columns are NaN-free), and it is REFUSED: dropping a feature could
    # drop the leaky one, and a comparison won by removing the evidence is the
    # starving §1.3 forbids.
    #
    # So every column is kept and incomplete rows go: 95,159 of 338,159 survive.
    # That is a real reduction and it is reported, not buried -- a correlation
    # detector has ample rows at 95k, but the row set is no longer the fixture's
    # full population and any verdict is about the complete-case subset.
    d = df.dropna()
    if d.empty:
        raise ValueError("complete-case filtering left no rows")
    r = api.audit(d, target=a.target, time_col=a.time_col)
    data = getattr(r, "data", None)
    if not isinstance(data, dict):
        raise TypeError("AuditResult.data is %s" % type(data).__name__)
    risks = data.get("risks")
    if not isinstance(risks, list):
        raise TypeError("'risks' is %s" % type(risks).__name__)
    high = [x for x in risks if str(x.get("severity", "")).lower() == "high"]
    # A RISK NAMED "Detector error: ..." IS A could_not_run FOR THAT DETECTOR,
    # NOT AN ABSENCE. The first sweep folded it into a severity count and
    # reported finding=False -- the one detector that would have found target
    # leakage had ERRORED, and nothing said so. Errors are separated out and the
    # verdict refuses to be a clean null while any detector is broken.
    errs = [x for x in risks if str(x.get("name", "")).lower().startswith("detector error")]
    return {"rows_in": n0, "rows_audited": len(d), "rows_dropped_incomplete": n0 - len(d),
            "n_risks": len(risks), "n_high": len(high),
            "high": [x.get("name") for x in high],
            "all": [x.get("name") for x in risks],
            "detector_errors": [{"name": x.get("name"), "detail": str(x.get("detail"))[:400],
                                 "evidence": str(x.get("evidence"))[:400]} for x in errs],
            "finding": None if errs else bool(high),
            "mapping": "severity == 'high' is a leakage finding; medium/low are "
                       "advisory. ANY 'Detector error' makes the verdict None -- "
                       "could_not_run for that detector, never a clean null."}


def run_leakfence():
    """R148 §1.3 -- `audit_split` WITH a subject, so the group check arms.

    The first sweep called it with train/test indices and nothing else. Its own
    docstring says "subject: per-window subject id. **Omit to skip the group
    check**" -- so the check never ran and the zero violations were vacuous.

    THE SUBJECT IS `ts_floor`, the fixture's own time bucket. Rows sharing a
    `ts_floor` are the same bucket, so a chronological split that puts one bucket
    on both sides of the cut IS the overlap this check exists to find. That is
    the fixture's real grouping, not one invented to make the tool fire.
    """
    import leakfence
    n = len(df)
    cut = int(n * 0.8)
    tr, te = list(range(cut)), list(range(cut, n))
    # A DEGENERATE SUBJECT ARMS NOTHING. Supplying `ts_floor` made
    # `n_subject_values` equal the ROW COUNT: it is unique per row, so every row
    # is its own group and a group-overlap check can never fire. That is a
    # SECOND vacuous zero wearing the first one's fix -- the check was armed in
    # form and dead in substance.
    #
    # Both candidates are one-group-per-row (338,159 distinct of 338,159 rows),
    # so THIS FIXTURE HAS NO SUBJECT GROUPING and the group check is UNPOSABLE
    # on it. Coarsening the timestamp into buckets would manufacture a grouping
    # the fixture does not have, purely to make the tool produce a number.
    #
    # The group check is therefore recorded unposable, and `check_duplicates` --
    # which needs no grouping -- still runs and still answers.
    subj, subj_col, group_state = None, None, None
    for cand in ("ts_floor", "timestamp"):
        if cand in df.columns:
            vals = df[cand].astype(str)
            if vals.nunique() < len(vals):
                subj, subj_col = vals.tolist(), cand
            else:
                group_state = ("unposable: %s is unique per row (%d of %d), so "
                               "every row is its own group" % (cand, vals.nunique(), len(vals)))
            break
    if subj is not None:
        rep = leakfence.audit_split(train_idx=tr, test_idx=te, subject=subj)
        group_state = "armed on %s (%d groups)" % (subj_col, len(set(subj)))
        v = list(getattr(rep, "violations", None) or [])
    else:
        v = []
    dup = leakfence.check_duplicates(df.select_dtypes("number").to_numpy(),
                                     train_idx=tr, test_idx=te)
    dv = dup[-1] if isinstance(dup, tuple) else (dup if isinstance(dup, list) else None)
    if dv is None:
        raise TypeError("check_duplicates returned %s" % type(dup).__name__)
    names = [getattr(x, "check", str(x)) for x in v] + \
            [getattr(x, "check", str(x)) for x in dv]
    return {"split": "chronological 80/20 by row order",
            "group_check": group_state,
            "duplicate_check": "ran on %d numeric columns" % df.select_dtypes("number").shape[1],
            "n_violations": len(names), "violations": names,
            "finding": bool(names),
            "mapping": "a non-empty Violation list is a finding. The GROUP check "
                       "is unposable on this fixture (no subject grouping exists) "
                       "and contributes NO evidence either way; the DUPLICATE "
                       "check ran and its zero is a real result."}


def run_temporalcv():
    """R148 §1.3 -- pose the question the gate was built for.

    The first sweep compared a MEAN PREDICTOR against persistence. That measures
    whether a trivial constant beats persistence; it contains no leakage question
    at all, and its -111% "improvement" was about the mean, not the fixture.

    THE REAL QUESTION, and the shape the tool's own fired control used: fit a
    MODEL ON THE FEATURES, forecast the target, and compare its error against the
    persistence baseline. If a side leaks, the model's error collapses and the
    improvement over persistence becomes implausible -- which is exactly what
    `gate_suspicious_improvement` exists to flag. Fed as MAE, an ERROR metric;
    feeding an accuracy is defect #7 and is what made k6's gate unable to fire.

    Chronological 80/20, fit on train only, scored on test only.
    """
    from temporalcv.gates import GateStatus, gate_suspicious_improvement
    from sklearn.linear_model import Ridge
    import numpy as np

    d = df.dropna()
    if len(d) < 1000:
        raise ValueError("only %d complete rows; too few to fit" % len(d))
    feat = [c for c in d.columns
            if c != a.target and pd.api.types.is_numeric_dtype(d[c])
            and not c.startswith("fwd_move_ticks")]
    X = d[feat].to_numpy(dtype=float)
    y = d[a.target].to_numpy(dtype=float)
    cut = int(len(d) * 0.8)
    # PERSISTENCE: the previous row's target, the baseline the gate documents.
    base = float(np.mean(np.abs(y[cut:] - np.concatenate([[y[cut - 1]], y[cut:-1]]))))

    # THE GATE DECLARES ITS OWN DOMAIN, because B-3 found it firing on a clean
    # series. `gate_suspicious_improvement` assumes PERSISTENCE IS A STRONG
    # BASELINE -- true for near-unit-root forecasting, which is what it was built
    # for. On an iid or mean-reverting target the MEAN PREDICTOR ALONE beats
    # persistence by ~29% (E|y-mu| = 0.798σ against E|y_t - y_t-1| = 1.128σ),
    # which trips a 20% threshold with no leakage present at all.
    #
    # So the precondition is measured before the gate is consulted: if the mean
    # predictor already beats persistence past the gate's own threshold, any
    # HALT is arithmetic rather than evidence, and the tool is UNSUPPORTED on
    # this target rather than firing spuriously.
    meanpred = float(np.mean(np.abs(y[cut:] - y[:cut].mean())))
    precondition = 1.0 - meanpred / base if base > 0 else float("nan")
    if precondition > 0.20:
        raise Unsupported(
            "persistence is not a strong baseline for this target: the mean "
            "predictor alone beats it by %+.3f, past the gate's own 0.20 "
            "threshold, so any HALT would be arithmetic and not evidence "
            "(lag-1 autocorrelation too low for the gate's forecasting regime)"
            % precondition)

    m = Ridge(alpha=1.0).fit(X[:cut], y[:cut])
    pred = m.predict(X[cut:])
    model = float(np.mean(np.abs(y[cut:] - pred)))
    r = gate_suspicious_improvement(model, base, metric_name="MAE")
    st = r.status.name if isinstance(r.status, GateStatus) else str(r.status)
    return {"n_features": len(feat), "rows_fit": cut, "rows_scored": len(d) - cut,
            "precondition_mean_vs_persistence": precondition,
            "model_mae": model, "baseline_mae": base,
            "improvement_ratio": r.details.get("improvement_ratio"),
            "status": st, "message": r.message,
            "finding": st == "HALT",
            "mapping": "GateStatus.HALT on an ERROR metric is a finding. Other "
                       "fwd_move_ticks_* columns are EXCLUDED from features -- "
                       "they are sibling targets, and leaving them in would "
                       "manufacture leakage the fixture did not put there"}


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
